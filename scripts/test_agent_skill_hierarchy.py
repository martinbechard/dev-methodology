# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies the generated interactive agent-to-skill hierarchy structure and behavior hooks.

from __future__ import annotations

import importlib.util
import re
import unittest
import xml.etree.ElementTree as element_tree
from pathlib import Path
from types import ModuleType

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "scripts" / "build-agent-skill-hierarchy.py"
OUTPUT_PATH = REPOSITORY_ROOT / "design" / "agent-skill-hierarchy.svg"
ROLE_MAP_PATH = REPOSITORY_ROOT / "design" / "agent-and-skill-definitions.html"
ROLES_ROOT = REPOSITORY_ROOT / "agents" / "roles"
DETECTION_REGISTRY_PATH = (
    REPOSITORY_ROOT
    / "skills"
    / "detect-technology-skills"
    / "references"
    / "technology-skill-detection-registry.yaml"
)
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
        """The committed SVG must exactly match the generator output."""
        self.assertEqual(self.rendered, OUTPUT_PATH.read_text(encoding="utf-8"))

    def test_hierarchy_omits_model_profiles_and_setup_time_skills(self) -> None:
        """The visual map should contain agent relationships without setup-time clutter."""
        visible_text = " ".join(text.strip() for text in self.root.itertext() if text.strip())
        self.assertNotIn("Model profiles", visible_text)
        self.assertNotIn("model-edge", self.rendered)
        self.assertEqual("group", self.root.attrib.get("role"))

        group_nodes = self.root.findall(
            f".//{{{SVG_NAMESPACE}}}text[@class='group']"
        )
        skill_group_labels = [
            node.text
            for node in group_nodes
            if int(node.attrib["x"]) == self.module.SKILL_X
        ]
        self.assertNotIn("Stack And Domain", skill_group_labels)
        self.assertNotIn("setup-time technology", visible_text)
        visible_skills = {
            node.attrib["data-skill"]
            for node in self.root.findall(
                f".//{{{SVG_NAMESPACE}}}g[@class='skill-node']"
            )
        }
        detection_registry = yaml.safe_load(
            DETECTION_REGISTRY_PATH.read_text(encoding="utf-8")
        )
        detected_skills = {
            entry["skill"] for entry in detection_registry["skills"]
        }
        self.assertTrue(detected_skills)
        self.assertTrue(visible_skills.isdisjoint(detected_skills))

    def test_agents_and_skills_expose_selection_and_keyboard_hooks(self) -> None:
        """Every conceptual definition and skill should be an accessible selector with mapped edges."""
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
        self.assertIn("agents use", self.rendered)

    def test_agent_dependencies_are_directional_and_user_controllable(self) -> None:
        """Fixed direct agent use should render as optional directional arrows."""
        expected_edges = [
            (role["name"], target_role)
            for path in ROLES_ROOT.glob("*/*.role.yaml")
            for role in (self.module._load_yaml(path),)
            for target_role in role.get("agentDependencies", [])
        ]
        dependency_edges = self.root.findall(
            f".//{{{SVG_NAMESPACE}}}path[@class='dependency-edge']"
        )
        actual_edges = [
            (
                edge.attrib.get("data-source-role"),
                edge.attrib.get("data-target-role"),
            )
            for edge in dependency_edges
        ]
        self.assertEqual(len(expected_edges), len(dependency_edges))
        self.assertEqual(len(actual_edges), len(set(actual_edges)))
        self.assertCountEqual(expected_edges, actual_edges)

        role_centers = {}
        for node in self.root.findall(
            f".//{{{SVG_NAMESPACE}}}g[@class='role-node']"
        ):
            rect = node.find(f"{{{SVG_NAMESPACE}}}rect")
            self.assertIsNotNone(rect)
            role_centers[node.attrib["data-role"]] = (
                float(rect.attrib["x"]) + float(rect.attrib["width"]),
                float(rect.attrib["y"]) + (float(rect.attrib["height"]) / 2),
            )

        for edge in dependency_edges:
            with self.subTest(
                source=edge.attrib.get("data-source-role"),
                target=edge.attrib.get("data-target-role"),
            ):
                coordinates = [
                    float(value)
                    for value in re.findall(r"-?\d+(?:\.\d+)?", edge.attrib["d"])
                ]
                self.assertEqual(8, len(coordinates))
                source_x, source_y = role_centers[edge.attrib["data-source-role"]]
                target_x, target_y = role_centers[edge.attrib["data-target-role"]]
                self.assertEqual((source_x, source_y), tuple(coordinates[:2]))
                self.assertEqual((target_x + 1, target_y), tuple(coordinates[-2:]))
        self.assertTrue(
            all(
                edge.attrib.get("marker-end") == "url(#dependency-arrow)"
                for edge in dependency_edges
            )
        )
        dependency_marker = self.root.find(
            f".//{{{SVG_NAMESPACE}}}marker[@id='dependency-arrow']"
        )
        self.assertIsNotNone(dependency_marker)
        self.assertEqual("userSpaceOnUse", dependency_marker.attrib.get("markerUnits"))
        self.assertEqual("7", dependency_marker.attrib.get("markerWidth"))
        self.assertIn(".dependency-arrowhead{fill:none", self.rendered)
        dependency_toggle = self.root.find(
            f".//{{{SVG_NAMESPACE}}}g[@role='checkbox']"
        )
        self.assertIsNotNone(dependency_toggle)
        self.assertEqual("checkbox", dependency_toggle.attrib.get("role"))
        self.assertEqual("true", dependency_toggle.attrib.get("aria-checked"))
        self.assertEqual("0", dependency_toggle.attrib.get("tabindex"))
        self.assertIn("checked", dependency_toggle.attrib.get("class", "").split())
        self.assertIn(
            "show-agent-dependencies",
            self.root.attrib.get("class", "").split(),
        )
        self.assertIn("Show agent dependencies", " ".join(self.root.itertext()))
        self.assertNotIn("Click to select.", self.rendered)
        self.assertIn("let showAgentDependencies = true", self.rendered)
        self.assertIn("toggleAgentDependencies", self.rendered)

    def test_agent_groups_follow_the_role_schema_order(self) -> None:
        """The visual reading order should match the maintained definition-group contract."""
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
                "Dev Activities",
                "Wiki Activities",
                "Project Setup",
                "Methodology Maintenance",
            ],
            role_group_labels,
        )

    def test_skill_groups_start_with_development_then_wiki(self) -> None:
        """The skill reading order should mirror the first two agent categories."""
        group_nodes = self.root.findall(
            f".//{{{SVG_NAMESPACE}}}text[@class='group']"
        )
        skill_group_labels = [
            node.text
            for node in group_nodes
            if int(node.attrib["x"]) == self.module.SKILL_X
        ]

        self.assertEqual(
            [
                "Development Practice",
                "Wiki And Knowledge",
                "Documentation Methodology",
                "Artifact Creation",
                "Artifact Review",
            ],
            skill_group_labels,
        )

    def test_role_cards_follow_the_role_schema_order(self) -> None:
        """The reader-facing conceptual agent definition cards follow group order."""
        role_map = ROLE_MAP_PATH.read_text(encoding="utf-8")
        group_markers = [
            f'data-role-group="{group}"'
            for group in self.module._load_yaml(
                self.module.ROLE_SCHEMA_PATH
            )["roleGroups"]
        ]

        self.assertEqual(
            sorted(role_map.index(marker) for marker in group_markers),
            [role_map.index(marker) for marker in group_markers],
        )

    def test_map_legend_stays_with_the_map_without_a_category_summary(self) -> None:
        """The edge legend belongs to the diagram instead of a standalone section."""
        role_map = ROLE_MAP_PATH.read_text(encoding="utf-8")
        hierarchy_section = role_map.split(
            '<section class="section" aria-labelledby="hierarchy-title">', 1
        )[1].split("</section>", 1)[0]

        self.assertIn(
            "This diagram uses color to distinguish agent-to-skill assignments from agent-to-agent dependencies.",
            hierarchy_section,
        )
        self.assertIn("Amber lines show skills an agent always uses", hierarchy_section)
        self.assertIn("Blue arrows show direct dependencies between agents", hierarchy_section)
        self.assertIn(
            "Blue skill cards have a separate meaning: they identify technology skills selected during project setup.",
            hierarchy_section,
        )
        self.assertNotIn("Role Agent Categories", role_map)
        self.assertNotIn("The role model has four operating categories", role_map)

    def test_default_edges_are_balanced_and_selected_edges_use_full_intensity(self) -> None:
        """Unselected relationship types should be comparable while selected paths remain prominent."""
        self.assertIn(
            ".edge{fill:none;stroke:#94a3b8;stroke-width:1;opacity:.32;",
            self.rendered,
        )
        self.assertIn(".edge.active{stroke:#0f766e;stroke-width:2.4;opacity:1}", self.rendered)
        self.assertIn(
            ".show-agent-dependencies .dependency-edge{opacity:.32}",
            self.rendered,
        )
        self.assertIn(
            ".show-agent-dependencies .dependency-edge.active{stroke-width:3;opacity:1}",
            self.rendered,
        )

    def test_selected_items_expose_the_definition_view_bridge(self) -> None:
        """A selected conceptual agent definition or skill enables a reusable definition control."""
        view_control = self.root.find(
            f".//{{{SVG_NAMESPACE}}}g[@class='view-control disabled']"
        )
        self.assertIsNotNone(view_control)
        self.assertEqual("button", view_control.attrib.get("role"))
        self.assertEqual("-1", view_control.attrib.get("tabindex"))
        self.assertEqual("true", view_control.attrib.get("aria-disabled"))
        self.assertIn("View definition", " ".join(self.root.itertext()))
        self.assertIn('"dev-methodology:view-definition"', self.rendered)
        self.assertIn("window.parent.postMessage", self.rendered)
        self.assertIn('target.searchParams.set("definitionKind", kind)', self.rendered)

    def test_double_clicking_a_node_opens_its_definition(self) -> None:
        """Double-click should select an agent or skill and use the definition bridge."""
        self.assertIn('node.addEventListener("dblclick"', self.rendered)
        self.assertIn("viewRoleDefinition(node.dataset.role)", self.rendered)
        self.assertIn("viewSkillDefinition(node.dataset.skill)", self.rendered)
        self.assertNotIn("Click to select.", self.rendered)


if __name__ == "__main__":
    unittest.main()
