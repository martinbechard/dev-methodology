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
import sys
import tempfile
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = Path(__file__).with_name("contract.py")
SPEC = importlib.util.spec_from_file_location("design_system_runner_contract", MODULE_PATH)
assert SPEC and SPEC.loader
contract = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(contract)

AGENT_TEST_ROOT = ROOT / "evals" / "agent-tests"
sys.path.insert(0, str(AGENT_TEST_ROOT))
try:
    RUNNER_SPEC = importlib.util.spec_from_file_location(
        "documentation_design_system_suite_runner",
        AGENT_TEST_ROOT / "runner.py",
    )
    assert RUNNER_SPEC and RUNNER_SPEC.loader
    suite_runner = importlib.util.module_from_spec(RUNNER_SPEC)
    sys.modules[RUNNER_SPEC.name] = suite_runner
    RUNNER_SPEC.loader.exec_module(suite_runner)
finally:
    sys.path.remove(str(AGENT_TEST_ROOT))


class ChecklistRunnerContractTests(unittest.TestCase):
    """Exercise the runner report and role boundaries without invoking a model."""

    def _report(self, results: list[str]) -> dict[str, object]:
        """Build one strict report for the supplied ordered result values."""

        return {
            "status": "NOT TESTED" if "NOT TESTED" in results else "FAIL" if "FAIL" in results else "PASS",
            "page": "page.html",
            "checklist": "Shared",
            "checks": [
                {"id": f"DDS-TST-{index:03d}", "result": result, "evidence": f"evidence {index}"}
                for index, result in enumerate(results, start=1)
            ],
            "findings": [
                {"id": f"DDS-TST-{index:03d}", "remediation": f"correct item {index}"}
                for index, result in enumerate(results, start=1)
                if result == "FAIL"
            ],
            "limits": [
                {"id": f"DDS-TST-{index:03d}", "missingEvidence": f"missing evidence {index}"}
                for index, result in enumerate(results, start=1)
                if result == "NOT TESTED"
            ],
        }

    def _validate(self, report: object, ids: tuple[str, ...] | None = None) -> tuple[str, ...]:
        """Validate one report against the class's exact assignment identity."""

        expected_ids = ids or tuple(check["id"] for check in report["checks"])
        return contract.validate_report("page.html", "Shared", expected_ids, report)

    def test_statuses_are_derived_from_item_results(self) -> None:
        """PASS, FAIL, and NOT TESTED must follow the strict precedence rule."""

        for results in (
            ["PASS"],
            ["PASS", "FAIL"],
            ["PASS", "NOT TESTED"],
            ["FAIL", "NOT TESTED"],
        ):
            report = self._report(list(results))
            with self.subTest(results=results):
                self.assertEqual((), self._validate(report))

    def test_missing_duplicate_and_extra_items_are_rejected(self) -> None:
        """Every assigned item must occur exactly once and no other item may appear."""

        report = self._report(["PASS", "PASS"])
        report["checks"].append(dict(report["checks"][0]))
        report["checks"].append({"id": "DDS-TST-999", "result": "PASS", "evidence": "extra"})
        errors = self._validate(
            report,
            ("DDS-TST-001", "DDS-TST-002", "DDS-TST-003"),
        )
        self.assertIn("duplicate checklist item DDS-TST-001", errors)
        self.assertIn("missing checklist item DDS-TST-003", errors)
        self.assertIn("unexpected checklist item DDS-TST-999", errors)

    def test_assignment_identity_is_exact_and_non_empty(self) -> None:
        """Empty assignments and reports for another page or checklist are malformed."""

        report = self._report(["PASS"])
        self.assertIn(
            "assigned checklist identifiers must not be empty",
            contract.validate_report("page.html", "Shared", (), report),
        )
        wrong_page = {**report, "page": "other.html"}
        wrong_checklist = {**report, "checklist": "Content"}
        self.assertIn("page must match the assigned page", self._validate(wrong_page))
        self.assertIn("checklist must match the assigned checklist", self._validate(wrong_checklist))

    def test_malformed_or_null_reports_return_errors_without_crashing(self) -> None:
        """Untrusted output shape errors are bounded contract failures."""

        malformed_reports = (
            None,
            [],
            {},
            {"checks": None},
            {**self._report(["PASS"]), "status": []},
            {
                **self._report(["PASS"]),
                "checks": [
                    {"id": "DDS-TST-001", "result": [], "evidence": "evidence"}
                ],
            },
            {**self._report(["PASS"]), "checks": [None]},
            {**self._report(["PASS"]), "findings": [[]]},
            {**self._report(["PASS"]), "limits": {"id": "DDS-TST-001"}},
        )
        for report in malformed_reports:
            with self.subTest(report=report):
                errors = contract.validate_report(
                    "page.html",
                    "Shared",
                    ("DDS-TST-001",),
                    report,
                )
                self.assertTrue(errors)

    def test_malformed_assignment_shapes_return_errors_without_crashing(self) -> None:
        """Null, whitespace, mixed-type, and unhashable assignment values fail closed."""

        report = self._report(["PASS"])
        malformed_assignments = (
            (None, "Shared", ("DDS-TST-001",)),
            ("page.html", [], ("DDS-TST-001",)),
            ("   ", "Shared", ("DDS-TST-001",)),
            ("page.html", "Shared", None),
            ("page.html", "Shared", "DDS-TST-001"),
            ("page.html", "Shared", ("DDS-TST-001", [])),
            ("page.html", "Shared", ("DDS-TST-001", "  ")),
        )
        for page, checklist, checklist_ids in malformed_assignments:
            with self.subTest(
                page=page,
                checklist=checklist,
                checklist_ids=checklist_ids,
            ):
                errors = contract.validate_report(
                    page,
                    checklist,
                    checklist_ids,
                    report,
                )
                self.assertTrue(errors)

    def test_findings_and_limits_are_typed_and_cover_their_results(self) -> None:
        """Every FAIL has actionable remediation and every NOT TESTED has a missing-evidence limit."""

        failed = self._report(["FAIL"])
        failed["findings"] = []
        self.assertIn("FAIL item DDS-TST-001 needs an actionable finding", self._validate(failed))
        untested = self._report(["NOT TESTED"])
        untested["limits"] = []
        self.assertIn("NOT TESTED item DDS-TST-001 needs a missing-evidence limit", self._validate(untested))
        malformed = self._report(["PASS"])
        malformed["findings"] = None
        malformed["limits"] = "none"
        errors = self._validate(malformed)
        self.assertIn("findings must be a list", errors)
        self.assertIn("limits must be a list", errors)

    def test_unavailable_input_report_uses_the_expected_inventory(self) -> None:
        """Unavailable evidence must retain every coordinator-owned item as NOT TESTED."""

        report = contract.build_not_tested_report(
            "page.html",
            "Shared",
            ("DDS-TST-001", "DDS-TST-002"),
            "rendered page unavailable",
        )
        self.assertEqual((), self._validate(report))
        self.assertEqual(["NOT TESTED", "NOT TESTED"], [item["result"] for item in report["checks"]])
        with self.assertRaisesRegex(ValueError, "must not be empty"):
            contract.build_not_tested_report("page.html", "Shared", (), "missing")

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

    def test_suite_wires_its_specific_contract_and_counterexample_scenarios(self) -> None:
        """The runner suite must stage its own semantic contract and adverse input cases."""

        suite_root = Path(__file__).parent
        suite = yaml.safe_load((suite_root / "suite.yaml").read_text(encoding="utf-8"))
        self.assertEqual(
            ["skills/methodology-design-system-checklist-runner-suite-contract/SKILL.md"],
            suite["projectSkills"]["suite"],
        )
        self.assertTrue((suite_root / suite["projectSkills"]["suite"][0]).is_file())
        scenario_document = yaml.safe_load(
            (suite_root / "scenarios.yaml").read_text(encoding="utf-8")
        )
        for scenario in scenario_document["scenarios"]:
            self.assertIs(True, scenario["requiresWorkspaceInventory"])
            self.assertIs(True, scenario["requiresNoDetectedMutation"])
        scenarios = (suite_root / "scenarios.yaml").read_text(encoding="utf-8")
        for phrase in (
            "wrong page or checklist identity",
            "malformed or empty output",
            "unavailable supplied input",
            "FAIL and NOT TESTED",
        ):
            self.assertIn(phrase, scenarios)

        suite_skill = "methodology-design-system-checklist-runner-suite-contract"
        for agent_name in ("supervisor.toml", "judge.toml"):
            agent_text = (suite_root / "agents" / agent_name).read_text(encoding="utf-8")
            self.assertIn(suite_skill, agent_text)

    def test_every_scenario_resolves_and_stages_its_workspace_inventory(self) -> None:
        """Every inventory-enforced scenario must stage from a real suite-local fixture."""

        suite_root = Path(__file__).parent
        manifest = yaml.safe_load((suite_root / "suite.yaml").read_text(encoding="utf-8"))
        scenarios = tuple(
            yaml.safe_load((suite_root / "scenarios.yaml").read_text(encoding="utf-8"))["scenarios"]
        )
        suite = suite_runner._Suite(
            suite_id=manifest["id"],
            priority=manifest["priority"],
            path=suite_root,
            manifest=manifest,
            scenarios=scenarios,
        )
        run = suite_runner._RunSpec(
            suite=suite,
            scenario_ids=tuple(scenario["id"] for scenario in scenarios),
        )
        with tempfile.TemporaryDirectory() as directory:
            temporary_root = Path(directory)
            fixture_root = temporary_root / "fixtures"
            checkpoint_root = temporary_root / "checkpoints"
            fixture_root.mkdir()
            checkpoint_root.mkdir()
            baselines = suite_runner._stage_workspace_inventory_fixtures(
                (run,),
                fixture_root,
                checkpoint_root,
            )

            expected_keys = {(suite.suite_id, scenario["id"]) for scenario in scenarios}
            self.assertEqual(expected_keys, set(baselines))
            for scenario in scenarios:
                with self.subTest(scenario=scenario["id"]):
                    self.assertIs(True, scenario["requiresWorkspaceInventory"])
                    self.assertIs(True, scenario["requiresNoDetectedMutation"])
                    self.assertTrue((suite_root / scenario["executableCase"]).is_dir())
                    staged_root = fixture_root / suite.suite_id / scenario["id"]
                    self.assertTrue((staged_root / ".git").is_dir())
                    self.assertTrue((staged_root / "TASK.md").is_file())
                    self.assertTrue(
                        (
                            checkpoint_root
                            / suite.suite_id
                            / scenario["id"]
                            / "artifacts"
                            / "workspace-baseline.json"
                        ).is_file()
                    )


if __name__ == "__main__":
    unittest.main()
