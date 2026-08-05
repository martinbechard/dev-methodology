# Align Baseline Development Skills

Status: Running

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/apply-object-oriented-skill-group-design/align-baseline-development-skills.md

Completion: direct-main

Series: backlog/feature-backlog/apply-object-oriented-skill-group-design/index.md

## Current Dispatch Reservation

Transition: Ready -> Starting.
Parent Coordination Thread: /root/apply_skill_group_design_backlog.
Launch Reservation: One distinct bounded launch reservation for this provider record.
Normalized Objective: Align the baseline development skill group with the approved object-oriented design and update its individual evaluations.
Dispatch Time: 2026-08-05T03:42:41Z.
Intended Root Dev Orchestrator Role: Dev Orchestrator.
Owner: Unowned pending accepted root.
Current Launch Evidence: Parent Coordinator authorized this exact reservation; exact-file backlog claim reserve-align-baseline-development-skills acquired with outcome SHARED_CHECKOUT_ACQUIRED and event ca2c93bc-1521-4af5-8060-7a4bf4970f72. Runtime Thread creation and root acceptance have not occurred.
Required Next Lifecycle Transition: The root Dev Orchestrator must separately accept Starting -> Running before repository mutation.
Reconciliation: Root acceptance recorded separately below; the parent reservation remains preserved.

## Current Running Acceptance

Transition: Starting -> Running.
Canonical Thread: /root/apply_skill_group_design_backlog/align_baseline_development_skills.
Root Agent Task: /root/apply_skill_group_design_backlog/align_baseline_development_skills.
Owner: Dev Orchestrator.
Branch: codex/align-baseline-development-skills-019fab.
Worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/align-baseline-development-skills-019fab.
Phase: Implementation dispatch.
Started At: 2026-08-05T03:47:05Z.
Claim Evidence: The private delivery lane was claim-free immediately before this acceptance (claim status outcome STATUS with no live claims). This exact primary-main backlog mutation is protected by exact-file claim running-align-baseline-development-skills-019fab, acquired with outcome SHARED_CHECKOUT_ACQUIRED and event dba10391-6547-4015-99d3-ba8641406138.
Preserved Coordination: Parent Coordination Thread /root/apply_skill_group_design_backlog and its Ready -> Starting launch reservation remain canonical.

## Summary

Align the nine Baseline Development skills with their proposed public procedure boundaries and rename fix-explanation to explain-code-fix. Update exact Agent references and focused evaluations in the same delivery.

## Context

The reviewed Baseline Development proposal keeps subject-oriented packages when they expose several related procedures or guidance members. It adds explicit operation headings to careful-coding, code-comments, code-discovery, test-driven-development, structured-design, structured-explanation, organise-project-files, and review-structured-artifact. code-discovery must retain both Discover Code Context and Determine Change Scope. fix-explanation has one dominant operation and becomes explain-code-fix.

## Source Evidence

The user directed in the active Codex task on 2026-08-04: "create separate work items to update skills according to the new design, and update individual evals." The exact approved design is design/skill-groups/baseline-development.md at reviewed baseline commit c426c970153948f9d5d2d92f1b7b718613a8d4f7.

## Requirements

- Apply every Baseline Development recommendation without changing the documented responsibility boundaries.
- Rename fix-explanation to explain-code-fix, including frontmatter, metadata, direct Agent references, live catalogs, and generated mirrors.
- Introduce headings that match the proposed functions and preserve non-callable guidance as data or reference material.
- Give code-discovery separate Discover Code Context and Determine Change Scope procedures.
- Update or add an individual behavioral evaluation for every changed skill; do not rely only on catalog-presence checks.
- Preserve authorized behavior and avoid rewriting historical evaluation result records.

## Acceptance Criteria

- The nine canonical skill definitions match the proposed diagram and recommendation table.
- No maintained live source refers to fix-explanation after the rename, except migration or historical evidence that intentionally names the former identity.
- Dev Coder and Dev Merge Coordinator load explain-code-fix where they previously loaded fix-explanation.
- Each changed skill has a focused probe, case, or Agent-suite scenario that exercises its public procedure vocabulary and critical boundary.
- Generated mirrors and public catalogs are fresh, and focused validation passes.

## Dependencies

None.

## Verification

- Run the supported definition-change precheck for every governed canonical path below.
- Run focused skill probes and affected Dev Coder and Dev Merge Coordinator suites.
- Run scripts/test_agent_skill_evals.py, scripts/test_eval_coverage_catalog.py, scripts/test_bundle_content.py, and generated-output freshness checks.
- Search maintained sources for stale fix-explanation references and invented whole-skill procedures.
- Run git diff --check and obtain independent methodology review and verification.

## Open Questions

Resolve the most source-faithful final heading wording when a current section mixes a procedure with supporting guidance; retain the source mapping in review evidence.

## Governed Definition Approval

### Governed Canonical Sources

- skills/careful-coding/SKILL.md
- skills/code-comments/SKILL.md
- skills/code-discovery/SKILL.md
- skills/test-driven-development/SKILL.md
- skills/structured-design/SKILL.md
- skills/structured-explanation/SKILL.md
- skills/organise-project-files/SKILL.md
- skills/review-structured-artifact/SKILL.md
- skills/fix-explanation/SKILL.md
- skills/fix-explanation/agents/openai.yaml
- skills/explain-code-fix/SKILL.md
- skills/explain-code-fix/agents/openai.yaml
- agents/roles/dev-activities/dev-coder.role.yaml
- agents/roles/dev-activities/dev-merge-coordinator.role.yaml

### Allowed Dependent Artifacts

- approval-record-align-baseline-development-skills.yaml
- evals/skill-probes.yaml
- evals/cases.yaml
- evals/workflow-packs.yaml
- evals/agent-tests/dev-coder
- evals/agent-tests/dev-merge-coordinator
- README.md
- design/agent-and-skill-definitions.html
- design/agent-and-skill-evaluations.html
- design/generated/skill-definitions.js
- design/generated/role-definitions.js
- generated/adapters files regenerated from only the approved canonical sources
- scripts/test_agent_skill_evals.py
- scripts/test_eval_coverage_catalog.py
- scripts/test_bundle_content.py
- Directly related non-governed documentation and focused tests required to keep these approved definitions coherent

### Approval Resolution

Approved at creation on 2026-08-04 by the user statement in the active Codex task: "create separate work items to update skills according to the new design, and update individual evals." The reviewed Baseline Development design names the exact current and proposed skill identities and shows the Agent relationships covered here. Approval is limited to the governed canonical paths listed above. Any additional governed definition requires new explicit user approval recorded in this item.
