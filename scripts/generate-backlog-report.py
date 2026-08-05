#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Generates a deterministic, self-contained HTML view of repository work items and explicitly requested Future Ideas.
# Governing backlog items: backlog/feature-backlog/add-styled-backlog-report-with-user-input.md, backlog/feature-backlog/add-lightweight-future-ideas-capture.md, backlog/feature-backlog/add-dedicated-watchdog-and-stalled-lifecycle.md, and backlog/feature-backlog/archive-terminal-work-item-series.md

"""Generate an offline HTML report from the repository backlog."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import tempfile
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence
from urllib.parse import urlsplit


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
FUTURE_IDEAS_FOLDER = "future-ideas"
FUTURE_IDEA_REQUIRED_SECTIONS = ("Synopsis", "Origin or Rationale")
FUTURE_IDEA_PROMOTION_QUEUES = {"active", "holding", "user-action-required"}
ALLOWED_COMPLETIONS = {"direct-main", "feature-branch", "UNSET"}
REQUIRED_SECTIONS = (
    "Summary",
    "Context",
    "Requirements",
    "Acceptance Criteria",
    "Dependencies",
    "Verification",
)
USER_SECTIONS = (
    "User Action Required",
    "Question for the User",
    "Why User Input Is Required",
    "Resolution",
    "Unattended Work Boundary",
)
ALLOWED_TYPES = {"Defect", "Feature", "Analysis", "Investigation", "Holding"}
DISPATCHABLE_TYPES = {"Defect", "Feature", "Analysis", "Investigation"}
ALLOWED_STATUSES = {
    "Ready",
    "Starting",
    "Claimed",
    "Running",
    "Stalled",
    "Blocked",
    "User Action Required",
    "Awaiting Review",
    "Target Merge Pending",
    "Completed",
    "Failed",
    "Abandoned",
    "Holding",
}
TERMINAL_SERIES_STATUSES = {"Completed", "Failed", "Abandoned"}
SEMANTIC_STATUS_CLASSES = {
    "Stalled": "stalled",
    "Blocked": "blocked",
    "User Action Required": "user-action-required",
}
STALLED_EVIDENCE_FIELDS = (
    "Last Known Productive Evidence",
    "Phase Estimate",
    "Hard Stop",
    "Anomaly or Progress Gap",
    "Canonical Conversation",
    "Root Agent Task",
    "Current Ownership and Coordination State",
    "Diagnostic Owner",
    "Next Investigation Action",
)
DEPENDENCY_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^]]+\]\(([^)#?]+\.md)(?:#[^)]*)?\)")
DEPENDENCY_LINK_PATTERN = re.compile(r"\[[^]\r\n]+\]\(([^)\r\n]+)\)")
INLINE_MARKDOWN_PATTERN = re.compile(r"(`[^`]*`|\*\*([^*]+)\*\*|\*([^*]+)\*|\[([^]]+)\]\([^)]+\))")


@dataclass
class _Item:
    path: str
    slug: str
    work_item_id: str
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
    provider: str = ""
    completion: str = ""
    owner: str = ""
    diagnostic_owner: str = ""
    next_investigation_action: str = ""
    source_evidence: str = ""
    stalled_evidence: dict[str, str] = field(default_factory=dict)
    stalled_evidence_missing: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    anomalies: list[str] = field(default_factory=list)
    unmet_dependencies: list[str] = field(default_factory=list)
    satisfied_dependencies: list[str] = field(default_factory=list)
    eligible: bool = False
    promotion_complete: bool = False
    authority_valid: bool = True


@dataclass
class _FutureIdea:
    path: str
    title: str
    synopsis: str
    origin: str
    notes: str
    revisit_trigger: str
    promoted_to: str
    anomalies: list[str] = field(default_factory=list)


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


def _parse_labeled_section(section: str) -> dict[str, str]:
    """Parse one-line label and value pairs from a Markdown section."""
    fields: dict[str, str] = {}
    for line in section.splitlines():
        match = re.fullmatch(r"([A-Za-z][A-Za-z ]+):\s*(.*?)\s*", line.strip())
        if match:
            fields[match.group(1)] = match.group(2)
    return fields


def _external_uri(value: str) -> bool:
    """Return whether a complete dependency value identifies a non-local URI."""
    try:
        parsed = urlsplit(value)
    except ValueError:
        return False
    return bool(parsed.scheme or parsed.netloc)


def _local_backlog_dependency_slug(
    target: str, item_path: Path, backlog_root: Path
) -> str | None:
    """Return the slug for a relative Markdown target contained by the backlog."""
    try:
        parsed = urlsplit(target)
    except ValueError:
        return None
    if (
        parsed.scheme
        or parsed.netloc
        or "?" in target
        or "#" in target
        or any(character.isspace() for character in target)
    ):
        return None
    target_path = Path(parsed.path)
    if target_path.is_absolute() or target_path.suffix != ".md":
        return None
    try:
        resolved_target = (item_path.parent / target_path).resolve()
        resolved_target.relative_to(backlog_root.resolve())
    except (OSError, RuntimeError, ValueError):
        return None
    return resolved_target.stem


def _dependencies(section: str, item_path: Path, backlog_root: Path) -> list[str]:
    """Extract dependency declarations while preserving their declared order."""
    if not section or section.strip().lower() == "none":
        return []
    values: list[str] = []
    for line in section.splitlines():
        candidate = line.strip().lstrip("-* ").strip()
        normalized = candidate.strip("`.,;:()[]")
        if not candidate or normalized.lower() == "none":
            continue
        link_match = DEPENDENCY_LINK_PATTERN.fullmatch(candidate)
        if link_match:
            local_slug = _local_backlog_dependency_slug(
                link_match.group(1), item_path, backlog_root
            )
            if local_slug:
                candidate = local_slug
        elif (
            not DEPENDENCY_LINK_PATTERN.search(candidate)
            and not any(character.isspace() for character in candidate)
            and not _external_uri(candidate)
        ):
            candidate = normalized
        values.append(candidate)
    return values


def _series_orders(
    backlog_root: Path,
) -> tuple[dict[str, tuple[str, int]], list[str], list[tuple[str, str]]]:
    """Map series order and report unreadable, terminal-active, or broken navigation."""
    orders: dict[str, tuple[str, int]] = {}
    ignored: list[str] = []
    findings: list[tuple[str, str]] = []
    for folder_name in SCAN_FOLDERS:
        folder = backlog_root / folder_name
        if not folder.is_dir():
            continue
        for index in sorted(folder.rglob("index.md")):
            relative_index = index.relative_to(backlog_root.parent).as_posix()
            ignored.append(relative_index)
            try:
                content = index.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                findings.append(
                    (
                        relative_index,
                        f"Unreadable series index: {type(exc).__name__}: {exc}",
                    )
                )
                continue
            series = index.parent.name
            linked_statuses: list[str] = []
            linked_items_complete = True
            for position, target in enumerate(
                MARKDOWN_LINK_PATTERN.findall(content), start=1
            ):
                child = (index.parent / target).resolve()
                try:
                    relative_child = child.relative_to(
                        backlog_root.parent.resolve()
                    ).as_posix()
                except ValueError:
                    continue
                orders.setdefault(relative_child, (series, position))
                try:
                    child.relative_to(backlog_root.resolve())
                except ValueError:
                    continue
                if not child.is_file():
                    findings.append(
                        (relative_index, f"Broken series index link: {target}.")
                    )
                    linked_items_complete = False
                    continue
                if child.name in {"README.md", "index.md"}:
                    continue
                try:
                    _, child_fields, _ = _parse_document(child)
                except (OSError, UnicodeError):
                    linked_items_complete = False
                    continue
                child_status = child_fields.get("Status", "")
                if not child_status:
                    linked_items_complete = False
                    continue
                linked_statuses.append(child_status)
                child_series = child_fields.get("Series", "")
                if child_series and child_series != relative_index:
                    findings.append(
                        (
                            relative_child,
                            "Child Series reference does not match its index: "
                            f"expected {relative_index}, found {child_series}.",
                        )
                    )
            relative_to_backlog = index.relative_to(backlog_root)
            if (
                relative_to_backlog.parts[0] in ACTIVE_FOLDERS
                and linked_items_complete
                and linked_statuses
                and all(
                    status in TERMINAL_SERIES_STATUSES
                    for status in linked_statuses
                )
            ):
                findings.append(
                    (
                        relative_index,
                        "Terminal series index remains in an active typed backlog.",
                    )
                )
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


def _is_resolved_regular_file_within(
    path: Path,
    authority_root: Path,
    repository_root: Path,
) -> bool:
    """Return whether path resolves to a regular file inside both authority roots."""
    try:
        resolved_path = path.resolve(strict=True)
        resolved_path.relative_to(authority_root.resolve(strict=True))
        resolved_path.relative_to(repository_root.resolve(strict=True))
    except (OSError, RuntimeError, ValueError):
        return False
    return resolved_path.is_file()


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
            queue = _queue_for(relative)
            if path.name in {"README.md", "index.md"}:
                if relative_text not in ignored:
                    ignored.append(relative_text)
                continue
            if not _is_resolved_regular_file_within(
                path, folder, repository_root
            ):
                item = _Item(
                    relative_text, path.stem, path.stem, path.stem, queue, "", "", "", []
                )
                item.authority_valid = False
                item.anomalies.append(
                    "Backlog item resolves outside canonical backlog authority: "
                    f"{relative_text}."
                )
                items.append(item)
                continue
            try:
                title, fields, sections = _parse_document(path)
            except (OSError, UnicodeError) as exc:
                item = _Item(relative_text, path.stem, path.stem, path.stem, queue, "", "", "", [])
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
            stalled_evidence = _parse_labeled_section(
                sections.get("Stalled Evidence", "")
            )
            stalled_evidence_missing: list[str] = []
            if fields.get("Status") == "Stalled":
                stalled_evidence_missing = [
                    name
                    for name in STALLED_EVIDENCE_FIELDS
                    if not stalled_evidence.get(name, "").strip()
                ]
            item = _Item(
                path=relative_text,
                slug=path.stem,
                work_item_id=fields.get("Work Item ID", "") or path.stem,
                title=title or path.stem,
                queue=queue,
                declared_type=fields.get("Type", ""),
                status=fields.get("Status", ""),
                summary=_plain_text(sections.get("Summary", "")),
                dependencies=_dependencies(
                    sections.get("Dependencies", ""), path, backlog_root
                ),
                series=series,
                series_order=series_order,
                priority=priority,
                question=_plain_text(sections.get("Question for the User", "")),
                resolution=_plain_text(sections.get("Resolution", "")),
                provider=fields.get("Provider", ""),
                completion=fields.get("Completion", ""),
                owner=fields.get("Owner", ""),
                diagnostic_owner=fields.get("Diagnostic Owner", ""),
                next_investigation_action=fields.get(
                    "Next Investigation Action",
                    "",
                ),
                source_evidence=sections.get("Source Evidence", ""),
                stalled_evidence=stalled_evidence,
                stalled_evidence_missing=stalled_evidence_missing,
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
            if item.work_item_id != path.stem:
                item.anomalies.append(
                    "Work Item ID does not match the immutable filename stem: "
                    f"{item.work_item_id}."
                )
            if item.missing:
                item.anomalies.append("Missing required fields: " + ", ".join(item.missing) + ".")
            if item.stalled_evidence_missing:
                item.anomalies.extend(
                    f"Missing Stalled evidence: {name}."
                    for name in item.stalled_evidence_missing
                )
            absent: list[str] = []
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
            promotion_type_valid = item.declared_type in DISPATCHABLE_TYPES or (
                queue == "holding" and item.declared_type == "Holding"
            )
            item.promotion_complete = (
                not item.missing
                and not item.stalled_evidence_missing
                and promotion_type_valid
                and item.provider == "file"
                and item.work_item_id == path.stem
                and item.completion in ALLOWED_COMPLETIONS
                and bool(item.source_evidence.strip())
                and bool(sections.get("Open Questions", "").strip())
                and (
                    (
                        queue == "active"
                        and expected_type == item.declared_type
                        and item.status
                        in {
                            "Ready",
                            "Starting",
                            "Claimed",
                            "Running",
                            "Stalled",
                            "Blocked",
                            "Awaiting Review",
                            "Target Merge Pending",
                        }
                    )
                    or (queue == "holding" and item.status == "Holding")
                    or (
                        queue == "user-action-required"
                        and item.status == "User Action Required"
                        and not absent
                    )
                )
            )
            items.append(item)
    items_by_id: dict[str, list[_Item]] = {}
    for item in items:
        items_by_id.setdefault(item.work_item_id, []).append(item)
    for work_item_id, matches in items_by_id.items():
        if work_item_id and len(matches) > 1:
            locations = ", ".join(sorted(item.path for item in matches))
            for item in matches:
                item.anomalies.append(
                    f"Duplicate Work Item ID {work_item_id}: {locations}."
                )
    return items, scanned, sorted(set(ignored)), scope_findings


def _source_evidence_references(section: str, canonical_path: str) -> bool:
    """Return whether Source Evidence contains one exact canonical path reference."""
    for line in section.splitlines():
        candidate = line.strip().lstrip("-* ").strip()
        if candidate.strip("`") == canonical_path:
            return True
        link = DEPENDENCY_LINK_PATTERN.fullmatch(candidate)
        if link and link.group(1) == canonical_path:
            return True
    return False


def _read_future_ideas(
    repository_root: Path,
    work_items: list[_Item],
) -> tuple[list[_FutureIdea], list[str], list[str]]:
    """Read and validate lightweight ideas only for an explicit listing operation."""
    ideas_root = repository_root / "backlog" / FUTURE_IDEAS_FOLDER
    if not ideas_root.is_dir():
        return [], [], []
    work_items_by_path = {item.path: item for item in work_items}
    work_items_by_id = {item.work_item_id: item for item in work_items}
    ideas: list[_FutureIdea] = []
    ignored: list[str] = []
    for path in sorted(ideas_root.rglob("*.md")):
        relative_text = path.relative_to(repository_root).as_posix()
        if path.name in {"README.md", "index.md"}:
            ignored.append(relative_text)
            continue
        if not _is_resolved_regular_file_within(
            path, ideas_root, repository_root
        ):
            idea = _FutureIdea(relative_text, path.stem, "", "", "", "", "")
            idea.anomalies.append(
                "Future Idea resolves outside canonical Future Ideas authority: "
                f"{relative_text}."
            )
            ideas.append(idea)
            continue
        try:
            title, fields, sections = _parse_document(path)
        except (OSError, UnicodeError) as exc:
            idea = _FutureIdea(relative_text, path.stem, "", "", "", "", "")
            idea.anomalies.append(
                f"Unreadable Future Idea: {type(exc).__name__}: {exc}"
            )
            ideas.append(idea)
            continue
        missing = [
            name
            for name in FUTURE_IDEA_REQUIRED_SECTIONS
            if not sections.get(name)
        ]
        if not title:
            missing.insert(0, "Title")
        idea = _FutureIdea(
            path=relative_text,
            title=title or path.stem,
            synopsis=_plain_text(sections.get("Synopsis", "")),
            origin=_plain_text(sections.get("Origin or Rationale", "")),
            notes=_plain_text(sections.get("Notes", "")),
            revisit_trigger=_plain_text(sections.get("Revisit Trigger", "")),
            promoted_to=fields.get("Promoted To", ""),
        )
        if missing:
            idea.anomalies.append(
                "Missing required idea fields: " + ", ".join(missing) + "."
            )
        if idea.promoted_to:
            target = Path(idea.promoted_to)
            valid_parts = (
                not target.is_absolute()
                and ".." not in target.parts
                and len(target.parts) >= 3
                and target.parts[0] == "backlog"
                and target.suffix == ".md"
            )
            valid_identifier = bool(DEPENDENCY_PATTERN.fullmatch(idea.promoted_to))
            target_item = (
                work_items_by_id.get(idea.promoted_to)
                if valid_identifier
                else None
            )
            if target_item is None and valid_parts:
                target_item = work_items_by_path.get(idea.promoted_to)
            if (
                target_item is None
                or target_item.queue not in FUTURE_IDEA_PROMOTION_QUEUES
            ):
                idea.anomalies.append(
                    f"Invalid Promoted To Work Item ID: {idea.promoted_to}."
                )
            elif not target_item.authority_valid:
                idea.anomalies.append(
                    "Promotion target resolves outside canonical backlog authority: "
                    f"{idea.promoted_to}."
                )
            else:
                if not target_item.promotion_complete:
                    idea.anomalies.append(
                        "Promotion target is not a complete work item: "
                        f"{idea.promoted_to}."
                    )
                if not _source_evidence_references(
                    target_item.source_evidence, relative_text
                ):
                    idea.anomalies.append(
                        "Promotion target Source Evidence does not reference "
                        f"{relative_text}: {idea.promoted_to}."
                    )
        ideas.append(idea)
    return ideas, [ideas_root.relative_to(repository_root).as_posix()], ignored


def _reconcile(items: list[_Item]) -> None:
    """Resolve dependency evidence and validate canonical dispatch lifecycle in place."""
    completed = {item.work_item_id for item in items if item.queue == "completed"}
    known = {item.work_item_id for item in items}
    for item in items:
        for dependency in item.dependencies:
            if not DEPENDENCY_PATTERN.fullmatch(dependency):
                item.unmet_dependencies.append(dependency)
                if (
                    any(character.isspace() for character in dependency)
                    or DEPENDENCY_LINK_PATTERN.search(dependency)
                    or _external_uri(dependency)
                ):
                    item.anomalies.append(
                        "External prerequisite requires manual satisfaction: "
                        f"{dependency}"
                    )
                else:
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
        if item.queue == "active" and item.status == "Ready" and item.unmet_dependencies:
            item.anomalies.append(
                "Invalid lifecycle: Ready status has unmet hard dependencies; "
                "record Blocked with an exact unblock condition before dispatch."
            )
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


def _status_badge(status: str) -> str:
    """Render a labelled status badge with semantic styling where required."""
    classes = ["badge", "badge-status"]
    semantic_class = SEMANTIC_STATUS_CLASSES.get(status)
    if semantic_class:
        classes.append(f"badge-status-{semantic_class}")
    return f'<span class="{" ".join(classes)}">{_escape(status or "Missing")}</span>'


def _item_card(item: _Item) -> str:
    """Render a traceable backlog item card with lifecycle and dependency evidence."""
    metadata = [_badge(item.declared_type, "type"), _status_badge(item.status)]
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
    elif item.status == "Stalled":
        stalled_evidence = dict(item.stalled_evidence)
        if not stalled_evidence.get("Current Ownership and Coordination State", ""):
            stalled_evidence["Current Ownership and Coordination State"] = (
                item.owner or "Unowned"
            )
        if not stalled_evidence.get("Diagnostic Owner", ""):
            stalled_evidence["Diagnostic Owner"] = item.diagnostic_owner
        if not stalled_evidence.get("Next Investigation Action", ""):
            stalled_evidence["Next Investigation Action"] = (
                item.next_investigation_action
            )
        detail = (
            '<dl class="interaction">'
            + "".join(
                f"<dt>{_escape(field_name)}</dt>"
                f"<dd>{_escape(stalled_evidence.get(field_name, '') or 'Missing')}</dd>"
                for field_name in STALLED_EVIDENCE_FIELDS
            )
            + "</dl>"
        )
    return (
        '<article class="item">'
        f'<div class="badges">{"".join(metadata)}</div>'
        f'<h3>{_escape(item.title)}</h3>'
        f'<p>{_escape(item.summary or "No summary provided.")}</p>'
        f'<p class="detail"><strong>Work Item ID:</strong> '
        f'<code>{_escape(item.work_item_id)}</code></p>'
        f'<p class="detail"><strong>Dependencies:</strong> {_escape(dependency_text)}</p>'
        f'{detail}<p class="source"><strong>Source:</strong> <code>{_escape(item.path)}</code></p>'
        '</article>'
    )


def _future_idea_card(idea: _FutureIdea) -> str:
    """Render one explicitly requested Future Idea without lifecycle badges."""
    notes = (
        f'<p class="detail"><strong>Notes:</strong> {_escape(idea.notes)}</p>'
        if idea.notes
        else ""
    )
    revisit = idea.revisit_trigger or "None recorded"
    promoted_to = idea.promoted_to or "Not promoted"
    return (
        '<article class="item">'
        '<div class="badges"><span class="badge">Future Idea</span></div>'
        f'<h3>{_escape(idea.title)}</h3>'
        f'<p>{_escape(idea.synopsis or "Missing synopsis.")}</p>'
        f'<p class="detail"><strong>Origin or Rationale:</strong> '
        f'{_escape(idea.origin or "Missing")}</p>'
        f"{notes}"
        f'<p class="detail"><strong>Revisit Trigger:</strong> {_escape(revisit)}</p>'
        f'<p class="detail"><strong>Promoted To:</strong> {_escape(promoted_to)}</p>'
        f'<p class="source"><strong>Source:</strong> '
        f'<code>{_escape(idea.path)}</code></p>'
        "</article>"
    )


def _section(title: str, description: str, items: Iterable[_Item], empty: str) -> str:
    """Render a named report section and a stable empty state."""
    rendered = "".join(_item_card(item) for item in items)
    body = f'<div class="item-grid">{rendered}</div>' if rendered else f'<p class="empty">{_escape(empty)}</p>'
    return f'<section class="section"><div class="section-head"><div><h2>{_escape(title)}</h2><p>{_escape(description)}</p></div></div>{body}</section>'


def _future_ideas_section(ideas: Iterable[_FutureIdea]) -> str:
    """Render the opt-in idea inventory and its stable empty state."""
    rendered = "".join(_future_idea_card(idea) for idea in ideas)
    body = (
        f'<div class="item-grid">{rendered}</div>'
        if rendered
        else '<p class="empty">No Future Ideas are currently recorded.</p>'
    )
    return (
        '<section class="section"><div class="section-head"><div>'
        '<h2>Future Ideas</h2><p>Explicitly requested lightweight ideas that are '
        "not approved work, lifecycle items, or unattended dispatch candidates.</p>"
        f"</div></div>{body}</section>"
    )


def _sort_key(item: _Item) -> tuple[int, str, int, int, str]:
    """Order by queue, series, series order, priority, and stable path."""
    queue_order = {"user-action-required": 0, "active": 1, "holding": 2, "completed": 3, "failed": 4, "invalid": 5}
    return (queue_order[item.queue], item.series, item.series_order, item.priority, item.path)


def _render_report(
    items: list[_Item],
    future_ideas: list[_FutureIdea],
    include_future_ideas: bool,
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
    stalled = [item for item in active if item.status == "Stalled"]
    blocked = [item for item in active if item.status == "Blocked"]
    holding = [item for item in ordered if item.queue == "holding"]
    completed = [item for item in ordered if item.queue == "completed"]
    failed = [item for item in ordered if item.queue == "failed"]
    type_counts = Counter(item.declared_type or "Missing" for item in ordered)
    status_counts = Counter(item.status or "Missing" for item in ordered)
    anomalies = [(item, anomaly) for item in ordered for anomaly in item.anomalies]
    idea_anomalies = [
        (idea, anomaly) for idea in future_ideas for anomaly in idea.anomalies
    ]
    metrics = [
        ("Active typed items", len(active)),
        ("Runnable now", len(runnable)),
        ("Needs your input", len(needs_input)),
        ("Stalled", len(stalled)),
        ("Holding", len(holding)),
        ("Completed archive", len(completed)),
        ("Failed archive", len(failed)),
        (
            "Validation findings",
            len(anomalies) + len(idea_anomalies) + len(scope_findings),
        ),
    ]
    if include_future_ideas:
        metrics.insert(4, ("Future ideas", len(future_ideas)))
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
        f'<li><strong>{_escape(idea.title)}</strong>: {_escape(message)} '
        f'<code>{_escape(idea.path)}</code></li>'
        for idea, message in idea_anomalies
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
    :root{color-scheme:light dark;--page:#f7f7f5;--surface:#fff;--soft:#ededeb;--text:#202124;--muted:#62666d;--line:#d6d7d4;--accent:#164f86;--accent-bg:#e8f2ff;--warn:#8a4318;--warn-bg:#fff0e6;--input:#5c3cad;--input-bg:#f0ebff;--stalled:#7a3a0c;--stalled-bg:#fff0df;--blocked:#8c1d2c;--blocked-bg:#fdebed;--user-action:#5c3cad;--user-action-bg:#f0ebff}
    @media(prefers-color-scheme:dark){:root{--page:#171819;--surface:#222426;--soft:#303235;--text:#f4f5f6;--muted:#b4b7bc;--line:#414449;--accent:#b9dcff;--accent-bg:#173653;--warn:#ffc39c;--warn-bg:#4e2b18;--input:#d0c1ff;--input-bg:#35265b;--stalled:#ffc39c;--stalled-bg:#4e2b18;--blocked:#ffb3bd;--blocked-bg:#541f29;--user-action:#d0c1ff;--user-action-bg:#35265b}}
    *{box-sizing:border-box}body{margin:0;background:var(--page);color:var(--text);font:16px/1.5 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}main{width:min(100%,1120px);margin:auto;padding:clamp(1rem,3vw,2.5rem)}h1,h2,h3,p{margin-top:0}h1{max-width:20ch;font-size:clamp(2rem,5vw,3.5rem);line-height:1.05;letter-spacing:-.035em}h2{font-size:clamp(1.35rem,3vw,1.75rem)}h3{margin:.6rem 0 .35rem;font-size:1.05rem}.lede,.meta,.section-head p,.detail,.source{color:var(--muted)}.meta,.detail,.findings li,.snapshot{overflow-wrap:anywhere}.meta{font-size:.85rem}.metric-grid,.item-grid,.count-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,210px),1fr));gap:.75rem}.metric,.item,.panel{min-width:0;padding:1rem;border:1px solid var(--line);border-radius:.9rem;background:var(--surface)}.metric span,.metric strong{display:block}.metric strong{font-size:2rem;line-height:1.1}.section{margin-top:2.5rem}.section-head{margin-bottom:.9rem}.section-head p{max-width:75ch;margin:.25rem 0 0}.badges{display:flex;flex-wrap:wrap;gap:.4rem}.badge{display:inline-block;padding:.14rem .5rem;border:1px solid var(--line);border-radius:999px;font-size:.76rem;font-weight:650}.badge-status{color:var(--accent);background:var(--accent-bg)}.badge-status-stalled{color:var(--stalled);background:var(--stalled-bg);border-color:var(--stalled)}.badge-status-blocked{color:var(--blocked);background:var(--blocked-bg);border-color:var(--blocked)}.badge-status-user-action-required{color:var(--user-action);background:var(--user-action-bg);border-color:var(--user-action)}.badge-type{color:var(--input);background:var(--input-bg)}code{overflow-wrap:anywhere}.interaction{margin:.75rem 0;padding:.75rem;border-left:4px solid var(--input);background:var(--input-bg)}.interaction dt{font-weight:700}.interaction dd{margin:0 0 .55rem}.interaction dd:last-child{margin-bottom:0}.source{margin-bottom:0;font-size:.82rem}.empty{padding:1rem;border:1px dashed var(--line);border-radius:.9rem}.count-grid table{width:100%;border-collapse:collapse}.count-grid th{text-align:left;font-weight:500}.count-grid td{text-align:right}.count-grid th,.count-grid td{padding:.35rem;border-bottom:1px solid var(--line)}.findings{padding-left:1.25rem}.findings li{margin:.5rem 0}.snapshot{border-left:4px solid var(--accent)}a{color:inherit;text-underline-offset:.18em}a:focus-visible{outline:3px solid var(--accent);outline-offset:3px}@media(max-width:420px){main{padding:.75rem}.metric,.item,.panel{padding:.8rem}.badges{align-items:flex-start}}
    @media print{body{background:#fff;color:#111}.metric,.item,.panel{break-inside:avoid}}
    """
    return f"""<!doctype html>
<!-- Generated from repository backlog sources. Do not edit this report by hand. -->
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light dark"><title>Backlog Operator Report</title><style>{css}</style></head>
<body><main>
<header><p class="meta">Repository backlog · source commit {_escape(snapshot.source_commit)}</p><h1>Backlog operator report</h1><p class="lede">A source-backed view of dispatchable work, lifecycle evidence, dependencies, archives, and decisions that need your input.</p><p class="meta">Generated {_escape(snapshot.generated_at)}</p></header>
<section aria-labelledby="summary-title"><h2 id="summary-title">Summary</h2><div class="metric-grid">{metrics_html}</div><div class="count-grid"><div class="panel"><h3>Underlying type counts</h3><table><tbody>{count_rows}</tbody></table></div><div class="panel"><h3>Declared status counts</h3><table><tbody>{status_rows}</tbody></table></div></div></section>
{_section("Needs Your Input", "Waiting for a decision, approval, action, or information from you. These items retain Status: User Action Required and are excluded from unattended work.", needs_input, "No user action is currently required.")}
{_section("Runnable Work", "Items whose canonical lifecycle is Ready. A malformed Ready record with an unmet hard dependency is rejected and reported for provider reconciliation.", runnable, "No canonical Ready items are dispatchable.")}
{_section("Stalled Work", "Active items with evidence that progress has stopped while the cause remains unknown. Each item names its diagnostic owner and next investigation action.", stalled, "No stalled active items.")}
{_section("Blocked Work", "Active items whose canonical provider status is Blocked.", blocked, "No blocked active items.")}
{_section("Holding", "Visible work intentionally excluded from unattended dispatch.", holding, "No holding items.")}
{_future_ideas_section(future_ideas) if include_future_ideas else ""}
{_section("Active Typed Work", "All items found in typed active queues, including running and non-runnable states.", active, "No active typed items.")}
{_section("Completed Archive", "Successful outcomes found in the completed archive.", completed, "No completed archive items.")}
{_section("Failed Archive", "Failed or abandoned outcomes found in the failed archive.", failed, "No failed archive items.")}
<section class="section" aria-labelledby="findings-title"><div class="section-head"><div><h2 id="findings-title">Lifecycle Reconciliation</h2><p>Read-only findings about metadata, dependencies, status, placement, and archives. Status: Proposed is treated as migration debt and never as an operational bucket.</p></div></div><div class="panel"><ul class="findings">{anomaly_rows}</ul></div></section>
<section class="section" aria-labelledby="claims-title"><div class="section-head"><div><h2 id="claims-title">Workspace Claim Snapshot</h2><p>Captured {_escape(snapshot.claim_captured_at)}. Claims and worktrees are workspace coordination evidence, not backlog lifecycle status or dispatch eligibility.</p></div></div><div class="panel snapshot"><ul>{claims_html}</ul></div></section>
<section class="section" aria-labelledby="scope-title"><div class="section-head"><div><h2 id="scope-title">Report Scope</h2><p>Freshness and inventory boundaries for this generated snapshot.</p></div></div><div class="count-grid"><div class="panel"><h3>Scanned folders</h3><ul>{scope_rows}</ul></div><div class="panel"><h3>Ignored guidance files</h3><ul>{ignored_rows}</ul></div></div></section>
</main></body></html>"""


