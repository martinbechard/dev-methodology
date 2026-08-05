# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Verifies exact quotation resolution for retained Wiki Artifact Reviewer evidence.
# Governing test plan: evals/agent-tests/wiki-artifact-reviewer/scenarios.yaml

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

from quotation_traceability import validate_review_quotations


SUITE_ROOT = Path(__file__).resolve().parent
FIXTURE_ROOT = SUITE_ROOT / "fixtures" / "quotation-traceability"


class QuotationTraceabilityTests(unittest.TestCase):
    """Protect exact quotation evidence from plausible paraphrase substitution."""

    def test_resolvable_fixture_accepts_exact_and_omitted_source_text(self) -> None:
        """Exact text and explicitly omitted intervening text remain traceable."""
        diagnostics = validate_review_quotations(
            FIXTURE_ROOT / "resolvable-review.md",
            FIXTURE_ROOT,
        )

        self.assertEqual([], diagnostics)

    def test_absent_paraphrase_fixture_fails_with_source_specific_diagnostic(self) -> None:
        """A plausible sentence cannot pass as an exact quotation when it is absent."""
        diagnostics = validate_review_quotations(
            FIXTURE_ROOT / "absent-paraphrase-review.md",
            FIXTURE_ROOT,
        )

        self.assertEqual(1, len(diagnostics))
        self.assertIn("source.md", diagnostics[0])
        self.assertIn("does not occur exactly", diagnostics[0])

    def test_line_endings_are_normalized_without_rewriting_words_or_punctuation(self) -> None:
        """CRLF and LF compare equally while punctuation remains significant."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source.md").write_bytes(b"First line.\r\nSecond line!\r\n")
            (root / "review.md").write_text(
                "- Evidence type: exact quotation\n"
                "- Evidence source: source.md\n"
                "- Evidence:\n"
                "  > First line.\n"
                "  > Second line!\n",
                encoding="utf-8",
            )
            accepted = validate_review_quotations(root / "review.md", root)
            (root / "review.md").write_text(
                "- Evidence type: exact quotation\n"
                "- Evidence source: source.md\n"
                "- Evidence:\n"
                "  > First line.\n"
                "  > Second line.\n",
                encoding="utf-8",
            )
            rejected = validate_review_quotations(root / "review.md", root)

        self.assertEqual([], accepted)
        self.assertEqual(1, len(rejected))

    def test_inline_evidence_value_resolves_against_the_named_source(self) -> None:
        """The canonical Evidence field accepts concise inline exact text."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source.md").write_text("Exact sentence.\n", encoding="utf-8")
            (root / "review.md").write_text(
                "- Evidence type: exact quotation\n"
                "- Evidence source: source.md\n"
                "- Evidence: Exact sentence.\n",
                encoding="utf-8",
            )

            diagnostics = validate_review_quotations(root / "review.md", root)

        self.assertEqual([], diagnostics)

    def test_lone_carriage_return_is_not_normalized_to_lf(self) -> None:
        """Only CRLF may normalize; a lone carriage return remains significant."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source.md").write_bytes(b"First line.\rSecond line!\n")
            (root / "review.md").write_text(
                "- Evidence type: exact quotation\n"
                "- Evidence source: source.md\n"
                "- Evidence:\n"
                "  > First line.\n"
                "  > Second line!\n",
                encoding="utf-8",
            )

            diagnostics = validate_review_quotations(root / "review.md", root)

        self.assertEqual(1, len(diagnostics))
        self.assertIn("does not occur exactly", diagnostics[0])

    def test_source_resolution_rejects_paths_outside_the_evidence_root(self) -> None:
        """Named evidence cannot escape the frozen suite evidence boundary."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            review = root / "review.md"
            review.write_text(
                "- Evidence type: exact quotation\n"
                "- Evidence source: ../outside.md\n"
                "- Evidence:\n"
                "  > Unavailable text.\n",
                encoding="utf-8",
            )

            diagnostics = validate_review_quotations(review, root)

        self.assertEqual(1, len(diagnostics))
        self.assertIn("outside the evidence root", diagnostics[0])

    def test_suite_contract_routes_exact_quotation_failure_to_the_judge(self) -> None:
        """The accepted scenario and independent Judge share the resolver contract."""
        scenarios = yaml.safe_load((SUITE_ROOT / "scenarios.yaml").read_text(encoding="utf-8"))
        accepted = next(
            scenario
            for scenario in scenarios["scenarios"]
            if scenario["id"] == "accepted-wiki-methodology-artifact"
        )
        contract = (
            SUITE_ROOT / "skills" / "wiki-artifact-reviewer-suite-contract" / "SKILL.md"
        ).read_text(encoding="utf-8")
        judge = (SUITE_ROOT / "agents" / "judge.toml").read_text(encoding="utf-8")

        self.assertIn("Resolve every exact quotation", accepted["requiredBehaviors"])
        self.assertIn("Unsupported exact quotation", accepted["forbiddenBehaviors"])
        self.assertIn("source-link-resolution", accepted["deterministicChecks"])
        self.assertIn("quotation_traceability.py", contract)
        self.assertIn("checklist-integrity failure", contract)
        self.assertIn("checklist-integrity failure", judge)

    def test_approved_skills_share_evidence_and_broken_link_boundaries(self) -> None:
        """Review skills distinguish evidence types and preserve complete reviews."""
        structured = (
            SUITE_ROOT.parents[2] / "skills" / "review-structured-artifact" / "SKILL.md"
        ).read_text(encoding="utf-8")
        wiki_review = (
            SUITE_ROOT.parents[2] / "skills" / "project-wiki-review" / "SKILL.md"
        ).read_text(encoding="utf-8")
        verifier = (
            SUITE_ROOT.parents[2] / "skills" / "verify-documentation-page" / "SKILL.md"
        ).read_text(encoding="utf-8")

        for skill in (structured, wiki_review, verifier):
            with self.subTest(skill=skill.splitlines()[1]):
                self.assertIn("Evidence type", skill)
                self.assertIn("exact quotation", skill)
                self.assertIn("summary", skill)
                self.assertIn("assessment", skill)
                self.assertIn("[omitted]", skill)
        self.assertIn("must not discard or refuse the completed review", verifier)
        self.assertIn("Open Questions", verifier)


if __name__ == "__main__":
    unittest.main()
