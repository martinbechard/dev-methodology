# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies the Codex task mapping without duplicating portable work-item policy.
# Governing design: design/orchestrated-development-lifecycle.html

from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
RETIRED_SKILL_NAME = "coordinate-" + "codex-work-items"
CODEX_SKILL_PATH = ROOT / "skills" / "coordinate-codex-tasks" / "SKILL.md"
PORTABLE_SKILL_PATH = ROOT / "skills" / "coordinate-work-items" / "SKILL.md"
ROLE_PATHS = {
    name: ROOT / "agents" / "roles" / "dev-activities" / f"{name}.role.yaml"
    for name in (
        "dev-backlog-coordinator",
        "dev-backlog-steward",
        "dev-backlog-watchdog",
        "dev-orchestrator",
    )
}

CANONICAL_STANDING_PROMPT = """Act as the dedicated read-only Dev Methodology backlog watchdog for parent task {parent_task_id} in {repository_root}.

Apply skills/coordinate-work-items/SKILL.md for portable capacity, lifecycle reconciliation, Blocked, Stalled, and read-only Watchdog criteria. Apply skills/coordinate-codex-tasks/SKILL.md only for Codex task identity, conversation-title observation, bounded resumption, and archival mapping. Observe task state through runtime tools. Consult provider, Git, and resource records only for a lifecycle decision, anomaly, dependency, delivery, or cleanup question; do not reconstruct lifecycle history on every cycle.

Remain strictly read-only. Do not mutate repository files, provider lifecycle, claims, tasks, branches, worktrees, or shared resources. Do not dispatch, integrate, clean up, archive, or run expensive or live verification. Notify parent task {parent_task_id} only when a specific Coordinator decision is required. State the affected item, decision, and smallest recommended action without copying durable evidence into the message. When healthy, send nothing."""


def _selected_skills(role: dict[str, object]) -> dict[str, dict[str, str]]:
    """Return a role's skill entries by skill identifier."""

    return {
        next(iter(entry)): entry[next(iter(entry))]
        for entry in role["skills"]  # type: ignore[index]
    }


