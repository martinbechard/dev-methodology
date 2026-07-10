# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies the generated interactive agent-to-skill hierarchy structure and behavior hooks.

from __future__ import annotations

import importlib.util
import unittest
import xml.etree.ElementTree as element_tree
from pathlib import Path
from types import ModuleType


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "scripts" / "build-agent-skill-hierarchy.py"
OUTPUT_PATH = REPOSITORY_ROOT / "design" / "agent-skill-hierarchy.svg"
ROLES_ROOT = REPOSITORY_ROOT / "agents" / "roles"
SVG_NAMESPACE = "http://www.w3.org/2000/svg"


def _load_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "build_agent_skill_hierarchy", SCRIPT_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AgentSkillHierarchyTests(unittest.TestCase):
    """Protects the hierarchy's generated output, ordering, and selection affordances."""

    def setUp(self) -> None:
        """Render and parse the current hierarchy for each isolated test."""
        self.module = _load_module()
        self.rendered = self.module.build_svg()
        self.root = element_tree.fromstring(self.rendered)

    def test_generated_hierarchy_is_current(self) -> None:
        """The committed SVG must exactly match the canonical generator output."""
        self.assertEqual(self.rendered, OUTPUT_PATH.read_text(encoding="utf-8"))

    def test_hierarchy_omits_model_profiles_and_puts_stack_skills_last(self) -> None:
        """The visual map should reserve its final skill group for setup-time stacks."""
        visible_text = " ".join(text.strip() for text in self.root.itertext() if text.strip())
        self.assertNotIn("Model profiles", visible_text)
        self.assertNotIn("model-edge", self.rendered)
        self.assertEqual("group", self.root.attrib.get("role"))

        group_nodes = self.root.findall(
            f".//{{{SVG_NAMESPACE}}}text[@class='group']"
        )
        skill_group_nodes = [
            node for node in group_nodes if int(node.attrib["x"]) == self.module.SKILL_X
        ]
        self.assertEqual("Stack And Domain", skill_group_nodes[-1].text)

    def test_agents_and_skills_expose_selection_and_keyboard_hooks(self) -> None:
        """Every role and skill should be an accessible selector with mapped edges."""
        role_nodes = self.root.findall(
            f".//{{{SVG_NAMESPACE}}}g[@class='role-node']"
        )
        self.assertEqual(len(list(ROLES_ROOT.glob("*/*.role.yaml"))), len(role_nodes))
        for node in role_nodes:
            with self.subTest(role=node.attrib.get("data-role")):
                self.assertEqual("button", node.attrib.get("role"))
                self.assertEqual("0", node.attrib.get("tabindex"))
                self.assertEqual("false", node.attrib.get("aria-pressed"))
                self.assertTrue(node.attrib.get("data-role"))
                self.assertTrue(node.attrib.get("data-display-name"))

        skill_nodes = self.root.findall(
            f".//{{{SVG_NAMESPACE}}}g[@class='skill-node']"
        )
        self.assertTrue(skill_nodes)
        for node in skill_nodes:
            with self.subTest(skill=node.attrib.get("data-skill")):
                self.assertEqual("button", node.attrib.get("role"))
                self.assertEqual("0", node.attrib.get("tabindex"))
                self.assertEqual("false", node.attrib.get("aria-pressed"))
                self.assertTrue(node.attrib.get("data-skill"))

        edges = self.root.findall(f".//{{{SVG_NAMESPACE}}}path[@data-role]")
        self.assertTrue(edges)
        self.assertTrue(all(edge.attrib.get("data-skill") for edge in edges))
        self.assertIn('event.key === "Enter"', self.rendered)
        self.assertIn('event.key === "Escape"', self.rendered)
        self.assertIn('aria-live="polite"', self.rendered)
        self.assertIn("function selectSkill(skillName)", self.rendered)
        self.assertIn("edge.dataset.skill === selectedSkill", self.rendered)
        self.assertIn("canonical agents use", self.rendered)

    def test_agent_groups_follow_the_canonical_schema_order(self) -> None:
        """The visual reading order should match the maintained role-group contract."""
        group_nodes = self.root.findall(
            f".//{{{SVG_NAMESPACE}}}text[@class='group']"
        )
        role_group_labels = [
            node.text
            for node in group_nodes
            if int(node.attrib["x"]) == self.module.ROLE_X
        ]
        self.assertEqual(
            [
                "Methodology Maintenance",
                "Project Setup",
                "Wiki Activities",
                "Development Use",
            ],
            role_group_labels,
        )


if __name__ == "__main__":
    unittest.main()
