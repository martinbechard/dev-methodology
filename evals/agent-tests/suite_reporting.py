#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Runs agent suites with bounded parallelism and renders durable offline HTML reports.
# Governing design: backlog/feature-backlog/automate-parallel-agent-test-reporting.md
# Governing test plan: evals/agent-tests/test_suite_reporting.py

from __future__ import annotations

import argparse
import concurrent.futures
import dataclasses
import datetime as dt
import hashlib
import html
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path, PurePosixPath
from typing import Any

import yaml


_ROOT = Path(__file__).resolve().parent
_REPOSITORY_ROOT = _ROOT.parents[1]
_CATALOG_PATH = _ROOT / "suite-index.yaml"
_RUNNER_PATH = _ROOT / "runner.py"
_HARNESSES = frozenset({"codex", "junie"})
_TERMINAL_STATUSES = frozenset(
    {"PASS", "FAIL", "BLOCKED", "STALE", "INFRASTRUCTURE_FAILED"}
)
_VISIBLE_INPUT_STATES = frozenset(
    {
        "CURRENT",
        "MISSING",
        "STALE",
        "MALFORMED",
        "DUPLICATE",
        "INCOMPATIBLE_REVISION",
        "MIXED_HARNESS",
    }
)
_ABSOLUTE_WORKER_LIMIT = 4
_MEMORY_BYTES_PER_WORKER = 2 * 1024**3
_SCHEMA = "dev-methodology-agent-suite-report"
_POINTER_SCHEMA = "dev-methodology-agent-suite-report-pointer"
_EVIDENCE_BUNDLE_SCHEMA = "dev-methodology-agent-suite-evidence-bundle"
_EVIDENCE_RECEIPT_SCHEMA = "dev-methodology-agent-suite-evidence-receipt"
_JUDGE_OUTPUT_SCHEMA = "dev-methodology-agent-suite-judge-output"
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
_JUDGE_PROVENANCE_FIELDS = {
    "status", "sessionId", "parentSessionId", "invocation", "runIdentity",
    "suite", "scenario", "rolloutPath", "rolloutSha256", "responseEventIndex",
    "responsePath", "responseSha256", "outputPath", "outputSha256", "disposition",
}


@dataclasses.dataclass(frozen=True)
class HostResources:
    """Describe the portable processor and memory measurements used to bound workers."""

    processor_count: int
    available_memory_bytes: int


@dataclasses.dataclass(frozen=True)
class SuiteExecution:
    """Capture one isolated suite execution result returned by an execution adapter."""

    exit_code: int
    summary: Mapping[str, Any] | None
    stdout: str = ""
    stderr: str = ""


SuiteExecutor = Callable[[str, str, Path, int], SuiteExecution]
SafetyProbe = Callable[[HostResources], bool]


def _utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def _atomic_write(path: Path, content: str) -> None:
    """Replace one report file only after complete bytes are durable in its directory."""

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _atomic_write_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def catalog_suite_ids(path: Path = _CATALOG_PATH) -> tuple[str, ...]:
    """Return suite ids in governed catalog priority order."""

    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    suites = loaded.get("suites", []) if isinstance(loaded, dict) else []
    if not isinstance(suites, list):
        raise ValueError("suite-index.yaml suites must be a list")
    values: list[tuple[int, str]] = []
    for item in suites:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            raise ValueError("each suite catalog entry must have a string id")
        values.append((int(item.get("priority", 0)), item["id"]))
    ids = [suite_id for _, suite_id in sorted(values)]
    if len(ids) != len(set(ids)):
        raise ValueError("suite catalog contains duplicate ids")
    return tuple(ids)


def select_suites(catalog: Sequence[str], requested: Sequence[str]) -> tuple[str, ...]:
    """Validate one, many, or default-all suite selectors before harness execution."""

    duplicates = sorted({value for value in requested if requested.count(value) > 1})
    if duplicates:
        raise ValueError(f"duplicate suite selections: {', '.join(duplicates)}")
    unknown = sorted(set(requested) - set(catalog))
    if unknown:
        raise ValueError(f"unknown suite selections: {', '.join(unknown)}")
    chosen = set(requested) if requested else set(catalog)
    return tuple(value for value in catalog if value in chosen)


def discover_resources() -> HostResources:
    """Measure portable processor and available-memory bounds without third-party packages."""

    processors = max(1, os.cpu_count() or 1)
    available = 0
    if hasattr(os, "sysconf"):
        try:
            page_size = int(os.sysconf("SC_PAGE_SIZE"))
            available_pages = int(os.sysconf("SC_AVPHYS_PAGES"))
            available = page_size * available_pages
        except (OSError, ValueError):
            available = 0
    if available <= 0:
        try:
            completed = subprocess.run(
                ("vm_stat",), capture_output=True, text=True, check=False, timeout=2
            )
            page_match = re.search(r"page size of (\d+) bytes", completed.stdout)
            page_size = int(page_match.group(1)) if page_match else 4096
            pages = sum(
                int(match.group(1))
                for name in ("free", "inactive", "speculative", "purgeable")
                if (match := re.search(rf"Pages {name}:\s+(\d+)", completed.stdout))
            )
            available = page_size * pages
        except (OSError, ValueError, subprocess.TimeoutExpired):
            available = 0
    return HostResources(processors, max(0, available))


def resolve_workers(
    selected_count: int, resources: HostResources, override: int | None = None
) -> int:
    """Resolve a finite worker count capped by suites, processors, memory, and policy."""

    if selected_count < 1:
        raise ValueError("at least one suite must be selected")
    if override is not None and not 1 <= override <= _ABSOLUTE_WORKER_LIMIT:
        raise ValueError(
            f"maximum workers must be between 1 and {_ABSOLUTE_WORKER_LIMIT}"
        )
    if resources.available_memory_bytes <= 0:
        raise ValueError("available memory could not be measured safely")
    memory_bound = resources.available_memory_bytes // _MEMORY_BYTES_PER_WORKER
    if memory_bound < 1:
        raise ValueError(
            f"available memory is below the {_MEMORY_BYTES_PER_WORKER}-byte per-worker safety bound"
        )
    processor_bound = max(1, resources.processor_count // 2)
    safe = min(selected_count, processor_bound, memory_bound, _ABSOLUTE_WORKER_LIMIT)
    return min(safe, override) if override is not None else safe


def _source_revision(repository: Path = _REPOSITORY_ROOT) -> str:
    completed = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=repository,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"unable to resolve source revision: {completed.stderr.strip()}"
        )
    return completed.stdout.strip()


