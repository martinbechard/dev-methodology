# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Simulates provider-selected capacity, blocked dispositions, claims, and terminal cleanup.
# Governing design: design/orchestrated-development-lifecycle.html
# Test plan: evals/agent-tests/dev-backlog-coordinator/requirements-matrix.md

"""Provide deterministic state transitions for parent backlog coordination."""

from __future__ import annotations

import re
from dataclasses import dataclass, field, replace
from datetime import datetime
from typing import Sequence


RUNNING_TARGET = 10
CLAIM_KINDS = ("integration", "completion")
CLAIM_ATTEMPT_OUTCOMES = frozenset(
    {"ACQUIRED", "CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED"}
)
RELEASE_OR_RECOVERY_NOTIFICATION = re.compile(
    r"(?:release|recovery):[A-Za-z0-9][A-Za-z0-9._/-]*"
)
SHARED_CLAIM_OPERATIONS = frozenset(
    {
        "primary main integration",
        "existing backlog update",
        "shared browser",
        "shared database",
        "shared port",
        "shared live model",
        "shared install",
        "shared deployment",
    }
)
PERSISTENCE_MANAGERS = {
    "file": "manage-file-work-items",
    "github": "manage-github-work-items",
    "gitlab": "manage-gitlab-work-items",
    "azure-devops": "manage-azure-devops-work-items",
    "jira": "manage-jira-work-items",
}
PLACEHOLDER_PROVIDERS = frozenset({"azure-devops", "jira"})


@dataclass
class WorkItem:
    """Represent execution fields returned by a selected provider manager.

    Example:
        item = WorkItem("feature-a", "Ready")
        assert item.canonical_task_id is None
    """

    item_id: str
    status: str
    canonical_task_id: str | None = None
    canonical_thread_id: str | None = None
    provider: str = "file"
    dirty_owner_task_id: str | None = None
    delivery_accepted: bool = False
    phase: str | None = None
    branch: str | None = None
    worktree: str | None = None
    candidate_commit: str | None = None
    git_state: str = ""
    review_verification_evidence: tuple[str, ...] = ()
    live_claims: tuple[str, ...] = ()
    correction_attempt_history: list[str] = field(default_factory=list)
    blocked_disposition: BlockedDisposition | None = None
    disposition_history: list[BlockedDisposition] = field(default_factory=list)
    bounded_retry_used: bool = False
    claim_attempts: dict[str, list[dict[str, object]]] = field(default_factory=dict)
    acquired_claims: set[str] = field(default_factory=set)
    open_issues: list[str] = field(default_factory=list)


@dataclass
class TaskCandidate:
    """Represent one task candidate during ambiguous-dispatch reconciliation.

    Example:
        candidate = TaskCandidate("task-1", "parent", "provider:a", "a", datetime.now())
        assert not candidate.archived
    """

    task_id: str
    parent_task_id: str
    provider_reference: str
    normalized_objective: str
    created_at: datetime
    repository_mutation_count: int = 0
    status: str = "running"
    archived: bool = False
    containment_transitions: list[str] = field(default_factory=list)

    def contain_duplicate(self) -> None:
        """Stop and archive a duplicate only after proving zero mutation."""

        self.status = "stopped"
        self.containment_transitions.append("stopped")
        if self.repository_mutation_count:
            raise ValueError("a duplicate with repository mutations requires preservation")
        self.containment_transitions.append("zero mutation verified")
        self.archived = True
        self.containment_transitions.append("archived")


@dataclass(frozen=True)
class DispatchReconciliation:
    """Return one canonical task and every safely contained duplicate."""

    canonical_task_id: str
    contained_duplicates: tuple[TaskCandidate, ...]
    retry_count: int


@dataclass(frozen=True)
class BlockedDisposition:
    """Record one immutable Coordinator outcome after corrections are exhausted.

    Exactly one outcome family carries content. The unresolved findings and all
    outcome-specific evidence remain available across later resumption.
    """

    outcome: str
    unresolved_findings: tuple[str, ...]
    state: str = "PROPOSED"
    recovery_action: str = ""
    recovery_owner: str = ""
    recovery_evidence: str = ""
    recovery_findings: tuple[str, ...] = ()
    retry_plan: str = ""
    retry_evidence: str = ""
    retry_findings: tuple[str, ...] = ()
    retry_limit: int = 0
    user_explanation: str = ""
    user_owned_decision: str = ""
    user_question: str = ""
    user_options: tuple[str, ...] = ()
    user_tradeoffs: tuple[str, ...] = ()
    unattended_work_boundary: str = ""
    dependency_kind: str = ""
    dependency: str = ""
    dependency_owner: str = ""
    observable_trigger: str = ""


