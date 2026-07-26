# Bind Project-Files Claims to the Primary Worktree

Status: User Action Required

Type: Defect

Owner: Unowned

Provider: file

Provider Reference: backlog/user-action-required/bind-project-files-claims-to-primary-worktree.md

Completion: direct-main

## Summary

Make project-files claim acquisition and release safe for direct-main delivery when the claimant uses a linked worktree.

## Context

The canonical root-AGENTS task 019f9fd6-d7c1-7902-bf33-e10883383b7e delivered accepted candidate 71387a2968d3f879e12d599887bc2981e1bb7144 through non-ancestral primary-main integration 1dded7f556cf4270e2a0bff12178382eac17c3c4. Its live project-files claim, integrate-reconcile-root-agents-019f9fd6, was acquired from linked worktree /Users/martinbechard/.codex/worktrees/9188/dev-methodology. The helper permits that acquisition because project_files is excluded from the primary-worktree scope check, but release validates the claimant worktree HEAD and cannot observe the primary-main integration. The release was rejected as missing_commit_or_no_change.

## Source Evidence

The Parent Coordinator explicitly directed durable Ready logging of this distinct confirmed defect after reviewing the accepted candidate, integration, claim registry, rejected-release event 0abe6b25-19f3-4635-bb38-15769a7861ec, and helper behavior. The defect is separate from the root-AGENTS correction and requires no runtime task at creation.

## Requirements

- Require Event-2 project-files claims to bind to the primary worktree, or return a clear primary-required outcome when requested from a linked worktree.
- Align release validation with that binding so an accepted non-ancestral primary-main integration can be observed safely.
- Preserve the existing claim-event contract and unrelated claim scopes.
- Add a focused public-command regression covering linked acquisition and non-ancestral primary-main integration.

## Acceptance Criteria

- A linked-worktree project-files acquisition either binds safely to primary-main delivery or returns a clear primary-required outcome.
- Release validation recognizes the supported binding and does not falsely require the linked worktree HEAD to contain a non-ancestral primary-main integration.
- The focused public-command regression passes and proves the linked-acquisition and non-ancestral-integration behavior.
- Existing event-contract coverage remains valid.

## Dependencies

None.

## Verification

- Run the focused public-command regression for linked project-files acquisition and non-ancestral primary-main integration.
- Run directly affected helper and event-contract tests.
- Obtain independent review of the claim lifecycle change.

## Open Questions

Do you approve expanding this same task to add a targeted administrative recovery operation by changing the governed definition skills/agent-claim-command/SKILL.md, its implementation skills/agent-claim-command/scripts/claim.py, focused tests, and only the supported generated mirrors? The operation will require the exact claim ID and incarnation, acquisition and rejected-release event IDs, integrated commit, and verified content mapping; it will lock the registry, remove only that claim, and append a durable recovery-release event.

## User Action Required

The same canonical task needs one explicit user decision before any new recovery capability can be implemented.

## Question for the User

Do you approve expanding this same task to add a targeted administrative recovery operation by changing the governed definition skills/agent-claim-command/SKILL.md, its implementation skills/agent-claim-command/scripts/claim.py, focused tests, and only the supported generated mirrors? The operation will require the exact claim ID and incarnation, acquisition and rejected-release event IDs, integrated commit, and verified content mapping; it will lock the registry, remove only that claim, and append a durable recovery-release event.

Options:

- Approve: bounded implementation, review, and verification; recover only this claim; then integrate 682f521c49e1f6200e7ddcbcba1d19dad7a6c32b.
- Narrow: provide a revised plan.
- Defer: preserve all state.
- Decline: leave both items blocked with no new capability.

## Why User Input Is Required

The requested capability changes a governed skill definition and the claim-helper implementation. The project requires explicit, scope-specific user approval before either surface is changed.

## Unattended Work Boundary

No governed definition, helper, registry, journal, integration, closeout, or cleanup mutation may occur before an answer.

## Resolution

Pending user answer.

## Preserved Recovery Evidence

- Canonical Work-Item Thread And Root Agent Task: 019f9fef-1edc-7ea1-a058-bf8dfddcd2fb.
- Accepted Prevention Candidate: 682f521c49e1f6200e7ddcbcba1d19dad7a6c32b. It remains preserved and unintegrated pending the requested approval and a supported recovery operation.
- Rejected Candidate: c604e237865c3e20739e61e6c12e8eae568040d9. Preserve it as rejected recovery history; do not integrate it.
- Review And Verification: Retain the accepted prevention candidate's review and verification evidence in the canonical task context. This lifecycle transition does not accept, rerun, replace, or discard that evidence.
- Retained Live Claim: integrate-reconcile-root-agents-019f9fd6, incarnation 475d66c7-a792-434b-bdaf-1b0f8a6bccfb, remains a live project-files claim. Its baseline and linked-worktree HEAD are 71387a2968d3f879e12d599887bc2981e1bb7144; its linked worktree is /Users/martinbechard/.codex/worktrees/9188/dev-methodology.
- Project Configurator Conclusion: No current command or MCP helper supports targeted administrative recovery for this claim.
- Prohibited Recovery Shortcuts: Do not use normal release, no-change release, out-of-domain reconciliation, registry or journal editing, candidate integration, closeout, or cleanup.

## Starting Reservation

- Transition: Ready -> Starting.
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a.
- Reservation: One parent-owned launch reservation.
- Normalized Objective: Bind Event-2 project-files claims to the primary worktree and prevent unreleasable non-ancestral integrations.
- Dispatched At: 2026-07-26T19:36:56Z.
- Intended Root Role: Dev Orchestrator.
- Runtime Thread And Task Id: Pending canonical child task creation by the parent after this durable reservation.
- Coordination Note: Integration and recovery of the live claim integrate-reconcile-root-agents-019f9fd6 remain deferred until this candidate is accepted.

## Preserved Running Acceptance

- Prior Transition: Starting -> Running.
- Canonical Work-Item Thread: 019f9fef-1edc-7ea1-a058-bf8dfddcd2fb.
- Canonical Root Agent Task: 019f9fef-1edc-7ea1-a058-bf8dfddcd2fb.
- Prior Owner: root Dev Orchestrator.
- Parent Coordinator: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a.
- Branch: codex/bind-project-files-primary-019f9fef.
- Worktree: /Users/martinbechard/.codex/worktrees/aa2f/dev-methodology.
- Phase: Root-cause reproduction and candidate implementation.
- Started-At Evidence: Root Dev Orchestrator acceptance recorded by the primary-main file provider transaction on 2026-07-26.
- Claim Evidence: SHARED_CHECKOUT_ACQUIRED event 52d1510e-a5b9-4b4e-b402-3e0cfa145ed3 protected this exact backlog file for the acceptance transaction.
- Transition Note: This User Action Required transition preserves the canonical task and all candidate, review, verification, and retained-live-claim evidence. It creates no replacement Thread.

## Notes

This item is not runnable or approved for unattended work until the user answers the exact question above. The retained live project-files claim remains outside this backlog transaction.
