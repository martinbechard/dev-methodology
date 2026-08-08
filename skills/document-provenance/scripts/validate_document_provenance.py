#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Validates governed Markdown and HTML creation provenance against runtime or historical evidence rules.

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Mapping, Sequence


_SUCCESS_EXIT_CODE = 0
_VALIDATION_ERROR_EXIT_CODE = 1
_USAGE_ERROR_EXIT_CODE = 2
_SUPPORTED_STATES = {"new", "historical"}
_SUPPORTED_MARKDOWN_SUFFIXES = {".md", ".markdown"}
_SUPPORTED_HTML_SUFFIXES = {".html", ".htm"}
_CORE_FIELDS = (
    "Artifact-ID",
    "Created-UTC",
    "Creating-Agent",
    "Runtime",
    "Dispatched-Model",
    "Reasoning-Effort",
    "Task-ID",
)
_EVIDENCE_FIELDS = tuple(f"{field}-Evidence" for field in _CORE_FIELDS)
_REQUIRED_FIELDS = _CORE_FIELDS + _EVIDENCE_FIELDS
_RUNTIME_EVIDENCE = "runtime-supplied"
_HISTORICAL_UNKNOWN = "historical-unknown"
_ALLOWED_HISTORICAL_EVIDENCE = {
    "Artifact-ID-Evidence": {
        _RUNTIME_EVIDENCE,
        "retained-task-evidence",
        "retained-rollout-evidence",
        "migration-assigned",
    },
    "Created-UTC-Evidence": {
        _RUNTIME_EVIDENCE,
        "retained-task-evidence",
        "retained-rollout-evidence",
        "git-derived",
        _HISTORICAL_UNKNOWN,
    },
    "Creating-Agent-Evidence": {
        _RUNTIME_EVIDENCE,
        "retained-task-evidence",
        "retained-rollout-evidence",
        _HISTORICAL_UNKNOWN,
    },
    "Runtime-Evidence": {
        _RUNTIME_EVIDENCE,
        "retained-task-evidence",
        "retained-rollout-evidence",
        _HISTORICAL_UNKNOWN,
    },
    "Dispatched-Model-Evidence": {
        _RUNTIME_EVIDENCE,
        "retained-task-evidence",
        "retained-rollout-evidence",
        _HISTORICAL_UNKNOWN,
    },
    "Reasoning-Effort-Evidence": {
        _RUNTIME_EVIDENCE,
        "retained-task-evidence",
        "retained-rollout-evidence",
        _HISTORICAL_UNKNOWN,
    },
    "Task-ID-Evidence": {
        _RUNTIME_EVIDENCE,
        "retained-task-evidence",
        "retained-rollout-evidence",
        _HISTORICAL_UNKNOWN,
    },
}
_COMMENT_PATTERN = re.compile(r"<!--(?P<body>.*?)-->", re.DOTALL)
_FIELD_PATTERN = re.compile(r"^(?P<label>[A-Za-z][A-Za-z0-9-]*):[ \t]*(?P<value>.*)$")
_DOCTYPE_PATTERN = re.compile(r"\A\ufeff?\s*(?P<doctype><!doctype\s+html\s*>)", re.IGNORECASE)
_FRONTMATTER_OPEN_PATTERN = re.compile(r"\A---[ \t]*(?:\r?\n|\Z)")
_FRONTMATTER_DELIMITER_PATTERN = re.compile(r"^---[ \t]*\r?$", re.MULTILINE)
_BLANK_LINES_PATTERN = re.compile(r"(?:[ \t]*(?:\r\n|\n|\r))*")
_UTC_TIMESTAMP_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|\+00:00)$"
)
_ARTIFACT_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{7,199}$")
_PLACEHOLDER_PATTERN = re.compile(
    r"(?:\{\{.*?\}\}|<[^>]+>|\b(?:todo|tbd|placeholder|replace[-_ ]?me|unknown|n/?a)\b)",
    re.IGNORECASE,
)
_INFERRED_PROFILE_PATTERN = re.compile(
    r"(?:current[-_ ]?profile|configured[-_ ]?profile|profile[-_ ]?mapping|"
    r"configuration[-_ ]?inferred|self[-_ ]?reported)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ValidationFinding:
    """Identify one deterministic validation failure for one document field.

    Validators return these immutable records so command callers can report the
    exact path, field, and reason without parsing prose from a combined result.
    """

    path: Path
    field: str
    message: str


def load_runtime_envelope(path: Path) -> dict[str, dict[str, str]]:
    """Load runtime-supplied creation records indexed by Artifact-ID.

    Args:
        path: JSON envelope created by the dispatching coordinator or harness.

    Returns:
        A new mapping from each durable artifact identifier to its creation record.

    Raises:
        OSError: The envelope cannot be read.
        ValueError: The envelope shape, fields, values, or identifiers are invalid.
    """

    try:
        envelope = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"runtime envelope is not valid JSON: {error}") from error
    if not isinstance(envelope, dict):
        raise ValueError("runtime envelope must be a JSON object")
    if envelope.get("schema_version") != 1:
        raise ValueError("runtime envelope schema_version must equal 1")
    records = envelope.get("records")
    if not isinstance(records, list):
        raise ValueError("runtime envelope records must be a JSON array")

    indexed: dict[str, dict[str, str]] = {}
    for index, raw_record in enumerate(records):
        if not isinstance(raw_record, dict):
            raise ValueError(f"runtime envelope record {index} must be a JSON object")
        missing = sorted(set(_CORE_FIELDS) - set(raw_record))
        unexpected = sorted(set(raw_record) - set(_CORE_FIELDS))
        if missing:
            raise ValueError(f"runtime envelope record {index} is missing: {', '.join(missing)}")
        if unexpected:
            raise ValueError(f"runtime envelope record {index} has unsupported fields: {', '.join(unexpected)}")
        if any(not isinstance(raw_record[field], str) or not raw_record[field].strip() for field in _CORE_FIELDS):
            raise ValueError(f"runtime envelope record {index} fields must be non-empty strings")

        record = {field: raw_record[field].strip() for field in _CORE_FIELDS}
        artifact_id = record["Artifact-ID"]
        if not _is_valid_artifact_id(artifact_id):
            raise ValueError(f"runtime envelope record {index} has an invalid Artifact-ID")
        if not _is_valid_utc_timestamp(record["Created-UTC"]):
            raise ValueError(f"runtime envelope record {index} has an invalid Created-UTC")
        for field in _CORE_FIELDS:
            if field not in {"Artifact-ID", "Created-UTC"} and _is_placeholder(record[field]):
                raise ValueError(f"runtime envelope record {index} has a placeholder {field}")
            if _INFERRED_PROFILE_PATTERN.search(record[field]):
                raise ValueError(f"runtime envelope record {index} has inferred configuration in {field}")
        if artifact_id in indexed:
            raise ValueError(f"runtime envelope contains duplicate Artifact-ID: {artifact_id}")
        indexed[artifact_id] = record
    return indexed


