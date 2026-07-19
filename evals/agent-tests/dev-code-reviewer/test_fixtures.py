# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies the clean and evidence-limited Dev Code Reviewer fixtures.

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


SUITE_ROOT = Path(__file__).resolve().parent


class DevCodeReviewerFixtureTests(unittest.TestCase):
    def run_fixture_tests(self, fixture_name: str, test_file: str) -> None:
        fixture = SUITE_ROOT / "fixtures" / fixture_name
        completed = subprocess.run(
            [sys.executable, "-m", "unittest", test_file],
            cwd=fixture,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)

    def test_clean_review_fixture_is_green(self) -> None:
        self.run_fixture_tests("justified-clean-review", "test_retry_policy.py")

    def test_incomplete_review_fixture_exposes_missing_upgrade_evidence(self) -> None:
        fixture = SUITE_ROOT / "fixtures" / "incomplete-review-evidence"
        status = json.loads((fixture / "upgrade-fixture-status.json").read_text())

        self.assertEqual("unavailable", status["status"])
        self.assertEqual(1, status["requiredVersion"])
        self.run_fixture_tests("incomplete-review-evidence", "test_migration.py")


if __name__ == "__main__":
    unittest.main()
