# Bind Project-Files Claims to the Primary Worktree

Status: Completed

Type: Defect

Owner: Unowned

Provider: file

Provider Reference: backlog/completed-backlog/defects/bind-project-files-claims-to-primary-worktree.md

Completion: direct-main

## Summary

Bind Event-2 project-files claim acquisition to the primary worktree and revise normal release cleanup so it removes only its exact claim under the registry lock and appends RELEASED evidence, without Git or delivery validation.

## Context

The canonical root-AGENTS task 019f9fd6-d7c1-7902-bf33-e10883383b7e delivered accepted candidate 71387a2968d3f879e12d599887bc2981e1bb7144 through non-ancestral primary-main integration 1dded7f556cf4270e2a0bff12178382eac17c3c4. Its live project-files claim, integrate-reconcile-root-agents-019f9fd6, was acquired from linked worktree /Users/martinbechard/.codex/worktrees/9188/dev-methodology. The helper permits that acquisition because project_files is excluded from the primary-worktree scope check, but release validates the claimant worktree HEAD and cannot observe the primary-main integration. The release was rejected as missing_commit_or_no_change. The revised direction is that ordinary claim release removes only the exact claim while holding the registry lock and appends RELEASED evidence; it performs no Git or delivery validation.

## Source Evidence

The Parent Coordinator explicitly directed durable Ready logging of this distinct confirmed defect after reviewing the accepted candidate, integration, claim registry, rejected-release event 0abe6b25-19f3-4635-bb38-15769a7861ec, and helper behavior. The defect is separate from the root-AGENTS correction and requires no runtime task at creation. In the canonical task on 2026-07-26, the user said: “Ok do it and add a directive that before putting an item in user action required you should check the agent-claim skill”. This approves the revised direction, but it does not satisfy the repository's exact-scope definition approval requirement for all six newly discovered governed definitions.

On 2026-07-26, in canonical task and work-item Thread 019f9fef-1edc-7ea1-a058-bf8dfddcd2fb, the user answered `Approved`, explicitly authorizing exactly these governed definitions: skills/agent-claim/SKILL.md; skills/agent-claim-command/SKILL.md; skills/agent-claim-mcp/SKILL.md; skills/create-file-work-item/SKILL.md; skills/manage-file-work-items/SKILL.md; and skills/codex-workitem-coordination/SKILL.md. The approval also covers the already-stated dependent ordinary helper code, focused tests, and supported generated skill mirrors.

## Requirements

- Require Event-2 project-files claims to bind to the primary worktree, or return a clear primary-required outcome when requested from a linked worktree.
- Make normal release remove only the exact claim under the registry lock and append RELEASED evidence, with no Git or delivery validation.
- Remove normal-release no_change and out-of-domain reconciliation contracts from the command and MCP surfaces.
- Before creating or transitioning an item to User Action Required, when agent-claim is loaded, apply it to the blocker and confirm that a genuine user-owned decision remains.
- Preserve unrelated claim scopes and the existing claim-event contract outside the revised release semantics.

## Acceptance Criteria

- A linked-worktree project-files acquisition either binds safely to primary-main delivery or returns a clear primary-required outcome.
- Normal release removes only its exact claim while holding the registry lock and records RELEASED evidence without Git or delivery validation.
- Command and MCP normal-release surfaces no longer expose no_change or out-of-domain reconciliation contracts.
- User Action Required creation and transition guidance applies agent-claim to the blocker when loaded and only proceeds when a genuine user-owned decision remains.
- Focused helper and contract tests cover the revised behavior, and only supported generated skill mirrors are refreshed.

## Dependencies

None.

## Verification

- Run focused helper, command/MCP surface, and User Action Required workflow tests.
- Run directly affected event-contract tests.
- Validate supported generated-skill mirror freshness.
- Obtain independent review of the governed-definition and helper changes.

## Open Questions

None. The recorded exact-scope approval resolves the previous governed-definition authorization question.

## Resolved User Action Required

The same canonical task required one explicit user decision before any new recovery capability could be implemented. That decision is now recorded in Resolution.

## Resolved Question

Do you approve changing exactly these six governed definitions to implement the revised claim-cleanup and User Action Required rules: skills/agent-claim/SKILL.md; skills/agent-claim-command/SKILL.md; skills/agent-claim-mcp/SKILL.md; skills/create-file-work-item/SKILL.md; skills/manage-file-work-items/SKILL.md; skills/codex-workitem-coordination/SKILL.md?

Options:

- Approve exact six paths: authorize only the six listed governed definitions; dependent ordinary scope after approval is skills/agent-claim-command/scripts/claim.py, focused tests, and only supported generated skill mirrors.
- Narrow: provide a smaller exact-path approval scope.
- Defer: preserve all evidence and do not resume work.
- Decline: end this revised direction without mutation.

## Resolved Approval Basis

The revised direction requires changes to six governed skill definitions. The project requires explicit, scope-specific approval naming each canonical definition before any governed definition can be changed. The user's recorded wording approves the direction but not this exact six-path scope.

## Post-Resolution Boundary

Exact approval is recorded and User Action Required -> Ready is now durable. A parent Coordinator must separately reserve Ready -> Starting for the preserved canonical Thread, and its root Dev Orchestrator must separately accept Starting -> Running before any governed definition, helper, test, generated-mirror, claim-release, candidate-integration, provider-resumption, or cleanup mutation.

