#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import shutil
import sys
from pathlib import Path

import yaml


SKILL_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = Path(__file__).resolve().parents[1] / "references" / "technology-skill-registry.yaml"
IGNORED_PARTS = {".git", ".next", "dist", "node_modules", "target"}


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


def candidate_files(root: Path, scopes: list[Path]) -> list[Path]:
    files: set[Path] = set()
    for scope in scopes:
        path = scope if scope.is_absolute() else root / scope
        if path.is_file():
            files.add(path)
        elif path.is_dir():
            for child in path.rglob("*"):
                if child.is_file() and not (set(child.relative_to(root).parts) & IGNORED_PARTS):
                    files.add(child)
    return sorted(files)


def project_files(root: Path) -> list[Path]:
    return sorted(
        path for path in root.rglob("*")
        if path.is_file() and not (set(path.relative_to(root).parts) & IGNORED_PARTS)
    )


def scoped_evidence_files(root: Path, scopes: list[Path], scope_files: list[Path], all_files: list[Path]) -> list[Path]:
    evidence = set(scope_files)
    directories: set[Path] = set()
    for scope in scopes:
        path = scope if scope.is_absolute() else root / scope
        current = path.parent if path.is_file() else path
        if not current.exists():
            current = current.parent
        while current == root or root in current.parents:
            directories.add(current)
            if current == root:
                break
            current = current.parent
    evidence.update(path for path in all_files if path.parent in directories)
    return sorted(evidence)


def nearest_dependency_manifests(root: Path, scopes: list[Path], scope_files: list[Path]) -> list[Path]:
    manifests: set[Path] = set()
    candidates = scope_files or [scope if scope.is_absolute() else root / scope for scope in scopes]
    for candidate in candidates:
        current = candidate.parent if candidate.is_file() else candidate
        if not current.exists():
            current = current.parent
        while current == root or root in current.parents:
            manifest = current / "package.json"
            if manifest.is_file():
                manifests.add(manifest)
                break
            if current == root:
                break
            current = current.parent
    return sorted(manifests)


def package_dependencies(files: list[Path]) -> set[str]:
    dependencies: set[str] = set()
    for path in files:
        if path.name != "package.json":
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for field in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
            value = data.get(field, {})
            if isinstance(value, dict):
                dependencies.update(str(name) for name in value)
    return dependencies


def matches(
    entry: dict[str, object],
    root: Path,
    scope_files: list[Path],
    evidence_files: list[Path],
    dependency_manifests: list[Path],
) -> list[str]:
    activation = entry.get("activation", {})
    scope_groups: list[list[str]] = []
    project_groups: list[list[str]] = []
    relative_scope = [relative(path, root) for path in scope_files]
    extensions = set(activation.get("fileExtensions", []))
    if extensions:
        group = [
            f"scope extension {path.suffix.lower()}: {relative(path, root)}"
            for path in scope_files
            if path.suffix.lower() in extensions
        ]
        scope_groups.append(group[:1])
    file_globs = activation.get("fileGlobs", [])
    if file_globs:
        group: list[str] = []
        for pattern in file_globs:
            match = next((value for value in relative_scope if fnmatch.fnmatch(value, pattern)), None)
            if match:
                group.append(f"scope path {pattern}: {match}")
        scope_groups.append(group)
    evidence_relative = [relative(path, root) for path in evidence_files]
    manifest_files = activation.get("manifestFiles", [])
    if manifest_files:
        group = []
        for pattern in manifest_files:
            match = next((value for value in evidence_relative if fnmatch.fnmatch(value, pattern) or fnmatch.fnmatch(Path(value).name, pattern)), None)
            if match:
                group.append(f"project marker {pattern}: {match}")
        project_groups.append(group)
    dependencies = package_dependencies(dependency_manifests)
    manifest_dependencies = activation.get("manifestDependencies", [])
    if manifest_dependencies:
        project_groups.append([
            f"manifest dependency: {dependency}"
            for dependency in manifest_dependencies
            if dependency in dependencies
        ])
    content_patterns = activation.get("contentPatterns", [])
    if content_patterns:
        group = []
        for pattern in content_patterns:
            for path in evidence_files:
                value = relative(path, root)
                if not fnmatch.fnmatch(value, pattern["glob"]) and not fnmatch.fnmatch(path.name, pattern["glob"]):
                    continue
                try:
                    text = path.read_text(encoding="utf-8")
                except (OSError, UnicodeDecodeError):
                    continue
                if pattern["contains"] in text:
                    group.append(f"content {pattern['contains']}: {value}")
                    break
        project_groups.append(group)
    commands = activation.get("commands", [])
    if commands:
        group = []
        for command in commands:
            location = shutil.which(command)
            if location:
                group.append(f"available command {command}: {location}")
        project_groups.append(group)
    if not scope_groups and not project_groups:
        return []
    scope_evidence = [item for group in scope_groups for item in group]
    project_evidence = [item for group in project_groups for item in group]
    if scope_groups and not scope_evidence:
        return []
    if project_groups and not project_evidence:
        return []
    return scope_evidence + project_evidence


