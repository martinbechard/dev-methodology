# Distinguish Blocked From Queued Dependency Waits

Status: Blocked

Type: Defect

Provider: file

Work Item ID: distinguish-blocked-from-queued-dependency-waits

Completion: main-branch

## Summary

Reserve stored Blocked for the first real impediment in an ordered series and derive every downstream child's effective state without lifecycle churn.

## Source Evidence

On 2026-08-12, the user clarified that a dependent waiting behind a healthy pending, Ready, Starting, or Running predecessor is queued rather than Blocked and must not count toward the Watchdog Blocked threshold.

## Requirements

- Make `skills/coordinate-work-items/SKILL.md` the normative owner of ordered-series scheduling and derived dependency state.
- Require dependent Work Items to be children of one ordered series folder whose `index.md` defines their execution order.
- Store `Blocked` only on the first child with a genuine preventing condition requiring recovery.
- Do not rewrite later child records merely to copy Blocked or Holding. Derive each later child's effective Blocked state from the first stored Blocked predecessor, or effective Holding while any earlier predecessor is healthy and nonterminal.
- When predecessors complete, derive the next child's schedulability from its own stored lifecycle. Do not mutate that child merely to clear a derived state.
- Reject new cross-folder Work Item dependencies. Migrate related dependent items into one ordered series before dispatch rather than silently deriving across folders.
- Permit a completed child to move to its canonical archive while its series index retains the ordered link and stable Work Item identity. This is not a cross-folder active dependency exception.
- Treat an external prerequisite as a condition, not a Work Item dependency edge; classify a real preventing condition according to ordinary lifecycle policy.
- Update `skills/create-work-item-file/SKILL.md` and `skills/manage-work-items-file/SKILL.md` to create, validate, inventory, and schedule this stored-versus-effective model without downstream lifecycle writes.
- Keep `agents/roles/dev-activities/dev-backlog-watchdog.role.yaml` a thin read-only mapping that counts the stored first Blocked item once, derives affected downstream items for reporting, and alerts on stale order or stored-state contradictions.
- Preserve `resolve-backlog-blockage` thresholds; correct lifecycle classification supplies their input.
- Add focused creation, management, coordination, Watchdog, and crisis-threshold regressions.

## Acceptance Criteria

- A healthy predecessor wait is effectively Holding, without rewriting the dependent child's stored lifecycle, and does not count toward a crisis threshold.
- Exactly the first genuinely impeded child stores Blocked and counts once; later children derive effective Blocked with the causal Work Item reference.
- Recovery changes only the genuinely impeded child's stored lifecycle; downstream effective states recalculate from order and stored lifecycle.
- The next child becomes schedulable only after every earlier required child completes and its own stored lifecycle is dispatchable.
- New cross-folder Work Item dependencies are rejected with a required same-series migration; archived completed children remain valid ordered predecessors through the series index.
- Provider creation, management, inventory, capacity, scheduling, Watchdog reporting, and crisis-threshold behavior agree on stored versus effective state.
- Watchdog guidance remains read-only and detects order, stored-state, and derived-state contradictions.
- Fresh independent skill, role, and verification gates pass.

## Dependencies

None.

## Verification

- Validate all changed skill and conceptual role sources.
- Regenerate mechanically required Watchdog adapters and projections.
- Run focused provider lifecycle, series-order, derived-state scheduling, cross-folder rejection, Watchdog, crisis-threshold, and bundle tests.
- Run Git diff whitespace validation.

## Governed Definition Approval

### Governed Canonical Sources

- `skills/coordinate-work-items/SKILL.md`
- `skills/create-work-item-file/SKILL.md`
- `skills/manage-work-items-file/SKILL.md`
- `agents/roles/dev-activities/dev-backlog-watchdog.role.yaml`

### Allowed Dependent Artifacts

- Mechanically generated Dev Backlog Watchdog adapters and projections.
- Focused tests proven to validate the approved lifecycle, dependency, Watchdog, and crisis-threshold rules.

### Approval Resolution

Approved at creation by the user's explicit 2026-08-12 lifecycle-policy clarification. No other governed skill or Agent definition is authorized.

## Notes

- This policy item is Ready but must not be dispatched while the current serialized crisis execution remains Blocked or while its protected-path recovery is unresolved.
- Future Ideas remain excluded from ordinary provider inventory and threshold calculations.

## Current Series Audit

- `backlog/feature-backlog/inspect-ai-evaluation-adoption/` already contains all eight active dependent children and an ordered `index.md`; no path migration is required. Its seven downstream children retain stored Ready and derive effective Holding behind the first Ready child.
- `backlog/feature-backlog/html-documentation-review-and-design-alignment/` already groups the active alignment children. Completed text-review and alignment predecessors remain linked through the series index at their canonical archive paths; no active cross-folder migration is required.
- No active standalone file-provider Work Item declares a cross-folder Work Item dependency. No exception is currently required.

## Starting Handoff Evidence

- Reserved At: 2026-08-13T00:39:12Z.
- Parent Runtime Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Intended Root Role: Dev Orchestrator.
- Baseline: `16b1267d9208e8e1b3d21be50f7372abd0b8aa74` on primary `main`.
- Dispatch Reservation: Exactly one new canonical collaboration execution; identity pending caller-owned creation.
- Launch State: Authorized under restored MULTITASK mode; successful creation does not imply Running.
- Transition Claim: `start-folder-derived-dependency-policy-019ff2c3`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `fa8af8ea-a2bd-49a2-ae75-e5b6ebee2e31`.
- Next Reconciliation: Reconcile the exact creation result; the Dev Orchestrator records Starting -> Running before mutation.

