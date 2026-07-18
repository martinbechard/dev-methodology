#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Runs bounded, identity-gated conceptual-agent suites in disposable Codex workspaces.
# Governing design: evals/agent-tests/implementation-plan.md
# Governing test plan: evals/agent-tests/test_runner.py

from __future__ import annotations

import argparse
import contextlib
import dataclasses
import datetime as dt
import hashlib
import json
import os
import re
import secrets
import shlex
import signal
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import tomllib
from collections.abc import Callable, Iterator, Sequence
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import yaml


_SUITE_ROOT = Path(__file__).resolve().parent
_REPOSITORY_ROOT = _SUITE_ROOT.parents[1]
_RUNTIME_NAME = re.compile(r"^[a-z][a-z0-9_]*$")
_TERMINAL_STATUSES = frozenset({"PASS", "FAIL", "BLOCKED", "STALE"})
_REPORT_STATUSES = frozenset((*_TERMINAL_STATUSES, "INFRASTRUCTURE_FAILED"))
_EXECUTABLE_STATUSES = frozenset({"executable", "fixture-backed"})
_RUNTIME_CAPABILITIES = frozenset(
    {
        "browser-automation",
        "child-process-inspection",
        "loopback",
        "offline-maven-repository",
        "offline-node-modules",
    }
)
_ISOLATED_RUNTIME_CAPABILITIES = frozenset(
    {"browser-automation", "child-process-inspection", "loopback"}
)
_CAPTURE_REPLACEMENTS = (
    ("Martin.Bechard@DevConsult.ca", "[REDACTED-NONBEHAVIORAL-IDENTITY]"),
)
_MAXIMUM_CAPTURE_BYTES = 10 * 1024 * 1024


@dataclasses.dataclass(frozen=True)
class _Suite:
    suite_id: str
    priority: int
    path: Path
    manifest: dict[str, Any]
    scenarios: tuple[dict[str, Any], ...]


@dataclasses.dataclass(frozen=True)
class _RunSpec:
    suite: _Suite
    scenario_ids: tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class _StagedAgent:
    invocation: str
    source: Path
    developer_instructions: str
    sha256: str
    instruction_marker: str


@dataclasses.dataclass(frozen=True)
class _Session:
    session_id: str
    parent_thread_id: str | None
    invocation: str | None
    depth: int
    started_at: float
    finished_at: float
    instruction_markers: frozenset[str]


