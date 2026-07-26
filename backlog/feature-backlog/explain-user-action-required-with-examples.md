# Explain User Action Required Requests With Examples

Status: Starting

Type: Feature

Owner: Parent Dev Backlog Coordinator reservation pending root acceptance

Claim: None

Provider: file

Provider Reference: backlog/feature-backlog/explain-user-action-required-with-examples.md

Completion: direct-main

## Recovery Resumption

- Transition: Blocked -> Ready.
- Recovery Authority: The user's current request explicitly authorizes this fresh bounded recovery; all prior exact governed-definition approvals and the canonical work-item identity remain preserved.
- Preserved Canonical Thread/Task: 019f9722-61cb-7190-8a6d-21c5ab319339. No replacement Thread or task is authorized.
- Recovery Scope: Reconcile current-main semantics first; make a bounded correction only if needed; obtain fresh prompt, methodology, and source review; run focused verification; deliver directly on main and close the provider record only if acceptance evidence supports it. A full repository regression is not requested.
- Ready Evidence: The prior two-cycle correction exhaustion and all candidate, review, verification, approval, and blocked-handoff evidence below remain durable recovery context. The parent Dev Backlog Coordinator may now make a distinct Ready -> Starting reservation for the preserved canonical Thread.

## Current Launch Reservation

- Transition: Ready -> Starting.
- Parent Coordination Thread: /root/resume_blocked_after_claim_publication.
- Reservation: One recovery launch is reserved for the preserved canonical work-item Thread 019f9722-61cb-7190-8a6d-21c5ab319339; no replacement Thread is authorized.
- Normalized Objective: Reconcile current-main semantics first; make a bounded correction if needed; obtain fresh prompt, methodology, and source review; run focused verification; deliver directly on main and close the provider record only if acceptance evidence supports it; do not run a full repository regression.
- Dispatched At: 2026-07-26T07:24:06Z.
- Intended Root Role: Dev Orchestrator.
- Root Acceptance: Pending. No Starting -> Running transition, root task identifier, branch/worktree assignment, or delivery ownership has been recorded by this reservation.

## Prior Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Reservation: One same-task resumption launch reserved by the parent Dev Backlog Coordinator.
- Normalized Objective: Explain User Action Required requests with examples.
- Dispatched At: 2026-07-25T03:15:31Z
- Intended Root Role: Dev Orchestrator
- Runtime Thread And Task Id at reservation: Existing canonical work-item Thread 019f9722-61cb-7190-8a6d-21c5ab319339 is retained; no replacement task was created.
- Approval Provenance: The same canonical task recorded the example-backed exact `ok approved` answer for agents/roles/dev-activities/dev-orchestrator.role.yaml and skills/manage-file-work-items/SKILL.md before this resumption reservation.

## Active Ownership

- Canonical Dev Orchestrator Task/Thread: 019f9722-61cb-7190-8a6d-21c5ab319339
- Canonical Owner: Dev Orchestrator
- Checkout: /Users/martinbechard/.codex/worktrees/a8df/dev-methodology
- Branch: HEAD
- Checkout State: Detached HEAD at 271c0fe1a12d9c720fca3c041eb79a6f5ec422bb.
- Current Phase: Starting under the current parent reservation; root acceptance remains pending.
- Transition Evidence: Parent Coordinator 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a provided the direct baton after the prior backlog transaction released. The file provider was reconciled as Starting at main commit 49c78f81a91c3eccab21e50a7413d707b7fe3938, then this serialized backlog claim was acquired as 019f9722-user-action-required-starting-running (claim event 5fa1c816-7d42-4fd0-9724-a13f5bbe6587). After the same-task approval was recorded, the provider was reconciled as Starting at main commit ef9efa60914050236ba2a409abe505eeea1c34d6 and claim 019f9722-approved-starting-running was acquired for this Starting to Running transition (claim event 0f5c6788-42bc-4f4d-bd24-25967053830d).

## Blocked Handoff

### Exact Blocker

The bounded correction loop is exhausted after two correction cycles. Final fresh prompt-contract review and fresh source and test review did not accept candidate 12721aaf54ae680671596a1ee934e0fa45d30a05.

### Persistent Findings

- Replay versus repeated-request wording remains contradictory.
- Stable envelope normalization and state transitions are insufficiently deterministic.
- Semantic adversarial tests still accept synonym and negated contradictions and weak task-local durability.
- skills/manage-file-work-items/SKILL.md still contains a direct UNSET ask bypass.
- The User Action Required resume example and status conflict with the existing RUNNING output contract.

### Review Disposition

Methodology review v3 was GOOD, but it cannot override the prompt-contract and source and test review rejection gates.

### Candidate Chain

- Initial: 59e9938810c9a498f3264f00a75d1424ed1deac4, base 1d909c76.
- Correction 1: 331c33eb402853b08105cdc65dfdd4a2311050b5, base campaign 21737be5.
- Correction 2 and final: 12721aaf54ae680671596a1ee934e0fa45d30a05, same base.
- Branch: codex/uar-protocol-correction1-a8df.
- Private worktree: /Users/martinbechard/.codex/worktrees/a8df/dev-methodology, clean.

### Verification Evidence

Candidate-focused verification had 23 passing checks, and skill validation, YAML, and diff checks passed. Fresh prompt and source reviews returned NEEDS_CORRECTION. Verifier, integration, generation, documentation, and direct-main delivery were not run because review acceptance failed.

### Related Defect

backlog/defect-backlog/align-coordinator-unset-selection-with-user-action-required-reconciliation.md was separately logged as Ready in commit 8b8f575e. It is related evidence, not a substitute for resolving this blocked item.

