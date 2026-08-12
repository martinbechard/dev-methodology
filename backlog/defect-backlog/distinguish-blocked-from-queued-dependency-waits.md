# Distinguish Blocked From Queued Dependency Waits

Status: Ready

Type: Defect

Provider: file

Work Item ID: distinguish-blocked-from-queued-dependency-waits

Completion: main-branch

## Summary

Reserve Blocked for real impediments and keep healthy predecessor waits in the normal queued lifecycle.

## Source Evidence

On 2026-08-12, the user clarified that a dependent waiting behind a healthy pending, Ready, Starting, or Running predecessor is queued rather than Blocked and must not count toward the Watchdog Blocked threshold.

## Requirements

- Make `skills/coordinate-work-items/SKILL.md` the normative owner of dependency-wait classification and propagation.
- Update `skills/create-work-item-file/SKILL.md` and `skills/manage-work-items-file/SKILL.md` so a healthy unmet predecessor uses the canonical non-active queued state, with dependency and resumption evidence.
- Reserve Blocked for a real preventing condition requiring recovery.
- When a predecessor becomes truly Blocked, propagate that causal Blocked state to affected dependents with the predecessor Work Item ID and blocker reference.
- When the predecessor recovers, reconcile dependents to the correct queued state or Ready when satisfied.
- Keep `agents/roles/dev-activities/dev-backlog-watchdog.role.yaml` a thin read-only mapping that counts only truthfully Blocked records and alerts on stale dependency propagation.
- Preserve `resolve-backlog-blockage` thresholds; correct lifecycle classification supplies their input.
- Add focused creation, management, coordination, Watchdog, and crisis-threshold regressions.

## Acceptance Criteria

- A healthy predecessor wait is not Blocked and does not count toward a crisis threshold.
- A truly Blocked predecessor propagates its causal blocker to affected dependents.
- Recovery removes propagated Blocked state and restores the correct queued or Ready state.
- Provider creation and transition behavior agree with central coordination policy.
- Watchdog guidance remains read-only and detects stale propagation in both directions.
- Fresh independent skill, role, and verification gates pass.

## Dependencies

None.

## Verification

- Validate all changed skill and conceptual role sources.
- Regenerate mechanically required Watchdog adapters and projections.
- Run focused provider lifecycle, dependency scheduling, Watchdog, crisis-threshold, and bundle tests.
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
