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
import importlib.util
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
from collections.abc import Callable, Iterator, Mapping, Sequence
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlsplit

import yaml
import workspace_inventory as workspace_inventory_support


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
_EVIDENCE_RECEIPT_SCHEMA = "dev-methodology-agent-suite-evidence-receipt"
_WORKSPACE_MUTATION_SCHEMA = "dev-methodology-workspace-mutation-evidence"
_JUDGE_OUTPUT_SCHEMA = "dev-methodology-agent-suite-judge-output"
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
_IMMEDIATE_NOOP_CLOSE_SECONDS = 10.0


class _JunieEvidenceInsufficient(RuntimeError):
    """Signal that a Junie run must be BLOCKED because its ledger cannot prove topology."""

    def __init__(self, message: str, diagnostics: Mapping[str, Any] | None = None) -> None:
        super().__init__(message)
        self.diagnostics = dict(diagnostics or {})


_DEPENDENCY_ROUTING_FIXTURE_FIELDS = (
    "lanes.source.owner",
    "lanes.source.input",
    "lanes.source.requestedBehavior",
    "lanes.source.acceptanceCriteria",
    "lanes.source.verification",
    "lanes.documentation.owner",
    "lanes.documentation.input",
    "lanes.documentation.requestedBehavior",
    "lanes.documentation.acceptanceCriteria",
    "lanes.documentation.verification",
    "surfaces.fixture",
    "surfaces.source",
    "surfaces.documentation",
    "surfaces.generatedReadOnly",
    "surfaces.report",
    "orchestration.dependencyOrder",
    "orchestration.claims",
    "orchestration.integration",
    "orchestration.postIntegrationReviews",
    "orchestration.finalVerification",
    "orchestration.closeout",
    "handoffReceipt.requiredLanes",
    "handoffReceipt.requiredFields",
    "runtimeResources.python",
    "runtimeResources.model",
    "runtimeResources.externalNetwork",
)


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
    rollout_path: Path | None = None
    rollout_sha256: str | None = None
    terminal_response_index: int | None = None
    terminal_response: bytes | None = None
    terminal_response_error: str | None = None
    suite_exclusion_candidate: str | None = None


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


def _dotted_value(document: dict[str, Any], dotted_path: str) -> Any:
    """Return one nested mapping value, or None when any path component is absent."""
    value: Any = document
    for component in dotted_path.split("."):
        if not isinstance(value, dict) or component not in value:
            return None
        value = value[component]
    return value


def _validate_fixture_contract(suite: _Suite, scenario: dict[str, Any]) -> None:
    """Validate the dependency-routing fixture's required structured inputs."""
    relative = scenario.get("fixtureContract")
    if relative is None:
        return
    if not isinstance(relative, str) or not relative.strip():
        raise ValueError(f"{suite.suite_id}:{scenario.get('id', '')} has an invalid fixtureContract")
    path = (suite.path / relative).resolve()
    if suite.path.resolve() not in path.parents or not path.is_file():
        raise ValueError(f"{suite.suite_id}:{scenario.get('id', '')} has no fixture contract: {path}")
    contract = _load_yaml(path)
    identity = f"{suite.suite_id}:{scenario.get('id', '')}"
    for dotted_path in _DEPENDENCY_ROUTING_FIXTURE_FIELDS:
        value = _dotted_value(contract, dotted_path)
        if value is None or value == "" or value == [] or value == {}:
            raise ValueError(f"{identity} missing fixture field {dotted_path}")
    expected_lanes = scenario.get("requiredHandoffReceiptLanes", [])
    if expected_lanes and contract["handoffReceipt"]["requiredLanes"] != expected_lanes:
        raise ValueError(f"{identity} fixture handoffReceipt.requiredLanes disagrees with scenario")
    expected_fields = scenario.get("requiredHandoffReceiptFields", [])
    if expected_fields and contract["handoffReceipt"]["requiredFields"] != expected_fields:
        raise ValueError(f"{identity} fixture handoffReceipt.requiredFields disagrees with scenario")
    expected_order = scenario.get("requiredDependencyOrder", [])
    observed_order = [str(item.get("role", "")) for item in contract["orchestration"]["dependencyOrder"]]
    if expected_order and observed_order != expected_order:
        raise ValueError(f"{identity} fixture orchestration.dependencyOrder disagrees with scenario")


def _agent_dependencies(run: _RunSpec) -> tuple[str, ...]:
    """Return the fixed and selected task dependencies required by one run."""
    dependencies = {
        str(value)
        for value in run.suite.manifest.get("target", {}).get("allowedAgentDependencies", [])
    }
    selected = set(run.scenario_ids)
    dependencies.update(
        str(value)
        for scenario in run.suite.scenarios
        if str(scenario.get("id", "")) in selected
        for value in scenario.get("taskSelectedAgentDependencies", [])
    )
    return tuple(sorted(dependencies))


def _scenario_dependencies(suite: _Suite, scenario_id: str) -> tuple[str, ...]:
    """Return fixed dependencies plus only those selected by one scenario."""
    dependencies = {
        str(value) for value in suite.manifest.get("target", {}).get("allowedAgentDependencies", [])
    }
    scenario = next(value for value in suite.scenarios if str(value.get("id", "")) == scenario_id)
    dependencies.update(str(value) for value in scenario.get("taskSelectedAgentDependencies", []))
    return tuple(sorted(dependencies))


def _scenario_declared_values(run: _RunSpec, field: str) -> tuple[str, ...]:
    """Return the unique string values declared by selected scenarios for one field."""
    selected = set(run.scenario_ids)
    return tuple(
        sorted(
            {
                str(value)
                for scenario in run.suite.scenarios
                if str(scenario.get("id", "")) in selected
                for value in scenario.get(field, [])
            }
        )
    )


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
    selectable_dependencies = {
        str(value) for value in target.get("taskSelectableAgentDependencies", [])
    }
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
        requires_inventory = scenario.get("requiresWorkspaceInventory", False)
        if type(requires_inventory) is not bool:
            raise ValueError(
                f"{suite.suite_id}:{scenario_id} requiresWorkspaceInventory must be a boolean"
            )
        if requires_inventory and "no-forbidden-mutation" not in scenario.get(
            "deterministicChecks", []
        ):
            raise ValueError(
                f"{suite.suite_id}:{scenario_id} workspace inventory requires no-forbidden-mutation"
            )
        for field in (
            "taskSelectedAgentDependencies",
            "requiredDependencyOrder",
            "requiredHandoffReceiptLanes",
            "requiredHandoffReceiptFields",
        ):
            values = scenario.get(field, [])
            if not isinstance(values, list) or not all(isinstance(value, str) and value for value in values):
                raise ValueError(f"{suite.suite_id}:{scenario_id} {field} must be a list of strings")
        unknown_dependencies = set(scenario.get("taskSelectedAgentDependencies", [])) - selectable_dependencies
        if unknown_dependencies:
            raise ValueError(
                f"{suite.suite_id}:{scenario_id} selects undeclared task dependencies: "
                f"{', '.join(sorted(unknown_dependencies))}"
            )
        allowed_dependencies = {
            str(value) for value in target.get("allowedAgentDependencies", [])
        } | set(scenario.get("taskSelectedAgentDependencies", []))
        unknown_order = set(scenario.get("requiredDependencyOrder", [])) - allowed_dependencies
        if unknown_order:
            raise ValueError(
                f"{suite.suite_id}:{scenario_id} orders undeclared dependencies: "
                f"{', '.join(sorted(unknown_order))}"
            )
        _validate_fixture_contract(suite, scenario)
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
        nested_enabled = int(run.suite.manifest["execution"].get("nestedAgentLimit", 0)) > 0
        nested_already_enabled = any(
            int(value.suite.manifest["execution"].get("nestedAgentLimit", 0)) > 0
            for value in ordinary
        )
        if nested_enabled and nested_already_enabled:
            batches.append(tuple(ordinary))
            ordinary = []
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


def _bundled_junie_executable() -> Path:
    configured = os.environ.get("JUNIE_CLI")
    discovered = shutil.which("junie")
    candidates = [*([Path(configured)] if configured else []), *([Path(discovered)] if discovered else [])]
    for candidate in candidates:
        resolved = candidate.expanduser().resolve()
        if resolved.is_file() and os.access(resolved, os.X_OK):
            return resolved
    raise RuntimeError("The managed Junie CLI is unavailable")


def _copy_junie_agent(
    source: Path,
    invocation: str,
    agent_root: Path,
    invocation_bindings: Mapping[str, str],
) -> _StagedAgent:
    junie_name = invocation.replace("_", "-")
    if not re.fullmatch(r"[a-z][a-z0-9-]*", junie_name):
        raise ValueError(f"Invalid staged Junie agent invocation: {junie_name}")
    source_text = source.read_text(encoding="utf-8")
    if source.suffix == ".toml":
        loaded = tomllib.loads(source_text)
        instructions = str(loaded.get("developer_instructions", ""))
        description = str(loaded.get("description", f"Governed {junie_name} evaluation agent."))
        if not instructions:
            raise ValueError(f"Staged Junie agent has no instructions: {source}")
        instructions = re.sub(
            r"generated/adapters/codex/agents/([a-z0-9-]+)\.toml",
            r"generated/adapters/junie/agents/\1.md",
            instructions,
        )
        instructions = instructions.replace("Codex adapter", "Junie native adapter")
        instructions = instructions.replace("Codex agent", "Junie custom agent")
        instructions = re.sub(
            r"by passing agent_type exactly ([a-z0-9_]+) and fork_context exactly false to spawn_agent",
            lambda match: (
                "by delegating only to the Junie custom agent named "
                f"{invocation_bindings.get(match.group(1), match.group(1).replace('_', '-'))} "
                "in a fresh independent context"
            ),
            instructions,
        )
        instructions = re.sub(
            r"by passing agent_type exactly ([a-z0-9_]+) and fork_context exactly false",
            lambda match: (
                "by delegating only to the Junie custom agent named "
                f"{invocation_bindings.get(match.group(1), match.group(1).replace('_', '-'))} "
                "in a fresh independent context"
            ),
            instructions,
        )
        for codex_name, bound_name in sorted(
            invocation_bindings.items(), key=lambda item: len(item[0]), reverse=True
        ):
            instructions = re.sub(
                rf"(?<![A-Za-z0-9_]){re.escape(codex_name)}(?![A-Za-z0-9_])",
                bound_name,
                instructions,
            )
        binding_summary = ", ".join(sorted(set(invocation_bindings.values())))
        instructions += (
            "\n\nJunie runtime authority: use the generated native definitions under "
            "generated/adapters/junie/agents, never the Codex adapter tree. "
            f"The complete governed runtime-name allowlist is: {binding_summary}."
        )
        frontmatter = yaml.safe_dump(
            {"name": junie_name, "description": description, "model": "opus", "reasoningLevel": "high"},
            sort_keys=False,
        ).strip()
        rendered = f"---\n{frontmatter}\n---\n\n{instructions.strip()}\n"
    else:
        rendered = source_text
        loaded_frontmatter = yaml.safe_load(rendered.split("---", 2)[1])
        if not isinstance(loaded_frontmatter, dict):
            raise ValueError(f"Staged Junie agent frontmatter is invalid: {source}")
        instructions = rendered.split("---", 2)[2].strip()
        loaded_frontmatter["name"] = junie_name
        rendered = f"---\n{yaml.safe_dump(loaded_frontmatter, sort_keys=False).strip()}\n---\n{instructions}\n"
    marker = f"AGENT-INSTRUCTION-BINDING-{junie_name}-{secrets.token_hex(16)}"
    rendered += f"\nRuntime instruction binding marker retained by the harness: {marker}.\n"
    destination = agent_root / f"{junie_name}.md"
    destination.write_text(rendered, encoding="utf-8")
    return _StagedAgent(junie_name, source, instructions, _sha256(destination), marker)


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
        for dependency in _agent_dependencies(run):
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


