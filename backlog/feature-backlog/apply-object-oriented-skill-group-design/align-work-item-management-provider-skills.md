# Align Work-Item Management Provider Skills

Status: Starting

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/apply-object-oriented-skill-group-design/align-work-item-management-provider-skills.md

Completion: direct-main

Series: backlog/feature-backlog/apply-object-oriented-skill-group-design/index.md

## Current Dispatch Reservation

Transition: Ready -> Starting.
Parent Coordination Thread: /root/apply_skill_group_design_backlog.
Launch Reservation: One distinct bounded launch reservation for this provider record.
Normalized Objective: Align the work-item management provider skills with the approved object-oriented design and update their individual evaluations.
Dispatch Time: 2026-08-05T03:43:54Z.
Intended Root Dev Orchestrator Role: Dev Orchestrator.
Owner: Unowned pending accepted root.
Current Launch Evidence: Parent Coordinator authorized this exact reservation; exact-file backlog claim reserve-align-work-item-management-provider-skills acquired with outcome SHARED_CHECKOUT_ACQUIRED and event d2288904-dc02-4f48-a39c-31f2fff4be8f. Runtime Thread creation and root acceptance have not occurred.
Required Next Lifecycle Transition: The root Dev Orchestrator must separately accept Starting -> Running before repository mutation.
Reconciliation: Pending.

## Summary

Align all five work-item management providers on Inventory Work Items, Transition Work Item, Reconcile Work Item Completion, Recover Work Item, and Report Work Items while preserving provider-specific lifecycle behavior.

## Context

The Backlog Management proposal treats the five management skills as provider implementations selected through project routing. They need the same public procedure vocabulary, but file, GitHub, GitLab, Azure DevOps, and Jira retain distinct authority, lookup, lifecycle, recovery, and availability rules.

## Source Evidence

The user directed in the active Codex task on 2026-08-04: "create separate work items to update skills according to the new design, and update individual evals." The exact provider recommendations are in design/skill-groups/backlog-management.md at reviewed baseline commit c426c970153948f9d5d2d92f1b7b718613a8d4f7.

## Requirements

- Introduce the same five public operation headings in every provider.
- Preserve each provider's native lookup, state, recovery, authority, result, and ambiguous-outcome rules.
- Route unsupported Azure DevOps and Jira operations to their truthful blocked result without pretending successful lifecycle support.
- Align common input and result terms only where provider semantics remain equivalent.
- Add individual evaluation coverage for every provider and every public procedure, using representative cases rather than only name-presence checks.

## Acceptance Criteria

- Every provider exposes the same five procedure names.
- Supported providers retain correct technology-specific lifecycle behavior, and unsupported providers retain truthful blocked behavior.
- AGENTS.md selection can refer to provider-neutral management procedures without requiring one provider to know another.
- Individual evaluations cover inventory, transition, reconciliation, recovery, and reporting across the provider family.
- Generated mirrors, catalogs, and focused tests are fresh and passing.

## Dependencies

None.

## Verification

- Run the supported definition-change precheck for all five governed paths.
- Run every provider's focused probe and provider fixture or contract tests.
- Run scripts/test_agent_skill_evals.py, scripts/test_eval_coverage_catalog.py, scripts/test_bundle_content.py, and generated-output freshness checks.
- Compare all five headings, inputs, results, and unsupported-operation behavior.
- Run git diff --check and obtain independent methodology review and verification.

## Open Questions

Determine which shared data members can be named consistently without weakening a provider's native lifecycle constraints.

## Governed Definition Approval

### Governed Canonical Sources

- skills/manage-file-work-items/SKILL.md
- skills/manage-github-work-items/SKILL.md
- skills/manage-gitlab-work-items/SKILL.md
- skills/manage-azure-devops-work-items/SKILL.md
- skills/manage-jira-work-items/SKILL.md

### Allowed Dependent Artifacts

- approval-record-align-work-item-management-provider-skills.yaml
- evals/skill-probes.yaml
- evals/cases.yaml
- evals/workflow-packs.yaml
- evals/agent-tests/dev-backlog-steward
- evals/agent-tests/dev-backlog-coordinator
- scripts/test_github_work_item_provider_fixture.py
- scripts/test_generate_backlog_report.py
- scripts/test_agent_skill_evals.py
- scripts/test_eval_coverage_catalog.py
- scripts/test_bundle_content.py
- README.md
- design/agent-and-skill-definitions.html
- design/agent-and-skill-evaluations.html
- design/generated/skill-definitions.js
- generated/adapters files regenerated from only the approved canonical sources
- Directly related non-governed documentation, provider fixtures, and focused tests required to keep these approved definitions coherent

### Approval Resolution

Approved at creation on 2026-08-04 by the user statement in the active Codex task: "create separate work items to update skills according to the new design, and update individual evals." Approval is limited to the five governed canonical paths listed above. Any additional governed definition requires new explicit user approval recorded in this item.
