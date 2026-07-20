# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies that every suite-local Dev Coder fixture is executable and internally consistent.

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

import yaml


SUITE_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = SUITE_ROOT.parents[2]


class DevCoderFixtureTests(unittest.TestCase):
    """Verify the executable fixtures and contracts used by the Dev Coder suite."""

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

    def test_contract_narrowing_guidance_and_typescript_scenario_are_explicit(self) -> None:
        """Require source guidance and Judge inputs to preserve the authorized numeric domain."""

        skill_expectations = {
            "code-discovery": (
                "Separate explicit public constraints in accepted authority from "
                "implementation conveniences, representation choices, and inferred preferences."
            ),
            "careful-coding": (
                "Preserve every public input and output value allowed by accepted authority "
                "unless the user or a stronger accepted source authorizes narrowing it."
            ),
            "test-driven-development": (
                "Do not encode implementation conveniences or inferred restrictions as "
                "invalid-input expectations."
            ),
        }
        for skill_id, expectation in skill_expectations.items():
            skill_text = (REPOSITORY_ROOT / "skills" / skill_id / "SKILL.md").read_text()
            self.assertIn(expectation, skill_text)

        scenario_catalog = yaml.safe_load((SUITE_ROOT / "scenarios.yaml").read_text())
        scenario = next(
            item
            for item in scenario_catalog["scenarios"]
            if item["id"] == "typescript-behavior-change"
        )
        self.assertIn(
            "Preserve the inclusive zero-through-one-hundred dependency contract, including 12.5 percent.",
            scenario["requiredBehaviors"],
        )
        self.assertIn(
            "Test zero and one hundred percent boundaries, out-of-range and non-finite dependency results, cent rounding, and propagated dependency rejection.",
            scenario["requiredBehaviors"],
        )
        self.assertIn(
            "Reject an in-range fractional percentage because integer-cent arithmetic is simpler.",
            scenario["forbiddenBehaviors"],
        )

        task_text = (
            REPOSITORY_ROOT / "evals" / "projects" / "typescript-order-pricing" / "TASK.md"
        ).read_text()
        for expectation in (
            "including fractional values such as 12.5",
            "zero and one hundred percent boundary results",
            "out-of-range and non-finite dependency results",
            "round the final discounted total to the nearest cent",
            "Propagate coupon dependency failures to the caller.",
        ):
            self.assertIn(expectation, task_text)


if __name__ == "__main__":
    unittest.main()
