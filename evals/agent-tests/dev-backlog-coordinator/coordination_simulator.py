# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Provides deterministic state transitions for the Dev Backlog Coordinator suite.
# Design: design/orchestrated-development-lifecycle.html
# Test plan: evals/agent-tests/dev-backlog-coordinator/requirements-matrix.md

"""Simulate observable coordination decisions for deterministic evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Iterable, Sequence


class CampaignState(str, Enum):
    """Represent the valid execution states of one artifact campaign.

    Example:
        assert CampaignState.ACTIVE.value == "active"
    """

    QUEUED = "queued"
    ACTIVE = "active"
    REVIEW = "review"


@dataclass
class Campaign:
    """Track one campaign and its mutable scheduler state.

    A coordinator creates a campaign with an identifier and lets the simulator
    move it from queued to active to review.

    Example:
        campaign = Campaign("role")
        assert campaign.state is CampaignState.QUEUED
    """

    campaign_id: str
    state: CampaignState = CampaignState.QUEUED


@dataclass
class TaskCandidate:
    """Represent a reconciled Codex task and its containment state.

    Identity fields mirror the task-list evidence used for reconciliation.
    ``repository_mutation_count`` records mutations performed by the task,
    while ``status`` and ``archived`` model reversible UI lifecycle state.

    Example:
        candidate = TaskCandidate(
            task_id="task-1",
            parent_task_id="parent-1",
            backlog_path="backlog/feature-backlog/item.md",
            normalized_objective="deliver item",
            created_at=datetime(2026, 7, 19),
            status="waiting",
            title="Preflight item",
        )
        assert candidate.repository_mutation_count == 0
    """

    task_id: str
    parent_task_id: str
    backlog_path: str
    normalized_objective: str
    created_at: datetime
    status: str
    title: str
    repository_mutation_count: int = 0
    archived: bool = False
    containment_transitions: list[str] = field(default_factory=list)

    def contain_duplicate(self) -> None:
        """Stop and archive this duplicate after proving it made no mutation.

        The parent coordinator calls this only after choosing another task as
        canonical. The method changes reversible task UI state and records each
        transition. It does not change ``repository_mutation_count``. A
        ``ValueError`` prevents archival when the duplicate has repository
        mutations that require a separate preservation decision.
        """

        self.status = "stopped"
        self.containment_transitions.append("stopped")
        if self.repository_mutation_count != 0:
            raise ValueError(
                "a duplicate with repository mutations cannot be archived"
            )
        self.containment_transitions.append("zero mutation verified")
        self.archived = True
        self.containment_transitions.append("archived")


@dataclass(frozen=True)
class DispatchReconciliation:
    """Describe the canonical task and contained duplicate task states.

    The result is durable reconciliation evidence. Callers inspect the retained
    task id, each duplicate's stopped/no-mutation/archive state, and the retry
    count before continuing dispatch.

    Example:
        result = DispatchReconciliation("task-1", (), 0)
        assert result.expected_retry_count == 0
    """

    canonical_task_id: str
    contained_duplicates: tuple[TaskCandidate, ...]
    expected_retry_count: int

    def evidence(self) -> dict[str, object]:
        """Return serializable reconciliation evidence without side effects."""

        return {
            "canonicalTaskId": self.canonical_task_id,
            "containedDuplicates": tuple(
                {
                    "taskId": duplicate.task_id,
                    "status": duplicate.status,
                    "repositoryMutationCount": duplicate.repository_mutation_count,
                    "archived": duplicate.archived,
                    "transitions": tuple(duplicate.containment_transitions),
                }
                for duplicate in self.contained_duplicates
            ),
            "expectedRetryCount": self.expected_retry_count,
        }


@dataclass(frozen=True)
class ChainTask:
    """Identify one named task in the deterministic successor chain.

    Example:
        task = ChainTask("Wiki Research", "task-wiki")
        assert task.label == "Wiki Research"
    """

    label: str
    task_id: str


@dataclass
class WakeObligation:
    """Track one parent-owned predecessor-to-successor wake obligation.

    The predecessor reports release evidence to the parent. The parent owns
    delivery and acknowledgement state; the successor never polls.

    Example:
        obligation = WakeObligation("source", "successor", ("commit",))
        assert obligation.phase == "ARTIFACT WAIT"
    """

    source_id: str
    successor_id: str
    required_evidence: tuple[str, ...]
    predecessor_released: bool = False
    delivered_evidence: set[str] = field(default_factory=set)
    notified: bool = False
    acknowledged: bool = False
    successor_poll_count: int = 0
    phase: str = "ARTIFACT WAIT"
    last_audit_minutes: int | None = None


@dataclass(frozen=True)
class WakeAuditFinding:
    """Report missing evidence, notification, or acknowledgement for one baton.

    Example:
        finding = WakeAuditFinding("source", "successor", (), True, True)
        assert finding.notification_missing
    """

    source_id: str
    successor_id: str
    missing_evidence: tuple[str, ...]
    notification_missing: bool
    acknowledgement_missing: bool


SUCCESSOR_CHAIN = (
    ChainTask("Codex coordination", "019f77f4-c4bd-7c91-b197-c987a7beb838"),
    ChainTask(
        "review quotation traceability",
        "019f7a45-a697-7d80-9744-a06c8d22d69a",
    ),
    ChainTask("Wiki Research", "019f7a45-9c77-79c1-9c68-35cf6cb9f710"),
    ChainTask("Hibernate/Panache", "019f7a73-53f1-7b12-9f66-c4aebe6bab2e"),
    ChainTask("MySQL", "019f79e6-25ef-7b51-ab3c-39fce2656db4"),
)
"""Concrete regression chain used only by the executable evaluation suite."""


class CoordinationSimulator:
    """Model coordinator decisions that require deterministic evidence.

    Create an instance with dependency-ready campaign identifiers, execute the
    relevant coordination decisions, and inspect public state or returned
    evidence.

    Example:
        simulator = CoordinationSimulator(("skill", "role", "evals"))
        assert len(simulator.start_initial_campaigns()) == 3
    """

    def __init__(self, campaign_ids: Sequence[str] = ()) -> None:
        """Initialize queued campaigns and empty event and wake ledgers.

        ``campaign_ids`` supplies unique campaign identifiers in deterministic
        scheduling order. Construction performs no I/O or external mutation.
        """

        self.campaigns = {
            campaign_id: Campaign(campaign_id) for campaign_id in campaign_ids
        }
        self.active_limit = 3
        self.events: list[dict[str, object]] = []
        self.wake_obligations: dict[tuple[str, str], WakeObligation] = {}

    def start_initial_campaigns(self) -> tuple[str, ...]:
        """Activate the required starting floor of three queued campaigns.

        Returns active campaign ids in input order and records one scheduler
        event. Raises ``ValueError`` when fewer than three campaigns are ready.
        """

        queued = [
            campaign
            for campaign in self.campaigns.values()
            if campaign.state is CampaignState.QUEUED
        ]
        if len(queued) < 3:
            raise ValueError("three dependency-ready campaigns are required")
        started = queued[:3]
        for campaign in started:
            campaign.state = CampaignState.ACTIVE
        active = self.active_campaign_ids()
        self.events.append({"event": "initial-floor-started", "active": active})
        return active

    def record_healthy_interval(self) -> tuple[str, ...]:
        """Scale healthy active work by at most one queued campaign.

        Returns all active campaign ids. Records a scale event only when a
        queued campaign exists. Raises ``ValueError`` below the healthy floor.
        """

        if len(self.active_campaign_ids()) < 3:
            raise ValueError("the current floor is not healthy")
        next_campaign = next(
            (
                campaign
                for campaign in self.campaigns.values()
                if campaign.state is CampaignState.QUEUED
            ),
            None,
        )
        if next_campaign is None:
            return self.active_campaign_ids()
        self.active_limit += 1
        next_campaign.state = CampaignState.ACTIVE
        active = self.active_campaign_ids()
        self.events.append({"event": "healthy-plus-one", "active": active})
        return active

    def route_finished_campaign(self, campaign_id: str) -> str:
        """Move one active campaign to independent review.

        ``campaign_id`` must identify an active campaign. The method mutates
        that campaign, records the routing event, and returns the destination.
        A missing id raises ``KeyError`` and a non-active id raises
        ``ValueError``.
        """

        campaign = self.campaigns[campaign_id]
        if campaign.state is not CampaignState.ACTIVE:
            raise ValueError("only an active campaign can finish")
        campaign.state = CampaignState.REVIEW
        self.events.append(
            {
                "event": "finished-lane-routed",
                "campaign": campaign_id,
                "destination": "independent review",
                "still_active": self.active_campaign_ids(),
            }
        )
        return "independent review"

    def active_campaign_ids(self) -> tuple[str, ...]:
        """Return active campaign ids in deterministic insertion order."""

        return tuple(
            campaign.campaign_id
            for campaign in self.campaigns.values()
            if campaign.state is CampaignState.ACTIVE
        )

    def lifecycle_start(
        self, *, checkout: str, primary_backlog_mutation_active: bool
    ) -> dict[str, object]:
        """Authorize lifecycle start or refuse a mismatched isolated checkout.

        ``checkout`` is ``isolated`` for an isolated worktree; other values
        model primary execution. ``primary_backlog_mutation_active`` states
        whether primary is occupied. The returned decision and appended event
        expose ``PRIMARY_REQUIRED`` without starting artifact work.
        """

        refused = checkout == "isolated" and primary_backlog_mutation_active
        decision: dict[str, object] = {
            "phase": "LIFECYCLE START",
            "outcome": "PRIMARY_REQUIRED" if refused else "AUTHORIZED",
            "artifact_go": not refused,
        }
        self.events.append({"event": "lifecycle-start-decision", **decision})
        return decision

    @staticmethod
    def reconcile_ambiguous_dispatch(
        immediate_matches: Sequence[TaskCandidate],
        settled_matches: Sequence[TaskCandidate],
    ) -> DispatchReconciliation:
        """Adopt the oldest settled match and contain every duplicate.

        The immediate read wins when non-empty; otherwise the bounded-settlement
        read is used. Each later-created match transitions to stopped, verified
        zero-mutation, and archived state. The result requires zero retries. A
        ``ValueError`` signals that both reads were empty or that a duplicate
        already made a repository mutation.
        """

        matches = immediate_matches or settled_matches
        if not matches:
            raise ValueError(
                "one retry is required only after the settled read is empty"
            )
        ordered = sorted(matches, key=lambda candidate: candidate.created_at)
        canonical = ordered[0]
        duplicates = tuple(ordered[1:])
        for duplicate in duplicates:
            duplicate.contain_duplicate()
        return DispatchReconciliation(
            canonical_task_id=canonical.task_id,
            contained_duplicates=duplicates,
            expected_retry_count=0,
        )

    @staticmethod
    def success_title(work_item: str) -> str:
        """Return the exact successful terminal display title.

        ``work_item`` must contain non-whitespace text. The return value uses
        the display-only ``Done —`` convention. Empty input raises
        ``ValueError``.
        """

        normalized = work_item.strip()
        if not normalized:
            raise ValueError("a work-item title is required")
        return f"Done — {normalized}"

    def seed_successor_chain(
        self, required_evidence: Iterable[str]
    ) -> tuple[WakeObligation, ...]:
        """Create parent-owned wake obligations for the regression chain.

        ``required_evidence`` names every evidence field that each baton must
        carry. The method replaces matching ledger entries and returns the
        ordered obligations without waking successors.
        """

        evidence = tuple(required_evidence)
        obligations = []
        for source, successor in zip(SUCCESSOR_CHAIN, SUCCESSOR_CHAIN[1:]):
            obligation = WakeObligation(
                source_id=source.task_id,
                successor_id=successor.task_id,
                required_evidence=evidence,
            )
            self.wake_obligations[(source.task_id, successor.task_id)] = obligation
            obligations.append(obligation)
        return tuple(obligations)

    def record_predecessor_release(self, source_id: str) -> None:
        """Mark all obligations from ``source_id`` as predecessor-released."""

        for obligation in self.wake_obligations.values():
            if obligation.source_id == source_id:
                obligation.predecessor_released = True

    def audit_wake_obligations(
        self, *, elapsed_minutes: int
    ) -> tuple[WakeAuditFinding, ...]:
        """Find released batons missing evidence, delivery, or acknowledgement.

        ``elapsed_minutes`` is the time since the preceding audit. Values below
        fifteen return no findings and make no ledger changes. At fifteen or
        more, the method records the audit time and returns findings without
        waking or polling a successor.
        """

        if elapsed_minutes < 15:
            return ()
        findings = []
        for obligation in self.wake_obligations.values():
            obligation.last_audit_minutes = elapsed_minutes
            if not obligation.predecessor_released:
                continue
            missing = tuple(
                evidence
                for evidence in obligation.required_evidence
                if evidence not in obligation.delivered_evidence
            )
            if missing or not obligation.notified or not obligation.acknowledged:
                findings.append(
                    WakeAuditFinding(
                        source_id=obligation.source_id,
                        successor_id=obligation.successor_id,
                        missing_evidence=missing,
                        notification_missing=not obligation.notified,
                        acknowledgement_missing=not obligation.acknowledged,
                    )
                )
        return tuple(findings)

    def parent_repair_baton(
        self,
        *,
        source_id: str,
        successor_id: str,
        delivered_evidence: Iterable[str],
    ) -> WakeObligation:
        """Deliver one complete evidence-bearing repair wake as the parent.

        The source and successor ids select an existing obligation.
        The predecessor must already be released. ``delivered_evidence`` is
        merged into the evidence set for the first delivery. Missing required
        evidence raises ``ValueError``; success records exactly one
        notification, changes the phase to ``ARTIFACT RESUME``, appends one
        event, and returns the mutated obligation. Later repair attempts are
        idempotent while acknowledgement remains pending.
        """

        obligation = self.wake_obligations[(source_id, successor_id)]
        if not obligation.predecessor_released:
            raise ValueError("the predecessor must release before ARTIFACT RESUME")
        if obligation.notified:
            return obligation
        obligation.delivered_evidence.update(delivered_evidence)
        missing = set(obligation.required_evidence) - obligation.delivered_evidence
        if missing:
            raise ValueError(f"missing required baton evidence: {sorted(missing)}")
        obligation.notified = True
        obligation.phase = "ARTIFACT RESUME"
        self.events.append(
            {
                "event": "parent-baton-repaired",
                "source": source_id,
                "successor": successor_id,
            }
        )
        return obligation

    def acknowledge_resume(self, *, source_id: str, successor_id: str) -> None:
        """Record successor acknowledgement after the parent delivered a baton.

        The ids select an existing obligation. Calling before notification
        raises ``ValueError``; success mutates only acknowledgement state.
        """

        obligation = self.wake_obligations[(source_id, successor_id)]
        if not obligation.notified:
            raise ValueError(
                "the parent must deliver the baton before acknowledgement"
            )
        obligation.acknowledged = True
