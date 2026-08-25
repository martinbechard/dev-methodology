#!/usr/bin/env python3
"""Capture and render the repository-private Codex runtime tool catalog."""

# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Generated with AI assistance.
# Responsibility: Select, snapshot, validate, and render supported runtime tool definitions.

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any


# These paths keep snapshot ownership and generated output inside this skill.
SKILL_ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_PATH = SKILL_ROOT / "references" / "tool-definitions.json"
OUTPUT_ROOT = SKILL_ROOT / "references" / "tools"

# The schema identifier prevents an unrelated JSON document from being accepted.
SCHEMA = "dev-methodology-runtime-tool-definitions"

# Group identifiers are both approved directory names and stable catalog sections.
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

# This is the single allowlist for namespaced live tools. New connector
# namespaces must not become Agent design inputs merely by appearing in ALL_TOOLS.
NAMESPACED_TOOL_GROUPS = (
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


def parse_args() -> argparse.Namespace:
    """Parse the mutually exclusive capture and freshness-check modes.

    Returns:
        The parsed command arguments from the current process.

    Raises:
        SystemExit: Argparse exits for invalid arguments or help output.
    """

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
    """Return whether a live registry name belongs to an approved tool surface.

    Args:
        name: The exact name supplied by the live ALL_TOOLS registry.

    Returns:
        True for unnamespaced generic controls or a name matched by the single
        namespaced-tool allowlist; otherwise False.
    """

    if "__" not in name:
        return True
    return any(name.startswith(prefix) for prefix, _ in NAMESPACED_TOOL_GROUPS)


def group_for(name: str) -> str:
    """Map an included tool name to its stable documentation group.

    Args:
        name: An unnamespaced generic tool or an allowlisted namespaced tool.

    Returns:
        The stable group identifier used as the generated subfolder name.

    Raises:
        ValueError: The caller supplied a namespaced tool outside the allowlist.
    """

    if "__" not in name:
        return "generic-local"
    for prefix, group in NAMESPACED_TOOL_GROUPS:
        if name.startswith(prefix):
            return group
    raise ValueError(f"unsupported namespaced tool: {name}")


def validate_snapshot(loaded: object, path: Path) -> dict[str, Any]:
    """Validate and return one parsed snapshot.

    Args:
        loaded: Parsed JSON content to validate without mutation.
        path: The source path to identify in validation errors.

    Returns:
        The same dictionary after its schema and tool records are validated.

    Raises:
        ValueError: The schema, date, group, or a tool record is invalid.

    Validation performs no file-system writes. Restricting groups to the known
    identifiers also prevents output paths from escaping the catalog root.
    """

    if (
        not isinstance(loaded, dict)
        or loaded.get("schema") != SCHEMA
        or loaded.get("version") != 1
    ):
        raise ValueError(f"unsupported tool snapshot: {path}")
    for field in ("harness", "observedDate"):
        if not isinstance(loaded.get(field), str) or not loaded[field].strip():
            raise ValueError(f"snapshot field {field} must be non-empty: {path}")
    try:
        dt.date.fromisoformat(loaded["observedDate"])
    except ValueError as error:
        raise ValueError(
            f"snapshot observedDate must be an ISO date: {path}"
        ) from error
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
        if tool["group"] not in GROUP_TITLES:
            raise ValueError(f"unsupported tool group: {tool['group']}")
        if tool["name"] in names:
            raise ValueError(f"duplicate tool name: {tool['name']}")
        names.add(tool["name"])
    return loaded


def load_snapshot(path: Path = SNAPSHOT_PATH) -> dict[str, Any]:
    """Read and validate a snapshot from disk without mutating it.

    Args:
        path: Snapshot path; defaults to the skill's canonical JSON snapshot.

    Returns:
        The validated snapshot dictionary.

    Raises:
        OSError: The snapshot cannot be read.
        json.JSONDecodeError: The snapshot is not valid JSON.
        ValueError: The decoded snapshot violates the catalog schema.
    """

    return validate_snapshot(json.loads(path.read_text(encoding="utf-8")), path)


def atomic_write(path: Path, content: str) -> None:
    """Atomically replace a UTF-8 text file after writing it beside the target.

    Args:
        path: Destination whose parent directory may be created.
        content: Complete text to encode as UTF-8.

    Side effects:
        Creates parent directories and replaces the destination on success.

    Raises:
        OSError: Directory creation, writing, syncing, or replacement fails.
    """

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", dir=path.parent
    )
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
    """Replace live nested entries while preserving reviewed direct tools.

    Args:
        live_tools: The complete parsed ALL_TOOLS JSON array. Each entry must
            provide a non-empty string name and description.

    Returns:
        The validated snapshot written to the canonical snapshot path.

    Side effects:
        Atomically replaces the canonical snapshot after candidate validation.

    Raises:
        ValueError: The live registry or resulting snapshot is invalid.
        OSError: The existing snapshot cannot be read or replaced.

    Reviewed runtime-direct records are preserved because they are not exposed
    through ALL_TOOLS.
    """

    if not isinstance(live_tools, list):
        raise ValueError("capture input must be a JSON array")
    current = load_snapshot()
    direct = [
        tool for tool in current["tools"] if tool.get("source") == "runtime-direct"
    ]
    nested: list[dict[str, str]] = []
    for value in live_tools:
        if not isinstance(value, dict):
            raise ValueError("each live tool must be an object")
        name = value.get("name")
        description = value.get("description")
        if (
            not isinstance(name, str)
            or not name.strip()
            or not isinstance(description, str)
            or not description.strip()
        ):
            raise ValueError(
                "each live tool needs non-empty string name and description"
            )
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
    validate_snapshot(current, SNAPSHOT_PATH)
    loadable = json.dumps(current, indent=2, sort_keys=False) + "\n"
    atomic_write(SNAPSHOT_PATH, loadable)
    return current


