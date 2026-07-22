#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies file-work-item template classification and governed approval artifacts.

from __future__ import annotations

import argparse
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path


_REQUIRED_EVIDENCE = (
    "READY-OPEN-QUESTIONS",
    "CONTEXT-ONLY-REJECTED",
    "GENUINE-USER-ACTION",
    "HOLDING",
    "SERIES-LINKAGE",
    "GOVERNED-MANIFEST-REJECTED",
    "EXACT-APPROVAL-ACCEPTED",
    "OUT-OF-SCOPE-REJECTED",
    "CHECKER-NOT-AUTHORITY",
)

_GOVERNED_SOURCES = (
    "skills/create-file-work-item/SKILL.md",
    "agents/roles/dev-activities/dev-coder.role.yaml",
    "agents/role-schema.yaml",
    "agents/model-profiles.yaml",
    "adapters/codex/model-profiles.yaml",
    "skills/create-file-work-item/agents/openai.yaml",
    "adapters/codex/skills/codex-harness-directives/SKILL.md",
    "adapters/codex/skills/codex-harness-directives/agents/openai.yaml",
)

_DEPENDENT_ARTIFACTS = (
    "design/generated/skill-definitions.js",
    "scripts/test_bundle_content.py",
)

_REQUIRED_ITEM_SECTIONS = (
    "Summary",
    "Context",
    "Source Evidence",
    "Requirements",
    "Acceptance Criteria",
    "Dependencies",
    "Verification",
    "Open Questions",
)

_USER_ACTION_SUBSECTIONS = (
    "Question for the User",
    "Why User Input Is Required",
    "Options and Tradeoffs",
    "Resolution",
    "Unattended Work Boundary",
)

_TITLE_PATTERN = re.compile(r"^#[ \t]+([^#].*?)[ \t]*$")
_HEADING_PATTERN = re.compile(r"^(#{2,6})[ \t]+(.+?)[ \t]*$")
_FIELD_PATTERN = re.compile(r"^([A-Za-z][A-Za-z ]+):[ \t]*(.*)$")
_BULLET_PATTERN = re.compile(r"^-[ \t]+(.+?)[ \t]*$")
_BACKTICK_FENCE_PATTERN = re.compile(r"^ {0,3}(`{3,})[^`]*$")
_TILDE_FENCE_PATTERN = re.compile(r"^ {0,3}(~{3,}).*$")


@dataclass(frozen=True)
class Heading:
    """One parsed Markdown heading and its structural ancestry."""

    level: int
    title: str
    line: int
    parents: tuple[str, ...]


