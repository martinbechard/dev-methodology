#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Renders project authority, claim transport, workflow, folder technology, and project skill guidance.

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
SKILL_FILE_NAME = "SKILL.md"
FRONTMATTER_DELIMITER = "---"
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")
AUTHORITY_HEADING = "## Agent And Skill Definition Approval"
CLAIM_TRANSPORT_HEADING = "## Agent Claim Transport"
PROJECT_SKILL_EXTENSIONS_HEADING = "## Project Skill Extensions"
CLAIM_TRANSPORT_SKILLS = {
    "mcp": "agent-claim-mcp",
    "command": "agent-claim-command",
}
PROVIDER_SKILLS = {
    "file": ("create-file-work-item", "manage-file-work-items"),
    "github": ("create-github-work-item", "manage-github-work-items"),
    "gitlab": ("create-gitlab-work-item", "manage-gitlab-work-items"),
    "azure-devops": ("create-azure-devops-work-item", "manage-azure-devops-work-items"),
    "jira": ("create-jira-work-item", "manage-jira-work-items"),
}
PROVIDER_VALUES = (*PROVIDER_SKILLS, "none", "UNSET")
COMPLETION_SKILLS = {
    "direct-main": "complete-work-item-direct-main",
    "feature-branch": "complete-work-item-feature-branch",
}
COMPLETION_VALUES = (*COMPLETION_SKILLS, "UNSET")
LEGACY_PROVIDER_VALUES = {
    "file-based-backlog": "file",
    "github-issues-backlog": "github",
    "none": "none",
    "UNSET": "UNSET",
}
LEGACY_COMPLETION_VALUES = {
    "simple-workitem": "direct-main",
    "feature-branch-workitem": "feature-branch",
    "UNSET": "UNSET",
}
PROVENANCE_REFERENCE_PATTERNS = {
    "user-message": re.compile(r"^thread:[^/\s]+/message:[^/\s]+$"),
    "delegated-user-direction": re.compile(r"^thread:[^/\s]+/delegation:[^/\s]+$"),
}
GOVERNED_SOURCE_CATEGORIES = (
    "conceptual_agents",
    "agent_definition_inputs",
    "distributed_skills",
    "adapter_skills",
    "skill_metadata",
)


def parse_boolean(value: str) -> bool:
    """Parse an explicit true-or-false command-line value."""

    normalized = value.lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise argparse.ArgumentTypeError("expected true or false")


def load_yaml(path: Path) -> dict[str, object]:
    """Load one PROJECT.yaml mapping from path."""
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a YAML mapping: {path}")
    return value


def loadouts(value: dict[str, object]) -> list[dict[str, object]]:
    """Return normalized technology skillset mappings from a project configuration."""
    rows = value.get("technology_skill_loadouts", value.get("loadouts", []))
    return [row for row in rows if isinstance(row, dict)] if isinstance(rows, list) else []


def _normalized_skill_id(value: object, field: str) -> str:
    """Return one lowercase, trimmed skill identifier or reject its exact field."""

    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must normalize to a lowercase hyphenated skill id")
    normalized = value.strip().lower()
    if not SKILL_NAME_PATTERN.fullmatch(normalized):
        raise ValueError(f"{field} must normalize to a lowercase hyphenated skill id")
    return normalized


def _definition_owned_skill_paths(value: dict[str, object]) -> dict[str, str]:
    """Return the first PROJECT.yaml field owning each valid role skill identifier."""

    owned: dict[str, str] = {}
    roles = value.get("role_agent_set", [])
    if not isinstance(roles, list):
        return owned
    for role_index, role in enumerate(roles):
        if not isinstance(role, Mapping):
            continue
        skills = role.get("skills", [])
        if isinstance(skills, list):
            for skill_index, skill in enumerate(skills):
                if not isinstance(skill, str):
                    continue
                normalized = skill.strip().lower()
                if SKILL_NAME_PATTERN.fullmatch(normalized):
                    owned.setdefault(
                        normalized,
                        f"role_agent_set[{role_index}].skills[{skill_index}]",
                    )
        conditional = role.get("conditional_skills", [])
        if isinstance(conditional, list):
            for skill_index, entry in enumerate(conditional):
                if not isinstance(entry, Mapping) or not isinstance(entry.get("skill"), str):
                    continue
                normalized = entry["skill"].strip().lower()
                if SKILL_NAME_PATTERN.fullmatch(normalized):
                    owned.setdefault(
                        normalized,
                        f"role_agent_set[{role_index}].conditional_skills[{skill_index}].skill",
                    )
    return owned


def _project_skill_extensions(value: dict[str, object]) -> list[str]:
    """Validate and return ordered, normalized root project skill references.

    PROJECT.yaml may omit project_skill_extensions or provide an empty list. Each list
    entry is either a bundled skill id string or a registered-skill mapping with exactly
    skill, registration, availability, and catalog. Registered entries are accepted only
    when setup recorded registration, runtime availability, and a non-empty catalog
    identifier. Normalized skill ids determine duplicate and definition-owned conflicts.
    The returned order matches the declared list order and no skill body is loaded.
    """

    if "project_skill_extensions" not in value:
        return []
    entries = value["project_skill_extensions"]
    if not isinstance(entries, list):
        raise ValueError(
            "project_skill_extensions must be a list; use [] when no project-level extension is selected"
        )

    normalized_entries: list[str] = []
    first_paths: dict[str, str] = {}
    for index, entry in enumerate(entries):
        prefix = f"project_skill_extensions[{index}]"
        registered = isinstance(entry, Mapping)
        if isinstance(entry, str):
            skill = _normalized_skill_id(entry, prefix)
        elif registered:
            if set(entry) != {"skill", "registration", "availability", "catalog"}:
                raise ValueError(
                    f"{prefix} keys must be exactly: skill, registration, availability, catalog"
                )
            skill = _normalized_skill_id(entry.get("skill"), f"{prefix}.skill")
        else:
            raise ValueError(
                f"{prefix} must be a bundled skill id string or a registered-skill mapping"
            )

        if skill in first_paths:
            raise ValueError(
                f"{prefix} skill id {skill!r} duplicates {first_paths[skill]}; remove the duplicate entry"
            )
        first_paths[skill] = prefix

        if registered:
            if entry.get("registration") != "registered":
                raise ValueError(
                    f"{prefix}.registration must be registered; use a bundled skill id string for bundled skills"
                )
            availability = entry.get("availability")
            if availability not in {"AVAILABLE", "UNAVAILABLE"}:
                raise ValueError(f"{prefix}.availability must be AVAILABLE or UNAVAILABLE")
            catalog = entry.get("catalog")
            if not isinstance(catalog, str) or not catalog.strip():
                raise ValueError(
                    f"{prefix}.catalog must be a non-empty registered catalog identifier"
                )
            if availability == "UNAVAILABLE":
                raise ValueError(
                    f"{prefix}.availability is UNAVAILABLE for skill {skill!r}; install or expose the registered skill, then set {prefix}.availability to AVAILABLE"
                )
        elif not (SKILLS_ROOT / skill / SKILL_FILE_NAME).is_file():
            raise ValueError(
                f"{prefix} unknown bundled skill id {skill!r}; use a bundled skill id or a registered-skill mapping"
            )
        normalized_entries.append(skill)

    definition_owned = _definition_owned_skill_paths(value)
    for index, skill in enumerate(normalized_entries):
        if skill in definition_owned:
            raise ValueError(
                f"project_skill_extensions[{index}] skill id {skill!r} duplicates definition-owned skill "
                f"{definition_owned[skill]}; remove it from project_skill_extensions"
            )
    return normalized_entries


