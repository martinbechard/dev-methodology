#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Synchronizes derived Codex skill interface metadata while preserving hand-authored policy and dependencies.

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

SUCCESS_EXIT_CODE = 0
ERROR_EXIT_CODE = 1
SKILL_FILE_NAME = "SKILL.md"
AGENTS_FOLDER_NAME = "agents"
OPENAI_METADATA_FILE_NAME = "openai.yaml"
FRONTMATTER_DELIMITER = "---"
MAX_SHORT_DESCRIPTION_LENGTH = 96
WORD_SEPARATOR_PATTERN = re.compile(r"[-_]+")
SENTENCE_END_PATTERN = re.compile(r"(?<=[.!?])\s+")
DERIVED_INTERFACE_KEYS = {"display_name", "short_description"}
INTERFACE_SECTION_KEY = "interface"
POLICY_SECTION_KEY = "policy"
DEPENDENCIES_SECTION_KEY = "dependencies"


def split_frontmatter(text: str) -> dict[str, object]:
    lines = text.splitlines()
    if not lines or lines[0] != FRONTMATTER_DELIMITER:
        raise ValueError("SKILL.md must start with YAML frontmatter")
    for index, line in enumerate(lines[1:], start=1):
        if line == FRONTMATTER_DELIMITER:
            parsed = yaml.safe_load("\n".join(lines[1:index]))
            if not isinstance(parsed, dict):
                raise ValueError("SKILL.md frontmatter must be a YAML object")
            return parsed
    raise ValueError("SKILL.md frontmatter delimiter is missing")


def load_skill_frontmatter(skill_directory: Path) -> dict[str, object]:
    skill_file = skill_directory / SKILL_FILE_NAME
    if not skill_file.is_file():
        raise FileNotFoundError(f"SKILL.md is missing: {skill_file}")
    return split_frontmatter(skill_file.read_text(encoding="utf-8"))


def display_name_from_skill_name(skill_name: str) -> str:
    """Convert a skill identifier to a UI label while preserving the JHipster brand spelling."""
    words = WORD_SEPARATOR_PATTERN.split(skill_name)
    return " ".join("JHipster" if word.lower() == "jhipster" else word.title() for word in words)


def short_description_from_skill_description(description: str) -> str:
    first_sentence = SENTENCE_END_PATTERN.split(description.strip(), maxsplit=1)[0].strip()
    if len(first_sentence) <= MAX_SHORT_DESCRIPTION_LENGTH:
        return first_sentence
    trimmed = first_sentence[: MAX_SHORT_DESCRIPTION_LENGTH + 1].rsplit(" ", maxsplit=1)[0]
    return trimmed.rstrip(".,;:") + "..."


def default_prompt_from_skill_name(skill_name: str) -> str:
    return f"Use ${skill_name} for work covered by this skill."


def load_existing_metadata(metadata_path: Path) -> dict[str, object]:
    if not metadata_path.is_file():
        return {}
    parsed = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
    if parsed is None:
        return {}
    if not isinstance(parsed, dict):
        raise ValueError(f"openai.yaml must be a YAML object: {metadata_path}")
    return parsed


def derived_interface(frontmatter: dict[str, object]) -> dict[str, str]:
    skill_name = frontmatter.get("name")
    description = frontmatter.get("description")
    if not isinstance(skill_name, str) or not skill_name.strip():
        raise ValueError("SKILL.md frontmatter name must be a non-empty string")
    if not isinstance(description, str) or not description.strip():
        raise ValueError("SKILL.md frontmatter description must be a non-empty string")
    normalized_name = skill_name.strip()
    return {
        "display_name": display_name_from_skill_name(normalized_name),
        "short_description": short_description_from_skill_description(description),
        "default_prompt": default_prompt_from_skill_name(normalized_name),
    }


def build_metadata(frontmatter: dict[str, object], existing: dict[str, object]) -> dict[str, object]:
    generated_interface = derived_interface(frontmatter)
    existing_interface = existing.get(INTERFACE_SECTION_KEY)
    if existing_interface is None:
        existing_interface = {}
    if not isinstance(existing_interface, dict):
        raise ValueError("openai.yaml interface must be a YAML object")
    merged_interface = {key: value for key, value in existing_interface.items() if key not in DERIVED_INTERFACE_KEYS}
    merged_interface.update({"display_name": generated_interface["display_name"], "short_description": generated_interface["short_description"]})
    if "default_prompt" not in merged_interface:
        merged_interface["default_prompt"] = generated_interface["default_prompt"]
    metadata: dict[str, object] = {INTERFACE_SECTION_KEY: merged_interface}
    for section_key in (POLICY_SECTION_KEY, DEPENDENCIES_SECTION_KEY):
        section_value = existing.get(section_key)
        if section_value is not None:
            metadata[section_key] = section_value
    return metadata


