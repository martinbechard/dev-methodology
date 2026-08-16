# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies file and repository skill token estimation behavior.

from __future__ import annotations

import csv
import io
import tempfile
import unittest
from pathlib import Path

from estimate_file_tokens import estimate_tokens
from estimate_skill_tokens import estimate_skill_tokens, iter_skill_files, write_csv


class _WordEncoder:
    def encode(self, text: str, *, disallowed_special: tuple[()] = ()) -> list[int]:
        del disallowed_special
        return list(range(len(text.split())))


class EstimateFileTokensTests(unittest.TestCase):
    def test_estimates_utf8_file_with_supplied_encoder(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "sample.txt"
            path.write_text("one two café", encoding="utf-8")

            self.assertEqual(3, estimate_tokens(path, encoder=_WordEncoder()))


class EstimateSkillTokensTests(unittest.TestCase):
    def test_discovers_only_private_and_publishable_skill_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            private = root / ".agents" / "skills" / "private-one" / "SKILL.md"
            publishable = root / "skills" / "public-one" / "SKILL.md"
            ignored = root / "other" / "SKILL.md"
            for path in (private, publishable, ignored):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(path.parent.name, encoding="utf-8")

            discovered = list(iter_skill_files(root))

            self.assertEqual(
                [("private", private), ("publishable", publishable)], discovered
            )

    def test_estimates_each_discovered_skill_with_shared_encoder(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            private = root / ".agents" / "skills" / "private-one" / "SKILL.md"
            publishable = root / "skills" / "public-one" / "SKILL.md"
            private.parent.mkdir(parents=True)
            publishable.parent.mkdir(parents=True)
            private.write_text("one two", encoding="utf-8")
            publishable.write_text("one two three", encoding="utf-8")

            estimates = estimate_skill_tokens(root, encoder=_WordEncoder())

            self.assertEqual(
                [
                    ("private", private.relative_to(root), 2),
                    ("publishable", publishable.relative_to(root), 3),
                ],
                estimates,
            )

    def test_writes_rectangular_csv_with_quoted_paths(self) -> None:
        output = io.StringIO(newline="")

        write_csv(
            [("publishable", Path("skills/public,one/SKILL.md"), 42)], output
        )

        self.assertEqual(
            [
                ["visibility", "path", "tokens"],
                ["publishable", "skills/public,one/SKILL.md", "42"],
            ],
            list(csv.reader(io.StringIO(output.getvalue()))),
        )


if __name__ == "__main__":
    unittest.main()
