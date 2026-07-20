#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Validates completed Dev Artifact Reviewer checklists against their canonical source sequences.
# Governing design: evals/agent-tests/dev-artifact-reviewer/skills/dev-artifact-reviewer-suite-contract/SKILL.md
# Governing test plan: backlog/feature-backlog/agent-skill-lifecycle/preserve-canonical-review-checklists.md

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import re
from pathlib import Path
from typing import Optional, Sequence


_QUESTION_PREFIX = "- Question: "
_FIELD_PATTERN = re.compile(r"^- ([A-Z][^:]*):\s*(.*)$")
_RECORD_HEADING_PATTERN = re.compile(r"^## (Q\d{3})\s*$", re.MULTILINE)
_NEXT_HEADING_PATTERN = re.compile(r"^##\s+", re.MULTILINE)
_VALID_STATUSES = frozenset({"pass", "fail", "question", "n/a"})
_REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


@dataclasses.dataclass(frozen=True)
class CanonicalChecklist:
    """Represent the source-owned completion fields and objective question sequence."""

    path: str
    sha256: str
    fields: tuple[str, ...]
    questions: tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class ValidationResult:
    """Report one source-to-completed comparison without mutating either artifact."""

    canonical: str
    canonical_sha256: str
    completed: str
    completed_sha256: str
    expected_count: int
    completed_count: int
    valid: bool
    errors: tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class _CompletedRecord:
    identifier: str
    fields: tuple[tuple[str, str], ...]


def load_canonical_checklist(
    path: Path, repository_root: Optional[Path] = None
) -> CanonicalChecklist:
    """Load one canonical Markdown checklist.

    The canonical source owns both the Completion Format field names and every
    objective Question line. A malformed or empty source raises ValueError so
    callers cannot treat unavailable authority as a passing checklist.
    """
    root = (repository_root or _REPOSITORY_ROOT).resolve()
    relative = _canonical_relative_path(path, root)
    source_bytes = path.read_bytes()
    text = source_bytes.decode("utf-8")
    fields = _completion_fields(text)
    questions = _objective_questions(text)
    if not fields:
        raise ValueError(f"canonical checklist has no Completion Format fields: {path}")
    if not questions:
        raise ValueError(f"canonical checklist has no objective questions: {path}")
    if len(questions) != len(set(questions)):
        raise ValueError(f"canonical checklist repeats an objective question: {path}")
    return CanonicalChecklist(
        relative.as_posix(), hashlib.sha256(source_bytes).hexdigest(), fields, questions
    )


def validate_completed_checklist(
    canonical_path: Path,
    completed_path: Path,
    repository_root: Optional[Path] = None,
) -> ValidationResult:
    """Compare one completed checklist with one canonical source.

    Questions must appear exactly once in source order under sequential Q001
    record headings. Every record must retain the source-defined Completion
    Format fields with non-empty values and a canonical status. Content after
    the last record may summarize findings without affecting the comparison.
    """
    root = (repository_root or _REPOSITORY_ROOT).resolve()
    canonical = load_canonical_checklist(canonical_path, root)
    completed_bytes = completed_path.read_bytes()
    completed_text = completed_bytes.decode("utf-8")
    completed_relative = _repository_relative_path(completed_path, root, "completed checklist")
    records = _completed_records(completed_text)
    errors: list[str] = []
    expected_identifiers = tuple(f"Q{index:03d}" for index in range(1, len(canonical.questions) + 1))
    observed_identifiers = tuple(record.identifier for record in records)
    if observed_identifiers != expected_identifiers[: len(records)] or len(records) != len(
        expected_identifiers
    ):
        errors.append(
            "completed identifiers must be "
            + ", ".join(expected_identifiers)
            + "; found "
            + (", ".join(observed_identifiers) or "none")
        )
    if len(records) != len(canonical.questions):
        errors.append(
            f"expected {len(canonical.questions)} completed questions, found {len(records)}"
        )
    if _non_record_section_interrupts_completion(completed_text, len(canonical.questions)):
        errors.append("a non-record section appears before all canonical records")
    for index, record in enumerate(records):
        expected_identifier = f"Q{index + 1:03d}"
        field_values: dict[str, str] = {}
        duplicate_fields: set[str] = set()
        for field, value in record.fields:
            if field in field_values:
                duplicate_fields.add(field)
            else:
                field_values[field] = value
        for field in sorted(duplicate_fields):
            errors.append(f"{expected_identifier} repeats field {field}")
        for field in canonical.fields:
            if not field_values.get(field, "").strip():
                errors.append(f"{expected_identifier} must complete field {field}")
        status = field_values.get("Status", "").strip()
        if status and status not in _VALID_STATUSES:
            errors.append(f"{expected_identifier} has invalid Status {status!r}")
        if index < len(canonical.questions):
            observed_question = field_values.get("Question", "")
            expected_question = canonical.questions[index]
            if observed_question != expected_question:
                errors.append(
                    f"{expected_identifier} wording differs from canonical source: "
                    f"expected {expected_question!r}, found {observed_question!r}"
                )
    return ValidationResult(
        canonical=canonical.path,
        canonical_sha256=canonical.sha256,
        completed=completed_relative.as_posix(),
        completed_sha256=hashlib.sha256(completed_bytes).hexdigest(),
        expected_count=len(canonical.questions),
        completed_count=len(records),
        valid=not errors,
        errors=tuple(errors),
    )


