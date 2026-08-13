#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Simulates read-only active, blocked, and terminal campaign reconciliation.
# Governing design: design/orchestrated-development-lifecycle.html
# Governing test plan: evals/agent-tests/dev-backlog-watchdog/requirements-matrix.md

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


ACTIVE_CAPACITY_STATUSES = {"Starting", "Running"}
ACTIVE_CAPACITY_LIMIT = 10
ACTIVE_SERIES_STATUSES = {"Ready", "Starting", "Running", "Awaiting Review"}
TERMINAL_STATUSES = {"Completed", "Failed", "Abandoned"}
BLOCKAGE_EXCLUDED_STATUSES = {
    "User Action Required",
    "Holding",
    "Future Idea",
    *TERMINAL_STATUSES,
}
_TASK_ANOMALY_STATES = {"failed", "stopped", "missing"}
_ACTIVE_TASK_STATES = {"active", "running"}
_RUNNING_TITLE_PHASES = {
    "Implementing",
    "Reviewing",
    "Verifying",
    "Integrating",
    "Waiting for Claim",
    "Waiting for Help",
}
_LIFECYCLE_TITLE_LABELS = {
    "Ready": "Ready",
    "Starting": "Starting",
    "User Action Required": "Waiting for User",
    "Stalled": "Stalled",
    "Blocked": "Blocked",
    "Holding": "Holding",
    "Awaiting Review": "Awaiting Review",
    "Completed": "Done",
    "Failed": "Failed",
    "Abandoned": "Abandoned",
}
_SAFE_TERMINAL_WORKTREE_DISPOSITIONS = {"absent", "removed"}
_SAFE_DELIVERY_BRANCH_DISPOSITIONS = {"absent", "merged", "removed"}
_SAFE_CLEANUP_BRANCH_DISPOSITIONS = {"absent", "removed"}
_SAFE_SOURCE_BRANCH_DISPOSITIONS = {"absent", "removed"}
_PRESERVABLE_SOURCE_BRANCH_RELATIONS = {"non-ancestral", "non-equivalent"}
_CLAIM_APPLICABILITY_VALUES = {"unknown", "not-applicable", "applicable"}
_NORMALIZED_EFFECTIVE_STATUSES = {
    "Ready",
    "Starting",
    "Running",
    "Stalled",
    "Blocked",
    "User Action Required",
    "Holding",
    "Awaiting Review",
    *TERMINAL_STATUSES,
}


@dataclass(frozen=True)
class DispositionReceipt:
    """Describe a structured disposition already recorded for a Blocked item."""

    outcome: str
    state: str
    owner: str
    evidence: str
    observable_trigger: str
    unresolved_findings: tuple[str, ...] = ()


@dataclass(frozen=True)
class ArchivePauseEvidence:
    """Describe current user direction that pauses named Codex task archival.

    source identifies whether the evidence is current user direction. scope must
    name Codex task archival. task_ids contains the exact affected task IDs.
    evidence retains the direction, and acknowledged records Coordinator receipt.
    """

    source: str
    scope: str
    task_ids: tuple[str, ...]
    evidence: str
    acknowledged: bool


@dataclass
class WorkItem:
    """Represent the evidence visible to one deterministic watchdog cycle.

    provider_identity is the selected provider reference or provider-none task.
    status is the current lifecycle state. The remaining fields describe
    observable progress, canonical execution identity, exit conditions, and
    terminal cleanup evidence. Instances are read by WatchdogCycle and are
    never mutated.
    """

    provider_identity: str
    status: str
    effective_status: str = ""
    causal_work_item_id: str = ""
    dependency_state_issue: str = ""
    phase: str = ""
    canonical_thread: str = ""
    root_task: str = ""
    short_title: str = ""
    runtime_task_kind: str = "canonical"
    conversation_title: str = ""
    last_productive_evidence: str = ""
    phase_estimate: str = ""
    hard_stop: str = ""
    progress_observation: str = ""
    estimate_boundary_crossed: bool = False
    hard_stop_crossed: bool = False
    progress_gap: bool = False
    task_state: str = "active"
    preventing_cause: str = ""
    blocker_owner: str = ""
    unblock_condition: str = ""
    next_action_owner: str = ""
    dependencies: tuple[str, ...] = ()
    dependency_evidence: tuple[str, ...] = ()
    candidate_evidence: tuple[str, ...] = ()
    review_verification_evidence: tuple[str, ...] = ()
    git_state: str = ""
    live_claims: tuple[str, ...] = ()
    dependency_or_unblock_satisfied: bool = False
    agent_actionable_recovery: str = ""
    active_recovery_owner: str = ""
    recovery_acknowledged: bool = False
    preservation_evidence_issue: str = ""
    correction_attempts_exhausted: bool = False
    correction_attempt_history: tuple[str, ...] = ()
    current_disposition: DispositionReceipt | None = None
    lifecycle_evidence_issue: str = ""
    next_action_owner_correct: bool = True
    stalled_exit_satisfied: bool = False
    blocker_exit_satisfied: bool = False
    provider_terminal_evidence: bool = False
    code_merged: bool = False
    claim_applicability: str = "unknown"
    released_claims: tuple[str, ...] = ()
    worktree: str = ""
    worktree_disposition: str = ""
    delivery_branch: str = ""
    delivery_branch_disposition: str = ""
    cleanup_branch: str = ""
    cleanup_branch_disposition: str = ""
    source_branch: str = ""
    source_branch_relation: str = ""
    source_branch_disposition: str = ""
    source_branch_preservation_evidence: str = ""
    acknowledged_source_branch_preservation_evidence: str = ""
    notification_pending: bool = False
    codex_archived: bool = False
    archive_pause: ArchivePauseEvidence | None = None


