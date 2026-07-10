#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
ROLES_ROOT = ROOT / "agents" / "roles"
ROUTER_SKILL = SKILLS_ROOT / "route-technology-skills"
REGISTRY_YAML = ROUTER_SKILL / "references" / "technology-skill-registry.yaml"
REGISTRY_JS = ROOT / "design" / "generated" / "technology-skill-registry.js"
ROUTING_FILE = "routing.yaml"
SPECIALIZED_KINDS = {"technology", "domain", "tool"}
ALLOWED_KINDS = SPECIALIZED_KINDS | {"generic"}
ALLOWED_SELECTIONS = {"additive", "exclusive"}
GENERIC_FORBIDDEN_TERMS = {
    "ast-grep",
    "clerk",
    "drizzle",
    "electron",
    "java",
    "javascript",
    "jest",
    "langgraph",
    "next.js",
    "playwright",
    "postgresql",
    "react",
    "spring",
    "tailwind",
    "typescript",
    "vitest",
}


def load_yaml(path: Path) -> dict[str, object]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a YAML mapping: {path}")
    return value


def skill_names() -> set[str]:
    return {path.parent.name for path in SKILLS_ROOT.glob("*/SKILL.md")}


def role_names() -> set[str]:
    return {str(load_yaml(path)["name"]) for path in ROLES_ROOT.glob("*/*.role.yaml")}


def validate_string_list(value: object, field: str, path: Path, allow_empty: bool = True) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise ValueError(f"{field} must be a list of non-empty strings: {path}")
    if not allow_empty and not value:
        raise ValueError(f"{field} must not be empty: {path}")
    return list(value)


def validate_activation(value: object, path: Path, required: bool) -> dict[str, list[object]]:
    if value is None:
        if required:
            raise ValueError(f"Specialized routing must define activation evidence: {path}")
        return {}
    if not isinstance(value, dict):
        raise ValueError(f"activation must be a mapping: {path}")
    allowed = {
        "commands",
        "contentPatterns",
        "fileExtensions",
        "fileGlobs",
        "manifestDependencies",
        "manifestFiles",
    }
    unexpected = sorted(set(value) - allowed)
    if unexpected:
        raise ValueError(f"Unknown activation keys {unexpected}: {path}")
    normalized: dict[str, list[object]] = {}
    for key, items in value.items():
        if not isinstance(items, list):
            raise ValueError(f"activation.{key} must be a list: {path}")
        if key == "contentPatterns":
            patterns: list[object] = []
            for item in items:
                if not isinstance(item, dict) or set(item) != {"glob", "contains"}:
                    raise ValueError(f"contentPatterns entries need glob and contains: {path}")
                if not all(isinstance(item[name], str) and item[name] for name in ("glob", "contains")):
                    raise ValueError(f"contentPatterns values must be strings: {path}")
                patterns.append(dict(item))
            normalized[key] = patterns
        else:
            normalized[key] = validate_string_list(items, f"activation.{key}", path)
    if required and not any(normalized.values()):
        raise ValueError(f"Specialized routing activation must not be empty: {path}")
    return normalized


def load_routing() -> list[dict[str, object]]:
    available_skills = skill_names()
    available_roles = role_names()
    entries: list[dict[str, object]] = []
    for path in sorted(SKILLS_ROOT.glob(f"*/{ROUTING_FILE}")):
        entry = load_yaml(path)
        if entry.get("schema") != "dev-methodology-skill-routing" or entry.get("version") != 1:
            raise ValueError(f"Unsupported routing schema or version: {path}")
        skill = entry.get("skill")
        if skill != path.parent.name or skill not in available_skills:
            raise ValueError(f"Routing skill must match an existing skill directory: {path}")
        kind = entry.get("kind")
        if kind not in ALLOWED_KINDS:
            raise ValueError(f"Unknown routing kind {kind}: {path}")
        capabilities = validate_string_list(entry.get("capabilities"), "capabilities", path, allow_empty=False)
        applicable_roles = validate_string_list(entry.get("applicableRoles", []), "applicableRoles", path)
        unknown_roles = sorted(set(applicable_roles) - available_roles)
        if unknown_roles:
            raise ValueError(f"Unknown applicable roles {unknown_roles}: {path}")
        companions = validate_string_list(entry.get("companions", []), "companions", path)
        unknown_companions = sorted(set(companions) - available_skills)
        if unknown_companions:
            raise ValueError(f"Unknown companion skills {unknown_companions}: {path}")
        selection = entry.get("selection", "additive")
        if selection not in ALLOWED_SELECTIONS:
            raise ValueError(f"Unknown selection mode {selection}: {path}")
        exclusive_group = entry.get("exclusiveGroup")
        if selection == "exclusive" and (not isinstance(exclusive_group, str) or not exclusive_group):
            raise ValueError(f"Exclusive routing needs exclusiveGroup: {path}")
        if selection == "additive" and exclusive_group is not None:
            raise ValueError(f"Additive routing cannot define exclusiveGroup: {path}")
        activation = validate_activation(entry.get("activation"), path, kind in SPECIALIZED_KINDS)
        label = entry.get("label")
        if not isinstance(label, str) or not label:
            raise ValueError(f"label must be a non-empty string: {path}")
        priority = entry.get("priority", 100)
        if not isinstance(priority, int):
            raise ValueError(f"priority must be an integer: {path}")
        normalized = {
            "skill": skill,
            "kind": kind,
            "label": label,
            "capabilities": capabilities,
            "applicableRoles": applicable_roles,
            "activation": activation,
            "companions": companions,
            "selection": selection,
            "priority": priority,
            "requiredWhenMatched": bool(entry.get("requiredWhenMatched", True)),
        }
        if exclusive_group is not None:
            normalized["exclusiveGroup"] = exclusive_group
        entries.append(normalized)
    return entries


