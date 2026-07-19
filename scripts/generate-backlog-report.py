#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Generates a deterministic, self-contained HTML view of a repository backlog.
# Governing backlog item: backlog/feature-backlog/add-styled-backlog-report-with-user-input.md

"""Generate an offline HTML report from the repository backlog."""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence


ACTIVE_FOLDERS = {
    "defect-backlog": "Defect",
    "feature-backlog": "Feature",
    "analysis-backlog": "Analysis",
    "investigation-backlog": "Investigation",
}
SCAN_FOLDERS = (
    *ACTIVE_FOLDERS,
    "user-action-required",
    "holding",
    "completed-backlog",
    "failed-backlog",
)
REQUIRED_SECTIONS = (
    "Summary",
    "Requirements",
    "Acceptance Criteria",
    "Dependencies",
    "Verification",
)
USER_SECTIONS = (
    "Question for the User",
    "Why User Input Is Required",
    "Resolution",
    "Unattended Work Boundary",
)
ALLOWED_TYPES = {"Defect", "Feature", "Analysis", "Investigation", "Holding"}
DISPATCHABLE_TYPES = {"Defect", "Feature", "Analysis", "Investigation"}
ALLOWED_STATUSES = {
    "Ready",
    "Claimed",
    "Running",
    "Blocked",
    "User Action Required",
    "Target Merge Pending",
    "Completed",
    "Failed",
    "Abandoned",
    "Holding",
}
DEPENDENCY_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^]]+\]\(([^)#?]+\.md)(?:#[^)]*)?\)")
INLINE_MARKDOWN_PATTERN = re.compile(r"(`[^`]*`|\*\*([^*]+)\*\*|\*([^*]+)\*|\[([^]]+)\]\([^)]+\))")


@dataclass
class _Item:
    path: str
    slug: str
    title: str
    queue: str
    declared_type: str
    status: str
    summary: str
    dependencies: list[str]
    series: str = ""
    series_order: int = 10**9
    priority: int = 10**9
    question: str = ""
    resolution: str = ""
    missing: list[str] = field(default_factory=list)
    anomalies: list[str] = field(default_factory=list)
    unmet_dependencies: list[str] = field(default_factory=list)
    satisfied_dependencies: list[str] = field(default_factory=list)
    eligible: bool = False


@dataclass(frozen=True)
class _Snapshot:
    source_commit: str
    generated_at: str
    claim_captured_at: str
    claims: tuple[dict[str, object], ...]
    claim_status: str


def _plain_text(markdown: str) -> str:
    """Return compact readable text for the small Markdown subset used by backlog fields."""
    text = " ".join(line.strip().lstrip("-* ") for line in markdown.splitlines() if line.strip())
    return INLINE_MARKDOWN_PATTERN.sub(lambda match: next((group for group in match.groups()[1:] if group), match.group(0).strip("`")), text)


def _parse_document(path: Path) -> tuple[str, dict[str, str], dict[str, str]]:
    """Parse a backlog Markdown file into its title, scalar fields, and level-two sections."""
    content = path.read_text(encoding="utf-8")
    title = ""
    fields: dict[str, str] = {}
    sections: dict[str, list[str]] = {}
    current_section = ""
    for line in content.splitlines():
        if line.startswith("# ") and not title:
            title = line[2:].strip()
            continue
        if line.startswith("## "):
            current_section = line[3:].strip()
            sections.setdefault(current_section, [])
            continue
        if current_section:
            sections[current_section].append(line)
            continue
        match = re.match(r"^([A-Za-z][A-Za-z ]+):\s*(.*?)\s*$", line)
        if match:
            fields[match.group(1)] = match.group(2)
    return title, fields, {name: "\n".join(lines).strip() for name, lines in sections.items()}


def _dependencies(section: str) -> list[str]:
    """Extract dependency slugs while preserving their declared order."""
    if not section or section.strip().lower() == "none":
        return []
    values: list[str] = []
    for line in section.splitlines():
        candidate = line.strip().lstrip("-* ").strip()
        if not candidate or candidate.lower() == "none":
            continue
        link_match = MARKDOWN_LINK_PATTERN.search(candidate)
        if link_match:
            candidate = Path(link_match.group(1)).stem
        else:
            candidate = candidate.split()[0].strip("`.,;:()[]")
        if candidate.lower() == "none":
            continue
        values.append(candidate)
    return values


def _series_orders(
    backlog_root: Path,
) -> tuple[dict[str, tuple[str, int]], list[str], list[tuple[str, str]]]:
    """Map readable series indexes to order and report ignored or invalid indexes."""
    orders: dict[str, tuple[str, int]] = {}
    ignored: list[str] = []
    findings: list[tuple[str, str]] = []
    for index in sorted(backlog_root.rglob("index.md")):
        relative_index = index.relative_to(backlog_root.parent).as_posix()
        ignored.append(relative_index)
        try:
            content = index.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            findings.append(
                (relative_index, f"Unreadable series index: {type(exc).__name__}: {exc}")
            )
            continue
        series = index.parent.name
        for position, target in enumerate(MARKDOWN_LINK_PATTERN.findall(content), start=1):
            child = (index.parent / target).resolve()
            try:
                relative_child = child.relative_to(backlog_root.parent.resolve()).as_posix()
            except ValueError:
                continue
            orders.setdefault(relative_child, (series, position))
    return orders, ignored, findings


def _queue_for(relative: Path) -> str:
    """Classify an item from its location without using the location as its work type."""
    parts = relative.parts
    top = parts[1] if len(parts) > 1 else ""
    if top in ACTIVE_FOLDERS:
        return "active"
    if top == "user-action-required":
        return "user-action-required"
    if top == "holding":
        return "holding"
    if top == "completed-backlog":
        return "completed"
    if top == "failed-backlog":
        return "failed"
    return "invalid"


def _expected_type(relative: Path, queue: str) -> str:
    """Return the type implied by a typed active or archive folder, when one exists."""
    parts = relative.parts
    if queue == "active":
        return ACTIVE_FOLDERS.get(parts[1], "")
    if queue in {"completed", "failed"} and len(parts) > 2:
        return {
            "defects": "Defect",
            "features": "Feature",
            "analyses": "Analysis",
            "investigations": "Investigation",
        }.get(parts[2], "")
    return ""


def _read_items(
    repository_root: Path,
) -> tuple[list[_Item], list[str], list[str], list[tuple[str, str]]]:
    """Read all configured backlog queues and report scanned and ignored paths."""
    backlog_root = repository_root / "backlog"
    if not backlog_root.is_dir():
        raise ValueError(f"Backlog directory does not exist: {backlog_root}")
    series_orders, ignored, scope_findings = _series_orders(backlog_root)
    queue_readme = backlog_root / "user-action-required" / "README.md"
    if queue_readme.is_file():
        ignored.append(queue_readme.relative_to(repository_root).as_posix())
    scanned: list[str] = []
    items: list[_Item] = []
    for folder_name in SCAN_FOLDERS:
        folder = backlog_root / folder_name
        if not folder.is_dir():
            continue
        scanned.append(folder.relative_to(repository_root).as_posix())
        for path in sorted(folder.rglob("*.md")):
            relative = path.relative_to(repository_root)
            relative_text = relative.as_posix()
            if path.name in {"README.md", "index.md"}:
                if relative_text not in ignored:
                    ignored.append(relative_text)
                continue
            queue = _queue_for(relative)
            try:
                title, fields, sections = _parse_document(path)
            except (OSError, UnicodeError) as exc:
                item = _Item(relative_text, path.stem, path.stem, queue, "", "", "", [])
                item.anomalies.append(f"Unreadable item: {type(exc).__name__}: {exc}")
                items.append(item)
                continue
            missing = [name for name in ("Status", "Type") if not fields.get(name)]
            missing.extend(name for name in REQUIRED_SECTIONS if not sections.get(name))
            if not title:
                missing.append("Title")
            fallback_series = path.parent.name if queue == "active" and path.parent != folder else ""
            series, series_order = series_orders.get(relative_text, (fallback_series, 10**9))
            priority_text = fields.get("Priority", "")
            priority = int(priority_text) if priority_text.isdigit() else 10**9
            item = _Item(
                path=relative_text,
                slug=path.stem,
                title=title or path.stem,
                queue=queue,
                declared_type=fields.get("Type", ""),
                status=fields.get("Status", ""),
                summary=_plain_text(sections.get("Summary", "")),
                dependencies=_dependencies(sections.get("Dependencies", "")),
                series=series,
                series_order=series_order,
                priority=priority,
                question=_plain_text(sections.get("Question for the User", "")),
                resolution=_plain_text(sections.get("Resolution", "")),
                missing=missing,
            )
            expected_type = _expected_type(relative, queue)
            if item.declared_type and item.declared_type not in ALLOWED_TYPES:
                item.anomalies.append(f"Invalid Type value: {item.declared_type}.")
            if item.status and item.status not in ALLOWED_STATUSES and item.status != "Proposed":
                item.anomalies.append(f"Invalid Status value: {item.status}.")
            if queue in {"completed", "failed"} and not expected_type:
                item.anomalies.append(
                    "Archive placement is not a recognized typed archive folder."
                )
            if expected_type and item.declared_type and expected_type != item.declared_type:
                item.anomalies.append(
                    f"Folder and Type mismatch: {relative.parts[1] if queue == 'active' else relative.parts[2]} expects {expected_type}, item declares {item.declared_type}."
                )
            if item.status == "Proposed":
                item.anomalies.append("Migration anomaly: Status Proposed is not an operational state.")
            if item.missing:
                item.anomalies.append("Missing required fields: " + ", ".join(item.missing) + ".")
            if queue == "user-action-required":
                absent = [name for name in USER_SECTIONS if not sections.get(name)]
                if item.status != "User Action Required":
                    item.anomalies.append("User Action Required queue item has a non-canonical status.")
                if item.declared_type and item.declared_type not in DISPATCHABLE_TYPES:
                    item.anomalies.append(
                        "User Action Required item has no dispatchable underlying Type: "
                        f"{item.declared_type}."
                    )
                if absent:
                    item.anomalies.append("Missing user-action fields: " + ", ".join(absent) + ".")
            if queue == "holding" and item.status != "Holding":
                item.anomalies.append("Holding item has a non-Holding declared status.")
            if queue == "active" and item.status == "Completed":
                item.anomalies.append("Completed item remains in an active folder.")
            if queue == "completed" and item.status != "Completed":
                item.anomalies.append("Completed archive contains an item not declared Completed.")
            if queue == "failed" and item.status not in {"Failed", "Abandoned"}:
                item.anomalies.append("Failed archive contains an item without Failed or Abandoned status.")
            items.append(item)
    return items, scanned, sorted(set(ignored)), scope_findings


def _reconcile(items: list[_Item]) -> None:
    """Resolve dependency evidence and effective dispatch eligibility in place."""
    completed = {item.slug for item in items if item.queue == "completed"}
    known = {item.slug for item in items}
    for item in items:
        for dependency in item.dependencies:
            if not DEPENDENCY_PATTERN.fullmatch(dependency):
                item.unmet_dependencies.append(dependency)
                item.anomalies.append(f"Invalid dependency identifier: {dependency}.")
            elif dependency not in known:
                item.unmet_dependencies.append(dependency)
                item.anomalies.append(f"Unresolved dependency: {dependency}.")
            elif dependency in completed:
                item.satisfied_dependencies.append(dependency)
            else:
                item.unmet_dependencies.append(dependency)
                item.anomalies.append(
                    f"Unmet dependency: {dependency} is not in the completed archive."
                )
        if item.queue == "active" and item.status == "Blocked" and not item.unmet_dependencies:
            item.anomalies.append("Stale blocked status: all declared dependencies are satisfied.")
        if item.queue == "active" and item.status == "Ready" and item.unmet_dependencies:
            item.anomalies.append("Ready status has unmet dependencies and is not effectively eligible.")
        item.eligible = (
            item.queue == "active"
            and item.status == "Ready"
            and item.declared_type in DISPATCHABLE_TYPES
            and not item.unmet_dependencies
            and not item.missing
            and item.status != "Proposed"
        )


def _source_commit(repository_root: Path) -> str:
    """Read the source Git commit, returning a visible marker outside a Git checkout."""
    result = subprocess.run(
        ["git", "-C", str(repository_root), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else "unavailable"


def _claim_snapshot(
    repository_root: Path, generated_at: str
) -> tuple[str, tuple[dict[str, object], ...], str]:
    """Read repository-global claim state without interpreting it as backlog lifecycle."""
    result = subprocess.run(
        ["git", "-C", str(repository_root), "rev-parse", "--git-common-dir"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return generated_at, (), "unavailable: repository is not a Git checkout"
    common = Path(result.stdout.strip())
    if not common.is_absolute():
        common = repository_root / common
    registry = common.resolve() / "agent-claims.json"
    try:
        registry_text = registry.read_text(encoding="utf-8")
    except FileNotFoundError:
        return generated_at, (), "unavailable: claim registry is missing"
    except (OSError, UnicodeError) as exc:
        return generated_at, (), f"unavailable: claim registry is unreadable ({type(exc).__name__})"
    try:
        payload = json.loads(registry_text)
    except ValueError:
        return generated_at, (), "unavailable: claim registry contains invalid JSON"
    if isinstance(payload, dict):
        if "claims" not in payload:
            return generated_at, (), "unavailable: claim registry is missing its claims field"
        raw_claims = payload.get("claims", [])
    elif isinstance(payload, list):
        raw_claims = payload
    else:
        return generated_at, (), "unavailable: claim registry has an invalid root value"
    if not isinstance(raw_claims, list):
        return generated_at, (), "unavailable: claim registry has an invalid claims field"
    if any(not isinstance(entry, dict) for entry in raw_claims):
        return generated_at, (), "unavailable: claim registry contains an invalid claim entry"
    claims = tuple(sorted((entry for entry in raw_claims if isinstance(entry, dict)), key=lambda value: str(value.get("claim_id", ""))))
    return generated_at, claims, "available"


def _escape(value: object) -> str:
    """Escape a value for safe HTML text and attribute placement."""
    return html.escape(str(value), quote=True)


def _badge(text: str, style: str = "neutral") -> str:
    """Render a text-labelled badge so status never depends on color alone."""
    return f'<span class="badge badge-{_escape(style)}">{_escape(text or "Missing")}</span>'


def _item_card(item: _Item) -> str:
    """Render a traceable backlog item card with lifecycle and dependency evidence."""
    metadata = [_badge(item.declared_type, "type"), _badge(item.status, "status")]
    if item.series:
        metadata.append(_badge(f"Series: {item.series}", "neutral"))
    if item.series_order < 10**9:
        metadata.append(_badge(f"Recommended order: {item.series_order}", "neutral"))
    dependency_text = "None"
    if item.dependencies:
        parts = [f"{value} (satisfied)" for value in item.satisfied_dependencies]
        parts.extend(f"{value} (unmet)" for value in item.unmet_dependencies)
        dependency_text = ", ".join(parts)
    detail = ""
    if item.queue == "user-action-required":
        detail = (
            f'<dl class="interaction"><dt>Question for the User</dt><dd>{_escape(item.question or "Missing")}</dd>'
            f'<dt>Resolution</dt><dd>{_escape(item.resolution or "Missing")}</dd></dl>'
        )
    return (
        '<article class="item">'
        f'<div class="badges">{"".join(metadata)}</div>'
        f'<h3>{_escape(item.title)}</h3>'
        f'<p>{_escape(item.summary or "No summary provided.")}</p>'
        f'<p class="detail"><strong>Dependencies:</strong> {_escape(dependency_text)}</p>'
        f'{detail}<p class="source"><strong>Source:</strong> <code>{_escape(item.path)}</code></p>'
        '</article>'
    )


def _section(title: str, description: str, items: Iterable[_Item], empty: str) -> str:
    """Render a named report section and a stable empty state."""
    rendered = "".join(_item_card(item) for item in items)
    body = f'<div class="item-grid">{rendered}</div>' if rendered else f'<p class="empty">{_escape(empty)}</p>'
    return f'<section class="section"><div class="section-head"><div><h2>{_escape(title)}</h2><p>{_escape(description)}</p></div></div>{body}</section>'


def _sort_key(item: _Item) -> tuple[int, str, int, int, str]:
    """Order by queue, series, series order, priority, and stable path."""
    queue_order = {"user-action-required": 0, "active": 1, "holding": 2, "completed": 3, "failed": 4, "invalid": 5}
    return (queue_order[item.queue], item.series, item.series_order, item.priority, item.path)


def _render_report(
    items: list[_Item],
    scanned: list[str],
    ignored: list[str],
    scope_findings: list[tuple[str, str]],
    snapshot: _Snapshot,
) -> str:
    """Render the complete accessible report as one offline HTML document."""
    ordered = sorted(items, key=_sort_key)
    active = [item for item in ordered if item.queue == "active"]
    needs_input = [item for item in ordered if item.queue == "user-action-required"]
    runnable = [item for item in active if item.eligible]
    blocked = [item for item in active if item.unmet_dependencies or item.status == "Blocked"]
    holding = [item for item in ordered if item.queue == "holding"]
    completed = [item for item in ordered if item.queue == "completed"]
    failed = [item for item in ordered if item.queue == "failed"]
    type_counts = Counter(item.declared_type or "Missing" for item in ordered)
    status_counts = Counter(item.status or "Missing" for item in ordered)
    anomalies = [(item, anomaly) for item in ordered for anomaly in item.anomalies]
    metrics = (
        ("Active typed items", len(active)),
        ("Runnable now", len(runnable)),
        ("Needs your input", len(needs_input)),
        ("Holding", len(holding)),
        ("Completed archive", len(completed)),
        ("Failed archive", len(failed)),
        ("Validation findings", len(anomalies) + len(scope_findings)),
    )
    metrics_html = "".join(f'<div class="metric"><span>{_escape(label)}</span><strong>{value}</strong></div>' for label, value in metrics)
    count_rows = "".join(
        f'<tr><th scope="row">{_escape(label)}</th><td>{count}</td></tr>'
        for label, count in sorted(type_counts.items())
    )
    status_rows = "".join(
        f'<tr><th scope="row">{_escape(label)}</th><td>{count}</td></tr>'
        for label, count in sorted(status_counts.items())
    )
    anomaly_rows = "".join(
        f'<li><strong>{_escape(item.title)}</strong>: {_escape(message)} <code>{_escape(item.path)}</code></li>'
        for item, message in anomalies
    )
    anomaly_rows += "".join(
        f'<li><strong>Scan finding</strong>: {_escape(message)} <code>{_escape(path)}</code></li>'
        for path, message in scope_findings
    )
    anomaly_rows = anomaly_rows or '<li>No lifecycle anomalies detected.</li>'
    rendered_claims = "".join(
        '<li>'
        f'<strong>{_escape(claim.get("claim_id", "unnamed"))}</strong> — {_escape(claim.get("agent", "unknown agent"))}; '
        f'branch {_escape(claim.get("branch", "unknown"))}; '
        f'worktree {_escape(claim.get("worktree", "unknown"))}; '
        f'heartbeat {_escape(claim.get("heartbeat", "unknown"))}'
        '</li>'
        for claim in snapshot.claims
    )
    if snapshot.claim_status != "available":
        claims_html = f'<li>Claim snapshot {_escape(snapshot.claim_status)}.</li>'
    else:
        claims_html = rendered_claims or '<li>No active claims were present in the captured registry.</li>'
    scope_rows = "".join(f'<li><code>{_escape(path)}</code></li>' for path in scanned)
    ignored_rows = "".join(f'<li><code>{_escape(path)}</code></li>' for path in ignored) or '<li>None</li>'
    css = """
    :root{color-scheme:light dark;--page:#f7f7f5;--surface:#fff;--soft:#ededeb;--text:#202124;--muted:#62666d;--line:#d6d7d4;--accent:#164f86;--accent-bg:#e8f2ff;--warn:#8a4318;--warn-bg:#fff0e6;--input:#5c3cad;--input-bg:#f0ebff}
    @media(prefers-color-scheme:dark){:root{--page:#171819;--surface:#222426;--soft:#303235;--text:#f4f5f6;--muted:#b4b7bc;--line:#414449;--accent:#b9dcff;--accent-bg:#173653;--warn:#ffc39c;--warn-bg:#4e2b18;--input:#d0c1ff;--input-bg:#35265b}}
    *{box-sizing:border-box}body{margin:0;background:var(--page);color:var(--text);font:16px/1.5 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}main{width:min(100%,1120px);margin:auto;padding:clamp(1rem,3vw,2.5rem)}h1,h2,h3,p{margin-top:0}h1{max-width:20ch;font-size:clamp(2rem,5vw,3.5rem);line-height:1.05;letter-spacing:-.035em}h2{font-size:clamp(1.35rem,3vw,1.75rem)}h3{margin:.6rem 0 .35rem;font-size:1.05rem}.lede,.meta,.section-head p,.detail,.source{color:var(--muted)}.meta{font-size:.85rem}.metric-grid,.item-grid,.count-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,210px),1fr));gap:.75rem}.metric,.item,.panel{min-width:0;padding:1rem;border:1px solid var(--line);border-radius:.9rem;background:var(--surface)}.metric span,.metric strong{display:block}.metric strong{font-size:2rem;line-height:1.1}.section{margin-top:2.5rem}.section-head{margin-bottom:.9rem}.section-head p{max-width:75ch;margin:.25rem 0 0}.badges{display:flex;flex-wrap:wrap;gap:.4rem}.badge{display:inline-block;padding:.14rem .5rem;border:1px solid var(--line);border-radius:999px;font-size:.76rem;font-weight:650}.badge-status{color:var(--accent);background:var(--accent-bg)}.badge-type{color:var(--input);background:var(--input-bg)}code{overflow-wrap:anywhere}.interaction{margin:.75rem 0;padding:.75rem;border-left:4px solid var(--input);background:var(--input-bg)}.interaction dt{font-weight:700}.interaction dd{margin:0 0 .55rem}.interaction dd:last-child{margin-bottom:0}.source{margin-bottom:0;font-size:.82rem}.empty{padding:1rem;border:1px dashed var(--line);border-radius:.9rem}.count-grid table{width:100%;border-collapse:collapse}.count-grid th{text-align:left;font-weight:500}.count-grid td{text-align:right}.count-grid th,.count-grid td{padding:.35rem;border-bottom:1px solid var(--line)}.findings{padding-left:1.25rem}.findings li{margin:.5rem 0}.snapshot{border-left:4px solid var(--accent)}a{color:inherit;text-underline-offset:.18em}a:focus-visible{outline:3px solid var(--accent);outline-offset:3px}@media(max-width:420px){main{padding:.75rem}.metric,.item,.panel{padding:.8rem}.badges{align-items:flex-start}}
    @media print{body{background:#fff;color:#111}.metric,.item,.panel{break-inside:avoid}}
    """
    return f"""<!doctype html>
<!-- Generated from repository backlog sources. Do not edit this report by hand. -->
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light dark"><title>Backlog Operator Report</title><style>{css}</style></head>
<body><main>
<header><p class="meta">Repository backlog · source commit {_escape(snapshot.source_commit)}</p><h1>Backlog operator report</h1><p class="lede">A source-backed view of dispatchable work, lifecycle evidence, dependencies, archives, and decisions that need your input.</p><p class="meta">Generated {_escape(snapshot.generated_at)}</p></header>
<section aria-labelledby="summary-title"><h2 id="summary-title">Summary</h2><div class="metric-grid">{metrics_html}</div><div class="count-grid"><div class="panel"><h3>Underlying type counts</h3><table><tbody>{count_rows}</tbody></table></div><div class="panel"><h3>Declared status counts</h3><table><tbody>{status_rows}</tbody></table></div></div></section>
{_section("Needs Your Input", "Waiting for a decision, approval, action, or information from you. These items retain Status: User Action Required and are excluded from unattended work.", needs_input, "No user action is currently required.")}
{_section("Runnable Work", "Ready items whose declared dependencies are satisfied. Workspace claims do not change this lifecycle classification.", runnable, "No items are effectively eligible for dispatch.")}
{_section("Blocked Work", "Active items with unmet dependencies or a declared Blocked status.", blocked, "No blocked active items.")}
{_section("Holding", "Visible work intentionally excluded from unattended dispatch.", holding, "No holding items.")}
{_section("Active Typed Work", "All items found in typed active queues, including running and non-runnable states.", active, "No active typed items.")}
{_section("Completed Archive", "Successful outcomes found in the completed archive.", completed, "No completed archive items.")}
{_section("Failed Archive", "Failed or abandoned outcomes found in the failed archive.", failed, "No failed archive items.")}
<section class="section" aria-labelledby="findings-title"><div class="section-head"><div><h2 id="findings-title">Lifecycle Reconciliation</h2><p>Read-only findings about metadata, dependencies, status, placement, and archives. Status: Proposed is treated as migration debt and never as an operational bucket.</p></div></div><div class="panel"><ul class="findings">{anomaly_rows}</ul></div></section>
<section class="section" aria-labelledby="claims-title"><div class="section-head"><div><h2 id="claims-title">Workspace Claim Snapshot</h2><p>Captured {_escape(snapshot.claim_captured_at)}. Claims and worktrees are workspace coordination evidence, not backlog lifecycle status or dispatch eligibility.</p></div></div><div class="panel snapshot"><ul>{claims_html}</ul></div></section>
<section class="section" aria-labelledby="scope-title"><div class="section-head"><div><h2 id="scope-title">Report Scope</h2><p>Freshness and inventory boundaries for this generated snapshot.</p></div></div><div class="count-grid"><div class="panel"><h3>Scanned folders</h3><ul>{scope_rows}</ul></div><div class="panel"><h3>Ignored guidance files</h3><ul>{ignored_rows}</ul></div></div></section>
</main></body></html>"""


def generate_report(repository_root: Path, output: Path, generated_at: str | None = None) -> None:
    """Generate a report from repository_root and write it to output.

    repository_root must contain a backlog directory. output must not resolve
    to a scanned backlog source or guidance file; its parent directories are
    created after that validation. generated_at
    accepts an explicit ISO-8601 snapshot value for reproducible automation and
    otherwise defaults to the current UTC time. Source backlog files are read
    but never modified. Invalid backlog content is rendered as findings; a
    missing backlog root raises ValueError and output failures propagate.
    """
    resolved_root = repository_root.resolve()
    timestamp = generated_at or datetime.now(timezone.utc).isoformat(timespec="seconds")
    items, scanned, ignored, scope_findings = _read_items(resolved_root)
    scanned_sources = {resolved_root / item.path for item in items}
    scanned_sources.update(resolved_root / path for path in ignored)
    resolved_output = output.resolve()
    if resolved_output in {path.resolve() for path in scanned_sources}:
        raise ValueError(f"Output path would overwrite a backlog source: {resolved_output}")
    _reconcile(items)
    claim_captured_at, claims, claim_status = _claim_snapshot(resolved_root, timestamp)
    snapshot = _Snapshot(
        _source_commit(resolved_root), timestamp, claim_captured_at, claims, claim_status
    )
    rendered = _render_report(items, scanned, ignored, scope_findings, snapshot)
    resolved_output.parent.mkdir(parents=True, exist_ok=True)
    resolved_output.write_text(rendered, encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line generator and return a process exit status.

    argv is an optional argument sequence used by tests and embedded callers;
    None reads the process arguments. The command writes one explicit output
    path and returns zero on success. Parsing, input, and I/O errors are exposed
    to the caller with their original causes.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd(), help="repository containing backlog/")
    parser.add_argument("--output", type=Path, required=True, help="standalone HTML output path")
    parser.add_argument("--generated-at", help="explicit ISO-8601 snapshot time for reproducible output")
    arguments = parser.parse_args(argv)
    generate_report(arguments.repository_root, arguments.output, arguments.generated_at)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