def _utc_now() -> str:
    return dt.datetime.now(dt.UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_yaml(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"Expected a YAML mapping in {path}")
    return loaded


def _load_catalog(
    suite_root: Path = _SUITE_ROOT,
    include_ids: set[str] | None = None,
) -> dict[str, _Suite]:
    index = _load_yaml(suite_root / "suite-index.yaml")
    entries = index.get("suites", [])
    available_ids = {str(entry["id"]) for entry in entries}
    if include_ids is not None:
        unknown = include_ids - available_ids
        if unknown:
            raise ValueError(f"Unknown suites: {', '.join(sorted(unknown))}")
    suites: dict[str, _Suite] = {}
    for entry in entries:
        suite_id = str(entry["id"])
        if include_ids is not None and suite_id not in include_ids:
            continue
        suite_path = suite_root / str(entry["path"])
        manifest = _load_yaml(suite_path / "suite.yaml")
        scenario_document = _load_yaml(suite_path / "scenarios.yaml")
        suite = _Suite(
            suite_id=suite_id,
            priority=int(entry["priority"]),
            path=suite_path,
            manifest=manifest,
            scenarios=tuple(scenario_document.get("scenarios", [])),
        )
        _validate_suite(suite, require_executable=False)
        if suite_id in suites:
            raise ValueError(f"Duplicate suite id: {suite_id}")
        suites[suite_id] = suite
    if not suites:
        raise ValueError("The suite index contains no suites")
    return suites


def _validate_suite(suite: _Suite, require_executable: bool = True) -> None:
    manifest = suite.manifest
    execution = manifest.get("execution", {})
    target = manifest.get("target", {})
    if manifest.get("id") != suite.suite_id:
        raise ValueError(f"Suite id mismatch for {suite.suite_id}")
    if execution.get("scenarioCatalog") != "scenarios.yaml":
        raise ValueError(f"{suite.suite_id} must use scenarios.yaml")
    if execution.get("maximumActiveChildren") != 1:
        raise ValueError(f"{suite.suite_id} maximumActiveChildren must be 1")
    nested_limit = int(execution.get("nestedAgentLimit", 0))
    if nested_limit not in (0, 1):
        raise ValueError(f"{suite.suite_id} nestedAgentLimit must be 0 or 1")
    if nested_limit == 1 and not target.get("allowedAgentDependencies"):
        raise ValueError(f"{suite.suite_id} declares a nested child without an allowed dependency")
    for field in ("supervisorInvocation", "targetInvocation", "judgeInvocation"):
        invocation = str(execution.get(field, ""))
        if not _RUNTIME_NAME.fullmatch(invocation):
            raise ValueError(f"{suite.suite_id} has an invalid {field}: {invocation}")
    if len(suite.scenarios) < 3:
        raise ValueError(f"{suite.suite_id} requires at least three scenarios")
    scenario_ids: set[str] = set()
    for scenario in suite.scenarios:
        scenario_id = str(scenario.get("id", ""))
        if not scenario_id or scenario_id in scenario_ids:
            raise ValueError(f"{suite.suite_id} has a missing or duplicate scenario id")
        scenario_ids.add(scenario_id)
        if require_executable and scenario.get("status") not in _EXECUTABLE_STATUSES:
            raise ValueError(f"{suite.suite_id}:{scenario_id} is not executable")
        executable_case = scenario.get("executableCase")
        if require_executable and (not isinstance(executable_case, str) or not executable_case.strip()):
            raise ValueError(f"{suite.suite_id}:{scenario_id} has no executableCase")
        capabilities = scenario.get("runtimeCapabilities", [])
        if not isinstance(capabilities, list) or not all(isinstance(value, str) for value in capabilities):
            raise ValueError(f"{suite.suite_id}:{scenario_id} runtime capabilities must be a list of strings")
        unknown_capabilities = set(capabilities) - _RUNTIME_CAPABILITIES
        if unknown_capabilities:
            raise ValueError(
                f"{suite.suite_id}:{scenario_id} has an unknown runtime capability: "
                f"{', '.join(sorted(unknown_capabilities))}"
            )
    for path_field in ("conceptualRole", "nativeAgent"):
        path = _REPOSITORY_ROOT / str(target.get(path_field, ""))
        if not path.is_file():
            raise ValueError(f"{suite.suite_id} has no {path_field}: {path}")
    native_agent_path = _REPOSITORY_ROOT / str(target.get("nativeAgent", ""))
    native_instructions = str(tomllib.loads(native_agent_path.read_text(encoding="utf-8")).get("developer_instructions", ""))
    for skill_name in target.get("requiredSkills", []):
        if str(skill_name) not in native_instructions:
            raise ValueError(f"{suite.suite_id} native agent does not include required skill {skill_name}")
    for path_field in ("supervisor", "judge"):
        relative = manifest.get("projectAgents", {}).get(path_field)
        path = suite.path / str(relative or "")
        if not path.is_file():
            raise ValueError(f"{suite.suite_id} has no project {path_field}: {path}")
    for skill_path in manifest.get("projectSkills", {}).get("shared", []) + manifest.get("projectSkills", {}).get("suite", []):
        path = (suite.path / str(skill_path)).resolve()
        if not path.is_file():
            raise ValueError(f"{suite.suite_id} has no project skill: {path}")


def _select_runs(
    catalog: dict[str, _Suite],
    requested_suites: Sequence[str],
    requested_scenarios: Sequence[str],
) -> tuple[_RunSpec, ...]:
    scenario_filters: dict[str, list[str]] = {}
    for value in requested_scenarios:
        suite_id, separator, scenario_id = value.partition(":")
        if not separator or not suite_id or not scenario_id:
            raise ValueError(f"Scenario filters use suite-id:scenario-id: {value}")
        scenario_filters.setdefault(suite_id, []).append(scenario_id)
    selected_ids = set(requested_suites) | set(scenario_filters)
    if not selected_ids:
        selected_ids = set(catalog)
    unknown = selected_ids - set(catalog)
    if unknown:
        raise ValueError(f"Unknown suites: {', '.join(sorted(unknown))}")
    runs: list[_RunSpec] = []
    for suite in sorted((catalog[suite_id] for suite_id in selected_ids), key=lambda item: item.priority):
        available = {str(scenario["id"]) for scenario in suite.scenarios}
        chosen = tuple(scenario_filters.get(suite.suite_id, ())) or tuple(
            str(scenario["id"]) for scenario in suite.scenarios
        )
        missing = set(chosen) - available
        if missing:
            raise ValueError(f"Unknown scenarios for {suite.suite_id}: {', '.join(sorted(missing))}")
        selected_scenarios = [scenario for scenario in suite.scenarios if str(scenario["id"]) in set(chosen)]
        for scenario in selected_scenarios:
            if scenario.get("status") not in _EXECUTABLE_STATUSES:
                raise ValueError(f"{suite.suite_id}:{scenario['id']} is not executable")
            executable_case = scenario.get("executableCase")
            if not isinstance(executable_case, str) or not executable_case.strip():
                raise ValueError(f"{suite.suite_id}:{scenario['id']} has no executableCase")
        runs.append(_RunSpec(suite=suite, scenario_ids=chosen))
    return tuple(runs)


def _batch_runs(runs: Sequence[_RunSpec], maximum: int) -> tuple[tuple[_RunSpec, ...], ...]:
    if maximum < 1 or maximum > 4:
        raise ValueError("maximum concurrent supervisors must be between 1 and 4")
    batches: list[tuple[_RunSpec, ...]] = []
    ordinary: list[_RunSpec] = []
    for run in runs:
        if _runtime_capabilities((run,)) & _ISOLATED_RUNTIME_CAPABILITIES:
            if ordinary:
                batches.append(tuple(ordinary))
                ordinary = []
            batches.append((run,))
            continue
        ordinary.append(run)
        if len(ordinary) == maximum:
            batches.append(tuple(ordinary))
            ordinary = []
    if ordinary:
        batches.append(tuple(ordinary))
    return tuple(batches)


def _runtime_capabilities(batch: Sequence[_RunSpec]) -> frozenset[str]:
    capabilities: set[str] = set()
    for run in batch:
        selected = set(run.scenario_ids)
        for scenario in run.suite.scenarios:
            if str(scenario["id"]) in selected:
                capabilities.update(str(value) for value in scenario.get("runtimeCapabilities", []))
    return frozenset(capabilities)


@contextlib.contextmanager
def _temporary_run_root(label: str) -> Iterator[Path]:
    safe_label = re.sub(r"[^a-z0-9-]+", "-", label.lower()).strip("-") or "batch"
    with tempfile.TemporaryDirectory(prefix=f"dev-methodology-agent-{safe_label}-") as temporary:
        yield Path(temporary)


def _copy_agent(
    source: Path,
    invocation: str,
    agent_root: Path,
    python_executable: Path | None = None,
) -> _StagedAgent:
    if not _RUNTIME_NAME.fullmatch(invocation):
        raise ValueError(f"Invalid staged agent invocation: {invocation}")
    destination = agent_root / f"{invocation}.toml"
    source_text = source.read_text(encoding="utf-8")
    loaded = tomllib.loads(source_text)
    actual_name = loaded.get("name")
    if actual_name != invocation:
        raise ValueError(f"Staged agent name mismatch: expected {invocation}, found {actual_name}")
    instructions = str(loaded.get("developer_instructions", ""))
    if not instructions:
        raise ValueError(f"Staged agent has no developer instructions: {source}")
    marker = f"AGENT_INSTRUCTION_BINDING_{invocation}_{secrets.token_hex(16)}"
    runtime_python = python_executable or _bundled_python_executable()
    binding_instruction = (
        "\n\nRuntime instruction binding marker retained by the harness: "
        f"{marker}. "
        f"For every repository Python command, invoke {runtime_python} exactly instead of python or python3 so "
        "the required Python 3.11 standard library is available."
    )
    assignment = 'developer_instructions = """'
    start = source_text.find(assignment)
    end = source_text.find('"""', start + len(assignment))
    if start < 0 or end < 0:
        raise ValueError(f"Cannot instrument staged agent instructions: {source}")
    instruction_start = start + len(assignment)
    staged_text = source_text[:instruction_start] + binding_instruction + source_text[instruction_start:]
    if "model" not in loaded:
        staged_text = 'model = "gpt-5.6-sol"\n' + staged_text
    destination.write_text(staged_text, encoding="utf-8")
    return _StagedAgent(invocation, source, instructions, _sha256(destination), marker)


def _copy_skill_package(skill_file: Path, skill_root: Path) -> None:
    package = skill_file.resolve().parent
    destination = skill_root / package.name
    if destination.exists():
        return
    shutil.copytree(package, destination)


def _bundled_browser_plugin_root() -> Path:
    configured = os.environ.get("CODEX_BUNDLED_BROWSER_PLUGIN")
    if configured:
        candidates = [Path(configured)]
    else:
        cache_root = Path.home() / ".codex" / "plugins" / "cache" / "openai-bundled" / "browser"
        candidates = sorted((path for path in cache_root.glob("*") if path.is_dir()), reverse=True)
    for candidate in candidates:
        if (candidate / "scripts" / "browser-client.mjs").is_file() and (
            candidate / "skills" / "control-in-app-browser" / "SKILL.md"
        ).is_file():
            return candidate
    raise RuntimeError("The bundled in-app Browser runtime is unavailable")


def _bundled_computer_use_service() -> Path:
    configured = os.environ.get("CODEX_BUNDLED_COMPUTER_USE_SERVICE")
    if configured:
        candidates = [Path(configured)]
    else:
        cache_root = Path.home() / ".codex" / "plugins" / "cache" / "openai-bundled" / "computer-use"
        candidates = sorted(
            (path / "Codex Computer Use.app" for path in cache_root.glob("*") if path.is_dir()),
            reverse=True,
        )
    for candidate in candidates:
        if (candidate / "Contents" / "MacOS" / "SkyComputerUseService").is_file():
            return candidate
    raise RuntimeError("The bundled in-app Browser computer-use service is unavailable")


def _bundled_node_executable() -> Path:
    configured = os.environ.get("CODEX_BUNDLED_NODE")
    candidates = [
        *([Path(configured)] if configured else []),
        Path("/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node"),
    ]
    for candidate in candidates:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate
    raise RuntimeError("The bundled Node runtime is unavailable")


def _bundled_python_executable() -> Path:
    configured = os.environ.get("CODEX_BUNDLED_PYTHON")
    candidates = [
        *([Path(configured)] if configured else []),
        Path("/opt/homebrew/bin/python3.11"),
        Path(sys.executable),
    ]
    for candidate in candidates:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate
    raise RuntimeError("The required Python 3.11 runtime is unavailable")


def _bundled_codex_executable() -> Path:
    configured = os.environ.get("CODEX_BUNDLED_CLI")
    candidates = [
        *([Path(configured)] if configured else []),
        Path("/Applications/ChatGPT.app/Contents/Resources/codex"),
    ]
    for candidate in candidates:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate
    raise RuntimeError("The app-bundled Codex CLI is unavailable")


def _stage_browser_runtime(
    plugin_root: Path,
    codex_home: Path,
    skill_root: Path,
    app_resources: Path | None = None,
    computer_use_service: Path | None = None,
) -> Path:
    runtime_root = codex_home / "browser-runtime"
    shutil.copytree(plugin_root, runtime_root)
    source_skill = runtime_root / "skills" / "control-in-app-browser"
    destination_skill = skill_root / "control-in-app-browser"
    shutil.copytree(source_skill, destination_skill)
    skill_path = destination_skill / "SKILL.md"
    skill_path.write_text(
        skill_path.read_text(encoding="utf-8").replace("<plugin root>", str(runtime_root)),
        encoding="utf-8",
    )
    resources = app_resources or Path("/Applications/ChatGPT.app/Contents/Resources")
    executables = {
        "node_repl": resources / "cua_node" / "bin" / "node_repl",
        "node": resources / "cua_node" / "bin" / "node",
        "codex": resources / "codex",
    }
    unavailable = [str(path) for path in executables.values() if not path.is_file()]
    if unavailable:
        raise RuntimeError(f"The in-app Browser runtime lacks required executables: {', '.join(unavailable)}")
    service_source = computer_use_service or _bundled_computer_use_service()
    service_destination = codex_home / "computer-use-service.app"
    shutil.copytree(service_source, service_destination)
    browser_client = runtime_root / "scripts" / "browser-client.mjs"
    config = {
        "BROWSER_USE_AVAILABLE_BACKENDS": "iab",
        "BROWSER_USE_CODEX_APP_BUILD_FLAVOR": "prod",
        "BROWSER_USE_CODEX_APP_VERSION": plugin_root.name,
        "CODEX_CLI_PATH": str(executables["codex"]),
        "CODEX_HOME": str(codex_home),
        "NODE_REPL_INSTRUCTIONS_USE_CASE_BROWSER": (
            "Control only the isolated in-app browser for the current local synthetic evaluation."
        ),
        "NODE_REPL_NATIVE_PIPE_CONNECT_TIMEOUT_MS": "1000",
        "NODE_REPL_NODE_MODULE_DIRS": str(resources / "cua_node" / "lib" / "node_modules"),
        "NODE_REPL_NODE_PATH": str(executables["node"]),
        "NODE_REPL_TRUSTED_BROWSER_CLIENT_SHA256S": _sha256(browser_client),
        "NODE_REPL_TRUSTED_CODE_PATHS": str(codex_home),
        "SKY_CUA_SERVICE_PATH": str(service_destination),
    }
    config_lines = [
        "[mcp_servers.node_repl]",
        f"command = {json.dumps(str(executables['node_repl']))}",
        "",
        "[mcp_servers.node_repl.env]",
        *(f"{name} = {json.dumps(value)}" for name, value in config.items()),
        "",
    ]
    (codex_home / "config.toml").write_text("\n".join(config_lines), encoding="utf-8")
    return runtime_root


def _validate_target_skills(suite: _Suite, scenario_ids: Sequence[str], repository_root: Path) -> None:
    selected = set(scenario_ids)
    required_skills = {str(value) for value in suite.manifest["target"].get("requiredSkills", [])}
    for scenario in suite.scenarios:
        if str(scenario["id"]) not in selected:
            continue
        declared_skills = {str(value) for value in scenario.get("targetSkills", [])}
        for skill_name in required_skills | declared_skills:
            source = repository_root / "skills" / str(skill_name) / "SKILL.md"
            if not source.is_file():
                raise ValueError(f"{suite.suite_id}:{scenario['id']} requires missing skill {skill_name}")


def _stage_offline_project_dependencies(
    batch: Sequence[_RunSpec],
    repository_root: Path,
    workspace: Path,
    node_executable: Path | None = None,
) -> tuple[str, ...]:
    staged: list[str] = []
    for run in batch:
        selected = set(run.scenario_ids)
        for scenario in run.suite.scenarios:
            if str(scenario["id"]) not in selected:
                continue
            if "offline-node-modules" not in scenario.get("runtimeCapabilities", []):
                continue
            executable_case = str(scenario["executableCase"])
            case_path = Path(executable_case)
            if case_path.is_absolute() or len(case_path.parts) != 1 or case_path.name != executable_case:
                raise RuntimeError(
                    f"Offline Node fixture must be one project directory name: {run.suite.suite_id}:"
                    f"{scenario['id']}"
                )
            relative = Path("evals") / "projects" / executable_case / "node_modules"
            project_root = (repository_root / "evals" / "projects").resolve()
            workspace_project_root = (workspace / "evals" / "projects").resolve()
            source = (repository_root / relative).resolve()
            destination = (workspace / relative).resolve()
            if not source.is_relative_to(project_root) or not destination.is_relative_to(workspace_project_root):
                raise RuntimeError(
                    f"Offline Node fixture escapes its project root: {run.suite.suite_id}:{scenario['id']}"
                )
            if not source.is_dir():
                raise RuntimeError(
                    f"Pinned offline Node dependencies are unavailable for {run.suite.suite_id}:"
                    f"{scenario['id']}: {source}"
                )
            for candidate in source.rglob("*"):
                if candidate.is_symlink() and not candidate.resolve().is_relative_to(source):
                    raise RuntimeError(f"Offline Node fixture contains an escaping symlink: {candidate}")
            package_lock = source.parent / "package-lock.json"
            installed_package = source / "typescript" / "package.json"
            if not package_lock.is_file() or not installed_package.is_file():
                raise RuntimeError(f"Offline Node fixture lacks TypeScript lock evidence: {source.parent}")
            locked = json.loads(package_lock.read_text(encoding="utf-8"))
            installed = json.loads(installed_package.read_text(encoding="utf-8"))
            locked_version = (locked.get("packages", {}).get("node_modules/typescript", {}) or {}).get("version")
            if not locked_version or locked_version != installed.get("version"):
                raise RuntimeError(f"Offline Node fixture TypeScript version does not match its lockfile: {source.parent}")
            if destination.exists():
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source, destination, symlinks=True)
            typescript_launcher = destination / ".bin" / "tsc"
            if typescript_launcher.exists() or typescript_launcher.is_symlink():
                bundled_node = node_executable or _bundled_node_executable()
                typescript_launcher.unlink()
                typescript_launcher.write_text(
                    f"#!/bin/sh\nexec {shlex.quote(str(bundled_node))} "
                    '"$(dirname "$0")/../typescript/bin/tsc" "$@"\n',
                    encoding="utf-8",
                )
                typescript_launcher.chmod(0o755)
            staged.append(relative.as_posix())
    return tuple(staged)