def validate_checklist_pairs(
    pairs: Sequence[tuple[Path, Path]],
    repository_root: Optional[Path] = None,
) -> tuple[ValidationResult, ...]:
    """Validate generic and specialized checklist pairs independently in caller order."""
    return tuple(
        validate_completed_checklist(canonical, completed, repository_root)
        for canonical, completed in pairs
    )


def _canonical_relative_path(path: Path, repository_root: Path) -> Path:
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(repository_root)
    except ValueError as error:
        raise ValueError(f"canonical checklist is outside the repository: {path}") from error
    parts = relative.parts
    if (
        len(parts) != 4
        or parts[0] != "skills"
        or not parts[1].startswith("review-")
        or parts[2] != "references"
        or not parts[3].startswith("review-checklist-")
        or not parts[3].endswith(".md")
        or not resolved.is_file()
    ):
        raise ValueError(f"canonical checklist is not a repository review source: {relative}")
    return relative


def _repository_relative_path(path: Path, repository_root: Path, label: str) -> Path:
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(repository_root)
    except ValueError as error:
        raise ValueError(f"{label} is outside the repository: {path}") from error
    if not resolved.is_file():
        raise ValueError(f"{label} is not a file: {relative}")
    return relative


def _completion_fields(text: str) -> tuple[str, ...]:
    heading = "## Completion Format"
    start = text.find(heading)
    if start < 0:
        return ()
    body_start = start + len(heading)
    next_heading = _NEXT_HEADING_PATTERN.search(text, body_start)
    section = text[body_start : next_heading.start() if next_heading else len(text)]
    fields: list[str] = []
    for line in section.splitlines():
        match = _FIELD_PATTERN.fullmatch(line)
        if match:
            fields.append(match.group(1))
    return tuple(fields)


def _objective_questions(text: str) -> tuple[str, ...]:
    completion_heading = "## Completion Format"
    completion_start = text.find(completion_heading)
    search_start = completion_start + len(completion_heading) if completion_start >= 0 else 0
    first_question_heading = _NEXT_HEADING_PATTERN.search(text, search_start)
    question_text = text[first_question_heading.start() :] if first_question_heading else ""
    return tuple(
        line[len(_QUESTION_PREFIX) :]
        for line in question_text.splitlines()
        if line.startswith(_QUESTION_PREFIX)
    )


def _completed_records(text: str) -> tuple[_CompletedRecord, ...]:
    headings = tuple(_RECORD_HEADING_PATTERN.finditer(text))
    records: list[_CompletedRecord] = []
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        section = text[heading.end() : end]
        next_non_record_heading = _NEXT_HEADING_PATTERN.search(section)
        if next_non_record_heading:
            section = section[: next_non_record_heading.start()]
        fields = tuple(
            (match.group(1), match.group(2))
            for line in section.splitlines()
            if (match := _FIELD_PATTERN.fullmatch(line)) is not None
        )
        records.append(_CompletedRecord(heading.group(1), fields))
    return tuple(records)


def _non_record_section_interrupts_completion(text: str, expected_count: int) -> bool:
    completed_records = 0
    for heading in re.finditer(r"^## ([^\n]+)\s*$", text, re.MULTILINE):
        if re.fullmatch(r"Q\d{3}", heading.group(1)):
            completed_records += 1
            continue
        if 0 < completed_records < expected_count:
            return True
    return False


def _argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare completed review checklists with canonical Markdown sources."
    )
    parser.add_argument(
        "--pair",
        action="append",
        nargs=2,
        metavar=("CANONICAL", "COMPLETED"),
        required=True,
        help="Canonical source and its independently completed checklist.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run deterministic checklist validation and emit one compact JSON result."""
    arguments = _argument_parser().parse_args(argv)
    pairs = tuple((Path(canonical), Path(completed)) for canonical, completed in arguments.pair)
    results = validate_checklist_pairs(pairs)
    print(
        json.dumps(
            {
                "valid": all(result.valid for result in results),
                "checklists": [dataclasses.asdict(result) for result in results],
            },
            sort_keys=True,
        )
    )
    return 0 if all(result.valid for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
