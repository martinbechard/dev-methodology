#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Verifies OKF migration and validation for concept and reserved project-wiki pages.

"""Regression tests for OKF migration and validation."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from project_wiki_ops.core import lint_page
from project_wiki_ops.okf import (
    migrate_page_to_okf,
    split_frontmatter,
    validate_okf_page,
)

EXPECTED_NO_FINDINGS = 0
EXPECTED_ONE_FINDING = 1
PROVENANCE_COMMENT = """<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: artifact-reserved-page
Created-UTC: 2026-08-08T18:17:00Z
Creating-Agent: Wiki Writer
Runtime: Codex
Dispatched-Model: gpt-5.5
Reasoning-Effort: high
Task-ID: task-reserved-page
Artifact-ID-Evidence: runtime-supplied
Created-UTC-Evidence: runtime-supplied
Creating-Agent-Evidence: runtime-supplied
Runtime-Evidence: runtime-supplied
Dispatched-Model-Evidence: runtime-supplied
Reasoning-Effort-Evidence: runtime-supplied
Task-ID-Evidence: runtime-supplied
-->"""


class OkfMigrationTest(unittest.TestCase):
    def test_migrates_concept_page_with_inferred_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            page = root / "docs" / "wiki" / "techniques" / "token-counting.md"
            page.parent.mkdir(parents=True)
            page.write_text(
                "\n".join(
                    [
                        "# Token Counting",
                        "",
                        "## Current Understanding",
                        "",
                        "Token counting sizes prompts before model calls.",
                    ]
                ),
                encoding="utf-8",
            )

            result = migrate_page_to_okf(page)
            frontmatter, body, parsed = split_frontmatter(page.read_text(encoding="utf-8"))

        self.assertTrue(result.changed)
        self.assertTrue(parsed)
        self.assertEqual("Technique", frontmatter["type"])
        self.assertEqual("Token Counting", frontmatter["title"])
        self.assertEqual(["techniques"], frontmatter["tags"])
        self.assertTrue(body.startswith("# Token Counting"))

    def test_reserved_index_page_stays_without_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            page = Path(directory) / "docs" / "wiki" / "techniques" / "index.md"
            page.parent.mkdir(parents=True)
            page.write_text("# Techniques\n\n- [Token Counting](token-counting.md)\n", encoding="utf-8")

            result = migrate_page_to_okf(page)
            findings = validate_okf_page(page)

        self.assertFalse(result.changed)
        self.assertEqual(EXPECTED_NO_FINDINGS, len(findings))

    def test_reserved_index_and_log_accept_leading_provenance_comment(self) -> None:
        for filename, title in (("index.md", "Techniques"), ("log.md", "Change Log")):
            with self.subTest(filename=filename):
                with tempfile.TemporaryDirectory() as directory:
                    page = Path(directory) / "docs" / "wiki" / "techniques" / filename
                    page.parent.mkdir(parents=True)
                    page.write_text(
                        f"{PROVENANCE_COMMENT}\n# {title}\n",
                        encoding="utf-8",
                    )

                    findings = validate_okf_page(page)

                self.assertEqual(EXPECTED_NO_FINDINGS, len(findings))

    def test_reserved_page_rejects_malformed_leading_comment(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            page = Path(directory) / "docs" / "wiki" / "techniques" / "index.md"
            page.parent.mkdir(parents=True)
            page.write_text(
                "<!--\nCopyright (c) 2026 Martin.Bechard@DevConsult.ca\n# Techniques\n",
                encoding="utf-8",
            )

            findings = validate_okf_page(page)

        self.assertEqual(EXPECTED_ONE_FINDING, len(findings))
        self.assertIn("malformed leading HTML comment", findings[0].message)

    def test_reserved_page_with_provenance_still_rejects_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            page = Path(directory) / "docs" / "wiki" / "techniques" / "log.md"
            page.parent.mkdir(parents=True)
            page.write_text(
                f'{PROVENANCE_COMMENT}\n---\ntype: "Log"\n---\n# Change Log\n',
                encoding="utf-8",
            )

            findings = validate_okf_page(page)

        self.assertTrue(any("must not use frontmatter" in finding.message for finding in findings))

    def test_validation_requires_type_for_concepts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            page = Path(directory) / "docs" / "wiki" / "topic.md"
            page.parent.mkdir(parents=True)
            page.write_text("---\ntitle: Topic\n---\n\n# Topic\n", encoding="utf-8")

            findings = validate_okf_page(page)

        self.assertEqual(EXPECTED_ONE_FINDING, len(findings))
        self.assertIn("non-empty type", findings[0].message)

    def test_project_wiki_lint_reads_body_after_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            page = Path(directory) / "docs" / "wiki" / "topic.md"
            page.parent.mkdir(parents=True)
            page.write_text(
                "\n".join(
                    [
                        "---",
                        'type: "Topic"',
                        "---",
                        "",
                        "# Topic",
                        "",
                        "## Current Understanding",
                        "",
                        "## Authoritative Sources",
                        "",
                        "## Related Code",
                        "",
                        "## Related Tests",
                        "",
                        "## Related Backlog Items",
                        "",
                        "## Related Wiki Pages",
                        "",
                        "## Open Questions",
                        "",
                        "## Maintenance Notes",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            findings = lint_page(page)

        self.assertEqual(EXPECTED_NO_FINDINGS, len(findings))

    def test_description_skips_comments_and_uses_plain_link_text(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            page = Path(directory) / "docs" / "wiki" / "source-workflows" / "raw-monitor.md"
            page.parent.mkdir(parents=True)
            page.write_text(
                "\n".join(
                    [
                        "# Raw Monitor",
                        "",
                        "<!-- generated note -->",
                        "",
                        "## Current Understanding",
                        "",
                        "The raw monitor checks [Clippings](../../../Clippings) before raw files.",
                    ]
                ),
                encoding="utf-8",
            )

            migrate_page_to_okf(page)
            frontmatter, _body, _parsed = split_frontmatter(page.read_text(encoding="utf-8"))

        self.assertEqual("The raw monitor checks Clippings before raw files.", frontmatter["description"])


if __name__ == "__main__":
    unittest.main()
