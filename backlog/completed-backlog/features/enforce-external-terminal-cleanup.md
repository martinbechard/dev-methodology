# Enforce External Terminal Cleanup

Status: Completed

Type: Feature

Provider: file

Work Item ID: enforce-external-terminal-cleanup

Completion: main-branch

## Summary

Concisely enforce one external terminal-cleanup boundary across the private Backlog Dispatcher, Codex task coordination, and main-branch delivery skills.

## Starting Handoff Evidence

- Starting Recorded At: 2026-08-12T20:42:44Z.
- Coordinator: Backlog Dispatcher Codex task `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`, acting through canonical Dev Backlog Coordinator subagent `/root/backlog_coordinator`.
- Dispatch Reservation: `reserve-starting-external-terminal-cleanup-019ff2c3`.
- Normalized Objective: Concisely enforce external terminal cleanup across exactly the three user-approved skill sources, with Orchestrator evidence handoff, Coordinator verification and authorization, root Dispatcher cleanup and archive-last execution, returned outcomes, and post-cleanup capacity reconciliation.
- Intended Root Role: Dev Orchestrator.
- Launch Result: Started.
- Canonical Execution: Codex Task `019ff7b7-a43a-7d22-8b6b-047cd44341b4`; retained Conversation `019ff7b7-a43a-7d22-8b6b-047cd44341b4` on the runtime's combined task surface.
- Baseline Commit: `d1d0af1cce496141a86d8a9aebaf24fb46d910cf`.
- Provider Claim: `reserve-starting-external-terminal-cleanup-019ff2c3`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `6ee68833-d8f4-41a4-8351-f2d74c5759af`.
- Last Contact: 2026-08-12T20:42:44Z.
- Next Reconciliation: Immediately after the caller returns the exact runtime creation result; do not retry an ambiguous result.
- Next Lifecycle Owner: The new root Dev Orchestrator must record the distinct Starting -> Running acceptance before source mutation.

## Running Acceptance Evidence

- Accepted At: 2026-08-12T20:46:02Z.
- Owner: Dev Orchestrator.
- Codex Task ID: `019ff7b7-a43a-7d22-8b6b-047cd44341b4`.
- Conversation ID: `019ff7b7-a43a-7d22-8b6b-047cd44341b4`.
- Runtime Parent Task ID: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Task ID: `/root/backlog_coordinator` under runtime parent `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Branch: `codex/enforce-external-terminal-cleanup`.
- Worktree: `/Users/martinbechard/.codex/worktrees/568d/dev-methodology`.
- Current Phase: Planning and bounded producer assignment.
- Accepted Baseline: `d1d0af1cce496141a86d8a9aebaf24fb46d910cf`.
- Provider Reservation Commit: `ec8d921de898eed00da93439834de2159158e19e`.
- Accepted Execution Evidence: The canonical root execution is active, its private worktree is clean, and exact Work Item activity `update` claim `enforce-external-terminal-cleanup-update-019ff7b7` returned `SHARED_CHECKOUT_ACQUIRED` with event `8da28bd3-439a-47e2-b332-951ca2196707` before this transition.
- Next Action: Commit this provider transition, release update ownership with handoff, then acquire outcome-work and exact approved-path ownership before producer mutation.

## Scheduling Evidence

- Mode: MULTITASK enabled.
- Active Eligibility Before Reservation: zero Starting and zero Running items.
- Effective Scheduling Limit: one launch in this pass because the user directed this correction immediately and the separate Ready documentation/role item consumes related review, generation, and integration capacity.
- Capacity Result: the one pass-local slot is reserved by this Starting item.
- Dependencies: None.
- Overlap Result: no active canonical execution, claim, candidate, worktree, or finish-lane item overlaps the three exact skill sources. `document-external-terminal-cleanup` remains Ready and must not mutate or integrate overlapping contract projections while this item is active.

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

## Completion Evidence

- Completed At: 2026-08-12T21:19:21Z.
- Accepted Candidate: `720030e8f4350b30ea5aa9e75829d8a8954ed96f` on `codex/enforce-external-terminal-cleanup`.
- Independent Review: Fresh Dev Code Reviewer accepted the exact four-file candidate with no findings.
- Candidate Verification: Python compile, the focused external-cleanup contract test, 30 directly affected task-control and main-branch tests, OpenAI metadata validation, and Git diff checks passed.
- Integration Commit: `d2c248aeba9e8dcd6372d19e8986ef836f1d7249` on configured `main`.
- Integration Mapping: Each of the four accepted candidate blobs is byte-identical at the integration commit; the candidate was replayed onto current main without importing cumulative source-branch ancestry.
- Main Observation: Primary main is clean at `d2c248aeba9e8dcd6372d19e8986ef836f1d7249`, and the integration commit is reachable from `main`.
- Primary Skill Validation: Configured MCP `skill_validate` returned `{"ok":true,"findings":[]}` for the exact integrated primary-root bytes of the private Backlog Dispatcher, Codex task coordination, and main-branch delivery skills.
- Post-Integration Verification: Fresh Dev Verifier passed Python compile, the focused external-cleanup test, 30 directly affected contract tests, OpenAI metadata, exact scope, byte equivalence, main reachability, clean-state, and Git diff checks.
- Generated Freshness Residual: `scripts/build-skill-docs.py --check` truthfully reports only `design/generated/skill-definitions.js`; no other generated projection or adapter differs. Work Item `document-external-terminal-cleanup`, updated at `f0b8ca96db4b8aa2d56fd7c7f864ea475fb05b8c`, owns that exact residual.
- Claim Reconciliation: Outcome-work claim `enforce-external-terminal-cleanup-work-resume-019ff7b7` released with `handoff`; exact source-path claim `enforce-external-terminal-cleanup-paths-resume-019ff7b7` released. The terminal provider transaction owns only this active path and its completed destination until its commit and release finish.
- Commit Disposition: READY for requested lifecycle COMPLETED.
- Cleanup Eligibility: The canonical task, current worktree, and checked-out branch are retained. Dev Backlog Coordinator must verify terminal provider and delivery evidence, released claims, worktree cleanliness, and branch-to-delivery equivalence before authorizing exact external cleanup. Root Backlog Dispatcher removes the authorized worktree, safely deletes the authorized branch, archives the task last, returns every outcome, and only then may the Coordinator reconcile capacity.
