# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies the offline explorer shell, filtering contract, and keyboard navigation helpers.

from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE_PATH = ROOT / "design" / "agent-skill-explorer.html"
SCRIPT_PATH = ROOT / "design" / "agent-skill-explorer.js"
DATA_PATH = ROOT / "design" / "generated" / "agent-skill-explorer-data.js"


class AgentSkillExplorerTests(unittest.TestCase):
    """Protect the explorer's offline, data-driven, and keyboard-accessible behavior."""

    def test_page_is_offline_and_exposes_the_complete_filter_surface(self) -> None:
        """The static shell must load local data and label every required filter."""
        page = PAGE_PATH.read_text(encoding="utf-8")

        self.assertNotIn("https://", page)
        self.assertNotIn("http://", page)
        self.assertIn('src="generated/agent-skill-explorer-data.js"', page)
        self.assertIn('src="agent-skill-explorer.js"', page)
        self.assertIn('id="relationship-map"', page)
        self.assertIn('aria-live="polite"', page)
        self.assertIn('id="evidence-list"', page)
        script = SCRIPT_PATH.read_text(encoding="utf-8")
        self.assertIn("data.evidence", script)
        self.assertIn("receiptPaths", script)
        for filter_id in (
            "agent",
            "category",
            "technology",
            "capability",
            "folder-scope",
            "harness",
            "model-profile",
            "loading-mode",
            "declaration-status",
            "verified-behavior",
        ):
            self.assertIn(f'id="filter-{filter_id}"', page)

    def test_filtering_and_keyboard_helpers_cover_representative_paths(self) -> None:
        """Pure browser helpers must preserve relationships and deterministic focus movement."""
        fixture = {
            "roles": [
                {
                    "id": "dev-coder",
                    "modelProfile": "advanced",
                    "dynamicFolderSkills": True,
                    "generatedAdapters": [{"harness": "codex"}],
                    "coverage": {"executableCases": ["case-a"], "verifiedCases": []},
                },
                {
                    "id": "wiki-writer",
                    "modelProfile": "default",
                    "dynamicFolderSkills": False,
                    "generatedAdapters": [{"harness": "claude"}],
                    "coverage": {"executableCases": [], "verifiedCases": []},
                },
            ],
            "skills": [
                {
                    "id": "typescript",
                    "category": "stack-and-domain",
                    "kind": "technology",
                    "capabilities": ["typed-javascript"],
                    "coverage": {"executableCases": ["case-a"], "verifiedCases": []},
                },
                {
                    "id": "careful-coding",
                    "category": "development-practice",
                    "kind": "core",
                    "capabilities": [],
                    "coverage": {"executableCases": [], "verifiedCases": ["case-b"]},
                },
            ],
            "edges": [
                {"role": "dev-coder", "skill": "typescript", "kind": "detected-folder"},
                {"role": "dev-coder", "skill": "careful-coding", "kind": "fixed"},
            ],
            "loadingModes": [
                {"id": "codex-folder", "harness": "codex", "mode": "instruction-driven", "edgeKinds": ["detected-folder"]},
                {"id": "core-inline", "harness": "all", "mode": "static-inline", "edgeKinds": ["fixed"]}
            ],
        }
        node_program = f"""
const explorer = require({json.dumps(str(SCRIPT_PATH))});
const data = {json.dumps(fixture)};
const byAgent = explorer.filterGraph(data, {{agent: 'dev-coder'}});
const byTechnology = explorer.filterGraph(data, {{technology: 'typescript'}});
const byCapability = explorer.filterGraph(data, {{capability: 'typed-javascript'}});
const byLoading = explorer.filterGraph(data, {{loadingMode: 'instruction-driven'}});
const byInline = explorer.filterGraph(data, {{loadingMode: 'static-inline'}});
const verified = explorer.filterGraph(data, {{verifiedBehavior: 'verified'}});
process.stdout.write(JSON.stringify({{
  byAgent: [byAgent.roles.map(x => x.id), byAgent.skills.map(x => x.id), byAgent.edges.length],
  byTechnology: [byTechnology.roles.map(x => x.id), byTechnology.skills.map(x => x.id)],
  byCapability: byCapability.skills.map(x => x.id),
  byLoading: byLoading.roles.map(x => x.id),
  byLoadingSkills: byLoading.skills.map(x => x.id),
  byInlineSkills: byInline.skills.map(x => x.id),
  verified: verified.skills.map(x => x.id),
  keys: [
    explorer.nextIndex(0, 'ArrowRight', 5, 2),
    explorer.nextIndex(2, 'ArrowUp', 5, 2),
    explorer.nextIndex(3, 'Home', 5, 2),
    explorer.nextIndex(1, 'End', 5, 2)
  ]
}}));
"""
        result = subprocess.run(
            ["node", "-e", node_program],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        actual = json.loads(result.stdout)
        self.assertEqual(
            [["dev-coder"], ["careful-coding", "typescript"], 2], actual["byAgent"]
        )
        self.assertEqual([["dev-coder"], ["typescript"]], actual["byTechnology"])
        self.assertEqual(["typescript"], actual["byCapability"])
        self.assertEqual(["dev-coder"], actual["byLoading"])
        self.assertEqual(["typescript"], actual["byLoadingSkills"])
        self.assertEqual(["careful-coding"], actual["byInlineSkills"])
        self.assertEqual(["careful-coding"], actual["verified"])
        self.assertEqual([1, 0, 0, 4], actual["keys"])

    def test_text_states_and_component_boundaries_meet_contrast_targets(self) -> None:
        """Every evidence color and the shared boundary token must remain perceivable."""
        page = PAGE_PATH.read_text(encoding="utf-8")
        colors = dict(re.findall(r"--([a-z-]+):\s*(#[0-9a-fA-F]{6});", page))

        def luminance(value: str) -> float:
            channels = [int(value[index : index + 2], 16) / 255 for index in (1, 3, 5)]
            linear = [
                channel / 12.92
                if channel <= 0.04045
                else ((channel + 0.055) / 1.055) ** 2.4
                for channel in channels
            ]
            return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

        def contrast(first: str, second: str) -> float:
            lighter, darker = sorted(
                (luminance(first), luminance(second)), reverse=True
            )
            return (lighter + 0.05) / (darker + 0.05)

        for token in ("ink", "muted", "amber", "cyan", "magenta", "green", "red"):
            with self.subTest(token=token):
                self.assertGreaterEqual(contrast(colors[token], colors["panel"]), 4.5)
        self.assertGreaterEqual(contrast(colors["line"], colors["panel-raised"]), 3.0)

    def test_generated_nodes_edges_and_links_resolve_to_canonical_sources(self) -> None:
        """Every displayed relationship and link must resolve inside the repository."""
        source = DATA_PATH.read_text(encoding="utf-8")
        match = re.search(r"= (\{.*\});\s*$", source, re.DOTALL)
        self.assertIsNotNone(match)
        payload = json.loads(match.group(1))
        role_ids = {item["id"] for item in payload["roles"]}
        skill_ids = {item["id"] for item in payload["skills"]}

        self.assertEqual(
            {"conditional", "detected-folder", "fixed"},
            {item["kind"] for item in payload["edges"]},
        )
        self.assertTrue({"typescript", "spring-boot", "python", "fastapi"} <= skill_ids)
        for edge in payload["edges"]:
            self.assertIn(edge["role"], role_ids)
            self.assertIn(edge["skill"], skill_ids)
        paths = []
        for role in payload["roles"]:
            paths.append(role["sourcePath"])
            paths.extend(item["path"] for item in role["generatedAdapters"])
        for skill in payload["skills"]:
            paths.extend(
                path for path in (skill["sourcePath"], skill["detectionPath"]) if path
            )
        for record in payload["evidence"]:
            paths.append(record["sourcePath"])
            paths.extend(record["receiptPaths"])
        for path in paths:
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file(), path)


if __name__ == "__main__":
    unittest.main()
