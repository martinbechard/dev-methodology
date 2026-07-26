#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies read-only watchdog alerts and Coordinator-owned Stalled dispositions.
# Governing design: design/orchestrated-development-lifecycle.html
# Governing test plan: evals/agent-tests/dev-backlog-watchdog/requirements-matrix.md

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import unittest

import yaml

from watchdog_simulator import (
    CoordinatorDisposition,
    WorkItem,
    WatchdogCycle,
    active_capacity,
    series_state,
    terminal_archive_destination,
)


CASES_PATH = Path(__file__).with_name("fixtures") / "cases.yaml"
SUITE_PATH = Path(__file__).parent


class WatchdogSimulatorTests(unittest.TestCase):
    """Exercise watchdog and lifecycle boundaries through deterministic state."""

    @classmethod
    def setUpClass(cls) -> None:
        """Load the suite-owned synthetic cases once for this focused test class."""

        cls.cases = yaml.safe_load(CASES_PATH.read_text(encoding="utf-8"))["cases"]

    def test_quiet_work_returns_no_action_without_mutation(self) -> None:
        """Quiet work inside its progress boundary remains healthy."""

        case = self.cases["healthy-quiet-cycle"]
        items = [WorkItem(**item) for item in case["items"]]
        before = deepcopy(items)

        result = WatchdogCycle().evaluate(items)

        self.assertEqual("NO_ACTION", result.status)
        self.assertEqual(case["expectedMessage"], result.message)
        self.assertIsNone(result.alert)
        self.assertEqual(before, items)

    def test_suspected_stall_alerts_parent_without_setting_stalled(self) -> None:
        """The Watchdog reports evidence while leaving lifecycle state unchanged."""

        case = self.cases["suspected-stall-alert"]
        item = WorkItem(**case["item"])
        before = deepcopy(item)

        result = WatchdogCycle().evaluate([item])

        self.assertEqual("ALERT", result.status)
        self.assertEqual(before, item)
        self.assertIsNotNone(result.alert)
        alert = result.alert
        assert alert is not None
        self.assertEqual(case["expectedProviderIdentity"], alert.provider_identity)
        self.assertEqual(case["expectedReason"], alert.reason)
        self.assertEqual(case["expectedAction"], alert.recommended_action)
        self.assertEqual("", alert.preventing_cause)
        self.assertIn("hard_stop_crossed=true", alert.evidence)
        self.assertIn(
            "hard_stop=2026-07-26T16:30:00Z",
            alert.evidence,
        )
        self.assertIn("progress_gap=true", alert.evidence)
        self.assertIn(
            "progress_observation=no evidence-bearing output for 18 minutes",
            alert.evidence,
        )
        self.assertFalse(result.mutated)

    def test_known_preventing_cause_recommends_blocked_not_stalled(self) -> None:
        """A known cause follows the Blocked route without a lifecycle mutation."""

        case = self.cases["known-cause-alert"]
        item = WorkItem(**case["item"])
        before = deepcopy(item)

        result = WatchdogCycle().evaluate([item])

        self.assertEqual("ALERT", result.status)
        self.assertEqual(before, item)
        self.assertIsNotNone(result.alert)
        alert = result.alert
        assert alert is not None
        self.assertEqual(case["expectedReason"], alert.reason)
        self.assertEqual(case["expectedAction"], alert.recommended_action)
        self.assertNotIn("Stalled", alert.recommended_action)
        self.assertFalse(result.mutated)

    def test_whitespace_only_cause_remains_unknown(self) -> None:
        """A blank cause is the only route to unknown-cause Stalled investigation."""

        item = WorkItem(
            provider_identity="backlog/feature-backlog/blank-cause.md",
            status="Running",
            progress_gap=True,
            preventing_cause=" \t ",
        )

        result = WatchdogCycle().evaluate([item])

        self.assertIsNotNone(result.alert)
        alert = result.alert
        assert alert is not None
        self.assertIn("cause remains unknown", alert.reason)
        self.assertIn("Stalled", alert.recommended_action)

    def test_starting_missing_or_stopped_task_alerts_without_mutation(self) -> None:
        """Starting task disappearance requires the same read-only alert as Running."""

        for task_state in ("missing", "stopped"):
            item = WorkItem(
                provider_identity=f"backlog/feature-backlog/starting-{task_state}.md",
                status="Starting",
                task_state=task_state,
                canonical_thread=f"thread-starting-{task_state}",
                root_task=f"task-starting-{task_state}",
            )
            before = deepcopy(item)

            result = WatchdogCycle().evaluate([item])

            with self.subTest(task_state=task_state):
                self.assertEqual("ALERT", result.status)
                self.assertEqual(before, item)
                self.assertIsNotNone(result.alert)
                alert = result.alert
                assert alert is not None
                self.assertIn(item.provider_identity, alert.provider_identity)
                self.assertIn("task_boundary_crossed=true", alert.evidence)
                self.assertIn(f"task_state={task_state}", alert.evidence)
                self.assertFalse(result.mutated)

    def test_estimate_boundary_evidence_names_observed_value(self) -> None:
        """Crossed estimates identify both the boundary and its observed value."""

        item = WorkItem(
            provider_identity="backlog/analysis-backlog/estimate-crossed.md",
            status="Running",
            phase="focused verification",
            phase_estimate="12 minutes",
            estimate_boundary_crossed=True,
            last_productive_evidence="test process started",
        )

        result = WatchdogCycle().evaluate([item])

        self.assertIsNotNone(result.alert)
        alert = result.alert
        assert alert is not None
        self.assertIn("estimate_boundary_crossed=true", alert.evidence)
        self.assertIn("phase_estimate=12 minutes", alert.evidence)

    def test_aggregate_alert_filters_empty_preventing_causes(self) -> None:
        """Aggregate cause evidence contains only concrete preventing causes."""

        unknown_items = [
            WorkItem(
                provider_identity=f"backlog/feature-backlog/unknown-{index}.md",
                status="Running",
                progress_gap=True,
                preventing_cause=cause,
            )
            for index, cause in enumerate(("", " \t "))
        ]
        unknown_result = WatchdogCycle().evaluate(unknown_items)
        self.assertIsNotNone(unknown_result.alert)
        unknown_alert = unknown_result.alert
        assert unknown_alert is not None
        self.assertEqual("", unknown_alert.preventing_cause)

        mixed_items = [
            *unknown_items,
            WorkItem(
                provider_identity="backlog/defect-backlog/known-cause.md",
                status="Running",
                progress_gap=True,
                preventing_cause=" upstream credential unavailable ",
            ),
        ]
        mixed_result = WatchdogCycle().evaluate(mixed_items)
        self.assertIsNotNone(mixed_result.alert)
        mixed_alert = mixed_result.alert
        assert mixed_alert is not None
        self.assertEqual(
            "upstream credential unavailable",
            mixed_alert.preventing_cause,
        )

    def test_stalled_is_outside_starting_plus_running_capacity(self) -> None:
        """Only Starting and Running consume the durable active-capacity target."""

        statuses = self.cases["capacity"]["statuses"]
        self.assertEqual(
            self.cases["capacity"]["expectedActiveCount"],
            active_capacity(WorkItem(str(index), status) for index, status in enumerate(statuses)),
        )

    def test_satisfied_exit_conditions_alert_without_disposition(self) -> None:
        """Stalled and Blocked exit evidence requests Coordinator attention only."""

        case = self.cases["satisfied-exit-conditions"]
        items = [WorkItem(**item) for item in case["items"]]
        before = deepcopy(items)

        result = WatchdogCycle().evaluate(items)

        self.assertEqual("ALERT", result.status)
        self.assertEqual(before, items)
        self.assertIsNotNone(result.alert)
        alert = result.alert
        assert alert is not None
        for reason in case["expectedReasons"]:
            with self.subTest(reason=reason):
                self.assertIn(reason, alert.reason)
        for item in case["items"]:
            with self.subTest(provider_identity=item["provider_identity"]):
                self.assertIn(item["provider_identity"], alert.provider_identity)
        self.assertIn(" | ", alert.reason)
        self.assertIn("Coordinator", alert.recommended_action)
        self.assertIn("one aggregate parent alert", result.message)
        self.assertFalse(result.mutated)

    def test_aggregate_alert_keeps_all_unknown_causes_blank(self) -> None:
        """Several unknown-cause observations must not fabricate cause content."""

        items = [
            WorkItem(
                provider_identity=f"backlog/feature-backlog/unknown-{index}.md",
                status="Stalled",
                stalled_exit_satisfied=True,
            )
            for index in range(2)
        ]

        result = WatchdogCycle().evaluate(items)

        self.assertIsNotNone(result.alert)
        alert = result.alert
        assert alert is not None
        self.assertEqual("", alert.preventing_cause)
        self.assertFalse(alert.preventing_cause)

    def test_aggregate_alert_preserves_only_meaningful_known_causes(self) -> None:
        """Mixed observations retain known causes without empty separators."""

        items = [
            WorkItem(
                provider_identity="backlog/feature-backlog/unknown.md",
                status="Stalled",
                stalled_exit_satisfied=True,
            ),
            WorkItem(
                provider_identity="backlog/defect-backlog/known.md",
                status="Blocked",
                preventing_cause="upstream release is unavailable",
                blocker_exit_satisfied=True,
            ),
        ]

        result = WatchdogCycle().evaluate(items)

        self.assertIsNotNone(result.alert)
        alert = result.alert
        assert alert is not None
        self.assertEqual(
            "upstream release is unavailable",
            alert.preventing_cause,
        )

    def test_coordinator_dispositions_are_evidence_gated(self) -> None:
        """Every Stalled exit has one deterministic evidence boundary."""

        disposition = CoordinatorDisposition()
        cases = self.cases["stalled-dispositions"]
        self.assertEqual("Running", disposition.choose(**cases["sameOwnerResumed"]))
        self.assertEqual("Ready", disposition.choose(**cases["ownershipEnded"]))
        self.assertEqual("Blocked", disposition.choose(**cases["knownBlocker"]))
        self.assertEqual(
            "User Action Required",
            disposition.choose(**cases["userAction"]),
        )
        self.assertEqual("Failed", disposition.choose(**cases["terminalFailure"]))
        with self.assertRaisesRegex(ValueError, "terminal evidence"):
            disposition.choose(**cases["terminalWithoutEvidence"])
        with self.assertRaisesRegex(ValueError, "active-capacity slot"):
            disposition.choose(**cases["sameOwnerResumedAfterRefill"])
        with self.assertRaisesRegex(ValueError, "no evidence-backed Stalled disposition"):
            disposition.choose(**cases["insufficientEvidence"])

    def test_series_and_archive_rules_keep_stalled_nonterminal(self) -> None:
        """Series state and terminal archival must not collapse Stalled into Blocked."""

        self.assertEqual("stalled", series_state(["Stalled", "Stalled"]))
        self.assertEqual("blocked", series_state(["Blocked", "Blocked"]))
        self.assertEqual("active", series_state(["Running", "Stalled"]))
        self.assertEqual("stalled", series_state(["Completed", "Stalled"]))
        self.assertEqual("blocked", series_state(["Completed", "Blocked"]))
        self.assertEqual("completed", series_state(["Completed", "Abandoned"]))
        self.assertEqual("completed", series_state(["Abandoned", "Abandoned"]))
        self.assertEqual("stalled", series_state(["Abandoned", "Stalled"]))
        self.assertEqual("blocked", series_state(["Abandoned", "Blocked"]))
        self.assertEqual(
            "mixed:Blocked,Stalled",
            series_state(["Completed", "Abandoned", "Blocked", "Stalled"]),
        )
        with self.assertRaisesRegex(ValueError, "Stalled is nonterminal"):
            terminal_archive_destination("Feature", "Stalled", True)
        self.assertEqual(
            "backlog/failed-backlog/features",
            terminal_archive_destination("Feature", "Failed", True),
        )

    def test_python_artifacts_name_their_governing_sources(self) -> None:
        """The simulator and test retain direct design and test-plan traceability."""

        expected = (
            "Governing design: design/orchestrated-development-lifecycle.html",
            "Governing test plan: "
            "evals/agent-tests/dev-backlog-watchdog/requirements-matrix.md",
        )
        for filename in ("watchdog_simulator.py", "test_watchdog_simulator.py"):
            source = (SUITE_PATH / filename).read_text(encoding="utf-8")
            for reference in expected:
                with self.subTest(filename=filename, reference=reference):
                    self.assertIn(reference, source)


if __name__ == "__main__":
    unittest.main()
