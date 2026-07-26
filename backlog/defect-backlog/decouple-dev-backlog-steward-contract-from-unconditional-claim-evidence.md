# Decouple Dev Backlog Steward Contract From Unconditional Claim Evidence

Status: Ready

Type: Defect

Owner: Unowned

Provider: file

Provider Reference: backlog/defect-backlog/decouple-dev-backlog-steward-contract-from-unconditional-claim-evidence.md

Completion: direct-main

## Recovery Resumption

- Transition: Blocked -> Ready under the user's restart-blocked authorization.
- Historical Canonical Work-Item Thread/Task: 019f96f1-1a19-7b01-b166-c5948a50fff5 remains preserved; all approvals, candidates, and authority boundaries remain unchanged.
- Recovery Scope: Reconcile current-main semantics first, then make a bounded correction only if needed, with fresh independent review, focused verification, direct-main delivery/provider closure, and no full repository regression.
- Next Lifecycle Owner: Parent Dev Backlog Coordinator reserves Ready -> Starting; root Dev Orchestrator acceptance is required before Running.

## Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Reservation: One parent-owned same-task resumption launch reservation.
- Normalized Objective: Decouple Dev Backlog Steward contracts from unconditional claim evidence.
- Dispatched At: 2026-07-25T04:08:26Z
- Intended Root Role: Dev Orchestrator
- Runtime Thread And Task Id: Existing canonical work-item Thread 019f96f1-1a19-7b01-b166-c5948a50fff5 is retained; no replacement task was created.

## Execution Ownership

- Canonical Work-item Thread And Task Id: 019f96f1-1a19-7b01-b166-c5948a50fff5
- Root Owner: Dev Orchestrator
- Delivery Branch: Detached pending delivery claim.
- Delivery Worktree: /Users/martinbechard/.codex/worktrees/ecbc/dev-methodology
- Phase: Approved implementation and focused coordination matrix.
- Started At: 2026-07-25T04:09:25Z

## Coordination Evidence

- Backlog Claim: 019f96f1-running-transition acquired on primary main at 2026-07-25T02:05:01.221304Z; acquisition journal event 48f71097-1095-4071-9b12-165048f4e832.
- Direct Release Baton: running-backlog-lifecycle-019f96f0 was released after primary-main backlog transaction 766464a894ab3427d8eebc3aa28bc865119e199b; release event 5f486be7-acea-4f90-a200-75dcbe75fd43.
- Prior Release Baton: decouple-dev-orchestrator-eval-correction1-019f96ce released event c1cd5671-52fe-468f-a363-c561e7e0140f.
- Current Backlog Claim: 019f96f1-running-discovery-transition acquired on primary main at 2026-07-25T02:46:17.204850Z; acquisition journal event ef354e4e-41bb-46ea-a849-1c1287ca8eac.
- Approved-Implementation Backlog Claim: 019f96f1-running-approved-implementation acquired on primary main at 2026-07-25T04:09:25.562855Z; acquisition journal event 0f745454-173b-4c39-8c9c-71a0544f447e.

## Blocked Handoff

Blocker: After two bounded correction rounds, fresh final artifact review is NOT APPROVED on FIND-1 (Medium). The mechanically fresh generator-owned design/agent-and-skill-evaluations.html unconditionally requires a claim or new claim in the Dev Backlog Steward scenario rows because evals/agent-tests/dev-backlog-steward/scenarios.yaml remains unchanged. The approved canonical role is neutral and delegates coordination to project guidance.

Required Resolution: Correct the scenario source so claim behavior is explicitly conditional on resource_coordination: agent-claim, add equivalent resource_coordination: none coverage, regenerate the page, and run page-level regression. No third correction is authorized in this candidate lifecycle.

Preserved Candidate Chain: 9b746336b6663eee9cfb0124a99780482392f1d2 -> 32396d241493f3ef542b633b6f28d335e3fd5dab -> f30bbb84c47359a84f7e798c3a875b5657f0f923 on branch codex/decouple-backlog-steward-correction2-019f96f1. The preserved worktree is clean at /Users/martinbechard/dev/dev-methodology/.worktrees/019f96f1-steward-correction2-isolated, and all project claims are released.

Passing Evidence: Role and renderer tests passed (116); full scripts passed (697); generator freshness, skill validation, and git diff --check passed; fresh code review approved. Final artifact review remains blocked only on FIND-1.

Unblock Condition And Recovery Owner: A separately authorized or resumed lifecycle must correct the evaluation scenario, obtain fresh review and verification, then reuse the preserved commits without reimplementation. Until then, Owner remains Unowned.

## Prior User Action Resolution

Prior Requested Approval: NOT APPROVED. The user explicitly rejected the single canonical-role path as the solution.

Resolution Provenance: Current user message in canonical Thread 019f96f1-1a19-7b01-b166-c5948a50fff5.

Corrected Architectural Direction:

- PROJECT.yaml -> AGENTS.md conversion adds the selected resource-coordination skill by reference or inline only when the selection is other than none.
- When the selection is none, AGENTS.md mentions no coordination skill or lifecycle.
- Portable Dev Backlog Steward contracts do not embed claim mechanics.

Resumption Requirement: Perform fresh discovery of the renderer, generated AGENTS.md, portable-role neutrality, and the exact governed approval manifest before requesting any new scope-specific approval.

