# Align Project Setup Skills

Status: Starting

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/apply-object-oriented-skill-group-design/align-project-setup-skills.md

Completion: direct-main

Series: backlog/feature-backlog/apply-object-oriented-skill-group-design/index.md

## Current Dispatch Reservation

Transition: Ready -> Starting.
Parent Coordination Thread: /root/apply_skill_group_design_backlog.
Launch Reservation: One distinct bounded launch reservation for this provider record.
Normalized Objective: Align Project Setup skills with the approved object-oriented design and update their individual evaluations.
Dispatch Time: 2026-08-05T03:43:25Z.
Intended Root Dev Orchestrator Role: Dev Orchestrator.
Owner: Unowned pending accepted root.
Current Launch Evidence: Parent Coordinator authorized this exact reservation; exact-file backlog claim reserve-align-project-setup-skills acquired with outcome SHARED_CHECKOUT_ACQUIRED and event 709aa785-38fb-4ecf-8964-3576c879aa80. Runtime Thread creation and root acceptance have not occurred.
Required Next Lifecycle Transition: The root Dev Orchestrator must separately accept Starting -> Running before repository mutation.
Reconciliation: Pending.

## Summary

Give detect-technology-skills and create-project-configuration explicit public procedure headings while preserving direct exact-name loading and per-skill technology selection in AGENTS.md.

## Context

The reviewed Project Setup design rejects a synthetic selected-skill-set interface because generated AGENTS.md names each confirmed technology skill independently. The two direct Project Setup skills keep their current names and gain Detect Technology Skills and Create Or Update Project Configuration procedure headings.

## Source Evidence

The user directed in the active Codex task on 2026-08-04: "create separate work items to update skills according to the new design, and update individual evals." The exact approved design is design/skill-groups/project-setup.md at reviewed baseline commit c426c970153948f9d5d2d92f1b7b718613a8d4f7.

## Requirements

- Rename the generic Workflow headings to the two proposed public procedure headings.
- Preserve all current evidence, configuration, authority, and generated-guidance boundaries.
- Do not introduce one interface node or aggregate procedure for the selected technology-skill set.
- Update individual evaluations so each procedure is invoked by its public vocabulary and its important negative boundaries remain covered.

## Acceptance Criteria

- Both SKILL.md files expose the proposed procedure heading without changing their exact skill names.
- Project setup still records and renders each confirmed technology skill by exact name.
- Project Configurator and Project Bootstrapper evaluations exercise the revised public procedure wording and reject unsupported technology-selection shortcuts.
- Generated mirrors and focused tests are fresh and passing.

## Dependencies

None.

## Verification

- Run the supported definition-change precheck for both governed paths.
- Run focused Project Configurator, Project Bootstrapper, technology-detection, project-configuration, and skill-probe evaluations.
- Run scripts/test_agent_skill_evals.py, scripts/test_eval_coverage_catalog.py, scripts/test_bundle_content.py, and renderer freshness checks.
- Run git diff --check and obtain independent methodology review and verification.

## Open Questions

None.

## Governed Definition Approval

### Governed Canonical Sources

- skills/detect-technology-skills/SKILL.md
- skills/create-project-configuration/SKILL.md

### Allowed Dependent Artifacts

- approval-record-align-project-setup-skills.yaml
- evals/skill-probes.yaml
- evals/cases.yaml
- evals/workflow-packs.yaml
- evals/agent-tests/project-configurator
- evals/agent-tests/project-bootstrapper
- evals/projects/project-configuration-routing
- scripts/test_technology_detection.py
- scripts/test_agent_skill_evals.py
- scripts/test_eval_coverage_catalog.py
- scripts/test_bundle_content.py
- README.md
- design/agent-and-skill-definitions.html
- design/agent-and-skill-evaluations.html
- design/generated/skill-definitions.js
- generated/adapters files regenerated from only the approved canonical sources
- Directly related non-governed documentation and focused tests required to keep these approved definitions coherent

### Approval Resolution

Approved at creation on 2026-08-04 by the user statement in the active Codex task: "create separate work items to update skills according to the new design, and update individual evals." Approval is limited to the two governed canonical paths listed above. Any additional governed definition requires new explicit user approval recorded in this item.
