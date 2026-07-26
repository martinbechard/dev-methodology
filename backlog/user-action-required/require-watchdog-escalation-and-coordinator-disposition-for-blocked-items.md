# Require Watchdog Escalation And Coordinator Disposition For Blocked Items

Status: User Action Required

Owner: Dev Orchestrator (canonical work-item Thread 019f9fb0-41c4-7892-a0bb-c641e53d8cea; root Agent Task 019f9fb0-41c4-7892-a0bb-c641e53d8cea)

Type: Feature

Provider: file

Provider Reference: backlog/user-action-required/require-watchdog-escalation-and-coordinator-disposition-for-blocked-items.md

Completion: direct-main

## Summary

Make the Dev Backlog Watchdog account explicitly for every Blocked work item and require the Dev Backlog Coordinator to choose and record an evidence-backed unblocking disposition when correction attempts are exhausted.

## Context

The read-only watchdog previously counted eight Blocked items but reported only that no unblock condition was satisfied. It did not expose the item-by-item reconciliation and missed one item whose recorded dependency had already completed and whose next action belonged to the Coordinator.

Several other Blocked records preserve rejected candidate chains after bounded correction attempts were exhausted. Leaving those records indefinitely Blocked without an explicit Coordinator decision makes recoverable work invisible and allows active capacity to remain unused.

The watchdog must remain read-only. It reports the condition and prompts the Coordinator; the Coordinator owns diagnosis, lifecycle choice, retry authorization within its authority, and user escalation.

## Source Evidence

Direct user request in the watchdog task on 2026-07-26: log an improvement work item so Blocked items cannot be silently suppressed; when correction attempts are exhausted, require the Coordinator to provide an unblocking action, authorize more retries when evidence indicates another bounded attempt is likely to resolve the findings, or convert the item to User Action Required when agents cannot safely resolve the needed decision or authority. The user also directed the watchdog to prompt the Coordinator when the current queue exhibits this condition.

## Requirements

- Require each watchdog cycle to reconcile every Blocked item against its exact blocker, unblock condition, next-action owner, dependencies, candidate and review evidence, canonical task state, Git state, and applicable live claims.
- Include a concise per-item disposition in watchdog evidence even when only actionable conditions are sent to the Coordinator.
- Alert the Coordinator when a Blocked item has a satisfied dependency, an agent-actionable recovery step, exhausted correction attempts without a current disposition, stale or contradictory lifecycle evidence, or an incorrect next-action owner.
- When correction attempts are exhausted, require the Coordinator to choose and record one of these outcomes:
  - provide a concrete evidence-backed unblocking action and owner;
  - authorize a fresh bounded retry plan when the remaining findings are specific and another attempt is reasonably likely to resolve them;
  - convert the item to User Action Required with one exact question, options and tradeoffs, and an unattended-work boundary when a genuine user-owned decision or authority grant prevents further agent action;
  - preserve Blocked with a concrete external or technical dependency and an observable unblock condition when neither retry nor user action is currently appropriate.
- Prohibit indefinite Blocked status whose only next action is vague authorization, reconsideration, or future recovery without an assigned owner and observable trigger.
- Require the Coordinator to preserve canonical task identity, candidate commits, review and verification evidence, claims, and prior attempt history across any resumption.
- Preserve the separation between watchdog advice, Coordinator scheduling and lifecycle decisions, Dev Backlog Steward provider mutation, and Dev Orchestrator delivery ownership.
- Discover the smallest governed agent and skill definition paths required for implementation and obtain exact scope-specific approval before mutating them.

## Acceptance Criteria

- A watchdog fixture with multiple Blocked items emits an evidence-backed reconciliation result for every item rather than only a count.
- A Blocked item whose dependency has completed produces an actionable Coordinator alert naming the evidence and smallest next action.
- An item with exhausted corrections cannot remain silently Blocked: the Coordinator records an unblocking action, a justified fresh bounded retry, a valid User Action Required transition, or a concrete continuing dependency.
- A retry is authorized only with a bounded plan tied to unresolved review findings and evidence that another attempt is likely to help.
- A User Action Required transition contains one exact user-owned question, explanation, options and tradeoffs when known, and the prohibited unattended action.
- A technical or external dependency remains Blocked and is not incorrectly converted to User Action Required.
- No watchdog path mutates provider records, tasks, claims, branches, or worktrees.
- Focused tests prevent regression to count-only Blocked reporting or indefinite exhausted-correction suppression.

## Dependencies

- backlog/feature-backlog/add-dedicated-watchdog-and-stalled-lifecycle.md

## Verification

- Add focused watchdog simulations for satisfied dependencies, exhausted retries, justified additional retries, User Action Required conversion, and continuing technical blockers.
- Add Coordinator contract tests proving that each exhausted-correction alert receives one explicit disposition.
- Validate affected work-item lifecycle and generated Coordinator snapshot behavior.
- Run targeted skill, role, and generated-output freshness checks for each approved governed source that changes.
- Run git diff --check.
- Obtain fresh independent methodology and prompt-contract review.

