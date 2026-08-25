#!/usr/bin/env python3
"""Focused tests for runtime tool catalog generation."""

# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Responsibility: Verify runtime tool selection, validation, and deterministic rendering.

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


# Load the sibling script as a module without making the maintenance skill a package.
MODULE_PATH = Path(__file__).with_name("generate.py")
SPEC = importlib.util.spec_from_file_location(
    "runtime_tool_catalog_generator", MODULE_PATH
)
assert SPEC is not None and SPEC.loader is not None
generator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = generator
SPEC.loader.exec_module(generator)


class RuntimeToolCatalogGeneratorTests(unittest.TestCase):
    """Exercise the generator's selection and generated-file contracts."""

    def test_selection_excludes_connected_and_project_specific_families(self) -> None:
        """Reject known and previously unseen connector namespaces."""

        for name in (
            "mcp__codex_apps__vercel_list_projects",
            "mcp__codex_apps__github_search",
            "mcp__greptile__list_pull_requests",
            "mcp__mcp_agent_report__generate_report",
            "mcp__mcp_agent_ops__skill_list",
            "mcp__future_connector__arbitrary_tool",
            "future_plugin__arbitrary_tool",
        ):
            self.assertFalse(generator.include_nested_tool(name), name)

    def test_selection_includes_each_approved_runtime_family(self) -> None:
        """Accept generic controls and every explicitly approved namespace."""

        for name in (
            "exec_command",
            "codex_app__read_thread",
            "mcp__codex_apps__codex_document_control_list_document_sessions",
            "mcp__codex_apps__plugin_management_get_app_permissions",
            "plugin_management__uninstall_plugin",
            "mcp__codex_apps__safety_settings_get_family_info",
            "mcp__codex_apps__hotline_get_local_hotline",
            "mcp__codex_apps__openai_platform_list_openai_api_key_targets",
            "mcp__openai_api_key_local_confirmation__confirm_openai_api_key",
            "mcp__openaiDeveloperDocs__search_openai_docs",
            "mcp__node_repl__js",
            "image_gen__imagegen",
            "web__run",
        ):
            self.assertTrue(generator.include_nested_tool(name), name)

    def test_snapshot_generates_one_file_per_tool_and_one_index(self) -> None:
        """Generate one root index and exactly one page for every tool."""

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

    def test_index_sorts_tools_independently_of_snapshot_order(self) -> None:
        """Keep index links deterministic when snapshot records are unordered."""

        snapshot = generator.load_snapshot()
        snapshot["tools"] = list(reversed(snapshot["tools"]))
        index = generator.expected_files(snapshot)[Path("index.md")]
        apply_patch = index.index("[apply_patch]")
        create_goal = index.index("[create_goal]")
        self.assertLess(apply_patch, create_goal)

    def test_snapshot_validation_rejects_duplicate_tool_names(self) -> None:
        """Reject duplicate records before capture can replace the snapshot."""

        snapshot = generator.load_snapshot()
        snapshot["tools"].append(dict(snapshot["tools"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate tool name"):
            generator.validate_snapshot(snapshot, generator.SNAPSHOT_PATH)

    def test_snapshot_validation_rejects_unknown_groups(self) -> None:
        """Reject group names that could escape or fragment the output tree."""

        snapshot = generator.load_snapshot()
        snapshot["tools"][0]["group"] = "../../outside"
        with self.assertRaisesRegex(ValueError, "unsupported tool group"):
            generator.validate_snapshot(snapshot, generator.SNAPSHOT_PATH)

    def test_checked_in_catalog_matches_snapshot(self) -> None:
        """Keep checked-in Markdown byte-for-byte aligned with the snapshot."""

        generator.render(generator.load_snapshot(), check=True)


if __name__ == "__main__":
    unittest.main()
