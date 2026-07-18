#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Verifies project-wiki setup, ingest, digest, linking, and verifier guidance.

"""Regression tests for project wiki setup guidance."""

from __future__ import annotations

import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_DOCUMENT = SKILL_ROOT / "SKILL.md"
OPERATIONS_REFERENCE = SKILL_ROOT / "references" / "operations.md"
PAGE_SCHEMA_REFERENCE = SKILL_ROOT / "references" / "page-schema.md"
VERIFICATION_CHECKLIST = SKILL_ROOT / "references" / "topic-page-verification-checklist.md"
CORE_IMPLEMENTATION = SKILL_ROOT / "scripts" / "project_wiki_ops" / "core.py"
CONSTANTS_IMPLEMENTATION = SKILL_ROOT / "scripts" / "project_wiki_ops" / "constants.py"
TOPIC_WRITER_SKILL = SKILL_ROOT.parent / "project-wiki-topic-write" / "SKILL.md"
TOPIC_VERIFIER_SKILL = SKILL_ROOT.parent / "project-wiki-topic-verify" / "SKILL.md"
WIKI_OPS_COMMAND_PREFIX = "python3 project-wiki-skill-root/scripts/wiki_ops.py"

DIGEST_REPAIR_PHRASES = [
    "When repairing an existing digest, inspect the current month page for bundled dated paragraphs and rewrite the requested date range into item-level synopsis entries instead of only appending new entries.",
    "Reorder the affected Current Understanding entries into reverse chronological order by entry date before finishing.",
    "Use durable leaf pages as the content anchor for digest prose; keep source files in Authoritative Sources as provenance rather than repeating source-log wording.",
    "Do not create separate digest entries for duplicate raw captures or repeated source-window sightings unless they add distinct content; fold them into the existing item or closely coupled product-family entry.",
]

RAW_INGEST_AUTOMATION_PHRASES = [
    "Raw-source ingest automation prompts must repeat the digest granularity and ordering rules directly: one digest entry per independently changing item or closely coupled product family; never group digest entries by raw source artifact, collector run, sweep category, or ingestion batch; keep monthly digest Current Understanding entries in reverse chronological order by entry date.",
    "When a digest page changes, the automation closeout must report that digest granularity and ordering were checked with the project-wiki-topic-verify checklist, or that the full verifier returned GOOD.",
    "High-volume raw sources may update many durable leaves without forcing every touched leaf into the digest; omit low-signal digest mentions rather than compress unrelated entities into a vague grouped bullet.",
]

LEAF_LINKING_PHRASES = [
    "Run the leaf-link pass after creating or updating a durable leaf page.",
    "Use repository grep to find existing wiki mentions of each leaf title before finishing.",
    "A page that mentions a durable leaf title should link the first unlinked mention to that leaf unless the mention is inside a heading, code fence, or existing link.",
    f"{WIKI_OPS_COMMAND_PREFIX} link-leaves",
]

OKF_GUIDANCE_PHRASES = [
    "Project wikis should be OKF-compatible.",
    "Non-reserved Markdown concept documents should have YAML frontmatter with a non-empty type field",
    "Folder index.md and log.md files are OKF reserved files",
    f"{WIKI_OPS_COMMAND_PREFIX} okf-migrate",
    f"{WIKI_OPS_COMMAND_PREFIX} okf-validate",
]

AGENTS_GUIDANCE_PHRASES = [
    "Add AGENTS.md wiki workflow guidance during setup.",
    "use the project-wiki-query skill for wiki-backed questions and lightweight project knowledge lookups",
    "check docs/wiki first when answering project questions",
    "save a raw wiki fragment under raw before synthesizing it into docs/wiki",
    "commit wiki changes with the source, test, or documentation changes that made them necessary",
]

COMMIT_GUIDANCE_PHRASES = [
    "When committing a task, include docs/wiki pages, raw fragments, raw/processed moves, wiki helper scripts, and related AGENTS.md guidance in the same coherent commit as the source, test, or documentation changes that made them necessary.",
    "If a task changes only wiki artifacts, commit that verified wiki-only slice on its own.",
    "Do not leave docs/wiki, raw fragments, or raw/processed moves unstaged after committing the related task.",
]

ON_DEMAND_RESEARCH_PHRASES = [
    "project-wiki-research skill",
    "On-demand research: owns ad-hoc topic research when docs/wiki and any upstream wiki do not already answer the request; it saves a sourced synthesis report under raw for later ingest instead of editing docs/wiki directly.",
]

REQUIRED_SKILL_PHRASES = [
    "Present a setup recommendation pack before asking setup questions.",
    "recommended wiki-related skills, workflows, and automations",
    "recommended public update feed topics",
    "topic roots that fit the repository purpose",
    "## Federated Wikis",
    "one-way reference",
    "search upstream topic indexes before creating local entity leaves",
    "downstream-owned lens",
    "operational folders",
    "raw/processed",
    "Clippings",
    "scripts",
    "synonyms",
    "conflicting ideas",
    "factor common ideas",
    "source-specific ideas",
    "A digest entry may keep the date when the information was added or modified, but the text must summarize the content change rather than list page or file changes.",
    "Use one digest entry per independently changing item or closely coupled product family; do not bundle unrelated items into one dated paragraph.",
    "Monthly digest Current Understanding entries must appear in reverse chronological order by entry date, newest first; keep same-date entries in stable content order unless a clearer local grouping is needed.",
    *DIGEST_REPAIR_PHRASES,
    *RAW_INGEST_AUTOMATION_PHRASES,
    *LEAF_LINKING_PHRASES,
    *OKF_GUIDANCE_PHRASES,
    *AGENTS_GUIDANCE_PHRASES,
    *COMMIT_GUIDANCE_PHRASES,
    *ON_DEMAND_RESEARCH_PHRASES,
]

