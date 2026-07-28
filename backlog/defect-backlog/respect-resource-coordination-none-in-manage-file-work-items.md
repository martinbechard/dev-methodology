# Make file-provider claim events conditional on configured resource coordination

Status: Ready

User Question: Do you explicitly approve editing the governed canonical definition skills/manage-file-work-items/SKILL.md to make its provider claim directions conditional for resource coordination agent-claim versus none?

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/respect-resource-coordination-none-in-manage-file-work-items.md

Completion: direct-main

Owner: Unowned

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-first-eight-lint-defects-019fa9bb

Normalized Objective: Make file-provider work-item procedures valid when a project selects resource coordination none as well as when it selects agent-claim.

Dispatch Time: 2026-07-28T18:22:25Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019fa9f9-9548-7853-9fe3-301c76b94b82

Root Agent Task: 019fa9f9-9548-7853-9fe3-301c76b94b82

Branch: codex/respect-resource-coordination-none-019fa9f9

Worktree: /Users/martinbechard/.codex/worktrees/c089/dev-methodology

Current Phase: Paused pending scope-specific user authorization for a governed canonical definition change.

Started At Evidence: Root acceptance recorded by Dev Backlog Steward on 2026-07-28T18:39:39Z after the parent reservation, against Runtime Thread and Root Agent Task 019fa9f9-9548-7853-9fe3-301c76b94b82.

Claim Evidence: SHARED_CHECKOUT_ACQUIRED claim running-acceptance-respect-resource-coordination-none-019fa9f9; incarnation a1e091bf-51fe-4f58-a077-b2ead9fe9f49; claim journal event 3d683343-0e55-46fe-b292-421593bcdfdb; exact provider path claimed in the primary main checkout.

Next Lifecycle Owner: User, then Parent Coordinator and the preserved Root Dev Orchestrator.

## User Action Required

Why User Input Is Required: Only the user can grant the explicit, scope-specific authority required to change a governed canonical definition. Repository access, a defect record, review, testing, or coordinator direction cannot supply that authority.

Prohibited Unattended Actions: Do not mutate the definition, tests, generated mirrors, integration state, or delivery artifacts until the user grants the requested approval.

Required After Approval: Record the exact approval evidence for skills/manage-file-work-items/SKILL.md, then run the supported pre-mutation definition-change check before any definition mutation.

Approval Scope: skills/manage-file-work-items/SKILL.md

Parent Coordinator Task: 019fa9bb-1423-7e80-bcde-3caa765e3758

Resolution: Approved on 2026-07-28. Exact user direction: The manage-file-work-items skill shouldn't know about agent claims, they are independent concerns that would both be loaded based on the agent and/or project definition, so clean up the manage-file-work-items.md to not have that in one form or another.

## Resumption Evidence

Transition: User Action Required to Ready recorded on 2026-07-28.

Answer Provenance: User message in preserved canonical Runtime Thread 019fa9f9-9548-7853-9fe3-301c76b94b82, routed to Parent Coordination Thread 019fa9bb-1423-7e80-bcde-3caa765e3758.

Approved Scope and Semantics: skills/manage-file-work-items/SKILL.md only. Remove agent-claim knowledge in every form. Agent-claim remains independently loaded and applied; no other governed definition scope is approved.

Preserved Execution Identity: Runtime Thread and Root Agent Task 019fa9f9-9548-7853-9fe3-301c76b94b82; branch codex/respect-resource-coordination-none-019fa9f9; worktree /Users/martinbechard/.codex/worktrees/c089/dev-methodology; prior lifecycle and recovery history remain intact.

Pre-Mutation Requirement: Before any governed definition mutation, create the exact approval record from this user direction and pass the supported definition-change preflight for skills/manage-file-work-items/SKILL.md.

## Recovery Evidence

Prior Claim Rejection: DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED

Prior Claim Journal Event: 4e21cbb8-b901-4079-8977-303417ab7d58

Recovery Authorization: Parent Coordinator confirmed that concurrent User Action Required moves committed through a4d13eae514829047b61a25e77272ec886d00e06, primary main was clean, and the claim registry was empty before this one retry.

## Read-Only Findings

No candidate or implementation change exists. The active record's source evidence identifies the governed definition and requires explicit user approval before any correction work.

## Summary

Make file-provider work-item procedures valid when a project selects resource coordination none as well as when it selects agent-claim.

## Context

The primary affected skill is skills/manage-file-work-items/SKILL.md. Its clauses require agent-claim even when a valid project selects resource_coordination: none. In that configuration there is no enabled claim procedure for the mandatory operation, leaving no valid provider route.

## Source Evidence

The user authorized immediate creation of independently dispatchable Defect records for every accepted skill-lint finding on 2026-07-28. The accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records the affected clauses at skills/manage-file-work-items/SKILL.md:28,150,244. Independent reviewer /root/confirm_critical_c accepted it as CONFIRMED_CRITICAL.

## Requirements

- Make provider claim directions conditional on the configured coordination implementation.
- Define the valid no-claim route when resource coordination is none.
- Preserve the agent-claim route when it is configured.

## Acceptance Criteria

- Identical provider transitions have a valid documented route under agent-claim and none configurations.
- The none configuration does not require an unavailable claim procedure.
- The agent-claim configuration retains conflict protection.

## Dependencies

None

## Verification

- Exercise identical provider transitions under agent-claim and none configurations.
- Confirm a valid route in both cases.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None.

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/manage-file-work-items/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check.