def _stage_junie_batch(batch: Sequence[_RunSpec], run_root: Path) -> tuple[Path, Path, Path, tuple[_StagedAgent, ...]]:
    workspace = run_root / "workspace"
    junie_home = run_root / "junie-home"
    agent_root = run_root / "junie-agents"
    skill_root = run_root / "junie-skills"
    home_root = run_root / "home"
    for path in (junie_home, agent_root, skill_root, home_root, run_root / "tmp"):
        path.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["git", "clone", "--quiet", "--no-hardlinks", str(_REPOSITORY_ROOT), str(workspace)],
        check=True,
        text=True,
        capture_output=True,
    )
    _stage_offline_project_dependencies(batch, _REPOSITORY_ROOT, workspace)
    _stage_offline_maven_dependencies(batch, _REPOSITORY_ROOT, workspace, home_root)
    if _runtime_capabilities(batch) & frozenset({"browser-automation"}):
        raise RuntimeError("Junie browser-automation agent suites require an externally approved browser adapter")
    invocation_bindings: dict[str, str] = {}
    for run in batch:
        execution = run.suite.manifest["execution"]
        for field in ("supervisorInvocation", "targetInvocation", "judgeInvocation"):
            value = str(execution[field])
            invocation_bindings[value] = value.replace("_", "-")
        for dependency in run.suite.manifest["target"].get("allowedAgentDependencies", []):
            value = str(dependency).replace("-", "_")
            invocation_bindings[value] = value.replace("_", "-")
    staged: dict[str, _StagedAgent] = {}
    for run in batch:
        suite = run.suite
        _validate_target_skills(suite, run.scenario_ids, _REPOSITORY_ROOT)
        manifest = suite.manifest
        execution = manifest["execution"]
        project_agents = manifest["projectAgents"]
        codex_target = Path(str(manifest["target"]["nativeAgent"]))
        junie_target = _REPOSITORY_ROOT / Path(
            str(codex_target).replace("generated/adapters/codex/agents/", "generated/adapters/junie/agents/")
        ).with_suffix(".md")
        sources = (
            (suite.path / project_agents["supervisor"], execution["supervisorInvocation"]),
            (junie_target, execution["targetInvocation"]),
            (suite.path / project_agents["judge"], execution["judgeInvocation"]),
        )
        for source, invocation in sources:
            junie_invocation = str(invocation).replace("_", "-")
            if junie_invocation not in staged:
                staged[junie_invocation] = _copy_junie_agent(
                    source, str(invocation), agent_root, invocation_bindings
                )
        for dependency in manifest["target"].get("allowedAgentDependencies", []):
            invocation = str(dependency).replace("_", "-")
            source = _REPOSITORY_ROOT / "generated" / "adapters" / "junie" / "agents" / f"{dependency}.md"
            if invocation not in staged:
                staged[invocation] = _copy_junie_agent(
                    source, str(dependency), agent_root, invocation_bindings
                )
        for skill_path in manifest.get("projectSkills", {}).get("shared", []) + manifest.get("projectSkills", {}).get("suite", []):
            _copy_skill_package(suite.path / skill_path, skill_root)
        selected = set(run.scenario_ids)
        scenario_skills = {
            str(skill)
            for scenario in suite.scenarios
            if str(scenario["id"]) in selected
            for skill in scenario.get("targetSkills", [])
        }
        for skill_name in scenario_skills:
            _copy_skill_package(_REPOSITORY_ROOT / "skills" / skill_name / "SKILL.md", skill_root)
    return workspace, junie_home, skill_root, tuple(staged.values())


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
                                    "deterministicEvidence",
                                    "modelJudgeEvidence",
                                    "evidenceReceipts",
                                    "cleanup",
                                    "evidence",
                                ],
                                "properties": {
                                    "scenario": {"type": "string"},
                                    "status": {"type": "string", "enum": sorted(_REPORT_STATUSES)},
                                    "targetInvoked": {"type": "boolean"},
                                    "judgeInvoked": {"type": "boolean"},
                                    "identityEvidence": {"type": "array", "items": {"type": "string"}},
                                    "deterministicEvidence": {"type": "array", "items": {"type": "string"}},
                                    "modelJudgeEvidence": {"type": "array", "items": {"type": "string"}},
                                    "evidenceReceipts": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "additionalProperties": False,
                                            "required": ["path", "sha256"],
                                            "properties": {
                                                "path": {"type": "string"},
                                                "sha256": {
                                                    "type": "string",
                                                    "pattern": "^[0-9a-f]{64}$",
                                                },
                                            },
                                        },
                                    },
                                    "cleanup": {"type": "string", "enum": ["clean", "failed"]},
                                    "evidence": {"type": "array", "items": {"type": "string"}},
                                    "handoffReceipts": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "additionalProperties": False,
                                            "required": [
                                                "lane",
                                                "role",
                                                "commit",
                                                "review",
                                                "verification",
                                                "claimRelease",
                                            ],
                                            "properties": {
                                                "lane": {"type": "string"},
                                                "role": {
                                                    "type": "object",
                                                    "additionalProperties": False,
                                                    "required": ["invocation", "sessionIds"],
                                                    "properties": {
                                                        "invocation": {"type": "string"},
                                                        "sessionIds": {
                                                            "type": "array",
                                                            "minItems": 1,
                                                            "items": {"type": "string"},
                                                        },
                                                    },
                                                },
                                                "commit": {
                                                    "type": "object",
                                                    "additionalProperties": False,
                                                    "required": ["repository", "sha"],
                                                    "properties": {
                                                        "repository": {"type": "string"},
                                                        "sha": {"type": "string"},
                                                    },
                                                },
                                                "review": {
                                                    "type": "object",
                                                    "additionalProperties": False,
                                                    "required": ["sessionIds"],
                                                    "properties": {
                                                        "sessionIds": {
                                                            "type": "array",
                                                            "minItems": 1,
                                                            "items": {"type": "string"},
                                                        }
                                                    },
                                                },
                                                "verification": {
                                                    "type": "object",
                                                    "additionalProperties": False,
                                                    "required": ["sessionIds"],
                                                    "properties": {
                                                        "sessionIds": {
                                                            "type": "array",
                                                            "minItems": 1,
                                                            "items": {"type": "string"},
                                                        }
                                                    },
                                                },
                                                "claimRelease": {
                                                    "type": "object",
                                                    "additionalProperties": False,
                                                    "required": ["eventIds"],
                                                    "properties": {
                                                        "eventIds": {
                                                            "type": "array",
                                                            "minItems": 1,
                                                            "items": {"type": "string"},
                                                        }
                                                    },
                                                },
                                            },
                                        },
                                    },
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


