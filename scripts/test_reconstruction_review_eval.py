# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies sealed checklist-review corpus validation and promotion decisions.
# Governing design: skills/documentation-reverse-engineer/SKILL.md

from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from types import ModuleType


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
EVALUATION_ROOT = REPOSITORY_ROOT / "evals" / "reconstruction-review"
RUNNER_PATH = EVALUATION_ROOT / "run_checklist_eval.py"
RUNNER_MODULE_NAME = "reconstruction_review_evaluation"


def load_runner() -> ModuleType:
    """Load the evaluation runner from its maintained corpus directory."""
    specification = importlib.util.spec_from_file_location(
        RUNNER_MODULE_NAME,
        RUNNER_PATH,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"Unable to load reconstruction evaluation runner from {RUNNER_PATH}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class ReconstructionReviewEvaluationTests(unittest.TestCase):
    """Exercise corpus and result validation without invoking external models."""

    @classmethod
    def setUpClass(cls) -> None:
        """Load the runner and sealed corpus once for the focused test class."""
        cls.runner = load_runner()
        cls.corpus_path = EVALUATION_ROOT / "corpus.json"
        cls.corpus = cls.runner.load_corpus(cls.corpus_path)
        cls.case = cls.corpus["cases"][0]
        cls.checklist = json.loads(
            (EVALUATION_ROOT / cls.case["checklistPath"]).read_text(encoding="utf-8")
        )
        cls.adjudication = json.loads(
            (EVALUATION_ROOT / cls.case["adjudicationPath"]).read_text(encoding="utf-8")
        )

    def setUp(self) -> None:
        """Create separate disposable result files for each evaluation scenario."""
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.workspace = Path(self.temporary_directory.name)
        self.candidate_path = self.workspace / "candidate.jsonl"
        self.reference_path = self.workspace / "reference.jsonl"

    def _record(
        self,
        reviewer_class: str,
        index: int,
        elapsed_seconds: float,
        token_count: int,
    ) -> dict[str, object]:
        """Create one fully bound checklist result with complete evidence citations."""
        question_ids = [question["id"] for question in self.checklist["questions"]]
        defect_ids = [defect["id"] for defect in self.adjudication["defects"]]
        return {
            "adjudicationSha256": self.case["adjudicationSha256"],
            "answeredQuestionIds": question_ids,
            "artifactSha256": self.case["artifactSha256"],
            "caseId": self.case["id"],
            "checklistVersion": self.case["checklistVersion"],
            "citations": [
                {
                    "questionId": question_id,
                    "quote": f"Synthetic evidence for {question_id}",
                    "sourcePath": self.case["artifactPath"],
                }
                for question_id in question_ids
            ],
            "corpusId": self.corpus["corpusId"],
            "costStatus": "UNAVAILABLE",
            "elapsedSeconds": elapsed_seconds,
            "inputTokens": token_count,
            "invocationId": f"{reviewer_class}-{index}",
            "modelProfile": f"{reviewer_class}-profile",
            "outputTokens": 0,
            "reportedDefectIds": defect_ids,
            "reviewerClass": reviewer_class,
        }

    def _write_results(
        self,
        path: Path,
        reviewer_class: str,
        elapsed_seconds: float,
        token_count: int,
    ) -> None:
        """Write the required three independent invocations for one reviewer class."""
        path.write_text(
            "".join(
                json.dumps(
                    self._record(
                        reviewer_class,
                        index,
                        elapsed_seconds,
                        token_count,
                    ),
                    sort_keys=True,
                )
                + "\n"
                for index in range(3)
            ),
            encoding="utf-8",
        )

    def test_sealed_corpus_identity_and_references_validate(self) -> None:
        """The committed corpus ID reproduces from its four required identity inputs."""
        corpus = self.runner.load_corpus(self.corpus_path)

        self.assertEqual(
            "18eaadac17bf6ab26e6ee3ab22c8785fca850539c90d6924b3a2a253130d8e7e",
            corpus["corpusId"],
        )

    def test_complete_faster_candidate_is_promoted(self) -> None:
        """A candidate passing every quality gate and improving time is promotable."""
        self._write_results(self.candidate_path, "candidate", 75.0, 1000)
        self._write_results(self.reference_path, "reference", 100.0, 1000)

        result = self.runner.evaluate_results(
            self.corpus_path,
            self.candidate_path,
            self.reference_path,
        )

        self.assertEqual("PROMOTE", result["recommendation"])
        self.assertTrue(result["gates"]["quality"])
        self.assertTrue(result["gates"]["efficiency"])

    def test_blocking_defect_miss_retains_reference(self) -> None:
        """Efficiency never offsets one missed adjudicated blocking defect."""
        candidate_records = [
            self._record("candidate", index, 50.0, 500)
            for index in range(3)
        ]
        candidate_records[1]["reportedDefectIds"].pop()
        self.candidate_path.write_text(
            "".join(json.dumps(record, sort_keys=True) + "\n" for record in candidate_records),
            encoding="utf-8",
        )
        self._write_results(self.reference_path, "reference", 100.0, 1000)

        result = self.runner.evaluate_results(
            self.corpus_path,
            self.candidate_path,
            self.reference_path,
        )

        self.assertEqual("RETAIN_REFERENCE", result["recommendation"])
        self.assertFalse(result["gates"]["quality"])

    def test_corpus_id_tampering_is_rejected(self) -> None:
        """Changing the corpus label cannot preserve the sealed evaluation identity."""
        copied_root = self.workspace / "copied-corpus"
        shutil.copytree(EVALUATION_ROOT, copied_root)
        copied_corpus_path = copied_root / "corpus.json"
        copied_corpus = json.loads(copied_corpus_path.read_text(encoding="utf-8"))
        copied_corpus["corpusId"] = "0" * 64
        copied_corpus_path.write_text(
            json.dumps(copied_corpus, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            self.runner.EvaluationError,
            "Corpus ID does not match",
        ):
            self.runner.load_corpus(copied_corpus_path)


if __name__ == "__main__":
    unittest.main()