@dataclass(frozen=True)
class PersistenceRoute:
    """Describe the observable result of resolving one Persistence selector."""

    provider: str
    management_skill: str | None
    durable_inventory: bool
    status: str
    zero_mutation: bool
    user_question: str | None = None


@dataclass(frozen=True)
class DeliveryEvidence:
    """Represent a completed work item that is eligible for parent cleanup.

    Example:
        evidence = DeliveryEvidence(
            "abc", True, "integration", "release-a", "def", "completion",
            "release-b", True, True
        )
        assert evidence.completion_ready
    """

    integration_commit: str | None
    focused_tests_passed: bool
    integration_claim_id: str | None
    integration_release_event: str | None
    completion_commit: str | None
    completion_claim_id: str | None
    completion_release_event: str | None
    worktree_clean: bool
    branch_fully_merged: bool

    @property
    def completion_ready(self) -> bool:
        """Return whether work-item completion can precede parent cleanup."""

        return bool(
            self.integration_commit
            and self.focused_tests_passed
            and self.integration_claim_id
            and self.integration_release_event
            and self.completion_commit
            and self.completion_claim_id
            and self.completion_release_event
            and self.integration_claim_id != self.completion_claim_id
            and self.worktree_clean
            and self.branch_fully_merged
        )


@dataclass(frozen=True)
class TaskCleanupEvidence:
    """Represent parent cleanup after the work-item completion commit."""

    delivery: DeliveryEvidence
    worktree_removed: bool
    merged_branch_deleted: bool

    @property
    def complete(self) -> bool:
        """Return whether the parent may title Done and archive the task."""

        return bool(
            self.delivery.completion_ready
            and self.worktree_removed
            and self.merged_branch_deleted
        )


