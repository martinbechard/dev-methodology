# Decouple Dev Backlog Steward Contract From Unconditional Claim Evidence

Status: User Action Required

Type: Defect

Owner: Unowned

Provider: file

Provider Reference: backlog/user-action-required/decouple-dev-backlog-steward-contract-from-unconditional-claim-evidence.md

Completion: direct-main

## Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Reservation: One same-task resumption launch reserved by the parent Dev Backlog Coordinator.
- Normalized Objective: Decouple Dev Backlog Steward contracts from unconditional claim evidence.
- Dispatched At: 2026-07-25T02:43:56Z
- Intended Root Role: Dev Orchestrator
- Runtime Thread And Task Id: Existing canonical work-item Thread 019f96f1-1a19-7b01-b166-c5948a50fff5 is retained; no replacement task was created.

## Prior Execution Ownership

- Canonical Work-item Thread And Task Id: 019f96f1-1a19-7b01-b166-c5948a50fff5
- Prior Root Owner: Dev Orchestrator
- Delivery Branch: Detached pending delivery claim.
- Delivery Worktree: /Users/martinbechard/.codex/worktrees/ecbc/dev-methodology
- Phase: Fresh renderer and portable-contract discovery.
- Started At: 2026-07-25T02:46:17Z

## Coordination Evidence

- Backlog Claim: 019f96f1-running-transition acquired on primary main at 2026-07-25T02:05:01.221304Z; acquisition journal event 48f71097-1095-4071-9b12-165048f4e832.
- Direct Release Baton: running-backlog-lifecycle-019f96f0 was released after primary-main backlog transaction 766464a894ab3427d8eebc3aa28bc865119e199b; release event 5f486be7-acea-4f90-a200-75dcbe75fd43.
- Prior Release Baton: decouple-dev-orchestrator-eval-correction1-019f96ce released event c1cd5671-52fe-468f-a363-c561e7e0140f.
- Current Backlog Claim: 019f96f1-running-discovery-transition acquired on primary main at 2026-07-25T02:46:17.204850Z; acquisition journal event ef354e4e-41bb-46ea-a849-1c1287ca8eac.

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

## User Action Required

Question: Do you approve mutation of agents/roles/dev-activities/dev-backlog-steward.role.yaml specifically to REMOVE resource-coordination selection and agent-claim mechanics from the portable Steward contract, leaving provider lifecycle durability in the role and relying entirely on PROJECT.yaml -> AGENTS.md injection for coordination behavior?

Why Input Is Required: This is materially different from the prior rejected conditional-wording proposal. It changes the portable role boundary by removing coordination mechanics, so it requires new exact scope-specific user approval.

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

Prohibited Unattended Action: Do not mutate the canonical role or regenerate any mirror before explicit approval.

Permitted Resumption: Record the answer in this same canonical Thread, restore User Action Required -> Ready, have the parent Coordinator reserve Ready -> Starting, then have this same root Dev Orchestrator record Starting -> Running before delivery resumes.

Resolution: Pending explicit user answer to this distinct approval question.

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