def _prompt_template(text: str, heading: str) -> str:
    """Return the exact text fenced below one canonical prompt heading."""

    match = re.search(
        rf"^### {re.escape(heading)}\n\n```text\n(.*?)\n```$",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise AssertionError(f"missing canonical prompt template: {heading}")
    return match.group(1)


class CodexTaskControlPackageTests(unittest.TestCase):
    """Keep Codex task creation, identity, reconciliation, and cleanup in one peer."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.codex = CODEX_SKILL_PATH.read_text(encoding="utf-8")
        cls.portable = PORTABLE_SKILL_PATH.read_text(encoding="utf-8")
        cls.normalized = " ".join(cls.codex.split())

    def test_codex_skill_owns_only_runtime_mapping_sections(self) -> None:
        for heading in (
            "Codex Capability Check",
            "Codex Task Creation And Resumption",
            "Canonical Codex Task Identity",
            "Conversation Title Contract",
            "Codex Runtime Reconciliation",
            "Task Follow-Up",
            "Watchdog Task Mapping",
            "Task Archival",
        ):
            with self.subTest(heading=heading):
                self.assertIn(f"## {heading}", self.codex)

    def test_codex_skill_excludes_portable_policy_ownership(self) -> None:
        forbidden_headings = (
            "Authority And Roles",
            "Active Execution And Capacity",
            "Resource Coordination",
            "Queue Target And Scheduling",
            "Effective Commit Delivery And Persistence Closure",
            "Blocker Classification",
            "Reporting",
        )
        for heading in forbidden_headings:
            with self.subTest(heading=heading):
                self.assertNotIn(f"## {heading}", self.codex)
        for phrase in (
            "Persistence-selected management skill",
            "Commit-selected skill",
            "Claim Events table",
            "Count no more than ten",
            "ALLOWED_APPROVED_DEFINITION_CHANGE",
        ):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, self.codex)

    def test_codex_skill_declares_portable_peer_without_absorbing_it(self) -> None:
        self.assertIn(
            "Apply coordinate-work-items together with this skill",
            self.normalized,
        )
        self.assertIn(
            "does not create provider lifecycle authority, delivery authority, or resource ownership",
            self.normalized,
        )
        self.assertNotIn("coordinate-codex-tasks", self.portable)

    def test_task_creation_and_ambiguous_results_are_reconciled(self) -> None:
        normalized_lower = self.normalized.lower()
        for clause in (
            "create at most one root Dev Orchestrator task",
            "after coordinate-work-items records the Starting reservation",
            "Do not retry task creation after an error, timeout, disconnect, or ambiguous response",
            "Reconcile active and archived Codex tasks",
            "adopt it as the canonical task",
            "stop every duplicate before mutation",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause.lower(), normalized_lower)

    def test_visible_work_item_tasks_do_not_inherit_parent_conversation(self) -> None:
        for clause in (
            "Collaboration subagent launches follow the Codex Harness Collaboration Subagent Launch Contract",
            "A separate user-visible Codex work-item task is not a collaboration subagent launch",
            "explicit provider and canonical-task handoffs",
            "self-contained dispatch prompt",
            "no implicit parent-conversation inheritance",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, self.normalized)

    def test_canonical_identity_preserves_task_and_conversation_distinction(self) -> None:
        normalized_lower = self.normalized.lower()
        for clause in (
            "A Codex task is the canonical runtime execution identity",
            "A conversation is the retained user-visible context",
            "task identifier and conversation identifier are distinct",
            "Do not infer either identity from the conversation title",
            "preserve the same canonical task and conversation",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause.lower(), normalized_lower)

    def test_title_contract_maps_every_lifecycle_state(self) -> None:
        for lifecycle in (
            "Ready",
            "Starting",
            "Running",
            "User Action Required",
            "Stalled",
            "Blocked",
            "Holding",
            "Awaiting Review",
            "Completed",
            "Failed",
            "Abandoned",
        ):
            with self.subTest(lifecycle=lifecycle):
                self.assertRegex(self.normalized, rf"{re.escape(lifecycle)}[^.;]*—")
        self.assertIn("conversation title is display state", self.normalized)
        self.assertIn("after every successful lifecycle transition", self.normalized)

    def test_follow_up_resumes_the_same_task(self) -> None:
        normalized_lower = self.normalized.lower()
        for clause in (
            "send one follow-up only to resume an authorized bounded next action or deliver a Coordinator decision",
            "Never use follow-up for routine status, heartbeat, lifecycle history, capacity evidence, provider mutation, or proof of progress",
            "do not create a replacement task merely because the task is idle",
            "preserve the original task identity and reconcile the returned runtime state",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause.lower(), normalized_lower)

    def test_archival_waits_for_portable_terminal_closeout(self) -> None:
        for clause in (
            "Task archival is mandatory by default after the applicable ordinary terminal gates pass",
            "terminal provider or task-local disposition",
            "safe branch and worktree disposition",
            "no unresolved notification",
            "An idle, stopped, titled, or archived Codex task proves none of those facts",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, self.normalized)

    def test_watchdog_prompt_is_canonical_without_heartbeat_messages(self) -> None:
        standing = _prompt_template(self.codex, "Canonical Standing Prompt Template")

        self.assertEqual(CANONICAL_STANDING_PROMPT, standing)
        self.assertEqual(
            CANONICAL_STANDING_PROMPT.replace("{parent_task_id}", "parent-17").replace(
                "{repository_root}", "/workspace/project"
            ),
            standing.replace("{parent_task_id}", "parent-17").replace(
                "{repository_root}", "/workspace/project"
            ),
        )
        self.assertNotIn("Canonical Heartbeat Prompt Template", self.codex)
        self.assertIn("Do not send scheduled heartbeat or progress follow-ups", self.codex)

    def test_portable_skill_contains_no_codex_only_vocabulary(self) -> None:
        for phrase in (
            "Codex",
            "conversation title",
            "task creation",
            "task archival",
            "follow-up to the same canonical task",
        ):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase.lower(), self.portable.lower())


class CodexTaskControlRoleRoutingTests(unittest.TestCase):
    """Keep the Codex peer conditional in all conceptual backlog roles."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.roles = {
            name: yaml.safe_load(path.read_text(encoding="utf-8"))
            for name, path in ROLE_PATHS.items()
        }

    def test_every_codex_dependency_is_explicitly_conditional(self) -> None:
        for name, role in self.roles.items():
            selected = _selected_skills(role)
            codex = selected["coordinate-codex-tasks"]
            with self.subTest(role=name):
                self.assertIn("condition", codex)
                self.assertRegex(codex["condition"], re.compile(r"Codex", re.IGNORECASE))

    def test_non_codex_routing_uses_portable_peer_only(self) -> None:
        for name, role in self.roles.items():
            selected = _selected_skills(role)
            portable = selected["coordinate-work-items"]
            codex = selected["coordinate-codex-tasks"]
            with self.subTest(role=name):
                self.assertNotIn("Codex", portable.get("condition", ""))
                self.assertIn("Codex", codex["condition"])

    def test_roles_reference_both_peers_without_redefining_sections(self) -> None:
        normative = (
            "create at most one root Dev Orchestrator task",
            "A Codex task is the canonical runtime execution identity",
            "Ready: Ready —",
            "send one follow-up to the same canonical task",
            "Archive a terminal Codex task only after",
        )
        for name, role in self.roles.items():
            selected = _selected_skills(role)
            role_text = json.dumps(role, sort_keys=True)
            with self.subTest(role=name):
                self.assertIn("coordinate-work-items", selected)
                self.assertIn("coordinate-codex-tasks", selected)
                for clause in normative:
                    self.assertNotIn(clause, role_text)

    def test_codex_generated_agents_keep_both_dependencies(self) -> None:
        for name in ROLE_PATHS:
            adapter = ROOT / "generated" / "adapters" / "codex" / "agents" / f"{name}.toml"
            text = adapter.read_text(encoding="utf-8")
            with self.subTest(role=name):
                self.assertIn("coordinate-work-items", text)
                self.assertIn("coordinate-codex-tasks", text)

    def test_non_codex_generated_agents_do_not_name_portable_policy_as_codex(self) -> None:
        stale_or_unguarded_contracts = (
            "Active Execution, Capacity, And Conversation Titles",
            "central-contract conversation-title handoff",
            "canonical conversation and root Agent Task reconciliation",
            "require Dev the root Dev Orchestrator's verified terminal conversation-title coordination",
        )
        required_guards = (
            "When coordinate-codex-tasks is active",
            "For other runtimes",
        )
        codex_behavior = re.compile(
            r"Codex task|conversation[- ]title|Conversation Title|follow-up|task archival",
            re.IGNORECASE,
        )
        explicit_guard = re.compile(
            r"when .*Codex|when coordinate-codex-tasks is active|for other runtimes",
            re.IGNORECASE,
        )
        for runtime in ("claude", "gemini", "junie"):
            for name in ROLE_PATHS:
                adapter = ROOT / "generated" / "adapters" / runtime / "agents" / f"{name}.md"
                text = adapter.read_text(encoding="utf-8")
                with self.subTest(runtime=runtime, role=name):
                    self.assertIn("coordinate-work-items", text)
                    self.assertNotIn(RETIRED_SKILL_NAME, text)
                    for phrase in stale_or_unguarded_contracts:
                        self.assertNotIn(phrase, text)
                    self.assertTrue(
                        any(guard in text for guard in required_guards),
                        f"{adapter} lacks an explicit non-Codex runtime guard",
                    )
                    role_body = text.split("## Boundaries", 1)[1].split(
                        "These definition-owned skills", 1
                    )[0]
                    for line in role_body.splitlines():
                        if codex_behavior.search(line):
                            self.assertRegex(
                                line,
                                explicit_guard,
                                f"unguarded Codex behavior in {adapter}: {line}",
                            )


if __name__ == "__main__":
    unittest.main()