def yaml_scalar(value: object) -> str:
    dumped = yaml.safe_dump(value, allow_unicode=True, default_flow_style=True, sort_keys=False, width=4096).strip()
    return dumped.removesuffix("\n...")


def append_mapping(lines: list[str], mapping: dict[object, object], indent: int) -> None:
    for key, value in mapping.items():
        if isinstance(value, dict):
            lines.append(" " * indent + f"{key}:")
            append_mapping(lines, value, indent + 2)
        elif isinstance(value, list):
            lines.append(" " * indent + f"{key}:")
            dumped = yaml.safe_dump(value, allow_unicode=True, sort_keys=False).splitlines()
            lines.extend(" " * (indent + 2) + line for line in dumped)
        else:
            lines.append(" " * indent + f"{key}: {yaml_scalar(value)}")


def render_metadata(metadata: dict[str, object]) -> str:
    interface = metadata[INTERFACE_SECTION_KEY]
    if not isinstance(interface, dict):
        raise ValueError("metadata interface must be a YAML object")
    lines = [
        "# Codex app metadata for this skill.",
        "# Derived interface fields are refreshed from SKILL.md by scripts/openai_metadata.py.",
        "interface:",
        "  # User-facing name shown in Codex skill surfaces.",
        f"  display_name: {yaml_scalar(interface['display_name'])}",
        "  # User-facing summary shown in Codex skill surfaces.",
        f"  short_description: {yaml_scalar(interface['short_description'])}",
    ]
    for key, value in interface.items():
        if key in DERIVED_INTERFACE_KEYS:
            continue
        if key == "default_prompt":
            lines.append("  # Prompt Codex can use when launching this skill directly.")
        lines.append(f"  {key}: {yaml_scalar(value)}")
    policy = metadata.get(POLICY_SECTION_KEY)
    if policy is not None:
        if not isinstance(policy, dict):
            raise ValueError("metadata policy must be a YAML object")
        lines.extend(["", "# Invocation policy. Omit this section to use Codex defaults.", "policy:"])
        append_mapping(lines, policy, 2)
    else:
        lines.extend(["", "# Optional invocation policy placeholder.", "# policy:", "#   allow_implicit_invocation: false"])
    dependencies = metadata.get(DEPENDENCIES_SECTION_KEY)
    if dependencies is not None:
        if not isinstance(dependencies, dict):
            raise ValueError("metadata dependencies must be a YAML object")
        lines.extend(["", "# Tool dependencies Codex should install or wire for this skill.", "dependencies:"])
        append_mapping(lines, dependencies, 2)
    else:
        lines.extend(["", "# Optional tool dependency placeholder.", "# dependencies:", "#   tools: []"])
    return "\n".join(lines) + "\n"


def is_skill_directory(path: Path) -> bool:
    return path.is_dir() and (path / SKILL_FILE_NAME).is_file()


def skill_directories_from_path(path: Path) -> list[Path]:
    if path.name == SKILL_FILE_NAME:
        return [path.parent]
    if is_skill_directory(path):
        return [path]
    if path.is_dir():
        return sorted(child for child in path.iterdir() if is_skill_directory(child))
    raise FileNotFoundError(f"Skill path does not exist: {path}")


def sync_skill_metadata(skill_directory: Path, check: bool) -> bool:
    frontmatter = load_skill_frontmatter(skill_directory)
    metadata_path = skill_directory / AGENTS_FOLDER_NAME / OPENAI_METADATA_FILE_NAME
    existing = load_existing_metadata(metadata_path)
    rendered = render_metadata(build_metadata(frontmatter, existing))
    current = metadata_path.read_text(encoding="utf-8") if metadata_path.is_file() else None
    if current == rendered:
        return False
    if check:
        return True
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(rendered, encoding="utf-8")
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sync Codex openai.yaml metadata from SKILL.md files.")
    parser.add_argument("paths", nargs="+", help="Skill roots, skill directories, or SKILL.md files")
    parser.add_argument("--check", action="store_true", help="Report stale metadata without rewriting files.")
    args = parser.parse_args(argv)
    try:
        skill_directories = [skill_directory for path in args.paths for skill_directory in skill_directories_from_path(Path(path))]
        changed = [skill_directory for skill_directory in skill_directories if sync_skill_metadata(skill_directory, args.check)]
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return ERROR_EXIT_CODE
    if args.check and changed:
        for skill_directory in changed:
            print(f"stale {skill_directory}")
        return ERROR_EXIT_CODE
    for skill_directory in changed:
        print(f"synced {skill_directory}")
    if not changed:
        print("OpenAI metadata already in sync.")
    return SUCCESS_EXIT_CODE


if __name__ == "__main__":
    raise SystemExit(main())