class CoordinationSimulator:
    """Simulate observable parent scheduling and recovery decisions."""

    def __init__(self, items: Sequence[WorkItem]) -> None:
        """Initialize from provider-returned work items without a second registry."""

        self.items = list(items)
        self.events: list[dict[str, object]] = []

    def running_count(self) -> int:
        """Count only provider-returned Running work items."""

        return sum(item.status == "Running" for item in self.items)

    def dispatch_to_target(self) -> tuple[str, ...]:
        """Promote eligible Ready items until ten items are Running."""

        vacancies = max(0, RUNNING_TARGET - self.running_count())
        started: list[str] = []
        for item in self.items:
            if not vacancies:
                break
            if item.status != "Ready":
                continue
            item.status = "Running"
            item.phase = "Implementation"
            item.canonical_task_id = f"task-{item.item_id}"
            started.append(item.item_id)
            vacancies -= 1
        self.events.append(
            {
                "event": "capacity-restored",
                "started": tuple(started),
                "running": self.running_count(),
            }
        )
        return tuple(started)

    def resume_user_action_thread(
        self,
        item_id: str,
        *,
        user_answer: str,
        canonical_task_id: str,
        canonical_thread_id: str,
        selected_skill_available: bool | None,
        priority_eligible: bool,
        capacity_available: bool | None,
        root_accepts: bool,
        preserved_artifacts: Sequence[str] = (),
    ) -> tuple[str, ...]:
        """Resume one answered item through its recorded identity and dispatch gates."""

        item = self._item(item_id)
        if item.status != "User Action Required":
            raise ValueError("only a User Action Required item may use this resumption")
        if not user_answer.strip():
            raise ValueError("same-thread resumption requires an explicit user answer")
        if item.canonical_task_id is None or item.canonical_thread_id is None:
            raise ValueError("same-thread resumption requires recorded canonical identities")
        if item.canonical_task_id != canonical_task_id:
            raise ValueError("same-thread resumption cannot replace the canonical task")
        if item.canonical_thread_id != canonical_thread_id:
            raise ValueError("same-thread resumption cannot replace the canonical Thread")
        if item.provider not in {*PERSISTENCE_MANAGERS, "none"}:
            raise ValueError(f"unsupported provider: {item.provider}")
        if item.provider in PLACEHOLDER_PROVIDERS:
            raise ValueError("placeholder provider remains BLOCKED with zero mutation")
        if item.provider == "none" and selected_skill_available is not None:
            raise ValueError("provider none has no selected management skill")
        if item.provider != "none" and selected_skill_available is not True:
            raise ValueError("selected provider manager is unavailable with zero mutation")
        if item.provider == "none" and capacity_available is not None:
            raise ValueError("provider none must not supply or infer capacity")
        if item.provider != "none" and capacity_available is None:
            raise ValueError("selected-provider dispatch requires current capacity evidence")

        statuses = ["User Action Required"]
        self.events.append(
            {
                "event": "user-answer-recorded",
                "item": item_id,
                "task": canonical_task_id,
                "thread": canonical_thread_id,
                "answer": user_answer,
                "evidence": "task-local" if item.provider == "none" else "provider",
            }
        )
        transitions = [("Ready", "dev-backlog-coordinator")]
        ownership_reconciled = item.dirty_owner_task_id in {None, canonical_task_id}
        if priority_eligible and ownership_reconciled and (
            item.provider == "none" or capacity_available is True
        ):
            transitions.append(("Starting", "dev-backlog-coordinator"))
            if root_accepts:
                transitions.append(("Running", "dev-orchestrator"))

        for status, decision_owner in transitions:
            item.status = status
            statuses.append(status)
            self.events.append(
                {
                    "event": "lifecycle-transition",
                    "item": item_id,
                    "task": canonical_task_id,
                    "thread": canonical_thread_id,
                    "status": status,
                    "decisionOwner": decision_owner,
                    "mutationAgent": (
                        None
                        if item.provider == "none"
                        else "dev-backlog-steward"
                    ),
                    "evidence": (
                        "task-local"
                        if item.provider == "none"
                        else "selected-provider"
                    ),
                    "capacityInferred": False if item.provider == "none" else None,
                }
            )

        if item.status == "Running":
            item.phase = "Reconciliation" if preserved_artifacts else "Implementation"
        if preserved_artifacts:
            item.open_issues.append(
                "Preserved out-of-sequence evidence requires ownership, scope, "
                "review, verification, and delivery reconciliation."
            )
            self.events.append(
                {
                    "event": "out-of-sequence-evidence-preserved",
                    "item": item_id,
                    "task": canonical_task_id,
                    "thread": canonical_thread_id,
                    "artifacts": tuple(preserved_artifacts),
                    "dirtyOwnerTask": item.dirty_owner_task_id,
                    "deliveryAccepted": item.delivery_accepted,
                }
            )
        if not ownership_reconciled:
            item.open_issues.append(
                "Dirty ownership belongs to another task and must be handed off "
                "without release or override before dispatch."
            )
        return tuple(statuses)

    @staticmethod
    def persistence_route(
        provider: str,
        *,
        selected_skill_available: bool = True,
        file_provider_available: bool = True,
    ) -> PersistenceRoute:
        """Resolve provider inventory without inferring or falling back to another provider."""

        normalized = provider.strip().lower()
        if normalized == "none":
            return PersistenceRoute(normalized, None, False, "READY", True)
        if normalized == "unset":
            if file_provider_available:
                return PersistenceRoute(
                    normalized,
                    None,
                    False,
                    "USER_ACTION_REQUIRED",
                    True,
                    "Do you want to use the available file-backed work-item provider?",
                )
            return PersistenceRoute(normalized, None, False, "BLOCKED", True)
        if normalized not in PERSISTENCE_MANAGERS:
            raise ValueError(f"unsupported provider: {provider}")
        management_skill = PERSISTENCE_MANAGERS[normalized]
        if not selected_skill_available or normalized in PLACEHOLDER_PROVIDERS:
            return PersistenceRoute(
                normalized,
                management_skill,
                False,
                "BLOCKED",
                True,
            )
        return PersistenceRoute(normalized, management_skill, True, "READY", False)

    def record_claim_attempt(
        self,
        item_id: str,
        *,
        claim_kind: str,
        outcome: str,
        blocking_claim_id: str | None = None,
        release_or_recovery_notification: str | None = None,
    ) -> None:
        """Record an immediate claim attempt or a notification-triggered retry."""

        if claim_kind not in CLAIM_KINDS:
            raise ValueError(f"unsupported claim kind: {claim_kind}")
        if outcome not in CLAIM_ATTEMPT_OUTCOMES:
            raise ValueError(f"unsupported claim attempt outcome: {outcome}")
        item = self._item(item_id)
        if item.status != "Running":
            raise ValueError("only a Running work item may attempt an Event Contract claim")
        if claim_kind in item.acquired_claims:
            raise ValueError(f"{claim_kind} claim is already acquired")
        attempts = item.claim_attempts.setdefault(claim_kind, [])
        if not attempts and release_or_recovery_notification:
            raise ValueError("the immediate attempt cannot consume a release notification")
        if attempts and not release_or_recovery_notification:
            raise ValueError(
                f"{claim_kind} claim retry requires a release or recovery notification"
            )
        if (
            release_or_recovery_notification is not None
            and RELEASE_OR_RECOVERY_NOTIFICATION.fullmatch(
                release_or_recovery_notification
            )
            is None
        ):
            raise ValueError(
                "claim retry notification must be a direct release or recovery notification"
            )
        used_notifications = {
            attempt["releaseOrRecoveryNotification"]
            for attempt in attempts
            if attempt["releaseOrRecoveryNotification"]
        }
        if release_or_recovery_notification in used_notifications:
            raise ValueError("one release or recovery notification may trigger only one retry")
        phase_name = "Integration" if claim_kind == "integration" else "Completion"
        item.phase = phase_name if outcome == "ACQUIRED" else f"{phase_name} Wait"
        attempts.append(
            {
                "claimKind": claim_kind,
                "outcome": outcome,
                "blockingClaimId": blocking_claim_id,
                "releaseOrRecoveryNotification": release_or_recovery_notification,
            }
        )
        if outcome == "ACQUIRED":
            item.acquired_claims.add(claim_kind)
        else:
            item.open_issues.append(
                (
                    f"{claim_kind} claim remained unavailable after "
                    f"{release_or_recovery_notification}: "
                    if release_or_recovery_notification
                    else f"{claim_kind} claim awaits a direct release or recovery notification: "
                )
                + f"{blocking_claim_id or 'unknown owner'}"
            )
            if release_or_recovery_notification:
                item.phase = f"{phase_name} Recovery"

    def claims_requiring_recovery(self) -> tuple[str, ...]:
        """Return Running work items whose notified retry still conflicts."""

        return tuple(
            item.item_id
            for item in self.items
            if item.status == "Running"
            and item.phase in {"Integration Recovery", "Completion Recovery"}
        )

    def dispose_unresolved_claim(self, item_id: str, *, user_decision: bool) -> None:
        """Free one active slot after a notified recovery remains unresolved."""

        item = self._item(item_id)
        if item.phase not in {"Integration Recovery", "Completion Recovery"}:
            raise ValueError("a notified release or recovery attempt must remain unresolved")
        item.status = "User Action Required" if user_decision else "Blocked"
        item.phase = None
        self.events.append(
            {"event": "wait-disposed", "item": item_id, "status": item.status}
        )

    def record_exhausted_correction_disposition(
        self,
        item_id: str,
        *,
        unresolved_findings: Sequence[str],
        recovery_action: str = "",
        recovery_owner: str = "",
        recovery_evidence: str = "",
        recovery_findings: Sequence[str] = (),
        retry_plan: str = "",
        retry_evidence: str = "",
        retry_findings: Sequence[str] = (),
        retry_limit: int = 0,
        user_explanation: str = "",
        user_owned_decision: str = "",
        user_question: str = "",
        user_options: Sequence[str] = (),
        user_tradeoffs: Sequence[str] = (),
        unattended_work_boundary: str = "",
        dependency_kind: str = "",
        dependency: str = "",
        dependency_owner: str = "",
        observable_trigger: str = "",
    ) -> BlockedDisposition:
        """Return one immutable Coordinator decision after corrections are exhausted.

        The Coordinator does not mutate provider state. A separate Steward-model
        operation applies the returned decision.
        """

        item = self._item(item_id)
        if item.status != "Blocked":
            raise ValueError("exhausted correction disposition requires Blocked")
        if item.blocked_disposition is not None:
            raise ValueError("Blocked item already has an active disposition")
        findings = tuple(finding.strip() for finding in unresolved_findings if finding.strip())
        if not findings:
            raise ValueError("disposition requires specific unresolved findings")
        if len(item.correction_attempt_history) < 2:
            raise ValueError("disposition requires retained exhausted correction history")

        recovery_links = tuple(
            finding.strip() for finding in recovery_findings if finding.strip()
        )
        retry_links = tuple(
            finding.strip() for finding in retry_findings if finding.strip()
        )
        recovery_selected = bool(
            recovery_action.strip()
            or recovery_owner.strip()
            or recovery_evidence.strip()
            or recovery_links
        )
        retry_selected = bool(
            retry_plan.strip()
            or retry_evidence.strip()
            or retry_links
            or retry_limit
        )
        user_selected = bool(
            user_explanation.strip()
            or user_owned_decision.strip()
            or user_question.strip()
            or user_options
            or user_tradeoffs
            or unattended_work_boundary.strip()
        )
        dependency_selected = bool(
            dependency_kind.strip()
            or dependency.strip()
            or dependency_owner.strip()
            or observable_trigger.strip()
        )
        selected = (
            recovery_selected,
            retry_selected,
            user_selected,
            dependency_selected,
        )
        if sum(selected) != 1:
            raise ValueError("exhausted corrections require exactly one concrete disposition")

        options = tuple(option.strip() for option in user_options if option.strip())
        tradeoffs = tuple(tradeoff.strip() for tradeoff in user_tradeoffs if tradeoff.strip())
        if recovery_selected and not (
            recovery_action.strip()
            and recovery_owner.strip()
            and recovery_evidence.strip()
            and set(recovery_links) == set(findings)
        ):
            raise ValueError(
                "recovery disposition requires an action, owner, evidence, "
                "and links to every unresolved finding"
            )
        if retry_selected and not (
            retry_plan.strip()
            and retry_evidence.strip()
            and set(retry_links) == set(findings)
            and retry_limit == 1
            and not item.bounded_retry_used
        ):
            raise ValueError(
                "retry disposition requires one unused bounded attempt with a plan, "
                "evidence, and links to every unresolved finding"
            )
        if user_selected and not (
            user_explanation.strip()
            and user_owned_decision.strip()
            and user_question.strip()
            and len(options) >= 2
            and len(options) == len(tradeoffs)
            and unattended_work_boundary.strip()
        ):
            raise ValueError(
                "User Action Required requires an explanation, genuine user-owned "
                "decision, exact question, options, tradeoffs, and unattended-work boundary"
            )
        if dependency_selected and not (
            dependency_kind in {"external", "technical"}
            and dependency.strip()
            and dependency_owner.strip()
            and observable_trigger.strip()
        ):
            raise ValueError(
                "continuing Blocked requires an external or technical dependency, "
                "owner, and observable trigger"
            )

        outcome = (
            "RECOVERY_ACTION"
            if recovery_selected
            else "BOUNDED_RETRY"
            if retry_selected
            else "USER_ACTION_REQUIRED"
            if user_selected
            else "CONTINUING_BLOCKED"
        )
        disposition = BlockedDisposition(
            outcome=outcome,
            unresolved_findings=findings,
            recovery_action=recovery_action.strip(),
            recovery_owner=recovery_owner.strip(),
            recovery_evidence=recovery_evidence.strip(),
            recovery_findings=recovery_links,
            retry_plan=retry_plan.strip(),
            retry_evidence=retry_evidence.strip(),
            retry_findings=retry_links,
            retry_limit=retry_limit,
            user_explanation=user_explanation.strip(),
            user_owned_decision=user_owned_decision.strip(),
            user_question=user_question.strip(),
            user_options=options,
            user_tradeoffs=tradeoffs,
            unattended_work_boundary=unattended_work_boundary.strip(),
            dependency_kind=dependency_kind.strip(),
            dependency=dependency.strip(),
            dependency_owner=dependency_owner.strip(),
            observable_trigger=observable_trigger.strip(),
        )
        self.events.append(
            {
                "event": "exhausted-correction-disposition-proposed",
                "item": item_id,
                "outcome": outcome,
                "unresolvedFindings": findings,
                "canonicalTask": item.canonical_task_id,
                "candidateCommit": item.candidate_commit,
                "reviewVerificationEvidence": item.review_verification_evidence,
                "gitState": item.git_state,
                "liveClaims": item.live_claims,
                "correctionAttemptHistory": tuple(item.correction_attempt_history),
            }
        )
        return disposition

    def apply_blocked_disposition(
        self,
        item_id: str,
        disposition: BlockedDisposition,
    ) -> BlockedDisposition:
        """Model the distinct Steward operation that applies a Coordinator decision."""

        item = self._item(item_id)
        if item.status != "Blocked" or disposition.state != "PROPOSED":
            raise ValueError("Steward applies one proposed disposition to a Blocked item")
        if item.blocked_disposition is not None:
            raise ValueError("Blocked item already has an active disposition")
        applied = replace(disposition, state="APPLIED")
        item.blocked_disposition = applied
        item.disposition_history.append(applied)
        if applied.outcome == "USER_ACTION_REQUIRED":
            item.status = "User Action Required"
        elif applied.outcome in {"RECOVERY_ACTION", "BOUNDED_RETRY"}:
            item.status = "Running"
        self.events.append(
            {
                "event": "steward-applied-blocked-disposition",
                "item": item_id,
                "outcome": applied.outcome,
            }
        )
        return applied

    def finish_bounded_retry(self, item_id: str, *, resolved: bool) -> None:
        """Consume the single extra retry and reopen reconciliation only on failure."""

        item = self._item(item_id)
        active = item.blocked_disposition
        if (
            active is None
            or active.outcome != "BOUNDED_RETRY"
            or active.state != "APPLIED"
        ):
            raise ValueError("no applied bounded retry is active")
        consumed = replace(active, state="CONSUMED")
        item.disposition_history[-1] = consumed
        item.blocked_disposition = None
        item.bounded_retry_used = True
        item.status = "Running" if resolved else "Blocked"
        self.events.append(
            {
                "event": "bounded-retry-finished",
                "item": item_id,
                "resolved": resolved,
            }
        )

    @staticmethod
    def reconcile_ambiguous_dispatch(
        immediate_matches: Sequence[TaskCandidate],
        settled_matches: Sequence[TaskCandidate],
    ) -> DispatchReconciliation:
        """Adopt the oldest visible match and safely contain duplicates."""

        matches = tuple(immediate_matches or settled_matches)
        if not matches:
            raise ValueError("one retry is allowed only after the settled read is empty")
        ordered = sorted(matches, key=lambda candidate: candidate.created_at)
        duplicates = tuple(ordered[1:])
        for duplicate in duplicates:
            duplicate.contain_duplicate()
        return DispatchReconciliation(ordered[0].task_id, duplicates, 0)

    @staticmethod
    def success_title(work_item: str) -> str:
        """Return the exact successful terminal display title."""

        normalized = work_item.strip()
        if not normalized:
            raise ValueError("a work-item title is required")
        return f"Done — {normalized}"

    @staticmethod
    def shared_claim_required(operation: str) -> bool:
        """Return whether an operation mutates shared state or an exclusive resource."""

        return operation in SHARED_CLAIM_OPERATIONS

    @staticmethod
    def verification_plan(
        *,
        focused_failure: bool = False,
        cross_cutting_risk: bool = False,
        combined_regression: bool = False,
    ) -> tuple[str, ...]:
        """Select focused item checks or the one combined regression."""

        if combined_regression:
            return ("system-wide regression",)
        checks = ["focused tests"]
        if focused_failure or cross_cutting_risk:
            checks.append("expanded regression")
        return tuple(checks)

    @staticmethod
    def combined_regression_run(
        *,
        selected_items: Sequence[str],
        merged_items: Sequence[str],
        main_commit: str,
        recorded_runs: Sequence[tuple[str, tuple[str, ...]]] = (),
    ) -> tuple[str, tuple[str, ...]] | None:
        """Schedule one run after every selected item is present on main."""

        selected = tuple(selected_items)
        if not selected or len(selected) != len(set(selected)):
            raise ValueError("selected work items must be non-empty and unique")
        if not main_commit.strip():
            raise ValueError("the tested main commit is required")
        if not set(selected).issubset(set(merged_items)):
            return None
        run = (main_commit, selected)
        return None if run in recorded_runs else run

    @staticmethod
    def combined_regression_failure(
        *,
        main_commit: str,
        failure: str,
        distinct_defect: bool,
    ) -> tuple[str, str] | None:
        """Route a distinct combined-regression failure against tested main."""

        if not distinct_defect:
            return None
        if not main_commit.strip() or not failure.strip():
            raise ValueError("a tested main commit and failure are required")
        return (main_commit, failure)

    @staticmethod
    def post_facto_reduction(
        *,
        actual_waste_observed: bool,
        options: Sequence[str],
        selected: str,
    ) -> str | None:
        """Select one of three reductions only after broad-work waste is observed."""

        if not actual_waste_observed:
            return None
        if len(options) != 3 or selected not in options:
            raise ValueError("a post-facto audit requires three options and one selection")
        return selected

    def _item(self, item_id: str) -> WorkItem:
        """Resolve one item by its provider-returned canonical identifier."""

        try:
            return next(item for item in self.items if item.item_id == item_id)
        except StopIteration as error:
            raise KeyError(item_id) from error