def _project_skill_extension_lines(value: dict[str, object]) -> list[str]:
    """Render the final root-only, reference-only project skill section."""

    extensions = _project_skill_extensions(value)
    if not extensions:
        return []
    return [
        PROJECT_SKILL_EXTENSIONS_HEADING,
        "",
        "These references apply through the root AGENTS.md only. Load each selected skill completely in the declared order when starting project work. Skill definitions remain in their bundled or registered catalogs and are not copied here.",
        "",
        *(f"- {skill}" for skill in extensions),
        "",
    ]


def _required_boolean(mapping: dict[str, object], key: str, expected: bool, prefix: str) -> None:
    """Require one policy boolean to have its canonical value."""

    if mapping.get(key) is not expected:
        rendered = str(expected).lower()
        raise ValueError(f"{prefix}.{key} must be {rendered}")


def _required_patterns(mapping: dict[str, object], key: str, prefix: str) -> list[str]:
    """Return one non-empty list of project-relative path patterns."""

    patterns = mapping.get(key)
    if not isinstance(patterns, list) or not patterns or not all(isinstance(item, str) and item for item in patterns):
        raise ValueError(f"{prefix}.{key} must be a non-empty list of path patterns")
    return patterns


def _validated_path_patterns(mapping: dict[str, object], key: str, prefix: str) -> list[str]:
    """Return canonical, project-relative path patterns from one policy field."""

    patterns = _required_patterns(mapping, key, prefix)
    for pattern in patterns:
        field = f"{prefix}.{key} path pattern"
        try:
            normalized = _normalize_project_path(pattern)
        except ValueError as error:
            detail = str(error).removeprefix("definition path ")
            raise ValueError(f"{field} {detail}") from error
        if normalized != pattern:
            raise ValueError(f"{field} must be normalized: {pattern}")
    return patterns


def _require_exact_keys(mapping: dict[str, object], expected: tuple[str, ...], prefix: str) -> None:
    """Require a category mapping to contain exactly the supported keys."""

    if set(mapping) != set(expected):
        raise ValueError(f"{prefix} keys must be exactly: {', '.join(expected)}")


def definition_change_authority(value: dict[str, object]) -> dict[str, object] | None:
    """Validate and return the project-level definition-change authority mapping.

    Project Configurator and the renderer pass the mapping loaded from PROJECT.yaml.
    The optional definition_change_authority value must contain the required approval,
    provenance, governed-source, generated-mirror, non-approval, and test-repair shapes.
    The function returns that validated mapping without mutating it, or None when the
    directive is absent. It raises ValueError when the directive is malformed,
    incomplete, or internally contradictory.
    """

    policy = value.get("definition_change_authority")
    if policy is None:
        return None
    if not isinstance(policy, dict):
        raise ValueError("definition_change_authority must be a mapping")
    _required_boolean(policy, "approval_required", True, "definition_change_authority")

    evidence = policy.get("approval_evidence")
    if not isinstance(evidence, dict):
        raise ValueError("definition_change_authority.approval_evidence must be a mapping")
    for key in ("user_direction_required", "exact_scope_required", "audit_record_required"):
        _required_boolean(evidence, key, True, "definition_change_authority.approval_evidence")
    if evidence.get("required_basis") != "explicit-user-direction":
        raise ValueError("definition_change_authority.approval_evidence.required_basis must be explicit-user-direction")
    allowed_sources = evidence.get("allowed_provenance_sources")
    if not isinstance(allowed_sources, list) or not allowed_sources or not all(
        isinstance(source, str) and source for source in allowed_sources
    ):
        raise ValueError("definition_change_authority.approval_evidence.allowed_provenance_sources must be a non-empty list")
    if set(allowed_sources) != set(PROVENANCE_REFERENCE_PATTERNS):
        raise ValueError("definition_change_authority.approval_evidence.allowed_provenance_sources must contain only the supported explicit-user-direction sources")
    _required_boolean(
        evidence,
        "provenance_reference_required",
        True,
        "definition_change_authority.approval_evidence",
    )

    sources = policy.get("governed_sources")
    if not isinstance(sources, dict):
        raise ValueError("definition_change_authority.governed_sources must be a mapping")
    _require_exact_keys(
        sources,
        GOVERNED_SOURCE_CATEGORIES,
        "definition_change_authority.governed_sources",
    )
    for key in GOVERNED_SOURCE_CATEGORIES:
        _validated_path_patterns(sources, key, "definition_change_authority.governed_sources")
    generated = _validated_path_patterns(policy, "generated_mirrors", "definition_change_authority")
    relationships = policy.get("regeneration_relationships")
    if not isinstance(relationships, dict):
        raise ValueError("definition_change_authority.regeneration_relationships must be a mapping")
    _require_exact_keys(
        relationships,
        GOVERNED_SOURCE_CATEGORIES,
        "definition_change_authority.regeneration_relationships",
    )
    for key in GOVERNED_SOURCE_CATEGORIES:
        allowed_mirrors = _validated_path_patterns(
            relationships,
            key,
            "definition_change_authority.regeneration_relationships",
        )
        if not set(allowed_mirrors).issubset(generated):
            raise ValueError(
                "definition_change_authority.regeneration_relationships."
                f"{key} must contain only configured generated_mirrors"
            )
    non_approval = _required_patterns(policy, "non_approval_bases", "definition_change_authority")
    required_bases = {"repository access", "failing test", "repair assignment", "general write authority"}
    if not required_bases.issubset(non_approval):
        raise ValueError("definition_change_authority.non_approval_bases must reject repository access, failing test, repair assignment, and general write authority")
    if evidence["required_basis"] in non_approval:
        raise ValueError("definition_change_authority.approval_evidence.required_basis must not be a non-approval basis")

    test_repair = policy.get("test_repair")
    if not isinstance(test_repair, dict):
        raise ValueError("definition_change_authority.test_repair must be a mapping")
    _required_boolean(test_repair, "investigate_incorrect_expectations", True, "definition_change_authority.test_repair")
    _required_boolean(test_repair, "ordinary_test_corrections_allowed", True, "definition_change_authority.test_repair")
    _required_boolean(test_repair, "definition_rewrite_without_approval", False, "definition_change_authority.test_repair")
    return policy


