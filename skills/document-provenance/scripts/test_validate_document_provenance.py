#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies compact, legacy, and historical document provenance validation.

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from validate_document_provenance import (
    ValidationFinding,
    load_runtime_envelope,
    main,
    validate_document,
)


_PACKAGE_ROOT = Path(__file__).resolve().parents[1]
_FIXTURES = _PACKAGE_ROOT / "fixtures"
_COPYRIGHT = "Copyright (c) 2026 Martin.Bechard@DevConsult.ca"
_COMPACT_MARKDOWN = """<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: artifact-test-compact
Created-Local: 2026-08-08T14:15:00-04:00
Creating-Agent: Dev Documentation Writer
Runtime: Codex
Dispatched-Model: gpt-5.5
Reasoning-Effort: high
-->
# Compact
"""
class DocumentProvenanceValidatorTest(unittest.TestCase):
    """Exercise compact new, compatible legacy, and historical provenance."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.runtime_envelope = load_runtime_envelope(
            _FIXTURES / "runtime-envelope.json"
        )
        cls.legacy_envelope = load_runtime_envelope(
            _FIXTURES / "runtime-envelope-v1.json"
        )

    def test_accepts_compact_new_governed_document_formats(self) -> None:
        valid_paths = (
            "valid/markdown-without-front-matter.md",
            "valid/markdown-with-okf-front-matter.md",
            "valid/wiki/index.md",
            "valid/wiki/log.md",
            "valid/maintained.html",
            "valid/generated.md",
            "valid/positive-offset.md",
        )

        for relative_path in valid_paths:
            with self.subTest(relative_path=relative_path):
                self.assertEqual(
                    [],
                    validate_document(
                        _FIXTURES / relative_path,
                        route="new",
                        copyright_statement=_COPYRIGHT,
                        runtime_envelope=self.runtime_envelope,
                    ),
                )

    def test_accepts_positive_and_negative_local_offsets(self) -> None:
        paths = (
            _FIXTURES / "valid/markdown-without-front-matter.md",
            _FIXTURES / "valid/positive-offset.md",
        )
        for path in paths:
            with self.subTest(path=path):
                self.assertEqual(
                    [],
                    validate_document(
                        path,
                        route="new",
                        copyright_statement=_COPYRIGHT,
                        runtime_envelope=self.runtime_envelope,
                    ),
                )

    def test_v2_created_utc_schema_and_validator_require_z(self) -> None:
        schema = json.loads(
            (_PACKAGE_ROOT / "assets/provenance-envelope.schema.json").read_text(
                encoding="utf-8"
            )
        )
        pattern = schema["$defs"]["createdUtc"]["pattern"]
        self.assertRegex("2026-08-08T18:15:00Z", pattern)
        self.assertNotRegex("2026-08-08T18:15:00+00:00", pattern)

        record = dict(self.runtime_envelope.records["artifact-test-compact"])
        record["Created-UTC"] = "2026-08-08T18:15:00+00:00"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "runtime-envelope.json"
            path.write_text(
                json.dumps({"schema_version": 2, "records": [record]}),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "invalid Created-UTC"):
                load_runtime_envelope(path)

            historical = json.loads(
                json.dumps(
                    self.runtime_envelope.records["artifact-historical-all-known"]
                )
            )
            historical["Known-Facts"]["Created-UTC"]["Value"] = (
                "2026-07-20T08:01:32+00:00"
            )
            path.write_text(
                json.dumps({"schema_version": 2, "records": [historical]}),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "Created-UTC is invalid"):
                load_runtime_envelope(path)

    def test_v1_created_utc_keeps_zero_offset_compatibility(self) -> None:
        record = dict(next(iter(self.legacy_envelope.records.values())))
        record["Created-UTC"] = "2026-08-08T18:22:49+00:00"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "runtime-envelope.json"
            path.write_text(
                json.dumps({"schema_version": 1, "records": [record]}),
                encoding="utf-8",
            )
            loaded = load_runtime_envelope(path)
        self.assertEqual(1, loaded.schema_version)

    def test_legacy_route_accepts_unchanged_package_headers(self) -> None:
        paths = (
            _PACKAGE_ROOT / "SKILL.md",
            _PACKAGE_ROOT / "references/format-contract.md",
            _PACKAGE_ROOT / "references/historical-migration.md",
        )

        for path in paths:
            with self.subTest(path=path):
                self.assertEqual(
                    [],
                    validate_document(
                        path,
                        route="legacy",
                        copyright_statement=_COPYRIGHT,
                        runtime_envelope=self.legacy_envelope,
                    ),
                )

    def test_historical_route_accepts_verbose_and_compact_forms(self) -> None:
        self.assertEqual(
            [],
            validate_document(
                _FIXTURES / "valid/historical-unknown.md",
                route="historical",
                copyright_statement=_COPYRIGHT,
            ),
        )
        self.assertEqual(
            [],
            validate_document(
                _FIXTURES / "valid/historical-compact.html",
                route="historical",
                copyright_statement=_COPYRIGHT,
                runtime_envelope=self.runtime_envelope,
            ),
        )
        self.assertEqual(
            [],
            validate_document(
                _FIXTURES / "valid/historical-all-known.html",
                route="historical",
                copyright_statement=_COPYRIGHT,
                runtime_envelope=self.runtime_envelope,
            ),
        )

    def test_rejects_invalid_local_time_and_instant_mismatch(self) -> None:
        cases = {
            "offset-free-local.md": "numeric UTC offset",
            "z-local.md": "numeric UTC offset",
            "malformed-positive-offset.md": "numeric UTC offset",
            "malformed-negative-offset.md": "numeric UTC offset",
            "nonexistent-local-time.md": "valid ISO 8601",
            "instant-mismatch.md": "same instant",
        }

        for filename, message in cases.items():
            with self.subTest(filename=filename):
                findings = validate_document(
                    _FIXTURES / "invalid" / filename,
                    route="new",
                    copyright_statement=_COPYRIGHT,
                    runtime_envelope=self.runtime_envelope,
                )
                self.assertTrue(
                    any(
                        finding.field == "Created-Local"
                        and message in finding.message
                        for finding in findings
                    ),
                    findings,
                )

    def test_rejects_html_marker_and_footnote_failures(self) -> None:
        cases = (
            "html-missing-correlation.html",
            "html-duplicate-correlation.html",
            "html-misplaced-correlation.html",
            "html-missing-footnote.html",
            "html-duplicate-footnote.html",
            "html-footnote-outside-footer.html",
            "html-wrong-footnote-version.html",
            "html-missing-field.html",
            "html-duplicate-field.html",
            "html-artifact-mismatch.html",
            "html-value-mismatch.html",
            "html-visible-evidence.html",
            "html-wrong-field-tag.html",
            "html-task-id-comment.html",
            "html-task-id-attribute.html",
        )

        for filename in cases:
            with self.subTest(filename=filename):
                findings = validate_document(
                    _FIXTURES / "invalid" / filename,
                    route="new",
                    copyright_statement=_COPYRIGHT,
                    runtime_envelope=self.runtime_envelope,
                )
                self.assertNotEqual([], findings)

    def test_rejects_reordered_compact_copyright(self) -> None:
        findings = validate_document(
            _FIXTURES / "invalid/reordered-copyright.md",
            route="new",
            copyright_statement=_COPYRIGHT,
            runtime_envelope=self.runtime_envelope,
        )
        self.assertTrue(
            any(finding.field == "Provenance" for finding in findings),
            findings,
        )

    def test_rejects_forbidden_metadata_split_across_inline_elements(self) -> None:
        findings = validate_document(
            _FIXTURES / "invalid/html-split-task-id.html",
            route="new",
            copyright_statement=_COPYRIGHT,
            runtime_envelope=self.runtime_envelope,
        )
        self.assertTrue(
            any(finding.field == "Footnote" for finding in findings),
            findings,
        )

    def test_historical_known_and_unknown_facts_control_visibility(self) -> None:
        known_findings = validate_document(
            _FIXTURES / "invalid/historical-known-omitted.html",
            route="historical",
            copyright_statement=_COPYRIGHT,
            runtime_envelope=self.runtime_envelope,
        )
        unknown_findings = validate_document(
            _FIXTURES / "invalid/historical-unknown-displayed.html",
            route="historical",
            copyright_statement=_COPYRIGHT,
            runtime_envelope=self.runtime_envelope,
        )

        self.assertIn("Created-Local", {finding.field for finding in known_findings})
        self.assertIn("Runtime", {finding.field for finding in unknown_findings})

    def test_rejects_compact_internal_metadata(self) -> None:
        fixtures = (
            "compact-task-id.md",
            "compact-evidence.md",
            "compact-placeholder.md",
            "compact-inferred.md",
        )
        for filename in fixtures:
            with self.subTest(filename=filename):
                self.assertNotEqual(
                    [],
                    validate_document(
                        _FIXTURES / "invalid" / filename,
                        route="new",
                        copyright_statement=_COPYRIGHT,
                        runtime_envelope=self.runtime_envelope,
                    ),
                )

    def test_optional_external_task_id_is_not_a_document_field(self) -> None:
        records = {
            "artifact-test-compact": {
                "Record-Type": "new",
                "Artifact-ID": "artifact-test-compact",
                "Created-Local": "2026-08-08T14:15:00-04:00",
                "Created-UTC": "2026-08-08T18:15:00Z",
                "Creating-Agent": "Dev Documentation Writer",
                "Runtime": "Codex",
                "Dispatched-Model": "gpt-5.5",
                "Reasoning-Effort": "high",
                "Task-ID": "external-only-task",
            }
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "document.md"
            path.write_text(_COMPACT_MARKDOWN, encoding="utf-8")
            self.assertEqual(
                [],
                validate_document(
                    path,
                    route="new",
                    copyright_statement=_COPYRIGHT,
                    runtime_envelope=self.runtime_envelope.with_records(records),
                ),
            )

    def test_rejects_schema_and_route_mismatches(self) -> None:
        compact = _FIXTURES / "valid/markdown-without-front-matter.md"
        legacy = _PACKAGE_ROOT / "SKILL.md"
        cases = (
            (compact, "new", self.legacy_envelope),
            (legacy, "legacy", self.runtime_envelope),
            (legacy, "new", self.runtime_envelope),
            (compact, "legacy", self.legacy_envelope),
        )
        for path, route, envelope in cases:
            with self.subTest(path=path, route=route):
                self.assertNotEqual(
                    [],
                    validate_document(
                        path,
                        route=route,
                        copyright_statement=_COPYRIGHT,
                        runtime_envelope=envelope,
                    ),
                )

    def test_rejects_invalid_historical_partitions(self) -> None:
        cases = (
            _FIXTURES / "invalid/runtime-envelope-historical-overlap.json",
            _FIXTURES / "invalid/runtime-envelope-historical-incomplete.json",
        )
        for path in cases:
            with self.subTest(path=path):
                with self.assertRaisesRegex(ValueError, "Known-Facts|Unknown-Facts"):
                    load_runtime_envelope(path)

    def test_generated_fixture_matches_its_owning_template(self) -> None:
        template = (
            _FIXTURES / "generated/source-template.md.tmpl"
        ).read_text(encoding="utf-8")
        rendered = template
        replacements = {
            "{{COPYRIGHT}}": _COPYRIGHT,
            "{{ARTIFACT_ID}}": "artifact-valid-generated",
            "{{CREATED_LOCAL}}": "2026-08-08T14:20:00-04:00",
            "{{CREATING_AGENT}}": "Dev Documentation Writer",
            "{{RUNTIME}}": "Codex",
            "{{DISPATCHED_MODEL}}": "gpt-5.5",
            "{{REASONING_EFFORT}}": "high",
        }
        for placeholder, value in replacements.items():
            rendered = rendered.replace(placeholder, value)

        expected = (_FIXTURES / "valid/generated.md").read_text(encoding="utf-8")
        self.assertNotIn("{{", rendered)
        self.assertEqual(expected, rendered)

    def test_cli_validates_each_exact_route(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = main(
                [
                    "--copyright",
                    _COPYRIGHT,
                    "--envelope",
                    str(_FIXTURES / "runtime-envelope.json"),
                    "--new",
                    str(_FIXTURES / "valid/markdown-without-front-matter.md"),
                    "--historical",
                    str(_FIXTURES / "valid/historical-compact.html"),
                ]
            )
        self.assertEqual(0, result)
        self.assertIn("validated 2 documents", output.getvalue())

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = main(
                [
                    "--copyright",
                    _COPYRIGHT,
                    "--envelope",
                    str(_FIXTURES / "runtime-envelope-v1.json"),
                    "--legacy",
                    str(_PACKAGE_ROOT / "SKILL.md"),
                    "--historical",
                    str(_FIXTURES / "valid/historical-unknown.md"),
                ]
            )
        self.assertEqual(0, result)
        self.assertIn("validated 2 documents", output.getvalue())

    def test_cli_reports_exact_path_and_field(self) -> None:
        path = _FIXTURES / "invalid/malformed-utc.md"
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = main(
                [
                    "--copyright",
                    _COPYRIGHT,
                    "--envelope",
                    str(_FIXTURES / "runtime-envelope.json"),
                    "--new",
                    str(path),
                ]
            )
        self.assertEqual(1, result)
        self.assertIn(f"{path}: Created-Local:", output.getvalue())

    def test_rejects_unsupported_document_formats_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "document.pdf"
            path.write_bytes(b"%PDF-1.7")
            findings = validate_document(
                path,
                route="new",
                copyright_statement=_COPYRIGHT,
                runtime_envelope=self.runtime_envelope,
            )
        self.assertEqual("Format", findings[0].field)


if __name__ == "__main__":
    unittest.main()
