#!/usr/bin/env python3
# Copyright (c) 2026 Martin.Bechard@DevConsult.ca
# AI attribution: Modified with AI assistance.
# Summary: Generates the interactive agent-to-skill hierarchy SVG.

from __future__ import annotations

import argparse
import html
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
ROLES_ROOT = ROOT / "agents" / "roles"
ROLE_SCHEMA_PATH = ROOT / "agents" / "role-schema.yaml"
SKILLS_ROOT = ROOT / "skills"
CATEGORIES_PATH = ROOT / "design" / "skill-categories.yaml"
ROLE_CATALOG_GROUPS_PATH = ROOT / "design" / "role-catalog-groups.yaml"
OUTPUT_PATH = ROOT / "design" / "agent-skill-hierarchy.svg"
STACK_AND_DOMAIN_CATEGORY = "stack-and-domain"
HIERARCHY_SKILL_CATEGORY_PRIORITY = (
    "development-practice",
    "wiki-and-knowledge",
)
ROW_HEIGHT = 30
TOP = 150
ROLE_X = 30
SKILL_X = 760
ROLE_WIDTH = 320
SKILL_WIDTH = 360
SVG_WIDTH = 1150
ROLE_DISPLAY_ACRONYMS = {"e2e": "E2E", "qa": "QA", "ux": "UX"}
BACKLOG_MANAGEMENT_ROLES = (
    "dev-backlog-coordinator",
    "dev-backlog-steward",
    "dev-orchestrator",
)


def _load_yaml(path: Path) -> dict[str, object]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected YAML object: {path}")
    return value


def _role_skill_entries(role: dict[str, object]) -> list[tuple[str, bool]]:
    value = role.get("skills")
    if not isinstance(value, list):
        raise ValueError(f"Conceptual agent definition {role.get('name')} skills must be a list.")
    entries: list[tuple[str, bool]] = []
    for item in value:
        if isinstance(item, str):
            entries.append((item, False))
        elif isinstance(item, dict) and len(item) == 1:
            name, metadata = next(iter(item.items()))
            entries.append(
                (str(name), isinstance(metadata, dict) and "condition" in metadata)
            )
        else:
            raise ValueError(
                f"Conceptual agent definition {role.get('name')} has an invalid skill entry: {item}"
            )
    return entries


def _shared_role_skill_entries() -> list[tuple[str, bool]]:
    """Return the fixed skills that the role schema adds to every role."""

    schema = _load_yaml(ROLE_SCHEMA_PATH)
    fixed_behavior = schema.get("fixedBehavior")
    if not isinstance(fixed_behavior, dict):
        raise ValueError("Role schema fixedBehavior must be an object.")
    entries = _role_skill_entries(
        {
            "name": "role schema",
            "skills": fixed_behavior.get("sharedSkills"),
        }
    )
    if any(conditional for _name, conditional in entries):
        raise ValueError("Role schema shared skills cannot be conditional.")
    return entries


def _effective_role_skill_entries(
    role: dict[str, object],
    shared_entries: list[tuple[str, bool]],
) -> list[tuple[str, bool]]:
    """Combine schema-owned shared skills with one role's declared skills."""

    role_entries = _role_skill_entries(role)
    duplicate_names = sorted(
        {name for name, _conditional in shared_entries}
        & {name for name, _conditional in role_entries}
    )
    if duplicate_names:
        raise ValueError(
            f"Conceptual agent definition {role.get('name')} repeats shared skills: "
            + ", ".join(duplicate_names)
        )
    return [*shared_entries, *role_entries]


def _role_agent_dependencies(role: dict[str, object]) -> list[str]:
    value = role.get("agentDependencies", [])
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        raise ValueError(
            f"Conceptual agent definition {role.get('name')} agentDependencies must be a list of conceptual definition names."
        )
    dependencies = [item.strip() for item in value]
    if len(dependencies) != len(set(dependencies)):
        raise ValueError(
            f"Conceptual agent definition {role.get('name')} agentDependencies contains duplicates."
        )
    return dependencies


