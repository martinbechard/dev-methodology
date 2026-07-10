#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "design" / "agent-skill-test-coverage-checklist.md"

TECHNOLOGY_GROUPS = {
    "TypeScript and Node.js": [
        "typescript-coding",
        "typescript-strict",
        "typescript-esm",
        "node-cli",
        "jest",
        "vitest",
    ],
    "Java and Spring Boot": ["java-coding", "spring-boot"],
    "SQL and PostgreSQL": ["sql-coding", "postgres-drizzle"],
    "React, Next.js, Vite, and Tailwind": [
        "nextjs-app-router",
        "react-server-components",
        "react-vite-renderer",
        "tailwind-design-system",
    ],
    "Electron": ["electron-main", "electron-preload"],
    "Browser automation": ["playwright"],
    "HTTP APIs and authentication": ["api-routes", "clerk-auth"],
    "Agent and model runtimes": [
        "harness-implementation",
        "langgraph",
        "local-model-integration",
        "plan-engine-implementation",
        "tool-runtime-implementation",
    ],
}

HARNESS_ROWS = [
    ("Generic Agent Skills", True, False, "Installer behavior is unit-tested; no native role format or live harness run."),
    ("Codex", True, True, "Skill installation, native role generation, semantic model resolution, and live evaluations passed."),
    ("Claude Code", True, False, "Skill installation and native role generation are tested; no live behavior evaluation yet."),
    ("Gemini CLI", True, False, "Skill installation behavior is unit-tested; native role generation and live behavior are not covered."),
    ("JetBrains Junie CLI", True, False, "Destination and dry-run installation behavior are unit-tested; native role generation and live behavior are not covered."),
]


def load_yaml(path: Path) -> dict[str, object]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a mapping in {path}")
    return value


def load_skills() -> dict[str, str]:
    skills: dict[str, str] = {}
    for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
        parts = path.read_text(encoding="utf-8").split("---", 2)
        if len(parts) != 3:
            raise ValueError(f"Missing frontmatter in {path}")
        frontmatter = yaml.safe_load(parts[1])
        name = str(frontmatter["name"])
        category = str(frontmatter.get("metadata", {}).get("category", "uncategorized"))
        skills[name] = category
    return skills


def load_roles() -> dict[str, dict[str, object]]:
    roles: dict[str, dict[str, object]] = {}
    for path in sorted((ROOT / "agents" / "roles").glob("*/*.role.yaml")):
        role = load_yaml(path)
        roles[str(role["name"])] = role
    return roles


def load_evaluation_coverage() -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    agent_cases: dict[str, list[str]] = defaultdict(list)
    skill_cases: dict[str, list[str]] = defaultdict(list)
    for case in load_yaml(ROOT / "evals" / "cases.yaml")["cases"]:
        case_id = str(case["id"])
        for agent in case.get("requiredAgents", []):
            agent_cases[str(agent)].append(case_id)
        for skill in case.get("requiredSkills", []):
            skill_cases[str(skill)].append(case_id)
    return dict(agent_cases), dict(skill_cases)


def checkbox(value: bool) -> str:
    return "[x]" if value else "[ ]"