class Document:
    """Parse the metadata fields and heading tree of one fixture document."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.lines = text.splitlines()
        self.fenced_lines = self._find_fenced_lines()
        self.titles = self._parse_titles()
        self.headings = self._parse_headings()
        self.fields, self.duplicate_fields = self._parse_fields()

    def _parse_titles(self) -> list[tuple[int, str]]:
        titles: list[tuple[int, str]] = []
        for line_number, line in enumerate(self.lines):
            if line_number in self.fenced_lines:
                continue
            match = _TITLE_PATTERN.fullmatch(line)
            if match is not None:
                titles.append((line_number, match.group(1).strip()))
        return titles

    def _find_fenced_lines(self) -> set[int]:
        fenced_lines: set[int] = set()
        fence_character: str | None = None
        fence_length = 0
        for line_number, line in enumerate(self.lines):
            if fence_character is None:
                match = _BACKTICK_FENCE_PATTERN.fullmatch(line)
                if match is None:
                    match = _TILDE_FENCE_PATTERN.fullmatch(line)
                if match is None:
                    continue
                fence = match.group(1)
                fence_character = fence[0]
                fence_length = len(fence)
                fenced_lines.add(line_number)
                continue
            fenced_lines.add(line_number)
            closing_pattern = re.compile(
                rf"^ {{0,3}}{re.escape(fence_character)}{{{fence_length},}}[ \t]*$"
            )
            if closing_pattern.fullmatch(line) is not None:
                fence_character = None
                fence_length = 0
        return fenced_lines

    def _parse_headings(self) -> list[Heading]:
        headings: list[Heading] = []
        ancestors: list[Heading] = []
        for line_number, line in enumerate(self.lines):
            if line_number in self.fenced_lines:
                continue
            match = _HEADING_PATTERN.fullmatch(line)
            if match is None:
                continue
            level = len(match.group(1))
            while ancestors and ancestors[-1].level >= level:
                ancestors.pop()
            headings.append(
                Heading(
                    level=level,
                    title=match.group(2).strip(),
                    line=line_number,
                    parents=tuple(heading.title for heading in ancestors),
                )
            )
            ancestors.append(headings[-1])
        return headings

    def _parse_fields(self) -> tuple[dict[str, str], set[str]]:
        fields: dict[str, str] = {}
        duplicates: set[str] = set()
        metadata_end = next(
            (heading.line for heading in self.headings if heading.level == 2),
            len(self.lines),
        )
        for line_number, line in enumerate(self.lines[1:metadata_end], start=1):
            if line_number in self.fenced_lines:
                continue
            match = _FIELD_PATTERN.fullmatch(line)
            if match is None:
                continue
            name, value = match.groups()
            if name in fields:
                duplicates.add(name)
            fields[name] = value.strip()
        return fields, duplicates

    def unexpected_preamble_lines(self) -> tuple[str, ...]:
        first_section = next(
            (heading.line for heading in self.headings if heading.level == 2),
            len(self.lines),
        )
        unexpected: list[str] = []
        for line_number, line in enumerate(self.lines[1:first_section], start=1):
            if line_number in self.fenced_lines or not line.strip():
                continue
            if _FIELD_PATTERN.fullmatch(line) is None:
                unexpected.append(line)
        return tuple(unexpected)

    def find_heading(
        self,
        title: str,
        *,
        level: int,
        parents: tuple[str, ...],
    ) -> Heading | None:
        matches = [
            heading
            for heading in self.headings
            if heading.title == title
            and heading.level == level
            and heading.parents == parents
        ]
        return matches[0] if len(matches) == 1 else None

    def _section_end(self, heading: Heading) -> int:
        end = len(self.lines)
        for later in self.headings:
            if later.line > heading.line and later.level <= heading.level:
                end = later.line
                break
        return end

    def raw_section_lines(self, heading: Heading) -> list[str]:
        return self.lines[heading.line + 1 : self._section_end(heading)]

    def section_lines(self, heading: Heading) -> list[str]:
        end = self._section_end(heading)
        return [
            line
            for line_number, line in enumerate(
                self.lines[heading.line + 1 : end],
                start=heading.line + 1,
            )
            if line_number not in self.fenced_lines
        ]

    def section_text(self, heading: Heading) -> str:
        return "\n".join(self.section_lines(heading)).strip()

    def section_substantive_text(self, heading: Heading) -> str:
        substantive: list[str] = []
        for line in self.section_lines(heading):
            if not line.strip():
                continue
            if _HEADING_PATTERN.fullmatch(line) is not None:
                continue
            if _TITLE_PATTERN.fullmatch(line) is not None:
                continue
            substantive.append(line)
        return "\n".join(substantive).strip()

    def section_manifest(
        self,
        heading: Heading,
    ) -> tuple[tuple[str, ...], tuple[str, ...]]:
        bullets: list[str] = []
        unexpected: list[str] = []
        for line in self.raw_section_lines(heading):
            if not line.strip():
                continue
            match = _BULLET_PATTERN.fullmatch(line)
            if match is not None:
                bullets.append(match.group(1))
            else:
                unexpected.append(line)
        return tuple(bullets), tuple(unexpected)

    def section_fields(
        self,
        heading: Heading,
    ) -> tuple[dict[str, str], tuple[str, ...], tuple[str, ...]]:
        fields: dict[str, str] = {}
        duplicates: list[str] = []
        unexpected: list[str] = []
        for line in self.section_lines(heading):
            if not line.strip():
                continue
            match = _FIELD_PATTERN.fullmatch(line)
            if match is None:
                unexpected.append(line)
                continue
            name, value = match.groups()
            if name in fields:
                duplicates.append(name)
            fields[name] = value.strip()
        return fields, tuple(duplicates), tuple(unexpected)


def _read(root: Path, relative_path: str, errors: list[str]) -> str:
    path = root / relative_path
    if not path.is_file():
        errors.append(f"missing artifact: {relative_path}")
        return ""
    return path.read_text(encoding="utf-8")


def _require(text: str, markers: tuple[str, ...], label: str, errors: list[str]) -> None:
    for marker in markers:
        if marker not in text:
            errors.append(f"{label} missing: {marker}")


def _require_item_shape(
    text: str,
    label: str,
    errors: list[str],
    *,
    expected_status: str,
    expected_type: str,
    expected_reference: str,
) -> Document:
    document = Document(text)
    if len(document.titles) != 1 or document.titles[0][0] != 0:
        errors.append(
            f"{label} requires exactly one level-1 title at document start: "
            f"{document.titles!r}"
        )
    unexpected_preamble = document.unexpected_preamble_lines()
    if unexpected_preamble:
        errors.append(
            f"{label} metadata preamble contains non-field structure: "
            f"{unexpected_preamble!r}"
        )
    expected_fields = {
        "Status": expected_status,
        "Type": expected_type,
        "Provider": "file",
        "Provider Reference": expected_reference,
        "Completion": "direct-main",
    }
    for name, expected in expected_fields.items():
        actual = document.fields.get(name)
        if actual != expected:
            errors.append(f"{label} field {name} expected {expected!r}, got {actual!r}")
    for name in sorted(document.duplicate_fields):
        errors.append(f"{label} duplicate metadata field: {name}")
    for title in _REQUIRED_ITEM_SECTIONS:
        if document.find_heading(title, level=2, parents=()) is None:
            errors.append(f"{label} missing level-2 section: {title}")
    if "TODO" in text or "<!--" in text:
        errors.append(f"{label} retained template guidance")
    return document


def _require_user_action_hierarchy(
    document: Document,
    label: str,
    errors: list[str],
) -> dict[str, Heading]:
    user_action = document.find_heading("User Action Required", level=2, parents=())
    if user_action is None:
        errors.append(f"{label} missing level-2 User Action Required section")
        return {}
    subsections: dict[str, Heading] = {}
    for title in _USER_ACTION_SUBSECTIONS:
        heading = document.find_heading(
            title,
            level=3,
            parents=("User Action Required",),
        )
        if heading is None:
            errors.append(f"{label} missing User Action Required subsection: {title}")
        else:
            subsections[title] = heading
            if not document.section_substantive_text(heading):
                errors.append(f"{label} empty User Action Required subsection: {title}")
    return subsections


def _validate_governed_item(document: Document, errors: list[str]) -> None:
    label = "governed item"
    subsections = _require_user_action_hierarchy(document, label, errors)
    governed = document.find_heading(
        "Governed Canonical Sources",
        level=3,
        parents=("User Action Required",),
    )
    dependent = document.find_heading(
        "Allowed Dependent Artifacts",
        level=3,
        parents=("User Action Required",),
    )
    question = subsections.get("Question for the User")
    if governed is None:
        errors.append("governed item missing classified Governed Canonical Sources section")
    if dependent is None:
        errors.append("governed item missing classified Allowed Dependent Artifacts section")
    if governed is not None:
        actual_governed, unexpected_governed = document.section_manifest(governed)
        if unexpected_governed:
            errors.append(
                "governed item canonical sources contain unclassified content: "
                f"{unexpected_governed!r}"
            )
        if actual_governed != _GOVERNED_SOURCES:
            errors.append(
                "governed item canonical sources differ from exact approved manifest: "
                f"{actual_governed!r}"
            )
    if dependent is not None:
        actual_dependents, unexpected_dependents = document.section_manifest(dependent)
        if unexpected_dependents:
            errors.append(
                "governed item dependent artifacts contain unclassified content: "
                f"{unexpected_dependents!r}"
            )
        if actual_dependents != _DEPENDENT_ARTIFACTS:
            errors.append(
                "governed item dependent artifacts differ from exact approved manifest: "
                f"{actual_dependents!r}"
            )
    if governed is not None and question is not None and governed.line > question.line:
        errors.append("governed manifest appears after the approval question")
    if dependent is not None and question is not None and dependent.line > question.line:
        errors.append("dependent manifest appears after the approval question")
    resolution = subsections.get("Resolution")
    if resolution is not None:
        fields, duplicates, unexpected = document.section_fields(resolution)
        expected_fields = {
            "Answer": "Approved.",
            "User wording": "approved",
            "Date": "2026-07-21",
            "Provenance": "user-message:thread-123/message-456",
        }
        if fields != expected_fields:
            errors.append(
                "governed item resolution fields differ from exact approval evidence: "
                f"{fields!r}"
            )
        if duplicates:
            errors.append(f"governed item resolution has duplicate fields: {duplicates!r}")
        if unexpected:
            errors.append(f"governed item resolution has unclassified content: {unexpected!r}")


def _validate(root: Path) -> list[str]:
    errors: list[str] = []
    ready_path = "backlog/analysis-backlog/design-parser-boundary.md"
    ready = _read(root, ready_path, errors)
    ready_document = _require_item_shape(
        ready,
        "ready item",
        errors,
        expected_status="Ready",
        expected_type="Analysis",
        expected_reference=ready_path,
    )
    _require(ready, ("parser boundary",), "ready item", errors)
    if ready_document.find_heading("User Action Required", level=2, parents=()) is not None:
        errors.append("ready technical uncertainty became User Action Required")

    forbidden_context_item = root / "backlog/feature-backlog/context-only-request.md"
    if forbidden_context_item.exists():
        errors.append("context-only Source Evidence created an item")

    user_action_path = "backlog/user-action-required/publish-release.md"
    user_action = _read(root, user_action_path, errors)
    user_action_document = _require_item_shape(
        user_action,
        "user-action item",
        errors,
        expected_status="User Action Required",
        expected_type="Feature",
        expected_reference=user_action_path,
    )
    user_action_sections = _require_user_action_hierarchy(
        user_action_document,
        "user-action item",
        errors,
    )
    resolution = user_action_sections.get("Resolution")
    if resolution is not None and user_action_document.section_text(resolution) != "Pending":
        errors.append("user-action item resolution is not exactly Pending")

    holding_path = "backlog/holding/deferred-dashboard.md"
    holding = _read(root, holding_path, errors)
    holding_document = _require_item_shape(
        holding,
        "holding item",
        errors,
        expected_status="Holding",
        expected_type="Holding",
        expected_reference=holding_path,
    )
    _require(holding, ("next planning cycle", "resumption"), "holding item", errors)
    if holding_document.find_heading("User Action Required", level=2, parents=()) is not None:
        errors.append("Holding item invented a user question")

    series_index = _read(root, "backlog/feature-backlog/import-series/index.md", errors)
    series_path = "backlog/feature-backlog/import-series/phase-one.md"
    series_child = _read(root, series_path, errors)
    series_document = _require_item_shape(
        series_child,
        "series child",
        errors,
        expected_status="Ready",
        expected_type="Feature",
        expected_reference=series_path,
    )
    _require(series_index, ("phase-one.md",), "series index", errors)
    if series_document.fields.get("Series") != "backlog/feature-backlog/import-series/index.md":
        errors.append("series child missing exact Series metadata")

    governed_path = "backlog/feature-backlog/governed-definition-update.md"
    governed = _read(root, governed_path, errors)
    governed_document = _require_item_shape(
        governed,
        "governed item",
        errors,
        expected_status="Ready",
        expected_type="Feature",
        expected_reference=governed_path,
    )
    _validate_governed_item(governed_document, errors)

    checker = _read(root, "checker-approval.yaml", errors)
    _require(
        checker,
        ("definition_scope: skills/**", "derived operational evidence"),
        "checker widening fixture",
        errors,
    )

    result = _read(root, "eval-result.md", errors)
    _require(result, _REQUIRED_EVIDENCE, "evaluation result", errors)
    _require(
        result,
        (
            "See the conversation above",
            "skills/unapproved/SKILL.md",
            "derived operational evidence",
            "cannot create or widen approval",
        ),
        "rejection evidence",
        errors,
    )
    return errors


def _write_valid_workspace(root: Path) -> None:
    def item(
        title: str,
        status: str,
        item_type: str,
        provider_reference: str,
        context: str,
        source_evidence: str,
        open_questions: str,
        extra: str = "",
        series: str = "",
        notes: str | None = "None.",
    ) -> str:
        series_field = f"Series: {series}\n\n" if series else ""
        notes_section = f"\n## Notes\n\n{notes}\n" if notes is not None else "\n"
        return f"""# {title}

