# Require Watchdog Escalation And Coordinator Disposition For Blocked Items

Status: Completed

Owner: Unowned

Type: Feature

Provider: file

Provider Reference: backlog/completed-backlog/features/require-watchdog-escalation-and-coordinator-disposition-for-blocked-items.md

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
- Dispatched At: 2026-07-26T21:07:34.874791Z.
- Launch Reservation: one parent-owned launch reservation; active Starting-plus-Running capacity was 1 of 10 at reservation preflight.
- Provider Mutation Claim Evidence: Event-1 exact-file claim reserve-watchdog-escalation-starting-019f9fb0 acquired by dev-backlog-steward; acquisition event 00d2b85d-19d4-4fb1-a06c-ab3b26aa1b29.
- Intended Root Dev Orchestrator: Dev Orchestrator; preserved canonical work-item Thread and root Agent Task 019f9fb0-41c4-7892-a0bb-c641e53d8cea; no replacement task was created.
- Dependency Satisfaction Evidence: backlog/completed-backlog/features/add-dedicated-watchdog-and-stalled-lifecycle.md is present at its required terminal commit 942bac974d87d7b7c7a11ee724b80c0d91c3d0e6; its current blob is 86f1abb7edff36dc26a738e807a4749644a69977, matching that commit.
- Governed Definition Boundary: No governed definition mutation is authorized until direct user direction and exact scope-specific approval evidence pass the repository definition-change check.
- Next Lifecycle Owner: the eventual root Dev Orchestrator must record a distinct Starting -> Running acceptance before any implementation or further repository mutation.

## Historical Running Acceptance

- Lifecycle Transition: Prior Starting -> Running acceptance retained as historical evidence only; it is not the current lifecycle state.
- Canonical Work-item Thread: 019f9fb0-41c4-7892-a0bb-c641e53d8cea.
- Canonical Root Agent Task: 019f9fb0-41c4-7892-a0bb-c641e53d8cea.
- Root Dev Orchestrator Worktree: /Users/martinbechard/.codex/worktrees/dbb1/dev-methodology.
- Branch and Commit State: detached HEAD at 4733705ac28f0a3dae8e6bb577ab9d9836b9605e; no branch has been created.
- Started At: 2026-07-26T18:32:09Z, recorded by this primary-main lifecycle transaction after the root Dev Orchestrator accepted ownership.
- Separate Starting -> Running Claim Evidence: claim starting-to-running-019f9fb0 acquired by dev-backlog-steward for this exact backlog file at 2026-07-26T18:31:57.086198Z; outcome SHARED_CHECKOUT_ACQUIRED; acquisition event 36365d64-d472-492a-ad94-47d9c4ad0bd9.

## Current Running Acceptance

- Lifecycle Transition: Starting -> Running accepted by the root Dev Orchestrator in a distinct transaction after the parent reservation.
- Canonical Work-item Thread: 019f9fb0-41c4-7892-a0bb-c641e53d8cea.
- Canonical Root Agent Task: 019f9fb0-41c4-7892-a0bb-c641e53d8cea.
- Owner: Dev Orchestrator, tied to the preserved canonical work-item Thread and root Agent Task.
- Phase: Ownership accepted; implementation has not started.
- Started At: 2026-07-26T21:10:10.433723Z.
- Root Dev Orchestrator Worktree: /Users/martinbechard/.codex/worktrees/dbb1/dev-methodology.
- Branch and Commit State: detached HEAD at 4733705ac28f0a3dae8e6bb577ab9d9836b9605e; after this Running acceptance is durable, the root Dev Orchestrator will create branch codex/watchdog-blocked-disposition-019f9fb0 from current primary main.
- Parent Reservation Commit: 1e994fd079a96a75b83fc825b727ee0957676975.
- Parent Reservation Claim Evidence: claim reserve-watchdog-escalation-starting-019f9fb0; acquisition event 00d2b85d-19d4-4fb1-a06c-ab3b26aa1b29; release event a9021acd-6652-464b-a1ac-3706c41b1981.
- Approved Governed Definition Scope: agents/roles/dev-activities/dev-backlog-watchdog.role.yaml, agents/roles/dev-activities/dev-backlog-coordinator.role.yaml, and skills/codex-workitem-coordination/SKILL.md, as recorded in the user approval and resumption evidence below.
- Explicit Exclusion: skills/manage-file-work-items/SKILL.md remains excluded from the approved definition scope and may not be changed.
- Separate Starting -> Running Claim Evidence: claim starting-to-running-watchdog-blocked-disposition-019f9fb0 acquired by dev-backlog-steward for this exact backlog file; outcome SHARED_CHECKOUT_ACQUIRED; acquisition event 578dc92c-459d-490b-a8ed-fac8b3deb47f.

## Recorded User Approval And Resumption

User Answer: "Ok approved"

Answer Date And Canonical Provenance: 2026-07-26 in canonical work-item Thread 019f9fb0-41c4-7892-a0bb-c641e53d8cea, after the root Dev Orchestrator clarified and recommended the corrected scope.

Approved Governed Canonical Definition Scope:

- agents/roles/dev-activities/dev-backlog-watchdog.role.yaml
- agents/roles/dev-activities/dev-backlog-coordinator.role.yaml
- skills/codex-workitem-coordination/SKILL.md

Corrected Scope Rationale: These three definitions are the smallest governed surfaces for per-item Blocked reconciliation, watchdog escalation, and evidence-backed Coordinator disposition. The file-provider management contract already provides the required provider-mutation boundary; it was not approved for this change.

Explicit Exclusion: skills/manage-file-work-items/SKILL.md is excluded. It may not be changed unless later evidence supports a separate exact approval request.

Resulting Disposition: Ready.

Resulting Owner: Unowned.

Preserved Canonical Coordination Identity: Parent Coordinator Thread 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a.

Preserved Canonical Work-Item Identity: canonical work-item Thread and root Agent Task 019f9fb0-41c4-7892-a0bb-c641e53d8cea.

Historical Evidence Retained: The prior User Action Required question, Starting reservation, and Running acceptance remain in this record as lifecycle history. The required separate Ready -> Starting parent reservation and Starting -> Running root-Orchestrator acceptance must use the preserved canonical work-item Thread before any implementation or further repository mutation.

## Notes

This item does not authorize mutation of a governed agent or skill definition by itself. Implementation must identify the exact canonical definition paths and record the direct user direction plus exact-path approval evidence required by the repository definition-change check.

## Completion Evidence

- Accepted direct-main commit: `ab23eb7d44f878a866fe6f0286fb6b2c9a731626`.
- Delivered behavior: every Blocked item receives a retained reconciliation result; actionable disposition gaps alert the Coordinator; exhausted correction outcomes require complete evidence; Coordinator decisions remain separate from Steward provider mutation; and a failed extra retry is consumed and cannot repeat.
- Focused verification: Watchdog simulator 19/19, Coordinator simulator 23/23, coordination contracts 36/36, and the affected bundle catalog test 1/1.
- Source checks: all three definition-change checks returned `ALLOWED_APPROVED_DEFINITION_CHANGE`; skill validation, Python compilation, generator freshness, and `git diff --check` passed.
- Publication: the Codex user-level bundle was replaced from the accepted main source. Installed Coordinator, Watchdog, and `codex-workitem-coordination` bytes match the repository sources.
- Claim evidence: none. The user directed temporary single-task delivery without claims.
