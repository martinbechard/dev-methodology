# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies that every suite-local Dev Coder fixture is executable and internally consistent.

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


SUITE_ROOT = Path(__file__).resolve().parent


class DevCoderFixtureTests(unittest.TestCase):
    def test_conflicting_contract_fixture_preserves_accepted_behavior(self) -> None:
        fixture = SUITE_ROOT / "fixtures" / "insufficient-contract-authority"
        contract = json.loads((fixture / "accepted-contract.json").read_text())

        self.assertEqual("percentage from 0 through 30", contract["discountMeaning"])
        self.assertEqual("unsupported", contract["fixedAmountDiscounts"])
        completed = subprocess.run(
            [sys.executable, "-m", "unittest", "test_pricing.py"],
            cwd=fixture,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)


if __name__ == "__main__":
    unittest.main()
