# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies file-backed capacity, claim retry, dispatch, and cleanup contracts.
# Test plan: evals/agent-tests/dev-backlog-coordinator/requirements-matrix.md

"""Verify the deterministic parent backlog coordination simulator."""

from datetime import datetime, timezone
from pathlib import Path
import unittest

import yaml

from coordination_simulator import (
    CLAIM_ATTEMPT_MINUTES,
    CoordinationSimulator,
    DeliveryEvidence,
    TaskCleanupEvidence,
    TaskCandidate,
    WorkItem,
)


CASES_PATH = Path(__file__).parent / "fixtures" / "cases.yaml"


def _fixture_cases() -> dict[str, dict[str, object]]:
    """Load the suite-owned executable coordination cases."""

    return yaml.safe_load(CASES_PATH.read_text(encoding="utf-8"))["cases"]


class CoordinationSimulatorTests(unittest.TestCase):
    """Exercise queue capacity and delivery recovery through observable state."""

    def test_dispatches_ready_items_until_ten_are_running(self) -> None:
        """Use file-backed status to fill three vacancies without placeholders."""

        case = _fixture_cases()["file-backed-ten-item-dispatch"]
        items = [
            WorkItem(f"running-{index}", "Running")
            for index in range(case["runningItems"])
        ]
        items.extend(
            WorkItem(f"ready-{index}", "Ready")
            for index in range(case["readyItems"])
        )
        items.extend(
            WorkItem(f"non-running-{index}", status)
            for index, status in enumerate(case["nonRunningStatuses"])
        )
        simulator = CoordinationSimulator(items)

        self.assertEqual(("ready-0", "ready-1", "ready-2"), simulator.dispatch_to_target())
        self.assertEqual(case["targetRunningItems"], simulator.running_count())
        self.assertEqual(case["expectedDispatchCount"], len(simulator.events[-1]["started"]))
        self.assertEqual("Ready", simulator.items[10].status)
        for item in simulator.items[7:10]:
            self.assertEqual(f"task-{item.item_id}", item.canonical_task_id)
            self.assertEqual("Implementation", item.phase)

    def test_dispatches_every_ready_item_when_queue_has_less_than_ten(self) -> None:
        """Report a real eligible-work shortage instead of creating wait-only work."""

        simulator = CoordinationSimulator(
            (WorkItem("running", "Running"), WorkItem("ready", "Ready"))
        )

        self.assertEqual(("ready",), simulator.dispatch_to_target())
        self.assertEqual(2, simulator.running_count())

    def test_claim_retry_window_is_bounded_to_thirty_minutes(self) -> None:
        """Record one immediate attempt and six five-minute retries in the work item."""

        case = _fixture_cases()["bounded-integration-retry-and-closeout"]
        item = WorkItem("integration", "Running")
        simulator = CoordinationSimulator((item,))

        for elapsed in case["claimAttemptMinutes"]:
            simulator.record_claim_attempt(
                "integration",
                claim_kind="integration",
                elapsed_minutes=elapsed,
                outcome="WAIT",
                blocking_claim_id="shared-generator",
            )

        self.assertEqual(list(CLAIM_ATTEMPT_MINUTES), [
            attempt["elapsedMinutes"]
            for attempt in item.claim_attempts["integration"]
        ])
        self.assertEqual(case["maximumRetries"], len(item.claim_attempts["integration"]) - 1)
        self.assertEqual("Integration Investigation", item.phase)
        self.assertEqual(("integration",), simulator.waits_requiring_investigation())
        self.assertIn("shared-generator", item.open_issues[0])
        with self.assertRaisesRegex(ValueError, "retry window is exhausted"):
            simulator.record_claim_attempt(
                "integration",
                claim_kind="integration",
                elapsed_minutes=30,
                outcome="WAIT",
            )

    def test_successful_retry_stops_the_wait_window(self) -> None:
        """Move directly into integration as soon as the exact claim succeeds."""

        item = WorkItem("integration", "Running")
        simulator = CoordinationSimulator((item,))
        simulator.record_claim_attempt(
            "integration",
            claim_kind="integration",
            elapsed_minutes=0,
            outcome="WAIT",
            blocking_claim_id="owner",
        )
        simulator.record_claim_attempt(
            "integration",
            claim_kind="integration",
            elapsed_minutes=5,
            outcome="ACQUIRED",
        )

        self.assertEqual("Integration", item.phase)
        self.assertEqual((), simulator.waits_requiring_investigation())
        with self.assertRaisesRegex(ValueError, "already acquired"):
            simulator.record_claim_attempt(
                "integration",
                claim_kind="integration",
                elapsed_minutes=10,
                outcome="WAIT",
            )

    def test_claim_windows_reject_out_of_order_and_separate_completion(self) -> None:
        """Reject reordered attempts and start completion only after integration acquisition."""

        item = WorkItem("delivery", "Running")
        simulator = CoordinationSimulator((item,))
        with self.assertRaisesRegex(ValueError, "minute 0"):
            simulator.record_claim_attempt(
                "delivery",
                claim_kind="integration",
                elapsed_minutes=5,
                outcome="WAIT",
            )
        with self.assertRaisesRegex(ValueError, "requires acquired integration"):
            simulator.record_claim_attempt(
                "delivery",
                claim_kind="completion",
                elapsed_minutes=0,
                outcome="WAIT",
            )
        simulator.record_claim_attempt(
            "delivery",
            claim_kind="integration",
            elapsed_minutes=0,
            outcome="ACQUIRED",
        )
        simulator.record_claim_attempt(
            "delivery",
            claim_kind="completion",
            elapsed_minutes=0,
            outcome="WAIT",
        )
        simulator.record_claim_attempt(
            "delivery",
            claim_kind="completion",
            elapsed_minutes=5,
            outcome="ACQUIRED",
        )

        self.assertEqual({"integration", "completion"}, item.acquired_claims)
        self.assertEqual([0, 5], [
            attempt["elapsedMinutes"]
            for attempt in item.claim_attempts["completion"]
        ])

    def test_unresolved_wait_frees_capacity_only_after_investigation(self) -> None:
        """Route an exhausted wait truthfully before dispatching a replacement."""

        stalled = WorkItem("stalled", "Running", phase="Integration Investigation")
        replacement = WorkItem("replacement", "Ready")
        running = [WorkItem(f"running-{index}", "Running") for index in range(9)]
        simulator = CoordinationSimulator((stalled, replacement, *running))

        simulator.dispose_unresolved_wait("stalled", user_decision=False)
        self.assertEqual("Blocked", stalled.status)
        self.assertEqual(("replacement",), simulator.dispatch_to_target())
        self.assertEqual(10, simulator.running_count())

    def test_settled_dispatch_contains_duplicate_without_retry(self) -> None:
        """Keep one canonical task and stop, verify, and archive its duplicate."""

        common = {
            "parent_task_id": "parent-123",
            "backlog_path": "backlog/feature-backlog/example.md",
            "normalized_objective": "deliver example",
        }
        canonical = TaskCandidate(
            task_id="task-original",
            created_at=datetime(2026, 7, 20, 10, 0, tzinfo=timezone.utc),
            **common,
        )
        duplicate = TaskCandidate(
            task_id="task-duplicate",
            created_at=datetime(2026, 7, 20, 10, 0, 2, tzinfo=timezone.utc),
            **common,
        )

        result = CoordinationSimulator.reconcile_ambiguous_dispatch(
            immediate_matches=(), settled_matches=(duplicate, canonical)
        )

        self.assertEqual("task-original", result.canonical_task_id)
        self.assertEqual(0, result.retry_count)
        self.assertEqual("stopped", duplicate.status)
        self.assertTrue(duplicate.archived)
        self.assertEqual(
            ("stopped", "zero mutation verified", "archived"),
            tuple(duplicate.containment_transitions),
        )

    def test_completion_handoff_precedes_parent_cleanup(self) -> None:
        """Complete the work item before parent worktree, branch, title, and archive cleanup."""

        incomplete_delivery = DeliveryEvidence(
            integration_commit="abc",
            focused_tests_passed=True,
            integration_claim_id="integration-claim",
            integration_release_event="release-integration",
            completion_commit="def",
            completion_claim_id="completion-claim",
            completion_release_event="release-completion",
            worktree_clean=True,
            branch_fully_merged=False,
        )
        ready_delivery = DeliveryEvidence(
            integration_commit="abc",
            focused_tests_passed=True,
            integration_claim_id="integration-claim",
            integration_release_event="release-integration",
            completion_commit="def",
            completion_claim_id="completion-claim",
            completion_release_event="release-completion",
            worktree_clean=True,
            branch_fully_merged=True,
        )
        waiting_cleanup = TaskCleanupEvidence(ready_delivery, False, False)
        complete_cleanup = TaskCleanupEvidence(ready_delivery, True, True)

        self.assertFalse(incomplete_delivery.completion_ready)
        self.assertTrue(ready_delivery.completion_ready)
        self.assertFalse(waiting_cleanup.complete)
        self.assertTrue(complete_cleanup.complete)
        self.assertEqual(
            "Done — example",
            CoordinationSimulator.success_title("example"),
        )

    def test_private_work_claims_tiered_tests_and_post_facto_audits_are_executable(self) -> None:
        """Exercise private scope, focused verification, and non-gating audit choices."""

        case = _fixture_cases()["private-worktree-and-tiered-verification"]
        for operation in case["privateOperations"]:
            self.assertFalse(CoordinationSimulator.shared_claim_required(operation))
        for operation in case["sharedOperations"]:
            self.assertTrue(CoordinationSimulator.shared_claim_required(operation))
        self.assertEqual(
            tuple(case["perItemVerification"]),
            CoordinationSimulator.verification_plan(),
        )
        self.assertEqual(
            tuple(case["expandedVerification"]),
            CoordinationSimulator.verification_plan(cross_cutting_risk=True),
        )
        self.assertEqual(
            tuple(case["finalCampaignVerification"]),
            CoordinationSimulator.verification_plan(final_campaign=True),
        )
        self.assertIsNone(
            CoordinationSimulator.post_facto_reduction(
                actual_waste_observed=False,
                options=case["postFactoOptions"],
                selected=case["selectedPostFactoOption"],
            )
        )
        self.assertEqual(
            case["selectedPostFactoOption"],
            CoordinationSimulator.post_facto_reduction(
                actual_waste_observed=True,
                options=case["postFactoOptions"],
                selected=case["selectedPostFactoOption"],
            ),
        )


if __name__ == "__main__":
    unittest.main()