def definition_change_authority_lines(value: dict[str, object]) -> list[str]:
    """Render the configured authority mapping as the complete AGENTS.md section.

    The input is a project mapping accepted by definition_change_authority. The return
    value is an ordered list of Markdown lines containing the authority heading,
    operational preflight, governed patterns, generated-mirror boundary, and test-repair
    rule. An absent directive returns an empty list. Invalid configured content raises
    ValueError through definition_change_authority. The function performs no file I/O.
    """

    policy = definition_change_authority(value)
    if policy is None:
        return []
    sources = policy["governed_sources"]
    assert isinstance(sources, dict)
    generated = policy["generated_mirrors"]
    relationships = policy["regeneration_relationships"]
    assert isinstance(generated, list)
    assert isinstance(relationships, dict)
    lines = [
        AUTHORITY_HEADING,
        "",
        "Every change to an agent definition or skill definition requires explicit, scope-specific user approval before mutation. Record the user's direction, the exact definition scope it authorizes, and the approval evidence in the work lifecycle. Silence, unrelated prior approval, and broad repository mutation authority are insufficient.",
        "",
        "Repository access, a failing test, a repair assignment, general write authority, review work, verification work, and a desire to make validation pass do not authorize a definition change.",
        "",
        "The harness-loaded directive is the project authority boundary. Before mutating a governed canonical source, run the supported pre-mutation check with an approval record that cites existing explicit user direction:",
        "",
        "```bash",
        "python3 scripts/render-agents-technology-skills.py --project PROJECT.yaml --check-definition-change path/to/definition --approval-record path/to/approval-record.yaml",
        "```",
        "",
        "The check validates the configured path boundary, exact scope, basis, and provenance record. It does not enforce filesystem permissions, create approval, or let an agent manufacture user-direction provenance.",
        "",
        "Governed canonical definition surfaces:",
        "",
    ]
    labels = (
        ("conceptual_agents", "Conceptual agent definitions"),
        ("agent_definition_inputs", "Agent definition schemas and model inputs"),
        ("distributed_skills", "Distributed skill definitions"),
        ("adapter_skills", "Adapter-owned skill definitions"),
        ("skill_metadata", "Skill definition metadata"),
    )
    for key, label in labels:
        patterns = sources[key]
        assert isinstance(patterns, list)
        lines.append(f"- {label}: {', '.join(patterns)}.")
    lines.extend([
        "",
        "Generated definition mirrors are source-owned and must never be edited directly:",
        "",
        f"- {', '.join(generated)}.",
        "",
        "Supported source-category to generated-mirror relationships:",
        "",
    ])
    for key, label in labels:
        allowed_mirrors = relationships[key]
        assert isinstance(allowed_mirrors, list)
        lines.append(f"- {label}: {', '.join(allowed_mirrors)}.")
    lines.extend([
        "- Regenerate a mirror only when it is listed for the approved canonical source category. Cross-family role-to-skill and skill-to-role documentation regeneration is blocked. A supported regeneration does not require a second approval.",
        "",
        "When a test fails, investigate whether the test, fixture, assertion, or expected result is incorrect before proposing a definition change. Ordinary authorized implementation changes and corrections to incorrect tests remain allowed when they do not alter a governed definition.",
        "",
    ])
    return lines


def _normalize_project_path(path: str) -> str:
    """Normalize one relative project path without resolving parent traversal."""

    portable = path.replace("\\", "/")
    if portable.startswith("/") or re.match(r"^[A-Za-z]:/", portable):
        raise ValueError(f"definition path must be project-relative: {path}")
    segments: list[str] = []
    for segment in portable.split("/"):
        if segment in {"", "."}:
            continue
        if segment == "..":
            raise ValueError(f"definition path must not contain parent traversal: {path}")
        segments.append(segment)
    if not segments:
        raise ValueError("definition path must not be empty")
    return "/".join(segments)


def _segment_glob_matches(path: tuple[str, ...], pattern: tuple[str, ...]) -> bool:
    """Match path segments while allowing a double-star segment to cross directories."""

    if not pattern:
        return not path
    if pattern[0] == "**":
        return _segment_glob_matches(path, pattern[1:]) or (
            bool(path) and _segment_glob_matches(path[1:], pattern)
        )
    return bool(path) and fnmatch.fnmatchcase(path[0], pattern[0]) and _segment_glob_matches(
        path[1:],
        pattern[1:],
    )


def _matches(path: str, patterns: list[str]) -> bool:
    """Return whether a normalized project-relative path matches a segment-aware pattern."""

    path_segments = tuple(_normalize_project_path(path).split("/"))
    return any(
        _segment_glob_matches(path_segments, tuple(_normalize_project_path(pattern).split("/")))
        for pattern in patterns
    )


