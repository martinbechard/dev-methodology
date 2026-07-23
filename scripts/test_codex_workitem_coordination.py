# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
"""Focused contract tests for Codex work-item coordination guidance."""

import json
from pathlib import Path
import unittest

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = REPOSITORY_ROOT / "skills" / "codex-workitem-coordination" / "SKILL.md"
ROLE_PATH = (
    REPOSITORY_ROOT
    / "agents"
    / "roles"
    / "dev-activities"
    / "dev-orchestrator.role.yaml"
)


class CodexWorkItemCoordinationWatchdogTests(unittest.TestCase):
    """Keep watchdog authority and notification boundaries explicit."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.skill_text = SKILL_PATH.read_text(encoding="utf-8")
        heading = "### Dedicated Read-Only Watchdog"
        if heading not in cls.skill_text:
            raise AssertionError(f"missing watchdog section: {heading}")
        cls.watchdog_section = cls.skill_text.split(heading, 1)[1].split("\n## ", 1)[0]

    def test_watchdog_is_one_scheduled_read_only_observer(self) -> None:
        required = (
            "one dedicated watchdog task",
            "schedule it to observe the fifteen-minute review checks",
            "never performs the parent review's scheduling or recovery adjustment",
            "observer, not a work-item owner, queue entry, Running slot, durable record",
            "must remain read-only",
            "does not mutate repository files or lifecycle state",
            "does not create a replacement ledger or duplicate watchdog",
        )
        for clause in required:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.watchdog_section)

    def test_watchdog_checks_blocked_running_and_terminal_boundaries(self) -> None:
        required = (
            "published estimate, hard stop, and latest evidence-bearing progress",
            "Blocked item's exact blocker and unblock condition",
            "accepted work stranded before integration",
            "integrated work awaiting provider closeout",
            "terminal work awaiting cleanup",
            "stale, unsafe, or unnecessarily broad shared-resource ownership",
        )
        for clause in required:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.watchdog_section)

    def test_watchdog_alerts_only_for_actionable_attention(self) -> None:
        required = (
            "Notify the parent only when an actionable condition exists",
            "affected item or task",
            "observed evidence",
            "why attention is required now",
            "smallest recommended parent action",
            "without messaging or interrupting the parent",
            "this self-report is its only task-state exception",
            "The parent retains every scheduling, lifecycle, ownership, recovery, dispatch, integration, and cleanup decision",
        )
        for clause in required:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.watchdog_section)


class AwaitingReviewPersistenceContractTests(unittest.TestCase):
    """Keep nonterminal and terminal Persistence updates distinct and idempotent."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.skill_text = SKILL_PATH.read_text(encoding="utf-8")
        cls.role_text = json.dumps(
            yaml.safe_load(ROLE_PATH.read_text(encoding="utf-8")),
            sort_keys=True,
        )

    def test_coordination_records_awaiting_review_once_before_terminal_closure(self) -> None:
        required = (
            "ask Dev Backlog Steward exactly once to record the nonterminal lifecycle AWAITING_REVIEW",
            "reconcile the existing update instead of dispatching a duplicate",
            "Never request lifecycle COMPLETED from an AWAITING_REVIEW handoff",
            "ask Dev Backlog Steward exactly once for the distinct terminal lifecycle COMPLETED update",
        )
        for clause in required:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.skill_text)

    def test_orchestrator_routes_the_same_two_phase_persistence_sequence(self) -> None:
        required = (
            "dispatch dev-backlog-steward exactly once to record the nonterminal AWAITING_REVIEW lifecycle update",
            "reconcile that recorded update instead of dispatching a duplicate",
            "Do not request lifecycle COMPLETED while Commit is AWAITING_REVIEW",
            "dispatch dev-backlog-steward exactly once for the distinct terminal COMPLETED update",
        )
        for clause in required:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.role_text)

if __name__ == "__main__":
    unittest.main()
