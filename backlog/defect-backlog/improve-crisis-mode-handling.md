# Improve Crisis Mode Handling

Status: Ready

Type: Defect

Owner: Unowned

Provider: file

Work Item ID: improve-crisis-mode-handling

Completion: main-branch

## Summary

Make declared backlog crisis recovery an unambiguous, single-Coordinator SOLO procedure that resets live claim state once and performs no claim operations until normal MULTITASK coordination resumes.

## Context

The existing blockage skill says the Coordinator temporarily owns delivery and stops claim operations, while the normal Coordinator role prohibits taking over per-item delivery and project guidance generally requires claims before shared mutation. Crisis activation also depends on a user or Watchdog declaration without requiring the Coordinator to evaluate the crisis criteria during its own queue reconciliation. Existing tests emphasize dispatch-mode switching and do not prove direct sequential delivery, claim-registry reset, or crisis completion.

The original crisis-mode authority explicitly required one Coordinator thread, no concurrent delivery, and no claim operations. A later proposal to retain claims during crisis was declined with the user answer “crisis mode is crisis mode, no coordination.” The current direction confirms that regular SOLO mode must be entered, all active work preserved, the live claim registry reset to an empty slate, and the claim mechanism left unused throughout crisis recovery.

## Source Evidence

On 2026-08-09, the user corrected the recovery plan: “in crisis mode we go to the regular SOLO mode and dont use the claim mechanism at all during this time, and reset the claim repository to an empty slate.” The user then explicitly requested creation of a separate work item for “improve crisis mode handling.” Historical supporting authority is retained in completed Work Item `add-backlog-crisis-mode` and the declined claim-retention Work Item `backlog-crisis-retain-agent-claim`.

## Requirements

- Require Dev Backlog Coordinator to evaluate the automatic crisis criteria after every relevant inventory reconciliation and Blocked transition instead of relying exclusively on a separately formatted Watchdog declaration.
- Treat an equivalent user or Watchdog crisis alert as a declaration even when it does not reproduce one exact phrase, provided the triggering criterion and crisis set are observable.
- Give declared crisis recovery explicit precedence over the Coordinator's normal prohibition on taking over delivery.
- Enter the existing regular SOLO mode before crisis mutation and stop new dispatch.
- Stop or pause every other mutating execution at a safe preservation boundary. Retain its commits, diffs, candidates, worktrees, review evidence, and blocker evidence before resetting live ownership.
- Run the configured claim-helper reset operation exactly once when entering a new crisis epoch, after other mutators are stopped and preservation is verified.
- Require reset to leave the live claim registry empty while preserving claim-event audit history. Correct the helper implementation if focused evidence shows reset discards required history.
- After the entry reset, prohibit every claim status, acquire, extend, deadline extension, heartbeat, release, wait, retry, and additional reset operation while the crisis remains active.
- Establish a project-wide crisis exception so generated resource-coordination guidance does not require claims for the sole Coordinator during an active SOLO crisis.
- Process exactly one crisis item at a time in the existing Coordinator task. Permit direct work-item correction, source implementation, focused testing, commit, delivery, and terminal lifecycle closure within the original request and standing authority.
- Adopt clear preserved work rather than recreating it. Reconcile only an exact overlapping file before continuing.
- Keep an item in the crisis set until it is Completed, Abandoned, Superseded, or explicitly removed by the user. Ready or Starting alone does not resolve a crisis item.
- Add newly Blocked items to the active crisis set and suppress routine capacity, dispatch, inactivity, and repeated blocker alerts.
- Exit only after all crisis-set items have terminal dispositions, no active Blocked item remains, repository state is clean, no other mutation is active, required combined regression has a disposition, and the Watchdog reports the exit conditions satisfied.
- Re-enable regular MULTITASK mode after exit. Normal resource-claim policy resumes only after that transition; crisis-era claim state must not be reconstructed.