def _stage_offline_maven_dependencies(
    batch: Sequence[_RunSpec],
    repository_root: Path,
    workspace: Path,
    home_root: Path,
    maven_repository: Path | None = None,
) -> tuple[str, ...]:
    source_repository = (maven_repository or Path.home() / ".m2" / "repository").resolve()
    destination_repository = (home_root / ".m2" / "repository").resolve()
    project_root = (repository_root / "evals" / "projects").resolve()
    workspace_project_root = (workspace / "evals" / "projects").resolve()
    staged: list[str] = []
    for run in batch:
        selected = set(run.scenario_ids)
        for scenario in run.suite.scenarios:
            if str(scenario["id"]) not in selected:
                continue
            if "offline-maven-repository" not in scenario.get("runtimeCapabilities", []):
                continue
            executable_case = str(scenario["executableCase"])
            case_path = Path(executable_case)
            if case_path.is_absolute() or len(case_path.parts) != 1 or case_path.name != executable_case:
                raise RuntimeError(
                    f"Offline Maven fixture must be one project directory name: {run.suite.suite_id}:"
                    f"{scenario['id']}"
                )
            relative_manifest = (
                Path("evals") / "projects" / executable_case / "offline-maven-repository.json"
            )
            source_manifest = (repository_root / relative_manifest).resolve()
            workspace_manifest = (workspace / relative_manifest).resolve()
            if not source_manifest.is_relative_to(project_root) or not workspace_manifest.is_relative_to(
                workspace_project_root
            ):
                raise RuntimeError(
                    f"Offline Maven fixture escapes its project root: {run.suite.suite_id}:{scenario['id']}"
                )
            if not source_manifest.is_file() or not workspace_manifest.is_file():
                raise RuntimeError(f"Offline Maven fixture lacks lock evidence: {source_manifest}")
            if _sha256(source_manifest) != _sha256(workspace_manifest):
                raise RuntimeError(f"Offline Maven fixture lock evidence changed during staging: {source_manifest}")
            manifest = json.loads(source_manifest.read_text(encoding="utf-8"))
            if (
                manifest.get("schema") != "dev-methodology-offline-maven-repository"
                or manifest.get("version") != 1
                or not isinstance(manifest.get("files"), list)
                or not manifest["files"]
            ):
                raise RuntimeError(f"Offline Maven fixture lock evidence is invalid: {source_manifest}")
            for entry in manifest["files"]:
                if not isinstance(entry, dict):
                    raise RuntimeError(f"Offline Maven fixture lock entry is invalid: {source_manifest}")
                relative_text = str(entry.get("path", ""))
                relative = Path(relative_text)
                expected_sha256 = str(entry.get("sha256", ""))
                if (
                    relative.is_absolute()
                    or not relative_text
                    or relative.as_posix() != relative_text
                    or ".." in relative.parts
                    or not re.fullmatch(r"[0-9a-f]{64}", expected_sha256)
                ):
                    raise RuntimeError(f"Offline Maven fixture lock entry is unsafe: {source_manifest}")
                source = (source_repository / relative).resolve()
                destination = (destination_repository / relative).resolve()
                if not source.is_relative_to(source_repository) or not destination.is_relative_to(
                    destination_repository
                ):
                    raise RuntimeError(f"Offline Maven fixture lock entry escapes its repository: {relative_text}")
                if not source.is_file() or source.is_symlink():
                    raise RuntimeError(f"Pinned offline Maven artifact is unavailable: {source}")
                observed_sha256 = _sha256(source)
                if observed_sha256 != expected_sha256:
                    raise RuntimeError(
                        f"Pinned offline Maven artifact checksum drift for {relative_text}: "
                        f"expected {expected_sha256}, observed {observed_sha256}"
                    )
                if destination.exists():
                    if not destination.is_file() or _sha256(destination) != expected_sha256:
                        raise RuntimeError(f"Conflicting offline Maven artifact destination: {destination}")
                    continue
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, destination)
            staged.append(relative_manifest.as_posix())
    if staged:
        destination_repository.mkdir(parents=True, exist_ok=True)
        (destination_repository / ".agent-suite-offline").write_text("governed\n", encoding="utf-8")
    return tuple(staged)


def _stage_batch(batch: Sequence[_RunSpec], run_root: Path) -> tuple[Path, Path, tuple[_StagedAgent, ...]]:
    workspace = run_root / "workspace"
    codex_home = run_root / "codex-home"
    agent_root = codex_home / "agents"
    skill_root = codex_home / "skills"
    home_root = run_root / "home"
    for path in (agent_root, skill_root, home_root, run_root / "tmp"):
        path.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["git", "clone", "--quiet", "--no-hardlinks", str(_REPOSITORY_ROOT), str(workspace)],
        check=True,
        text=True,
        capture_output=True,
    )
    _stage_offline_project_dependencies(batch, _REPOSITORY_ROOT, workspace)
    _stage_offline_maven_dependencies(batch, _REPOSITORY_ROOT, workspace, home_root)
    if "browser-automation" in _runtime_capabilities(batch):
        _stage_browser_runtime(_bundled_browser_plugin_root(), codex_home, skill_root)
    auth_source = Path(os.environ.get("CODEX_AUTH_FILE", str(Path.home() / ".codex" / "auth.json")))
    if not auth_source.is_file():
        raise RuntimeError(f"Codex authentication file is unavailable: {auth_source}")
    auth_destination = codex_home / "auth.json"
    shutil.copyfile(auth_source, auth_destination)
    auth_destination.chmod(0o600)
    staged: dict[str, _StagedAgent] = {}
    for run in batch:
        suite = run.suite
        _validate_target_skills(suite, run.scenario_ids, _REPOSITORY_ROOT)
        manifest = suite.manifest
        execution = manifest["execution"]
        project_agents = manifest["projectAgents"]
        sources = (
            (suite.path / project_agents["supervisor"], execution["supervisorInvocation"]),
            (_REPOSITORY_ROOT / manifest["target"]["nativeAgent"], execution["targetInvocation"]),
            (suite.path / project_agents["judge"], execution["judgeInvocation"]),
        )
        for source, invocation in sources:
            if invocation not in staged:
                staged[invocation] = _copy_agent(source, invocation, agent_root)
        for dependency in manifest["target"].get("allowedAgentDependencies", []):
            invocation = str(dependency).replace("-", "_")
            source = _REPOSITORY_ROOT / "generated" / "adapters" / "codex" / "agents" / f"{dependency}.toml"
            if invocation not in staged:
                staged[invocation] = _copy_agent(source, invocation, agent_root)
        for skill_path in manifest.get("projectSkills", {}).get("shared", []) + manifest.get("projectSkills", {}).get("suite", []):
            _copy_skill_package(suite.path / skill_path, skill_root)
        selected = {scenario_id for scenario_id in run.scenario_ids}
        scenario_skills = {
            str(skill)
            for scenario in suite.scenarios
            if str(scenario["id"]) in selected
            for skill in scenario.get("targetSkills", [])
        }
        for skill_name in scenario_skills:
            source = _REPOSITORY_ROOT / "skills" / skill_name / "SKILL.md"
            _copy_skill_package(source, skill_root)
    return workspace, codex_home, tuple(staged.values())


def _coordinator_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["runs", "batchCleanup", "residualRisk"],
        "properties": {
            "runs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "suite",
                        "scenarioResults",
                        "maximumActiveChildrenObserved",
                        "cleanup",
                    ],
                    "properties": {
                        "suite": {"type": "string"},
                        "scenarioResults": {
                            "type": "array",
                            "minItems": 1,
                            "items": {
                                "type": "object",
                                "additionalProperties": False,
                                "required": [
                                    "scenario",
                                    "status",
                                    "targetInvoked",
                                    "judgeInvoked",
                                    "identityEvidence",
                                    "cleanup",
                                    "evidence",
                                ],
                                "properties": {
                                    "scenario": {"type": "string"},
                                    "status": {"type": "string", "enum": sorted(_REPORT_STATUSES)},
                                    "targetInvoked": {"type": "boolean"},
                                    "judgeInvoked": {"type": "boolean"},
                                    "identityEvidence": {"type": "array", "items": {"type": "string"}},
                                    "cleanup": {"type": "string", "enum": ["clean", "failed"]},
                                    "evidence": {"type": "array", "items": {"type": "string"}},
                                },
                            },
                        },
                        "maximumActiveChildrenObserved": {"type": "integer", "minimum": 0, "maximum": 1},
                        "cleanup": {"type": "string", "enum": ["clean", "failed"]},
                    },
                },
            },
            "batchCleanup": {"type": "string", "enum": ["clean", "failed"]},
            "residualRisk": {"type": "string"},
        },
    }


def _agent_registration_arguments(staged: Sequence[_StagedAgent], codex_home: Path) -> tuple[str, ...]:
    arguments: list[str] = []
    for agent in staged:
        config_path = codex_home / "agents" / f"{agent.invocation}.toml"
        loaded = tomllib.loads(config_path.read_text(encoding="utf-8"))
        description = str(loaded.get("description", f"Governed {agent.invocation} evaluation agent."))
        arguments.extend(
            (
                "-c",
                f"agents.{agent.invocation}.description={json.dumps(description)}",
                "-c",
                f"agents.{agent.invocation}.config_file={json.dumps(str(config_path))}",
            )
        )
    return tuple(arguments)


def _multi_agent_runtime_arguments(maximum_threads: int) -> tuple[str, ...]:
    return (
        "--model",
        "gpt-5.5",
        "--enable",
        "multi_agent",
        "--disable",
        "multi_agent_v2",
        "-c",
        f"agents.max_threads={maximum_threads}",
    )


