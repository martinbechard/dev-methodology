# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies the executable Dev Documentation Writer module-design fixture contract.

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


_FIXTURE_ROOT = (
    Path(__file__).resolve().parent / "fixtures" / "module-design-template-conformance"
)
_VALIDATOR = _FIXTURE_ROOT / "validate_fixture.py"
_SCENARIOS = Path(__file__).resolve().parent / "scenarios.yaml"
_JUDGES = Path(__file__).resolve().parents[2] / "judges.yaml"
_TEMPLATE = (
    Path(__file__).resolve().parents[3]
    / "skills"
    / "route-documentation-work"
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

    if artifact is not None:
        with tempfile.TemporaryDirectory() as directory:
            fixture_root = _copy_fixture(Path(directory))
            target = fixture_root / "docs" / "inventory-normalization-module-design.md"
            target.parent.mkdir()
            target.write_text(artifact.read_text(encoding="utf-8"), encoding="utf-8")
            return _run_copied_validator(fixture_root, phase, artifact=target)

    command = [sys.executable, str(_VALIDATOR), phase, "--template", str(_TEMPLATE)]
    return subprocess.run(
        command,
        cwd=_FIXTURE_ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )


def _copy_fixture(destination: Path) -> Path:
    """Copy the synthetic fixture without carrying interpreter cache evidence."""

    copied = destination / "module-design-template-conformance"
    shutil.copytree(
        _FIXTURE_ROOT,
        copied,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    return copied


def _run_copied_validator(
    fixture_root: Path,
    phase: str,
    *,
    artifact: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run a copied validator so artifact-relative evidence stays testable."""

    command = [
        sys.executable,
        str(fixture_root / "validate_fixture.py"),
        phase,
        "--template",
        str(_TEMPLATE),
    ]
    if artifact is not None:
        command.extend(("--artifact", str(artifact)))
    return subprocess.run(
        command,
        cwd=fixture_root,
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
        body = "Evidence is grounded in ../src/inventory.py and ../tests/test_inventory.py."
        if heading == "## Implementation Readiness":
            body = readiness
        elif heading == "## Verification":
            body = (
                "The accepted command is:\n\n"
                "```bash\n" + "\n".join(accepted_commands) + "\n"
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
            artifact.write_text(
                _complete_artifact_text(headings=headings), encoding="utf-8"
            )
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
        artifact_text = _complete_artifact_text(
            readiness="**READY. Evidence is incomplete."
        )

        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(3, completed.returncode)
        self.assertFalse(json.loads(completed.stdout)["readinessValid"])

    def test_final_validator_rejects_dangling_closing_readiness_emphasis(self) -> None:
        artifact_text = _complete_artifact_text(
            readiness="READY.** Evidence is incomplete."
        )

        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(3, completed.returncode)
        self.assertFalse(json.loads(completed.stdout)["readinessValid"])

    def test_final_validator_accepts_canonical_bold_readiness_markers(self) -> None:
        for marker in ("**READY.**", "**BLOCKED.**"):
            with (
                self.subTest(marker=marker),
                tempfile.TemporaryDirectory() as directory,
            ):
                artifact = Path(directory) / "module-design.md"
                artifact.write_text(
                    _complete_artifact_text(
                        readiness=f"{marker} Evidence-backed decision."
                    ),
                    encoding="utf-8",
                )
                completed = _run_validator("final", artifact=artifact)

            self.assertEqual(
                0, completed.returncode, completed.stdout + completed.stderr
            )
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
            ["python3 -m unittest discover -s tests", "pytest -q"],
            evidence["commandClaims"],
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
            with (
                self.subTest(prefix=prefix),
                tempfile.TemporaryDirectory() as directory,
            ):
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
            artifact.write_text(
                "# Design\n\n## Verification\n\nNo checks.\n", encoding="utf-8"
            )
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
        artifact_text = (
            _complete_artifact_text()
            + "\ntests/../../../../runner.py is supporting evidence.\n"
        )

        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(3, completed.returncode)
        self.assertFalse(json.loads(completed.stdout)["evidenceReferencesValid"])

    def test_final_validator_rejects_absolute_prefixed_evidence_path(self) -> None:
        artifact_text = (
            _complete_artifact_text()
            + "\n/tmp/src/inventory.py is supporting evidence.\n"
        )

        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(3, completed.returncode)
        evidence = json.loads(completed.stdout)
        self.assertFalse(evidence["evidenceReferencesValid"])
        self.assertIn("/tmp/src/inventory.py", evidence["referencedPaths"])

    def test_routed_authoring_uses_defined_deterministic_check_ids(self) -> None:
        scenarios = yaml.safe_load(_SCENARIOS.read_text(encoding="utf-8"))
        judges = yaml.safe_load(_JUDGES.read_text(encoding="utf-8"))
        routed = next(
            item for item in scenarios["scenarios"] if item["id"] == "routed-authoring"
        )
        defined = {item["id"] for item in judges["checks"]}

        self.assertEqual([], sorted(set(routed["deterministicChecks"]) - defined))

    def test_final_validator_rejects_node_and_wrapped_commands_outside_shell_fence(
        self,
    ) -> None:
        mutations = (
            "\nRun node tools/check.js before handoff.\n",
            "\nUse `node tools/check.js` before handoff.\n",
            "\n```text\nnode tools/check.js\n```\n",
            "\n> timeout 30s node tools/check.js\n",
            "\n- env NODE_ENV=test node tools/check.js\n",
            "\nTo verify, run node tools/check.js.\n",
            "\nenv -u NODE_ENV node tools/check.js\n",
            "\ntimeout -s TERM 30s node tools/check.js\n",
            "\necho ok;node tools/check.js\n",
        )
        for mutation in mutations:
            with (
                self.subTest(mutation=mutation),
                tempfile.TemporaryDirectory() as directory,
            ):
                artifact = Path(directory) / "module-design.md"
                artifact.write_text(
                    _complete_artifact_text() + mutation, encoding="utf-8"
                )
                completed = _run_validator("final", artifact=artifact)

            self.assertEqual(3, completed.returncode)
            self.assertFalse(json.loads(completed.stdout)["testCommandValid"])

    def test_final_validator_rejects_bold_command_outside_shell_fence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(
                _complete_artifact_text() + "\n**node tools/check.js**\n",
                encoding="utf-8",
            )
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(3, completed.returncode)
        evidence = json.loads(completed.stdout)
        self.assertFalse(evidence["testCommandValid"])
        self.assertIn("node tools/check.js", evidence["commandClaims"])

    def test_final_validator_rejects_command_separator_wrapper_outside_shell_fence(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(
                _complete_artifact_text() + "\ncommand -- node tools/check.js\n",
                encoding="utf-8",
            )
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(3, completed.returncode)
        evidence = json.loads(completed.stdout)
        self.assertFalse(evidence["testCommandValid"])
        self.assertIn("command -- node tools/check.js", evidence["commandClaims"])

    def test_final_validator_rejects_wrapped_unapproved_shell_command(self) -> None:
        commands = [
            "python3 -m unittest discover -s tests",
            "command node tools/check.js",
        ]
        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(
                _complete_artifact_text(commands=commands), encoding="utf-8"
            )
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(3, completed.returncode)
        evidence = json.loads(completed.stdout)
        self.assertFalse(evidence["testCommandValid"])
        self.assertEqual(commands, evidence["commandClaims"])

    def test_final_validator_rejects_imperative_command_after_introductory_clause(
        self,
    ) -> None:
        introductions = (
            "After editing, run",
            "After editing: run",
            "After editing run",
        )
        for introduction in introductions:
            with (
                self.subTest(introduction=introduction),
                tempfile.TemporaryDirectory() as directory,
            ):
                artifact = Path(directory) / "module-design.md"
                artifact.write_text(
                    _complete_artifact_text()
                    + f"\n{introduction} node tools/check.js.\n",
                    encoding="utf-8",
                )
                completed = _run_validator("final", artifact=artifact)

            self.assertEqual(3, completed.returncode)
            self.assertFalse(json.loads(completed.stdout)["testCommandValid"])

    def test_final_validator_accepts_explanatory_node_prose(self) -> None:
        explanations = (
            "The Node runtime and tools/check.js are not part of this fixture.",
            "Developers use node tools/check.js in other projects.",
        )
        for explanation in explanations:
            with (
                self.subTest(explanation=explanation),
                tempfile.TemporaryDirectory() as directory,
            ):
                artifact = Path(directory) / "module-design.md"
                artifact.write_text(
                    _complete_artifact_text() + f"\n{explanation}\n",
                    encoding="utf-8",
                )
                completed = _run_validator("final", artifact=artifact)

            self.assertEqual(
                0, completed.returncode, completed.stdout + completed.stderr
            )

    def test_final_validator_accepts_local_reference_style_destinations(self) -> None:
        artifact_text = _complete_artifact_text().replace(
            "../src/inventory.py",
            "[inventory source][source-code]",
        ).replace(
            "../tests/test_inventory.py",
            "[inventory tests][test-code]",
        ) + (
            "\n[source-code]: ../src/inventory.py\n"
            '[test-code]: <../tests/test_inventory.py> "Fixture tests"\n'
        )
        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        self.assertTrue(json.loads(completed.stdout)["evidenceReferencesValid"])

    def test_final_validator_rejects_external_reference_style_evidence_destinations(
        self,
    ) -> None:
        artifact_text = _complete_artifact_text().replace(
            "../src/inventory.py",
            "[inventory source][source-code]",
        ).replace(
            "../tests/test_inventory.py",
            "[inventory tests][test-code]",
        ) + (
            "\n[source-code]: https://evidence.invalid/src/inventory.py\n"
            "[test-code]: https://evidence.invalid/tests/test_inventory.py\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(3, completed.returncode)
        self.assertFalse(json.loads(completed.stdout)["evidenceReferencesValid"])

    def test_final_validator_accepts_local_shortcut_reference_destinations(
        self,
    ) -> None:
        artifact_text = _complete_artifact_text().replace(
            "../src/inventory.py",
            "[source-code]",
        ).replace(
            "../tests/test_inventory.py",
            "[test-code]",
        ) + (
            "\n[source-code]: ../src/inventory.py\n"
            "[test-code]: ../tests/test_inventory.py\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        self.assertTrue(json.loads(completed.stdout)["evidenceReferencesValid"])

    def test_final_validator_rejects_image_only_evidence_destinations(self) -> None:
        mutations = (
            _complete_artifact_text()
            .replace(
                "../src/inventory.py",
                "![inventory source](../src/inventory.py)",
            )
            .replace(
                "../tests/test_inventory.py",
                "![inventory tests](../tests/test_inventory.py)",
            ),
            _complete_artifact_text()
            .replace(
                "../src/inventory.py",
                "![inventory source][source-code]",
            )
            .replace(
                "../tests/test_inventory.py",
                "![inventory tests][test-code]",
            )
            + (
                "\n[source-code]: ../src/inventory.py\n"
                "[test-code]: ../tests/test_inventory.py\n"
            ),
        )
        for artifact_text in mutations:
            with (
                self.subTest(artifact_text=artifact_text),
                tempfile.TemporaryDirectory() as directory,
            ):
                artifact = Path(directory) / "module-design.md"
                artifact.write_text(artifact_text, encoding="utf-8")
                completed = _run_validator("final", artifact=artifact)

            self.assertEqual(3, completed.returncode)
            self.assertFalse(json.loads(completed.stdout)["evidenceReferencesValid"])

    def test_final_validator_ignores_unrelated_external_reference_destination(
        self,
    ) -> None:
        artifact_text = _complete_artifact_text() + (
            "\nSee [external format notes][format-notes].\n"
            "[format-notes]: https://example.invalid/reference\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)

    def test_final_validator_rejects_anaphoric_coverage_contradictions(self) -> None:
        disclaimer = "The blank-value ValueError branch is source-observed and is not covered by an automated test."
        contradictions = (
            "Nevertheless, it is fully exercised by unit tests.",
            "It is fully tested.",
            "This behavior has regression coverage.",
            "That rejection path is verified automatically.",
            "Both branches are covered by automated checks.",
            "Complete regression coverage exists for it.",
            "Unit tests cover it.",
            "Automated checks exercise that path.",
            "The same branch is fully tested.",
        )
        for contradiction in contradictions:
            artifact_text = _complete_artifact_text().replace(
                disclaimer,
                f"{disclaimer} {contradiction}",
            )
            with (
                self.subTest(contradiction=contradiction),
                tempfile.TemporaryDirectory() as directory,
            ):
                artifact = Path(directory) / "module-design.md"
                artifact.write_text(artifact_text, encoding="utf-8")
                completed = _run_validator("final", artifact=artifact)

            self.assertEqual(3, completed.returncode)
            self.assertFalse(json.loads(completed.stdout)["testClaimsValid"])

    def test_final_validator_accepts_nonanaphoric_that_coverage_claim(self) -> None:
        disclaimer = "The blank-value ValueError branch is source-observed and is not covered by an automated test."
        artifact_text = _complete_artifact_text().replace(
            disclaimer,
            f"{disclaimer} Note that unit tests cover the success path.",
        )
        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        self.assertTrue(json.loads(completed.stdout)["testClaimsValid"])

    def test_final_validator_excludes_html_comments_from_visible_evidence(self) -> None:
        disclaimer = "The blank-value ValueError branch is source-observed and is not covered by an automated test."
        hidden_disclaimer = _complete_artifact_text().replace(
            disclaimer,
            f"<!-- {disclaimer} -->",
        )
        hidden_contradictions = _complete_artifact_text() + (
            "\n<!-- node tools/check.js\nAutomated tests cover the blank-value rejection. -->\n"
        )
        for artifact_text, expected_valid in (
            (hidden_disclaimer, False),
            (hidden_contradictions, True),
        ):
            with (
                self.subTest(expected_valid=expected_valid),
                tempfile.TemporaryDirectory() as directory,
            ):
                artifact = Path(directory) / "module-design.md"
                artifact.write_text(artifact_text, encoding="utf-8")
                completed = _run_validator("final", artifact=artifact)

            self.assertEqual(0 if expected_valid else 3, completed.returncode)
            evidence = json.loads(completed.stdout)
            self.assertEqual(expected_valid, evidence["testClaimsValid"])
            self.assertTrue(evidence["testCommandValid"])

    def test_final_validator_does_not_extend_html_comment_across_quote_depth(
        self,
    ) -> None:
        artifact_text = _complete_artifact_text() + (
            "\n> <!-- quoted comment\nnode tools/check.js\n> -->\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(3, completed.returncode)
        evidence = json.loads(completed.stdout)
        self.assertFalse(evidence["testCommandValid"])
        self.assertIn("node tools/check.js", evidence["commandClaims"])

    def test_final_validator_treats_html_comment_markers_in_fences_as_literal(
        self,
    ) -> None:
        artifact_text = _complete_artifact_text() + (
            "\n```text\n<!-- literal example without a comment close\n```\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        self.assertTrue(json.loads(completed.stdout)["markdownStructureValid"])

    def test_final_validator_excludes_nested_blockquote_fences_from_evidence(
        self,
    ) -> None:
        disclaimer = "The blank-value ValueError branch is source-observed and is not covered by an automated test."
        mutations = (
            (
                _complete_artifact_text()
                .replace("../src/inventory.py", "the inventory source")
                .replace("../tests/test_inventory.py", "the inventory test")
                + (
                    "\n> ```text\n"
                    "> ../src/inventory.py and ../tests/test_inventory.py\n"
                    "> ```\n"
                ),
                "evidenceReferencesValid",
            ),
            (
                _complete_artifact_text().replace(disclaimer, "")
                + f"\n> ```text\n> {disclaimer}\n> ```\n",
                "testClaimsValid",
            ),
        )
        for artifact_text, evidence_key in mutations:
            with (
                self.subTest(evidence_key=evidence_key),
                tempfile.TemporaryDirectory() as directory,
            ):
                artifact = Path(directory) / "module-design.md"
                artifact.write_text(artifact_text, encoding="utf-8")
                completed = _run_validator("final", artifact=artifact)

            self.assertEqual(3, completed.returncode)
            self.assertFalse(json.loads(completed.stdout)[evidence_key])

    def test_final_validator_treats_html_comments_in_nested_fences_as_literal(
        self,
    ) -> None:
        artifact_text = _complete_artifact_text() + (
            "\n> ```text\n> <!-- literal example without a comment close\n> ```\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        self.assertTrue(json.loads(completed.stdout)["markdownStructureValid"])

    def test_final_validator_rejects_cross_container_fence_closure(self) -> None:
        artifact_text = _complete_artifact_text().replace(
            "python3 -m unittest discover -s tests\n```",
            "python3 -m unittest discover -s tests\n> ```",
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(3, completed.returncode)
        self.assertFalse(json.loads(completed.stdout)["markdownStructureValid"])

    def test_final_validator_rejects_cross_container_fence_content(self) -> None:
        mutations = (
            "\n> ```text\nliteral content\n> ```\n",
            "\n```text\n> literal content\n```\n",
        )
        for mutation in mutations:
            with (
                self.subTest(mutation=mutation),
                tempfile.TemporaryDirectory() as directory,
            ):
                artifact = Path(directory) / "module-design.md"
                artifact.write_text(
                    _complete_artifact_text() + mutation,
                    encoding="utf-8",
                )
                completed = _run_validator("final", artifact=artifact)

            self.assertEqual(3, completed.returncode)
            self.assertFalse(json.loads(completed.stdout)["markdownStructureValid"])

    def test_final_validator_treats_nested_blockquotes_as_visible_prose(self) -> None:
        disclaimer = "The blank-value ValueError branch is source-observed and is not covered by an automated test."
        quoted_disclaimer = _complete_artifact_text().replace(
            disclaimer, f"> > {disclaimer}"
        )
        quoted_contradiction = quoted_disclaimer.replace(
            f"> > {disclaimer}",
            f"> > {disclaimer}\n> > It is covered by unit tests.",
        )
        with tempfile.TemporaryDirectory() as directory:
            valid_artifact = Path(directory) / "valid.md"
            invalid_artifact = Path(directory) / "invalid.md"
            valid_artifact.write_text(quoted_disclaimer, encoding="utf-8")
            invalid_artifact.write_text(quoted_contradiction, encoding="utf-8")
            accepted = _run_validator("final", artifact=valid_artifact)
            rejected = _run_validator("final", artifact=invalid_artifact)

        self.assertEqual(0, accepted.returncode, accepted.stdout + accepted.stderr)
        self.assertEqual(3, rejected.returncode)
        self.assertFalse(json.loads(rejected.stdout)["testClaimsValid"])

    def test_final_validator_does_not_count_nested_blockquote_heading_as_structure(
        self,
    ) -> None:
        artifact_text = _complete_artifact_text().replace(
            "## Current Understanding",
            "> > ## Current Understanding",
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "module-design.md"
            artifact.write_text(artifact_text, encoding="utf-8")
            completed = _run_validator("final", artifact=artifact)

        self.assertEqual(3, completed.returncode)
        self.assertFalse(json.loads(completed.stdout)["headingsMatch"])


if __name__ == "__main__":
    unittest.main()
