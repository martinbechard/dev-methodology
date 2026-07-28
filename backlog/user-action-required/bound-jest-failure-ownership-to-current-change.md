# Bound Jest failure ownership to the current change

Status: User Action Required

Type: Defect

Provider: file

Provider Reference: backlog/user-action-required/bound-jest-failure-ownership-to-current-change.md

Completion: direct-main

Owner: Unowned pending user action

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-first-eight-lint-defects-019fa9bb

Normalized Objective: Limit Jest repair ownership to failures attributable to the current change and preserve unrelated failures as separate evidence.

Dispatch Time: 2026-07-28T18:22:25Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019fa9f9-33ef-7c73-872e-bcf0c7cb4b87

Root Agent Task: 019fa9f9-33ef-7c73-872e-bcf0c7cb4b87

Next Lifecycle Owner: Dev Backlog Coordinator

## Running Acceptance

- Transition: Starting -> Running.
- Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758.
- Canonical Work-Item Thread: 019fa9f9-33ef-7c73-872e-bcf0c7cb4b87.
- Canonical Root Agent Task Id: 019fa9f9-33ef-7c73-872e-bcf0c7cb4b87.
- Owner: Root Dev Orchestrator.
- Delivery Branch: codex/bound-jest-failure-ownership-019fa9f9.
- Delivery Worktree: /Users/martinbechard/.codex/worktrees/31c1/dev-methodology.
- Phase: Read-only approval-boundary analysis.
- Started At: 2026-07-28T18:42:17Z.
- Started-At Evidence: The canonical root Dev Orchestrator accepted the parent-reserved work item and requested this distinct provider transition.
- Claim Evidence: running-acceptance-019fa9f9-33ef-7c73-872e-bcf0c7cb4b87; claim outcome SHARED_CHECKOUT_ACQUIRED; claim event c4a373dc-1f50-4c4d-a23a-6a33cfa0a286; claimed 2026-07-28T18:41:53.538838Z.

## User Action Required

- Transition: Running -> User Action Required.
- Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758.
- Canonical Work-Item Thread: 019fa9f9-33ef-7c73-872e-bcf0c7cb4b87.
- Canonical Root Agent Task Id: 019fa9f9-33ef-7c73-872e-bcf0c7cb4b87.
- Read-Only Analysis Evidence: No code, test, or generator-only fix can satisfy the objective. skills/jest/SKILL.md:32 is the exact governed defect.
- Candidate Commit: None.
- Lifecycle Claim Evidence: uar-bound-jest-failure-ownership-019fa9f9; claim outcome SHARED_CHECKOUT_ACQUIRED; claim event f6079333-8eef-42a5-99d4-42b061bf948a; claimed 2026-07-28T18:49:28.529439Z.

### Question for the User

Do you explicitly approve modifying only skills/jest/SKILL.md to bound Jest repair ownership to failures attributable to the current change, record unrelated or pre-existing failures separately, and allow a scoped change to complete when its own applicable verification passes?

### Why User Input Is Required

AGENTS.md requires explicit scope-specific user approval for every skill definition mutation. Current dispatch and provider authority explicitly do not authorize this governed definition change.

### Options and Tradeoffs

- Approve the exact path: creates a provenance approval record, runs the required pre-mutation check, then permits implementation, focused testing, supported regeneration, review, verification, and direct-main delivery.
- Do not approve: stops the definition mutation and delivery while preserving the read-only analysis, branch, worktree, and lifecycle evidence.

### Resolution

Pending.

### Unattended Work Boundary

Do not mutate skills/jest/SKILL.md, its generated mirrors, or proceed with delivery until approval is recorded. Preserve the read-only analysis and branch/worktree. No other skill or agent definition is requested.

### Resumption

After an answer, the parent Dev Backlog Coordinator must record User Action Required -> Ready for this preserved canonical Thread. It must then separately reserve Ready -> Starting, and the same root Dev Orchestrator must separately accept Starting -> Running before any governed definition or delivery mutation.

## Summary

Limit Jest repair ownership to failures attributable to the current change and preserve unrelated failures as separate evidence.

## Context

The primary affected skill is skills/jest/SKILL.md. It treats every failing test as belonging to the current task. This expands ownership to unrelated failures and can block an otherwise complete scoped change.

## Source Evidence

The user authorized immediate creation of independently dispatchable Defect records for every accepted skill-lint finding on 2026-07-28. The accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records this finding at skills/jest/SKILL.md:32. Independent reviewer /root/confirm_critical_b accepted it as CONFIRMED_CRITICAL.

## Requirements

- Require attribution to the current change before assigning repair ownership.
- Record unrelated or pre-existing failures separately.
- Preserve bounded verification and defect-reporting routes.

## Acceptance Criteria

- One attributable and one pre-existing failure produce repair ownership only for the attributable failure.
- The pre-existing failure is recorded without expanding the current task scope.
- A scoped change can complete when its own verification conditions pass.

## Dependencies

None

## Verification

- Present one attributable and one pre-existing failure.
- Confirm repair ownership only for the attributable failure.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None.

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/jest/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check.