def evaluate_definition_change(
    value: dict[str, object],
    path: str,
    approval: dict[str, object] | None,
    *,
    regenerated_from: str | None = None,
) -> dict[str, str]:
    """Classify one proposed repository change under the configured authority policy.

    value is the loaded project mapping. path is a project-relative target; separators,
    repeated separators, and dot segments are normalized, while absolute paths, parent
    traversal, and empty paths are rejected. approval is either None or a mapping with
    basis, exact definition_scope, and provenance source and reference fields.
    regenerated_from optionally names the approved canonical source for a generated
    mirror.

    The returned mapping contains classification and outcome. Outcomes distinguish
    ordinary changes, approved definition changes, approved regeneration, direct
    generated edits, missing approval, and invalid approval. The function only evaluates
    policy and never mutates files or enforces filesystem permissions. It raises
    ValueError for invalid project policy or invalid target, pattern, or regenerated
    source paths; malformed approval records return a blocked outcome instead.
    """

    normalized = _normalize_project_path(path)
    policy = definition_change_authority(value)
    if policy is None:
        return {"outcome": "ALLOWED_ORDINARY_CHANGE", "classification": "ordinary"}
    sources = policy["governed_sources"]
    generated = policy["generated_mirrors"]
    relationships = policy["regeneration_relationships"]
    assert isinstance(sources, dict)
    assert isinstance(generated, list)
    assert isinstance(relationships, dict)
    source_patterns = [pattern for category in GOVERNED_SOURCE_CATEGORIES for pattern in sources[category]]
    if _matches(normalized, generated):
        source_category = next(
            (
                category
                for category in GOVERNED_SOURCE_CATEGORIES
                if regenerated_from and _matches(regenerated_from, sources[category])
            ),
            None,
        )
        if source_category is not None:
            allowed_mirrors = relationships[source_category]
            assert isinstance(allowed_mirrors, list)
            if not _matches(normalized, allowed_mirrors):
                return {
                    "outcome": "BLOCKED_UNSUPPORTED_REGENERATION",
                    "classification": "generated-mirror",
                }
            assert regenerated_from is not None
            approval_outcome = _approval_outcome(policy, approval, regenerated_from)
            if approval_outcome == "MATCHED":
                return {"outcome": "ALLOWED_APPROVED_REGENERATION", "classification": "generated-mirror"}
            return {"outcome": approval_outcome, "classification": "generated-mirror"}
        if regenerated_from is not None:
            _normalize_project_path(regenerated_from)
            return {
                "outcome": "BLOCKED_UNSUPPORTED_REGENERATION",
                "classification": "generated-mirror",
            }
        return {"outcome": "BLOCKED_DIRECT_GENERATED_EDIT", "classification": "generated-mirror"}
    if _matches(normalized, source_patterns):
        approval_outcome = _approval_outcome(policy, approval, normalized)
        if approval_outcome == "MATCHED":
            return {"outcome": "ALLOWED_APPROVED_DEFINITION_CHANGE", "classification": "governed-definition"}
        return {"outcome": approval_outcome, "classification": "governed-definition"}
    return {"outcome": "ALLOWED_ORDINARY_CHANGE", "classification": "ordinary"}


def _approval_outcome(
    policy: dict[str, object],
    approval: dict[str, object] | None,
    path: str,
) -> str:
    """Return MATCHED or the blocking outcome for one proposed approval record."""

    if approval is None:
        return "BLOCKED_APPROVAL_REQUIRED"
    if not isinstance(approval, dict):
        return "BLOCKED_INVALID_APPROVAL"
    evidence = policy["approval_evidence"]
    non_approval_bases = policy["non_approval_bases"]
    assert isinstance(evidence, dict)
    assert isinstance(non_approval_bases, list)
    basis = approval.get("basis")
    if basis in non_approval_bases or basis != evidence["required_basis"]:
        return "BLOCKED_INVALID_APPROVAL"
    scope = approval.get("definition_scope")
    if not isinstance(scope, str):
        return "BLOCKED_INVALID_APPROVAL"
    try:
        normalized_scope = _normalize_project_path(scope)
    except ValueError:
        return "BLOCKED_INVALID_APPROVAL"
    if normalized_scope != _normalize_project_path(path):
        return "BLOCKED_APPROVAL_REQUIRED"
    provenance = approval.get("provenance")
    if not isinstance(provenance, dict):
        return "BLOCKED_INVALID_APPROVAL"
    allowed_sources = evidence["allowed_provenance_sources"]
    assert isinstance(allowed_sources, list)
    if provenance.get("source") not in allowed_sources:
        return "BLOCKED_INVALID_APPROVAL"
    reference = provenance.get("reference")
    source = provenance["source"]
    assert isinstance(source, str)
    reference_pattern = PROVENANCE_REFERENCE_PATTERNS[source]
    if not isinstance(reference, str) or not reference_pattern.fullmatch(reference):
        return "BLOCKED_INVALID_APPROVAL"
    return "MATCHED"


def update_authority_directive(existing: str, section_lines: list[str]) -> str:
    """Merge a generated authority section into maintained AGENTS.md text.

    existing is the complete maintained document and section_lines is the non-empty
    output from definition_change_authority_lines. The returned text replaces the
    existing authority section, inserts it before Technology Skills when absent, or
    appends it when neither heading exists. Other sections retain their content and the
    result ends with one newline. The function performs no file I/O and raises ValueError
    when section_lines is empty.
    """

    if not section_lines:
        raise ValueError("definition_change_authority is required to update the authority directive")
    lines = existing.splitlines()
    try:
        start = lines.index(AUTHORITY_HEADING)
    except ValueError:
        start = next((index for index, line in enumerate(lines) if line == "## Technology Skills"), len(lines))
        end = start
    else:
        end = next((index for index in range(start + 1, len(lines)) if lines[index].startswith("## ")), len(lines))
    replacement = section_lines[:]
    while replacement and replacement[-1] == "":
        replacement.pop()
    prefix = lines[:start]
    suffix = lines[end:]
    while prefix and prefix[-1] == "":
        prefix.pop()
    while suffix and suffix[0] == "":
        suffix.pop(0)
    merged = prefix + ([""] if prefix else []) + replacement + ([""] if suffix else []) + suffix
    return "\n".join(merged) + "\n"


