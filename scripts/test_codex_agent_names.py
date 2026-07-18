#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies Codex adapter names satisfy the runtime identifier contract without changing portable role identities.

from __future__ import annotations

import importlib.util
import re
import sys
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "scripts" / "build-skill-docs.py"
CODEX_NAME_PATTERN = re.compile(r"^[a-z0-9_]+$")


def _load_build_skill_docs():
    """Load the generator so tests exercise its public rendering boundary."""

    specification = importlib.util.spec_from_file_location(
        "build_skill_docs_codex_agent_names",
        BUILD_SCRIPT,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"Unable to load {BUILD_SCRIPT}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


class CodexAgentNameTests(unittest.TestCase):
    """Protect the distinction between runtime-safe Codex names and portable role IDs."""

    def test_rendered_codex_names_are_runtime_safe(self) -> None:
        """Require every generated Codex name to contain only runtime-supported characters."""

        build_skill_docs = _load_build_skill_docs()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        profile_ids = set(build_skill_docs.load_model_profiles())
        profiles = build_skill_docs.load_adapter_model_profiles("codex", profile_ids)

        for role in roles:
            with self.subTest(role=role.name):
                payload = tomllib.loads(build_skill_docs.render_codex_agent(role, profiles))
                self.assertRegex(payload["name"], CODEX_NAME_PATTERN)

    def test_codex_name_normalization_preserves_portable_identity_and_filename(self) -> None:
        """Keep conceptual IDs and output paths unchanged while adapting the Codex name field."""

        build_skill_docs = _load_build_skill_docs()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        role = next(item for item in roles if item.name == "dev-coder")
        profile_ids = set(build_skill_docs.load_model_profiles())
        profiles = build_skill_docs.load_adapter_model_profiles("codex", profile_ids)

        payload = tomllib.loads(build_skill_docs.render_codex_agent(role, profiles))

        self.assertEqual("dev_coder", payload["name"])
        self.assertEqual("dev-coder", role.name)
        self.assertEqual("dev-coder", role.filename)
        self.assertEqual(
            "dev-coder.toml",
            f"{role.filename}{build_skill_docs.CODEX_AGENT_EXTENSION}",
        )

    def test_codex_runtime_invocations_use_runtime_safe_agent_names(self) -> None:
        """Require adapter-specific examples to invoke the declared Codex agent name."""

        build_skill_docs = _load_build_skill_docs()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))

        for role in roles:
            expected_prefix = f"${build_skill_docs.codex_agent_name(role.name)} "
            for index, example in enumerate(role.examples):
                with self.subTest(role=role.name, example=index):
                    self.assertTrue(
                        example["runtimeInvocations"]["codex"].startswith(expected_prefix),
                        example["runtimeInvocations"]["codex"],
                    )

    def test_generated_codex_instructions_use_runtime_safe_dependency_names(self) -> None:
        """Keep model-facing delegation selectors aligned with generated name fields."""

        build_skill_docs = _load_build_skill_docs()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        outputs = build_skill_docs.expected_role_outputs(roles)
        role_by_name = {role.name: role for role in roles}

        for role in roles:
            if not role.agent_dependencies:
                continue
            output_path = (
                build_skill_docs.CODEX_AGENT_OUTPUT_ROOT
                / f"{role.filename}{build_skill_docs.CODEX_AGENT_EXTENSION}"
            )
            payload = tomllib.loads(outputs[output_path])
            instructions = payload["developer_instructions"]
            for dependency in role.agent_dependencies:
                with self.subTest(role=role.name, dependency=dependency):
                    runtime_name = build_skill_docs.codex_agent_name(dependency)
                    self.assertIn(runtime_name, instructions)
                    self.assertIsNotNone(role_by_name.get(dependency))
                    self.assertIsNone(
                        re.search(
                            rf"(?<![a-z0-9_-]){re.escape(dependency)}(?![a-z0-9_-])",
                            instructions,
                        ),
                        instructions,
                    )


if __name__ == "__main__":
    unittest.main()
