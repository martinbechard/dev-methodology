#!/usr/bin/env python3
"""Regression tests for project wiki open-question extraction."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from project_wiki_ops.core import extract_open_questions_from_page

EXPECTED_QUESTION_COUNT = 3
FIRST_QUESTION_LINE = 5


class OpenQuestionsTest(unittest.TestCase):
    def test_extracts_questions_and_ignores_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            page = Path(directory) / "topic.md"
            page.write_text(
                "\n".join(
                    [
                        "# Topic",
                        "",
                        "## Open Questions",
                        "",
                        "- Which runtime should be the default?",
                        "- Should multi-line questions keep",
                        "  their continuation text?",
                        "- No open wiki questions are recorded for another topic.",
                        "- Which security model should be reviewed first?",
                        "",
                        "## Maintenance Notes",
                        "",
                        "- Created for testing.",
                    ]
                ),
                encoding="utf-8",
            )

            questions = extract_open_questions_from_page(page)

        self.assertEqual(EXPECTED_QUESTION_COUNT, len(questions))
        self.assertEqual(FIRST_QUESTION_LINE, questions[0].line)
        self.assertEqual("Which runtime should be the default?", questions[0].question)
        self.assertEqual("Should multi-line questions keep their continuation text?", questions[1].question)
        self.assertEqual("Which security model should be reviewed first?", questions[2].question)


if __name__ == "__main__":
    unittest.main()
