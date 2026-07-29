# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies that Tailwind guidance remains self-contained across supported application routes.

from __future__ import annotations

import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TAILWIND_SKILL_PATH = REPOSITORY_ROOT / "skills" / "tailwind-design-system" / "SKILL.md"
EXPECTED_AGENT_ROUTES = (
    "- Load with Dev Coder for component styling, layout, responsive states, tokens, themes, and visual variants.",
    "- Load with Dev UX Specialist when the work needs independent usability or visual review.",
)
EXPECTED_STANDALONE_GUIDANCE = (
    "Use existing tokens, spacing, typography, and component patterns before adding new ones.",
    "Keep repeated visual decisions in shared components or variants.",
    "Verify responsive behavior for dense operational screens and mobile views.",
    "Preserve visible focus, disabled, loading, empty, and error states.",
    "Run component or E2E tests for changed workflows when available.",
    "Inspect affected breakpoints and interaction states.",
    "Run build after Tailwind config, class generation, or component import changes.",
)
FORBIDDEN_COMPANION_ROUTES = (
    "React Server Components",
    "React Vite Renderer",
    "Next.js App Router",
    "Jest",
    "Playwright",
)


class TailwindDesignSystemContractTests(unittest.TestCase):
    def test_guidance_is_self_contained_for_vite_and_nextjs(self) -> None:
        skill_text = TAILWIND_SKILL_PATH.read_text(encoding="utf-8")

        for application_route in ("Vite", "Next.js"):
            with self.subTest(application_route=application_route):
                for guidance in EXPECTED_STANDALONE_GUIDANCE:
                    self.assertIn(guidance, skill_text)

    def test_guidance_does_not_route_other_skills(self) -> None:
        skill_text = TAILWIND_SKILL_PATH.read_text(encoding="utf-8")
        routing_section = skill_text.split("## Routing", maxsplit=1)[1].split(
            "## Guidance",
            maxsplit=1,
        )[0]
        routing_lines = tuple(
            line for line in routing_section.splitlines() if line.startswith("- ")
        )

        self.assertEqual(EXPECTED_AGENT_ROUTES, routing_lines)
        self.assertNotIn("companion skill", skill_text.lower())
        for companion_route in FORBIDDEN_COMPANION_ROUTES:
            with self.subTest(companion_route=companion_route):
                self.assertNotIn(companion_route, skill_text)


if __name__ == "__main__":
    unittest.main()
