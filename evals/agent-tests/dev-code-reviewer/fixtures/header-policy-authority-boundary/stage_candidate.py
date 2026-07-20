#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Stages one reviewer candidate behind a path-checked boundary that excludes evaluator-owned oracle files.

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path


FIXTURE_ROOT = Path(__file__).resolve().parent
CANDIDATE_INPUTS = FIXTURE_ROOT / "candidate-inputs"
CASES = frozenset({"absent-header-policy", "explicit-header-policy"})
ORACLE_NAMES = frozenset({"evaluate_synthesis.py", "expected-results.json"})


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _overlaps(first: Path, second: Path) -> bool:
    return first == second or first.is_relative_to(second) or second.is_relative_to(first)


def _stage(case_id: str, destination: Path, manifest: Path) -> dict[str, object]:
    if case_id not in CASES:
        raise ValueError(f"unknown candidate case: {case_id}")
    source = (CANDIDATE_INPUTS / case_id).resolve()
    candidate_root = destination.resolve()
    manifest_path = manifest.resolve()
    if _overlaps(candidate_root, FIXTURE_ROOT.resolve()):
        raise ValueError("candidate destination overlaps evaluator-owned fixture")
    if manifest_path.is_relative_to(FIXTURE_ROOT.resolve()):
        raise ValueError("candidate manifest overlaps evaluator-owned fixture")
    if manifest_path.is_relative_to(candidate_root):
        raise ValueError("candidate manifest must remain outside candidate workspace")
    if destination.exists():
        raise ValueError(f"candidate destination already exists: {destination}")
    for path in source.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"candidate source contains a symbolic link: {path}")

    shutil.copytree(source, destination)
    staged_files = sorted(path for path in destination.rglob("*") if path.is_file())
    forbidden = sorted(path.name for path in staged_files if path.name in ORACLE_NAMES)
    if forbidden:
        shutil.rmtree(destination)
        raise ValueError(f"candidate workspace contains evaluator oracle: {', '.join(forbidden)}")
    for path in staged_files:
        path.chmod(0o444)
    for path in sorted(
        (path for path in destination.rglob("*") if path.is_dir()),
        key=lambda value: len(value.parts),
        reverse=True,
    ):
        path.chmod(0o555)
    destination.chmod(0o555)

    evidence: dict[str, object] = {
        "schema": "dev-code-reviewer-candidate-workspace",
        "version": 1,
        "case": case_id,
        "candidateRoot": candidate_root.as_posix(),
        "accessBoundary": {
            "allowedReadRoot": candidate_root.as_posix(),
            "oracleFilesPresent": False,
        },
        "files": [
            {
                "path": path.relative_to(destination).as_posix(),
                "sha256": _sha256(path),
            }
            for path in staged_files
        ],
    }
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return evidence


def _main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    arguments = parser.parse_args()
    try:
        evidence = _stage(arguments.case, arguments.destination, arguments.manifest)
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    print(json.dumps(evidence, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
