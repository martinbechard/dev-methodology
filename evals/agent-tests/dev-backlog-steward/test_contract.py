# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies Dev Backlog Steward blocked-work resumption and Future Ideas evaluation contracts.
# Governing design: evals/agent-tests/dev-backlog-steward/skills/dev-backlog-steward-suite-contract/SKILL.md
# Governing test plan: evals/agent-tests/dev-backlog-steward/scenarios.yaml

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

import yaml


SUITE_ROOT = Path(__file__).resolve().parent
_HARNESS_PATH = SUITE_ROOT / "contract_harness.py"
_SPEC = importlib.util.spec_from_file_location(
    "dev_backlog_steward_contract_harness", _HARNESS_PATH
)
assert _SPEC is not None and _SPEC.loader is not None
contract_harness = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = contract_harness
_SPEC.loader.exec_module(contract_harness)


class DevBacklogStewardContractTests(unittest.TestCase):
    """Protect explicit claim acquisition and evidence preservation during resumption."""

    def test_blocked_handoff_releases_prior_ownership_and_preserves_evidence(self) -> None:
        """A blocked handoff ends the prior claim without losing durable evidence."""
        fixture = yaml.safe_load(
            (SUITE_ROOT / "fixtures" / "cases.yaml").read_text(encoding="utf-8")
        )["cases"]["blocked-state-transition"]
        before = fixture["itemBefore"].encode("utf-8")

        after, transitions = contract_harness.block_for_handoff(before)

        self.assertEqual(("running", "blocked", "released"), transitions)
        expected = before.replace(b"Status: Running", b"Status: Blocked", 1)
        expected = expected.replace(b"Owner: dev-coder", b"Owner: Unowned", 1)
        expected = expected.replace(
            b"Claim: schema-migration-active", b"Claim: None", 1
        )
        self.assertEqual(expected, after)
        for preserved_line in (
            b"Blocker: External schema decision is unavailable.",
            b"Unblock Condition: Approved schema decision is recorded.",
            b"Evidence: Existing schema analysis and verification log.",
            (
                b"Acceptance Criteria: Schema decision remains traceable; "
                b"existing verification remains required."
            ),
        ):
            with self.subTest(preserved_line=preserved_line):
                self.assertIn(preserved_line, after)

    def test_future_ideas_case_and_output_contract_are_aligned(self) -> None:
        """Every suite surface exposes a meaningful Future Idea output contract."""
        fixture = yaml.safe_load(
            (SUITE_ROOT / "fixtures" / "cases.yaml").read_text(encoding="utf-8")
        )["cases"]["future-ideas-capture-and-promotion"]
        scenarios = yaml.safe_load(
            (SUITE_ROOT / "scenarios.yaml").read_text(encoding="utf-8")
        )["scenarios"]
        scenario = next(
            entry
            for entry in scenarios
            if entry["id"] == "future-ideas-capture-and-promotion"
        )
        suite = yaml.safe_load(
            (SUITE_ROOT / "suite.yaml").read_text(encoding="utf-8")
        )
        role = yaml.safe_load(
            (
                SUITE_ROOT.parent.parent.parent
                / "agents"
                / "roles"
                / "dev-activities"
                / "dev-backlog-steward.role.yaml"
            ).read_text(encoding="utf-8")
        )
        expected_output = "backlog item, Future Idea, or status update"

        self.assertEqual("file", fixture["provider"])
        self.assertEqual("github", fixture["nonFileProviderWithoutOverride"])
        self.assertIn("BLOCKED", fixture["nonFileProviderResult"])
        self.assertFalse(fixture["ordinaryScanIncludesIdea"])
        self.assertNotIn("Status:", fixture["ideaBefore"])
        self.assertIn("Completion: direct-main", fixture["promotedWorkItem"])
        self.assertIn("## Open Questions", fixture["promotedWorkItem"])
        self.assertEqual(expected_output, fixture["expectedOutput"])
        self.assertIn(expected_output, scenario["expectedOutputs"])
        self.assertIn(expected_output, suite["target"]["requiredOutputs"])
        self.assertIn(
            expected_output,
            [next(iter(entry)) for entry in role["outputContract"]],
        )
        self.assertIn(
            "Return the Future Idea output contract", scenario["requiredBehaviors"]
        )

    def test_future_idea_promotion_is_failure_atomic_at_every_boundary(self) -> None:
        """Collision and injected failures restore exact pre-attempt promotion state."""
        fixture = yaml.safe_load(
            (SUITE_ROOT / "fixtures" / "cases.yaml").read_text(encoding="utf-8")
        )["cases"]["future-ideas-capture-and-promotion"]
        scenario = next(
            entry
            for entry in yaml.safe_load(
                (SUITE_ROOT / "scenarios.yaml").read_text(encoding="utf-8")
            )["scenarios"]
            if entry["id"] == "future-ideas-capture-and-promotion"
        )
        contract_text = (
            SUITE_ROOT
            / "skills"
            / "dev-backlog-steward-suite-contract"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        role = yaml.safe_load(
            (
                SUITE_ROOT.parent.parent.parent
                / "agents"
                / "roles"
                / "dev-activities"
                / "dev-backlog-steward.role.yaml"
            ).read_text(encoding="utf-8")
        )
        transaction = fixture["promotionTransaction"]
        collision = transaction["collision"]

        self.assertEqual("BLOCKED", collision["result"])
        self.assertFalse(collision["writesAttempted"])
        self.assertEqual(collision["ideaBefore"], collision["ideaAfter"])
        self.assertEqual(collision["targetBefore"], collision["targetAfter"])
        self.assertEqual(
            {"target-write", "idea-write", "validation", "commit"},
            {
                failure["boundary"]
                for failure in transaction["injectedFailures"]
            },
        )
        for failure in transaction["injectedFailures"]:
            with self.subTest(boundary=failure["boundary"]):
                self.assertEqual(failure["ideaBefore"], failure["ideaAfter"])
                if failure["targetExistedBefore"]:
                    self.assertEqual(failure["targetBefore"], failure["targetAfter"])
                else:
                    self.assertEqual("absent", failure["targetAfter"])
                self.assertEqual(
                    "remove only a target created by this attempt",
                    failure["cleanupScope"],
                )

        for behavior in (
            "Preflight target collisions before any promotion write",
            "Snapshot exact idea bytes target bytes and target existence",
            "Restore exact pre-attempt state after target-write idea-write validation or commit failure",
        ):
            with self.subTest(required_behavior=behavior):
                self.assertIn(behavior, scenario["requiredBehaviors"])
        self.assertIn("failure-atomic transaction", contract_text)
        self.assertIn("target-write, idea-write, validation, or commit", contract_text)
        self.assertTrue(
            any(
                "Restore the exact pre-attempt idea and target state"
                in step
                for step in role["instructions"]["failureHandling"]
            )
        )

    def test_blocked_resumption_has_negative_and_positive_scenarios(self) -> None:
        """The suite covers unowned, failed-claim, and successful claim outcomes."""
        scenarios = yaml.safe_load(
            (SUITE_ROOT / "scenarios.yaml").read_text(encoding="utf-8")
        )["scenarios"]
        by_id = {scenario["id"]: scenario for scenario in scenarios}

        shortcut = by_id["blocked-unowned-running-shortcut"]
        self.assertEqual("BLOCKED", shortcut["expectedTerminalStatus"])
        self.assertIn("Leave the backlog item unchanged", shortcut["requiredBehaviors"])
        self.assertIn(
            "Reject because no new claim and owner exist",
            shortcut["requiredBehaviors"],
        )

        resumption = by_id["blocked-claimed-resumption"]
        self.assertEqual("PASS", resumption["expectedTerminalStatus"])
        self.assertIn(
            "Record Ready then a successful new claim and owner before Running",
            resumption["requiredBehaviors"],
        )

        failed_claim = by_id["blocked-failed-claim-resumption"]
        self.assertEqual("BLOCKED", failed_claim["expectedTerminalStatus"])
        self.assertIn("CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED", failed_claim["initialState"])
        self.assertIn("project-hash-policy", failed_claim["deterministicChecks"])

    def test_failed_or_missing_claim_leaves_the_item_unchanged(self) -> None:
        """Missing and conflict-wait claim outcomes keep exact blocked bytes and evidence."""
        cases = yaml.safe_load(
            (SUITE_ROOT / "fixtures" / "cases.yaml").read_text(encoding="utf-8")
        )["cases"]

        expected_transitions = {
            "blocked-unowned-running-shortcut": ("blocked", "rejected-unowned"),
            "blocked-failed-claim-resumption": (
                "blocked",
                "ready",
                "claim-failed",
                "blocked",
            ),
        }
        for case_id, transitions_expected in expected_transitions.items():
            fixture = cases[case_id]
            before = fixture["itemBefore"].encode("utf-8")
            claim_outcomes = [fixture["claimOutcome"]]
            claim_outcomes.extend(fixture.get("otherFailedClaimOutcomes", []))
            for claim_outcome in claim_outcomes:
                after, transitions = contract_harness.attempt_resumption(
                    before,
                    unblock_condition_satisfied=fixture["unblockConditionSatisfied"],
                    claim_outcome=claim_outcome,
                )

                with self.subTest(case_id=case_id, claim_outcome=claim_outcome):
                    self.assertEqual(before, after)
                    self.assertEqual(transitions_expected, transitions)
                    self.assertIn(b"Status: Blocked", after)
                    self.assertIn(b"Owner: Unowned", after)
                    self.assertIn(b"Claim: None", after)
                    self.assertNotIn(b"Status: Running", after)

    def test_successful_claim_resumes_in_order_and_preserves_evidence(self) -> None:
        """A new claim and owner precede Running without rewriting prior evidence."""
        fixture = yaml.safe_load(
            (SUITE_ROOT / "fixtures" / "cases.yaml").read_text(encoding="utf-8")
        )["cases"]["blocked-claimed-resumption"]
        before = fixture["itemBefore"].encode("utf-8")

        after, transitions = contract_harness.attempt_resumption(
            before,
            unblock_condition_satisfied=fixture["unblockConditionSatisfied"],
            claim_outcome=fixture["claimOutcome"],
            new_owner=fixture["newOwner"],
            new_claim=fixture["newClaim"],
        )

        self.assertEqual(("blocked", "ready", "claimed", "running"), transitions)
        self.assertLess(transitions.index("ready"), transitions.index("claimed"))
        self.assertLess(transitions.index("claimed"), transitions.index("running"))
        expected = before.replace(b"Status: Blocked", b"Status: Running", 1)
        expected = expected.replace(b"Owner: Unowned", b"Owner: dev-coder", 1)
        expected = expected.replace(
            b"Claim: None", b"Claim: schema-migration-resumption", 1
        )
        self.assertEqual(expected, after)
        for preserved_line in (
            b"Blocker: External schema decision is unavailable.",
            b"Unblock Condition: Approved schema decision is recorded.",
            b"Evidence: Existing schema analysis and verification log.",
            (
                b"Acceptance Criteria: Schema decision remains traceable; "
                b"existing verification remains required."
            ),
        ):
            with self.subTest(preserved_line=preserved_line):
                self.assertIn(preserved_line, after)


if __name__ == "__main__":
    unittest.main()
