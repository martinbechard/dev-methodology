#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
import tomllib
from pathlib import Path

import yaml


HERE = Path(__file__).resolve()
if HERE.parent.name == "scripts" and HERE.parents[1].name == "detect-technology-skills":
    DEFAULT_SKILLS_ROOT = HERE.parents[2]
    DEFAULT_REGISTRY = HERE.parents[1] / "references" / "technology-skill-detection-registry.yaml"
else:
    REPOSITORY_ROOT = HERE.parents[1]
    DEFAULT_SKILLS_ROOT = REPOSITORY_ROOT / "skills"
    DEFAULT_REGISTRY = DEFAULT_SKILLS_ROOT / "detect-technology-skills" / "references" / "technology-skill-detection-registry.yaml"

IGNORED_PARTS = {".git", ".next", ".venv", "__pycache__", "dist", "node_modules", "target", "venv"}
OWNER_FILE_NAMES = {"package.json", "pom.xml", "pyproject.toml"}
OWNER_FILE_GLOBS = ("build.gradle*", "requirements*.txt")


def load_yaml(path: Path) -> dict[str, object]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a YAML mapping: {path}")
    return value


def relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def is_ignored(path: Path, root: Path) -> bool:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return True
    return bool(set(parts) & IGNORED_PARTS)


def scope_files(root: Path, scope: Path) -> list[Path]:
    path = scope if scope.is_absolute() else root / scope
    if path.is_file():
        return [path]
    if not path.is_dir():
        return []
    return sorted(child for child in path.rglob("*") if child.is_file() and not is_ignored(child, root))


def owner_files(directory: Path) -> list[Path]:
    found = [directory / name for name in OWNER_FILE_NAMES if (directory / name).is_file()]
    for pattern in OWNER_FILE_GLOBS:
        found.extend(path for path in directory.glob(pattern) if path.is_file())
    return sorted(set(found))


def nearest_owner_files(root: Path, scope: Path, files: list[Path]) -> list[Path]:
    candidates = files or [scope if scope.is_absolute() else root / scope]
    owners: set[Path] = set()
    for candidate in candidates:
        current = candidate.parent if candidate.is_file() else candidate
        if not current.exists():
            current = current.parent
        while current == root or root in current.parents:
            matches = owner_files(current)
            if matches:
                owners.update(matches)
                break
            if current == root:
                break
            current = current.parent
    return sorted(owners)


def manifest_dependencies(paths: list[Path]) -> set[str]:
    dependencies: set[str] = set()
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if path.name == "package.json":
            try:
                value = json.loads(text)
            except json.JSONDecodeError:
                continue
            for field in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
                if isinstance(value.get(field), dict):
                    dependencies.update(str(name) for name in value[field])
        elif path.name == "pyproject.toml":
            try:
                value = tomllib.loads(text)
            except tomllib.TOMLDecodeError:
                continue
            project = value.get("project", {})
            for item in project.get("dependencies", []) if isinstance(project, dict) else []:
                if isinstance(item, str):
                    dependencies.add(re.split(r"[<>=!~;\s\[]", item, maxsplit=1)[0].lower())
            optional = project.get("optional-dependencies", {}) if isinstance(project, dict) else {}
            if isinstance(optional, dict):
                for items in optional.values():
                    for item in items if isinstance(items, list) else []:
                        if isinstance(item, str):
                            dependencies.add(re.split(r"[<>=!~;\s\[]", item, maxsplit=1)[0].lower())
            poetry = value.get("tool", {}).get("poetry", {}).get("dependencies", {})
            if isinstance(poetry, dict):
                dependencies.update(str(name).lower() for name in poetry if str(name).lower() != "python")
        elif fnmatch.fnmatch(path.name, "requirements*.txt"):
            for line in text.splitlines():
                item = line.strip()
                if item and not item.startswith(("#", "-")):
                    dependencies.add(re.split(r"[<>=!~;\s\[]", item, maxsplit=1)[0].lower())
    return dependencies


