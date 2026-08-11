#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies the STE skill, documentation-role routing, and semantic-preservation boundaries.

from __future__ import annotations

import importlib.util
import sys
import tomllib
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "scripts" / "build-skill-docs.py"
SKILL_PATH = ROOT / "skills" / "ste-technical-writing" / "SKILL.md"
OPENAI_METADATA_PATH = SKILL_PATH.parent / "agents" / "openai.yaml"
ROLE_SCHEMA_PATH = ROOT / "agents" / "role-schema.yaml"
CODEX_PROFILES_PATH = ROOT / "adapters" / "codex" / "model-profiles.yaml"
HIERARCHY_PATH = ROOT / "design" / "agent-skill-hierarchy.svg"
ROLES_ROOT = ROOT / "agents" / "roles"

DOCUMENTATION_ROLES = {
    "wiki-architect",
    "wiki-researcher",
}

PROJECT_SETUP_PARAGRAPH = (
    "Project agent and skill setup asks Setup mode first, defaulting to Basic, and "
    "records the result in one root PROJECT.yaml as an intermediate, reviewable intent "
    "log. Basic asks whether to create the Wiki and asks the user to confirm detected "
    "technologies; it shows Concurrent tasking No, Persistence none, Commit main-branch, "
    "installed core skill delivery, and technology skill delivery by-reference as Set "
    "values. Advanced exposes Concurrent tasking, conditional capacity, Persistence, "
    "Commit, wiki/specifications/both documentation structure, technology confirmation, "
    "and technology delivery. Setup creates only selected empty documentation roots and "
    "never runs reverse engineering."
)

STE_ACTIVATION_FIXTURES = (
    (
        "technical-document-prose",
        "technical-document",
        "Rewrite the README installation section.",
        True,
        True,
        "Apply this skill when an agent writes, rewrites, or reviews technical-document prose.",
    ),
    (
        "ordinary-communication",
        "ordinary-communication",
        "Tell the user that the focused tests passed.",
        False,
        False,
        "Do not apply them to an ordinary user or agent message unless that message contains technical-document prose.",
    ),
    (
        "non-document-artifact",
        "machine-readable-data",
        "resource_coordination: resource-claim",
        False,
        False,
        "Do not rewrite code blocks, machine-readable data, syntax examples",
    ),
)


