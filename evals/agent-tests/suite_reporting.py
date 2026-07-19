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
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
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
        for run in report.get("runs", []) if isinstance(report, dict) else []:
            for scenario in (
                run.get("scenarioResults", []) if isinstance(run, dict) else []
            ):
                if isinstance(scenario, dict):
                    rows.append(dict(scenario))
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
    status = _terminal_status(execution, scenarios)
    omissions: list[str] = []
    if execution.summary is None:
        omissions.append("runner summary unavailable or malformed")
    if not scenarios:
        omissions.append("no governed scenario results were retained")
    missing_deterministic = [
        str(scenario.get("scenario", "unknown"))
        for scenario in scenarios
        if not isinstance(scenario.get("deterministicEvidence"), list)
    ]
    missing_judge = [
        str(scenario.get("scenario", "unknown"))
        for scenario in scenarios
        if not isinstance(scenario.get("modelJudgeEvidence"), list)
    ]
    if missing_deterministic:
        omissions.append(
            "explicit deterministic evidence unavailable for "
            + ", ".join(missing_deterministic)
        )
    if missing_judge:
        omissions.append(
            "explicit model-Judge evidence unavailable for " + ", ".join(missing_judge)
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
<h2>Scenario results</h2><table><thead><tr><th scope="col">Scenario</th><th scope="col">Status</th><th scope="col">Evidence</th><th scope="col">Deterministic evidence</th><th scope="col">Model-Judge evidence</th></tr></thead><tbody>{"".join(rows) or '<tr><td colspan="5">No scenario results retained.</td></tr>'}</tbody></table>
<h2>Omissions</h2><ul>{omissions}</ul><h2>Retained evidence</h2><p>{html.escape(str(metadata["evidenceRoot"]))}</p></main>{_embedded_metadata(metadata)}</body></html>\n"""


def write_suite_report(
    report_root: Path, metadata: Mapping[str, Any]
) -> tuple[Path, Path]:
    """Publish one immutable generation through a single atomic pointer replacement."""

    harness = str(metadata["harness"])
    suite_id = str(metadata["suite"])
    metadata_content = json.dumps(metadata, indent=2, sort_keys=True) + "\n"
    html_content = render_suite_html(metadata)
    generation = hashlib.sha256(
        metadata_content.encode("utf-8") + html_content.encode("utf-8")
    ).hexdigest()
    generation_root = report_root / "generations" / harness / suite_id / generation
    metadata_path = generation_root / "metadata.json"
    html_path = generation_root / "report.html"
    _atomic_write(metadata_path, metadata_content)
    _atomic_write(html_path, html_content)
    pointer = {
        "schema": _POINTER_SCHEMA,
        "version": 1,
        "identity": f"{harness}:{suite_id}",
        "harness": harness,
        "suite": suite_id,
        "generation": generation,
        "metadata": metadata_path.relative_to(report_root).as_posix(),
        "metadataSha256": hashlib.sha256(metadata_content.encode("utf-8")).hexdigest(),
        "html": html_path.relative_to(report_root).as_posix(),
        "htmlSha256": hashlib.sha256(html_content.encode("utf-8")).hexdigest(),
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
        or pointer.get("version") != 1
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
    metadata_content = metadata_path.read_text(encoding="utf-8")
    html_content = html_path.read_text(encoding="utf-8")
    if hashlib.sha256(metadata_content.encode("utf-8")).hexdigest() != pointer.get(
        "metadataSha256"
    ):
        raise ValueError("suite report metadata digest mismatch")
    if hashlib.sha256(html_content.encode("utf-8")).hexdigest() != pointer.get(
        "htmlSha256"
    ):
        raise ValueError("suite report HTML digest mismatch")
    generation = hashlib.sha256(
        metadata_content.encode("utf-8") + html_content.encode("utf-8")
    ).hexdigest()
    if generation != pointer.get("generation"):
        raise ValueError("suite report generation digest mismatch")
    if (
        metadata_path.parent != html_path.parent
        or metadata_path.parent.name != generation
    ):
        raise ValueError(
            "suite report files do not share their governed generation directory"
        )
    metadata = json.loads(metadata_content)
    if (
        not isinstance(metadata, dict)
        or metadata.get("identity") != pointer.get("identity")
        or metadata.get("harness") != pointer.get("harness")
        or metadata.get("suite") != pointer.get("suite")
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
        write_suite_report(report_root, metadata)
        return metadata

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
