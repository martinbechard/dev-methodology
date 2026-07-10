#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "evals" / "cases.yaml"


def content_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_cases() -> dict[str, dict[str, object]]:
    data = yaml.safe_load(CASES_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
        raise ValueError("evals/cases.yaml must define a cases list.")
    cases: dict[str, dict[str, object]] = {}
    for item in data["cases"]:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            raise ValueError("Every eval case must define an id.")
        cases[item["id"]] = item
    return cases


def run(command: str, cwd: Path) -> bool:
    print(f"[{cwd.name}] {command}")
    completed = subprocess.run(command, cwd=cwd, shell=True, check=False)
    return completed.returncode == 0


def validate_case(case: dict[str, object], project_root: Path, result_path: Path | None) -> list[str]:
    errors: list[str] = []
    task_path = project_root / str(case["task"])
    if not task_path.is_file():
        errors.append(f"missing task: {task_path}")
    for skill in case["requiredSkills"]:
        skill_path = ROOT / "skills" / str(skill) / "SKILL.md"
        if not skill_path.is_file():
            errors.append(f"missing skill: {skill}")
    if result_path is not None:
        if not result_path.is_file():
            errors.append(f"missing result: {result_path}")
        else:
            text = result_path.read_text(encoding="utf-8")
            for heading in ("Skills Used", "Evidence Packet", "Review Synthesis"):
                if heading not in text:
                    errors.append(f"result missing section: {heading}")
    return errors


def require_non_empty_string(value: object, field: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"evidence missing non-empty {field}")


def validate_reference(value: object, field: str, evidence_path: Path, errors: list[str]) -> None:
    if not isinstance(value, str) or "#" not in value:
        errors.append(f"evidence {field} must be a relative file#marker reference")
        return
    file_name, marker = value.rsplit("#", 1)
    if not file_name or not marker:
        errors.append(f"evidence {field} must include a file and marker")
        return
    target = (evidence_path.parent / file_name).resolve()
    evidence_root = evidence_path.parent.resolve()
    if target != evidence_root and evidence_root not in target.parents:
        errors.append(f"evidence {field} reference escapes the receipt directory")
        return
    if not target.is_file():
        errors.append(f"evidence {field} reference target is missing: {file_name}")
        return
    try:
        referenced_text = target.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"evidence {field} reference target is not UTF-8 text: {file_name}")
        return
    if marker not in referenced_text:
        errors.append(f"evidence {field} marker is missing from {file_name}: {marker}")


def validate_harness_event(
    value: object,
    field: str,
    evidence_path: Path,
    expected: dict[str, object],
    errors: list[str],
) -> None:
    validate_reference(value, field, evidence_path, errors)
    if not isinstance(value, str) or "#" not in value:
        return
    file_name, marker = value.rsplit("#", 1)
    target = (evidence_path.parent / file_name).resolve()
    if not target.is_file():
        return
    events: list[dict[str, object]] = []
    try:
        for line in target.read_text(encoding="utf-8").splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(event, dict) and str(event.get("id")) == marker:
                events.append(event)
    except UnicodeDecodeError:
        return
    if len(events) != 1:
        errors.append(f"evidence {field} must identify exactly one JSON harness event: {marker}")
        return
    event = events[0]
    for key, expected_value in expected.items():
        if event.get(key) != expected_value:
            errors.append(f"evidence {field} harness event {key} does not match {expected_value}")