## Resolution

- User answer: `Approved`.
- Date: 2026-07-26.
- Provenance: canonical task and work-item Thread 019f9fef-1edc-7ea1-a058-bf8dfddcd2fb.
- Exact approval scope: skills/agent-claim/SKILL.md; skills/agent-claim-command/SKILL.md; skills/agent-claim-mcp/SKILL.md; skills/create-file-work-item/SKILL.md; skills/manage-file-work-items/SKILL.md; and skills/codex-workitem-coordination/SKILL.md, plus the already-stated dependent ordinary helper code, focused tests, and supported generated skill mirrors.
- Resulting disposition: User Action Required -> Ready in backlog/defect-backlog, with Owner: Unowned.
- Canonical identity: preserve canonical Work-Item Thread and Root Agent Task 019f9fef-1edc-7ea1-a058-bf8dfddcd2fb. No replacement Thread is authorized.

## Preserved Recovery Evidence

- Canonical Work-Item Thread And Root Agent Task: 019f9fef-1edc-7ea1-a058-bf8dfddcd2fb.
- Accepted Prevention Candidate: 682f521c49e1f6200e7ddcbcba1d19dad7a6c32b. It remains preserved as evidence pending revised-objective reconciliation; this record does not assert that it will necessarily be integrated.
- Rejected Candidate: c604e237865c3e20739e61e6c12e8eae568040d9. Preserve it as rejected recovery history; do not integrate it.
- Review And Verification: Retain the accepted prevention candidate's review and verification evidence in the canonical task context. This lifecycle transition does not accept, rerun, replace, or discard that evidence.
- Retained Live Claim: integrate-reconcile-root-agents-019f9fd6, incarnation 475d66c7-a792-434b-bdaf-1b0f8a6bccfb, remains a live project-files claim. Its baseline and linked-worktree HEAD are 71387a2968d3f879e12d599887bc2981e1bb7144; its linked worktree is /Users/martinbechard/.codex/worktrees/9188/dev-methodology.
- Project Configurator Conclusion: The revised semantics require exact governed-definition approval before any command or MCP release-surface change can be made.
- Prohibited Recovery Shortcuts: Do not release the retained claim, edit the registry or journal, integrate either candidate, resume the provider, close out, or clean up before the recorded approval and lifecycle resumption are durable.

## Starting Reservation

- Transition: Ready -> Starting.
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a.
- Reservation: One parent-owned launch reservation.
- Normalized Objective: Make claim release exact-claim cleanup only, remove no-change/out-of-domain release contracts, and require applying agent-claim before User Action Required.
- Dispatched At: 2026-07-26T21:05:46Z.
- Intended Root Role: Dev Orchestrator.
- Runtime Thread And Task Id: 019f9fef-1edc-7ea1-a058-bf8dfddcd2fb, accepted by the preserved root Dev Orchestrator.
- Coordination Note: Integration and recovery of the live claim integrate-reconcile-root-agents-019f9fd6 remain deferred until this candidate is accepted.

## Running Acceptance

- Transition: Starting -> Running.
- Canonical Work-Item Thread: 019f9fef-1edc-7ea1-a058-bf8dfddcd2fb.
- Canonical Root Agent Task: 019f9fef-1edc-7ea1-a058-bf8dfddcd2fb.
- Owner: root Dev Orchestrator.
- Parent Coordinator: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a.
- Branch: codex/bind-project-files-primary-019f9fef.
- Worktree: /Users/martinbechard/.codex/worktrees/aa2f/dev-methodology.
- Phase: Root-cause reproduction and candidate implementation.
- Started-At Evidence: Root Dev Orchestrator accepted the preserved canonical Thread on 2026-07-26; this primary-main transaction records that acceptance.
- Claim Evidence: SHARED_CHECKOUT_ACQUIRED event 3ab5a83d-f658-436a-877b-ea4e86c92dcd protected this exact backlog file for this acceptance transaction.
- Reservation Evidence: Ready -> Starting commit daa13c0adeb48e37f0ea1b56bc364e7f461deff2, following Ready approval commit 40cc7744e88dc15af04739a96ff3c37e4857ef51; reservation events a972a346-943c-45a0-ba40-0e234683513d and e6898101-147a-4cf9-87fd-791eacbf17ac.
- Preserved Constraint: The live claim integrate-reconcile-root-agents-019f9fd6 and its recovery remain untouched.

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

This item is completed. The preserved canonical Thread remains the execution identity.

## Completion Evidence

- Accepted delivery on main: cd11437ecc922e89e57d6cb996b098437306d9cd.
- Main includes cleanup-only release, registry reset, linked-worktree project-files rejection, revised User Action Required guidance, focused tests, and generated mirrors.
- The former retained claim integrate-reconcile-root-agents-019f9fd6 is absent from the live registry.
- Ten focused helper, command, transport, and contract tests passed.
- The focused Coordinator reset test passed.
- Generated-output freshness, six-skill validation, and Git diff check passed.
- Installed agent-claim, agent-claim-command, and helper bytes match main.
- Independent-review omission: the user directed direct single-task completion without delegation; this terminal verification reviewed the delivered main behavior directly.
