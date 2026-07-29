# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Summary: Verifies the offline explorer shell, filtering contract, and keyboard navigation helpers.

from __future__ import annotations

import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE_PATH = ROOT / "design" / "agent-skill-explorer.html"
SCRIPT_PATH = ROOT / "design" / "agent-skill-explorer.js"
DATA_PATH = ROOT / "design" / "generated" / "agent-skill-explorer-data.js"
NODE_PATH = shutil.which("node")


class AgentSkillExplorerTests(unittest.TestCase):
    """Protect the explorer's offline, data-driven, and keyboard-accessible behavior."""

    def test_page_is_offline_and_exposes_the_complete_filter_surface(self) -> None:
        """The static shell must load local data and label every required filter."""
        page = PAGE_PATH.read_text(encoding="utf-8")

        self.assertNotIn("https://", page)
        self.assertNotIn("http://", page)
        self.assertIn('class="site-header"', page)
        self.assertIn(
            '<a class="site-brand" href="../index.html">',
            page,
        )
        self.assertIn("<span>AI-Assisted Coding Toolkit Index</span>", page)
        self.assertNotIn("Back to Documentation Index", page)
        self.assertIn(
            'href="agent-and-skill-definitions.html">Back to Core Agent and Skills</a>',
            page,
        )
        self.assertIn('src="documentation-settings.js"', page)
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

    @unittest.skipUnless(NODE_PATH, "Node is unavailable for pure JavaScript checks")
    def test_filtering_routes_status_and_keyboard_helpers_cover_representative_paths(self) -> None:
        """Pure helpers must preserve harness routes, graph scope, status, and focus state."""
        fixture = {
            "roles": [
                {
                    "id": "dev-coder",
                    "modelProfile": "advanced",
                    "dynamicFolderSkills": True,
                    "generatedAdapters": [
                        {"harness": harness}
                        for harness in ("claude", "codex", "gemini", "junie")
                    ],
                    "skillAvailability": [
                        {"name": "typescript", "enabled": False}
                    ],
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
                {"id": "core-inline", "harness": "all", "mode": "static-inline", "status": "declared", "sourcePath": "scripts/build.py", "edgeKinds": ["fixed"]},
                {"id": "claude-preload", "harness": "claude", "mode": "native-preload", "status": "declared", "sourcePath": "scripts/build.py", "edgeKinds": ["fixed"]},
                {"id": "claude-folder", "harness": "claude", "mode": "skill-tool", "status": "declared", "sourcePath": "agents/schema.yaml", "edgeKinds": ["detected-folder"]},
                {"id": "codex-folder", "harness": "codex", "mode": "instruction-driven", "status": "declared", "sourcePath": "agents/schema.yaml", "edgeKinds": ["detected-folder"]},
                {"id": "codex-availability", "harness": "codex", "mode": "availability-override", "status": "declared", "sourcePath": "agents/schema.yaml", "edgeKinds": []},
                {"id": "codex-app-server", "harness": "codex", "mode": "app-server-injection", "status": "missing", "sourcePath": "evals/cases.yaml", "edgeKinds": []},
            ],
        }
        node_program = f"""
const explorer = require({json.dumps(str(SCRIPT_PATH))});
const data = {json.dumps(fixture)};
const byAgent = explorer.filterGraph(data, {{agent: 'dev-coder'}});
const byTechnology = explorer.filterGraph(data, {{technology: 'typescript'}});
const byCapability = explorer.filterGraph(data, {{capability: 'typed-javascript'}});
const byDetectedFolder = explorer.filterGraph(data, {{folderScope: 'dynamic'}});
const byDefinition = explorer.filterGraph(data, {{folderScope: 'static'}});
const byCodex = explorer.filterGraph(data, {{harness: 'codex'}});
const byClaude = explorer.filterGraph(data, {{harness: 'claude'}});
const byGemini = explorer.filterGraph(data, {{harness: 'gemini'}});
const byJunie = explorer.filterGraph(data, {{harness: 'junie'}});
const byAvailability = explorer.filterGraph(data, {{harness: 'codex', loadingMode: 'availability-override'}});
const byAppServer = explorer.filterGraph(data, {{harness: 'codex', loadingMode: 'app-server-injection'}});
const disconnectedProfile = explorer.filterGraph(data, {{modelProfile: 'default'}});
const verified = explorer.filterGraph(data, {{verifiedBehavior: 'verified'}});
process.stdout.write(JSON.stringify({{
  byAgent: [byAgent.roles.map(x => x.id), byAgent.skills.map(x => x.id), byAgent.edges.length],
  byTechnology: [byTechnology.roles.map(x => x.id), byTechnology.skills.map(x => x.id)],
  byCapability: byCapability.skills.map(x => x.id),
  byDetectedFolder: [byDetectedFolder.roles.map(x => x.id), byDetectedFolder.skills.map(x => x.id), byDetectedFolder.edges.map(x => x.kind)],
  byDefinition: [byDefinition.roles.map(x => x.id), byDefinition.skills.map(x => x.id), byDefinition.edges.map(x => x.kind)],
  harnessKinds: [byCodex, byClaude, byGemini, byJunie].map(graph => graph.edges.map(x => x.kind).sort()),
  emptyEdgeModes: [byAvailability, byAppServer].map(graph => [graph.roles.length, graph.skills.length, graph.edges.length]),
  disconnectedProfile: [disconnectedProfile.roles.length, disconnectedProfile.skills.length, disconnectedProfile.edges.length],
  fixedClaudeRoutes: explorer.routesForNode(data, 'skill', 'careful-coding', {{harness: 'claude'}}).map(x => x.id),
  detectedClaudeRoutes: explorer.routesForNode(data, 'skill', 'typescript', {{harness: 'claude'}}).map(x => x.id),
  detectedCodexRoutes: explorer.routesForNode(data, 'skill', 'typescript', {{harness: 'codex'}}).map(x => x.id),
  availabilityAgentRoutes: explorer.routesForNode(data, 'agent', 'dev-coder', {{harness: 'codex', loadingMode: 'availability-override'}}).map(x => x.id),
  verified: verified.skills.map(x => x.id),
  staleWins: explorer.nodeStatus({{coverage: {{verifiedCases: ['case-b'], staleByDigestCases: ['case-a']}}}}),
  selection: [
    explorer.reconcileSelection('skill:typescript', ['agent:dev-coder', 'skill:typescript']),
    explorer.reconcileSelection('skill:typescript', ['agent:dev-coder'])
  ],
  keys: [
    explorer.nextIndex(0, 'ArrowRight', 5, 2),
    explorer.nextIndex(2, 'ArrowUp', 5, 2),
    explorer.nextIndex(3, 'Home', 5, 2),
    explorer.nextIndex(1, 'End', 5, 2)
  ]
}}));
"""
        result = subprocess.run(
            [NODE_PATH, "-e", node_program],
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
        self.assertEqual(
            [["dev-coder"], ["typescript"], ["detected-folder"]],
            actual["byDetectedFolder"],
        )
        self.assertEqual(
            [["dev-coder"], ["careful-coding"], ["fixed"]],
            actual["byDefinition"],
        )
        self.assertEqual(
            [
                ["detected-folder", "fixed"],
                ["detected-folder", "fixed"],
                ["fixed"],
                ["fixed"],
            ],
            actual["harnessKinds"],
        )
        self.assertEqual([[1, 2, 2], [1, 2, 2]], actual["emptyEdgeModes"])
        self.assertEqual([0, 0, 0], actual["disconnectedProfile"])
        self.assertEqual(["core-inline", "claude-preload"], actual["fixedClaudeRoutes"])
        self.assertEqual(["claude-folder"], actual["detectedClaudeRoutes"])
        self.assertEqual(["codex-folder"], actual["detectedCodexRoutes"])
        self.assertEqual(["codex-availability"], actual["availabilityAgentRoutes"])
        self.assertEqual(["careful-coding"], actual["verified"])
        self.assertEqual("blocked", actual["staleWins"])
        self.assertEqual(["skill:typescript", ""], actual["selection"])
        self.assertEqual([1, 0, 0, 4], actual["keys"])

    def test_interaction_contract_exposes_routes_overrides_and_roving_state(self) -> None:
        """Static assets must expose loading evidence, overrides, and accessible state."""
        page = PAGE_PATH.read_text(encoding="utf-8")
        script = SCRIPT_PATH.read_text(encoding="utf-8")

        self.assertIn("min-width: 75rem", page)
        self.assertIn(".map-node.status-missing rect", page)
        self.assertIn(".map-node.status-verified rect", page)
        self.assertIn("node-status", page + script)
        self.assertIn("skillAvailability", script)
        self.assertIn("sourcePath", script)
        self.assertIn('"aria-pressed"', script)
        self.assertIn('setAttribute("tabindex", "0")', script)
        self.assertIn("resolveHarness", script)
        self.assertIn("dev-methodology:documentation-settings-change", script)

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
