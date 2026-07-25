# Explain User Action Required Requests With Examples

Status: Starting

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/explain-user-action-required-with-examples.md

Completion: direct-main

## Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Reservation: One launch reserved by the parent Dev Backlog Coordinator.
- Normalized Objective: Explain User Action Required requests with examples.
- Dispatched At: 2026-07-25T02:36:47Z
- Intended Root Role: Dev Orchestrator
- Runtime Thread And Task Id: Not created; the root Dev Orchestrator must accept ownership before a canonical identity is recorded.

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
