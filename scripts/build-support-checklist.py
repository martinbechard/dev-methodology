#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Builds the agent-skill support checklist and generated explorer coverage data.

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import defaultdict
from pathlib import Path
from types import ModuleType

import yaml


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "design" / "agent-skill-test-coverage-checklist.md"
EXPLORER_PATH = ROOT / "design" / "generated" / "agent-skill-explorer-data.js"
REGISTRY_PATH = ROOT / "skills" / "detect-technology-skills" / "references" / "technology-skill-detection-registry.yaml"
EVIDENCE_ROOT = ROOT / "evals" / "evidence"
EVAL_RUNNER_PATH = ROOT / "scripts" / "run-agent-skill-evals.py"

HARNESS_ROWS = [
    ("Generic Agent Skills", True, False, False, "Installer behavior is unit-tested; no native role format or captured behavior evidence."),
    ("Codex", True, True, False, "Native generation and manual runs exist; current evidence lacks machine-verifiable load and invocation receipts."),
    ("Claude Code", True, False, False, "Skill installation and native role generation are tested; no captured behavior evidence."),
    ("Gemini CLI", True, False, False, "Skill installation behavior is unit-tested; native role generation and behavior are not covered."),
    ("JetBrains Junie CLI", True, False, False, "Destination and dry-run installation behavior are unit-tested; native role generation and behavior are not covered."),
]


def load_yaml(path: Path) -> dict[str, object]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a mapping in {path}")
    return value


def role_skill_entries(role: dict[str, object]) -> list[tuple[str, str | None]]:
    value = role.get("skills")
    if not isinstance(value, list):
        raise ValueError(f"Role {role.get('name')} skills must be a list.")
    entries: list[tuple[str, str | None]] = []
    for item in value:
        if isinstance(item, str):
            entries.append((item, None))
        elif isinstance(item, dict) and len(item) == 1:
            name, metadata = next(iter(item.items()))
            condition = metadata.get("condition") if isinstance(metadata, dict) else None
            entries.append((str(name), str(condition) if condition is not None else None))
        else:
            raise ValueError(f"Role {role.get('name')} has an invalid skill entry: {item}")
    return entries


def role_skill_names(role: dict[str, object]) -> list[str]:
    return [name for name, _condition in role_skill_entries(role)]


