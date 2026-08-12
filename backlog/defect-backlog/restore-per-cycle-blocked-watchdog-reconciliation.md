# Restore Per-Cycle Blocked Watchdog Reconciliation

Status: Starting

Type: Defect

Provider: file

Work Item ID: restore-per-cycle-blocked-watchdog-reconciliation

Completion: main-branch

## Summary

Restore the Dev Backlog Watchdog contract so every scheduled cycle inventories and reconciles every current Blocked work item, verifies that every observed canonical task title accurately reflects authoritative lifecycle and current Running phase, and notifies the Coordinator only when current evidence requires a decision.

## Context

The completed predecessor require-watchdog-escalation-and-coordinator-disposition-for-blocked-items required per-cycle reconciliation of every Blocked item and focused regression coverage. Current sources retain most of that behavior, including a complete Blocked inventory requirement in skills/coordinate-work-items/SKILL.md and a blocked-inventory-reconciliation evaluation scenario.

The contract is now internally inconsistent. skills/coordinate-work-items/SKILL.md and agents/roles/dev-activities/dev-backlog-watchdog.role.yaml also say to reconcile a Blocked item only after an observed change or missing disposition. That event-only gate can prevent the Watchdog from reading enough current provider evidence to discover unattended agent-actionable recovery, stale ownership, or preservation claims that contradict Git or runtime state. Repeated quiet heartbeat cycles can therefore suppress a recoverable Blocked item until a user manually notices it.

The correction must remain read-only at runtime and avoid duplicating Blocked policy across dispatcher, provider-manager, claim, and design surfaces. The portable coordination skill owns the policy; role and runtime mappings remain thin references to that policy.

## Source Evidence

On 2026-08-12, after observing a Blocked item whose verifier-placement problem and missing preserved branch were not surfaced automatically, the user asked how the Watchdog procedure could resolve such blockages automatically. The user then asked for the proposed changes to be organized by skill file, challenged the proposal for DRY, YAGNI, and skill-writing quality, and directed: “ok create the item.”

Later on 2026-08-12, after observing simultaneous Waiting for Help, Verifying, Completed, and Done labels that contradicted provider or runtime state, the user explicitly directed: “Fix these damn titles, and ensure they stay clean in the future accurately showing their state. Make sure that's in the watchdog skill in the future” and “make sure you record this in your skill.” This authorizes the exact title-reconciliation additions below.

Repository evidence on 2026-08-12 shows that the completed predecessor already promised per-cycle Blocked reconciliation, while current skills/coordinate-work-items/SKILL.md and agents/roles/dev-activities/dev-backlog-watchdog.role.yaml retain an event-only reconciliation clause that conflicts with that promise.

## Requirements

- Make skills/coordinate-work-items/SKILL.md the single normative owner of the per-cycle Blocked reconciliation policy.
- Require every scheduled Watchdog cycle to obtain the current Blocked inventory and reconcile each item sufficiently to classify it as active recovery, a genuine unchanged user or external wait, or unattended agent-actionable recovery.
- Alert the Coordinator when current evidence shows agent-owned recovery without an active owner, an invalid or missing next-action owner or trigger, a satisfied dependency or unblock condition, exhausted correction attempts without a current disposition, or preservation evidence contradicted by Git or runtime state.
- Suppress repeat alerts only while acknowledged recovery is actively owned or an unchanged concrete user or external trigger remains unsatisfied.
- Require every scheduled Watchdog cycle to compare each observed canonical runtime task title with the exact title derived from authoritative provider lifecycle and current material Running phase.
- Alert the Coordinator when a canonical task title is stale, noncanonical, or contradicts lifecycle or phase. Do not infer lifecycle from the title and do not let title drift change capacity, ownership, or delivery evidence.
- Enforce the existing title vocabulary: Completed maps to Done —, Blocked maps to Blocked —, and Waiting for Help — is valid only for a Running task currently awaiting technical help. A bounded noncanonical verifier task that finishes must not remain visibly titled Verifying.
- Keep agents/roles/dev-activities/dev-backlog-watchdog.role.yaml and the canonical Watchdog runtime prompt in skills/coordinate-codex-tasks/SKILL.md as thin mappings to the owning policy. Remove or replace conflicting event-only wording instead of restating the full classification rules.
- Preserve the Watchdog's read-only authority boundary. It reports the Work Item ID and smallest Coordinator action; it does not mutate lifecycle, claims, tasks, branches, worktrees, provider records, or shared resources.
- Add focused regression coverage for unattended agent-owned recovery, acknowledged active recovery, and provider preservation evidence that contradicts Git or runtime state.
- Regenerate Dev Backlog Watchdog adapters from the conceptual role source through the owning generator; do not edit generated adapters by hand.
- Do not change .agents/skills/backlog-dispatcher/SKILL.md, skills/manage-work-items-file/SKILL.md, skills/resource-claim/SKILL.md, or design/orchestrated-development-lifecycle.html unless implementation evidence proves a direct dependency and the work item is explicitly reconciled before mutation.
- Do not introduce a generalized alert-acknowledgment subsystem, new lifecycle state, new provider field, or broad monitoring framework.

