#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies the shared communication skill and its generated-agent wiring.

from __future__ import annotations

import importlib.util
import json
import re
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "scripts" / "build-skill-docs.py"
SKILL_PATH = ROOT / "skills" / "effective-communication" / "SKILL.md"
ROLE_SCHEMA_PATH = ROOT / "agents" / "role-schema.yaml"
HIERARCHY_PATH = ROOT / "design" / "agent-skill-hierarchy.svg"
EXPLORER_PATH = ROOT / "design" / "generated" / "agent-skill-explorer-data.js"
ROLES_ROOT = ROOT / "agents" / "roles"


def load_build_module():
    spec = importlib.util.spec_from_file_location("build_skill_docs", BUILD_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load build-skill-docs.py.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def unexplained_definite_references(text: str, nouns: tuple[str, ...]) -> list[str]:
    """Return nouns used with 'the' before an introducing phrase."""

    issues: list[str] = []
    normalized = re.sub(r"\s+", " ", text.lower())
    for noun in nouns:
        definite = re.search(rf"\bthe {re.escape(noun)}\b", normalized)
        if definite is None:
            continue
        introduction = re.search(
            rf"\b(?:a|an|one|this|that|each|every)"
            rf"(?: [a-z][a-z-]*){{0,3}} {re.escape(noun)}\b",
            normalized,
        )
        if introduction is None or introduction.start() > definite.start():
            issues.append(noun)
    return issues


class EffectiveCommunicationContractTests(unittest.TestCase):
    def test_skill_contains_required_user_and_handoff_contracts(self) -> None:
        text = SKILL_PATH.read_text(encoding="utf-8")

        required_phrases = (
            "Start with the outcome",
            "Keep sentences short",
            "Put one rule or idea in each sentence",
            "Explain a specialized or project-specific term when it first appears",
            "Introduce a specific instance before later referring to it with “the.”",
            "State an approval question directly",
            "Explain the practical consequence of each option",
            "State the blocker, its evidence, the owner of the next action",
            "An agent handoff gives another agent enough information to continue",
            "Do not narrate routine tool use",
        )
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_common_noun_reference_check_rejects_unintroduced_instance(self) -> None:
        self.assertEqual(
            ["result"],
            unexplained_definite_references(
                "The result identifies an owner.",
                ("result",),
            ),
        )
        self.assertEqual(
            [],
            unexplained_definite_references(
                "A claim result identifies an owner. The result identifies a file.",
                ("result",),
            ),
        )

    def test_role_schema_assigns_communication_to_every_role(self) -> None:
        schema = yaml.safe_load(ROLE_SCHEMA_PATH.read_text(encoding="utf-8"))
        shared_entries = schema["fixedBehavior"]["sharedSkills"]
        self.assertEqual(
            ["effective-communication", "ste-technical-writing"],
            [next(iter(entry)) for entry in shared_entries],
        )

        build_skill_docs = load_build_module()
        skills = set(build_skill_docs.build_payload()["skills"])
        roles = build_skill_docs.load_role_definitions(skills)
        self.assertTrue(roles)
        for role in roles:
            with self.subTest(role=role.name):
                self.assertIn("effective-communication", role.skills)
                self.assertNotIn("effective-communication", role.skill_conditions)

    def test_generated_relationship_views_assign_communication_to_every_role(self) -> None:
        role_count = len(list(ROLES_ROOT.glob("*/*.role.yaml")))

        hierarchy = ET.parse(HIERARCHY_PATH).getroot()
        hierarchy_edges = [
            edge
            for edge in hierarchy.iter("{http://www.w3.org/2000/svg}path")
            if edge.attrib.get("data-skill") == "effective-communication"
        ]
        self.assertEqual(role_count, len(hierarchy_edges))
        self.assertTrue(
            all(
                "conditional-edge" not in edge.attrib["class"]
                for edge in hierarchy_edges
            )
        )
        communication_node = next(
            node
            for node in hierarchy.iter("{http://www.w3.org/2000/svg}g")
            if node.attrib.get("data-skill") == "effective-communication"
        )
        self.assertNotIn(
            "unassigned",
            " ".join(text.strip() for text in communication_node.itertext()),
        )

        explorer_text = EXPLORER_PATH.read_text(encoding="utf-8")
        explorer_payload = json.loads(explorer_text.split(" = ", 1)[1].rstrip(";\n"))
        explorer_edges = [
            edge
            for edge in explorer_payload["edges"]
            if edge["skill"] == "effective-communication"
        ]
        self.assertEqual(role_count, len(explorer_edges))
        self.assertTrue(all(edge["kind"] == "fixed" for edge in explorer_edges))


if __name__ == "__main__":
    unittest.main()
