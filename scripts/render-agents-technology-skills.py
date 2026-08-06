#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Renders project setup, deadline-aware coordination, workflows, folder technology, and project skill guidance.

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from collections.abc import Mapping, Sequence
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
SKILL_FILE_NAME = "SKILL.md"
FRONTMATTER_DELIMITER = "---"
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")
CLAIM_TRANSPORT_HEADING = "## Agent Claim Helper"
RESOURCE_COORDINATION_HEADING = "## Resource Coordination Skill Reference"
_RESOURCE_DEADLINE_CLASS_IDS = (
    "backlog-mutation",
    "main-integration",
    "browser-server",
    "database-port",
    "live-model-evaluation",
)
PROJECT_SKILL_EXTENSIONS_HEADING = "## Project Skill Extensions"
CLAIM_TRANSPORT_SKILLS = {
    "mcp": "agent-claim-mcp",
    "command": "agent-claim-command",
}
RESOURCE_COORDINATION_VALUES = {"none", "agent-claim"}
RESOURCE_COORDINATION_RESERVED_SKILLS = frozenset(
    {"agent-claim", *CLAIM_TRANSPORT_SKILLS.values()}
)
PROVIDER_SKILLS = {
    "file": ("create-work-item-file", "manage-work-items-file"),
    "github": ("create-work-item-github", "manage-work-items-github"),
    "gitlab": ("create-work-item-gitlab", "manage-work-items-gitlab"),
    "azure-devops": ("create-work-item-azure-devops", "manage-work-items-azure-devops"),
    "jira": ("create-work-item-jira", "manage-work-items-jira"),
}
PROVIDER_VALUES = (*PROVIDER_SKILLS, "none", "UNSET")
COMPLETION_SKILLS = {
    "direct-main": "deliver-work-item-direct-main",
    "feature-branch": "deliver-work-item-feature-branch",
}
COMPLETION_VALUES = (*COMPLETION_SKILLS, "UNSET")
SETUP_MODES = ("basic", "advanced")
DOCUMENTATION_CHOICES = ("none", "wiki", "specifications", "both")
SKILL_DELIVERY_MODES = ("by-reference", "inline")
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


def _normalized_technology_scope(value: object, field: str) -> str:
    """Return one canonical project-relative technology scope pattern."""

    if not isinstance(value, str) or not value or "\n" in value or "\r" in value:
        raise ValueError(f"{field} must be a normalized project-relative path pattern")
    try:
        normalized = _normalize_project_path(value)
    except ValueError as error:
        raise ValueError(
            f"{field} must be a normalized project-relative path pattern"
        ) from error
    if normalized != value:
        raise ValueError(f"{field} must be a normalized project-relative path pattern")
    return normalized


def _single_line_rendered_text(value: object, field: str) -> str:
    """Return non-empty text that cannot introduce generated guidance structure."""

    if (
        not isinstance(value, str)
        or not value.strip()
        or any(
            unicodedata.category(character).startswith("C")
            or unicodedata.category(character) in {"Zl", "Zp"}
            for character in value
        )
    ):
        raise ValueError(f"{field} must be non-empty single-line text without control characters")
    return value


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

        if skill in RESOURCE_COORDINATION_RESERVED_SKILLS:
            raise ValueError(
                f"{prefix} skill id {skill!r} is reserved for resource_coordination; "
                "remove it from project_skill_extensions"
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


def _normalize_project_path(path: str) -> str:
    """Normalize one relative project path without resolving parent traversal."""

    portable = path.replace("\\", "/")
    if portable.startswith("/") or re.match(r"^[A-Za-z]:/", portable):
        raise ValueError(f"project path must be project-relative: {path}")
    segments: list[str] = []
    for segment in portable.split("/"):
        if segment in {"", "."}:
            continue
        if segment == "..":
            raise ValueError(f"project path must not contain parent traversal: {path}")
        segments.append(segment)
    if not segments:
        raise ValueError("project path must not be empty")
    return "/".join(segments)


def _legacy_process_configuration(
    selection: dict[str, object],
    source_key: str,
    target_key: str,
    values: dict[str, str],
) -> dict[str, object]:
    """Normalize one backlog or workitem selector into its canonical selector shape."""

    prefix = f"workflow_selection.{source_key}"
    target_path = f"workflow_selection.{target_key}"
    mappings = ", ".join(f"{source} -> {target}" for source, target in values.items())
    guidance = f"supported legacy values and canonical replacements: {mappings}"
    configuration = selection[source_key]
    if not isinstance(configuration, dict):
        raise ValueError(
            f"{prefix} must be a mapping; canonical replacement: {target_path}; {guidance}"
        )
    if set(configuration) - {"default", "folder_overrides"}:
        raise ValueError(f"{prefix} keys must be exactly: default, folder_overrides; {guidance}")
    default = configuration.get("default")
    if not isinstance(default, str) or default not in values:
        raise ValueError(
            f"{prefix}.default rejects {default!r}; supported legacy values and canonical replacements: {mappings}"
        )
    overrides = configuration.get("folder_overrides", [])
    if not isinstance(overrides, list):
        raise ValueError(f"{prefix}.folder_overrides must be a list; {guidance}")
    normalized_overrides: list[dict[str, str]] = []
    seen_patterns: dict[str, tuple[int, str]] = {}
    for index, override in enumerate(overrides):
        override_prefix = f"{prefix}.folder_overrides[{index}]"
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
            index,
            pattern,
            process,
            guidance=guidance,
        )
        normalized_overrides.append({"pattern": pattern, target_key: values[process]})
    return {
        "default": values[default],
        "folder_overrides": normalized_overrides,
    }


