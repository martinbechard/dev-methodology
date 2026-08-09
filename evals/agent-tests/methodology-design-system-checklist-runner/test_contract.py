"""
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
AI attribution: Generated with AI assistance.
Responsibility: Tests strict runner statuses, complete exactly-once coverage, and the conceptual no-delegation boundary.
Design: agents/roles/methodology-maintenance/methodology-design-system-checklist-runner.role.yaml
Tests: evals/agent-tests/methodology-design-system-checklist-runner/test_contract.py
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = Path(__file__).with_name("contract.py")
SPEC = importlib.util.spec_from_file_location("design_system_runner_contract", MODULE_PATH)
assert SPEC and SPEC.loader
contract = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(contract)


class ChecklistRunnerContractTests(unittest.TestCase):
    """Exercise the runner report and role boundaries without invoking a model."""

    def _report(self, results: list[str]) -> dict[str, object]:
        """Build one strict report for the supplied ordered result values."""

        return {
            "status": "FAIL" if "FAIL" in results else "NOT TESTED" if "NOT TESTED" in results else "PASS",
            "page": "page.html",
            "checklist": "Shared",
            "checks": [
                {"id": f"DDS-TST-{index:03d}", "result": result, "evidence": f"evidence {index}"}
                for index, result in enumerate(results, start=1)
            ],
            "findings": [],
            "limits": [],
        }

    def test_statuses_are_derived_from_item_results(self) -> None:
        """PASS, FAIL, and NOT TESTED must follow the strict precedence rule."""

        for results in (["PASS"], ["PASS", "FAIL"], ["PASS", "NOT TESTED"]):
            report = self._report(list(results))
            checklist_ids = [check["id"] for check in report["checks"]]
            with self.subTest(results=results):
                self.assertEqual((), contract.validate_report(checklist_ids, report))

    def test_missing_duplicate_and_extra_items_are_rejected(self) -> None:
        """Every assigned item must occur exactly once and no other item may appear."""

        report = self._report(["PASS", "PASS"])
        report["checks"].append(dict(report["checks"][0]))
        report["checks"].append({"id": "DDS-TST-999", "result": "PASS", "evidence": "extra"})
        errors = contract.validate_report(("DDS-TST-001", "DDS-TST-002", "DDS-TST-003"), report)
        self.assertIn("duplicate checklist item DDS-TST-001", errors)
        self.assertIn("missing checklist item DDS-TST-003", errors)
        self.assertIn("unexpected checklist item DDS-TST-999", errors)

    def test_role_has_one_local_skill_and_no_dependency_or_delegation(self) -> None:
        """The conceptual runner must remain isolated, read-only, and non-delegating."""

        role_path = ROOT / "agents/roles/methodology-maintenance/methodology-design-system-checklist-runner.role.yaml"
        role = yaml.safe_load(role_path.read_text(encoding="utf-8"))
        instructions = " ".join(
            str(value)
            for section in role["instructions"].values()
            for value in (section if isinstance(section, list) else [section])
        )
        self.assertEqual("never", role["repositoryMutation"])
        self.assertEqual("read-only", role["isolation"])
        self.assertEqual(["review-documentation-design-system"], [next(iter(item)) for item in role["skills"]])
        self.assertNotIn("agentDependencies", role)
        self.assertIn("Do not expand the assignment, delegate work, invoke another agent", instructions)


if __name__ == "__main__":
    unittest.main()
