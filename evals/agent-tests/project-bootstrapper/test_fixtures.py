# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies the observable initial contracts for all Project Bootstrapper fixtures.

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


SUITE_ROOT = Path(__file__).resolve().parent


def run_fixture(fixture_name: str, *arguments: str) -> subprocess.CompletedProcess[str]:
    """Run a bootstrap fixture command with captured output."""

    return subprocess.run(
        [sys.executable, *arguments],
        cwd=SUITE_ROOT / "fixtures" / fixture_name,
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )


class ProjectBootstrapperFixtureTests(unittest.TestCase):
    def test_valid_direct_path_has_valid_configuration_and_one_missing_document(self) -> None:
        completed = run_fixture(
            "valid-configuration-direct-path", "validate_fixture.py", "initial"
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        evidence = json.loads(completed.stdout)
        self.assertTrue(evidence["configurationValid"])
        self.assertTrue(evidence["acceptedConfigurationReview"])
        self.assertFalse(evidence["moduleDocumentPresent"])

    def test_missing_configuration_path_starts_without_setup_artifacts(self) -> None:
        completed = run_fixture(
            "missing-configuration-multi-contribution", "validate_fixture.py", "initial"
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        self.assertFalse(any(json.loads(completed.stdout).values()))

    def test_invalid_configuration_reports_both_expected_errors(self) -> None:
        completed = run_fixture(
            "invalid-configuration-no-authority", "validate_fixture.py"
        )
        self.assertEqual(2, completed.returncode, completed.stdout + completed.stderr)
        errors = json.loads(completed.stdout)["errors"]
        self.assertEqual(
            [
                "conceptual agent does not exist: missing-conceptual-agent",
                "configured folder does not exist: src/missing-module",
            ],
            errors,
        )

    def test_fixture_source_tests_are_green(self) -> None:
        direct = run_fixture(
            "valid-configuration-direct-path", "-m", "unittest", "test_inventory.py"
        )
        multi = run_fixture(
            "missing-configuration-multi-contribution",
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
        )
        self.assertEqual(0, direct.returncode, direct.stdout + direct.stderr)
        self.assertEqual(0, multi.returncode, multi.stdout + multi.stderr)


if __name__ == "__main__":
    unittest.main()