def _legacy_selector_migration(selection: dict[str, object]) -> str | None:
    """Validate prototype selectors and return deterministic canonical migration guidance."""

    migrations: list[str] = []
    collisions: list[str] = []
    for legacy_key, target_key, values in (
        ("workitem", "completion", LEGACY_COMPLETION_VALUES),
        ("backlog", "provider", LEGACY_PROVIDER_VALUES),
    ):
        if legacy_key not in selection:
            continue
        prefix = f"workflow_selection.{legacy_key}"
        mappings = ", ".join(f"{source} -> {target}" for source, target in values.items())
        guidance = f"supported legacy values and canonical replacements: {mappings}"
        configuration = selection[legacy_key]
        if not isinstance(configuration, dict):
            raise ValueError(
                f"{prefix} must be a mapping; canonical replacement: workflow_selection.{target_key}; {guidance}"
            )
        unsupported_keys = set(configuration) - {"default", "folder_overrides"}
        if unsupported_keys:
            raise ValueError(f"{prefix} keys must be exactly: default, folder_overrides; {guidance}")
        default = configuration.get("default")
        if not isinstance(default, str) or default not in values:
            raise ValueError(
                f"{prefix}.default rejects {default!r}; supported legacy values and canonical replacements: {mappings}"
            )
        canonical_default: str | None = None
        canonical_overrides: list[tuple[str, str]] = []
        if target_key in selection:
            supported_values = PROVIDER_VALUES if target_key == "provider" else COMPLETION_VALUES
            canonical_default, canonical_overrides = _workflow_configuration(
                selection,
                target_key,
                supported_values,
            )
        mapped_default = values[default]
        if canonical_default is None:
            migrations.append(f"workflow_selection.{target_key}.default: {mapped_default}")
        else:
            legacy_path = f"{prefix}.default"
            canonical_path = f"workflow_selection.{target_key}.default"
            if mapped_default == canonical_default:
                collisions.append(
                    f"{legacy_path} {default!r} maps to {mapped_default!r}, redundantly matching "
                    f"{canonical_path} {canonical_default!r}; preserve {canonical_path}, migrate any "
                    f"remaining {prefix} overrides, then remove {prefix}"
                )
            else:
                collisions.append(
                    f"{legacy_path} {default!r} maps to {mapped_default!r}, conflicts with "
                    f"{canonical_path} {canonical_default!r}; preserve the valid canonical maintainer edit "
                    f"at {canonical_path}; migrate any remaining {prefix} overrides, then remove {prefix} "
                    f"without overwriting {canonical_path}"
                )
        overrides = configuration.get("folder_overrides", [])
        if not isinstance(overrides, list):
            raise ValueError(f"{prefix}.folder_overrides must be a list; {guidance}")
        seen_patterns: dict[str, tuple[int, str]] = {}
        for override_index, override in enumerate(overrides):
            override_prefix = f"{prefix}.folder_overrides[{override_index}]"
            if not isinstance(override, dict):
                raise ValueError(
                    f"{override_prefix} must be a mapping with pattern and process; {guidance}"
                )
            if "pattern" not in override:
                _validated_override_pattern(override_prefix, None, guidance=guidance)
            if set(override) != {"pattern", "process"}:
                raise ValueError(f"{override_prefix} keys must be exactly: pattern, process; {guidance}")
            pattern = _validated_override_pattern(
                override_prefix,
                override.get("pattern"),
                guidance=guidance,
            )
            process = override.get("process")
            if not isinstance(process, str) or process not in values:
                raise ValueError(
                    f"{override_prefix}.process rejects {process!r}; supported legacy values and canonical replacements: {mappings}"
                )
            _reject_duplicate_override_pattern(
                seen_patterns,
                prefix,
                override_index,
                pattern,
                process,
                guidance=guidance,
            )
            mapped_process = values[process]
            canonical_match = next(
                (
                    (canonical_index, canonical_value)
                    for canonical_index, (canonical_pattern, canonical_value) in enumerate(canonical_overrides)
                    if canonical_pattern == pattern
                ),
                None,
            )
            if canonical_match is None:
                migrations.append(
                    f"add workflow_selection.{target_key}.folder_overrides entry: "
                    f"pattern={pattern}, {target_key}={mapped_process}"
                )
                continue
            canonical_index, canonical_value = canonical_match
            legacy_path = f"{override_prefix}.process"
            canonical_path = (
                f"workflow_selection.{target_key}.folder_overrides[{canonical_index}].{target_key}"
            )
            if mapped_process == canonical_value:
                collisions.append(
                    f"{legacy_path} {process!r} maps to {mapped_process!r}, redundantly matching "
                    f"{canonical_path} {canonical_value!r} for pattern {pattern!r}; preserve "
                    f"{canonical_path} and remove the redundant legacy override"
                )
            else:
                collisions.append(
                    f"{legacy_path} {process!r} maps to {mapped_process!r}, conflicts with "
                    f"{canonical_path} {canonical_value!r} for pattern {pattern!r}; preserve the valid "
                    f"canonical maintainer edit at {canonical_path} and resolve the legacy override explicitly"
                )
    if collisions:
        collision_message = (
            collisions[0]
            if len(collisions) == 1
            else "mixed legacy and canonical workflow selectors collide: " + "; ".join(collisions)
        )
        if migrations:
            collision_message += (
                "; after resolving these collisions, apply remaining migration guidance without changing "
                "canonical fields: " + "; ".join(migrations)
            )
        raise ValueError(collision_message)
    if not migrations:
        return None
    return (
        "legacy workflow selectors require migration: "
        + "; ".join(migrations)
        + "; preserve folder overrides under the matching independent selector and do not infer replacements from repository evidence"
    )


def _validated_override_pattern(
    prefix: str,
    pattern: object,
    *,
    guidance: str | None = None,
) -> str:
    """Return one normalized non-empty project-relative selector override pattern."""

    suffix = f"; {guidance}" if guidance else ""
    if not isinstance(pattern, str) or not pattern:
        raise ValueError(
            f"{prefix}.pattern must be a non-empty project-relative path pattern{suffix}"
        )
    try:
        normalized_pattern = _normalize_project_path(pattern)
    except ValueError as error:
        detail = str(error).removeprefix("definition path ")
        raise ValueError(f"{prefix}.pattern {detail}{suffix}") from error
    if normalized_pattern != pattern:
        raise ValueError(f"{prefix}.pattern must be normalized: {pattern}{suffix}")
    return pattern


def _reject_duplicate_override_pattern(
    seen_patterns: dict[str, tuple[int, str]],
    selector_prefix: str,
    override_index: int,
    pattern: str,
    selected_value: str,
    *,
    guidance: str | None = None,
) -> None:
    """Reject a repeated exact folder pattern with its original and repeated values."""

    previous = seen_patterns.get(pattern)
    if previous is None:
        seen_patterns[pattern] = (override_index, selected_value)
        return
    previous_index, previous_value = previous
    current_path = f"{selector_prefix}.folder_overrides[{override_index}].pattern"
    previous_path = f"{selector_prefix}.folder_overrides[{previous_index}].pattern"
    suffix = f"; {guidance}" if guidance else ""
    if previous_value == selected_value:
        raise ValueError(
            f"{current_path} {pattern!r} duplicates {previous_path} with value {selected_value!r}; "
            f"duplicate patterns are not allowed{suffix}"
        )
    raise ValueError(
        f"{current_path} {pattern!r} conflicts with {previous_path} using values "
        f"{previous_value!r} and {selected_value!r}{suffix}"
    )


