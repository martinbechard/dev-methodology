# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies the executable Dev Documentation Writer module-design fixture contract.

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


_FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "module-design-template-conformance"
_VALIDATOR = _FIXTURE_ROOT / "validate_fixture.py"
_TEMPLATE = (
    Path(__file__).resolve().parents[3]
    / "skills"
    / "development-methodology"
    / "assets"
    / "templates"
    / "module-design-template.md"
)


def _run_validator(
    phase: str,
    *,
    artifact: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run the fixture validator with deterministic paths and captured output."""

    command = [sys.executable, str(_VALIDATOR), phase, "--template", str(_TEMPLATE)]
    if artifact is not None:
        command.extend(("--artifact", str(artifact)))
    return subprocess.run(
        command,
        cwd=_FIXTURE_ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )


def _complete_artifact_text(*, headings: list[str] | None = None) -> str:
    """Build one source-faithful artifact for validator acceptance tests."""

    ordered = headings or [
        line
        for line in _TEMPLATE.read_text(encoding="utf-8").splitlines()
        if line.startswith("## ")
    ]
    sections = []
    for heading in ordered:
        body = "Evidence is grounded in src/inventory.py and tests/test_inventory.py."
        if heading == "## Implementation Readiness":
            body = "READY. The existing implementation contract is source-backed."
        elif heading == "## Verification":
            body = (
                "The accepted command is python3 -m unittest discover -s tests. "
                "The success path is tested. The blank-value ValueError branch is source-observed "
                "and is not covered by an automated test."
            )
        sections.extend((heading, "", body, ""))
    return "# Inventory Normalization Module Design\n\n" + "\n".join(sections)


class DocumentationWriterFixtureTests(unittest.TestCase):
    """Protect the first-attempt module-design fixture and its deterministic gate."""

    def test_initial_fixture_has_source_test_and_no_module_design(self) -> None:
        completed = _run_validator("initial")

        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        evidence = json.loads(completed.stdout)
        self.assertTrue(evidence["sourcePresent"])
        self.assertTrue(evidence["testPresent"])
        self.assertFalse(evidence["artifactPresent"])
        self.assertEqual(1, evidence["testsRun"])

    def test_final_validator_accepts_complete_source_faithful_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(_complete_artifact_text(), encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        evidence = json.loads(completed.stdout)
        self.assertTrue(evidence["headingsMatch"])
        self.assertTrue(evidence["readinessValid"])
        self.assertTrue(evidence["evidenceReferencesValid"])
        self.assertTrue(evidence["testClaimsValid"])

    def test_final_validator_rejects_reordered_headings(self) -> None:
        headings = [
            line
            for line in _TEMPLATE.read_text(encoding="utf-8").splitlines()
            if line.startswith("## ")
        ]
        headings[0], headings[1] = headings[1], headings[0]

        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(_complete_artifact_text(headings=headings), encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(3, completed.returncode)
        evidence = json.loads(completed.stdout)
        self.assertFalse(evidence["headingsMatch"])

    def test_final_validator_rejects_invalid_readiness_lead(self) -> None:
        artifact_text = _complete_artifact_text().replace(
            "READY. The existing implementation contract is source-backed.",
            "The implementation contract is source-backed but has no readiness marker.",
        )

        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(3, completed.returncode)
        evidence = json.loads(completed.stdout)
        self.assertFalse(evidence["readinessValid"])

    def test_final_validator_rejects_invented_boundary_test(self) -> None:
        artifact_text = _complete_artifact_text() + (
            "\ntests/test_inventory_boundaries.py covers the blank-value ValueError branch.\n"
        )

        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(3, completed.returncode)
        evidence = json.loads(completed.stdout)
        self.assertFalse(evidence["evidenceReferencesValid"])
        self.assertFalse(evidence["testClaimsValid"])


if __name__ == "__main__":
    unittest.main()