def _canonical_workflow_selection(
    selection: dict[str, object],
) -> tuple[dict[str, object], list[str]]:
    """Normalize one compatible selector family per domain to Persistence and Commit."""

    allowed_keys = {
        "persistence",
        "commit",
        "provider",
        "completion",
        "backlog",
        "workitem",
        "selection_policy",
    }
    unsupported = set(selection) - allowed_keys
    if unsupported:
        raise ValueError(
            "workflow_selection keys must be canonical persistence and commit, compatibility "
            "provider, completion, backlog, or workitem, and optional selection_policy"
        )
    normalized: dict[str, object] = {}
    notices: list[str] = []
    for target_key, families in (
        ("persistence", ("persistence", "provider", "backlog")),
        ("commit", ("commit", "completion", "workitem")),
    ):
        present = [key for key in families if key in selection]
        if len(present) > 1:
            source_key = next(key for key in present if key != target_key) if target_key in present else present[1]
            other_key = target_key if target_key in present else present[0]
            raise ValueError(
                f"workflow_selection.{source_key} collides with workflow_selection.{other_key}; "
                f"replace workflow_selection.{source_key} with workflow_selection.{target_key} "
                "and keep exactly one selector family"
            )
        if not present:
            continue
        source_key = present[0]
        if source_key == target_key:
            normalized[target_key] = selection[source_key]
        elif source_key in {"provider", "completion"}:
            supported_values = PROVIDER_VALUES if target_key == "persistence" else COMPLETION_VALUES
            default, overrides = _workflow_configuration(selection, source_key, supported_values)
            normalized[target_key] = {
                "default": default,
                "folder_overrides": [
                    {"pattern": pattern, target_key: selected}
                    for pattern, selected in overrides
                ],
            }
            notices.append(
                f"Normalized workflow_selection.{source_key} to workflow_selection.{target_key} "
                "without changing selected values."
            )
        else:
            values = LEGACY_PROVIDER_VALUES if target_key == "persistence" else LEGACY_COMPLETION_VALUES
            normalized[target_key] = _legacy_process_configuration(
                selection,
                source_key,
                target_key,
                values,
            )
            notices.append(
                f"Normalized workflow_selection.{source_key} to workflow_selection.{target_key} "
                "using the documented compatibility value mapping."
            )
    if "selection_policy" in selection:
        normalized["selection_policy"] = selection["selection_policy"]
    return normalized, notices


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
        detail = str(error).removeprefix("project path ")
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
        legacy_values = (
            LEGACY_PROVIDER_VALUES
            if key in {"provider", "persistence"}
            else LEGACY_COMPLETION_VALUES
        )
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
            other_key = {
                "provider": "completion",
                "persistence": "commit",
                "completion": "provider",
                "commit": "persistence",
            }[key]
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
            legacy_values = (
                LEGACY_PROVIDER_VALUES
                if key in {"provider", "persistence"}
                else LEGACY_COMPLETION_VALUES
            )
            if isinstance(selected_value, str) and selected_value in legacy_values:
                raise ValueError(
                    f"{override_prefix}.{key} uses legacy value {selected_value!r}; migrate to {legacy_values[selected_value]!r}"
                )
            rendered_values = ", ".join(supported_values)
            split_guidance = ""
            if isinstance(selected_value, str) and "+" in selected_value:
                other_key = {
                    "provider": "completion",
                    "persistence": "commit",
                    "completion": "provider",
                    "commit": "persistence",
                }[key]
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


