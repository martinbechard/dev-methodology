# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies optional document provenance project config validation and root-only rendering.

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

DOCUMENT_PROVENANCE_CONDITION = (
    "when an Agent creates, generates, migrates, or accepts a maintained document "
    "governed by the project document_provenance configuration"
)
COPYRIGHT = "Copyright (c) 2026 Martin.Bechard@DevConsult.ca"


def _project(*, provenance: object | None = None, include_route: bool = True) -> dict[str, object]:
    """Return one minimal renderable project with optional provenance configuration."""

    project: dict[str, object] = {
        "resource_coordination": {"selected": "none"},
        "workflow_selection": {
            "persistence": {"default": "UNSET"},
            "commit": {"default": "UNSET"},
        },
        "role_agent_set": [],
    }
    if include_route:
        project["shared_agent_skills"] = [
            {
                "skill": "document-provenance",
                "condition": DOCUMENT_PROVENANCE_CONDITION,
            }
        ]
    if provenance is not None:
        project["document_provenance"] = provenance
    return project


def _enabled_configuration() -> dict[str, object]:
    """Return one valid enabled provenance configuration."""

    return {
        "enabled": True,
        "copyright": COPYRIGHT,
        "governed_paths": ["README.md", "docs/**/*.md", "design/**/*.html"],
        "excluded_paths": ["raw/**", "design/generated/**"],
    }


class ProjectDocumentProvenanceTests(unittest.TestCase):
    """Verify project-owned provenance validation and root guidance generation."""

    def test_enabled_configuration_renders_root_only_guidance(self) -> None:
        """Render the complete governance boundary only in root project guidance."""

        project = _project(provenance=_enabled_configuration())

        root = RENDERER.render(project)
        nested = RENDERER.render(project, include_project_skill_extensions=False)

        self.assertIn(RENDERER.DOCUMENT_PROVENANCE_HEADING, root)
        self.assertIn(DOCUMENT_PROVENANCE_CONDITION, root)
        self.assertIn(COPYRIGHT, root)
        self.assertIn("- README.md", root)
        self.assertIn("- docs/**/*.md", root)
        self.assertIn("- raw/**", root)
        self.assertIn("Markdown front matter remains the first construct", root)
        self.assertIn("HTML doctype remains the first construct", root)
        self.assertIn("runtime-supplied", root)
        self.assertIn("generator or owning source", root)
        self.assertIn("project-authorized sidecar or manifest", root)
        self.assertNotIn(RENDERER.DOCUMENT_PROVENANCE_HEADING, nested)

    def test_absent_or_disabled_configuration_renders_nothing(self) -> None:
        """Omit provenance guidance when both route and configuration are inactive."""

        absent = _project(include_route=False)
        disabled = _project(provenance={"enabled": False}, include_route=False)

        self.assertNotIn(RENDERER.DOCUMENT_PROVENANCE_HEADING, RENDERER.render(absent))
        self.assertNotIn(RENDERER.DOCUMENT_PROVENANCE_HEADING, RENDERER.render(disabled))

    def test_enabled_configuration_rejects_malformed_or_ambiguous_values(self) -> None:
        """Reject unsafe enabled values instead of guessing the governance boundary."""

        valid = _enabled_configuration()
        invalid_cases = (
            ("enabled must be a boolean", {**valid, "enabled": "true"}),
            ("keys must be exactly", {"enabled": False, "copyright": COPYRIGHT}),
            ("keys must be exactly", {"enabled": True}),
            ("must be exact non-placeholder", {**valid, "copyright": "TODO"}),
            ("must be exact non-placeholder", {**valid, "copyright": "Copyright 2026"}),
            ("governed_paths must be a non-empty list", {**valid, "governed_paths": []}),
            ("excluded_paths must be a non-empty list", {**valid, "excluded_paths": "raw/**"}),
            (
                "governed_paths\[1\].*duplicates governed_paths\[0\]",
                {**valid, "governed_paths": ["README.md", "README.md"]},
            ),
            (
                "normalized project-relative path pattern",
                {**valid, "governed_paths": ["./README.md"]},
            ),
            (
                "normalized project-relative path pattern",
                {**valid, "governed_paths": ["/README.md"]},
            ),
            (
                "supported maintained-document format",
                {**valid, "governed_paths": ["docs/**"]},
            ),
            (
                "exact non-placeholder path pattern",
                {**valid, "governed_paths": ["TODO.md"]},
            ),
            (
                "also appears in governed_paths",
                {**valid, "excluded_paths": ["README.md"]},
            ),
        )

        for message, configuration in invalid_cases:
            with self.subTest(message=message, configuration=configuration):
                with self.assertRaisesRegex(ValueError, message):
                    RENDERER.render(_project(provenance=configuration))

    def test_route_and_enabled_configuration_must_be_aligned(self) -> None:
        """Reject an enabled gate without routing and routing without an enabled gate."""

        with self.assertRaisesRegex(ValueError, "requires shared_agent_skills"):
            RENDERER.render(
                _project(provenance=_enabled_configuration(), include_route=False)
            )
        with self.assertRaisesRegex(ValueError, "requires document_provenance.enabled true"):
            RENDERER.render(_project())
        with self.assertRaisesRegex(ValueError, "requires document_provenance.enabled true"):
            RENDERER.render(_project(provenance={"enabled": False}))
        placeholder_route = _project(provenance=_enabled_configuration())
        placeholder_route["shared_agent_skills"][0]["condition"] = "TODO"
        with self.assertRaisesRegex(ValueError, "condition must be exact non-placeholder"):
            RENDERER.render(placeholder_route)

    def test_current_project_declares_exact_centralized_governance(self) -> None:
        """Keep current configuration, shared routing, and generated guidance synchronized."""

        project = RENDERER.load_yaml(REPOSITORY_ROOT / "PROJECT.yaml")
        configuration = project["document_provenance"]
        shared_skills = dict(RENDERER._shared_agent_skills(project))
        guidance = (REPOSITORY_ROOT / "AGENTS.md").read_text(encoding="utf-8")

        self.assertEqual(True, configuration["enabled"])
        self.assertEqual(COPYRIGHT, configuration["copyright"])
        self.assertIn("README.md", configuration["governed_paths"])
        self.assertIn("design/**/*.html", configuration["governed_paths"])
        self.assertIn("skills/*/SKILL.md", configuration["governed_paths"])
        self.assertIn("backlog/**", configuration["excluded_paths"])
        self.assertIn("raw/**", configuration["excluded_paths"])
        self.assertIn("**/*.yaml", configuration["excluded_paths"])
        self.assertIn("design/generated/**", configuration["excluded_paths"])
        self.assertEqual(
            DOCUMENT_PROVENANCE_CONDITION,
            shared_skills["document-provenance"],
        )
        self.assertEqual(1, guidance.count(RENDERER.DOCUMENT_PROVENANCE_HEADING))
        self.assertEqual(1, guidance.count(COPYRIGHT))


if __name__ == "__main__":
    unittest.main()
