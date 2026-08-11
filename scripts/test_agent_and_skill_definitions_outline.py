# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies the durable outline and generated definitions-page sibling order.

from __future__ import annotations

import json
import re
import unittest
import xml.etree.ElementTree as element_tree
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
OUTLINE_PATH = ROOT / "design" / "agent-and-skill-definitions.outline.md"
PAGE_PATH = ROOT / "design" / "agent-and-skill-definitions.html"
ROLE_GROUPS_PATH = ROOT / "design" / "role-catalog-groups.yaml"
SKILL_CATEGORIES_PATH = ROOT / "design" / "skill-categories.yaml"
ROLE_DATA_PATH = ROOT / "design" / "generated" / "role-definitions.js"
HIERARCHY_PATH = ROOT / "design" / "agent-skill-hierarchy.svg"
SVG_NAMESPACE = "http://www.w3.org/2000/svg"
REQUIRED_DIRECTIVE = (
    "design/agent-and-skill-definitions.html and its complete generated catalog must "
    "follow this outline and sibling order. The interactive hierarchy must preserve the "
    "relative skill-category order from design/skill-categories.yaml while omitting Stack "
    "and domain skills, which are setup-time skills. Any intentional structural change "
    "must update the outline and its conformance tests in the same accepted change."
)


def _read_json_assignment(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    payload = text.split(" = ", 1)[1].rstrip(";\n")
    value = json.loads(payload)
    if not isinstance(value, dict):
        raise AssertionError(f"Expected generated object in {path}")
    return value


def _outline_tree(text: str) -> list[tuple[int, str]]:
    match = re.search(r"```text\n(.*?)\n```", text, flags=re.DOTALL)
    if match is None:
        raise AssertionError("The outline must contain one text directory tree.")
    rows: list[tuple[int, str]] = []
    for raw_line in match.group(1).splitlines():
        branch_match = re.fullmatch(r"((?:│   |    )*)(?:├── |└── )(.+)", raw_line)
        if branch_match is None:
            if rows:
                raise AssertionError(f"Invalid directory-tree row: {raw_line}")
            rows.append((0, raw_line))
            continue
        rows.append((len(branch_match.group(1)) // 4 + 1, branch_match.group(2)))
    return rows


def _expected_tree(
    page_text: str,
    role_groups: list[dict[str, str]],
    skill_categories: list[dict[str, str]],
) -> list[tuple[int, str]]:
    headings = re.findall(r"<h([123])(?: id=\"[^\"]+\")?>([^<]+)</h\1>", page_text)
    page_tree = [(int(level) - 1, label) for level, label in headings]
    agent_index = page_tree.index((1, "Conceptual Agent Definitions")) + 1
    page_tree[agent_index:agent_index] = [
        (2, f"Agents for {group['label']}") for group in role_groups
    ]
    catalog_index = page_tree.index((2, "Generated Skill Catalog")) + 1
    page_tree[catalog_index:catalog_index] = [
        (3, category["label"]) for category in skill_categories
    ]
    return page_tree


def _assert_conformance(
    outline_text: str,
    page_text: str,
    role_groups: list[dict[str, str]],
    skill_categories: list[dict[str, str]],
) -> None:
    if REQUIRED_DIRECTIVE not in outline_text:
        raise AssertionError("The normative outline directive is missing.")
    if _outline_tree(outline_text) != _expected_tree(
        page_text, role_groups, skill_categories
    ):
        raise AssertionError("The definitions page and generated catalogs drifted from the outline.")


class AgentAndSkillDefinitionsOutlineTests(unittest.TestCase):
    """Protect the durable definitions-page outline and generated sibling order."""

    def setUp(self) -> None:
        """Load the maintained outline and its source-backed presentation catalogs."""
        self.outline_text = OUTLINE_PATH.read_text(encoding="utf-8")
        self.page_text = PAGE_PATH.read_text(encoding="utf-8")
        role_payload = yaml.safe_load(ROLE_GROUPS_PATH.read_text(encoding="utf-8"))
        skill_payload = yaml.safe_load(
            SKILL_CATEGORIES_PATH.read_text(encoding="utf-8")
        )
        self.role_groups = role_payload["groups"]
        self.skill_categories = skill_payload["categories"]

    def test_outline_matches_page_and_catalog_structure(self) -> None:
        """The page and its generated catalog inputs must match the durable tree."""
        _assert_conformance(
            self.outline_text,
            self.page_text,
            self.role_groups,
            self.skill_categories,
        )

    def test_generated_role_cards_and_hierarchy_follow_outline_group_order(self) -> None:
        """Both generated role views must preserve the outline's agent-group order."""
        expected_labels = [group["label"] for group in self.role_groups]
        role_data = _read_json_assignment(ROLE_DATA_PATH)
        self.assertEqual(
            expected_labels,
            [group["label"] for group in role_data["catalogGroups"]],
        )

        root = element_tree.parse(HIERARCHY_PATH).getroot()
        hierarchy_labels = [
            node.text
            for node in root.findall(f".//{{{SVG_NAMESPACE}}}text[@class='group']")
            if node.attrib.get("x") == "30"
        ]
        self.assertEqual(expected_labels, hierarchy_labels)

    def test_generated_skill_hierarchy_follows_outline_category_order(self) -> None:
        """The generated hierarchy must preserve the outline's skill-category order."""
        expected_labels = [
            category["id"].replace("-", " ").title()
            for category in self.skill_categories
            if category["id"] != "stack-and-domain"
        ]
        root = element_tree.parse(HIERARCHY_PATH).getroot()
        hierarchy_labels = [
            node.text
            for node in root.findall(f".//{{{SVG_NAMESPACE}}}text[@class='group']")
            if node.attrib.get("x") == "760"
        ]

        self.assertEqual(expected_labels, hierarchy_labels)

    def test_section_order_mutation_breaks_conformance(self) -> None:
        """Moving relationships after agent definitions must fail the contract."""
        relationships = self.page_text.index(
            '<section class="section" aria-labelledby="relationships-title">'
        )
        agents = self.page_text.index(
            '<section class="section" aria-labelledby="agent-definitions-title">'
        )
        self.assertLess(relationships, agents)
        relationship_match = re.search(
            r'  <section class="section" aria-labelledby="relationships-title">'
            r".*?  </section>\n",
            self.page_text,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(relationship_match)
        relationship_section = relationship_match.group(0)
        without_relationships = self.page_text.replace(relationship_section, "", 1)
        agent_match = re.search(
            r'  <section class="section" aria-labelledby="agent-definitions-title">'
            r".*?  </section>\n",
            without_relationships,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(agent_match)
        mutant = (
            without_relationships[: agent_match.end()]
            + relationship_section
            + without_relationships[agent_match.end() :]
        )
        with self.assertRaisesRegex(AssertionError, "drifted"):
            _assert_conformance(
                self.outline_text,
                mutant,
                self.role_groups,
                self.skill_categories,
            )

    def test_catalog_order_mutation_breaks_conformance(self) -> None:
        """Moving Backlog Management before Dev Activities must fail the contract."""
        self.assertEqual(
            ["dev-activities", "backlog-management"],
            [group["id"] for group in self.role_groups[:2]],
        )
        mutant = [self.role_groups[1], self.role_groups[0], *self.role_groups[2:]]
        with self.assertRaisesRegex(AssertionError, "drifted"):
            _assert_conformance(
                self.outline_text,
                self.page_text,
                mutant,
                self.skill_categories,
            )


if __name__ == "__main__":
    unittest.main()
