"""
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
AI attribution: Generated with AI assistance.
Responsibility: Simulates strict report validation, evidence reconciliation, acceptance, exact pricing, and ranking for the design-system coordinator.
Design: agents/roles/methodology-maintenance/methodology-design-system-review-coordinator.role.yaml
Tests: evals/agent-tests/methodology-design-system-review-coordinator/test_coordination_simulator.py
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from decimal import Decimal, InvalidOperation
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


def _missing_assignment(assignment: Assignment, reason: str) -> dict[str, str]:
    """Return one exact missing-coverage record."""

    page, checklist, _ = assignment
    return {"page": page, "checklist": checklist, "reason": reason}


def _base_output(assignments: Sequence[Assignment]) -> dict[str, object]:
    """Create every coordinator output field with its exact nested container type."""

    return {
        "status": "BLOCKED",
        "coverage": {"required": len(assignments), "completed": 0, "missing": []},
        "reconciledFindings": [],
        "evidenceConflicts": [],
        "acceptanceRationale": "Required evidence is incomplete.",
        "modelEvalRanking": [],
        "runnerReports": [],
    }


def _normalize_claim(claim: Mapping[str, object]) -> dict[str, str]:
    """Normalize a material claim without discarding its source."""

    return {
        "page": str(claim.get("page", "")),
        "checklist": str(claim.get("checklist", "")),
        "id": str(claim.get("id", "")),
        "result": str(claim.get("result", "")),
        "evidence": str(claim.get("evidence", "")),
        "source": str(claim.get("source", "unspecified")),
    }


def reconcile_claims(
    claims: Iterable[Mapping[str, object]],
    authoritative_evidence: Mapping[str, Mapping[str, object]] | None = None,
) -> tuple[list[dict[str, str]], list[dict[str, object]]]:
    """De-duplicate claims and resolve only conflicts covered by supplied authority."""

    unique: list[dict[str, str]] = []
    seen: set[tuple[tuple[str, str], ...]] = set()
    by_item: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for claim in claims:
        normalized = _normalize_claim(claim)
        signature = tuple(sorted(normalized.items()))
        if signature in seen:
            continue
        seen.add(signature)
        unique.append(normalized)
        by_item[(normalized["page"], normalized["checklist"], normalized["id"])].append(normalized)

    authority = authoritative_evidence or {}
    conflicts: list[dict[str, object]] = []
    for (page, checklist, check_id), item_claims in sorted(by_item.items()):
        results = {claim["result"] for claim in item_claims}
        if len(results) <= 1:
            continue
        key = f"{page}:{checklist}:{check_id}"
        supplied = authority.get(key)
        authoritative: dict[str, str] | None = None
        resolution = "unresolved"
        if isinstance(supplied, Mapping):
            candidate = {
                "result": str(supplied.get("result", "")),
                "evidence": str(supplied.get("evidence", "")),
                "source": str(supplied.get("source", "")),
            }
            if (
                candidate["result"] in runner_contract.ALLOWED_RESULTS
                and candidate["result"] in results
                and candidate["evidence"].strip()
                and candidate["source"].strip()
            ):
                authoritative = candidate
                resolution = "resolved"
        conflicts.append(
            {
                "page": page,
                "checklist": checklist,
                "id": check_id,
                "claims": item_claims,
                "resolution": resolution,
                "authoritativeEvidence": authoritative,
            }
        )
    return unique, conflicts


def coordinate(
    assignments: Sequence[Assignment],
    report_attempts: Mapping[str, Sequence[object]],
    *,
    unavailable: Mapping[str, str] | Iterable[str] = (),
    extra_claims: Iterable[Mapping[str, object]] = (),
    authoritative_evidence: Mapping[str, Mapping[str, object]] | None = None,
    candidates: Sequence[Mapping[str, object]] = (),
) -> dict[str, object]:
    """Return the exact coordinator output after at most one malformed retry."""

    output = _base_output(assignments)
    if not assignments:
        output["acceptanceRationale"] = "The required assignment inventory is empty."
        return output

    keys = [assignment_key(assignment) for assignment in assignments]
    duplicate_keys = {key for key in keys if keys.count(key) > 1}
    malformed_assignments = [
        assignment
        for assignment in assignments
        if runner_contract._assignment_errors(*assignment)
    ]
    if duplicate_keys or malformed_assignments:
        missing = [
            _missing_assignment(
                assignment,
                "duplicate assignment" if assignment_key(assignment) in duplicate_keys else "malformed assignment",
            )
            for assignment in assignments
            if assignment_key(assignment) in duplicate_keys or assignment in malformed_assignments
        ]
        output["coverage"]["missing"] = missing
        output["acceptanceRationale"] = "The assignment inventory contains duplicate or malformed entries."
        return output

    unavailable_reasons = (
        dict(unavailable)
        if isinstance(unavailable, Mapping)
        else {key: "unavailable" for key in unavailable}
    )
    missing: list[dict[str, str]] = []
    runner_reports: list[dict[str, object]] = []
    findings: list[dict[str, object]] = []
    claims: list[dict[str, object]] = [dict(claim) for claim in extra_claims]

    for page, checklist, checklist_ids in assignments:
        assignment = (page, checklist, checklist_ids)
        key = assignment_key(assignment)
        if key in unavailable_reasons:
            missing.append(_missing_assignment(assignment, unavailable_reasons[key]))
            continue
        attempts = list(report_attempts.get(key, ()))[:2]
        accepted_report: dict[str, Any] | None = None
        accepted_attempt = 0
        for index, report in enumerate(attempts, start=1):
            errors = runner_contract.validate_report(
                page,
                checklist,
                checklist_ids,
                report,
            )
            if not errors:
                accepted_report = dict(report)
                accepted_attempt = index
                break
        if accepted_report is None:
            reason = "missing report" if not attempts else "malformed after one retry"
            missing.append(_missing_assignment(assignment, reason))
            continue

        report_status = str(accepted_report["status"])
        runner_reports.append(
            {
                "page": page,
                "checklist": checklist,
                "status": report_status,
                "attempts": accepted_attempt,
                "checks": [dict(item) for item in accepted_report["checks"]],
                "findings": [dict(item) for item in accepted_report["findings"]],
                "limits": [dict(item) for item in accepted_report["limits"]],
            }
        )
        for check in accepted_report["checks"]:
            claims.append(
                {
                    "page": page,
                    "checklist": checklist,
                    "id": check["id"],
                    "result": check["result"],
                    "evidence": check["evidence"],
                    "source": key,
                }
            )
        for finding in accepted_report["findings"]:
            findings.append(
                {
                    "page": page,
                    "checklist": checklist,
                    "id": finding["id"],
                    "remediation": finding["remediation"],
                    "source": key,
                }
            )

    reconciled_claims, conflicts = reconcile_claims(claims, authoritative_evidence)
    unresolved_conflicts = [item for item in conflicts if item["resolution"] == "unresolved"]
    effective_results: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    for claim in reconciled_claims:
        key = (claim["page"], claim["checklist"], claim["id"])
        effective_results[key].add(claim["result"])
    for conflict in conflicts:
        authoritative = conflict["authoritativeEvidence"]
        if conflict["resolution"] == "resolved" and authoritative:
            key = (str(conflict["page"]), str(conflict["checklist"]), str(conflict["id"]))
            effective_results[key] = {authoritative["result"]}
    has_failure = any("FAIL" in results for results in effective_results.values())
    incomplete = any("NOT TESTED" in results for results in effective_results.values())

    reconciled_findings: list[dict[str, object]] = []
    finding_index: dict[tuple[str, str, str, str], dict[str, object]] = {}
    for finding in findings:
        signature = (
            str(finding["page"]),
            str(finding["checklist"]),
            str(finding["id"]),
            str(finding["remediation"]),
        )
        if signature not in finding_index:
            record = {
                "page": signature[0],
                "checklist": signature[1],
                "id": signature[2],
                "remediation": signature[3],
                "sources": [],
            }
            finding_index[signature] = record
            reconciled_findings.append(record)
        sources = finding_index[signature]["sources"]
        source = str(finding["source"])
        if source not in sources:
            sources.append(source)

    status = "ACCEPTED"
    rationale = "Every required checklist item has complete reconciled PASS evidence."
    if missing:
        status = "BLOCKED"
        rationale = "Required runner coverage is missing or malformed."
    elif incomplete:
        status = "BLOCKED"
        rationale = "At least one required checklist item is NOT TESTED."
    elif unresolved_conflicts:
        status = "BLOCKED"
        rationale = "At least one material evidence contradiction remains unresolved."
    elif has_failure:
        status = "REJECTED"
        rationale = "Complete reconciled evidence contains a confirmed material failure."

    output.update(
        {
            "status": status,
            "coverage": {
                "required": len(assignments),
                "completed": len(runner_reports),
                "missing": missing,
            },
            "reconciledFindings": reconciled_findings,
            "evidenceConflicts": conflicts,
            "acceptanceRationale": rationale,
            "modelEvalRanking": rank_candidates(candidates)["ranking"] if candidates else [],
            "runnerReports": runner_reports,
        }
    )
    return output


def _decimal(value: object, field_name: str) -> Decimal:
    """Return one finite nonnegative Decimal without accepting binary rounding."""

    if isinstance(value, bool) or value is None:
        raise ValueError(f"{field_name} must be a finite nonnegative number")
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(f"{field_name} must be a finite nonnegative number") from None
    if not number.is_finite() or number < 0:
        raise ValueError(f"{field_name} must be a finite nonnegative number")
    return number


def estimated_cost(
    usage: Mapping[str, object],
    rates: Mapping[str, object] | None,
) -> Decimal | None:
    """Return exact supplied-rate cost after separate cached-input charging."""

    if rates is None:
        return None
    total_input = _decimal(usage.get("input_tokens"), "input_tokens")
    cached = _decimal(usage.get("cached_input_tokens"), "cached_input_tokens")
    output = _decimal(usage.get("output_tokens"), "output_tokens")
    if cached > total_input:
        raise ValueError("cached_input_tokens must not exceed input_tokens")
    input_rate = _decimal(rates.get("input_tokens"), "input_tokens rate")
    cached_rate = _decimal(rates.get("cached_input_tokens"), "cached_input_tokens rate")
    output_rate = _decimal(rates.get("output_tokens"), "output_tokens rate")
    return (
        (total_input - cached) * input_rate
        + cached * cached_rate
        + output * output_rate
    ) / Decimal(1_000_000)


def _candidate(candidate: Mapping[str, object]) -> dict[str, object]:
    """Validate and normalize one candidate while preserving null pricing."""

    candidate_id = candidate.get("id")
    if not isinstance(candidate_id, str) or not candidate_id.strip():
        raise ValueError("candidate id must be a non-empty string")
    cost_value = candidate.get("estimated_cost")
    return {
        "id": candidate_id.strip(),
        "accuracy": _decimal(candidate.get("accuracy"), "accuracy"),
        "estimated_cost": None if cost_value is None else _decimal(cost_value, "estimated_cost"),
        "wall_seconds": _decimal(candidate.get("wall_seconds"), "wall_seconds"),
    }


def _append_rank_group(
    ranked: list[dict[str, object]],
    group: Sequence[dict[str, object]],
    rank: int,
    *,
    pricing_status: str,
) -> int:
    """Append stable candidates and retain a shared rank for exact ties."""

    previous_metrics: tuple[Decimal, Decimal | None, Decimal] | None = None
    current_rank = rank
    for candidate in group:
        metrics = (
            candidate["accuracy"],
            candidate["estimated_cost"],
            candidate["wall_seconds"],
        )
        if previous_metrics is None or metrics != previous_metrics:
            current_rank = len(ranked) + 1
        ranked.append(
            {
                **candidate,
                "rank": current_rank,
                "tie": sum(
                    1
                    for peer in group
                    if (
                        peer["accuracy"],
                        peer["estimated_cost"],
                        peer["wall_seconds"],
                    )
                    == metrics
                )
                > 1,
                "pricingStatus": pricing_status,
                "provisional": pricing_status == "unpriced",
                "evidence": (
                    "Exact measured accuracy, pricing status, inclusive cost band, and wall time determine this rank."
                ),
            }
        )
        previous_metrics = metrics
    return current_rank


def rank_candidates(candidates: Sequence[Mapping[str, object]]) -> dict[str, object]:
    """Rank exact measurements with an inclusive rational 115-percent boundary."""

    normalized = [_candidate(candidate) for candidate in candidates]
    ids = [str(candidate["id"]) for candidate in normalized]
    if len(ids) != len(set(ids)):
        raise ValueError("candidate identifiers must be unique")

    ranked: list[dict[str, object]] = []
    for accuracy in sorted({candidate["accuracy"] for candidate in normalized}, reverse=True):
        peers = [candidate for candidate in normalized if candidate["accuracy"] == accuracy]
        priced = [candidate for candidate in peers if candidate["estimated_cost"] is not None]
        unpriced = [candidate for candidate in peers if candidate["estimated_cost"] is None]
        while priced:
            cheapest = min(candidate["estimated_cost"] for candidate in priced)
            boundary = cheapest * Decimal(115) / Decimal(100)
            band = [candidate for candidate in priced if candidate["estimated_cost"] <= boundary]
            priced = [candidate for candidate in priced if candidate not in band]
            band.sort(key=lambda candidate: (candidate["wall_seconds"], candidate["estimated_cost"], candidate["id"]))
            _append_rank_group(ranked, band, len(ranked) + 1, pricing_status="priced")
        unpriced.sort(key=lambda candidate: (candidate["wall_seconds"], candidate["id"]))
        _append_rank_group(ranked, unpriced, len(ranked) + 1, pricing_status="unpriced")

    return {
        "ranking": ranked,
        "winner_provisional": bool(ranked and ranked[0]["pricingStatus"] == "unpriced"),
    }
