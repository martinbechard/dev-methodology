# Reconcile Objective Visualization and Repository Path-Tree Rules

Status: User Action Required

Type: Feature

Provider: file

Provider Reference: backlog/user-action-required/reconcile-objective-visualization-and-path-tree-rules.md

Completion: direct-main

## Execution / Ownership

- Owner: Unowned
- Canonical task: /root/process_backlog/orch_objective_path_rules
- Proposed artifact claim: objective-path-rules-019f817f-reconcile
- Claim: None
- Branch: codex/reconcile-objective-path-rules-019f817f
- Canonical worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/objective-path-rules-019f817f-reconcile
- Phase: Exact approval pending.
- Starting main: af0a3fe63404a793f2bf7dcf40dd2a3de563109e
- Accepted candidate: None.
- Claim wait started at: None.
- Claim wait attempts: 0.
- Open issues: Exact governed-scope approval is required before implementation.
- Next owner: User.
- Delivery evidence: Pending.

## Read-Only Discovery

- Completed: Current-main and preserved-branch evidence was inspected without artifact mutation.
- Evidence branch: codex/objective-diagram-rules-019f817f at e9b31dbf961d32c1eccdc68becd5666f05497b73.
- Artifact claim: None acquired.
- Candidate: None accepted.
- Artifact mutation: None performed.

## User Action Required

### Question For The User

Do you explicitly approve changing exactly the eight governed paths listed above solely to reconcile objective diagram-trigger and repository path-tree rules against current main, together with regeneration of only their supported generated mirrors? Non-governed template, checklist, and focused regression changes remain ordinary implementation work; this approval does not authorize changing review-high-level-design or reverse-engineering acceptance semantics.

### Why User Input Is Required

The completed read-only discovery identified the exact governed paths below. Repository policy requires explicit scope-specific approval before their mutation.

### Exact Governed Scope

- skills/create-architecture/SKILL.md
- skills/create-functional-spec/SKILL.md
- skills/create-high-level-design/SKILL.md
- skills/create-module-design/SKILL.md
- skills/development-methodology/SKILL.md
- skills/review-architecture/SKILL.md
- skills/review-functional-spec/SKILL.md
- skills/review-module-design/SKILL.md

### Options And Tradeoffs

- Approve the exact eight-path scope: permit governed-source reconciliation and supported mirror regeneration.
- Narrow the scope: preserve excluded paths as unresolved work.
- Defer: retain the discovery evidence without implementation.

### Resolution

Pending.

### Unattended Work Boundary

No artifact claim or mutation is authorized while this question is pending. The approval must not be inferred from prior Ready or Running state, and it must not change review-high-level-design or reverse-engineering acceptance semantics.

## Summary

Reconcile objective visualization and repository path-tree rules against current main while preserving accepted reverse-engineering and high-level-design contracts.

## Context

The preserved source branch codex/objective-diagram-rules-019f817f contains commit e9b31dbf961d32c1eccdc68becd5666f05497b73, Improve diagram and path-tree documentation rules. Its generated and template bytes may not match current main and are evidence, not a cherry-pick target.

Current main retains a reverse-engineering contract that accepts intentionally absent later artifacts during the current pass. Current high-level-design guidance requires a Mermaid sequence diagram when ordered or dependent implementation actions or verification gates are described. Reconciliation must preserve both contracts.

## Source Evidence

- Direct user authorization in the 2026-07-22 parent coordination request to create this Ready Feature item.
- Preserved source branch codex/objective-diagram-rules-019f817f at e9b31dbf961d32c1eccdc68becd5666f05497b73.
- Current main canonical evidence in skills/create-architecture/SKILL.md, skills/review-high-level-design/SKILL.md, and skills/development-methodology/assets/templates/high-level-design-template.md.

## Requirements

- Inspect current main canonical sources before selecting any implementation change.
- Compare the preserved branch intent and relevant source changes with current main using evidence-led reconciliation.
- Define and apply coherent rules for objective visualizations and repository path-tree representation where current evidence supports them.
- Preserve the accepted current reverse-engineering contract; do not reintroduce requirements for intentionally absent later artifacts.
- Preserve the current high-level-design implementation sequence-diagram contract for ordered or dependent actions and verification gates.
- Do not blindly cherry-pick old generated or template bytes.
- Before mutating any governed agent or skill definition, obtain exact scope-specific user approval and run the supported pre-mutation approval check.
- Regenerate only supported generated mirrors after an approved canonical-source mutation.

## Acceptance Criteria

- The selected changes are traced to current-main and preserved-branch evidence.
- The resulting rules do not contradict the accepted reverse-engineering contract.
- The resulting rules retain the high-level-design sequence-diagram requirement for applicable ordered implementation or verification sequences.
- No generated mirror is edited directly, and no stale generated or template bytes are copied without reconciliation.
- Any governed definition mutation has durable exact scope-specific approval evidence and passes the supported pre-mutation check.

## Dependencies

None.

## Verification

- Review the current canonical sources and the preserved source-branch diff before implementation.
- Run focused template, skill, and bundle checks that cover every approved changed surface.
- Run the applicable supported generator freshness check only when an approved canonical source requires regeneration.
- Run git diff --check and obtain independent review of the exact change.

## Notes

This item authorizes analysis and ready-state dispatch. It does not itself authorize governed definition mutations.
