#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Validates compact, legacy, and historical document creation provenance.

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Mapping, Sequence


_SUCCESS_EXIT_CODE = 0
_VALIDATION_ERROR_EXIT_CODE = 1
_USAGE_ERROR_EXIT_CODE = 2
_SUPPORTED_ROUTES = {"new", "legacy", "historical"}
_SUPPORTED_MARKDOWN_SUFFIXES = {".md", ".markdown"}
_SUPPORTED_HTML_SUFFIXES = {".html", ".htm"}
_COMPACT_FIELDS = (
    "Artifact-ID",
    "Created-Local",
    "Creating-Agent",
    "Runtime",
    "Dispatched-Model",
    "Reasoning-Effort",
)
_HTML_READER_FIELDS = (
    "Copyright",
    "Created-Local",
    "Creating-Agent",
    "Runtime",
    "Dispatched-Model",
    "Reasoning-Effort",
)
_LEGACY_CORE_FIELDS = (
    "Artifact-ID",
    "Created-UTC",
    "Creating-Agent",
    "Runtime",
    "Dispatched-Model",
    "Reasoning-Effort",
    "Task-ID",
)
_LEGACY_EVIDENCE_FIELDS = tuple(
    f"{field}-Evidence" for field in _LEGACY_CORE_FIELDS
)
_LEGACY_FIELDS = _LEGACY_CORE_FIELDS + _LEGACY_EVIDENCE_FIELDS
_HISTORICAL_FACTS = {
    "Created-UTC",
    "Created-Local",
    "Creating-Agent",
    "Runtime",
    "Dispatched-Model",
    "Reasoning-Effort",
}
_RUNTIME_EVIDENCE = "runtime-supplied"
_HISTORICAL_UNKNOWN = "historical-unknown"
_HISTORICAL_ARTIFACT_ID_EVIDENCE = {
    _RUNTIME_EVIDENCE,
    "retained-task-evidence",
    "retained-rollout-evidence",
    "migration-assigned",
}
_HISTORICAL_FACT_EVIDENCE = {
    "Created-UTC": {
        _RUNTIME_EVIDENCE,
        "retained-task-evidence",
        "retained-rollout-evidence",
        "git-derived",
    },
    "Created-Local": {
        _RUNTIME_EVIDENCE,
        "retained-task-evidence",
        "retained-rollout-evidence",
        "git-derived",
    },
    **{
        field: {
            _RUNTIME_EVIDENCE,
            "retained-task-evidence",
            "retained-rollout-evidence",
        }
        for field in (
            "Creating-Agent",
            "Runtime",
            "Dispatched-Model",
            "Reasoning-Effort",
        )
    },
}
_ALLOWED_LEGACY_EVIDENCE = {
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
    **{
        f"{field}-Evidence": {
            _RUNTIME_EVIDENCE,
            "retained-task-evidence",
            "retained-rollout-evidence",
            _HISTORICAL_UNKNOWN,
        }
        for field in (
            "Creating-Agent",
            "Runtime",
            "Dispatched-Model",
            "Reasoning-Effort",
            "Task-ID",
        )
    },
}
_COMMENT_PATTERN = re.compile(r"<!--(?P<body>.*?)-->", re.DOTALL)
_CORRELATION_PATTERN = re.compile(
    r"<!-- Document-Provenance Artifact-ID: (?P<artifact_id>[^\r\n]+) -->"
)
_FIELD_PATTERN = re.compile(
    r"^(?P<label>[A-Za-z][A-Za-z0-9-]*):[ \t]*(?P<value>.*)$"
)
_DOCTYPE_PATTERN = re.compile(
    r"\A\ufeff?\s*(?P<doctype><!doctype\s+html\s*>)", re.IGNORECASE
)
_FRONTMATTER_OPEN_PATTERN = re.compile(r"\A---[ \t]*(?:\r?\n|\Z)")
_FRONTMATTER_DELIMITER_PATTERN = re.compile(r"^---[ \t]*\r?$", re.MULTILINE)
_BLANK_LINES_PATTERN = re.compile(r"(?:[ \t]*(?:\r\n|\n|\r))*")
_UTC_TIMESTAMP_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|\+00:00)$"
)
_LOCAL_TIMESTAMP_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?"
    r"[+-](?:0\d|1[0-4]):[0-5]\d$"
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
_FORBIDDEN_VISIBLE_METADATA = re.compile(
    r"(?:Task-ID|Artifact-ID|(?:[A-Za-z][A-Za-z0-9-]*)-Evidence|"
    r"historical-unknown|migration-assigned|runtime-supplied|"
    r"retained-(?:task|rollout)-evidence|git-derived)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ValidationFinding:
    """Identify one deterministic validation failure for one document field."""

    path: Path
    field: str
    message: str


@dataclass(frozen=True)
class RuntimeEnvelope:
    """Hold one validated versioned envelope indexed by Artifact-ID."""

    schema_version: int
    records: Mapping[str, Mapping[str, object]]

    def with_records(
        self, records: Mapping[str, Mapping[str, object]]
    ) -> RuntimeEnvelope:
        """Return a test-scoped envelope with the same schema version."""

        return RuntimeEnvelope(self.schema_version, dict(records))


@dataclass
class _HtmlFootnote:
    in_footer: bool
    fields: dict[str, list[str]]
    time_datetimes: dict[str, list[str | None]]
    text_parts: list[str]


class _ProvenanceHtmlParser(HTMLParser):
    """Collect semantic provenance footnotes without changing document HTML."""

    _VOID_ELEMENTS = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.footer_depth = 0
        self._elements: list[str] = []
        self.footnotes: list[_HtmlFootnote] = []
        self._footnote_depth: int | None = None
        self._current: _HtmlFootnote | None = None
        self._field_stack: list[tuple[str, int, list[str]]] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attr_map = dict(attrs)
        if tag not in self._VOID_ELEMENTS:
            self._elements.append(tag)
        if tag == "footer":
            self.footer_depth += 1
        if tag == "p" and "data-document-provenance" in attr_map:
            current = _HtmlFootnote(
                in_footer=self.footer_depth > 0,
                fields={},
                time_datetimes={},
                text_parts=[],
            )
            self.footnotes.append(current)
            self._current = current
            self._footnote_depth = len(self._elements)
            current.fields.setdefault(
                "Footnote-Version", []
            ).append(attr_map.get("data-document-provenance") or "")
        if self._current is None:
            return
        label = attr_map.get("data-provenance-field")
        if label is not None:
            self._field_stack.append((label, len(self._elements), []))
            if tag == "time":
                self._current.time_datetimes.setdefault(label, []).append(
                    attr_map.get("datetime")
                )

    def handle_data(self, data: str) -> None:
        if self._current is None:
            return
        self._current.text_parts.append(data)
        for _, _, parts in self._field_stack:
            parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        depth = len(self._elements)
        while self._field_stack and self._field_stack[-1][1] == depth:
            label, _, parts = self._field_stack.pop()
            if self._current is not None:
                self._current.fields.setdefault(label, []).append(
                    _normalize_text("".join(parts))
                )
        if tag == "p" and self._footnote_depth == depth:
            self._current = None
            self._footnote_depth = None
            self._field_stack.clear()
        if tag == "footer" and self.footer_depth:
            self.footer_depth -= 1
        while self._elements:
            open_tag = self._elements.pop()
            if open_tag == tag:
                break


def load_runtime_envelope(path: Path) -> RuntimeEnvelope:
    """Load and validate a schema-version-1 or schema-version-2 envelope."""

    try:
        envelope = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"runtime envelope is not valid JSON: {error}") from error
    if not isinstance(envelope, dict):
        raise ValueError("runtime envelope must be a JSON object")
    if set(envelope) != {"schema_version", "records"}:
        raise ValueError("runtime envelope must contain only schema_version and records")
    schema_version = envelope.get("schema_version")
    if schema_version not in {1, 2}:
        raise ValueError("runtime envelope schema_version must equal 1 or 2")
    records = envelope.get("records")
    if not isinstance(records, list):
        raise ValueError("runtime envelope records must be a JSON array")

    indexed: dict[str, Mapping[str, object]] = {}
    for index, raw_record in enumerate(records):
        if not isinstance(raw_record, dict):
            raise ValueError(f"runtime envelope record {index} must be a JSON object")
        record = (
            _validate_v1_record(raw_record, index)
            if schema_version == 1
            else _validate_v2_record(raw_record, index)
        )
        artifact_id = str(record["Artifact-ID"])
        if artifact_id in indexed:
            raise ValueError(
                f"runtime envelope contains duplicate Artifact-ID: {artifact_id}"
            )
        indexed[artifact_id] = record
    return RuntimeEnvelope(schema_version, indexed)