## Acceptance Criteria

- A cycle with a Blocked item whose recovery is agent-actionable and unowned emits one Coordinator alert even when no external unblock event occurred since the prior cycle.
- A cycle with acknowledged, actively owned recovery retains reconciliation evidence without emitting a duplicate alert.
- A cycle where the provider says a candidate branch or worktree is preserved but Git or runtime proves it absent emits one alert naming the Work Item ID and the smallest reconciliation action.
- A cycle with an unchanged concrete user or external dependency remains quiet after retaining its current reconciliation result.
- A Blocked item titled Waiting for Help emits one title-reconciliation alert without changing provider lifecycle.
- A Completed item titled Completed instead of Done emits one title-reconciliation alert even when the task is idle, terminal, or archived.
- A finished bounded verifier task is no longer presented as actively Verifying.
- The portable policy has one normative classification rule; role and runtime prompt mappings reference it without duplicating its decision table.
- Existing healthy-cycle, singular-alert, no-forbidden-mutation, and complete Blocked-inventory behavior remains intact.
- Generated Dev Backlog Watchdog adapters are fresh and derived from the conceptual role source.
- Focused tests prevent regression to event-only Blocked inspection.

## Dependencies

None.

## Verification

- Run the focused Dev Backlog Watchdog simulator tests, including new cases for unattended recovery, active recovery, and preservation contradiction.
- Validate evals/agent-tests/dev-backlog-watchdog/scenarios.yaml, fixtures/cases.yaml, and requirements-matrix.md against the suite contract.
- Run focused structural assertions in scripts/test_bundle_content.py for the owning policy, thin mappings, and generated adapter freshness.
- Run the owning role/adapter generator and verify exact generated-output freshness for Dev Backlog Watchdog.
- Validate each changed skill and conceptual role source with the repository's targeted contract checks.
- Run git diff --check.
- Obtain fresh independent skill-writing and prompt-contract review focused on DRY, YAGNI, authority boundaries, and alert semantics.

## Open Questions

- Which existing retained reconciliation structure should record the active-recovery acknowledgment without adding a new provider field or subsystem?

## Governed Definition Approval

### Governed Canonical Sources

- skills/coordinate-work-items/SKILL.md
- skills/coordinate-codex-tasks/SKILL.md
- agents/roles/dev-activities/dev-backlog-watchdog.role.yaml

### Allowed Dependent Artifacts

- evals/agent-tests/dev-backlog-watchdog/scenarios.yaml
- evals/agent-tests/dev-backlog-watchdog/fixtures/cases.yaml
- evals/agent-tests/dev-backlog-watchdog/watchdog_simulator.py
- evals/agent-tests/dev-backlog-watchdog/test_watchdog_simulator.py
- evals/agent-tests/dev-backlog-watchdog/requirements-matrix.md
- scripts/test_bundle_content.py
- generated/adapters/codex/agents/dev-backlog-watchdog.toml
- generated/adapters/claude/agents/dev-backlog-watchdog.md
- generated/adapters/gemini/agents/dev-backlog-watchdog.md
- generated/adapters/junie/agents/dev-backlog-watchdog.md
- design/generated/skill-definitions.js
- design/generated/role-definitions.js
- generated/adapters/agent-generation-manifest.json

### Approval Resolution

Approved at creation and expanded by later answer. On 2026-08-12, after the exact source and test responsibilities were organized and narrowed for DRY, YAGNI, and skill-writing quality, the user directed: “ok create the item.” Later that day, the user explicitly required accurate future title enforcement in the Watchdog skill. Approval is limited to the exact governed canonical sources and allowed dependent artifacts listed above. Any additional governed definition requires separate reconciliation and scope-specific approval.

## Notes

