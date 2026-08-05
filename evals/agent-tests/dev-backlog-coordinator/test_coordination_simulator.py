# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies provider-selected capacity, blockage dispatch modes, claims, and cleanup.
# Governing design: design/orchestrated-development-lifecycle.html
# Test plan: evals/agent-tests/dev-backlog-coordinator/requirements-matrix.md

"""Verify the deterministic parent backlog coordination simulator."""

from datetime import datetime, timezone
from pathlib import Path
import unittest

import yaml

from coordination_simulator import (
    CoordinationSimulator,
    DeliveryEvidence,
    TaskCleanupEvidence,
    TaskCandidate,
    WorkItem,
    dispatch_mode_transition,
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

    def test_blockage_entry_and_resumption_change_only_secondary_dispatch(self) -> None:
        """Make entry, repeat, recovery, and resumption safe and explicit."""

        case = _fixture_cases()["blockage-dispatch-modes"]

        entered = dispatch_mode_transition(
            mechanism_configured=True,
            dispatch_enabled=True,
            blockage_active=True,
        )
        continued = dispatch_mode_transition(
            mechanism_configured=True,
            dispatch_enabled=entered.dispatch_enabled,
            blockage_active=True,
        )
        resumed = dispatch_mode_transition(
            mechanism_configured=True,
            dispatch_enabled=continued.dispatch_enabled,
            blockage_active=False,
        )
        already_resumed = dispatch_mode_transition(
            mechanism_configured=True,
            dispatch_enabled=resumed.dispatch_enabled,
            blockage_active=False,
        )
        absent = dispatch_mode_transition(
            mechanism_configured=False,
            dispatch_enabled=None,
            blockage_active=True,
        )

        self.assertEqual(case["expectedResults"], [
            entered.result,
            continued.result,
            resumed.result,
            already_resumed.result,
            absent.result,
        ])
        self.assertFalse(entered.dispatch_enabled)
        self.assertFalse(continued.dispatch_enabled)
        self.assertTrue(resumed.dispatch_enabled)
        self.assertTrue(already_resumed.dispatch_enabled)
        self.assertIsNone(absent.dispatch_enabled)
        self.assertFalse(absent.mutated)

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
            "UNSET": (None, False, "USER_ACTION_REQUIRED", True),
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

        unset = CoordinationSimulator.persistence_route("UNSET")
        self.assertEqual(
            "Do you want to use the available file-backed work-item provider?",
            unset.user_question,
        )
        unavailable_file_provider = CoordinationSimulator.persistence_route(
            "UNSET",
            file_provider_available=False,
        )
        self.assertEqual("BLOCKED", unavailable_file_provider.status)
        self.assertIsNone(unavailable_file_provider.user_question)

        unavailable = CoordinationSimulator.persistence_route(
            "github", selected_skill_available=False
        )
        self.assertEqual("manage-github-work-items", unavailable.management_skill)
        self.assertEqual("BLOCKED", unavailable.status)
        self.assertTrue(unavailable.zero_mutation)

    def test_new_item_notification_only_prompts_inventory_reconciliation(self) -> None:
        """Only a successful new item wakes the existing Coordinator."""

        reference = "backlog/feature-backlog/new-item.md"
        sent = CoordinationSimulator.new_item_notification(
            reference,
            creation_succeeded=True,
            item_created=True,
            coordinator_available=True,
        )
        self.assertTrue(sent.sent)
        self.assertEqual(reference, sent.provider_reference)
        self.assertTrue(sent.coordinator_reconciles_inventory)
        self.assertFalse(sent.lifecycle_mutated)

        for creation_succeeded, item_created, coordinator_available in (
            (False, False, True),
            (True, False, True),
            (True, True, False),
        ):
            with self.subTest(
                creation_succeeded=creation_succeeded,
                item_created=item_created,
                coordinator_available=coordinator_available,
            ):
                skipped = CoordinationSimulator.new_item_notification(
                    reference,
                    creation_succeeded=creation_succeeded,
                    item_created=item_created,
                    coordinator_available=coordinator_available,
                )
                self.assertFalse(skipped.sent)
                self.assertIsNone(skipped.provider_reference)
                self.assertFalse(skipped.coordinator_reconciles_inventory)
                self.assertFalse(skipped.lifecycle_mutated)

    def test_claim_retry_requires_release_or_recovery_notification(self) -> None:
        """Reject time-driven polling and consume each notification at most once."""

        case = _fixture_cases()["selected-commit-retry-and-closeout"]
        item = WorkItem("integration", "Running")
        simulator = CoordinationSimulator((item,))
        notified_retry = case["notifiedRetry"]

        simulator.record_claim_attempt(
            "integration",
            claim_kind="integration",
            outcome="CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
            blocking_claim_id="shared-generator",
        )
        with self.assertRaisesRegex(ValueError, "unsupported claim attempt outcome"):
            simulator.record_claim_attempt(
                "integration",
                claim_kind="integration",
                outcome="UNRELATED_FAILURE",
            )
        with self.assertRaisesRegex(ValueError, "direct release or recovery"):
            simulator.record_claim_attempt(
                "integration",
                claim_kind="integration",
                outcome="ACQUIRED",
                release_or_recovery_notification="timer:5m",
            )
        with self.assertRaisesRegex(ValueError, "requires a release or recovery notification"):
            simulator.record_claim_attempt(
                "integration",
                claim_kind="integration",
                outcome="CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
            )
        simulator.record_claim_attempt(
            "integration",
            claim_kind="integration",
            outcome="CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
            blocking_claim_id="replacement-owner",
            release_or_recovery_notification=notified_retry["notification"],
        )

        self.assertEqual(
            [None, notified_retry["notification"]],
            [
                attempt["releaseOrRecoveryNotification"]
                for attempt in item.claim_attempts["integration"]
            ],
        )
        self.assertEqual(case["initialAttempts"], 1)
        self.assertEqual(case["maximumUnnotifiedRetries"], 0)
        self.assertEqual("Integration Recovery", item.phase)
        self.assertEqual(("integration",), simulator.claims_requiring_recovery())
        self.assertIn("shared-generator", item.open_issues[0])
        self.assertIn("replacement-owner", item.open_issues[-1])
        with self.assertRaisesRegex(ValueError, "only one retry"):
            simulator.record_claim_attempt(
                "integration",
                claim_kind="integration",
                outcome="CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
                release_or_recovery_notification=notified_retry["notification"],
            )

    def test_release_notification_can_trigger_successful_retry(self) -> None:
        """Move directly into integration when a notified exact claim succeeds."""

        item = WorkItem("integration", "Running")
        simulator = CoordinationSimulator((item,))
        simulator.record_claim_attempt(
            "integration",
            claim_kind="integration",
            outcome="CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
            blocking_claim_id="owner",
        )
        simulator.record_claim_attempt(
            "integration",
            claim_kind="integration",
            outcome="ACQUIRED",
            release_or_recovery_notification="release:owner",
        )

        self.assertEqual("Integration", item.phase)
        self.assertEqual((), simulator.claims_requiring_recovery())
        with self.assertRaisesRegex(ValueError, "already acquired"):
            simulator.record_claim_attempt(
                "integration",
                claim_kind="integration",
                outcome="CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
            )

    def test_claim_events_reject_notified_initial_attempt_and_keep_events_independent(self) -> None:
        """Keep the first attempt immediate and each named event independent."""

        item = WorkItem("delivery", "Running")
        simulator = CoordinationSimulator((item,))
        with self.assertRaisesRegex(ValueError, "immediate attempt cannot consume"):
            simulator.record_claim_attempt(
                "delivery",
                claim_kind="integration",
                outcome="CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
                release_or_recovery_notification="release:not-yet-waiting",
            )
        simulator.record_claim_attempt(
            "delivery",
            claim_kind="completion",
            outcome="CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED",
        )
        simulator.record_claim_attempt(
            "delivery",
            claim_kind="completion",
            outcome="ACQUIRED",
            release_or_recovery_notification="release:completion-owner",
        )
        simulator.record_claim_attempt(
            "delivery",
            claim_kind="integration",
            outcome="ACQUIRED",
        )

        self.assertEqual({"integration", "completion"}, item.acquired_claims)
        self.assertEqual(
            [None, "release:completion-owner"],
            [
                attempt["releaseOrRecoveryNotification"]
                for attempt in item.claim_attempts["completion"]
            ],
        )

    def test_unresolved_notified_claim_frees_capacity_only_after_recovery(self) -> None:
        """Route an unresolved notified claim before dispatching a replacement."""

        stalled = WorkItem("stalled", "Running", phase="Integration Recovery")
        replacement = WorkItem("replacement", "Ready")
        running = [WorkItem(f"running-{index}", "Running") for index in range(9)]
        simulator = CoordinationSimulator((stalled, replacement, *running))

        simulator.dispose_unresolved_claim("stalled", user_decision=False)
        self.assertEqual("Blocked", stalled.status)
        self.assertEqual(("replacement",), simulator.dispatch_to_target())
        self.assertEqual(10, simulator.running_count())

    def test_exhausted_corrections_require_exactly_one_concrete_disposition(
        self,
    ) -> None:
        """Reject indefinite Blocked while preserving evidence for one exact outcome."""

        case = _fixture_cases()["exhausted-correction-dispositions"]
        shared = {
            "status": "Blocked",
            "canonical_task_id": "task-original",
            "canonical_thread_id": "thread-original",
            "candidate_commit": "abc123",
            "branch": "feature/original",
            "git_state": "candidate abc123 remains reachable",
            "review_verification_evidence": (
                "review finding F-17 remained after correction attempt 2",
            ),
            "live_claims": ("integration-claim:released",),
            "correction_attempt_history": case["correctionAttemptHistory"],
        }
        items = [
            WorkItem("recovery", **shared),
            WorkItem("retry", **shared),
            WorkItem("user-action", **shared),
            WorkItem("dependency", **shared),
            WorkItem("vague", **shared),
            WorkItem("multiple", **shared),
        ]
        simulator = CoordinationSimulator(items)

        recovery = simulator.record_exhausted_correction_disposition(
                "recovery",
                unresolved_findings=("F-17",),
                recovery_action="restore the missing validation fixture",
                recovery_owner="dev-coder",
                recovery_evidence="the missing fixture causes finding F-17",
                recovery_findings=("F-17",),
            )
        retry = simulator.record_exhausted_correction_disposition(
                "retry",
                unresolved_findings=("F-17",),
                retry_plan="retry only the failing validation case once",
                retry_evidence="fixture restoration directly addresses F-17",
                retry_findings=("F-17",),
                retry_limit=1,
            )
        user_action = simulator.record_exhausted_correction_disposition(
                "user-action",
                unresolved_findings=("F-17",),
                user_explanation="Only the user can select the compatibility policy.",
                user_owned_decision="choose the supported compatibility policy",
                user_question="Which compatibility behavior should remain supported?",
                user_options=("preserve legacy", "adopt corrected contract"),
                user_tradeoffs=(
                    "preserve legacy keeps compatibility but retains complexity",
                    "adopt corrected contract simplifies behavior but drops legacy input",
                ),
                unattended_work_boundary="No contract mutation continues until answered.",
            )
        dependency = simulator.record_exhausted_correction_disposition(
                "dependency",
                unresolved_findings=("F-17",),
                dependency_kind="external",
                dependency="upstream schema publication",
                dependency_owner="schema publisher",
                observable_trigger="published schema digest changes",
            )
        outcomes = {
            recovery.outcome,
            retry.outcome,
            user_action.outcome,
            dependency.outcome,
        }

        self.assertTrue(all(item.status == "Blocked" for item in items))
        self.assertTrue(all(item.blocked_disposition is None for item in items))
        self.assertEqual(
            set(case["expectedOutcomes"]),
            outcomes,
        )
        simulator.apply_blocked_disposition("recovery", recovery)
        simulator.apply_blocked_disposition("retry", retry)
        simulator.apply_blocked_disposition("user-action", user_action)
        simulator.apply_blocked_disposition("dependency", dependency)
        self.assertEqual("User Action Required", items[2].status)
        self.assertEqual("Blocked", items[3].status)
        self.assertEqual("abc123", items[3].candidate_commit)
        self.assertEqual("task-original", items[3].canonical_task_id)
        self.assertEqual(
            case["correctionAttemptHistory"],
            items[3].correction_attempt_history,
        )
        self.assertEqual("candidate abc123 remains reachable", items[3].git_state)
        self.assertEqual(
            ("review finding F-17 remained after correction attempt 2",),
            items[3].review_verification_evidence,
        )
        self.assertEqual(("integration-claim:released",), items[3].live_claims)
        with self.assertRaisesRegex(ValueError, "exactly one concrete disposition"):
            simulator.record_exhausted_correction_disposition(
                "vague",
                unresolved_findings=("F-17",),
            )
        with self.assertRaisesRegex(ValueError, "exactly one concrete disposition"):
            simulator.record_exhausted_correction_disposition(
                "multiple",
                unresolved_findings=("F-17",),
                recovery_action="restore fixture",
                recovery_owner="dev-coder",
                recovery_evidence="fixture evidence for F-17",
                recovery_findings=("F-17",),
                dependency_kind="technical",
                dependency="parser defect",
                dependency_owner="parser maintainer",
                observable_trigger="parser regression passes",
            )
        with self.assertRaisesRegex(ValueError, "active disposition"):
            simulator.record_exhausted_correction_disposition(
                "dependency",
                unresolved_findings=("F-17",),
                dependency_kind="external",
                dependency="upstream schema publication",
                dependency_owner="schema publisher",
                observable_trigger="published schema digest changes",
            )

    def test_retry_is_consumed_before_a_new_non_retry_disposition(self) -> None:
        """Permit one failed extra attempt, then prohibit another retry."""

        item = WorkItem(
            "retry",
            "Blocked",
            correction_attempt_history=["attempt 1", "attempt 2"],
        )
        simulator = CoordinationSimulator((item,))
        retry = simulator.record_exhausted_correction_disposition(
            "retry",
            unresolved_findings=("F-17",),
            retry_plan="correct the exact F-17 parser boundary once",
            retry_evidence="the new parser trace identifies the F-17 branch",
            retry_findings=("F-17",),
            retry_limit=1,
        )
        simulator.apply_blocked_disposition("retry", retry)
        simulator.finish_bounded_retry("retry", resolved=False)

        self.assertEqual("Blocked", item.status)
        self.assertTrue(item.bounded_retry_used)
        self.assertIsNone(item.blocked_disposition)
        self.assertEqual("CONSUMED", item.disposition_history[-1].state)
        with self.assertRaisesRegex(ValueError, "one unused bounded attempt"):
            simulator.record_exhausted_correction_disposition(
                "retry",
                unresolved_findings=("F-17",),
                retry_plan="try F-17 again",
                retry_evidence="repeat the same trace",
                retry_findings=("F-17",),
                retry_limit=1,
            )

        dependency = simulator.record_exhausted_correction_disposition(
            "retry",
            unresolved_findings=("F-17",),
            dependency_kind="technical",
            dependency="upstream parser release",
            dependency_owner="parser maintainer",
            observable_trigger="the F-17 parser regression passes",
        )
        simulator.apply_blocked_disposition("retry", dependency)
        self.assertEqual("CONTINUING_BLOCKED", item.blocked_disposition.outcome)

    def test_user_action_requires_a_genuine_user_owned_decision(self) -> None:
        """Reject an agent-actionable question disguised as User Action Required."""

        item = WorkItem(
            "user-action",
            "Blocked",
            correction_attempt_history=["attempt 1", "attempt 2"],
        )
        simulator = CoordinationSimulator((item,))
        with self.assertRaisesRegex(ValueError, "genuine user-owned decision"):
            simulator.record_exhausted_correction_disposition(
                "user-action",
                unresolved_findings=("F-17",),
                user_explanation="The fixture can be corrected by the coder.",
                user_question="Should the coder correct the fixture?",
                user_options=("yes", "no"),
                user_tradeoffs=("fixes the test", "leaves the test failing"),
                unattended_work_boundary="Do not edit while waiting.",
            )

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
            tuple(case["combinedRegressionVerification"]),
            CoordinationSimulator.verification_plan(combined_regression=True),
        )
        regression = case["combinedRegression"]
        self.assertIsNone(
            CoordinationSimulator.combined_regression_run(
                selected_items=regression["selectedItems"],
                merged_items=regression["incompleteMergedItems"],
                main_commit=regression["mainCommit"],
            )
        )
        expected_run = (
            regression["mainCommit"],
            tuple(regression["selectedItems"]),
        )
        self.assertEqual(
            expected_run,
            CoordinationSimulator.combined_regression_run(
                selected_items=regression["selectedItems"],
                merged_items=regression["completeMergedItems"],
                main_commit=regression["mainCommit"],
            ),
        )
        self.assertIsNone(
            CoordinationSimulator.combined_regression_run(
                selected_items=regression["selectedItems"],
                merged_items=regression["completeMergedItems"],
                main_commit=regression["mainCommit"],
                recorded_runs=[expected_run],
            )
        )
        self.assertEqual(
            (regression["mainCommit"], regression["distinctFailure"]),
            CoordinationSimulator.combined_regression_failure(
                main_commit=regression["mainCommit"],
                failure=regression["distinctFailure"],
                distinct_defect=True,
            ),
        )
        self.assertIsNone(
            CoordinationSimulator.combined_regression_failure(
                main_commit=regression["mainCommit"],
                failure=regression["distinctFailure"],
                distinct_defect=False,
            )
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
