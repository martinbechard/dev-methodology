#!/usr/bin/env python3
"""Regression tests for leaf-to-wiki backlink insertion."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from project_wiki_ops.core import apply_leaf_links_to_page_texts
from project_wiki_ops.models import LeafPage

EXPECTED_CHANGE_COUNT = 2


class LeafLinkingTest(unittest.TestCase):
    def test_links_longest_leaf_titles_with_relative_targets(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "docs" / "wiki" / "overview.md"
            target.parent.mkdir(parents=True)
            company_leaf = root / "docs" / "wiki" / "companies" / "example-labs.md"
            framework_leaf = root / "docs" / "wiki" / "agentic-frameworks" / "example-agent-sdk.md"
            leaves = [
                LeafPage(path=company_leaf, title="Example Labs"),
                LeafPage(path=framework_leaf, title="Example Agent SDK"),
            ]
            page_texts = {
                target: "Example Agent SDK builds on Example Labs platform patterns.\n",
                company_leaf: "# Example Labs\n",
                framework_leaf: "# Example Agent SDK\n",
            }

            updated_texts, changes = apply_leaf_links_to_page_texts(leaves, page_texts)

        self.assertEqual(EXPECTED_CHANGE_COUNT, len(changes))
        self.assertEqual(
            "[Example Agent SDK](agentic-frameworks/example-agent-sdk.md) builds on [Example Labs](companies/example-labs.md) platform patterns.\n",
            updated_texts[target],
        )

    def test_does_not_relink_page_that_already_links_leaf(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "docs" / "wiki" / "products" / "overview.md"
            target.parent.mkdir(parents=True)
            leaf = root / "docs" / "wiki" / "companies" / "example-labs.md"
            leaves = [LeafPage(path=leaf, title="Example Labs")]
            page_texts = {
                target: "The [Example Labs](../companies/example-labs.md) page tracks Example Labs company context.\n",
                leaf: "# Example Labs\n",
            }

            updated_texts, changes = apply_leaf_links_to_page_texts(leaves, page_texts)

        self.assertEqual([], changes)
        self.assertEqual(page_texts[target], updated_texts[target])


if __name__ == "__main__":
    unittest.main()
