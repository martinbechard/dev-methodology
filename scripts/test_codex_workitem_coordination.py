# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Verifies conditional coordination behavior in the watchdog and generated coordinator adapters.

from pathlib import Path
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = REPOSITORY_ROOT / "skills" / "codex-workitem-coordination" / "SKILL.md"
_GENERATED_COORDINATOR_ADAPTERS = tuple(
    REPOSITORY_ROOT / "generated" / "adapters" / adapter / "agents" / filename
    for adapter, filename in (
        ("claude", "dev-backlog-coordinator.md"),
        ("codex", "dev-backlog-coordinator.toml"),
        ("gemini", "dev-backlog-coordinator.md"),
        ("junie", "dev-backlog-coordinator.md"),
    )
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

    def test_watchdog_omits_coordination_registry_work_under_none(self) -> None:
        """Branch registry reads, ownership evaluation, and alerts inside the watchdog body."""

        self.assertNotIn(
            "reads current work items, Git state, coordination-registry state, and task state",
            self.watchdog_section,
        )
        for clause in (
            "When resource coordination selects agent-claim, it also reads coordination-registry state and evaluates shared-resource ownership.",
            "When resource coordination selects none, it omits coordination-registry reads, shared-resource ownership evaluation, and coordination alerts or evidence.",
            "when resource coordination selects agent-claim, stale, unsafe, or unnecessarily broad shared-resource ownership",
            "unsafe coordination state when resource coordination selects agent-claim",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, self.watchdog_section)

    def test_registry_cleanup_and_generated_coordinators_remain_conditional(self) -> None:
        """Keep registry cleanup out of none and preserve conditional adapter wording."""

        self.assertIn(
            "When resource coordination selects agent-claim, keep administrative coordination-registry cleanup",
            self.skill_text,
        )
        self.assertIn(
            "When none is selected, omit coordination-registry cleanup and coordination evidence.",
            self.skill_text,
        )
        for adapter_path in _GENERATED_COORDINATOR_ADAPTERS:
            adapter = adapter_path.read_text(encoding="utf-8")
            with self.subTest(adapter=adapter_path.parent.parent.name):
                self.assertIn("enabled resource coordination", adapter)
                self.assertIn("when coordination is enabled", adapter)
                self.assertNotIn(
                    "reads current work items, Git state, coordination-registry state, and task state",
                    adapter,
                )


if __name__ == "__main__":
    unittest.main()
