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


def _complete_artifact_text(
    *,
    commands: list[str] | None = None,
    headings: list[str] | None = None,
    readiness: str = "**READY.** The existing implementation contract is source-backed.",
) -> str:
    """Build one source-faithful artifact for validator acceptance tests."""

    ordered = headings or [
        line
        for line in _TEMPLATE.read_text(encoding="utf-8").splitlines()
        if line.startswith("## ")
    ]
    accepted_commands = commands or ["python3 -m unittest discover -s tests"]
    sections = []
    for heading in ordered:
        body = "Evidence is grounded in src/inventory.py and tests/test_inventory.py."
        if heading == "## Implementation Readiness":
            body = readiness
        elif heading == "## Verification":
            body = (
                "The accepted command is:\n\n"
                "```bash\n"
                + "\n".join(accepted_commands)
                + "\n"
                "```\n\n"
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
        artifact_text = _complete_artifact_text(
            readiness="The implementation contract is source-backed but has no readiness marker.",
        )

        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(3, completed.returncode)
        evidence = json.loads(completed.stdout)
        self.assertFalse(evidence["readinessValid"])

    def test_final_validator_rejects_unbalanced_readiness_emphasis(self) -> None:
        artifact_text = _complete_artifact_text(readiness="**READY. Evidence is incomplete.")

        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(3, completed.returncode)
        self.assertFalse(json.loads(completed.stdout)["readinessValid"])

    def test_final_validator_accepts_canonical_bold_readiness_markers(self) -> None:
        for marker in ("**READY.**", "**BLOCKED.**"):
            with self.subTest(marker=marker), tempfile.TemporaryDirectory() as directory:
                artifact = Path(directory) / "module-design.md"
                artifact.write_text(
                    _complete_artifact_text(readiness=f"{marker} Evidence-backed decision."),
                    encoding="utf-8",
                )
                completed = _run_validator("final", artifact=artifact)

            self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
            self.assertTrue(json.loads(completed.stdout)["readinessValid"])

    def test_final_validator_rejects_unapproved_command(self) -> None:
        artifact_text = _complete_artifact_text(
            commands=["python3 -m unittest discover -s tests", "pytest -q"]
        )

        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(3, completed.returncode)
        evidence = json.loads(completed.stdout)
        self.assertFalse(evidence["testCommandValid"])
        self.assertEqual(
            ["python3 -m unittest discover -s tests", "pytest -q"], evidence["commandClaims"]
        )

    def test_final_validator_rejects_non_python_command(self) -> None:
        artifact_text = _complete_artifact_text(
            commands=["python3 -m unittest discover -s tests", "make test"]
        )

        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(3, completed.returncode)
        self.assertFalse(json.loads(completed.stdout)["testCommandValid"])

    def test_final_validator_rejects_prefixed_allowed_command(self) -> None:
        prefixes = ("sudo ", "false && ", "env PYTHONPATH=/unapproved ")
        for prefix in prefixes:
            with self.subTest(prefix=prefix), tempfile.TemporaryDirectory() as directory:
                artifact = Path(directory) / "module-design.md"
                artifact.write_text(
                    _complete_artifact_text(
                        commands=[f"{prefix}python3 -m unittest discover -s tests"]
                    ),
                    encoding="utf-8",
                )
                completed = _run_validator("final", artifact=artifact)

            self.assertEqual(3, completed.returncode)
            self.assertFalse(json.loads(completed.stdout)["testCommandValid"])

    def test_final_validator_rejects_noncanonical_template(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            artifact = temporary / "module-design.md"
            template = temporary / "module-design-template.md"
            artifact.write_text("# Design\n\n## Verification\n\nNo checks.\n", encoding="utf-8")
            template.write_text(artifact.read_text(encoding="utf-8"), encoding="utf-8")
            command = [
                sys.executable,
                str(_VALIDATOR),
                "final",
                "--template",
                str(template),
                "--artifact",
                str(artifact),
            ]
            completed = subprocess.run(
                command,
                cwd=_FIXTURE_ROOT,
                capture_output=True,
                text=True,
                check=False,
                timeout=10,
            )

        self.assertEqual(3, completed.returncode)
        self.assertFalse(json.loads(completed.stdout)["templateAuthorityValid"])

    def test_final_validator_rejects_invented_boundary_test(self) -> None:
        artifact_text = _complete_artifact_text() + (
            "\nAutomated tests exercise the blank rejection behavior.\n"
        )

        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(3, completed.returncode)
        evidence = json.loads(completed.stdout)
        self.assertFalse(evidence["testClaimsValid"])

    def test_final_validator_rejects_same_line_coverage_contradiction(self) -> None:
        artifact_text = _complete_artifact_text().replace(
            "The blank-value ValueError branch is source-observed and is not covered by an automated test.",
            "The blank-value ValueError branch is source-observed and is not covered by an automated test, "
            "but automated tests exercise the blank rejection behavior.",
        )

        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(3, completed.returncode)
        self.assertFalse(json.loads(completed.stdout)["testClaimsValid"])

    def test_final_validator_rejects_escaping_evidence_path(self) -> None:
        artifact_text = _complete_artifact_text() + "\ntests/../../../../runner.py is supporting evidence.\n"

        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(3, completed.returncode)
        self.assertFalse(json.loads(completed.stdout)["evidenceReferencesValid"])

    def test_final_validator_rejects_absolute_prefixed_evidence_path(self) -> None:
        artifact_text = _complete_artifact_text() + "\n/tmp/src/inventory.py is supporting evidence.\n"

        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(3, completed.returncode)
        evidence = json.loads(completed.stdout)
        self.assertFalse(evidence["evidenceReferencesValid"])
        self.assertIn("/tmp/src/inventory.py", evidence["referencedPaths"])


if __name__ == "__main__":
    unittest.main()
