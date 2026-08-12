# Reconcile Project Configurator Receipt-Integrity Candidate

Status: Ready

Type: Defect

Provider: file

Work Item ID: reconcile-project-configurator-receipt-integrity-candidate

Completion: main-branch

## Summary

Reassess the abandoned Project Configurator receipt-integrity corrections against current main and retain only missing protections against mixed or contaminated inspection evidence.

## Context

The branch codex/baton-10-project-configurator-verdict at ce6e0a49313a949e50e168e1796e85bf8d5d0d9c contains Project Configurator corrections that prove inspection receipts, bind target evidence, reject mixed read roots, close receipt gaps, and reject contaminated traces. Its history also contains the separately reviewed offline-runner commit, which is outside this work item's scope.

A fresh non-mutating merge now conflicts across the Project Configurator Judge, supervisor, fixtures, scenarios, suite contract, runner, and tests. Current main has materially changed those surfaces since the earlier mergeability review.

## Source Evidence

On 2026-08-12, the user approved preserving the Project Configurator receipt-integrity outcome before deleting legacy worktrees. Fresh integration reconciliation found broad content conflicts, so direct merging is no longer safe.

## Requirements

- Compare the five Project Configurator-specific branch commits with current main: 37689f674ccb68e74ff2c0879a6511f405cd5737, 3949bb9e24ab5c98b798517f42b7a256448f7282, a79ce66fa0a396e6d55f4e4763f14f4d8ed93d86, 06f49f98473779bc373930ae0294b08db6fc7087, and ce6e0a49313a949e50e168e1796e85bf8d5d0d9c.
- Classify each inspection-receipt and contamination protection as already covered, obsolete, or a reproducible current-main gap.
- Implement only confirmed gaps using the current Judge, supervisor, runner, fixture, and contract structure.
- Keep the offline dependency and strict-schema candidate outside this work item.
- Do not replay the branch or restore obsolete evaluation contracts.

## Acceptance Criteria

- Every Project Configurator-specific candidate behavior has a current-main disposition.
- Confirmed receipt-integrity gaps have focused positive and negative coverage.
- Mixed roots, substituted targets, incomplete verdict evidence, and contaminated traces are rejected wherever current contracts require that behavior.
- Existing Project Configurator evaluation behavior remains intact.

## Dependencies

None.

## Verification

- Inspect the five recorded commits and current Project Configurator evaluation surfaces.
- Run focused Project Configurator fixture, runner, and receipt-integrity tests for confirmed gaps.
- Run git diff --check.
- Obtain independent review of the evidence classification and retained protections.

## Open Questions

None.

## Notes

- The legacy branch and worktree can be deleted after this record is committed and verified.