Status: {status}

Type: {item_type}

Provider: file

Provider Reference: {provider_reference}

Completion: direct-main

{series_field}## Summary

Deliver the requested outcome.

## Context

{context}

## Source Evidence

{source_evidence}

## Requirements

- Deliver the bounded item.

## Acceptance Criteria

- The requested outcome is observable.

## Dependencies

None.

## Verification

- Run the fixture verifier.

## Open Questions

{open_questions}

{extra}{notes_section}"""

    governed_extra = (
        "## User Action Required\n\n"
        "### Governed Canonical Sources\n\n- "
        + "\n- ".join(_GOVERNED_SOURCES)
        + "\n\n### Allowed Dependent Artifacts\n\n- "
        + "\n- ".join(_DEPENDENT_ARTIFACTS)
        + "\n\n### Question for the User\n\nDo you approve the exact manifest?\n\n"
        "### Why User Input Is Required\n\nRepository policy reserves this exact scope decision for the user.\n\n"
        "### Options and Tradeoffs\n\n- Approve the exact manifest or narrow it.\n\n"
        "### Resolution\n\nAnswer: Approved.\nUser wording: approved\nDate: 2026-07-21\n"
        "Provenance: user-message:thread-123/message-456\n\n"
        "### Unattended Work Boundary\n\nDo not mutate governed definitions before approval; read-only discovery may continue.\n"
    )
    outputs = {
        "backlog/analysis-backlog/design-parser-boundary.md": item(
            "Design Parser Boundary",
            "Ready",
            "Analysis",
            "backlog/analysis-backlog/design-parser-boundary.md",
            "Agents own technical discovery.",
            "The user requested this design analysis.",
            "Agents must discover the parser boundary.",
            notes=None,
        ),
        "backlog/user-action-required/publish-release.md": item(
            "Publish Release",
            "User Action Required",
            "Feature",
            "backlog/user-action-required/publish-release.md",
            "Publication requires a user-owned authority grant.",
            "The user requested release preparation.",
            "None.",
            """## User Action Required