def _persistence_reference(label: str, persistence: str) -> str:
    """Render one Persistence selection as create and manage skill references."""

    if persistence == "UNSET":
        return (
            f"- {label} UNSET: when durable work-item management is first requested, "
            "ask whether to select the available file provider. Do not create or manage "
            "work items before the user answers. After approval, Project Configurator "
            "updates PROJECT.yaml and renders proposed guidance to AGENTS.md.candidate. "
            "Compare that candidate with AGENTS.md, preserve project-specific directives, "
            "move reusable project directives into project skills referenced by PROJECT.yaml "
            "when appropriate, regenerate the candidate, and apply AGENTS.md only after the "
            "comparison is complete. Then resume the original work-item request. A deferred "
            "answer leaves Persistence UNSET; an explicit none selection remains none."
        )
    if persistence == "none":
        return (
            f"- {label} none: no durable persistence skill; durable create and manage operations are invalid."
        )
    create_skill, manage_skill = PROVIDER_SKILLS[persistence]
    suffix = ""
    if persistence in {"azure-devops", "jira"}:
        suffix = " The unsupported placeholder remains selected and reports BLOCKED without mutation."
    return (
        f"- {label} {persistence}: create with {create_skill}; manage with {manage_skill}."
        f"{suffix}"
    )


def _commit_reference(label: str, commit: str) -> str:
    """Render one Commit selection as a delivery skill reference."""

    if commit == "UNSET":
        return (
            f"- {label} UNSET: the pertinent agent asks for the Commit decision before implementation or publication."
        )
    return f"- {label} {commit}: use {COMPLETION_SKILLS[commit]}."


def workflow_lines(value: dict[str, object]) -> list[str]:
    """Render canonical Persistence and Commit guidance from compatible selector inputs."""

    selection = value.get("workflow_selection")
    if selection is None:
        raise ValueError(
            "workflow_selection is required; record workflow_selection.persistence.default and "
            "workflow_selection.commit.default explicitly, using UNSET when either decision is deferred"
        )
    if not isinstance(selection, dict):
        raise ValueError("workflow_selection must be a mapping")
    canonical_selection, notices = _canonical_workflow_selection(selection)
    selection_policy = canonical_selection.get("selection_policy")
    if selection_policy is not None and (
        not isinstance(selection_policy, str) or not selection_policy
    ):
        raise ValueError("workflow_selection.selection_policy must be a non-empty string")
    persistence, persistence_overrides = _workflow_configuration(
        canonical_selection,
        "persistence",
        PROVIDER_VALUES,
    )
    commit, commit_overrides = _workflow_configuration(
        canonical_selection,
        "commit",
        COMPLETION_VALUES,
    )

    lines = [
        "## Work-Item Workflow Skill References",
        "",
        "Project Configurator owns the independent Persistence and Commit selectors. Persistence routes durable work-item storage; Commit routes delivery. Workflow skills are referenced by name only and technology skill routing remains separate.",
        "",
        *(f"- {notice}" for notice in notices),
        _persistence_reference("Default persistence", persistence),
    ]
    lines.extend(
        _persistence_reference(f"{pattern} persistence", selected)
        for pattern, selected in persistence_overrides
    )
    lines.append(_commit_reference("Default commit", commit))
    lines.extend(
        _commit_reference(f"{pattern} commit", selected)
        for pattern, selected in commit_overrides
    )
    lines.extend([
        "",
        "Most-specific matching folder pattern wins independently for Persistence and Commit overrides. A folder override changes only its own selector.",
        "",
        "When a selector is UNSET, the pertinent agent asks at the stated operation boundary and does not infer either value from repository or hosting evidence, files, remotes, templates, plugins, or available tools.",
        "",
    ])
    return lines


def _resource_deadline_seconds(
    policy: dict[str, object],
    field: str,
    context: str,
    *,
    allow_zero: bool = False,
) -> int:
    value = policy.get(field)
    valid = isinstance(value, int) and not isinstance(value, bool)
    valid = valid and (value >= 0 if allow_zero else value > 0)
    if not valid:
        qualifier = "non-negative" if allow_zero else "positive"
        raise ValueError(f"{context}.{field} must be a {qualifier} integer")
    return value