def _coordinator_prompt(
    batch: Sequence[_RunSpec],
    checkpoint_root: Path,
    fixture_root: Path,
    run_identity: str,
) -> str:
    assignments = []
    for run in batch:
        execution = run.suite.manifest["execution"]
        assignments.append(
            {
                "suite": run.suite.suite_id,
                "runIdentity": run_identity,
                "supervisor": execution["supervisorInvocation"],
                "target": execution["targetInvocation"],
                "judge": execution["judgeInvocation"],
                "scenarios": list(run.scenario_ids),
                "nestedAgentLimit": int(execution.get("nestedAgentLimit", 0)),
                "runtimeCapabilities": sorted(_runtime_capabilities((run,))),
                "checkpointRoot": str(checkpoint_root),
                "fixtureRoot": str(fixture_root / run.suite.suite_id),
                "workspaceInventoryRoots": {
                    str(scenario["id"]): str(
                        fixture_root / run.suite.suite_id / str(scenario["id"])
                    )
                    for scenario in run.suite.scenarios
                    if str(scenario["id"]) in set(run.scenario_ids)
                    and scenario.get("requiresWorkspaceInventory") is True
                },
                "agentDependencies": list(_agent_dependencies(run)),
                "fixtureContracts": [
                    str(scenario["fixtureContract"])
                    for scenario in run.suite.scenarios
                    if str(scenario["id"]) in set(run.scenario_ids) and scenario.get("fixtureContract")
                ],
                "requiredHandoffReceiptLanes": list(
                    _scenario_declared_values(run, "requiredHandoffReceiptLanes")
                ),
                "requiredHandoffReceiptFields": list(
                    _scenario_declared_values(run, "requiredHandoffReceiptFields")
                ),
                "dependencyOrderByScenario": {
                    str(scenario["id"]): list(scenario.get("requiredDependencyOrder", []))
                    for scenario in run.suite.scenarios
                    if str(scenario["id"]) in set(run.scenario_ids)
                },
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
        "and create every suite-owned candidate repository, worktree, or fixture beneath its listed fixtureRoot, "
        "never under /tmp or /private/tmp. The fixtureRoot is inside the coordinator workspace so target and dependency "
        "patch operations remain within the approved write boundary. "
        "write the required checkpointRoot/suite-id/scenario-id.json checkpoint immediately after each terminal "
        "scenario and before starting later work. Each checkpoint must contain suite, scenario, status, targetInvoked, "
        "judgeInvoked, identityEvidence, deterministicEvidence, modelJudgeEvidence, and evidence as arrays of "
        "diagnostic strings, evidenceReceipts as an array of exact path and lowercase SHA-256 references, cleanup as clean or "
        "failed, residualRisk as a string, and any assignment-declared handoffReceipts as structured objects with "
        "the declared lanes and fields. Each receipt role must contain the producer invocation and its exact retained "
        "sessionIds. Each receipt commit must contain repository relative to its suite fixtureRoot "
        "and an ancestor commit sha; review and verification must each contain retained dependency sessionIds; "
        "claimRelease must contain successful fixture claim-journal eventIds whose resulting commit and agent match "
        "the receipt. Keep each clean candidate repository and its Git claim journal available until the outer runner "
        "audits them. Prose cannot substitute for those receipts. Nested objects are forbidden in the diagnostic arrays. "
        "The diagnostic strings never prove a verdict. Beneath checkpointRoot/suite/scenario, retain one artifacts file and "
        "one receipts JSON file per configured deterministic check. Each deterministic-check-disposition receipt must bind "
        "schema dev-methodology-agent-suite-evidence-receipt version 1, the assignment runIdentity, suite, scenario, exact "
        "checkId, catalog critical boolean, passed or failed verdict, and a relative artifacts path with its SHA-256. Retain "
        "each configured check exactly once. When Judge runs, instruct that exact Judge child to return only one compact JSON "
        "object with exactly schema dev-methodology-agent-suite-judge-output, version 1, runIdentity, suite, scenario, "
        "judgeInvocation, and disposition. The Judge must use passed, failed, blocked, or stale as disposition and return no "
        "fence, commentary, or trailing newline. Preserve those exact Judge output_text bytes verbatim as the Judge output "
        "artifact, then retain one judge-disposition receipt that binds that artifact and the same identity fields. When an authorized critical deterministic "
        "failure skips Judge, retain one judge-skip-disposition receipt binding the same exact failed checkId, critical true, "
        "deterministicVerdict failed, disposition skipped-critical-failure, and the same evidence artifact. Receipt paths must "
        "be directly beneath suite/scenario/receipts and artifact paths directly beneath suite/scenario/artifacts. "
        "Each result must state "
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


def _junie_coordinator_prompt(
    batch: Sequence[_RunSpec],
    checkpoint_root: Path,
    fixture_root: Path,
    run_identity: str,
) -> str:
    prompt = _coordinator_prompt(batch, checkpoint_root, fixture_root, run_identity)
    for run in batch:
        execution = run.suite.manifest["execution"]
        for field in ("supervisorInvocation", "targetInvocation", "judgeInvocation"):
            invocation = str(execution[field])
            prompt = prompt.replace(invocation, invocation.replace("_", "-"))
    return prompt.replace(
        "using agent_type exactly equal to its supervisor value and fork_context exactly false",
        "by routing to the custom agent whose name is exactly its supervisor value in a fresh context",
    ).replace(
        "pass agent_type exactly equal to the listed target or judge and fork_context exactly false for those child spawns",
        "route to the custom agent named exactly by the listed target or judge in a fresh context",
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


def _retained_artifact(
    root: Path,
    reference: object,
    expected_parent: PurePosixPath,
    field: str,
    diagnostics: list[str],
) -> Path | None:
    if not isinstance(reference, Mapping) or set(reference) != {"path", "sha256"}:
        diagnostics.append(f"{field} must contain exactly path and sha256")
        return None
    relative_value = reference.get("path")
    digest = reference.get("sha256")
    if (
        not isinstance(relative_value, str)
        or not relative_value
        or "\\" in relative_value
        or PurePosixPath(relative_value).is_absolute()
        or any(part in {"", ".", ".."} for part in PurePosixPath(relative_value).parts)
    ):
        diagnostics.append(f"{field} path is not a safe retained relative path")
        return None
    relative = PurePosixPath(relative_value)
    if relative.parent != expected_parent:
        diagnostics.append(
            f"{field} path must be directly beneath {expected_parent.as_posix()}"
        )
        return None
    if not isinstance(digest, str) or not _SHA256_PATTERN.fullmatch(digest):
        diagnostics.append(f"{field} sha256 must be a lowercase SHA-256 digest")
        return None
    candidate = root.joinpath(*relative.parts)
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            diagnostics.append(f"{field} path contains a symbolic link: {relative_value}")
            return None
    try:
        resolved_root = root.resolve(strict=True)
        resolved = candidate.resolve(strict=True)
    except (OSError, RuntimeError):
        diagnostics.append(f"{field} retained artifact is missing: {relative_value}")
        return None
    if resolved_root not in resolved.parents or not resolved.is_file():
        diagnostics.append(f"{field} retained artifact is unsafe: {relative_value}")
        return None
    if _sha256(resolved) != digest:
        diagnostics.append(f"{field} retained artifact digest mismatch: {relative_value}")
        return None
    return resolved


def _json_mapping(path: Path, field: str, diagnostics: list[str]) -> Mapping[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        diagnostics.append(f"{field} must be a retained JSON object: {path.name}")
        return None
    if not isinstance(value, Mapping):
        diagnostics.append(f"{field} must be a retained JSON object: {path.name}")
        return None
    return value


def _deterministic_check_catalog() -> dict[str, bool]:
    document = _load_yaml(_REPOSITORY_ROOT / "evals" / "judges.yaml")
    return {
        str(item["id"]): bool(item["critical"])
        for item in document.get("checks", [])
        if isinstance(item, Mapping)
        and isinstance(item.get("id"), str)
        and isinstance(item.get("critical"), bool)
    }


def _validate_workspace_mutation_evidence(
    evidence: Mapping[str, Any],
    field: str,
    diagnostics: list[str],
    expected_root: Path | None = None,
) -> None:
    expected_fields = {
        "schema",
        "version",
        "root",
        "baseline",
        "baselineSha256",
        "observed",
        "observedSha256",
        "detected",
        "derivedMutationClaim",
        "preExisting",
        "cleanup",
        "final",
        "finalSha256",
        "remaining",
        "finalMatchesBaseline",
    }
    change_fields = {"created", "modified", "deleted", "gitMetadata"}
    baseline = evidence.get("baseline")
    observed = evidence.get("observed")
    detected = evidence.get("detected")
    remaining = evidence.get("remaining")
    cleanup = evidence.get("cleanup")
    pre_existing = evidence.get("preExisting")
    final = evidence.get("final")
    def valid_inventory(value: object) -> bool:
        if not isinstance(value, Mapping) or set(value) != {
            "schema", "version", "root", "git", "entries"
        }:
            return False
        git = value.get("git")
        if (
            value.get("schema") != "dev-methodology-workspace-inventory"
            or value.get("version") != 1
            or value.get("root") != evidence.get("root")
            or not isinstance(git, Mapping)
            or set(git) != {"head", "symbolicHead", "indexSha256", "refsSha256"}
            or not isinstance(git.get("head"), str)
            or re.fullmatch(r"[0-9a-f]{40,64}", str(git.get("head"))) is None
            or git.get("symbolicHead") is not None
            and not isinstance(git.get("symbolicHead"), str)
            or any(
                not isinstance(git.get(key), str)
                or _SHA256_PATTERN.fullmatch(str(git.get(key))) is None
                for key in ("indexSha256", "refsSha256")
            )
            or not isinstance(value.get("entries"), list)
        ):
            return False
        seen: set[str] = set()
        for entry in value["entries"]:
            if not isinstance(entry, Mapping):
                return False
            path = entry.get("path")
            kind = entry.get("kind")
            relative = PurePosixPath(str(path)) if isinstance(path, str) else None
            if (
                relative is None
                or relative.is_absolute()
                or any(part in {"", ".", ".."} for part in relative.parts)
                or path in seen
                or re.fullmatch(r"[0-7]{4}", str(entry.get("mode"))) is None
            ):
                return False
            seen.add(path)
            if kind == "directory":
                if set(entry) != {"path", "kind", "mode"}:
                    return False
            elif kind in {"file", "symlink"}:
                if (
                    set(entry) != {"path", "kind", "mode", "sha256", "gitState"}
                    or _SHA256_PATTERN.fullmatch(str(entry.get("sha256"))) is None
                    or entry.get("gitState") not in {"tracked", "ignored", "untracked"}
                ):
                    return False
            else:
                return False
        return True

    valid_inventories = all(valid_inventory(value) for value in (baseline, observed, final))
    recomputed_detected = (
        workspace_inventory_support._changes(dict(baseline), dict(observed))
        if valid_inventories
        else None
    )
    recomputed_remaining = (
        workspace_inventory_support._changes(dict(baseline), dict(final))
        if valid_inventories
        else None
    )
    valid_changes = (
        isinstance(detected, Mapping)
        and isinstance(remaining, Mapping)
        and dict(detected) == recomputed_detected
        and dict(remaining) == recomputed_remaining
    )
    has_detected_changes = valid_changes and any(detected[key] for key in change_fields)
    has_remaining_changes = valid_changes and any(remaining[key] for key in change_fields)
    expected_claim = "side-effects-detected" if has_detected_changes else "no-changes-detected"
    created_paths = {
        str(entry.get("path"))
        for entry in detected.get("created", [])
        if isinstance(entry, Mapping) and isinstance(entry.get("path"), str)
    } if isinstance(detected, Mapping) else set()
    removed_paths = set(cleanup.get("removed", [])) if isinstance(cleanup, Mapping) else set()
    preserved_paths = set(cleanup.get("preserved", [])) if isinstance(cleanup, Mapping) else set()
    cleanup_requested = cleanup.get("requested") if isinstance(cleanup, Mapping) else None
    cleanup_accounts_for_created = (
        cleanup_requested is True
        and not (removed_paths & preserved_paths)
        and removed_paths | preserved_paths == created_paths
    ) or (cleanup_requested is False and not removed_paths and not preserved_paths)
    final_digest = (
        hashlib.sha256(
            json.dumps(final, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        if isinstance(final, Mapping)
        else None
    )
    valid = (
        set(evidence) == expected_fields
        and evidence.get("schema") == _WORKSPACE_MUTATION_SCHEMA
        and evidence.get("version") == 1
        and isinstance(evidence.get("root"), str)
        and bool(evidence.get("root"))
        and (expected_root is None or evidence.get("root") == str(expected_root.resolve(strict=True)))
        and isinstance(evidence.get("baselineSha256"), str)
        and _SHA256_PATTERN.fullmatch(str(evidence.get("baselineSha256"))) is not None
        and isinstance(evidence.get("finalSha256"), str)
        and _SHA256_PATTERN.fullmatch(str(evidence.get("finalSha256"))) is not None
        and valid_changes
        and valid_inventories
        and evidence.get("baselineSha256")
        == hashlib.sha256(
            json.dumps(baseline, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        and evidence.get("observedSha256")
        == hashlib.sha256(
            json.dumps(observed, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        and evidence.get("derivedMutationClaim") == expected_claim
        and isinstance(pre_existing, Mapping)
        and set(pre_existing) == {"ignored", "untracked"}
        and all(
            isinstance(pre_existing[key], list)
            and all(isinstance(path, str) and path for path in pre_existing[key])
            for key in ("ignored", "untracked")
        )
        and isinstance(cleanup, Mapping)
        and set(cleanup) == {"requested", "removed", "preserved"}
        and type(cleanup.get("requested")) is bool
        and all(
            isinstance(cleanup.get(key), list)
            and all(isinstance(path, str) and path for path in cleanup[key])
            for key in ("removed", "preserved")
        )
        and cleanup_accounts_for_created
        and evidence.get("finalSha256") == final_digest
        and type(evidence.get("finalMatchesBaseline")) is bool
        and evidence.get("finalMatchesBaseline") is (not has_remaining_changes)
    )
    if not valid:
        diagnostics.append(f"{field} is not a complete workspace mutation inventory")


def _validate_evidence_receipts(
    checkpoint_root: Path,
    references: object,
    run: _RunSpec,
    scenario_id: str,
    run_identity: str,
    reported_status: str,
    judge_invoked: bool,
    require_runtime_judge_provenance: bool,
    fixture_root: Path | None = None,
) -> dict[str, Any]:
    diagnostics: list[str] = []
    if not isinstance(references, list):
        references = []
        diagnostics.append("evidenceReceipts must be an array of path and SHA-256 references")
    scenario = next(
        (value for value in run.suite.scenarios if str(value.get("id")) == scenario_id),
        {},
    )
    raw_check_ids = scenario.get("deterministicChecks", [])
    expected_check_ids = [str(value) for value in raw_check_ids] if isinstance(raw_check_ids, list) else []
    if not expected_check_ids or len(expected_check_ids) != len(set(expected_check_ids)):
        diagnostics.append("selected scenario deterministicChecks must identify unique checks")
    catalog = _deterministic_check_catalog()
    unknown_checks = sorted(set(expected_check_ids) - set(catalog))
    if unknown_checks:
        diagnostics.append(f"selected scenario uses unknown deterministic checks: {', '.join(unknown_checks)}")
    receipt_parent = PurePosixPath(run.suite.suite_id, scenario_id, "receipts")
    artifact_parent = PurePosixPath(run.suite.suite_id, scenario_id, "artifacts")
    deterministic: dict[str, Mapping[str, Any]] = {}
    judge_receipts: list[Mapping[str, Any]] = []
    judge_output_reference: Mapping[str, Any] | None = None
    skip_receipts: list[Mapping[str, Any]] = []
    seen_paths: set[str] = set()
    for index, reference in enumerate(references):
        field = f"evidenceReceipts[{index}]"
        path_value = reference.get("path") if isinstance(reference, Mapping) else None
        if isinstance(path_value, str) and path_value in seen_paths:
            diagnostics.append(f"duplicate evidence receipt path: {path_value}")
            continue
        if isinstance(path_value, str):
            seen_paths.add(path_value)
        receipt_path = _retained_artifact(
            checkpoint_root,
            reference,
            receipt_parent,
            field,
            diagnostics,
        )
        if receipt_path is None:
            continue
        receipt = _json_mapping(receipt_path, field, diagnostics)
        if receipt is None:
            continue
        if (
            receipt.get("schema") != _EVIDENCE_RECEIPT_SCHEMA
            or receipt.get("version") != 1
            or receipt.get("runIdentity") != run_identity
            or receipt.get("suite") != run.suite.suite_id
            or receipt.get("scenario") != scenario_id
        ):
            diagnostics.append(f"{field} receipt identity mismatch")
            continue
        event_type = receipt.get("eventType")
        evidence_path = _retained_artifact(
            checkpoint_root,
            receipt.get("evidence"),
            artifact_parent,
            f"{field}.evidence",
            diagnostics,
        )
        if evidence_path is None:
            continue
        if event_type == "deterministic-check-disposition":
            expected_fields = {
                "schema", "version", "eventType", "runIdentity", "suite", "scenario",
                "checkId", "critical", "verdict", "evidence",
            }
            check_id = receipt.get("checkId")
            if set(receipt) != expected_fields:
                diagnostics.append(f"{field} deterministic receipt fields are malformed")
            if not isinstance(check_id, str) or check_id not in expected_check_ids:
                diagnostics.append(f"{field} deterministic check identity is not selected: {check_id}")
                continue
            if check_id in deterministic:
                diagnostics.append(f"duplicate deterministic check receipt: {check_id}")
                continue
            if receipt.get("critical") is not catalog.get(check_id):
                diagnostics.append(f"{field} deterministic criticality mismatch: {check_id}")
            if receipt.get("verdict") not in {"passed", "failed"}:
                diagnostics.append(f"{field} deterministic verdict is invalid: {check_id}")
            if check_id == "no-forbidden-mutation" and scenario.get("requiresWorkspaceInventory") is True:
                inventory = _json_mapping(evidence_path, f"{field}.evidence", diagnostics)
                if inventory is not None:
                    expected_inventory_root = (
                        fixture_root / run.suite.suite_id / scenario_id
                        if fixture_root is not None
                        else None
                    )
                    if expected_inventory_root is not None and not expected_inventory_root.is_dir():
                        diagnostics.append(
                            f"{field}.evidence protected workspace is missing: {expected_inventory_root}"
                        )
                        expected_inventory_root = None
                    _validate_workspace_mutation_evidence(
                        inventory,
                        f"{field}.evidence",
                        diagnostics,
                        expected_inventory_root,
                    )
                    if expected_inventory_root is not None:
                        actual_final = workspace_inventory_support._inventory(expected_inventory_root)
                        if inventory.get("final") != actual_final:
                            diagnostics.append(
                                f"{field}.evidence final inventory does not match the protected workspace"
                            )
                if (
                    inventory is not None
                    and receipt.get("verdict") == "passed"
                    and inventory.get("finalMatchesBaseline") is not True
                ):
                    diagnostics.append(
                        f"{field} no-forbidden-mutation passed without restoring the baseline inventory"
                    )
            deterministic[check_id] = receipt
        elif event_type == "judge-disposition":
            expected_fields = {
                "schema", "version", "eventType", "runIdentity", "suite", "scenario",
                "judgeInvocation", "disposition", "evidence",
            }
            if set(receipt) != expected_fields:
                diagnostics.append(f"{field} Judge receipt fields are malformed")
            judge_receipts.append(receipt)
            judge_output_reference = receipt.get("evidence")
            output = _json_mapping(evidence_path, f"{field}.evidence", diagnostics)
            expected_output = {
                "schema": _JUDGE_OUTPUT_SCHEMA,
                "version": 1,
                "runIdentity": run_identity,
                "suite": run.suite.suite_id,
                "scenario": scenario_id,
                "judgeInvocation": run.suite.manifest["execution"]["judgeInvocation"],
                "disposition": receipt.get("disposition"),
            }
            if output is not None and dict(output) != expected_output:
                diagnostics.append(f"{field} does not bind an actual selected Judge disposition")
        elif event_type == "judge-skip-disposition":
            expected_fields = {
                "schema", "version", "eventType", "runIdentity", "suite", "scenario",
                "checkId", "critical", "deterministicVerdict", "disposition", "evidence",
            }
            if set(receipt) != expected_fields:
                diagnostics.append(f"{field} Judge-skip receipt fields are malformed")
            skip_receipts.append(receipt)
        else:
            diagnostics.append(f"{field} receipt eventType is invalid: {event_type}")

    observed_checks = set(deterministic)
    expected_checks = set(expected_check_ids)
    if observed_checks != expected_checks:
        diagnostics.append(
            "deterministic receipt coverage mismatch: "
            f"expected {sorted(expected_checks)}, observed {sorted(observed_checks)}"
        )
    failed_critical = sorted(
        check_id
        for check_id, receipt in deterministic.items()
        if receipt.get("critical") is True and receipt.get("verdict") == "failed"
    )
    if reported_status == "PASS" and any(
        receipt.get("verdict") != "passed" for receipt in deterministic.values()
    ):
        diagnostics.append("PASS is incompatible with a failed deterministic receipt")
    judge_disposition: str | None = None
    failed_critical_check: str | None = None
    if judge_invoked:
        if len(judge_receipts) != 1:
            diagnostics.append("an invoked Judge requires exactly one Judge disposition receipt")
        if skip_receipts:
            diagnostics.append("an invoked Judge cannot retain a Judge-skip disposition")
        if judge_receipts:
            judge_receipt = judge_receipts[0]
            judge_disposition = str(judge_receipt.get("disposition"))
            expected_judge = str(run.suite.manifest["execution"]["judgeInvocation"])
            if judge_receipt.get("judgeInvocation") != expected_judge:
                diagnostics.append("Judge receipt invocation does not match the selected Judge")
            expected_disposition = {
                "PASS": "passed",
                "FAIL": "failed",
                "BLOCKED": "blocked",
                "STALE": "stale",
            }.get(reported_status)
            if judge_disposition != expected_disposition:
                diagnostics.append(
                    f"Judge disposition {judge_disposition} is incompatible with {reported_status}"
                )
        if failed_critical and run.suite.manifest.get("acceptance", {}).get(
            "criticalFailureSkipsJudge"
        ) is True:
            diagnostics.append("a critical deterministic failure requires the exact Judge-skip disposition")
    else:
        if judge_receipts:
            diagnostics.append("a skipped Judge cannot retain a Judge disposition receipt")
        if len(skip_receipts) != 1:
            diagnostics.append("a skipped Judge requires exactly one structured Judge-skip disposition")
        if skip_receipts:
            skip = skip_receipts[0]
            check_id = skip.get("checkId")
            failed_critical_check = str(check_id) if isinstance(check_id, str) else None
            matching = deterministic.get(str(check_id))
            if (
                reported_status != "FAIL"
                or run.suite.manifest.get("acceptance", {}).get("criticalFailureSkipsJudge") is not True
                or skip.get("critical") is not True
                or skip.get("deterministicVerdict") != "failed"
                or skip.get("disposition") != "skipped-critical-failure"
                or check_id not in failed_critical
                or matching is None
                or skip.get("evidence") != matching.get("evidence")
            ):
                diagnostics.append("Judge-skip disposition does not match the selected failed critical check")
            else:
                judge_disposition = "skipped-critical-failure"
    status = "invalid" if diagnostics else "verified"
    if status == "verified" and judge_invoked and require_runtime_judge_provenance:
        status = "pending-runtime-judge"
    return {
        "status": status,
        "runIdentity": run_identity,
        "deterministicChecks": [
            {
                "checkId": check_id,
                "critical": receipt.get("critical"),
                "verdict": receipt.get("verdict"),
            }
            for check_id, receipt in sorted(deterministic.items())
        ],
        "judgeDisposition": judge_disposition,
        "judgeOutput": dict(judge_output_reference) if isinstance(judge_output_reference, Mapping) else None,
        "judgeProvenance": None,
        "failedCriticalCheck": failed_critical_check,
        "diagnostics": diagnostics,
    }


def _load_checkpoint_report(
    checkpoint_root: Path,
    batch: Sequence[_RunSpec],
    run_identity: str,
    *,
    require_runtime_judge_provenance: bool = True,
    fixture_root: Path | None = None,
) -> dict[str, Any] | None:
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
            deterministic_evidence = loaded.get("deterministicEvidence")
            model_judge_evidence = loaded.get("modelJudgeEvidence")
            evidence_receipts = loaded.get("evidenceReceipts")
            evidence = loaded.get("evidence")
            if not isinstance(identity_evidence, list) or not all(
                isinstance(value, str) for value in identity_evidence
            ):
                raise RuntimeError(f"Scenario checkpoint identityEvidence must be an array of strings: {path}")
            if not isinstance(deterministic_evidence, list) or not all(
                isinstance(value, str) for value in deterministic_evidence
            ):
                raise RuntimeError(f"Scenario checkpoint deterministicEvidence must be an array of strings: {path}")
            if not isinstance(model_judge_evidence, list) or not all(
                isinstance(value, str) for value in model_judge_evidence
            ):
                raise RuntimeError(f"Scenario checkpoint modelJudgeEvidence must be an array of strings: {path}")
            if not isinstance(evidence, list) or not all(isinstance(value, str) for value in evidence):
                raise RuntimeError(f"Scenario checkpoint evidence must be an array of strings: {path}")
            if not isinstance(evidence_receipts, list):
                evidence_receipts = []
            handoff_receipts = loaded.get("handoffReceipts", [])
            if not isinstance(handoff_receipts, list) or not all(
                isinstance(receipt, dict) for receipt in handoff_receipts
            ):
                raise RuntimeError(f"Scenario checkpoint handoffReceipts must be an array of objects: {path}")
            if loaded.get("status") not in _TERMINAL_STATUSES:
                raise RuntimeError(f"Scenario checkpoint status must be terminal: {path}")
            if type(loaded.get("targetInvoked")) is not bool or type(loaded.get("judgeInvoked")) is not bool:
                raise RuntimeError(f"Scenario checkpoint invocation flags must be booleans: {path}")
            if loaded.get("cleanup") not in {"clean", "failed"}:
                raise RuntimeError(f"Scenario checkpoint cleanup must be clean or failed: {path}")
            if not isinstance(loaded.get("residualRisk"), str):
                raise RuntimeError(f"Scenario checkpoint residualRisk must be a string: {path}")
            receipt_audit = _validate_evidence_receipts(
                checkpoint_root,
                evidence_receipts,
                run,
                scenario_id,
                run_identity,
                str(loaded.get("status")),
                bool(loaded.get("judgeInvoked")),
                require_runtime_judge_provenance,
                fixture_root,
            )
            reported_status = str(loaded.get("status"))
            validated_status = (
                "BLOCKED"
                if reported_status in {"PASS", "FAIL"} and receipt_audit["status"] != "verified"
                else reported_status
            )
            retained_evidence = list(evidence)
            retained_evidence.extend(
                f"Evidence receipt validation: {diagnostic}"
                for diagnostic in receipt_audit["diagnostics"]
            )
            scenario_results.append(
                {
                    "scenario": scenario_id,
                    "status": validated_status,
                    "reportedStatus": reported_status,
                    "targetInvoked": loaded.get("targetInvoked"),
                    "judgeInvoked": loaded.get("judgeInvoked"),
                    "identityEvidence": identity_evidence,
                    "deterministicEvidence": deterministic_evidence,
                    "modelJudgeEvidence": model_judge_evidence,
                    "evidenceReceipts": evidence_receipts,
                    "receiptAudit": receipt_audit,
                    "cleanup": loaded["cleanup"],
                    "evidence": retained_evidence,
                    "handoffReceipts": handoff_receipts,
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
    scenarios = {
        (run.suite.suite_id, str(scenario["id"])): scenario
        for run in batch
        for scenario in run.suite.scenarios
        if str(scenario["id"]) in set(run.scenario_ids)
    }
    for identity in sorted(expected):
        compared_fields = [
            "status", "targetInvoked", "judgeInvoked", "evidenceReceipts", "cleanup"
        ]
        if scenarios[identity].get("requiredHandoffReceiptFields"):
            compared_fields.append("handoffReceipts")
        if any(final_results[identity].get(field) != checkpoints[identity].get(field) for field in compared_fields):
            raise RuntimeError(f"Final report disagrees with checkpoint for {identity[0]}:{identity[1]}")


def _attach_receipt_audits(
    report: dict[str, Any],
    checkpoint_report: dict[str, Any],
) -> None:
    receipt_audits = {
        (str(run_result.get("suite", "")), str(scenario.get("scenario", ""))): scenario.get(
            "receiptAudit"
        )
        for run_result in checkpoint_report.get("runs", [])
        for scenario in run_result.get("scenarioResults", [])
    }
    for run_result in report.get("runs", []):
        suite_id = str(run_result.get("suite", ""))
        for scenario in run_result.get("scenarioResults", []):
            identity = (suite_id, str(scenario.get("scenario", "")))
            receipt_audit = receipt_audits.get(identity)
            if isinstance(receipt_audit, Mapping):
                scenario["receiptAudit"] = json.loads(json.dumps(receipt_audit))


def _audit_report(
    batch: Sequence[_RunSpec],
    report: dict[str, Any],
    checkpoint_report: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    expected = {run.suite.suite_id: set(run.scenario_ids) for run in batch}
    suites = {run.suite.suite_id: run.suite for run in batch}
    scenarios = {
        (run.suite.suite_id, str(scenario["id"])): scenario
        for run in batch
        for scenario in run.suite.scenarios
        if str(scenario["id"]) in set(run.scenario_ids)
    }
    observed: dict[str, set[str]] = {}
    runs = report.get("runs", [])
    checkpoint_results = {
        (str(run_result.get("suite", "")), str(scenario_result.get("scenario", ""))): scenario_result
        for run_result in (checkpoint_report or {}).get("runs", [])
        for scenario_result in run_result.get("scenarioResults", [])
    }
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
            scenario_id = str(scenario_result.get("scenario", ""))
            scenario = scenarios.get((suite_id, scenario_id), {})
            if scenario_result.get("status") not in _TERMINAL_STATUSES:
                raise RuntimeError(f"Invalid terminal status for {suite_id}:{scenario_result.get('scenario')}")
            if not isinstance(scenario_result.get("targetInvoked"), bool) or not isinstance(
                scenario_result.get("judgeInvoked"), bool
            ):
                raise RuntimeError(f"Missing invocation disposition for {suite_id}:{scenario_result.get('scenario')}")
            if scenario_result.get("judgeInvoked") and not scenario_result.get("targetInvoked"):
                raise RuntimeError(f"Judge ran without target for {suite_id}:{scenario_result.get('scenario')}")
            for evidence_field in (
                "identityEvidence",
                "deterministicEvidence",
                "modelJudgeEvidence",
                "evidence",
            ):
                field_value = scenario_result.get(evidence_field)
                if not isinstance(field_value, list) or not all(
                    isinstance(value, str) for value in field_value
                ):
                    raise RuntimeError(
                        f"{evidence_field} must be an array of strings for "
                        f"{suite_id}:{scenario_result.get('scenario')}"
                    )
            evidence_receipts = scenario_result.get("evidenceReceipts")
            if not isinstance(evidence_receipts, list) or any(
                not isinstance(value, Mapping)
                or set(value) != {"path", "sha256"}
                or not isinstance(value.get("path"), str)
                or not isinstance(value.get("sha256"), str)
                or not _SHA256_PATTERN.fullmatch(str(value.get("sha256")))
                for value in evidence_receipts
            ):
                raise RuntimeError(
                    f"evidenceReceipts must contain exact path and SHA-256 references for "
                    f"{suite_id}:{scenario_result.get('scenario')}"
                )
            model_judge_evidence = scenario_result.get("modelJudgeEvidence", [])
            if not scenario_result.get("judgeInvoked") and model_judge_evidence:
                raise RuntimeError(f"Unexpected model-Judge evidence for {suite_id}:{scenario_result.get('scenario')}")
            checkpoint_result = checkpoint_results.get(
                (suite_id, str(scenario_result.get("scenario", ""))), {}
            )
            if checkpoint_result and evidence_receipts != checkpoint_result.get("evidenceReceipts"):
                raise RuntimeError(
                    f"Final report evidenceReceipts disagree with checkpoint for "
                    f"{suite_id}:{scenario_result.get('scenario')}"
                )
            receipt_audit = checkpoint_result.get("receiptAudit", {})
            if scenario_result.get("status") in {"PASS", "FAIL"} and (
                not isinstance(receipt_audit, Mapping)
                or receipt_audit.get("status") != "verified"
            ):
                raise RuntimeError(
                    f"Terminal verdict lacks validated evidence receipts for "
                    f"{suite_id}:{scenario_result.get('scenario')}"
                )
            if (
                scenario_result.get("status") in {"PASS", "FAIL"}
                and scenario_result.get("judgeInvoked")
                and isinstance(receipt_audit, Mapping)
            ):
                expected_judge_disposition = (
                    "passed" if scenario_result.get("status") == "PASS" else "failed"
                )
                if receipt_audit.get("judgeDisposition") != expected_judge_disposition:
                    raise RuntimeError(
                        f"Judge receipt disposition disagrees with terminal status for "
                        f"{suite_id}:{scenario_result.get('scenario')}"
                    )
            critical_failure_skipped_judge = (
                scenario_result.get("status") == "FAIL"
                and scenario_result.get("targetInvoked")
                and not scenario_result.get("judgeInvoked")
                and suites[suite_id].manifest.get("acceptance", {}).get("criticalFailureSkipsJudge") is True
                and isinstance(receipt_audit, Mapping)
                and receipt_audit.get("status") == "verified"
                and receipt_audit.get("judgeDisposition") == "skipped-critical-failure"
                and isinstance(receipt_audit.get("failedCriticalCheck"), str)
            )
            if scenario_result.get("status") in {"PASS", "FAIL"} and not (
                scenario_result.get("targetInvoked")
                and (scenario_result.get("judgeInvoked") or critical_failure_skipped_judge)
            ):
                raise RuntimeError(f"Terminal verdict lacks target and Judge for {suite_id}:{scenario_result.get('scenario')}")
            if not scenario_result.get("identityEvidence"):
                raise RuntimeError(f"Missing identity evidence for {suite_id}:{scenario_result.get('scenario')}")
            if scenario_result.get("cleanup") != "clean":
                raise RuntimeError(f"Cleanup failed for {suite_id}:{scenario_result.get('scenario')}")
            required_lanes = scenario.get("requiredHandoffReceiptLanes", [])
            required_fields = scenario.get("requiredHandoffReceiptFields", [])
            if required_lanes or required_fields:
                handoff_receipts = scenario_result.get("handoffReceipts", [])
                if not isinstance(handoff_receipts, list):
                    raise RuntimeError(f"{suite_id}:{scenario_id} handoffReceipts must be a list")
                receipts_by_lane: dict[str, dict[str, Any]] = {}
                for receipt in handoff_receipts:
                    if not isinstance(receipt, dict):
                        raise RuntimeError(f"{suite_id}:{scenario_id} handoff receipt must be an object")
                    lane = str(receipt.get("lane", ""))
                    if lane in receipts_by_lane:
                        raise RuntimeError(f"{suite_id}:{scenario_id} duplicate handoff receipt lane {lane}")
                    receipts_by_lane[lane] = receipt
                for lane in required_lanes:
                    if lane not in receipts_by_lane:
                        raise RuntimeError(f"{suite_id}:{scenario_id} missing handoff receipt lane {lane}")
                    for field in required_fields:
                        value = receipts_by_lane[lane].get(field)
                        if value is None or value == "" or value == [] or value == {}:
                            raise RuntimeError(
                                f"{suite_id}:{scenario_id} handoff receipt {lane} missing field {field}"
                            )
                    commit = receipts_by_lane[lane].get("commit")
                    role = receipts_by_lane[lane].get("role")
                    role_session_ids = role.get("sessionIds") if isinstance(role, dict) else None
                    if (
                        not isinstance(role, dict)
                        or not isinstance(role.get("invocation"), str)
                        or not role["invocation"]
                        or not isinstance(role_session_ids, list)
                        or not role_session_ids
                        or not all(isinstance(item, str) and item for item in role_session_ids)
                    ):
                        raise RuntimeError(
                            f"{suite_id}:{scenario_id} handoff receipt {lane} field role must be structured"
                        )
                    if not isinstance(commit, dict) or not all(
                        isinstance(commit.get(field), str) and commit[field]
                        for field in ("repository", "sha")
                    ):
                        raise RuntimeError(
                            f"{suite_id}:{scenario_id} handoff receipt {lane} field commit must be structured"
                        )
                    for field, key in (("review", "sessionIds"), ("verification", "sessionIds"), ("claimRelease", "eventIds")):
                        evidence_value = receipts_by_lane[lane].get(field)
                        values = evidence_value.get(key) if isinstance(evidence_value, dict) else None
                        if not isinstance(values, list) or not values or not all(
                            isinstance(item, str) and item for item in values
                        ):
                            raise RuntimeError(
                                f"{suite_id}:{scenario_id} handoff receipt {lane} field {field} must be structured"
                            )
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


def _terminal_response(
    events: Sequence[Mapping[str, Any]],
) -> tuple[int | None, bytes | None, str | None]:
    candidates: list[tuple[int, bytes]] = []
    for index, event in enumerate(events):
        payload = event.get("payload")
        if (
            event.get("type") != "response_item"
            or not isinstance(payload, Mapping)
            or payload.get("type") != "message"
            or payload.get("role") != "assistant"
            or payload.get("phase") != "final_answer"
        ):
            continue
        content = payload.get("content")
        if (
            not isinstance(content, list)
            or len(content) != 1
            or not isinstance(content[0], Mapping)
            or set(content[0]) != {"type", "text"}
            or content[0].get("type") != "output_text"
            or not isinstance(content[0].get("text"), str)
        ):
            return None, None, "terminal assistant response is not one exact output_text item"
        candidates.append((index, str(content[0]["text"]).encode("utf-8")))
    if not candidates:
        return None, None, "terminal assistant response is absent"
    if len(candidates) != 1:
        return None, None, "terminal assistant response is ambiguous"
    index, response = candidates[0]
    return index, response, None


def _noop_exclusion_candidate(
    events: Sequence[Mapping[str, Any]],
    parse_complete: bool,
    invocation: str | None,
    depth: int,
    started_at: float,
    finished_at: float,
) -> str | None:
    """Return auditable evidence for an inert, immediately aborted default/noop child."""
    if not parse_complete or invocation not in {"default", "noop"} or depth != 1:
        return None
    prompts: list[str] = []
    aborted = False
    unexpected_activity = False
    for event in events:
        event_type = event.get("type")
        payload = event.get("payload")
        if event_type in {"session_meta", "turn_context", "world_state"}:
            continue
        if event_type == "response_item" and isinstance(payload, Mapping):
            if payload.get("type") != "message":
                unexpected_activity = True
                continue
            if payload.get("role") == "developer":
                serialized = json.dumps(payload, sort_keys=True)
                if "AGENT_INSTRUCTION_BINDING_" in serialized:
                    unexpected_activity = True
                continue
            if payload.get("role") != "user":
                unexpected_activity = True
                continue
            content = payload.get("content", [])
            if not isinstance(content, list):
                unexpected_activity = True
                continue
            for item in content:
                if not isinstance(item, Mapping) or item.get("type") != "input_text":
                    unexpected_activity = True
                    continue
                text = str(item.get("text", "")).strip()
                if text.startswith("<turn_aborted>"):
                    aborted = True
                elif text.startswith(("<recommended_plugins>", "# AGENTS.md instructions for ", "<environment_context>")):
                    continue
                elif text:
                    prompts.append(text)
            continue
        if event_type == "event_msg" and isinstance(payload, Mapping):
            payload_type = payload.get("type")
            if payload_type == "user_message":
                message = str(payload.get("message", "")).strip()
                if message:
                    prompts.append(message)
            elif payload_type == "turn_aborted":
                aborted = True
            elif payload_type not in {"task_started", "token_count"}:
                unexpected_activity = True
            continue
        unexpected_activity = True
    duration = finished_at - started_at
    if (
        unexpected_activity
        or not aborted
        or not prompts
        or any(prompt.casefold() != "noop" for prompt in prompts)
        or duration < 0
        or duration > _IMMEDIATE_NOOP_CLOSE_SECONDS
    ):
        return None
    return (
        f"depth-one {invocation} session received only literal noop input and was turn-aborted "
        f"after {duration:.3f}s without assistant, tool, or instruction-binding activity"
    )


def _load_sessions(codex_home: Path) -> tuple[_Session, ...]:
    sessions: list[_Session] = []
    for rollout in codex_home.glob("**/rollout-*.jsonl"):
        rollout_text = rollout.read_text(encoding="utf-8", errors="replace")
        events = []
        parse_complete = True
        for line in rollout_text.splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                parse_complete = False
                continue
            if not isinstance(event, dict) or not isinstance(event.get("timestamp"), str):
                parse_complete = False
                continue
            events.append(event)
        metadata = next((event.get("payload", {}) for event in events if event.get("type") == "session_meta"), None)
        if not isinstance(metadata, dict) or not events:
            continue
        source = metadata.get("source", {})
        spawn = source.get("subagent", {}).get("thread_spawn", {}) if isinstance(source, dict) else {}
        invocation = metadata.get("agent_role") or spawn.get("agent_role")
        response_index, response, response_error = _terminal_response(events)
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
        depth = int(spawn.get("depth", 0))
        started_at = _timestamp_seconds(str(events[0]["timestamp"]))
        finished_at = _timestamp_seconds(str(events[-1]["timestamp"]))
        sessions.append(
            _Session(
                session_id=str(metadata.get("id", rollout.stem)),
                parent_thread_id=metadata.get("parent_thread_id"),
                invocation=str(invocation) if invocation else None,
                depth=depth,
                started_at=started_at,
                finished_at=finished_at,
                instruction_markers=frozenset(bound_markers),
                rollout_path=rollout.resolve(),
                rollout_sha256=_sha256(rollout),
                terminal_response_index=response_index,
                terminal_response=response,
                terminal_response_error=response_error,
                suite_exclusion_candidate=_noop_exclusion_candidate(
                    events,
                    parse_complete,
                    str(invocation) if invocation else None,
                    depth,
                    started_at,
                    finished_at,
                ),
            )
        )
    return tuple(sessions)


def _suite_lifecycle_sessions(
    sessions: Sequence[_Session],
    batch: Sequence[_RunSpec],
) -> tuple[tuple[_Session, ...], list[dict[str, Any]]]:
    """Partition proven inert noops from sessions participating in the evaluated suite."""
    expected_invocations = {
        str(run.suite.manifest["execution"][key])
        for run in batch
        for key in ("supervisorInvocation", "targetInvocation", "judgeInvocation")
    }
    expected_invocations.update(
        str(dependency).replace("-", "_")
        for run in batch
        for dependency in _agent_dependencies(run)
    )
    parent_ids = {str(session.parent_thread_id) for session in sessions if session.parent_thread_id}
    participating: list[_Session] = []
    excluded: list[dict[str, Any]] = []
    for session in sessions:
        reason = session.suite_exclusion_candidate
        if (
            reason is None
            or session.invocation in expected_invocations
            or session.session_id in parent_ids
        ):
            participating.append(session)
            continue
        excluded.append(
            {
                "sessionId": session.session_id,
                "parentSessionId": session.parent_thread_id,
                "invocation": session.invocation,
                "reason": reason,
                "rolloutPath": str(session.rollout_path) if session.rollout_path else None,
                "rolloutSha256": session.rollout_sha256,
            }
        )
    return tuple(participating), excluded


def _audit_identity(
    staged: Sequence[_StagedAgent],
    codex_home: Path,
    expected_invocation_counts: dict[str, int],
    batch: Sequence[_RunSpec] | None = None,
    report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    all_sessions = _load_sessions(codex_home)
    sessions, excluded_sessions = (
        _suite_lifecycle_sessions(all_sessions, batch) if batch is not None else (all_sessions, [])
    )
    sessions_by_invocation: dict[str, list[_Session]] = {}
    for session in sessions:
        if session.invocation:
            sessions_by_invocation.setdefault(session.invocation, []).append(session)
    agents = []
    for agent in staged:
        matching_sessions = sessions_by_invocation.get(agent.invocation, [])
        exact_sessions = [session for session in matching_sessions if agent.instruction_marker in session.instruction_markers]
        exact_direct_sessions = [session for session in exact_sessions if session.depth < 3]
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
                "directBoundSessionIds": [session.session_id for session in exact_direct_sessions],
            }
        )
        if matching_sessions and len(exact_sessions) != len(matching_sessions):
            raise RuntimeError(f"Missing runtime instruction binding for {agent.invocation}")
        if agent.invocation in expected_invocation_counts and len(exact_direct_sessions) != required_count:
            raise RuntimeError(
                f"Custom-agent session count mismatch for {agent.invocation}: "
                f"expected {required_count}, observed {len(exact_direct_sessions)}"
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
    return {
        "rolloutCount": len(all_sessions),
        "suiteLifecycleRolloutCount": len(sessions),
        "excludedSessions": excluded_sessions,
        "agents": agents,
        "scenarioBindings": scenario_bindings,
    }


def _retained_relative_path(root: Path, path: Path, field: str) -> str:
    try:
        resolved_root = root.resolve(strict=True)
        resolved = path.resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise RuntimeError(f"{field} is missing") from error
    if resolved_root not in resolved.parents or resolved.is_symlink() or not resolved.is_file():
        raise RuntimeError(f"{field} is outside retained run evidence")
    return resolved.relative_to(resolved_root).as_posix()


def _bind_codex_judge_provenance(
    checkpoint_report: dict[str, Any],
    identity: Mapping[str, Any],
    batch: Sequence[_RunSpec],
    checkpoint_root: Path,
    retained_session_root: Path,
    evidence_root: Path,
) -> None:
    sessions = _load_sessions(retained_session_root)
    sessions_by_id: dict[str, list[_Session]] = {}
    for session in sessions:
        sessions_by_id.setdefault(session.session_id, []).append(session)
    bindings = identity.get("scenarioBindings")
    binding_rows = list(bindings) if isinstance(bindings, list) else []
    runs = {run.suite.suite_id: run for run in batch}
    for run_result in checkpoint_report.get("runs", []):
        suite_id = str(run_result.get("suite", ""))
        run = runs.get(suite_id)
        for scenario in run_result.get("scenarioResults", []):
            if scenario.get("judgeInvoked") is not True:
                continue
            scenario_id = str(scenario.get("scenario", ""))
            audit = scenario.get("receiptAudit")
            if not isinstance(audit, dict):
                continue
            diagnostics = audit.setdefault("diagnostics", [])
            errors: list[str] = []
            expected_invocation = (
                str(run.suite.manifest["execution"]["judgeInvocation"])
                if run is not None
                else ""
            )
            matching_bindings = [
                value
                for value in binding_rows
                if isinstance(value, Mapping)
                and value.get("suite") == suite_id
                and value.get("scenario") == scenario_id
                and value.get("kind") == "judge"
            ]
            if len(matching_bindings) != 1:
                errors.append("exact Judge session binding is absent or ambiguous")
                binding: Mapping[str, Any] = {}
            else:
                binding = matching_bindings[0]
            session_id = binding.get("sessionId")
            matching_sessions = (
                sessions_by_id.get(str(session_id), [])
                if isinstance(session_id, str)
                else []
            )
            if len(matching_sessions) != 1:
                errors.append("bound Judge session is absent or ambiguous")
                session = None
            else:
                session = matching_sessions[0]
            if binding.get("invocation") != expected_invocation:
                errors.append("Judge session binding invocation mismatch")
            if session is not None:
                if session.invocation != expected_invocation:
                    errors.append("bound session is not the selected Judge invocation")
                if str(session.parent_thread_id) != str(binding.get("parentSessionId")):
                    errors.append("bound Judge session parent mismatch")
                if session.terminal_response is None:
                    errors.append(
                        session.terminal_response_error
                        or "bound Judge terminal response is unavailable"
                    )
            response: Mapping[str, Any] | None = None
            if session is not None and session.terminal_response is not None:
                try:
                    loaded_response = json.loads(session.terminal_response.decode("utf-8"))
                except (UnicodeError, json.JSONDecodeError):
                    errors.append("bound Judge terminal response is malformed")
                else:
                    if isinstance(loaded_response, Mapping):
                        response = loaded_response
                    else:
                        errors.append("bound Judge terminal response is not an object")
            expected_response = {
                "schema": _JUDGE_OUTPUT_SCHEMA,
                "version": 1,
                "runIdentity": audit.get("runIdentity"),
                "suite": suite_id,
                "scenario": scenario_id,
                "judgeInvocation": expected_invocation,
                "disposition": audit.get("judgeDisposition"),
            }
            if response is not None and dict(response) != expected_response:
                errors.append("bound Judge terminal response identity or disposition mismatch")
            output_reference = audit.get("judgeOutput")
            output_diagnostics: list[str] = []
            output_path = (
                _retained_artifact(
                    checkpoint_root,
                    output_reference,
                    PurePosixPath(suite_id, scenario_id, "artifacts"),
                    "Judge output",
                    output_diagnostics,
                )
                if run is not None
                else None
            )
            errors.extend(output_diagnostics)
            if (
                session is not None
                and session.terminal_response is not None
                and output_path is not None
                and output_path.read_bytes() != session.terminal_response
            ):
                errors.append("Judge output artifact does not match retained child response bytes")
            if errors:
                diagnostics.extend(errors)
                audit["status"] = "invalid"
                audit["judgeProvenance"] = None
                if scenario.get("reportedStatus") in {"PASS", "FAIL"}:
                    scenario["status"] = "BLOCKED"
                continue
            assert session is not None
            assert session.terminal_response is not None
            assert session.rollout_path is not None
            assert session.rollout_sha256 is not None
            assert session.terminal_response_index is not None
            assert output_path is not None
            response_digest = hashlib.sha256(session.terminal_response).hexdigest()
            response_path = retained_session_root / "responses" / f"{response_digest}.json"
            response_path.parent.mkdir(parents=True, exist_ok=True)
            if response_path.exists() and response_path.read_bytes() != session.terminal_response:
                diagnostics.append("retained Judge response digest collision")
                audit["status"] = "invalid"
                audit["judgeProvenance"] = None
                if scenario.get("reportedStatus") in {"PASS", "FAIL"}:
                    scenario["status"] = "BLOCKED"
                continue
            response_path.write_bytes(session.terminal_response)
            output_digest = _sha256(output_path)
            audit["judgeProvenance"] = {
                "status": "verified",
                "sessionId": session.session_id,
                "parentSessionId": str(session.parent_thread_id),
                "invocation": expected_invocation,
                "runIdentity": audit.get("runIdentity"),
                "suite": suite_id,
                "scenario": scenario_id,
                "rolloutPath": _retained_relative_path(
                    evidence_root, session.rollout_path, "Judge rollout"
                ),
                "rolloutSha256": session.rollout_sha256,
                "responseEventIndex": session.terminal_response_index,
                "responsePath": _retained_relative_path(
                    evidence_root, response_path, "Judge response"
                ),
                "responseSha256": response_digest,
                "outputPath": _retained_relative_path(
                    evidence_root, output_path, "Judge output"
                ),
                "outputSha256": output_digest,
                "disposition": audit.get("judgeDisposition"),
            }
            audit["status"] = "verified"
            if scenario.get("reportedStatus") in {"PASS", "FAIL"}:
                scenario["status"] = scenario["reportedStatus"]
def _bind_target_sessions(
    sessions: Sequence[_Session],
    batch: Sequence[_RunSpec],
    report: dict[str, Any],
) -> dict[tuple[str, str], _Session]:
    """Bind each reported target invocation to its scenario by supervisor child order."""
    by_parent: dict[str, list[_Session]] = {}
    for session in sessions:
        if session.parent_thread_id:
            by_parent.setdefault(session.parent_thread_id, []).append(session)
    reported = {
        (str(run_result.get("suite", "")), str(result.get("scenario", ""))): result
        for run_result in report.get("runs", [])
        for result in run_result.get("scenarioResults", [])
    }
    bindings: dict[tuple[str, str], _Session] = {}
    for run in batch:
        supervisor_invocation = str(run.suite.manifest["execution"]["supervisorInvocation"])
        supervisors = [
            session for session in sessions if session.depth == 1 and session.invocation == supervisor_invocation
        ]
        if len(supervisors) != 1:
            raise RuntimeError(f"Cannot bind scenario targets for {run.suite.suite_id}")
        target_invocation = str(run.suite.manifest["execution"]["targetInvocation"])
        target_sessions = sorted(
            (
                session
                for session in by_parent.get(supervisors[0].session_id, [])
                if session.invocation == target_invocation
            ),
            key=lambda session: session.started_at,
        )
        invoked_scenarios = [
            scenario_id
            for scenario_id in run.scenario_ids
            if reported.get((run.suite.suite_id, scenario_id), {}).get("targetInvoked")
        ]
        if len(target_sessions) != len(invoked_scenarios):
            raise RuntimeError(f"Cannot bind scenario targets for {run.suite.suite_id}")
        bindings.update(
            {
                (run.suite.suite_id, scenario_id): session
                for scenario_id, session in zip(invoked_scenarios, target_sessions, strict=True)
            }
        )
    return bindings


def _git_common_directory(
    repository: Path,
    containment_root: Path | None = None,
    containment_name: str = "fixture",
) -> Path:
    """Return a candidate's common Git directory and enforce an optional runner-owned boundary."""
    completed = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        cwd=repository,
        check=False,
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"Receipt repository is not a Git worktree: {repository}")
    common = Path(completed.stdout.strip())
    resolved = common.resolve() if common.is_absolute() else (repository / common).resolve()
    if containment_root is not None:
        boundary = containment_root.resolve()
        if resolved != boundary and boundary not in resolved.parents:
            raise RuntimeError(f"Git common directory escapes {containment_name} containment: {repository}")
    return resolved


def _release_events(repository: Path, fixture_root: Path) -> dict[str, dict[str, Any]]:
    """Load successful release events retained by one disposable fixture repository."""
    common = _git_common_directory(repository, fixture_root, "fixture")
    event_root = common / "agent-claim-events" / "hot"
    resolved_event_root = event_root.resolve()
    if common not in resolved_event_root.parents:
        raise RuntimeError(f"Claim release journal escapes fixture containment: {event_root}")
    events: dict[str, dict[str, Any]] = {}
    for journal in sorted(event_root.glob("*.jsonl")):
        resolved_journal = journal.resolve()
        if common not in resolved_journal.parents:
            raise RuntimeError(f"Claim release journal escapes fixture containment: {journal}")
        for line in journal.read_text(encoding="utf-8").splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if (
                isinstance(event, dict)
                and event.get("action") == "release"
                and event.get("outcome") == "RELEASED"
                and isinstance(event.get("event_id"), str)
            ):
                events[str(event["event_id"])] = event
    return events


def _audit_handoff_evidence(
    batch: Sequence[_RunSpec],
    report: dict[str, Any],
    sessions: Sequence[_Session],
    fixture_root: Path,
) -> None:
    """Bind dependency-routing receipts to repository, session, and claim journal evidence."""
    target_bindings = _bind_target_sessions(sessions, batch, report)
    report_results = {
        (str(run_result.get("suite", "")), str(result.get("scenario", ""))): result
        for run_result in report.get("runs", [])
        for result in run_result.get("scenarioResults", [])
    }
    lane_roles = {
        "source": ("dev_coder", ("dev_code_reviewer", 0), (("dev_verifier", 0),)),
        "documentation": ("dev_documentation_writer", ("dev_artifact_reviewer", 0), (("dev_verifier", 0),)),
        "integration": (
            "dev_merge_coordinator",
            (("dev_code_reviewer", 1), ("dev_artifact_reviewer", 1)),
            (("dev_verifier", 1),),
        ),
        "closeout": (
            "dev_backlog_steward",
            (("dev_code_reviewer", 1), ("dev_artifact_reviewer", 1)),
            (("dev_verifier", 1),),
        ),
    }
    for run in batch:
        scenarios = {str(value["id"]): value for value in run.suite.scenarios}
        for scenario_id in run.scenario_ids:
            scenario = scenarios.get(scenario_id)
            if scenario is None:
                raise RuntimeError(
                    f"{run.suite.suite_id}:{scenario_id} is absent from the selected scenario contract"
                )
            if not scenario.get("requiredHandoffReceiptFields"):
                continue
            identity = f"{run.suite.suite_id}:{scenario_id}"
            target = target_bindings.get((run.suite.suite_id, scenario_id))
            if target is None:
                raise RuntimeError(f"{identity} has no target session for handoff evidence")
            nested = sorted(
                (session for session in sessions if session.parent_thread_id == target.session_id),
                key=lambda session: session.started_at,
            )
            sessions_by_role: dict[str, list[_Session]] = {}
            for session in nested:
                sessions_by_role.setdefault(str(session.invocation), []).append(session)
            reported_result = report_results.get((run.suite.suite_id, scenario_id))
            if not isinstance(reported_result, Mapping):
                raise RuntimeError(f"{identity} has no retained scenario result for handoff evidence")
            reported_receipts = reported_result.get("handoffReceipts", [])
            if not isinstance(reported_receipts, list) or not all(
                isinstance(receipt, dict) for receipt in reported_receipts
            ):
                raise RuntimeError(f"{identity} malformed handoff receipts: expected an array of objects")
            receipts: dict[str, dict[str, Any]] = {}
            for receipt in reported_receipts:
                receipt_lane = receipt.get("lane")
                if not isinstance(receipt_lane, str) or not receipt_lane:
                    raise RuntimeError(
                        f"{identity} malformed handoff receipt lane: expected a non-empty string"
                    )
                receipts[receipt_lane] = receipt
            suite_fixture_root = (fixture_root / run.suite.suite_id).resolve()
            for lane in scenario.get("requiredHandoffReceiptLanes", []):
                if lane not in receipts:
                    raise RuntimeError(f"{identity} missing handoff receipt lane {lane}")
                receipt = receipts[lane]
                if lane not in lane_roles:
                    raise RuntimeError(f"{identity} has no evidence binding for handoff lane {lane}")
                producer_role, review_spec, verification_spec = lane_roles[lane]
                required_receipt_fields = (
                    "role",
                    "commit",
                    "review",
                    "verification",
                    "claimRelease",
                )
                missing_fields = [field for field in required_receipt_fields if field not in receipt]
                if missing_fields:
                    raise RuntimeError(
                        f"{identity} malformed handoff receipt {lane}: missing {missing_fields[0]}"
                    )
                receipt_role = receipt.get("role")
                commit = receipt.get("commit")
                review = receipt.get("review")
                verification = receipt.get("verification")
                claim_release = receipt.get("claimRelease")
                if not isinstance(receipt_role, dict):
                    raise RuntimeError(f"{identity} malformed handoff receipt {lane}: role must be an object")
                if not isinstance(commit, dict):
                    raise RuntimeError(f"{identity} malformed handoff receipt {lane}: commit must be an object")
                if not isinstance(review, dict):
                    raise RuntimeError(f"{identity} malformed handoff receipt {lane}: review must be an object")
                if not isinstance(verification, dict):
                    raise RuntimeError(
                        f"{identity} malformed handoff receipt {lane}: verification must be an object"
                    )
                if not isinstance(claim_release, dict):
                    raise RuntimeError(
                        f"{identity} malformed handoff receipt {lane}: claimRelease must be an object"
                    )
                structured_fields = (
                    ("role.sessionIds", receipt_role.get("sessionIds")),
                    ("review.sessionIds", review.get("sessionIds")),
                    ("verification.sessionIds", verification.get("sessionIds")),
                    ("claimRelease.eventIds", claim_release.get("eventIds")),
                )
                for field, values in structured_fields:
                    if not isinstance(values, list) or not values or not all(
                        isinstance(value, str) and value for value in values
                    ):
                        raise RuntimeError(
                            f"{identity} malformed handoff receipt {lane}: {field} must be a non-empty string array"
                        )
                if not all(
                    isinstance(commit.get(field), str) and commit[field]
                    for field in ("repository", "sha")
                ):
                    raise RuntimeError(
                        f"{identity} malformed handoff receipt {lane}: commit fields must be strings"
                    )
                if receipt_role.get("invocation") != producer_role:
                    raise RuntimeError(
                        f"{identity} handoff receipt {lane} role invocation does not match lane producer"
                    )
                producer_sessions = sessions_by_role.get(producer_role, [])
                if not producer_sessions:
                    raise RuntimeError(f"{identity} handoff receipt {lane} role has no matching producer session")
                if receipt_role["sessionIds"] != [session.session_id for session in producer_sessions]:
                    raise RuntimeError(
                        f"{identity} handoff receipt {lane} producer sessions are not retained evidence"
                    )

                repository = (suite_fixture_root / str(commit["repository"])).resolve()
                if repository != suite_fixture_root and suite_fixture_root not in repository.parents:
                    raise RuntimeError(f"{identity} handoff receipt {lane} repository escapes fixture root")
                sha = str(commit["sha"])
                if not repository.is_dir() or re.fullmatch(r"[0-9a-f]{40,64}", sha) is None:
                    raise RuntimeError(f"{identity} handoff receipt {lane} commit lacks repository ancestry evidence")
                commit_exists = subprocess.run(
                    ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
                    cwd=repository,
                    check=False,
                    text=True,
                    capture_output=True,
                )
                ancestor = subprocess.run(
                    ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
                    cwd=repository,
                    check=False,
                    text=True,
                    capture_output=True,
                )
                if commit_exists.returncode != 0 or ancestor.returncode != 0:
                    raise RuntimeError(f"{identity} handoff receipt {lane} commit lacks repository ancestry evidence")
                status = subprocess.run(
                    ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
                    cwd=repository,
                    check=False,
                    text=True,
                    capture_output=True,
                )
                if status.returncode != 0 or status.stdout:
                    raise RuntimeError(f"{identity} handoff receipt {lane} repository has uncommitted drift")

                review_specs = (review_spec,) if isinstance(review_spec[0], str) else review_spec
                expected_review_ids = []
                for role, index in review_specs:
                    role_sessions = sessions_by_role.get(role, [])
                    if len(role_sessions) <= index:
                        raise RuntimeError(f"{identity} handoff receipt {lane} lacks retained review session")
                    expected_review_ids.append(role_sessions[index].session_id)
                if review["sessionIds"] != expected_review_ids:
                    raise RuntimeError(f"{identity} handoff receipt {lane} review sessions are not retained evidence")

                expected_verification_ids = []
                for role, index in verification_spec:
                    role_sessions = sessions_by_role.get(role, [])
                    if len(role_sessions) <= index:
                        raise RuntimeError(f"{identity} handoff receipt {lane} lacks retained verification session")
                    expected_verification_ids.append(role_sessions[index].session_id)
                if verification["sessionIds"] != expected_verification_ids:
                    raise RuntimeError(
                        f"{identity} handoff receipt {lane} verification sessions are not retained evidence"
                    )

                release_events = _release_events(repository, suite_fixture_root)
                for event_id in claim_release["eventIds"]:
                    event = release_events.get(event_id)
                    if (
                        event is None
                        or event.get("resulting_commit") != sha
                        or event.get("agent") != producer_role
                    ):
                        raise RuntimeError(
                            f"{identity} handoff receipt {lane} claim release lacks fixture lifecycle evidence"
                        )


def _audit_session_concurrency(
    sessions: Sequence[_Session],
    maximum_threads: int,
    batch: Sequence[_RunSpec] | None = None,
    report: dict[str, Any] | None = None,
) -> dict[str, int]:
    all_sessions = sessions
    excluded_session_count = 0
    if batch is not None:
        sessions, excluded_sessions = _suite_lifecycle_sessions(sessions, batch)
        excluded_session_count = len(excluded_sessions)
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
        [(session.started_at, 1, session.depth) for session in all_sessions]
        + [(session.finished_at, -1, session.depth) for session in all_sessions]
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
            for dependency in _agent_dependencies(run)
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
        run_by_target = {
            str(run.suite.manifest["execution"]["targetInvocation"]): run for run in batch
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
        target_bindings: dict[tuple[str, str], _Session] = {}
        if report is not None:
            target_bindings = _bind_target_sessions(sessions, batch, report)
            identity_by_target = {session.session_id: identity for identity, session in target_bindings.items()}
            for nested in (session for session in sessions if session.depth >= 3):
                identity = identity_by_target.get(str(nested.parent_thread_id))
                if identity is None:
                    raise RuntimeError(f"Nested dependency {nested.invocation} has no scenario-bound target")
                suite_id, scenario_id = identity
                run = next(value for value in batch if value.suite.suite_id == suite_id)
                allowed = {
                    value.replace("-", "_")
                    for value in _scenario_dependencies(run.suite, scenario_id)
                }
                if nested.invocation not in allowed:
                    raise RuntimeError(
                        f"Nested dependency {nested.invocation} is not allowed for {suite_id}:{scenario_id}"
                    )
        else:
            for nested in (session for session in sessions if session.depth >= 3):
                parent = session_by_id.get(str(nested.parent_thread_id))
                run = run_by_target.get(str(parent.invocation)) if parent else None
                suite_dependencies = {
                    str(value).replace("-", "_")
                    for value in _agent_dependencies(run)
                } if run else set()
                if nested.invocation not in suite_dependencies:
                    raise RuntimeError(
                        f"Nested dependency {nested.invocation} is not allowed for parent "
                        f"{parent.invocation if parent else nested.parent_thread_id}"
                    )
        if report is not None:
            for run in batch:
                scenarios = {str(value["id"]): value for value in run.suite.scenarios}
                for scenario_id in run.scenario_ids:
                    target_session = target_bindings.get((run.suite.suite_id, scenario_id))
                    if target_session is None:
                        continue
                    expected_order = [
                        str(value).replace("-", "_")
                        for value in scenarios[scenario_id].get("requiredDependencyOrder", [])
                    ]
                    if not expected_order:
                        continue
                    observed_order = [
                        str(session.invocation)
                        for session in sorted(
                            by_parent.get(target_session.session_id, []),
                            key=lambda session: session.started_at,
                        )
                    ]
                    if observed_order != expected_order:
                        raise RuntimeError(
                            f"Dependency order mismatch for {run.suite.suite_id}:{scenario_id}: "
                            f"expected {expected_order}, observed {observed_order}"
                        )
    return {
        "maximumActiveSessions": maximum_active,
        "maximumChildrenObserved": maximum_children,
        "excludedSessionCount": excluded_session_count,
    }


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
        target = destination / rollout.relative_to(codex_home)
        target.parent.mkdir(parents=True, exist_ok=True)
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
            "PYTHONDONTWRITEBYTECODE": "1",
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
    fixture_root = workspace / ".agent-suite-fixtures"
    repositories: list[tuple[Path, Path, str]] = []
    if (workspace / ".git").exists():
        repositories.append((workspace, workspace, "cleanup"))
    if fixture_root.is_dir():
        repositories.extend(
            (git_entry.parent, fixture_root, "cleanup")
            for git_entry in sorted(fixture_root.glob("**/.git"))
        )
    registries: dict[Path, tuple[Path, bool]] = {}
    for repository, containment_root, containment_name in repositories:
        git_entry = repository / ".git"
        if git_entry.is_dir():
            common = git_entry.resolve()
            boundary = containment_root.resolve()
            if common != boundary and boundary not in common.parents:
                raise RuntimeError(
                    f"Git common directory escapes {containment_name} containment: {repository}"
                )
        else:
            common = _git_common_directory(repository, containment_root, containment_name)
        registries.setdefault(
            common / "agent-claims.json",
            (repository, repository == workspace),
        )
    for registry, (repository, is_workspace) in registries.items():
        if not registry.is_file():
            continue
        loaded = json.loads(registry.read_text(encoding="utf-8"))
        claims = loaded.get("claims", loaded) if isinstance(loaded, dict) else loaded
        if claims:
            if is_workspace:
                raise RuntimeError("Disposable workspace retains active claims")
            raise RuntimeError(
                f"Fixture repository retains active claims: {repository}"
            )
    return "clean"


def _extract_junie_report(event_path: Path) -> dict[str, Any]:
    if not event_path.is_file() or event_path.is_symlink():
        raise RuntimeError("Junie event stream is missing or unsafe")
    events: list[dict[str, Any]] = []
    for line_number, line in enumerate(event_path.read_text(encoding="utf-8").splitlines(), start=1):
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            raise RuntimeError(f"Junie event stream line {line_number} is malformed") from error
        if not isinstance(value, dict):
            raise RuntimeError(f"Junie event stream line {line_number} is not an object")
        events.append(value)
    results = [event for event in events if event.get("type") == "result"]
    if len(results) != 1 or not events or events[-1] is not results[0]:
        raise RuntimeError("Junie event stream must contain one terminal result event")
    result = results[0].get("result")
    if not isinstance(result, str) or not result.strip():
        raise RuntimeError("Junie terminal result is empty")
    try:
        report = json.loads(result)
    except json.JSONDecodeError as error:
        raise RuntimeError("Junie terminal result is not the required JSON report") from error
    if not isinstance(report, dict):
        raise RuntimeError("Junie terminal result must contain a JSON object")
    return report


def _junie_lifecycle_evidence(junie_home: Path) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    for event_path in sorted((junie_home / "sessions").glob("**/events.jsonl")):
        if event_path.is_symlink() or not event_path.is_file():
            continue
        for line in event_path.read_text(encoding="utf-8").splitlines():
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                continue
            event = value.get("event") if isinstance(value, dict) else None
            agent_event = event.get("agentEvent") if isinstance(event, dict) else None
            agent = agent_event.get("agent") if isinstance(agent_event, dict) else None
            if isinstance(agent_event, dict) and agent_event.get("kind") == "CustomAgentBlockUpdatedEvent":
                event_digest = hashlib.sha256(
                    json.dumps(
                        agent_event,
                        sort_keys=True,
                        separators=(",", ":"),
                        ensure_ascii=True,
                    ).encode("utf-8")
                ).hexdigest()
                evidence.append(
                    {
                        "timestamp": value.get("timestamp"),
                        "agent": {
                            "id": agent.get("id") if isinstance(agent, dict) else None,
                            "name": agent.get("name") if isinstance(agent, dict) else None,
                        },
                        "eventType": agent_event.get("kind"),
                        "name": agent_event.get("name"),
                        "status": agent_event.get("status"),
                        "stepId": agent_event.get("stepId"),
                        "menuItems": agent_event.get("menuItems"),
                        "details": agent_event.get("details"),
                        "model": agent_event.get("model"),
                        "eventDigest": event_digest,
                    }
                )
    return evidence


def _retain_junie_staged_manifest(
    agent_root: Path,
    destination: Path,
    staged: Sequence[_StagedAgent],
) -> Path:
    destination.mkdir(parents=True, exist_ok=False)
    agents: list[dict[str, str]] = []
    for agent in sorted(staged, key=lambda value: value.invocation):
        source = agent_root / f"{agent.invocation}.md"
        retained = destination / source.name
        shutil.copyfile(source, retained)
        digest = _sha256(retained)
        if digest != agent.sha256:
            raise RuntimeError(f"Staged Junie definition digest changed for {agent.invocation}")
        agents.append(
            {
                "name": agent.invocation,
                "path": retained.relative_to(destination).as_posix(),
                "sha256": digest,
            }
        )
    manifest = destination / "staged-agent-manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "schema": "dev-methodology-agent-suite-junie-staged-manifest",
                "version": 1,
                "configuredAgentLocation": str(agent_root),
                "agents": agents,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return manifest


def _audit_junie_staged_manifest(
    manifest_path: Path | None,
    staged: Sequence[_StagedAgent],
) -> dict[str, Any]:
    if manifest_path is None:
        return {"status": "not-retained"}
    loaded = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_names = {agent.invocation for agent in staged}
    if (
        not isinstance(loaded, Mapping)
        or set(loaded) != {"schema", "version", "configuredAgentLocation", "agents"}
        or loaded.get("schema") != "dev-methodology-agent-suite-junie-staged-manifest"
        or loaded.get("version") != 1
        or not isinstance(loaded.get("configuredAgentLocation"), str)
        or not isinstance(loaded.get("agents"), list)
    ):
        raise RuntimeError("Retained Junie staged-agent manifest is malformed")
    observed: set[str] = set()
    for item in loaded["agents"]:
        if (
            not isinstance(item, Mapping)
            or set(item) != {"name", "path", "sha256"}
            or item.get("name") in observed
            or item.get("name") not in expected_names
            or item.get("path") != f"{item.get('name')}.md"
            or not isinstance(item.get("sha256"), str)
            or not _SHA256_PATTERN.fullmatch(str(item.get("sha256")))
        ):
            raise RuntimeError("Retained Junie staged-agent manifest entry is invalid")
        path = manifest_path.parent / str(item["path"])
        if path.is_symlink() or not path.is_file() or _sha256(path) != item["sha256"]:
            raise RuntimeError(f"Retained Junie staged definition is missing or stale: {item.get('name')}")
        observed.add(str(item["name"]))
    if observed != expected_names:
        raise RuntimeError("Retained Junie staged-agent manifest coverage mismatch")
    return {
        "status": "path-and-digest-bound",
        "configuredAgentLocation": loaded["configuredAgentLocation"],
        "manifestPath": str(manifest_path),
        "agents": sorted(observed),
    }


def _audit_junie_agent_lifecycles(
    junie_home: Path,
    batch: Sequence[_RunSpec],
    report: Mapping[str, Any],
    staged: Sequence[_StagedAgent],
    staged_manifest: Path | None = None,
) -> dict[str, Any]:
    expected_counts = {
        invocation.replace("_", "-"): count
        for invocation, count in _expected_invocation_counts(batch, dict(report)).items()
    }
    allowed_agents: set[str] = set()
    for run in batch:
        execution = run.suite.manifest["execution"]
        supervisor = str(execution["supervisorInvocation"]).replace("_", "-")
        target = str(execution["targetInvocation"]).replace("_", "-")
        judge = str(execution["judgeInvocation"]).replace("_", "-")
        allowed_agents.update((supervisor, target, judge))
        nested_limit = int(execution.get("nestedAgentLimit", 0))
        for dependency in run.suite.manifest["target"].get("allowedAgentDependencies", []):
            dependency_name = str(dependency).replace("_", "-")
            if nested_limit != 1:
                raise RuntimeError(
                    f"Junie suite declares dependency {dependency_name} without nestedAgentLimit 1"
                )
            allowed_agents.add(dependency_name)

    staged_by_invocation = {agent.invocation: agent for agent in staged}
    missing_definitions = sorted(allowed_agents - set(staged_by_invocation))
    if missing_definitions:
        raise RuntimeError(f"Junie lifecycle agents lack staged definitions: {', '.join(missing_definitions)}")
    observed: dict[tuple[str, str], dict[str, Any]] = {}
    for agent_event in _junie_lifecycle_evidence(junie_home):
        agent = agent_event.get("agent")
        name = agent.get("name") if isinstance(agent, Mapping) else None
        if name not in allowed_agents:
            raise RuntimeError(f"Junie session ledger contains unexpected custom agent: {name}")
        step_id = agent_event.get("stepId")
        status = agent_event.get("status")
        agent_id = agent.get("id") if isinstance(agent, Mapping) else None
        if (
            not isinstance(step_id, str)
            or status not in {"STARTED", "FINISHED"}
            or not isinstance(agent_id, str)
            or not agent_id
            or agent_event.get("eventType") != "CustomAgentBlockUpdatedEvent"
        ):
            raise _JunieEvidenceInsufficient(
                "Junie ledger custom-agent identity, step, or status evidence is malformed"
            )
        if agent_event.get("name") != name:
            raise RuntimeError(f"Junie custom-agent event identity mismatch for {name}:{step_id}")
        record = observed.setdefault(
            (str(name), step_id),
            {
                "name": str(name),
                "agentId": agent_id,
                "statuses": [],
                "eventDigests": [],
            },
        )
        if record["agentId"] != agent_id:
            raise RuntimeError(f"Junie lifecycle agent id changed for {name}:{step_id}")
        if status in record["statuses"]:
            raise RuntimeError(f"Junie lifecycle has conflicting {status} events for {name}:{step_id}")
        record["statuses"].append(status)
        record["eventDigests"].append(agent_event["eventDigest"])

    complete: list[dict[str, Any]] = []
    for record in observed.values():
        if record["statuses"] != ["STARTED", "FINISHED"]:
            raise _JunieEvidenceInsufficient(
                f"Junie ledger has an incomplete lifecycle for {record['name']}"
            )
        complete.append(record)

    mismatches = []
    for name, expected_count in expected_counts.items():
        actual_count = sum(record["name"] == name for record in complete)
        if actual_count != expected_count:
            mismatches.append(f"{name} expected {expected_count}, observed {actual_count}")
    if mismatches:
        raise _JunieEvidenceInsufficient(
            f"Junie session ledger custom-agent lifecycle mismatch: {'; '.join(mismatches)}"
        )

    diagnostics = {
        "status": "name-verified",
        "definitionDigestBound": False,
        "agents": dict(sorted(expected_counts.items())),
        "lifecycles": [
            {
                "agentId": str(record["agentId"]),
                "name": str(record["name"]),
                "stepId": str(step_id),
                "statuses": list(record["statuses"]),
                "eventDigests": list(record["eventDigests"]),
            }
            for (_, step_id), record in sorted(observed.items())
        ],
        "controlledLookup": _audit_junie_staged_manifest(staged_manifest, staged),
        "parentChildVerified": False,
        "targetJudgeOrderVerified": False,
        "childConcurrencyVerified": False,
        "nestedDependencyConstraintsVerified": False,
    }
    raise _JunieEvidenceInsufficient(
        "Junie name-level lifecycle cannot bind the emitted custom agent to its staged definition or parent topology",
        diagnostics,
    )


def _blocked_junie_report(report: Mapping[str, Any], reason: str) -> dict[str, Any]:
    blocked = json.loads(json.dumps(report))
    for run_result in blocked.get("runs", []):
        for scenario in run_result.get("scenarioResults", []):
            scenario["status"] = "BLOCKED"
            scenario.setdefault("evidence", []).append(reason)
            scenario.setdefault("deterministicEvidence", []).append(reason)
    blocked["residualRisk"] = reason
    return blocked


def _run_live_junie_batch(
    batch: Sequence[_RunSpec],
    batch_number: int,
    result_root: Path,
    timeout_seconds: int,
) -> dict[str, Any]:
    label = f"batch-{batch_number:02d}"
    run_identity = f"junie-{label}-{secrets.token_hex(16)}"
    with _temporary_run_root(f"junie-{label}") as run_root:
        workspace, junie_home, skill_root, staged = _stage_junie_batch(batch, run_root)
        fixture_root = workspace / ".agent-suite-fixtures"
        fixture_root.mkdir()
        checkpoint_root = run_root / "checkpoints"
        checkpoint_root.mkdir()
        event_path = run_root / "junie-events.jsonl"
        cache_root = run_root / "junie-cache"
        agent_root = run_root / "junie-agents"
        command = [
            str(_bundled_junie_executable()),
            f"--project={workspace}",
            "--output-format=json-stream",
            f"--json-output-file={event_path}",
            f"--cache-dir={cache_root}",
            "--skip-update-check",
            "--config-default-locations=false",
            "--model-default-locations=false",
            "--mcp-default-locations=false",
            "--skill-default-locations=false",
            "--agent-default-location=false",
            "--command-default-location=false",
            f"--skill-location={skill_root}",
            f"--agent-location={agent_root}",
            f"--timeout={timeout_seconds * 1000}",
            f"--task={_junie_coordinator_prompt(batch, checkpoint_root, fixture_root, run_identity)}",
        ]
        environment = _controlled_environment(run_root / "home", junie_home, run_root / "tmp")
        environment.pop("CODEX_HOME", None)
        environment["JUNIE_HOME"] = str(junie_home)
        if "JUNIE_API_KEY" in os.environ:
            environment["JUNIE_API_KEY"] = os.environ["JUNIE_API_KEY"]
        completed = _run_process(command, workspace, environment, timeout_seconds, containment_root=run_root)
        result_root.mkdir(parents=True, exist_ok=True)
        evidence_prefix = result_root / label
        evidence_prefix.with_suffix(".stdout.log").write_text(_redact_capture(completed["stdout"]), encoding="utf-8")
        evidence_prefix.with_suffix(".stderr.log").write_text(_redact_capture(completed["stderr"]), encoding="utf-8")
        retained_events = evidence_prefix.with_suffix(".jsonl")
        if event_path.is_file():
            retained_events.write_text(_redact_capture(event_path.read_text(encoding="utf-8")), encoding="utf-8")
        retained_lifecycles = evidence_prefix.with_suffix(".lifecycles.jsonl")
        retained_lifecycles.write_text(
            "".join(f"{json.dumps(value, sort_keys=True)}\n" for value in _junie_lifecycle_evidence(junie_home)),
            encoding="utf-8",
        )
        retained_staged_root = result_root / f"{label}.staged-agents"
        staged_manifest = _retain_junie_staged_manifest(agent_root, retained_staged_root, staged)
        checkpoint_destination = result_root / f"{label}.checkpoints"
        if checkpoint_root.is_dir():
            shutil.copytree(checkpoint_root, checkpoint_destination, dirs_exist_ok=True)
        report: dict[str, Any] | None = None
        checkpoint_report: dict[str, Any] | None = None
        errors: list[str] = []
        try:
            checkpoint_report = _load_checkpoint_report(
                checkpoint_destination,
                batch,
                run_identity,
                require_runtime_judge_provenance=False,
                fixture_root=fixture_root,
            )
            report = _extract_junie_report(event_path)
            _audit_report(batch, report, checkpoint_report)
            _audit_checkpoint_agreement(report, checkpoint_report, batch)
            if checkpoint_report is not None:
                _attach_receipt_audits(report, checkpoint_report)
        except (json.JSONDecodeError, RuntimeError) as error:
            errors.append(str(error))
        try:
            identity = _audit_junie_agent_lifecycles(
                junie_home,
                batch,
                report or {},
                staged,
                staged_manifest,
            )
        except _JunieEvidenceInsufficient as error:
            identity = dict(error.diagnostics)
            identity["status"] = "unverified"
            identity["definitionDigestBound"] = False
            identity["blockedReason"] = str(error)
            if report is not None:
                report = _blocked_junie_report(report, str(error))
            else:
                errors.append(str(error))
        except RuntimeError as error:
            errors.append(str(error))
            identity = {"status": "unverified", "error": str(error)}
        try:
            cleanup = _audit_workspace_cleanup(workspace)
        except RuntimeError as error:
            errors.append(str(error))
            cleanup = "failed"
        if completed["exitCode"] != 0:
            errors.append(f"Junie exited with {completed['exitCode']}")
        if completed["cleanup"] != "clean":
            errors.append(f"Process cleanup: {completed['cleanup']}")
        return {
            "batch": batch_number,
            "runIdentity": run_identity,
            "harness": "junie",
            "status": "infrastructure-failed" if errors else "completed",
            "processExitCode": completed["exitCode"],
            "report": report,
            "infrastructureErrors": errors,
            "identityAudit": identity,
            "workspaceCleanup": cleanup,
            "evidence": {
                "events": str(retained_events),
                "lifecycles": str(retained_lifecycles),
                "stagedAgents": str(retained_staged_root),
                "checkpoints": str(checkpoint_destination),
                "stderr": str(evidence_prefix.with_suffix('.stderr.log')),
            },
        }


def _run_live_batch(
    batch: Sequence[_RunSpec],
    batch_number: int,
    result_root: Path,
    timeout_seconds: int,
) -> dict[str, Any]:
    label = f"batch-{batch_number:02d}"
    run_identity = f"codex-{label}-{secrets.token_hex(16)}"
    with _temporary_run_root(label) as run_root:
        workspace, codex_home, staged = _stage_batch(batch, run_root)
        capabilities = _runtime_capabilities(batch)
        checkpoint_root = run_root / "checkpoints"
        checkpoint_root.mkdir()
        fixture_root = workspace / ".agent-suite-fixtures"
        fixture_root.mkdir()
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
            _coordinator_prompt(batch, checkpoint_root, fixture_root, run_identity),
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
        checkpoint_destination = result_root / f"{label}.checkpoints"
        if checkpoint_root.is_dir():
            shutil.copytree(checkpoint_root, checkpoint_destination, dirs_exist_ok=True)
        partial_report: dict[str, Any] | None = None
        report_error: str | None = None
        try:
            checkpoint_report = _load_checkpoint_report(
                checkpoint_destination,
                batch,
                run_identity,
                fixture_root=fixture_root,
            )
        except (json.JSONDecodeError, RuntimeError) as checkpoint_error:
            checkpoint_report = None
            report_error = f"checkpoint error: {checkpoint_error}"
        try:
            partial_report = _extract_coordinator_report(completed["stdout"])
        except RuntimeError as error:
            report_error = f"{report_error}; {error}" if report_error else str(error)
            if checkpoint_report is not None:
                partial_report = checkpoint_report
        expected_invocation_counts = _expected_invocation_counts(batch, partial_report or {})
        identity_error: str | None = None
        try:
            identity = _audit_identity(
                staged,
                session_directory,
                expected_invocation_counts,
                batch,
                partial_report or {},
            )
            if checkpoint_report is not None:
                _bind_codex_judge_provenance(
                    checkpoint_report,
                    identity,
                    batch,
                    checkpoint_destination,
                    session_directory,
                    result_root,
                )
        except RuntimeError as error:
            identity_error = str(error)
            identity = {"rolloutCount": retained_session_count, "error": identity_error}
        if partial_report is not None:
            try:
                _audit_report(batch, partial_report, checkpoint_report)
                _audit_checkpoint_agreement(partial_report, checkpoint_report, batch)
                if checkpoint_report is not None:
                    _attach_receipt_audits(partial_report, checkpoint_report)
            except RuntimeError as error:
                report_error = f"{report_error}; {error}" if report_error else str(error)
                if checkpoint_report is not None:
                    partial_report = checkpoint_report
        browser_error: str | None = None
        try:
            browser_audit = _audit_browser_activity(codex_home, batch, identity, partial_report or {})
        except RuntimeError as error:
            browser_error = str(error)
            browser_audit = {"error": browser_error}
        concurrency_error: str | None = None
        retained_sessions = _load_sessions(codex_home)
        try:
            concurrency = _audit_session_concurrency(
                retained_sessions, maximum_threads, batch, partial_report or {}
            )
        except RuntimeError as error:
            concurrency_error = str(error)
            concurrency = {"error": concurrency_error}
        handoff_error: str | None = None
        try:
            _audit_handoff_evidence(batch, partial_report or {}, retained_sessions, fixture_root)
        except RuntimeError as error:
            handoff_error = str(error)
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
                handoff_error,
                cleanup_error,
            )
            if message
        ]
        return {
            "batch": batch_number,
            "runIdentity": run_identity,
            "status": "infrastructure-failed" if infrastructure_errors else "completed",
            "processExitCode": completed["exitCode"],
            "report": partial_report,
            "infrastructureErrors": infrastructure_errors,
            "identityAudit": identity,
            "browserAudit": browser_audit,
            "concurrencyAudit": concurrency,
            "handoffAudit": "bound" if handoff_error is None else {"error": handoff_error},
            "workspaceCleanup": workspace_cleanup,
            "capabilityPreflight": list(preflight_evidence),
            "evidence": {
                "events": str(evidence_prefix.with_suffix(".jsonl")),
                "stderr": str(evidence_prefix.with_suffix(".stderr.log")),
                "identity": str(identity_path),
                "identitySha256": _sha256(identity_path),
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
    parser.add_argument("--harness", required=True, choices=("codex", "junie"), help="Explicit execution harness.")
    parser.add_argument("--suite", action="append", default=[], help="Suite id to run; repeat for multiple suites.")
    parser.add_argument(
        "--scenario",
        action="append",
        default=[],
        help="Scenario selector in suite-id:scenario-id form; repeat for multiple scenarios.",
    )
    parser.add_argument("--jobs", type=int, default=4, help="Maximum concurrent supervisors, from 1 through 4.")
    parser.add_argument("--timeout-seconds", type=int, default=3600, help="Wall-clock limit for each coordinator batch.")
    parser.add_argument("--validate-only", action="store_true", help="Validate and schedule suites without invoking a harness.")
    parser.add_argument("--list", action="store_true", help="List validated suites and scenarios, then exit.")
    parser.add_argument(
        "--result-dir",
        type=Path,
        default=_SUITE_ROOT / "run-evidence",
        help="Runner-owned evidence directory outside disposable workspaces.",
    )
    return parser


def _reporting_main(argv: Sequence[str]) -> int:
    module_path = _SUITE_ROOT / "suite_reporting.py"
    specification = importlib.util.spec_from_file_location(
        "agent_suite_reporting_entrypoint",
        module_path,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"Cannot load suite reporting entry point: {module_path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return int(module.main(argv))


def main(argv: Sequence[str] | None = None) -> int:
    """Validate selections, execute bounded batches, and retain a machine-readable summary.

    Callers use the reporting subcommand for durable suite reports, or the execution flags to select
    suites or scenarios, cap supervisor concurrency, choose validation-only or live execution, and
    name the runner-owned evidence directory. Live execution creates isolated homes and workspaces,
    invokes Codex or Junie, records UTC and monotonic timing, retains partial failures, and removes
    disposable state before returning. The process returns zero only when every requested batch
    validates or completes without an infrastructure failure.
    """
    raw_arguments = tuple(sys.argv[1:] if argv is None else argv)
    if raw_arguments[:1] == ("reporting",):
        return _reporting_main(raw_arguments[1:])
    arguments = _argument_parser().parse_args(raw_arguments)
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
        live_runner = _run_live_batch if arguments.harness == "codex" else _run_live_junie_batch
        results = _execute_batches(
            batches,
            lambda batch, batch_number: live_runner(batch, batch_number, result_root, arguments.timeout_seconds),
        )
    result_root.mkdir(parents=True, exist_ok=True)
    summary_path = result_root / "summary.json"
    summary = {
        "schema": "dev-methodology-agent-suite-run-summary",
        "version": 1,
        "generatedAtUtc": _utc_now(),
        "harness": arguments.harness,
        "validateOnly": bool(arguments.validate_only),
        "maximumConcurrentSupervisors": arguments.jobs,
        "results": results,
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(summary_path)
    return 0 if all(result["status"] in {"validated", "completed"} for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