### Question for the User

Do you grant external publication authority?

### Why User Input Is Required

Only the user can grant this authority.

### Options and Tradeoffs

- Grant or defer publication.

### Resolution

Pending

### Unattended Work Boundary

Do not publish before resolution.
""",
        ),
        "backlog/holding/deferred-dashboard.md": item(
            "Deferred Dashboard",
            "Holding",
            "Holding",
            "backlog/holding/deferred-dashboard.md",
            "The user deferred this until the next planning cycle. The resumption condition is the next planning review.",
            "The user explicitly deferred the work.",
            "None.",
        ),
        "backlog/feature-backlog/import-series/index.md": """# Import Series

- [Phase One](phase-one.md)
""",
        "backlog/feature-backlog/import-series/phase-one.md": item(
            "Phase One",
            "Ready",
            "Feature",
            "backlog/feature-backlog/import-series/phase-one.md",
            "This is the first independently runnable phase.",
            "The user requested the related series.",
            "None.",
            series="backlog/feature-backlog/import-series/index.md",
        ),
        "backlog/feature-backlog/governed-definition-update.md": item(
            "Governed Definition Update",
            "Ready",
            "Feature",
            "backlog/feature-backlog/governed-definition-update.md",
            "The exact governed scope is approved.",
            "The user approved the exact manifest.",
            "None.",
            governed_extra,
        ),
        "checker-approval.yaml": """# derived operational evidence only; not approval authority
