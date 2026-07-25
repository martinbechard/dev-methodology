# Explain User Action Required Requests With Examples

Status: Ready

Type: Feature

Owner: Unowned

Claim: None

Provider: file

Provider Reference: backlog/feature-backlog/explain-user-action-required-with-examples.md

Completion: direct-main

## Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Reservation: One launch reserved by the parent Dev Backlog Coordinator.
- Normalized Objective: Explain User Action Required requests with examples.
- Dispatched At: 2026-07-25T02:36:47Z
- Intended Root Role: Dev Orchestrator
- Runtime Thread And Task Id at reservation: Existing canonical work-item Thread 019f9722-61cb-7190-8a6d-21c5ab319339 is retained; no replacement task was created.

## Active Ownership

- Canonical Dev Orchestrator Task/Thread: 019f9722-61cb-7190-8a6d-21c5ab319339
- Canonical Owner: Dev Orchestrator
- Checkout: /Users/martinbechard/dev/dev-methodology
- Branch: main
- Checkout State: Attached to main; not detached.
- Current Phase: Approved User Action Required response recorded; Ready for the parent-owned resumption reservation.
- Transition Evidence: Parent Coordinator 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a provided the direct baton after the prior backlog transaction released. The file provider was reconciled as Starting at main commit 49c78f81a91c3eccab21e50a7413d707b7fe3938, then this serialized backlog claim was acquired as 019f9722-user-action-required-starting-running (claim event 5fa1c816-7d42-4fd0-9724-a13f5bbe6587).

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