def validate_document(
    path: Path,
    *,
    state: str,
    copyright_statement: str,
    runtime_envelope: Mapping[str, Mapping[str, str]] | None = None,
) -> list[ValidationFinding]:
    """Validate one explicit governed document without modifying it.

    Args:
        path: Markdown or HTML document selected by the governing project.
        state: Either new for runtime-enveloped content or historical for migration.
        copyright_statement: Exact statement supplied by applicable project authority.
        runtime_envelope: Runtime records required for every new document.

    Returns:
        Exact field findings. An empty list means the document conforms.

    Raises:
        ValueError: The caller supplies an unsupported validation state or empty copyright.
    """

    if state not in _SUPPORTED_STATES:
        raise ValueError(f"state must be one of: {', '.join(sorted(_SUPPORTED_STATES))}")
    if not copyright_statement.strip():
        raise ValueError("copyright_statement must be non-empty")

    suffix = path.suffix.lower()
    if suffix not in _SUPPORTED_MARKDOWN_SUFFIXES | _SUPPORTED_HTML_SUFFIXES:
        return [
            _finding(
                path,
                "Format",
                "unsupported governed document format; use an authorized sidecar or report it",
            )
        ]
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        return [_finding(path, "Document", f"cannot read UTF-8 document: {error}")]

    findings: list[ValidationFinding] = []
    candidates = _provenance_comments(
        text,
        copyright_statement,
        skip_markdown_fences=suffix in _SUPPORTED_MARKDOWN_SUFFIXES,
    )
    if not candidates:
        findings.append(_finding(path, "Provenance", "creation provenance HTML comment is missing"))
        if state == "new" and runtime_envelope is None:
            findings.append(_finding(path, "Runtime-Envelope", "new documents require a runtime-supplied envelope"))
        return findings
    if len(candidates) > 1:
        findings.append(_finding(path, "Provenance", "multiple creation provenance blocks are not allowed"))
    provenance = candidates[0]

    if suffix in _SUPPORTED_MARKDOWN_SUFFIXES:
        findings.extend(_validate_markdown_placement(path, text, provenance))
    else:
        findings.extend(_validate_html_placement(path, text, provenance))

    values, block_findings = _parse_provenance_block(path, provenance.group("body"), copyright_statement)
    findings.extend(block_findings)
    findings.extend(_validate_field_values(path, values, state))

    if state == "new":
        findings.extend(_compare_runtime_envelope(path, values, runtime_envelope))
    return findings