def _write_local_runtime_profile(codex_home: Path) -> str:
    profile_name = "agent-suite-local-runtime"
    profile_path = codex_home / f"{profile_name}.config.toml"
    profile_path.write_text(
        f'''default_permissions = "{profile_name}"

[permissions.{profile_name}]
extends = ":workspace"

[permissions.{profile_name}.network]
enabled = true
mode = "limited"
allow_local_binding = true

[permissions.{profile_name}.network.domains]
"localhost" = "allow"
"127.0.0.1" = "allow"
''',
        encoding="utf-8",
    )
    return profile_name


def _capability_runtime_arguments(capabilities: frozenset[str], codex_home: Path) -> tuple[str, ...]:
    if not capabilities & _ISOLATED_RUNTIME_CAPABILITIES:
        return ("--sandbox", "workspace-write")
    profile_name = _write_local_runtime_profile(codex_home)
    arguments = ["-p", profile_name, "--enable", "network_proxy"]
    if "browser-automation" in capabilities:
        arguments.extend(("--enable", "in_app_browser", "--enable", "browser_use"))
    return tuple(arguments)


def _sandbox_profile_arguments(codex_home: Path, workspace: Path) -> tuple[str, ...]:
    profile_name = "agent-suite-local-runtime"
    if not (codex_home / f"{profile_name}.config.toml").is_file():
        _write_local_runtime_profile(codex_home)
    return (
        str(_bundled_codex_executable()),
        "sandbox",
        "-C",
        str(workspace),
        "-p",
        profile_name,
        "-P",
        profile_name,
        "--enable",
        "network_proxy",
        "--",
    )


def _available_loopback_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind(("127.0.0.1", 0))
        return int(listener.getsockname()[1])


def _preflight_browser_service(
    workspace: Path,
    codex_home: Path,
    environment: dict[str, str],
) -> str:
    fixture = workspace / "evals" / "agent-tests" / "dev-browser-operator" / "fixtures" / "browser-workflow"
    manifest = _load_yaml(fixture / "runtime-manifest.yaml")
    frozen = str(manifest.get("serviceCommand", ""))
    if "--bind 127.0.0.1" not in frozen:
        raise RuntimeError("Browser fixture service command must bind explicitly to 127.0.0.1")
    port = _available_loopback_port()
    service_arguments = tuple(
        value.replace("PORT", str(port)).replace("FIXTURE_ROOT", str(fixture))
        for value in shlex.split(frozen)
    )
    profile = _sandbox_profile_arguments(codex_home, workspace)
    process = subprocess.Popen(
        [*profile, *service_arguments],
        cwd=workspace,
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    route = str(manifest.get("healthRoute", ""))
    deadline = time.monotonic() + 5
    response = ""
    try:
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise RuntimeError(f"Browser fixture service exited during preflight with {process.returncode}")
            completed = subprocess.run(
                [*profile, "/usr/bin/curl", "-fsS", "--max-time", "1", f"http://127.0.0.1:{port}{route}"],
                cwd=workspace,
                env=environment,
                check=False,
                text=True,
                capture_output=True,
            )
            if completed.returncode == 0:
                response = completed.stdout
                break
            time.sleep(0.05)
        if not response:
            raise RuntimeError("Browser fixture health route was unavailable during preflight")
    finally:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=3)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.settimeout(0.5)
        if probe.connect_ex(("127.0.0.1", port)) == 0:
            raise RuntimeError("Browser fixture service retained its port after preflight cleanup")
    return f"{frozen} route={route} bytes={len(response.encode('utf-8'))} cleanup=clean"


def _preflight_runtime_capabilities(
    batch: Sequence[_RunSpec],
    workspace: Path,
    codex_home: Path,
    environment: dict[str, str],
) -> tuple[str, ...]:
    capabilities = _runtime_capabilities(batch)
    evidence: list[str] = []
    if "offline-node-modules" in capabilities:
        for run in batch:
            selected = set(run.scenario_ids)
            for scenario in run.suite.scenarios:
                if str(scenario["id"]) not in selected or "offline-node-modules" not in scenario.get(
                    "runtimeCapabilities", []
                ):
                    continue
                project = workspace / "evals" / "projects" / str(scenario["executableCase"])
                node_version = subprocess.run(
                    [str(_bundled_node_executable()), "--version"],
                    cwd=project,
                    env=environment,
                    check=True,
                    text=True,
                    capture_output=True,
                )
                completed = subprocess.run(
                    [str(project / "node_modules" / ".bin" / "tsc"), "--version"],
                    cwd=project,
                    env=environment,
                    check=True,
                    text=True,
                    capture_output=True,
                )
                evidence.append(
                    f"{run.suite.suite_id}:{scenario['id']} "
                    f"Node {node_version.stdout.strip()} {completed.stdout.strip()}"
                )
    if "offline-maven-repository" in capabilities:
        for run in batch:
            selected = set(run.scenario_ids)
            for scenario in run.suite.scenarios:
                if str(scenario["id"]) not in selected or "offline-maven-repository" not in scenario.get(
                    "runtimeCapabilities", []
                ):
                    continue
                project = workspace / "evals" / "projects" / str(scenario["executableCase"])
                version = subprocess.run(
                    ["mvn", "--version"],
                    cwd=project,
                    env=environment,
                    check=True,
                    text=True,
                    capture_output=True,
                )
                completed = subprocess.run(
                    ["mvn", "-q", "test"],
                    cwd=project,
                    env=environment,
                    check=True,
                    text=True,
                    capture_output=True,
                )
                version_line = version.stdout.splitlines()[0] if version.stdout else "Maven version unavailable"
                evidence.append(
                    f"{run.suite.suite_id}:{scenario['id']} {version_line} offline-test=pass "
                    f"stdout-bytes={len(completed.stdout.encode('utf-8'))}"
                )
    if capabilities & {"loopback", "child-process-inspection"}:
        profile = _sandbox_profile_arguments(codex_home, workspace)
        bind_probe = subprocess.run(
            [
                *profile,
                "/usr/bin/python3",
                "-c",
                "import socket; s=socket.socket(); s.bind(('127.0.0.1',0)); print(s.getsockname()[1])",
            ],
            cwd=workspace,
            env=environment,
            check=True,
            text=True,
            capture_output=True,
        )
        evidence.append(f"loopback-bind-port {bind_probe.stdout.strip()}")
        external_probe = subprocess.run(
            [*profile, "/usr/bin/curl", "-fsS", "--max-time", "2", "https://example.invalid"],
            cwd=workspace,
            env=environment,
            check=False,
            text=True,
            capture_output=True,
        )
        if external_probe.returncode == 0:
            raise RuntimeError("The local-runtime permission profile permitted a non-local destination")
        evidence.append("managed network proxy denied non-local destination")
    if "child-process-inspection" in capabilities:
        fixture = workspace / "evals" / "agent-tests" / "dev-runtime-diagnostician" / "fixtures" / "retained-process-port"
        profile = _sandbox_profile_arguments(codex_home, workspace)
        for command in ("reproduce", "verify-clean"):
            completed = subprocess.run(
                [*profile, "/usr/bin/python3", str(fixture / "lifecycle_probe.py"), command],
                cwd=fixture,
                env=environment,
                check=True,
                text=True,
                capture_output=True,
            )
            observed = json.loads(completed.stdout)
            required_true = (
                ("parentExited", "portRetainedAfterParentExit", "processInspectionVerified", "cleanupVerified")
                if command == "reproduce"
                else ("cleanRestartsVerified",)
            )
            if not isinstance(observed, dict) or not all(observed.get(field) is True for field in required_true):
                raise RuntimeError(f"Retained-process preflight did not prove {command}: {completed.stdout.strip()}")
            if command == "reproduce" and observed.get("inspectedPid") != observed.get("childPid"):
                raise RuntimeError(f"Retained-process preflight inspected the wrong process: {completed.stdout.strip()}")
            evidence.append(f"retained-process-port {command} {completed.stdout.strip()}")
    if "browser-automation" in capabilities:
        browser_client = codex_home / "browser-runtime" / "scripts" / "browser-client.mjs"
        browser_skill = codex_home / "skills" / "control-in-app-browser" / "SKILL.md"
        if not browser_client.is_file() or not browser_skill.is_file():
            raise RuntimeError("The isolated Browser runtime did not stage completely")
        if str(codex_home / "browser-runtime") not in browser_skill.read_text(encoding="utf-8"):
            raise RuntimeError("The isolated Browser skill is not bound to its staged runtime")
        evidence.append(
            f"isolated in-app Browser runtime staged client-sha256={_sha256(browser_client)} "
            f"skill-sha256={_sha256(browser_skill)}"
        )
        if "loopback" in capabilities:
            evidence.append(f"browser fixture service {_preflight_browser_service(workspace, codex_home, environment)}")
    return tuple(evidence)


def _coordinator_prompt(batch: Sequence[_RunSpec], checkpoint_root: Path) -> str:
    assignments = []
    for run in batch:
        execution = run.suite.manifest["execution"]
        assignments.append(
            {
                "suite": run.suite.suite_id,
                "supervisor": execution["supervisorInvocation"],
                "target": execution["targetInvocation"],
                "judge": execution["judgeInvocation"],
                "scenarios": list(run.scenario_ids),
                "nestedAgentLimit": int(execution.get("nestedAgentLimit", 0)),
                "runtimeCapabilities": sorted(_runtime_capabilities((run,))),
                "checkpointRoot": str(checkpoint_root),
            }
        )
    return (
        "Coordinate this governed synthetic evaluation batch. Spawn every listed custom supervisor concurrently, "
        "using agent_type exactly equal to its supervisor value and fork_context exactly false so the registered "
        "custom config is "
        "applied instead of inheriting coordinator model settings. Give each supervisor only its listed suite and scenarios, plus "
        "an explicit instruction to pass agent_type exactly equal to the listed target or judge and fork_context exactly "
        "false for those child spawns. "
        "Each supervisor must run its selected scenarios sequentially, use exactly one active child at a time, invoke "
        "only those hardcoded agents, retain one independent result per scenario, "
        "write the required checkpointRoot/suite-id/scenario-id.json checkpoint immediately after each terminal "
        "scenario and before starting later work. Each checkpoint must contain suite, scenario, status, targetInvoked, "
        "judgeInvoked, identityEvidence as an array of strings, evidence as an array of strings, cleanup as clean or "
        "failed, and residualRisk as a string; nested objects are forbidden for those fields. Each result must state "
        "targetInvoked and judgeInvoked explicitly, "
        "and clean every fixture, claim, process, worktree, and credential it owns. One supervisor child may use one "
        "declared nested dependency at a time only where nestedAgentLimit is 1; serialize that temporary tenth-agent "
        "slot across the batch. Do not browse external sites; local fixture browser automation is allowed only for "
        "a scenario that declares browser-automation. Those scenarios must use only the staged control-in-app-browser "
        "skill, open a fresh local-target tab, avoid existing tabs or authenticated state, and close every owned tab. "
        "Do not install software, read outside this disposable "
        "repository, alter the "
        "evaluation contracts during a run, or fix a distributed skill. Classify actual test-infrastructure failures "
        "separately from target findings. Wait for every supervisor, then return only the required JSON report. "
        f"Assignments: {json.dumps(assignments, sort_keys=True)}"
    )