definition_scope: skills/**
""",
        "eval-result.md": "\n".join(_REQUIRED_EVIDENCE)
        + "\nSee the conversation above was rejected.\n"
        "skills/unapproved/SKILL.md was rejected.\n"
        "Checker YAML is derived operational evidence and cannot create or widen approval.\n",
    }
    for relative_path, content in outputs.items():
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def _expect_governed_rejection(
    root: Path,
    original: str,
    changed: str,
    expected_fragment: str,
    label: str,
    errors: list[str],
) -> None:
    path = root / "backlog/feature-backlog/governed-definition-update.md"
    path.write_text(changed, encoding="utf-8")
    validation = _validate(root)
    if not any(expected_fragment in error for error in validation):
        errors.append(f"self-test did not reject {label}: {validation!r}")
    path.write_text(original, encoding="utf-8")


def _self_test() -> list[str]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as temporary_directory:
        root = Path(temporary_directory)
        _write_valid_workspace(root)
        errors.extend(f"valid fixture: {error}" for error in _validate(root))

        context_item = root / "backlog/feature-backlog/context-only-request.md"
        context_item.parent.mkdir(parents=True, exist_ok=True)
        context_item.write_text("## Source Evidence\n\nSee the conversation above.\n", encoding="utf-8")
        if "context-only Source Evidence created an item" not in _validate(root):
            errors.append("self-test did not reject context-only source evidence")
        context_item.unlink()

        governed_path = root / "backlog/feature-backlog/governed-definition-update.md"
        original = governed_path.read_text(encoding="utf-8")
        _expect_governed_rejection(
            root,
            original,
            original.replace(_GOVERNED_SOURCES[0], "skills/unapproved/SKILL.md", 1),
            "canonical sources differ",
            "missing and extra governed source",
            errors,
        )
        _expect_governed_rejection(
            root,
            original,
            original.replace("- " + _GOVERNED_SOURCES[0] + "\n", "", 1),
            "canonical sources differ",
            "missing governed source",
            errors,
        )
        _expect_governed_rejection(
            root,
            original,
            original.replace(_GOVERNED_SOURCES[0], "skills/**", 1),
            "canonical sources differ",
            "wildcard governed source",
            errors,
        )
        _expect_governed_rejection(
            root,
            original,
            original.replace(
                "- " + _GOVERNED_SOURCES[0],
                "- " + _DEPENDENT_ARTIFACTS[0],
                1,
            ),
            "canonical sources differ",
            "dependent artifact misclassified as governed",
            errors,
        )
        _expect_governed_rejection(
            root,
            original,
            original.replace(
                "- " + _GOVERNED_SOURCES[-1],
                "- " + _GOVERNED_SOURCES[-1] + "\n  - skills/unapproved/SKILL.md",
                1,
            ),
            "canonical sources contain unclassified content",
            "nested governed path",
            errors,
        )
        _expect_governed_rejection(
            root,
            original,
            original.replace(
                "- " + _GOVERNED_SOURCES[-1],
                "- " + _GOVERNED_SOURCES[-1] + "\nskills/unapproved/SKILL.md",
                1,
            ),
            "canonical sources contain unclassified content",
            "governed prose path",
            errors,
        )
        _expect_governed_rejection(
            root,
            original,
            original.replace(
                "- " + _DEPENDENT_ARTIFACTS[-1],
                "- " + _DEPENDENT_ARTIFACTS[-1] + "\n  - skills/unapproved/SKILL.md",
                1,
            ),
            "dependent artifacts contain unclassified content",
            "nested dependent path",
            errors,
        )
        _expect_governed_rejection(
            root,
            original,
            original.replace(
                "- " + _DEPENDENT_ARTIFACTS[-1],
                "- " + _DEPENDENT_ARTIFACTS[-1] + "\nskills/unapproved/SKILL.md",
                1,
            ),
            "dependent artifacts contain unclassified content",
            "dependent prose path",
            errors,
        )
        for fence_open, fence_close in (("```text", "```"), ("~~~text", "~~~")):
            _expect_governed_rejection(
                root,
                original,
                original.replace(
                    "- " + _GOVERNED_SOURCES[-1],
                    "- "
                    + _GOVERNED_SOURCES[-1]
                    + f"\n{fence_open}\n- skills/unapproved/SKILL.md\n{fence_close}",
                    1,
                ),
                "canonical sources contain unclassified content",
                f"governed path hidden in {fence_open[:3]} fence",
                errors,
            )
        governed_block = "- " + "\n- ".join(_GOVERNED_SOURCES)
        dependent_block = "- " + "\n- ".join(_DEPENDENT_ARTIFACTS)
        swapped = original.replace(governed_block, "SWAP-GOVERNED", 1)
        swapped = swapped.replace(dependent_block, governed_block, 1)
        swapped = swapped.replace("SWAP-GOVERNED", dependent_block, 1)
        _expect_governed_rejection(
            root,
            original,
            swapped,
            "canonical sources differ",
            "swapped governed and dependent classifications",
            errors,
        )
        _expect_governed_rejection(
            root,
            original,
            original.replace("### Why User Input Is Required", "#### Why User Input Is Required", 1),
            "missing User Action Required subsection",
            "incomplete User Action Required hierarchy",
            errors,
        )
        _expect_governed_rejection(
            root,
            original,
            original.replace(
                "Answer: Approved.",
                "Answer: Declined.\nExplanation: Answer: Approved.",
                1,
            ),
            "resolution fields differ from exact approval evidence",
            "contradictory governed resolution",
            errors,
        )
        _expect_governed_rejection(
            root,
            original,
            original.replace(
                "Answer: Approved.",
                "Answer: Declined.\nAnswer: Approved.",
                1,
            ),
            "resolution has duplicate fields",
            "duplicate governed resolution field",
            errors,
        )

        user_action_path = root / "backlog/user-action-required/publish-release.md"
        user_action_original = user_action_path.read_text(encoding="utf-8")
        incomplete_user_action = user_action_original
        for evidence in (
            "Do you grant external publication authority?",
            "Only the user can grant this authority.",
            "- Grant or defer publication.",
            "Do not publish before resolution.",
        ):
            incomplete_user_action = incomplete_user_action.replace(evidence, "", 1)
        user_action_path.write_text(incomplete_user_action, encoding="utf-8")
        incomplete_errors = _validate(root)
        if not any("empty User Action Required subsection" in error for error in incomplete_errors):
            errors.append("self-test accepted empty User Action Required evidence")
        heading_only_user_action = user_action_original
        for evidence in (
            "Do you grant external publication authority?",
            "Only the user can grant this authority.",
            "- Grant or defer publication.",
            "Do not publish before resolution.",
        ):
            heading_only_user_action = heading_only_user_action.replace(
                evidence,
                "#### Placeholder",
                1,
            )
        user_action_path.write_text(heading_only_user_action, encoding="utf-8")
        heading_only_errors = _validate(root)
        if not any("empty User Action Required subsection" in error for error in heading_only_errors):
            errors.append("self-test accepted heading-only User Action Required evidence")
        user_action_path.write_text(user_action_original, encoding="utf-8")

        ready_path = root / "backlog/analysis-backlog/design-parser-boundary.md"
        ready_original = ready_path.read_text(encoding="utf-8")
        ready_path.write_text(
            ready_original.replace("Status: Ready", "Status: Blocked", 1)
            + "\n## Notes\n\nMisleading narrative says Status: Ready.\n",
            encoding="utf-8",
        )
        lifecycle_errors = _validate(root)
        if not any("field Status expected 'Ready', got 'Blocked'" in error for error in lifecycle_errors):
            errors.append("self-test did not reject misleading lifecycle text")
        ready_path.write_text(ready_original, encoding="utf-8")

        ready_path.write_text(
            ready_original.replace("# Design Parser Boundary\n\n", "", 1),
            encoding="utf-8",
        )
        missing_title_errors = _validate(root)
        if not any("requires exactly one level-1 title at document start" in error for error in missing_title_errors):
            errors.append("self-test accepted a missing level-1 title")
        ready_path.write_text(
            ready_original.replace(
                "# Design Parser Boundary\n\n",
                "# Design Parser Boundary\n\n# Duplicate Title\n\n",
                1,
            ),
            encoding="utf-8",
        )
        duplicate_title_errors = _validate(root)
        if not any("requires exactly one level-1 title at document start" in error for error in duplicate_title_errors):
            errors.append("self-test accepted duplicate level-1 titles")
        ready_path.write_text(
            ready_original.replace("Status: Ready", "### Nested Metadata\n\nStatus: Ready", 1),
            encoding="utf-8",
        )
        nested_metadata_errors = _validate(root)
        if not any("metadata preamble contains non-field structure" in error for error in nested_metadata_errors):
            errors.append("self-test accepted metadata nested beneath another heading")
        ready_path.write_text(ready_original, encoding="utf-8")

        metadata_start = ready_original.index("Status: Ready")
        metadata_end = ready_original.index("## Summary")
        fenced_metadata = (
            ready_original[:metadata_start]
            + "```text\n"
            + ready_original[metadata_start:metadata_end]
            + "```\n\n"
            + ready_original[metadata_end:]
        )
        ready_path.write_text(fenced_metadata, encoding="utf-8")
        fenced_metadata_errors = _validate(root)
        if not any("field Status expected 'Ready', got None" in error for error in fenced_metadata_errors):
            errors.append("self-test accepted lifecycle metadata inside a code fence")
        ready_path.write_text(
            ready_original.replace("## Summary", "```markdown\n## Summary\n```", 1),
            encoding="utf-8",
        )
        fenced_heading_errors = _validate(root)
        if not any("missing level-2 section: Summary" in error for error in fenced_heading_errors):
            errors.append("self-test accepted a required heading inside a code fence")
        for fence in ("```text~", "~~~text`~"):
            ready_path.write_text(
                ready_original[:metadata_start]
                + fence
                + "\n"
                + ready_original[metadata_start:],
                encoding="utf-8",
            )
            unclosed_fence_errors = _validate(root)
            if not any(
                "field Status expected 'Ready', got None" in error
                for error in unclosed_fence_errors
            ):
                errors.append(
                    "self-test accepted metadata inside an unclosed fence with info string: "
                    f"{fence}"
                )
        ready_path.write_text(ready_original, encoding="utf-8")

        governed_path.write_text(
            original.replace(
                "- " + _GOVERNED_SOURCES[-1],
                "- " + _GOVERNED_SOURCES[-1] + "\n- skills/unapproved/SKILL.md",
                1,
            ),
            encoding="utf-8",
        )
        widening_errors = _validate(root)
        if not any("canonical sources differ" in error for error in widening_errors):
            errors.append("self-test let checker YAML widen governed approval")
    return errors


def _main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors = _self_test() if args.self_test else _validate(Path.cwd())
    if errors:
        print("\n".join(errors))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
