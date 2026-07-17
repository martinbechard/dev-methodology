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
import signal
import shutil
import subprocess
import tempfile
import threading
import time
import tomllib
from collections.abc import Callable, Iterator, Sequence
from pathlib import Path
from typing import Any

import yaml


_SUITE_ROOT = Path(__file__).resolve().parent
_REPOSITORY_ROOT = _SUITE_ROOT.parents[1]
_RUNTIME_NAME = re.compile(r"^[a-z][a-z0-9_]*$")
_TERMINAL_STATUSES = frozenset({"PASS", "FAIL", "BLOCKED", "STALE"})
_EXECUTABLE_STATUSES = frozenset({"executable", "fixture-backed"})
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


@dataclasses.dataclass(frozen=True)
class _Session:
    session_id: str
    parent_thread_id: str | None
    invocation: str | None
    depth: int
    started_at: float
    finished_at: float


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
    for path_field in ("conceptualRole", "nativeAgent"):
        path = _REPOSITORY_ROOT / str(target.get(path_field, ""))
        if not path.is_file():
            raise ValueError(f"{suite.suite_id} has no {path_field}: {path}")
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
    return tuple(tuple(runs[start : start + maximum]) for start in range(0, len(runs), maximum))


@contextlib.contextmanager
def _temporary_run_root(label: str) -> Iterator[Path]:
    safe_label = re.sub(r"[^a-z0-9-]+", "-", label.lower()).strip("-") or "batch"
    with tempfile.TemporaryDirectory(prefix=f"dev-methodology-agent-{safe_label}-") as temporary:
        yield Path(temporary)


def _copy_agent(source: Path, invocation: str, agent_root: Path) -> _StagedAgent:
    if not _RUNTIME_NAME.fullmatch(invocation):
        raise ValueError(f"Invalid staged agent invocation: {invocation}")
    destination = agent_root / f"{invocation}.toml"
    shutil.copy2(source, destination)
    loaded = tomllib.loads(source.read_text(encoding="utf-8"))
    actual_name = loaded.get("name")
    if actual_name != invocation:
        raise ValueError(f"Staged agent name mismatch: expected {invocation}, found {actual_name}")
    instructions = str(loaded.get("developer_instructions", ""))
    if not instructions:
        raise ValueError(f"Staged agent has no developer instructions: {source}")
    return _StagedAgent(invocation, source, instructions, _sha256(source))


def _copy_skill_package(skill_file: Path, skill_root: Path) -> None:
    package = skill_file.resolve().parent
    destination = skill_root / package.name
    if destination.exists():
        return
    shutil.copytree(package, destination)


def _validate_target_skills(suite: _Suite, scenario_ids: Sequence[str], repository_root: Path) -> None:
    selected = set(scenario_ids)
    for scenario in suite.scenarios:
        if str(scenario["id"]) not in selected:
            continue
        for skill_name in scenario.get("targetSkills", []):
            source = repository_root / "skills" / str(skill_name) / "SKILL.md"
            if not source.is_file():
                raise ValueError(f"{suite.suite_id}:{scenario['id']} requires missing skill {skill_name}")


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
                                "required": ["scenario", "status", "identityEvidence", "cleanup", "evidence"],
                                "properties": {
                                    "scenario": {"type": "string"},
                                    "status": {"type": "string", "enum": sorted(_TERMINAL_STATUSES)},
                                    "identityEvidence": {"type": "array", "minItems": 1, "items": {"type": "string"}},
                                    "cleanup": {"type": "string", "enum": ["clean"]},
                                    "evidence": {"type": "array", "minItems": 1, "items": {"type": "string"}},
                                },
                            },
                        },
                        "maximumActiveChildrenObserved": {"type": "integer", "minimum": 0, "maximum": 1},
                        "cleanup": {"type": "string", "enum": ["clean"]},
                    },
                },
            },
            "batchCleanup": {"type": "string", "enum": ["clean"]},
            "residualRisk": {"type": "string"},
        },
    }


