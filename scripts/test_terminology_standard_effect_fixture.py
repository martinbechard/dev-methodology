# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Protects the positive-only terminology rewrite evaluation contract.

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


_ROOT = (
    Path(__file__).resolve().parents[1]
    / "evals"
    / "projects"
    / "terminology-standard-effect"
)
_SOURCE = _ROOT / "source-document.md"
_STANDARD = _ROOT / "terminology.md"
_CASES = Path(__file__).resolve().parents[1] / "evals" / "cases.yaml"

_CONFORMING_SENTENCES = {
    "TERM-01": "The Acceptance criterion AC-17 requires the Artifact to retain all 35 concept statements.",
    "TERM-02": "The Agent uses the `dev_documentation_writer` model, instructions, context, and tools within delegated authority.",
    "TERM-03": "The Agent harness supplies the runtime, tools, context, and lifecycle controls for the arbitrary writing Workflow.",
    "TERM-04": "The rewritten guide is the durable Artifact created by this work.",
    "TERM-05": "The Backlog contains every Work item used for planning and coordination, regardless of lifecycle state.",
    "TERM-06": "The Business scenario describes the release problem, business participants, context, and desired outcome.",
    "TERM-07": "The Campaign coordinates the bounded Evaluation runs for release baseline build-2026.08.08.",
    "TERM-08": "Contract validation checks that the JSON field `agent_role` satisfies its schema and allowed values.",
    "TERM-09": "A Defect is recorded when observed behavior reproducibly differs from required behavior.",
    "TERM-10": "An Evaluation applies defined criteria to an Artifact during testing or an operating agentic Workflow.",
    "TERM-11": "Each Evaluation case varies one input while the target configuration and criteria remain fixed.",
    "TERM-12": "The Evaluation decision normalizes the completed checks and judgments to PASS or FAIL.",
    "TERM-13": "The Evaluation portfolio is the governed stable collection available for selection across releases.",
    "TERM-14": "The Evaluation result records a decision, label, or score with supporting Evidence.",
    "TERM-15": "An Evaluation run executes one Evaluation against the specified target configuration.",
    "TERM-16": "The Evaluation suite groups related Evaluations for documentation agents.",
    "TERM-17": "The Evaluator agent performs the Evaluation; a human participant remains a QA analyst or expert evaluator.",
    "TERM-18": "Evidence is retained information that supports or contradicts a claim about an Artifact, action, or result.",
    "TERM-19": "The Requirement states a documented capability, behavior, quality, or constraint that the Artifact must satisfy.",
    "TERM-20": "The Review examines the Artifact and reports findings without changing it.",
    "TERM-21": "The Skill is a reusable instruction package that teaches an Agent a bounded kind of work.",
    "TERM-22": "The Test repeatably compares observed behavior with an expected result.",
    "TERM-23": "The Test case specifies the preconditions, inputs, actions, expected results, and postconditions for one Test.",
    "TERM-24": "The Test condition identifies the testable aspect used to derive Test cases.",
    "TERM-25": "The Test fixture establishes controlled data, files, configuration, and starting environment state.",
    "TERM-26": "The Test harness prepares and executes tests in a controlled environment.",
    "TERM-27": "The Test report retains the scope, environment, results, Evidence, and limitations of the Test runs.",
    "TERM-28": "The Test result records the outcome and supporting Evidence produced by executing one Test case.",
    "TERM-29": "The Test run executes 26 Test suites and 78 selected Test cases in the defined environment.",
    "TERM-30": "The Test suite is the stable named collection of related Test cases, independent of an execution.",
    "TERM-31": "The Use case specifies system behavior through interactions with actors that achieve a goal.",
    "TERM-32": "The User story is the informal evolving expression of a user need used in agile planning.",
    "TERM-33": "Verification runs `python3 verify.py` and uses Evidence to check that a claimed result satisfies Requirements and Acceptance criteria.",
    "TERM-34": "The Work item is the bounded unit of planned work with an objective, owner, state, and completion conditions.",
    "TERM-35": "The Workflow is the defined sequence of activities, decisions, and handoffs that produces the intended result.",
}