def main(argv: Sequence[str] | None = None) -> int:
    """Validate an explicit bounded set of new and historical documents.

    The command reads only the listed files and optional JSON envelope. It emits
    one path-and-field finding per line and returns a failing status for invalid
    documents, envelope failures, or invalid arguments.
    """

    parser = argparse.ArgumentParser(description="Validate governed document creation provenance.")
    parser.add_argument("--copyright", required=True, help="Exact project-authorized copyright statement")
    parser.add_argument("--envelope", type=Path, help="Runtime-supplied JSON envelope for new documents")
    parser.add_argument("--new", action="append", default=[], type=Path, metavar="PATH")
    parser.add_argument("--historical", action="append", default=[], type=Path, metavar="PATH")
    args = parser.parse_args(argv)

    assignments = [(path, "new") for path in args.new] + [(path, "historical") for path in args.historical]
    if not assignments:
        print("at least one --new or --historical path is required", file=sys.stderr)
        return _USAGE_ERROR_EXIT_CODE
    states_by_path: dict[Path, str] = {}
    for path, state in assignments:
        if path in states_by_path:
            print(f"duplicate document path: {path}", file=sys.stderr)
            return _USAGE_ERROR_EXIT_CODE
        states_by_path[path] = state

    runtime_envelope = None
    if args.envelope is not None:
        try:
            runtime_envelope = load_runtime_envelope(args.envelope)
        except (OSError, ValueError) as error:
            print(f"{args.envelope}: Runtime-Envelope: {error}", file=sys.stderr)
            return _USAGE_ERROR_EXIT_CODE

    findings = [
        finding
        for path, state in assignments
        for finding in validate_document(
            path,
            state=state,
            copyright_statement=args.copyright,
            runtime_envelope=runtime_envelope,
        )
    ]
    if findings:
        for finding in findings:
            print(f"{finding.path}: {finding.field}: {finding.message}")
        return _VALIDATION_ERROR_EXIT_CODE
    print(f"validated {len(assignments)} documents")
    return _SUCCESS_EXIT_CODE


def _finding(path: Path, field: str, message: str) -> ValidationFinding:
    return ValidationFinding(path=path, field=field, message=message)


