#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies read-only watchdog alerts and Coordinator-owned Stalled dispositions.

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
        self.assertEqual([], result.alerts)
        self.assertEqual(before, items)

    def test_suspected_stall_alerts_parent_without_setting_stalled(self) -> None:
        """The Watchdog reports evidence while leaving lifecycle state unchanged."""

        case = self.cases["suspected-stall-alert"]
        item = WorkItem(**case["item"])
        before = deepcopy(item)

        result = WatchdogCycle().evaluate([item])

        self.assertEqual("ALERT", result.status)
        self.assertEqual(before, item)
        self.assertEqual(1, len(result.alerts))
        alert = result.alerts[0]
        self.assertEqual(case["expectedProviderIdentity"], alert.provider_identity)
        self.assertEqual(case["expectedReason"], alert.reason)
        self.assertEqual(case["expectedAction"], alert.recommended_action)
        self.assertEqual("unknown", alert.preventing_cause)
        self.assertFalse(result.mutated)

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
        self.assertEqual(case["expectedReasons"], [alert.reason for alert in result.alerts])
        self.assertTrue(
            all("Coordinator" in alert.recommended_action for alert in result.alerts)
        )
        self.assertFalse(result.mutated)

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
        with self.assertRaisesRegex(ValueError, "no evidence-backed Stalled disposition"):
            disposition.choose(**cases["insufficientEvidence"])

    def test_series_and_archive_rules_keep_stalled_nonterminal(self) -> None:
        """Series state and terminal archival must not collapse Stalled into Blocked."""

        self.assertEqual("stalled", series_state(["Stalled", "Stalled"]))
        self.assertEqual("blocked", series_state(["Blocked", "Blocked"]))
        self.assertEqual("active", series_state(["Running", "Stalled"]))
        self.assertEqual(
            "mixed:Blocked,Stalled",
            series_state(["Blocked", "Stalled"]),
        )
        with self.assertRaisesRegex(ValueError, "Stalled is nonterminal"):
            terminal_archive_destination("Feature", "Stalled", True)
        self.assertEqual(
            "backlog/failed-backlog/features",
            terminal_archive_destination("Feature", "Failed", True),
        )


if __name__ == "__main__":
    unittest.main()
