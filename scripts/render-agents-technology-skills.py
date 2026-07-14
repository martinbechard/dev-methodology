#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Renders unconditional folder technology guidance from PROJECT.yaml.

from __future__ import annotations

import argparse
from pathlib import Path

import yaml


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


def render(value: dict[str, object]) -> str:
    """Render root AGENTS.md technology sections."""
    lines: list[str] = [
        "## Technology Skills",
        "",
        "Technology detection is owned by Project Configurator. Do not rerun detection during ordinary work.",
        "",
        "Before acting on files under a matching folder, every agent must read each listed skill completely. These folder skills govern technology-specific implementation, review, diagnosis, verification, security, interface, prompt, and technical documentation work together with the agent's definition-owned skills.",
        "",
        "Folder skillsets:",
        "",
    ]
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
        lines.append(f"- {pattern}: load {', '.join(names)} before acting.")
        for evidence in item.get("sourceEvidence", item.get("source_evidence", [])):
            if isinstance(evidence, dict) and isinstance(evidence.get("skill"), str):
                facts = evidence.get("evidence", [])
                if isinstance(facts, list) and facts:
                    lines.append(f"  - {evidence['skill']} evidence: {'; '.join(str(fact) for fact in facts)}")
        rendered += 1
    if rendered == 0:
        lines.append("- No bundled technology variant was detected for the analyzed folders.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    """Render configured AGENTS.md sections to stdout or an explicit output file."""
    parser = argparse.ArgumentParser(description="Render unconditional AGENTS.md technology skill guidance.")
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    content = render(load_yaml(args.project))
    if args.output:
        args.output.write_text(content, encoding="utf-8")
    else:
        print(content, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
