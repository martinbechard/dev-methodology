# Enforce External Terminal Cleanup

Status: Ready

Type: Feature

Provider: file

Work Item ID: enforce-external-terminal-cleanup

Completion: main-branch

## Summary

Concisely enforce one external terminal-cleanup boundary across the private Backlog Dispatcher, Codex task coordination, and main-branch delivery skills.

## Context

The completed Static Classes delivery archived its own active Codex task and removed its current worktree before the Dev Backlog Coordinator could verify and authorize those destructive cleanup operations. Terminal delivery evidence and cleanup execution must be separate.

## Source Evidence

On 2026-08-12, the user directed an immediate update limited to `.agents/skills/backlog-dispatcher/SKILL.md`, `skills/coordinate-codex-tasks/SKILL.md`, and `skills/deliver-work-item-main-branch/SKILL.md`. The user specified that Dev Orchestrator returns terminal evidence and cleanup eligibility; Coordinator verifies terminal, provider, delivery, claims, cleanliness, and equivalence and authorizes exact cleanup; Root Backlog Dispatcher removes the worktree, safely deletes the branch, archives the task last, returns outcomes; and Coordinator then reconciles capacity.

## Requirements

- Update only the three named skill sources and mechanically required focused tests.
- State that Dev Orchestrator must not archive its active Codex task or remove its current worktree or checked-out branch.
- Require Dev Orchestrator to return complete terminal evidence and cleanup eligibility.
- Require Dev Backlog Coordinator to verify terminal provider and delivery evidence, released claims, worktree cleanliness, and branch-to-delivery equivalence before authorizing exact cleanup.
- Require the root Backlog Dispatcher to execute only the authorized worktree removal and safe branch deletion, archive the task last, and return every outcome for Coordinator reconciliation.
- Require capacity reconciliation only after the cleanup outcomes return.
- Keep the added prose concise and avoid documentation, role-source, or generated-adapter changes in this item.

## Acceptance Criteria

- All three skill sources express the same ownership and ordering invariant without duplicating portable procedures unnecessarily.
- No Dev Orchestrator instruction permits self-removal of its current worktree, deletion of its checked-out branch, or self-archival of its active task.
- The Dispatcher packet and result contracts cover exact cleanup authorization and outcomes.
- Focused tests reject premature Orchestrator cleanup and enforce task archival last.
- Fresh independent skill review and verification accept the exact scope.

## Dependencies

None.

## Verification

- Run focused skill-contract and bundle-content tests for all three sources.
- Validate the private and portable skill packages through repository-supported checks.
- Run generated freshness checks and confirm that this item changes no generated output.
- Run Git diff whitespace validation.
- Obtain fresh independent skill review and verification.

## Open Questions

None.

## Governed Definition Approval

### Governed Canonical Sources

- .agents/skills/backlog-dispatcher/SKILL.md
- skills/coordinate-codex-tasks/SKILL.md
- skills/deliver-work-item-main-branch/SKILL.md

### Allowed Dependent Artifacts

- Focused test files only when repository discovery proves they directly validate one of the three approved sources.

### Approval Resolution

Approved at creation. On 2026-08-12, the user explicitly ordered immediate concise updates to exactly the three canonical skill sources listed above. Documentation, role sources, generated adapters, and any additional governed definition remain outside this item's approved scope.

## Notes

This item changes the executable coordination contract only. The separate documentation and role-projection item owns broader explanatory alignment.