## Acceptance Criteria

- Every automatic crisis criterion and user declaration has deterministic entry coverage.
- Entering crisis stops other mutators, preserves their work, selects SOLO mode, and resets the live registry exactly once.
- Claim-event history survives the reset while live claim status is empty.
- No claim operation occurs after reset and before crisis exit.
- The Coordinator can safely modify and commit the current crisis item without a claim.
- Normal no-takeover and claim requirements are explicitly superseded only for the active crisis set and active crisis epoch.
- Repeated crisis observations neither create another crisis task nor reset the registry again.
- The Coordinator completes crisis items sequentially and does not treat Ready or Starting as crisis completion.
- Crisis exit restores MULTITASK mode and normal claim behavior only after all exit gates pass.
- Deterministic tests fail if another agent mutates during crisis, a claim operation occurs, live claims survive entry, audit history is erased, or normal dispatch resumes early.

## Dependencies

None.

## Verification

- Add focused Coordinator and Watchdog scenarios for automatic declaration, user declaration, preservation, one-time reset, no-claim sequential recovery, repeated observation, newly Blocked membership, and exit.
- Extend deterministic simulator coverage from dispatch-mode switching to direct crisis delivery and completion.
- Add resource-claim and helper tests proving empty live registry plus retained event history after reset.
- Add generated AGENTS guidance tests proving the active-crisis exception and ordinary-mode claim requirement coexist without ambiguity.
- Run focused Coordinator, Watchdog, resource-claim helper, bundle-content, skill-validation, role-validation, generated-adapter freshness, and `git diff --check` gates.
- Obtain fresh independent skill, role, prompt-contract, and recovery-safety review.

## Open Questions

- Determine the smallest durable crisis-epoch marker that prevents repeated reset without creating a second coordination registry or task ledger.

## Governed Definition Approval

### Governed Canonical Sources

- skills/resolve-backlog-blockage/SKILL.md
- skills/resource-claim/SKILL.md
- agents/roles/dev-activities/dev-backlog-coordinator.role.yaml
- agents/roles/dev-activities/dev-backlog-watchdog.role.yaml

### Allowed Dependent Artifacts

- skills/resource-claim-helper-command/scripts/claim.py
- scripts/render-agents-technology-skills.py
- scripts/test_resource_claim_helper.py
- scripts/test_bundle_content.py
- AGENTS.md
- evals/agent-tests/dev-backlog-coordinator/scenarios.yaml
- evals/agent-tests/dev-backlog-coordinator/requirements-matrix.md
- evals/agent-tests/dev-backlog-coordinator/fixtures/cases.yaml
- evals/agent-tests/dev-backlog-coordinator/coordination_simulator.py
- evals/agent-tests/dev-backlog-coordinator/test_coordination_simulator.py
- evals/agent-tests/dev-backlog-watchdog/scenarios.yaml
- evals/agent-tests/dev-backlog-watchdog/test_watchdog_simulator.py
- design/agents/backlog-management.md
- design/agents/work-item-dispatching-and-delivery.md
- design/generated/role-definitions.js
- generated/adapters files regenerated from the approved canonical sources
- Directly related non-governed focused tests and generated projections required to keep these definitions coherent

### Approval Resolution

Approved at creation. User wording on 2026-08-09 explicitly requires regular SOLO mode, no claim mechanism during crisis, and a reset of the live claim repository to an empty slate. Historical user authority also explicitly rejected retaining claim coordination during crisis. Approval is limited to the governed canonical paths listed above; an additional governed definition path requires separately recorded scope-specific approval.

## Notes

- The reset targets live ownership, not historical audit evidence.
- This item does not weaken ordinary MULTITASK resource coordination outside a declared crisis epoch.
- This item and `improve-blocked-item-handling` overlap in the Coordinator role and related generated artifacts, so their implementation should be sequenced or deliberately integrated even though neither is a hard prerequisite for the other.
