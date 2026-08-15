# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies the Codex task mapping without duplicating portable work-item policy.
# Governing design: design/orchestrated-development-lifecycle.html

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, replace
import json
from pathlib import Path
import re
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
RETIRED_SKILL_NAME = "coordinate-" + "codex-work-items"
CODEX_SKILL_PATH = ROOT / "skills" / "coordinate-codex-tasks" / "SKILL.md"
DISPATCHER_SKILL_PATH = (
    ROOT / ".agents" / "skills" / "backlog-dispatcher" / "SKILL.md"
)
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

CANONICAL_STANDING_PROMPT = """Act as the dedicated read-only Dev Methodology backlog watchdog created by runtime parent task {runtime_parent_task_id} for Dev Backlog Coordinator task {coordinator_task_id} in {repository_root}.

Apply skills/coordinate-work-items/SKILL.md for portable capacity, lifecycle reconciliation, Blocked, Stalled, and read-only Watchdog criteria. Apply skills/coordinate-codex-tasks/SKILL.md only for Codex task identity, conversation-title observation, bounded resumption, and archival mapping. Observe task state through runtime tools. On every cycle, obtain the current Blocked inventory, compare every observed canonical Codex task title with the exact title derived from current Work-item lifecycle and material Running phase, and compare each observed bounded verifier title with its current runtime outcome. Consult provider, Git, and resource records only for those reconciliations or another lifecycle decision, anomaly, dependency, delivery, or cleanup question; do not reconstruct lifecycle history on every cycle.

Remain strictly read-only. Do not mutate repository files, Work-item lifecycle, claims, tasks, branches, worktrees, or shared resources. Do not dispatch, integrate, clean up, archive, or run expensive or live verification. Notify Coordinator task {coordinator_task_id} only when a specific Coordinator decision is required. State the affected item, decision, and smallest recommended action without copying durable evidence into the message. When healthy, send nothing."""

REFERENCE_PLUS_DELTA_LAUNCH_PROMPT = """Launch one Dev Orchestrator subagent to execute Work Item <opaque Work Item ID>.
As the root task, you provide the Codex title and messaging the subagents may need.
Authoritative provider: <provider locator>
Dispatch-time delta: <launch-only facts absent from the provider, or none>"""

ORDINARY_WORKER_IDENTITY = {
    "task_id": "task-visible-worker-123",
    "conversation_id": "conversation-visible-worker-456",
}
COMBINED_RUNTIME_IDENTITY = {
    "task_id": "combined-visible-worker-789",
    "conversation_id": "combined-visible-worker-789",
}

_TITLE_UPDATED = "TITLE_UPDATED"
_COORDINATOR_DECISION_REQUIRED = "COORDINATOR_DECISION_REQUIRED"
_POST_CALL_IDENTITY_MISMATCH = "POST_CALL_IDENTITY_MISMATCH"
_PROVIDER_RECORDED_TARGET = "provider-recorded worker identity"


@dataclass(frozen=True)
class _ProviderIdentityObservation:
    """Represent both canonical identifiers from one provider observation."""

    task_id: str
    conversation_id: str
    task_revision: str
    conversation_revision: str
    ambiguous: bool = False
    conflicting: bool = False


@dataclass(frozen=True)
class _TitleTarget:
    """Represent the requested title target and its claimed provenance."""

    task_id: str
    conversation_id: str
    source: str


def _is_atomic_provider_identity(
    observation: _ProviderIdentityObservation | None,
) -> bool:
    """Return whether one conclusive provider revision supplied both IDs."""

    return bool(
        observation is not None
        and observation.task_id
        and observation.conversation_id
        and observation.task_revision
        and observation.task_revision == observation.conversation_revision
        and not observation.ambiguous
        and not observation.conflicting
    )


def _execute_self_title_operation(
    before: _ProviderIdentityObservation | None,
    target: _TitleTarget,
    after: _ProviderIdentityObservation | None,
    title_call: Callable[[str, str], None],
) -> str:
    """Apply the executable self-title identity and zero-call contract."""

    if not _is_atomic_provider_identity(before):
        return _COORDINATOR_DECISION_REQUIRED
    assert before is not None
    if (
        target.source != _PROVIDER_RECORDED_TARGET
        or target.task_id != before.task_id
        or target.conversation_id != before.conversation_id
    ):
        return _COORDINATOR_DECISION_REQUIRED

    title_call(target.task_id, target.conversation_id)

    if not _is_atomic_provider_identity(after):
        return _POST_CALL_IDENTITY_MISMATCH
    assert after is not None
    if (
        after.task_id != before.task_id
        or after.conversation_id != before.conversation_id
        or after.task_revision != before.task_revision
    ):
        return _POST_CALL_IDENTITY_MISMATCH
    return _TITLE_UPDATED


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


def _user_action_required_section(text: str) -> str:
    """Return the normalized project-private User Action Required contract."""

    section = text.split("## User Action Required Handoff", 1)[1].split(
        "## Dispatch Workflow",
        1,
    )[0]
    return " ".join(section.split())