- This item is a regression correction to the completed predecessor, not a second feature for the same outcome.
- The intended test additions are three focused behavioral cases, not a broad evaluation-suite expansion.
- Coordinator recovery policy remains owned by skills/coordinate-work-items/SKILL.md; this defect does not move provider mutation or dispatcher authority into the Watchdog.

## Delivered Work Lifecycle Reconciliation

- Reconciled At: 2026-08-12.
- Preserved Main Commit: `ba00c950364740f51a250ef53eb7ba4049369aed` contains the complete 16-path user-authorized source, role, generated-adapter, projection, and focused-regression change set.
- Preserved Reported Gates: The originating execution reports fresh independent acceptance and verification. Preserve those results for adoption; do not redispatch or reimplement the requested behavior.
- Lifecycle Anomaly: The provider remained Ready while the work was implemented, reviewed, verified, and committed directly to main. It contains no durable Starting or Running acceptance, canonical root Dev Orchestrator identity, selected Commit READY result, or terminal provider transaction.
- Current Disposition: Ready -> Blocked; Owner Unowned. Direct Ready -> Completed is prohibited because Git delivery and Watchdog assertions do not substitute for the missing lifecycle and Commit gates.
- Confirmed Blocker: Finish-lane adoption must reconcile the already-delivered main commit through one authorized root Dev Orchestrator execution without changing its accepted content or redispatching implementation.
- Blocker Owner: Dev Backlog Coordinator.
- Unblock Condition: After `align-orchestrated-development-lifecycle-with-documentation-design-system` finishes its active terminal provider transaction and cleanup, reserve exactly one lifecycle-adoption execution. That execution must record Starting -> Running, verify `ba00c950` and reported gates against current main, obtain any missing fresh terminal gate, apply `deliver-work-item-main-branch` to READY without replaying content, then close and archive this provider item.
- Overlap Constraint: `skills/coordinate-codex-tasks/SKILL.md` is also required by Ready item `prefer-durable-recovery-evidence-over-codex-task-identity`. Do not dispatch that item until this adoption closes or explicitly releases the delivered path ownership.
- Preservation Boundary: Do not revert, amend, cherry-pick, regenerate, or rewrite `ba00c950` merely to repair lifecycle order. Preserve unrelated lifecycle-alignment provider changes and every unrelated worktree or branch.
- Transition Claim: `block-watchdog-delivery-lifecycle-adoption-019ff2c3`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `e9f44706-81ba-4a2d-9aa7-fcd58ef8d328`.

## Blocked Recovery

- Reconciled At: 2026-08-12T22:09:48Z.
- Recovery Decision: The lifecycle-alignment finish lane completed its provider transaction, worktree and branch cleanup, and successor-task archival. The recorded unblock condition is satisfied.
- Ready Scope: Reserve exactly one root Dev Orchestrator execution to adopt the already-delivered `ba00c950364740f51a250ef53eb7ba4049369aed` result. Do not replay implementation or change its accepted content.
- Required Outcome: Record Starting -> Running, verify the preserved commit and reported gates against current main, obtain any missing fresh terminal gate, apply `deliver-work-item-main-branch` to a truthful READY result without replaying content, and close and archive this provider item.
- Recovery Claim: `ready-watchdog-delivery-lifecycle-adoption-019ff2c3`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `2c413e21-38f7-4a8e-9bf3-c1c06dd60ff7`.

## Starting Handoff Evidence

- Reserved At: 2026-08-12T22:10:15Z.
- Parent Runtime Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Normalized Objective: Adopt the already-delivered Watchdog reconciliation result at `ba00c950364740f51a250ef53eb7ba4049369aed` through the missing lifecycle, independent terminal-gate, selected Commit, provider-closeout, and external-cleanup sequence without replaying or changing accepted implementation content.
- Intended Root Role: Dev Orchestrator.
- Baseline: `f3b6eff5e97b3120b693adaf095448fd4ca48392` on primary `main`.
- Dispatch Reservation: Exactly one new canonical root execution; runtime identity pending caller-owned creation. No prior canonical execution exists for this adoption boundary.
- Launch State: Authorized and pending root Backlog Dispatcher creation result; successful creation does not imply Running.
- Last Contact: 2026-08-12T22:10:15Z.
- Next Reconciliation: Reconcile the exact create result immediately; the new root execution must record Starting -> Running before any adoption mutation.
- Transition Claim: `start-watchdog-delivery-lifecycle-adoption-019ff2c3`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `24ae02ec-a4c5-4a81-93e0-2f8e6225e45a`.