def _redact_capture(text: str) -> str:
    for original, replacement in _CAPTURE_REPLACEMENTS:
        text = text.replace(original, replacement)
    text = re.sub(r"gAAAAA[A-Za-z0-9_-]{40,}", "[REDACTED-ENCRYPTED-PAYLOAD]", text)
    return text


def _extract_coordinator_report(stream: str) -> dict[str, Any]:
    messages: list[str] = []
    for line in stream.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        item = event.get("item") if isinstance(event, dict) else None
        if isinstance(item, dict) and item.get("type") == "agent_message" and isinstance(item.get("text"), str):
            messages.append(item["text"])
    if not messages:
        raise RuntimeError("The Codex event stream contains no coordinator report")
    try:
        report = json.loads(messages[-1])
    except json.JSONDecodeError as error:
        raise RuntimeError("The coordinator report is not valid JSON") from error
    if not isinstance(report, dict):
        raise RuntimeError("The coordinator report must be a JSON object")
    return report


def _load_checkpoint_report(checkpoint_root: Path, batch: Sequence[_RunSpec]) -> dict[str, Any] | None:
    runs: list[dict[str, Any]] = []
    for run in batch:
        scenario_results: list[dict[str, Any]] = []
        residual_risks: list[str] = []
        for scenario_id in run.scenario_ids:
            path = checkpoint_root / run.suite.suite_id / f"{scenario_id}.json"
            if not path.is_file():
                continue
            loaded = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(loaded, dict):
                raise RuntimeError(f"Scenario checkpoint must be an object: {path}")
            if loaded.get("suite") != run.suite.suite_id or loaded.get("scenario") != scenario_id:
                raise RuntimeError(f"Scenario checkpoint identity mismatch: {path}")
            identity_evidence = loaded.get("identityEvidence")
            evidence = loaded.get("evidence")
            if not isinstance(identity_evidence, list) or not all(
                isinstance(value, str) for value in identity_evidence
            ):
                raise RuntimeError(f"Scenario checkpoint identityEvidence must be an array of strings: {path}")
            if not isinstance(evidence, list) or not all(isinstance(value, str) for value in evidence):
                raise RuntimeError(f"Scenario checkpoint evidence must be an array of strings: {path}")
            if loaded.get("status") not in _TERMINAL_STATUSES:
                raise RuntimeError(f"Scenario checkpoint status must be terminal: {path}")
            if type(loaded.get("targetInvoked")) is not bool or type(loaded.get("judgeInvoked")) is not bool:
                raise RuntimeError(f"Scenario checkpoint invocation flags must be booleans: {path}")
            if loaded.get("cleanup") not in {"clean", "failed"}:
                raise RuntimeError(f"Scenario checkpoint cleanup must be clean or failed: {path}")
            if not isinstance(loaded.get("residualRisk"), str):
                raise RuntimeError(f"Scenario checkpoint residualRisk must be a string: {path}")
            scenario_results.append(
                {
                    "scenario": scenario_id,
                    "status": loaded.get("status"),
                    "targetInvoked": loaded.get("targetInvoked"),
                    "judgeInvoked": loaded.get("judgeInvoked"),
                    "identityEvidence": identity_evidence,
                    "cleanup": loaded["cleanup"],
                    "evidence": evidence,
                }
            )
            if loaded.get("residualRisk"):
                residual_risks.append(str(loaded["residualRisk"]))
        if scenario_results:
            runs.append(
                {
                    "suite": run.suite.suite_id,
                    "scenarioResults": scenario_results,
                    "maximumActiveChildrenObserved": 1,
                    "cleanup": "clean" if all(item["cleanup"] == "clean" for item in scenario_results) else "failed",
                    "checkpointResidualRisk": "; ".join(residual_risks),
                }
            )
    if not runs:
        return None
    return {
        "runs": runs,
        "batchCleanup": "unknown",
        "residualRisk": "Partial supervisor checkpoints retained before coordinator completion.",
    }


def _audit_checkpoint_agreement(
    report: dict[str, Any],
    checkpoint_report: dict[str, Any] | None,
    batch: Sequence[_RunSpec],
) -> None:
    expected = {
        (run.suite.suite_id, scenario_id)
        for run in batch
        for scenario_id in run.scenario_ids
    }

    def scenario_map(document: dict[str, Any] | None) -> dict[tuple[str, str], dict[str, Any]]:
        mapped: dict[tuple[str, str], dict[str, Any]] = {}
        for run_result in (document or {}).get("runs", []):
            suite_id = str(run_result.get("suite", ""))
            for scenario_result in run_result.get("scenarioResults", []):
                mapped[(suite_id, str(scenario_result.get("scenario", "")))] = scenario_result
        return mapped

    final_results = scenario_map(report)
    checkpoints = scenario_map(checkpoint_report)
    if set(checkpoints) != expected:
        raise RuntimeError(
            f"Checkpoint coverage mismatch: expected {sorted(expected)}, observed {sorted(checkpoints)}"
        )
    compared_fields = ("status", "targetInvoked", "judgeInvoked", "cleanup")
    for identity in sorted(expected):
        if any(final_results[identity].get(field) != checkpoints[identity].get(field) for field in compared_fields):
            raise RuntimeError(f"Final report disagrees with checkpoint for {identity[0]}:{identity[1]}")


def _audit_report(batch: Sequence[_RunSpec], report: dict[str, Any]) -> list[dict[str, Any]]:
    expected = {run.suite.suite_id: set(run.scenario_ids) for run in batch}
    observed: dict[str, set[str]] = {}
    runs = report.get("runs", [])
    if not isinstance(runs, list):
        raise RuntimeError("Coordinator report runs must be a list")
    for item in runs:
        suite_id = str(item.get("suite", ""))
        if suite_id in observed:
            raise RuntimeError(f"Duplicate coordinator result for {suite_id}")
        scenario_results = item.get("scenarioResults", [])
        if not isinstance(scenario_results, list):
            raise RuntimeError(f"Scenario results must be a list for {suite_id}")
        scenario_names = [str(value.get("scenario", "")) for value in scenario_results]
        if len(scenario_names) != len(set(scenario_names)):
            raise RuntimeError(f"Duplicate scenario result for {suite_id}")
        observed[suite_id] = set(scenario_names)
        for scenario_result in scenario_results:
            if scenario_result.get("status") not in _TERMINAL_STATUSES:
                raise RuntimeError(f"Invalid terminal status for {suite_id}:{scenario_result.get('scenario')}")
            if not isinstance(scenario_result.get("targetInvoked"), bool) or not isinstance(
                scenario_result.get("judgeInvoked"), bool
            ):
                raise RuntimeError(f"Missing invocation disposition for {suite_id}:{scenario_result.get('scenario')}")
            if scenario_result.get("judgeInvoked") and not scenario_result.get("targetInvoked"):
                raise RuntimeError(f"Judge ran without target for {suite_id}:{scenario_result.get('scenario')}")
            if scenario_result.get("status") in {"PASS", "FAIL"} and not (
                scenario_result.get("targetInvoked") and scenario_result.get("judgeInvoked")
            ):
                raise RuntimeError(f"Terminal verdict lacks target and Judge for {suite_id}:{scenario_result.get('scenario')}")
            if not scenario_result.get("identityEvidence"):
                raise RuntimeError(f"Missing identity evidence for {suite_id}:{scenario_result.get('scenario')}")
            if scenario_result.get("cleanup") != "clean":
                raise RuntimeError(f"Cleanup failed for {suite_id}:{scenario_result.get('scenario')}")
        if int(item.get("maximumActiveChildrenObserved", -1)) > 1:
            raise RuntimeError(f"Child concurrency exceeded for {suite_id}")
        if item.get("cleanup") != "clean":
            raise RuntimeError(f"Suite cleanup failed for {suite_id}")
    if observed != expected:
        raise RuntimeError(f"Coordinator result coverage mismatch: expected {expected}, observed {observed}")
    if report.get("batchCleanup") != "clean":
        raise RuntimeError("Batch cleanup did not complete")
    return runs


def _timestamp_seconds(value: str) -> float:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()


def _load_sessions(codex_home: Path) -> tuple[_Session, ...]:
    sessions: list[_Session] = []
    for rollout in codex_home.glob("**/rollout-*.jsonl"):
        rollout_text = rollout.read_text(encoding="utf-8", errors="replace")
        events = []
        for line in rollout_text.splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(event, dict) and isinstance(event.get("timestamp"), str):
                events.append(event)
        metadata = next((event.get("payload", {}) for event in events if event.get("type") == "session_meta"), None)
        if not isinstance(metadata, dict) or not events:
            continue
        source = metadata.get("source", {})
        spawn = source.get("subagent", {}).get("thread_spawn", {}) if isinstance(source, dict) else {}
        invocation = metadata.get("agent_role") or spawn.get("agent_role")
        bound_markers: set[str] = set()
        for event in events:
            payload = event.get("payload", {})
            if not isinstance(payload, dict) or event.get("type") != "response_item":
                continue
            if payload.get("type") != "message" or payload.get("role") != "developer":
                continue
            developer_text = "\n".join(
                str(item.get("text", ""))
                for item in payload.get("content", [])
                if isinstance(item, dict) and item.get("type") == "input_text"
            )
            bound_markers.update(
                re.findall(r"AGENT_INSTRUCTION_BINDING_[a-z0-9_]+_[a-f0-9]{32}", developer_text)
            )
        sessions.append(
            _Session(
                session_id=str(metadata.get("id", rollout.stem)),
                parent_thread_id=metadata.get("parent_thread_id"),
                invocation=str(invocation) if invocation else None,
                depth=int(spawn.get("depth", 0)),
                started_at=_timestamp_seconds(str(events[0]["timestamp"])),
                finished_at=_timestamp_seconds(str(events[-1]["timestamp"])),
                instruction_markers=frozenset(bound_markers),
            )
        )
    return tuple(sessions)