def _same_existing_file(first: Path, second: Path) -> bool:
    """Return whether two existing paths identify the same underlying file.

    Missing paths return False. Other filesystem comparison failures propagate
    so callers cannot write after an inconclusive source-protection check.
    """
    try:
        return os.path.samefile(first, second)
    except FileNotFoundError:
        return False


def _has_multiple_hard_links(path: Path) -> bool:
    """Return whether an existing path has aliases to the same underlying file.

    A missing output is safe to create. Other stat failures propagate so an
    inconclusive alias check cannot be followed by a report write.
    """
    try:
        return path.stat().st_nlink > 1
    except FileNotFoundError:
        return False


def _write_output_atomically(output: Path, rendered: str) -> None:
    """Replace output with rendered text only after a sibling temporary write succeeds.

    output identifies the final report path. rendered is the complete UTF-8
    report. The function creates output's parent, writes a private sibling
    temporary file, and atomically replaces output. Any write or replacement
    failure propagates after the temporary file is removed, preserving prior
    output bytes.
    """
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=output.parent,
        prefix=f".{output.name}.",
        suffix=".tmp",
    )
    temporary = Path(temporary_name)
    try:
        try:
            temporary_stream = os.fdopen(descriptor, "wb")
        except BaseException:
            os.close(descriptor)
            raise
        with temporary_stream:
            temporary_stream.write(rendered.encode("utf-8"))
            temporary_stream.flush()
        os.replace(temporary, output)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def generate_report(
    repository_root: Path,
    output: Path,
    generated_at: str | None = None,
    *,
    include_future_ideas: bool = False,
) -> None:
    """Generate a report from repository_root and write it to output.

    repository_root must contain a backlog directory. output must not resolve
    to a scanned backlog source or guidance file; its parent directories are
    created after that validation. generated_at accepts an explicit ISO-8601
    snapshot value for reproducible automation and otherwise defaults to the
    current UTC time. include_future_ideas explicitly adds the lightweight
    backlog/future-ideas inventory; the default ordinary scan does not read or
    count that folder. Output is always rejected when its lexical path is inside
    backlog/future-ideas, its resolved destination enters that folder, or an
    existing output has multiple hard links. The default mode neither
    enumerates nor stats backlog/future-ideas; only include_future_ideas opens
    that store. Source backlog files are read but never modified. A still-open
    sibling temporary descriptor receives the report bytes before an atomic
    replacement preserves prior output. Invalid scanned content is rendered as
    findings; missing input, unsafe output, and I/O failures propagate to the
    caller.
    """
    lexical_repository_root = Path(os.path.abspath(os.fspath(repository_root)))
    resolved_root = repository_root.resolve()
    lexical_output = Path(os.path.abspath(os.fspath(output)))
    lexical_future_ideas_root = Path(
        os.path.abspath(
            os.fspath(
                lexical_repository_root / "backlog" / FUTURE_IDEAS_FOLDER
            )
        )
    )
    resolved_output = output.resolve()
    resolved_future_ideas_root = resolved_root / "backlog" / FUTURE_IDEAS_FOLDER
    try:
        resolved_output.relative_to(resolved_future_ideas_root)
    except ValueError:
        pass
    else:
        raise ValueError(
            "Output path cannot resolve inside backlog/future-ideas: "
            f"{resolved_output}"
        )
    try:
        lexical_output.relative_to(lexical_future_ideas_root)
    except ValueError:
        pass
    else:
        raise ValueError(
            "Output path cannot be located inside backlog/future-ideas: "
            f"{lexical_output}"
        )
    if _has_multiple_hard_links(resolved_output):
        raise ValueError(
            f"Output path would overwrite a backlog source: {resolved_output}"
        )
    timestamp = generated_at or datetime.now(timezone.utc).isoformat(timespec="seconds")
    items, scanned, ignored, scope_findings = _read_items(resolved_root)
    future_ideas: list[_FutureIdea] = []
    if include_future_ideas:
        future_ideas, idea_scanned, idea_ignored = _read_future_ideas(
            resolved_root, items
        )
        scanned.extend(idea_scanned)
        ignored.extend(idea_ignored)
    scanned_sources = {resolved_root / item.path for item in items}
    scanned_sources.update(resolved_root / idea.path for idea in future_ideas)
    scanned_sources.update(resolved_root / path for path in ignored)
    if resolved_output in {path.resolve() for path in scanned_sources} or any(
        _same_existing_file(resolved_output, path) for path in scanned_sources
    ):
        raise ValueError(f"Output path would overwrite a backlog source: {resolved_output}")
    _reconcile(items)
    claim_captured_at, claims, claim_status = _claim_snapshot(resolved_root, timestamp)
    snapshot = _Snapshot(
        _source_commit(resolved_root), timestamp, claim_captured_at, claims, claim_status
    )
    rendered = _render_report(
        items,
        future_ideas,
        include_future_ideas,
        scanned,
        ignored,
        scope_findings,
        snapshot,
    )
    _write_output_atomically(resolved_output, rendered)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line generator and return a process exit status.

    argv is an optional argument sequence used by tests and embedded callers;
    None reads the process arguments. The command writes one explicit output
    path, includes Future Ideas only when --include-future-ideas is present, and
    returns zero on success. Parsing, input, and I/O errors are exposed to the
    caller with their original causes.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd(), help="repository containing backlog/")
    parser.add_argument("--output", type=Path, required=True, help="standalone HTML output path")
    parser.add_argument("--generated-at", help="explicit ISO-8601 snapshot time for reproducible output")
    parser.add_argument(
        "--include-future-ideas",
        action="store_true",
        help="explicitly include and validate backlog/future-ideas",
    )
    arguments = parser.parse_args(argv)
    generate_report(
        arguments.repository_root,
        arguments.output,
        arguments.generated_at,
        include_future_ideas=arguments.include_future_ideas,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