def _load_build_module():
    spec = importlib.util.spec_from_file_location("build_skill_docs", BUILD_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load build-skill-docs.py.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _ste_activates_for_fixture(
    surface: str,
    *,
    contains_technical_document_prose: bool,
) -> bool:
    if surface == "technical-document":
        return True
    if surface == "ordinary-communication":
        return contains_technical_document_prose
    return False


def _semantic_violations(
    source: str,
    candidate: str,
    *,
    protected: tuple[str, ...] = (),
    conditions: tuple[str, ...] = (),
    owners: tuple[str, ...] = (),
    descriptive: bool = False,
    unordered: bool = False,
) -> list[str]:
    violations: list[str] = []
    for value in (*protected, *conditions, *owners):
        if value in source and value not in candidate:
            violations.append(f"changed or removed: {value}")
    for modality in ("must not", "must", "may"):
        if modality in source and modality not in candidate:
            violations.append(f"changed normative force: {modality}")
    if "resourceCoordination" not in source and "resourceCoordination" in candidate:
        violations.append("invented configuration: resourceCoordination")
    if descriptive and any(
        line.lstrip().startswith(("1.", "2.", "3."))
        for line in candidate.splitlines()
    ):
        violations.append("changed description into instructions")
    if unordered and any(
        line.lstrip().startswith(("1.", "2.", "3."))
        for line in candidate.splitlines()
    ):
        violations.append("changed unordered information into an ordered procedure")
    return violations


class SteTechnicalWritingContractTests(unittest.TestCase):
    """Verify the source contracts and generated routing for technical-document prose."""

    def test_skill_package_owns_prose_without_claiming_formal_compliance(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")
        metadata = yaml.safe_load(OPENAI_METADATA_PATH.read_text(encoding="utf-8"))

        required_phrases = (
            "Preserve the source meaning",
            "Preserve each requirement, condition, permission, prohibition",
            "Keep a description descriptive",
            "The opening of a section gives readers the conceptual frame",
            "Write this essential definition before properties, components, examples",
            "Do not open a section with an enumeration",
            "Identify the essence and central idea of each section",
            "Let the artifact-specific skill control document structure",
            "does not verify or certify formal ASD-STE100 compliance",
            "Do not rewrite code blocks, machine-readable data, syntax examples",
            "structured-explanation",
            "effective-communication",
        )
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill_text)

        self.assertEqual(
            "Ste Technical Writing",
            metadata["interface"]["display_name"],
        )
        self.assertIn(
            "$ste-technical-writing",
            metadata["interface"]["default_prompt"],
        )

    def test_section_opening_contract_defines_the_topic_before_enumeration(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")
        section = skill_text.split("## Establish the Topic First\n", 1)[1]
        section = section.split("\n## ", 1)[0].strip()

        definition = "The opening of a section gives readers the conceptual frame"
        first_rule = "- Write this essential definition before properties"
        self.assertTrue(section.startswith(definition))
        self.assertLess(section.index(definition), section.index(first_rule))
        self.assertIn(
            "- Do not open a section with an enumeration unless preceding prose "
            "has already established that frame.",
            section,
        )

    def test_every_conceptual_agent_receives_the_shared_ste_contract(self) -> None:
        schema = yaml.safe_load(ROLE_SCHEMA_PATH.read_text(encoding="utf-8"))
        shared_skills = [
            next(iter(entry))
            for entry in schema["fixedBehavior"]["sharedSkills"]
        ]
        self.assertEqual(
            ["effective-communication", "ste-technical-writing"],
            shared_skills,
        )

        build_skill_docs = _load_build_module()
        skills = set(build_skill_docs.build_payload()["skills"])
        roles = build_skill_docs.load_role_definitions(skills)
        self.assertTrue(roles)
        for role in roles:
            with self.subTest(role=role.name):
                self.assertIn("ste-technical-writing", role.skills)
                self.assertNotIn(
                    "ste-technical-writing",
                    role.skill_conditions,
                )

    def test_generated_hierarchy_assigns_ste_to_every_role(self) -> None:
        role_count = len(list(ROLES_ROOT.glob("*/*.role.yaml")))

        hierarchy = ET.parse(HIERARCHY_PATH).getroot()
        hierarchy_edges = [
            edge
            for edge in hierarchy.iter("{http://www.w3.org/2000/svg}path")
            if edge.attrib.get("data-skill") == "ste-technical-writing"
        ]
        self.assertEqual(role_count, len(hierarchy_edges))
        self.assertTrue(
            all(
                "conditional-edge" not in edge.attrib["class"]
                for edge in hierarchy_edges
            )
        )

    def test_documentation_roles_and_codex_profile_use_gpt_55_high(self) -> None:
        build_skill_docs = _load_build_module()
        skills = set(build_skill_docs.build_payload()["skills"])
        roles = build_skill_docs.load_role_definitions(skills)
        roles_by_name = {role.name: role for role in roles}

        self.assertEqual(
            DOCUMENTATION_ROLES,
            {
                role.name
                for role in roles
                if role.model_profile == "documentation"
            },
        )

        profiles = yaml.safe_load(
            CODEX_PROFILES_PATH.read_text(encoding="utf-8")
        )["profiles"]
        self.assertEqual("gpt-5.5", profiles["documentation"]["model"])
        self.assertEqual("high", profiles["documentation"]["effort"])

        writer = roles_by_name["dev-documentation-writer"]
        self.assertIn("structured-explanation", writer.instructions)
        self.assertIn(
            "facts, hypotheses, unknowns, technical causes, decisions",
            writer.instructions,
        )
        self.assertIn(
            "Do not require QUERY, FACT, or ANSWER items",
            writer.instructions,
        )

        codex_profiles = build_skill_docs.load_adapter_model_profiles(
            "codex",
            set(build_skill_docs.load_model_profiles()),
        )
        for role_name in DOCUMENTATION_ROLES:
            with self.subTest(role=role_name):
                role = roles_by_name[role_name]
                rendered = build_skill_docs.render_codex_agent(
                    role,
                    codex_profiles,
                    known_role_names=tuple(roles_by_name),
                )
                parsed = tomllib.loads(rendered)
                self.assertEqual("gpt-5.5", parsed["model"])
                self.assertEqual("high", parsed["model_reasoning_effort"])

    def test_non_codex_documentation_profile_mappings_remain_native(self) -> None:
        expected = {
            "claude": ("fable-5", None),
            "gemini": ("auto", None),
            "junie": ("gpt-5.6-sol", "high"),
        }
        build_skill_docs = _load_build_module()
        source_profiles = set(build_skill_docs.load_model_profiles())
        for adapter, mapping in expected.items():
            with self.subTest(adapter=adapter):
                profile = build_skill_docs.load_adapter_model_profiles(
                    adapter,
                    source_profiles,
                )["documentation"]
                self.assertEqual(mapping, (profile.model, profile.effort))

    def test_boundary_skills_preserve_format_and_semantics(self) -> None:
        skill_texts = {
            name: (
                ROOT / "skills" / name / "SKILL.md"
            ).read_text(encoding="utf-8")
            for name in (
                "effective-communication",
                "structured-explanation",
                "verify-documentation-page",
            )
        }
        self.assertIn(
            "ordinary user and agent messages",
            skill_texts["effective-communication"],
        )
        self.assertIn(
            "Do not convert descriptive artifact content into instructions",
            skill_texts["effective-communication"],
        )
        self.assertIn(
            "STE governs the prose inside each item",
            skill_texts["structured-explanation"],
        )
        self.assertIn(
            "does not replace the item model",
            skill_texts["structured-explanation"],
        )
        verifier = skill_texts["verify-documentation-page"]
        for phrase in (
            "semantic changes caused by mechanical STE application",
            "A description changed into an instruction",
            "Unordered information changed into an ordered procedure",
            "identifier, configuration value, modality, condition, ownership",
            "Do not report formal ASD-STE100 verification or certification",
        ):
            with self.subTest(verifier_phrase=phrase):
                self.assertIn(phrase, verifier)

    def test_activation_fixtures_exclude_ordinary_messages_and_data(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")

        for (
            fixture_id,
            surface,
            content,
            contains_technical_document_prose,
            expected_activation,
            contract,
        ) in STE_ACTIVATION_FIXTURES:
            with self.subTest(fixture=fixture_id):
                self.assertTrue(content)
                self.assertIn(contract, skill_text)
                self.assertEqual(
                    expected_activation,
                    _ste_activates_for_fixture(
                        surface,
                        contains_technical_document_prose=(
                            contains_technical_document_prose
                        ),
                    ),
                )

    def test_project_setup_description_rejects_an_ordered_procedure(self) -> None:
        candidate = """\
1. Select Basic or Advanced Setup mode.
2. Record the result in PROJECT.yaml.
3. Configure Concurrent tasking, Persistence, Commit, and documentation.
4. Create the selected documentation roots.
"""
        violations = _semantic_violations(
            PROJECT_SETUP_PARAGRAPH,
            candidate,
            protected=(
                "Setup mode",
                "Basic",
                "Advanced",
                "PROJECT.yaml",
                "Concurrent tasking",
                "Persistence",
                "Commit",
                "main-branch",
                "by-reference",
                "Set",
            ),
            descriptive=True,
            unordered=True,
        )
        self.assertIn("changed description into instructions", violations)
        self.assertIn(
            "changed unordered information into an ordered procedure",
            violations,
        )

    def test_fixture_rejects_invented_configuration_and_changed_modality(self) -> None:
        invented = (
            PROJECT_SETUP_PARAGRAPH
            + " Set resourceCoordination to resource-claim."
        )
        self.assertIn(
            "invented configuration: resourceCoordination",
            _semantic_violations(PROJECT_SETUP_PARAGRAPH, invented),
        )

        source = (
            "If PROJECT.yaml selects resource-claim, Project Configurator must preserve "
            "AGENTS.md. The writer must not change `--inline-tech-skills`. "
            "The reviewer may quote \"Set\"."
        )
        candidate = (
            "Project Configurator should preserve AGENTS.md. "
            "The writer can change `--inline-tech-skills`."
        )
        violations = _semantic_violations(
            source,
            candidate,
            protected=(
                "PROJECT.yaml",
                "AGENTS.md",
                "`--inline-tech-skills`",
                '"Set"',
            ),
            conditions=("If PROJECT.yaml selects resource-claim",),
            owners=("Project Configurator", "writer", "reviewer"),
        )
        self.assertIn("changed normative force: must", violations)
        self.assertIn("changed normative force: must not", violations)
        self.assertIn("changed normative force: may", violations)
        self.assertIn(
            "changed or removed: If PROJECT.yaml selects resource-claim",
            violations,
        )

    def test_fixture_rejects_changed_identifier(self) -> None:
        source = "Project Configurator must read `PROJECT.yaml`."
        candidate = "Project Configurator must read `PROJECT.yml`."

        self.assertEqual(
            ["changed or removed: `PROJECT.yaml`"],
            _semantic_violations(
                source,
                candidate,
                protected=("`PROJECT.yaml`",),
            ),
        )

    def test_fixture_rejects_changed_configuration_value(self) -> None:
        source = "Set Commit to `main-branch`."
        candidate = "Set Commit to `feature-branch`."

        self.assertEqual(
            ["changed or removed: `main-branch`"],
            _semantic_violations(
                source,
                candidate,
                protected=("`main-branch`",),
            ),
        )

    def test_fixture_rejects_changed_owner(self) -> None:
        source = "Project Configurator records the selected setup mode."
        candidate = "Dev Orchestrator records the selected setup mode."

        self.assertEqual(
            ["changed or removed: Project Configurator"],
            _semantic_violations(
                source,
                candidate,
                owners=("Project Configurator",),
            ),
        )

    def test_fixture_accepts_exact_technical_content_in_all_prose_surfaces(self) -> None:
        source = """\
# Configuration

**FACT: F-1**
- **SYNOPSIS:** If `PROJECT.yaml` selects `resource-claim`, run `python3 tool.py --check`.

| Fixed label | Value |
| --- | --- |
| Schema | `dev-methodology-role` |

```yaml
resource_coordination: resource-claim
```

The operator said, "Keep AGENTS.md unchanged."
"""
        candidate = source.replace(
            "If `PROJECT.yaml` selects `resource-claim`, run",
            "If `PROJECT.yaml` selects `resource-claim`, run",
        )
        self.assertEqual(
            [],
            _semantic_violations(
                source,
                candidate,
                protected=(
                    "# Configuration",
                    "**FACT: F-1**",
                    "**SYNOPSIS:**",
                    "`PROJECT.yaml`",
                    "`resource-claim`",
                    "`python3 tool.py --check`",
                    "| Fixed label | Value |",
                    "`dev-methodology-role`",
                    "resource_coordination: resource-claim",
                    '"Keep AGENTS.md unchanged."',
                ),
                conditions=("If `PROJECT.yaml` selects `resource-claim`",),
            ),
        )


if __name__ == "__main__":
    unittest.main()