def load_eval_runner() -> ModuleType:
    spec = importlib.util.spec_from_file_location("run_agent_skill_evals", EVAL_RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load the agent-skill evaluation validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def load_evaluation_coverage() -> tuple[dict[str, list[str]], dict[str, list[str]], dict[str, list[str]], dict[str, list[str]]]:
    declared_agents: dict[str, list[str]] = defaultdict(list)
    declared_skills: dict[str, list[str]] = defaultdict(list)
    verified_agents: dict[str, list[str]] = defaultdict(list)
    verified_skills: dict[str, list[str]] = defaultdict(list)
    cases = load_yaml(ROOT / "evals" / "cases.yaml")["cases"]
    cases_by_id = {str(case["id"]): case for case in cases}
    for case in cases:
        case_id = str(case["id"])
        for agent in case.get("requiredAgents", []):
            declared_agents[str(agent)].append(case_id)
        for skill in case.get("requiredSkills", []):
            declared_skills[str(skill)].append(case_id)
    if EVIDENCE_ROOT.is_dir():
        for path in sorted(EVIDENCE_ROOT.glob("*.yaml")):
            evidence = load_yaml(path)
            if evidence.get("schema") != "dev-methodology-eval-evidence" or evidence.get("version") != 1:
                raise ValueError(f"Unsupported evaluation evidence schema: {path}")
            case_id = str(evidence.get("case"))
            if case_id not in cases_by_id:
                raise ValueError(f"Evaluation evidence references unknown case {case_id}: {path}")
            if evidence.get("verdict") != "verified":
                continue
            errors = load_eval_runner().validate_evidence(cases_by_id[case_id], path)
            if errors:
                raise ValueError(f"Invalid verified evaluation evidence {path}: {'; '.join(errors)}")
            agent = evidence.get("agent", {})
            if isinstance(agent, dict) and isinstance(agent.get("id"), str):
                verified_agents[agent["id"]].append(case_id)
            for skill in evidence.get("skills", []):
                if isinstance(skill, dict) and isinstance(skill.get("id"), str):
                    verified_skills[skill["id"]].append(case_id)
    return dict(declared_agents), dict(declared_skills), dict(verified_agents), dict(verified_skills)


def checkbox(value: bool) -> str:
    return "[x]" if value else "[ ]"


def render() -> str:
    skills = load_skills()
    roles = load_roles()
    declared_agents, declared_skills, verified_agents, verified_skills = load_evaluation_coverage()
    registry = load_yaml(REGISTRY_PATH)
    categories = load_yaml(ROOT / "design" / "skill-categories.yaml")["categories"]
    category_labels = {str(item["id"]): str(item["label"]) for item in categories}

    specialized = list(registry["skills"])

    lines = [
        "# Agent, Skill, Technology, And Test Coverage Checklist",
        "",
        "This page is generated from the canonical roles, bundled skill frontmatter, setup-time technology detection registry, declared evaluation cases, and verified evidence receipts. Regenerate it with scripts/build-support-checklist.py.",
        "",
        "## Status Meaning",
        "",
        "- [x] Structural means the item exists in the canonical catalog and is covered by repository validation or generation checks.",
        "- Declared means an evaluation case names the item. Declaration does not prove invocation or behavior.",
        "- Manual means a human-observed run exists without a complete machine-verifiable invocation and skill-read receipt.",
        "- [x] Verified behavior requires captured agent identity, concrete model, skill content digests, skill-read tool evidence, deterministic assertions, and an independent verdict.",
        "- [ ] Verified behavior means that proof is absent.",
        "- A passing structural check is not a substitute for a behavior evaluation.",
        "",
        "## Summary",
        "",
        f"- [x] {len(roles)} canonical agents are defined and generate through the supported native role adapters.",
        f"- [x] {len(skills)} bundled skills pass catalog and Agent Skill validation.",
        f"- [x] {len(declared_agents)} agents and {len(declared_skills)} skills are named in current evaluation cases.",
        f"- [ ] {len(verified_agents)} agents and {len(verified_skills)} skills have independently verified behavior evidence under the current proof contract.",
        "- TypeScript implementation, Java and Spring Boot implementation, SQL behavior, and TypeScript code review have useful manual observations that must be rerun with truthful receipts.",
        "",
        "## Harness Support",
        "",
        "| Harness | Structural | Manual run | Verified behavior | Coverage |",
        "| --- | --- | --- | --- | --- |",
    ]
    for name, structural, manual, verified, note in HARNESS_ROWS:
        lines.append(f"| {name} | {checkbox(structural)} | {checkbox(manual)} | {checkbox(verified)} | {note} |")

    lines.extend([
        "",
        "## Technology Detection Registry",
        "",
        "| Skill | Kind | Label | Capabilities | Declared cases | Verified behavior |",
        "| --- | --- | --- | --- | --- | --- |",
    ])
    for entry in specialized:
        skill = str(entry["skill"])
        verified_text = ", ".join(verified_skills.get(skill, [])) or "None"
        lines.append(
            f"| {skill} | {entry['kind']} | {entry['label']} | {', '.join(entry['capabilities'])} | {', '.join(declared_skills.get(skill, [])) or 'None'} | {checkbox(bool(verified_skills.get(skill)))} {verified_text} |"
        )

    lines.extend([
        "",
        "## Canonical Agent Checklist",
        "",
        "| Agent | Profile | Structural | Declared cases | Verified behavior | Verified evidence |",
        "| --- | --- | --- | --- | --- | --- |",
    ])
    for name, role in sorted(roles.items()):
        declared = declared_agents.get(name, [])
        verified = verified_agents.get(name, [])
        lines.append(
            f"| {name} | {role['modelProfile']} | [x] | {', '.join(declared) if declared else 'None'} | {checkbox(bool(verified))} | {', '.join(verified) if verified else 'None'} |"
        )

    lines.extend(["", "## Bundled Skill Checklist", ""])
    for category in categories:
        category_id = str(category["id"])
        lines.extend([f"### {category_labels[category_id]}", ""])
        for name in sorted(skill for skill, value in skills.items() if value == category_id):
            declared = declared_skills.get(name, [])
            verified = verified_skills.get(name, [])
            verified_text = ", ".join(verified) if verified else "none"
            lines.append(f"- [x] {name} — structural; declared: {', '.join(declared) if declared else 'none'}; verified behavior: {checkbox(bool(verified))} {verified_text}")
        lines.append("")

    lines.extend([
        "## Manual Evaluation Observations Requiring Receipt-Based Reruns",
        "",
        "- [ ] TypeScript order pricing produced eight passing tests and a build, but lacks a machine-verifiable agent and skill-read receipt.",
        "- [ ] Spring Boot order cancellation produced ten passing tests and useful boundary evidence, but lacks a machine-verifiable agent and skill-read receipt.",
        "- [ ] TypeScript code review truthfully found all seeded defects in a read-only run, but lacks a complete captured invocation and skill-read receipt.",
        "- [ ] Staged model execution remains unverified until separate evidence-extraction and synthesis invocations are captured.",
        "",
        "## Repository Verification Layers",
        "",
        "- [x] Agent Skill format validation for every bundled skill.",
        "- [x] Canonical role schema, skill reference, model profile, and adapter completeness tests.",
        "- [x] Codex TOML and Claude Code Markdown native role generation checks.",
        "- [x] Generic, Codex, Gemini CLI, Claude Code, and Junie CLI installer behavior tests.",
        "- [x] Generated documentation and agent-skill hierarchy freshness checks.",
        "- [x] Shared installation refresh exercised for Agents, Codex, and Claude destinations.",
        "- [x] Evaluation fixture runner verifies expected project behavior, including intentionally failing review fixtures.",
        "- [ ] Agent and skill attribution remains unchecked until a valid evidence receipt is supplied.",
        "",
    ])
    return "\n".join(lines)


def render_explorer_data() -> str:
    skills = load_skills()
    roles = load_roles()
    declared_agents, declared_skills, verified_agents, verified_skills = load_evaluation_coverage()
    registry = load_yaml(REGISTRY_PATH)
    detection = {str(entry["skill"]): entry for entry in registry["skills"]}
    role_items = []
    edges = []
    for role_id, role in sorted(roles.items()):
        skill_entries = role_skill_entries(role)
        fixed_skills = [name for name, condition in skill_entries if condition is None]
        conditional_skills = {
            name: condition for name, condition in skill_entries if condition is not None
        }
        role_items.append({
            "id": role_id,
            "label": role.get("label", role_id),
            "description": role.get("description", ""),
            "modelProfile": role["modelProfile"],
            "fixedSkills": fixed_skills,
            "conditionalSkills": conditional_skills,
            "dynamicFolderSkills": bool(role.get("dynamicFolderSkills", False)),
            "declaredCases": declared_agents.get(role_id, []),
            "verifiedCases": verified_agents.get(role_id, []),
        })
        edges.extend({"role": role_id, "skill": skill, "kind": "fixed"} for skill in fixed_skills)
        edges.extend(
            {"role": role_id, "skill": skill, "kind": "conditional", "condition": condition}
            for skill, condition in conditional_skills.items()
        )
    skill_items = []
    for skill_id, category in sorted(skills.items()):
        entry = detection.get(skill_id)
        skill_items.append({
            "id": skill_id,
            "category": category,
            "detection": entry,
            "declaredCases": declared_skills.get(skill_id, []),
            "verifiedCases": verified_skills.get(skill_id, []),
        })
    payload = {
        "schema": "dev-methodology-agent-skill-explorer-data",
        "version": 1,
        "roles": role_items,
        "skills": skill_items,
        "edges": sorted(edges, key=lambda item: (item["role"], item["kind"], item["skill"])),
        "evidenceStatus": {
            "declaredAgentCount": len(declared_agents),
            "declaredSkillCount": len(declared_skills),
            "verifiedAgentCount": len(verified_agents),
            "verifiedSkillCount": len(verified_skills),
        },
    }
    return (
        "// Copyright (c) 2026 Martin.Bechard@DevConsult.ca\n"
        "// AI attribution: Generated with AI assistance.\n"
        "// Summary: Provides deterministic generated agent-skill coverage data to static design pages.\n"
        "// Generated by scripts/build-support-checklist.py. Do not edit by hand.\n"
        "window.DEV_METHODOLOGY_AGENT_SKILL_EXPLORER_DATA = "
        + json.dumps(payload, indent=2, sort_keys=True)
        + ";\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the agent, skill, technology, and test coverage checklist.")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = {OUTPUT_PATH: render(), EXPLORER_PATH: render_explorer_data()}
    if args.check:
        stale = [path for path, content in outputs.items() if not path.is_file() or path.read_text(encoding="utf-8") != content]
        if stale:
            for path in stale:
                print(f"stale {path}")
            return 1
        print("Agent and skill support checklist is current.")
        return 0
    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")
        print(f"generated {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