def _audit_identity(
    staged: Sequence[_StagedAgent],
    codex_home: Path,
    expected_invocation_counts: dict[str, int],
    batch: Sequence[_RunSpec] | None = None,
    report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    sessions = _load_sessions(codex_home)
    sessions_by_invocation: dict[str, list[_Session]] = {}
    for session in sessions:
        if session.invocation:
            sessions_by_invocation.setdefault(session.invocation, []).append(session)
    agents = []
    for agent in staged:
        matching_sessions = sessions_by_invocation.get(agent.invocation, [])
        exact_sessions = [session for session in matching_sessions if agent.instruction_marker in session.instruction_markers]
        exact_session = bool(exact_sessions)
        required_count = expected_invocation_counts.get(agent.invocation, 0)
        required = required_count > 0
        agents.append(
            {
                "invocation": agent.invocation,
                "definitionSha256": agent.sha256,
                "required": required,
                "requiredSessionCount": required_count,
                "exactCustomAgentSession": exact_session,
                "instructionBinding": "runtime-developer-input-bound-to-staged-definition" if exact_session else "missing",
                "boundSessionIds": [session.session_id for session in exact_sessions],
            }
        )
        if matching_sessions and len(exact_sessions) != len(matching_sessions):
            raise RuntimeError(f"Missing runtime instruction binding for {agent.invocation}")
        if agent.invocation in expected_invocation_counts and len(exact_sessions) != required_count:
            raise RuntimeError(
                f"Custom-agent session count mismatch for {agent.invocation}: "
                f"expected {required_count}, observed {len(exact_sessions)}"
            )
    scenario_bindings: list[dict[str, str]] = []
    if batch is not None:
        reported_scenarios = {
            (str(run_result.get("suite", "")), str(scenario_result.get("scenario", ""))): scenario_result
            for run_result in (report or {}).get("runs", [])
            for scenario_result in run_result.get("scenarioResults", [])
        }
        for run in batch:
            execution = run.suite.manifest["execution"]
            supervisors = [
                session
                for session in sessions
                if session.depth == 1 and session.invocation == execution["supervisorInvocation"]
            ]
            if len(supervisors) != 1:
                raise RuntimeError(f"Cannot bind scenarios to supervisor for {run.suite.suite_id}")
            supervisor = supervisors[0]
            children = sorted(
                (session for session in sessions if session.parent_thread_id == supervisor.session_id),
                key=lambda session: session.started_at,
            )
            expected_sequence: list[tuple[str, str, str]] = []
            for scenario_id in run.scenario_ids:
                scenario_result = reported_scenarios.get((run.suite.suite_id, scenario_id), {})
                if scenario_result.get("targetInvoked"):
                    expected_sequence.append((scenario_id, "target", str(execution["targetInvocation"])))
                if scenario_result.get("judgeInvoked"):
                    expected_sequence.append((scenario_id, "judge", str(execution["judgeInvocation"])))
            observed_sequence = [str(session.invocation) for session in children]
            expected_invocations = [invocation for _, _, invocation in expected_sequence]
            if observed_sequence != expected_invocations:
                raise RuntimeError(
                    f"Scenario child sequence mismatch for {run.suite.suite_id}: "
                    f"expected {expected_invocations}, observed {observed_sequence}"
                )
            for (scenario_id, kind, invocation), session in zip(expected_sequence, children, strict=True):
                scenario_bindings.append(
                    {
                        "suite": run.suite.suite_id,
                        "scenario": scenario_id,
                        "kind": kind,
                        "invocation": invocation,
                        "sessionId": session.session_id,
                        "parentSessionId": str(session.parent_thread_id),
                    }
                )
    return {"rolloutCount": len(sessions), "agents": agents, "scenarioBindings": scenario_bindings}


def _audit_session_concurrency(
    sessions: Sequence[_Session],
    maximum_threads: int,
    batch: Sequence[_RunSpec] | None = None,
) -> dict[str, int]:
    by_parent: dict[str, list[_Session]] = {}
    for session in sessions:
        if session.parent_thread_id:
            by_parent.setdefault(session.parent_thread_id, []).append(session)
    supervisor_sessions = [session for session in sessions if session.depth == 1]
    if len(supervisor_sessions) > 4:
        raise RuntimeError(f"Supervisor concurrency limit exceeded: {len(supervisor_sessions)} > 4")
    if batch is not None:
        anonymous = [session.session_id for session in sessions if session.depth > 0 and not session.invocation]
        if anonymous:
            raise RuntimeError(f"Anonymous child sessions are not allowed: {', '.join(sorted(anonymous))}")
        expected_supervisors = sorted(
            str(run.suite.manifest["execution"]["supervisorInvocation"]) for run in batch
        )
        observed_supervisors = sorted(str(session.invocation) for session in supervisor_sessions)
        if observed_supervisors != expected_supervisors:
            raise RuntimeError(
                f"Supervisor identity mismatch: expected {expected_supervisors}, observed {observed_supervisors}"
            )
    supervisors = {session.session_id for session in supervisor_sessions}
    maximum_children = 0
    for supervisor in supervisors:
        children = by_parent.get(supervisor, [])
        maximum_children = max(maximum_children, 1 if children else 0)
        for index, first in enumerate(children):
            for second in children[index + 1 :]:
                if max(first.started_at, second.started_at) < min(first.finished_at, second.finished_at):
                    raise RuntimeError(f"Supervisor {supervisor} has overlapping children")
    timeline = sorted(
        [(session.started_at, 1, session.depth) for session in sessions]
        + [(session.finished_at, -1, session.depth) for session in sessions]
    )
    active = 0
    active_nested = 0
    maximum_active = 0
    for _, delta, depth in timeline:
        active += delta
        if depth >= 3:
            active_nested += delta
        maximum_active = max(maximum_active, active)
        if active > maximum_threads:
            raise RuntimeError(f"Runtime agent ceiling exceeded: {active} > {maximum_threads}")
        if active_nested > 1:
            raise RuntimeError("Nested dependency execution was not serialized")
    if batch is not None:
        allowed_dependencies = {
            str(dependency).replace("-", "_")
            for run in batch
            for dependency in run.suite.manifest["target"].get("allowedAgentDependencies", [])
        }
        known_invocations = {
            str(run.suite.manifest["execution"][key])
            for run in batch
            for key in ("supervisorInvocation", "targetInvocation", "judgeInvocation")
        } | allowed_dependencies
        unexpected = sorted(
            {str(session.invocation) for session in sessions if session.depth > 0 and session.invocation}
            - known_invocations
        )
        if unexpected:
            raise RuntimeError(f"Unexpected custom-agent sessions: {', '.join(unexpected)}")
        for session in sessions:
            if session.depth >= 3 and session.invocation not in allowed_dependencies:
                raise RuntimeError(f"Undeclared nested dependency session: {session.invocation}")
        session_by_id = {session.session_id: session for session in sessions}
        suite_by_supervisor = {
            str(run.suite.manifest["execution"]["supervisorInvocation"]): run.suite for run in batch
        }
        suite_by_target = {
            str(run.suite.manifest["execution"]["targetInvocation"]): run.suite for run in batch
        }
        for supervisor in supervisor_sessions:
            suite = suite_by_supervisor.get(str(supervisor.invocation))
            if suite is None:
                continue
            execution = suite.manifest["execution"]
            allowed_children = {str(execution["targetInvocation"]), str(execution["judgeInvocation"])}
            child_invocations = {
                str(child.invocation) for child in by_parent.get(supervisor.session_id, []) if child.invocation
            }
            invalid_children = sorted(child_invocations - allowed_children)
            if invalid_children:
                raise RuntimeError(
                    f"Supervisor {supervisor.invocation} spawned undeclared children: {', '.join(invalid_children)}"
                )
        for nested in (session for session in sessions if session.depth >= 3):
            parent = session_by_id.get(str(nested.parent_thread_id))
            suite = suite_by_target.get(str(parent.invocation)) if parent else None
            suite_dependencies = {
                str(value).replace("-", "_")
                for value in suite.manifest["target"].get("allowedAgentDependencies", [])
            } if suite else set()
            if nested.invocation not in suite_dependencies:
                raise RuntimeError(
                    f"Nested dependency {nested.invocation} is not allowed for parent "
                    f"{parent.invocation if parent else nested.parent_thread_id}"
                )
    return {"maximumActiveSessions": maximum_active, "maximumChildrenObserved": maximum_children}


def _expected_invocation_counts(batch: Sequence[_RunSpec], report: dict[str, Any]) -> dict[str, int]:
    expected: dict[str, int] = {}
    reported_scenarios = {
        (str(run_result.get("suite", "")), str(scenario_result.get("scenario", ""))): scenario_result
        for run_result in report.get("runs", [])
        for scenario_result in run_result.get("scenarioResults", [])
    }
    for run in batch:
        execution = run.suite.manifest["execution"]
        expected[str(execution["supervisorInvocation"])] = 1
        expected[str(execution["targetInvocation"])] = sum(
            bool(reported_scenarios.get((run.suite.suite_id, scenario_id), {}).get("targetInvoked"))
            for scenario_id in run.scenario_ids
        )
        expected[str(execution["judgeInvocation"])] = sum(
            bool(reported_scenarios.get((run.suite.suite_id, scenario_id), {}).get("judgeInvoked"))
            for scenario_id in run.scenario_ids
        )
    return expected


def _retain_sessions(codex_home: Path, destination: Path) -> int:
    count = 0
    destination.mkdir(parents=True, exist_ok=True)
    for rollout in codex_home.glob("**/rollout-*.jsonl"):
        target = destination / rollout.name
        target.write_text(_redact_capture(rollout.read_text(encoding="utf-8", errors="replace")), encoding="utf-8")
        count += 1
    return count


def _audit_browser_activity(
    codex_home: Path,
    batch: Sequence[_RunSpec],
    identity: dict[str, Any],
    report: dict[str, Any],
) -> dict[str, int]:
    browser_scenarios = {
        (run.suite.suite_id, scenario_id)
        for run in batch
        for scenario_id in run.scenario_ids
        for scenario in run.suite.scenarios
        if str(scenario["id"]) == scenario_id and "browser-automation" in scenario.get("runtimeCapabilities", [])
    }
    if not browser_scenarios:
        return {"targetSessions": 0, "nodeReplCalls": 0, "blockedTargetSessions": 0}
    statuses = {
        (str(run_result.get("suite", "")), str(scenario_result.get("scenario", ""))): str(
            scenario_result.get("status", "")
        )
        for run_result in report.get("runs", [])
        for scenario_result in run_result.get("scenarioResults", [])
    }
    bindings = {
        (str(binding.get("suite", "")), str(binding.get("scenario", ""))): str(binding.get("sessionId", ""))
        for binding in identity.get("scenarioBindings", [])
        if binding.get("kind") == "target"
    }
    missing = sorted(browser_scenarios - set(bindings))
    if missing:
        raise RuntimeError(f"Browser target session binding is missing for {missing}")
    events_by_session: dict[str, list[dict[str, Any]]] = {}
    for rollout in codex_home.glob("**/rollout-*.jsonl"):
        events: list[dict[str, Any]] = []
        for line in rollout.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(event, dict):
                events.append(event)
        metadata = next(
            (event.get("payload", {}) for event in events if event.get("type") == "session_meta"),
            {},
        )
        if isinstance(metadata, dict) and metadata.get("id"):
            events_by_session[str(metadata["id"])] = events
    call_count = 0
    blocked_count = 0
    for suite_scenario in sorted(browser_scenarios):
        session_id = bindings[suite_scenario]
        events = events_by_session.get(session_id, [])
        arguments: list[str] = []
        tool_results: list[str] = []
        for event in events:
            if event.get("type") not in {"response_item", "event_msg"}:
                continue
            payload = event.get("payload", {})
            if not isinstance(payload, dict):
                continue
            if payload.get("type") in {"custom_tool_call_output", "mcp_tool_call_end"}:
                tool_results.append(json.dumps(payload, sort_keys=True))
            raw_arguments = payload.get("arguments", payload.get("input", ""))
            serialized = raw_arguments if isinstance(raw_arguments, str) else json.dumps(raw_arguments)
            direct_call = payload.get("name") == "mcp__node_repl__js"
            nested_call = payload.get("name") == "exec" and "tools.mcp__node_repl__js" in serialized
            if direct_call or nested_call:
                arguments.append(serialized)
        if not arguments:
            raise RuntimeError(f"Browser target did not invoke Node REPL for {suite_scenario[0]}:{suite_scenario[1]}")
        call_count += len(arguments)
        activity = "\n".join(arguments).replace('\\"', '"').replace("\\'", "'")
        external_backend = re.search(r"browsers\.get\(\s*['\"]extension['\"]\s*\)|globalThis\.chrome", activity)
        destinations = re.findall(r"https?://[^\s'\"\\]+", activity)
        external_destination = any(
            (urlsplit(destination).hostname or "").lower() not in {"localhost", "127.0.0.1"}
            for destination in destinations
        )
        if external_backend or external_destination:
            raise RuntimeError(
                f"Browser target selected an external browser or destination for {suite_scenario[0]}:"
                f"{suite_scenario[1]}"
            )
        backend_unavailable_block = (
            statuses.get(suite_scenario) == "BLOCKED"
            and bool(re.search(r"browsers\.get\(\s*['\"]iab['\"]\s*\)", activity))
            and bool(re.search(r"Browser is not available:\s*iab", "\n".join(tool_results)))
            and not re.search(r"\.tabs\.new\(", activity)
        )
        if backend_unavailable_block:
            blocked_count += 1
            continue
        required_activity = {
            "in-app browser selection": bool(
                re.search(r"browsers\.get\(\s*['\"]iab['\"]\s*\)|browsers\.getForUrl\(", activity)
            ),
            "fresh tab": bool(re.search(r"\.tabs\.new\(", activity)),
            "browser interaction": ".playwright" in activity or ".cua" in activity,
            "tab cleanup": bool(re.search(r"\.close\(", activity)),
        }
        absent = [name for name, observed in required_activity.items() if not observed]
        if absent:
            raise RuntimeError(
                f"Browser target activity is incomplete for {suite_scenario[0]}:{suite_scenario[1]}: "
                f"missing {', '.join(absent)}"
            )
    return {
        "targetSessions": len(browser_scenarios),
        "nodeReplCalls": call_count,
        "blockedTargetSessions": blocked_count,
    }


def _controlled_environment(
    home: Path,
    codex_home: Path,
    temporary: Path,
    node_executable: Path | None = None,
    python_executable: Path | None = None,
) -> dict[str, str]:
    bundled_node = node_executable or _bundled_node_executable()
    bundled_python = python_executable or _bundled_python_executable()
    inherited_path = os.environ.get("PATH", "/usr/bin:/bin")
    environment = {
        "PATH": f"{bundled_python.parent}{os.pathsep}{bundled_node.parent}{os.pathsep}{inherited_path}"
    }
    for name in ("LANG", "LC_ALL"):
        if name in os.environ:
            environment[name] = os.environ[name]
    environment.update(
        {
            "HOME": str(home),
            "CODEX_HOME": str(codex_home),
            "TMPDIR": str(temporary),
            "GIT_AUTHOR_NAME": "Synthetic Agent Eval",
            "GIT_AUTHOR_EMAIL": "agent-eval@example.invalid",
            "GIT_COMMITTER_NAME": "Synthetic Agent Eval",
            "GIT_COMMITTER_EMAIL": "agent-eval@example.invalid",
        }
    )
    offline_maven_repository = home / ".m2" / "repository"
    if (offline_maven_repository / ".agent-suite-offline").is_file():
        environment["MAVEN_ARGS"] = f"--offline -Dmaven.repo.local={offline_maven_repository}"
    return environment


def _kill_process_group(pid: int) -> None:
    try:
        os.killpg(pid, signal.SIGKILL)
    except (PermissionError, ProcessLookupError):
        pass


def _process_parent_map() -> dict[int, int]:
    completed = subprocess.run(
        ["ps", "-axo", "pid=,ppid="],
        check=False,
        text=True,
        capture_output=True,
    )
    relationships: dict[int, int] = {}
    for line in completed.stdout.splitlines():
        fields = line.split()
        if len(fields) == 2 and all(field.isdigit() for field in fields):
            relationships[int(fields[0])] = int(fields[1])
    return relationships


def _record_descendants(root_pid: int, tracked: set[int]) -> None:
    relationships = _process_parent_map()
    changed = True
    tracked.add(root_pid)
    while changed:
        changed = False
        for pid, parent_pid in relationships.items():
            if parent_pid in tracked and pid not in tracked:
                tracked.add(pid)
                changed = True


def _pid_exists(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except (PermissionError, ProcessLookupError):
        return False
    return True


def _pids_with_environment_token(token: str) -> set[int]:
    completed = subprocess.run(
        ["ps", "eww", "-axo", "pid=,command="],
        check=False,
        text=True,
        capture_output=True,
    )
    needle = f"AGENT_SUITE_PROCESS_TOKEN={token}"
    pids: set[int] = set()
    for line in completed.stdout.splitlines():
        pid_text, separator, command = line.strip().partition(" ")
        if separator and pid_text.isdigit() and needle in command:
            pids.add(int(pid_text))
    return pids


def _pids_with_cwd_under(root: Path) -> set[int]:
    completed = subprocess.run(
        ["/usr/sbin/lsof", "-n", "-P", "-Fpn", "-a", "-d", "cwd"],
        check=False,
        text=True,
        capture_output=True,
    )
    current_pid: int | None = None
    pids: set[int] = set()
    resolved_root = root.resolve()
    for line in completed.stdout.splitlines():
        if line.startswith("p") and line[1:].isdigit():
            current_pid = int(line[1:])
        elif line.startswith("n") and current_pid is not None:
            try:
                Path(line[1:]).resolve().relative_to(resolved_root)
            except ValueError:
                continue
            pids.add(current_pid)
    return pids


def _stop_tracked_processes(
    root_pid: int,
    tracked: set[int],
    process_token: str,
    containment_root: Path | None,
) -> str:
    _record_descendants(root_pid, tracked)
    tracked.update(_pids_with_environment_token(process_token))
    if containment_root is not None:
        tracked.update(_pids_with_cwd_under(containment_root))
    retained = {pid for pid in tracked if pid != root_pid and _pid_exists(pid)}
    _kill_process_group(root_pid)
    for pid in retained:
        try:
            os.kill(pid, signal.SIGKILL)
        except (PermissionError, ProcessLookupError):
            pass
    deadline = time.monotonic() + 2.0
    while time.monotonic() < deadline and any(_pid_exists(pid) for pid in retained):
        time.sleep(0.02)
    survivors = {pid for pid in retained if _pid_exists(pid)}
    if survivors:
        return f"failed-surviving-pids:{','.join(str(pid) for pid in sorted(survivors))}"
    return "failed-retained-processes-recovered" if retained else "clean"


def _run_process(
    argv: Sequence[str],
    cwd: Path,
    environment: dict[str, str],
    timeout_seconds: float,
    containment_root: Path | None = None,
) -> dict[str, Any]:
    process_token = secrets.token_hex(24)
    child_environment = dict(environment)
    child_environment["AGENT_SUITE_PROCESS_TOKEN"] = process_token
    process = subprocess.Popen(
        list(argv),
        cwd=cwd,
        env=child_environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False,
        start_new_session=True,
    )
    buffers = {"stdout": bytearray(), "stderr": bytearray()}
    exceeded = threading.Event()
    tracking_stop = threading.Event()
    tracked_pids: set[int] = {process.pid}

    def track_descendants() -> None:
        while not tracking_stop.is_set():
            _record_descendants(process.pid, tracked_pids)
            tracked_pids.update(_pids_with_environment_token(process_token))
            tracking_stop.wait(0.05)
        _record_descendants(process.pid, tracked_pids)
        tracked_pids.update(_pids_with_environment_token(process_token))

    def drain(name: str, stream: Any) -> None:
        while True:
            chunk = stream.read(65536)
            if not chunk:
                return
            remaining = _MAXIMUM_CAPTURE_BYTES - len(buffers[name])
            if remaining > 0:
                buffers[name].extend(chunk[:remaining])
            if len(chunk) > remaining:
                exceeded.set()
                _kill_process_group(process.pid)

    threads = [
        threading.Thread(target=drain, args=("stdout", process.stdout), daemon=True),
        threading.Thread(target=drain, args=("stderr", process.stderr), daemon=True),
    ]
    tracker = threading.Thread(target=track_descendants, daemon=True)
    tracker.start()
    for thread in threads:
        thread.start()
    timed_out = False
    try:
        process.wait(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        _kill_process_group(process.pid)
        process.wait()
    finally:
        tracking_stop.set()
        tracker.join()
        cleanup = _stop_tracked_processes(process.pid, tracked_pids, process_token, containment_root)
    for thread in threads:
        thread.join()
    if process.stdout is not None:
        process.stdout.close()
    if process.stderr is not None:
        process.stderr.close()
    stdout = bytes(buffers["stdout"]).decode("utf-8", errors="replace")
    stderr = bytes(buffers["stderr"]).decode("utf-8", errors="replace")
    if timed_out:
        return {"exitCode": 124, "stdout": stdout, "stderr": f"{stderr}\nprocess timed out".lstrip(), "cleanup": cleanup}
    if exceeded.is_set():
        return {"exitCode": 125, "stdout": stdout, "stderr": f"{stderr}\nprocess output limit exceeded".lstrip(), "cleanup": cleanup}
    return {"exitCode": int(process.returncode), "stdout": stdout, "stderr": stderr, "cleanup": cleanup}


def _audit_workspace_cleanup(workspace: Path) -> str:
    registry = workspace / ".git" / "agent-claims.json"
    if registry.is_file():
        loaded = json.loads(registry.read_text(encoding="utf-8"))
        claims = loaded.get("claims", loaded) if isinstance(loaded, dict) else loaded
        if claims:
            raise RuntimeError("Disposable workspace retains active claims")
    return "clean"


def _run_live_batch(
    batch: Sequence[_RunSpec],
    batch_number: int,
    result_root: Path,
    timeout_seconds: int,
) -> dict[str, Any]:
    label = f"batch-{batch_number:02d}"
    with _temporary_run_root(label) as run_root:
        workspace, codex_home, staged = _stage_batch(batch, run_root)
        capabilities = _runtime_capabilities(batch)
        checkpoint_root = run_root / "checkpoints"
        checkpoint_root.mkdir()
        schema_path = run_root / "coordinator-output-schema.json"
        schema_path.write_text(json.dumps(_coordinator_schema(), indent=2) + "\n", encoding="utf-8")
        temporary_home = run_root / "home"
        temporary_dir = run_root / "tmp"
        maximum_threads = 10 if any(int(run.suite.manifest["execution"].get("nestedAgentLimit", 0)) == 1 for run in batch) else 9
        command = [
            str(_bundled_codex_executable()),
            *_multi_agent_runtime_arguments(maximum_threads),
            *_capability_runtime_arguments(capabilities, codex_home),
            "-c",
            "agents.max_depth=3",
            "--ask-for-approval",
            "never",
            "--add-dir",
            str(workspace / ".git"),
            "--add-dir",
            str(checkpoint_root),
            "--strict-config",
            *_agent_registration_arguments(staged, codex_home),
            "exec",
            "--json",
            "--ignore-rules",
            "--output-schema",
            str(schema_path),
            "-C",
            str(workspace),
            _coordinator_prompt(batch, checkpoint_root),
        ]
        environment = _controlled_environment(temporary_home, codex_home, temporary_dir)
        preflight_evidence = _preflight_runtime_capabilities(batch, workspace, codex_home, environment)
        completed = _run_process(
            command,
            workspace,
            environment,
            timeout_seconds,
            containment_root=run_root,
        )
        result_root.mkdir(parents=True, exist_ok=True)
        evidence_prefix = result_root / label
        evidence_prefix.with_suffix(".jsonl").write_text(_redact_capture(completed["stdout"]), encoding="utf-8")
        evidence_prefix.with_suffix(".stderr.log").write_text(_redact_capture(completed["stderr"]), encoding="utf-8")
        session_directory = result_root / f"{label}.sessions"
        retained_session_count = _retain_sessions(codex_home, session_directory)
        partial_report: dict[str, Any] | None = None
        report_error: str | None = None
        try:
            checkpoint_report = _load_checkpoint_report(checkpoint_root, batch)
        except (json.JSONDecodeError, RuntimeError) as checkpoint_error:
            checkpoint_report = None
            report_error = f"checkpoint error: {checkpoint_error}"
        try:
            partial_report = _extract_coordinator_report(completed["stdout"])
            _audit_report(batch, partial_report)
            _audit_checkpoint_agreement(partial_report, checkpoint_report, batch)
        except RuntimeError as error:
            report_error = f"{report_error}; {error}" if report_error else str(error)
            if checkpoint_report is not None:
                partial_report = checkpoint_report
        checkpoint_destination = result_root / f"{label}.checkpoints"
        if checkpoint_root.is_dir():
            shutil.copytree(checkpoint_root, checkpoint_destination, dirs_exist_ok=True)
        expected_invocation_counts = _expected_invocation_counts(batch, partial_report or {})
        identity_error: str | None = None
        try:
            identity = _audit_identity(staged, codex_home, expected_invocation_counts, batch, partial_report or {})
        except RuntimeError as error:
            identity_error = str(error)
            identity = {"rolloutCount": retained_session_count, "error": identity_error}
        browser_error: str | None = None
        try:
            browser_audit = _audit_browser_activity(codex_home, batch, identity, partial_report or {})
        except RuntimeError as error:
            browser_error = str(error)
            browser_audit = {"error": browser_error}
        concurrency_error: str | None = None
        try:
            concurrency = _audit_session_concurrency(_load_sessions(codex_home), maximum_threads, batch)
        except RuntimeError as error:
            concurrency_error = str(error)
            concurrency = {"error": concurrency_error}
        identity_path = evidence_prefix.with_suffix(".identity.json")
        identity_path.write_text(json.dumps(identity, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        cleanup_error: str | None = None
        try:
            workspace_cleanup = _audit_workspace_cleanup(workspace)
        except RuntimeError as error:
            cleanup_error = str(error)
            workspace_cleanup = "failed"
        infrastructure_errors = [
            message
            for message in (
                None if completed["exitCode"] == 0 else f"Codex exited with {completed['exitCode']}",
                None if completed["cleanup"] == "clean" else f"Process cleanup: {completed['cleanup']}",
                report_error,
                identity_error,
                browser_error,
                concurrency_error,
                cleanup_error,
            )
            if message
        ]
        return {
            "batch": batch_number,
            "status": "infrastructure-failed" if infrastructure_errors else "completed",
            "processExitCode": completed["exitCode"],
            "report": partial_report,
            "infrastructureErrors": infrastructure_errors,
            "identityAudit": identity,
            "browserAudit": browser_audit,
            "concurrencyAudit": concurrency,
            "workspaceCleanup": workspace_cleanup,
            "capabilityPreflight": list(preflight_evidence),
            "evidence": {
                "events": str(evidence_prefix.with_suffix(".jsonl")),
                "stderr": str(evidence_prefix.with_suffix(".stderr.log")),
                "identity": str(identity_path),
                "sessions": str(session_directory),
                "checkpoints": str(checkpoint_destination),
            },
        }


def _execute_batches(
    batches: Sequence[Sequence[_RunSpec]],
    execute: Callable[[tuple[_RunSpec, ...], int], dict[str, Any]],
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for batch_number, raw_batch in enumerate(batches, start=1):
        batch = tuple(raw_batch)
        started_at = _utc_now()
        started_monotonic = time.monotonic()
        try:
            result = dict(execute(batch, batch_number))
        except Exception as error:  # Preserve partial evidence and continue with later independent batches.
            result = {"batch": batch_number, "status": "infrastructure-failed", "error": str(error)}
        result["startedAtUtc"] = started_at
        result["finishedAtUtc"] = _utc_now()
        result["elapsedSeconds"] = round(time.monotonic() - started_monotonic, 6)
        result["suites"] = [run.suite.suite_id for run in batch]
        results.append(result)
    return results


def _argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run identity-gated conceptual-agent suites.")
    parser.add_argument("--suite", action="append", default=[], help="Suite id to run; repeat for multiple suites.")
    parser.add_argument(
        "--scenario",
        action="append",
        default=[],
        help="Scenario selector in suite-id:scenario-id form; repeat for multiple scenarios.",
    )
    parser.add_argument("--jobs", type=int, default=4, help="Maximum concurrent supervisors, from 1 through 4.")
    parser.add_argument("--timeout-seconds", type=int, default=3600, help="Wall-clock limit for each coordinator batch.")
    parser.add_argument("--validate-only", action="store_true", help="Validate and schedule suites without invoking Codex.")
    parser.add_argument("--list", action="store_true", help="List validated suites and scenarios, then exit.")
    parser.add_argument(
        "--result-dir",
        type=Path,
        default=_SUITE_ROOT / "run-evidence",
        help="Runner-owned evidence directory outside disposable workspaces.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Validate selections, execute bounded batches, and retain a machine-readable summary.

    Callers use the command-line flags to select suites or scenarios, cap supervisor concurrency,
    choose validation-only or live execution, and name the runner-owned evidence directory. Live
    execution creates isolated homes and workspaces, invokes Codex, records UTC and monotonic timing,
    retains partial failures, and removes disposable state before returning. The process returns zero
    only when every requested batch validates or completes without an infrastructure failure.
    """
    arguments = _argument_parser().parse_args(argv)
    selected_suite_ids = set(arguments.suite)
    selected_suite_ids.update(value.partition(":")[0] for value in arguments.scenario if ":" in value)
    catalog = _load_catalog(include_ids=selected_suite_ids or None)
    if arguments.list:
        for suite in sorted(catalog.values(), key=lambda item: item.priority):
            print(f"{suite.suite_id}: {', '.join(str(item['id']) for item in suite.scenarios)}")
        return 0
    runs = _select_runs(catalog, tuple(arguments.suite), tuple(arguments.scenario))
    batches = _batch_runs(runs, arguments.jobs)
    result_root = arguments.result_dir.resolve()
    if arguments.validate_only:
        def validate(batch: tuple[_RunSpec, ...], batch_number: int) -> dict[str, Any]:
            for run in batch:
                _validate_target_skills(run.suite, run.scenario_ids, _REPOSITORY_ROOT)
            return {"batch": batch_number, "status": "validated", "supervisorCount": len(batch)}

        results = _execute_batches(batches, validate)
    else:
        results = _execute_batches(
            batches,
            lambda batch, batch_number: _run_live_batch(
                batch,
                batch_number,
                result_root,
                arguments.timeout_seconds,
            ),
        )
    result_root.mkdir(parents=True, exist_ok=True)
    summary_path = result_root / "summary.json"
    summary = {
        "schema": "dev-methodology-agent-suite-run-summary",
        "version": 1,
        "generatedAtUtc": _utc_now(),
        "validateOnly": bool(arguments.validate_only),
        "maximumConcurrentSupervisors": arguments.jobs,
        "results": results,
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(summary_path)
    return 0 if all(result["status"] in {"validated", "completed"} for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
