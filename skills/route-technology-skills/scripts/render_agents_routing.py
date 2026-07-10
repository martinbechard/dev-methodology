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


def render(plan: dict[str, object]) -> str:
    lines = [
        "## Specialized Skill Routing",
        "",
        "Before source implementation, review, verification, diagnosis, security, interface, prompt, or technical documentation work:",
        "",
        "1. Read the root and nearest AGENTS.md.",
        "2. Run the Route Technology Skills resolver for the active role and exact file scope.",
        "3. Read every resolved skill file and preserve the final routing receipt.",
        "4. Stop when a required project-bound skill is unavailable.",
        "5. When no bundled variant exists, use generic guidance and report the specialized-guidance gap.",
        "",
        "Project bindings:",
        "",
    ]
    rows = 0
    for item in plan.get("skill_loadouts", []):
        if not isinstance(item, dict):
            continue
        scope = str(item.get("scope", "Unnamed scope"))
        paths = [str(value) for value in item.get("paths", []) if isinstance(value, str)]
        skills = [str(value) for value in item.get("skills", []) if isinstance(value, str)]
        if paths and skills:
            lines.append(f"- {scope}: paths {', '.join(paths)}; required skills {', '.join(skills)}")
            rows += 1
    for item in plan.get("folder_routing", []):
        if not isinstance(item, dict):
            continue
        pattern = item.get("pattern")
        skills = [str(value) for value in item.get("required_skills", []) if isinstance(value, str)]
        if isinstance(pattern, str) and skills:
            lines.append(f"- Folder route {pattern}: required skills {', '.join(skills)}")
            rows += 1
    if rows == 0:
        lines.append("- No specialized project bindings were identified. Runtime routing must report this gap rather than inventing bindings.")
    lines.extend([
        "",
        "The routing receipt proves deterministic selection, availability, and content digests. Harness tool-call evidence is required to prove the selected skill files were actually read.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the AGENTS.md specialized skill routing section from AGENTS-PLAN.yaml.")
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