## Open Questions

- Which durable field should distinguish a newly authorized bounded recovery from another attempt in the exhausted correction loop?
- What evidence threshold should the Coordinator use to conclude that another bounded retry is reasonably likely to resolve the remaining findings?
- Should healthy-cycle watchdog output list every Blocked item individually or provide a stable digest with item-level details available in retained evidence?

## Current Starting Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a.
- Lifecycle Reservation: Ready -> Starting recorded by the parent Dev Backlog Coordinator through its Dev Backlog Steward child.
- Normalized Objective: Require per-item watchdog escalation and evidence-backed Coordinator disposition for Blocked work.
- Dispatched At: 2026-07-26T18:28:15.761081Z.
- Launch Reservation: one parent-owned launch reservation; active Starting-plus-Running capacity was 0 of 10 at reservation preflight.
- Intended Root Dev Orchestrator: Dev Orchestrator; runtime task identity pending creation.
- Dependency Satisfaction Evidence: backlog/completed-backlog/features/add-dedicated-watchdog-and-stalled-lifecycle.md is present at its required terminal commit 942bac974d87d7b7c7a11ee724b80c0d91c3d0e6; its current blob is 86f1abb7edff36dc26a738e807a4749644a69977, matching that commit.
- Governed Definition Boundary: No governed definition mutation is authorized until direct user direction and exact scope-specific approval evidence pass the repository definition-change check.
- Next Lifecycle Owner: the eventual root Dev Orchestrator must record a distinct Starting -> Running acceptance before any implementation or further repository mutation.

## Current Running Acceptance

- Lifecycle Transition: Starting -> Running accepted by the root Dev Orchestrator through its Dev Backlog Steward child.
- Canonical Work-item Thread: 019f9fb0-41c4-7892-a0bb-c641e53d8cea.
- Canonical Root Agent Task: 019f9fb0-41c4-7892-a0bb-c641e53d8cea.
- Root Dev Orchestrator Worktree: /Users/martinbechard/.codex/worktrees/dbb1/dev-methodology.
- Branch and Commit State: detached HEAD at 4733705ac28f0a3dae8e6bb577ab9d9836b9605e; no branch has been created.
- Started At: 2026-07-26T18:32:09Z, recorded by this primary-main lifecycle transaction after the root Dev Orchestrator accepted ownership.
- Separate Starting -> Running Claim Evidence: claim starting-to-running-019f9fb0 acquired by dev-backlog-steward for this exact backlog file at 2026-07-26T18:31:57.086198Z; outcome SHARED_CHECKOUT_ACQUIRED; acquisition event 36365d64-d472-492a-ad94-47d9c4ad0bd9.

## Definition Change Approval Needed

Question: "Do you approve changing exactly these four governed canonical definitions for this item: agents/roles/dev-activities/dev-backlog-watchdog.role.yaml; agents/roles/dev-activities/dev-backlog-coordinator.role.yaml; skills/codex-workitem-coordination/SKILL.md; and skills/manage-file-work-items/SKILL.md?"

Why Input Is Required: Repository policy requires direct exact-path approval, and read-only tracing shows these are the smallest definitions needed for per-item Blocked reconciliation, watchdog escalation, Coordinator disposition, and durable file-provider evidence.

Options And Tradeoffs:

- Approve permits only these four definitions plus their supported generated mirrors and directly dependent focused tests/docs.
- Narrow requires revising the implementation plan and rechecking scope.
- Defer leaves the item in User Action Required.
- Decline ends this implementation direction without governed changes.

Unattended-Work Boundary: No governed definition, supported mirror, implementation, test, or documentation mutation will occur until the answer is durably recorded and this same canonical task resumes through User Action Required -> Ready -> Starting -> Running.

Discovered Dependent Artifacts, Non-Governed:

- Supported generated/adapters mirrors for the two roles and two skills.
- design/generated/role-definitions.js.
- design/generated/skill-definitions.js.
- design/orchestrated-development-lifecycle.html.
- scripts/test_codex_workitem_coordination.py.
- scripts/test_bundle_content.py.
- evals/agent-tests/dev-backlog-watchdog/{scenarios.yaml,requirements-matrix.md,fixtures/cases.yaml,watchdog_simulator.py,test_watchdog_simulator.py}.
- evals/agent-tests/dev-backlog-coordinator/{scenarios.yaml,requirements-matrix.md,fixtures/cases.yaml,coordination_simulator.py,test_coordination_simulator.py}.

Excluded Governed Definitions: dev-orchestrator and dev-backlog-steward roles already enforce blocker handoff and authority separation, so they are not in scope.

## Notes

This item does not authorize mutation of a governed agent or skill definition by itself. Implementation must identify the exact canonical definition paths and record the direct user direction plus exact-path approval evidence required by the repository definition-change check.