def render() -> str:
    skills = load_skills()
    roles = load_roles()
    agent_cases, skill_cases = load_evaluation_coverage()
    categories = load_yaml(ROOT / "design" / "skill-categories.yaml")["categories"]
    category_labels = {str(item["id"]): str(item["label"]) for item in categories}

    stack_skills = {name for name, category in skills.items() if category == "stack-and-domain"}
    classified_stack_skills = {skill for group in TECHNOLOGY_GROUPS.values() for skill in group}
    if stack_skills != classified_stack_skills:
        missing = sorted(stack_skills - classified_stack_skills)
        extra = sorted(classified_stack_skills - stack_skills)
        raise ValueError(f"Technology classification mismatch; missing={missing}, extra={extra}")

    lines = [
        "# Agent, Skill, Technology, And Test Coverage Checklist",
        "",
        "This page is generated from the canonical roles, bundled skill frontmatter, technology classification, and evaluation cases. Regenerate it with scripts/build-support-checklist.py.",
        "",
        "## Status Meaning",
        "",
        "- [x] Structural means the item exists in the canonical catalog and is covered by repository validation or generation checks.",
        "- [x] Live behavior means the item participated in a recorded live agent evaluation.",
        "- [ ] Live behavior means no dedicated live evaluation currently proves that item.",
        "- A passing structural check is not a substitute for a behavior evaluation.",
        "",
        "## Summary",
        "",
        f"- [x] {len(roles)} canonical agents are defined and generate through the supported native role adapters.",
        f"- [x] {len(skills)} bundled skills pass catalog and Agent Skill validation.",
        f"- [x] {len(agent_cases)} agents have direct live behavior evidence.",
        f"- [x] {len(skill_cases)} skills have direct live behavior evidence.",
        "- [x] TypeScript implementation, Java and Spring Boot implementation, SQL behavior, and TypeScript code review have live evaluation evidence.",
        "- [ ] The remaining agents, skills, technologies, and harnesses need dedicated behavior evaluations as marked below.",
        "",
        "## Harness Support",
        "",
        "| Harness | Structural | Live behavior | Coverage |",
        "| --- | --- | --- | --- |",
    ]
    for name, structural, live, note in HARNESS_ROWS:
        lines.append(f"| {name} | {checkbox(structural)} | {checkbox(live)} | {note} |")

    lines.extend([
        "",
        "## Supported Technology Skills",
        "",
        "| Technology | Skills | Structural | Direct live coverage |",
        "| --- | --- | --- | --- |",
    ])
    for technology, group_skills in TECHNOLOGY_GROUPS.items():
        direct_coverage = [
            f"{skill}: {', '.join(skill_cases[skill])}"
            for skill in group_skills
            if skill_cases.get(skill)
        ]
        evidence = "; ".join(direct_coverage) if direct_coverage else "None"
        lines.append(
            f"| {technology} | {', '.join(group_skills)} | [x] | {evidence} |"
        )

    lines.extend([
        "",
        "## Canonical Agent Checklist",
        "",
        "| Agent | Profile | Structural | Live behavior | Evaluation evidence |",
        "| --- | --- | --- | --- | --- |",
    ])
    for name, role in sorted(roles.items()):
        cases = agent_cases.get(name, [])
        lines.append(
            f"| {name} | {role['modelProfile']} | [x] | {checkbox(bool(cases))} | {', '.join(cases) if cases else 'None'} |"
        )

    lines.extend(["", "## Bundled Skill Checklist", ""])
    for category in categories:
        category_id = str(category["id"])
        lines.extend([f"### {category_labels[category_id]}", ""])
        for name in sorted(skill for skill, value in skills.items() if value == category_id):
            cases = skill_cases.get(name, [])
            behavior = f"[x] Live behavior: {', '.join(cases)}" if cases else "[ ] Live behavior: no dedicated evaluation"
            lines.append(f"- [x] {name} — structural; {behavior}")
        lines.append("")

    lines.extend([
        "## Recorded Live Evaluations",
        "",
        "- [x] TypeScript order pricing: Coding Agent implementation, eight passing tests, build, coding checklist evidence, and review synthesis.",
        "- [x] Spring Boot order cancellation: Coding Agent implementation, ten passing tests, HTTP, transaction, persisted-state, and conditional SQL evidence.",
        "- [x] TypeScript code review: read-only Code Review Agent found the unawaited lookup, swallowed provider failure, and missing percentage validation in a deliberately defective change.",
        "- [x] Codex model mapping: the live review exposed the rejected friendly alias and passed after generation switched to the concrete gpt-5.6-luna identifier.",
        "",
        "## Repository Verification Layers",
        "",
        "- [x] Agent Skill format validation for every bundled skill.",
        "- [x] Canonical role schema, skill reference, model profile, and adapter completeness tests.",
        "- [x] Codex TOML and Claude Code Markdown native role generation checks.",
        "- [x] Generic, Codex, Gemini CLI, Claude Code, and Junie CLI installer behavior tests.",
        "- [x] Generated documentation and agent-skill hierarchy freshness checks.",
        "- [x] Shared installation refresh exercised for Agents, Codex, and Claude destinations.",
        "- [x] Evaluation fixture runner verifies expected passing and intentionally failing behavior.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the agent, skill, technology, and test coverage checklist.")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = render()
    if args.check:
        if not OUTPUT_PATH.is_file() or OUTPUT_PATH.read_text(encoding="utf-8") != content:
            print(f"stale {OUTPUT_PATH}")
            return 1
        print("Agent and skill support checklist is current.")
        return 0
    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(f"generated {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