def _conversation_title_section(text: str) -> str:
    """Return the normalized canonical conversation-title contract."""

    section = text.split("## Conversation Title Contract", 1)[1].split(
        "## Codex Runtime Reconciliation",
        1,
    )[0]
    return " ".join(section.split())


def _visible_task_launch_section(text: str) -> str:
    """Return the normalized visible Work Item task launch contract."""

    section = text.split("## Visible Work Item Task Launch", 1)[1].split(
        "## User Action Required Handoff",
        1,
    )[0]
    return " ".join(section.split())


def _assert_user_action_required_contract(
    test_case: unittest.TestCase,
    section: str,
) -> None:
    """Assert the visible-task ownership and outcome contract for one section."""

    for clause in (
        "visible Work Item root task owns the user-facing question and retained conversation",
        "The question must not exist only in the hidden nested Dev Orchestrator context",
        "User Action Required releases active execution capacity",
        "must not replace or archive that preserved task while the answer is pending",
        "clear answer selects an offered in-scope option that approves continued work",
        "A clear deferral does not run the restart sequence",
        "A clear decline does not run the restart sequence",
    ):
        test_case.assertIn(clause, section)

    forbidden_patterns = (
        r"\b(?:root backlog )?dispatcher\b.{0,40}\b(?:may|can|must|should|will)\b(?!\s+not\b).{0,25}\bwait(?:s|ing)?\b",
        r"\bquestion\b.{0,40}\b(?:may|can|must|should|will)\b(?!\s+not\b).{0,30}\b(?:exist|remain|stay|be)\b.{0,30}\b(?:only|solely)\b.{0,30}\bhidden\b",
        r"\b(?:hidden|nested dev orchestrator)\b.{0,40}\b(?:may|can|must|should|will)\b(?!\s+not\b).{0,30}\b(?:be|own|hold)\b.{0,30}\b(?:only|sole)\b.{0,30}\b(?:context|question)\b",
        r"\b(?:preserved|canonical|visible)\b.{0,30}\btask\b.{0,30}\b(?:may|can|must|should|will)\b(?!\s+not\b).{0,25}\b(?:archiv(?:e|ed|ing)|replac(?:e|ed|ing))\b",
        r"\b(?:root )?(?:backlog )?dispatcher\b.{0,40}\b(?:may|can|must|should|will)\b(?!\s+not\b).{0,25}\b(?:archiv(?:e|ed|ing)|replac(?:e|ed|ing))\b.{0,40}\b(?:preserved|canonical|visible)\b.{0,20}\btask\b",
        r"\b(?:user action required|uar)\b.{0,40}\b(?:may|can|must|should|will)\b(?!\s+not\b).{0,30}\b(?:retain|consume|occupy|hold)\b.{0,30}\b(?:active )?capacity\b",
        r"\b(?:all|every|any)\b.{0,20}\bclear answers?\b.{0,30}\b(?:may|can|must|should|will)\b(?!\s+not\b).{0,25}\b(?:restart|resume)\b",
    )
    normalized_lower = section.lower()
    for pattern in forbidden_patterns:
        test_case.assertNotRegex(normalized_lower, pattern)