def _conforming_artifact() -> str:
    body = "\n\n".join(
        f"[{marker}] {sentence}" for marker, sentence in _CONFORMING_SENTENCES.items()
    )
    return f"# Clear Evaluation Program Guide\n\n{body}\n"


def _run_verifier(artifact_text: str) -> subprocess.CompletedProcess[str]:
    catalog = yaml.safe_load(_CASES.read_text(encoding="utf-8"))
    case = next(
        item
        for item in catalog["cases"]
        if item["id"] == "terminology-standard-effect"
    )
    command = case["verify"]["argv"]
    with tempfile.TemporaryDirectory() as directory:
        artifact = Path(directory) / "rewritten-document.md"
        artifact.write_text(artifact_text, encoding="utf-8")
        return subprocess.run(
            [sys.executable, *command[1:]],
            cwd=directory,
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )


class TerminologyEffectVerifierTests(unittest.TestCase):
    """Keep the experimental red/green contract positive-first and auditable."""

    def test_standard_contains_every_preferred_term_and_no_avoid_rules(self) -> None:
        standard = _STANDARD.read_text(encoding="utf-8")

        self.assertNotIn("\nAvoid:", standard)
        for sentence in _CONFORMING_SENTENCES.values():
            preferred_term = sentence.split(" ", 2)[1] if sentence.startswith("The ") else sentence.split(" ", 1)[0]
            self.assertTrue(preferred_term)

        headings = {
            line.removeprefix("### ")
            for line in standard.splitlines()
            if line.startswith("### ")
        }
        self.assertEqual(
            {
                "Acceptance criterion", "Agent", "Agent harness", "Artifact", "Backlog",
                "Business scenario", "Campaign", "Contract validation", "Defect", "Evaluation",
                "Evaluation case", "Evaluation decision", "Evaluation portfolio", "Evaluation result",
                "Evaluation run", "Evaluation suite", "Evaluator agent", "Evidence", "Requirement",
                "Review", "Skill", "Test", "Test case", "Test condition", "Test fixture",
                "Test harness", "Test report", "Test result", "Test run", "Test suite", "Use case",
                "User story", "Verification", "Work item", "Workflow",
            },
            headings,
        )

    def test_unchanged_source_fails_positive_terminology_conformance(self) -> None:
        completed = _run_verifier(_SOURCE.read_text(encoding="utf-8"))

        self.assertEqual(3, completed.returncode)
        evidence = json.loads(completed.stdout)
        self.assertFalse(evidence["preferredTerminologyValid"])
        self.assertTrue(evidence["semanticMarkersValid"])

    def test_conforming_rewrite_passes_with_clean_scratchpad_observation(self) -> None:
        completed = _run_verifier(_conforming_artifact())

        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        evidence = json.loads(completed.stdout)
        self.assertTrue(evidence["preferredTerminologyValid"])
        self.assertTrue(evidence["semanticMarkersValid"])
        self.assertTrue(evidence["protectedLiteralsValid"])
        self.assertEqual([], evidence["scratchpadCandidateOccurrences"])

    def test_missing_meaning_marker_fails(self) -> None:
        artifact = _conforming_artifact().replace("[TERM-19] ", "", 1)
        completed = _run_verifier(artifact)

        self.assertEqual(3, completed.returncode)
        self.assertFalse(json.loads(completed.stdout)["semanticMarkersValid"])

    def test_scratchpad_candidate_is_reported_without_becoming_a_normative_rule(self) -> None:
        artifact = _conforming_artifact().replace(
            "The Test run executes 26 Test suites",
            "The Test run rollout executes 26 Test suites",
        )
        completed = _run_verifier(artifact)

        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        evidence = json.loads(completed.stdout)
        self.assertEqual(
            [{"candidate": "rollout", "marker": "TERM-29"}],
            evidence["scratchpadCandidateOccurrences"],
        )


if __name__ == "__main__":
    unittest.main()
