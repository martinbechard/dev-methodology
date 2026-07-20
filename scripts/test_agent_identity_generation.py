#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies generated native agent instructions state the conceptual role identity.

from __future__ import annotations

import importlib.util
import sys
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "scripts" / "build-skill-docs.py"


def _load_build_skill_docs():
    """Load the generator so tests exercise the native rendering boundary."""

    specification = importlib.util.spec_from_file_location(
        "build_skill_docs_agent_identity",
        BUILD_SCRIPT,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"Unable to load {BUILD_SCRIPT}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def _markdown_instruction_body(rendered: str) -> str:
    """Return the instruction body after one generated agent frontmatter block."""

    parts = rendered.split("---", 2)
    if len(parts) != 3:
        raise AssertionError("Generated Markdown agent is missing frontmatter")
    body = parts[2].lstrip()
    if body.startswith("<!--"):
        _, separator, body = body.partition("-->")
        if not separator:
            raise AssertionError("Generated Markdown agent has an unterminated comment")
    return body.lstrip()


class GeneratedAgentIdentityTests(unittest.TestCase):
    """Require every native agent to know its generated conceptual role name."""

    def assert_identity_boundary(self, body: str, expected: str) -> None:
        """Require one exact identity statement at the instruction boundary."""

        self.assertTrue(body.startswith(f"{expected}\n\n"), body[:200])
        self.assertEqual(1, body.count(expected), body[:500])

    def test_all_native_instructions_open_with_role_identity(self) -> None:
        """Generate the display name into every supported native instruction body."""

        build_skill_docs = _load_build_skill_docs()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        profile_ids = set(build_skill_docs.load_model_profiles())
        profiles = {
            adapter: build_skill_docs.load_adapter_model_profiles(adapter, profile_ids)
            for adapter in ("codex", "claude", "gemini", "junie")
        }

        for role in roles:
            expected = f"You are the {role.display_name}."
            for inline_core_skills in (True, False):
                with self.subTest(
                    role=role.name,
                    adapter="codex",
                    inline_core_skills=inline_core_skills,
                ):
                    codex = tomllib.loads(
                        build_skill_docs.render_codex_agent(
                            role,
                            profiles["codex"],
                            inline_core_skills=inline_core_skills,
                        )
                    )
                    self.assert_identity_boundary(
                        codex["developer_instructions"], expected
                    )
                for adapter, renderer in (
                    ("claude", build_skill_docs.render_claude_agent),
                    ("gemini", build_skill_docs.render_gemini_agent),
                    ("junie", build_skill_docs.render_junie_agent),
                ):
                    with self.subTest(
                        role=role.name,
                        adapter=adapter,
                        inline_core_skills=inline_core_skills,
                    ):
                        body = _markdown_instruction_body(
                            renderer(
                                role,
                                profiles[adapter],
                                inline_core_skills=inline_core_skills,
                            )
                        )
                        self.assert_identity_boundary(body, expected)

    def test_parent_coordinator_source_names_its_role(self) -> None:
        """Keep the immediate one-off parent identity explicit in conceptual source."""

        build_skill_docs = _load_build_skill_docs()
        skill_payload = build_skill_docs.build_payload()
        role = next(
            role
            for role in build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
            if role.name == "dev-backlog-coordinator"
        )

        self.assertIn("Dev Backlog Coordinator", role.instructions)


if __name__ == "__main__":
    unittest.main()