## Running Acceptance Evidence

- Accepted At: 2026-08-13T00:40:57Z.
- Owner: Dev Orchestrator `/root/distinguish_blocked_waits`.
- Canonical Conversation: Runtime parent Task `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Root Agent Task: `/root/distinguish_blocked_waits`.
- Branch: `main`.
- Worktree: `/Users/martinbechard/dev/dev-methodology`.
- Phase: implementation planning and technical review.
- Accepted Execution Evidence: The authorized canonical collaboration execution resolved reservation commit `cba1acefc37402689033229787323ecccced6809` and acquired Work Item update claim `distinguish-blocked-waits-running-update` with outcome `SHARED_CHECKOUT_ACQUIRED` and event `f82bbefd-dc96-4d5c-af8d-58eca1ce1601`.
- Next Action: Dev Coder creates the bounded implementation and TDD plan and the required authoritative hierarchy plan before source mutation.

## Plan Workspace Blocker

- Recorded At: 2026-08-13T00:49:12Z.
- Exact Blocker: The first `create_hierarchy_plan` call supplied `/Users/martinbechard/.codex/visualizations/2026/08/11/019ff2c3-1710-7aa1-89c4-9d6066f51fe4`, which the configured provider rejected as outside its workspace roots. No plan or source mutation occurred.
- Blocker Owner: Dev Backlog Coordinator.
- Recovery Finding: `manage-complex-development-plan` makes `output_folder` optional and requires the provider default when a custom folder is inappropriate. Provider reconfiguration is unnecessary.
- Unblock Condition: Retry the same create operation once with `output_folder` omitted, then use and verify the provider-returned JSON path and sibling HTML.
- Preserved Execution: `/root/distinguish_blocked_waits`; safe to resume without replacement.
- Transition Claim: `block-folder-dependency-plan-path-019ff2c3`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `6a55d2e4-257d-4493-b454-ce9086f7910f`.

## Plan Workspace Recovery

- Reconciled At: 2026-08-13T00:49:36Z.
- Decision: The rejected custom visualization folder was optional dispatch data, not a required provider configuration. The configured default output folder is the supported recovery route.
- Ready Action: Resume the same execution and retry `create_hierarchy_plan` exactly once with `output_folder` omitted. Accept only the returned authoritative JSON path after verifying its JSON and sibling HTML.
- Recovery Claim: `ready-folder-dependency-plan-default-019ff2c3`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `fde79ab0-7b47-4e6e-b13d-fdfb97d5db4d`.

## Same-Execution Plan Restart

- Reserved At: 2026-08-13T00:49:55Z.
- Transition: Ready -> Starting.
- Canonical Execution: `/root/distinguish_blocked_waits`.
- Resume Delta: Retry the required hierarchy-plan creation once with the optional `output_folder` omitted; use the configured provider default and verify the returned JSON and HTML artifacts.
- Transition Claim: `restart-folder-dependency-plan-default-019ff2c3`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `e7f5f499-01ad-4c33-aed5-6468d32079de`.
- Acceptance Boundary: The same Dev Orchestrator records Starting -> Running before the retry or source mutation.

## Generated Projection Blocker

- Recorded At: 2026-08-13T01:19:17Z.
- Exact Blocker: `design/generated/skill-definitions.js` contains pre-existing generated drift from `coordinate-codex-tasks` owned by Work Item `document-external-terminal-cleanup`. This item must later regenerate the same whole projection from its three authorized skill changes and cannot safely split or absorb the unrelated source ownership by generated hunk.
- Blocker Owner: Dev Backlog Coordinator.
- Recovery Decision: Complete `document-external-terminal-cleanup` first so it integrates the deferred projection against its authoritative sources. Do not authorize a generated-hunk handoff.
- Unblock Condition: `document-external-terminal-cleanup` reaches Completed on main with fresh generated-output verification and a clean projection baseline. Then resume `/root/distinguish_blocked_waits` through Blocked -> Ready -> Starting and regenerate from current authoritative sources.
- Preserved Evidence: Authoritative JSON/HTML hierarchy plan exists at the repository root; no implementation candidate exists and no source mutation began.
- Transition Claim: `block-folder-policy-generated-projection-019ff2c3`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `c1370c23-40e1-4525-b2fb-245342e61de3`.

## Same-Execution Running Acceptance

- Accepted At: 2026-08-13T00:50:34Z.
- Owner: Dev Orchestrator `/root/distinguish_blocked_waits`.
- Canonical Conversation: Runtime parent Task `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Root Agent Task: `/root/distinguish_blocked_waits`.
- Branch: `main`.
- Worktree: `/Users/martinbechard/dev/dev-methodology`.
- Phase: hierarchy-plan recovery and technical review.
- Accepted Execution Evidence: The same canonical execution resolved recovery commits `4fec0d60b90d400bfe086ba3577ab2cbcbb64d50`, `b5ffef747e1d62d67b555f89aeab343e279517e2`, and `951aa60b4b7aa837526f70fffeca94a32f58b9f0`, then acquired Work Item update claim `distinguish-blocked-waits-resume-running` with outcome `SHARED_CHECKOUT_ACQUIRED` and event `ab287ef3-5102-4b02-a2eb-30c8baf982b9`.
- Next Action: The existing Dev Coder retries `create_hierarchy_plan` exactly once with `output_folder` omitted and verifies only the provider-returned JSON and sibling HTML.