def activation_evidence(
    entry: dict[str, object],
    root: Path,
    files: list[Path],
    manifests: list[Path],
) -> list[str]:
    activation = entry.get("activation", {})
    scope_evidence: list[str] = []
    project_evidence: list[str] = []
    relative_files = [relative(path, root) for path in files]
    extensions = {str(value).lower() for value in activation.get("fileExtensions", [])}
    match = next((path for path in files if path.suffix.lower() in extensions), None)
    if match:
        scope_evidence.append(f"scope extension {match.suffix.lower()}: {relative(match, root)}")
    for pattern in activation.get("fileGlobs", []):
        matched = next((value for value in relative_files if fnmatch.fnmatch(value, str(pattern))), None)
        if matched:
            scope_evidence.append(f"scope path {pattern}: {matched}")
    owner_evidence = sorted(set(manifests + [child for path in manifests for child in path.parent.iterdir() if child.is_file()]))
    manifest_relative = [relative(path, root) for path in owner_evidence]
    for pattern in activation.get("manifestFiles", []):
        matched = next(
            (
                value for value in manifest_relative
                if fnmatch.fnmatch(value, str(pattern)) or fnmatch.fnmatch(Path(value).name, str(pattern))
            ),
            None,
        )
        if matched:
            project_evidence.append(f"owning manifest {pattern}: {matched}")
    dependencies = manifest_dependencies(manifests)
    for dependency in activation.get("manifestDependencies", []):
        if str(dependency).lower() in dependencies:
            project_evidence.append(f"owning manifest dependency {dependency}")
    content_files = sorted(set(files + owner_evidence))
    for pattern in activation.get("contentPatterns", []):
        for path in content_files:
            value = relative(path, root)
            if not fnmatch.fnmatch(value, str(pattern["glob"])) and not fnmatch.fnmatch(path.name, str(pattern["glob"])):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if str(pattern["contains"]) in text:
                project_evidence.append(f"content {pattern['contains']}: {value}")
                break
    has_scope_selectors = bool(activation.get("fileExtensions") or activation.get("fileGlobs"))
    has_project_signals = bool(
        activation.get("manifestFiles")
        or activation.get("manifestDependencies")
        or activation.get("contentPatterns")
    )
    if has_scope_selectors and not scope_evidence:
        return []
    if has_project_signals and not project_evidence:
        return []
    return scope_evidence + project_evidence


