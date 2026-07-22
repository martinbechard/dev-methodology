#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies mutation policy plus selectable resource coordination in project configuration.

from __future__ import annotations

import importlib.util
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml


ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "scripts" / "build-skill-docs.py"
ROLE_SCHEMA = ROOT / "agents" / "role-schema.yaml"
PROJECT_TEMPLATE = ROOT / "skills" / "development-methodology" / "assets" / "templates" / "project-template.yaml"
PROJECT_CONFIGURATION_SKILL = ROOT / "skills" / "create-project-configuration" / "SKILL.md"
FEATURE_BRANCH_SKILL = ROOT / "skills" / "complete-work-item-feature-branch" / "SKILL.md"
DIRECT_MAIN_SKILL = ROOT / "skills" / "complete-work-item-direct-main" / "SKILL.md"
WORK_MERGE_SKILL = ROOT / "skills" / "agent-work-merge" / "SKILL.md"
EXECUTE_WORKITEM_SKILL = ROOT / "skills" / "execute-workitem" / "SKILL.md"
SIMPLE_WORKITEM_PROCESS = ROOT / "skills" / "execute-workitem" / "references" / "simple-workitem.md"
FEATURE_WORKITEM_PROCESS = ROOT / "skills" / "execute-workitem" / "references" / "feature-branch-workitem.md"
README = ROOT / "README.md"
ORCHESTRATED_LIFECYCLE = ROOT / "design" / "orchestrated-development-lifecycle.html"
OPERATIONAL_CLAIM_PHRASES = (
    re.compile(r"\bclaim (?:a|the|transition|wait|attempt|owner|evidence|release)\b", re.IGNORECASE),
    re.compile(r"\bclaimed (?:file|files|resource|resources|worktree|worktrees)\b", re.IGNORECASE),
    re.compile(r"\bactive claims\b", re.IGNORECASE),
    re.compile(r"\breleased?(?:-| )(?:claim|claims)\b", re.IGNORECASE),
    re.compile(r"\breleased? the [a-z-]+ claim\b", re.IGNORECASE),
    re.compile(r"\bclaim pressure\b", re.IGNORECASE),
    re.compile(r"\brelease events\b", re.IGNORECASE),
    re.compile(r"\brelease\s+receipt\b", re.IGNORECASE),
    re.compile(r"\bclaimed\s+the\s+integration\s+resources\b", re.IGNORECASE),
)


def _load_build_skill_docs():
    """Load the documentation generator so tests exercise conceptual definition validation."""
    specification = importlib.util.spec_from_file_location("build_skill_docs_mutation_policy", BUILD_SCRIPT)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"Unable to load {BUILD_SCRIPT}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


