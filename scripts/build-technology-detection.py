#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Validates technology detection definitions and generates their portable registry and detector mirror.
# Design: design/technology-skill-detection-spec.md

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
DETECTOR_SKILL = SKILLS_ROOT / "detect-technology-skills"
REGISTRY_YAML = DETECTOR_SKILL / "references" / "technology-skill-detection-registry.yaml"
REGISTRY_JS = ROOT / "design" / "generated" / "technology-skill-detection-registry.js"
SOURCE_DETECTOR = ROOT / "scripts" / "detect-technology-skills.py"
INSTALLED_DETECTOR = DETECTOR_SKILL / "scripts" / "detect.py"
DETECTION_FILE = "detection.yaml"
ALLOWED_KINDS = {"technology", "domain"}
ALLOWED_SELECTIONS = {"additive", "exclusive"}
SCHEMA = "dev-methodology-technology-detection"
SCHEMA_VERSION = 2
COMPOSITE_KEYS = {"allOf", "anyOf"}
STRING_PREDICATES = {"fileExtension", "fileGlob", "manifestFile", "owningDependency"}
MAPPING_PREDICATES = {"contentPattern", "fileMatch", "sourceImport"}


def load_yaml(path: Path) -> dict[str, object]:
    """Load one YAML mapping so malformed source definitions fail validation."""
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a YAML mapping: {path}")
    return value


def role_skill_names(role: dict[str, object]) -> list[str]:
    """Return source skill identifiers from string and justified role entries."""
    value = role.get("skills")
    if not isinstance(value, list):
        raise ValueError(f"Role {role.get('name')} skills must be a list.")
    names: list[str] = []
    for item in value:
        if isinstance(item, str):
            names.append(item)
        elif isinstance(item, dict) and len(item) == 1:
            names.append(str(next(iter(item))))
        else:
            raise ValueError(f"Role {role.get('name')} has an invalid skill entry: {item}")
    return names


def skill_names() -> set[str]:
    """Return every bundled skill identifier available to detection definitions."""
    return {path.parent.name for path in SKILLS_ROOT.glob("*/SKILL.md")}


def validate_string_list(value: object, field: str, path: Path, *, allow_empty: bool = True) -> list[str]:
    """Validate a YAML list whose values must be non-empty strings."""
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise ValueError(f"{field} must be a list of non-empty strings: {path}")
    if not allow_empty and not value:
        raise ValueError(f"{field} must not be empty: {path}")
    return list(value)


def validate_mapping_predicate(key: str, value: object, field: str, path: Path) -> dict[str, object]:
    """Validate predicates that bind multiple values to one observed artifact."""
    if not isinstance(value, dict):
        raise ValueError(f"{field}.{key} must be a mapping: {path}")
    required = {
        "contentPattern": ("glob", "contains"),
        "fileMatch": ("glob", "extensions"),
        "sourceImport": ("module", "extensions"),
    }[key]
    if set(value) != set(required):
        raise ValueError(f"{field}.{key} requires {sorted(required)}: {path}")
    normalized: dict[str, object] = {}
    for name in required:
        item = value[name]
        if name == "extensions":
            extensions = validate_string_list(item, f"{field}.{key}.extensions", path, allow_empty=False)
            if any(not extension.startswith(".") for extension in extensions):
                raise ValueError(f"{field}.{key}.extensions values must start with a period: {path}")
            if key == "sourceImport" and any(extension not in {".py", ".pyi"} for extension in extensions):
                raise ValueError(f"{field}.sourceImport currently supports Python extensions only: {path}")
            normalized[name] = extensions
        elif not isinstance(item, str) or not item:
            raise ValueError(f"{field}.{key}.{name} must be a non-empty string: {path}")
        else:
            normalized[name] = item
    return normalized


