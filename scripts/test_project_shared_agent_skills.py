# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies project-wide conditional Agent skill validation and rendering.

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RENDERER_PATH = REPOSITORY_ROOT / "scripts" / "render-agents-technology-skills.py"
SPEC = importlib.util.spec_from_file_location("render_agents_technology_skills", RENDERER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load renderer: {RENDERER_PATH}")
RENDERER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RENDERER)


class ProjectSharedAgentSkillsTests(unittest.TestCase):
    """Verify shared conditional skills remain project-owned and non-duplicated."""

    def test_shared_skill_is_rendered_once_with_its_condition(self) -> None:
        """Render one shared skill once while preserving its PROJECT.yaml condition."""

        project = {
            "shared_agent_skills": [
                {
                    "skill": "organise-project-files",
                    "condition": "when an Agent must choose or audit a project path",
                }
            ],
            "role_agent_set": [],
        }

        self.assertEqual(
            [
                "## Shared Agent Skills",
                "",
                "These project-wide references apply to every Agent. Load a listed skill only when its condition applies; the skill definitions remain in the bundled catalog and are not copied here.",
                "",
                "- organise-project-files: load when an Agent must choose or audit a project path.",
                "",
            ],
            RENDERER._shared_agent_skill_lines(project),
        )

    def test_shared_skill_cannot_repeat_a_role_owned_skill(self) -> None:
        """Reject a shared skill already owned by one selected conceptual Agent."""

        project = {
            "shared_agent_skills": [
                {
                    "skill": "organise-project-files",
                    "condition": "when an Agent creates a project file",
                }
            ],
            "role_agent_set": [{"skills": ["organise-project-files"]}],
        }

        with self.assertRaisesRegex(
            ValueError,
            r"shared_agent_skills\[0\]\.skill.*role_agent_set\[0\]\.skills\[0\]",
        ):
            RENDERER._shared_agent_skills(project)

    def test_extension_cannot_repeat_a_shared_agent_skill(self) -> None:
        """Reject a project extension that repeats a shared conditional Agent skill."""

        project = {
            "shared_agent_skills": [
                {
                    "skill": "organise-project-files",
                    "condition": "when an Agent creates a project file",
                }
            ],
            "project_skill_extensions": ["organise-project-files"],
            "role_agent_set": [],
        }

        with self.assertRaisesRegex(
            ValueError,
            r"project_skill_extensions\[0\].*shared_agent_skills\[0\]\.skill",
        ):
            RENDERER._project_skill_extensions(project)

    def test_shared_skill_requires_exact_fields_and_safe_condition(self) -> None:
        """Reject malformed shared entries and multiline text that would corrupt guidance."""

        invalid_projects = (
            (
                {"shared_agent_skills": "organise-project-files"},
                "shared_agent_skills must be a list",
            ),
            (
                {"shared_agent_skills": [{"skill": "organise-project-files"}]},
                r"shared_agent_skills\[0\] keys must be exactly: skill, condition",
            ),
            (
                {
                    "shared_agent_skills": [
                        {
                            "skill": "organise-project-files",
                            "condition": "when a path must be chosen\nwithout guidance",
                        }
                    ]
                },
                r"shared_agent_skills\[0\]\.condition must be non-empty single-line text",
            ),
        )

        for project, message in invalid_projects:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    RENDERER._shared_agent_skills(project)

    def test_shared_skill_rejects_duplicates_unknown_and_reserved_ids(self) -> None:
        """Reject ambiguous, unavailable, and resource-coordination skill selections."""

        condition = "when an Agent must choose a project path"
        invalid_projects = (
            (
                {
                    "shared_agent_skills": [
                        {"skill": "organise-project-files", "condition": condition},
                        {"skill": " Organise-Project-Files ", "condition": condition},
                    ]
                },
                r"shared_agent_skills\[1\]\.skill.*duplicates shared_agent_skills\[0\]\.skill",
            ),
            (
                {
                    "shared_agent_skills": [
                        {"skill": "not-a-bundled-skill", "condition": condition}
                    ]
                },
                "unknown bundled skill id",
            ),
            (
                {
                    "shared_agent_skills": [
                        {"skill": "resource-claim", "condition": condition}
                    ]
                },
                "reserved for resource_coordination",
            ),
        )

        for project, message in invalid_projects:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    RENDERER._shared_agent_skills(project)

    def test_root_sections_are_ordered_and_omitted_from_nested_guidance(self) -> None:
        """Place shared routing before extensions and omit both from nested output."""

        project = {
            "resource_coordination": {"selected": "none"},
            "workflow_selection": {
                "persistence": {"default": "UNSET"},
                "commit": {"default": "UNSET"},
            },
            "shared_agent_skills": [
                {
                    "skill": "organise-project-files",
                    "condition": "when an Agent must choose a project path",
                }
            ],
            "project_skill_extensions": ["python"],
            "role_agent_set": [],
        }

        root = RENDERER.render(project)
        nested = RENDERER.render(project, include_project_skill_extensions=False)

        self.assertLess(
            root.index(RENDERER.SHARED_AGENT_SKILLS_HEADING),
            root.index(RENDERER.PROJECT_SKILL_EXTENSIONS_HEADING),
        )
        self.assertNotIn(RENDERER.SHARED_AGENT_SKILLS_HEADING, nested)
        self.assertNotIn(RENDERER.PROJECT_SKILL_EXTENSIONS_HEADING, nested)


if __name__ == "__main__":
    unittest.main()