def _suite_digest(suite_id: str, harness: str = "codex") -> str:
    digest = hashlib.sha256()
    paths = [
        _CATALOG_PATH,
        _ROOT / suite_id / "suite.yaml",
        _ROOT / suite_id / "scenarios.yaml",
    ]
    manifest = yaml.safe_load(paths[1].read_text(encoding="utf-8"))
    target = manifest.get("target", {}) if isinstance(manifest, dict) else {}
    for field in ("conceptualRole", "nativeAgent"):
        relative = target.get(field) if isinstance(target, dict) else None
        if isinstance(relative, str):
            if harness == "junie" and field == "nativeAgent":
                relative = relative.replace(
                    "generated/adapters/codex/agents/",
                    "generated/adapters/junie/agents/",
                )
                relative = str(Path(relative).with_suffix(".md"))
            paths.append(_REPOSITORY_ROOT / relative)
    for path in sorted({value.resolve() for value in paths}, key=str):
        digest.update(str(path.relative_to(_REPOSITORY_ROOT)).encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _default_executor(
    harness: str, suite_id: str, result_dir: Path, timeout_seconds: int
) -> SuiteExecution:
    command = (
        sys.executable,
        str(_RUNNER_PATH),
        "--harness",
        harness,
        "--suite",
        suite_id,
        "--jobs",
        "1",
        "--timeout-seconds",
        str(timeout_seconds),
        "--result-dir",
        str(result_dir),
    )
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    summary_path = result_dir / "summary.json"
    summary: Mapping[str, Any] | None = None
    if summary_path.is_file():
        try:
            loaded = json.loads(summary_path.read_text(encoding="utf-8"))
            summary = loaded if isinstance(loaded, dict) else None
        except json.JSONDecodeError:
            summary = None
    return SuiteExecution(
        completed.returncode, summary, completed.stdout, completed.stderr
    )


def _scenario_rows(execution: SuiteExecution) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for batch in (execution.summary or {}).get("results", []):
        report = batch.get("report") if isinstance(batch, dict) else None
        evidence = batch.get("evidence") if isinstance(batch, dict) else None
        checkpoint_root = (
            evidence.get("checkpoints") if isinstance(evidence, Mapping) else None
        )
        identity_path = evidence.get("identity") if isinstance(evidence, Mapping) else None
        identity_digest = (
            evidence.get("identitySha256") if isinstance(evidence, Mapping) else None
        )
        run_identity = batch.get("runIdentity") if isinstance(batch, Mapping) else None
        for run in report.get("runs", []) if isinstance(report, dict) else []:
            for scenario in (
                run.get("scenarioResults", []) if isinstance(run, dict) else []
            ):
                if isinstance(scenario, dict):
                    row = dict(scenario)
                    if isinstance(checkpoint_root, str):
                        row["_checkpointRoot"] = checkpoint_root
                    if isinstance(identity_path, str) and isinstance(identity_digest, str):
                        row["_identityAudit"] = {
                            "path": identity_path,
                            "sha256": identity_digest,
                        }
                    if isinstance(run_identity, str):
                        row["_runIdentity"] = run_identity
                    rows.append(row)
    return rows


def _terminal_status(
    execution: SuiteExecution, scenarios: Sequence[Mapping[str, Any]]
) -> str:
    if execution.exit_code != 0 or execution.summary is None:
        return "INFRASTRUCTURE_FAILED"
    statuses = [
        str(value.get("status", "INFRASTRUCTURE_FAILED")).upper() for value in scenarios
    ]
    for status in ("INFRASTRUCTURE_FAILED", "FAIL", "BLOCKED", "STALE"):
        if status in statuses:
            return status
    return "PASS" if statuses else "INFRASTRUCTURE_FAILED"


def _governed_evidence_error(
    scenario: Mapping[str, Any], suite_id: str
) -> str | None:
    terminal_status = str(scenario.get("status", "")).upper()
    if terminal_status not in {"PASS", "FAIL"}:
        return None
    references = scenario.get("evidenceReceipts")
    if not isinstance(references, list) or not references or any(
        not isinstance(value, Mapping)
        or set(value) != {"path", "sha256"}
        or not isinstance(value.get("path"), str)
        or not isinstance(value.get("sha256"), str)
        or not re.fullmatch(r"[0-9a-f]{64}", str(value.get("sha256")))
        for value in references
    ):
        return "validated path- and SHA-256-bound evidence receipts were not retained"
    receipt_audit = scenario.get("receiptAudit")
    if not isinstance(receipt_audit, Mapping) or receipt_audit.get("status") != "verified":
        return "the runner did not verify the retained evidence receipts"
    deterministic = receipt_audit.get("deterministicChecks")
    if not isinstance(deterministic, list) or not deterministic:
        return "the exact deterministic-check receipts were not verified"
    judge_invoked = scenario.get("judgeInvoked")
    if not isinstance(judge_invoked, bool):
        return "the Judge invocation disposition was not retained"
    judge_disposition = receipt_audit.get("judgeDisposition")
    if judge_invoked is True:
        expected = "passed" if terminal_status == "PASS" else "failed"
        if judge_disposition != expected:
            return f"the actual Judge disposition is not {expected}"
        provenance = receipt_audit.get("judgeProvenance")
        if (
            not isinstance(provenance, Mapping)
            or provenance.get("status") != "verified"
            or provenance.get("runIdentity") != receipt_audit.get("runIdentity")
            or provenance.get("disposition") != expected
            or provenance.get("suite") != suite_id
            or provenance.get("scenario") != scenario.get("scenario")
        ):
            return "the actual Judge child session response was not retained"
    elif (
        terminal_status != "FAIL"
        or judge_disposition != "skipped-critical-failure"
        or not isinstance(receipt_audit.get("failedCriticalCheck"), str)
    ):
        return "the exact failed-critical-check Judge-skip disposition was not verified"
    return None


def suite_metadata(
    harness: str,
    suite_id: str,
    execution: SuiteExecution,
    *,
    source_revision: str,
    suite_digest: str,
    started_at: str,
    finished_at: str,
    elapsed_seconds: float,
    evidence_root: Path,
) -> dict[str, Any]:
    """Normalize one runner result into the stable machine-readable report contract."""

    scenarios = _scenario_rows(execution)
    evidence_errors: list[str] = []
    for scenario in scenarios:
        error = _governed_evidence_error(scenario, suite_id)
        if error is None:
            continue
        scenario_id = str(scenario.get("scenario", "unknown"))
        evidence_errors.append(f"{scenario_id}: {error}")
        scenario["status"] = "INFRASTRUCTURE_FAILED"
        scenario.setdefault("evidence", []).append(f"Governed evidence rejection: {error}.")
    status = _terminal_status(execution, scenarios)
    omissions: list[str] = []
    if execution.summary is None:
        omissions.append("runner summary unavailable or malformed")
    if not scenarios:
        omissions.append("no governed scenario results were retained")
    if evidence_errors:
        omissions.append("unsupported terminal verdicts demoted: " + "; ".join(evidence_errors))
    missing_receipts = [
        str(scenario.get("scenario", "unknown"))
        for scenario in scenarios
        if not isinstance(scenario.get("receiptAudit"), Mapping)
        or scenario.get("receiptAudit", {}).get("status") != "verified"
    ]
    missing_judge = [
        str(scenario.get("scenario", "unknown"))
        for scenario in scenarios
        if scenario.get("judgeInvoked") is True
        and (
            not isinstance(scenario.get("receiptAudit"), Mapping)
            or scenario.get("receiptAudit", {}).get("judgeDisposition")
            not in {"passed", "failed", "blocked", "stale"}
        )
    ]
    if missing_receipts:
        omissions.append(
            "validated deterministic and Judge receipts unavailable for "
            + ", ".join(missing_receipts)
        )
    if missing_judge:
        omissions.append(
            "actual Judge disposition unavailable for " + ", ".join(missing_judge)
        )
    return {
        "schema": _SCHEMA,
        "version": 1,
        "identity": f"{harness}:{suite_id}",
        "harness": harness,
        "suite": suite_id,
        "sourceRevision": source_revision,
        "suiteDigest": suite_digest,
        "startedAtUtc": started_at,
        "finishedAtUtc": finished_at,
        "elapsedSeconds": round(elapsed_seconds, 6),
        "status": status,
        "scenarioResults": scenarios,
        "deterministicEvidence": [
            value
            for scenario in scenarios
            for value in scenario.get("deterministicEvidence", [])
            if isinstance(value, str)
        ],
        "modelJudgeEvidence": [
            value
            for scenario in scenarios
            for value in scenario.get("modelJudgeEvidence", [])
            if isinstance(value, str)
        ],
        "evidenceReceipts": [
            dict(value)
            for scenario in scenarios
            for value in scenario.get("evidenceReceipts", [])
            if isinstance(value, Mapping)
        ],
        "receiptAudits": [
            dict(scenario["receiptAudit"])
            for scenario in scenarios
            if isinstance(scenario.get("receiptAudit"), Mapping)
        ],
        "omissions": omissions,
        "evidenceRoot": str(evidence_root),
        "runnerExitCode": execution.exit_code,
        "runnerStderr": execution.stderr[-4000:],
        "machine": {
            "platform": platform.system(),
            "architecture": platform.machine(),
            "python": platform.python_version(),
        },
    }


def _embedded_metadata(metadata: Mapping[str, Any]) -> str:
    encoded = json.dumps(metadata, sort_keys=True, separators=(",", ":")).replace(
        "</", "<\\/"
    )
    return f'<script id="report-metadata" type="application/json">{encoded}</script>'


def render_suite_html(metadata: Mapping[str, Any]) -> str:
    """Render one self-contained accessible suite report without network dependencies."""

    rows = []
    for scenario in metadata.get("scenarioResults", []):
        rows.append(
            '<tr><th scope="row">{}</th><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
                html.escape(str(scenario.get("scenario", "unknown"))),
                html.escape(str(scenario.get("status", "unknown"))),
                html.escape(
                    "; ".join(str(value) for value in scenario.get("evidence", []))
                ),
                html.escape(
                    "; ".join(
                        str(value)
                        for value in scenario.get("deterministicEvidence", [])
                    )
                ),
                html.escape(
                    "; ".join(
                        str(value) for value in scenario.get("modelJudgeEvidence", [])
                    )
                ),
            )
        )
    omissions = (
        "".join(
            f"<li>{html.escape(str(value))}</li>"
            for value in metadata.get("omissions", [])
        )
        or "<li>None</li>"
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(str(metadata["suite"]))} {html.escape(str(metadata["harness"]))} report</title>
<style>body{{font:16px system-ui,sans-serif;line-height:1.5;margin:auto;max-width:72rem;padding:1rem;color:#18212b;background:#fff}}a{{color:#0645ad}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #667;padding:.55rem;text-align:left;vertical-align:top}}.status{{font-weight:700}}@media(max-width:40rem){{table{{display:block;overflow-x:auto}}}}</style></head>
<body><main><h1>{html.escape(str(metadata["suite"]))}</h1><p class="status">{html.escape(str(metadata["status"]))} · {html.escape(str(metadata["harness"]))}</p>
<h2>Run identity</h2><dl><dt>Source revision</dt><dd>{html.escape(str(metadata["sourceRevision"]))}</dd><dt>Suite digest</dt><dd>{html.escape(str(metadata["suiteDigest"]))}</dd><dt>Elapsed</dt><dd>{metadata["elapsedSeconds"]} seconds</dd></dl>
<h2>Scenario results</h2><table><thead><tr><th scope="col">Scenario</th><th scope="col">Status</th><th scope="col">Evidence</th><th scope="col">Deterministic diagnostics</th><th scope="col">Judge diagnostics</th></tr></thead><tbody>{"".join(rows) or '<tr><td colspan="5">No scenario results retained.</td></tr>'}</tbody></table>
<h2>Omissions</h2><ul>{omissions}</ul><h2>Retained evidence</h2><p>{html.escape(str(metadata["evidenceRoot"]))}</p></main>{_embedded_metadata(metadata)}</body></html>\n"""


def _safe_relative(value: object) -> PurePosixPath | None:
    if (
        not isinstance(value, str)
        or not value
        or "\\" in value
        or PurePosixPath(value).is_absolute()
        or any(part in {"", ".", ".."} for part in PurePosixPath(value).parts)
    ):
        return None
    return PurePosixPath(value)


def _judge_rollout_binding_error(
    rollout_bytes: bytes,
    response_bytes: bytes,
    provenance: Mapping[str, Any],
) -> str | None:
    """Independently bind one retained Judge final response to its child rollout."""

    try:
        rollout_events = [
            json.loads(line) for line in rollout_bytes.decode("utf-8").splitlines()
        ]
    except (UnicodeError, json.JSONDecodeError):
        return "Judge rollout is malformed"
    eligible_responses: list[tuple[int, str]] = []
    for index, event in enumerate(rollout_events):
        payload = event.get("payload") if isinstance(event, Mapping) else None
        content = payload.get("content") if isinstance(payload, Mapping) else None
        item = (
            content[0]
            if isinstance(content, list)
            and len(content) == 1
            and isinstance(content[0], Mapping)
            else None
        )
        if (
            isinstance(payload, Mapping)
            and event.get("type") == "response_item"
            and payload.get("type") == "message"
            and payload.get("role") == "assistant"
            and payload.get("phase") == "final_answer"
            and isinstance(item, Mapping)
            and item.get("type") == "output_text"
            and isinstance(item.get("text"), str)
        ):
            eligible_responses.append((index, str(item["text"])))
    if len(eligible_responses) != 1:
        return (
            "Judge rollout must contain exactly one eligible terminal assistant "
            "final_answer"
        )
    response_index, response_text = eligible_responses[0]
    if type(provenance.get("responseEventIndex")) is not int or provenance.get(
        "responseEventIndex"
    ) != response_index:
        return "Judge responseEventIndex does not identify the sole eligible terminal response"
    if response_text.encode("utf-8") != response_bytes:
        return "Judge rollout response bytes mismatch"
    session_payloads = [
        event.get("payload")
        for event in rollout_events
        if isinstance(event, Mapping)
        and event.get("type") == "session_meta"
        and isinstance(event.get("payload"), Mapping)
    ]
    if (
        len(session_payloads) != 1
        or session_payloads[0].get("id") != provenance.get("sessionId")
        or session_payloads[0].get("parent_thread_id")
        != provenance.get("parentSessionId")
        or session_payloads[0].get("agent_role") != provenance.get("invocation")
    ):
        return "Judge rollout session binding mismatch"
    return None


def _bundle_evidence(
    metadata: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, bytes], dict[str, Any]]:
    prepared = json.loads(json.dumps(metadata))
    diagnostics: list[str] = []
    entries: list[dict[str, Any]] = []
    objects: dict[str, bytes] = {}
    evidence_root_value = prepared.get("evidenceRoot")
    evidence_root = (
        Path(evidence_root_value)
        if isinstance(evidence_root_value, str)
        else Path()
    )
    try:
        resolved_evidence_root = evidence_root.resolve(strict=True)
    except (OSError, RuntimeError):
        resolved_evidence_root = evidence_root.resolve()
        diagnostics.append("retained evidence root is missing")

    def capture(
        root: Path,
        reference: object,
        expected_parent: PurePosixPath | None,
        kind: str,
        label: str,
    ) -> tuple[Path | None, bytes | None]:
        entry: dict[str, Any] = {"kind": kind, "status": "invalid"}
        if not isinstance(reference, Mapping) or set(reference) != {"path", "sha256"}:
            entry["sourcePath"] = "unresolved"
            entries.append(entry)
            diagnostics.append(f"{label} reference must contain exactly path and sha256")
            return None, None
        relative = _safe_relative(reference.get("path"))
        declared = reference.get("sha256")
        entry["sourcePath"] = str(reference.get("path", "unresolved"))
        entry["declaredSha256"] = declared
        if relative is None or (
            expected_parent is not None and relative.parent != expected_parent
        ):
            entries.append(entry)
            diagnostics.append(f"{label} path is outside its retained evidence directory")
            return None, None
        if not isinstance(declared, str) or not _SHA256_PATTERN.fullmatch(declared):
            entries.append(entry)
            diagnostics.append(f"{label} digest is malformed")
            return None, None
        candidate = root.joinpath(*relative.parts)
        current = root
        for part in relative.parts:
            current = current / part
            if current.is_symlink():
                entries.append(entry)
                diagnostics.append(f"{label} contains a symbolic link")
                return None, None
        try:
            resolved_root = root.resolve(strict=True)
            resolved = candidate.resolve(strict=True)
        except (OSError, RuntimeError):
            entries.append(entry)
            diagnostics.append(f"{label} is missing")
            return None, None
        if resolved_root not in resolved.parents or not resolved.is_file():
            entries.append(entry)
            diagnostics.append(f"{label} is outside retained evidence")
            return None, None
        try:
            retained_path = resolved.relative_to(resolved_evidence_root).as_posix()
        except ValueError:
            entries.append(entry)
            diagnostics.append(f"{label} is outside the runner result evidenceRoot")
            return None, None
        content = resolved.read_bytes()
        actual = hashlib.sha256(content).hexdigest()
        entry["sourcePath"] = retained_path
        entry["sha256"] = actual
        entry["bundlePath"] = f"evidence/objects/{actual}"
        objects.setdefault(actual, content)
        if actual != declared:
            entries.append(entry)
            diagnostics.append(f"{label} digest mismatch")
            return resolved, content
        entry["status"] = "verified"
        entries.append(entry)
        return resolved, content

    for scenario in prepared.get("scenarioResults", []):
        if not isinstance(scenario, dict):
            diagnostics.append("scenario result is malformed")
            continue
        suite_id = str(prepared.get("suite", ""))
        scenario_id = str(scenario.get("scenario", ""))
        retained_run_identity = scenario.pop("_runIdentity", None)
        identity_reference = scenario.pop("_identityAudit", None)
        try:
            suite_manifest = yaml.safe_load(
                (_ROOT / suite_id / "suite.yaml").read_text(encoding="utf-8")
            )
        except (OSError, UnicodeError, yaml.YAMLError):
            suite_manifest = None
        expected_judge_invocation = (
            suite_manifest.get("execution", {}).get("judgeInvocation")
            if isinstance(suite_manifest, Mapping)
            and isinstance(suite_manifest.get("execution"), Mapping)
            else None
        )
        if not isinstance(expected_judge_invocation, str):
            diagnostics.append(f"{scenario_id}: governed Judge invocation is unavailable")
        checkpoint_value = scenario.pop("_checkpointRoot", None)
        checkpoint_root: Path | None = None
        if isinstance(checkpoint_value, str):
            candidate = Path(checkpoint_value)
            if not candidate.is_absolute():
                candidate = resolved_evidence_root / candidate
            try:
                resolved_checkpoint = candidate.resolve(strict=True)
            except (OSError, RuntimeError):
                diagnostics.append(f"{scenario_id}: retained checkpoint root is missing")
            else:
                if (
                    resolved_checkpoint.parent != resolved_evidence_root
                    or not resolved_checkpoint.is_dir()
                    or resolved_checkpoint.is_symlink()
                ):
                    diagnostics.append(
                        f"{scenario_id}: retained checkpoint root is outside evidenceRoot or ambiguous"
                    )
                else:
                    checkpoint_root = resolved_checkpoint
        else:
            diagnostics.append(f"{scenario_id}: retained checkpoint root is missing")
        references = scenario.get("evidenceReceipts")
        if not isinstance(references, list) or not references:
            diagnostics.append(f"{scenario_id}: retained evidence receipts are missing")
            references = []
        audit = scenario.get("receiptAudit")
        if not isinstance(audit, Mapping):
            diagnostics.append(f"{scenario_id}: runner receipt audit is missing")
            audit = {}
        if not isinstance(retained_run_identity, str) or audit.get(
            "runIdentity"
        ) != retained_run_identity:
            diagnostics.append(f"{scenario_id}: retained run identity mismatch")
        seen_receipts: set[str] = set()
        deterministic: list[dict[str, Any]] = []
        deterministic_receipts: dict[str, Mapping[str, Any]] = {}
        judge_dispositions: list[str] = []
        judge_invocations: list[str] = []
        judge_output: tuple[Path, bytes, str] | None = None
        skip_rows: list[Mapping[str, Any]] = []
        for index, reference in enumerate(references):
            path_value = reference.get("path") if isinstance(reference, Mapping) else None
            if isinstance(path_value, str) and path_value in seen_receipts:
                entries.append(
                    {
                        "kind": "receipt",
                        "status": "duplicate",
                        "sourcePath": path_value,
                        "declaredSha256": reference.get("sha256"),
                    }
                )
                diagnostics.append(f"{scenario_id}: duplicate receipt path {path_value}")
                continue
            if isinstance(path_value, str):
                seen_receipts.add(path_value)
            if checkpoint_root is None:
                entries.append(
                    {
                        "kind": "receipt",
                        "status": "missing-root",
                        "sourcePath": str(path_value or "unresolved"),
                        "declaredSha256": (
                            reference.get("sha256")
                            if isinstance(reference, Mapping)
                            else None
                        ),
                    }
                )
                continue
            receipt_path, receipt_bytes = capture(
                checkpoint_root,
                reference,
                PurePosixPath(suite_id, scenario_id, "receipts"),
                "receipt",
                f"{scenario_id} evidenceReceipts[{index}]",
            )
            if receipt_path is None or receipt_bytes is None:
                continue
            try:
                receipt = json.loads(receipt_bytes.decode("utf-8"))
            except (UnicodeError, json.JSONDecodeError):
                diagnostics.append(f"{scenario_id}: retained receipt is malformed JSON")
                continue
            if (
                not isinstance(receipt, dict)
                or receipt.get("schema") != _EVIDENCE_RECEIPT_SCHEMA
                or receipt.get("version") != 1
                or receipt.get("runIdentity") != audit.get("runIdentity")
                or receipt.get("suite") != suite_id
                or receipt.get("scenario") != scenario_id
            ):
                diagnostics.append(f"{scenario_id}: retained receipt identity mismatch")
                continue
            artifact_path, artifact_bytes = capture(
                checkpoint_root,
                receipt.get("evidence"),
                PurePosixPath(suite_id, scenario_id, "artifacts"),
                "artifact",
                f"{scenario_id} receipt evidence",
            )
            if artifact_path is None or artifact_bytes is None:
                continue
            event_type = receipt.get("eventType")
            if event_type == "deterministic-check-disposition":
                expected_fields = {
                    "schema", "version", "eventType", "runIdentity", "suite", "scenario",
                    "checkId", "critical", "verdict", "evidence",
                }
                if (
                    set(receipt) != expected_fields
                    or not isinstance(receipt.get("checkId"), str)
                    or type(receipt.get("critical")) is not bool
                    or receipt.get("verdict") not in {"passed", "failed"}
                ):
                    diagnostics.append(f"{scenario_id}: deterministic receipt is malformed")
                deterministic.append(
                    {
                        "checkId": receipt.get("checkId"),
                        "critical": receipt.get("critical"),
                        "verdict": receipt.get("verdict"),
                    }
                )
                check_id = receipt.get("checkId")
                if isinstance(check_id, str):
                    if check_id in deterministic_receipts:
                        diagnostics.append(
                            f"{scenario_id}: duplicate deterministic receipt {check_id}"
                        )
                    deterministic_receipts[check_id] = receipt
            elif event_type == "judge-disposition":
                expected_fields = {
                    "schema", "version", "eventType", "runIdentity", "suite", "scenario",
                    "judgeInvocation", "disposition", "evidence",
                }
                if set(receipt) != expected_fields:
                    diagnostics.append(f"{scenario_id}: Judge receipt is malformed")
                judge_dispositions.append(str(receipt.get("disposition")))
                judge_invocations.append(str(receipt.get("judgeInvocation")))
                judge_output = (
                    artifact_path,
                    artifact_bytes,
                    hashlib.sha256(artifact_bytes).hexdigest(),
                )
            elif event_type == "judge-skip-disposition":
                expected_fields = {
                    "schema", "version", "eventType", "runIdentity", "suite", "scenario",
                    "checkId", "critical", "deterministicVerdict", "disposition", "evidence",
                }
                if set(receipt) != expected_fields:
                    diagnostics.append(f"{scenario_id}: Judge-skip receipt is malformed")
                skip_rows.append(receipt)
            else:
                diagnostics.append(f"{scenario_id}: retained receipt event type is invalid")
        expected_deterministic = audit.get("deterministicChecks")
        if not isinstance(expected_deterministic, list) or sorted(
            deterministic, key=lambda value: str(value.get("checkId"))
        ) != sorted(
            [dict(value) for value in expected_deterministic if isinstance(value, Mapping)],
            key=lambda value: str(value.get("checkId")),
        ):
            diagnostics.append(f"{scenario_id}: deterministic receipt audit mismatch")
        judge_invoked = scenario.get("judgeInvoked")
        if judge_invoked is True:
            if judge_dispositions != [audit.get("judgeDisposition")]:
                diagnostics.append(f"{scenario_id}: Judge receipt audit mismatch")
            provenance = audit.get("judgeProvenance")
            if not isinstance(provenance, Mapping) or set(provenance) != _JUDGE_PROVENANCE_FIELDS:
                diagnostics.append(f"{scenario_id}: exact Judge child provenance is missing")
                provenance = {}
            expected_identity = {
                "status": "verified",
                "runIdentity": audit.get("runIdentity"),
                "suite": suite_id,
                "scenario": scenario_id,
                "disposition": audit.get("judgeDisposition"),
            }
            if any(provenance.get(key) != value for key, value in expected_identity.items()):
                diagnostics.append(f"{scenario_id}: Judge provenance identity mismatch")
            if (
                provenance.get("invocation") != expected_judge_invocation
                or judge_invocations != [expected_judge_invocation]
            ):
                diagnostics.append(f"{scenario_id}: selected Judge invocation mismatch")
            normalized_identity_reference: object = identity_reference
            if isinstance(identity_reference, Mapping) and isinstance(
                identity_reference.get("path"), str
            ):
                raw_identity_path = Path(str(identity_reference["path"]))
                if raw_identity_path.is_absolute():
                    try:
                        relative_identity_path = raw_identity_path.resolve(
                            strict=True
                        ).relative_to(resolved_evidence_root)
                    except (OSError, RuntimeError, ValueError):
                        relative_identity_path = None
                    normalized_identity_reference = {
                        "path": (
                            relative_identity_path.as_posix()
                            if relative_identity_path is not None
                            else str(identity_reference["path"])
                        ),
                        "sha256": identity_reference.get("sha256"),
                    }
            _, identity_bytes = capture(
                resolved_evidence_root,
                normalized_identity_reference,
                None,
                "identity-audit",
                f"{scenario_id} identity audit",
            )
            identity_document: object = None
            if identity_bytes is not None:
                try:
                    identity_document = json.loads(identity_bytes.decode("utf-8"))
                except (UnicodeError, json.JSONDecodeError):
                    diagnostics.append(f"{scenario_id}: retained identity audit is malformed")
            identity_bindings = (
                identity_document.get("scenarioBindings")
                if isinstance(identity_document, Mapping)
                else None
            )
            matching_identity_bindings = [
                value
                for value in identity_bindings
                if isinstance(value, Mapping)
                and value.get("suite") == suite_id
                and value.get("scenario") == scenario_id
                and value.get("kind") == "judge"
                and value.get("invocation") == provenance.get("invocation")
                and value.get("sessionId") == provenance.get("sessionId")
                and value.get("parentSessionId") == provenance.get("parentSessionId")
            ] if isinstance(identity_bindings, list) else []
            if len(matching_identity_bindings) != 1:
                diagnostics.append(
                    f"{scenario_id}: Judge session is not paired by retained identity/order evidence"
                )
            provenance_files: dict[str, tuple[Path | None, bytes | None]] = {}
            for kind, path_field, digest_field in (
                ("judge-rollout", "rolloutPath", "rolloutSha256"),
                ("judge-response", "responsePath", "responseSha256"),
                ("judge-output", "outputPath", "outputSha256"),
            ):
                provenance_files[kind] = capture(
                    resolved_evidence_root,
                    {"path": provenance.get(path_field), "sha256": provenance.get(digest_field)},
                    None,
                    kind,
                    f"{scenario_id} {kind}",
                )
            response_path, response_bytes = provenance_files["judge-response"]
            output_path, output_bytes = provenance_files["judge-output"]
            rollout_path, rollout_bytes = provenance_files["judge-rollout"]
            if response_bytes is None or output_bytes is None or response_bytes != output_bytes:
                diagnostics.append(f"{scenario_id}: Judge response and output bytes mismatch")
            if (
                judge_output is None
                or output_path is None
                or output_path != judge_output[0]
                or provenance.get("outputSha256") != judge_output[2]
            ):
                diagnostics.append(f"{scenario_id}: Judge receipt output and provenance mismatch")
            response_document: object = None
            if response_bytes is not None:
                try:
                    response_document = json.loads(response_bytes.decode("utf-8"))
                except (UnicodeError, json.JSONDecodeError):
                    diagnostics.append(f"{scenario_id}: Judge response is malformed")
            expected_response = {
                "schema": _JUDGE_OUTPUT_SCHEMA,
                "version": 1,
                "runIdentity": audit.get("runIdentity"),
                "suite": suite_id,
                "scenario": scenario_id,
                "judgeInvocation": provenance.get("invocation"),
                "disposition": audit.get("judgeDisposition"),
            }
            if response_document != expected_response:
                diagnostics.append(f"{scenario_id}: Judge response contract mismatch")
            if rollout_bytes is not None and response_bytes is not None:
                rollout_error = _judge_rollout_binding_error(
                    rollout_bytes, response_bytes, provenance
                )
                if rollout_error is not None:
                    diagnostics.append(f"{scenario_id}: {rollout_error}")
        elif judge_invoked is False:
            skip = skip_rows[0] if len(skip_rows) == 1 else {}
            matching_deterministic = deterministic_receipts.get(str(skip.get("checkId")))
            if (
                len(skip_rows) != 1
                or audit.get("judgeDisposition") != "skipped-critical-failure"
                or skip.get("critical") is not True
                or skip.get("deterministicVerdict") != "failed"
                or skip.get("disposition") != "skipped-critical-failure"
                or matching_deterministic is None
                or matching_deterministic.get("critical") is not True
                or matching_deterministic.get("verdict") != "failed"
                or skip.get("evidence") != matching_deterministic.get("evidence")
                or audit.get("failedCriticalCheck") != skip.get("checkId")
            ):
                diagnostics.append(f"{scenario_id}: exact critical Judge skip is missing")
        else:
            diagnostics.append(f"{scenario_id}: Judge invocation disposition is missing")

    bundle_status = "invalid" if diagnostics else "verified"
    for scenario in prepared.get("scenarioResults", []):
        if isinstance(scenario, dict) and bundle_status != "verified" and str(
            scenario.get("status", "")
        ).upper() in {"PASS", "FAIL"}:
            scenario["status"] = "INFRASTRUCTURE_FAILED"
            scenario.setdefault("evidence", []).append(
                "Governed evidence bundle validation failed before publication."
            )
    if bundle_status != "verified" and prepared.get("status") in {"PASS", "FAIL"}:
        prepared["status"] = "INFRASTRUCTURE_FAILED"
        prepared.setdefault("omissions", []).append(
            "evidence bundle incomplete: " + "; ".join(diagnostics)
        )
    manifest = {
        "schema": _EVIDENCE_BUNDLE_SCHEMA,
        "version": 1,
        "identity": prepared.get("identity"),
        "status": bundle_status,
        "entries": entries,
        "diagnostics": diagnostics,
    }
    manifest_content = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    prepared["evidenceBundle"] = {
        "schema": _EVIDENCE_BUNDLE_SCHEMA,
        "version": 1,
        "status": bundle_status,
        "manifest": "evidence/manifest.json",
        "manifestSha256": hashlib.sha256(manifest_content.encode("utf-8")).hexdigest(),
        "objectCount": len(objects),
        "diagnostics": diagnostics,
    }
    return prepared, objects, manifest


def _validate_evidence_bundle(generation_root: Path, metadata: Mapping[str, Any]) -> str:
    bundle = metadata.get("evidenceBundle")
    if not isinstance(bundle, Mapping) or bundle.get("schema") != _EVIDENCE_BUNDLE_SCHEMA:
        raise ValueError("suite report evidence bundle metadata is missing")
    manifest_relative = _safe_relative(bundle.get("manifest"))
    if manifest_relative != PurePosixPath("evidence/manifest.json"):
        raise ValueError("suite report evidence bundle manifest path is invalid")
    manifest_path = generation_root.joinpath(*manifest_relative.parts)
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise ValueError("suite report evidence bundle manifest is missing or unsafe")
    manifest_content = manifest_path.read_bytes()
    manifest_digest = hashlib.sha256(manifest_content).hexdigest()
    if manifest_digest != bundle.get("manifestSha256"):
        raise ValueError("suite report evidence bundle manifest digest mismatch")
    manifest = json.loads(manifest_content.decode("utf-8"))
    if (
        not isinstance(manifest, Mapping)
        or manifest.get("schema") != _EVIDENCE_BUNDLE_SCHEMA
        or manifest.get("version") != 1
        or manifest.get("identity") != metadata.get("identity")
        or manifest.get("status") != bundle.get("status")
        or not isinstance(manifest.get("entries"), list)
        or not isinstance(manifest.get("diagnostics"), list)
    ):
        raise ValueError("suite report evidence bundle manifest is malformed")
    manifest_entries = manifest["entries"]
    object_digests: set[str] = set()
    object_contents: dict[str, bytes] = {}
    for entry in manifest_entries:
        if not isinstance(entry, Mapping):
            raise ValueError("suite report evidence bundle entry is malformed")
        bundle_path = entry.get("bundlePath")
        digest = entry.get("sha256")
        if bundle_path is None:
            if entry.get("status") == "verified":
                raise ValueError("verified evidence bundle entry lacks an object")
            continue
        if (
            not isinstance(digest, str)
            or not _SHA256_PATTERN.fullmatch(digest)
            or bundle_path != f"evidence/objects/{digest}"
        ):
            raise ValueError("suite report evidence bundle object binding is malformed")
        object_path = generation_root / str(bundle_path)
        if object_path.is_symlink() or not object_path.is_file():
            raise ValueError("suite report evidence bundle object is missing or unsafe")
        content = object_path.read_bytes()
        if hashlib.sha256(content).hexdigest() != digest:
            raise ValueError("suite report evidence bundle object digest mismatch")
        object_digests.add(digest)
        object_contents[digest] = content
    if len(object_digests) != bundle.get("objectCount"):
        raise ValueError("suite report evidence bundle object count mismatch")
    if bundle.get("status") != "verified":
        if metadata.get("status") in {"PASS", "FAIL"}:
            raise ValueError("terminal suite verdict lacks a verified evidence bundle")
        return manifest_digest

    def bound_object(
        provenance: Mapping[str, Any],
        kind: str,
        path_field: str,
        digest_field: str,
    ) -> bytes:
        path_value = provenance.get(path_field)
        digest_value = provenance.get(digest_field)
        matches = [
            entry
            for entry in manifest_entries
            if isinstance(entry, Mapping)
            and entry.get("kind") == kind
            and entry.get("status") == "verified"
            and entry.get("sourcePath") == path_value
            and entry.get("sha256") == digest_value
            and entry.get("bundlePath") == f"evidence/objects/{digest_value}"
        ]
        if len(matches) != 1 or not isinstance(digest_value, str):
            raise ValueError(f"suite report {kind} provenance binding is invalid")
        content = object_contents.get(digest_value)
        if content is None:
            raise ValueError(f"suite report {kind} object is unavailable")
        return content

    scenario_results = metadata.get("scenarioResults")
    if not isinstance(scenario_results, list):
        raise ValueError("suite report scenarioResults must be a list")
    for scenario in scenario_results:
        if not isinstance(scenario, Mapping) or scenario.get("judgeInvoked") is not True:
            continue
        scenario_id = scenario.get("scenario")
        audit = scenario.get("receiptAudit")
        provenance = audit.get("judgeProvenance") if isinstance(audit, Mapping) else None
        if (
            not isinstance(audit, Mapping)
            or not isinstance(provenance, Mapping)
            or set(provenance) != _JUDGE_PROVENANCE_FIELDS
            or provenance.get("status") != "verified"
            or provenance.get("runIdentity") != audit.get("runIdentity")
            or provenance.get("suite") != metadata.get("suite")
            or provenance.get("scenario") != scenario_id
            or provenance.get("disposition") != audit.get("judgeDisposition")
        ):
            raise ValueError("suite report Judge provenance identity binding is invalid")
        rollout_bytes = bound_object(
            provenance, "judge-rollout", "rolloutPath", "rolloutSha256"
        )
        response_bytes = bound_object(
            provenance, "judge-response", "responsePath", "responseSha256"
        )
        output_bytes = bound_object(
            provenance, "judge-output", "outputPath", "outputSha256"
        )
        if response_bytes != output_bytes:
            raise ValueError("suite report Judge response and output bytes mismatch")
        try:
            response_document = json.loads(response_bytes.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as error:
            raise ValueError("suite report Judge response is malformed") from error
        expected_response = {
            "schema": _JUDGE_OUTPUT_SCHEMA,
            "version": 1,
            "runIdentity": audit.get("runIdentity"),
            "suite": metadata.get("suite"),
            "scenario": scenario_id,
            "judgeInvocation": provenance.get("invocation"),
            "disposition": audit.get("judgeDisposition"),
        }
        if response_document != expected_response:
            raise ValueError("suite report Judge response contract mismatch")
        rollout_error = _judge_rollout_binding_error(
            rollout_bytes, response_bytes, provenance
        )
        if rollout_error is not None:
            raise ValueError(f"suite report {rollout_error}")
        matching_identity_bindings = []
        seen_identity_objects: set[str] = set()
        for entry in manifest_entries:
            if (
                not isinstance(entry, Mapping)
                or entry.get("kind") != "identity-audit"
                or entry.get("status") != "verified"
                or not isinstance(entry.get("sha256"), str)
                or entry["sha256"] in seen_identity_objects
            ):
                continue
            seen_identity_objects.add(str(entry["sha256"]))
            identity_bytes = object_contents.get(str(entry["sha256"]))
            if identity_bytes is None:
                continue
            try:
                identity_document = json.loads(identity_bytes.decode("utf-8"))
            except (UnicodeError, json.JSONDecodeError):
                continue
            bindings = (
                identity_document.get("scenarioBindings")
                if isinstance(identity_document, Mapping)
                else None
            )
            if isinstance(bindings, list):
                matching_identity_bindings.extend(
                    binding
                    for binding in bindings
                    if isinstance(binding, Mapping)
                    and binding.get("suite") == metadata.get("suite")
                    and binding.get("scenario") == scenario_id
                    and binding.get("kind") == "judge"
                    and binding.get("invocation") == provenance.get("invocation")
                    and binding.get("sessionId") == provenance.get("sessionId")
                    and binding.get("parentSessionId")
                    == provenance.get("parentSessionId")
                )
        if len(matching_identity_bindings) != 1:
            raise ValueError(
                "suite report Judge session lacks unique identity/order binding"
            )
    return manifest_digest


def _validate_generation_content(
    generation_root: Path,
    metadata: Mapping[str, Any],
    metadata_content: str,
    html_content: str,
    manifest_content: str,
) -> None:
    if (generation_root / "metadata.json").read_text(encoding="utf-8") != metadata_content:
        raise ValueError("suite report staged metadata bytes mismatch")
    if (generation_root / "report.html").read_text(encoding="utf-8") != html_content:
        raise ValueError("suite report staged HTML bytes mismatch")
    if (
        generation_root / "evidence" / "manifest.json"
    ).read_text(encoding="utf-8") != manifest_content:
        raise ValueError("suite report staged evidence manifest bytes mismatch")
    if _embedded_metadata(metadata) not in html_content:
        raise ValueError("suite report staged HTML metadata binding mismatch")
    _validate_evidence_bundle(generation_root, metadata)


def write_suite_report(
    report_root: Path, metadata: Mapping[str, Any]
) -> tuple[Path, Path]:
    """Publish one immutable generation through a single atomic pointer replacement."""

    prepared, objects, manifest = _bundle_evidence(metadata)
    harness = str(prepared["harness"])
    suite_id = str(prepared["suite"])
    manifest_content = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    metadata_content = json.dumps(prepared, indent=2, sort_keys=True) + "\n"
    html_content = render_suite_html(prepared)
    generation = hashlib.sha256(
        metadata_content.encode("utf-8")
        + html_content.encode("utf-8")
        + manifest_content.encode("utf-8")
    ).hexdigest()
    generation_root = report_root / "generations" / harness / suite_id / generation
    metadata_path = generation_root / "metadata.json"
    html_path = generation_root / "report.html"
    pending_parent = report_root / "generations" / harness / suite_id
    pending_parent.mkdir(parents=True, exist_ok=True)
    pending_root = Path(tempfile.mkdtemp(prefix=".pending-", dir=pending_parent))
    try:
        _atomic_write(pending_root / "metadata.json", metadata_content)
        _atomic_write(pending_root / "report.html", html_content)
        _atomic_write(pending_root / "evidence" / "manifest.json", manifest_content)
        for digest, content in objects.items():
            object_path = pending_root / "evidence" / "objects" / digest
            _atomic_write_bytes(object_path, content)
        _validate_generation_content(
            pending_root,
            prepared,
            metadata_content,
            html_content,
            manifest_content,
        )
        if generation_root.exists():
            _validate_generation_content(
                generation_root,
                prepared,
                metadata_content,
                html_content,
                manifest_content,
            )
        else:
            os.replace(pending_root, generation_root)
        _validate_generation_content(
            generation_root,
            prepared,
            metadata_content,
            html_content,
            manifest_content,
        )
    finally:
        if pending_root.exists():
            shutil.rmtree(pending_root)
    pointer = {
        "schema": _POINTER_SCHEMA,
        "version": 2,
        "identity": f"{harness}:{suite_id}",
        "harness": harness,
        "suite": suite_id,
        "generation": generation,
        "metadata": metadata_path.relative_to(report_root).as_posix(),
        "metadataSha256": hashlib.sha256(metadata_content.encode("utf-8")).hexdigest(),
        "html": html_path.relative_to(report_root).as_posix(),
        "htmlSha256": hashlib.sha256(html_content.encode("utf-8")).hexdigest(),
        "evidenceManifest": (
            generation_root / "evidence" / "manifest.json"
        ).relative_to(report_root).as_posix(),
        "evidenceManifestSha256": prepared["evidenceBundle"]["manifestSha256"],
    }
    pointer_path = report_root / "suites" / harness / f"{suite_id}.manifest.json"
    _atomic_write(pointer_path, json.dumps(pointer, indent=2, sort_keys=True) + "\n")
    return html_path, metadata_path


def _metadata_candidates(report_root: Path) -> tuple[Path, ...]:
    return tuple(sorted(report_root.glob("suites/**/*.manifest.json")))


def _load_generation_pointer(
    report_root: Path, pointer_path: Path
) -> tuple[Mapping[str, Any], Path]:
    if pointer_path.is_symlink() or not pointer_path.is_file():
        raise ValueError("suite report pointer is missing or unsafe")
    pointer = json.loads(pointer_path.read_text(encoding="utf-8"))
    if (
        not isinstance(pointer, dict)
        or pointer.get("schema") != _POINTER_SCHEMA
        or pointer.get("version") != 2
        or pointer.get("harness") not in _HARNESSES
        or not isinstance(pointer.get("suite"), str)
        or not isinstance(pointer.get("generation"), str)
    ):
        raise ValueError("invalid suite report pointer")

    def governed_path(field: str) -> Path:
        relative_text = pointer.get(field)
        if not isinstance(relative_text, str):
            raise ValueError(f"suite report pointer lacks {field}")
        relative = Path(relative_text)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"suite report pointer {field} escapes the report root")
        resolved = (report_root / relative).resolve()
        if (
            not resolved.is_relative_to(report_root.resolve())
            or resolved.is_symlink()
            or not resolved.is_file()
        ):
            raise ValueError(f"suite report pointer {field} is missing or unsafe")
        return resolved

    metadata_path = governed_path("metadata")
    html_path = governed_path("html")
    evidence_manifest_path = governed_path("evidenceManifest")
    metadata_content = metadata_path.read_text(encoding="utf-8")
    html_content = html_path.read_text(encoding="utf-8")
    evidence_manifest_content = evidence_manifest_path.read_text(encoding="utf-8")
    if hashlib.sha256(metadata_content.encode("utf-8")).hexdigest() != pointer.get(
        "metadataSha256"
    ):
        raise ValueError("suite report metadata digest mismatch")
    if hashlib.sha256(html_content.encode("utf-8")).hexdigest() != pointer.get(
        "htmlSha256"
    ):
        raise ValueError("suite report HTML digest mismatch")
    if hashlib.sha256(evidence_manifest_content.encode("utf-8")).hexdigest() != pointer.get(
        "evidenceManifestSha256"
    ):
        raise ValueError("suite report evidence manifest digest mismatch")
    generation = hashlib.sha256(
        metadata_content.encode("utf-8")
        + html_content.encode("utf-8")
        + evidence_manifest_content.encode("utf-8")
    ).hexdigest()
    if generation != pointer.get("generation"):
        raise ValueError("suite report generation digest mismatch")
    if (
        metadata_path.parent != html_path.parent
        or metadata_path.parent != evidence_manifest_path.parents[1]
        or metadata_path.parent.name != generation
    ):
        raise ValueError(
            "suite report files do not share their governed generation directory"
        )
    metadata = json.loads(metadata_content)
    manifest_digest = _validate_evidence_bundle(metadata_path.parent, metadata)
    if (
        not isinstance(metadata, dict)
        or metadata.get("identity") != pointer.get("identity")
        or metadata.get("harness") != pointer.get("harness")
        or metadata.get("suite") != pointer.get("suite")
        or manifest_digest != pointer.get("evidenceManifestSha256")
        or _embedded_metadata(metadata) not in html_content
    ):
        raise ValueError("suite report generation identity mismatch")
    return metadata, html_path


def _valid_metadata(value: Mapping[str, Any]) -> bool:
    return (
        value.get("schema") == _SCHEMA
        and value.get("version") == 1
        and value.get("harness") in _HARNESSES
        and isinstance(value.get("suite"), str)
        and bool(value.get("suite"))
        and isinstance(value.get("sourceRevision"), str)
        and bool(value.get("sourceRevision"))
        and isinstance(value.get("suiteDigest"), str)
        and bool(value.get("suiteDigest"))
        and value.get("status") in _TERMINAL_STATUSES
        and isinstance(value.get("scenarioResults"), list)
        and isinstance(value.get("omissions"), list)
        and isinstance(value.get("evidenceBundle"), Mapping)
        and value.get("evidenceBundle", {}).get("schema") == _EVIDENCE_BUNDLE_SCHEMA
    )


def aggregate_entries(
    report_root: Path,
    catalog: Sequence[str],
    harness: str,
    current_revision: str,
) -> tuple[dict[str, Any], ...]:
    """Classify report metadata, keeping missing and every non-passing input state visible."""

    parsed: dict[tuple[str, str], list[tuple[Path, Mapping[str, Any], Path]]] = {}
    malformed: list[Path] = []
    for path in _metadata_candidates(report_root):
        try:
            value, html_path = _load_generation_pointer(report_root, path)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError):
            malformed.append(path)
            continue
        if not isinstance(value, dict) or not _valid_metadata(value):
            malformed.append(path)
            continue
        key = (str(value.get("harness", "")), str(value.get("suite", "")))
        parsed.setdefault(key, []).append((path, value, html_path))
    entries: list[dict[str, Any]] = []
    for suite_id in catalog:
        candidates = parsed.get((harness, suite_id), [])
        if not candidates:
            entries.append(
                {
                    "identity": f"{harness}:{suite_id}",
                    "harness": harness,
                    "suite": suite_id,
                    "inputState": "MISSING",
                    "status": "MISSING",
                }
            )
            continue
        path, value, html_path = candidates[0]
        state = "DUPLICATE" if len(candidates) > 1 else "CURRENT"
        if state == "CURRENT" and value.get("sourceRevision") != current_revision:
            state = "STALE"
        if state == "CURRENT" and value.get("suiteDigest") != _suite_digest(
            suite_id, harness
        ):
            state = "INCOMPATIBLE_REVISION"
        entry = dict(value)
        entry.update(
            {"inputState": state, "reportLink": os.path.relpath(html_path, report_root)}
        )
        entries.append(entry)
    for (candidate_harness, suite_id), candidates in sorted(parsed.items()):
        if candidate_harness != harness:
            path, value, html_path = candidates[0]
            entry = dict(value)
            entry.update(
                {
                    "inputState": "MIXED_HARNESS",
                    "reportLink": os.path.relpath(
                        html_path,
                        report_root,
                    ),
                }
            )
            entries.append(entry)
        elif suite_id not in catalog:
            path, value, html_path = candidates[0]
            entry = dict(value)
            entry.update(
                {
                    "inputState": "INCOMPATIBLE_REVISION",
                    "reportLink": os.path.relpath(
                        html_path,
                        report_root,
                    ),
                }
            )
            entries.append(entry)
    entries.extend(
        {
            "identity": f"malformed:{path.name}",
            "harness": "unknown",
            "suite": path.name,
            "inputState": "MALFORMED",
            "status": "MALFORMED",
        }
        for path in malformed
    )
    if any(entry["inputState"] not in _VISIBLE_INPUT_STATES for entry in entries):
        raise RuntimeError("unrecognized aggregate input state")
    return tuple(entries)


def render_global_html(
    entries: Sequence[Mapping[str, Any]], harness: str, revision: str
) -> str:
    """Render the deterministic offline catalog report from normalized suite metadata."""

    ordered = sorted(
        entries,
        key=lambda value: (
            str(value.get("harness")),
            str(value.get("suite")),
            str(value.get("identity")),
        ),
    )
    input_state_counts: dict[str, int] = {}
    terminal_status_counts = {status: 0 for status in sorted(_TERMINAL_STATUSES)}
    rows = []
    for entry in ordered:
        state = str(entry.get("inputState", "MALFORMED"))
        input_state_counts[state] = input_state_counts.get(state, 0) + 1
        status = str(entry.get("status", ""))
        if state == "CURRENT" and status in terminal_status_counts:
            terminal_status_counts[status] += 1
        label = html.escape(str(entry.get("suite", "unknown")))
        link = entry.get("reportLink")
        suite_cell = (
            f'<a href="{html.escape(str(link))}">{label}</a>' if link else label
        )
        rows.append(
            f'<tr><th scope="row">{suite_cell}</th><td>{html.escape(str(entry.get("harness", "unknown")))}</td><td>{html.escape(str(entry.get("status", "unknown")))}</td><td>{html.escape(state)}</td><td>{html.escape(str(entry.get("finishedAtUtc", "—")))}</td></tr>'
        )
    aggregate = {
        "schema": "dev-methodology-agent-suite-global-report",
        "version": 1,
        "harness": harness,
        "sourceRevision": revision,
        "counts": input_state_counts,
        "inputStateCounts": input_state_counts,
        "terminalStatusCounts": terminal_status_counts,
        "entries": ordered,
    }
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Agent suite reports</title><style>body{{font:16px system-ui,sans-serif;line-height:1.5;margin:auto;max-width:80rem;padding:1rem;color:#18212b;background:#fff}}a{{color:#0645ad}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #667;padding:.5rem;text-align:left}}@media(max-width:40rem){{table{{display:block;overflow-x:auto}}}}</style></head><body><main><h1>Agent suite reports</h1><p>Harness: {html.escape(harness)} · Revision: {html.escape(revision)}</p><h2>Input states</h2><p>{html.escape(json.dumps(input_state_counts, sort_keys=True))}</p><h2>Terminal statuses</h2><p>{html.escape(json.dumps(terminal_status_counts, sort_keys=True))}</p><h2>Suites</h2><table><thead><tr><th scope="col">Suite</th><th scope="col">Harness</th><th scope="col">Status</th><th scope="col">Input state</th><th scope="col">Finished</th></tr></thead><tbody>{"".join(rows)}</tbody></table></main>{_embedded_metadata(aggregate)}</body></html>\n"""


def rebuild_global(
    report_root: Path, catalog: Sequence[str], harness: str, revision: str
) -> Path:
    """Atomically rebuild the global report solely from durable suite report metadata."""

    entries = aggregate_entries(report_root, catalog, harness, revision)
    path = report_root / "index.html"
    _atomic_write(path, render_global_html(entries, harness, revision))
    return path


def run_suites(
    harness: str,
    requested: Sequence[str],
    report_root: Path,
    *,
    maximum_workers: int | None = None,
    timeout_seconds: int = 3600,
    allow_full_junie: bool = False,
    executor: SuiteExecutor = _default_executor,
    resources: HostResources | None = None,
    safety_probe: SafetyProbe | None = None,
) -> tuple[dict[str, Any], ...]:
    """Run selected suites in disjoint destinations while preserving every completed report."""

    if harness not in _HARNESSES:
        raise ValueError("harness must be codex or junie")
    catalog = catalog_suite_ids()
    selected = select_suites(catalog, requested)
    if harness == "junie" and selected == catalog and not allow_full_junie:
        raise ValueError("a full Junie selection requires --allow-full-junie")
    measured = resources or discover_resources()
    workers = resolve_workers(len(selected), measured, maximum_workers)
    active_safety_probe = safety_probe
    if active_safety_probe is None and resources is None:

        def resource_boundary_is_safe(current: HostResources) -> bool:
            try:
                return resolve_workers(len(selected), current) >= workers
            except ValueError:
                return False

        active_safety_probe = resource_boundary_is_safe
    revision = _source_revision()
    run_id = f"{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    stop = threading.Event()

    def execute(suite_id: str) -> dict[str, Any]:
        if stop.is_set():
            return {"suite": suite_id, "status": "NOT_SCHEDULED"}
        if active_safety_probe is not None:
            try:
                safe_to_continue = active_safety_probe(discover_resources())
            except Exception:
                safe_to_continue = False
            if not safe_to_continue:
                stop.set()
                return {"suite": suite_id, "status": "NOT_SCHEDULED"}
        result_dir = report_root / "runs" / harness / suite_id / run_id
        started = _utc_now()
        monotonic = time.monotonic()
        try:
            execution = executor(harness, suite_id, result_dir, timeout_seconds)
        except Exception as error:
            execution = SuiteExecution(
                1, None, stderr=f"suite executor failed: {error}"
            )
        metadata = suite_metadata(
            harness,
            suite_id,
            execution,
            source_revision=revision,
            suite_digest=_suite_digest(suite_id, harness),
            started_at=started,
            finished_at=_utc_now(),
            elapsed_seconds=time.monotonic() - monotonic,
            evidence_root=result_dir,
        )
        _, metadata_path = write_suite_report(report_root, metadata)
        return json.loads(metadata_path.read_text(encoding="utf-8"))

    results: list[dict[str, Any]] = []
    iterator = iter(selected)
    futures: dict[concurrent.futures.Future[dict[str, Any]], str] = {}
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=workers, thread_name_prefix="agent-suite"
    ) as pool:
        for _ in range(workers):
            try:
                suite_id = next(iterator)
            except StopIteration:
                break
            futures[pool.submit(execute, suite_id)] = suite_id
        while futures:
            done, _ = concurrent.futures.wait(
                futures, return_when=concurrent.futures.FIRST_COMPLETED
            )
            for future in done:
                suite_id = futures.pop(future)
                try:
                    results.append(future.result())
                except Exception as error:
                    results.append(
                        {
                            "suite": suite_id,
                            "status": "INFRASTRUCTURE_FAILED",
                            "error": str(error),
                        }
                    )
                if not stop.is_set():
                    try:
                        next_suite = next(iterator)
                    except StopIteration:
                        continue
                    futures[pool.submit(execute, next_suite)] = next_suite
    rebuild_global(report_root, catalog, harness, revision)
    order = {suite_id: index for index, suite_id in enumerate(catalog)}
    return tuple(sorted(results, key=lambda value: order[str(value["suite"])]))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run and aggregate bounded parallel agent-suite reports."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    run = subparsers.add_parser(
        "run", help="Run one, several, or all suites and update reports."
    )
    run.add_argument("--harness", required=True, choices=sorted(_HARNESSES))
    run.add_argument("--suite", action="append", default=[])
    run.add_argument("--max-workers", type=int)
    run.add_argument("--timeout-seconds", type=int, default=3600)
    run.add_argument("--allow-full-junie", action="store_true")
    run.add_argument("--report-dir", type=Path, default=_ROOT / "run-reports")
    for name in ("rebuild", "update"):
        command = subparsers.add_parser(
            name, help=f"{name.title()} the global report without running suites."
        )
        command.add_argument("--harness", required=True, choices=sorted(_HARNESSES))
        command.add_argument("--report-dir", type=Path, default=_ROOT / "run-reports")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Execute the command-line run, report-only rebuild, or incremental update workflow."""

    arguments = _parser().parse_args(argv)
    if arguments.command == "run":
        results = run_suites(
            arguments.harness,
            tuple(arguments.suite),
            arguments.report_dir.resolve(),
            maximum_workers=arguments.max_workers,
            timeout_seconds=arguments.timeout_seconds,
            allow_full_junie=arguments.allow_full_junie,
        )
        return 0 if all(value.get("status") == "PASS" for value in results) else 1
    path = rebuild_global(
        arguments.report_dir.resolve(),
        catalog_suite_ids(),
        arguments.harness,
        _source_revision(),
    )
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