def validate_complete_coverage(entries: list[dict[str, object]]) -> None:
    routed = {str(entry["skill"]) for entry in entries}
    stack_skills: set[str] = set()
    for path in SKILLS_ROOT.glob("*/SKILL.md"):
        frontmatter = yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1])
        if frontmatter.get("metadata", {}).get("category") == "stack-and-domain":
            stack_skills.add(path.parent.name)
    required = stack_skills | {"ast-grep"}
    missing = sorted(required - routed)
    if missing:
        raise ValueError(f"Specialized skills missing routing metadata: {missing}")


def validate_generic_skill_text(entries: list[dict[str, object]]) -> None:
    generic_skills = {str(entry["skill"]) for entry in entries if entry["kind"] == "generic"}
    for role_path in ROLES_ROOT.glob("*/*.role.yaml"):
        generic_skills.update(str(skill) for skill in load_yaml(role_path).get("skills", []))
    for skill in sorted(generic_skills):
        path = SKILLS_ROOT / skill / "SKILL.md"
        text = path.read_text(encoding="utf-8").lower()
        found = sorted(
            term for term in GENERIC_FORBIDDEN_TERMS
            if re.search(rf"(?<![a-z0-9-]){re.escape(term)}(?![a-z0-9-])", text)
        )
        if found:
            raise ValueError(f"Generic skill contains specialized terms {found}: {path}")


def validate_role_loadouts(entries: list[dict[str, object]]) -> None:
    specialized = {str(entry["skill"]) for entry in entries if entry["kind"] in SPECIALIZED_KINDS}
    violations: list[str] = []
    for path in sorted(ROLES_ROOT.glob("*/*.role.yaml")):
        role = load_yaml(path)
        fixed = sorted(set(role.get("skills", [])) & specialized)
        if fixed:
            violations.append(f"{role['name']}: {', '.join(fixed)}")
    if violations:
        raise ValueError("Canonical roles contain specialized fixed skills: " + "; ".join(violations))


def registry(entries: list[dict[str, object]]) -> dict[str, object]:
    specialized_capabilities = {
        capability
        for entry in entries
        if entry["kind"] in SPECIALIZED_KINDS
        for capability in entry["capabilities"]
    }
    role_expectations: dict[str, list[str]] = {}
    for path in sorted(ROLES_ROOT.glob("*/*.role.yaml")):
        role = load_yaml(path)
        expectations = validate_string_list(role.get("routedCapabilities", []), "routedCapabilities", path)
        unknown = sorted(set(expectations) - specialized_capabilities)
        if unknown:
            raise ValueError(f"Role expects unregistered routed capabilities {unknown}: {path}")
        if expectations:
            role_expectations[str(role["name"])] = expectations
    return {
        "schema": "dev-methodology-technology-skill-registry",
        "version": 1,
        "selectionPolicy": {
            "projectBindings": "required",
            "repositoryEvidence": "deterministic",
            "promptKeywords": "advisory-only-not-selection",
            "missingRequiredSkill": "blocked",
            "missingVariant": "generic-guidance-with-explicit-gap",
        },
        "roleCapabilityExpectations": role_expectations,
        "skills": sorted(entries, key=lambda item: (int(item["priority"]), str(item["skill"]))),
    }


def render_yaml(value: dict[str, object]) -> str:
    return yaml.safe_dump(value, sort_keys=False, allow_unicode=False)


def render_js(value: dict[str, object]) -> str:
    payload = json.dumps(value, indent=2, sort_keys=True)
    return "// Generated by scripts/build-skill-routing.py. Do not edit by hand.\nwindow.DEV_METHODOLOGY_TECHNOLOGY_SKILL_REGISTRY = " + payload + ";\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and validate the portable skill routing registry.")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    entries = load_routing()
    validate_complete_coverage(entries)
    validate_generic_skill_text(entries)
    validate_role_loadouts(entries)
    value = registry(entries)
    outputs = {REGISTRY_YAML: render_yaml(value), REGISTRY_JS: render_js(value)}
    if args.check:
        stale = [str(path) for path, content in outputs.items() if not path.is_file() or path.read_text(encoding="utf-8") != content]
        if stale:
            for path in stale:
                print(f"stale {path}")
            return 1
        print("Technology skill registry is current.")
        return 0
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"generated {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
