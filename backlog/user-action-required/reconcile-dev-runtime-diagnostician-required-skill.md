# Reconcile Dev Runtime Diagnostician Required Skill

Status: User Action Required

Type: Defect

Provider: file

Work Item ID: reconcile-dev-runtime-diagnostician-required-skill

Completion: main-branch

## Summary

Reconcile the Dev Runtime Diagnostician native role with the `structured-explanation` skill required by its evaluation suite, then restore unrestricted validate-only coverage.

## Context

Independent verification of `reconcile-offline-staging-and-strict-result-schema` ran the unrestricted Codex validate-only workflow. Validation stopped because `agents/roles/dev-activities/dev-runtime-diagnostician.role.yaml` does not declare the required `structured-explanation` skill. The selected `dev-orchestrator` workflow and all changed-surface checks passed, so this defect is separate from that delivery.

## Source Evidence

On 2026-08-13, Dev Verifier confirmed this error outside candidate `e31b4ea5c69c7bb256bb40090598d4f7ee29b284`: `ValueError: dev-runtime-diagnostician native agent does not include required skill structured-explanation`. The verifier identified the role definition and unrestricted validate-only command as the runnable correction boundary.

## Requirements

- Determine whether the evaluation requirement or the Dev Runtime Diagnostician role definition is authoritative for `structured-explanation`.
- Reconcile the smallest canonical source and every supported generated effect.
- Preserve governed-definition approval boundaries before changing any named skill or agent definition.
- Restore unrestricted Codex validate-only coverage without weakening the affected evaluation.

## Acceptance Criteria

- The Dev Runtime Diagnostician role and its evaluation agree on the required skill set.
- The unrestricted Codex validate-only workflow passes the previously failing role boundary.
- Applicable generated adapters, bundle checks, independent review, and verification pass.

## Dependencies

None.

## Verification

- Run `python3.11 evals/agent-tests/runner.py --harness codex --validate-only --result-dir <external-temp>`.
- Run focused role, generated-adapter, bundle-content, and definition-approval checks selected during planning.
- Run `git diff --check`.
- Obtain independent review of the authority and generated-effect decision.

## Open Questions

- Does the current evaluation requirement reflect the intended Dev Runtime Diagnostician role contract, or should the evaluation be corrected instead?

## User Action Required

### Question for the User

Do you authorize a separate work item to reconcile the Dev Runtime Diagnostician role and its required `structured-explanation` skill?

### Why User Input Is Required

This defect was independently discovered during another delivery. The user did not request this separate governed definition change, so implementation authority cannot be inferred from the verification finding.

### Options and Tradeoffs

- Approve the work item: move it to the active defect backlog and determine the smallest authoritative correction.
- Defer the work item: keep the current unrestricted validate-only failure visible without changing the role or evaluation.
- Reject the work item: archive the proposal without implementation.

### Resolution

Pending. Record the user's exact answer, date, and canonical conversation provenance before resumption.

### Unattended Work Boundary

Do not modify the Dev Runtime Diagnostician role, its skill declarations, or its evaluation until the user authorizes this separate work. Read-only inventory and duplicate reconciliation may continue.

## Notes

This item is the deliberate excluded-issue disposition from `reconcile-offline-staging-and-strict-result-schema`; it does not block that candidate's main-branch delivery.
