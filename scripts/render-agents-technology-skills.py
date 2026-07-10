#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import yaml


def load_yaml(path: Path) -> dict[str, object]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a YAML mapping: {path}")
    return value


def loadouts(value: dict[str, object]) -> list[dict[str, object]]:
    rows = value.get("technology_skill_loadouts", value.get("loadouts", []))
    return [row for row in rows if isinstance(row, dict)] if isinstance(rows, list) else []


def render(value: dict[str, object]) -> str:
    lines = [
        "## Technology Skills",
        "",
        "Technology detection is owned by Project Agent Setup. Do not rerun detection during ordinary work.",
        "",
        "Before acting on files under a matching folder, every agent must read each listed skill completely. These folder skills govern technology-specific implementation, review, diagnosis, verification, security, interface, prompt, and technical documentation work together with the agent's fixed-role skills.",
        "",
        "Folder loadouts:",
        "",
    ]
    rendered = 0
    for item in loadouts(value):
        pattern = item.get("pathPattern", item.get("pattern"))
        skills = item.get("skills", item.get("required_skills", []))
        if not isinstance(pattern, str) or not isinstance(skills, list) or not skills:
            continue
        names = [str(skill) for skill in skills if isinstance(skill, str)]
        if not names:
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
    parser = argparse.ArgumentParser(description="Render unconditional AGENTS.md technology skill guidance.")
    parser.add_argument("--agents-plan", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    content = render(load_yaml(args.agents_plan))
    if args.output:
        args.output.write_text(content, encoding="utf-8")
    else:
        print(content, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
