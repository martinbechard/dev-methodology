# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies report-relative Wiki Researcher source-link generation and validation.

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SUITE_ROOT = Path(__file__).resolve().parent
VALIDATOR_PATH = SUITE_ROOT / "fixtures" / "wiki-research" / "validate_links.py"
_SPEC = importlib.util.spec_from_file_location("wiki_research_link_validator", VALIDATOR_PATH)
assert _SPEC is not None and _SPEC.loader is not None
_VALIDATOR = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_VALIDATOR)


class WikiResearchSourceLinkTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.repository = Path(self.temporary_directory.name)
        (self.repository / "sources" / "nested").mkdir(parents=True)
        (self.repository / "raw" / "moved").mkdir(parents=True)
        (self.repository / "conflicting-sources.md").write_text("# Conflicts\n", encoding="utf-8")
        (self.repository / "sources" / "nested" / "policy.md").write_text(
            "# Policy\n", encoding="utf-8"
        )
        (self.repository / "sources" / "nested" / "policy_(draft).md").write_text(
            "# Draft policy\n", encoding="utf-8"
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_root_report_preserves_root_source_path(self) -> None:
        report = self.repository / "research.md"
        source = self.repository / "conflicting-sources.md"

        self.assertEqual(
            "conflicting-sources.md",
            _VALIDATOR.relative_source_link(report, source, self.repository),
        )

    def test_nested_report_resolves_root_and_nested_sources_from_final_location(self) -> None:
        report = self.repository / "raw" / "research.md"
        report.write_text(
            "[conflict](../conflicting-sources.md)\n"
            "[policy][policy-source]\n"
            "[policy-source]: ../sources/nested/policy.md#cadence\n"
            "[draft](../sources/nested/policy_(draft).md)\n"
            "[escaped draft](../sources/nested/policy_\\(draft\\).md)\n"
            "[public](https://example.invalid/policy)\n",
            encoding="utf-8",
        )

        self.assertEqual((), _VALIDATOR.validate_report_links(report, self.repository))
        completed = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR_PATH),
                str(report),
                "--repository-root",
                str(self.repository),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)

    def test_moved_report_requires_links_relative_to_its_new_parent(self) -> None:
        report = self.repository / "raw" / "moved" / "research.md"
        report.write_text("[policy](../../sources/nested/policy.md)\n", encoding="utf-8")

        self.assertEqual((), _VALIDATOR.validate_report_links(report, self.repository))
        report.write_text("[policy](../sources/nested/policy.md)\n", encoding="utf-8")
        self.assertEqual(
            ("local link does not resolve from report: ../sources/nested/policy.md",),
            _VALIDATOR.validate_report_links(report, self.repository),
        )

    def test_collision_safe_name_does_not_change_link_correctness(self) -> None:
        source = self.repository / "conflicting-sources.md"
        first = self.repository / "raw" / "2026-07-20-dependency-policy.md"
        collision_safe = self.repository / "raw" / "2026-07-20-dependency-policy-2.md"
        first.write_text("occupied\n", encoding="utf-8")
        link = _VALIDATOR.relative_source_link(collision_safe, source, self.repository)
        collision_safe.write_text(f"[conflict]({link})\n", encoding="utf-8")

        self.assertEqual("../conflicting-sources.md", link)
        self.assertEqual((), _VALIDATOR.validate_report_links(collision_safe, self.repository))

    def test_required_validation_fails_cleanly_for_missing_local_source(self) -> None:
        report = self.repository / "raw" / "research.md"
        report.write_text(
            "[missing](../sources/missing.md)\n[mail](mailto:owner@example.invalid)\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            _VALIDATOR.SourceLinkValidationError,
            "local link does not resolve from report",
        ):
            _VALIDATOR.require_valid_report_links(report, self.repository)
        completed = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR_PATH),
                str(report),
                "--repository-root",
                str(self.repository),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(1, completed.returncode)
        self.assertIn("local link does not resolve from report", completed.stdout)


if __name__ == "__main__":
    unittest.main()
