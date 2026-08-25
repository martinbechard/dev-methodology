#!/usr/bin/env python3
"""Capture and render the repository-private Codex runtime tool catalog."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_PATH = SKILL_ROOT / "references" / "tool-definitions.json"
OUTPUT_ROOT = SKILL_ROOT / "references" / "tools"
SCHEMA = "dev-methodology-runtime-tool-definitions"
GROUP_TITLES = {
    "generic-local": "Generic Local and Control Tools",
    "codex-task-control": "Codex Task and Application Control",
    "codex-document-control": "Codex Document Control",
    "codex-plugin-management": "Codex Plugin Management",
    "codex-safety": "Codex Safety and Support",
    "openai-platform": "OpenAI Platform Setup",
    "openai-documentation": "Official OpenAI Documentation",
    "javascript-runtime": "Persistent JavaScript Runtime",
    "media": "Media Generation",
    "web": "Web Access",
    "collaboration": "Agent Collaboration",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--capture-file",
        type=Path,
        help="Read the complete live ALL_TOOLS JSON array from one disposable file.",
    )
    mode.add_argument(
        "--check",
        action="store_true",
        help="Fail when generated Markdown differs from the snapshot.",
    )
    return parser.parse_args()


def include_nested_tool(name: str) -> bool:
    """Select Codex-native and generic nested tools from the live registry."""
    if name.startswith(("mcp__mcp_agent_ops__", "mcp__mcp_agent_report__", "mcp__greptile__")):
        return False
    if not name.startswith("mcp__codex_apps__"):
        return True
    return name.startswith(
        (
            "mcp__codex_apps__codex_document_control_",
            "mcp__codex_apps__plugin_management_",
            "mcp__codex_apps__safety_settings_",
            "mcp__codex_apps__openai_platform_",
            "mcp__codex_apps__hotline_",
        )
    )


def group_for(name: str) -> str:
    if "__" not in name:
        return "generic-local"
    prefixes = (
        ("codex_app__", "codex-task-control"),
        ("mcp__codex_apps__codex_document_control_", "codex-document-control"),
        ("mcp__codex_apps__plugin_management_", "codex-plugin-management"),
        ("plugin_management__", "codex-plugin-management"),
        ("mcp__codex_apps__safety_settings_", "codex-safety"),
        ("mcp__codex_apps__hotline_", "codex-safety"),
        ("mcp__codex_apps__openai_platform_", "openai-platform"),
        ("mcp__openai_api_key_local_confirmation__", "openai-platform"),
        ("mcp__openaiDeveloperDocs__", "openai-documentation"),
        ("mcp__node_repl__", "javascript-runtime"),
        ("image_gen__", "media"),
        ("web__", "web"),
    )
    for prefix, group in prefixes:
        if name.startswith(prefix):
            return group
    return "generic-local"


def load_snapshot(path: Path = SNAPSHOT_PATH) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict) or loaded.get("schema") != SCHEMA or loaded.get("version") != 1:
        raise ValueError(f"unsupported tool snapshot: {path}")
    tools = loaded.get("tools")
    if not isinstance(tools, list):
        raise ValueError(f"snapshot tools must be an array: {path}")
    names: set[str] = set()
    for tool in tools:
        if not isinstance(tool, dict):
            raise ValueError("every snapshot tool must be an object")
        for field in ("name", "group", "surface", "source", "description"):
            if not isinstance(tool.get(field), str) or not tool[field].strip():
                raise ValueError(f"tool field {field} must be non-empty")
        if tool["name"] in names:
            raise ValueError(f"duplicate tool name: {tool['name']}")
        names.add(tool["name"])
    return loaded


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def capture_snapshot(live_tools: object) -> dict[str, Any]:
    if not isinstance(live_tools, list):
        raise ValueError("capture input must be a JSON array")
    current = load_snapshot()
    direct = [tool for tool in current["tools"] if tool.get("source") == "runtime-direct"]
    nested: list[dict[str, str]] = []
    for value in live_tools:
        if not isinstance(value, dict):
            raise ValueError("each live tool must be an object")
        name = value.get("name")
        description = value.get("description")
        if not isinstance(name, str) or not isinstance(description, str):
            raise ValueError("each live tool needs string name and description")
        if include_nested_tool(name):
            nested.append(
                {
                    "name": name,
                    "group": group_for(name),
                    "surface": "nested",
                    "source": "ALL_TOOLS",
                    "description": description,
                }
            )
    current["observedDate"] = dt.date.today().isoformat()
    current["tools"] = sorted(
        [*nested, *direct], key=lambda tool: (tool["group"], tool["name"])
    )
    loadable = json.dumps(current, indent=2, sort_keys=False) + "\n"
    atomic_write(SNAPSHOT_PATH, loadable)
    return load_snapshot()


def filename_for(name: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if not value:
        raise ValueError(f"tool name has no filename characters: {name!r}")
    return f"{value}.md"


def tool_markdown(tool: dict[str, str], observed_date: str) -> str:
    title = tool["name"]
    return (
        "<!-- Generated by scripts/generate.py; do not edit directly. -->\n"
        f"# {title}\n\n"
        f"Group: {GROUP_TITLES.get(tool['group'], tool['group'])}\n\n"
        f"Surface: {tool['surface']}\n\n"
        f"Source: {tool['source']}\n\n"
        f"Observed: {observed_date}\n\n"
        "## Definition\n\n"
        f"{tool['description'].rstrip()}\n"
    )


def index_markdown(snapshot: dict[str, Any], groups: dict[str, list[dict[str, str]]]) -> str:
    lines = [
        "<!-- Generated by scripts/generate.py; do not edit directly. -->",
        "# Codex and Generic Runtime Tools",
        "",
        f"Harness: {snapshot['harness']}",
        "",
        f"Observed: {snapshot['observedDate']}",
        "",
        f"Tools: {sum(len(values) for values in groups.values())}",
        "",
        f"Groups: {len(groups)}",
        "",
    ]
    for group, tools in groups.items():
        title = GROUP_TITLES.get(group, group)
        lines.extend(
            [
                f"## {title}",
                "",
                f"Tools: {len(tools)}",
                "",
            ]
        )
        lines.extend(
            f"- [{tool['name']}]({group}/{filename_for(tool['name'])})"
            for tool in tools
        )
        lines.append("")
    lines.extend(
        [
            "This catalog is harness evidence. It does not grant tool authorization or inject definitions into Agent prompts.",
            "",
        ]
    )
    return "\n".join(lines)

def expected_files(snapshot: dict[str, Any]) -> dict[Path, str]:
    groups: dict[str, list[dict[str, str]]] = {}
    filenames: set[Path] = set()
    for tool in snapshot["tools"]:
        groups.setdefault(tool["group"], []).append(tool)
    groups = dict(sorted(groups.items()))
    expected = {Path("index.md"): index_markdown(snapshot, groups)}
    for group, tools in groups.items():
        tools.sort(key=lambda tool: tool["name"])
        for tool in tools:
            path = Path(group) / filename_for(tool["name"])
            if path in filenames:
                raise ValueError(f"tool filenames collide at {path}")
            filenames.add(path)
            expected[path] = tool_markdown(tool, snapshot["observedDate"])
    return expected


def render(snapshot: dict[str, Any], check: bool = False) -> None:
    expected = expected_files(snapshot)
    existing = {
        path.relative_to(OUTPUT_ROOT): path.read_text(encoding="utf-8")
        for path in OUTPUT_ROOT.rglob("*.md")
    } if OUTPUT_ROOT.is_dir() else {}
    if check:
        missing = sorted(set(expected) - set(existing), key=str)
        extra = sorted(set(existing) - set(expected), key=str)
        changed = sorted(
            (path for path in set(expected) & set(existing) if expected[path] != existing[path]),
            key=str,
        )
        if missing or extra or changed:
            raise ValueError(
                f"generated catalog is stale: missing={missing}, extra={extra}, changed={changed}"
            )
        return
    for path in OUTPUT_ROOT.rglob("*.md") if OUTPUT_ROOT.is_dir() else ():
        if path.relative_to(OUTPUT_ROOT) not in expected:
            path.unlink()
    for relative, content in expected.items():
        atomic_write(OUTPUT_ROOT / relative, content)
    for directory in sorted(OUTPUT_ROOT.glob("*")):
        if directory.is_dir() and not any(directory.iterdir()):
            directory.rmdir()


def main() -> int:
    arguments = parse_args()
    if arguments.capture_file:
        snapshot = capture_snapshot(
            json.loads(arguments.capture_file.read_text(encoding="utf-8"))
        )
    else:
        snapshot = load_snapshot()
    render(snapshot, check=arguments.check)
    print(
        f"{snapshot['harness']} catalog: {len(snapshot['tools'])} tools, "
        f"{len({tool['group'] for tool in snapshot['tools']})} groups, "
        f"observed {snapshot['observedDate']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