def _workflow_configuration(
    selection: dict[str, object],
    key: str,
    supported_values: tuple[str, ...],
) -> tuple[str, list[tuple[str, str]]]:
    """Return one validated selector default and its folder overrides."""

    configuration = selection.get(key)
    prefix = f"workflow_selection.{key}"
    if not isinstance(configuration, dict):
        raise ValueError(
            f"{prefix} must be a mapping; record {prefix}.default: UNSET when the {key} decision is deferred"
        )
    allowed_configuration_keys = {"default", "folder_overrides"}
    unsupported_configuration_keys = set(configuration) - allowed_configuration_keys
    if unsupported_configuration_keys:
        raise ValueError(f"{prefix} keys must be exactly: default, folder_overrides")
    if "default" not in configuration:
        raise ValueError(
            f"{prefix}.default is required; record {prefix}.default: UNSET when the {key} decision is deferred"
        )
    default = configuration.get("default")
    if not isinstance(default, str) or default not in supported_values:
        legacy_values = LEGACY_PROVIDER_VALUES if key == "provider" else LEGACY_COMPLETION_VALUES
        if isinstance(default, str) and default in legacy_values:
            raise ValueError(
                f"{prefix}.default uses legacy value {default!r}; migrate to {legacy_values[default]!r}"
            )
        rendered_values = ", ".join(supported_values)
        raise ValueError(f"{prefix}.default rejects {default!r}; supported values: {rendered_values}")
    overrides = configuration.get("folder_overrides", [])
    if not isinstance(overrides, list):
        raise ValueError(f"{prefix}.folder_overrides must be a list")
    validated_overrides: list[tuple[str, str]] = []
    seen_patterns: dict[str, tuple[int, str]] = {}
    for override_index, override in enumerate(overrides):
        override_prefix = f"{prefix}.folder_overrides[{override_index}]"
        if not isinstance(override, dict):
            raise ValueError(f"{override_prefix} must be a mapping")
        if "pattern" not in override:
            _validated_override_pattern(override_prefix, None)
        combined_process = override.get("process")
        if (
            set(override) == {"pattern", "process"}
            and isinstance(combined_process, str)
            and "+" in combined_process
        ):
            other_key = "completion" if key == "provider" else "provider"
            rendered_values = ", ".join(supported_values)
            raise ValueError(
                f"{override_prefix}.process rejects combined value {combined_process!r}; supported {key} "
                f"values: {rendered_values}; split it into {override_prefix}.{key} and a "
                f"workflow_selection.{other_key}.folder_overrides entry with the same pattern"
            )
        if set(override) != {"pattern", key}:
            raise ValueError(f"{override_prefix} keys must be exactly: pattern, {key}")
        pattern = _validated_override_pattern(override_prefix, override.get("pattern"))
        selected_value = override.get(key)
        if not isinstance(selected_value, str) or selected_value not in supported_values:
            legacy_values = LEGACY_PROVIDER_VALUES if key == "provider" else LEGACY_COMPLETION_VALUES
            if isinstance(selected_value, str) and selected_value in legacy_values:
                raise ValueError(
                    f"{override_prefix}.{key} uses legacy value {selected_value!r}; migrate to {legacy_values[selected_value]!r}"
                )
            rendered_values = ", ".join(supported_values)
            split_guidance = ""
            if isinstance(selected_value, str) and "+" in selected_value:
                other_key = "completion" if key == "provider" else "provider"
                split_guidance = (
                    f"; split the combined value into {override_prefix}.{key} and a "
                    f"workflow_selection.{other_key}.folder_overrides entry with the same pattern"
                )
            raise ValueError(
                f"{override_prefix}.{key} rejects {selected_value!r}; supported values: "
                f"{rendered_values}{split_guidance}"
            )
        _reject_duplicate_override_pattern(
            seen_patterns,
            prefix,
            override_index,
            pattern,
            selected_value,
        )
        validated_overrides.append((pattern, selected_value))
    return default, validated_overrides


def _provider_reference(label: str, provider: str) -> str:
    """Render one provider selection as create and manage skill references."""

    if provider == "UNSET":
        return f"- {label} provider UNSET: the pertinent agent asks for the provider decision before a provider operation."
    if provider == "none":
        return (
            f"- {label} provider none: no durable provider skill; durable create and manage operations are invalid."
        )
    create_skill, manage_skill = PROVIDER_SKILLS[provider]
    suffix = ""
    if provider in {"azure-devops", "jira"}:
        suffix = " The unsupported placeholder remains selected and reports BLOCKED without mutation."
    return (
        f"- {label} provider {provider}: create with {create_skill}; manage with {manage_skill}."
        f"{suffix}"
    )


def _completion_reference(label: str, completion: str) -> str:
    """Render one completion selection as a completion skill reference."""

    if completion == "UNSET":
        return (
            f"- {label} completion UNSET: the pertinent agent asks for the completion decision before implementation or publication."
        )
    return f"- {label} completion {completion}: use {COMPLETION_SKILLS[completion]}."


def workflow_lines(value: dict[str, object]) -> list[str]:
    """Render reference-only provider and completion workflow guidance."""

    selection = value.get("workflow_selection")
    if selection is None:
        raise ValueError(
            "workflow_selection is required; record workflow_selection.provider.default and "
            "workflow_selection.completion.default explicitly, using UNSET when either decision is deferred"
        )
    if not isinstance(selection, dict):
        raise ValueError("workflow_selection must be a mapping")
    migration = _legacy_selector_migration(selection)
    if migration is not None:
        raise ValueError(migration)
    allowed_keys = {"provider", "completion", "selection_policy"}
    unsupported_keys = set(selection) - allowed_keys
    if unsupported_keys:
        raise ValueError(
            "workflow_selection keys must be exactly provider, completion, and optional selection_policy"
        )
    selection_policy = selection.get("selection_policy")
    if selection_policy is not None and (
        not isinstance(selection_policy, str) or not selection_policy
    ):
        raise ValueError("workflow_selection.selection_policy must be a non-empty string")
    provider, provider_overrides = _workflow_configuration(
        selection,
        "provider",
        PROVIDER_VALUES,
    )
    completion, completion_overrides = _workflow_configuration(
        selection,
        "completion",
        COMPLETION_VALUES,
    )

    lines = [
        "## Work-Item Workflow Skill References",
        "",
        "Project Configurator owns these independent selectors. Workflow skills are referenced by name only and are never inlined; their procedures stay in the selected skill definitions. Technology skill inlining is a separate mechanism below.",
        "",
        _provider_reference("Default", provider),
    ]
    lines.extend(_provider_reference(pattern, selected) for pattern, selected in provider_overrides)
    lines.append(_completion_reference("Default", completion))
    lines.extend(
        _completion_reference(pattern, selected)
        for pattern, selected in completion_overrides
    )
    lines.extend([
        "",
        "Most-specific matching folder pattern wins independently for provider and completion overrides. A folder override changes only its own selector.",
        "",
        "When a selector is UNSET, the pertinent agent asks at the stated operation boundary and does not infer either value from repository or hosting evidence, files, remotes, templates, plugins, or available tools.",
        "",
    ])
    return lines


