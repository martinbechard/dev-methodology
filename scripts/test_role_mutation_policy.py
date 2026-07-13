#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies canonical role mutation policy and keeps generic claim procedure out of project configuration.

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "scripts" / "build-skill-docs.py"
ROLE_SCHEMA = ROOT / "agents" / "role-schema.yaml"
PROJECT_TEMPLATE = ROOT / "skills" / "development-methodology" / "assets" / "templates" / "project-template.yaml"
PROJECT_CONFIGURATION_SKILL = ROOT / "skills" / "create-project-configuration" / "SKILL.md"


def _load_build_skill_docs():
    """Load the documentation generator so tests exercise its canonical role validation."""
    specification = importlib.util.spec_from_file_location("build_skill_docs_mutation_policy", BUILD_SCRIPT)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"Unable to load {BUILD_SCRIPT}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


class RoleMutationPolicyTests(unittest.TestCase):
    """Protect the role-owned repository mutation contract and project-file boundary."""

    def test_every_role_declares_consistent_repository_mutation_policy(self) -> None:
        """Require fixed, conditional, or absent claim loading according to each role declaration."""
        build_skill_docs = _load_build_skill_docs()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))

        self.assertEqual(26, len(roles))
        self.assertEqual(
            {"required", "conditional", "never"},
            {role.repository_mutation for role in roles},
        )
        for role in roles:
            with self.subTest(role=role.name, policy=role.repository_mutation):
                fixed_claim = "agent-claim" in build_skill_docs.fixed_role_skills(role)
                conditional_claim = "agent-claim" in role.skill_conditions
                if role.repository_mutation == "required":
                    self.assertTrue(fixed_claim)
                    self.assertFalse(conditional_claim)
                elif role.repository_mutation == "conditional":
                    self.assertFalse(fixed_claim)
                    self.assertTrue(conditional_claim)
                else:
                    self.assertFalse(fixed_claim)
                    self.assertFalse(conditional_claim)

    def test_evidence_writing_reviewers_claim_conditionally(self) -> None:
        """Ensure reviewer roles acquire ownership only when their evidence becomes a repository artifact."""
        build_skill_docs = _load_build_skill_docs()
        skill_payload = build_skill_docs.build_payload()
        roles = {
            role.name: role
            for role in build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        }
        reviewers = {
            "dev-artifact-reviewer",
            "dev-code-reviewer",
            "dev-prompt-reviewer",
            "dev-security-reviewer",
            "methodology-artifact-reviewer",
            "wiki-artifact-reviewer",
        }

        for role_name in reviewers:
            with self.subTest(role=role_name):
                role = roles[role_name]
                self.assertEqual("conditional", role.repository_mutation)
                self.assertIn("agent-claim", role.skill_conditions)
                self.assertIn("when the requested review creates or updates", role.skill_conditions["agent-claim"])

    def test_read_only_roles_cannot_load_agent_claim(self) -> None:
        """Keep query response and topic verification read-only without unnecessary writer claims."""
        build_skill_docs = _load_build_skill_docs()
        skill_payload = build_skill_docs.build_payload()
        roles = {
            role.name: role
            for role in build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        }

        self.assertEqual("never", roles["wiki-query-responder"].repository_mutation)
        self.assertEqual("never", roles["wiki-topic-verifier"].repository_mutation)
        self.assertNotIn("agent-claim", roles["wiki-query-responder"].skills)
        self.assertNotIn("agent-claim", roles["wiki-topic-verifier"].skills)

    def test_project_configuration_omits_generic_claim_procedure(self) -> None:
        """Keep universal claim policy in shared roles and skills rather than copied project artifacts."""
        template_text = PROJECT_TEMPLATE.read_text(encoding="utf-8")
        skill_text = PROJECT_CONFIGURATION_SKILL.read_text(encoding="utf-8")

        self.assertNotIn("agent_coordination:", template_text)
        self.assertNotIn("claim_skill:", template_text)
        self.assertNotIn("dirty_unclaimed_policy:", template_text)
        self.assertIn("Generic repository-mutation behavior belongs to canonical role definitions", skill_text)
        self.assertIn("Do not reproduce that procedure in PROJECT.yaml or AGENTS.md", skill_text)

    def test_role_schema_requires_repository_mutation(self) -> None:
        """Expose repository mutation as a required canonical role capability declaration."""
        schema = yaml.safe_load(ROLE_SCHEMA.read_text(encoding="utf-8"))

        self.assertEqual(3, schema["version"])
        self.assertIn("repositoryMutation", schema["required"])
        self.assertEqual("mutation-policy", schema["properties"]["repositoryMutation"])

    def test_generator_rejects_claim_policy_mismatch(self) -> None:
        """Fail generation when a role declaration contradicts its agent-claim loadout."""
        build_skill_docs = _load_build_skill_docs()
        required, allowed, groups = build_skill_docs.load_role_schema()
        skill_names = set(build_skill_docs.build_payload()["skills"])
        model_profiles = set(build_skill_docs.load_model_profiles())
        source = ROOT / "agents" / "roles" / "dev-activities" / "dev-coder.role.yaml"
        role = yaml.safe_load(source.read_text(encoding="utf-8"))
        role["repositoryMutation"] = "never"

        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "dev-activities" / "dev-coder.role.yaml"
            target.parent.mkdir()
            target.write_text(yaml.safe_dump(role, sort_keys=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Read-only role must not load agent-claim"):
                build_skill_docs.load_role_definition(
                    target,
                    required,
                    allowed,
                    groups,
                    skill_names,
                    model_profiles,
                )


if __name__ == "__main__":
    unittest.main()
