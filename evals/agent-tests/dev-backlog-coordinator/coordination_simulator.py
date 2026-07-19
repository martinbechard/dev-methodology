# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# Summary: Provides deterministic state transitions for the Dev Backlog Coordinator suite.

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Iterable, Sequence


class CampaignState(str, Enum):
    QUEUED = "queued"
    ACTIVE = "active"
    REVIEW = "review"


@dataclass
class Campaign:
    campaign_id: str
    state: CampaignState = CampaignState.QUEUED


@dataclass(frozen=True)
class TaskCandidate:
    task_id: str
    parent_task_id: str
    backlog_path: str
    normalized_objective: str
    created_at: datetime
    status: str
    title: str


@dataclass(frozen=True)
class DispatchReconciliation:
    canonical_task_id: str
    contained_duplicate_ids: tuple[str, ...]
    duplicate_containment_steps: tuple[str, ...]
    expected_retry_count: int

    def evidence(self) -> dict[str, object]:
        return {
            "canonicalTaskId": self.canonical_task_id,
            "containedDuplicateIds": self.contained_duplicate_ids,
            "duplicateContainmentSteps": self.duplicate_containment_steps,
            "expectedRetryCount": self.expected_retry_count,
        }


@dataclass(frozen=True)
class ChainTask:
    label: str
    task_id: str


@dataclass
class WakeObligation:
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


class CoordinationSimulator:
    """Model the coordinator decisions that must have deterministic evidence."""

    def __init__(self, campaign_ids: Sequence[str] = ()) -> None:
        self.campaigns = {
            campaign_id: Campaign(campaign_id) for campaign_id in campaign_ids
        }
        self.active_limit = 3
        self.events: list[dict[str, object]] = []
        self.wake_obligations: dict[tuple[str, str], WakeObligation] = {}

    def start_initial_campaigns(self) -> tuple[str, ...]:
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
        return tuple(
            campaign.campaign_id
            for campaign in self.campaigns.values()
            if campaign.state is CampaignState.ACTIVE
        )

    def lifecycle_start(
        self, *, checkout: str, primary_backlog_mutation_active: bool
    ) -> dict[str, object]:
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
        matches = immediate_matches or settled_matches
        if not matches:
            raise ValueError(
                "one retry is required only after the settled read is empty"
            )
        ordered = sorted(matches, key=lambda candidate: candidate.created_at)
        canonical = ordered[0]
        duplicates = tuple(candidate.task_id for candidate in ordered[1:])
        return DispatchReconciliation(
            canonical_task_id=canonical.task_id,
            contained_duplicate_ids=duplicates,
            duplicate_containment_steps=(
                "stop",
                "verify stopped and no mutation",
                "archive when supported",
            ),
            expected_retry_count=0,
        )

    @staticmethod
    def success_title(work_item: str) -> str:
        normalized = work_item.strip()
        if not normalized:
            raise ValueError("a work-item title is required")
        return f"Done — {normalized}"

    def seed_successor_chain(
        self, required_evidence: Iterable[str]
    ) -> tuple[WakeObligation, ...]:
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
        for obligation in self.wake_obligations.values():
            if obligation.source_id == source_id:
                obligation.predecessor_released = True

    def audit_wake_obligations(
        self, *, elapsed_minutes: int
    ) -> tuple[WakeAuditFinding, ...]:
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
        obligation = self.wake_obligations[(source_id, successor_id)]
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
        obligation = self.wake_obligations[(source_id, successor_id)]
        if not obligation.notified:
            raise ValueError("the parent must deliver the baton before acknowledgement")
        obligation.acknowledged = True