def validate_document(
    path: Path,
    *,
    route: str,
    copyright_statement: str,
    runtime_envelope: RuntimeEnvelope | None = None,
) -> list[ValidationFinding]:
    """Validate one explicit governed document through one exact route."""

    if route not in _SUPPORTED_ROUTES:
        raise ValueError(
            f"route must be one of: {', '.join(sorted(_SUPPORTED_ROUTES))}"
        )
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

    if route == "new":
        if runtime_envelope is None:
            return [
                _finding(
                    path,
                    "Runtime-Envelope",
                    "new documents require a schema-version-2 envelope",
                )
            ]
        if runtime_envelope.schema_version != 2:
            return [
                _finding(
                    path,
                    "Runtime-Envelope",
                    "--new requires schema version 2",
                )
            ]
        if suffix in _SUPPORTED_HTML_SUFFIXES:
            return _validate_compact_html(
                path, text, route, copyright_statement, runtime_envelope
            )
        return _validate_compact_markdown(
            path, text, copyright_statement, runtime_envelope
        )

    if route == "legacy":
        if runtime_envelope is None or runtime_envelope.schema_version != 1:
            return [
                _finding(
                    path,
                    "Runtime-Envelope",
                    "--legacy requires a schema-version-1 envelope",
                )
            ]
        return _validate_legacy_document(
            path,
            text,
            state="legacy",
            copyright_statement=copyright_statement,
            runtime_envelope=runtime_envelope,
        )

    if suffix in _SUPPORTED_HTML_SUFFIXES and _CORRELATION_PATTERN.search(text):
        if runtime_envelope is None or runtime_envelope.schema_version != 2:
            return [
                _finding(
                    path,
                    "Runtime-Envelope",
                    "compact historical HTML requires a schema-version-2 envelope",
                )
            ]
        return _validate_compact_html(
            path, text, route, copyright_statement, runtime_envelope
        )
    return _validate_legacy_document(
        path,
        text,
        state="historical",
        copyright_statement=copyright_statement,
        runtime_envelope=None,
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Validate an explicit bounded set of routed governed documents."""

    parser = argparse.ArgumentParser(
        description="Validate governed document creation provenance."
    )
    parser.add_argument(
        "--copyright", required=True, help="Exact project-authorized copyright statement"
    )
    parser.add_argument("--envelope", type=Path, help="External provenance envelope")
    parser.add_argument("--new", action="append", default=[], type=Path, metavar="PATH")
    parser.add_argument(
        "--legacy", action="append", default=[], type=Path, metavar="PATH"
    )
    parser.add_argument(
        "--historical", action="append", default=[], type=Path, metavar="PATH"
    )
    args = parser.parse_args(argv)
    assignments = (
        [(path, "new") for path in args.new]
        + [(path, "legacy") for path in args.legacy]
        + [(path, "historical") for path in args.historical]
    )
    if not assignments:
        print(
            "at least one --new, --legacy, or --historical path is required",
            file=sys.stderr,
        )
        return _USAGE_ERROR_EXIT_CODE
    seen: set[Path] = set()
    for path, _ in assignments:
        if path in seen:
            print(f"duplicate document path: {path}", file=sys.stderr)
            return _USAGE_ERROR_EXIT_CODE
        seen.add(path)

    runtime_envelope = None
    if args.envelope is not None:
        try:
            runtime_envelope = load_runtime_envelope(args.envelope)
        except (OSError, ValueError) as error:
            print(f"{args.envelope}: Runtime-Envelope: {error}", file=sys.stderr)
            return _USAGE_ERROR_EXIT_CODE
    findings = [
        finding
        for path, route in assignments
        for finding in validate_document(
            path,
            route=route,
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


def _validate_v1_record(
    raw_record: Mapping[str, object], index: int
) -> Mapping[str, object]:
    missing = sorted(set(_LEGACY_CORE_FIELDS) - set(raw_record))
    unexpected = sorted(set(raw_record) - set(_LEGACY_CORE_FIELDS))
    if missing:
        raise ValueError(
            f"runtime envelope record {index} is missing: {', '.join(missing)}"
        )
    if unexpected:
        raise ValueError(
            f"runtime envelope record {index} has unsupported fields: {', '.join(unexpected)}"
        )
    record = _string_record(raw_record, _LEGACY_CORE_FIELDS, index)
    if not _is_valid_artifact_id(record["Artifact-ID"]):
        raise ValueError(f"runtime envelope record {index} has an invalid Artifact-ID")
    if not _is_valid_utc_timestamp(record["Created-UTC"]):
        raise ValueError(f"runtime envelope record {index} has an invalid Created-UTC")
    _validate_no_inference(record, index, exempt={"Artifact-ID", "Created-UTC"})
    return record


def _validate_v2_record(
    raw_record: Mapping[str, object], index: int
) -> Mapping[str, object]:
    record_type = raw_record.get("Record-Type")
    if record_type == "new":
        required = {
            "Record-Type",
            "Artifact-ID",
            "Created-Local",
            "Created-UTC",
            "Creating-Agent",
            "Runtime",
            "Dispatched-Model",
            "Reasoning-Effort",
        }
        allowed = required | {"Task-ID"}
        _require_exact_keys(raw_record, required, allowed, index)
        record = _string_record(raw_record, allowed & set(raw_record), index)
        _validate_common_v2_values(record, index)
        return record
    if record_type != "historical":
        raise ValueError(
            f"runtime envelope record {index} Record-Type must be new or historical"
        )
    required = {
        "Record-Type",
        "Artifact-ID",
        "Artifact-ID-Evidence",
        "Known-Facts",
        "Unknown-Facts",
    }
    allowed = required | {"Task-ID"}
    _require_exact_keys(raw_record, required, allowed, index)
    artifact_id = raw_record.get("Artifact-ID")
    if not isinstance(artifact_id, str) or not _is_valid_artifact_id(artifact_id):
        raise ValueError(f"runtime envelope record {index} has an invalid Artifact-ID")
    artifact_evidence = raw_record.get("Artifact-ID-Evidence")
    if artifact_evidence not in _HISTORICAL_ARTIFACT_ID_EVIDENCE:
        raise ValueError(
            f"runtime envelope record {index} has unsupported Artifact-ID-Evidence"
        )
    task_id = raw_record.get("Task-ID")
    if task_id is not None and (
        not isinstance(task_id, str) or _is_placeholder(task_id)
    ):
        raise ValueError(f"runtime envelope record {index} has an invalid Task-ID")
    known = raw_record.get("Known-Facts")
    unknown = raw_record.get("Unknown-Facts")
    if not isinstance(known, dict):
        raise ValueError(f"runtime envelope record {index} Known-Facts must be an object")
    if not isinstance(unknown, list) or any(
        not isinstance(field, str) for field in unknown
    ):
        raise ValueError(f"runtime envelope record {index} Unknown-Facts must be a string array")
    known_keys = set(known)
    unknown_keys = set(unknown)
    if len(unknown) != len(unknown_keys):
        raise ValueError(f"runtime envelope record {index} Unknown-Facts contains duplicates")
    if known_keys & unknown_keys:
        raise ValueError(
            f"runtime envelope record {index} Known-Facts and Unknown-Facts overlap"
        )
    if known_keys | unknown_keys != _HISTORICAL_FACTS:
        raise ValueError(
            f"runtime envelope record {index} Known-Facts and Unknown-Facts must partition the supported historical facts"
        )
    normalized_known: dict[str, Mapping[str, str]] = {}
    for field, fact in known.items():
        if not isinstance(fact, dict) or set(fact) != {"Value", "Evidence"}:
            raise ValueError(
                f"runtime envelope record {index} Known-Facts {field} must contain Value and Evidence"
            )
        value = fact.get("Value")
        evidence = fact.get("Evidence")
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"runtime envelope record {index} Known-Facts {field} has an invalid Value"
            )
        if evidence not in _HISTORICAL_FACT_EVIDENCE[field]:
            raise ValueError(
                f"runtime envelope record {index} Known-Facts {field} has unsupported Evidence"
            )
        if _is_placeholder(value) or _INFERRED_PROFILE_PATTERN.search(value):
            raise ValueError(
                f"runtime envelope record {index} Known-Facts {field} has inferred or placeholder data"
            )
        normalized_known[field] = {"Value": value.strip(), "Evidence": str(evidence)}
    _validate_historical_times(normalized_known, index)
    return {
        "Record-Type": "historical",
        "Artifact-ID": artifact_id.strip(),
        "Artifact-ID-Evidence": artifact_evidence,
        "Known-Facts": normalized_known,
        "Unknown-Facts": list(unknown),
        **({"Task-ID": task_id.strip()} if isinstance(task_id, str) else {}),
    }


def _validate_common_v2_values(record: Mapping[str, str], index: int) -> None:
    if not _is_valid_artifact_id(record["Artifact-ID"]):
        raise ValueError(f"runtime envelope record {index} has an invalid Artifact-ID")
    local = _parse_local_timestamp(record["Created-Local"])
    if local is None:
        raise ValueError(f"runtime envelope record {index} has an invalid Created-Local")
    utc = _parse_utc_timestamp(record["Created-UTC"])
    if utc is None:
        raise ValueError(f"runtime envelope record {index} has an invalid Created-UTC")
    if local.astimezone(timezone.utc) != utc:
        raise ValueError(
            f"runtime envelope record {index} Created-Local and Created-UTC do not represent the same instant"
        )
    _validate_no_inference(
        record, index, exempt={"Record-Type", "Artifact-ID", "Created-Local", "Created-UTC"}
    )


def _validate_historical_times(
    known: Mapping[str, Mapping[str, str]], index: int
) -> None:
    local = known.get("Created-Local", {}).get("Value")
    utc = known.get("Created-UTC", {}).get("Value")
    parsed_local = _parse_local_timestamp(local) if local is not None else None
    parsed_utc = _parse_utc_timestamp(utc) if utc is not None else None
    if local is not None and parsed_local is None:
        raise ValueError(
            f"runtime envelope record {index} Known-Facts Created-Local is invalid"
        )
    if utc is not None and parsed_utc is None:
        raise ValueError(
            f"runtime envelope record {index} Known-Facts Created-UTC is invalid"
        )
    if parsed_local is not None and parsed_utc is not None:
        if parsed_local.astimezone(timezone.utc) != parsed_utc:
            raise ValueError(
                f"runtime envelope record {index} historical creation times do not represent the same instant"
            )


def _validate_compact_markdown(
    path: Path,
    text: str,
    copyright_statement: str,
    runtime_envelope: RuntimeEnvelope,
) -> list[ValidationFinding]:
    candidates = _provenance_comments(
        text,
        copyright_statement,
        markers=_COMPACT_FIELDS + _LEGACY_FIELDS,
        skip_markdown_fences=True,
    )
    if not candidates:
        return [_finding(path, "Provenance", "compact provenance comment is missing")]
    findings: list[ValidationFinding] = []
    if len(candidates) > 1:
        findings.append(_finding(path, "Provenance", "multiple provenance blocks are not allowed"))
    provenance = candidates[0]
    findings.extend(_validate_markdown_placement(path, text, provenance))
    values, block_findings = _parse_block(
        path,
        provenance.group("body"),
        copyright_statement,
        _COMPACT_FIELDS,
    )
    findings.extend(block_findings)
    findings.extend(_validate_compact_values(path, values))
    findings.extend(
        _compare_compact_record(path, values, runtime_envelope, expected_type="new")
    )
    return findings


def _validate_compact_html(
    path: Path,
    text: str,
    route: str,
    copyright_statement: str,
    runtime_envelope: RuntimeEnvelope,
) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    correlations = list(_CORRELATION_PATTERN.finditer(text))
    if not correlations:
        return [_finding(path, "Artifact-ID", "HTML correlation comment is missing")]
    if len(correlations) > 1:
        findings.append(_finding(path, "Artifact-ID", "HTML correlation comment is duplicated"))
    correlation = correlations[0]
    doctype = _DOCTYPE_PATTERN.match(text)
    if doctype is None:
        findings.append(_finding(path, "Placement", "maintained HTML must start with a doctype"))
    elif correlation.start() != _skip_blank_lines(text, doctype.end("doctype")):
        findings.append(
            _finding(
                path,
                "Placement",
                "HTML correlation comment must be the first construct after the doctype",
            )
        )
    artifact_id = correlation.group("artifact_id").strip()
    if not _is_valid_artifact_id(artifact_id):
        findings.append(_finding(path, "Artifact-ID", "HTML correlation identifier is invalid"))
        return findings
    record = runtime_envelope.records.get(artifact_id)
    if record is None:
        findings.append(
            _finding(path, "Runtime-Envelope", f"no record exists for Artifact-ID {artifact_id}")
        )
        return findings
    expected_type = "new" if route == "new" else "historical"
    if record.get("Record-Type") != expected_type:
        findings.append(
            _finding(
                path,
                "Runtime-Envelope",
                f"--{route} requires a {expected_type} envelope record",
            )
        )
        return findings

    parser = _ProvenanceHtmlParser()
    try:
        parser.feed(text)
        parser.close()
    except Exception as error:  # HTMLParser reports malformed parser state variably.
        return [_finding(path, "HTML", f"cannot parse maintained HTML: {error}")]
    if len(parser.footnotes) != 1:
        findings.append(
            _finding(path, "Footnote", "maintained HTML must contain exactly one provenance footnote")
        )
        if not parser.footnotes:
            return findings
    footnote = parser.footnotes[0]
    if not footnote.in_footer:
        findings.append(_finding(path, "Placement", "provenance footnote must be inside footer"))
    versions = footnote.fields.pop("Footnote-Version", [])
    if versions != ["v2"]:
        findings.append(_finding(path, "Footnote", "provenance footnote marker must equal v2"))
    visible_text = _normalize_text(" ".join(footnote.text_parts))
    if _FORBIDDEN_VISIBLE_METADATA.search(visible_text):
        findings.append(
            _finding(path, "Footnote", "internal correlation or evidence metadata is visible")
        )
    findings.extend(_validate_footnote_fields(path, footnote, record, route, copyright_statement))
    return findings


def _validate_footnote_fields(
    path: Path,
    footnote: _HtmlFootnote,
    record: Mapping[str, object],
    route: str,
    copyright_statement: str,
) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    unexpected = sorted(set(footnote.fields) - set(_HTML_READER_FIELDS))
    for field in unexpected:
        findings.append(_finding(path, field, "unsupported provenance footnote field"))
    expected: dict[str, str] = {"Copyright": copyright_statement}
    forbidden: set[str] = set()
    if route == "new":
        expected.update(
            {
                field: str(record[field])
                for field in _HTML_READER_FIELDS
                if field != "Copyright"
            }
        )
    else:
        known = record["Known-Facts"]
        unknown = set(record["Unknown-Facts"])
        assert isinstance(known, Mapping)
        for field in _HTML_READER_FIELDS:
            if field == "Copyright":
                continue
            if field in known:
                fact = known[field]
                assert isinstance(fact, Mapping)
                expected[field] = str(fact["Value"])
            elif field in unknown:
                forbidden.add(field)
    for field, value in expected.items():
        actual = footnote.fields.get(field, [])
        if not actual:
            findings.append(_finding(path, field, "required provenance footnote field is missing"))
            continue
        if len(actual) > 1:
            findings.append(_finding(path, field, "provenance footnote field is duplicated"))
        if actual[0] != value:
            findings.append(_finding(path, field, "footnote value does not match authoritative evidence"))
    for field in forbidden:
        if field in footnote.fields:
            findings.append(_finding(path, field, "externally unknown fact must be omitted"))
    time_values = footnote.time_datetimes.get("Created-Local", [])
    if "Created-Local" in expected:
        if len(time_values) != 1:
            findings.append(
                _finding(path, "Created-Local", "must use exactly one time element with datetime")
            )
        elif time_values[0] != expected["Created-Local"]:
            findings.append(
                _finding(path, "Created-Local", "time datetime does not match authoritative evidence")
            )
    return findings


def _validate_legacy_document(
    path: Path,
    text: str,
    *,
    state: str,
    copyright_statement: str,
    runtime_envelope: RuntimeEnvelope | None,
) -> list[ValidationFinding]:
    candidates = _provenance_comments(
        text,
        copyright_statement,
        markers=_LEGACY_FIELDS,
        skip_markdown_fences=path.suffix.lower() in _SUPPORTED_MARKDOWN_SUFFIXES,
    )
    if not candidates:
        return [_finding(path, "Provenance", "legacy provenance comment is missing")]
    findings: list[ValidationFinding] = []
    if len(candidates) > 1:
        findings.append(_finding(path, "Provenance", "multiple provenance blocks are not allowed"))
    provenance = candidates[0]
    if path.suffix.lower() in _SUPPORTED_MARKDOWN_SUFFIXES:
        findings.extend(_validate_markdown_placement(path, text, provenance))
    else:
        findings.extend(_validate_legacy_html_placement(path, text, provenance))
    values, block_findings = _parse_block(
        path, provenance.group("body"), copyright_statement, _LEGACY_FIELDS
    )
    findings.extend(block_findings)
    findings.extend(_validate_legacy_values(path, values, state))
    if state == "legacy" and runtime_envelope is not None:
        findings.extend(_compare_legacy_record(path, values, runtime_envelope))
    return findings


def _parse_block(
    path: Path,
    body: str,
    copyright_statement: str,
    required_fields: Sequence[str],
) -> tuple[dict[str, str], list[ValidationFinding]]:
    findings: list[ValidationFinding] = []
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    if lines.count(copyright_statement) != 1:
        findings.append(
            _finding(path, "Copyright", "provenance must contain the exact copyright statement once")
        )
    collected: dict[str, list[str]] = {}
    encountered: list[str] = []
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
        if label not in required_fields:
            findings.append(_finding(path, label, "unsupported provenance field"))
            continue
        encountered.append(label)
        collected.setdefault(label, []).append(match.group("value").strip())
    values: dict[str, str] = {}
    for field in required_fields:
        field_values = collected.get(field, [])
        if not field_values:
            findings.append(_finding(path, field, "required provenance field is missing"))
            continue
        if len(field_values) > 1:
            findings.append(_finding(path, field, "provenance field is duplicated"))
        values[field] = field_values[0]
    if encountered != list(required_fields):
        findings.append(_finding(path, "Provenance", "provenance fields are not in canonical order"))
    return values, findings


def _validate_compact_values(
    path: Path, values: Mapping[str, str]
) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    artifact_id = values.get("Artifact-ID")
    if artifact_id is not None and not _is_valid_artifact_id(artifact_id):
        findings.append(_finding(path, "Artifact-ID", "must be a durable opaque identifier"))
    local = values.get("Created-Local")
    if local is not None and _parse_local_timestamp(local) is None:
        message = (
            "must include an explicit numeric UTC offset; Z and offset-free values are not allowed"
            if local.endswith("Z") or _LOCAL_TIMESTAMP_PATTERN.fullmatch(local) is None
            else "must be a valid ISO 8601 local timestamp"
        )
        findings.append(_finding(path, "Created-Local", message))
    for field in _COMPACT_FIELDS:
        value = values.get(field)
        if value is None:
            continue
        if _is_placeholder(value):
            findings.append(_finding(path, field, "placeholder values are not allowed"))
        if _INFERRED_PROFILE_PATTERN.search(value):
            findings.append(_finding(path, field, "inferred configuration is not evidence"))
    return findings


def _validate_legacy_values(
    path: Path, values: Mapping[str, str], state: str
) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    artifact_id = values.get("Artifact-ID")
    if artifact_id is not None and not _is_valid_artifact_id(artifact_id):
        findings.append(_finding(path, "Artifact-ID", "must be a durable opaque identifier"))
    created_utc = values.get("Created-UTC")
    if created_utc is not None:
        if state == "historical" and created_utc == _HISTORICAL_UNKNOWN:
            pass
        elif not _is_valid_utc_timestamp(created_utc):
            findings.append(_finding(path, "Created-UTC", "must be an ISO 8601 UTC timestamp"))
    for field in _LEGACY_CORE_FIELDS:
        value = values.get(field)
        if value is None:
            continue
        if state == "legacy" and value == _HISTORICAL_UNKNOWN:
            findings.append(_finding(path, field, "historical-unknown is not valid for legacy new records"))
        elif value != _HISTORICAL_UNKNOWN and _is_placeholder(value):
            findings.append(_finding(path, field, "placeholder values are not allowed"))
        if _INFERRED_PROFILE_PATTERN.search(value):
            findings.append(_finding(path, field, "inferred configuration is not evidence"))
    for core, evidence_field in zip(
        _LEGACY_CORE_FIELDS, _LEGACY_EVIDENCE_FIELDS, strict=True
    ):
        evidence = values.get(evidence_field)
        value = values.get(core)
        if evidence is None:
            continue
        if state == "legacy":
            if evidence != _RUNTIME_EVIDENCE:
                findings.append(_finding(path, evidence_field, "legacy new records require runtime-supplied evidence"))
            continue
        if evidence not in _ALLOWED_LEGACY_EVIDENCE[evidence_field]:
            findings.append(_finding(path, evidence_field, "unsupported historical evidence status"))
        elif value == _HISTORICAL_UNKNOWN and evidence != _HISTORICAL_UNKNOWN:
            findings.append(_finding(path, evidence_field, "unknown values require matching evidence status"))
        elif value not in {None, _HISTORICAL_UNKNOWN} and evidence == _HISTORICAL_UNKNOWN:
            findings.append(_finding(path, evidence_field, "concrete values require concrete evidence"))
    return findings


def _compare_compact_record(
    path: Path,
    values: Mapping[str, str],
    envelope: RuntimeEnvelope,
    *,
    expected_type: str,
) -> list[ValidationFinding]:
    artifact_id = values.get("Artifact-ID")
    if artifact_id is None or not _is_valid_artifact_id(artifact_id):
        return []
    record = envelope.records.get(artifact_id)
    if record is None:
        return [_finding(path, "Runtime-Envelope", f"no record exists for Artifact-ID {artifact_id}")]
    if record.get("Record-Type") != expected_type:
        return [_finding(path, "Runtime-Envelope", f"record type does not match {expected_type} route")]
    findings: list[ValidationFinding] = []
    local = values.get("Created-Local")
    record_local = record.get("Created-Local")
    record_utc = record.get("Created-UTC")
    if isinstance(local, str):
        parsed_local = _parse_local_timestamp(local)
        parsed_utc = _parse_utc_timestamp(record_utc) if isinstance(record_utc, str) else None
        if parsed_local is not None and parsed_utc is not None:
            if parsed_local.astimezone(timezone.utc) != parsed_utc:
                findings.append(_finding(path, "Created-Local", "must represent the same instant as Created-UTC"))
    for field in _COMPACT_FIELDS:
        if field in values and values[field] != record.get(field):
            findings.append(_finding(path, field, "document value does not match the runtime envelope"))
    if local is not None and local == record_local and _parse_local_timestamp(local) is None:
        return findings
    return findings


def _compare_legacy_record(
    path: Path, values: Mapping[str, str], envelope: RuntimeEnvelope
) -> list[ValidationFinding]:
    artifact_id = values.get("Artifact-ID")
    if artifact_id is None or not _is_valid_artifact_id(artifact_id):
        return []
    record = envelope.records.get(artifact_id)
    if record is None:
        return [_finding(path, "Runtime-Envelope", f"no record exists for Artifact-ID {artifact_id}")]
    return [
        _finding(path, field, "document value does not match the runtime envelope")
        for field in _LEGACY_CORE_FIELDS
        if values.get(field) != record.get(field)
    ]


def _provenance_comments(
    text: str,
    copyright_statement: str,
    *,
    markers: Sequence[str],
    skip_markdown_fences: bool,
) -> list[re.Match[str]]:
    marker_tokens = tuple(f"{field}:" for field in markers)
    return [
        match
        for match in _COMMENT_PATTERN.finditer(text)
        if (
            copyright_statement in match.group("body")
            or any(token in match.group("body") for token in marker_tokens)
        )
        and (
            not skip_markdown_fences
            or not _inside_markdown_fence(text, match.start())
        )
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


def _validate_markdown_placement(
    path: Path, text: str, provenance: re.Match[str]
) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    frontmatter_end = _markdown_frontmatter_end(text)
    expected_start = _skip_blank_lines(
        text, frontmatter_end if frontmatter_end is not None else 0
    )
    if provenance.start() != expected_start:
        findings.append(
            _finding(
                path,
                "Placement",
                "provenance must be the first construct after YAML front matter, or the first document construct",
            )
        )
    if frontmatter_end is None and _starts_with_frontmatter(
        text[provenance.end() :].lstrip()
    ):
        findings.append(_finding(path, "Placement", "provenance appears before YAML front matter"))
    return findings


def _validate_legacy_html_placement(
    path: Path, text: str, provenance: re.Match[str]
) -> list[ValidationFinding]:
    doctype = _DOCTYPE_PATTERN.match(text)
    if doctype is None:
        return [_finding(path, "Placement", "maintained HTML must start with a doctype")]
    if provenance.start() != _skip_blank_lines(text, doctype.end("doctype")):
        return [_finding(path, "Placement", "legacy provenance must follow the doctype")]
    return []


def _markdown_frontmatter_end(text: str) -> int | None:
    if not _starts_with_frontmatter(text):
        return None
    delimiters = list(_FRONTMATTER_DELIMITER_PATTERN.finditer(text))
    return delimiters[1].end() if len(delimiters) >= 2 else None


def _starts_with_frontmatter(text: str) -> bool:
    return _FRONTMATTER_OPEN_PATTERN.match(text) is not None


def _skip_blank_lines(text: str, start: int) -> int:
    match = _BLANK_LINES_PATTERN.match(text, start)
    return match.end() if match is not None else start


def _require_exact_keys(
    record: Mapping[str, object],
    required: set[str],
    allowed: set[str],
    index: int,
) -> None:
    missing = sorted(required - set(record))
    unexpected = sorted(set(record) - allowed)
    if missing:
        raise ValueError(
            f"runtime envelope record {index} is missing: {', '.join(missing)}"
        )
    if unexpected:
        raise ValueError(
            f"runtime envelope record {index} has unsupported fields: {', '.join(unexpected)}"
        )


def _string_record(
    raw: Mapping[str, object], fields: Sequence[str] | set[str], index: int
) -> dict[str, str]:
    record: dict[str, str] = {}
    for field in fields:
        value = raw.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"runtime envelope record {index} {field} must be a non-empty string"
            )
        record[field] = value.strip()
    return record


def _validate_no_inference(
    record: Mapping[str, str], index: int, *, exempt: set[str]
) -> None:
    for field, value in record.items():
        if field in exempt:
            continue
        if _is_placeholder(value):
            raise ValueError(f"runtime envelope record {index} has a placeholder {field}")
        if _INFERRED_PROFILE_PATTERN.search(value):
            raise ValueError(
                f"runtime envelope record {index} has inferred configuration in {field}"
            )


def _is_valid_artifact_id(value: str) -> bool:
    return _ARTIFACT_ID_PATTERN.fullmatch(value) is not None and not _is_placeholder(value)


def _is_valid_utc_timestamp(value: str) -> bool:
    return _parse_utc_timestamp(value) is not None


def _parse_utc_timestamp(value: str | None) -> datetime | None:
    if value is None or _UTC_TIMESTAMP_PATTERN.fullmatch(value) is None:
        return None
    try:
        normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.utcoffset() is None or parsed.utcoffset().total_seconds() != 0:
        return None
    return parsed.astimezone(timezone.utc)


def _parse_local_timestamp(value: str | None) -> datetime | None:
    if value is None or _LOCAL_TIMESTAMP_PATTERN.fullmatch(value) is None:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    return parsed if parsed.utcoffset() is not None else None


def _is_placeholder(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized == _HISTORICAL_UNKNOWN:
        return False
    return not normalized or _PLACEHOLDER_PATTERN.search(value) is not None


def _normalize_text(value: str) -> str:
    return " ".join(value.split())


def _finding(path: Path, field: str, message: str) -> ValidationFinding:
    return ValidationFinding(path=path, field=field, message=message)


if __name__ == "__main__":
    raise SystemExit(main())
