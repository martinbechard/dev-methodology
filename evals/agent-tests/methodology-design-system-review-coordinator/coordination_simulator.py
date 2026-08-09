"""
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
AI attribution: Generated with AI assistance.
Responsibility: Simulates deterministic report validation, evidence reconciliation, acceptance, pricing, and ranking for the design-system coordinator.
Design: agents/roles/methodology-maintenance/methodology-design-system-review-coordinator.role.yaml
Tests: evals/agent-tests/methodology-design-system-review-coordinator/test_coordination_simulator.py
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
import importlib.util
from pathlib import Path
from typing import Any


RUNNER_CONTRACT_PATH = (
    Path(__file__).resolve().parents[1]
    / "methodology-design-system-checklist-runner"
    / "contract.py"
)
RUNNER_SPEC = importlib.util.spec_from_file_location(
    "design_system_runner_contract_for_coordinator",
    RUNNER_CONTRACT_PATH,
)
assert RUNNER_SPEC and RUNNER_SPEC.loader
runner_contract = importlib.util.module_from_spec(RUNNER_SPEC)
RUNNER_SPEC.loader.exec_module(runner_contract)


Assignment = tuple[str, str, tuple[str, ...]]


def assignment_key(assignment: Assignment) -> str:
    """Return the stable page-checklist key for one bounded assignment."""

    page, checklist, _ = assignment
    return f"{page}:{checklist}"


def reconcile_claims(claims: Iterable[Mapping[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, object]]]:
    """De-duplicate exact claims and preserve contradictory results by page and item."""

    unique: list[dict[str, str]] = []
    seen: set[tuple[tuple[str, str], ...]] = set()
    by_item: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for claim in claims:
        normalized = {str(key): str(value) for key, value in claim.items()}
        signature = tuple(sorted(normalized.items()))
        if signature in seen:
            continue
        seen.add(signature)
        unique.append(normalized)
        by_item[(normalized.get("page", ""), normalized.get("id", ""))].append(normalized)

    conflicts: list[dict[str, object]] = []
    for (page, check_id), item_claims in by_item.items():
        results = {claim.get("result") for claim in item_claims}
        if len(results) > 1:
            conflicts.append({"page": page, "id": check_id, "claims": item_claims})
    return unique, conflicts


def coordinate(
    assignments: Sequence[Assignment],
    report_attempts: Mapping[str, Sequence[dict[str, Any]]],
    *,
    unavailable: Iterable[str] = (),
    extra_claims: Iterable[Mapping[str, str]] = (),
) -> dict[str, object]:
    """Return the coordinator decision for bounded assignments and at most one retry.

    Each assignment has one initial runner invocation. A malformed initial report may
    have one corrected retry. Unavailable, missing, twice-malformed, incomplete, or
    contradictory evidence produces BLOCKED without local checklist substitution.
    """

    keys = [assignment_key(assignment) for assignment in assignments]
    duplicate_keys = sorted(key for key in set(keys) if keys.count(key) > 1)
    if duplicate_keys:
        return {
            "status": "BLOCKED",
            "coverage": {"required": len(assignments), "completed": 0, "missing": duplicate_keys},
            "retries": [],
            "findings": [],
            "claims": [],
            "conflicts": [{"duplicateAssignments": duplicate_keys}],
        }

    unavailable_keys = set(unavailable)
    completed: list[str] = []
    missing: list[str] = []
    retries: list[str] = []
    findings: list[dict[str, str]] = []
    claims: list[dict[str, str]] = [dict(claim) for claim in extra_claims]
    has_failure = False
    incomplete = False

    for page, checklist, checklist_ids in assignments:
        key = f"{page}:{checklist}"
        if key in unavailable_keys:
            missing.append(key)
            continue
        attempts = list(report_attempts.get(key, ()))[:2]
        accepted_report: dict[str, Any] | None = None
        for index, report in enumerate(attempts):
            errors = runner_contract.validate_report(checklist_ids, report)
            if not errors:
                accepted_report = report
                break
            if index == 0:
                retries.append(key)
        if accepted_report is None:
            missing.append(key)
            continue
        completed.append(key)
        has_failure = has_failure or accepted_report["status"] == "FAIL"
        incomplete = incomplete or accepted_report["status"] == "NOT TESTED"
        for check in accepted_report["checks"]:
            claims.append(
                {
                    "page": page,
                    "id": str(check["id"]),
                    "result": str(check["result"]),
                    "evidence": str(check["evidence"]),
                }
            )
        findings.extend(dict(finding) for finding in accepted_report["findings"])

    unique_claims, conflicts = reconcile_claims(claims)
    unique_findings: list[dict[str, str]] = []
    finding_signatures: set[tuple[tuple[str, str], ...]] = set()
    for finding in findings:
        signature = tuple(sorted((str(key), str(value)) for key, value in finding.items()))
        if signature not in finding_signatures:
            finding_signatures.add(signature)
            unique_findings.append(finding)

    status = "ACCEPTED"
    if missing or conflicts or incomplete:
        status = "BLOCKED"
    elif has_failure:
        status = "REJECTED"
    return {
        "status": status,
        "coverage": {"required": len(assignments), "completed": len(completed), "missing": missing},
        "retries": retries,
        "findings": unique_findings,
        "claims": unique_claims,
        "conflicts": conflicts,
    }


def estimated_cost(usage: Mapping[str, int], rates: Mapping[str, float] | None) -> float | None:
    """Return supplied-rate cost after subtracting cached input from full-price input."""

    if rates is None:
        return None
    cached = max(int(usage["cached_input_tokens"]), 0)
    total_input = max(int(usage["input_tokens"]), 0)
    uncached = max(total_input - cached, 0)
    output = max(int(usage["output_tokens"]), 0)
    return (
        uncached * float(rates["input_tokens"])
        + cached * float(rates["cached_input_tokens"])
        + output * float(rates["output_tokens"])
    ) / 1_000_000


def rank_candidates(candidates: Sequence[Mapping[str, object]]) -> dict[str, object]:
    """Rank candidates by exact accuracy, inclusive priced-cost bands, then speed."""

    remaining = [dict(candidate) for candidate in candidates]
    ranked: list[dict[str, object]] = []
    rank = 0
    while remaining:
        best_accuracy = max(float(candidate["accuracy"]) for candidate in remaining)
        accuracy_peers = [candidate for candidate in remaining if float(candidate["accuracy"]) == best_accuracy]
        remaining = [candidate for candidate in remaining if candidate not in accuracy_peers]
        priced = [candidate for candidate in accuracy_peers if candidate.get("estimated_cost") is not None]
        unpriced = [candidate for candidate in accuracy_peers if candidate.get("estimated_cost") is None]

        while priced:
            cheapest = min(float(candidate["estimated_cost"]) for candidate in priced)
            ceiling = cheapest * 1.15
            equivalent = [candidate for candidate in priced if float(candidate["estimated_cost"]) <= ceiling + 1e-12]
            priced = [candidate for candidate in priced if candidate not in equivalent]
            equivalent.sort(key=lambda candidate: (float(candidate["wall_seconds"]), str(candidate["id"])))
            for candidate in equivalent:
                rank += 1
                ranked.append({**candidate, "rank": rank, "pricing_status": "priced", "provisional": False})

        unpriced.sort(key=lambda candidate: (float(candidate["wall_seconds"]), str(candidate["id"])))
        for candidate in unpriced:
            rank += 1
            ranked.append({**candidate, "rank": rank, "pricing_status": "unpriced", "provisional": rank == 1})

    return {
        "ranking": ranked,
        "winner_provisional": bool(ranked and ranked[0]["pricing_status"] == "unpriced"),
    }
