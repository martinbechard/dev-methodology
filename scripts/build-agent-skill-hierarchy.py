#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
ROLES_ROOT = ROOT / "agents" / "roles"
MODEL_PROFILES_PATH = ROOT / "agents" / "model-profiles.yaml"
SKILLS_ROOT = ROOT / "skills"
DETECTION_REGISTRY_PATH = SKILLS_ROOT / "detect-technology-skills" / "references" / "technology-skill-detection-registry.yaml"
OUTPUT_PATH = ROOT / "design" / "agent-skill-hierarchy.svg"
ROW_HEIGHT = 30
TOP = 110
MODEL_X = 30
ROLE_X = 360
SKILL_X = 1120
NODE_WIDTH = 300
SKILL_WIDTH = 360


def load_yaml(path: Path) -> dict[str, object]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected YAML object: {path}")
    return value


def role_skill_entries(role: dict[str, object]) -> list[tuple[str, bool]]:
    value = role.get("skills")
    if not isinstance(value, list):
        raise ValueError(f"Role {role.get('name')} skills must be a list.")
    entries: list[tuple[str, bool]] = []
    for item in value:
        if isinstance(item, str):
            entries.append((item, False))
        elif isinstance(item, dict) and len(item) == 1:
            name, metadata = next(iter(item.items()))
            entries.append((str(name), isinstance(metadata, dict) and "condition" in metadata))
        else:
            raise ValueError(f"Role {role.get('name')} has an invalid skill entry: {item}")
    return entries


