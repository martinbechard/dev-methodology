"""
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
AI attribution: Generated with AI assistance.
Responsibility: Validates one strict Documentation Design System checklist-runner report against its assigned item IDs.
Design: agents/roles/methodology-maintenance/methodology-design-system-checklist-runner.role.yaml
Tests: evals/agent-tests/methodology-design-system-checklist-runner/test_contract.py
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from typing import Any


ALLOWED_RESULTS = frozenset({"PASS", "FAIL", "NOT TESTED"})
REQUIRED_FIELDS = frozenset({"status", "page", "checklist", "checks", "findings", "limits"})


def validate_report(checklist_ids: Sequence[str], report: dict[str, Any]) -> tuple[str, ...]:
    """Return deterministic contract errors for one page-checklist report.

    The caller supplies the ordered checklist identifiers and an untrusted report.
    Validation is read-only. The function reports every missing, duplicate, extra,
    malformed, or status-inconsistent result without repairing the report.
    """

    errors: list[str] = []
    if set(report) != REQUIRED_FIELDS:
        errors.append("report fields must match the strict output contract")
    checks = report.get("checks")
    if not isinstance(checks, list):
        return (*errors, "checks must be a list")

    observed_ids: list[str] = []
    observed_results: list[str] = []
    for check in checks:
        if not isinstance(check, dict) or set(check) != {"id", "result", "evidence"}:
            errors.append("each check must contain only id, result, and evidence")
            continue
        check_id = check.get("id")
        result = check.get("result")
        evidence = check.get("evidence")
        if not isinstance(check_id, str) or not check_id:
            errors.append("check id must be a non-empty string")
            continue
        observed_ids.append(check_id)
        if result not in ALLOWED_RESULTS:
            errors.append(f"{check_id} has an invalid result")
        else:
            observed_results.append(result)
        if not isinstance(evidence, str) or not evidence.strip():
            errors.append(f"{check_id} lacks page-specific evidence")

    expected_counts = Counter(checklist_ids)
    observed_counts = Counter(observed_ids)
    if any(count != 1 for count in expected_counts.values()):
        errors.append("assigned checklist identifiers must be unique")
    for check_id in checklist_ids:
        if observed_counts[check_id] == 0:
            errors.append(f"missing checklist item {check_id}")
        elif observed_counts[check_id] > 1:
            errors.append(f"duplicate checklist item {check_id}")
    for check_id in observed_counts.keys() - expected_counts.keys():
        errors.append(f"unexpected checklist item {check_id}")

    expected_status = "PASS"
    if "FAIL" in observed_results:
        expected_status = "FAIL"
    elif "NOT TESTED" in observed_results:
        expected_status = "NOT TESTED"
    if report.get("status") != expected_status:
        errors.append(f"status must be {expected_status}")
    return tuple(errors)
