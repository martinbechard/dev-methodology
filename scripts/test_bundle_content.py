from __future__ import annotations

import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
README_PATH = REPOSITORY_ROOT / "README.md"
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
CODEX_ADAPTER_SKILLS_ROOT = REPOSITORY_ROOT / "adapters" / "codex" / "skills"
REMOVED_ROOT_FILES = (
    "documentation-methodology.md",
    "procedure-reverse-engineer-project-documentation.md",
)
REMOVED_DEVELOPMENT_REFERENCES = (
    "documentation-methodology.md",
    "procedure-reverse-engineer-project-documentation.md",
)
NEW_WORKFLOW_SKILLS = (
    "documentation-bootstrap",
    "documentation-reverse-engineering",
    "code-project-wiki",
    "documentation-page-verifier",
)
ARTIFACT_REVIEW_SKILLS = (
    ("project-wiki-review", "project-wiki-review-checklist.md"),
    ("functional-spec-review", "functional-spec-review-checklist.md"),
    ("architecture-review", "architecture-review-checklist.md"),
    ("high-level-design-review", "high-level-design-review-checklist.md"),
    ("module-design-review", "module-design-review-checklist.md"),
)
EXAMPLE_PROJECT_SKILL_PACKS = (
    "api-routes",
    "clerk-auth",
    "electron-main",
    "electron-preload",
    "harness-implementation",
    "jest",
    "langgraph",
    "local-model-integration",
    "nextjs-app-router",
    "node-cli",
    "plan-engine-implementation",
    "playwright",
    "postgres-drizzle",
    "react-server-components",
    "react-vite-renderer",
    "tailwind-design-system",
    "tool-runtime-implementation",
    "typescript-esm",
    "typescript-strict",
    "vitest",
)
README_REQUIRED_PHRASES = (
    "Use the installed skills as the operating surface.",
    "documentation-bootstrap",
    "documentation-reverse-engineering",
    "code-project-wiki",
    "documentation-page-verifier",
    "project-wiki-review",
    "functional-spec-review",
    "architecture-review",
    "high-level-design-review",
    "module-design-review",
    "Junie CLI",
    "--adapter junie",
    "skills/development-methodology/assets/templates",
    "python3 scripts/validate-agent-skills.py skills",
)
README_FORBIDDEN_PHRASES = (
    "Copy documentation-methodology.md",
    "Copy the templates folder",
    "procedure-reverse-engineer-project-documentation.md before treating the wiki as complete",
    "okf-skill-validate skills/*",
)
REVERSE_ENGINEERING_DISCOVERY_PHRASES = (
    "## Code Discovery Tools",
    "Use ast-grep when discovery depends on syntax, nesting, imports, exports, callers, route declarations, component shapes, async flow, error handling, or test structure.",
    "Before using ast-grep, run ast-grep --version.",
    "If ast-grep is unavailable, continue with rg, grep, repository file walking, and direct source reading.",
    "Do not treat ast-grep matches as documentation evidence until the matched code has been read.",
)


class BundleContentTests(unittest.TestCase):
    def test_redundant_root_manuals_are_removed(self) -> None:
        for file_name in REMOVED_ROOT_FILES:
            with self.subTest(file_name=file_name):
                self.assertFalse((REPOSITORY_ROOT / file_name).exists())

    def test_root_templates_are_not_a_second_distribution_surface(self) -> None:
        self.assertFalse((REPOSITORY_ROOT / "templates").exists())

    def test_development_methodology_does_not_copy_monolithic_references(self) -> None:
        references_root = SKILLS_ROOT / "development-methodology" / "references"

        for file_name in REMOVED_DEVELOPMENT_REFERENCES:
            with self.subTest(file_name=file_name):
                self.assertFalse((references_root / file_name).exists())

    def test_workflow_skills_and_codex_metadata_are_packaged(self) -> None:
        for skill_name in NEW_WORKFLOW_SKILLS:
            with self.subTest(skill_name=skill_name):
                self.assertTrue((SKILLS_ROOT / skill_name / "SKILL.md").is_file())
                self.assertTrue(
                    (
                        CODEX_ADAPTER_SKILLS_ROOT
                        / skill_name
                        / "agents"
                        / "openai.yaml"
                    ).is_file()
                )

    def test_artifact_review_skills_have_checklists_and_metadata(self) -> None:
        development_methodology_text = (
            SKILLS_ROOT / "development-methodology" / "SKILL.md"
        ).read_text(encoding="utf-8")

        for skill_name, checklist_name in ARTIFACT_REVIEW_SKILLS:
            with self.subTest(skill_name=skill_name):
                skill_path = SKILLS_ROOT / skill_name / "SKILL.md"
                checklist_path = SKILLS_ROOT / skill_name / "references" / checklist_name
                metadata_path = (
                    CODEX_ADAPTER_SKILLS_ROOT
                    / skill_name
                    / "agents"
                    / "openai.yaml"
                )

                self.assertTrue(skill_path.is_file())
                self.assertTrue(checklist_path.is_file())
                self.assertTrue(metadata_path.is_file())

                skill_text = skill_path.read_text(encoding="utf-8")
                checklist_text = checklist_path.read_text(encoding="utf-8")

                self.assertIn(checklist_name, skill_text)
                self.assertIn("documentation-page-verifier", skill_text)
                self.assertIn("Review Checklist", checklist_text)
                self.assertIn("Findings", checklist_text)
                self.assertIn(skill_name, development_methodology_text)

    def test_example_project_skill_packs_are_packaged(self) -> None:
        for skill_name in EXAMPLE_PROJECT_SKILL_PACKS:
            with self.subTest(skill_name=skill_name):
                skill_path = SKILLS_ROOT / skill_name / "SKILL.md"
                source_metadata_path = SKILLS_ROOT / skill_name / "agents" / "openai.yaml"
                adapter_metadata_path = (
                    CODEX_ADAPTER_SKILLS_ROOT
                    / skill_name
                    / "agents"
                    / "openai.yaml"
                )

                self.assertTrue(skill_path.is_file())
                self.assertTrue(adapter_metadata_path.is_file())
                self.assertFalse(source_metadata_path.exists())

    def test_skill_frontmatter_uses_agent_skill_schema(self) -> None:
        for skill_path in sorted(SKILLS_ROOT.glob("*/SKILL.md")):
            with self.subTest(skill_path=skill_path):
                skill_text = skill_path.read_text(encoding="utf-8")
                frontmatter = skill_text.split("---", maxsplit=2)[1]

                self.assertIn("name:", frontmatter)
                self.assertIn("description:", frontmatter)
                self.assertNotIn("type: Skill", frontmatter)

    def test_readme_points_to_skill_based_setup(self) -> None:
        readme_text = README_PATH.read_text(encoding="utf-8")

        for phrase in README_REQUIRED_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, readme_text)

        for phrase in README_FORBIDDEN_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, readme_text)

    def test_reverse_engineering_uses_structural_code_discovery(self) -> None:
        skill_text = (
            SKILLS_ROOT / "documentation-reverse-engineering" / "SKILL.md"
        ).read_text(encoding="utf-8")

        for phrase in REVERSE_ENGINEERING_DISCOVERY_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill_text)


if __name__ == "__main__":
    unittest.main()