def claim_transport_lines(value: dict[str, object]) -> list[str]:
    """Render the one setup-verified claim transport selected by Project Configurator.

    The input must contain agent_claim_transport with exactly selected, availability,
    and verification. selected is mcp or command, availability is AVAILABLE, and
    verification is a non-empty list of evidence strings. An unavailable selection
    produces a deterministic reconfiguration error instead of guidance that could fall
    back at runtime. The returned lines inline only the matching bundled adapter body.
    Invalid configuration or adapter content raises ValueError or OSError.
    """

    configuration = value.get("agent_claim_transport")
    if configuration is None:
        raise ValueError(
            "agent_claim_transport is required; run Project Configurator to select and verify mcp or command"
        )
    if not isinstance(configuration, dict):
        raise ValueError("agent_claim_transport must be a mapping")
    if set(configuration) != {"selected", "availability", "verification"}:
        raise ValueError(
            "agent_claim_transport keys must be exactly: selected, availability, verification"
        )
    selected = configuration.get("selected")
    if not isinstance(selected, str) or selected not in CLAIM_TRANSPORT_SKILLS:
        raise ValueError("agent_claim_transport.selected must be mcp or command")
    availability = configuration.get("availability")
    if availability not in {"AVAILABLE", "UNAVAILABLE"}:
        raise ValueError(
            "agent_claim_transport.availability must be AVAILABLE or UNAVAILABLE"
        )
    verification = configuration.get("verification")
    if not isinstance(verification, list) or not verification or not all(
        isinstance(item, str) and item for item in verification
    ):
        raise ValueError(
            "agent_claim_transport.verification must be a non-empty list of evidence strings"
        )
    if availability == "UNAVAILABLE":
        raise ValueError(
            f"configured claim transport {selected} is unavailable; run Project Configurator to select and verify one available transport"
        )

    skill_name = CLAIM_TRANSPORT_SKILLS[selected]
    return [
        CLAIM_TRANSPORT_HEADING,
        "",
        f"Project Configurator selected and verified the {selected} transport. Apply the shared agent-claim semantics and the inlined {skill_name} adapter for every claim operation.",
        "",
        "Invoke this configured adapter directly. Runtime work does not probe or switch to another transport. If it is unavailable, report CLAIM_TRANSPORT_UNAVAILABLE and request Project Configurator reconfiguration.",
        "",
        f"----- BEGIN INLINED CLAIM TRANSPORT SKILL: {skill_name} -----",
        inlined_skill_body(skill_name),
        f"----- END INLINED CLAIM TRANSPORT SKILL: {skill_name} -----",
        "",
    ]


def inlined_skill_body(skill_name: str) -> str:
    """Return one validated bundled technology skill body."""

    if not SKILL_NAME_PATTERN.fullmatch(skill_name):
        raise ValueError(f"Invalid technology skill name: {skill_name}")
    skill_path = SKILLS_ROOT / skill_name / SKILL_FILE_NAME
    lines = skill_path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != FRONTMATTER_DELIMITER:
        raise ValueError(f"Missing YAML frontmatter: {skill_path}")
    try:
        closing_index = lines[1:].index(FRONTMATTER_DELIMITER) + 1
    except ValueError as error:
        raise ValueError(f"Missing closing frontmatter delimiter: {skill_path}") from error
    frontmatter = yaml.safe_load("\n".join(lines[1:closing_index]))
    if not isinstance(frontmatter, dict) or frontmatter.get("name") != skill_name:
        raise ValueError(f"Skill name must match its directory: {skill_path}")
    return "\n".join(lines[closing_index + 1:]).strip()