def _provenance_comments(
    text: str,
    copyright_statement: str,
    *,
    skip_markdown_fences: bool,
) -> list[re.Match[str]]:
    markers = tuple(f"{field}:" for field in _CORE_FIELDS)
    return [
        match
        for match in _COMMENT_PATTERN.finditer(text)
        if (copyright_statement in match.group("body") or any(marker in match.group("body") for marker in markers))
        and (not skip_markdown_fences or not _inside_markdown_fence(text, match.start()))
    ]


def _inside_markdown_fence(text: str, offset: int) -> bool:
    active_marker: str | None = None
    for line in text[:offset].splitlines():
        stripped = line.lstrip()
        if active_marker is None:
            if stripped.startswith("```"):
                active_marker = "```"
            elif stripped.startswith("~~~"):
                active_marker = "~~~"
        elif stripped.startswith(active_marker):
            active_marker = None
    return active_marker is not None


def _validate_markdown_placement(path: Path, text: str, provenance: re.Match[str]) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    frontmatter_end = _markdown_frontmatter_end(text)
    expected_start = _skip_blank_lines(
        text,
        frontmatter_end if frontmatter_end is not None else 0,
    )
    if provenance.start() != expected_start:
        findings.append(
            _finding(
                path,
                "Placement",
                "provenance must be the first construct after YAML front matter, or the first document construct",
            )
        )
    if frontmatter_end is None and _starts_with_frontmatter(text[provenance.end() :].lstrip()):
        findings.append(_finding(path, "Placement", "provenance appears before YAML front matter"))
    return findings


def _validate_html_placement(path: Path, text: str, provenance: re.Match[str]) -> list[ValidationFinding]:
    doctype = _DOCTYPE_PATTERN.match(text)
    if doctype is None:
        return [_finding(path, "Placement", "maintained HTML must start with an HTML doctype before provenance")]
    expected_start = _skip_blank_lines(text, doctype.end("doctype"))
    if provenance.start() != expected_start:
        return [_finding(path, "Placement", "HTML provenance must be the first construct after the doctype")]
    return []


def _markdown_frontmatter_end(text: str) -> int | None:
    if not _starts_with_frontmatter(text):
        return None
    delimiters = list(_FRONTMATTER_DELIMITER_PATTERN.finditer(text))
    if len(delimiters) < 2:
        return None
    return delimiters[1].end()


def _starts_with_frontmatter(text: str) -> bool:
    return _FRONTMATTER_OPEN_PATTERN.match(text) is not None


def _skip_blank_lines(text: str, start: int) -> int:
    """Skip line breaks and whitespace-only lines without consuming opener indentation."""

    match = _BLANK_LINES_PATTERN.match(text, start)
    if match is None:
        return start
    return match.end()


def _parse_provenance_block(
    path: Path,
    body: str,
    copyright_statement: str,
) -> tuple[dict[str, str], list[ValidationFinding]]:
    findings: list[ValidationFinding] = []
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    copyright_count = lines.count(copyright_statement)
    if copyright_count != 1:
        findings.append(_finding(path, "Copyright", "provenance must contain the exact copyright statement once"))

    collected: dict[str, list[str]] = {}
    for line in lines:
        if line == copyright_statement:
            continue
        if line.lower().startswith("copyright"):
            continue
        match = _FIELD_PATTERN.fullmatch(line)
        if match is None:
            findings.append(_finding(path, "Provenance", f"unsupported provenance line: {line}"))
            continue
        label = match.group("label")
        if label not in _REQUIRED_FIELDS:
            findings.append(_finding(path, label, "unsupported provenance field"))
            continue
        collected.setdefault(label, []).append(match.group("value").strip())

    values: dict[str, str] = {}
    for field in _REQUIRED_FIELDS:
        field_values = collected.get(field, [])
        if not field_values:
            findings.append(_finding(path, field, "required provenance field is missing"))
            continue
        if len(field_values) > 1:
            findings.append(_finding(path, field, "provenance field is duplicated"))
        values[field] = field_values[0]
    return values, findings