class CodexTaskControlPackageTests(unittest.TestCase):
    """Keep Codex task creation, identity, reconciliation, and cleanup in one peer."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.codex = CODEX_SKILL_PATH.read_text(encoding="utf-8")
        cls.dispatcher = DISPATCHER_SKILL_PATH.read_text(encoding="utf-8")
        cls.portable = PORTABLE_SKILL_PATH.read_text(encoding="utf-8")
        cls.normalized = " ".join(cls.codex.split())
        cls.normalized_dispatcher = " ".join(cls.dispatcher.split())

    def test_codex_skill_owns_only_runtime_mapping_sections(self) -> None:
        for heading in (
            "Codex Capability Check",
            "Codex Task Creation And Resumption",
            "Canonical Codex Task Identity",
            "Conversation Title Contract",
            "Codex Runtime Reconciliation",
            "Bounded Successor Recovery",
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
            "does not create Work-item lifecycle authority, delivery authority, or resource ownership",
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

    def test_self_title_requires_exact_recorded_identity_pair(self) -> None:
        title_contract = _conversation_title_section(self.codex)

        self.assertNotEqual(
            ORDINARY_WORKER_IDENTITY["task_id"],
            ORDINARY_WORKER_IDENTITY["conversation_id"],
        )
        for clause in (
            "own recorded canonical Codex Task ID and Conversation ID",
            "one atomic provider observation",
            "same authoritative provider revision",
            "exactly match both recorded identifiers before the title operation",
            "Confirm the same Task ID, Conversation ID, and authoritative provider revision",
            "Report a post-call identity mismatch",
            "Do not report title success for that outcome",
            "does not collapse the two required identity checks",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, title_contract)

    def test_self_title_runtime_call_contract_is_table_driven(self) -> None:
        ordinary_before = _ProviderIdentityObservation(
            task_id=ORDINARY_WORKER_IDENTITY["task_id"],
            conversation_id=ORDINARY_WORKER_IDENTITY["conversation_id"],
            task_revision="provider-revision-101",
            conversation_revision="provider-revision-101",
        )
        ordinary_target = _TitleTarget(
            task_id=ordinary_before.task_id,
            conversation_id=ordinary_before.conversation_id,
            source=_PROVIDER_RECORDED_TARGET,
        )
        combined_before = _ProviderIdentityObservation(
            task_id=COMBINED_RUNTIME_IDENTITY["task_id"],
            conversation_id=COMBINED_RUNTIME_IDENTITY["conversation_id"],
            task_revision="provider-revision-202",
            conversation_revision="provider-revision-202",
        )
        combined_target = _TitleTarget(
            task_id=combined_before.task_id,
            conversation_id=combined_before.conversation_id,
            source=_PROVIDER_RECORDED_TARGET,
        )
        cases = (
            (
                "accepted unequal pair",
                ordinary_before,
                ordinary_target,
                ordinary_before,
                _TITLE_UPDATED,
                1,
            ),
            (
                "accepted combined identity",
                combined_before,
                combined_target,
                combined_before,
                _TITLE_UPDATED,
                1,
            ),
            *(
                (
                    f"rejected {source}",
                    ordinary_before,
                    _TitleTarget(
                        task_id=ordinary_before.task_id,
                        conversation_id=ordinary_before.conversation_id,
                        source=source,
                    ),
                    ordinary_before,
                    _COORDINATOR_DECISION_REQUIRED,
                    0,
                )
                for source in (
                    "delegation source",
                    "source_thread_id",
                    "runtime parent",
                    "root Dispatcher",
                    "Coordinator",
                    "nested Orchestrator",
                    "title-derived target",
                )
            ),
            (
                "missing evidence",
                None,
                ordinary_target,
                ordinary_before,
                _COORDINATOR_DECISION_REQUIRED,
                0,
            ),
            (
                "missing conversation identity",
                _ProviderIdentityObservation(
                    task_id=ordinary_before.task_id,
                    conversation_id="",
                    task_revision=ordinary_before.task_revision,
                    conversation_revision=ordinary_before.conversation_revision,
                ),
                ordinary_target,
                ordinary_before,
                _COORDINATOR_DECISION_REQUIRED,
                0,
            ),
            (
                "ambiguous evidence",
                replace(ordinary_before, ambiguous=True),
                ordinary_target,
                ordinary_before,
                _COORDINATOR_DECISION_REQUIRED,
                0,
            ),
            (
                "target conflicts with provider pair",
                ordinary_before,
                _TitleTarget(
                    task_id="task-other-worker-303",
                    conversation_id=ordinary_before.conversation_id,
                    source=_PROVIDER_RECORDED_TARGET,
                ),
                ordinary_before,
                _COORDINATOR_DECISION_REQUIRED,
                0,
            ),
            (
                "conflicting evidence",
                replace(ordinary_before, conflicting=True),
                ordinary_target,
                ordinary_before,
                _COORDINATOR_DECISION_REQUIRED,
                0,
            ),
            (
                "split provider revisions",
                _ProviderIdentityObservation(
                    task_id=ordinary_before.task_id,
                    conversation_id=ordinary_before.conversation_id,
                    task_revision="provider-revision-101",
                    conversation_revision="provider-revision-102",
                ),
                ordinary_target,
                ordinary_before,
                _COORDINATOR_DECISION_REQUIRED,
                0,
            ),
            (
                "post-call pair mismatch",
                ordinary_before,
                ordinary_target,
                _ProviderIdentityObservation(
                    task_id="task-other-worker-303",
                    conversation_id=ordinary_before.conversation_id,
                    task_revision=ordinary_before.task_revision,
                    conversation_revision=ordinary_before.conversation_revision,
                ),
                _POST_CALL_IDENTITY_MISMATCH,
                1,
            ),
            (
                "post-call revision mismatch",
                ordinary_before,
                ordinary_target,
                _ProviderIdentityObservation(
                    task_id=ordinary_before.task_id,
                    conversation_id=ordinary_before.conversation_id,
                    task_revision="provider-revision-303",
                    conversation_revision="provider-revision-303",
                ),
                _POST_CALL_IDENTITY_MISMATCH,
                1,
            ),
        )

        for label, before, target, after, expected, expected_calls in cases:
            calls: list[tuple[str, str]] = []

            def title_call(task_id: str, conversation_id: str) -> None:
                calls.append((task_id, conversation_id))

            with self.subTest(case=label):
                outcome = _execute_self_title_operation(
                    before,
                    target,
                    after,
                    title_call,
                )
                self.assertEqual(expected, outcome)
                self.assertEqual(expected_calls, len(calls))
                if expected_calls:
                    self.assertEqual(
                        [(target.task_id, target.conversation_id)],
                        calls,
                    )

    def test_combined_runtime_still_validates_both_identity_fields(self) -> None:
        title_contract = _conversation_title_section(self.codex)

        self.assertEqual(
            COMBINED_RUNTIME_IDENTITY["task_id"],
            COMBINED_RUNTIME_IDENTITY["conversation_id"],
        )
        self.assertIn(
            "When one combined runtime surface supplies the same value for both fields",
            title_contract,
        )
        self.assertIn(
            "validate that value independently as the recorded Task ID and Conversation ID",
            title_contract,
        )

    def test_self_title_rejects_routing_parent_and_derived_targets(self) -> None:
        title_contract = _conversation_title_section(self.codex)

        for rejected_target in (
            "delegation source",
            "source_thread_id",
            "runtime parent",
            "root Backlog Dispatcher",
            "Coordinator task",
            "nested Dev Orchestrator",
            "title-derived identity",
        ):
            with self.subTest(rejected_target=rejected_target):
                self.assertIn(rejected_target, title_contract)
        self.assertIn("routing or evidence fields only", title_contract)
        self.assertIn("must not be a self-title target", title_contract)

    def test_self_title_ambiguity_stops_before_mutation(self) -> None:
        title_contract = _conversation_title_section(self.codex)

        for clause in (
            "missing, ambiguous, or conflicts with authoritative Work-item content",
            "perform zero title mutation",
            "one specific Coordinator decision request",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, title_contract)

    def test_visible_worker_title_cannot_change_root_dispatcher_title(self) -> None:
        launch_contract = _visible_task_launch_section(self.dispatcher)

        for clause in (
            "uses only its own recorded canonical Codex Task ID and Conversation ID",
            "must not target the root Backlog Dispatcher",
            "root Backlog Dispatcher title is governed independently",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, launch_contract)

    def test_dispatcher_title_suppression_is_identity_scoped(self) -> None:
        watchdog = self.dispatcher.split("## Watchdog Boundary", 1)[1].split(
            "## Live Refinement",
            1,
        )[0]
        normalized_watchdog = " ".join(watchdog.split())

        for clause in (
            "corrected root Dispatcher title is terminal suppression evidence",
            "same root-title incident",
            "must not suppress an unresolved visible worker title mismatch",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, normalized_watchdog)

    def test_dispatcher_watchdog_uses_a_standalone_project_automation(self) -> None:
        watchdog = self.dispatcher.split("## Watchdog Boundary", 1)[1].split(
            "## Live Refinement",
            1,
        )[0]
        normalized_watchdog = " ".join(watchdog.split())

        for clause in (
            "project-private standalone Watchdog rule overrides the generic canonical-task wakeup mapping",
            "Create or update exactly one standalone project automation named Backlog Watchdog",
            "current saved project and its local execution environment",
            "starts a fresh Codex task for every run",
            "not attached to the root Backlog Dispatcher or any existing chat",
            "Do not create a chat-attached heartbeat",
            "do not set targetThreadId",
            "preserve its cadence and prompt while changing its execution topology",
            "do not create a duplicate",
            "read current authoritative provider and runtime evidence from scratch",
            "Archive its own run task only when the cycle finds nothing actionable",
            "Leave actionable or failed runs visible",
            "ask for the cadence instead of inventing one",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, normalized_watchdog)

    def test_dispatcher_run_is_disposable_and_not_a_worker_mailbox(self) -> None:
        run_lifetime = self.dispatcher.split(
            "## Dispatcher Run Lifetime",
            1,
        )[1].split("## Role Division", 1)[0]
        normalized_run_lifetime = " ".join(run_lifetime.split())

        for clause in (
            "Each automated Backlog Dispatcher cycle runs as a standalone scheduled task in a fresh conversation",
            "disposable runtime executor, not a retained coordination conversation",
            "obtains one Coordinator decision",
            "returns the exact result to the Coordinator during the same run",
            "then archives itself",
            "A launched Work Item task continues independently after the Dispatcher run ends",
            "Runtime Parent Task ID records which Dispatcher run created the task",
            "provenance and ambiguous-creation evidence, not a callback address",
            "Do not use a Dispatcher conversation as a polling loop, worker mailbox, durable queue, or coordination ledger",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, normalized_run_lifetime)

        workflow = self.dispatcher.split("## Dispatch Workflow", 1)[1].split(
            "## Dispatch Packet",
            1,
        )[0]
        normalized_workflow = " ".join(workflow.split())
        self.assertIn(
            "Observe the created or resumed task only until its identity and immediate runtime outcome are stable enough for reconciliation",
            normalized_workflow,
        )
        self.assertIn(
            "archive the calling Dispatcher run, and stop",
            normalized_workflow,
        )
        self.assertIn(
            "Do not wait for the Work Item task to finish",
            normalized_workflow,
        )

    def test_dispatcher_run_does_not_require_self_title_mutation(self) -> None:
        run_lifetime = self.dispatcher.split(
            "## Dispatcher Run Lifetime",
            1,
        )[1].split("## Role Division", 1)[0]
        normalized_run_lifetime = " ".join(run_lifetime.split())

        self.assertNotIn(
            "set the calling Dispatcher run's title",
            normalized_run_lifetime,
        )
        self.assertNotIn(
            "Dispatch followed by the short Work Item title",
            normalized_run_lifetime,
        )

    def test_dispatcher_cleanup_and_result_do_not_require_original_run(self) -> None:
        cleanup = self.dispatcher.split("## Terminal Cleanup", 1)[1].split(
            "## Partial And Ambiguous Runtime Outcomes",
            1,
        )[0]
        normalized_cleanup = " ".join(cleanup.split())
        self.assertIn(
            "need not be the Dispatcher run that originally created the Work Item task",
            normalized_cleanup,
        )
        self.assertIn(
            "Authorization and canonical identity come from the current provider record and Coordinator packet",
            normalized_cleanup,
        )

        result = self.dispatcher.split("## Result", 1)[1]
        normalized_result = " ".join(result.split())
        self.assertIn(
            "archive the calling Dispatcher run unless it must remain visible for one unresolved user decision or ambiguous runtime mutation",
            normalized_result,
        )
        self.assertIn(
            "Archiving the run must not pause or delete the recurring Dispatcher automation",
            normalized_result,
        )

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

    def test_dispatcher_launch_prompt_is_reference_plus_delta(self) -> None:
        launch_prompt = _prompt_template(
            self.dispatcher,
            "Reference-Plus-Delta Launch Prompt",
        )

        self.assertEqual(REFERENCE_PLUS_DELTA_LAUNCH_PROMPT, launch_prompt)
        self.assertEqual(1, launch_prompt.count("Launch one Dev Orchestrator subagent"))
        self.assertEqual(4, len(launch_prompt.splitlines()))
        self.assertEqual(
            1,
            launch_prompt.count(
                "As the root task, you provide the Codex title and messaging "
                "the subagents may need."
            ),
        )
        for copied_heading in (
            "Requirements:",
            "Scope:",
            "Acceptance Criteria:",
            "Verification:",
            "Lifecycle:",
            "Claims:",
            "Review:",
            "Delivery:",
            "Cleanup:",
            "Recovery:",
        ):
            with self.subTest(copied_heading=copied_heading):
                self.assertNotIn(copied_heading, launch_prompt)

    def test_private_dispatcher_precedence_narrows_generic_launch_topology(
        self,
    ) -> None:
        self.assertIn(
            "create at most one root Dev Orchestrator task",
            self.normalized,
        )

        for clause in (
            "For Backlog Dispatcher launches, this project-private skill governs launch topology",
            "takes precedence over the generic root Dev Orchestrator task wording in coordinate-codex-tasks",
            "coordinate-codex-tasks supplies task-control mechanics only",
            "This project-private runtime specialization does not move Work-item lifecycle, capacity, Persistence, or resource-claim authority to the visible task wrapper",
            "except the direct User Action Required answer recovery assigned below to the nested Dev Orchestrator",
            "The user-visible Codex task is the canonical Work Item runtime identity",
            "The nested Dev Orchestrator collaboration subagent is not that canonical task",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, self.normalized_dispatcher)

    def test_visible_dispatch_sequence_has_exact_actors_and_title_owner(
        self,
    ) -> None:
        self.assertIn("## Visible Work Item Task Launch", self.dispatcher)
        launch_contract = self.dispatcher.split(
            "## Visible Work Item Task Launch",
            1,
        )[1].split("## Dispatch Workflow", 1)[0]
        normalized_contract = " ".join(launch_contract.split())
        launch_prompt = _prompt_template(
            self.dispatcher,
            "Reference-Plus-Delta Launch Prompt",
        )
        sequence = (
            "The root Backlog Dispatcher creates exactly one user-visible Codex task",
            "The root Dispatcher gives that visible task the exact Reference-Plus-Delta Launch Prompt below as its initial prompt",
            "The visible task then launches exactly one nested Dev Orchestrator collaboration subagent for the authoritative Work-item content",
            "The nested Dev Orchestrator independently records Starting -> Running before any source mutation",
        )

        positions = [normalized_contract.index(clause) for clause in sequence]
        self.assertEqual(sorted(positions), positions)
        self.assertEqual(REFERENCE_PLUS_DELTA_LAUNCH_PROMPT, launch_prompt)
        self.assertEqual(1, launch_prompt.count("Launch one Dev Orchestrator subagent"))
        for clause in (
            "The root Dispatcher must not directly launch that hidden collaboration subagent as the Work Item launch",
            "Lifecycle and material Running-phase title operations remain on the visible Codex task",
            "They do not target the nested Dev Orchestrator collaboration subagent",
            "Preserve an already-live hidden Work Item execution as its existing owner until it stops or completes",
            "Do not create a visible replacement task while that hidden execution is live",
            "do not launch duplicate implementation",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, normalized_contract)

    def test_visible_root_prompt_defines_title_and_messaging_owner(self) -> None:
        launch_prompt = _prompt_template(
            self.dispatcher,
            "Reference-Plus-Delta Launch Prompt",
        )

        self.assertEqual(REFERENCE_PLUS_DELTA_LAUNCH_PROMPT, launch_prompt)
        for clause in (
            "root task means the visible Work Item root task",
            "It does not mean the root Backlog Dispatcher or the nested Dev Orchestrator",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, self.normalized_dispatcher)

    def test_user_action_required_question_stays_in_visible_context(self) -> None:
        normalized_handoff = _user_action_required_section(self.dispatcher)

        _assert_user_action_required_contract(self, normalized_handoff)

        for clause in (
            "visible Work Item root task owns the user-facing question and retained conversation",
            "one exact clear question with concrete examples or options",
            "The question must not exist only in the hidden nested Dev Orchestrator context",
            "The root Backlog Dispatcher must not become the waiting conversation or relay the question or answer",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, normalized_handoff)


    def test_user_action_required_contract_rejects_semantic_mutations(self) -> None:
        section = _user_action_required_section(self.dispatcher)
        mutations = (
            ("dispatcher wait", "The root Backlog Dispatcher may wait for the answer."),
            ("dispatcher wait actor", "A dispatcher can wait for the user reply."),
            (
                "hidden-only question",
                "The question can exist solely in the hidden Dev Orchestrator context.",
            ),
            (
                "hidden-only actor",
                "The nested Dev Orchestrator may be the only context for the question.",
            ),
            (
                "archive pending task",
                "The preserved task may be archived while the answer is pending.",
            ),
            (
                "replace pending task",
                "The root Dispatcher can replace the canonical task while waiting.",
            ),
            (
                "retain capacity",
                "User Action Required may retain an active capacity slot.",
            ),
            (
                "restart every clear answer",
                "Every clear answer must restart the work.",
            ),
        )

        for label, mutation in mutations:
            with self.subTest(mutation=label):
                with self.assertRaises(AssertionError):
                    _assert_user_action_required_contract(
                        self,
                        f"{section} {mutation}",
                    )

    def test_visible_root_synchronizes_own_title_before_reporting(self) -> None:
        for clause in (
            "synchronizes its own title immediately after durable authoritative lifecycle or material-phase evidence exists",
            "before reporting that evidence",
            "No separate authorization is required solely for this own-title update",
            "Waiting for User — short work-item title",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, self.normalized_dispatcher)

    def test_approved_in_scope_answer_runs_ordered_recovery_directly(self) -> None:
        handoff = self.dispatcher.split(
            "## User Action Required Handoff",
            1,
        )[1].split("## Dispatch Workflow", 1)[0]
        normalized_handoff = " ".join(handoff.split())
        sequence = (
            "clear answer selects an offered in-scope option that approves continued work",
            "forwards that approved answer directly to its nested Dev Orchestrator",
            "persists that exact answer through the selected Persistence manager",
            "records User Action Required -> Ready",
            "Ready -> Starting",
            "Starting -> Running",
            "resumes the preserved work",
        )

        for clause in sequence:
            with self.subTest(clause=clause):
                self.assertIn(clause, normalized_handoff)
        if all(clause in normalized_handoff for clause in sequence):
            positions = [normalized_handoff.index(clause) for clause in sequence]
            self.assertEqual(sorted(positions), positions)

    def test_deferred_answer_records_holding_without_restart(self) -> None:
        handoff = self.dispatcher.split(
            "## User Action Required Handoff",
            1,
        )[1].split("## Dispatch Workflow", 1)[0]
        normalized_handoff = " ".join(handoff.split())

        for clause in (
            "A clear deferral does not run the restart sequence",
            "records the portable Holding outcome",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, normalized_handoff)

    def test_declined_answer_records_rejection_without_restart(self) -> None:
        handoff = self.dispatcher.split(
            "## User Action Required Handoff",
            1,
        )[1].split("## Dispatch Workflow", 1)[0]
        normalized_handoff = " ".join(handoff.split())

        for clause in (
            "A clear decline does not run the restart sequence",
            "records the applicable portable rejection or abandonment outcome",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, normalized_handoff)

        self.assertNotIn(
            "Every clear answer runs the restart sequence",
            normalized_handoff,
        )
        for contradiction in (
            "A clear deferral runs the restart sequence",
            "A clear decline runs the restart sequence",
            "The nested Dev Orchestrator restarts work for every clear answer",
        ):
            with self.subTest(contradiction=contradiction):
                self.assertNotIn(contradiction, normalized_handoff)

    def test_user_action_required_preserves_same_task_and_evidence(self) -> None:
        handoff = self.dispatcher.split(
            "## User Action Required Handoff",
            1,
        )[1].split("## Dispatch Workflow", 1)[0]
        normalized_handoff = " ".join(handoff.split())

        for clause in (
            "preserves the same canonical visible Work Item root task",
            "candidate, provider evidence, and resumption context",
            "must not replace or archive that preserved task while the answer is pending",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, normalized_handoff)

        for contradiction in (
            "replace the preserved task while the answer is pending",
            "archive the preserved task while the answer is pending",
            "The root Backlog Dispatcher may replace the canonical task while the answer is pending",
        ):
            with self.subTest(contradiction=contradiction):
                self.assertNotIn(contradiction, normalized_handoff)

    def test_recovery_reacquires_claims_only_at_claim_events(self) -> None:
        self.assertIn(
            "reacquires each claim only at its applicable Claim Event boundary",
            self.normalized_dispatcher,
        )

    def test_user_action_required_releases_active_capacity(self) -> None:
        handoff = self.dispatcher.split(
            "## User Action Required Handoff",
            1,
        )[1].split("## Dispatch Workflow", 1)[0]
        normalized_handoff = " ".join(handoff.split())

        self.assertIn(
            "User Action Required releases active execution capacity",
            normalized_handoff,
        )
        self.assertNotIn(
            "User Action Required retains active execution capacity",
            normalized_handoff,
        )

    def test_dispatcher_continues_unrelated_eligible_work(self) -> None:
        self.assertIn(
            "continues dispatching unrelated eligible Work Items",
            self.normalized_dispatcher,
        )
        self.assertIn(
            "does not wait for the user's answer",
            self.normalized_dispatcher,
        )

    def test_user_action_required_escalation_has_bounded_exceptions(self) -> None:
        self.assertIn(
            "For this handoff, consult the Coordinator only for",
            self.normalized_dispatcher,
        )
        for clause in (
            "an ambiguous answer",
            "conflicting authoritative evidence",
            "an out-of-scope request or authority expansion",
            "a cross-item priority or capacity decision",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, self.normalized_dispatcher)

        self.assertIn(
            "This direct classification and provider mutation by the existing nested Dev Orchestrator is the user-authorized project-private specialization",
            self.normalized_dispatcher,
        )
        self.assertIn(
            "It does not require the root Backlog Dispatcher to relay a clear in-scope answer through the Coordinator",
            self.normalized_dispatcher,
        )

    def test_resumption_preserves_canonical_live_hidden_execution(self) -> None:
        launch_contract = self.dispatcher.split(
            "## Visible Work Item Task Launch",
            1,
        )[1].split("## Dispatch Workflow", 1)[0]
        workflow = self.dispatcher.split("## Dispatch Workflow", 1)[1].split(
            "## Dispatch Packet",
            1,
        )[0]
        normalized_launch = " ".join(launch_contract.split())
        normalized_workflow = " ".join(workflow.split())

        self.assertIn(
            "Preserve an already-live hidden Work Item execution as its existing owner until it stops or completes",
            normalized_launch,
        )
        self.assertIn(
            "this is the ordinary resume operation, including for an idle task or an already-live hidden execution preserved as the existing owner",
            normalized_workflow,
        )
        self.assertIn(
            "Require the visible wrapper only for a new dispatch",
            normalized_workflow,
        )
        self.assertNotIn(
            "resume the canonical visible task",
            normalized_workflow,
        )

    def test_dispatcher_resumes_unarchived_task_or_transfers_archived_owner(self) -> None:
        workflow = self.dispatcher.split("## Dispatch Workflow", 1)[1].split(
            "## Dispatch Packet",
            1,
        )[0]
        normalized_workflow = " ".join(workflow.split())

        for clause in (
            "first read the provider-recorded canonical task and reconcile whether that exact task is archived",
            "When it is not archived, call send_message_to_thread with its exact task ID and host",
            "this is the ordinary resume operation",
            "When the canonical task is archived, do not send a follow-up to it and do not unarchive it",
            "Require the Coordinator to authorize one successor",
            "create exactly one new visible task",
            "durably transfer runtime ownership in the Work-item provider from the archived identity to the returned successor identity",
            "Preserve the archived identity as predecessor provenance",
            "Reconcile an ambiguous creation result before any retry",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, normalized_workflow)

    def test_dispatcher_rejects_reconstructed_launch_packets(self) -> None:
        packet_contract = self.dispatcher.split("## Dispatch Packet", 1)[1].split(
            "## Incoming Coordination Messages",
            1,
        )[0]
        normalized_contract = " ".join(packet_contract.split())

        for clause in (
            "Persist every stable assignment fact missing from the Work-item content before launch",
            "A launch is invalid while a stable assignment fact is absent from the Work-item content",
            "Reject a launch prompt that copies provider requirements, scope, acceptance criteria, or verification expectations",
            "Reject a launch prompt that copies lifecycle, claim, review, verification, delivery, cleanup, or recovery procedures from selected skills",
            "Reject generic task or worker wording and any instruction to reconstruct root awareness",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, normalized_contract)

        for superseded_clause in (
            "normalized objective and complete initial or follow-up prompt",
            "work-item and path or resource claim instructions",
            "verification, delivery, provider closeout, reporting, and cleanup expectations",
        ):
            with self.subTest(superseded_clause=superseded_clause):
                self.assertNotIn(superseded_clause, normalized_contract)

        for legacy_complete_packet_clause in (
            "complete dispatch or resumption packets",
            "a complete execution packet",
        ):
            with self.subTest(
                legacy_complete_packet_clause=legacy_complete_packet_clause,
            ):
                self.assertNotIn(
                    legacy_complete_packet_clause,
                    self.normalized_dispatcher,
                )

    def test_dispatcher_prohibits_cross_project_runtime_control(self) -> None:
        for clause in (
            "A local claim or modified files do not extend runtime-control authority outside the current project or working-directory coordination context",
            "Do not send a coordination, stop, resume, cleanup, or lifecycle-control message to a task outside that context",
            "even when one of its subagents owns a local claim or modified files in the current repository",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, self.normalized_dispatcher)

    def test_dispatcher_stranded_ownership_requires_coordinator_recovery(
        self,
    ) -> None:
        for clause in (
            "do not use a cross-project parent task as a relay",
            "Treat the ownership as unaddressable or stranded",
            "Preserve the bytes and evidence",
            "perform no cross-project runtime mutation",
            "return the limitation to the Dev Backlog Coordinator for an explicitly authorized recovery decision",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause.lower(), self.normalized_dispatcher.lower())

    def test_successor_requires_failed_capability_and_exhausted_same_task_recovery(
        self,
    ) -> None:
        for clause in (
            "observed failure of an ordinary required capability during the active workload",
            "exhausted bounded identity-preserving recovery through the same canonical task",
            "A capability-pilot mismatch follows the pilot correction path and is not successor evidence",
            "Idle, slow, quiet, or awaiting an ordinary bounded operation",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, self.normalized)

    def test_successor_preserves_durable_authority_and_runs_once(self) -> None:
        for clause in (
            "complete Work-item content",
            "accepted commit",
            "branch and worktree",
            "applicable claims",
            "completed reviews",
            "verifier evidence",
            "delivery state",
            "authoritative recovery evidence",
            "exactly one successor root execution",
            "durable old-to-new identity handoff",
            "must not authorize another successor",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, self.normalized)

    def test_successor_reconciles_creation_and_accepts_running_before_work(self) -> None:
        for text in (self.normalized, self.normalized_dispatcher):
            with self.subTest(source="codex" if text == self.normalized else "dispatcher"):
                for clause in (
                    "reconcile active and archived runtime tasks",
                    "do not issue another create operation",
                    "Starting -> Running",
                    "before any repository or shared-work mutation",
                    "old execution and every duplicate must be stopped or permanently barred",
                    "only the accepted successor may mutate repository or shared work",
                    "truthful non-active provider disposition",
                ):
                    with self.subTest(clause=clause):
                        self.assertIn(clause.lower(), text.lower())

        self.assertIn(
            "The required Starting -> Running provider update remains the successor's lifecycle acceptance",
            self.normalized,
        )
        self.assertIn(
            "sole lifecycle mutation permitted before Running becomes durable",
            self.normalized,
        )
        self.assertIn(
            "execute only the Coordinator's exact one-successor authorization",
            self.normalized_dispatcher,
        )
        self.assertIn(
            "prevent concurrent mutation by the old execution, a duplicate, or the successor",
            self.normalized_dispatcher.lower(),
        )

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

    def test_watchdog_prompt_is_canonical_with_watchdog_owned_scheduling(self) -> None:
        standing = _prompt_template(self.codex, "Canonical Standing Prompt Template")

        self.assertEqual(CANONICAL_STANDING_PROMPT, standing)
        self.assertEqual(
            CANONICAL_STANDING_PROMPT.replace(
                "{runtime_parent_task_id}", "parent-17"
            )
            .replace("{coordinator_task_id}", "coordinator-23")
            .replace("{repository_root}", "/workspace/project"),
            standing.replace("{runtime_parent_task_id}", "parent-17")
            .replace("{coordinator_task_id}", "coordinator-23")
            .replace("{repository_root}", "/workspace/project"),
        )
        self.assertNotIn("Canonical Heartbeat Prompt Template", self.codex)
        self.assertIn(
            "When a Watchdog schedule is configured, it must wake the canonical Watchdog task",
            self.codex,
        )
        self.assertIn(
            "Do not schedule the Coordinator to wake merely to send routine heartbeat or progress follow-ups",
            self.codex,
        )
        self.assertIn(
            "do not use a Watchdog wakeup to request progress from another task",
            self.codex,
        )

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
