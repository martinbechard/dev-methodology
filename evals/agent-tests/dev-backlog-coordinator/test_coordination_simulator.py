# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies provider-selected capacity, same-thread resumption, claims, and cleanup.
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
        """Use provider lifecycle status to fill three vacancies without placeholders."""

        case = _fixture_cases()["provider-selected-ten-item-dispatch"]
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

    def test_user_action_resumes_same_task_and_preserves_early_work(self) -> None:
        """Adopt the answered canonical task and reconcile rather than reject its work."""

        case = _fixture_cases()["same-thread-user-action-resumption"]
        item = WorkItem(
            "user-action",
            "User Action Required",
            canonical_task_id=case["canonicalTaskId"],
            canonical_thread_id=case["canonicalThreadId"],
            provider=case["provider"],
            dirty_owner_task_id=case["dirtyOwnerTaskId"],
            branch=case["branch"],
            worktree=case["worktree"],
        )
        simulator = CoordinationSimulator((item,))

        statuses = simulator.resume_user_action_thread(
            item.item_id,
            user_answer=case["userAnswer"],
            canonical_task_id=case["canonicalTaskId"],
            canonical_thread_id=case["canonicalThreadId"],
            selected_skill_available=True,
            priority_eligible=case["priorityEligible"],
            capacity_available=case["capacityAvailable"],
            root_accepts=case["rootAccepts"],
            preserved_artifacts=case["preservedArtifacts"],
        )

        self.assertEqual(case["expectedStatusSequence"], list(statuses))
        self.assertEqual(case["canonicalTaskId"], item.canonical_task_id)
        self.assertEqual(case["canonicalThreadId"], item.canonical_thread_id)
        self.assertEqual("Running", item.status)
        self.assertEqual("Reconciliation", item.phase)
        self.assertEqual(case["dirtyOwnerTaskId"], item.dirty_owner_task_id)
        self.assertFalse(item.delivery_accepted)
        self.assertIn("Preserved out-of-sequence evidence", item.open_issues[0])
        self.assertEqual(
            tuple(case["preservedArtifacts"]),
            simulator.events[-1]["artifacts"],
        )
        self.assertEqual(
            case["dirtyOwnerTaskId"],
            simulator.events[-1]["dirtyOwnerTask"],
        )
        self.assertFalse(simulator.events[-1]["deliveryAccepted"])
        self.assertNotIn(
            "release",
            " ".join(str(event) for event in simulator.events).lower(),
        )

    def test_user_action_resumption_rejects_task_replacement(self) -> None:
        """Keep the original canonical task identity through lifecycle reconciliation."""

        item = WorkItem(
            "user-action",
            "User Action Required",
            canonical_task_id="task-original",
            canonical_thread_id="thread-original",
        )
        simulator = CoordinationSimulator((item,))

        with self.assertRaisesRegex(ValueError, "cannot replace"):
            simulator.resume_user_action_thread(
                item.item_id,
                user_answer="approved",
                canonical_task_id="task-replacement",
                canonical_thread_id="thread-original",
                selected_skill_available=True,
                priority_eligible=True,
                capacity_available=True,
                root_accepts=True,
            )

        self.assertEqual("User Action Required", item.status)
        self.assertEqual("task-original", item.canonical_task_id)

    def test_user_action_resumption_rejects_thread_replacement(self) -> None:
        """Reject a different Thread even when it reuses the canonical Agent Task id."""

        item = WorkItem(
            "user-action",
            "User Action Required",
            canonical_task_id="task-original",
            canonical_thread_id="thread-original",
        )
        simulator = CoordinationSimulator((item,))

        with self.assertRaisesRegex(ValueError, "canonical Thread"):
            simulator.resume_user_action_thread(
                item.item_id,
                user_answer="approved",
                canonical_task_id="task-original",
                canonical_thread_id="thread-replacement",
                selected_skill_available=True,
                priority_eligible=True,
                capacity_available=True,
                root_accepts=True,
            )

        self.assertEqual("User Action Required", item.status)
        self.assertEqual("thread-original", item.canonical_thread_id)

    def test_selected_provider_resumption_uses_steward_boundaries(self) -> None:
        """Keep routing decisions separate from selected-provider mutations."""

        item = WorkItem(
            "user-action",
            "User Action Required",
            canonical_task_id="task-original",
            canonical_thread_id="thread-original",
            provider="file",
        )
        simulator = CoordinationSimulator((item,))

        simulator.resume_user_action_thread(
            item.item_id,
            user_answer="approved",
            canonical_task_id="task-original",
            canonical_thread_id="thread-original",
            selected_skill_available=True,
            priority_eligible=True,
            capacity_available=True,
            root_accepts=True,
        )

        transitions = [
            event
            for event in simulator.events
            if event["event"] == "lifecycle-transition"
        ]
        self.assertEqual(
            ["dev-backlog-coordinator", "dev-backlog-coordinator", "dev-orchestrator"],
            [event["decisionOwner"] for event in transitions],
        )
        self.assertEqual(
            ["dev-backlog-steward"] * 3,
            [event["mutationAgent"] for event in transitions],
        )
        self.assertTrue(
            all(event["evidence"] == "selected-provider" for event in transitions)
        )

    def test_provider_none_resumption_has_zero_provider_mutation(self) -> None:
        """Record equivalent task-local states without Steward or capacity inference."""

        case = _fixture_cases()["same-thread-provider-none-resumption"]
        item = WorkItem(
            "provider-none",
            "User Action Required",
            canonical_task_id=case["canonicalTaskId"],
            canonical_thread_id=case["canonicalThreadId"],
            provider=case["provider"],
        )
        simulator = CoordinationSimulator((item,))

        statuses = simulator.resume_user_action_thread(
            item.item_id,
            user_answer=case["userAnswer"],
            canonical_task_id=case["canonicalTaskId"],
            canonical_thread_id=case["canonicalThreadId"],
            selected_skill_available=None,
            priority_eligible=case["priorityEligible"],
            capacity_available=None,
            root_accepts=case["rootAccepts"],
        )

        self.assertEqual(case["expectedStatusSequence"], list(statuses))
        transitions = [
            event
            for event in simulator.events
            if event["event"] == "lifecycle-transition"
        ]
        self.assertTrue(all(event["mutationAgent"] is None for event in transitions))
        self.assertTrue(all(event["evidence"] == "task-local" for event in transitions))
        self.assertTrue(
            all(event["capacityInferred"] is False for event in transitions)
        )

    def test_user_action_resumption_requires_recorded_identities(self) -> None:
        """Do not let arbitrary caller ids become canonical during resumption."""

        item = WorkItem("user-action", "User Action Required")
        simulator = CoordinationSimulator((item,))

        with self.assertRaisesRegex(ValueError, "recorded canonical identities"):
            simulator.resume_user_action_thread(
                item.item_id,
                user_answer="approved",
                canonical_task_id="task-invented",
                canonical_thread_id="thread-invented",
                selected_skill_available=True,
                priority_eligible=True,
                capacity_available=True,
                root_accepts=True,
            )

        self.assertIsNone(item.canonical_task_id)
        self.assertIsNone(item.canonical_thread_id)
        self.assertEqual("User Action Required", item.status)

    def test_user_action_resumption_stops_at_each_dispatch_gate(self) -> None:
        """Require priority, capacity, and root acceptance before Running."""

        def resume(
            *,
            priority_eligible: bool,
            capacity_available: bool,
            root_accepts: bool,
        ) -> tuple[str, ...]:
            item = WorkItem(
                "user-action",
                "User Action Required",
                canonical_task_id="task-original",
                canonical_thread_id="thread-original",
            )
            return CoordinationSimulator((item,)).resume_user_action_thread(
                item.item_id,
                user_answer="approved",
                canonical_task_id="task-original",
                canonical_thread_id="thread-original",
                selected_skill_available=True,
                priority_eligible=priority_eligible,
                capacity_available=capacity_available,
                root_accepts=root_accepts,
            )

        self.assertEqual(
            ("User Action Required", "Ready"),
            resume(
                priority_eligible=False,
                capacity_available=True,
                root_accepts=True,
            ),
        )
        self.assertEqual(
            ("User Action Required", "Ready"),
            resume(
                priority_eligible=True,
                capacity_available=False,
                root_accepts=True,
            ),
        )
        self.assertEqual(
            ("User Action Required", "Ready", "Starting"),
            resume(
                priority_eligible=True,
                capacity_available=True,
                root_accepts=False,
            ),
        )

    def test_placeholder_provider_resumption_is_blocked_without_mutation(self) -> None:
        """Preserve a placeholder manager's zero-mutation result."""

        for provider in ("azure-devops", "jira"):
            with self.subTest(provider=provider):
                item = WorkItem(
                    "user-action",
                    "User Action Required",
                    canonical_task_id="task-original",
                    canonical_thread_id="thread-original",
                    provider=provider,
                )
                simulator = CoordinationSimulator((item,))

                with self.assertRaisesRegex(ValueError, "zero mutation"):
                    simulator.resume_user_action_thread(
                        item.item_id,
                        user_answer="approved",
                        canonical_task_id="task-original",
                        canonical_thread_id="thread-original",
                        selected_skill_available=True,
                        priority_eligible=True,
                        capacity_available=True,
                        root_accepts=True,
                    )

                self.assertEqual("User Action Required", item.status)
                self.assertEqual([], simulator.events)

    def test_different_dirty_owner_blocks_dispatch_without_release(self) -> None:
        """Record the answer but stop before Starting while another task owns dirt."""

        item = WorkItem(
            "user-action",
            "User Action Required",
            canonical_task_id="task-original",
            canonical_thread_id="thread-original",
            dirty_owner_task_id="task-other",
        )
        simulator = CoordinationSimulator((item,))

        statuses = simulator.resume_user_action_thread(
            item.item_id,
            user_answer="approved",
            canonical_task_id="task-original",
            canonical_thread_id="thread-original",
            selected_skill_available=True,
            priority_eligible=True,
            capacity_available=True,
            root_accepts=True,
        )

        self.assertEqual(("User Action Required", "Ready"), statuses)
        self.assertEqual("Ready", item.status)
        self.assertEqual("task-other", item.dirty_owner_task_id)
        self.assertIn("must be handed off", item.open_issues[-1])
        self.assertNotIn(
            "release",
            " ".join(str(event) for event in simulator.events).lower(),
        )

    def test_unavailable_selected_manager_blocks_resumption_without_mutation(self) -> None:
        """Do not bypass a selected provider manager that cannot operate."""

        for provider in ("file", "github", "gitlab"):
            with self.subTest(provider=provider):
                item = WorkItem(
                    "user-action",
                    "User Action Required",
                    canonical_task_id="task-original",
                    canonical_thread_id="thread-original",
                    provider=provider,
                )
                simulator = CoordinationSimulator((item,))

                with self.assertRaisesRegex(ValueError, "unavailable with zero mutation"):
                    simulator.resume_user_action_thread(
                        item.item_id,
                        user_answer="approved",
                        canonical_task_id="task-original",
                        canonical_thread_id="thread-original",
                        selected_skill_available=False,
                        priority_eligible=True,
                        capacity_available=True,
                        root_accepts=True,
                    )

                self.assertEqual("User Action Required", item.status)
                self.assertEqual([], simulator.events)

    def test_persistence_routes_cover_supported_providers_without_fallback(self) -> None:
        """Preserve each selected provider's manager, inventory, and blocked semantics."""

        expected = {
            "file": ("manage-file-work-items", True, "READY", False),
            "github": ("manage-github-work-items", True, "READY", False),
            "gitlab": ("manage-gitlab-work-items", True, "READY", False),
            "azure-devops": (
                "manage-azure-devops-work-items",
                False,
                "BLOCKED",
                True,
            ),
            "jira": ("manage-jira-work-items", False, "BLOCKED", True),
            "none": (None, False, "READY", True),
            "UNSET": (None, False, "BLOCKED", True),
        }

        for provider, route_contract in expected.items():
            with self.subTest(provider=provider):
                route = CoordinationSimulator.persistence_route(provider)
                self.assertEqual(route_contract, (
                    route.management_skill,
                    route.durable_inventory,
                    route.status,
                    route.zero_mutation,
                ))

        unavailable = CoordinationSimulator.persistence_route(
            "github", selected_skill_available=False
        )
        self.assertEqual("manage-github-work-items", unavailable.management_skill)
        self.assertEqual("BLOCKED", unavailable.status)
        self.assertTrue(unavailable.zero_mutation)

    def test_claim_retry_window_is_bounded_to_thirty_minutes(self) -> None:
        """Record one immediate attempt and six five-minute retries in the work item."""

        case = _fixture_cases()["selected-commit-retry-and-closeout"]
        item = WorkItem("integration", "Running")
        simulator = CoordinationSimulator((item,))

        for elapsed in case["claimAttemptMinutes"]:
            simulator.record_claim_attempt(
                "integration",
                claim_kind="integration",
                elapsed_minutes=elapsed,
                outcome="CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
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
                outcome="CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
            )

    def test_successful_retry_stops_the_wait_window(self) -> None:
        """Move directly into integration as soon as the exact claim succeeds."""

        item = WorkItem("integration", "Running")
        simulator = CoordinationSimulator((item,))
        simulator.record_claim_attempt(
            "integration",
            claim_kind="integration",
            elapsed_minutes=0,
            outcome="CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
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
                outcome="CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
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
                outcome="CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
            )
        with self.assertRaisesRegex(ValueError, "requires acquired integration"):
            simulator.record_claim_attempt(
                "delivery",
                claim_kind="completion",
                elapsed_minutes=0,
                outcome="CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
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
            outcome="CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
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
            "provider_reference": "https://provider.example/items/42",
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
