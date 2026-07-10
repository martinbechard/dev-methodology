#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "evals" / "cases.yaml"


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
            for evidence_id in case["requiredEvidence"]:
                if str(evidence_id) not in text:
                    errors.append(f"result missing evidence: {evidence_id}")
            for finding in case.get("requiredFindings", []):
                if str(finding).lower() not in text.lower():
                    errors.append(f"result missing expected finding: {finding}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Run synthetic agent and skill evaluation projects.")
    parser.add_argument("--case", choices=sorted(load_cases()))
    parser.add_argument("--install", action="store_true")
    parser.add_argument("--project-root", type=Path)
    parser.add_argument("--result", type=Path)
    args = parser.parse_args()

    cases = load_cases()
    selected = [cases[args.case]] if args.case else list(cases.values())
    failures: list[str] = []
    for case in selected:
        default_root = ROOT / str(case["project"])
        project_root = args.project_root.resolve() if args.project_root else default_root
        case_errors = validate_case(case, project_root, args.result)
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
            print(f"PASS {case['id']}")

    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
