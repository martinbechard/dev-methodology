"""
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
AI attribution: Generated with AI assistance.
Responsibility: Validates one strict Documentation Design System checklist-runner report against its exact assignment.
Design: agents/roles/methodology-maintenance/methodology-design-system-checklist-runner.role.yaml
Tests: evals/agent-tests/methodology-design-system-checklist-runner/test_contract.py
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from typing import Any


ALLOWED_RESULTS = frozenset({"PASS", "FAIL", "NOT TESTED"})
REQUIRED_FIELDS = frozenset({"status", "page", "checklist", "checks", "findings", "limits"})


def _assignment_errors(
    expected_page: object,
    expected_checklist: object,
    checklist_ids: object,
) -> list[str]:
    """Return errors in the coordinator-owned assignment inventory."""

    errors: list[str] = []
    if not isinstance(expected_page, str) or not expected_page.strip():
        errors.append("assigned page must be a non-empty string")
    if not isinstance(expected_checklist, str) or not expected_checklist.strip():
        errors.append("assigned checklist must be a non-empty string")
    if not isinstance(checklist_ids, Sequence) or isinstance(checklist_ids, (str, bytes)):
        return [*errors, "assigned checklist identifiers must be a sequence"]
    if not checklist_ids:
        errors.append("assigned checklist identifiers must not be empty")
    valid_identifiers = all(
        isinstance(check_id, str) and bool(check_id.strip())
        for check_id in checklist_ids
    )
    if not valid_identifiers:
        errors.append("assigned checklist identifiers must be non-empty strings")
    elif len(checklist_ids) != len(set(checklist_ids)):
        errors.append("assigned checklist identifiers must be unique")
    return errors


def build_not_tested_report(
    expected_page: str,
    expected_checklist: str,
    checklist_ids: Sequence[str],
    missing_evidence: str,
) -> dict[str, object]:
    """Represent unavailable review evidence after preserving exact expected inventory."""

    errors = _assignment_errors(expected_page, expected_checklist, checklist_ids)
    if errors:
        raise ValueError("; ".join(errors))
    if not isinstance(missing_evidence, str) or not missing_evidence.strip():
        raise ValueError("missing evidence must be a non-empty string")
    reason = missing_evidence.strip()
    return {
        "status": "NOT TESTED",
        "page": expected_page,
        "checklist": expected_checklist,
        "checks": [
            {"id": check_id, "result": "NOT TESTED", "evidence": reason}
            for check_id in checklist_ids
        ],
        "findings": [],
        "limits": [
            {"id": check_id, "missingEvidence": reason}
            for check_id in checklist_ids
        ],
    }


def _validate_item_records(
    value: object,
    *,
    field_name: str,
    detail_field: str,
) -> tuple[list[str], Counter[str]]:
    """Validate findings or limits and return their checklist-ID counts."""

    if not isinstance(value, list):
        return [f"{field_name} must be a list"], Counter()
    errors: list[str] = []
    ids: list[str] = []
    expected_fields = {"id", detail_field}
    for item in value:
        if not isinstance(item, dict) or set(item) != expected_fields:
            errors.append(f"each {field_name} item must contain only id and {detail_field}")
            continue
        item_id = item.get("id")
        detail = item.get(detail_field)
        if not isinstance(item_id, str) or not item_id.strip():
            errors.append(f"{field_name} item id must be a non-empty string")
            continue
        ids.append(item_id)
        if not isinstance(detail, str) or not detail.strip():
            errors.append(f"{field_name} item {item_id} needs non-empty {detail_field}")
    return errors, Counter(ids)


def validate_report(
    expected_page: str,
    expected_checklist: str,
    checklist_ids: Sequence[str],
    report: object,
) -> tuple[str, ...]:
    """Return deterministic errors for one exact page-checklist report."""

    errors = _assignment_errors(expected_page, expected_checklist, checklist_ids)
    if errors:
        return tuple(errors)
    if not isinstance(report, dict):
        return (*errors, "report must be an object")
    if set(report) != REQUIRED_FIELDS:
        errors.append("report fields must match the strict output contract")
    if report.get("page") != expected_page:
        errors.append("page must match the assigned page")
    if report.get("checklist") != expected_checklist:
        errors.append("checklist must match the assigned checklist")

    checks = report.get("checks")
    if not isinstance(checks, list):
        checks = []
        errors.append("checks must be a list")

    observed_ids: list[str] = []
    result_by_id: dict[str, str] = {}
    for check in checks:
        if not isinstance(check, dict) or set(check) != {"id", "result", "evidence"}:
            errors.append("each check must contain only id, result, and evidence")
            continue
        check_id = check.get("id")
        result = check.get("result")
        evidence = check.get("evidence")
        if not isinstance(check_id, str) or not check_id.strip():
            errors.append("check id must be a non-empty string")
            continue
        observed_ids.append(check_id)
        if not isinstance(result, str) or result not in ALLOWED_RESULTS:
            errors.append(f"{check_id} has an invalid result")
        else:
            result_by_id[check_id] = result
        if not isinstance(evidence, str) or not evidence.strip():
            errors.append(f"{check_id} lacks page-specific evidence")

    expected_counts = Counter(checklist_ids)
    observed_counts = Counter(observed_ids)
    for check_id in checklist_ids:
        if observed_counts[check_id] == 0:
            errors.append(f"missing checklist item {check_id}")
        elif observed_counts[check_id] > 1:
            errors.append(f"duplicate checklist item {check_id}")
    for check_id in observed_counts.keys() - expected_counts.keys():
        errors.append(f"unexpected checklist item {check_id}")

    finding_errors, finding_counts = _validate_item_records(
        report.get("findings"),
        field_name="findings",
        detail_field="remediation",
    )
    limit_errors, limit_counts = _validate_item_records(
        report.get("limits"),
        field_name="limits",
        detail_field="missingEvidence",
    )
    errors.extend(finding_errors)
    errors.extend(limit_errors)
    for check_id, result in result_by_id.items():
        if result == "FAIL" and finding_counts[check_id] < 1:
            errors.append(f"FAIL item {check_id} needs an actionable finding")
        if result != "FAIL" and finding_counts[check_id]:
            errors.append(f"non-FAIL item {check_id} must not have a finding")
        if result == "NOT TESTED" and limit_counts[check_id] < 1:
            errors.append(f"NOT TESTED item {check_id} needs a missing-evidence limit")
        if result != "NOT TESTED" and limit_counts[check_id]:
            errors.append(f"tested item {check_id} must not have a limit")
    for check_id in finding_counts.keys() - result_by_id.keys():
        errors.append(f"finding references unknown checklist item {check_id}")
    for check_id in limit_counts.keys() - result_by_id.keys():
        errors.append(f"limit references unknown checklist item {check_id}")

    observed_results = set(result_by_id.values())
    expected_status = "PASS"
    if "NOT TESTED" in observed_results:
        expected_status = "NOT TESTED"
    elif "FAIL" in observed_results:
        expected_status = "FAIL"
    if report.get("status") != expected_status:
        errors.append(f"status must be {expected_status}")
    return tuple(errors)
