#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Simulates read-only watchdog observations and retained Blocked reconciliation evidence.
# Governing design: design/orchestrated-development-lifecycle.html
# Governing test plan: evals/agent-tests/dev-backlog-watchdog/requirements-matrix.md

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


ACTIVE_CAPACITY_STATUSES = {"Starting", "Running"}
ACTIVE_CAPACITY_LIMIT = 10
ACTIVE_SERIES_STATUSES = {"Ready", "Starting", "Running", "Awaiting Review"}
TERMINAL_STATUSES = {"Completed", "Failed", "Abandoned"}
CRISIS_EXCLUDED_STATUSES = {
    "User Action Required",
    "Holding",
    "Future Idea",
    *TERMINAL_STATUSES,
}
_TASK_ANOMALY_STATES = {"failed", "stopped", "missing"}


@dataclass(frozen=True)
class DispositionReceipt:
    """Describe a structured disposition already recorded for a Blocked item."""

    outcome: str
    state: str
    owner: str
    evidence: str
    observable_trigger: str
    unresolved_findings: tuple[str, ...] = ()


@dataclass
class WorkItem:
    """Represent the evidence visible to one deterministic watchdog cycle.

    provider_identity is the selected provider reference or provider-none task.
    status is the current lifecycle state. The remaining fields describe
    observable progress, canonical execution identity, and exit-condition
    evidence. Instances are read by WatchdogCycle and are never mutated.
    """

    provider_identity: str
    status: str
    phase: str = ""
    canonical_thread: str = ""
    root_task: str = ""
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
    correction_attempts_exhausted: bool = False
    correction_attempt_history: tuple[str, ...] = ()
    current_disposition: DispositionReceipt | None = None
    lifecycle_evidence_issue: str = ""
    next_action_owner_correct: bool = True
    stalled_exit_satisfied: bool = False
    blocker_exit_satisfied: bool = False


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
    git_state: str
    live_claims: tuple[str, ...]
    correction_attempt_history: tuple[str, ...]
    current_disposition: DispositionReceipt | None
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
class CycleResult:
    """Return retained Blocked results plus one no-action or aggregate alert outcome."""

    status: str
    message: str
    alert: WatchdogAlert | None
    blocked_reconciliations: tuple[BlockedReconciliation, ...] = ()
    mutated: bool = False


def backlog_crisis_reasons(
    items: Iterable[WorkItem],
    *,
    minutes_without_progress: int = 0,
    user_declared: bool = False,
) -> tuple[str, ...]:
    """Return the deterministic reasons that require backlog crisis mode."""

    active = [item for item in items if item.status not in CRISIS_EXCLUDED_STATUSES]
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
        for item in items:
            if item.status == "Blocked":
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
        if not observations:
            return CycleResult(
                "NO_ACTION",
                "No actionable watchdog condition observed.",
                None,
                tuple(blocked_reconciliations),
            )
        return CycleResult(
            "ALERT",
            (
                f"{len(observations)} actionable watchdog condition(s) observed "
                "in one aggregate parent alert."
            ),
            self._aggregate_alert(observations),
            tuple(blocked_reconciliations),
        )

    @staticmethod
    def _reconcile_blocked(item: WorkItem) -> BlockedReconciliation:
        """Compare all required Blocked evidence and retain actionable reasons."""

        reasons: list[str] = []
        if item.blocker_exit_satisfied or item.dependency_or_unblock_satisfied:
            reasons.append("dependency or unblock evidence is satisfied")
        if item.agent_actionable_recovery.strip():
            reasons.append("agent-actionable recovery is available")
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
            git_state=item.git_state,
            live_claims=tuple(item.live_claims),
            correction_attempt_history=tuple(item.correction_attempt_history),
            current_disposition=item.current_disposition,
            actionable_reasons=tuple(reasons),
        )

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