def validate_clause(value: object, field: str, path: Path) -> dict[str, object]:
    """Validate one recursive activation clause with exactly one operator or predicate."""
    if not isinstance(value, dict) or len(value) != 1:
        raise ValueError(f"{field} must contain exactly one activation key: {path}")
    key, item = next(iter(value.items()))
    if key in COMPOSITE_KEYS:
        if not isinstance(item, list) or not item:
            raise ValueError(f"{field}.{key} must be a non-empty list: {path}")
        return {key: [validate_clause(child, f"{field}.{key}", path) for child in item]}
    if key in STRING_PREDICATES:
        if not isinstance(item, str) or not item:
            raise ValueError(f"{field}.{key} must be a non-empty string: {path}")
        if key == "fileExtension" and not item.startswith("."):
            raise ValueError(f"{field}.fileExtension must start with a period: {path}")
        return {key: item}
    if key in MAPPING_PREDICATES:
        return {key: validate_mapping_predicate(key, item, field, path)}
    raise ValueError(f"Unknown activation key {key}: {path}")


def validate_activation(value: object, path: Path) -> dict[str, object]:
    """Validate the root any-of activation rule used to select one named skill."""
    normalized = validate_clause(value, "activation", path)
    if set(normalized) != {"anyOf"}:
        raise ValueError(f"activation must use anyOf as its root clause: {path}")
    return normalized


def load_detection_entries() -> list[dict[str, object]]:
    """Load and normalize every specialized skill detection definition."""
    available_skills = skill_names()
    entries: list[dict[str, object]] = []
    for path in sorted(SKILLS_ROOT.glob(f"*/{DETECTION_FILE}")):
        entry = load_yaml(path)
        if entry.get("schema") != SCHEMA or entry.get("version") != SCHEMA_VERSION:
            raise ValueError(f"Unsupported detection schema or version: {path}")
        allowed_fields = {
            "schema", "version", "skill", "kind", "label", "capabilities", "activation",
            "companions", "selection", "exclusiveGroup", "priority", "requiredWhenDetected",
        }
        unexpected_fields = sorted(set(entry) - allowed_fields)
        if unexpected_fields:
            raise ValueError(f"Unknown technology detection fields {unexpected_fields}: {path}")
        skill = entry.get("skill")
        if skill != path.parent.name or skill not in available_skills:
            raise ValueError(f"Detection skill must match an existing skill directory: {path}")
        kind = entry.get("kind")
        if kind not in ALLOWED_KINDS:
            raise ValueError(f"Technology detection only accepts technology or domain skills: {path}")
        label = entry.get("label")
        if not isinstance(label, str) or not label:
            raise ValueError(f"label must be a non-empty string: {path}")
        capabilities = validate_string_list(entry.get("capabilities"), "capabilities", path, allow_empty=False)
        companions = validate_string_list(entry.get("companions", []), "companions", path)
        unknown_companions = sorted(set(companions) - available_skills)
        if unknown_companions:
            raise ValueError(f"Unknown companion skills {unknown_companions}: {path}")
        selection = entry.get("selection", "additive")
        if selection not in ALLOWED_SELECTIONS:
            raise ValueError(f"Unknown selection mode {selection}: {path}")
        exclusive_group = entry.get("exclusiveGroup")
        if selection == "exclusive" and (not isinstance(exclusive_group, str) or not exclusive_group):
            raise ValueError(f"Exclusive detection needs exclusiveGroup: {path}")
        if selection == "additive" and exclusive_group is not None:
            raise ValueError(f"Additive detection cannot define exclusiveGroup: {path}")
        priority = entry.get("priority", 100)
        if not isinstance(priority, int):
            raise ValueError(f"priority must be an integer: {path}")
        normalized = {
            "skill": skill,
            "kind": kind,
            "label": label,
            "capabilities": capabilities,
            "activation": validate_activation(entry.get("activation"), path),
            "companions": companions,
            "selection": selection,
            "priority": priority,
            "requiredWhenDetected": bool(entry.get("requiredWhenDetected", True)),
        }
        if exclusive_group is not None:
            normalized["exclusiveGroup"] = exclusive_group
        entries.append(normalized)
    return entries


