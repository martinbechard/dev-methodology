# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies the source-backed cross-harness skill lifecycle documentation contract.
# Governing design: design/skills-modularization.html

from __future__ import annotations

import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MODULARIZATION_PATH = REPOSITORY_ROOT / "design" / "skills-modularization.html"
AGENTIC_CONFIGURATION_PATH = REPOSITORY_ROOT / "design" / "agentic-configuration.html"
SOURCE_MODEL_PATH = REPOSITORY_ROOT / "design" / "generic-agent-definitions-source.html"


class SkillLifecycleDocumentationTests(unittest.TestCase):
    """Keep lifecycle terminology, runtime sources, and evidence boundaries aligned."""

    def test_authoritative_page_defines_each_lifecycle_state(self) -> None:
        """The owner page should distinguish availability, delivery, use, and proof."""

        text = MODULARIZATION_PATH.read_text(encoding="utf-8")

        for phrase in (
            "Skill Lifecycle and Runtime Delivery",
            "Available",
            "Preloaded",
            "Dynamically invoked",
            "Content read",
            "Behaviorally applied",
            "Verified",
            "Catalog presence is availability, not preloading or activation proof.",
            "An outcome-less completed call is not semantic evidence.",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_runtime_mechanisms_link_to_primary_sources(self) -> None:
        """Claude and Codex mechanism claims should retain direct runtime sources."""

        text = MODULARIZATION_PATH.read_text(encoding="utf-8")

        for target in (
            "https://code.claude.com/docs/en/sub-agents#preload-skills-into-subagents",
            "https://code.claude.com/docs/en/slash-commands#restrict-claudes-skill-access",
            "https://developers.openai.com/codex/skills#how-codex-uses-skills",
            "https://developers.openai.com/codex/config-reference#skillsconfig",
            "https://developers.openai.com/codex/app-server#skills",
        ):
            with self.subTest(target=target):
                self.assertIn(f'href="{target}"', text)

        self.assertIn(
            "A restrictive subagent <code>tools</code> allowlist that omits <code>Skill</code>",
            text,
        )
        self.assertIn(
            "Enables or disables a catalog entry by name or absolute path.",
            text,
        )
        self.assertIn(
            "the server injects the full skill instructions",
            text,
        )

    def test_bundle_categories_and_evidence_boundaries_remain_explicit(self) -> None:
        """Bundle policy should cover every selection category and proof boundary."""

        text = MODULARIZATION_PATH.read_text(encoding="utf-8")

        for phrase in (
            "Definition-owned core skill",
            "Request-specific core or tool skill",
            "Detected-folder technology skill",
            "Unsupported technology",
            "<code>NO_VARIANT</code>",
            "Agents do not invent a skill",
            "Bundle-content tests",
            "accepted Codex agent-suite report",
            "does not verify per-skill content read or activation",
            "Schema support, staged skill packages, generated text",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_summary_pages_link_to_the_owner_without_obsolete_routing_language(self) -> None:
        """Sibling pages should summarize the lifecycle without restoring stale routing claims."""

        pages = {
            "owner": MODULARIZATION_PATH.read_text(encoding="utf-8"),
            "agentic configuration": AGENTIC_CONFIGURATION_PATH.read_text(encoding="utf-8"),
            "source model": SOURCE_MODEL_PATH.read_text(encoding="utf-8"),
        }

        for page, text in pages.items():
            with self.subTest(page=page):
                self.assertNotIn("router to load skills", text)
                self.assertNotIn("dynamic task-time routing", text)
                self.assertNotIn("load just the skills it needs", text)
                self.assertNotIn("loads on demand when a task matches", text)

        for page in ("agentic configuration", "source model"):
            with self.subTest(owner_link=page):
                self.assertIn(
                    "skills-modularization.html#skill-lifecycle-title",
                    pages[page],
                )

        owner = pages["owner"]
        self.assertNotIn("An optional entry loads dynamically", owner)
        self.assertNotIn("Optional skills through the MCP server", owner)
        self.assertNotIn("Request-specific optional skills remain dynamic", owner)
        self.assertIn(
            "The harness-specific lifecycle above determines how selected content reaches context.",
            owner,
        )
        self.assertIn(
            "This conditional <a href=\"../README.md#preferred-mcp-operations-layer\">MCP path</a> is a bundle procedure rather than a universal harness mechanism.",
            owner,
        )

        self.assertIn(
            "Dynamic load-by-name guidance appears only when technology inlining is explicitly disabled.",
            pages["agentic configuration"],
        )
        self.assertIn(
            "deliver their instructions through the applicable Agent harness lifecycle",
            pages["agentic configuration"],
        )
        self.assertIn(
            "Enablement is not preloading or behavioral evidence.",
            pages["source model"],
        )


if __name__ == "__main__":
    unittest.main()
