# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Simulates file-backed queue capacity, bounded claim retries, and terminal cleanup.
# Test plan: evals/agent-tests/dev-backlog-coordinator/requirements-matrix.md

"""Provide deterministic state transitions for parent backlog coordination."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Sequence


RUNNING_TARGET = 10
CLAIM_ATTEMPT_MINUTES = (0, 5, 10, 15, 20, 25, 30)
CLAIM_KINDS = ("integration", "completion")
SHARED_CLAIM_OPERATIONS = frozenset(
    {"main integration", "backlog mutation", "generated output", "exclusive resource"}
)


@dataclass
class WorkItem:
    """Represent the durable execution fields stored in one work-item file.

    Example:
        item = WorkItem("feature-a", "Ready")
        assert item.canonical_task_id is None
    """

    item_id: str
    status: str
    canonical_task_id: str | None = None
    phase: str | None = None
    branch: str | None = None
    worktree: str | None = None
    candidate_commit: str | None = None
    wait_started_minute: int | None = None
    claim_attempts: dict[str, list[dict[str, object]]] = field(default_factory=dict)
    acquired_claims: set[str] = field(default_factory=set)
    open_issues: list[str] = field(default_factory=list)


@dataclass
class TaskCandidate:
    """Represent one task candidate during ambiguous-dispatch reconciliation.

    Example:
        candidate = TaskCandidate("task-1", "parent", "backlog/a.md", "a", datetime.now())
        assert not candidate.archived
    """

    task_id: str
    parent_task_id: str
    backlog_path: str
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
        """Initialize from file-backed work items without a second registry."""

        self.items = list(items)
        self.events: list[dict[str, object]] = []

    def running_count(self) -> int:
        """Count only file-backed Running work items."""

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

    def record_claim_attempt(
        self,
        item_id: str,
        *,
        claim_kind: str,
        elapsed_minutes: int,
        outcome: str,
        blocking_claim_id: str | None = None,
    ) -> None:
        """Record the next permitted attempt in one bounded claim window."""

        if claim_kind not in CLAIM_KINDS:
            raise ValueError(f"unsupported claim kind: {claim_kind}")
        item = self._item(item_id)
        if item.status != "Running":
            raise ValueError("only a Running work item may own a claim retry window")
        if claim_kind == "completion" and "integration" not in item.acquired_claims:
            raise ValueError("completion claim requires acquired integration evidence")
        if claim_kind in item.acquired_claims:
            raise ValueError(f"{claim_kind} claim is already acquired")
        attempts = item.claim_attempts.setdefault(claim_kind, [])
        if len(attempts) >= len(CLAIM_ATTEMPT_MINUTES):
            raise ValueError(f"{claim_kind} claim retry window is exhausted")
        expected_minute = CLAIM_ATTEMPT_MINUTES[len(attempts)]
        if elapsed_minutes != expected_minute:
            raise ValueError(
                f"{claim_kind} claim attempt must occur at minute {expected_minute}"
            )
        if item.wait_started_minute is None:
            item.wait_started_minute = 0
        phase_name = "Integration" if claim_kind == "integration" else "Completion"
        item.phase = phase_name if outcome == "ACQUIRED" else f"{phase_name} Wait"
        attempts.append(
            {
                "claimKind": claim_kind,
                "elapsedMinutes": elapsed_minutes,
                "outcome": outcome,
                "blockingClaimId": blocking_claim_id,
            }
        )
        if outcome == "ACQUIRED":
            item.acquired_claims.add(claim_kind)
        elif elapsed_minutes == 30:
            item.phase = f"{phase_name} Investigation"
            item.open_issues.append(
                f"{claim_kind} claim wait reached 30 minutes: "
                f"{blocking_claim_id or 'unknown owner'}"
            )

    def waits_requiring_investigation(self) -> tuple[str, ...]:
        """Return Running work items whose bounded claim window expired."""

        return tuple(
            item.item_id
            for item in self.items
            if item.status == "Running"
            and item.phase in {"Integration Investigation", "Completion Investigation"}
        )

    def dispose_unresolved_wait(self, item_id: str, *, user_decision: bool) -> None:
        """Free one active slot through a truthful unresolved-wait disposition."""

        item = self._item(item_id)
        if item.phase not in {"Integration Investigation", "Completion Investigation"}:
            raise ValueError("the thirty-minute investigation must occur first")
        item.status = "User Action Required" if user_decision else "Blocked"
        item.phase = None
        self.events.append(
            {"event": "wait-disposed", "item": item_id, "status": item.status}
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
        final_campaign: bool = False,
    ) -> tuple[str, ...]:
        """Select focused item checks and reserve the complete catalog for final state."""

        if final_campaign:
            return ("complete agent catalog",)
        checks = ["focused tests"]
        if focused_failure or cross_cutting_risk:
            checks.append("expanded regression")
        return tuple(checks)

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
        """Resolve one item by its durable file-backed identifier."""

        try:
            return next(item for item in self.items if item.item_id == item_id)
        except StopIteration as error:
            raise KeyError(item_id) from error
