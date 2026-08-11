#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies mutation policy, safe solo fallback, and selectable resource coordination.

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml


ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "scripts" / "build-skill-docs.py"
ROLE_SCHEMA = ROOT / "agents" / "role-schema.yaml"
PROJECT_TEMPLATE = ROOT / "skills" / "route-documentation-work" / "assets" / "templates" / "project-template.yaml"
PROJECT_CONFIGURATION_SKILL = ROOT / "skills" / "create-project-configuration" / "SKILL.md"
FEATURE_BRANCH_SKILL = ROOT / "skills" / "deliver-work-item-feature-branch" / "SKILL.md"
MAIN_BRANCH_SKILL = ROOT / "skills" / "deliver-work-item-main-branch" / "SKILL.md"
WORK_MERGE_SKILL = ROOT / "skills" / "integrate-agent-work" / "SKILL.md"
SOLO_MODE_SKILL = ROOT / "skills" / "set-solo-mode" / "SKILL.md"
MULTITASK_MODE_SKILL = ROOT / "skills" / "set-multitask-mode" / "SKILL.md"
RESOURCE_CLAIM_SKILL = ROOT / "skills" / "resource-claim" / "SKILL.md"
PROJECT_BOOTSTRAPPER_ROLE = (
    ROOT / "agents" / "roles" / "project-setup" / "project-bootstrapper.role.yaml"
)
EXECUTE_WORKITEM_PACKAGE = ROOT / "skills" / "execute-workitem"
README = ROOT / "README.md"
ORCHESTRATED_LIFECYCLE = ROOT / "design" / "orchestrated-development-lifecycle.html"
RETIRED_UNCONDITIONAL_CLAIM_PHRASES = (
    "Acquire ownership before repository mutation",
    "Acquire implementation ownership before branch creation or source mutation",
    "acquired the integration-resource ownership",
    "required enabled resource ownership is released",
    "six five-minute retries",
    "thirty-minute retry window",
)
HISTORICAL_SKILL_ARTIFACT_IDS = {
    SOLO_MODE_SKILL: "792d36e6-5b37-4351-aeee-709c24a49ea1",
    MULTITASK_MODE_SKILL: "e8edc1ee-3dd9-4a6e-9925-32185f02f513",
    RESOURCE_CLAIM_SKILL: "be32b4bc-43bb-437f-8941-40671f28c7bd",
}


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

    def test_backlog_steward_leaves_resource_coordination_to_project_guidance(self) -> None:
        """Keep provider lifecycle authority portable while project guidance owns coordination."""

        build_skill_docs = _load_build_skill_docs()
        roles = build_skill_docs.load_role_definitions(
            set(build_skill_docs.build_payload()["skills"])
        )
        steward = next(role for role in roles if role.name == "dev-backlog-steward")
        contract = yaml.safe_dump(
            {
                "instructions": steward.instruction_sections,
                "examples": steward.examples,
                "outputContract": steward.output_contract,
            },
            sort_keys=False,
        )

        self.assertNotIn("resource_coordination", contract)
        self.assertNotIn("resource-claim", contract)
        self.assertNotIn("claim", contract.lower())
        self.assertIn(
            "Use applicable project guidance or an explicit task override",
            contract,
        )

    def test_repository_mutation_does_not_load_resource_coordination(self) -> None:
        """Keep mutation capability independent from the project-selected coordination skill."""
        build_skill_docs = _load_build_skill_docs()
        skill_payload = build_skill_docs.build_payload()
        roles = build_skill_docs.load_role_definitions(set(skill_payload["skills"]))

        self.assertEqual(
            len(list((ROOT / "agents" / "roles").glob("**/*.role.yaml"))),
            len(roles),
        )
        self.assertEqual(
            {"required", "conditional", "never"},
            {role.repository_mutation for role in roles},
        )
        for role in roles:
            with self.subTest(role=role.name, policy=role.repository_mutation):
                self.assertNotIn("resource-claim", role.skills)
                self.assertNotIn("resource-claim", role.skill_conditions)

    def test_dev_architect_mutation_is_bounded_to_design_sources(self) -> None:
        """Allow committed design candidates without granting unrelated production ownership."""

        source = (
            ROOT
            / "agents"
            / "roles"
            / "dev-activities"
            / "dev-architect.role.yaml"
        )
        role = yaml.safe_load(source.read_text(encoding="utf-8"))
        contract = yaml.safe_dump(role["instructions"], sort_keys=False)

        self.assertEqual("required", role["repositoryMutation"])
        self.assertNotIn("resource-claim", {next(iter(entry)) for entry in role["skills"]})
        self.assertIn("Do not silently expand requirements", contract)
        self.assertIn("Do not apply terminal Commit delivery", contract)
        self.assertIn("unrelated production code", contract)

    def test_core_roles_do_not_require_unconditional_claim_lifecycle_evidence(self) -> None:
        """Keep broad mutation claims absent while allowing Event Contract branches."""

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
            for phrase in RETIRED_UNCONDITIONAL_CLAIM_PHRASES:
                with self.subTest(role=role["name"], phrase=phrase):
                    self.assertNotIn(phrase, contract)

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
            for phrase in RETIRED_UNCONDITIONAL_CLAIM_PHRASES:
                with self.subTest(runtime=runtime_path.name, phrase=phrase):
                    self.assertNotIn(phrase, runtime_contract)

    def test_workflow_skills_delegate_claim_rules_to_resource_claim(self) -> None:
        """Keep claim triggers, scope, and release timing in the owning skill."""

        feature_branch = FEATURE_BRANCH_SKILL.read_text(encoding="utf-8")
        main_branch = MAIN_BRANCH_SKILL.read_text(encoding="utf-8")
        work_merge = WORK_MERGE_SKILL.read_text(encoding="utf-8")

        self.assertNotIn(
            "Acquire the narrow repository ownership and shared resources required for the current mutation phase.",
            feature_branch,
        )
        self.assertNotIn(
            "Release ownership only after the phase is committed, verified, clean, and safely published or preserved.",
            feature_branch,
        )
        for skill_text in (feature_branch, main_branch, work_merge):
            self.assertIn("Claim Events table in resource-claim", skill_text)
            self.assertNotIn("Event Contract", skill_text)
            self.assertNotIn("claim-free", skill_text)
            self.assertNotIn("needs no claim", skill_text)

    def test_execute_workitem_package_is_retired_without_weakening_delivery_contracts(self) -> None:
        """Keep the retired bridge absent while maintained Commit skills own clean delivery."""

        self.assertFalse(EXECUTE_WORKITEM_PACKAGE.exists())
        feature_branch = FEATURE_BRANCH_SKILL.read_text(encoding="utf-8")
        main_branch = MAIN_BRANCH_SKILL.read_text(encoding="utf-8")
        self.assertIn("Claim Events table in resource-claim", feature_branch)
        self.assertIn("Claim Events table in resource-claim", main_branch)
        for text in (feature_branch, main_branch):
            self.assertIn("clean", text.lower())
            self.assertIn("commit", text.lower())

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
                if role_name == "dev-merge-coordinator":
                    self.assertIn(
                        "every Event Contract claim actually triggered",
                        purpose,
                    )
                else:
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
        """Describe claim release and registry evidence only for enabled resource-claim projects."""

        readme = README.read_text(encoding="utf-8")
        lifecycle = ORCHESTRATED_LIFECYCLE.read_text(encoding="utf-8")

        self.assertIn(
            "Resource Claim](skills/resource-claim/SKILL.md) is the only source for events that require claims",
            readme,
        )
        self.assertNotIn("integration, claim release, and execution evidence", readme)
        self.assertNotIn("commit, and claim-release gates", readme)
        self.assertIn(
            "When resource-claim is selected, the coordination registry",
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
                self.assertNotIn("resource-claim", role.skills)

    def test_read_only_roles_cannot_load_resource_claim(self) -> None:
        """Keep query response and topic verification read-only without unnecessary writer claims."""
        build_skill_docs = _load_build_skill_docs()
        skill_payload = build_skill_docs.build_payload()
        roles = {
            role.name: role
            for role in build_skill_docs.load_role_definitions(set(skill_payload["skills"]))
        }

        self.assertEqual("never", roles["wiki-query-responder"].repository_mutation)
        self.assertEqual("never", roles["wiki-topic-verifier"].repository_mutation)
        self.assertNotIn("resource-claim", roles["wiki-query-responder"].skills)
        self.assertNotIn("resource-claim", roles["wiki-topic-verifier"].skills)

    def test_project_configuration_selects_resource_coordination_independently(self) -> None:
        """Select coordination without copying its procedure or coupling it to mutation."""
        template_text = PROJECT_TEMPLATE.read_text(encoding="utf-8")
        skill_text = PROJECT_CONFIGURATION_SKILL.read_text(encoding="utf-8")

        self.assertNotIn("agent_coordination:", template_text)
        self.assertNotIn("claim_skill:", template_text)
        self.assertNotIn("dirty_unclaimed_policy:", template_text)
        self.assertIn("resource_coordination:", template_text)
        self.assertIn("repositoryMutation belongs to conceptual agent definitions and does not select claim behavior", skill_text)
        self.assertIn("has no folder overrides", skill_text)
        self.assertIn(
            "For none, include no claim skill, helper, procedure, or evidence",
            skill_text,
        )
        self.assertIn("agent_claim_transport:", template_text)
        self.assertIn("Load resource-claim only through resource_coordination", skill_text)
        self.assertIn("Verify exactly one resource-claim-helper-command or resource-claim-helper-mcp Provider Skill against resource-claim-helper", skill_text)
        self.assertIn("Generated AGENTS.md references resource-claim and includes only the selected claim helper's instructions", skill_text)

    def test_missing_project_configuration_defaults_to_solo_and_can_transition(self) -> None:
        """Keep absent configuration safe without overriding later explicit configuration."""

        solo = SOLO_MODE_SKILL.read_text(encoding="utf-8")
        multitask = MULTITASK_MODE_SKILL.read_text(encoding="utf-8")

        self.assertIn(
            "When PROJECT.yaml is absent from the repository root, the effective coordination mode is SOLO.",
            solo,
        )
        self.assertIn(
            "Do not inspect or change a secondary-thread dispatch mechanism for this fallback.",
            solo,
        )
        self.assertIn(
            "the dispatcher coordinates and the single work-item task performs the work.",
            solo,
        )
        self.assertIn(
            "When PROJECT.yaml is absent from the repository root, do not enable secondary-thread dispatch.",
            multitask,
        )
        for text in (solo, multitask):
            self.assertIn(
                "A valid repository-root PROJECT.yaml replaces this fallback",
                text,
            )
            self.assertIn(
                "Persistence and Commit selectors remain independent",
                text,
            )
            self.assertIn("project_setup.concurrent_tasking", text)
            self.assertIn("valid legacy configuration", text)

        self.assertIn(
            "When project_setup.concurrent_tasking is false, keep secondary-thread dispatch disabled",
            solo,
        )
        self.assertIn(
            "When project_setup.concurrent_tasking is true, temporarily disable",
            solo,
        )
        self.assertIn(
            "When project_setup.concurrent_tasking is false, do not enable secondary-thread dispatch",
            multitask,
        )
        self.assertIn(
            "When project_setup.concurrent_tasking is true, enable",
            multitask,
        )

    def test_corrected_skills_have_bounded_historical_provenance(self) -> None:
        """Keep migration provenance immediately after front matter without invented runtime data."""

        for path, artifact_id in HISTORICAL_SKILL_ARTIFACT_IDS.items():
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                text = path.read_text(encoding="utf-8")
                closing_frontmatter = text.index("\n---\n", len("---\n")) + len("\n---\n")
                provenance_start = text.index("<!--\n", closing_frontmatter)
                self.assertEqual(closing_frontmatter, provenance_start)
                provenance_end = text.index("-->\n", provenance_start) + len("-->\n")
                provenance = text[provenance_start:provenance_end]
                self.assertIn(
                    "Copyright (c) 2026 Martin.Bechard@DevConsult.ca",
                    provenance,
                )
                self.assertIn(f"Artifact-ID: {artifact_id}", provenance)
                self.assertIn("Artifact-ID-Evidence: migration-assigned", provenance)
                for field in (
                    "Created-UTC",
                    "Creating-Agent",
                    "Runtime",
                    "Dispatched-Model",
                    "Reasoning-Effort",
                    "Task-ID",
                ):
                    self.assertIn(f"{field}: historical-unknown", provenance)
                    self.assertIn(f"{field}-Evidence: historical-unknown", provenance)

    def test_unconfigured_project_never_loads_or_mutates_claim_state(self) -> None:
        """Gate the complete claim stack on an explicit validated project selection."""

        policy = RESOURCE_CLAIM_SKILL.read_text(encoding="utf-8")

        self.assertIn(
            "Before loading a claim helper or reading claim state, require a valid PROJECT.yaml at the repository root",
            policy,
        )
        self.assertIn(
            "explicitly selects resource-claim",
            policy,
        )
        self.assertIn(
            "When the root file is absent, resource coordination is NOT_APPLICABLE.",
            policy,
        )
        for prohibited_action in (
            "load or invoke resource-claim-helper",
            "read claim state",
            "create claim state",
            "mutate claim state",
        ):
            with self.subTest(prohibited_action=prohibited_action):
                self.assertIn(prohibited_action, policy)
        self.assertIn(
            "does not select a Persistence or Commit default",
            policy,
        )
        self.assertIn(
            "configured resource-claim-helper-* Provider Skill",
            policy,
        )
        self.assertNotIn("through the configured Provider Skill", policy)
        self.assertIn(
            "does not disable an explicitly selected Persistence or Commit Provider Skill",
            policy,
        )

    def test_bootstrapper_requires_primary_configurator_handoff_without_configuration(self) -> None:
        """Prevent missing configuration from bypassing the effective SOLO boundary."""

        role = yaml.safe_load(PROJECT_BOOTSTRAPPER_ROLE.read_text(encoding="utf-8"))
        contract = yaml.safe_dump(
            {
                "instructions": role["instructions"],
                "examples": role.get("examples", []),
            },
            sort_keys=False,
        )
        normalized_contract = " ".join(contract.split())

        self.assertIn("effective coordination mode is SOLO", normalized_contract)
        self.assertIn(
            "Do not dispatch project-configurator as a secondary Agent",
            normalized_contract,
        )
        self.assertIn("primary Project Configurator handoff", normalized_contract)
        self.assertIn("End that Project Bootstrapper execution", normalized_contract)
        self.assertIn("separately resumed Project Bootstrapper execution", normalized_contract)
        self.assertIn("project_setup.concurrent_tasking", normalized_contract)
        self.assertIn("supported legacy configuration", normalized_contract)
        self.assertIn("only after Project Configurator runs as the primary Agent", normalized_contract)
        self.assertIn(
            "PRIMARY_PROJECT_CONFIGURATOR_HANDOFF_REQUIRED",
            normalized_contract,
        )
        self.assertIn("No claim helper or claim state was loaded", normalized_contract)

    def test_role_schema_requires_repository_mutation_and_v8_output_schemas(self) -> None:
        """Expose mutation policy and the two approved strict-output roles in schema version 8."""
        schema = yaml.safe_load(ROLE_SCHEMA.read_text(encoding="utf-8"))

        self.assertEqual(8, schema["version"])
        self.assertIn("repositoryMutation", schema["required"])
        self.assertEqual("mutation-policy", schema["properties"]["repositoryMutation"])

        build_skill_docs = _load_build_skill_docs()
        roles = {
            role.name: role
            for role in build_skill_docs.load_role_definitions(
                set(build_skill_docs.build_payload()["skills"])
            )
        }
        for role_name in (
            "methodology-design-system-checklist-runner",
            "methodology-design-system-review-coordinator",
        ):
            with self.subTest(role=role_name):
                output_schema = roles[role_name].output_schema
                self.assertEqual("object", output_schema["type"])
                self.assertFalse(output_schema["additionalProperties"])
                self.assertEqual(
                    list(roles[role_name].output_contract),
                    output_schema["required"],
                )

    def test_generator_accepts_mutation_policy_without_resource_claim(self) -> None:
        """Load a mutating conceptual definition without coupling it to resource-claim."""
        build_skill_docs = _load_build_skill_docs()
        required, allowed, groups = build_skill_docs.load_role_schema()
        skill_names = set(build_skill_docs.build_payload()["skills"])
        model_profiles = set(build_skill_docs.load_model_profiles())
        source = ROOT / "agents" / "roles" / "dev-activities" / "dev-coder.role.yaml"
        role = yaml.safe_load(source.read_text(encoding="utf-8"))
        role["skills"] = [
            entry for entry in role["skills"] if next(iter(entry)) != "resource-claim"
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
        self.assertNotIn("resource-claim", loaded.skills)

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
