# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies the Dev Merge Coordinator suite skill and claim-policy contract.

from __future__ import annotations

import tomllib
import unittest
from pathlib import Path

import yaml


SUITE_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = SUITE_ROOT.parents[2]


class DevMergeCoordinatorFixtureTests(unittest.TestCase):
    """Keep suite bindings aligned with the canonical merge coordinator contract."""

    def test_suite_required_skills_match_role_and_native_agent(self) -> None:
        """Keep fixed suite skills aligned with the canonical role and native instructions."""

        suite = yaml.safe_load((SUITE_ROOT / "suite.yaml").read_text(encoding="utf-8"))
        role = yaml.safe_load(
            (
                REPOSITORY_ROOT
                / suite["target"]["conceptualRole"]
            ).read_text(encoding="utf-8")
        )
        native_agent = tomllib.loads(
            (
                REPOSITORY_ROOT
                / suite["target"]["nativeAgent"]
            ).read_text(encoding="utf-8")
        )
        role_required_skills = {
            skill_id
            for entry in role["skills"]
            for skill_id, contract in entry.items()
            if "condition" not in contract
        }
        suite_required_skills = set(suite["target"]["requiredSkills"])

        self.assertEqual(role_required_skills, suite_required_skills)
        for skill_id in suite_required_skills:
            with self.subTest(skill=skill_id):
                self.assertIn(skill_id, native_agent["developer_instructions"])
        self.assertNotIn("resource-claim", suite_required_skills)
        self.assertEqual(
            "Resource coordination selects resource-claim.",
            suite["target"]["conditionalSkills"]["resource-claim"],
        )

    def test_suite_contract_branches_on_resource_coordination(self) -> None:
        """Require claims only for resource-claim projects and forbid them for none."""

        contract = (
            SUITE_ROOT
            / "skills"
            / "dev-merge-coordinator-suite-contract"
            / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "When project resource coordination selects resource-claim, integration mutation "
            "has an explicit claim lifecycle with claim-call and release evidence.",
            contract,
        )
        self.assertIn(
            "When project resource coordination selects none, integration mutation has zero "
            "claim calls and zero claim evidence.",
            contract,
        )
        self.assertNotIn(
            "Require an integration claim",
            contract,
        )


if __name__ == "__main__":
    unittest.main()
