# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Verifies Starting lifecycle and conditional watchdog behavior in coordination sources and generated adapters.

from pathlib import Path
import re
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = REPOSITORY_ROOT / "skills" / "codex-workitem-coordination" / "SKILL.md"
MANAGE_FILE_WORK_ITEMS_PATH = REPOSITORY_ROOT / "skills" / "manage-file-work-items" / "SKILL.md"
COORDINATOR_ROLE_PATH = (
    REPOSITORY_ROOT / "agents" / "roles" / "dev-activities" / "dev-backlog-coordinator.role.yaml"
)
ORCHESTRATOR_ROLE_PATH = (
    REPOSITORY_ROOT / "agents" / "roles" / "dev-activities" / "dev-orchestrator.role.yaml"
)
STEWARD_ROLE_PATH = (
    REPOSITORY_ROOT / "agents" / "roles" / "dev-activities" / "dev-backlog-steward.role.yaml"
)
_GENERATED_COORDINATOR_ADAPTERS = tuple(
    REPOSITORY_ROOT / "generated" / "adapters" / adapter / "agents" / filename
    for adapter, filename in (
        ("claude", "dev-backlog-coordinator.md"),
        ("codex", "dev-backlog-coordinator.toml"),
        ("gemini", "dev-backlog-coordinator.md"),
        ("junie", "dev-backlog-coordinator.md"),
    )
)


def _markdown_section(text: str, heading: str) -> str:
    marker = f"## {heading}"
    if marker not in text:
        raise AssertionError(f"missing coordination section: {marker}")
    return text.split(marker, 1)[1].split("\n## ", 1)[0]


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
            "assign one dedicated watchdog Task to an Agent",
            "schedule it to observe the fifteen-minute review checks",
            "never performs the parent review's scheduling or recovery adjustment",
            "observer, not a Work-item owner, queue entry, active-capacity slot, durable record, or substitute Coordinator",
            "must remain read-only",
            "does not mutate repository files or lifecycle state",
            "does not create a replacement ledger or duplicate watchdog",
        )
        for clause in required:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.watchdog_section)

        for retired_clause in (
            "one dedicated watchdog task",
            "watchdog Thread",
            "watchdog Role",
            "work-item owner, queue entry, Running slot",
        ):
            with self.subTest(retired_clause=retired_clause):
                self.assertNotIn(retired_clause, self.watchdog_section)

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

    def test_watchdog_never_infers_or_mutates_delivery_semantics(self) -> None:
        required = (
            "must not mutate backlog, claims, or task state",
            "must not infer integration readiness, accepted delivery, or completion readiness",
            "The parent retains every scheduling, lifecycle, ownership, recovery, dispatch, integration, and cleanup decision",
        )
        for clause in required:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.watchdog_section)

        for retired_contradiction in (
            "The watchdog infers integration readiness",
            "The watchdog decides accepted delivery",
            "The watchdog determines completion readiness",
            "The watchdog mutates backlog, claims, or task state",
            "The watchdog changes work-item lifecycle state",
        ):
            with self.subTest(retired_contradiction=retired_contradiction):
                self.assertNotIn(retired_contradiction, self.watchdog_section)

        semantic_verbs = re.compile(
            r"\b(?:infer(?:s|red)?|decid(?:e|es|ed)|determin(?:e|es|ed)|"
            r"mutat(?:e|es|ed)|chang(?:e|es|ed))\b",
            re.IGNORECASE,
        )
        for sentence in re.split(r"(?<=[.!?])\s+", self.watchdog_section):
            if semantic_verbs.search(sentence):
                with self.subTest(semantic_sentence=sentence):
                    self.assertRegex(sentence, r"(?i)\b(?:not|never|read-only)\b")

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


