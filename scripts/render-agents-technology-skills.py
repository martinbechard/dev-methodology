#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Renders project authority, workflow selectors, and unconditional folder technology guidance from PROJECT.yaml.

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from collections.abc import Sequence
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
SKILL_FILE_NAME = "SKILL.md"
FRONTMATTER_DELIMITER = "---"
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")
PROCESS_NAME_PATTERN = re.compile(r"^(?:[a-z0-9][a-z0-9-]*|UNSET)$")
AUTHORITY_HEADING = "## Agent And Skill Definition Approval"
PROVENANCE_REFERENCE_PATTERNS = {
    "user-message": re.compile(r"^thread:[^/\s]+/message:[^/\s]+$"),
    "delegated-user-direction": re.compile(r"^thread:[^/\s]+/delegation:[^/\s]+$"),
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
    for key in ("conceptual_agents", "distributed_skills", "adapter_skills", "definition_metadata"):
        _required_patterns(sources, key, "definition_change_authority.governed_sources")
    _required_patterns(policy, "generated_mirrors", "definition_change_authority")
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
    assert isinstance(generated, list)
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
        ("distributed_skills", "Distributed skill definitions"),
        ("adapter_skills", "Adapter-owned skill definitions"),
        ("definition_metadata", "Definition-affecting metadata and model inputs"),
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
        "- Regenerate these mirrors only from an approved canonical definition change. The regeneration itself does not require a second approval.",
        "",
        "When a test fails, investigate whether the test, fixture, assertion, or expected result is incorrect before proposing a definition change. Ordinary authorized implementation changes and corrections to incorrect tests remain allowed when they do not alter a governed definition.",
        "",
    ])
    return lines


def _normalize_project_path(path: str) -> str:
    """Normalize one relative project path without resolving parent traversal."""

    portable = path.replace("\\", "/")
    if portable.startswith("/"):
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
    assert isinstance(sources, dict)
    assert isinstance(generated, list)
    source_patterns = [pattern for patterns in sources.values() for pattern in patterns]
    if _matches(normalized, generated):
        if regenerated_from and _matches(regenerated_from, source_patterns):
            approval_outcome = _approval_outcome(policy, approval, regenerated_from)
            if approval_outcome == "MATCHED":
                return {"outcome": "ALLOWED_APPROVED_REGENERATION", "classification": "generated-mirror"}
            return {"outcome": approval_outcome, "classification": "generated-mirror"}
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


def workflow_lines(value: dict[str, object]) -> list[str]:
    """Render selector-only work-item and backlog workflow guidance."""

    selection = value.get("workflow_selection")
    if selection is None:
        return []
    if not isinstance(selection, dict):
        raise ValueError("workflow_selection must be a mapping")

    lines = [
        "## Work Item And Backlog Workflows",
        "",
        "Project Configurator owns these selectors. They choose role-owned procedures without duplicating those procedures here.",
        "",
    ]
    for key, label in (("workitem", "work-item"), ("backlog", "backlog")):
        configuration = selection.get(key)
        if not isinstance(configuration, dict):
            raise ValueError(f"workflow_selection.{key} must be a mapping")
        default = configuration.get("default")
        if not isinstance(default, str) or not PROCESS_NAME_PATTERN.fullmatch(default):
            raise ValueError(f"workflow_selection.{key}.default must be a process identifier or UNSET")
        lines.append(f"- Default {label} process: {default}.")
        overrides = configuration.get("folder_overrides", [])
        if not isinstance(overrides, list):
            raise ValueError(f"workflow_selection.{key}.folder_overrides must be a list")
        for override in overrides:
            if not isinstance(override, dict):
                raise ValueError(f"workflow_selection.{key}.folder_overrides entries must be mappings")
            pattern = override.get("pattern")
            process = override.get("process")
            if not isinstance(pattern, str) or not pattern:
                raise ValueError(f"workflow_selection.{key} override pattern must be a non-empty string")
            if not isinstance(process, str) or not PROCESS_NAME_PATTERN.fullmatch(process):
                raise ValueError(f"workflow_selection.{key} override process must be a process identifier or UNSET")
            lines.append(f"- {pattern}: use the {process} {label} process.")
    lines.extend([
        "",
        "When a required selector is UNSET, the pertinent agent asks the user before that operation and does not infer a process from repository or hosting evidence.",
        "",
    ])
    return lines


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


def render(value: dict[str, object], inline_tech_skills: bool = True) -> str:
    """Render root AGENTS.md workflow and technology sections."""
    lines: list[str] = definition_change_authority_lines(value)
    lines.extend(workflow_lines(value))
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
    for item in loadouts(value):
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
        for evidence in item.get("sourceEvidence", item.get("source_evidence", [])):
            if isinstance(evidence, dict) and isinstance(evidence.get("skill"), str):
                facts = evidence.get("evidence", [])
                if isinstance(facts, list) and facts:
                    lines.append(f"  - {evidence['skill']} evidence: {'; '.join(str(fact) for fact in facts)}")
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
    return "\n".join(lines)


def main(arguments: Sequence[str] | None = None) -> int:
    """Render configured AGENTS.md sections without replacing an output file implicitly."""
    parser = argparse.ArgumentParser(description="Render AGENTS.md workflow selectors and unconditional technology skill guidance.")
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
        content = render(project, args.inline_tech_skills)
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
