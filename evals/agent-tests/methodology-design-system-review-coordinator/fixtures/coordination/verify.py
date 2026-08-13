"""
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
AI attribution: Generated with AI assistance.
Responsibility: Executes the deterministic coordinator check against every fixture boundary.
Design: TASK.md
Tests: evals/agent-tests/methodology-design-system-review-coordinator/test_coordination_simulator.py
"""

from __future__ import annotations

from decimal import Decimal
import importlib.util
import json
from pathlib import Path
from typing import Any

import yaml


FIXTURE_PATH = Path(__file__).with_name("coordination-inputs.yaml")
SIMULATOR_PATH = Path(__file__).resolve().parents[2] / "coordination_simulator.py"


def _load_simulator() -> Any:
    """Load the coordinator simulator from the suite under test."""

    spec = importlib.util.spec_from_file_location(
        "documentation_design_system_coordination_fixture_checker",
        SIMULATOR_PATH,
    )
    if spec is None or spec.loader is None:
        raise SystemExit("coordinator simulator could not be loaded")
    simulator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(simulator)
    return simulator


def _assignment(payload: dict[str, object]) -> tuple[str, str, tuple[str, ...]]:
    """Convert the exact fixture assignment to the simulator contract."""

    return (
        str(payload["page"]),
        str(payload["checklist"]),
        tuple(str(check_id) for check_id in payload["checklistIds"]),
    )


def _report(
    assignment: tuple[str, str, tuple[str, ...]],
    results: list[str] | tuple[str, ...] | None = None,
) -> dict[str, object]:
    """Build one strict runner report from fixture results."""

    page, checklist, checklist_ids = assignment
    item_results = list(results or ("PASS" for _ in checklist_ids))
    status = (
        "NOT TESTED"
        if "NOT TESTED" in item_results
        else "FAIL"
        if "FAIL" in item_results
        else "PASS"
    )
    return {
        "status": status,
        "page": page,
        "checklist": checklist,
        "checks": [
            {
                "id": check_id,
                "result": result,
                "evidence": f"fixture evidence for {check_id}",
            }
            for check_id, result in zip(checklist_ids, item_results, strict=True)
        ],
        "findings": [
            {"id": check_id, "remediation": f"Correct {check_id}."}
            for check_id, result in zip(checklist_ids, item_results, strict=True)
            if result == "FAIL"
        ],
        "limits": [
            {"id": check_id, "missingEvidence": f"Obtain evidence for {check_id}."}
            for check_id, result in zip(checklist_ids, item_results, strict=True)
            if result == "NOT TESTED"
        ],
    }


def _candidate(candidate: dict[str, object]) -> dict[str, object]:
    """Map fixture-facing measurement names to the simulator contract."""

    return {
        "id": candidate["id"],
        "accuracy": candidate["accuracy"],
        "estimated_cost": candidate["estimatedCost"],
        "wall_seconds": candidate["wallSeconds"],
    }


def _expect(actual: object, expected: object, label: str) -> None:
    """Stop with a focused fixture failure when an expected result is not observed."""

    if actual != expected:
        raise SystemExit(f"{label}: expected {expected!r}, got {actual!r}")


def main() -> int:
    """Run coordination, conflict, ranking, numeric, and cache counterexamples."""

    payload = yaml.safe_load(FIXTURE_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("coordination fixture must be an object")
    _expect(
        payload.get("schema"),
        "dev-methodology-documentation-design-system-coordination-inputs",
        "fixture schema",
    )
    _expect(payload.get("version"), 2, "fixture version")
    simulator = _load_simulator()
    assignment = _assignment(payload["assignment"])
    assignment_key = simulator.assignment_key(assignment)
    complete_report = _report(assignment)
    malformed_report = {**complete_report, "checks": []}

    coordination_cases = payload["coordinationCases"]
    for case_name in ("malformedThenComplete", "retryExhaustion"):
        case = coordination_cases[case_name]
        reports_by_kind = {"malformed": malformed_report, "complete": complete_report}
        attempts = [reports_by_kind[kind] for kind in case["attemptKinds"]]
        output = simulator.coordinate((assignment,), {assignment_key: attempts})
        _expect(output["status"], case["expectedStatus"], f"{case_name} status")
        if "expectedAttempts" in case:
            _expect(
                output["runnerReports"][0]["attempts"],
                case["expectedAttempts"],
                f"{case_name} attempt count",
            )
        if "expectedMissingReason" in case:
            _expect(
                output["coverage"]["missing"][0]["reason"],
                case["expectedMissingReason"],
                f"{case_name} missing reason",
            )
        json.dumps(output, allow_nan=False)

    malformed_case = coordination_cases["malformedAssignment"]
    malformed_output = simulator.coordinate((malformed_case["assignment"],), {})
    _expect(malformed_output["status"], malformed_case["expectedStatus"], "malformed assignment status")
    _expect(
        malformed_output["acceptanceRationale"],
        malformed_case["expectedRationale"],
        "malformed assignment pre-dispatch rationale",
    )

    for case_name in ("unavailable", "timeout", "cancelled"):
        case = coordination_cases[case_name]
        output = simulator.coordinate(
            (assignment,),
            {},
            unavailable={assignment_key: case["reason"]},
        )
        _expect(output["status"], case["expectedStatus"], f"{case_name} status")
        _expect(output["coverage"]["missing"][0]["reason"], case["reason"], f"{case_name} reason")

    for case_name, case in payload["conflictCases"].items():
        authority = case.get("authoritativeEvidence")
        output = simulator.coordinate(
            (assignment,),
            {assignment_key: [_report(assignment, case["runnerResults"])]},
            extra_claims=case["extraClaims"],
            authoritative_evidence=authority,
        )
        _expect(output["status"], case["expectedStatus"], f"{case_name} status")
        _expect(len(output["reconciledFindings"]), case["expectedFindings"], f"{case_name} findings")
        _expect(
            output["evidenceConflicts"][0]["resolution"],
            case["expectedResolution"],
            f"{case_name} resolution",
        )
        _expect(len(output["evidenceConflicts"][0]["claims"]), 2, f"{case_name} raw claims")
        json.dumps(output, allow_nan=False)

    for case_name, case in payload["rankingCases"].items():
        result = simulator.rank_candidates(tuple(_candidate(item) for item in case["candidates"]))
        ranking = result["ranking"]
        _expect([item["id"] for item in ranking], case["expectedOrder"], f"{case_name} order")
        if "expectedWinnerProvisional" in case:
            _expect(
                result["winner_provisional"],
                case["expectedWinnerProvisional"],
                f"{case_name} provisional winner",
            )
        tie_ids = set(case.get("expectedTieIds", []))
        _expect(
            {item["id"] for item in ranking if item["tie"]},
            tie_ids,
            f"{case_name} exact ties",
        )
        json.dumps(result, allow_nan=False)

    invalid = payload["invalidMeasurements"]
    for candidate in invalid["candidates"]:
        try:
            simulator.rank_candidates((_candidate(candidate),))
        except ValueError:
            pass
        else:
            raise SystemExit(f"invalidMeasurements accepted {candidate['id']}")
    try:
        simulator.estimated_cost(invalid["cachedUsage"], payload["cachedAccounting"]["rates"])
    except ValueError:
        pass
    else:
        raise SystemExit("invalidMeasurements accepted cached tokens above total input")

    cached = payload["cachedAccounting"]
    _expect(
        simulator.estimated_cost(cached["usage"], cached["rates"]),
        Decimal(cached["expectedCost"]),
        "cachedAccounting exact cost",
    )
    print("coordination fixture check: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