def render(
    value: dict[str, object],
    inline_tech_skills: bool = True,
    include_project_skill_extensions: bool = True,
) -> str:
    """Render configured root AGENTS.md project authority and skill sections.

    value is the mapping loaded from PROJECT.yaml. Optional definition authority produces
    its corresponding section. agent_claim_transport is required and workflow_selection is required.
    Technology guidance is always produced from the configured loadouts, and an optional
    project_skill_extensions list produces the final root-only reference section when
    include_project_skill_extensions is true. The claim adapter is always embedded because
    setup selected it as a project-wide transport. When inline_tech_skills is true, the
    return value also embeds each referenced bundled technology skill body. When false, it
    emits dynamic technology loading instructions.

    The return value is the complete generated Markdown text and ends with a newline.
    Rendering does not write an output file, but inlined rendering reads bundled SKILL.md
    files. Invalid authority, workflow, project extension, or source-evidence configuration,
    unsafe skill names, and invalid skill frontmatter raise ValueError. Missing or unreadable
    skill files raise OSError, and malformed YAML may raise yaml.YAMLError.
    """
    lines: list[str] = definition_change_authority_lines(value)
    workflow = workflow_lines(value)
    lines.extend(claim_transport_lines(value))
    lines.extend(workflow)
    lines.extend([
        "## Technology Skills",
        "",
        "Technology detection is owned by Project Configurator. Do not rerun detection during ordinary work.",
        "",
        (
            "Before acting on files under a matching folder, every agent must apply each inlined skill completely. These folder skills govern technology-specific implementation, review, diagnosis, verification, security, interface, prompt, and technical documentation work together with the agent's definition-owned skills."
            if inline_tech_skills
            else "Before acting on files under a matching folder, every agent must read each listed skill completely. These folder skills govern technology-specific implementation, review, diagnosis, verification, security, interface, prompt, and technical documentation work together with the agent's definition-owned skills."
        ),
        "",
        "Folder skillsets:",
        "",
        "When configured folder patterns overlap, the most-specific matching pattern wins.",
        "",
    ])
    inlined_loadouts: list[tuple[str, list[str]]] = []
    rendered = 0
    for loadout_index, item in enumerate(loadouts(value)):
        evidence_key = "sourceEvidence" if "sourceEvidence" in item else "source_evidence"
        source_evidence = item.get(evidence_key, [])
        evidence_prefix = f"technology_skill_loadouts[{loadout_index}].{evidence_key}"
        if not isinstance(source_evidence, list):
            raise ValueError(f"{evidence_prefix} must be a list")
        evidence_lines: list[str] = []
        for evidence_index, evidence in enumerate(source_evidence):
            row_prefix = f"{evidence_prefix}[{evidence_index}]"
            if not isinstance(evidence, Mapping):
                raise ValueError(f"{row_prefix} must be a mapping")
            skill = evidence.get("skill")
            if not isinstance(skill, str):
                raise ValueError(f"{row_prefix}.skill must be a string")
            facts = evidence.get("evidence")
            facts_prefix = f"{row_prefix}.evidence"
            if not isinstance(facts, list):
                raise ValueError(f"{facts_prefix} must be a list of strings")
            for fact_index, fact in enumerate(facts):
                if not isinstance(fact, str):
                    raise ValueError(f"{facts_prefix}[{fact_index}] must be a string")
            if facts:
                evidence_lines.append(f"  - {skill} evidence: {'; '.join(facts)}")
        pattern = item.get("pathPattern", item.get("pattern"))
        skills = item.get("skills", item.get("required_skills", []))
        if not isinstance(pattern, str) or not isinstance(skills, list):
            continue
        names = [str(skill) for skill in skills if isinstance(skill, str)]
        if not names:
            if item.get("status") != "NO_VARIANT":
                continue
            fallback = item.get("fallback", "General model training")
            lines.append(
                f"- {pattern}: no pertinent specialized technology skill is available; "
                f"use {fallback} and continue full scope coverage."
            )
            rendered += 1
            continue
        if inline_tech_skills:
            noun = "skill" if len(names) == 1 else "skills"
            lines.append(
                f"- {pattern}: apply the inlined {', '.join(names)} {noun} instructions before acting."
            )
            inlined_loadouts.append((pattern, names))
        else:
            lines.append(f"- {pattern}: load {', '.join(names)} before acting.")
        lines.extend(evidence_lines)
        rendered += 1
    if rendered == 0:
        lines.append("- No bundled technology variant was detected for the analyzed folders.")
    if inlined_loadouts:
        lines.extend([
            "",
            "Inlined folder skill instructions:",
        ])
        for pattern, names in inlined_loadouts:
            lines.extend([
                "",
                f"### Folder pattern: {pattern}",
                "",
                "Apply every inlined technology skill below when working under this folder pattern.",
            ])
            for skill_name in names:
                lines.extend([
                    "",
                    f"----- BEGIN INLINED TECHNOLOGY SKILL: {skill_name} -----",
                    inlined_skill_body(skill_name),
                    f"----- END INLINED TECHNOLOGY SKILL: {skill_name} -----",
                ])
    lines.append("")
    project_skill_extension_lines = _project_skill_extension_lines(value)
    if include_project_skill_extensions:
        lines.extend(project_skill_extension_lines)
    return "\n".join(lines)


def main(arguments: Sequence[str] | None = None) -> int:
    """Run the renderer or definition-change preflight command-line interface.

    arguments is an explicit CLI argument sequence for programmatic callers, or None to
    parse the process arguments. Preflight mode prints one JSON policy result: allowed
    outcomes return 0 and blocked outcomes return 3. Render mode without an output path
    prints generated authority, selected claim-adapter, workflow, and technology Markdown.
    Output mode writes the generated Markdown to its file: it creates a missing file,
    replaces one only with the replace option, or updates only the authority section
    with the dedicated update option. Every successful render, output, and update mode
    returns 0.

    File creation and updates are the only repository side effects. Handled OSError,
    ValueError, and yaml.YAMLError failures are printed to standard error and return 1.
    Argument-parser usage failures raise SystemExit with argparse's exit code, normally 2.
    """
    parser = argparse.ArgumentParser(
        description="Render claim transport, workflow selectors, technology guidance, and root project skill references."
    )
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace an existing output file. Without this option, --output is create-only.",
    )
    parser.add_argument(
        "--update-authority-directive",
        action="store_true",
        help="Insert or replace only the configured authority directive in an existing AGENTS.md file.",
    )
    parser.add_argument(
        "--inline-tech-skills",
        type=parse_boolean,
        default=True,
        metavar="true|false",
        help="Statically embed discovered technology skills in AGENTS.md. Defaults to true.",
    )
    parser.add_argument(
        "--check-definition-change",
        metavar="PATH",
        help="Evaluate one proposed project-relative path before mutation and print a JSON outcome.",
    )
    parser.add_argument(
        "--approval-record",
        type=Path,
        help="YAML approval record containing basis, exact definition_scope, and user-direction provenance.",
    )
    parser.add_argument(
        "--regenerated-from",
        metavar="PATH",
        help="Approved canonical definition source for a generated-mirror check.",
    )
    args = parser.parse_args(arguments)
    try:
        if args.replace and args.update_authority_directive:
            raise ValueError("--replace and --update-authority-directive cannot be combined")
        project = load_yaml(args.project)
        if args.check_definition_change is not None:
            if args.output or args.replace or args.update_authority_directive:
                raise ValueError("--check-definition-change cannot be combined with output mutation options")
            if definition_change_authority(project) is None:
                raise ValueError("--check-definition-change requires definition_change_authority in PROJECT.yaml")
            approval = load_yaml(args.approval_record) if args.approval_record else None
            result = evaluate_definition_change(
                project,
                args.check_definition_change,
                approval,
                regenerated_from=args.regenerated_from,
            )
            print(json.dumps(result, sort_keys=True))
            return 0 if result["outcome"].startswith("ALLOWED_") else 3
        if args.approval_record or args.regenerated_from:
            raise ValueError("--approval-record and --regenerated-from require --check-definition-change")
        root_output = (
            args.output is None
            or args.output.resolve().parent == args.project.resolve().parent
        )
        content = render(
            project,
            args.inline_tech_skills,
            include_project_skill_extensions=root_output,
        )
        if args.output:
            if args.update_authority_directive:
                if not args.output.exists():
                    raise ValueError("--update-authority-directive requires an existing output file")
                content = update_authority_directive(
                    args.output.read_text(encoding="utf-8"),
                    definition_change_authority_lines(project),
                )
            elif args.output.exists() and not args.replace:
                raise ValueError(
                    f"output file already exists: {args.output}; use --replace to replace it"
                )
            args.output.write_text(content, encoding="utf-8")
        else:
            if args.update_authority_directive:
                raise ValueError("--update-authority-directive requires --output")
            print(content, end="")
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