def _resource_deadline_policy(configuration: dict[str, object]) -> dict[str, object]:
    policy = configuration.get("deadline_policy")
    if not isinstance(policy, dict):
        raise ValueError("resource_coordination.deadline_policy must be a mapping")
    if set(policy) != {"resource_classes", "resource_overrides"}:
        raise ValueError(
            "resource_coordination.deadline_policy keys must be exactly: resource_classes, resource_overrides"
        )
    classes = policy.get("resource_classes")
    if not isinstance(classes, dict):
        raise ValueError("resource_coordination.deadline_policy.resource_classes must be a mapping")
    if set(classes) != set(_RESOURCE_DEADLINE_CLASS_IDS):
        raise ValueError(
            "resource_coordination.deadline_policy.resource_classes keys must be exactly: "
            + ", ".join(_RESOURCE_DEADLINE_CLASS_IDS)
        )
    normalized_classes: dict[str, dict[str, int]] = {}
    for class_id in _RESOURCE_DEADLINE_CLASS_IDS:
        class_policy = classes[class_id]
        context = f"resource_coordination.deadline_policy.resource_classes.{class_id}"
        if not isinstance(class_policy, dict):
            raise ValueError(f"{context} must be a mapping")
        if set(class_policy) != {"maximum_duration_seconds", "cleanup_grace_seconds"}:
            raise ValueError(
                f"{context} keys must be exactly: maximum_duration_seconds, cleanup_grace_seconds"
            )
        normalized_classes[class_id] = {
            "maximum_duration_seconds": _resource_deadline_seconds(
                class_policy,
                "maximum_duration_seconds",
                context,
            ),
            "cleanup_grace_seconds": _resource_deadline_seconds(
                class_policy,
                "cleanup_grace_seconds",
                context,
                allow_zero=True,
            ),
        }

    overrides = policy.get("resource_overrides")
    if not isinstance(overrides, dict):
        raise ValueError("resource_coordination.deadline_policy.resource_overrides must be a mapping")
    normalized_overrides: dict[str, dict[str, object]] = {}
    for resource_id, override in overrides.items():
        if (
            not isinstance(resource_id, str)
            or not resource_id
            or resource_id != resource_id.strip()
            or len(resource_id) > 200
        ):
            raise ValueError(
                "resource override ids must be canonical non-empty strings of at most 200 characters"
            )
        context = f"resource_coordination.deadline_policy.resource_overrides.{resource_id}"
        if not isinstance(override, dict):
            raise ValueError(f"{context} must be a mapping")
        if set(override) != {
            "resource_class",
            "maximum_duration_seconds",
            "cleanup_grace_seconds",
        }:
            raise ValueError(
                f"{context} keys must be exactly: resource_class, maximum_duration_seconds, cleanup_grace_seconds"
            )
        resource_class = override.get("resource_class")
        if resource_class not in normalized_classes:
            raise ValueError(f"{context}.resource_class must name a configured resource class")
        normalized_overrides[resource_id] = {
            "resource_class": resource_class,
            "maximum_duration_seconds": _resource_deadline_seconds(
                override,
                "maximum_duration_seconds",
                context,
            ),
            "cleanup_grace_seconds": _resource_deadline_seconds(
                override,
                "cleanup_grace_seconds",
                context,
                allow_zero=True,
            ),
        }
    return {
        "resource_classes": normalized_classes,
        "resource_overrides": normalized_overrides,
    }


def resource_coordination_lines(value: dict[str, object]) -> list[str]:
    """Render the selected project-wide coordination skill as a reference.

    value is one loaded project mapping. resource_coordination is required. none permits only selected, requires
    agent_claim_transport to be absent, and returns no guidance. agent-claim also requires
    deadline_policy with all five resource classes and an exact resource-id override map.
    The returned Markdown lines render every validated integer-second value while leaving
    procedure in the bundled skill; the function does not mutate value or write files.
    Missing, unsupported, or internally inconsistent configuration raises ValueError.
    """

    configuration = value.get("resource_coordination")
    if configuration is None:
        raise ValueError(
            "resource_coordination is required; run Project Configurator to select none or agent-claim"
        )
    if not isinstance(configuration, dict):
        raise ValueError("resource_coordination must be a mapping")
    selected = configuration.get("selected")
    if not isinstance(selected, str) or selected not in RESOURCE_COORDINATION_VALUES:
        raise ValueError("resource_coordination.selected must be none or agent-claim")
    if selected == "none":
        if set(configuration) != {"selected"}:
            raise ValueError("resource_coordination keys must be exactly: selected")
        if "agent_claim_transport" in value:
            raise ValueError(
                "agent_claim_transport must be omitted when resource_coordination.selected is none"
            )
        return []
    if set(configuration) != {"selected", "deadline_policy"}:
        raise ValueError(
            "resource_coordination keys must be exactly: selected, deadline_policy when agent-claim is selected"
        )
    deadline_policy = _resource_deadline_policy(configuration)
    lines = [
        RESOURCE_COORDINATION_HEADING,
        "",
        "Project Configurator selected resource-coordination skill agent-claim. Apply that bundled skill by reference before taking ownership of repository paths or exclusive runtime and integration resources.",
        "",
        "The selected skill owns its coordination procedure and evidence. Work-item providers own durable assignment and lifecycle records; they do not own operational resources.",
        "",
        "Configured resource deadline policy:",
        "",
    ]
    for class_id in _RESOURCE_DEADLINE_CLASS_IDS:
        class_policy = deadline_policy["resource_classes"][class_id]
        lines.append(
            f"- {class_id}: maximum {class_policy['maximum_duration_seconds']} seconds; cleanup grace {class_policy['cleanup_grace_seconds']} seconds"
        )
    lines.extend(["", "Exact resource-id overrides:", ""])
    overrides = deadline_policy["resource_overrides"]
    if not overrides:
        lines.append("- None.")
    else:
        for resource_id in sorted(overrides):
            override = overrides[resource_id]
            lines.append(
                f"- {resource_id}: class {override['resource_class']}; maximum {override['maximum_duration_seconds']} seconds; cleanup grace {override['cleanup_grace_seconds']} seconds"
            )
    lines.append("")
    return lines


