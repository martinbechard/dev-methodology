"""
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
AI attribution: Generated with AI assistance.
Responsibility: Simulates strict report validation, evidence reconciliation, acceptance, exact pricing, and ranking for the design-system coordinator.
Design: agents/roles/methodology-maintenance/methodology-design-system-review-coordinator.role.yaml
Tests: evals/agent-tests/methodology-design-system-review-coordinator/test_coordination_simulator.py
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Sequence
from decimal import Decimal, InvalidOperation
import importlib.util
import math
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


def _is_sequence(value: object) -> bool:
    """Return whether a value is a non-text sequence safe for bounded iteration."""

    return isinstance(value, Sequence) and not isinstance(value, (str, bytes))


def _normalize_assignment(assignment: object) -> Assignment:
    """Return one exact typed assignment or a bounded validation error."""

    if not _is_sequence(assignment) or len(assignment) != 3:
        raise ValueError("assignment must contain exactly page, checklist, and checklist IDs")
    page, checklist, checklist_ids = assignment
    errors = runner_contract._assignment_errors(page, checklist, checklist_ids)
    if errors:
        raise ValueError("; ".join(errors))
    return page, checklist, tuple(checklist_ids)


def assignment_key(assignment: object) -> str:
    """Return the stable page-checklist key for one validated assignment."""

    page, checklist, _ = _normalize_assignment(assignment)
    return f"{page}:{checklist}"


def _missing_assignment(assignment: Assignment, reason: str) -> dict[str, str]:
    """Return one exact missing-coverage record."""

    page, checklist, _ = assignment
    return {"page": page, "checklist": checklist, "reason": reason}


def _invalid_assignment_record(index: int, assignment: object, reason: str) -> dict[str, str]:
    """Return schema-valid evidence for a malformed pre-dispatch assignment."""

    page = f"assignment[{index}]"
    checklist = "invalid assignment"
    if _is_sequence(assignment):
        if len(assignment) > 0 and isinstance(assignment[0], str) and assignment[0].strip():
            page = assignment[0]
        if len(assignment) > 1 and isinstance(assignment[1], str) and assignment[1].strip():
            checklist = assignment[1]
    return {"page": page, "checklist": checklist, "reason": reason}


def _base_output(required: int) -> dict[str, object]:
    """Create every coordinator output field with its exact nested container type."""

    return {
        "status": "BLOCKED",
        "coverage": {"required": required, "completed": 0, "missing": []},
        "reconciledFindings": [],
        "evidenceConflicts": [],
        "acceptanceRationale": "Required evidence is incomplete.",
        "modelEvalRanking": [],
        "runnerReports": [],
    }


def _normalize_claim(claim: object) -> dict[str, str]:
    """Normalize a material claim without discarding its source."""

    required = {"page", "checklist", "id", "result", "evidence", "source"}
    if not isinstance(claim, Mapping) or set(claim) != required:
        raise ValueError("each material claim must contain exactly page, checklist, id, result, evidence, and source")
    normalized: dict[str, str] = {}
    for field in ("page", "checklist", "id", "evidence", "source"):
        value = claim[field]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"material claim {field} must be a non-empty string")
        normalized[field] = value
    result = claim["result"]
    if not isinstance(result, str) or result not in runner_contract.ALLOWED_RESULTS:
        raise ValueError("material claim result is invalid")
    normalized["result"] = result
    return normalized


def _normalize_authoritative_entry(entry: object) -> dict[str, object]:
    """Return one exact authoritative resolution or a bounded validation error."""

    if not isinstance(entry, Mapping):
        raise ValueError("each authoritative evidence entry must be an object")
    base_fields = {"result", "evidence", "source"}
    allowed_fields = {*base_fields, "remediation"}
    if not base_fields <= set(entry) <= allowed_fields:
        raise ValueError(
            "each authoritative evidence entry must contain result, evidence, source, and only optional remediation"
        )
    result = entry["result"]
    evidence = entry["evidence"]
    source = entry["source"]
    remediation = entry.get("remediation")
    if not isinstance(result, str) or result not in runner_contract.ALLOWED_RESULTS:
        raise ValueError("authoritative evidence result is invalid")
    if not isinstance(evidence, str) or not evidence.strip():
        raise ValueError("authoritative evidence must be a non-empty string")
    if not isinstance(source, str) or not source.strip():
        raise ValueError("authoritative evidence source must be a non-empty string")
    if result == "FAIL":
        if not isinstance(remediation, str) or not remediation.strip():
            raise ValueError("authoritative FAIL evidence requires non-empty remediation")
    elif remediation is not None:
        raise ValueError("authoritative non-FAIL evidence must not contain remediation")
    return {
        "result": result,
        "evidence": evidence,
        "source": source,
        "remediation": remediation,
    }


def reconcile_claims(
    claims: object,
    authoritative_evidence: object = None,
) -> tuple[list[dict[str, str]], list[dict[str, object]]]:
    """De-duplicate claims and resolve only conflicts covered by supplied authority."""

    if not _is_sequence(claims):
        raise ValueError("material claims must be a sequence")
    if authoritative_evidence is None:
        raw_authority: Mapping[object, object] = {}
    elif isinstance(authoritative_evidence, Mapping):
        raw_authority = authoritative_evidence
    else:
        raise ValueError("authoritative evidence must be an object or null")
    if any(not isinstance(key, str) or not key.strip() for key in raw_authority):
        raise ValueError("authoritative evidence keys must be non-empty strings")
    authority = {
        key: _normalize_authoritative_entry(entry)
        for key, entry in raw_authority.items()
    }

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

    conflicts: list[dict[str, object]] = []
    for (page, checklist, check_id), item_claims in sorted(by_item.items()):
        results = {claim["result"] for claim in item_claims}
        if len(results) <= 1:
            continue
        key = f"{page}:{checklist}:{check_id}"
        supplied = authority.get(key)
        authoritative: dict[str, object] | None = None
        resolution = "unresolved"
        if supplied is not None and supplied["result"] in results:
            authoritative = supplied
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
    conflict_keys = {
        f"{conflict['page']}:{conflict['checklist']}:{conflict['id']}"
        for conflict in conflicts
    }
    unused_authority = sorted(set(authority) - conflict_keys)
    if unused_authority:
        raise ValueError(
            f"authoritative evidence does not match a material conflict: {unused_authority}"
        )
    return unique, conflicts


def coordinate(
    assignments: object,
    report_attempts: object,
    *,
    unavailable: object = (),
    extra_claims: object = (),
    authoritative_evidence: object = None,
    candidates: object = (),
) -> dict[str, object]:
    """Return the exact coordinator output after at most one malformed retry."""

    if not _is_sequence(assignments):
        output = _base_output(0)
        output["acceptanceRationale"] = "The assignment inventory is malformed."
        return output
    raw_assignments = list(assignments)
    output = _base_output(len(raw_assignments))
    if not raw_assignments:
        output["acceptanceRationale"] = "The required assignment inventory is empty."
        return output

    normalized_assignments: list[Assignment] = []
    invalid_assignments: list[dict[str, str]] = []
    for index, assignment in enumerate(raw_assignments, start=1):
        try:
            normalized_assignments.append(_normalize_assignment(assignment))
        except ValueError as error:
            invalid_assignments.append(
                _invalid_assignment_record(index, assignment, str(error))
            )
    if invalid_assignments:
        output["coverage"]["missing"] = invalid_assignments
        output["acceptanceRationale"] = (
            "The assignment inventory contains malformed identity before dispatch."
        )
        return output

    keys = [assignment_key(assignment) for assignment in normalized_assignments]
    duplicate_keys = {key for key in keys if keys.count(key) > 1}
    if duplicate_keys:
        missing = [
            _missing_assignment(assignment, "duplicate assignment")
            for assignment in normalized_assignments
            if assignment_key(assignment) in duplicate_keys
        ]
        output["coverage"]["missing"] = missing
        output["acceptanceRationale"] = (
            "The assignment inventory contains duplicate identity before dispatch."
        )
        return output

    known_keys = set(keys)
    if not isinstance(report_attempts, Mapping):
        output["coverage"]["missing"] = [
            _missing_assignment(assignment, "malformed report-attempt inventory")
            for assignment in normalized_assignments
        ]
        output["acceptanceRationale"] = "The report-attempt inventory is malformed."
        return output
    attempt_inventory_error = any(
        not isinstance(key, str)
        or not key.strip()
        or key not in known_keys
        or not _is_sequence(value)
        or len(value) > 2
        for key, value in report_attempts.items()
    )
    if attempt_inventory_error:
        output["coverage"]["missing"] = [
            _missing_assignment(assignment, "malformed report-attempt inventory")
            for assignment in normalized_assignments
        ]
        output["acceptanceRationale"] = "The report-attempt inventory is malformed."
        return output

    unavailable_reasons: dict[str, str] = {}
    if isinstance(unavailable, Mapping):
        for key, reason in unavailable.items():
            if (
                not isinstance(key, str)
                or key not in known_keys
                or not isinstance(reason, str)
                or not reason.strip()
            ):
                output["coverage"]["missing"] = [
                    _missing_assignment(assignment, "malformed unavailable-runner inventory")
                    for assignment in normalized_assignments
                ]
                output["acceptanceRationale"] = "The unavailable-runner inventory is malformed."
                return output
            unavailable_reasons[key] = reason
    elif _is_sequence(unavailable):
        for key in unavailable:
            if not isinstance(key, str) or key not in known_keys:
                output["coverage"]["missing"] = [
                    _missing_assignment(assignment, "malformed unavailable-runner inventory")
                    for assignment in normalized_assignments
                ]
                output["acceptanceRationale"] = "The unavailable-runner inventory is malformed."
                return output
            unavailable_reasons[key] = "unavailable"
    else:
        output["coverage"]["missing"] = [
            _missing_assignment(assignment, "malformed unavailable-runner inventory")
            for assignment in normalized_assignments
        ]
        output["acceptanceRationale"] = "The unavailable-runner inventory is malformed."
        return output

    if not _is_sequence(extra_claims):
        output["acceptanceRationale"] = "The material-claim inventory is malformed."
        return output
    try:
        normalized_extra_claims = [_normalize_claim(claim) for claim in extra_claims]
    except ValueError:
        output["acceptanceRationale"] = "The material-claim inventory is malformed."
        return output
    assigned_items = {
        (page, checklist, check_id)
        for page, checklist, checklist_ids in normalized_assignments
        for check_id in checklist_ids
    }
    if any(
        (claim["page"], claim["checklist"], claim["id"]) not in assigned_items
        for claim in normalized_extra_claims
    ):
        output["acceptanceRationale"] = "The material-claim inventory is outside the assignment boundary."
        return output
    if authoritative_evidence is not None and not isinstance(
        authoritative_evidence,
        Mapping,
    ):
        output["acceptanceRationale"] = "The authoritative-evidence inventory is malformed."
        return output
    if not _is_sequence(candidates):
        output["acceptanceRationale"] = "The candidate inventory is malformed."
        return output

    missing: list[dict[str, str]] = []
    runner_reports: list[dict[str, object]] = []
    findings: list[dict[str, object]] = []
    claims: list[dict[str, object]] = [dict(claim) for claim in normalized_extra_claims]

    for page, checklist, checklist_ids in normalized_assignments:
        assignment = (page, checklist, checklist_ids)
        key = assignment_key(assignment)
        if key in unavailable_reasons:
            missing.append(_missing_assignment(assignment, unavailable_reasons[key]))
            continue
        attempts = list(report_attempts.get(key, ()))
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

    try:
        reconciled_claims, conflicts = reconcile_claims(
            claims,
            authoritative_evidence,
        )
    except ValueError:
        output["coverage"] = {
            "required": len(normalized_assignments),
            "completed": len(runner_reports),
            "missing": missing,
        }
        output["runnerReports"] = runner_reports
        output["acceptanceRationale"] = "The evidence-reconciliation inventory is malformed."
        return output
    unresolved_conflicts = [item for item in conflicts if item["resolution"] == "unresolved"]
    raw_results: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    for claim in reconciled_claims:
        key = (claim["page"], claim["checklist"], claim["id"])
        raw_results[key].add(claim["result"])
    conflict_by_item = {
        (str(conflict["page"]), str(conflict["checklist"]), str(conflict["id"])): conflict
        for conflict in conflicts
    }
    effective_results: dict[tuple[str, str, str], str] = {}
    resolved_authority: dict[tuple[str, str, str], Mapping[str, object]] = {}
    for key, results in raw_results.items():
        conflict = conflict_by_item.get(key)
        if conflict is None:
            if len(results) == 1:
                effective_results[key] = next(iter(results))
            continue
        authoritative = conflict["authoritativeEvidence"]
        if conflict["resolution"] == "resolved" and isinstance(authoritative, Mapping):
            effective_results[key] = str(authoritative["result"])
            resolved_authority[key] = authoritative
    has_failure = "FAIL" in effective_results.values()
    incomplete = "NOT TESTED" in effective_results.values()

    reconciled_findings: list[dict[str, object]] = []
    finding_index: dict[tuple[str, str, str, str], dict[str, object]] = {}
    effective_finding_inputs: list[dict[str, object]] = []
    for finding in findings:
        item_key = (
            str(finding["page"]),
            str(finding["checklist"]),
            str(finding["id"]),
        )
        if effective_results.get(item_key) == "FAIL" and item_key not in resolved_authority:
            effective_finding_inputs.append(finding)
    for item_key, authoritative in resolved_authority.items():
        if effective_results[item_key] == "FAIL":
            effective_finding_inputs.append(
                {
                    "page": item_key[0],
                    "checklist": item_key[1],
                    "id": item_key[2],
                    "remediation": authoritative["remediation"],
                    "source": authoritative["source"],
                }
            )
    for finding in effective_finding_inputs:
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

    ranking: list[dict[str, object]] = []
    ranking_error = False
    try:
        ranking = rank_candidates(candidates)["ranking"] if candidates else []
    except ValueError:
        ranking_error = True

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
    elif ranking_error:
        status = "BLOCKED"
        rationale = "The candidate measurement or pricing inventory is invalid."
    elif has_failure:
        status = "REJECTED"
        rationale = "Complete reconciled evidence contains a confirmed material failure."

    output.update(
        {
            "status": status,
            "coverage": {
                "required": len(normalized_assignments),
                "completed": len(runner_reports),
                "missing": missing,
            },
            "reconciledFindings": reconciled_findings,
            "evidenceConflicts": conflicts,
            "acceptanceRationale": rationale,
            "modelEvalRanking": ranking,
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
    usage: object,
    rates: object,
) -> Decimal | None:
    """Return exact supplied-rate cost after separate cached-input charging."""

    if rates is None:
        return None
    expected_fields = {"input_tokens", "cached_input_tokens", "output_tokens"}
    if not isinstance(usage, Mapping) or set(usage) != expected_fields:
        raise ValueError("usage must contain exact token-count fields")
    if not isinstance(rates, Mapping) or set(rates) != expected_fields:
        raise ValueError("rates must contain exact token-price fields")
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


def _candidate(candidate: object) -> dict[str, object]:
    """Validate and normalize one candidate while preserving null pricing."""

    expected_fields = {"id", "accuracy", "estimated_cost", "wall_seconds"}
    if not isinstance(candidate, Mapping) or set(candidate) != expected_fields:
        raise ValueError("candidate must contain exact identity and measurement fields")
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


def _json_number(number: Decimal) -> float:
    """Convert an internally exact Decimal to a finite standard-JSON number."""

    converted = float(number)
    if not math.isfinite(converted):
        raise ValueError("numeric measurement is outside the standard-JSON number range")
    return converted


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
                "id": candidate["id"],
                "accuracy": _json_number(candidate["accuracy"]),
                "estimated_cost": (
                    None
                    if candidate["estimated_cost"] is None
                    else _json_number(candidate["estimated_cost"])
                ),
                "wall_seconds": _json_number(candidate["wall_seconds"]),
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


def rank_candidates(candidates: object) -> dict[str, object]:
    """Rank exact measurements with an inclusive rational 115-percent boundary."""

    if not _is_sequence(candidates):
        raise ValueError("candidates must be a sequence")
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