def validate_complete_coverage(entries: list[dict[str, object]]) -> None:
    """Require every stack-and-domain skill to declare setup-time detection metadata."""
    detected = {str(entry["skill"]) for entry in entries}
    specialized: set[str] = set()
    for path in SKILLS_ROOT.glob("*/SKILL.md"):
        frontmatter = yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1])
        if frontmatter.get("metadata", {}).get("category") == "stack-and-domain":
            specialized.add(path.parent.name)
    missing = sorted(specialized - detected)
    if missing:
        raise ValueError(f"Specialized skills missing detection metadata: {missing}")


def validate_fixed_role_loadouts(entries: list[dict[str, object]]) -> None:
    """Reject specialized detected skills from technology-neutral fixed role loadouts."""
    specialized = {str(entry["skill"]) for entry in entries}
    violations: list[str] = []
    for path in sorted((ROOT / "agents" / "roles").glob("*/*.role.yaml")):
        role = load_yaml(path)
        fixed_names = set(role_skill_names(role))
        fixed = sorted(fixed_names & specialized)
        if fixed:
            violations.append(f"{role['name']}: {', '.join(fixed)}")
    if violations:
        raise ValueError("Roles contain detected technology skills: " + "; ".join(violations))


def registry(entries: list[dict[str, object]]) -> dict[str, object]:
    """Build the portable registry document consumed by the detector and design pages."""
    return {
        "schema": "dev-methodology-technology-skill-detection-registry",
        "version": SCHEMA_VERSION,
        "selectionPolicy": {
            "scopeEvidence": "deterministic",
            "missingRequiredSkill": "blocked",
            "exclusiveConflict": "blocked",
            "noVariant": "explicit-empty-loadout",
        },
        "skills": sorted(entries, key=lambda item: (int(item["priority"]), str(item["skill"]))),
    }


def render_js(value: dict[str, object]) -> str:
    """Render the registry as deterministic browser data for static design pages."""
    payload = json.dumps(value, indent=2, sort_keys=True)
    return (
        "// Copyright (c) 2026 Martin.Bechard@DevConsult.ca\n"
        "// AI attribution: Generated with AI assistance.\n"
        "// Summary: Provides deterministic generated technology-skill detection data to static design pages.\n"
        "// Generated by scripts/build-technology-detection.py. Do not edit by hand.\n"
        "window.DEV_METHODOLOGY_TECHNOLOGY_SKILL_DETECTION_REGISTRY = " + payload + ";\n"
    )


def expected_outputs(entries: list[dict[str, object]]) -> dict[Path, str]:
    """Return every generated output and its expected content for build or check mode."""
    value = registry(entries)
    return {
        REGISTRY_YAML: yaml.safe_dump(value, sort_keys=False, allow_unicode=False),
        REGISTRY_JS: render_js(value),
        INSTALLED_DETECTOR: SOURCE_DETECTOR.read_text(encoding="utf-8"),
    }


def main() -> int:
    """Validate source definitions and write or check all generated detection artifacts."""
    parser = argparse.ArgumentParser(description="Build and validate setup-time technology detection artifacts.")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        entries = load_detection_entries()
        validate_complete_coverage(entries)
        validate_fixed_role_loadouts(entries)
        outputs = expected_outputs(entries)
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(error, file=sys.stderr)
        return 1
    stale = [path for path, content in outputs.items() if not path.is_file() or path.read_text(encoding="utf-8") != content]
    if args.check:
        for path in stale:
            print(f"stale {path}")
        if stale:
            return 1
        print("Technology detection artifacts are current.")
        return 0
    for path in stale:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(outputs[path], encoding="utf-8")
        print(f"generated {path}")
    if not stale:
        print("Technology detection artifacts are current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
