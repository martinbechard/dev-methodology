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

        status = "FAIL" if "FAIL" in results else "NOT TESTED" if "NOT TESTED" in results else "PASS"
        return {
            "status": status,
            "page": "page.html",
            "checklist": "Shared",
            "checks": [
                {"id": check_id, "result": result, "evidence": f"evidence {index}"}
                for index, (check_id, result) in enumerate(zip(self.assignment[2], results, strict=True), start=1)
            ],
            "findings": [],
            "limits": [],
        }

    def test_complete_pass_and_confirmed_failure(self) -> None:
        """Complete PASS accepts and a complete confirmed FAIL rejects."""

        key = subject.assignment_key(self.assignment)
        accepted = subject.coordinate((self.assignment,), {key: [self._report()]})
        rejected = subject.coordinate((self.assignment,), {key: [self._report(("PASS", "FAIL"))]})
        self.assertEqual("ACCEPTED", accepted["status"])
        self.assertEqual("REJECTED", rejected["status"])

    def test_missing_unavailable_and_not_tested_are_blocked(self) -> None:
        """The coordinator must never fill unavailable or incomplete runner evidence itself."""

        key = subject.assignment_key(self.assignment)
        self.assertEqual("BLOCKED", subject.coordinate((self.assignment,), {})["status"])
        self.assertEqual("BLOCKED", subject.coordinate((self.assignment,), {}, unavailable=(key,))["status"])
        incomplete = subject.coordinate((self.assignment,), {key: [self._report(("PASS", "NOT TESTED"))]})
        self.assertEqual("BLOCKED", incomplete["status"])

    def test_one_malformed_retry_can_recover_but_two_cannot(self) -> None:
        """Exactly one corrected retry is accepted after an initially malformed report."""

        key = subject.assignment_key(self.assignment)
        malformed = {**self._report(), "checks": []}
        recovered = subject.coordinate((self.assignment,), {key: [malformed, self._report()]})
        blocked = subject.coordinate((self.assignment,), {key: [malformed, malformed]})
        self.assertEqual("ACCEPTED", recovered["status"])
        self.assertEqual([key], recovered["retries"])
        self.assertEqual("BLOCKED", blocked["status"])

    def test_duplicate_findings_are_deduplicated_and_conflicts_are_preserved(self) -> None:
        """Identical findings collapse while contradictory material item results block."""

        key = subject.assignment_key(self.assignment)
        report = self._report(("PASS", "FAIL"))
        finding = {"page": "page.html", "id": "DDS-COM-002", "correction": "Match the version."}
        report["findings"] = [finding, dict(finding)]
        result = subject.coordinate((self.assignment,), {key: [report]})
        self.assertEqual(1, len(result["findings"]))
        conflict = subject.coordinate(
            (self.assignment,),
            {key: [self._report()]},
            extra_claims=(
                {"page": "page.html", "id": "DDS-COM-001", "result": "FAIL", "evidence": "contrary source"},
            ),
        )
        self.assertEqual("BLOCKED", conflict["status"])
        self.assertEqual(1, len(conflict["conflicts"]))

    def test_accuracy_precedes_every_other_measure(self) -> None:
        """A more accurate unpriced candidate wins provisionally over a cheaper faster peer."""

        result = subject.rank_candidates(
            (
                {"id": "accurate-unpriced", "accuracy": 1.0, "estimated_cost": None, "wall_seconds": 5.0},
                {"id": "less-accurate", "accuracy": 0.99, "estimated_cost": 0.01, "wall_seconds": 1.0},
            )
        )
        self.assertEqual("accurate-unpriced", result["ranking"][0]["id"])
        self.assertIsNone(result["ranking"][0]["estimated_cost"])
        self.assertTrue(result["winner_provisional"])

    def test_inclusive_cost_band_outside_boundary_and_speed(self) -> None:
        """Exactly 115 percent ties on cost, just outside does not, and speed breaks the tie."""

        result = subject.rank_candidates(
            (
                {"id": "slow-cheapest", "accuracy": 1.0, "estimated_cost": 100.0, "wall_seconds": 10.0},
                {"id": "fast-at-boundary", "accuracy": 1.0, "estimated_cost": 115.0, "wall_seconds": 2.0},
                {"id": "fast-outside", "accuracy": 1.0, "estimated_cost": 115.0001, "wall_seconds": 1.0},
            )
        )
        self.assertEqual(
            ["fast-at-boundary", "slow-cheapest", "fast-outside"],
            [candidate["id"] for candidate in result["ranking"]],
        )

    def test_cached_input_is_subtracted_before_cached_charge(self) -> None:
        """Cached tokens must not also receive the full input rate."""

        usage = {"input_tokens": 1_000_000, "cached_input_tokens": 400_000, "output_tokens": 0}
        rates = {"input_tokens": 25.0, "cached_input_tokens": 2.5, "output_tokens": 150.0}
        self.assertEqual(16.0, subject.estimated_cost(usage, rates))
        self.assertIsNone(subject.estimated_cost(usage, None))


if __name__ == "__main__":
    unittest.main()
