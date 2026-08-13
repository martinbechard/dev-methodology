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
CANONICAL_WORK_ITEM_AUTHORITY = (
    "The Work-item content is the Work-item authority and is stored according to the "
    "Persistence provider's specific format."
)
EXPLICIT_CURRENT_TERMINOLOGY_PATHS = (
    Path(".agents/skills/backlog-dispatcher/SKILL.md"),
    Path("README.md"),
    Path("skills/commit-file-provider-transaction/SKILL.md"),
    Path("skills/coordinate-work-items/SKILL.md"),
    Path("skills/coordinate-codex-tasks/SKILL.md"),
    Path("skills/resource-claim/SKILL.md"),
    Path("skills/manage-complex-development-plan/SKILL.md"),
    Path("skills/deliver-work-item-main-branch/SKILL.md"),
    Path("skills/set-multitask-mode/SKILL.md"),
    Path("skills/set-solo-mode/SKILL.md"),
    Path("agents/roles/dev-activities/dev-backlog-coordinator.role.yaml"),
    Path("agents/roles/dev-activities/dev-backlog-steward.role.yaml"),
    Path("agents/roles/dev-activities/dev-backlog-watchdog.role.yaml"),
    Path("agents/roles/dev-activities/dev-orchestrator.role.yaml"),
    Path("design/agents/backlog-management.md"),
    Path("design/work-item-provider-and-completion-contracts.md"),
    Path("design/orchestrated-development-lifecycle.html"),
    Path("design/documentation-templates.html"),
    Path("design/agents/work-item-dispatching-and-delivery.md"),
    Path("design/agents/review-and-verification.md"),
    Path("design/agentic-configuration.html"),
    Path("evals/agent-scenarios.yaml"),
    Path("evals/judges.yaml"),
    Path("evals/agent-tests/dev-backlog-coordinator/scenarios.yaml"),
    Path("evals/agent-tests/dev-backlog-coordinator/fixtures/cases.yaml"),
    Path(
        "evals/agent-tests/dev-backlog-coordinator/skills/"
        "dev-backlog-coordinator-suite-contract/SKILL.md"
    ),
    Path("evals/agent-tests/dev-backlog-watchdog/scenarios.yaml"),
    Path("evals/agent-tests/dev-backlog-watchdog/watchdog_simulator.py"),
    Path(
        "evals/agent-tests/dev-backlog-watchdog/skills/"
        "dev-backlog-watchdog-suite-contract/SKILL.md"
    ),
    Path("design/generated/skill-definitions.js"),
    Path("design/generated/role-definitions.js"),
    Path("design/agent-and-skill-evaluations.html"),
)
DERIVED_CURRENT_TERMINOLOGY_PATHS = tuple(
    sorted(
        {
            path.relative_to(ROOT)
            for pattern in (
                "create-work-item*/SKILL.md",
                "manage-work-items*/SKILL.md",
                "deliver-work-item*/SKILL.md",
            )
            for skill_path in (ROOT / "skills").glob(pattern)
            for path in (skill_path, skill_path.parent / "agents" / "openai.yaml")
            if path.is_file()
        }
    )
)
CURRENT_TERMINOLOGY_PATHS = tuple(
    dict.fromkeys(
        (*EXPLICIT_CURRENT_TERMINOLOGY_PATHS, *DERIVED_CURRENT_TERMINOLOGY_PATHS)
    )
)
GENERIC_PROVIDER_RECORD_PATTERN = re.compile(
    r"(?<!file-)\bprovider records?\b", re.IGNORECASE
)
PROVIDER_AUTHORITY_PATTERNS = (
    re.compile(r"\bprovider lifecycle (?:is )?authoritative\b", re.IGNORECASE),
    re.compile(r"\bprovider records? as lifecycle authority\b", re.IGNORECASE),
    re.compile(r"\bprovider remains (?:the durable )?lifecycle authority\b", re.IGNORECASE),
)
PROVIDER_NATIVE_OBJECT_AUTHORITY_PATTERNS = (
    re.compile(
        r"\bauthoritative\s+(?:GitHub|GitLab|Azure DevOps|Jira)\s+"
        r"(?:issues?|work items?|records?)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:GitHub|GitLab|Azure DevOps|Jira)\s+"
        r"(?:issues?|work items?|records?)\s+"
        r"(?:(?:is|are|remain|remains|stay|stays)\s+(?:the\s+)?)?"
        r"(?:authority|authoritative)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\b(?:sole\s+)?issue(?: object)? authority\b", re.IGNORECASE),
)
PROVIDER_NATIVE_CONTENT_SENTENCES = {
    Path("skills/create-work-item-github/SKILL.md"): (
        "GitHub issues store authoritative Work-item content."
    ),
    Path("skills/manage-work-items-github/SKILL.md"): (
        "GitHub issues store authoritative Work-item content."
    ),
    Path("skills/create-work-item-gitlab/SKILL.md"): (
        "GitLab issues store authoritative Work-item content."
    ),
    Path("skills/manage-work-items-gitlab/SKILL.md"): (
        "GitLab issues store authoritative Work-item content."
    ),
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
            CANONICAL_WORK_ITEM_AUTHORITY,
            "Git records branches, commits, delivery, and cleanup eligibility; it is not a work-item provider",
            "When resource-claim is loaded, use its Claim Events table and supporting rules",
            "effective Commit-selected skill",
            "effective Persistence-selected management skill",
            "Do not create a separate parent ledger",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, normalized)

    def test_current_methodology_uses_work_item_content_authority(self) -> None:
        """Reject object authority across derived maintained current surfaces."""

        self.assertIn(CANONICAL_WORK_ITEM_AUTHORITY, self.portable)
        file_provider_transaction = (
            ROOT / "skills" / "commit-file-provider-transaction" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("canonical file-provider record", file_provider_transaction)
        self.assertIsNone(GENERIC_PROVIDER_RECORD_PATTERN.search(file_provider_transaction))
        for invalid_phrase in (
            "Create one authoritative GitHub issue.",
            "GitLab issues are authoritative.",
            "Preserve GitHub issue authority.",
            "Use provider reads as the sole issue authority.",
        ):
            with self.subTest(invalid_provider_object_authority=invalid_phrase):
                self.assertTrue(
                    any(
                        pattern.search(invalid_phrase)
                        for pattern in PROVIDER_NATIVE_OBJECT_AUTHORITY_PATTERNS
                    )
                )
        for qualified_phrase in PROVIDER_NATIVE_CONTENT_SENTENCES.values():
            with self.subTest(qualified_provider_content=qualified_phrase):
                self.assertFalse(
                    any(
                        pattern.search(qualified_phrase)
                        for pattern in PROVIDER_NATIVE_OBJECT_AUTHORITY_PATTERNS
                    )
                )
        for path, sentence in PROVIDER_NATIVE_CONTENT_SENTENCES.items():
            with self.subTest(provider_content_path=path):
                self.assertIn(sentence, (ROOT / path).read_text(encoding="utf-8"))

        errors: list[str] = []
        paths = list(CURRENT_TERMINOLOGY_PATHS)
        paths.extend(
            path.relative_to(ROOT)
            for path in (ROOT / "generated" / "adapters").glob("*/agents/*")
            if path.is_file()
        )
        for path in paths:
            text = (ROOT / path).read_text(encoding="utf-8")
            for match in GENERIC_PROVIDER_RECORD_PATTERN.finditer(text):
                errors.append(f"{path}: generic {match.group(0)!r}")
                break
            for pattern in PROVIDER_AUTHORITY_PATTERNS:
                if match := pattern.search(text):
                    errors.append(f"{path}: provider authority {match.group(0)!r}")
                    break
            for pattern in PROVIDER_NATIVE_OBJECT_AUTHORITY_PATTERNS:
                if match := pattern.search(text):
                    errors.append(f"{path}: provider-native object authority {match.group(0)!r}")
                    break
        self.assertEqual([], errors, "\n".join(errors))

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

    def test_ordered_series_dependency_effective_state_contract(self) -> None:
        """Ordered lanes, not incidental index links, define predecessor gating."""

        policy = " ".join(
            _section(self.portable, "Ordered Series Dependency State").split()
        )
        for clause in (
            "one series folder",
            "required predecessor sets or ordered lanes",
            "index.md",
            "preceding members in that child's lane",
            "lists its members in causal-priority order",
            "breaks reporting ties only",
            "does not serialize otherwise independent predecessors",
            "Only the predecessors named for that child gate it.",
            "An earlier Markdown link, list entry, or child outside that lane is not a predecessor",
            "Never use ordinary Markdown order or global list order",
            "Stored Status remains the canonical lifecycle",
            "derive effective Holding",
            "first required predecessor in the child's causal-priority order whose stored Status is Blocked",
            "causal Work Item ID",
            "must not rewrite the downstream child's record",
            "Recalculate effective state",
            "every required predecessor has a terminal-successful disposition",
            "the child's own stored lifecycle is dispatchable",
            "Reject a new active cross-folder Work Item dependency edge",
            "same-series migration before dispatch",
            "archived terminal-successful predecessor",
            "stable Work Item identity and canonical index link",
            "External prerequisites are conditions, not Work Item dependency edges",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, policy)

    def test_dependency_counts_reporting_and_contradictions_are_normative(self) -> None:
        """Coordination owns counts, normalized reports, and contradiction criteria."""

        policy = " ".join(
            _section(self.portable, "Ordered Series Dependency State").split()
        )
        for clause in (
            "Count each stored Blocked Work Item exactly once",
            "never increment stored Blocked counts or shared-cause totals",
            "affected child Work Item ID, stored Status, effective state, and causal Work Item ID",
            "missing, duplicate, self-referential, unresolved, or prohibited cross-folder predecessor",
            "multiple predecessors without an explicit causal-priority order",
            "effective state differs from this algorithm",
            "effective Blocked lacks a causal Work Item ID",
            "not a required stored-Blocked predecessor",
            "not first by the child's declared causal priority",
            "causal Work Item ID appears on a non-derived result",
            "copied derived Holding or Blocked into stored lifecycle",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, policy)

    def test_definition_authorization_uses_exact_work_item_provenance(self) -> None:
        authorization = " ".join(
            _section(self.portable, "Governed Definition Work-Item Authorization").split()
        )
        for clause in (
            "explicit user-authorized work item",
            "Do not ask for a second approval",
            "auditable approval provenance",
            "exact approved manifest and provenance are the mutation authority",
            "do not require a separate executable approval checker",
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
            "must not change repository files, Work-item content, lifecycle state, claims",
            "Notify the Coordinator only when a specific decision is required",
            "When no decision is required, send nothing",
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
            "exact approved manifest and provenance are the mutation authority",
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