def _skill_category(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    frontmatter = yaml.safe_load(parts[1])
    if not isinstance(frontmatter, dict):
        raise ValueError(f"Expected skill frontmatter: {path}")
    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        raise ValueError(f"Expected skill metadata: {path}")
    return str(frontmatter["name"]), str(metadata["category"])


def _escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def _display_name(identifier: str) -> str:
    return " ".join(
        ROLE_DISPLAY_ACRONYMS.get(word, word.title())
        for word in identifier.split("-")
    )


def _load_role_catalog_groups(
    roles: list[dict[str, object]],
    conceptual_group_order: list[str],
) -> tuple[list[dict[str, str]], dict[str, str]]:
    payload = _load_yaml(ROLE_CATALOG_GROUPS_PATH)
    if payload.get("schema") != "agent-catalog-groups" or payload.get("version") != 1:
        raise ValueError("Role catalog groups must use agent-catalog-groups schema version 1.")
    raw_groups = payload.get("groups")
    if not isinstance(raw_groups, list) or not raw_groups:
        raise ValueError("Role catalog groups must be a non-empty list.")

    groups: list[dict[str, str]] = []
    for item in raw_groups:
        if not isinstance(item, dict):
            raise ValueError("Each role catalog group must be an object.")
        group_id = item.get("id")
        label = item.get("label")
        if not isinstance(group_id, str) or not group_id.strip():
            raise ValueError("Each role catalog group must have a non-empty id.")
        if not isinstance(label, str) or not label.strip():
            raise ValueError(f"Role catalog group {group_id} must have a non-empty label.")
        groups.append({"id": group_id.strip(), "label": label.strip()})

    group_ids = [group["id"] for group in groups]
    if len(group_ids) != len(set(group_ids)):
        raise ValueError("Role catalog group ids must be unique.")
    missing_conceptual_groups = set(conceptual_group_order) - set(group_ids)
    if missing_conceptual_groups:
        raise ValueError(
            "Role catalog groups omit conceptual groups: "
            + ", ".join(sorted(missing_conceptual_groups))
        )

    raw_overrides = payload.get("role_overrides", {})
    if not isinstance(raw_overrides, dict):
        raise ValueError("Role catalog role_overrides must be an object.")
    roles_by_name = {str(role["name"]): role for role in roles}
    unknown_roles = set(raw_overrides) - set(roles_by_name)
    if unknown_roles:
        raise ValueError(
            "Role catalog overrides reference unknown roles: "
            + ", ".join(sorted(unknown_roles))
        )

    assignments: dict[str, str] = {}
    for role_name, override in raw_overrides.items():
        if not isinstance(override, dict):
            raise ValueError(f"Role catalog override {role_name} must be an object.")
        group_id = override.get("group")
        source = override.get("source")
        evidence = override.get("evidence")
        if group_id not in group_ids:
            raise ValueError(
                f"Role catalog override {role_name} references unknown group {group_id}."
            )
        if source != roles_by_name[role_name]["sourcePath"]:
            raise ValueError(
                f"Role catalog override {role_name} must cite its conceptual source path."
            )
        if not isinstance(evidence, str) or not evidence.strip():
            raise ValueError(
                f"Role catalog override {role_name} must include source-backed evidence."
            )
        assignments[role_name] = str(group_id)

    return groups, assignments


def _visible_skill_categories(
    skills_by_category: dict[str, list[str]],
) -> list[tuple[str, list[str]]]:
    category_data = _load_yaml(CATEGORIES_PATH).get("categories")
    if not isinstance(category_data, list):
        raise ValueError("Skill categories must be a list.")
    category_order = [
        str(item["id"])
        for item in category_data
        if isinstance(item, dict) and "id" in item
    ]
    unknown_categories = set(skills_by_category) - set(category_order)
    if unknown_categories:
        raise ValueError(
            "Skills reference unknown categories: "
            + ", ".join(sorted(unknown_categories))
        )
    available_category_ids = [
        category_id
        for category_id in category_order
        if category_id != STACK_AND_DOMAIN_CATEGORY
    ]
    visible_category_ids = [
        category_id
        for category_id in HIERARCHY_SKILL_CATEGORY_PRIORITY
        if category_id in available_category_ids
    ]
    visible_category_ids.extend(
        category_id
        for category_id in available_category_ids
        if category_id not in visible_category_ids
    )
    return [
        (category_id, sorted(skills_by_category[category_id]))
        for category_id in visible_category_ids
        if category_id in skills_by_category
    ]


def _role_node(
    y: int,
    role_name: str,
    display_name: str,
    secondary: str,
) -> str:
    return (
        f'<g class="role-node" data-role="{_escape(role_name)}" '
        f'data-display-name="{_escape(display_name)}" role="button" tabindex="0" '
        f'aria-pressed="false" aria-label="Select {_escape(display_name)}">'
        f'<title>Select {_escape(display_name)} to isolate its skills and dependencies</title>'
        f'<rect x="{ROLE_X}" y="{y}" width="{ROLE_WIDTH}" height="24" rx="5" '
        f'class="node role"/>'
        f'<text x="{ROLE_X + 12}" y="{y + 16}">{_escape(role_name)}</text>'
        f'<text x="{ROLE_X + ROLE_WIDTH - 12}" y="{y + 16}" text-anchor="end" '
        f'class="secondary">{_escape(secondary)}</text>'
        "</g>"
    )


def _skill_node(
    y: int,
    skill_name: str,
    secondary: str,
    modifier: str,
) -> str:
    return (
        f'<g class="skill-node" data-skill="{_escape(skill_name)}" role="button" '
        f'tabindex="0" aria-pressed="false" '
        f'aria-label="Select skill {_escape(skill_name)}">'
        f'<title>Select {_escape(skill_name)} to isolate the agents using it</title>'
        f'<rect x="{SKILL_X}" y="{y}" width="{SKILL_WIDTH}" height="24" rx="5" '
        f'class="node skill{modifier}"/>'
        f'<path d="M {SKILL_X + 1} {y + 5} V {y + 19}" class="selection-marker"/>'
        f'<text x="{SKILL_X + 12}" y="{y + 16}">{_escape(skill_name)}</text>'
        f'<text x="{SKILL_X + SKILL_WIDTH - 12}" y="{y + 16}" text-anchor="end" '
        f'class="secondary">{_escape(secondary)}</text>'
        "</g>"
    )


def build_svg() -> str:
    """Render the interactive conceptual-definition-to-skill map from repository sources."""
    shared_skill_entries = _shared_role_skill_entries()
    roles: list[dict[str, object]] = []
    for path in sorted(ROLES_ROOT.glob("*/*.role.yaml")):
        role = _load_yaml(path)
        role["group"] = path.parent.name
        role["sourcePath"] = str(path.relative_to(ROOT))
        roles.append(role)

    role_names = {str(role["name"]) for role in roles}
    missing_backlog_roles = set(BACKLOG_MANAGEMENT_ROLES) - role_names
    if missing_backlog_roles:
        raise ValueError(
            "Backlog management focus references unknown conceptual definitions: "
            + ", ".join(sorted(missing_backlog_roles))
        )
    agent_dependencies: list[tuple[str, str]] = []
    for role in roles:
        source_role = str(role["name"])
        for target_role in _role_agent_dependencies(role):
            if target_role not in role_names:
                raise ValueError(
                    f"Conceptual agent definition {source_role} references unknown agent dependency {target_role}."
                )
            if target_role == source_role:
                raise ValueError(f"Conceptual agent definition {source_role} cannot depend on itself.")
            agent_dependencies.append((source_role, target_role))

    role_group_order = _load_yaml(ROLE_SCHEMA_PATH).get("roleGroups")
    if not isinstance(role_group_order, list) or not all(
        isinstance(group, str) for group in role_group_order
    ):
        raise ValueError("Conceptual agent definition groups must be a list of identifiers.")
    catalog_groups, catalog_group_by_role = _load_role_catalog_groups(
        roles,
        role_group_order,
    )

    skills_by_category: dict[str, list[str]] = {}
    for path in sorted(SKILLS_ROOT.glob("*/SKILL.md")):
        name, category = _skill_category(path)
        skills_by_category.setdefault(category, []).append(name)
    visible_skill_categories = _visible_skill_categories(skills_by_category)

    role_y: dict[str, int] = {}
    current_y = TOP
    grouped_roles: dict[str, list[dict[str, object]]] = {}
    roles_by_group: dict[str, list[dict[str, object]]] = {}
    for role in roles:
        catalog_group = catalog_group_by_role.get(
            str(role["name"]),
            str(role["group"]),
        )
        roles_by_group.setdefault(catalog_group, []).append(role)
    catalog_group_order = [group["id"] for group in catalog_groups]
    unknown_role_groups = set(roles_by_group) - set(catalog_group_order)
    if unknown_role_groups:
        raise ValueError(
            "Catalog roles reference unknown groups: " + ", ".join(sorted(unknown_role_groups))
        )
    for group in catalog_group_order:
        group_roles = roles_by_group.get(group)
        if group_roles:
            grouped_roles[group] = group_roles
    for group_roles in grouped_roles.values():
        current_y += ROW_HEIGHT
        for role in group_roles:
            role_y[str(role["name"])] = current_y
            current_y += ROW_HEIGHT
        current_y += 12

    skill_y: dict[str, int] = {}
    skill_current_y = TOP
    for _, skill_names in visible_skill_categories:
        skill_current_y += ROW_HEIGHT
        for skill_name in skill_names:
            skill_y[skill_name] = skill_current_y
            skill_current_y += ROW_HEIGHT
        skill_current_y += 12

    height = max(current_y, skill_current_y) + 90
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" class="show-agent-dependencies" width="{SVG_WIDTH}" height="{height}" '
        f'viewBox="0 0 {SVG_WIDTH} {height}" role="group" aria-labelledby="title desc">',
        '<title id="title">Interactive agent and skill hierarchy</title>',
        '<desc id="desc">Select an agent to highlight its skills, or select a skill to highlight every agent using it. Turn on agent dependencies to reveal arrows from using agents to used agents. Setup-time stack and domain skills are intentionally omitted because conceptual agent definitions do not link to them.</desc>',
        '<defs><marker id="dependency-arrow" viewBox="0 0 7 8" refX="6" refY="4" markerWidth="7" markerHeight="8" markerUnits="userSpaceOnUse" orient="auto"><path d="M 1 1.25 L 6 4 L 1 6.75" class="dependency-arrowhead"/></marker></defs>',
        """<style><![CDATA[
text{font-family:ui-sans-serif,system-ui,sans-serif;font-size:12px;fill:#172033}
.heading{font-size:18px;font-weight:700}.group{font-size:13px;font-weight:700;fill:#334155}
.secondary{font-size:9px;fill:#64748b}.instruction{font-size:11px;fill:#475569}
.status{font-size:11px;font-weight:650;fill:#0f766e}
.node{transition:fill 150ms ease,stroke 150ms ease,stroke-width 150ms ease}
.node.role{fill:#f8fafc;stroke:#64748b}.node.skill{fill:#fff7e6;stroke:#b45309}
.node.skill.conditional{fill:#eeeafd;stroke:#7c3aed}
.edge{fill:none;stroke:#94a3b8;stroke-width:1;opacity:.32;transition:opacity 150ms ease,stroke 150ms ease,stroke-width 150ms ease}
.edge.conditional-edge{stroke:#7c3aed}.edge.active{stroke:#0f766e;stroke-width:2.4;opacity:1}.edge.dimmed{opacity:.012}
.dependency-edge{fill:none;stroke:#2563eb;stroke-width:1.8;opacity:0;pointer-events:none;transition:opacity 150ms ease,stroke-width 150ms ease}.dependency-arrowhead{fill:none;stroke:#2563eb;stroke-width:1.35;stroke-linecap:round;stroke-linejoin:round}
.show-agent-dependencies .dependency-edge{opacity:.32}.show-agent-dependencies .dependency-edge.active{stroke-width:3;opacity:1}.show-agent-dependencies .dependency-edge.dimmed{opacity:.08}
.role-node,.skill-node{cursor:pointer;outline:none;transition:opacity 150ms ease}
.role-node:hover .node,.role-node:focus .node,.skill-node:hover .node,.skill-node:focus .node{stroke:#0f766e;stroke-width:2.2}
.role-node:focus .node,.skill-node:focus .node{stroke-dasharray:4 2}
.role-node.selected .node,.skill-node.selected .node{fill:#dff7f0;stroke:#0f766e;stroke-width:3;stroke-dasharray:none}
.role-node.dimmed .node,.skill-node.dimmed .node{fill:#f8fafc;stroke:#64748b}
.role-node.dimmed text,.skill-node.dimmed text{fill:#64748b}.role-node.active .node,.skill-node.active .node{stroke:#0f766e;stroke-width:2.6}
.selection-marker{fill:none;stroke:#0f766e;stroke-width:4;opacity:0}.skill-node.active .selection-marker,.skill-node.selected .selection-marker{opacity:1}
.reset-control,.view-control{cursor:pointer;outline:none}.reset-control rect{fill:#fff;stroke:#0f766e}.reset-control text{font-size:11px;font-weight:700;fill:#0f766e}
.view-control rect{fill:#0f766e;stroke:#0f766e}.view-control text{font-size:11px;font-weight:700;fill:#fff}
.backlog-focus-control{cursor:pointer;outline:none}.backlog-focus-control rect{fill:#eff6ff;stroke:#2563eb}.backlog-focus-control text{font-size:11px;font-weight:700;fill:#1d4ed8}.backlog-focus-control.active rect{fill:#2563eb}.backlog-focus-control.active text{fill:#fff}
.dependency-toggle{cursor:pointer;outline:none}.dependency-toggle .toggle-surface{fill:#fff;stroke:#2563eb}.dependency-toggle .toggle-box{fill:#fff;stroke:#2563eb;stroke-width:1.5}.dependency-toggle text{font-size:11px;font-weight:700;fill:#1d4ed8}.dependency-toggle .checkmark{fill:none;stroke:#fff;stroke-width:2;opacity:0}.dependency-toggle.checked .toggle-box{fill:#2563eb}.dependency-toggle.checked .checkmark{opacity:1}
.dependency-toggle:hover .toggle-surface,.dependency-toggle:focus .toggle-surface{stroke-width:2}.dependency-toggle:focus .toggle-surface{stroke-dasharray:4 2}
.backlog-focus-control:hover rect,.backlog-focus-control:focus rect{stroke-width:2}.backlog-focus-control:focus rect{stroke-dasharray:4 2}
.reset-control:hover rect,.reset-control:focus rect,.view-control:hover rect,.view-control:focus rect{stroke-width:2}.reset-control:focus rect,.view-control:focus rect{stroke-dasharray:4 2}
.reset-control.disabled,.view-control.disabled{cursor:default;opacity:.35}.reset-control.disabled:hover rect,.view-control.disabled:hover rect{stroke-width:1}
@media (prefers-reduced-motion:reduce){.node,.edge,.dependency-edge,.role-node,.skill-node{transition:none}}
]]></style>""",
        '<text x="30" y="38" class="heading">Choose an agent or skill. Trace its relationships.</text>',
        '<text x="30" y="64" id="selection-status" class="status" role="status" aria-live="polite">All agents and skills shown. Agent dependency arrows are visible.</text>',
        f'<g class="backlog-focus-control" data-focus-roles="{" ".join(BACKLOG_MANAGEMENT_ROLES)}" role="button" tabindex="0" aria-pressed="false" aria-label="Focus backlog management agents"><rect x="30" y="78" width="210" height="30" rx="15"/><text x="135" y="97" text-anchor="middle">Focus backlog management</text></g>',
        f'<g class="dependency-toggle checked" role="checkbox" tabindex="0" aria-checked="true" aria-label="Show agent dependencies"><rect x="{SVG_WIDTH - 585}" y="24" width="220" height="30" rx="15" class="toggle-surface"/><rect x="{SVG_WIDTH - 573}" y="32" width="14" height="14" rx="3" class="toggle-box"/><path d="M {SVG_WIDTH - 570} 39 L {SVG_WIDTH - 566} 43 L {SVG_WIDTH - 560} 35" class="checkmark"/><text x="{SVG_WIDTH - 550}" y="43">Show agent dependencies</text></g>',
        f'<g class="view-control disabled" role="button" tabindex="-1" aria-disabled="true" aria-label="Select an agent or skill to view its definition"><rect x="{SVG_WIDTH - 330}" y="24" width="160" height="30" rx="15"/><text x="{SVG_WIDTH - 250}" y="43" text-anchor="middle">View definition</text></g>',
        f'<g class="reset-control disabled" role="button" tabindex="-1" aria-disabled="true" aria-label="Clear map selection"><rect x="{SVG_WIDTH - 150}" y="24" width="120" height="30" rx="15"/><text x="{SVG_WIDTH - 90}" y="43" text-anchor="middle">Clear selection</text></g>',
        f'<text x="{ROLE_X}" y="126" class="heading">Agents</text>',
        f'<text x="{SKILL_X}" y="126" class="heading">Bundled skills</text>',
    ]

    for index, (source_role, target_role) in enumerate(agent_dependencies):
        source_y = role_y[source_role] + 12
        target_y = role_y[target_role] + 12
        endpoint_x = ROLE_X + ROLE_WIDTH
        lane_x = endpoint_x + 62 + (index * 12)
        parts.append(
            f'<path d="M {endpoint_x} {source_y} C {lane_x} {source_y}, '
            f'{lane_x} {target_y}, {endpoint_x + 1} {target_y}" '
            f'class="dependency-edge" data-source-role="{_escape(source_role)}" '
            f'data-target-role="{_escape(target_role)}" '
            f'marker-end="url(#dependency-arrow)"/>'
        )

    for role in roles:
        y = role_y[str(role["name"])]
        for skill_name, conditional in _effective_role_skill_entries(
            role, shared_skill_entries
        ):
            start_x = ROLE_X + ROLE_WIDTH
            end_x = SKILL_X
            first_control_x = start_x + 150
            second_control_x = end_x - 140
            parts.append(
                f'<path d="M {start_x} {y + 12} C {first_control_x} {y + 12}, '
                f'{second_control_x} {skill_y[skill_name] + 12}, {end_x} '
                f'{skill_y[skill_name] + 12}" class="edge'
                f'{" conditional-edge" if conditional else ""}" '
                f'data-role="{_escape(role["name"])}" data-skill="{_escape(skill_name)}"/>'
            )

    current_y = TOP
    catalog_group_labels = {
        group["id"]: group["label"]
        for group in catalog_groups
    }
    for group, group_roles in grouped_roles.items():
        parts.append(
            f'<text x="{ROLE_X}" y="{current_y + 18}" class="group">'
            f'{_escape(catalog_group_labels[group])}</text>'
        )
        current_y += ROW_HEIGHT
        for role in group_roles:
            entries = _effective_role_skill_entries(role, shared_skill_entries)
            conditional_count = sum(1 for _, conditional in entries if conditional)
            secondary = f"{len(entries)} skills"
            if conditional_count:
                secondary += f" · {conditional_count} conditional"
            dependency_count = len(_role_agent_dependencies(role))
            if dependency_count:
                secondary += f" · {dependency_count} dependencies"
            parts.append(
                _role_node(
                    current_y,
                    str(role["name"]),
                    _display_name(str(role["name"])),
                    secondary,
                )
            )
            current_y += ROW_HEIGHT
        current_y += 12

    skill_assignment_kinds: dict[str, set[str]] = {}
    for role in roles:
        for skill_name, conditional in _effective_role_skill_entries(
            role, shared_skill_entries
        ):
            skill_assignment_kinds.setdefault(skill_name, set()).add(
                "request-specific" if conditional else "definition-owned"
            )

    skill_current_y = TOP
    for category, skill_names in visible_skill_categories:
        parts.append(
            f'<text x="{SKILL_X}" y="{skill_current_y + 18}" class="group">'
            f'{_escape(category.replace("-", " ").title())}</text>'
        )
        skill_current_y += ROW_HEIGHT
        for skill_name in skill_names:
            assignment_kinds = skill_assignment_kinds.get(skill_name, set())
            secondary = " / ".join(sorted(assignment_kinds)) or "unassigned"
            modifier = (
                " conditional"
                if assignment_kinds == {"request-specific"}
                else ""
            )
            parts.append(
                _skill_node(
                    skill_current_y,
                    skill_name,
                    secondary,
                    modifier,
                )
            )
            skill_current_y += ROW_HEIGHT
        skill_current_y += 12

    parts.append("""<script><![CDATA[
(function () {
  const roleNodes = Array.from(document.querySelectorAll(".role-node"));
  const skillNodes = Array.from(document.querySelectorAll(".skill-node"));
  const edges = Array.from(document.querySelectorAll(".edge"));
  const dependencyEdges = Array.from(document.querySelectorAll(".dependency-edge"));
  const backlogFocusControl = document.querySelector(".backlog-focus-control");
  const dependencyToggle = document.querySelector(".dependency-toggle");
  const viewControl = document.querySelector(".view-control");
  const resetControl = document.querySelector(".reset-control");
  const status = document.getElementById("selection-status");
  const viewDefinitionMessage = "dev-methodology:view-definition";
  const backlogManagementRoles = new Set(backlogFocusControl.dataset.focusRoles.split(" "));
  const backlogManagementDependencyEdges = dependencyEdges.filter(
    (edge) => backlogManagementRoles.has(edge.dataset.sourceRole)
  );
  const backlogFocusRoles = new Set([
    ...backlogManagementRoles,
    ...backlogManagementDependencyEdges.map((edge) => edge.dataset.targetRole),
  ]);
  let selectedRole = "";
  let selectedSkill = "";
  let focusBacklogManagement = false;
  let showAgentDependencies = true;

  function renderSelection() {
    const hasSelection = Boolean(selectedRole || selectedSkill || focusBacklogManagement);
    const hasDefinitionSelection = Boolean(selectedRole || selectedSkill);
    const activeSkills = new Set(
      focusBacklogManagement
        ? edges
            .filter((edge) => backlogFocusRoles.has(edge.dataset.role))
            .map((edge) => edge.dataset.skill)
        : selectedRole
        ? edges
            .filter((edge) => edge.dataset.role === selectedRole)
            .map((edge) => edge.dataset.skill)
        : selectedSkill
          ? [selectedSkill]
          : []
    );
    const activeRoles = new Set(
      focusBacklogManagement
        ? backlogFocusRoles
        : selectedSkill
        ? edges
            .filter((edge) => edge.dataset.skill === selectedSkill)
            .map((edge) => edge.dataset.role)
        : selectedRole
          ? [selectedRole]
          : []
    );
    const activeDependencyEdges = dependencyEdges.filter(
      (edge) => showAgentDependencies && (
        focusBacklogManagement
          ? backlogManagementDependencyEdges.includes(edge)
          : selectedRole
            && (edge.dataset.sourceRole === selectedRole || edge.dataset.targetRole === selectedRole)
      )
    );
    activeDependencyEdges.forEach((edge) => {
      activeRoles.add(edge.dataset.sourceRole);
      activeRoles.add(edge.dataset.targetRole);
    });

    roleNodes.forEach((node) => {
      const isSelected = node.dataset.role === selectedRole;
      const isActive = activeRoles.has(node.dataset.role);
      node.classList.toggle("selected", isSelected);
      node.classList.toggle("active", isActive && !isSelected);
      node.classList.toggle("dimmed", hasSelection && !isActive);
      node.setAttribute("aria-pressed", String(isSelected));
    });
    edges.forEach((edge) => {
      const isActive = focusBacklogManagement
        ? backlogFocusRoles.has(edge.dataset.role)
        : selectedRole
        ? edge.dataset.role === selectedRole
        : edge.dataset.skill === selectedSkill;
      edge.classList.toggle("active", isActive);
      edge.classList.toggle("dimmed", hasSelection && !isActive);
    });
    dependencyEdges.forEach((edge) => {
      const isActive = activeDependencyEdges.includes(edge);
      edge.classList.toggle("active", isActive);
      edge.classList.toggle("dimmed", showAgentDependencies && hasSelection && !isActive);
    });
    skillNodes.forEach((node) => {
      const isSelected = node.dataset.skill === selectedSkill;
      const isActive = activeSkills.has(node.dataset.skill);
      node.classList.toggle("selected", isSelected);
      node.classList.toggle("active", isActive && !isSelected);
      node.classList.toggle("dimmed", hasSelection && !isActive);
      node.setAttribute("aria-pressed", String(isSelected));
    });

    const activeRoleNode = roleNodes.find(
      (node) => node.dataset.role === selectedRole
    );
    if (focusBacklogManagement) {
      status.textContent = `Backlog management: ${activeRoles.size} agents, ${activeSkills.size} linked skills, and ${activeDependencyEdges.length} dependency arrows highlighted.`;
    } else if (activeRoleNode) {
      const dependencyStatus = showAgentDependencies
        ? ` ${activeDependencyEdges.length} agent dependency arrows highlighted.`
        : "";
      status.textContent = `${activeRoleNode.dataset.displayName}: ${activeSkills.size} linked skills highlighted.${dependencyStatus}`;
    } else if (selectedSkill) {
      const agentLabel = activeRoles.size === 1 ? "agent uses" : "agents use";
      status.textContent = `${selectedSkill}: ${activeRoles.size} ${agentLabel} this skill.`;
    } else {
      status.textContent = showAgentDependencies
        ? "All agents and skills shown. Agent dependency arrows are visible."
        : "All agents and skills shown. Agent dependency arrows are hidden.";
    }
    document.documentElement.classList.toggle(
      "show-agent-dependencies",
      showAgentDependencies
    );
    dependencyToggle.classList.toggle("checked", showAgentDependencies);
    dependencyToggle.setAttribute("aria-checked", String(showAgentDependencies));
    backlogFocusControl.classList.toggle("active", focusBacklogManagement);
    backlogFocusControl.setAttribute("aria-pressed", String(focusBacklogManagement));
    const selectedKind = selectedRole ? "agent" : selectedSkill ? "skill" : "";
    const selectedName = selectedRole || selectedSkill;
    const selectedLabel = activeRoleNode
      ? activeRoleNode.dataset.displayName
      : selectedSkill;
    viewControl.classList.toggle("disabled", !hasDefinitionSelection);
    viewControl.setAttribute("aria-disabled", String(!hasDefinitionSelection));
    viewControl.setAttribute("tabindex", hasDefinitionSelection ? "0" : "-1");
    viewControl.setAttribute(
      "aria-label",
      hasDefinitionSelection
        ? `View ${selectedLabel} definition`
        : "Select an agent or skill to view its definition"
    );
    viewControl.dataset.definitionKind = selectedKind;
    viewControl.dataset.definitionName = selectedName;
    resetControl.classList.toggle("disabled", !hasSelection);
    resetControl.setAttribute("aria-disabled", String(!hasSelection));
    resetControl.setAttribute("tabindex", hasSelection ? "0" : "-1");
  }

  function selectRole(roleName) {
    const shouldClear = selectedRole === roleName && !selectedSkill;
    selectedRole = shouldClear ? "" : roleName;
    selectedSkill = "";
    focusBacklogManagement = false;
    renderSelection();
  }

  function selectSkill(skillName) {
    const shouldClear = selectedSkill === skillName && !selectedRole;
    selectedSkill = shouldClear ? "" : skillName;
    selectedRole = "";
    focusBacklogManagement = false;
    renderSelection();
  }

  function clearSelection() {
    selectedRole = "";
    selectedSkill = "";
    focusBacklogManagement = false;
    renderSelection();
  }

  function toggleBacklogManagementFocus() {
    selectedRole = "";
    selectedSkill = "";
    focusBacklogManagement = !focusBacklogManagement;
    renderSelection();
  }

  function toggleAgentDependencies() {
    showAgentDependencies = !showAgentDependencies;
    renderSelection();
  }

  function viewRoleDefinition(roleName) {
    selectedRole = roleName;
    selectedSkill = "";
    focusBacklogManagement = false;
    renderSelection();
    viewSelectedDefinition();
  }

  function viewSkillDefinition(skillName) {
    selectedRole = "";
    selectedSkill = skillName;
    focusBacklogManagement = false;
    renderSelection();
    viewSelectedDefinition();
  }

  function viewSelectedDefinition() {
    const kind = viewControl.dataset.definitionKind;
    const name = viewControl.dataset.definitionName;
    if (!kind || !name) return;
    if (window.parent === window) {
      const target = new URL("agent-and-skill-definitions.html", window.location.href);
      target.searchParams.set("definitionKind", kind);
      target.searchParams.set("definitionName", name);
      target.hash = "hierarchy-title";
      window.location.href = target.href;
      return;
    }
    window.parent.postMessage({ type: viewDefinitionMessage, kind, name }, "*");
  }

  roleNodes.forEach((node) => {
    node.addEventListener("click", (event) => {
      if (event.detail < 2) selectRole(node.dataset.role);
    });
    node.addEventListener("dblclick", () => viewRoleDefinition(node.dataset.role));
    node.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        selectRole(node.dataset.role);
      }
    });
  });
  skillNodes.forEach((node) => {
    node.addEventListener("click", (event) => {
      if (event.detail < 2) selectSkill(node.dataset.skill);
    });
    node.addEventListener("dblclick", () => viewSkillDefinition(node.dataset.skill));
    node.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        selectSkill(node.dataset.skill);
      }
    });
  });
  dependencyToggle.addEventListener("click", toggleAgentDependencies);
  dependencyToggle.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      toggleAgentDependencies();
    }
  });
  backlogFocusControl.addEventListener("click", toggleBacklogManagementFocus);
  backlogFocusControl.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      toggleBacklogManagementFocus();
    }
  });
  viewControl.addEventListener("click", () => {
    if (selectedRole || selectedSkill) viewSelectedDefinition();
  });
  viewControl.addEventListener("keydown", (event) => {
    if ((selectedRole || selectedSkill) && (event.key === "Enter" || event.key === " ")) {
      event.preventDefault();
      viewSelectedDefinition();
    }
  });
  resetControl.addEventListener("click", () => {
    if (selectedRole || selectedSkill || focusBacklogManagement) clearSelection();
  });
  resetControl.addEventListener("keydown", (event) => {
    if ((selectedRole || selectedSkill || focusBacklogManagement) && (event.key === "Enter" || event.key === " ")) {
      event.preventDefault();
      clearSelection();
    }
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && (selectedRole || selectedSkill || focusBacklogManagement)) clearSelection();
  });
  renderSelection();
})();
]]></script>""")
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> int:
    """Write the hierarchy SVG, or report whether the generated file is current."""
    parser = argparse.ArgumentParser(
        description="Generate the interactive agent and skill hierarchy SVG."
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = build_svg()
    if args.check:
        if not OUTPUT_PATH.is_file() or OUTPUT_PATH.read_text(encoding="utf-8") != rendered:
            print(f"stale {OUTPUT_PATH}")
            return 1
        return 0
    OUTPUT_PATH.write_text(rendered, encoding="utf-8")
    print(f"generated {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