@dataclass(frozen=True)
class BlockedReconciliation:
    """Retain one complete read-only reconciliation result for a Blocked item."""

    provider_identity: str
    exact_blocker: str
    blocker_owner: str
    unblock_condition: str
    next_action_owner: str
    dependencies: tuple[str, ...]
    dependency_evidence: tuple[str, ...]
    candidate_evidence: tuple[str, ...]
    review_verification_evidence: tuple[str, ...]
    canonical_task_state: str
    conversation_title: str
    expected_conversation_title: str
    git_state: str
    live_claims: tuple[str, ...]
    correction_attempt_history: tuple[str, ...]
    current_disposition: DispositionReceipt | None
    actionable_reasons: tuple[str, ...]


@dataclass(frozen=True)
class TerminalReconciliation:
    """Retain complete read-only reconciliation for one terminal campaign task.

    The result records the observed lifecycle, delivery, claim, worktree,
    branch, notification, preservation, archival, and exact pause evidence.
    actionable_reasons contains only Coordinator-owned next actions.
    """

    provider_identity: str
    task_id: str
    lifecycle_status: str
    conversation_title: str
    expected_conversation_title: str
    provider_terminal_evidence: bool
    code_merged: bool
    claim_applicability: str
    claim_reconciliation_complete: bool
    live_claims: tuple[str, ...]
    released_claims: tuple[str, ...]
    worktree: str
    worktree_disposition: str
    delivery_branch: str
    delivery_branch_disposition: str
    cleanup_branch: str
    cleanup_branch_disposition: str
    source_branch: str
    source_branch_relation: str
    source_branch_disposition: str
    source_branch_preservation_evidence: str
    acknowledged_source_branch_preservation_evidence: str
    source_branch_deliberately_preserved: bool
    notification_pending: bool
    codex_archived: bool
    archive_pause: ArchivePauseEvidence | None
    archive_pause_valid: bool
    actionable_reasons: tuple[str, ...]


@dataclass(frozen=True)
class WatchdogAlert:
    """Describe one actionable observation for the parent Coordinator."""

    provider_identity: str
    evidence: str
    reason: str
    recommended_action: str
    preventing_cause: str


@dataclass(frozen=True)
class DependencyEffect:
    """Retain one derived dependency effect without changing provider state."""

    provider_identity: str
    stored_status: str
    effective_status: str
    causal_work_item_id: str


@dataclass(frozen=True)
class CycleResult:
    """Return retained reconciliations plus one no-action or aggregate alert outcome."""

    status: str
    message: str
    alert: WatchdogAlert | None
    blocked_reconciliations: tuple[BlockedReconciliation, ...] = ()
    terminal_reconciliations: tuple[TerminalReconciliation, ...] = ()
    dependency_effects: tuple[DependencyEffect, ...] = ()
    mutated: bool = False


@dataclass(frozen=True)
class BlockageObservation:
    """Describe one read-only observation of active blockage recovery."""

    status: str
    alert_parent: bool
    mutated: bool = False


def backlog_blockage_reasons(
    items: Iterable[WorkItem],
    *,
    minutes_without_progress: int = 0,
    user_declared: bool = False,
) -> tuple[str, ...]:
    """Return the deterministic reasons that declare a backlog blockage."""

    active = [item for item in items if item.status not in BLOCKAGE_EXCLUDED_STATUSES]
    blocked = [item for item in active if item.status == "Blocked"]
    causes: dict[str, int] = {}
    for item in blocked:
        cause = item.preventing_cause.strip()
        if cause:
            causes[cause] = causes.get(cause, 0) + 1

    reasons: list[str] = []
    if len(blocked) >= 5:
        reasons.append("five-or-more-blocked")
    if active and len(blocked) == len(active):
        reasons.append("all-active-work-blocked")
    if any(count >= 3 for count in causes.values()):
        reasons.append("shared-blocker")
    if active and minutes_without_progress >= 60:
        reasons.append("no-progress-for-sixty-minutes")
    if user_declared:
        reasons.append("user-declared")
    return tuple(reasons)


