# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies reviewer fixtures, isolated candidate staging, and digest-bound evaluator handoffs.

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SUITE_ROOT = Path(__file__).resolve().parent


class DevCodeReviewerFixtureTests(unittest.TestCase):
    def run_fixture_tests(self, fixture_name: str, test_file: str) -> None:
        fixture = SUITE_ROOT / "fixtures" / fixture_name
        completed = subprocess.run(
            [sys.executable, "-m", "unittest", test_file],
            cwd=fixture,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)

    def test_clean_review_fixture_is_green(self) -> None:
        self.run_fixture_tests("justified-clean-review", "test_retry_policy.py")

    def test_incomplete_review_fixture_exposes_missing_upgrade_evidence(self) -> None:
        fixture = SUITE_ROOT / "fixtures" / "incomplete-review-evidence"
        status = json.loads((fixture / "upgrade-fixture-status.json").read_text())

        self.assertEqual("unavailable", status["status"])
        self.assertEqual(1, status["requiredVersion"])
        self.run_fixture_tests("incomplete-review-evidence", "test_migration.py")

    def run_synthesis_evaluator(
        self,
        case_id: str,
        synthesis: dict[str, object],
    ) -> subprocess.CompletedProcess[str]:
        """Evaluate one captured synthesis kept outside the fixture contract."""
        fixture = SUITE_ROOT / "fixtures" / "header-policy-authority-boundary"
        with tempfile.TemporaryDirectory() as directory:
            candidate_output = Path(directory) / "captured-synthesis.json"
            candidate_output.write_text(json.dumps(synthesis), encoding="utf-8")
            return subprocess.run(
                [
                    sys.executable,
                    str(fixture / "evaluate_synthesis.py"),
                    "--case",
                    case_id,
                    "--candidate-output",
                    str(candidate_output),
                ],
                cwd=fixture,
                capture_output=True,
                text=True,
                check=False,
            )

    def test_explicit_policy_accepts_paraphrase_with_structured_semantics(self) -> None:
        """Explanatory wording is free when independent semantic fields are correct."""
        completed = self.run_synthesis_evaluator(
            "explicit-header-policy",
            {
                "confirmedFindings": [
                    {
                        "summary": "The source omits the audit marker required by local policy.",
                        "authority": {
                            "source": "fixture-policy.md",
                            "location": {"line": 3},
                            "meaning": "provenance-header-required",
                            "description": "Tracked files need an authorship marker.",
                        },
                        "target": {"source": "src/price.ts", "location": {"line": 1}},
                        "contradiction": {
                            "expected": "provenance-header-present",
                            "observed": "provenance-header-absent",
                        },
                        "impact": {
                            "category": "traceability",
                            "meaning": "source-provenance-unverifiable",
                            "description": "Reviewers cannot trace how the file was produced.",
                        },
                        "uncertaintyClassification": "confirmed",
                    }
                ],
                "openQuestions": [],
            },
        )

        self.assertEqual(0, completed.returncode, completed.stderr)

    def test_explicit_policy_rejects_copied_fields_without_contradiction(self) -> None:
        """Copied-looking source and impact evidence cannot replace an observation."""
        completed = self.run_synthesis_evaluator(
            "explicit-header-policy",
            {
                "confirmedFindings": [
                    {
                        "summary": "The changed source violates the explicit provenance audit requirement.",
                        "authority": {
                            "source": "fixture-policy.md",
                            "location": {"line": 3},
                            "meaning": "provenance-header-required",
                        },
                        "target": {"source": "src/price.ts", "location": {"line": 1}},
                        "impact": {
                            "category": "traceability",
                            "meaning": "source-provenance-unverifiable",
                        },
                        "uncertaintyClassification": "confirmed",
                    }
                ],
                "openQuestions": [],
            },
        )

        self.assertNotEqual(0, completed.returncode)
        self.assertIn("explicit observed contradiction is missing", completed.stderr)

    def test_explicit_policy_checks_each_structured_semantic_field(self) -> None:
        """Every authority, target, contradiction, impact, and certainty field is material."""
        fixture = SUITE_ROOT / "fixtures" / "header-policy-authority-boundary"
        expected = json.loads((fixture / "expected-results.json").read_text())
        required = expected["cases"]["explicit-header-policy"]["requiredFinding"]
        mutations = (
            (("authority", "source"), "other-policy.md"),
            (("authority", "location", "line"), 4),
            (("authority", "meaning"), "optional-provenance-header"),
            (("target", "source"), "src/other.ts"),
            (("target", "location", "line"), 2),
            (("contradiction", "expected"), "provenance-header-optional"),
            (("contradiction", "observed"), "provenance-header-present"),
            (("impact", "category"), "formatting"),
            (("impact", "meaning"), "cosmetic-only"),
            (("uncertaintyClassification",), "uncertain"),
        )

        for path, replacement in mutations:
            with self.subTest(field=".".join(path)):
                candidate = json.loads(json.dumps(required))
                current = candidate
                for key in path[:-1]:
                    current = current[key]
                current[path[-1]] = replacement
                completed = self.run_synthesis_evaluator(
                    "explicit-header-policy",
                    {"confirmedFindings": [candidate], "openQuestions": []},
                )
                self.assertNotEqual(0, completed.returncode, path)

    def test_absent_policy_accepts_structured_uncertainty(self) -> None:
        """Missing authority remains an open question with independently typed evidence."""
        completed = self.run_synthesis_evaluator(
            "absent-header-policy",
            {
                "confirmedFindings": [],
                "openQuestions": [
                    {
                        "summary": "Confirm whether this repository requires provenance headers.",
                        "authority": {"status": "missing", "source": None, "location": None},
                        "target": {"source": "src/price.ts", "location": {"line": 1}},
                        "contradiction": {
                            "expected": "applicable-policy-established",
                            "observed": "applicable-policy-not-supplied",
                        },
                        "impact": {
                            "category": "decision-risk",
                            "meaning": "requirement-cannot-be-confirmed",
                        },
                        "uncertaintyClassification": "missing-authority",
                    }
                ],
            },
        )

        self.assertEqual(0, completed.returncode, completed.stderr)

    def test_absent_policy_rejects_structured_unsupported_promotion(self) -> None:
        """A confirmed finding remains invalid when the authority field is explicitly missing."""
        question = {
            "authority": {"status": "missing", "source": None, "location": None},
            "target": {"source": "src/price.ts", "location": {"line": 1}},
            "contradiction": {
                "expected": "applicable-policy-established",
                "observed": "applicable-policy-not-supplied",
            },
            "impact": {
                "category": "decision-risk",
                "meaning": "requirement-cannot-be-confirmed",
            },
            "uncertaintyClassification": "missing-authority",
        }
        completed = self.run_synthesis_evaluator(
            "absent-header-policy",
            {
                "confirmedFindings": [
                    {
                        "authority": question["authority"],
                        "target": question["target"],
                        "impact": question["impact"],
                        "uncertaintyClassification": "confirmed",
                    }
                ],
                "openQuestions": [question],
            },
        )

        self.assertNotEqual(0, completed.returncode)
        self.assertIn("unsupported confirmed finding", completed.stderr)

    def test_absent_policy_rejects_duplicate_uncertainty_locations(self) -> None:
        """The missing-authority observation has one canonical openQuestions location."""
        question = {
            "authority": {"status": "missing", "source": None, "location": None},
            "target": {"source": "src/price.ts", "location": {"line": 1}},
            "contradiction": {
                "expected": "applicable-policy-established",
                "observed": "applicable-policy-not-supplied",
            },
            "impact": {
                "category": "decision-risk",
                "meaning": "requirement-cannot-be-confirmed",
            },
            "uncertaintyClassification": "missing-authority",
        }
        completed = self.run_synthesis_evaluator(
            "absent-header-policy",
            {
                "confirmedFindings": [],
                "openQuestions": [question, question],
            },
        )

        self.assertNotEqual(0, completed.returncode)
        self.assertIn("exactly one openQuestions item", completed.stderr)

    def test_absent_policy_rejects_duplicate_residual_risk(self) -> None:
        """The missing-authority observation cannot be repeated as residual risk."""
        question = {
            "authority": {"status": "missing", "source": None, "location": None},
            "target": {"source": "src/price.ts", "location": {"line": 1}},
            "contradiction": {
                "expected": "applicable-policy-established",
                "observed": "applicable-policy-not-supplied",
            },
            "impact": {
                "category": "decision-risk",
                "meaning": "requirement-cannot-be-confirmed",
            },
            "uncertaintyClassification": "missing-authority",
        }
        completed = self.run_synthesis_evaluator(
            "absent-header-policy",
            {
                "confirmedFindings": [],
                "openQuestions": [question],
                "residualRisk": [question],
            },
        )

        self.assertNotEqual(0, completed.returncode)
        self.assertIn("must not be duplicated in residualRisk", completed.stderr)

    def test_authority_fixture_keeps_evaluator_inputs_outside_candidates(self) -> None:
        """Candidate workspaces contain only their assigned source and authority state."""
        fixture = SUITE_ROOT / "fixtures" / "header-policy-authority-boundary"
        candidate_inputs = fixture / "candidate-inputs"

        for evaluator_input in ("expected-results.json", "evaluate_synthesis.py"):
            self.assertFalse(
                (fixture / evaluator_input).resolve().is_relative_to(
                    candidate_inputs.resolve()
                )
            )
        absent = candidate_inputs / "absent-header-policy"
        explicit = candidate_inputs / "explicit-header-policy"
        self.assertTrue((absent / "TASK.md").is_file())
        self.assertTrue((absent / "src" / "price.ts").is_file())
        self.assertFalse((absent / "fixture-policy.md").exists())
        self.assertTrue((explicit / "TASK.md").is_file())
        self.assertTrue((explicit / "src" / "price.ts").is_file())
        self.assertTrue((explicit / "fixture-policy.md").is_file())

    def test_candidate_staging_enforces_evaluator_input_boundary(self) -> None:
        """The executable staging boundary exposes one case without evaluator inputs."""
        fixture = SUITE_ROOT / "fixtures" / "header-policy-authority-boundary"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            destination = root / "candidate"
            manifest = root / "candidate-manifest.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(fixture / "stage_candidate.py"),
                    "--case",
                    "explicit-header-policy",
                    "--destination",
                    str(destination),
                    "--manifest",
                    str(manifest),
                ],
                cwd=fixture,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(0, completed.returncode, completed.stderr)
            staged = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(destination.resolve().as_posix(), staged["candidateRoot"])
            self.assertEqual("explicit-header-policy", staged["case"])
            self.assertEqual(
                {
                    "allowedReadRoot": destination.resolve().as_posix(),
                    "oracleFilesPresent": False,
                },
                staged["accessBoundary"],
            )
            self.assertTrue((destination / "src" / "price.ts").is_file())
            self.assertTrue((destination / "fixture-policy.md").is_file())
            self.assertFalse((destination / "evaluate_synthesis.py").exists())
            self.assertFalse((destination / "expected-results.json").exists())
            expected_paths = ["TASK.md", "fixture-policy.md", "src/price.ts"]
            self.assertEqual(expected_paths, [entry["path"] for entry in staged["files"]])
            for entry in staged["files"]:
                staged_file = destination / entry["path"]
                self.assertEqual(
                    hashlib.sha256(staged_file.read_bytes()).hexdigest(),
                    entry["sha256"],
                )
                self.assertEqual(0o444, staged_file.stat().st_mode & 0o777)
            for staged_directory in (destination, destination / "src"):
                self.assertEqual(0o555, staged_directory.stat().st_mode & 0o777)

            rejected = subprocess.run(
                [
                    sys.executable,
                    str(fixture / "stage_candidate.py"),
                    "--case",
                    "absent-header-policy",
                    "--destination",
                    str(fixture / "candidate-inputs" / "nested"),
                    "--manifest",
                    str(root / "rejected.json"),
                ],
                cwd=fixture,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(0, rejected.returncode)
            self.assertIn("candidate destination overlaps evaluator-owned fixture", rejected.stderr)

    def test_candidate_staging_rejects_evaluator_owned_manifest_path(self) -> None:
        """The staging manifest cannot replace an evaluator-owned expected result."""
        fixture = SUITE_ROOT / "fixtures" / "header-policy-authority-boundary"
        expectations = fixture / "expected-results.json"
        original_digest = hashlib.sha256(expectations.read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory() as directory:
            completed = subprocess.run(
                [
                    sys.executable,
                    str(fixture / "stage_candidate.py"),
                    "--case",
                    "absent-header-policy",
                    "--destination",
                    str(Path(directory) / "candidate"),
                    "--manifest",
                    str(expectations),
                ],
                cwd=fixture,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertNotEqual(0, completed.returncode)
        self.assertIn("candidate manifest overlaps evaluator-owned fixture", completed.stderr)
        self.assertEqual(original_digest, hashlib.sha256(expectations.read_bytes()).hexdigest())

    def test_evaluator_handoff_binds_exact_capture_and_evaluator_identity(self) -> None:
        """Passing evaluation evidence identifies every byte sequence consumed by the gate."""
        fixture = SUITE_ROOT / "fixtures" / "header-policy-authority-boundary"
        synthesis = {
            "confirmedFindings": [],
            "openQuestions": [
                {
                    "authority": {"status": "missing", "source": None, "location": None},
                    "target": {"source": "src/price.ts", "location": {"line": 1}},
                    "contradiction": {
                        "expected": "applicable-policy-established",
                        "observed": "applicable-policy-not-supplied",
                    },
                    "impact": {
                        "category": "decision-risk",
                        "meaning": "requirement-cannot-be-confirmed",
                    },
                    "uncertaintyClassification": "missing-authority",
                }
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            capture = root / "capture.json"
            handoff = root / "handoff.json"
            capture.write_text(json.dumps(synthesis), encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable,
                    str(fixture / "evaluate_synthesis.py"),
                    "--case",
                    "absent-header-policy",
                    "--candidate-output",
                    str(capture),
                ],
                cwd=fixture,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            evidence = json.loads(completed.stdout)
            handoff.write_text(completed.stdout, encoding="utf-8")

            self.assertEqual("dev-code-reviewer-authority-evaluation", evidence["schema"])
            self.assertEqual("absent-header-policy", evidence["case"])
            self.assertEqual("passed", evidence["verdict"])
            self.assertEqual("absent-header-policy", evidence["bindings"]["case"])
            self.assertEqual(hashlib.sha256(capture.read_bytes()).hexdigest(), evidence["bindings"]["capturedSynthesisSha256"])
            self.assertEqual(hashlib.sha256((fixture / "evaluate_synthesis.py").read_bytes()).hexdigest(), evidence["bindings"]["evaluatorSha256"])
            self.assertEqual(hashlib.sha256((fixture / "expected-results.json").read_bytes()).hexdigest(), evidence["bindings"]["expectationsSha256"])

            verified = subprocess.run(
                [
                    sys.executable,
                    str(fixture / "evaluate_synthesis.py"),
                    "--verify-handoff",
                    str(handoff),
                    "--candidate-output",
                    str(capture),
                ],
                cwd=fixture,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, verified.returncode, verified.stderr)
            self.assertEqual("bound", json.loads(verified.stdout)["verdict"])

            altered_case = json.loads(json.dumps(evidence))
            altered_case["case"] = "explicit-header-policy"
            handoff.write_text(json.dumps(altered_case), encoding="utf-8")
            rejected_case = subprocess.run(
                [
                    sys.executable,
                    str(fixture / "evaluate_synthesis.py"),
                    "--verify-handoff",
                    str(handoff),
                    "--candidate-output",
                    str(capture),
                ],
                cwd=fixture,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(0, rejected_case.returncode)
            self.assertIn("evaluation case does not match handoff", rejected_case.stderr)
            handoff.write_text(completed.stdout, encoding="utf-8")

            capture.write_text(json.dumps({"confirmedFindings": [], "openQuestions": []}), encoding="utf-8")
            drifted = subprocess.run(
                [
                    sys.executable,
                    str(fixture / "evaluate_synthesis.py"),
                    "--verify-handoff",
                    str(handoff),
                    "--candidate-output",
                    str(capture),
                ],
                cwd=fixture,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(0, drifted.returncode)
            self.assertIn("captured synthesis SHA-256 does not match handoff", drifted.stderr)

            capture.write_text(json.dumps(synthesis), encoding="utf-8")
            for field, expected_error in (
                ("evaluatorSha256", "evaluator SHA-256 does not match handoff"),
                ("expectationsSha256", "expectations SHA-256 does not match handoff"),
            ):
                with self.subTest(binding=field):
                    altered = json.loads(json.dumps(evidence))
                    altered["bindings"][field] = "0" * 64
                    handoff.write_text(json.dumps(altered), encoding="utf-8")
                    rejected = subprocess.run(
                        [
                            sys.executable,
                            str(fixture / "evaluate_synthesis.py"),
                            "--verify-handoff",
                            str(handoff),
                            "--candidate-output",
                            str(capture),
                        ],
                        cwd=fixture,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertNotEqual(0, rejected.returncode)
                    self.assertIn(expected_error, rejected.stderr)

    def test_authority_tasks_and_scenario_use_one_absent_policy_contract(self) -> None:
        """The changed-file fact and missing-authority placement are unambiguous inputs."""
        fixture = SUITE_ROOT / "fixtures" / "header-policy-authority-boundary"
        positive_task = (fixture / "candidate-inputs" / "explicit-header-policy" / "TASK.md").read_text()
        scenario = (SUITE_ROOT / "scenarios.yaml").read_text()

        self.assertIn("The changed file is src/price.ts.", positive_task)
        self.assertIn("Keep the absent-header-policy observation in exactly one openQuestions item", scenario)
        self.assertNotIn("open questions or residual risk", scenario)


if __name__ == "__main__":
    unittest.main()
