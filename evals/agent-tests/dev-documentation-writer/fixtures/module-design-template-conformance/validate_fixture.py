# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Validates module-template structure, readiness, source evidence, test claims, and fixture tests.

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path


_ROOT = Path(__file__).resolve().parent
_CONTRACT_PATH = _ROOT / "fixture-contract.json"
_PATH_REFERENCE = re.compile(
    r"(?<![A-Za-z0-9_./-])"
    r"(?P<path>/(?:[A-Za-z0-9_.-]+/)*(?:src|tests)/[A-Za-z0-9_./-]+\.py"
    r"|(?:\.\.?/|[A-Za-z0-9_.-]+/)*(?:src|tests)/[A-Za-z0-9_./-]+\.py)"
)
_POSITIVE_COVERAGE = re.compile(
    r"(?:automated tests?|tests?)\s+(?:cover|covers|exercise|exercises|verify|verifies|assert|asserts)"
    r"|(?:covered|tested|verified)\s+by\s+(?:an\s+)?automated test"
)


def _load_contract() -> dict[str, object]:
    """Load the synthetic fixture contract."""

    return json.loads(_CONTRACT_PATH.read_text(encoding="utf-8"))


def _ordered_headings(path: Path) -> list[str]:
    """Return ordered level-two headings from a Markdown artifact."""

    return [
        line
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("## ")
    ]


def _first_section_content(text: str, heading: str) -> str:
    """Return the first nonblank content line under one level-two heading."""

    inside = False
    for line in text.splitlines():
        if line == heading:
            inside = True
            continue
        if inside and line.startswith("## "):
            return ""
        if inside and line.strip():
            return line.strip()
    return ""


def _sha256(path: Path) -> str:
    """Return the SHA-256 digest of one authoritative fixture input."""

    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def _command_claims(text: str) -> tuple[list[str], bool]:
    """Return complete lines from one command-only shell fence and its structural validity."""

    commands: list[str] = []
    active_fence = ""
    command_block_count = 0
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            if active_fence:
                active_fence = ""
            else:
                active_fence = stripped[3:].strip().lower()
                if active_fence in {"bash", "sh", "shell"}:
                    command_block_count += 1
            continue
        if active_fence in {"bash", "sh", "shell"} and stripped and not stripped.startswith("#"):
            commands.append(stripped)
    structure_valid = command_block_count == 1 and active_fence == ""
    return commands, structure_valid


def _readiness_valid(text: str) -> bool:
    """Accept plain or canonically emphasized READY and BLOCKED readiness leads."""

    first = _first_section_content(text, "## Implementation Readiness")
    return re.match(r"^(?:READY\.|BLOCKED\.|\*\*(?:READY\.|BLOCKED\.)\*\*)(?=\s|$)", first) is not None


def _references_valid(referenced_paths: list[str], required_paths: set[str]) -> bool:
    """Require all evidence paths to exist within the synthetic repository boundary."""

    root = _ROOT.resolve()
    if not required_paths.issubset(referenced_paths):
        return False
    for path in referenced_paths:
        candidate = (_ROOT / path).resolve()
        if not candidate.is_relative_to(root) or not candidate.is_file():
            return False
    return True


def _test_claims_valid(text: str, required_terms: list[str]) -> bool:
    """Reject positive automated-coverage claims for the declared source-only branch."""

    if not all(term in text for term in required_terms):
        return False
    for line in text.splitlines():
        lowered = line.lower()
        without_disclaimers = re.sub(
            r"(?:is\s+)?not covered by an automated test|not tested|untested|no automated test",
            "",
            lowered,
        )
        identifies_source_only_branch = any(
            subject in without_disclaimers for subject in ("blank", "valueerror", "rejection")
        )
        if identifies_source_only_branch and _POSITIVE_COVERAGE.search(without_disclaimers):
            return False
    return True


def _run_source_tests() -> tuple[int, bool, str]:
    """Run the fixture's accepted source-test boundary without bytecode writes."""

    suite = unittest.TestLoader().discover(str(_ROOT / "tests"))
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
        cwd=_ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
        env=environment,
    )
    return suite.countTestCases(), completed.returncode == 0, completed.stdout + completed.stderr


def _initial_evidence(contract: dict[str, object]) -> dict[str, object]:
    """Return source, test, artifact, and executable test evidence."""

    artifact = _ROOT / str(contract["artifactPath"])
    tests_run, tests_pass, test_output = _run_source_tests()
    return {
        "sourcePresent": (_ROOT / str(contract["sourcePath"])).is_file(),
        "testPresent": (_ROOT / str(contract["testPath"])).is_file(),
        "artifactPresent": artifact.is_file(),
        "testsRun": tests_run,
        "testsPass": tests_pass,
        "testOutput": test_output,
    }


def _final_evidence(
    contract: dict[str, object],
    *,
    artifact: Path,
    template: Path,
) -> dict[str, object]:
    """Return deterministic conformance and source-fidelity evidence."""

    text = artifact.read_text(encoding="utf-8") if artifact.is_file() else ""
    referenced_paths = sorted({match.group("path") for match in _PATH_REFERENCE.finditer(text)})
    required_paths = {str(contract["sourcePath"]), str(contract["testPath"])}
    source_only_terms = [str(term) for term in contract["sourceOnlyBranchTerms"]]
    command_claims, command_structure_valid = _command_claims(text)
    initial = _initial_evidence(contract)
    evidence = {
        **initial,
        "artifactPresent": artifact.is_file(),
        "templateAuthorityValid": template.is_file()
        and _sha256(template) == str(contract["canonicalTemplateSha256"]),
        "headingsMatch": artifact.is_file()
        and template.is_file()
        and _ordered_headings(artifact) == _ordered_headings(template),
        "readinessValid": _readiness_valid(text),
        "todoFree": "TODO" not in text,
        "evidenceReferencesValid": _references_valid(referenced_paths, required_paths),
        "testCommandValid": command_structure_valid
        and command_claims == [str(contract["acceptedTestCommand"])],
        "testClaimsValid": _test_claims_valid(text, source_only_terms),
        "commandClaims": command_claims,
        "commandStructureValid": command_structure_valid,
        "referencedPaths": referenced_paths,
    }
    return evidence


def main() -> int:
    """Validate the selected fixture phase and print machine-readable evidence."""

    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("initial", "final"))
    parser.add_argument("--artifact", type=Path)
    parser.add_argument("--template", type=Path, required=True)
    arguments = parser.parse_args()
    contract = _load_contract()

    if arguments.phase == "initial":
        evidence = _initial_evidence(contract)
        expected_count = int(contract["expectedTestCount"])
        accepted = (
            evidence["sourcePresent"]
            and evidence["testPresent"]
            and not evidence["artifactPresent"]
            and evidence["testsPass"]
            and evidence["testsRun"] == expected_count
        )
        print(json.dumps(evidence, sort_keys=True))
        return 0 if accepted else 2

    artifact = arguments.artifact or _ROOT / str(contract["artifactPath"])
    evidence = _final_evidence(contract, artifact=artifact, template=arguments.template)
    accepted = all(
        evidence[key]
        for key in (
            "sourcePresent",
            "testPresent",
            "artifactPresent",
            "testsPass",
            "templateAuthorityValid",
            "headingsMatch",
            "readinessValid",
            "todoFree",
            "evidenceReferencesValid",
            "testCommandValid",
            "testClaimsValid",
        )
    ) and evidence["testsRun"] == int(contract["expectedTestCount"])
    print(json.dumps(evidence, sort_keys=True))
    return 0 if accepted else 3


if __name__ == "__main__":
    raise SystemExit(main())