def _coordinator_prompt(batch: Sequence[_RunSpec]) -> str:
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
            }
        )
    return (
        "Coordinate this governed synthetic evaluation batch. Spawn every listed custom supervisor concurrently, "
        "using its exact supervisor value as task_name. Give each supervisor only its listed suite and scenarios, plus "
        "an explicit instruction to pass task_name exactly equal to the listed target and judge for those child spawns. "
        "Each supervisor must run its selected scenarios sequentially, use exactly one active child at a time, invoke "
        "only those hardcoded agents, retain one independent result per scenario, "
        "and clean every fixture, claim, process, worktree, and credential it owns. One supervisor child may use one "
        "declared nested dependency at a time only where nestedAgentLimit is 1; serialize that temporary tenth-agent "
        "slot across the batch. Do not browse, install software, read outside this disposable repository, alter the "
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
        observed[suite_id] = {str(value.get("scenario", "")) for value in scenario_results}
        for scenario_result in scenario_results:
            if scenario_result.get("status") not in _TERMINAL_STATUSES:
                raise RuntimeError(f"Invalid terminal status for {suite_id}:{scenario_result.get('scenario')}")
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
        events = []
        for line in rollout.read_text(encoding="utf-8", errors="replace").splitlines():
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
        agent_path = metadata.get("agent_path") or spawn.get("agent_path")
        invocation = str(agent_path).rsplit("/", 1)[-1] if agent_path else None
        sessions.append(
            _Session(
                session_id=str(metadata.get("id", rollout.stem)),
                parent_thread_id=metadata.get("parent_thread_id"),
                invocation=invocation,
                depth=int(spawn.get("depth", 0)),
                started_at=_timestamp_seconds(str(events[0]["timestamp"])),
                finished_at=_timestamp_seconds(str(events[-1]["timestamp"])),
            )
        )
    return tuple(sessions)


def _audit_identity(
    staged: Sequence[_StagedAgent],
    codex_home: Path,
    required_invocations: set[str],
) -> dict[str, Any]:
    sessions = _load_sessions(codex_home)
    observed = {session.invocation for session in sessions if session.invocation}
    agents = []
    for agent in staged:
        exact_session = agent.invocation in observed
        required = agent.invocation in required_invocations
        agents.append(
            {
                "invocation": agent.invocation,
                "definitionSha256": agent.sha256,
                "required": required,
                "exactCustomAgentSession": exact_session,
                "instructionBinding": "staged-definition-digest-bound-to-exact-agent-path" if exact_session else "missing",
            }
        )
        if required and not exact_session:
            raise RuntimeError(f"Missing exact custom-agent session for {agent.invocation}")
    return {"rolloutCount": len(sessions), "agents": agents}


def _audit_session_concurrency(sessions: Sequence[_Session], maximum_threads: int) -> dict[str, int]:
    by_parent: dict[str, list[_Session]] = {}
    for session in sessions:
        if session.parent_thread_id:
            by_parent.setdefault(session.parent_thread_id, []).append(session)
    supervisors = {session.session_id for session in sessions if session.depth == 1}
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
        if active > 9 and active_nested > 1:
            raise RuntimeError("Temporary tenth-agent slot was not serialized")
    return {"maximumActiveSessions": maximum_active, "maximumChildrenObserved": maximum_children}


def _required_invocations(batch: Sequence[_RunSpec], report: dict[str, Any]) -> set[str]:
    required = {run.suite.manifest["execution"]["supervisorInvocation"] for run in batch}
    reports = {str(item.get("suite", "")): item for item in report.get("runs", [])}
    for run in batch:
        item = reports.get(run.suite.suite_id, {})
        statuses = {result.get("status") for result in item.get("scenarioResults", [])}
        if statuses and statuses <= {"BLOCKED", "STALE"}:
            continue
        execution = run.suite.manifest["execution"]
        required.add(execution["targetInvocation"])
        required.add(execution["judgeInvocation"])
    return required


def _retain_sessions(codex_home: Path, destination: Path) -> int:
    count = 0
    destination.mkdir(parents=True, exist_ok=True)
    for rollout in codex_home.glob("**/rollout-*.jsonl"):
        target = destination / rollout.name
        target.write_text(_redact_capture(rollout.read_text(encoding="utf-8", errors="replace")), encoding="utf-8")
        count += 1
    return count


def _controlled_environment(home: Path, codex_home: Path, temporary: Path) -> dict[str, str]:
    environment = {"PATH": os.environ.get("PATH", "/usr/bin:/bin")}
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
    return environment


def _kill_process_group(pid: int) -> None:
    try:
        os.killpg(pid, signal.SIGKILL)
    except (PermissionError, ProcessLookupError):
        pass


def _run_process(
    argv: Sequence[str],
    cwd: Path,
    environment: dict[str, str],
    timeout_seconds: float,
) -> dict[str, Any]:
    process = subprocess.Popen(
        list(argv),
        cwd=cwd,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False,
        start_new_session=True,
    )
    buffers = {"stdout": bytearray(), "stderr": bytearray()}
    exceeded = threading.Event()

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
        _kill_process_group(process.pid)
    for thread in threads:
        thread.join()
    if process.stdout is not None:
        process.stdout.close()
    if process.stderr is not None:
        process.stderr.close()
    stdout = bytes(buffers["stdout"]).decode("utf-8", errors="replace")
    stderr = bytes(buffers["stderr"]).decode("utf-8", errors="replace")
    if timed_out:
        return {"exitCode": 124, "stdout": stdout, "stderr": f"{stderr}\nprocess timed out".lstrip(), "cleanup": "clean"}
    if exceeded.is_set():
        return {"exitCode": 125, "stdout": stdout, "stderr": f"{stderr}\nprocess output limit exceeded".lstrip(), "cleanup": "clean"}
    return {"exitCode": int(process.returncode), "stdout": stdout, "stderr": stderr, "cleanup": "clean"}


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
        schema_path = run_root / "coordinator-output-schema.json"
        schema_path.write_text(json.dumps(_coordinator_schema(), indent=2) + "\n", encoding="utf-8")
        temporary_home = run_root / "home"
        temporary_dir = run_root / "tmp"
        maximum_threads = 10 if any(int(run.suite.manifest["execution"].get("nestedAgentLimit", 0)) == 1 for run in batch) else 9
        command = [
            "codex",
            "--enable",
            "multi_agent",
            "--enable",
            "use_agent_identity",
            "-c",
            f"agents.max_threads={maximum_threads}",
            "-c",
            "agents.max_depth=3",
            "--ask-for-approval",
            "never",
            "--sandbox",
            "workspace-write",
            "--add-dir",
            str(workspace / ".git"),
            "exec",
            "--json",
            "--ignore-user-config",
            "--ignore-rules",
            "--output-schema",
            str(schema_path),
            "-C",
            str(workspace),
            _coordinator_prompt(batch),
        ]
        environment = _controlled_environment(temporary_home, codex_home, temporary_dir)
        completed = _run_process(
            command,
            workspace,
            environment,
            timeout_seconds,
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
            partial_report = _extract_coordinator_report(completed["stdout"])
            _audit_report(batch, partial_report)
        except RuntimeError as error:
            report_error = str(error)
        required = _required_invocations(batch, partial_report or {})
        identity_error: str | None = None
        try:
            identity = _audit_identity(staged, codex_home, required)
        except RuntimeError as error:
            identity_error = str(error)
            identity = {"rolloutCount": retained_session_count, "error": identity_error}
        concurrency_error: str | None = None
        try:
            concurrency = _audit_session_concurrency(_load_sessions(codex_home), maximum_threads)
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
                report_error,
                identity_error,
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
            "concurrencyAudit": concurrency,
            "workspaceCleanup": workspace_cleanup,
            "evidence": {
                "events": str(evidence_prefix.with_suffix(".jsonl")),
                "stderr": str(evidence_prefix.with_suffix(".stderr.log")),
                "identity": str(identity_path),
                "sessions": str(session_directory),
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
