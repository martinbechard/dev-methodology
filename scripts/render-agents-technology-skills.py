#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Renders unconditional folder technology guidance from PROJECT.yaml.

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Sequence
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
SKILL_FILE_NAME = "SKILL.md"
FRONTMATTER_DELIMITER = "---"
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def parse_boolean(value: str) -> bool:
    """Parse an explicit true-or-false command-line value."""

    normalized = value.lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise argparse.ArgumentTypeError("expected true or false")


def load_yaml(path: Path) -> dict[str, object]:
    """Load one PROJECT.yaml mapping from path."""
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a YAML mapping: {path}")
    return value


def loadouts(value: dict[str, object]) -> list[dict[str, object]]:
    """Return normalized technology skillset mappings from a project configuration."""
    rows = value.get("technology_skill_loadouts", value.get("loadouts", []))
    return [row for row in rows if isinstance(row, dict)] if isinstance(rows, list) else []


def inlined_skill_body(skill_name: str) -> str:
    """Return one validated bundled technology skill body."""

    if not SKILL_NAME_PATTERN.fullmatch(skill_name):
        raise ValueError(f"Invalid technology skill name: {skill_name}")
    skill_path = SKILLS_ROOT / skill_name / SKILL_FILE_NAME
    lines = skill_path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != FRONTMATTER_DELIMITER:
        raise ValueError(f"Missing YAML frontmatter: {skill_path}")
    try:
        closing_index = lines[1:].index(FRONTMATTER_DELIMITER) + 1
    except ValueError as error:
        raise ValueError(f"Missing closing frontmatter delimiter: {skill_path}") from error
    frontmatter = yaml.safe_load("\n".join(lines[1:closing_index]))
    if not isinstance(frontmatter, dict) or frontmatter.get("name") != skill_name:
        raise ValueError(f"Skill name must match its directory: {skill_path}")
    return "\n".join(lines[closing_index + 1:]).strip()


def render(value: dict[str, object], inline_tech_skills: bool = True) -> str:
    """Render root AGENTS.md technology sections."""
    lines: list[str] = [
        "## Technology Skills",
        "",
        "Technology detection is owned by Project Configurator. Do not rerun detection during ordinary work.",
        "",
        (
            "Before acting on files under a matching folder, every agent must apply each inlined skill completely. These folder skills govern technology-specific implementation, review, diagnosis, verification, security, interface, prompt, and technical documentation work together with the agent's definition-owned skills."
            if inline_tech_skills
            else "Before acting on files under a matching folder, every agent must read each listed skill completely. These folder skills govern technology-specific implementation, review, diagnosis, verification, security, interface, prompt, and technical documentation work together with the agent's definition-owned skills."
        ),
        "",
        "Folder skillsets:",
        "",
        "When configured folder patterns overlap, the most-specific matching pattern wins.",
        "",
    ]
    inlined_loadouts: list[tuple[str, list[str]]] = []
    rendered = 0
    for item in loadouts(value):
        pattern = item.get("pathPattern", item.get("pattern"))
        skills = item.get("skills", item.get("required_skills", []))
        if not isinstance(pattern, str) or not isinstance(skills, list):
            continue
        names = [str(skill) for skill in skills if isinstance(skill, str)]
        if not names:
            if item.get("status") != "NO_VARIANT":
                continue
            fallback = item.get("fallback", "General model training")
            lines.append(
                f"- {pattern}: no pertinent specialized technology skill is available; "
                f"use {fallback} and continue full scope coverage."
            )
            rendered += 1
            continue
        if inline_tech_skills:
            noun = "skill" if len(names) == 1 else "skills"
            lines.append(
                f"- {pattern}: apply the inlined {', '.join(names)} {noun} instructions before acting."
            )
            inlined_loadouts.append((pattern, names))
        else:
            lines.append(f"- {pattern}: load {', '.join(names)} before acting.")
        for evidence in item.get("sourceEvidence", item.get("source_evidence", [])):
            if isinstance(evidence, dict) and isinstance(evidence.get("skill"), str):
                facts = evidence.get("evidence", [])
                if isinstance(facts, list) and facts:
                    lines.append(f"  - {evidence['skill']} evidence: {'; '.join(str(fact) for fact in facts)}")
        rendered += 1
    if rendered == 0:
        lines.append("- No bundled technology variant was detected for the analyzed folders.")
    if inlined_loadouts:
        lines.extend([
            "",
            "Inlined folder skill instructions:",
        ])
        for pattern, names in inlined_loadouts:
            lines.extend([
                "",
                f"### Folder pattern: {pattern}",
                "",
                "Apply every inlined technology skill below when working under this folder pattern.",
            ])
            for skill_name in names:
                lines.extend([
                    "",
                    f"----- BEGIN INLINED TECHNOLOGY SKILL: {skill_name} -----",
                    inlined_skill_body(skill_name),
                    f"----- END INLINED TECHNOLOGY SKILL: {skill_name} -----",
                ])
    lines.append("")
    return "\n".join(lines)


def main(arguments: Sequence[str] | None = None) -> int:
    """Render configured AGENTS.md sections to stdout or an explicit output file."""
    parser = argparse.ArgumentParser(description="Render unconditional AGENTS.md technology skill guidance.")
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--inline-tech-skills",
        type=parse_boolean,
        default=True,
        metavar="true|false",
        help="Statically embed discovered technology skills in AGENTS.md. Defaults to true.",
    )
    args = parser.parse_args(arguments)
    try:
        content = render(load_yaml(args.project), args.inline_tech_skills)
        if args.output:
            args.output.write_text(content, encoding="utf-8")
        else:
            print(content, end="")
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
