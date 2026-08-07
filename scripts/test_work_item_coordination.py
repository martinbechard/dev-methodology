# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Verifies provider-neutral queue, lifecycle, authority, delivery, and watchdog coordination.
# Governing design: design/orchestrated-development-lifecycle.html

from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / "skills" / "coordinate-work-items" / "SKILL.md"
CODEX_SKILL_PATH = ROOT / "skills" / "coordinate-codex-tasks" / "SKILL.md"
RETIRED_SKILL_NAME = "coordinate-" + "codex-work-items"
RETIRED_SKILL_PATH = ROOT / "skills" / RETIRED_SKILL_NAME / "SKILL.md"
MANAGE_FILE_PATH = ROOT / "skills" / "manage-work-items-file" / "SKILL.md"
ROLE_PATHS = {
    name: ROOT / "agents" / "roles" / "dev-activities" / f"{name}.role.yaml"
    for name in (
        "dev-backlog-coordinator",
        "dev-backlog-steward",
        "dev-backlog-watchdog",
        "dev-orchestrator",
    )
}


def _section(text: str, heading: str) -> str:
    """Return the level-two Markdown section with the given heading."""

    marker = f"## {heading}"
    if marker not in text:
        raise AssertionError(f"missing section: {marker}")
    return text.split(marker, 1)[1].split("\n## ", 1)[0]


def _selected_skills(role: dict[str, object]) -> dict[str, dict[str, str]]:
    """Return a role's skill entries by skill identifier."""

    return {
        next(iter(entry)): entry[next(iter(entry))]
        for entry in role["skills"]  # type: ignore[index]
    }


