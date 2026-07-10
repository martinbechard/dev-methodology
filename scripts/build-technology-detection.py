#!/usr/bin/env python3
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
CANONICAL_DETECTOR = ROOT / "scripts" / "detect-technology-skills.py"
INSTALLED_DETECTOR = DETECTOR_SKILL / "scripts" / "detect.py"
DETECTION_FILE = "detection.yaml"
ALLOWED_KINDS = {"technology", "domain"}
ALLOWED_SELECTIONS = {"additive", "exclusive"}
SCHEMA = "dev-methodology-technology-detection"


def load_yaml(path: Path) -> dict[str, object]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a YAML mapping: {path}")
    return value


def role_skill_names(role: dict[str, object]) -> list[str]:
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
    return {path.parent.name for path in SKILLS_ROOT.glob("*/SKILL.md")}


def validate_string_list(value: object, field: str, path: Path, *, allow_empty: bool = True) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise ValueError(f"{field} must be a list of non-empty strings: {path}")
    if not allow_empty and not value:
        raise ValueError(f"{field} must not be empty: {path}")
    return list(value)


def validate_activation(value: object, path: Path) -> dict[str, list[object]]:
    if not isinstance(value, dict):
        raise ValueError(f"activation must be a mapping: {path}")
    allowed = {
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
                    raise ValueError(f"contentPatterns values must be non-empty strings: {path}")
                patterns.append(dict(item))
            normalized[key] = patterns
        else:
            normalized[key] = validate_string_list(items, f"activation.{key}", path)
    if not any(normalized.values()):
        raise ValueError(f"activation must contain evidence: {path}")
    return normalized


def load_detection_entries() -> list[dict[str, object]]:
    available_skills = skill_names()
    entries: list[dict[str, object]] = []
    for path in sorted(SKILLS_ROOT.glob(f"*/{DETECTION_FILE}")):
        entry = load_yaml(path)
        if entry.get("schema") != SCHEMA or entry.get("version") != 1:
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
    specialized = {str(entry["skill"]) for entry in entries}
    violations: list[str] = []
    for path in sorted((ROOT / "agents" / "roles").glob("*/*.role.yaml")):
        role = load_yaml(path)
        fixed_names = set(role_skill_names(role))
        fixed = sorted(fixed_names & specialized)
        if fixed:
            violations.append(f"{role['name']}: {', '.join(fixed)}")
    if violations:
        raise ValueError("Canonical roles contain detected technology skills: " + "; ".join(violations))


def registry(entries: list[dict[str, object]]) -> dict[str, object]:
    return {
        "schema": "dev-methodology-technology-skill-detection-registry",
        "version": 1,
        "selectionPolicy": {
            "scopeEvidence": "deterministic",
            "missingRequiredSkill": "blocked",
            "exclusiveConflict": "blocked",
            "noVariant": "explicit-empty-loadout",
        },
        "skills": sorted(entries, key=lambda item: (int(item["priority"]), str(item["skill"]))),
    }


def render_js(value: dict[str, object]) -> str:
    payload = json.dumps(value, indent=2, sort_keys=True)
    return (
        "// Generated by scripts/build-technology-detection.py. Do not edit by hand.\n"
        "window.DEV_METHODOLOGY_TECHNOLOGY_SKILL_DETECTION_REGISTRY = " + payload + ";\n"
    )


def expected_outputs(entries: list[dict[str, object]]) -> dict[Path, str]:
    value = registry(entries)
    return {
        REGISTRY_YAML: yaml.safe_dump(value, sort_keys=False, allow_unicode=False),
        REGISTRY_JS: render_js(value),
        INSTALLED_DETECTOR: CANONICAL_DETECTOR.read_text(encoding="utf-8"),
    }


def main() -> int:
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
