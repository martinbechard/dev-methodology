"""
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
AI attribution: Generated with AI assistance.
Responsibility: Tests coordinator coverage, retry, reconciliation, conflict, cost, and deterministic ranking boundaries.
Design: agents/roles/methodology-maintenance/methodology-design-system-review-coordinator.role.yaml
Tests: evals/agent-tests/methodology-design-system-review-coordinator/test_coordination_simulator.py
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest
from decimal import Decimal

import yaml


MODULE_PATH = Path(__file__).with_name("coordination_simulator.py")
SPEC = importlib.util.spec_from_file_location("design_system_coordination_simulator", MODULE_PATH)
assert SPEC and SPEC.loader
subject = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(subject)


class DesignSystemCoordinatorTests(unittest.TestCase):
    """Exercise every required coordinator decision without a live model call."""

    assignment = ("page.html", "Shared", ("DDS-COM-001", "DDS-COM-002"))

    def _report(self, results: tuple[str, str] = ("PASS", "PASS")) -> dict[str, object]:
        """Build one strict runner report for the class assignment."""

        status = "NOT TESTED" if "NOT TESTED" in results else "FAIL" if "FAIL" in results else "PASS"
        return {
            "status": status,
            "page": "page.html",
            "checklist": "Shared",
            "checks": [
                {"id": check_id, "result": result, "evidence": f"evidence {index}"}
                for index, (check_id, result) in enumerate(zip(self.assignment[2], results, strict=True), start=1)
            ],
            "findings": [
                {"id": check_id, "remediation": f"correct {check_id}"}
                for check_id, result in zip(self.assignment[2], results, strict=True)
                if result == "FAIL"
            ],
            "limits": [
                {"id": check_id, "missingEvidence": f"obtain evidence for {check_id}"}
                for check_id, result in zip(self.assignment[2], results, strict=True)
                if result == "NOT TESTED"
            ],
        }

    def test_complete_pass_and_confirmed_failure(self) -> None:
        """Complete PASS accepts and a complete confirmed FAIL rejects."""

        key = subject.assignment_key(self.assignment)
        accepted = subject.coordinate((self.assignment,), {key: [self._report()]})
        rejected = subject.coordinate((self.assignment,), {key: [self._report(("PASS", "FAIL"))]})
        self.assertEqual("ACCEPTED", accepted["status"])
        self.assertEqual("REJECTED", rejected["status"])
        self.assertEqual(
            {
                "status",
                "coverage",
                "reconciledFindings",
                "evidenceConflicts",
                "acceptanceRationale",
                "modelEvalRanking",
                "runnerReports",
            },
            set(accepted),
        )

    def test_missing_unavailable_and_not_tested_are_blocked(self) -> None:
        """The coordinator must never fill unavailable or incomplete runner evidence itself."""

        key = subject.assignment_key(self.assignment)
        self.assertEqual("BLOCKED", subject.coordinate((self.assignment,), {})["status"])
        self.assertEqual("BLOCKED", subject.coordinate((self.assignment,), {}, unavailable=(key,))["status"])
        incomplete = subject.coordinate((self.assignment,), {key: [self._report(("PASS", "NOT TESTED"))]})
        self.assertEqual("BLOCKED", incomplete["status"])
        mixed = subject.coordinate((self.assignment,), {key: [self._report(("FAIL", "NOT TESTED"))]})
        self.assertEqual("BLOCKED", mixed["status"])

    def test_one_malformed_retry_can_recover_but_two_cannot(self) -> None:
        """Exactly one corrected retry is accepted after an initially malformed report."""

        key = subject.assignment_key(self.assignment)
        malformed = {**self._report(), "checks": []}
        recovered = subject.coordinate((self.assignment,), {key: [malformed, self._report()]})
        blocked = subject.coordinate((self.assignment,), {key: [malformed, malformed]})
        self.assertEqual("ACCEPTED", recovered["status"])
        self.assertEqual(2, recovered["runnerReports"][0]["attempts"])
        self.assertEqual("BLOCKED", blocked["status"])

        wrong_identity = {**self._report(), "page": "wrong.html"}
        wrong_identity_blocked = subject.coordinate(
            (self.assignment,),
            {key: [wrong_identity, wrong_identity]},
        )
        self.assertEqual("BLOCKED", wrong_identity_blocked["status"])

    def test_duplicate_findings_are_deduplicated_and_conflicts_are_preserved(self) -> None:
        """Identical findings collapse while contradictory material item results block."""

        key = subject.assignment_key(self.assignment)
        report = self._report(("PASS", "FAIL"))
        finding = {"id": "DDS-COM-002", "remediation": "Match the version."}
        report["findings"] = [finding, dict(finding)]
        result = subject.coordinate((self.assignment,), {key: [report]})
        self.assertEqual(1, len(result["reconciledFindings"]))
        conflict = subject.coordinate(
            (self.assignment,),
            {key: [self._report()]},
            extra_claims=(
                {"page": "page.html", "checklist": "Shared", "id": "DDS-COM-001", "result": "FAIL", "evidence": "contrary source", "source": "secondary"},
            ),
        )
        self.assertEqual("BLOCKED", conflict["status"])
        self.assertEqual(1, len(conflict["evidenceConflicts"]))
        self.assertEqual(2, len(conflict["evidenceConflicts"][0]["claims"]))

        resolved = subject.coordinate(
            (self.assignment,),
            {key: [self._report()]},
            extra_claims=(
                {"page": "page.html", "checklist": "Shared", "id": "DDS-COM-001", "result": "FAIL", "evidence": "contrary source", "source": "secondary"},
            ),
            authoritative_evidence={
                "page.html:Shared:DDS-COM-001": {
                    "result": "PASS",
                    "evidence": "authoritative rendered audit",
                    "source": "authoritative-audit",
                }
            },
        )
        self.assertEqual("ACCEPTED", resolved["status"])
        self.assertEqual("resolved", resolved["evidenceConflicts"][0]["resolution"])
        self.assertEqual(2, len(resolved["evidenceConflicts"][0]["claims"]))

        reverse_resolved = subject.coordinate(
            (self.assignment,),
            {key: [self._report(("FAIL", "PASS"))]},
            extra_claims=(
                {
                    "page": "page.html",
                    "checklist": "Shared",
                    "id": "DDS-COM-001",
                    "result": "PASS",
                    "evidence": "contrary source",
                    "source": "secondary",
                },
            ),
            authoritative_evidence={
                "page.html:Shared:DDS-COM-001": {
                    "result": "PASS",
                    "evidence": "authoritative rendered audit",
                    "source": "authoritative-audit",
                }
            },
        )
        self.assertEqual("ACCEPTED", reverse_resolved["status"])
        self.assertEqual("resolved", reverse_resolved["evidenceConflicts"][0]["resolution"])
        self.assertEqual(
            2,
            len(reverse_resolved["evidenceConflicts"][0]["claims"]),
        )

    def test_timeout_and_cancellation_preserve_missing_assignments(self) -> None:
        """Unavailable runner outcomes remain explicit coverage gaps."""

        key = subject.assignment_key(self.assignment)
        for reason in ("unavailable", "timeout", "cancelled"):
            with self.subTest(reason=reason):
                result = subject.coordinate(
                    (self.assignment,),
                    {},
                    unavailable={key: reason},
                )
                self.assertEqual("BLOCKED", result["status"])
                self.assertEqual(reason, result["coverage"]["missing"][0]["reason"])

    def test_accuracy_precedes_every_other_measure(self) -> None:
        """A more accurate unpriced candidate wins provisionally over a cheaper faster peer."""

        result = subject.rank_candidates(
            (
                {"id": "accurate-unpriced", "accuracy": "1", "estimated_cost": None, "wall_seconds": "5"},
                {"id": "less-accurate", "accuracy": "0.99", "estimated_cost": "0.01", "wall_seconds": "1"},
            )
        )
        self.assertEqual("accurate-unpriced", result["ranking"][0]["id"])
        self.assertIsNone(result["ranking"][0]["estimated_cost"])
        self.assertTrue(result["winner_provisional"])

    def test_inclusive_cost_band_outside_boundary_and_speed(self) -> None:
        """Exactly 115 percent ties on cost, just outside does not, and speed breaks the tie."""

        result = subject.rank_candidates(
            (
                {"id": "slow-cheapest", "accuracy": "1", "estimated_cost": "100", "wall_seconds": "10"},
                {"id": "inside", "accuracy": "1", "estimated_cost": "114.999999999999999999", "wall_seconds": "3"},
                {"id": "at-boundary", "accuracy": "1", "estimated_cost": "115", "wall_seconds": "2"},
                {"id": "outside", "accuracy": "1", "estimated_cost": "115.000000000000000001", "wall_seconds": "1"},
            )
        )
        self.assertEqual(
            ["at-boundary", "inside", "slow-cheapest", "outside"],
            [candidate["id"] for candidate in result["ranking"]],
        )

    def test_priced_precedes_unpriced_and_exact_ties_remain_explicit(self) -> None:
        """Price availability is ordered before speed and exact metric ties share a rank."""

        result = subject.rank_candidates(
            (
                {"id": "unpriced-fast", "accuracy": "1", "estimated_cost": None, "wall_seconds": "1"},
                {"id": "priced-b", "accuracy": "1", "estimated_cost": "2", "wall_seconds": "3"},
                {"id": "priced-a", "accuracy": "1", "estimated_cost": "2", "wall_seconds": "3"},
            )
        )
        ranking = result["ranking"]
        self.assertEqual(["priced-a", "priced-b", "unpriced-fast"], [item["id"] for item in ranking])
        self.assertEqual(ranking[0]["rank"], ranking[1]["rank"])
        self.assertTrue(ranking[0]["tie"])
        self.assertTrue(ranking[1]["tie"])
        self.assertFalse(ranking[2]["tie"])

    def test_cached_input_is_subtracted_before_cached_charge(self) -> None:
        """Cached tokens must not also receive the full input rate."""

        usage = {"input_tokens": 1_000_000, "cached_input_tokens": 400_000, "output_tokens": 0}
        rates = {"input_tokens": 25.0, "cached_input_tokens": 2.5, "output_tokens": 150.0}
        self.assertEqual(Decimal("16"), subject.estimated_cost(usage, rates))
        self.assertIsNone(subject.estimated_cost(usage, None))

    def test_invalid_usage_rates_and_candidate_metrics_are_rejected(self) -> None:
        """Invalid numbers, duplicate IDs, and impossible cache usage cannot enter ranking."""

        with self.assertRaisesRegex(ValueError, "cached_input_tokens"):
            subject.estimated_cost(
                {"input_tokens": 1, "cached_input_tokens": 2, "output_tokens": 0},
                {"input_tokens": 1, "cached_input_tokens": 1, "output_tokens": 1},
            )
        invalid_candidates = (
            ({"id": "x", "accuracy": "NaN", "estimated_cost": "1", "wall_seconds": "1"},),
            ({"id": "x", "accuracy": "1", "estimated_cost": "-1", "wall_seconds": "1"},),
            ({"id": "x", "accuracy": "1", "estimated_cost": "1", "wall_seconds": "Infinity"},),
            (
                {"id": "x", "accuracy": "1", "estimated_cost": "1", "wall_seconds": "1"},
                {"id": "x", "accuracy": "1", "estimated_cost": "2", "wall_seconds": "2"},
            ),
        )
        for candidates in invalid_candidates:
            with self.subTest(candidates=candidates), self.assertRaises(ValueError):
                subject.rank_candidates(candidates)

    def test_suite_uses_its_own_contract_and_coordination_fixture(self) -> None:
        """Coordinator scenarios must not reuse the runner's non-delegating task."""

        suite_root = Path(__file__).parent
        suite = yaml.safe_load((suite_root / "suite.yaml").read_text(encoding="utf-8"))
        self.assertEqual(
            ["skills/methodology-design-system-review-coordinator-suite-contract/SKILL.md"],
            suite["projectSkills"]["suite"],
        )
        self.assertTrue((suite_root / suite["projectSkills"]["suite"][0]).is_file())
        scenarios = yaml.safe_load((suite_root / "scenarios.yaml").read_text(encoding="utf-8"))
        self.assertEqual(
            {"fixtures/coordination"},
            {item["executableCase"] for item in scenarios["scenarios"]},
        )
        task = (
            suite_root
            / "fixtures"
            / "coordination"
            / "TASK.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Coordinate", task)
        self.assertNotIn("Do not delegate", task)
        scenario_text = (suite_root / "scenarios.yaml").read_text(encoding="utf-8")
        for phrase in (
            "resolvable and unresolved conflicts",
            "retry exhaustion",
            "timeout and cancellation",
            "exact ties",
            "invalid numeric measurements",
        ):
            self.assertIn(phrase, scenario_text)


if __name__ == "__main__":
    unittest.main()