class WorkItemCoordinationPackageTests(unittest.TestCase):
    """Keep the portable package complete and separate from Codex task mechanics."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.portable = SKILL_PATH.read_text(encoding="utf-8")
        cls.codex = CODEX_SKILL_PATH.read_text(encoding="utf-8")

    def test_peer_packages_replace_retired_identity(self) -> None:
        self.assertFalse(RETIRED_SKILL_PATH.exists())
        self.assertIn("name: coordinate-work-items", self.portable)
        self.assertIn("name: coordinate-codex-tasks", self.codex)
        self.assertNotIn(RETIRED_SKILL_NAME, self.portable)
        self.assertNotIn(RETIRED_SKILL_NAME, self.codex)

    def test_portable_skill_owns_complete_work_item_policy(self) -> None:
        for heading in (
            "Authority And Roles",
            "Governed Definition Work-Item Authorization",
            "Active Execution And Capacity",
            "Resource Coordination",
            "Work-Item Execution Record",
            "Queue Target And Scheduling",
            "Effective Commit Delivery And Persistence Closure",
            "Verification",
            "Long-Running Execution Control",
            "Blocker Classification",
            "Stalled Investigation And Blocker Handoff",
            "Blocked Reconciliation And Disposition",
            "Parent Review",
            "Dedicated Read-Only Watchdog",
            "User Decisions And Terminal State",
            "Reporting",
        ):
            with self.subTest(heading=heading):
                self.assertIn(f"## {heading}", self.portable)

    def test_portable_skill_excludes_codex_task_mechanics(self) -> None:
        forbidden = (
            "Codex",
            "conversation title",
            "conversation-title",
            "spawn_agent",
            "followup_task",
            "archive the task",
            "archived tasks",
            "task creation",
            "task-creation",
        )
        for phrase in forbidden:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase.lower(), self.portable.lower())

    def test_portable_skill_keeps_provider_and_delivery_authority_external(self) -> None:
        normalized = " ".join(self.portable.split())
        for clause in (
            "effective Persistence-selected provider record is the durable work-item authority",
            "Git records branches, commits, delivery, and cleanup eligibility; it is not a work-item provider",
            "When resource-claim is loaded, use its Claim Events table and supporting rules",
            "effective Commit-selected skill",
            "effective Persistence-selected management skill",
            "Do not create a separate parent ledger",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, normalized)

    def test_starting_and_running_use_portable_execution_evidence(self) -> None:
        normalized = " ".join(self.portable.split())
        for clause in (
            "Starting is the durable handoff",
            "Canonical Execution: [runtime execution identity or None]",
            "Active Execution Evidence",
            "Condition Type: [root-execution, delegated-work, owned-wait, or progress-condition]",
            "Deadline or Expires At: [finite UTC timestamp]",
            "Next Reconciliation At: [UTC timestamp]",
            "both future boundaries must remain later than the current time",
            "Count no more than ten actively eligible work items",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, normalized)

    def test_queue_constraints_remain_event_scoped(self) -> None:
        queue = " ".join(_section(self.portable, "Queue Target And Scheduling").split())
        for clause in (
            "An unmet hard prerequisite makes the item dispatch-ineligible.",
            "A coordination-only overlap note does not block a safe private-worktree start.",
            "Defer only that event",
            "Future Ideas are not work-item states",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, queue)

    def test_definition_authorization_uses_exact_work_item_provenance(self) -> None:
        authorization = " ".join(
            _section(self.portable, "Governed Definition Work-Item Authorization").split()
        )
        for clause in (
            "explicit user-authorized work item",
            "Do not ask for a second approval",
            "auditable provenance record",
            "supported per-path pre-mutation check",
            "ALLOWED_APPROVED_DEFINITION_CHANGE",
            "outside the work item's exact named scope is additional work",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, authorization)

    def test_watchdog_policy_is_read_only_and_provider_neutral(self) -> None:
        watchdog = " ".join(
            _section(self.portable, "Dedicated Read-Only Watchdog").split()
        )
        for clause in (
            "never performs scheduling or recovery",
            "outside the provider queue and active capacity",
            "must not change repository files, provider records, lifecycle state, claims",
            "Notify the coordinator only when action is required",
            "one concise no-action cycle result",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, watchdog)
        self.assertNotIn("Codex", watchdog)
        self.assertNotIn("conversation", watchdog.lower())

    def test_portable_skill_does_not_absorb_codex_peer(self) -> None:
        self.assertNotIn("coordinate-codex-tasks", self.portable)
        portable_headings = set(re.findall(r"^## (.+)$", self.portable, re.MULTILINE))
        codex_headings = set(re.findall(r"^## (.+)$", self.codex, re.MULTILINE))
        self.assertEqual(set(), portable_headings & codex_headings)


class WorkItemCoordinationRoleRoutingTests(unittest.TestCase):
    """Keep portable coordination core or conditional according to each role."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.roles = {
            name: yaml.safe_load(path.read_text(encoding="utf-8"))
            for name, path in ROLE_PATHS.items()
        }

    def test_watchdog_has_portable_core_dependency(self) -> None:
        selected = _selected_skills(self.roles["dev-backlog-watchdog"])
        self.assertNotIn("condition", selected["coordinate-work-items"])

    def test_other_roles_select_portable_policy_conditionally(self) -> None:
        for name in (
            "dev-backlog-coordinator",
            "dev-backlog-steward",
            "dev-orchestrator",
        ):
            selected = _selected_skills(self.roles[name])
            with self.subTest(role=name):
                self.assertIn("condition", selected["coordinate-work-items"])
                self.assertNotIn("Codex", selected["coordinate-work-items"]["condition"])

    def test_roles_reference_portable_sections_without_copying_policy(self) -> None:
        section = "Governed Definition Work-Item Authorization"
        normative_markers = (
            "Starting Recorded At:",
            "Condition Type:",
            "Count no more than ten actively eligible work items",
            "ALLOWED_APPROVED_DEFINITION_CHANGE",
        )
        for name, role in self.roles.items():
            role_text = json.dumps(role, sort_keys=True)
            with self.subTest(role=name):
                self.assertIn("coordinate-work-items", _selected_skills(role))
                self.assertIn(section, role_text)
                for marker in normative_markers:
                    self.assertNotIn(marker, role_text)

    def test_existing_provider_delivery_and_helper_names_remain_supported(self) -> None:
        for path in (
            ROOT / "skills" / "create-work-item-file" / "SKILL.md",
            ROOT / "skills" / "manage-work-items-file" / "SKILL.md",
            ROOT / "skills" / "deliver-work-item-main-branch" / "SKILL.md",
            ROOT / "skills" / "resource-claim" / "SKILL.md",
            ROOT / "skills" / "resource-claim-helper-command" / "SKILL.md",
        ):
            with self.subTest(path=path):
                self.assertTrue(path.is_file())

    def test_file_provider_does_not_absorb_runtime_policy(self) -> None:
        provider = " ".join(MANAGE_FILE_PATH.read_text(encoding="utf-8").split())
        self.assertIn(
            "records only caller-authorized file-provider mutations and their evidence",
            provider,
        )
        self.assertIn(
            "does not determine active-execution eligibility, calculate capacity, inspect runtime or conversation state, or synchronize conversation titles",
            provider,
        )


if __name__ == "__main__":
    unittest.main()