def observe_backlog_blockage(
    *,
    active: bool,
    exit_conditions_satisfied: bool,
    state_already_reported: bool,
) -> BlockageObservation:
    """Report active or recovered blockage state without repeating an alert.

    active identifies an existing declared recovery. exit_conditions_satisfied
    indicates that the Coordinator may end recovery. state_already_reported
    suppresses a duplicate active-state alert. The function never mutates the
    observed provider, task, Git, claim, or dispatch state.
    """

    if not active:
        if exit_conditions_satisfied:
            raise ValueError("inactive blockage cannot satisfy recovery exit conditions")
        return BlockageObservation("INACTIVE", False)
    if exit_conditions_satisfied:
        return BlockageObservation("RECOVERY_READY", True)
    if state_already_reported:
        return BlockageObservation("ACTIVE_UNCHANGED", False)
    return BlockageObservation("ACTIVE", True)


class WatchdogCycle:
    """Evaluate source-backed anomalies without changing observed state."""

    def evaluate(self, items: Iterable[WorkItem]) -> CycleResult:
        """Return actionable alerts or one concise healthy-cycle result.

        items contains the current provider and task evidence. The method reads
        each instance, emits no coordination mutations, and returns ALERT when
        at least one anomaly or satisfied exit condition requires parent action.
        """

        observations: list[WatchdogAlert] = []
        blocked_reconciliations: list[BlockedReconciliation] = []
        terminal_reconciliations: list[TerminalReconciliation] = []
        dependency_effects: list[DependencyEffect] = []
        normalized_dependency_view_seen = False
        for item in items:
            normalized_dependency_view_seen = bool(
                normalized_dependency_view_seen or item.effective_status
            )
            if item.effective_status and item.effective_status != item.status:
                dependency_effects.append(
                    DependencyEffect(
                        provider_identity=item.provider_identity,
                        stored_status=item.status,
                        effective_status=item.effective_status,
                        causal_work_item_id=item.causal_work_item_id,
                    )
                )
            envelope_issues: list[str] = []
            if (
                item.effective_status
                and item.effective_status not in _NORMALIZED_EFFECTIVE_STATUSES
            ):
                envelope_issues.append(
                    f"invalid effective status: {item.effective_status}"
                )
            if (
                item.effective_status == "Blocked"
                and item.status != "Blocked"
                and not item.causal_work_item_id.strip()
            ):
                envelope_issues.append("derived Blocked lacks causal Work Item ID")
            if item.causal_work_item_id.strip() and (
                not item.effective_status or item.effective_status == item.status
            ):
                envelope_issues.append("causal Work Item ID on non-derived result")
            if item.dependency_state_issue.strip():
                envelope_issues.append(item.dependency_state_issue)
            if envelope_issues:
                observations.append(
                    WatchdogAlert(
                        provider_identity=item.provider_identity,
                        evidence="; ".join(envelope_issues),
                        reason="normalized dependency envelope is contradictory",
                        recommended_action=(
                            "Coordinator reconciles the series index and normalized "
                            "stored/effective view without changing provider lifecycle"
                        ),
                        preventing_cause="",
                    )
                )
            if item.status in TERMINAL_STATUSES:
                reconciliation = self._reconcile_terminal(item)
                terminal_reconciliations.append(reconciliation)
                if reconciliation.actionable_reasons:
                    actions = "; ".join(reconciliation.actionable_reasons)
                    observations.append(
                        WatchdogAlert(
                            provider_identity=item.provider_identity,
                            evidence=self._terminal_evidence(reconciliation),
                            reason=(
                                "Terminal reconciliation requires Coordinator "
                                f"attention: {actions}"
                            ),
                            recommended_action=(
                                f"Coordinator reconciles task {reconciliation.task_id}: "
                                f"{actions}"
                            ),
                            preventing_cause="",
                        )
                    )
            elif item.status == "Blocked":
                reconciliation = self._reconcile_blocked(item)
                blocked_reconciliations.append(reconciliation)
                if reconciliation.actionable_reasons:
                    reasons = "; ".join(reconciliation.actionable_reasons)
                    exit_only = reconciliation.actionable_reasons == (
                        "dependency or unblock evidence is satisfied",
                    )
                    observations.append(
                        WatchdogAlert(
                            provider_identity=item.provider_identity,
                            evidence=self._blocked_evidence(reconciliation),
                            reason=(
                                "Blocked recovery requires Coordinator attention"
                                if exit_only
                                else f"Blocked reconciliation requires Coordinator attention: {reasons}"
                            ),
                            recommended_action=(
                                "Coordinator validates the complete reconciliation "
                                "evidence and chooses exactly one authorized disposition"
                            ),
                            preventing_cause=item.preventing_cause,
                        )
                    )
            elif (
                item.status in ACTIVE_CAPACITY_STATUSES
                and item.task_state in _TASK_ANOMALY_STATES
            ):
                cause_is_known = self._known_preventing_cause(item)
                provider_boundary = (
                    "provider reservation"
                    if item.status == "Starting"
                    else "provider record"
                )
                reason = (
                    f"{item.status} canonical task {item.task_state}; task-state "
                    "boundary requires Coordinator attention"
                )
                recommended_action = (
                    f"Coordinator reconciles the {item.status} task, "
                    f"{provider_boundary}, and ownership before choosing any "
                    "lifecycle disposition"
                )
                if cause_is_known:
                    reason += " with a known preventing cause"
                    recommended_action = (
                        f"Coordinator reconciles the {item.status} task, "
                        f"{provider_boundary}, and ownership, then validates the "
                        "separate known cause and Coordinator-owned action before "
                        "choosing the Blocked disposition"
                    )
                observations.append(
                    WatchdogAlert(
                        provider_identity=item.provider_identity,
                        evidence=self._stall_evidence(item),
                        reason=reason,
                        recommended_action=recommended_action,
                        preventing_cause=item.preventing_cause,
                    )
                )
            elif item.status == "Running" and self._suspected_stall(item):
                cause_is_known = self._known_preventing_cause(item)
                observations.append(
                    WatchdogAlert(
                        provider_identity=item.provider_identity,
                        evidence=self._stall_evidence(item),
                        reason=(
                            "progress boundary crossed with a known preventing cause"
                            if cause_is_known
                            else "progress boundary crossed while the cause remains unknown"
                        ),
                        recommended_action=(
                            "Coordinator validates the cause, blocker owner, unblock "
                            "condition, and Coordinator-owned action before choosing "
                            "the Blocked disposition"
                            if cause_is_known
                            else "Coordinator investigates and delegates Stalled only if "
                            "the evidence justifies it"
                        ),
                        preventing_cause=item.preventing_cause,
                    )
                )
            elif item.status == "Stalled" and item.stalled_exit_satisfied:
                observations.append(
                    WatchdogAlert(
                        provider_identity=item.provider_identity,
                        evidence="the recorded Stalled exit condition is now satisfied",
                        reason="Stalled disposition requires Coordinator attention",
                        recommended_action=(
                            "Coordinator validates the evidence and chooses one "
                            "authorized Stalled disposition"
                        ),
                        preventing_cause=item.preventing_cause,
                    )
                )
            if (
                item.status not in TERMINAL_STATUSES
                and item.status != "Blocked"
                and self._conversation_title_issue(item)
            ):
                observations.append(
                    WatchdogAlert(
                        provider_identity=item.provider_identity,
                        evidence=(
                            f"conversation_title={item.conversation_title}; "
                            "expected_conversation_title="
                            f"{self._expected_conversation_title(item)}"
                        ),
                        reason="canonical conversation title contradicts current lifecycle or phase",
                        recommended_action=(
                            "Coordinator reconciles the canonical conversation title "
                            "without changing provider lifecycle"
                        ),
                        preventing_cause=item.preventing_cause,
                    )
                )
        if not observations:
            message = "No actionable watchdog condition observed."
            if dependency_effects:
                message = (
                    f"Observed {len(dependency_effects)} derived dependency "
                    "effect(s); no actionable watchdog condition observed."
                )
            elif normalized_dependency_view_seen:
                message = (
                    "Normalized dependency view has no derived effects; no "
                    "actionable watchdog condition observed."
                )
            return CycleResult(
                "NO_ACTION",
                message,
                None,
                tuple(blocked_reconciliations),
                tuple(terminal_reconciliations),
                tuple(dependency_effects),
            )
        return CycleResult(
            "ALERT",
            (
                f"{len(observations)} actionable watchdog condition(s) observed "
                "in one aggregate parent alert."
            ),
            self._aggregate_alert(observations),
            tuple(blocked_reconciliations),
            tuple(terminal_reconciliations),
            tuple(dependency_effects),
        )

    @staticmethod
    def _reconcile_terminal(item: WorkItem) -> TerminalReconciliation:
        """Evaluate every terminal gate while leaving all observed state unchanged."""

        reasons: list[str] = []
        if not item.root_task.strip():
            reasons.append("identify canonical Codex task")
        if not item.provider_terminal_evidence:
            reasons.append("confirm provider terminal evidence")
        if WatchdogCycle._conversation_title_issue(item):
            reasons.append("reconcile canonical conversation title")
        if item.status == "Completed" and not item.code_merged:
            reasons.append("confirm merged delivery")
        if (
            item.claim_applicability not in _CLAIM_APPLICABILITY_VALUES
            or item.claim_applicability == "unknown"
        ):
            reasons.append("determine terminal claim applicability")
        if item.live_claims:
            reasons.append("release live claim")
        elif item.claim_applicability == "applicable" and not item.released_claims:
            reasons.append("reconcile applicable terminal claim")
        claim_reconciliation_complete = bool(
            not item.live_claims
            and (
                item.claim_applicability == "not-applicable"
                or (
                    item.claim_applicability == "applicable"
                    and item.released_claims
                )
            )
        )

        if item.worktree_disposition == "clean-removable":
            reasons.append("remove clean terminal worktree")
        elif item.worktree_disposition not in _SAFE_TERMINAL_WORKTREE_DISPOSITIONS:
            reasons.append("reconcile terminal worktree disposition")

        if item.delivery_branch_disposition not in _SAFE_DELIVERY_BRANCH_DISPOSITIONS:
            reasons.append("reconcile delivery branch disposition")
        if item.cleanup_branch_disposition == "cleanup-eligible":
            reasons.append("clean up terminal branch")
        elif item.cleanup_branch_disposition not in _SAFE_CLEANUP_BRANCH_DISPOSITIONS:
            reasons.append("reconcile cleanup branch disposition")

        preserved = (
            item.source_branch_disposition == "deliberately-preserved"
            and item.source_branch_relation in _PRESERVABLE_SOURCE_BRANCH_RELATIONS
            and bool(item.source_branch_preservation_evidence.strip())
        )
        if item.source_branch_disposition == "cleanup-eligible":
            reasons.append("clean up terminal source branch")
        elif item.source_branch_disposition == "deliberately-preserved":
            if not preserved:
                reasons.append("reconcile unsupported source-branch preservation")
            elif (
                item.source_branch_preservation_evidence
                != item.acknowledged_source_branch_preservation_evidence
            ):
                reasons.append(
                    "acknowledge changed source-branch preservation evidence"
                )
        elif item.source_branch_disposition not in _SAFE_SOURCE_BRANCH_DISPOSITIONS:
            reasons.append("reconcile terminal source branch disposition")

        if item.notification_pending:
            reasons.append("resolve terminal notification")

        archive_pause_valid = WatchdogCycle._archive_pause_valid(item)
        if not reasons and not item.codex_archived and not archive_pause_valid:
            reasons.append("archive Codex task")

        return TerminalReconciliation(
            provider_identity=item.provider_identity,
            task_id=item.root_task,
            lifecycle_status=item.status,
            conversation_title=item.conversation_title,
            expected_conversation_title=(
                WatchdogCycle._expected_conversation_title(item)
            ),
            provider_terminal_evidence=item.provider_terminal_evidence,
            code_merged=item.code_merged,
            claim_applicability=item.claim_applicability,
            claim_reconciliation_complete=claim_reconciliation_complete,
            live_claims=tuple(item.live_claims),
            released_claims=tuple(item.released_claims),
            worktree=item.worktree,
            worktree_disposition=item.worktree_disposition,
            delivery_branch=item.delivery_branch,
            delivery_branch_disposition=item.delivery_branch_disposition,
            cleanup_branch=item.cleanup_branch,
            cleanup_branch_disposition=item.cleanup_branch_disposition,
            source_branch=item.source_branch,
            source_branch_relation=item.source_branch_relation,
            source_branch_disposition=item.source_branch_disposition,
            source_branch_preservation_evidence=(
                item.source_branch_preservation_evidence
            ),
            acknowledged_source_branch_preservation_evidence=(
                item.acknowledged_source_branch_preservation_evidence
            ),
            source_branch_deliberately_preserved=preserved,
            notification_pending=item.notification_pending,
            codex_archived=item.codex_archived,
            archive_pause=item.archive_pause,
            archive_pause_valid=archive_pause_valid,
            actionable_reasons=tuple(reasons),
        )

    @staticmethod
    def _archive_pause_valid(item: WorkItem) -> bool:
        """Accept only current, acknowledged user direction for this named task."""

        pause = item.archive_pause
        return bool(
            pause
            and pause.source == "current-user-direction"
            and pause.scope == "codex-task-archival"
            and item.root_task
            and item.root_task in pause.task_ids
            and pause.evidence.strip()
            and pause.acknowledged
        )

    @staticmethod
    def _terminal_evidence(reconciliation: TerminalReconciliation) -> str:
        """Render every observed terminal dimension for one campaign task."""

        return "; ".join(
            (
                f"task={reconciliation.task_id or 'missing'}",
                f"provider={reconciliation.provider_identity}",
                f"lifecycle_status={reconciliation.lifecycle_status}",
                f"conversation_title={reconciliation.conversation_title or 'missing'}",
                "expected_conversation_title="
                f"{reconciliation.expected_conversation_title or 'missing'}",
                "provider_terminal_evidence="
                f"{str(reconciliation.provider_terminal_evidence).lower()}",
                f"code_merged={str(reconciliation.code_merged).lower()}",
                f"claim_applicability={reconciliation.claim_applicability}",
                "claim_reconciliation_complete="
                f"{str(reconciliation.claim_reconciliation_complete).lower()}",
                f"live_claims={reconciliation.live_claims or ('none',)}",
                f"released_claims={reconciliation.released_claims or ('none',)}",
                f"worktree={reconciliation.worktree or 'none'}",
                f"worktree_disposition={reconciliation.worktree_disposition or 'missing'}",
                f"delivery_branch={reconciliation.delivery_branch or 'none'}",
                "delivery_branch_disposition="
                f"{reconciliation.delivery_branch_disposition or 'missing'}",
                f"cleanup_branch={reconciliation.cleanup_branch or 'none'}",
                "cleanup_branch_disposition="
                f"{reconciliation.cleanup_branch_disposition or 'missing'}",
                f"source_branch={reconciliation.source_branch or 'none'}",
                f"source_branch_relation={reconciliation.source_branch_relation or 'none'}",
                "source_branch_disposition="
                f"{reconciliation.source_branch_disposition or 'missing'}",
                "source_branch_preservation_evidence="
                f"{reconciliation.source_branch_preservation_evidence or 'none'}",
                "acknowledged_source_branch_preservation_evidence="
                f"{reconciliation.acknowledged_source_branch_preservation_evidence or 'none'}",
                "source_branch_deliberately_preserved="
                f"{str(reconciliation.source_branch_deliberately_preserved).lower()}",
                "notification_pending="
                f"{str(reconciliation.notification_pending).lower()}",
                f"codex_archived={str(reconciliation.codex_archived).lower()}",
                f"archive_pause={reconciliation.archive_pause or 'none'}",
                "archive_pause_valid="
                f"{str(reconciliation.archive_pause_valid).lower()}",
            )
        )

    @staticmethod
    def _reconcile_blocked(item: WorkItem) -> BlockedReconciliation:
        """Compare all required Blocked evidence and retain actionable reasons."""

        reasons: list[str] = []
        if item.blocker_exit_satisfied or item.dependency_or_unblock_satisfied:
            reasons.append("dependency or unblock evidence is satisfied")
        if WatchdogCycle._conversation_title_issue(item):
            reasons.append("reconcile canonical conversation title")
        recovery_is_actively_owned = bool(
            item.agent_actionable_recovery.strip()
            and item.active_recovery_owner.strip()
            and item.recovery_acknowledged
            and item.task_state in _ACTIVE_TASK_STATES
        )
        if item.agent_actionable_recovery.strip() and not recovery_is_actively_owned:
            reasons.append("agent-actionable recovery is available")
        if item.preservation_evidence_issue.strip():
            reasons.append("preservation evidence contradicts Git or runtime state")
        disposition_issue = WatchdogCycle._disposition_issue(item)
        if disposition_issue:
            reasons.append(disposition_issue)
        if item.lifecycle_evidence_issue.strip():
            reasons.append("lifecycle evidence is stale or contradictory")
        if not item.next_action_owner_correct:
            reasons.append("next-action owner is incorrect")
        missing_evidence = tuple(
            name
            for name, value in (
                ("blocker", item.preventing_cause),
                ("blocker owner", item.blocker_owner),
                ("unblock condition", item.unblock_condition),
                ("next-action owner", item.next_action_owner),
                ("Git state", item.git_state),
            )
            if not value.strip()
        )
        if missing_evidence:
            reasons.append(
                "Blocked evidence is incomplete: " + ", ".join(missing_evidence)
            )
        return BlockedReconciliation(
            provider_identity=item.provider_identity,
            exact_blocker=item.preventing_cause,
            blocker_owner=item.blocker_owner,
            unblock_condition=item.unblock_condition,
            next_action_owner=item.next_action_owner,
            dependencies=tuple(item.dependencies),
            dependency_evidence=tuple(item.dependency_evidence),
            candidate_evidence=tuple(item.candidate_evidence),
            review_verification_evidence=tuple(
                item.review_verification_evidence
            ),
            canonical_task_state=item.task_state,
            conversation_title=item.conversation_title,
            expected_conversation_title=(
                WatchdogCycle._expected_conversation_title(item)
            ),
            git_state=item.git_state,
            live_claims=tuple(item.live_claims),
            correction_attempt_history=tuple(item.correction_attempt_history),
            current_disposition=item.current_disposition,
            actionable_reasons=tuple(reasons),
        )

    @staticmethod
    def _conversation_title_issue(item: WorkItem) -> bool:
        """Return title drift against the expectation derived from current state."""

        expected = WatchdogCycle._expected_conversation_title(item)
        return bool(expected and item.conversation_title != expected)

    @staticmethod
    def _expected_conversation_title(item: WorkItem) -> str:
        """Derive display state from provider lifecycle or bounded task outcome."""

        if not item.short_title.strip():
            return ""
        if (
            item.runtime_task_kind == "bounded-verifier"
            and item.task_state == "completed"
        ):
            return f"Done — {item.short_title}"
        if item.status == "Running":
            label = item.phase if item.phase in _RUNNING_TITLE_PHASES else ""
        else:
            label = _LIFECYCLE_TITLE_LABELS.get(item.status, "")
        return f"{label} — {item.short_title}" if label else ""

    @staticmethod
    def _disposition_issue(item: WorkItem) -> str:
        """Return why a current Blocked disposition needs Coordinator attention."""

        receipt = item.current_disposition
        if receipt is None:
            return (
                "correction attempts exhausted without current disposition"
                if item.correction_attempts_exhausted
                else ""
            )
        if not isinstance(receipt, DispositionReceipt):
            return "current disposition receipt is malformed"
        if (
            receipt.outcome != "CONTINUING_BLOCKED"
            or receipt.state != "APPLIED"
            or not receipt.owner.strip()
            or not receipt.evidence.strip()
            or not receipt.observable_trigger.strip()
            or not receipt.unresolved_findings
        ):
            return "current disposition receipt is missing, vague, expired, or inconsistent"
        return ""

    @staticmethod
    def _blocked_evidence(reconciliation: BlockedReconciliation) -> str:
        """Render one concise complete Blocked reconciliation for an alert."""

        return "; ".join(
            (
                f"blocker={reconciliation.exact_blocker or 'missing'}",
                f"blocker_owner={reconciliation.blocker_owner or 'missing'}",
                f"unblock_condition={reconciliation.unblock_condition or 'missing'}",
                f"next_action_owner={reconciliation.next_action_owner or 'missing'}",
                f"dependencies={reconciliation.dependencies or ('none',)}",
                f"dependency_evidence={reconciliation.dependency_evidence or ('none',)}",
                f"candidate_evidence={reconciliation.candidate_evidence or ('none',)}",
                "review_verification_evidence="
                f"{reconciliation.review_verification_evidence or ('none',)}",
                f"canonical_task_state={reconciliation.canonical_task_state}",
                f"conversation_title={reconciliation.conversation_title or 'missing'}",
                "expected_conversation_title="
                f"{reconciliation.expected_conversation_title or 'missing'}",
                f"git_state={reconciliation.git_state or 'missing'}",
                f"live_claims={reconciliation.live_claims or ('none',)}",
                "correction_attempt_history="
                f"{reconciliation.correction_attempt_history or ('none',)}",
                f"current_disposition={reconciliation.current_disposition or 'none'}",
            )
        )

    @staticmethod
    def _suspected_stall(item: WorkItem) -> bool:
        return (
            item.estimate_boundary_crossed
            or item.hard_stop_crossed
            or item.progress_gap
        )

    @staticmethod
    def _known_preventing_cause(item: WorkItem) -> bool:
        return bool(item.preventing_cause.strip())

    @staticmethod
    def _aggregate_alert(observations: list[WatchdogAlert]) -> WatchdogAlert:
        """Combine all actionable observations into exactly one parent alert."""

        def combine(field: str) -> str:
            values = [getattr(observation, field) for observation in observations]
            values = [value for value in values if value]
            return " | ".join(values)

        return WatchdogAlert(
            provider_identity=combine("provider_identity"),
            evidence=combine("evidence"),
            reason=combine("reason"),
            recommended_action=combine("recommended_action"),
            preventing_cause=" | ".join(
                cause
                for observation in observations
                if (cause := observation.preventing_cause.strip())
            ),
        )

    @staticmethod
    def _stall_evidence(item: WorkItem) -> str:
        evidence = [
            f"phase={item.phase or 'unknown'}",
            f"last_productive_evidence={item.last_productive_evidence or 'missing'}",
            f"canonical_thread={item.canonical_thread or 'missing'}",
            f"root_task={item.root_task or 'missing'}",
        ]
        if item.estimate_boundary_crossed:
            evidence.extend(
                (
                    "estimate_boundary_crossed=true",
                    f"phase_estimate={item.phase_estimate or 'missing'}",
                )
            )
        if item.hard_stop_crossed:
            evidence.extend(
                (
                    "hard_stop_crossed=true",
                    f"hard_stop={item.hard_stop or 'missing'}",
                )
            )
        if item.progress_gap:
            evidence.extend(
                (
                    "progress_gap=true",
                    f"progress_observation={item.progress_observation or 'missing'}",
                )
            )
        if item.task_state in _TASK_ANOMALY_STATES:
            evidence.extend(
                (
                    "task_boundary_crossed=true",
                    f"task_state={item.task_state}",
                )
            )
        return "; ".join(evidence)


