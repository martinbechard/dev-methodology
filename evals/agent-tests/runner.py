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
import shutil
import subprocess
import tempfile
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


def _load_catalog(suite_root: Path = _SUITE_ROOT) -> dict[str, _Suite]:
    index = _load_yaml(suite_root / "suite-index.yaml")
    suites: dict[str, _Suite] = {}
    for entry in index.get("suites", []):
        suite_id = str(entry["id"])
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
        _validate_suite(suite)
        if suite_id in suites:
            raise ValueError(f"Duplicate suite id: {suite_id}")
        suites[suite_id] = suite
    if not suites:
        raise ValueError("The suite index contains no suites")
    return suites


def _validate_suite(suite: _Suite) -> None:
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
        if scenario.get("status") not in _EXECUTABLE_STATUSES:
            raise ValueError(f"{suite.suite_id}:{scenario_id} is not executable")
        executable_case = scenario.get("executableCase")
        if not isinstance(executable_case, str) or not executable_case.strip():
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
            if source.is_file():
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
                        "scenarios",
                        "status",
                        "maximumActiveChildrenObserved",
                        "identityEvidence",
                        "cleanup",
                        "evidence",
                    ],
                    "properties": {
                        "suite": {"type": "string"},
                        "scenarios": {"type": "array", "items": {"type": "string"}},
                        "status": {"type": "string", "enum": sorted(_TERMINAL_STATUSES)},
                        "maximumActiveChildrenObserved": {"type": "integer", "minimum": 0, "maximum": 1},
                        "identityEvidence": {"type": "array", "items": {"type": "string"}},
                        "cleanup": {"type": "string"},
                        "evidence": {"type": "array", "items": {"type": "string"}},
                    },
                },
            },
            "batchCleanup": {"type": "string"},
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
                "scenarios": list(run.scenario_ids),
                "nestedAgentLimit": int(execution.get("nestedAgentLimit", 0)),
            }
        )
    return (
        "Coordinate this governed synthetic evaluation batch. Spawn every listed custom supervisor concurrently, "
        "using its exact supervisor value as the custom agent type. Give each supervisor only its listed suite and "
        "scenarios. Each supervisor must run its selected scenarios sequentially, use exactly one active child at a "
        "time, invoke only the hardcoded target and Judge from suite.yaml, retain deterministic and semantic evidence, "
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


def _audit_report(batch: Sequence[_RunSpec], report: dict[str, Any]) -> None:
    expected = {run.suite.suite_id: set(run.scenario_ids) for run in batch}
    observed: dict[str, set[str]] = {}
    for item in report.get("runs", []):
        suite_id = str(item.get("suite", ""))
        if suite_id in observed:
            raise RuntimeError(f"Duplicate coordinator result for {suite_id}")
        observed[suite_id] = {str(value) for value in item.get("scenarios", [])}
        if item.get("status") not in _TERMINAL_STATUSES:
            raise RuntimeError(f"Invalid terminal status for {suite_id}: {item.get('status')}")
        if int(item.get("maximumActiveChildrenObserved", -1)) > 1:
            raise RuntimeError(f"Child concurrency exceeded for {suite_id}")
    if observed != expected:
        raise RuntimeError(f"Coordinator result coverage mismatch: expected {expected}, observed {observed}")


def _audit_identity(staged: Sequence[_StagedAgent], codex_home: Path) -> dict[str, Any]:
    rollouts = tuple(codex_home.glob("**/rollout-*.jsonl"))
    combined = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in rollouts)
    agents = []
    for agent in staged:
        agents.append(
            {
                "invocation": agent.invocation,
                "definitionSha256": agent.sha256,
                "nameObserved": agent.invocation in combined,
                "instructionsObserved": agent.developer_instructions in combined,
            }
        )
    return {"rolloutCount": len(rollouts), "agents": agents}


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
        environment = os.environ.copy()
        environment.update(
            {
                "CODEX_HOME": str(codex_home),
                "HOME": str(temporary_home),
                "TMPDIR": str(temporary_dir),
                "GIT_AUTHOR_NAME": "Synthetic Agent Eval",
                "GIT_AUTHOR_EMAIL": "agent-eval@example.invalid",
                "GIT_COMMITTER_NAME": "Synthetic Agent Eval",
                "GIT_COMMITTER_EMAIL": "agent-eval@example.invalid",
            }
        )
        completed = subprocess.run(
            command,
            cwd=workspace,
            env=environment,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
        result_root.mkdir(parents=True, exist_ok=True)
        evidence_prefix = result_root / label
        evidence_prefix.with_suffix(".jsonl").write_text(_redact_capture(completed.stdout), encoding="utf-8")
        evidence_prefix.with_suffix(".stderr.log").write_text(_redact_capture(completed.stderr), encoding="utf-8")
        identity = _audit_identity(staged, codex_home)
        identity_path = evidence_prefix.with_suffix(".identity.json")
        identity_path.write_text(json.dumps(identity, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if completed.returncode != 0:
            raise RuntimeError(f"Codex batch {batch_number} exited with {completed.returncode}")
        report = _extract_coordinator_report(completed.stdout)
        _audit_report(batch, report)
        return {
            "batch": batch_number,
            "status": "completed",
            "processExitCode": completed.returncode,
            "report": report,
            "identityAudit": identity,
            "evidence": {
                "events": str(evidence_prefix.with_suffix(".jsonl")),
                "stderr": str(evidence_prefix.with_suffix(".stderr.log")),
                "identity": str(identity_path),
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
    catalog = _load_catalog()
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