def filename_for(name: str) -> str:
    """Convert a tool name to a portable Markdown filename.

    Args:
        name: Exact runtime tool name.

    Returns:
        A lowercase hyphenated filename ending in .md.

    Raises:
        ValueError: The name contains no ASCII letter or digit.
    """

    value = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if not value:
        raise ValueError(f"tool name has no filename characters: {name!r}")
    return f"{value}.md"


def tool_markdown(tool: dict[str, str], observed_date: str) -> str:
    """Render the generated Markdown page for one validated tool record.

    Args:
        tool: A validated tool record from the canonical snapshot.
        observed_date: ISO date when the runtime definition was observed.

    Returns:
        Complete Markdown for the tool's generated page.
    """

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


def index_markdown(
    snapshot: dict[str, Any], groups: dict[str, list[dict[str, str]]]
) -> str:
    """Render the sole catalog index with direct links to every tool page.

    Args:
        snapshot: Validated snapshot supplying harness and observation metadata.
        groups: Deterministically ordered groups whose tools are name-sorted.

    Returns:
        Complete Markdown for the catalog's single index.
    """

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
            "This catalog is harness evidence. It does not grant tool "
            "authorization or inject definitions into Agent prompts.",
            "",
        ]
    )
    return "\n".join(lines)


def expected_files(snapshot: dict[str, Any]) -> dict[Path, str]:
    """Build the complete deterministic generated-file map for a snapshot.

    Args:
        snapshot: A validated tool snapshot.

    Returns:
        Relative output paths mapped to their complete generated Markdown.

    Raises:
        ValueError: Two tool names normalize to the same output path.
    """

    groups: dict[str, list[dict[str, str]]] = {}
    filenames: set[Path] = set()
    for tool in snapshot["tools"]:
        groups.setdefault(tool["group"], []).append(tool)
    groups = dict(sorted(groups.items()))
    for tools in groups.values():
        tools.sort(key=lambda tool: tool["name"])
    expected = {Path("index.md"): index_markdown(snapshot, groups)}
    for group, tools in groups.items():
        for tool in tools:
            path = Path(group) / filename_for(tool["name"])
            if path in filenames:
                raise ValueError(f"tool filenames collide at {path}")
            filenames.add(path)
            expected[path] = tool_markdown(tool, snapshot["observedDate"])
    return expected


def render(snapshot: dict[str, Any], check: bool = False) -> None:
    """Write generated pages or fail when checked-in pages are stale.

    Args:
        snapshot: A validated snapshot to render.
        check: When True, compare without writing; otherwise synchronize output.

    Side effects:
        Write mode replaces expected Markdown, removes obsolete Markdown, and
        removes empty immediate group directories. Check mode is read-only.

    Raises:
        ValueError: Check mode finds missing, extra, or changed pages, or output
            filenames collide.
        OSError: Generated output cannot be read, written, or removed.
    """

    expected = expected_files(snapshot)
    existing = (
        {
            path.relative_to(OUTPUT_ROOT): path.read_text(encoding="utf-8")
            for path in OUTPUT_ROOT.rglob("*.md")
        }
        if OUTPUT_ROOT.is_dir()
        else {}
    )
    if check:
        missing = sorted(set(expected) - set(existing), key=str)
        extra = sorted(set(existing) - set(expected), key=str)
        changed = sorted(
            (
                path
                for path in set(expected) & set(existing)
                if expected[path] != existing[path]
            ),
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
    """Run capture or snapshot rendering and report the resulting catalog size.

    Returns:
        Zero after the requested capture, render, or freshness check succeeds.

    Side effects:
        Reads command arguments and snapshot files, may synchronize generated
        output, and prints one catalog summary line.
    """

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
