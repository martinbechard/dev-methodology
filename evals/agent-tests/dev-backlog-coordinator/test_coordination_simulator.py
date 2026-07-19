# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# Summary: Verifies deterministic Dev Backlog Coordinator state and audit decisions.

from datetime import datetime, timezone
import unittest

from coordination_simulator import CoordinationSimulator, SUCCESSOR_CHAIN, TaskCandidate


class CoordinationSimulatorTests(unittest.TestCase):
    def test_scheduler_starts_three_scales_by_one_and_routes_finished_lane(
        self,
    ) -> None:
        simulator = CoordinationSimulator(("skill", "role", "evals", "docs"))

        self.assertEqual(
            ("skill", "role", "evals"), simulator.start_initial_campaigns()
        )
        self.assertEqual(3, len(simulator.active_campaign_ids()))
        self.assertEqual(
            ("skill", "role", "evals", "docs"),
            simulator.record_healthy_interval(),
        )
        self.assertEqual(4, simulator.active_limit)

        self.assertEqual(
            "independent review", simulator.route_finished_campaign("role")
        )
        self.assertEqual(("skill", "evals", "docs"), simulator.active_campaign_ids())
        self.assertEqual("finished-lane-routed", simulator.events[-1]["event"])

    def test_contention_wait_release_and_parent_resume_without_successor_polling(
        self,
    ) -> None:
        simulator = CoordinationSimulator()
        required = ("commit", "release event", "clean primary HEAD", "next mutation")
        obligations = simulator.seed_successor_chain(required)
        wiki_research = next(
            obligation
            for obligation in obligations
            if obligation.successor_id == "019f7a45-9c77-79c1-9c68-35cf6cb9f710"
        )

        self.assertEqual("ARTIFACT WAIT", wiki_research.phase)
        simulator.record_predecessor_release(wiki_research.source_id)
        self.assertEqual((), simulator.audit_wake_obligations(elapsed_minutes=14))
        finding = simulator.audit_wake_obligations(elapsed_minutes=15)[0]
        self.assertTrue(wiki_research.predecessor_released)
        self.assertEqual(wiki_research.source_id, finding.source_id)
        self.assertEqual(wiki_research.successor_id, finding.successor_id)
        self.assertEqual(required, finding.missing_evidence)
        self.assertTrue(finding.notification_missing)
        self.assertTrue(finding.acknowledgement_missing)

        repaired = simulator.parent_repair_baton(
            source_id=wiki_research.source_id,
            successor_id=wiki_research.successor_id,
            delivered_evidence=required,
        )
        simulator.acknowledge_resume(
            source_id=wiki_research.source_id,
            successor_id=wiki_research.successor_id,
        )
        self.assertEqual("ARTIFACT RESUME", repaired.phase)
        self.assertTrue(repaired.notified)
        self.assertTrue(repaired.acknowledged)
        self.assertEqual(0, repaired.successor_poll_count)
        self.assertEqual(15, repaired.last_audit_minutes)
        self.assertEqual((), simulator.audit_wake_obligations(elapsed_minutes=15))

    def test_concrete_successor_chain_and_wiki_research_obligation(self) -> None:
        self.assertEqual(
            (
                "019f77f4-c4bd-7c91-b197-c987a7beb838",
                "019f7a45-a697-7d80-9744-a06c8d22d69a",
                "019f7a45-9c77-79c1-9c68-35cf6cb9f710",
                "019f7a73-53f1-7b12-9f66-c4aebe6bab2e",
                "019f79e6-25ef-7b51-ab3c-39fce2656db4",
            ),
            tuple(task.task_id for task in SUCCESSOR_CHAIN),
        )
        self.assertEqual("Wiki Research", SUCCESSOR_CHAIN[2].label)

    def test_mismatched_isolated_checkout_refuses_lifecycle_and_artifact_go(
        self,
    ) -> None:
        simulator = CoordinationSimulator(("skill", "role", "evals"))

        decision = simulator.lifecycle_start(
            checkout="isolated", primary_backlog_mutation_active=True
        )

        self.assertEqual("PRIMARY_REQUIRED", decision["outcome"])
        self.assertFalse(decision["artifact_go"])
        self.assertEqual((), simulator.active_campaign_ids())

    def test_settled_matches_prevent_retry_and_contain_duplicate(self) -> None:
        common = {
            "parent_task_id": "parent-123",
            "backlog_path": "backlog/feature-backlog/example.md",
            "normalized_objective": "coordinate example delivery",
            "status": "waiting",
        }
        canonical = TaskCandidate(
            task_id="task-original",
            created_at=datetime(2026, 7, 19, 10, 0, tzinfo=timezone.utc),
            title="Preflight work item",
            **common,
        )
        duplicate = TaskCandidate(
            task_id="task-duplicate",
            created_at=datetime(2026, 7, 19, 10, 0, 2, tzinfo=timezone.utc),
            title="Generic old title",
            **common,
        )

        result = CoordinationSimulator.reconcile_ambiguous_dispatch(
            immediate_matches=(), settled_matches=(duplicate, canonical)
        )

        self.assertEqual("task-original", result.canonical_task_id)
        self.assertEqual(("task-duplicate",), result.contained_duplicate_ids)
        self.assertEqual(
            ("stop", "verify stopped and no mutation", "archive when supported"),
            result.duplicate_containment_steps,
        )
        self.assertEqual(0, result.evidence()["expectedRetryCount"])

    def test_success_title_is_exact_done_title(self) -> None:
        self.assertEqual(
            "Done — Codex work-item coordination",
            CoordinationSimulator.success_title("Codex work-item coordination"),
        )


if __name__ == "__main__":
    unittest.main()
