# Bound Jest failure ownership to the current change

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/bound-jest-failure-ownership-to-current-change.md

Completion: direct-main

Owner: Unowned

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

## User Action Resolution

- Transition: User Action Required -> Ready.
- Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758.
- Canonical Work-Item Thread: 019fa9f9-33ef-7c73-872e-bcf0c7cb4b87.
- Canonical Root Agent Task Id: 019fa9f9-33ef-7c73-872e-bcf0c7cb4b87.
- Prior Transition: Running -> User Action Required.
- Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758.
- Canonical Work-Item Thread: 019fa9f9-33ef-7c73-872e-bcf0c7cb4b87, preserved for same-Thread resumption.
- Canonical Root Agent Task Id: 019fa9f9-33ef-7c73-872e-bcf0c7cb4b87, preserved for same-Thread resumption.
- Read-Only Analysis Evidence: No code, test, or generator-only fix can satisfy the objective. skills/jest/SKILL.md:32 is the exact governed defect.
- User Answer: ok approved.
- Answer Date: 2026-07-28.
- Approved Governed Scope: skills/jest/SKILL.md only.
- Approval Contract: After attribution proves a failure unrelated or pre-existing, ask the user whether to repair it now. Include it in current ownership only with explicit authorization; otherwise preserve separate verification evidence without scope expansion and do not create an application Defect for that test failure.
- Exclusions: No other governed definition, generated mirror, application Defect, or unrelated repair is approved.
- Resulting Disposition: Ready with Owner: Unowned. The parent Dev Backlog Coordinator must separately reserve Ready -> Starting for this preserved canonical Thread. The same root Dev Orchestrator must then separately accept Starting -> Running before any governed definition or delivery mutation.
- Lifecycle Claim Evidence: uar-ready-approved-resumptions-019fa9bb; claim outcome SHARED_CHECKOUT_ACQUIRED; claim event a7e0c68a-5570-42fe-90e7-460aaad546e9; claimed 2026-07-29T00:04:51.124316Z.

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
