#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Simulates read-only watchdog observations and Coordinator-owned Stalled dispositions.

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


ACTIVE_CAPACITY_STATUSES = {"Starting", "Running"}
ACTIVE_SERIES_STATUSES = {"Ready", "Starting", "Running", "Awaiting Review"}
TERMINAL_STATUSES = {"Completed", "Failed", "Abandoned"}


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
    estimate_boundary_crossed: bool = False
    hard_stop_crossed: bool = False
    progress_gap: bool = False
    task_state: str = "active"
    preventing_cause: str = "unknown"
    stalled_exit_satisfied: bool = False
    blocker_exit_satisfied: bool = False


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
    """Return one no-action result or one collection of actionable alerts."""

    status: str
    message: str
    alerts: list[WatchdogAlert]
    mutated: bool = False


class WatchdogCycle:
    """Evaluate source-backed anomalies without changing observed state."""

    def evaluate(self, items: Iterable[WorkItem]) -> CycleResult:
        """Return actionable alerts or one concise healthy-cycle result.

        items contains the current provider and task evidence. The method reads
        each instance, emits no coordination mutations, and returns ALERT when
        at least one anomaly or satisfied exit condition requires parent action.
        """

        alerts: list[WatchdogAlert] = []
        for item in items:
            if item.status == "Running" and self._suspected_stall(item):
                alerts.append(
                    WatchdogAlert(
                        provider_identity=item.provider_identity,
                        evidence=self._stall_evidence(item),
                        reason="progress boundary crossed while the cause remains unknown",
                        recommended_action=(
                            "Coordinator investigates and delegates Stalled only if "
                            "the evidence justifies it"
                        ),
                        preventing_cause=item.preventing_cause,
                    )
                )
            elif item.status == "Stalled" and item.stalled_exit_satisfied:
                alerts.append(
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
            elif item.status == "Blocked" and item.blocker_exit_satisfied:
                alerts.append(
                    WatchdogAlert(
                        provider_identity=item.provider_identity,
                        evidence="the recorded Blocked unblock condition is now satisfied",
                        reason="Blocked recovery requires Coordinator attention",
                        recommended_action=(
                            "Coordinator validates the unblock evidence and chooses "
                            "the authorized provider disposition"
                        ),
                        preventing_cause=item.preventing_cause,
                    )
                )

        if not alerts:
            return CycleResult(
                "NO_ACTION",
                "No actionable watchdog condition observed.",
                [],
            )
        return CycleResult(
            "ALERT",
            f"{len(alerts)} actionable watchdog condition(s) observed.",
            alerts,
        )

    @staticmethod
    def _suspected_stall(item: WorkItem) -> bool:
        return (
            item.estimate_boundary_crossed
            or item.hard_stop_crossed
            or item.progress_gap
            or item.task_state in {"stopped", "missing"}
        )

    @staticmethod
    def _stall_evidence(item: WorkItem) -> str:
        evidence = [
            f"phase={item.phase or 'unknown'}",
            f"last_productive_evidence={item.last_productive_evidence or 'missing'}",
            f"canonical_thread={item.canonical_thread or 'missing'}",
            f"root_task={item.root_task or 'missing'}",
            f"task_state={item.task_state}",
        ]
        return "; ".join(evidence)


class CoordinatorDisposition:
    """Choose one authorized Stalled exit from mutually exclusive evidence."""

    def choose(
        self,
        *,
        same_owner_resumed: bool = False,
        ownership_ended: bool = False,
        known_blocker: bool = False,
        user_action_required: bool = False,
        terminal_status: str = "",
    ) -> str:
        """Return the one lifecycle state supported by the supplied evidence.

        Boolean inputs identify the mutually exclusive safe-resumption,
        redispatch, blocker, and user-action boundaries. terminal_status may be
        Completed, Failed, or Abandoned. Missing or conflicting evidence raises
        ValueError so no default lifecycle mutation can be inferred.
        """

        choices = [
            ("Running", same_owner_resumed),
            ("Ready", ownership_ended),
            ("Blocked", known_blocker),
            ("User Action Required", user_action_required),
            (terminal_status, bool(terminal_status)),
        ]
        selected = [status for status, enabled in choices if enabled]
        if terminal_status and terminal_status not in TERMINAL_STATUSES:
            raise ValueError(f"invalid terminal Stalled disposition: {terminal_status}")
        if len(selected) != 1:
            raise ValueError("no evidence-backed Stalled disposition")
        return selected[0]


def active_capacity(items: Iterable[WorkItem]) -> int:
    """Count only Starting and Running items against active capacity."""

    return sum(item.status in ACTIVE_CAPACITY_STATUSES for item in items)


def series_state(statuses: Iterable[str]) -> str:
    """Derive one deterministic series state without collapsing mixed pauses."""

    materialized = list(statuses)
    if not materialized:
        raise ValueError("series requires at least one child state")
    if all(status == "Completed" for status in materialized):
        return "completed"
    if any(status == "Failed" for status in materialized):
        return "failed"
    if any(status in ACTIVE_SERIES_STATUSES for status in materialized):
        return "active"
    if all(status == "Stalled" for status in materialized):
        return "stalled"
    if all(status == "Blocked" for status in materialized):
        return "blocked"
    return "mixed:" + ",".join(sorted(set(materialized)))


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