class CoordinatorDisposition:
    """Choose one authorized Stalled exit from mutually exclusive evidence."""

    def choose(
        self,
        *,
        same_owner_resumed: bool = False,
        ownership_ended: bool = False,
        blocker_cause: str = "",
        blocker_owner: str = "",
        unblock_condition: str = "",
        coordinator_action: str = "",
        user_owned_action: str = "",
        user_question: str = "",
        unattended_work_boundary: str = "",
        terminal_status: str = "",
        terminal_evidence: bool = False,
        active_capacity_count: int = 0,
    ) -> str:
        """Return the one lifecycle state supported by the supplied evidence.

        Boolean inputs identify the mutually exclusive safe-resumption and
        redispatch boundaries. Blocked requires its exact cause, owner, unblock
        condition, and Coordinator action. User Action Required requires its
        exact user-owned action, question, and unattended-work boundary.
        terminal_status may be Completed, Failed, or Abandoned only with
        terminal_evidence. A direct resumption also needs an available
        Starting-plus-Running slot. Missing or conflicting evidence raises
        ValueError so no default lifecycle mutation can be inferred.
        """

        if terminal_status and terminal_status not in TERMINAL_STATUSES:
            raise ValueError(f"invalid terminal Stalled disposition: {terminal_status}")
        if terminal_status and not terminal_evidence:
            raise ValueError("terminal Stalled disposition requires terminal evidence")
        if same_owner_resumed and active_capacity_count >= ACTIVE_CAPACITY_LIMIT:
            raise ValueError(
                "Stalled -> Running requires an available active-capacity slot"
            )
        blocker_evidence = (
            blocker_cause,
            blocker_owner,
            unblock_condition,
            coordinator_action,
        )
        blocker_fields_present = tuple(
            bool(value.strip()) for value in blocker_evidence
        )
        if any(blocker_fields_present) and not all(blocker_fields_present):
            raise ValueError(
                "Blocked disposition requires exact cause, blocker owner, "
                "unblock condition, and Coordinator action"
            )
        user_action_evidence = (
            user_owned_action,
            user_question,
            unattended_work_boundary,
        )
        user_action_fields_present = tuple(
            bool(value.strip()) for value in user_action_evidence
        )
        if any(user_action_fields_present) and not all(user_action_fields_present):
            raise ValueError(
                "User Action Required disposition requires exact user-owned "
                "action, question, and unattended-work boundary"
            )
        choices = [
            ("Running", same_owner_resumed),
            ("Ready", ownership_ended),
            ("Blocked", all(blocker_fields_present)),
            ("User Action Required", all(user_action_fields_present)),
            (terminal_status, bool(terminal_status and terminal_evidence)),
        ]
        selected = [status for status, enabled in choices if enabled]
        if len(selected) != 1:
            raise ValueError("no evidence-backed Stalled disposition")
        return selected[0]


