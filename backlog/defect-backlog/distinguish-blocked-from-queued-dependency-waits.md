# Distinguish Blocked From Queued Dependency Waits

Status: Ready

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