def skill_category(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    frontmatter = yaml.safe_load(parts[1])
    if not isinstance(frontmatter, dict):
        raise ValueError(f"Expected skill frontmatter: {path}")
    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        raise ValueError(f"Expected skill metadata: {path}")
    return str(frontmatter["name"]), str(metadata["category"])


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def node(
    x: int,
    y: int,
    width: int,
    label: str,
    secondary: str = "",
    modifier: str = "",
) -> str:
    secondary_text = (
        f'<text x="{x + width - 12}" y="{y + 16}" text-anchor="end" class="secondary">{escape(secondary)}</text>'
        if secondary
        else ""
    )
    return (
        f'<g><rect x="{x}" y="{y}" width="{width}" height="24" rx="5" class="node{modifier}"/>'
        f'<text x="{x + 12}" y="{y + 16}">{escape(label)}</text>{secondary_text}</g>'
    )


def build_svg() -> str:
    profiles = load_yaml(MODEL_PROFILES_PATH)["profiles"]
    if not isinstance(profiles, dict):
        raise ValueError("Canonical model profiles must be a mapping.")

    roles: list[dict[str, object]] = []
    for path in sorted(ROLES_ROOT.glob("*/*.role.yaml")):
        role = load_yaml(path)
        role["group"] = path.parent.name
        roles.append(role)

    skills_by_category: dict[str, list[str]] = {}
    for path in sorted(SKILLS_ROOT.glob("*/SKILL.md")):
        name, category = skill_category(path)
        skills_by_category.setdefault(category, []).append(name)
    detection_registry = load_yaml(DETECTION_REGISTRY_PATH)
    detection_by_skill = {str(entry["skill"]): entry for entry in detection_registry["skills"]}

    role_y: dict[str, int] = {}
    current_y = TOP
    grouped_roles: dict[str, list[dict[str, object]]] = {}
    for role in roles:
        grouped_roles.setdefault(str(role["group"]), []).append(role)
    for group_roles in grouped_roles.values():
        current_y += ROW_HEIGHT
        for role in group_roles:
            role_y[str(role["name"])] = current_y
            current_y += ROW_HEIGHT
        current_y += 12

    skill_y: dict[str, int] = {}
    skill_current_y = TOP
    for skill_names in skills_by_category.values():
        skill_current_y += ROW_HEIGHT
        for skill_name in skill_names:
            skill_y[skill_name] = skill_current_y
            skill_current_y += ROW_HEIGHT
        skill_current_y += 12

    height = max(current_y, skill_current_y) + 90
    width = 1540
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Canonical model profile, agent, and skill hierarchy</title>',
        '<desc id="desc">Every canonical role is connected to its semantic model profile, fixed generic skills, and conditionally loaded request-specific skills. Technology and domain skills are labeled as setup-time detected skills without task-time role edges.</desc>',
        '<style>text{font-family:ui-sans-serif,system-ui,sans-serif;font-size:12px;fill:#172033}.heading{font-size:18px;font-weight:600}.group{font-size:13px;font-weight:600;fill:#334155}.secondary{font-size:9px;fill:#64748b}.node{fill:#f8fafc;stroke:#94a3b8}.node.conditional{fill:#eeeafd;stroke:#7c3aed}.node.technology{fill:#e0f2fe;stroke:#0284c7}.model{fill:#e0f2fe;stroke:#0284c7}.edge{fill:none;stroke:#94a3b8;stroke-width:1;opacity:.32}.conditional-edge{stroke:#7c3aed;opacity:.55}.model-edge{stroke:#0284c7;opacity:.45}</style>',
        '<text x="30" y="44" class="heading">Model profiles</text>',
        '<text x="360" y="44" class="heading">Canonical agents</text>',
        '<text x="1120" y="44" class="heading">Bundled skills</text>',
        '<text x="30" y="70" class="secondary">Adapter mappings resolve concrete models</text>',
        '<text x="360" y="70" class="secondary">Roles own fixed and request-specific skills</text>',
        '<text x="1120" y="70" class="secondary">Violet is conditional; blue is setup-time technology</text>',
    ]

    profile_y: dict[str, int] = {}
    for index, (profile_id, profile) in enumerate(profiles.items()):
        y = TOP + index * 54
        profile_y[str(profile_id)] = y
        purpose = profile.get("purpose", "") if isinstance(profile, dict) else ""
        purpose = str(purpose)
        if len(purpose) > 42:
            purpose = purpose[:39] + "..."
        parts.append(f'<rect x="{MODEL_X}" y="{y}" width="280" height="42" rx="6" class="model"/>')
        parts.append(f'<text x="{MODEL_X + 12}" y="{y + 16}">{escape(profile_id)}</text>')
        parts.append(f'<text x="{MODEL_X + 12}" y="{y + 32}" class="secondary">{escape(purpose)}</text>')

    for role in roles:
        y = role_y[str(role["name"])]
        profile = str(role["modelProfile"])
        parts.append(
            f'<path d="M {MODEL_X + 280} {profile_y[profile] + 21} C 330 {profile_y[profile] + 21}, 330 {y + 12}, {ROLE_X} {y + 12}" class="edge model-edge"/>'
        )
        for skill_name, conditional in role_skill_entries(role):
            parts.append(
                f'<path d="M {ROLE_X + NODE_WIDTH} {y + 12} C 820 {y + 12}, 940 {skill_y[skill_name] + 12}, {SKILL_X} {skill_y[skill_name] + 12}" class="edge{" conditional-edge" if conditional else ""}"/>'
            )
    current_y = TOP
    for group, group_roles in grouped_roles.items():
        parts.append(f'<text x="{ROLE_X}" y="{current_y + 18}" class="group">{escape(group.replace("-", " ").title())}</text>')
        current_y += ROW_HEIGHT
        for role in group_roles:
            stage_count = len(role.get("modelStages", {}))
            secondary = f'{role["modelProfile"]}' + (f"; {stage_count} stage profiles" if stage_count else "")
            parts.append(node(ROLE_X, current_y, NODE_WIDTH, str(role["name"]), secondary))
            current_y += ROW_HEIGHT
        current_y += 12

    skill_current_y = TOP
    skill_assignment_kinds: dict[str, set[str]] = {}
    for role in roles:
        for skill_name, conditional in role_skill_entries(role):
            skill_assignment_kinds.setdefault(skill_name, set()).add(
                "request-specific" if conditional else "fixed"
            )
    for category, skill_names in skills_by_category.items():
        parts.append(f'<text x="{SKILL_X}" y="{skill_current_y + 18}" class="group">{escape(category.replace("-", " ").title())}</text>')
        skill_current_y += ROW_HEIGHT
        for skill_name in skill_names:
            detection = detection_by_skill.get(skill_name)
            assignment_kinds = skill_assignment_kinds.get(skill_name, set())
            secondary = (
                f"setup-time {detection['kind']}"
                if detection
                else " / ".join(sorted(assignment_kinds)) or "unassigned"
            )
            modifier = (
                " technology"
                if detection
                else " conditional"
                if assignment_kinds == {"request-specific"}
                else ""
            )
            parts.append(node(SKILL_X, skill_current_y, SKILL_WIDTH, skill_name, secondary, modifier))
            skill_current_y += ROW_HEIGHT
        skill_current_y += 12

    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the canonical agent and skill hierarchy SVG.")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = build_svg()
    if args.check:
        if not OUTPUT_PATH.is_file() or OUTPUT_PATH.read_text(encoding="utf-8") != rendered:
            print(f"stale {OUTPUT_PATH}")
            return 1
        return 0
    OUTPUT_PATH.write_text(rendered, encoding="utf-8")
    print(f"generated {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