def active_capacity(items: Iterable[WorkItem]) -> int:
    """Count only Starting and Running items against active capacity."""

    return sum(item.status in ACTIVE_CAPACITY_STATUSES for item in items)


def series_state(statuses: Iterable[str]) -> str:
    """Derive series state from required children without collapsing mixed pauses."""

    materialized = list(statuses)
    if not materialized:
        raise ValueError("series requires at least one child state")
    if any(status == "Failed" for status in materialized):
        return "failed"
    nonterminal = [
        status
        for status in materialized
        if status not in {"Completed", "Abandoned"}
    ]
    if not nonterminal:
        return "completed"
    if any(status in ACTIVE_SERIES_STATUSES for status in nonterminal):
        return "active"
    if all(status == "Stalled" for status in nonterminal):
        return "stalled"
    if all(status == "Blocked" for status in nonterminal):
        return "blocked"
    return "mixed:" + ",".join(sorted(set(nonterminal)))


def terminal_archive_destination(
    item_type: str,
    status: str,
    terminal_evidence: bool,
) -> str:
    """Return the typed terminal archive after validating terminal evidence."""

    if status == "Stalled":
        raise ValueError("Stalled is nonterminal and cannot be archived directly")
    if status not in TERMINAL_STATUSES or not terminal_evidence:
        raise ValueError("terminal archive requires a terminal status and evidence")
    type_folder = {
        "Defect": "defects",
        "Feature": "features",
        "Analysis": "analyses",
        "Investigation": "investigations",
    }.get(item_type)
    if not type_folder:
        raise ValueError(f"unsupported work-item type: {item_type}")
    archive = "completed-backlog" if status == "Completed" else "failed-backlog"
    return f"backlog/{archive}/{type_folder}"