def detect_scope(
    root: Path,
    scope: Path,
    registry: dict[str, object],
    skills_root: Path,
) -> dict[str, object]:
    target = (scope if scope.is_absolute() else root / scope).resolve()
    try:
        scope_value = target.relative_to(root).as_posix()
    except ValueError:
        scope_value = target.as_posix()
        return {
            "scope": scope_value,
            "pathPattern": scope_value,
            "skills": [],
            "sourceEvidence": [],
            "missingRequiredSkills": [],
            "exclusiveConflicts": [],
            "scopeErrors": ["scope resolves outside the project root"],
            "status": "BLOCKED",
        }
    if not target.exists():
        return {
            "scope": scope_value,
            "pathPattern": scope_value,
            "skills": [],
            "sourceEvidence": [],
            "missingRequiredSkills": [],
            "exclusiveConflicts": [],
            "scopeErrors": ["scope does not exist"],
            "status": "BLOCKED",
        }
    files = scope_files(root, scope)
    manifests = nearest_owner_files(root, scope, files)
    owner_directories = sorted({path.parent for path in manifests})
    if len(owner_directories) > 1:
        return {
            "scope": scope_value,
            "pathPattern": scope_value + ("/**" if target.is_dir() else ""),
            "skills": [],
            "sourceEvidence": [],
            "missingRequiredSkills": [],
            "exclusiveConflicts": [],
            "scopeErrors": [
                "scope spans multiple owning manifest directories; analyze each owner separately: "
                + ", ".join(relative(path, root) for path in owner_directories)
            ],
            "status": "BLOCKED",
        }
    entries = {str(item["skill"]): item for item in registry.get("skills", [])}
    selected: dict[str, dict[str, object]] = {}
    missing: list[dict[str, object]] = []
    conflicts: list[dict[str, object]] = []
    for skill, entry in entries.items():
        evidence = activation_evidence(entry, root, files, manifests)
        if evidence:
            selected[skill] = {
                "entry": entry,
                "evidence": evidence,
                "source": "scope-evidence",
                "required": bool(entry.get("requiredWhenDetected", True)),
            }
    pending = list(selected)
    while pending:
        owner = pending.pop()
        for companion in selected[owner]["entry"].get("companions", []):
            if companion in selected:
                continue
            companion_entry = entries.get(str(companion))
            if companion_entry is None:
                missing.append({"skill": companion, "reason": f"required companion of {owner}"})
                continue
            selected[str(companion)] = {
                "entry": companion_entry,
                "evidence": [f"companion of {owner}"],
                "source": "companion",
                "required": True,
            }
            pending.append(str(companion))
    groups: dict[str, list[str]] = {}
    for skill, value in selected.items():
        entry = value["entry"]
        if entry.get("selection") == "exclusive":
            groups.setdefault(str(entry["exclusiveGroup"]), []).append(skill)
    for group, members in groups.items():
        if len(members) < 2:
            continue
        highest = min(int(selected[member]["entry"]["priority"]) for member in members)
        winners = [member for member in members if int(selected[member]["entry"]["priority"]) == highest]
        if len(winners) != 1:
            conflicts.append({"group": group, "skills": sorted(members), "reason": "equal-priority exclusive matches"})
        else:
            for member in members:
                if member != winners[0]:
                    selected.pop(member)
    evidence_rows: list[dict[str, object]] = []
    skills: list[str] = []
    for skill, value in sorted(selected.items(), key=lambda item: (int(item[1]["entry"]["priority"]), item[0])):
        skill_file = skills_root / skill / "SKILL.md"
        if value["required"] and not skill_file.is_file():
            missing.append({"skill": skill, "reason": "detected required skill is unavailable"})
        skills.append(skill)
        evidence_rows.append({"skill": skill, "source": value["source"], "evidence": value["evidence"]})
    status = "BLOCKED" if missing or conflicts else "NO_VARIANT" if not skills else "READY"
    pattern = scope_value if any(char in scope_value for char in "*?[") else scope_value.rstrip("/") + ("/**" if target.is_dir() else "")
    return {
        "scope": scope_value,
        "pathPattern": pattern,
        "skills": skills,
        "sourceEvidence": evidence_rows,
        "missingRequiredSkills": missing,
        "exclusiveConflicts": conflicts,
        "scopeErrors": [],
        "status": status,
    }


def detect(args: argparse.Namespace) -> tuple[dict[str, object], int]:
    root = args.project_root.resolve()
    registry = load_yaml(args.registry)
    loadouts = [detect_scope(root, Path(value), registry, args.skills_root) for value in args.scope]
    blocked = any(item["status"] == "BLOCKED" for item in loadouts)
    result = {
        "schema": "dev-methodology-technology-skill-detection-result",
        "version": 1,
        "projectRoot": str(root),
        "loadouts": loadouts,
        "status": "BLOCKED" if blocked else "READY",
    }
    return result, 2 if blocked else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect setup-time technology skills for selected project folders.")
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--scope", action="append", required=True)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--skills-root", type=Path, default=DEFAULT_SKILLS_ROOT)
    parser.add_argument("--format", choices=("json", "yaml"), default="json")
    args = parser.parse_args()
    try:
        result, exit_code = detect(args)
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(error, file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True) if args.format == "json" else yaml.safe_dump(result, sort_keys=False), end="\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