def binding_matches(pattern: str, scope_paths: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) or path.startswith(pattern.rstrip("/**") + "/") for path in scope_paths)


def project_bindings(plan_path: Path | None, scope_paths: list[str]) -> tuple[dict[str, list[str]], list[dict[str, object]]]:
    bindings: dict[str, list[str]] = {}
    invalid: list[dict[str, object]] = []
    if plan_path is None or not plan_path.is_file():
        return bindings, invalid
    plan = load_yaml(plan_path)
    for item in plan.get("skill_loadouts", []):
        if not isinstance(item, dict):
            continue
        patterns = item.get("paths", [])
        if any(isinstance(pattern, str) and binding_matches(pattern, scope_paths) for pattern in patterns):
            activation_evidence = [value for value in item.get("activation_evidence", []) if isinstance(value, str) and value.strip()]
            for skill in item.get("skills", []):
                if isinstance(skill, str):
                    if not activation_evidence:
                        invalid.append({"skill": skill, "required": True, "reason": ["AGENTS-PLAN skill_loadout lacks activation_evidence"]})
                    else:
                        bindings.setdefault(skill, []).extend([
                            f"AGENTS-PLAN skill_loadouts: {item.get('scope', 'unnamed scope')}",
                            *[f"binding evidence: {value}" for value in activation_evidence],
                        ])
    for item in plan.get("folder_routing", []):
        if not isinstance(item, dict) or not isinstance(item.get("pattern"), str):
            continue
        if binding_matches(item["pattern"], scope_paths):
            source_evidence = [
                f"{value.get('path')}: {value.get('fact')}"
                for value in item.get("source_evidence", [])
                if isinstance(value, dict) and value.get("path") and value.get("fact")
            ]
            for skill in item.get("required_skills", []):
                if isinstance(skill, str):
                    if not source_evidence:
                        invalid.append({"skill": skill, "required": True, "reason": ["AGENTS-PLAN folder_routing lacks source_evidence"]})
                    else:
                        bindings.setdefault(skill, []).extend([
                            f"AGENTS-PLAN folder_routing: {item['pattern']}",
                            *[f"binding evidence: {value}" for value in source_evidence],
                        ])
    return bindings, invalid


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve(args: argparse.Namespace) -> tuple[dict[str, object], int]:
    root = args.project_root.resolve()
    scopes = [Path(value) for value in args.scope]
    scope_files = candidate_files(root, scopes)
    all_files = project_files(root)
    evidence_files = scoped_evidence_files(root, scopes, scope_files, all_files)
    dependency_manifests = nearest_dependency_manifests(root, scopes, scope_files)
    scope_paths = [relative((value if value.is_absolute() else root / value), root) for value in scopes]
    binding_paths = sorted(set(scope_paths + [relative(path, root) for path in scope_files]))
    registry = load_yaml(args.registry)
    entries = {str(item["skill"]): item for item in registry["skills"]}
    plan_path = args.agents_plan or ((root / "AGENTS-PLAN.yaml") if (root / "AGENTS-PLAN.yaml").is_file() else None)
    bindings, invalid_bindings = project_bindings(plan_path, binding_paths)
    selected: dict[str, dict[str, object]] = {}
    missing: list[dict[str, object]] = list(invalid_bindings)
    conflicts: list[dict[str, object]] = []
    for skill, reasons in bindings.items():
        entry = entries.get(skill)
        if entry is None:
            missing.append({"skill": skill, "required": True, "reason": reasons})
            continue
        live_evidence = matches(entry, root, scope_files, evidence_files, dependency_manifests)
        if scope_files and entry.get("kind") != "generic" and not live_evidence:
            conflicts.append({"group": "project-binding", "skills": [skill], "reason": "binding contradicts live scoped evidence"})
            continue
        selected[skill] = {"entry": entry, "evidence": reasons + live_evidence, "source": "project-binding", "required": True}
    for skill, entry in entries.items():
        roles = entry.get("applicableRoles", [])
        if roles and args.role not in roles:
            continue
        evidence = matches(entry, root, scope_files, evidence_files, dependency_manifests)
        if evidence:
            selected.setdefault(skill, {"entry": entry, "evidence": [], "source": "repository-evidence", "required": bool(entry.get("requiredWhenMatched", True))})
            selected[skill]["evidence"] = sorted(set(selected[skill]["evidence"] + evidence))
    pending_companions = list(selected)
    while pending_companions:
        owner = pending_companions.pop()
        owner_entry = selected[owner]["entry"]
        for companion in owner_entry.get("companions", []):
            if companion in selected:
                continue
            companion_entry = entries.get(companion)
            if companion_entry is None:
                missing.append({"skill": companion, "required": True, "reason": [f"companion of {owner}"]})
                continue
            selected[companion] = {
                "entry": companion_entry,
                "evidence": [f"companion of {owner}"],
                "source": "companion",
                "required": True,
            }
            pending_companions.append(companion)
    groups: dict[str, list[str]] = {}
    for skill, value in selected.items():
        entry = value["entry"]
        if entry.get("selection") == "exclusive":
            groups.setdefault(str(entry["exclusiveGroup"]), []).append(skill)
    for group, members in groups.items():
        if len(members) > 1:
            highest = min(int(selected[member]["entry"]["priority"]) for member in members)
            winners = [member for member in members if int(selected[member]["entry"]["priority"]) == highest]
            if len(winners) != 1:
                conflicts.append({"group": group, "skills": sorted(members), "reason": "equal-priority exclusive matches"})
            else:
                winner = winners[0]
                for member in members:
                    if member != winner:
                        selected.pop(member)
    confirmed = dict(item.split("=", 1) for item in args.confirm_read)
    resolved: list[dict[str, object]] = []
    for skill, value in sorted(selected.items(), key=lambda item: (int(item[1]["entry"]["priority"]), item[0])):
        skill_file = args.skills_root / skill / "SKILL.md"
        available = skill_file.is_file()
        content_digest = digest(skill_file) if available else None
        read_confirmed = available and confirmed.get(skill) == content_digest
        item = {
            "skill": skill,
            "kind": value["entry"]["kind"],
            "capabilities": value["entry"]["capabilities"],
            "required": value["required"],
            "source": value["source"],
            "evidence": value["evidence"],
            "skillFile": str(skill_file),
            "available": available,
            "contentDigest": content_digest,
            "readConfirmed": read_confirmed,
        }
        resolved.append(item)
        if value["required"] and not available:
            missing.append({"skill": skill, "required": True, "reason": value["evidence"]})
    if args.require_confirmed:
        for item in resolved:
            if item["required"] and not item["readConfirmed"]:
                missing.append({"skill": item["skill"], "required": True, "reason": ["read confirmation missing or digest does not match"]})
    expected_capabilities = registry.get("roleCapabilityExpectations", {}).get(args.role, [])
    resolved_capabilities = {
        capability
        for item in resolved
        for capability in item["capabilities"]
    }
    unbundled_capabilities = sorted(set(expected_capabilities) - resolved_capabilities)
    status = "BLOCKED" if missing or conflicts else "READY_WITH_GAPS" if unbundled_capabilities else "READY"
    receipt = {
        "schema": "dev-methodology-skill-routing-receipt",
        "version": 1,
        "role": args.role,
        "projectRoot": str(root),
        "scope": scope_paths,
        "agentsPlan": str(plan_path) if plan_path else None,
        "resolved": resolved,
        "missing": missing,
        "conflicts": conflicts,
        "unbundledCapabilities": unbundled_capabilities,
        "fallbackPolicy": "Use generic role guidance and model knowledge while explicitly reporting that no bundled specialized variant matched." if unbundled_capabilities else None,
        "proofBoundary": "Selection, availability, digest, and explicit read confirmation are recorded. Harness tool-call evidence is required to prove the agent read each file.",
        "status": status,
    }
    return receipt, 2 if missing or conflicts else 0


