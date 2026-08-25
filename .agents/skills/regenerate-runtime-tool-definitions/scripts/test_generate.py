#!/usr/bin/env python3
"""Focused tests for runtime tool catalog generation."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("generate.py")
SPEC = importlib.util.spec_from_file_location("runtime_tool_catalog_generator", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
generator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = generator
SPEC.loader.exec_module(generator)


class RuntimeToolCatalogGeneratorTests(unittest.TestCase):
    def test_selection_excludes_connected_and_project_specific_families(self) -> None:
        for name in (
            "mcp__codex_apps__vercel_list_projects",
            "mcp__codex_apps__github_search",
            "mcp__greptile__list_pull_requests",
            "mcp__mcp_agent_report__generate_report",
            "mcp__mcp_agent_ops__skill_list",
        ):
            self.assertFalse(generator.include_nested_tool(name), name)
        self.assertTrue(generator.include_nested_tool("exec_command"))
        self.assertTrue(generator.include_nested_tool("codex_app__read_thread"))
        self.assertTrue(
            generator.include_nested_tool(
                "mcp__codex_apps__codex_document_control_list_document_sessions"
            )
        )

    def test_snapshot_generates_one_file_per_tool_and_one_index(self) -> None:
        snapshot = generator.load_snapshot()
        expected = generator.expected_files(snapshot)
        tool_count = len(snapshot["tools"])
        self.assertEqual(1 + tool_count, len(expected))
        self.assertIn(Path("index.md"), expected)
        self.assertIn(Path("collaboration") / "spawn-agent.md", expected)
        self.assertEqual(
            [Path("index.md")],
            sorted(path for path in expected if path.name == "index.md"),
        )
        self.assertIn(
            "[spawn_agent](collaboration/spawn-agent.md)",
            expected[Path("index.md")],
        )

    def test_checked_in_catalog_matches_snapshot(self) -> None:
        generator.render(generator.load_snapshot(), check=True)


if __name__ == "__main__":
    unittest.main()
