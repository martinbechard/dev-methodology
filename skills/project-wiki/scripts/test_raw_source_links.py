#!/usr/bin/env python3
"""Regression tests for raw source link portability."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from project_wiki_ops.core import broken_link_findings

EXPECTED_FINDING_COUNT = 1


class RawSourceLinkTest(unittest.TestCase):
    def test_absolute_raw_link_fails_even_when_target_exists(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "raw" / "processed" / "source.md"
            source.parent.mkdir(parents=True)
            source.write_text("# Source\n", encoding="utf-8")
            page = root / "docs" / "wiki" / "topic.md"
            page.parent.mkdir(parents=True)
            text = f"- [source]({source})\n"

            findings = broken_link_findings(page, text)

        self.assertEqual(EXPECTED_FINDING_COUNT, len(findings))
        self.assertIn("raw source link must be relative, not absolute", findings[0].message)

    def test_non_raw_absolute_link_can_pass_when_target_exists(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            automation = root / ".agents" / "automations" / "ai-dev-wiki-raw-project-wiki-monitor" / "automation.toml"
            automation.parent.mkdir(parents=True)
            automation.write_text("[automation]\n", encoding="utf-8")
            page = root / "docs" / "wiki" / "topic.md"
            page.parent.mkdir(parents=True)
            text = f"- [automation]({automation})\n"

            findings = broken_link_findings(page, text)

        self.assertEqual([], findings)


if __name__ == "__main__":
    unittest.main()
