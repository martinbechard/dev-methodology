#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml


MAX_SKILL_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
SKILL_FILE_NAME = "SKILL.md"
FRONTMATTER_DELIMITER = "---"
ALLOWED_FRONTMATTER_KEYS = {
    "allowed-tools",
    "description",
    "license",
    "metadata",
    "name",
}
NAME_PATTERN = re.compile(r"^[a-z0-9-]+$")
SUCCESS_EXIT_CODE = 0
ERROR_EXIT_CODE = 1


@dataclass(frozen=True)
class SkillFinding:
    path: Path
    message: str


def split_frontmatter(text: str) -> tuple[dict[str, object], bool]:
    lines = text.splitlines()
    if not lines or lines[0] != FRONTMATTER_DELIMITER:
        return {}, False

    for index, line in enumerate(lines[1:], start=1):
        if line == FRONTMATTER_DELIMITER:
            frontmatter_text = "\n".join(lines[1:index])
            try:
                parsed = yaml.safe_load(frontmatter_text)
            except yaml.YAMLError as error:
                return {"__yaml_error__": str(error)}, False
            return parsed if isinstance(parsed, dict) else {}, isinstance(parsed, dict)

    return {}, False


def skill_files_from_path(path: Path) -> list[Path]:
    if path.name == SKILL_FILE_NAME:
        return [path]
    if (path / SKILL_FILE_NAME).is_file():
        return [path / SKILL_FILE_NAME]
    if path.is_dir():
        return sorted(child / SKILL_FILE_NAME for child in path.iterdir() if (child / SKILL_FILE_NAME).is_file())
    return [path / SKILL_FILE_NAME]


def validate_skill_file(skill_file: Path) -> list[SkillFinding]:
    findings: list[SkillFinding] = []
    if not skill_file.is_file():
        return [SkillFinding(skill_file, "SKILL.md is missing")]

    frontmatter, parsed = split_frontmatter(skill_file.read_text(encoding="utf-8"))
    if "__yaml_error__" in frontmatter:
        return [SkillFinding(skill_file, f"frontmatter YAML is invalid: {frontmatter['__yaml_error__']}")]
    if not parsed:
        return [SkillFinding(skill_file, "SKILL.md must start with YAML frontmatter")]

    unexpected_keys = sorted(set(frontmatter) - ALLOWED_FRONTMATTER_KEYS)
    if unexpected_keys:
        findings.append(SkillFinding(skill_file, "unexpected frontmatter keys: " + ", ".join(unexpected_keys)))

    name = frontmatter.get("name")
    if not isinstance(name, str) or not name.strip():
        findings.append(SkillFinding(skill_file, "frontmatter name must be a non-empty string"))
    else:
        normalized_name = name.strip()
        if not NAME_PATTERN.fullmatch(normalized_name):
            findings.append(SkillFinding(skill_file, "frontmatter name must use lowercase letters, digits, and hyphens"))
        if normalized_name.startswith("-") or normalized_name.endswith("-") or "--" in normalized_name:
            findings.append(SkillFinding(skill_file, "frontmatter name must not start or end with a hyphen or contain repeated hyphens"))
        if len(normalized_name) > MAX_SKILL_NAME_LENGTH:
            findings.append(SkillFinding(skill_file, f"frontmatter name must be at most {MAX_SKILL_NAME_LENGTH} characters"))
        if skill_file.parent.name != normalized_name:
            findings.append(SkillFinding(skill_file, "frontmatter name must match the skill directory name"))

    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        findings.append(SkillFinding(skill_file, "frontmatter description must be a non-empty string"))
    else:
        normalized_description = description.strip()
        if "<" in normalized_description or ">" in normalized_description:
            findings.append(SkillFinding(skill_file, "frontmatter description must not contain angle brackets"))
        if len(normalized_description) > MAX_DESCRIPTION_LENGTH:
            findings.append(SkillFinding(skill_file, f"frontmatter description must be at most {MAX_DESCRIPTION_LENGTH} characters"))

    if (skill_file.parent / "agents" / "openai.yaml").exists():
        findings.append(SkillFinding(skill_file, "source skills must not include agents/openai.yaml; use adapters instead"))

    return findings


def validate_skill_paths(paths: list[Path]) -> list[SkillFinding]:
    findings: list[SkillFinding] = []
    for path in paths:
        skill_files = skill_files_from_path(path)
        if not skill_files:
            findings.append(SkillFinding(path, "no skill files found"))
            continue
        for skill_file in skill_files:
            findings.extend(validate_skill_file(skill_file))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Agent Skill source files")
    parser.add_argument("paths", nargs="+", help="Skill roots, skill directories, or SKILL.md files")
    args = parser.parse_args(argv)

    findings = validate_skill_paths([Path(path) for path in args.paths])
    if not findings:
        print("Agent skill validation passed.")
        return SUCCESS_EXIT_CODE

    for finding in findings:
        print(f"- {finding.path}: {finding.message}")
    return ERROR_EXIT_CODE


if __name__ == "__main__":
    raise SystemExit(main())
