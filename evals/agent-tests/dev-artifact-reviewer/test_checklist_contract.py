# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Verifies source-faithful canonical checklist completion for the Dev Artifact Reviewer suite.
# Governing test plan: backlog/feature-backlog/agent-skill-lifecycle/preserve-canonical-review-checklists.md

from __future__ import annotations

import importlib.util
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


_MODULE_PATH = Path(__file__).with_name("checklist_contract.py")
_SPEC = importlib.util.spec_from_file_location("artifact_review_checklist_contract", _MODULE_PATH)
assert _SPEC is not None and _SPEC.loader is not None
contract = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = contract
_SPEC.loader.exec_module(contract)


class ChecklistContractTests(unittest.TestCase):
    """Protect exact checklist questions and completion fields from thematic replacement."""

    def test_accepts_complete_source_order_before_additional_observations(self) -> None:
        """A complete canonical sequence may be followed by concise synthesis."""
        result = self._validate(
            self._canonical(("First objective question?", "Second objective question?")),
            self._completed(("First objective question?", "Second objective question?"))
            + "\n## Additional Observations\n\nConcise synthesis.\n",
        )

        self.assertTrue(result.valid)
        self.assertEqual(2, result.expected_count)
        self.assertEqual(2, result.completed_count)
        self.assertRegex(result.completed_sha256, r"^[0-9a-f]{64}$")
        self.assertEqual((), result.errors)

    def test_rejects_thematic_compression_of_canonical_questions(self) -> None:
        """One thematic item cannot replace two source questions."""
        result = self._validate(
            self._canonical(("First objective question?", "Second objective question?")),
            self._completed(("Combined thematic question?",)),
        )

        self.assertFalse(result.valid)
        self.assertIn("expected 2 completed questions, found 1", result.errors)
        self.assertTrue(any("Q001 wording" in error for error in result.errors))

    def test_rejects_reordering_duplicate_ids_and_missing_canonical_fields(self) -> None:
        """Question identity, order, wording, and source-defined fields are all mandatory."""
        completed = self._completed(("Second objective question?", "First objective question?"))
        completed = completed.replace("## Q002", "## Q001", 1)
        completed = completed.replace("- Authority: authority\n", "", 1)

        result = self._validate(
            self._canonical(("First objective question?", "Second objective question?")),
            completed,
        )

        self.assertFalse(result.valid)
        self.assertTrue(any("identifiers must be Q001, Q002" in error for error in result.errors))
        self.assertTrue(any("Q001 wording" in error for error in result.errors))
        self.assertTrue(any("Authority" in error for error in result.errors))

    def test_rejects_synthesis_before_the_canonical_sequence_is_complete(self) -> None:
        """An arbitrarily named synthesis section cannot interrupt checklist evidence."""
        completed = self._completed(("First objective question?",))
        completed += "\n## Review Synthesis\n\nPremature synthesis.\n"
        completed += self._completed(("Second objective question?",)).replace("## Q001", "## Q002")

        result = self._validate(
            self._canonical(("First objective question?", "Second objective question?")),
            completed,
        )

        self.assertFalse(result.valid)
        self.assertIn("a non-record section appears before all canonical records", result.errors)

    def test_validates_generic_and_specialized_checklists_independently(self) -> None:
        """A valid generic checklist cannot hide an incomplete specialized checklist."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            generic_source = (
                root
                / "skills/review-structured-artifact/references/review-checklist-structured.md"
            )
            generic_completed = root / "target.review-checklist-structured.md"
            specialized_source = (
                root
                / "skills/review-functional-spec/references/review-checklist-functional-spec.md"
            )
            specialized_completed = root / "target.review-checklist-functional-spec.md"
            generic_source.parent.mkdir(parents=True)
            specialized_source.parent.mkdir(parents=True)
            generic_source.write_text(self._canonical(("Generic question?",)), encoding="utf-8")
            generic_completed.write_text(self._completed(("Generic question?",)), encoding="utf-8")
            specialized_source.write_text(self._canonical(("Specific one?", "Specific two?")), encoding="utf-8")
            specialized_completed.write_text(self._completed(("Specific one?",)), encoding="utf-8")

            results = contract.validate_checklist_pairs(
                (
                    (generic_source, generic_completed),
                    (specialized_source, specialized_completed),
                ),
                repository_root=root,
            )

        self.assertEqual((True, False), tuple(result.valid for result in results))
        self.assertEqual((1, 2), tuple(result.expected_count for result in results))

    def test_current_canonical_sources_have_stable_unique_question_sequences(self) -> None:
        """The validator reads the live generic and functional checklist sources without compression."""
        repository = Path(__file__).resolve().parents[3]
        sources = (
            repository / "skills/review-structured-artifact/references/review-checklist-structured.md",
            repository / "skills/review-functional-spec/references/review-checklist-functional-spec.md",
        )

        contracts = tuple(contract.load_canonical_checklist(path) for path in sources)

        self.assertEqual((36, 25), tuple(len(value.questions) for value in contracts))
        for value in contracts:
            self.assertEqual(len(value.questions), len(set(value.questions)))
            self.assertRegex(value.sha256, r"^[0-9a-f]{64}$")

    def test_rejects_an_alternate_same_name_canonical_source(self) -> None:
        """A fake same-named checklist cannot produce critical-gate evidence."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            canonical = root / "review-checklist-structured.md"
            completed = root / "target.review-checklist-structured.md"
            canonical.write_text(self._canonical(("Thematic replacement?",)), encoding="utf-8")
            completed.write_text(self._completed(("Thematic replacement?",)), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "outside the repository"):
                contract.validate_completed_checklist(canonical, completed)

    def test_binds_the_exact_completed_evidence_bytes(self) -> None:
        """The retained result digest identifies the completed checklist being judged."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            canonical = root / "skills/review-example/references/review-checklist-example.md"
            completed = root / "evidence/target.review-checklist-example.md"
            canonical.parent.mkdir(parents=True)
            completed.parent.mkdir(parents=True)
            canonical.write_text(self._canonical(("Objective question?",)), encoding="utf-8")
            completed_bytes = self._completed(("Objective question?",)).encode("utf-8")
            completed.write_bytes(completed_bytes)

            result = contract.validate_completed_checklist(
                canonical, completed, repository_root=root
            )

        self.assertEqual("evidence/target.review-checklist-example.md", result.completed)
        self.assertEqual(hashlib.sha256(completed_bytes).hexdigest(), result.completed_sha256)

    def test_suite_routes_all_three_scenarios_through_the_critical_validator(self) -> None:
        """The staged supervisor and deterministic catalog enforce the validator in live runs."""
        repository = Path(__file__).resolve().parents[3]
        scenario_document = yaml.safe_load(
            (repository / "evals/agent-tests/dev-artifact-reviewer/scenarios.yaml").read_text(
                encoding="utf-8"
            )
        )
        judge_document = yaml.safe_load(
            (repository / "evals/judges.yaml").read_text(encoding="utf-8")
        )
        checks = {entry["id"]: entry for entry in judge_document["checks"]}
        supervisor = (
            repository / "evals/agent-tests/dev-artifact-reviewer/agents/supervisor.toml"
        ).read_text(encoding="utf-8")

        for scenario in scenario_document["scenarios"]:
            self.assertIn("checklist-completeness", scenario["deterministicChecks"])
        self.assertTrue(checks["checklist-completeness"]["critical"])
        self.assertIn("checklist_contract.py", supervisor)
        self.assertIn(
            "one --pair for each applicable repository-owned canonical source", supervisor
        )

    def _validate(self, canonical_text: str, completed_text: str):
        """Write one synthetic pair and return its validation result."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            canonical = (
                root / "skills/review-example/references/review-checklist-example.md"
            )
            completed = root / "target.review-checklist-example.md"
            canonical.parent.mkdir(parents=True)
            canonical.write_text(canonical_text, encoding="utf-8")
            completed.write_text(completed_text, encoding="utf-8")
            return contract.validate_completed_checklist(
                canonical, completed, repository_root=root
            )

    @staticmethod
    def _canonical(questions: tuple[str, ...]) -> str:
        """Build a minimal canonical checklist with the generic completion fields."""
        fields = (
            "Status: pass, fail, question, or n/a.",
            "Question: copy the objective question being answered.",
            "Quoted evidence: quote the exact target text.",
            "Assessment: explain the status.",
            "Correction: state the expected change.",
            "Authority: cite the supporting rule.",
            "Impact: state the practical consequence.",
        )
        return (
            "# Example Checklist\n\n## Completion Format\n\n"
            + "".join(f"- {field}\n" for field in fields)
            + "\n## Questions\n\n"
            + "".join(f"- Question: {question}\n" for question in questions)
        )

    @staticmethod
    def _completed(questions: tuple[str, ...]) -> str:
        """Build completed records using every generic canonical field."""
        records = []
        for index, question in enumerate(questions, start=1):
            records.append(
                f"## Q{index:03d}\n\n"
                "- Status: pass\n"
                f"- Question: {question}\n"
                "- Quoted evidence: evidence\n"
                "- Assessment: assessment\n"
                "- Correction: correction\n"
                "- Authority: authority\n"
                "- Impact: impact\n"
            )
        return "\n".join(records)


if __name__ == "__main__":
    unittest.main()