REQUIRED_OPERATIONS_PHRASES = [
    "Start with a setup recommendation pack",
    "Useful wiki-related workflow candidates",
    "Useful public update feed topic candidates",
    "AI-assisted development wiki",
    "federated wiki recommendation",
    "upstream wiki root",
    "Do not schedule duplicate public feeds",
    "Operational folder candidates",
    "raw/processed",
    "Clippings",
    "scripts",
    "synonyms",
    "conflicting ideas",
    "factor common ideas",
    "source-specific ideas",
    "A digest entry may keep the date when the information was added or modified, but the text must summarize the content change rather than list page or file changes.",
    "Use one digest entry per independently changing item or closely coupled product family; do not bundle unrelated items into one dated paragraph.",
    "Keep monthly digest Current Understanding entries in reverse chronological order by entry date, newest first.",
    *DIGEST_REPAIR_PHRASES,
    *RAW_INGEST_AUTOMATION_PHRASES,
    *LEAF_LINKING_PHRASES,
    *OKF_GUIDANCE_PHRASES[2:],
    *AGENTS_GUIDANCE_PHRASES,
    *COMMIT_GUIDANCE_PHRASES,
    *ON_DEMAND_RESEARCH_PHRASES,
]


class SetupGuidanceTest(unittest.TestCase):
    def test_backlog_sources_use_the_repository_root_backlog_directory(self) -> None:
        constants_text = CONSTANTS_IMPLEMENTATION.read_text(encoding="utf-8")
        core_text = CORE_IMPLEMENTATION.read_text(encoding="utf-8")

        self.assertIn('(\"backlog/defect-backlog/\", \"docs/wiki/known-defects.md\")', constants_text)
        self.assertIn('(\"backlog/feature-backlog/\", \"docs/wiki/topic-index.md\")', constants_text)
        self.assertIn('\"backlog/\",', constants_text)
        self.assertIn("backlog/defect-backlog holds tracked defects", core_text)
        self.assertIn("backlog/feature-backlog holds tracked feature requests", core_text)
        self.assertNotIn("docs/feature-backlog", constants_text + core_text)

    def test_skill_setup_guidance_requires_concrete_recommendations(self) -> None:
        skill_text = SKILL_DOCUMENT.read_text(encoding="utf-8")

        for phrase in REQUIRED_SKILL_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill_text)

    def test_operations_reference_lists_useful_candidates(self) -> None:
        operations_text = OPERATIONS_REFERENCE.read_text(encoding="utf-8")

        for phrase in REQUIRED_OPERATIONS_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, operations_text)

    def test_shared_digest_repair_guidance_is_available(self) -> None:
        reference_paths = [
            PAGE_SCHEMA_REFERENCE,
            VERIFICATION_CHECKLIST,
            CORE_IMPLEMENTATION,
            TOPIC_WRITER_SKILL,
            TOPIC_VERIFIER_SKILL,
        ]

        for reference_path in reference_paths:
            reference_text = reference_path.read_text(encoding="utf-8")
            for phrase in DIGEST_REPAIR_PHRASES:
                with self.subTest(path=reference_path.name, phrase=phrase):
                    self.assertIn(phrase, reference_text)

    def test_raw_ingest_automation_guidance_is_available(self) -> None:
        reference_paths = [
            PAGE_SCHEMA_REFERENCE,
            VERIFICATION_CHECKLIST,
            CORE_IMPLEMENTATION,
        ]

        for reference_path in reference_paths:
            reference_text = reference_path.read_text(encoding="utf-8")
            for phrase in RAW_INGEST_AUTOMATION_PHRASES:
                with self.subTest(path=reference_path.name, phrase=phrase):
                    self.assertIn(phrase, reference_text)

    def test_shared_leaf_linking_guidance_is_available(self) -> None:
        reference_paths = [
            PAGE_SCHEMA_REFERENCE,
            VERIFICATION_CHECKLIST,
            TOPIC_WRITER_SKILL,
            TOPIC_VERIFIER_SKILL,
        ]

        for reference_path in reference_paths:
            reference_text = reference_path.read_text(encoding="utf-8")
            for phrase in LEAF_LINKING_PHRASES:
                with self.subTest(path=reference_path.name, phrase=phrase):
                    self.assertIn(phrase, reference_text)

    def test_okf_guidance_is_available(self) -> None:
        reference_paths = [
            PAGE_SCHEMA_REFERENCE,
            VERIFICATION_CHECKLIST,
            TOPIC_WRITER_SKILL,
            TOPIC_VERIFIER_SKILL,
        ]

        for reference_path in reference_paths:
            reference_text = reference_path.read_text(encoding="utf-8")
            for phrase in OKF_GUIDANCE_PHRASES[1:]:
                with self.subTest(path=reference_path.name, phrase=phrase):
                    self.assertIn(phrase, reference_text)


if __name__ == "__main__":
    unittest.main()