class RoleMutationPolicyTests(unittest.TestCase):
    """Protect the conceptual definition mutation contract and project-file boundary."""

    def test_repository_mutation_does_not_load_resource_coordination(self) -> None:
        """Keep mutation capability independent from the project-selected coordination skill."""
        build_skill_docs = _load_build_skill_docs()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))

        self.assertEqual(27, len(roles))
        self.assertEqual(
            {"required", "conditional", "never"},
            {role.repository_mutation for role in roles},
        )
        for role in roles:
            with self.subTest(role=role.name, policy=role.repository_mutation):
                self.assertNotIn("agent-claim", role.skills)
                self.assertNotIn("agent-claim", role.skill_conditions)

    def test_core_roles_do_not_require_unconditional_claim_lifecycle_evidence(self) -> None:
        """Keep canonical and generated runtime contracts neutral for coordination none."""

        role_paths = sorted((ROOT / "agents" / "roles").glob("**/*.role.yaml"))
        for role_path in role_paths:
            role = yaml.safe_load(role_path.read_text(encoding="utf-8"))
            contract = yaml.safe_dump(
                {
                    "instructions": role["instructions"],
                    "examples": role.get("examples", []),
                    "outputContract": role.get("outputContract", []),
                },
                sort_keys=False,
            )
            for pattern in OPERATIONAL_CLAIM_PHRASES:
                with self.subTest(role=role["name"], pattern=pattern.pattern):
                    self.assertIsNone(pattern.search(contract))

        runtime_paths = sorted(
            runtime_path
            for adapter in ("claude", "codex", "gemini", "junie")
            for runtime_path in (ROOT / "generated" / "adapters" / adapter / "agents").iterdir()
            if runtime_path.suffix in {".md", ".toml"}
        )
        self.assertEqual(
            {"claude", "codex", "gemini", "junie"},
            {runtime_path.parents[1].name for runtime_path in runtime_paths},
        )
        for runtime_path in runtime_paths:
            runtime_contract = runtime_path.read_text(encoding="utf-8")
            for pattern in OPERATIONAL_CLAIM_PHRASES:
                with self.subTest(runtime=runtime_path.name, pattern=pattern.pattern):
                    self.assertIsNone(pattern.search(runtime_contract))

    def test_workflow_skills_branch_on_the_selected_coordination_implementation(self) -> None:
        """Keep none free of skill application and operational ownership lifecycle steps."""

        feature_branch = FEATURE_BRANCH_SKILL.read_text(encoding="utf-8")
        direct_main = DIRECT_MAIN_SKILL.read_text(encoding="utf-8")
        work_merge = WORK_MERGE_SKILL.read_text(encoding="utf-8")

        self.assertNotIn(
            "Acquire the narrow repository ownership and shared resources required for the current mutation phase.",
            feature_branch,
        )
        self.assertNotIn(
            "Release ownership only after the phase is committed, verified, clean, and safely published or preserved.",
            feature_branch,
        )
        self.assertIn("When agent-claim is selected", feature_branch)
        self.assertIn("When none is selected", feature_branch)
        self.assertIn("without coordination operations or evidence", feature_branch)

        for skill_text in (direct_main, work_merge):
            with self.subTest(skill=skill_text.splitlines()[1]):
                self.assertNotIn(
                    "Apply the resource-coordination skill selected in PROJECT.yaml",
                    skill_text,
                )
                self.assertIn("When agent-claim is selected", skill_text)
                self.assertIn("When none is selected", skill_text)

    def test_execute_workitem_package_branches_coordination_without_a_none_bypass(self) -> None:
        """Keep clean delivery mandatory while none performs no coordination lifecycle."""

        package = EXECUTE_WORKITEM_SKILL.read_text(encoding="utf-8")
        simple_process = SIMPLE_WORKITEM_PROCESS.read_text(encoding="utf-8")
        feature_process = FEATURE_WORKITEM_PROCESS.read_text(encoding="utf-8")

        self.assertNotIn("Acquire ownership before repository mutation", package)
        self.assertNotIn("Acquire the narrow required claim", simple_process)
        self.assertNotIn("Acquire ownership before creating or switching branches", feature_process)
        for text in (package, simple_process, feature_process):
            with self.subTest(document=text.splitlines()[0]):
                self.assertIn("When agent-claim is selected", text)
                self.assertIn("When none is selected", text)
                self.assertIn("no coordination operations or evidence", text)
                self.assertIn("clean", text.lower())
                self.assertIn("commit", text.lower())

        for adapter in ("claude", "codex", "gemini", "junie"):
            adapter_root = ROOT / "generated" / "adapters" / adapter / "agents"
            matches = list(adapter_root.glob("dev-coder.*"))
            self.assertEqual(1, len(matches))
            runtime_contract = matches[0].read_text(encoding="utf-8")
            with self.subTest(adapter=adapter):
                self.assertIn(
                    "project-selected resource-coordination policy requires it",
                    runtime_contract,
                )
                self.assertIn("enabled resource-coordination", runtime_contract)
                self.assertIn("release of enabled resource ownership", runtime_contract)
                self.assertNotIn("When agent-claim is selected", runtime_contract)
                self.assertNotIn("Acquire ownership before repository mutation", runtime_contract)

    def test_role_and_adapter_output_contracts_use_general_closeout_fields(self) -> None:
        """Make delivery or commit closeout mandatory while coordination evidence stays conditional."""

        expected_output_names = {
            "dev-merge-coordinator": "commit and delivery closeout",
            "wiki-ingester": "ingest commit closeout",
            "wiki-writer": "delivery closeout",
        }
        role_paths = {
            path.stem.removesuffix(".role"): path
            for path in (ROOT / "agents" / "roles").glob("**/*.role.yaml")
        }
        for role_name, expected_output_name in expected_output_names.items():
            role = yaml.safe_load(role_paths[role_name].read_text(encoding="utf-8"))
            output_names = {next(iter(item)) for item in role["outputContract"]}
            with self.subTest(role=role_name):
                self.assertIn(expected_output_name, output_names)
                self.assertFalse(
                    any("coordination closeout" in output_name for output_name in output_names)
                )
                purpose = next(
                    item[expected_output_name]["purpose"]
                    for item in role["outputContract"]
                    if expected_output_name in item
                )
                self.assertIn("when resource coordination is enabled", purpose)

        for adapter in ("claude", "codex", "gemini", "junie"):
            adapter_root = ROOT / "generated" / "adapters" / adapter / "agents"
            for role_name, expected_output_name in expected_output_names.items():
                matches = list(adapter_root.glob(f"{role_name}.*"))
                self.assertEqual(1, len(matches))
                runtime_contract = matches[0].read_text(encoding="utf-8")
                with self.subTest(adapter=adapter, role=role_name):
                    self.assertIn(expected_output_name, runtime_contract)
                    self.assertNotIn("- coordination closeout:", runtime_contract)
                    self.assertNotIn("- commit and coordination closeout:", runtime_contract)

    def test_public_lifecycle_explains_registry_evidence_as_optional(self) -> None:
        """Describe claim release and registry evidence only for enabled agent-claim projects."""

        readme = README.read_text(encoding="utf-8")
        lifecycle = ORCHESTRATED_LIFECYCLE.read_text(encoding="utf-8")

        self.assertIn(
            "agent-claim adds claim-release gates; none adds no coordination operations or evidence",
            readme,
        )
        self.assertNotIn("integration, claim release, and execution evidence", readme)
        self.assertNotIn("commit, and claim-release gates", readme)
        self.assertIn(
            "When agent-claim is selected, the coordination registry",
            lifecycle,
        )
        self.assertIn("With none, registry evidence is absent.", lifecycle)
        self.assertIn("the coordination registry when enabled", lifecycle)

    def test_evidence_writing_reviewers_keep_conditional_mutation_capability(self) -> None:
        """Preserve reviewer mutation declarations without embedding one coordination implementation."""
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
                self.assertNotIn("agent-claim", role.skills)

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

    def test_project_configuration_selects_resource_coordination_independently(self) -> None:
        """Select coordination without copying its procedure or coupling it to mutation."""
        template_text = PROJECT_TEMPLATE.read_text(encoding="utf-8")
        skill_text = PROJECT_CONFIGURATION_SKILL.read_text(encoding="utf-8")

        self.assertNotIn("agent_coordination:", template_text)
        self.assertNotIn("claim_skill:", template_text)
        self.assertNotIn("dirty_unclaimed_policy:", template_text)
        self.assertIn("resource_coordination:", template_text)
        self.assertIn("repositoryMutation belongs to conceptual agent definitions as an independent capability declaration", skill_text)
        self.assertIn("has no folder overrides", skill_text)
        self.assertIn("For none, render no coordination skill, procedure, transport, or evidence", skill_text)
        self.assertIn("agent_claim_transport:", template_text)
        self.assertIn("Only when resource_coordination selects agent-claim", skill_text)
        self.assertIn(
            "Reserve agent-claim, agent-claim-mcp, and agent-claim-command",
            skill_text,
        )
        self.assertIn("generated AGENTS.md inlines only that adapter", skill_text)

    def test_role_schema_requires_repository_mutation(self) -> None:
        """Expose repository mutation as a required conceptual definition capability declaration."""
        schema = yaml.safe_load(ROLE_SCHEMA.read_text(encoding="utf-8"))

        self.assertEqual(4, schema["version"])
        self.assertIn("repositoryMutation", schema["required"])
        self.assertEqual("mutation-policy", schema["properties"]["repositoryMutation"])

    def test_generator_accepts_mutation_policy_without_agent_claim(self) -> None:
        """Load a mutating conceptual definition without coupling it to agent-claim."""
        build_skill_docs = _load_build_skill_docs()
        required, allowed, groups = build_skill_docs.load_role_schema()
        skill_names = set(build_skill_docs.build_payload()["skills"])
        model_profiles = set(build_skill_docs.load_model_profiles())
        source = ROOT / "agents" / "roles" / "dev-activities" / "dev-coder.role.yaml"
        role = yaml.safe_load(source.read_text(encoding="utf-8"))
        role["skills"] = [
            entry for entry in role["skills"] if next(iter(entry)) != "agent-claim"
        ]

        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "dev-activities" / "dev-coder.role.yaml"
            target.parent.mkdir()
            target.write_text(yaml.safe_dump(role, sort_keys=False), encoding="utf-8")
            with mock.patch.object(build_skill_docs, "REPOSITORY_ROOT", Path(directory)):
                loaded = build_skill_docs.load_role_definition(
                    target,
                    required,
                    allowed,
                    groups,
                    skill_names,
                    model_profiles,
                )

        self.assertEqual("required", loaded.repository_mutation)
        self.assertNotIn("agent-claim", loaded.skills)

    def test_generator_rejects_read_only_isolation_for_mutating_role(self) -> None:
        """Reserve read-only isolation for conceptual definitions that never mutate repositories."""
        build_skill_docs = _load_build_skill_docs()
        required, allowed, groups = build_skill_docs.load_role_schema()
        skill_names = set(build_skill_docs.build_payload()["skills"])
        model_profiles = set(build_skill_docs.load_model_profiles())
        source = ROOT / "agents" / "roles" / "dev-activities" / "dev-code-reviewer.role.yaml"
        role = yaml.safe_load(source.read_text(encoding="utf-8"))
        role["isolation"] = "read-only"

        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "dev-activities" / "dev-code-reviewer.role.yaml"
            target.parent.mkdir()
            target.write_text(yaml.safe_dump(role, sort_keys=False), encoding="utf-8")
            with mock.patch.object(build_skill_docs, "REPOSITORY_ROOT", Path(directory)):
                with self.assertRaisesRegex(
                    ValueError,
                    "read-only isolation must declare repositoryMutation never",
                ):
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
