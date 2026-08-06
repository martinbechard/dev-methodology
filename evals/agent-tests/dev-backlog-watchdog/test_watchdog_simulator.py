#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies read-only active, blocked, and terminal campaign reconciliation.
# Governing design: design/orchestrated-development-lifecycle.html
# Governing test plan: evals/agent-tests/dev-backlog-watchdog/requirements-matrix.md

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import unittest

import yaml

from watchdog_simulator import (
    ArchivePauseEvidence,
    CoordinatorDisposition,
    DispositionReceipt,
    WorkItem,
    WatchdogCycle,
    active_capacity,
    backlog_blockage_reasons,
    observe_backlog_blockage,
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

    def test_backlog_blockage_declaration_criteria_are_deterministic(self) -> None:
        """Each automatic criterion and the user declaration have a direct result."""

        five_blocked = [
            WorkItem(f"blocked-{index}", "Blocked", preventing_cause="shared")
            for index in range(5)
        ]
        self.assertEqual(
            (
                "five-or-more-blocked",
                "all-active-work-blocked",
                "shared-blocker",
            ),
            backlog_blockage_reasons(five_blocked),
        )
        self.assertEqual(
            ("all-active-work-blocked",),
            backlog_blockage_reasons([WorkItem("one", "Blocked")]),
        )
        self.assertEqual(
            ("shared-blocker",),
            backlog_blockage_reasons(
                [
                    WorkItem(
                        f"blocked-{index}",
                        "Blocked",
                        preventing_cause="same dependency",
                    )
                    for index in range(3)
                ]
                + [WorkItem("ready", "Ready")]
            ),
        )
        self.assertEqual(
            ("no-progress-for-sixty-minutes",),
            backlog_blockage_reasons(
                [WorkItem("ready", "Ready")],
                minutes_without_progress=60,
            ),
        )
        self.assertEqual(
            ("user-declared",),
            backlog_blockage_reasons([], user_declared=True),
        )

    def test_blockage_counts_exclude_deferred_and_terminal_items(self) -> None:
        """Deferred and terminal records do not create an automatic blockage."""

        excluded = [
            WorkItem(status.lower().replace(" ", "-"), status)
            for status in (
                "User Action Required",
                "Holding",
                "Future Idea",
                "Completed",
                "Failed",
                "Abandoned",
            )
        ]
        self.assertEqual((), backlog_blockage_reasons(excluded))

    def test_active_blockage_observation_is_idempotent_and_read_only(self) -> None:
        """Report continued recovery once and surface a satisfied exit without mutation."""

        active = observe_backlog_blockage(
            active=True,
            exit_conditions_satisfied=False,
            state_already_reported=False,
        )
        repeated = observe_backlog_blockage(
            active=True,
            exit_conditions_satisfied=False,
            state_already_reported=True,
        )
        recovered = observe_backlog_blockage(
            active=True,
            exit_conditions_satisfied=True,
            state_already_reported=False,
        )

        self.assertEqual("ACTIVE", active.status)
        self.assertTrue(active.alert_parent)
        self.assertEqual("ACTIVE_UNCHANGED", repeated.status)
        self.assertFalse(repeated.alert_parent)
        self.assertEqual("RECOVERY_READY", recovered.status)
        self.assertTrue(recovered.alert_parent)
        self.assertFalse(active.mutated)
        self.assertFalse(repeated.mutated)
        self.assertFalse(recovered.mutated)

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

    def test_task_state_anomalies_use_status_specific_actions(self) -> None:
        """All six task anomalies alert without confusing startup with Stalled."""

        provider_boundaries = {
            "Starting": "provider reservation",
            "Running": "provider record",
        }
        for status in ("Starting", "Running"):
            for task_state in ("stopped", "failed", "missing"):
                with self.subTest(status=status, task_state=task_state):
                    identity = f"{status.lower()}-{task_state}"
                    item = WorkItem(
                        provider_identity=(
                            f"backlog/feature-backlog/{identity}.md"
                        ),
                        status=status,
                        task_state=task_state,
                        canonical_thread=f"thread-{identity}",
                        root_task=f"task-{identity}",
                    )
                    before = deepcopy(item)

                    result = WatchdogCycle().evaluate([item])

                    self.assertEqual("ALERT", result.status)
                    self.assertEqual(before, item)
                    self.assertIsNotNone(result.alert)
                    alert = result.alert
                    assert alert is not None
                    expected_reason = (
                        f"{status} canonical task {task_state}; task-state "
                        "boundary requires Coordinator attention"
                    )
                    expected_action = (
                        f"Coordinator reconciles the {status} task, "
                        f"{provider_boundaries[status]}, and ownership before "
                        "choosing any lifecycle disposition"
                    )
                    self.assertEqual(item.provider_identity, alert.provider_identity)
                    self.assertIn("task_boundary_crossed=true", alert.evidence)
                    self.assertIn(f"task_state={task_state}", alert.evidence)
                    self.assertIn(
                        f"canonical_thread=thread-{identity}",
                        alert.evidence,
                    )
                    self.assertIn(f"root_task=task-{identity}", alert.evidence)
                    self.assertEqual(expected_reason, alert.reason)
                    self.assertEqual(expected_action, alert.recommended_action)
                    self.assertNotIn("Stalled", alert.recommended_action)
                    self.assertFalse(result.mutated)

    def test_task_state_anomaly_preserves_known_cause_blocked_route(self) -> None:
        """Mechanical reconciliation precedes the known-cause Blocked choice."""

        item = WorkItem(
            provider_identity="backlog/defect-backlog/running-failed-known.md",
            status="Running",
            task_state="failed",
            canonical_thread="thread-running-failed-known",
            root_task="task-running-failed-known",
            preventing_cause="upstream credential is unavailable",
        )

        result = WatchdogCycle().evaluate([item])

        self.assertIsNotNone(result.alert)
        alert = result.alert
        assert alert is not None
        self.assertEqual(
            "Running canonical task failed; task-state boundary requires "
            "Coordinator attention with a known preventing cause",
            alert.reason,
        )
        self.assertEqual(
            "Coordinator reconciles the Running task, provider record, and "
            "ownership, then validates the separate known cause and "
            "Coordinator-owned action before choosing the Blocked disposition",
            alert.recommended_action,
        )
        self.assertEqual(
            "upstream credential is unavailable",
            alert.preventing_cause,
        )

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

    def test_every_blocked_item_retains_reconciliation_even_when_only_one_alerts(
        self,
    ) -> None:
        """Retain complete per-item evidence while alerting only actionable Blocked work."""

        case = self.cases["blocked-reconciliation-cycle"]
        items = [WorkItem(**item) for item in case["items"]]
        before = deepcopy(items)

        result = WatchdogCycle().evaluate(items)

        self.assertEqual(before, items)
        self.assertEqual("ALERT", result.status)
        self.assertEqual(2, len(result.blocked_reconciliations))
        self.assertEqual(
            tuple(item.provider_identity for item in items),
            tuple(
                reconciliation.provider_identity
                for reconciliation in result.blocked_reconciliations
            ),
        )
        quiet, actionable = result.blocked_reconciliations
        self.assertFalse(quiet.actionable_reasons)
        self.assertEqual(
            tuple(case["expectedActionableReasons"]),
            actionable.actionable_reasons,
        )
        self.assertIn("candidate def456 preserved", actionable.candidate_evidence)
        self.assertIn(
            "correction attempts exhausted without current disposition",
            result.alert.reason if result.alert else "",
        )
        self.assertNotIn(
            "provider:quiet-blocked",
            result.alert.provider_identity if result.alert else "",
        )
        for provider in case["expectedAlertProviders"]:
            self.assertIn(
                provider,
                result.alert.provider_identity if result.alert else "",
            )

    def test_malformed_disposition_alerts_and_preserves_attempt_history(self) -> None:
        """A vague receipt cannot suppress an exhausted-correction alert."""

        item = WorkItem(
            provider_identity="provider:malformed-disposition",
            status="Blocked",
            preventing_cause="review finding F-17 remains",
            blocker_owner="dev-backlog-coordinator",
            unblock_condition="record one complete disposition",
            next_action_owner="dev-backlog-coordinator",
            git_state="candidate abc123 is preserved",
            correction_attempts_exhausted=True,
            correction_attempt_history=("attempt 1", "attempt 2"),
            current_disposition=DispositionReceipt(
                outcome="CONTINUING_BLOCKED",
                state="APPLIED",
                owner="",
                evidence="wait later",
                observable_trigger="",
                unresolved_findings=("F-17",),
            ),
        )

        result = WatchdogCycle().evaluate((item,))

        self.assertEqual("ALERT", result.status)
        reconciliation = result.blocked_reconciliations[0]
        self.assertEqual(
            ("attempt 1", "attempt 2"),
            reconciliation.correction_attempt_history,
        )
        self.assertIs(item.current_disposition, reconciliation.current_disposition)
        self.assertIn(
            "missing, vague, expired, or inconsistent",
            result.alert.reason if result.alert else "",
        )

    def test_each_blocked_alert_trigger_is_observable(self) -> None:
        """Exercise every reason that requires Coordinator reconciliation."""

        base = {
            "status": "Blocked",
            "preventing_cause": "delivery cannot continue",
            "blocker_owner": "external owner",
            "unblock_condition": "blocking evidence changes",
            "next_action_owner": "dev-backlog-coordinator",
            "git_state": "candidate abc123 is preserved",
            "current_disposition": DispositionReceipt(
                outcome="CONTINUING_BLOCKED",
                state="APPLIED",
                owner="dev-backlog-coordinator",
                evidence="external dependency remains unavailable",
                observable_trigger="dependency health check passes",
                unresolved_findings=("F-17",),
            ),
        }
        cases = (
            (
                "dependency",
                {"dependency_or_unblock_satisfied": True},
                "Blocked recovery requires Coordinator attention",
            ),
            (
                "recovery",
                {"agent_actionable_recovery": "restore the fixture"},
                "agent-actionable recovery is available",
            ),
            (
                "lifecycle",
                {"lifecycle_evidence_issue": "provider and task disagree"},
                "lifecycle evidence is stale or contradictory",
            ),
            (
                "owner",
                {"next_action_owner_correct": False},
                "next-action owner is incorrect",
            ),
        )

        for name, overrides, expected in cases:
            with self.subTest(name=name):
                item = WorkItem(
                    provider_identity=f"provider:{name}",
                    **base,
                    **overrides,
                )
                result = WatchdogCycle().evaluate((item,))
                self.assertEqual("ALERT", result.status)
                self.assertIn(expected, result.alert.reason if result.alert else "")

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

    def test_valid_archive_pause_suppresses_only_named_task_archival(self) -> None:
        """A current named-task pause leaves independent Git cleanup actionable."""

        case = self.cases["terminal-archive-pause-cleanup"]
        pause = ArchivePauseEvidence(**case["archive_pause"])
        item = WorkItem(**case["item"], archive_pause=pause)
        before = deepcopy(item)

        result = WatchdogCycle().evaluate((item,))

        self.assertEqual(before, item)
        self.assertEqual("ALERT", result.status)
        self.assertEqual(1, len(result.terminal_reconciliations))
        reconciliation = result.terminal_reconciliations[0]
        self.assertTrue(reconciliation.archive_pause_valid)
        self.assertIs(pause, reconciliation.archive_pause)
        self.assertIn(case["expectedAction"], reconciliation.actionable_reasons)
        self.assertNotIn("archive Codex task", reconciliation.actionable_reasons)
        self.assertIn(item.root_task, result.alert.evidence if result.alert else "")
        self.assertIn("scope='codex-task-archival'", result.alert.evidence if result.alert else "")

    def test_default_archival_requires_no_inferred_or_campaign_pause(self) -> None:
        """Only current, exact, acknowledged user direction can pause archival."""

        case = self.cases["terminal-default-archival"]
        pauses = (
            None,
            ArchivePauseEvidence(
                source="earlier-conversation",
                scope="codex-task-archival",
                task_ids=(case["item"]["root_task"],),
                evidence="an earlier campaign pause was mentioned",
                acknowledged=True,
            ),
            ArchivePauseEvidence(
                source="current-user-direction",
                scope="campaign",
                task_ids=(case["item"]["root_task"],),
                evidence="pause the campaign",
                acknowledged=True,
            ),
            ArchivePauseEvidence(
                source="current-user-direction",
                scope="codex-task-archival",
                task_ids=("another-task",),
                evidence="pause another task",
                acknowledged=True,
            ),
            ArchivePauseEvidence(
                source="current-user-direction",
                scope="codex-task-archival",
                task_ids=(case["item"]["root_task"],),
                evidence="",
                acknowledged=False,
            ),
        )

        for pause in pauses:
            with self.subTest(pause=pause):
                item = WorkItem(**case["item"], archive_pause=pause)
                result = WatchdogCycle().evaluate((item,))
                reconciliation = result.terminal_reconciliations[0]
                self.assertEqual("ALERT", result.status)
                self.assertFalse(reconciliation.archive_pause_valid)
                self.assertIn(case["expectedAction"], reconciliation.actionable_reasons)

    def test_preserved_source_branch_does_not_hide_removable_worktree(self) -> None:
        """A retained non-equivalent source branch does not retain its clean worktree."""

        case = self.cases["terminal-preserved-branch-removable-worktree"]
        item = WorkItem(**case["item"])

        result = WatchdogCycle().evaluate((item,))

        reconciliation = result.terminal_reconciliations[0]
        self.assertTrue(reconciliation.source_branch_deliberately_preserved)
        self.assertEqual(case["expectedPreservedBranch"], reconciliation.source_branch)
        self.assertEqual((case["expectedAction"],), reconciliation.actionable_reasons)
        self.assertEqual("ALERT", result.status)

    def test_terminal_cycle_aggregates_every_task_anomaly(self) -> None:
        """One alert retains every terminal task and its smallest required action."""

        case = self.cases["terminal-aggregate-anomalies"]
        items = [WorkItem(**item) for item in case["items"]]

        result = WatchdogCycle().evaluate(items)

        self.assertEqual("ALERT", result.status)
        self.assertEqual(len(items), len(result.terminal_reconciliations))
        self.assertIn("one aggregate parent alert", result.message)
        for task_id in case["expectedTasks"]:
            with self.subTest(task_id=task_id):
                self.assertIn(task_id, result.alert.evidence if result.alert else "")
        for action in case["expectedActions"]:
            with self.subTest(action=action):
                self.assertIn(action, result.alert.recommended_action if result.alert else "")

    def test_terminal_no_action_requires_complete_reconciliation(self) -> None:
        """NO_ACTION is available only when every terminal action is complete."""

        case = self.cases["terminal-completely-reconciled"]
        item = WorkItem(**case["item"])

        result = WatchdogCycle().evaluate((item,))

        self.assertEqual("NO_ACTION", result.status)
        self.assertIsNone(result.alert)
        self.assertFalse(result.terminal_reconciliations[0].actionable_reasons)

    def test_terminal_no_action_rejects_each_unacknowledged_dimension(self) -> None:
        """Each incomplete terminal dimension independently prevents NO_ACTION."""

        baseline = dict(self.cases["terminal-completely-reconciled"]["item"])
        cases = (
            ("task identity", {"root_task": ""}, "identify canonical Codex task"),
            ("provider", {"provider_terminal_evidence": False}, "confirm provider terminal evidence"),
            ("delivery", {"code_merged": False}, "confirm merged delivery"),
            ("claim", {"live_claims": ["work-item:live"]}, "release live claim"),
            (
                "missing claim release",
                {"claim_applicability": "applicable", "released_claims": []},
                "reconcile applicable terminal claim",
            ),
            (
                "unknown claim applicability",
                {"claim_applicability": "unknown", "released_claims": []},
                "determine terminal claim applicability",
            ),
            ("worktree", {"worktree_disposition": "clean-removable"}, "remove clean terminal worktree"),
            ("delivery branch", {"delivery_branch_disposition": "unmerged"}, "reconcile delivery branch disposition"),
            ("cleanup branch", {"cleanup_branch_disposition": "cleanup-eligible"}, "clean up terminal branch"),
            ("source branch", {"source_branch_disposition": "cleanup-eligible"}, "clean up terminal source branch"),
            ("notification", {"notification_pending": True}, "resolve terminal notification"),
            ("archival", {"codex_archived": False}, "archive Codex task"),
        )

        for name, overrides, expected_action in cases:
            with self.subTest(name=name):
                evidence = {**baseline, **overrides}
                result = WatchdogCycle().evaluate((WorkItem(**evidence),))
                self.assertEqual("ALERT", result.status)
                self.assertIn(
                    expected_action,
                    result.terminal_reconciliations[0].actionable_reasons,
                )

    def test_failed_and_abandoned_do_not_require_merged_delivery(self) -> None:
        """Failed and Abandoned reconcile terminal evidence without inventing merge."""

        case = self.cases["terminal-failed-and-abandoned"]
        for item_evidence in case["items"]:
            with self.subTest(status=item_evidence["status"]):
                result = WatchdogCycle().evaluate((WorkItem(**item_evidence),))
                reconciliation = result.terminal_reconciliations[0]
                self.assertEqual("ALERT", result.status)
                self.assertEqual(
                    (case["expectedAction"],),
                    reconciliation.actionable_reasons,
                )
                self.assertNotIn(
                    "confirm merged delivery",
                    reconciliation.actionable_reasons,
                )

                archived = {**item_evidence, "codex_archived": True}
                archived_result = WatchdogCycle().evaluate((WorkItem(**archived),))
                self.assertEqual("NO_ACTION", archived_result.status)

    def test_terminal_claim_applicability_requires_explicit_evidence(self) -> None:
        """Unknown, non-applicable, and applicable claim states stay distinct."""

        case = self.cases["terminal-claim-applicability"]
        unknown = WatchdogCycle().evaluate((WorkItem(**case["unknown"]),))
        not_applicable = WatchdogCycle().evaluate(
            (WorkItem(**case["notApplicable"]),)
        )
        missing_release = WatchdogCycle().evaluate(
            (WorkItem(**case["applicableMissingRelease"]),)
        )

        self.assertEqual("ALERT", unknown.status)
        self.assertIn(
            case["expectedUnknownAction"],
            unknown.terminal_reconciliations[0].actionable_reasons,
        )
        self.assertEqual("NO_ACTION", not_applicable.status)
        self.assertTrue(
            not_applicable.terminal_reconciliations[0].claim_reconciliation_complete
        )
        self.assertEqual("ALERT", missing_release.status)
        self.assertIn(
            case["expectedMissingReleaseAction"],
            missing_release.terminal_reconciliations[0].actionable_reasons,
        )

    def test_preservation_alert_repeats_only_when_evidence_changes(self) -> None:
        """Unchanged acknowledged retention stays quiet; changed evidence alerts again."""

        case = self.cases["terminal-preservation-evidence-change"]
        unchanged = WorkItem(**case["unchanged"])
        changed = WorkItem(**case["changed"])
        cleanup_eligible = WorkItem(**case["cleanupEligible"])

        unchanged_result = WatchdogCycle().evaluate((unchanged,))
        changed_result = WatchdogCycle().evaluate((changed,))
        cleanup_result = WatchdogCycle().evaluate((cleanup_eligible,))

        self.assertEqual("NO_ACTION", unchanged_result.status)
        self.assertEqual("ALERT", changed_result.status)
        self.assertIn(
            case["expectedChangedAction"],
            changed_result.terminal_reconciliations[0].actionable_reasons,
        )
        changed_evidence = changed_result.alert.evidence if changed_result.alert else ""
        self.assertIn(
            f"acknowledged_source_branch_preservation_evidence={case['expectedPreviousEvidence']}",
            changed_evidence,
        )
        self.assertIn(
            f"source_branch_preservation_evidence={case['expectedCurrentEvidence']}",
            changed_evidence,
        )
        self.assertEqual("ALERT", cleanup_result.status)
        self.assertIn(
            case["expectedCleanupAction"],
            cleanup_result.terminal_reconciliations[0].actionable_reasons,
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

    def test_blocked_and_user_action_dispositions_reject_incomplete_evidence(self) -> None:
        """Each nonterminal disposition requires its complete durable evidence."""

        disposition = CoordinatorDisposition()
        cases = self.cases["stalled-dispositions"]
        evidence_cases = (
            (
                "knownBlocker",
                (
                    "blocker_cause",
                    "blocker_owner",
                    "unblock_condition",
                    "coordinator_action",
                ),
                "Blocked disposition requires",
            ),
            (
                "userAction",
                (
                    "user_owned_action",
                    "user_question",
                    "unattended_work_boundary",
                ),
                "User Action Required disposition requires",
            ),
        )
        for case_name, fields, error in evidence_cases:
            for missing_field in fields:
                with self.subTest(
                    case_name=case_name,
                    missing_field=missing_field,
                ):
                    incomplete = dict(cases[case_name])
                    incomplete[missing_field] = " \t "
                    with self.assertRaisesRegex(ValueError, error):
                        disposition.choose(**incomplete)

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
        for status in ("Failed", "Abandoned"):
            with self.subTest(status=status):
                with self.assertRaisesRegex(ValueError, "terminal status and evidence"):
                    terminal_archive_destination("Feature", status, False)
                self.assertEqual(
                    "backlog/failed-backlog/features",
                    terminal_archive_destination("Feature", status, True),
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