### Next Action Owner

The parent Dev Backlog Coordinator must choose a recovery or resumption strategy under canonical task/thread 019f9722-61cb-7190-8a6d-21c5ab319339. Do not create a replacement task.

### Unblock Condition

An authorized bounded recovery addresses every exact review finding, passes new fresh prompt, methodology, and source review plus independent verification, reconciles the campaign base and main with supported mirrors and documentation, then resumes through Blocked to Ready to Starting to Running normally.

## Approval Resolution

### Recorded Question

Do you approve changes to both governed canonical definitions agents/roles/dev-activities/dev-orchestrator.role.yaml and skills/manage-file-work-items/SKILL.md for this item, with regeneration limited to their supported generated mirrors?

### Why User Input Was Required

Only the user may authorize a governed definition mutation with exact canonical-path scope. Repository access and the implementation assignment do not supply exact canonical-scope approval.

### Allowed Dependent Mirror Boundary

If the user approves the canonical definition scope, regeneration is limited to these supported dependent mirrors and no others:

- design/generated/role-definitions.js
- design/generated/skill-definitions.js
- generated/adapters/agent-generation-manifest.json
- generated/adapters/claude/agents/dev-orchestrator.md
- generated/adapters/codex/agents/dev-orchestrator.toml
- generated/adapters/gemini/agents/dev-orchestrator.md
- generated/adapters/junie/agents/dev-orchestrator.md

### Illustrative Options And Consequences Provided

- Approve both: Implement the complete provider-reconciliation plus user-facing protocol and regenerate only the supported mirrors listed above.
- Approve a narrower exact subset: Re-scope and reassess acceptance, with no mutation outside the approved paths.
- Decline or defer: No governed definitions or mirrors change; the item remains deferred or ends without satisfying the requested guidance.

### Prior Unattended Work Boundary

Before approval, all artifact mutation, generation, branch creation, and delivery were prohibited. The exact approved scope now governs later delivery; no scope outside it is authorized.

### Resolution

On 2026-07-25, after requesting and receiving a concrete lifecycle example in canonical task 019f9722-61cb-7190-8a6d-21c5ab319339, the user answered exactly `ok approved`. This authorizes mutation of exactly agents/roles/dev-activities/dev-orchestrator.role.yaml and skills/manage-file-work-items/SKILL.md for this item. Regeneration remains limited to the already-recorded supported mirrors above. Provenance: the answer followed the exact recorded two-path question in the same canonical task.

### Same-Task Resumption Boundary

The answer is recorded once against canonical task/thread 019f9722-61cb-7190-8a6d-21c5ab319339. Resume through Ready to Starting to Running without creating a duplicate task or repeating this question.

### User Action Required Transition Evidence

The Coordinator required this distinct Running to User Action Required provider transition before asking the user. The provider was reconciled as Running at main commit a63fa0618a5573b0a50ece9293d182d3f09277b7, then backlog claim 019f9722-user-action-required-gate was acquired (claim event 21f1fdad-1cc9-4c29-994f-5e2c8800eb4b) to serialize this move and update.

## Summary

Enhance User Action Required guidance so, after advising the Dev Backlog Coordinator, the responsible agent gives the user a plain-language explanation with illustrative examples before pausing work.

## Context

User Action Required is a narrow lifecycle state for a genuine user-owned decision, authority grant, risk acceptance, action, or user-held fact. The guidance must notify the Coordinator and reconcile the provider state first, then help the user understand the exact decision without turning ordinary dependencies or agent-resolvable technical questions into false gates. Resumption must retain the same canonical task context so the user is not asked the same question again.

## Source Evidence

Direct user instruction from watchdog task 019f8b04-225d-7151-b56b-ce7e63d58463: “Let's enhance the guidance for User Action Required. After advising the backlog coordinator, the agent should provide an explanation using examples for the user to consider. Add a backlog item to add this.”

## Requirements

- Preserve Coordinator notification and provider reconciliation before the user-facing explanation.
- State one exact plain-language question and why only the user can answer it.
- Provide illustrative examples or options with their practical consequences when they clarify the decision.
- State the unattended-work boundary and what may continue safely, if anything.
- Preserve and resume through the same canonical task or Thread without repeating an already answered question.
- Keep ordinary dependencies, missing tools, and agent-resolvable technical questions out of User Action Required.

## Acceptance Criteria

1. Guidance requires Coordinator notification and provider-state reconciliation before a user-facing User Action Required request.
2. Each genuine request contains one exact plain-language question and a concrete reason the user owns the answer.
3. Each request includes illustrative examples or viable options and states the practical consequence of each relevant choice.
4. Each request names the unattended-work boundary, including prohibited work and any safe read-only or independent work.
5. Resumption reuses the same canonical task or Thread and does not ask the user to repeat a recorded answer.
6. Tests reject vague, no-example, obscured, fabricated, or repeated requests and distinguish genuine user gates from ordinary dependencies and false gates.

## Dependencies

None.

## Verification

- Run focused lifecycle, provider-reconciliation, and User Action Required guidance tests.
- Add or run cases covering genuine user gates, ordinary dependencies, false gates, examples/options, and same-task resumption.
- Run applicable bundle-content and generated-definition freshness checks.
- Obtain fresh independent review.

## Open Questions

- Which existing lifecycle guidance and evaluator fixtures are the narrowest authoritative surfaces for the user-facing explanation contract?

## Notes

Discovery may identify governed canonical sources; any such source change requires an exact canonical-path approval record before mutation. This creation transaction authorizes backlog capture only and does not authorize delivery.
