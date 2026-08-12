# Restore Per-Cycle Blocked Watchdog Reconciliation

Status: Ready

Type: Defect

Provider: file

Work Item ID: restore-per-cycle-blocked-watchdog-reconciliation

Completion: main-branch

## Summary

Restore the Dev Backlog Watchdog contract so every scheduled cycle inventories and reconciles every current Blocked work item while notifying the Coordinator only when current evidence requires a decision.

## Context

The completed predecessor require-watchdog-escalation-and-coordinator-disposition-for-blocked-items required per-cycle reconciliation of every Blocked item and focused regression coverage. Current sources retain most of that behavior, including a complete Blocked inventory requirement in skills/coordinate-work-items/SKILL.md and a blocked-inventory-reconciliation evaluation scenario.

The contract is now internally inconsistent. skills/coordinate-work-items/SKILL.md and agents/roles/dev-activities/dev-backlog-watchdog.role.yaml also say to reconcile a Blocked item only after an observed change or missing disposition. That event-only gate can prevent the Watchdog from reading enough current provider evidence to discover unattended agent-actionable recovery, stale ownership, or preservation claims that contradict Git or runtime state. Repeated quiet heartbeat cycles can therefore suppress a recoverable Blocked item until a user manually notices it.

The correction must remain read-only at runtime and avoid duplicating Blocked policy across dispatcher, provider-manager, claim, and design surfaces. The portable coordination skill owns the policy; role and runtime mappings remain thin references to that policy.

## Source Evidence

On 2026-08-12, after observing a Blocked item whose verifier-placement problem and missing preserved branch were not surfaced automatically, the user asked how the Watchdog procedure could resolve such blockages automatically. The user then asked for the proposed changes to be organized by skill file, challenged the proposal for DRY, YAGNI, and skill-writing quality, and directed: “ok create the item.”

Repository evidence on 2026-08-12 shows that the completed predecessor already promised per-cycle Blocked reconciliation, while current skills/coordinate-work-items/SKILL.md and agents/roles/dev-activities/dev-backlog-watchdog.role.yaml retain an event-only reconciliation clause that conflicts with that promise.

## Requirements

- Make skills/coordinate-work-items/SKILL.md the single normative owner of the per-cycle Blocked reconciliation policy.
- Require every scheduled Watchdog cycle to obtain the current Blocked inventory and reconcile each item sufficiently to classify it as active recovery, a genuine unchanged user or external wait, or unattended agent-actionable recovery.
- Alert the Coordinator when current evidence shows agent-owned recovery without an active owner, an invalid or missing next-action owner or trigger, a satisfied dependency or unblock condition, exhausted correction attempts without a current disposition, or preservation evidence contradicted by Git or runtime state.
- Suppress repeat alerts only while acknowledged recovery is actively owned or an unchanged concrete user or external trigger remains unsatisfied.
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

### Approval Resolution

Approved at creation. On 2026-08-12, after the exact source and test responsibilities were organized and narrowed for DRY, YAGNI, and skill-writing quality, the user directed: “ok create the item.” Approval is limited to the exact governed canonical sources and allowed dependent artifacts listed above. Any additional governed definition requires separate reconciliation and scope-specific approval.

## Notes

- This item is a regression correction to the completed predecessor, not a second feature for the same outcome.
- The intended test additions are three focused behavioral cases, not a broad evaluation-suite expansion.
- Coordinator recovery policy remains owned by skills/coordinate-work-items/SKILL.md; this defect does not move provider mutation or dispatcher authority into the Watchdog.
