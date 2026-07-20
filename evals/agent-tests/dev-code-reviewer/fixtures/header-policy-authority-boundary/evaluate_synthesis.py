#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Evaluates structured review semantics and binds passing evidence to exact capture and oracle identities.

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


FIXTURE_ROOT = Path(__file__).resolve().parent
EXPECTED_RESULTS = FIXTURE_ROOT / "expected-results.json"
EVALUATOR = Path(__file__).resolve()
EVALUATION_SCHEMA = "dev-code-reviewer-authority-evaluation"
VERIFICATION_SCHEMA = "dev-code-reviewer-authority-evaluation-verification"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_object(path: Path) -> dict[str, Any]:
    return _decode_object(path.read_bytes(), path.as_posix())


def _decode_object(payload: bytes, identity: str) -> dict[str, Any]:
    loaded = json.loads(payload)
    if not isinstance(loaded, dict):
        raise ValueError(f"JSON document must be an object: {identity}")
    return loaded


def _matches_semantics(observed: object, expected: object) -> bool:
    """Return whether observed contains the independently expected semantic structure."""
    if isinstance(expected, dict):
        return isinstance(observed, dict) and all(
            key in observed and _matches_semantics(observed[key], value)
            for key, value in expected.items()
        )
    return observed == expected


def _matching_item(items: list[object], expected: dict[str, object]) -> bool:
    return any(_matches_semantics(item, expected) for item in items)


def _explicit_policy_errors(
    findings: list[object], expected: dict[str, object]
) -> list[str]:
    errors: list[str] = []
    if len(findings) != 1:
        errors.append("explicit-policy synthesis must contain exactly one confirmed finding")

    without_contradiction = {
        key: value for key, value in expected.items() if key != "contradiction"
    }
    base_matches = [
        finding
        for finding in findings
        if _matches_semantics(finding, without_contradiction)
    ]
    if not base_matches:
        errors.append("required structured confirmed finding is missing")
        return errors

    finding = base_matches[0]
    if not isinstance(finding, dict) or "contradiction" not in finding:
        errors.append("explicit observed contradiction is missing")
    elif not _matches_semantics(finding["contradiction"], expected["contradiction"]):
        errors.append("explicit observed contradiction does not match the fixture facts")
    return errors


def _evaluate(
    case_id: str,
    observed: dict[str, Any],
    expectation_document: dict[str, Any],
) -> list[str]:
    expected_cases = expectation_document.get("cases")
    if not isinstance(expected_cases, dict) or case_id not in expected_cases:
        return [f"unknown evaluation case: {case_id}"]
    expected = expected_cases[case_id]
    if not isinstance(expected, dict):
        return [f"evaluation case must be an object: {case_id}"]

    findings = observed.get("confirmedFindings")
    questions = observed.get("openQuestions")
    residual_risk = observed.get("residualRisk", [])
    if (
        not isinstance(findings, list)
        or not isinstance(questions, list)
        or not isinstance(residual_risk, list)
    ):
        return [
            "captured synthesis must contain confirmedFindings and openQuestions arrays, "
            "with residualRisk as an array when present"
        ]

    if case_id == "absent-header-policy":
        errors = []
        if findings:
            errors.append("unsupported confirmed finding was promoted without authority")
        if len(questions) != 1:
            errors.append("missing authority must appear in exactly one openQuestions item")
        required_question = expected.get("requiredOpenQuestion")
        if not isinstance(required_question, dict) or not _matching_item(
            questions, required_question
        ):
            errors.append("missing-policy structured uncertainty was not preserved")
        elif _matching_item(residual_risk, required_question):
            errors.append("missing-policy uncertainty must not be duplicated in residualRisk")
        return errors

    required_finding = expected.get("requiredFinding")
    if not isinstance(required_finding, dict):
        return ["explicit-policy semantic expectation is missing"]
    return _explicit_policy_errors(findings, required_finding)


def _bindings(
    case_id: str,
    candidate_payload: bytes,
    expectation_payload: bytes,
) -> dict[str, str]:
    return {
        "case": case_id,
        "capturedSynthesisSha256": hashlib.sha256(candidate_payload).hexdigest(),
        "evaluatorIdentity": EVALUATOR.name,
        "evaluatorSha256": _sha256(EVALUATOR),
        "expectationsIdentity": EXPECTED_RESULTS.name,
        "expectationsSha256": hashlib.sha256(expectation_payload).hexdigest(),
    }


def _evaluation_evidence(
    case_id: str,
    candidate_payload: bytes,
    expectation_payload: bytes,
) -> dict[str, object]:
    return {
        "schema": EVALUATION_SCHEMA,
        "version": 1,
        "case": case_id,
        "verdict": "passed",
        "bindings": _bindings(case_id, candidate_payload, expectation_payload),
    }


def _verify_handoff(handoff_path: Path, candidate_output: Path) -> dict[str, object]:
    handoff = _load_object(handoff_path)
    if handoff.get("schema") != EVALUATION_SCHEMA or handoff.get("version") != 1:
        raise ValueError("evaluation handoff has an unsupported schema or version")
    case_id = handoff.get("case")
    if not isinstance(case_id, str) or case_id not in {"absent-header-policy", "explicit-header-policy"}:
        raise ValueError("evaluation handoff has an unknown case")
    if handoff.get("verdict") != "passed":
        raise ValueError("evaluation handoff is not a passing result")
    observed = handoff.get("bindings")
    if not isinstance(observed, dict):
        raise ValueError("evaluation handoff has no structured bindings")
    candidate_payload = candidate_output.read_bytes()
    expectation_payload = EXPECTED_RESULTS.read_bytes()
    expected = _bindings(case_id, candidate_payload, expectation_payload)
    labels = {
        "case": "evaluation case",
        "capturedSynthesisSha256": "captured synthesis SHA-256",
        "evaluatorIdentity": "evaluator identity",
        "evaluatorSha256": "evaluator SHA-256",
        "expectationsIdentity": "expectations identity",
        "expectationsSha256": "expectations SHA-256",
    }
    for field, label in labels.items():
        if observed.get(field) != expected[field]:
            raise ValueError(f"{label} does not match handoff")
    return {
        "schema": VERIFICATION_SCHEMA,
        "version": 1,
        "case": case_id,
        "verdict": "bound",
        "bindings": expected,
    }


def _main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--case")
    mode.add_argument("--verify-handoff", type=Path)
    parser.add_argument("--candidate-output", required=True, type=Path)
    arguments = parser.parse_args()
    try:
        if arguments.verify_handoff is not None:
            evidence = _verify_handoff(arguments.verify_handoff, arguments.candidate_output)
            errors: list[str] = []
        else:
            candidate_payload = arguments.candidate_output.read_bytes()
            expectation_payload = EXPECTED_RESULTS.read_bytes()
            observed = _decode_object(candidate_payload, arguments.candidate_output.as_posix())
            expectations = _decode_object(expectation_payload, EXPECTED_RESULTS.as_posix())
            errors = _evaluate(arguments.case, observed, expectations)
            evidence = _evaluation_evidence(
                arguments.case,
                candidate_payload,
                expectation_payload,
            )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        errors = [str(error)]
        evidence = {}
    if errors:
        for message in errors:
            print(message, file=sys.stderr)
        return 1
    print(json.dumps(evidence, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