def validate_evidence(case: dict[str, object], evidence_path: Path | None) -> list[str]:
    errors: list[str] = []
    if evidence_path is None:
        return ["behavior evaluation requires --evidence"]
    if not evidence_path.is_file():
        return [f"missing evidence receipt: {evidence_path}"]
    evidence = yaml.safe_load(evidence_path.read_text(encoding="utf-8"))
    if not isinstance(evidence, dict):
        return [f"evidence receipt must be a YAML mapping: {evidence_path}"]
    if evidence.get("schema") != "dev-methodology-eval-evidence" or evidence.get("version") != 1:
        errors.append("evidence receipt has unsupported schema or version")
    if evidence.get("case") != case["id"]:
        errors.append("evidence receipt case does not match selected case")
    if evidence.get("verdict") != "verified":
        errors.append("evidence receipt verdict must be verified")
    provenance = evidence.get("captureProvenance")
    if not isinstance(provenance, dict):
        errors.append("evidence captureProvenance must be a mapping")
    else:
        if provenance.get("kind") not in {"trusted-ci", "human-attested-harness-export"}:
            errors.append("evidence captureProvenance.kind must identify a trusted capture source")
        validate_reference(provenance.get("reference"), "captureProvenance.reference", evidence_path, errors)
    agent = evidence.get("agent")
    if not isinstance(agent, dict):
        errors.append("evidence agent must be a mapping")
    else:
        if agent.get("id") not in case.get("requiredAgents", []):
            errors.append("evidence agent id does not match a required agent")
        for field in ("harness", "model", "invocationEvidence"):
            require_non_empty_string(agent.get(field), f"agent.{field}", errors)
        validate_harness_event(agent.get("invocationEvidence"), "agent.invocationEvidence", evidence_path, {
            "type": "invocation",
            "agent": agent.get("id"),
            "harness": agent.get("harness"),
            "model": agent.get("model"),
        }, errors)
    receipt_skills: dict[str, dict[str, object]] = {}
    skills = evidence.get("skills")
    if not isinstance(skills, list):
        errors.append("evidence skills must be a list")
    else:
        for item in skills:
            if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                errors.append("each evidence skill must be a mapping with id")
                continue
            receipt_skills[item["id"]] = item
        for skill in case["requiredSkills"]:
            item = receipt_skills.get(str(skill))
            if item is None:
                errors.append(f"evidence missing required skill: {skill}")
                continue
            source = ROOT / "skills" / str(skill) / "SKILL.md"
            if item.get("contentDigest") != content_digest(source):
                errors.append(f"evidence skill digest mismatch: {skill}")
            read_evidence = item.get("readEvidence")
            if not isinstance(read_evidence, list) or not read_evidence:
                errors.append(f"evidence missing skill read tool evidence: {skill}")
            elif any(not isinstance(value, dict) or value.get("type") != "tool-call" or not value.get("reference") for value in read_evidence):
                errors.append(f"skill read evidence must contain tool-call references: {skill}")
            else:
                for index, value in enumerate(read_evidence):
                    validate_harness_event(value["reference"], f"skills.{skill}.readEvidence[{index}]", evidence_path, {
                        "type": "tool-call",
                        "skill": str(skill),
                        "contentDigest": item.get("contentDigest"),
                    }, errors)
    assertions = evidence.get("behaviorAssertions")
    assertion_by_id = {
        str(item.get("id")): item
        for item in assertions
        if isinstance(item, dict)
    } if isinstance(assertions, list) else {}
    if not isinstance(assertions, list):
        errors.append("evidence behaviorAssertions must be a list")
    for assertion_id in case["requiredEvidence"]:
        item = assertion_by_id.get(str(assertion_id))
        if item is None:
            errors.append(f"evidence missing behavior assertion: {assertion_id}")
        elif item.get("verdict") != "passed" or not item.get("evidence"):
            errors.append(f"behavior assertion lacks passed evidence: {assertion_id}")
        else:
            validate_reference(item["evidence"], f"behaviorAssertions.{assertion_id}.evidence", evidence_path, errors)
    findings = evidence.get("findings", [])
    finding_ids = {str(item.get("id")) for item in findings if isinstance(item, dict) and item.get("evidence")}
    for finding_id in case.get("requiredFindings", []):
        if str(finding_id) not in finding_ids:
            errors.append(f"evidence missing expected finding: {finding_id}")
        else:
            item = next(value for value in findings if isinstance(value, dict) and str(value.get("id")) == str(finding_id))
            validate_reference(item["evidence"], f"findings.{finding_id}.evidence", evidence_path, errors)
    commands = evidence.get("commands")
    if not isinstance(commands, list) or not commands:
        errors.append("evidence commands must be a non-empty list")
    else:
        for item in commands:
            if not isinstance(item, dict):
                errors.append("each command evidence item must be a mapping")
                continue
            require_non_empty_string(item.get("command"), "commands.command", errors)
            if not isinstance(item.get("exitCode"), int):
                errors.append("command exitCode must be an integer")
            require_non_empty_string(item.get("expectation"), "commands.expectation", errors)
            require_non_empty_string(item.get("evidence"), "commands.evidence", errors)
            validate_reference(item.get("evidence"), "commands.evidence", evidence_path, errors)
    verifier = evidence.get("independentVerifier")
    if not isinstance(verifier, dict):
        errors.append("evidence independentVerifier must be a mapping")
    else:
        require_non_empty_string(verifier.get("kind"), "independentVerifier.kind", errors)
        require_non_empty_string(verifier.get("reference"), "independentVerifier.reference", errors)
        validate_reference(verifier.get("reference"), "independentVerifier.reference", evidence_path, errors)
    if case.get("readOnly"):
        before = evidence.get("projectHashBefore")
        after = evidence.get("projectHashAfter")
        require_non_empty_string(before, "projectHashBefore", errors)
        require_non_empty_string(after, "projectHashAfter", errors)
        if before != after:
            errors.append("read-only evaluation changed the project hash")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Run synthetic agent and skill evaluation projects.")
    parser.add_argument("--case", choices=sorted(load_cases()))
    parser.add_argument("--install", action="store_true")
    parser.add_argument("--project-root", type=Path)
    parser.add_argument("--result", type=Path)
    parser.add_argument("--evidence", type=Path)
    args = parser.parse_args()

    cases = load_cases()
    selected = [cases[args.case]] if args.case else list(cases.values())
    failures: list[str] = []
    for case in selected:
        default_root = ROOT / str(case["project"])
        project_root = args.project_root.resolve() if args.project_root else default_root
        case_errors = validate_case(case, project_root, args.result)
        if args.result is not None:
            case_errors.extend(validate_evidence(case, args.evidence))
        if args.install and not run(str(case["install"]), project_root):
            case_errors.append("install command failed")
        verification_passed = run(str(case["verify"]), project_root)
        expect_verify_failure = bool(case.get("expectVerifyFailure", False))
        if verification_passed == expect_verify_failure:
            expectation = "failure" if expect_verify_failure else "success"
            case_errors.append(f"verification command did not produce expected {expectation}")
        if case_errors:
            failures.extend(f"{case['id']}: {error}" for error in case_errors)
        else:
            label = "VERIFIED PASS" if args.result is not None else "FIXTURE PASS"
            print(f"{label} {case['id']}")

    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
