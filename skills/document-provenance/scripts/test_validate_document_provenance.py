#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies the deterministic document provenance validator and its representative fixtures.

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


class DocumentProvenanceValidatorTest(unittest.TestCase):
    """Exercise valid, invalid, generated, and historical document records."""

    @classmethod
    def setUpClass(cls) -> None:
        """Load the runtime envelope shared by new-document fixtures."""

        cls.runtime_envelope = load_runtime_envelope(_FIXTURES / "runtime-envelope.json")

    def test_accepts_new_governed_document_formats(self) -> None:
        valid_paths = (
            "valid/markdown-without-front-matter.md",
            "valid/markdown-with-okf-front-matter.md",
            "valid/wiki/index.md",
            "valid/wiki/log.md",
            "valid/maintained.html",
            "valid/generated.md",
        )

        for relative_path in valid_paths:
            with self.subTest(relative_path=relative_path):
                findings = validate_document(
                    _FIXTURES / relative_path,
                    state="new",
                    copyright_statement=_COPYRIGHT,
                    runtime_envelope=self.runtime_envelope,
                )

                self.assertEqual([], findings)

    def test_package_documentation_has_runtime_enveloped_provenance(self) -> None:
        package_documents = (
            _PACKAGE_ROOT / "SKILL.md",
            _PACKAGE_ROOT / "references/format-contract.md",
            _PACKAGE_ROOT / "references/historical-migration.md",
        )

        for path in package_documents:
            with self.subTest(path=path):
                findings = validate_document(
                    path,
                    state="new",
                    copyright_statement=_COPYRIGHT,
                    runtime_envelope=self.runtime_envelope,
                )

                self.assertEqual([], findings)

    def test_accepts_historical_unknowns_only_in_historical_mode(self) -> None:
        historical_path = _FIXTURES / "valid/historical-unknown.md"

        historical_findings = validate_document(
            historical_path,
            state="historical",
            copyright_statement=_COPYRIGHT,
        )
        new_findings = validate_document(
            historical_path,
            state="new",
            copyright_statement=_COPYRIGHT,
            runtime_envelope=self.runtime_envelope,
        )

        self.assertEqual([], historical_findings)
        self.assertTrue(any(finding.field == "Created-UTC-Evidence" for finding in new_findings))
        self.assertTrue(any(finding.field == "Creating-Agent" for finding in new_findings))

    def test_rejects_each_required_negative_fixture(self) -> None:
        expected_findings = {
            "missing-copyright.md": {"Copyright"},
            "missing-provenance.md": {"Provenance"},
            "comment-before-front-matter.md": {"Placement"},
            "missing-field.md": {"Task-ID"},
            "duplicate-field.md": {"Task-ID"},
            "placeholder.md": {"Creating-Agent"},
            "malformed-utc.md": {"Created-UTC"},
            "unsupported-evidence.md": {"Created-UTC-Evidence"},
            "inferred-profile.md": {
                "Dispatched-Model-Evidence",
                "Reasoning-Effort-Evidence",
            },
            "indented-provenance.md": {"Placement"},
        }

        for fixture_name, expected_fields in expected_findings.items():
            with self.subTest(fixture_name=fixture_name):
                findings = validate_document(
                    _FIXTURES / "invalid" / fixture_name,
                    state="new",
                    copyright_statement=_COPYRIGHT,
                    runtime_envelope=self.runtime_envelope,
                )

                self.assertTrue(expected_fields.issubset({finding.field for finding in findings}))

    def test_rejects_space_and_tab_indented_provenance_openers(self) -> None:
        source = (_FIXTURES / "invalid/indented-provenance.md").read_text(
            encoding="utf-8"
        )
        with tempfile.TemporaryDirectory() as directory:
            tab_indented = Path(directory) / "tab-indented.md"
            tab_indented.write_text(
                source.replace("    <!--", "\t<!--", 1),
                encoding="utf-8",
            )
            html_source = (_FIXTURES / "valid/maintained.html").read_text(
                encoding="utf-8"
            )
            space_indented_html = Path(directory) / "space-indented.html"
            space_indented_html.write_text(
                html_source.replace("\n<!--", "\n    <!--", 1),
                encoding="utf-8",
            )
            tab_indented_html = Path(directory) / "tab-indented.html"
            tab_indented_html.write_text(
                html_source.replace("\n<!--", "\n\t<!--", 1),
                encoding="utf-8",
            )

            space_findings = validate_document(
                _FIXTURES / "invalid/indented-provenance.md",
                state="new",
                copyright_statement=_COPYRIGHT,
                runtime_envelope=self.runtime_envelope,
            )
            tab_findings = validate_document(
                tab_indented,
                state="new",
                copyright_statement=_COPYRIGHT,
                runtime_envelope=self.runtime_envelope,
            )
            html_findings = [
                validate_document(
                    path,
                    state="new",
                    copyright_statement=_COPYRIGHT,
                    runtime_envelope=self.runtime_envelope,
                )
                for path in (space_indented_html, tab_indented_html)
            ]

        self.assertIn("Placement", {finding.field for finding in space_findings})
        self.assertIn("Placement", {finding.field for finding in tab_findings})
        for findings in html_findings:
            self.assertIn("Placement", {finding.field for finding in findings})

    def test_accepts_blank_line_separation_without_opener_indentation(self) -> None:
        cases = (
            (
                "valid/markdown-with-okf-front-matter.md",
                "---\n<!--",
                "---\n\n<!--",
            ),
            (
                "valid/maintained.html",
                "<!doctype html>\n<!--",
                "<!doctype html>\n\n<!--",
            ),
        )

        with tempfile.TemporaryDirectory() as directory:
            findings_by_name: dict[str, list[ValidationFinding]] = {}
            for relative_path, marker, replacement in cases:
                source_path = _FIXTURES / relative_path
                separated = Path(directory) / source_path.name
                separated.write_text(
                    source_path.read_text(encoding="utf-8").replace(
                        marker,
                        replacement,
                        1,
                    ),
                    encoding="utf-8",
                )
                findings_by_name[relative_path] = validate_document(
                    separated,
                    state="new",
                    copyright_statement=_COPYRIGHT,
                    runtime_envelope=self.runtime_envelope,
                )

        for relative_path, findings in findings_by_name.items():
            with self.subTest(relative_path=relative_path):
                self.assertEqual([], findings)

    def test_requires_runtime_envelope_for_new_documents(self) -> None:
        findings = validate_document(
            _FIXTURES / "valid/markdown-without-front-matter.md",
            state="new",
            copyright_statement=_COPYRIGHT,
        )

        self.assertIn("Runtime-Envelope", {finding.field for finding in findings})

    def test_reports_runtime_envelope_mismatch_on_the_exact_field(self) -> None:
        mismatched_envelope = {
            **self.runtime_envelope,
            "artifact-valid-markdown": {
                **self.runtime_envelope["artifact-valid-markdown"],
                "Dispatched-Model": "different-model",
            },
        }

        findings = validate_document(
            _FIXTURES / "valid/markdown-without-front-matter.md",
            state="new",
            copyright_statement=_COPYRIGHT,
            runtime_envelope=mismatched_envelope,
        )

        self.assertIn("Dispatched-Model", {finding.field for finding in findings})

    def test_generated_fixture_matches_its_owning_template(self) -> None:
        template = (_FIXTURES / "generated/source-template.md.tmpl").read_text(encoding="utf-8")
        rendered = template
        replacements = {
            "{{COPYRIGHT}}": _COPYRIGHT,
            "{{ARTIFACT_ID}}": "artifact-valid-generated",
            "{{CREATED_UTC}}": "2026-08-08T18:20:00Z",
            "{{CREATING_AGENT}}": "Dev Documentation Writer",
            "{{RUNTIME}}": "Codex",
            "{{DISPATCHED_MODEL}}": "gpt-5.5",
            "{{REASONING_EFFORT}}": "high",
            "{{TASK_ID}}": "task-generated-001",
        }
        for placeholder, value in replacements.items():
            rendered = rendered.replace(placeholder, value)

        expected = (_FIXTURES / "valid/generated.md").read_text(encoding="utf-8")

        self.assertNotIn("{{", rendered)
        self.assertEqual(expected, rendered)

    def test_cli_validates_a_bounded_mixed_state_set(self) -> None:
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
                    str(_FIXTURES / "valid/historical-unknown.md"),
                ]
            )

        self.assertEqual(0, result)
        self.assertIn("validated 2 documents", output.getvalue())

    def test_cli_returns_failure_with_exact_path_and_field(self) -> None:
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
        self.assertIn(f"{path}: Created-UTC:", output.getvalue())

    def test_cli_rejects_indented_provenance_opener(self) -> None:
        path = _FIXTURES / "invalid/indented-provenance.md"
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
        self.assertIn(f"{path}: Placement:", output.getvalue())

    def test_runtime_envelope_rejects_current_profile_inference(self) -> None:
        record = {
            "Artifact-ID": "artifact-invalid-envelope",
            "Created-UTC": "2026-08-08T18:45:00Z",
            "Creating-Agent": "Dev Documentation Writer",
            "Runtime": "Codex",
            "Dispatched-Model": "current-profile",
            "Reasoning-Effort": "high",
            "Task-ID": "task-invalid-envelope",
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "envelope.json"
            path.write_text(
                json.dumps({"schema_version": 1, "records": [record]}),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "inferred configuration"):
                load_runtime_envelope(path)

    def test_rejects_unsupported_document_formats_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "document.pdf"
            path.write_bytes(b"%PDF-1.7")

            findings = validate_document(
                path,
                state="new",
                copyright_statement=_COPYRIGHT,
                runtime_envelope=self.runtime_envelope,
            )

        self.assertEqual("Format", findings[0].field)


if __name__ == "__main__":
    unittest.main()