def _validate_field_values(path: Path, values: Mapping[str, str], state: str) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    artifact_id = values.get("Artifact-ID")
    if artifact_id is not None and not _is_valid_artifact_id(artifact_id):
        findings.append(
            _finding(
                path,
                "Artifact-ID",
                "must be a durable opaque identifier of 8 to 200 safe characters",
            )
        )

    created_utc = values.get("Created-UTC")
    if created_utc is not None:
        if state == "historical" and created_utc == _HISTORICAL_UNKNOWN:
            pass
        elif not _is_valid_utc_timestamp(created_utc):
            findings.append(
                _finding(
                    path,
                    "Created-UTC",
                    "must be an ISO 8601 timestamp with the Z or +00:00 UTC offset",
                )
            )

    for field in _CORE_FIELDS:
        value = values.get(field)
        if value is None:
            continue
        if state == "new" and value == _HISTORICAL_UNKNOWN:
            findings.append(_finding(path, field, "historical-unknown is forbidden for new documents"))
        elif value != _HISTORICAL_UNKNOWN and _is_placeholder(value):
            findings.append(_finding(path, field, "placeholder values are not allowed"))
        if _INFERRED_PROFILE_PATTERN.search(value):
            findings.append(
                _finding(
                    path,
                    field,
                    "current profile or self-reported inference is not execution evidence",
                )
            )

    for core_field, evidence_field in zip(_CORE_FIELDS, _EVIDENCE_FIELDS, strict=True):
        evidence = values.get(evidence_field)
        value = values.get(core_field)
        if evidence is None:
            continue
        if _INFERRED_PROFILE_PATTERN.search(evidence):
            findings.append(_finding(path, evidence_field, "current profile or self-reported inference is forbidden"))
        if state == "new":
            if evidence != _RUNTIME_EVIDENCE:
                findings.append(_finding(path, evidence_field, "new documents require runtime-supplied evidence"))
            continue
        if evidence not in _ALLOWED_HISTORICAL_EVIDENCE[evidence_field]:
            findings.append(_finding(path, evidence_field, "unsupported historical evidence status"))
            continue
        if value == _HISTORICAL_UNKNOWN and evidence != _HISTORICAL_UNKNOWN:
            findings.append(
                _finding(
                    path,
                    evidence_field,
                    "historical-unknown values require matching evidence status",
                )
            )
        if value not in {None, _HISTORICAL_UNKNOWN} and evidence == _HISTORICAL_UNKNOWN:
            findings.append(_finding(path, evidence_field, "a concrete value cannot use historical-unknown evidence"))
    return findings


def _compare_runtime_envelope(
    path: Path,
    values: Mapping[str, str],
    runtime_envelope: Mapping[str, Mapping[str, str]] | None,
) -> list[ValidationFinding]:
    if runtime_envelope is None:
        return [_finding(path, "Runtime-Envelope", "new documents require a runtime-supplied envelope")]
    artifact_id = values.get("Artifact-ID")
    if artifact_id is None or not _is_valid_artifact_id(artifact_id):
        return []
    expected = runtime_envelope.get(artifact_id)
    if expected is None:
        return [_finding(path, "Runtime-Envelope", f"no runtime record exists for Artifact-ID {artifact_id}")]
    return [
        _finding(path, field, "document value does not match the runtime envelope")
        for field in _CORE_FIELDS
        if field in values and values[field] != expected.get(field)
    ]


def _is_valid_artifact_id(value: str) -> bool:
    return _ARTIFACT_ID_PATTERN.fullmatch(value) is not None and not _is_placeholder(value)


def _is_valid_utc_timestamp(value: str) -> bool:
    if _UTC_TIMESTAMP_PATTERN.fullmatch(value) is None:
        return False
    try:
        normalized = value.removesuffix("Z") + "+00:00" if value.endswith("Z") else value
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return False
    return parsed.utcoffset() is not None and parsed.utcoffset().total_seconds() == 0


def _is_placeholder(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized == _HISTORICAL_UNKNOWN:
        return False
    return not normalized or _PLACEHOLDER_PATTERN.search(value) is not None


if __name__ == "__main__":
    raise SystemExit(main())