def markdown(receipt: dict[str, object]) -> str:
    lines = ["# Skill Routing Receipt", "", f"Status: {receipt['status']}", f"Role: {receipt['role']}", "", "## Scope", ""]
    lines.extend(f"- {path}" for path in receipt["scope"])
    lines.extend(["", "## Resolved Skills", ""])
    if not receipt["resolved"]:
        lines.append("- None")
    for item in receipt["resolved"]:
        lines.append(f"- {item['skill']}: available={str(item['available']).lower()}, read-confirmed={str(item['readConfirmed']).lower()}, required={str(item['required']).lower()}")
        lines.extend(f"  - Evidence: {value}" for value in item["evidence"])
        lines.append(f"  - Digest: {item['contentDigest'] or 'unavailable'}")
    lines.extend(["", "## Missing Or Conflicting", ""])
    if not receipt["missing"] and not receipt["conflicts"] and not receipt["unbundledCapabilities"]:
        lines.append("- None")
    lines.extend(f"- Missing {item['skill']}: {', '.join(item['reason'])}" for item in receipt["missing"])
    lines.extend(f"- Conflict {item['group']}: {', '.join(item['skills'])}" for item in receipt["conflicts"])
    lines.extend(f"- No bundled specialized variant matched capability: {capability}" for capability in receipt["unbundledCapabilities"])
    if receipt["fallbackPolicy"]:
        lines.append(f"- Fallback: {receipt['fallbackPolicy']}")
    lines.extend(["", "## Proof Boundary", "", str(receipt["proofBoundary"]), ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve specialized skills from project bindings and repository evidence.")
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--role", required=True)
    parser.add_argument("--scope", action="append", required=True)
    parser.add_argument("--agents-plan", type=Path)
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--skills-root", type=Path, default=SKILL_ROOT)
    parser.add_argument("--confirm-read", action="append", default=[])
    parser.add_argument("--require-confirmed", action="store_true")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args()
    receipt, exit_code = resolve(args)
    print(markdown(receipt) if args.format == "markdown" else json.dumps(receipt, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