def claim_transport_lines(value: dict[str, object]) -> list[str]:
    """Render the setup-verified claim helper selected by Project Configurator.

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
            f"configured claim helper {selected} is unavailable; run Project Configurator to select and verify one available helper"
        )

    skill_name = CLAIM_TRANSPORT_SKILLS[selected]
    return [
        CLAIM_TRANSPORT_HEADING,
        "",
        f"Project Configurator selected and verified the {selected} claim helper. Apply agent-claim for claim rules and use the inlined {skill_name} skill to run the helper.",
        "",
        "Use only this configured claim helper. If it cannot start, ask Project Configurator to configure a working helper.",
        "",
        f"----- BEGIN INLINED CLAIM HELPER SKILL: {skill_name} -----",
        inlined_skill_body(skill_name),
        f"----- END INLINED CLAIM HELPER SKILL: {skill_name} -----",
        "",
    ]


def _reconcile_setup_workflow(value: dict[str, object]) -> None:
    """Require persisted setup selectors to match normalized canonical workflow paths."""

    setup = value.get("project_setup")
    if setup is None:
        return
    if not isinstance(setup, dict):
        raise ValueError("project_setup must be a mapping")
    selection = value.get("workflow_selection")
    if not isinstance(selection, dict):
        raise ValueError("workflow_selection must be a mapping")
    canonical_selection, _ = _canonical_workflow_selection(selection)
    persistence, _ = _workflow_configuration(
        canonical_selection,
        "persistence",
        PROVIDER_VALUES,
    )
    commit, _ = _workflow_configuration(
        canonical_selection,
        "commit",
        COMPLETION_VALUES,
    )
    for setup_key, workflow_value in (
        ("persistence", persistence),
        ("commit", commit),
    ):
        setup_value = setup.get(setup_key)
        if setup_value != workflow_value:
            raise ValueError(
                f"project_setup.{setup_key} {setup_value!r} conflicts with "
                f"workflow_selection.{setup_key}.default {workflow_value!r}"
            )


def technology_confirmation_lines(value: dict[str, object]) -> list[str]:
    """Validate and render persisted technology candidates and user confirmation evidence."""

    confirmation = value.get("technology_confirmation")
    if not isinstance(confirmation, dict):
        raise ValueError("technology_confirmation must be a mapping")
    required_keys = {"candidates", "accepted_skills", "rejections", "confirmation"}
    if set(confirmation) != required_keys:
        raise ValueError(
            "technology_confirmation keys must be exactly candidates, accepted_skills, rejections, and confirmation"
        )
    candidates = confirmation["candidates"]
    accepted_skills = confirmation["accepted_skills"]
    rejections = confirmation["rejections"]
    if not isinstance(candidates, list):
        raise ValueError("technology_confirmation.candidates must be a list")
    if not isinstance(accepted_skills, list):
        raise ValueError("technology_confirmation.accepted_skills must be a list")
    normalized_accepted_skills = [
        _normalized_skill_id(
            skill,
            f"technology_confirmation.accepted_skills[{index}]",
        )
        for index, skill in enumerate(accepted_skills)
    ]
    if not isinstance(rejections, list):
        raise ValueError("technology_confirmation.rejections must be a list")

    accepted_candidates: list[str] = []
    accepted_bindings: list[tuple[str, str]] = []
    rejected_candidates: list[str] = []
    candidate_lines: list[str] = []
    for index, candidate in enumerate(candidates):
        prefix = f"technology_confirmation.candidates[{index}]"
        if not isinstance(candidate, dict):
            raise ValueError(f"{prefix} must be a mapping")
        if set(candidate) != {"scope", "skill", "evidence", "conflicts", "disposition"}:
            raise ValueError(
                f"{prefix} keys must be exactly scope, skill, evidence, conflicts, and disposition"
            )
        scope = _normalized_technology_scope(candidate.get("scope"), f"{prefix}.scope")
        skill = _normalized_skill_id(candidate.get("skill"), f"{prefix}.skill")
        evidence = candidate.get("evidence")
        conflicts = candidate.get("conflicts")
        disposition = candidate.get("disposition")
        if not isinstance(evidence, list) or not evidence or not all(
            isinstance(fact, str) and fact for fact in evidence
        ):
            raise ValueError(f"{prefix}.evidence must be a non-empty list of strings")
        evidence = [
            _single_line_rendered_text(fact, f"{prefix}.evidence[{fact_index}]")
            for fact_index, fact in enumerate(evidence)
        ]
        if not isinstance(conflicts, list) or not all(
            isinstance(conflict, str) and conflict for conflict in conflicts
        ):
            raise ValueError(f"{prefix}.conflicts must be a list of non-empty strings")
        conflicts = [
            _single_line_rendered_text(
                conflict,
                f"{prefix}.conflicts[{conflict_index}]",
            )
            for conflict_index, conflict in enumerate(conflicts)
        ]
        if disposition not in {"accepted", "rejected"}:
            raise ValueError(f"{prefix}.disposition must be accepted or rejected")
        target = accepted_candidates if disposition == "accepted" else rejected_candidates
        target.append(skill)
        if disposition == "accepted":
            accepted_bindings.append((scope, skill))
        conflict_text = "; ".join(conflicts) if conflicts else "none"
        candidate_lines.append(
            f"- Candidate {skill} for {scope}: {disposition}; evidence: {'; '.join(evidence)}; conflicts: {conflict_text}"
        )
    if normalized_accepted_skills != accepted_candidates:
        raise ValueError(
            "technology_confirmation.accepted_skills must match accepted candidate dispositions in order"
        )
    routed_bindings: list[tuple[str, str]] = []
    for loadout_index, loadout in enumerate(loadouts(value)):
        pattern = _normalized_technology_scope(
            loadout.get("pathPattern", loadout.get("pattern")),
            f"technology_skill_loadouts[{loadout_index}].pathPattern",
        )
        skills = loadout.get("skills", loadout.get("required_skills", []))
        if not isinstance(skills, list):
            raise ValueError(f"technology_skill_loadouts[{loadout_index}].skills must be a list")
        for skill_index, skill in enumerate(skills):
            routed_bindings.append(
                (
                    pattern,
                    _normalized_skill_id(
                        skill,
                        f"technology_skill_loadouts[{loadout_index}].skills[{skill_index}]",
                    ),
                )
            )
    if routed_bindings != accepted_bindings:
        raise ValueError(
            "technology_confirmation accepted scope and skill bindings must match technology_skill_loadouts in order"
        )

    rejection_names: list[str] = []
    rejection_lines: list[str] = []
    for index, rejection in enumerate(rejections):
        prefix = f"technology_confirmation.rejections[{index}]"
        if not isinstance(rejection, dict) or set(rejection) != {"skill", "reason"}:
            raise ValueError(f"{prefix} must contain exactly skill and reason")
        skill = _normalized_skill_id(rejection.get("skill"), f"{prefix}.skill")
        reason = rejection.get("reason")
        if not isinstance(reason, str) or not reason:
            raise ValueError(f"{prefix}.reason must be a non-empty string")
        reason = _single_line_rendered_text(reason, f"{prefix}.reason")
        rejection_names.append(skill)
        rejection_lines.append(f"- Rejected {skill}: {reason}")
    if rejection_names != rejected_candidates:
        raise ValueError(
            "technology_confirmation.rejections must match rejected candidate dispositions in order"
        )

    user_confirmation = confirmation["confirmation"]
    if not isinstance(user_confirmation, dict):
        raise ValueError("technology_confirmation.confirmation must be a mapping")
    if set(user_confirmation) != {"status", "evidence"}:
        raise ValueError(
            "technology_confirmation.confirmation keys must be exactly status and evidence"
        )
    if user_confirmation.get("status") != "confirmed":
        raise ValueError("technology_confirmation.confirmation.status must be confirmed")
    evidence_reference = user_confirmation.get("evidence")
    if not isinstance(evidence_reference, str) or not evidence_reference.strip():
        raise ValueError(
            "technology_confirmation.confirmation.evidence must be a non-empty auditable reference"
        )
    evidence_reference = _single_line_rendered_text(
        evidence_reference,
        "technology_confirmation.confirmation.evidence",
    )
    accepted_text = ", ".join(normalized_accepted_skills) if normalized_accepted_skills else "none"
    lines = [
        f"- Technology candidates: {len(candidates)}",
        *candidate_lines,
        f"- Accepted technology skills: {accepted_text}",
        *(rejection_lines or ["- Technology rejections: none"]),
        f"- Confirmation evidence: {evidence_reference}",
    ]
    return lines


def setup_lines(value: dict[str, object]) -> list[str]:
    """Validate and render persisted Basic or Advanced project setup selections."""

    setup = value.get("project_setup")
    if setup is None:
        return []
    if not isinstance(setup, dict):
        raise ValueError("project_setup must be a mapping")
    allowed_keys = {
        "mode",
        "concurrent_tasking",
        "concurrent_capacity",
        "persistence",
        "commit",
        "documentation",
        "core_skill_delivery",
        "technology_skill_delivery",
        "technology_confirmation_required",
    }
    unsupported = set(setup) - allowed_keys
    if unsupported:
        raise ValueError("project_setup contains unsupported fields: " + ", ".join(sorted(unsupported)))
    mode = setup.get("mode")
    if mode not in SETUP_MODES:
        raise ValueError("project_setup.mode must be basic or advanced")
    concurrent = setup.get("concurrent_tasking")
    if not isinstance(concurrent, bool):
        raise ValueError("project_setup.concurrent_tasking must be true or false")
    capacity = setup.get("concurrent_capacity")
    if not concurrent and capacity is not None:
        raise ValueError(
            "project_setup.concurrent_capacity is allowed only when concurrent_tasking is true"
        )
    if concurrent and (not isinstance(capacity, int) or isinstance(capacity, bool) or capacity < 1):
        raise ValueError(
            "project_setup.concurrent_capacity must be a positive integer when concurrent_tasking is true"
        )
    persistence = setup.get("persistence")
    commit = setup.get("commit")
    documentation = setup.get("documentation")
    technology_delivery = setup.get("technology_skill_delivery")
    if persistence not in PROVIDER_VALUES:
        raise ValueError("project_setup.persistence has an unsupported value")
    if commit not in COMPLETION_VALUES:
        raise ValueError("project_setup.commit has an unsupported value")
    if documentation not in DOCUMENTATION_CHOICES:
        raise ValueError("project_setup.documentation must be none, wiki, specifications, or both")
    if technology_delivery not in SKILL_DELIVERY_MODES:
        raise ValueError("project_setup.technology_skill_delivery must be by-reference or inline")
    if setup.get("technology_confirmation_required") is not True:
        raise ValueError("project_setup.technology_confirmation_required must be true")
    core_delivery = setup.get("core_skill_delivery")
    if not isinstance(core_delivery, dict):
        raise ValueError("project_setup.core_skill_delivery must be a mapping")
    if set(core_delivery) != {"mode", "source"}:
        raise ValueError("project_setup.core_skill_delivery keys must be exactly mode and source")
    if core_delivery.get("mode") not in SKILL_DELIVERY_MODES:
        raise ValueError("project_setup.core_skill_delivery.mode must be by-reference or inline")
    if core_delivery.get("source") != "installed-agent-metadata":
        raise ValueError(
            "project_setup.core_skill_delivery.source must be installed-agent-metadata; regenerate and install compatible native agents before changing the project value"
        )
    if mode == "basic":
        expected_basic = {
            "concurrent_tasking": False,
            "persistence": "none",
            "commit": "direct-main",
            "technology_skill_delivery": "by-reference",
        }
        for key, expected in expected_basic.items():
            if setup.get(key) != expected:
                raise ValueError(f"project_setup.{key} must be {expected!r} in Basic mode")
        if documentation not in {"none", "wiki"}:
            raise ValueError("project_setup.documentation must be none or wiki in Basic mode")
        wiki_answer = "Yes" if documentation == "wiki" else "No"
        selections = [
            "- Setup mode: Basic",
            "- Set: Concurrent tasking No",
            "- Set: Persistence none",
            "- Set: Commit direct-main",
            f"- Documentation question: Create the Wiki? {wiki_answer} (default Yes)",
            f"- Set: Core skill delivery {core_delivery['mode']}",
            "- Set: Technology skill delivery by-reference",
        ]
    else:
        if documentation == "none":
            raise ValueError(
                "project_setup.documentation must be wiki, specifications, or both in Advanced mode"
            )
        selections = [
            "- Setup mode: Advanced",
            f"- Concurrent tasking: {'Yes' if concurrent else 'No'}",
            f"- Persistence: {persistence}",
            f"- Commit: {commit}",
            f"- Documentation: {documentation}",
            f"- Set: Core skill delivery {core_delivery['mode']}",
            f"- Technology skill delivery: {technology_delivery}",
        ]
        if concurrent:
            selections.insert(2, f"- Concurrent capacity: {capacity}")
    selections.append(
        "- Technology confirmation: required; show detected candidates, evidence, conflicts, and the user-confirmed selection."
    )
    selections.extend(technology_confirmation_lines(value))
    selections.append("")
    return ["## Project Setup Selections", "", *selections]


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


def _resolved_inline_technology_delivery(
    value: dict[str, object],
    requested: bool | None,
) -> bool:
    """Resolve default by-reference delivery against the persisted setup selection."""

    setup = value.get("project_setup")
    if not isinstance(setup, dict):
        return False if requested is None else requested
    configured = setup.get("technology_skill_delivery")
    if configured not in SKILL_DELIVERY_MODES:
        raise ValueError("project_setup.technology_skill_delivery must be by-reference or inline")
    configured_inline = configured == "inline"
    if requested is not None and requested is not configured_inline:
        requested_label = "inline" if requested else "by-reference"
        raise ValueError(
            f"explicit technology delivery {requested_label} conflicts with "
            f"project_setup.technology_skill_delivery {configured!r}"
        )
    return configured_inline


def render(
    value: dict[str, object],
    inline_tech_skills: bool | None = None,
    include_project_skill_extensions: bool = True,
) -> str:
    """Render configured root AGENTS.md project and skill sections.

    value is the mapping loaded from PROJECT.yaml. workflow_selection and
    resource_coordination are required.
    agent_claim_transport is required only when resource_coordination selects agent-claim
    and must be absent when resource_coordination selects none.
    Technology guidance is always produced from the configured loadouts, and an optional
    project_skill_extensions list produces the final root-only reference section when
    include_project_skill_extensions is true. The optional inline_tech_skills request must
    agree with project_setup.technology_skill_delivery when setup metadata exists. With no
    setup metadata or explicit request, delivery defaults to by-reference. Inline delivery
    embeds each referenced bundled skill body. agent-claim is referenced and its selected
    claim helper is embedded only when resource coordination selects agent-claim.

    The return value is the complete generated Markdown text and ends with a newline.
    Rendering does not write an output file, but inlined rendering reads bundled SKILL.md
    files. Invalid workflow, project extension, or source-evidence configuration,
    unsafe skill names, and invalid skill frontmatter raise ValueError. Missing or unreadable
    skill files raise OSError, and malformed YAML may raise yaml.YAMLError.
    """
    _reconcile_setup_workflow(value)
    inline_tech_skills = _resolved_inline_technology_delivery(value, inline_tech_skills)
    lines: list[str] = []
    workflow = workflow_lines(value)
    coordination = resource_coordination_lines(value)
    lines.extend(coordination)
    if coordination:
        lines.extend(claim_transport_lines(value))
    lines.extend(setup_lines(value))
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
            skill = _normalized_skill_id(evidence.get("skill"), f"{row_prefix}.skill")
            if skill in RESOURCE_COORDINATION_RESERVED_SKILLS:
                raise ValueError(
                    f"{row_prefix}.skill id {skill!r} is reserved for "
                    "resource_coordination; remove it from technology_skill_loadouts"
                )
            facts = evidence.get("evidence")
            facts_prefix = f"{row_prefix}.evidence"
            if not isinstance(facts, list):
                raise ValueError(f"{facts_prefix} must be a list of strings")
            normalized_facts: list[str] = []
            for fact_index, fact in enumerate(facts):
                if not isinstance(fact, str):
                    raise ValueError(f"{facts_prefix}[{fact_index}] must be a string")
                normalized_facts.append(
                    _single_line_rendered_text(fact, f"{facts_prefix}[{fact_index}]")
                )
            facts = normalized_facts
            if facts:
                evidence_lines.append(f"  - {skill} evidence: {'; '.join(facts)}")
        pattern_value = item.get("pathPattern", item.get("pattern"))
        skills = item.get("skills", item.get("required_skills", []))
        pattern = _normalized_technology_scope(
            pattern_value,
            f"technology_skill_loadouts[{loadout_index}].pathPattern",
        )
        if not isinstance(skills, list):
            raise ValueError(f"technology_skill_loadouts[{loadout_index}].skills must be a list")
        names: list[str] = []
        for skill_index, skill in enumerate(skills):
            normalized_skill = _normalized_skill_id(
                skill,
                f"technology_skill_loadouts[{loadout_index}].skills[{skill_index}]",
            )
            if normalized_skill in RESOURCE_COORDINATION_RESERVED_SKILLS:
                raise ValueError(
                    f"technology_skill_loadouts[{loadout_index}].skills[{skill_index}] skill id "
                    f"{normalized_skill!r} is reserved for resource_coordination; remove it "
                    "from technology_skill_loadouts"
                )
            names.append(normalized_skill)
        if not names:
            if item.get("status") != "NO_VARIANT":
                continue
            fallback = _single_line_rendered_text(
                item.get("fallback", "General model training"),
                f"technology_skill_loadouts[{loadout_index}].fallback",
            )
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
    """Run the project-guidance renderer command-line interface.

    arguments is an explicit CLI argument sequence for programmatic callers, or None to
    parse the process arguments. Render mode without an output path prints generated
    coordination, workflow, and technology Markdown. Output mode writes the generated
    Markdown to its file: it creates a missing file or replaces one only with the replace
    option. Every successful render or output mode returns 0.

    File creation and updates are the only repository side effects. Handled OSError,
    ValueError, and yaml.YAMLError failures are printed to standard error and return 1.
    Argument-parser usage failures raise SystemExit with argparse's exit code, normally 2.
    """
    parser = argparse.ArgumentParser(
        description="Render resource coordination, workflow selectors, technology guidance, and root project skill references."
    )
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace an existing output file. Without this option, --output is create-only.",
    )
    parser.add_argument(
        "--inline-tech-skills",
        type=parse_boolean,
        default=None,
        metavar="true|false",
        help="Statically embed discovered technology skills. Defaults to the persisted project setup selection, or false when setup metadata is absent.",
    )
    args = parser.parse_args(arguments)
    try:
        project = load_yaml(args.project)
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
            if args.output.exists() and not args.replace:
                raise ValueError(
                    f"output file already exists: {args.output}; use --replace to replace it"
                )
            args.output.write_text(content, encoding="utf-8")
        else:
            print(content, end="")
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