class StartingLifecycleContractTests(unittest.TestCase):
    """Protect the durable startup bridge and mechanical watchdog boundaries."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.coordination = SKILL_PATH.read_text(encoding="utf-8")
        cls.provider = MANAGE_FILE_WORK_ITEMS_PATH.read_text(encoding="utf-8")
        cls.roles = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                COORDINATOR_ROLE_PATH,
                ORCHESTRATOR_ROLE_PATH,
                STEWARD_ROLE_PATH,
            )
        )
        cls.contract = "\n".join((cls.coordination, cls.provider, cls.roles))
        cls.queue_section = _markdown_section(
            cls.coordination,
            "Queue Target And Dispatch",
        )
        cls.reconciliation_section = _markdown_section(
            cls.coordination,
            "Dispatch Reconciliation",
        )
        cls.ownership_section = _markdown_section(
            cls.coordination,
            "Starting And Work-Item Thread Ownership",
        )
        cls.blocked_handoff_section = _markdown_section(
            cls.provider,
            "Blocked Handoff And Resumption",
        )

    def test_starting_counts_against_capacity_and_prevents_duplicate_start(self) -> None:
        required = (
            "Ready -> Starting",
            "Starting counts against capacity",
            "canonical task id",
            "must not create a duplicate",
            "ambiguous startup",
        )
        for clause in required:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.contract)

        self.assertIn(
            "Count Work items whose file-backed Status is Starting or Running.",
            self.queue_section,
        )
        self.assertIn(
            "create at most one user-visible work-item Thread for the Starting Work item",
            self.queue_section,
        )
        self.assertIn(
            "Never retry Thread creation after an ambiguous response.",
            self.reconciliation_section,
        )

    def test_start_acceptance_and_recovery_preserve_ownership_evidence(self) -> None:
        required = (
            "Starting -> Running",
            "restore Ready",
            "Blocked or User Action Required",
            "branch, worktree, and claim evidence",
            "root Dev Orchestrator",
            "Dev Backlog Steward child",
        )
        for clause in required:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.contract)

        self.assertIn(
            "After the work-item Thread's root Dev Orchestrator Agent accepts ownership, it uses its Dev Backlog Steward child for the atomic Starting -> Running transition.",
            self.ownership_section,
        )

    def test_runtime_terms_remain_distinct(self) -> None:
        for clause in (
            "A Thread is one execution context or conversation.",
            "An Agent is a runtime instance operating under a Role",
            "A Task is a bounded assignment to an Agent; it is never a synonym for Thread.",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, self.ownership_section)

        for retired_contradiction in (
            "A Thread is a bounded assignment to an Agent.",
            "A Task is one execution context or conversation.",
            "A Role is a runtime instance",
            "An Agent is a reusable responsibility and authority contract",
        ):
            with self.subTest(retired_contradiction=retired_contradiction):
                self.assertNotIn(retired_contradiction, self.ownership_section)

    def test_retired_capacity_and_startup_shortcuts_stay_absent(self) -> None:
        for retired_contradiction in (
            "Count Work items whose file-backed Status is Running.",
            "When an item leaves Running, fill the active-capacity vacancy",
            "recount Running capacity",
            "ten are Running",
        ):
            with self.subTest(retired_contradiction=retired_contradiction):
                self.assertNotIn(retired_contradiction, self.queue_section)

        lifecycle_sections = "\n".join(
            (self.queue_section, self.ownership_section, self.blocked_handoff_section)
        )
        for retired_contradiction in (
            "Ready -> Running",
            "Blocked -> Running",
            "Blocked/Ready -> Running",
            "Blocked or Ready -> Running",
        ):
            with self.subTest(retired_contradiction=retired_contradiction):
                self.assertNotIn(retired_contradiction, lifecycle_sections)

        for retired_contradiction in (
            "Retry Thread creation after an ambiguous response.",
            "Retry Task creation after ambiguous startup.",
            "Create another Thread after ambiguous startup.",
        ):
            with self.subTest(retired_contradiction=retired_contradiction):
                self.assertNotIn(retired_contradiction, self.reconciliation_section)

    def test_watchdog_reports_mechanical_task_and_coordination_mismatches(self) -> None:
        required = (
            "stopped, failed, or missing canonical task",
            "Starting or Running",
            "stopped task that retains a live coordination entry",
            "terminal item that retains a live coordination entry",
            "no extra grace timeout",
        )
        for clause in required:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.coordination)

    def test_watchdog_keeps_quiet_active_tasks_healthy_and_never_decides_delivery(self) -> None:
        required = (
            "active quiet tasks",
            "explicit deadline or hard stop",
            "must not infer integration readiness",
            "accepted delivery",
            "completion readiness",
            "must not mutate backlog, claims, or task state",
        )
        for clause in required:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.coordination)


if __name__ == "__main__":
    unittest.main()