Prior Discovery Evidence Retained: The definition_change_authority precheck returned BLOCKED_APPROVAL_REQUIRED; failing tests and a repair assignment were not approval. Five exact test_role_mutation_policy failures concerned one canonical role and generated Claude, Codex, Gemini, and Junie adapters. Supported mirrors remain generated/adapters/** and design/generated/role-definitions.js; two unrelated broad failures remain outside this item.

Unattended Work Boundary: Do not mutate a governed definition or regenerate a mirror until the fresh discovery identifies an exact governed scope and a successful user-approved manifest check exists.

Lifecycle Resumption: This answer restores the item to Ready only. The parent Coordinator must reserve Ready -> Starting, then the same root Dev Orchestrator must record Starting -> Running before delivery work resumes.

## Approved User Direction

Question: Do you approve mutation of agents/roles/dev-activities/dev-backlog-steward.role.yaml specifically to REMOVE resource-coordination selection and agent-claim mechanics from the portable Steward contract, leaving provider lifecycle durability in the role and relying entirely on PROJECT.yaml -> AGENTS.md injection for coordination behavior?

Approval: APPROVED.

Approval Provenance: Current user message in canonical Thread 019f96f1-1a19-7b01-b166-c5948a50fff5 on 2026-07-25.

Approved Semantics: Remove resource-coordination selection and agent-claim mechanics from the portable Steward contract; preserve provider lifecycle durability; rely entirely on existing PROJECT.yaml -> AGENTS.md injection, with no renderer behavior change.

### Governed Canonical Approval Scope

- agents/roles/dev-activities/dev-backlog-steward.role.yaml

### Generated Mirrors Only (Not Approval Scope)

- generated/adapters/claude/agents/dev-backlog-steward.*
- generated/adapters/codex/agents/dev-backlog-steward.*
- generated/adapters/gemini/agents/dev-backlog-steward.*
- generated/adapters/junie/agents/dev-backlog-steward.*
- design/generated/role-definitions.js

### Ordinary Test Scope (Not Governed)

- scripts/test_technology_detection.py: focused none-versus-agent-claim AGENTS.md output matrix.
- scripts/test_role_mutation_policy.py: portable-role neutrality.

Discovery Evidence: The renderer already emits no coordination or transport guidance when resource_coordination is none, and adds reference-only agent-claim plus the configured inlined transport only when selected. No renderer behavior change is planned.

Prior Rejected Proposal Retained: The conditional-wording proposal remains NOT APPROVED; this approval governs only removal of coordination mechanics from the portable Steward contract.

Resumption Path: This resolution restores Ready only. The parent Coordinator must reserve Ready -> Starting, then this same root Dev Orchestrator must record Starting -> Running in canonical Thread 019f96f1-1a19-7b01-b166-c5948a50fff5 before delivery resumes.

Resolution: Approved as recorded above. Before mutation, create and pass the exact governed approval manifest for the approved canonical path; regenerate only the supported mirrors after that check.

## Summary

Make Dev Backlog Steward’s canonical and generated contracts honor resource_coordination none without requiring claim calls or claim evidence, while preserving strict claim behavior when agent-claim is selected.

## Context

Candidate cb5c7725 reproduced five broad scripts-gate failures that map to one distinct unrecorded defect: Dev Backlog Steward canonical and generated contracts use unconditional claim-evidence wording even when resource_coordination is none. This conflicts with the project-selected resource-coordination contract, which requires provider-none flows to make zero claim calls and require no claim evidence.

## Source Evidence

The candidate cb5c7725 broad scripts gate reproduced the five related failures. The user policy in parent Thread 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a requires every confirmed defect to be durably logged rather than treated as a warning.

Discovery evidence: five exact test_role_mutation_policy failures concern one canonical role and the generated Claude, Codex, Gemini, and Junie adapters. The supported generated mirrors are generated/adapters/** and design/generated/role-definitions.js. Two unrelated broad failures are outside this item.

## Requirements

- Identify the exact canonical and generated Dev Backlog Steward contract surfaces that unconditionally require claim evidence.
- When resource_coordination is none, require zero claim calls, registry mutations, releases, and claim-specific lifecycle evidence.
- When agent-claim is selected, preserve strict short backlog-claim acquisition, committed mutation, and truthful release evidence.
- Keep file-provider lifecycle ownership and resource-coordination selection independent.
- Obtain an exact canonical-path approval record before mutating any governed definition source.

## Acceptance Criteria

- Provider-none scenarios for Dev Backlog Steward complete with zero claim calls and no claim-specific evidence requirement.
- Agent-claim-selected scenarios retain required acquisition, commit, and release evidence.
- Canonical source, generated adapter, and applicable scripts/evaluation/bundle surfaces agree on the selected behavior.
- The focused reproducer for the five related gate failures passes or is replaced by evidence-backed equivalent coverage.

## Dependencies

None.

## Verification

- Refine and run a focused reproducer across the affected scripts, evaluation, and bundle surfaces.
- Run focused resource-coordination-none and agent-claim-selected lifecycle tests.
- Run generated-definition freshness and applicable broad scripts gate checks.
- Obtain fresh independent review.

## Open Questions

- Which exact canonical Dev Backlog Steward definitions and derived adapters are implicated by the candidate’s five failures?

## Notes

This record preserves the current confirmed scope for implementation discovery. Do not change a governed canonical definition without a successful exact-path approval-manifest check.
