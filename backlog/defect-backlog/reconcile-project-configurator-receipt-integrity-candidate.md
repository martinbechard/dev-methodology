# Reconcile Project Configurator Receipt-Integrity Candidate

Status: Starting

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

## Starting Handoff Evidence

- Reserved At: 2026-08-13T12:14:19Z.
- Transition: `Ready -> Starting`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Baseline: `00fd8d3adc6e6e6b3030f517b7885ca98446e174` on primary `main`.
- Capacity: Reuses the slot released by completed `reconcile-documentation-template-parser-candidate`. Active count remains at most five.
- Overlap: Project Configurator receipt-integrity evaluation scope is independent of active private-dispatcher, evaluation-terminology, dependency-routing, and estimate correction paths. Do not absorb the separately queued offline dependency and strict-schema candidate.
- Dispatch Architecture: Create one visible Codex task whose initial prompt launches one Dev Orchestrator subagent and states the visible root title-and-messaging responsibility.
- Transition Claims: `start-reconcile-project-configurator-receipt-integrity-candidate-work-item`; event `5d2b2e28-2dda-488b-a5c3-f0b963e1e468`. `start-reconcile-project-configurator-receipt-integrity-candidate-provider`; event `a1b856ac-4632-4d96-8e77-44a1597b02d7`.
- Runtime Identity: Pending caller-owned visible task creation. Creation does not imply Running.

## Canonical Runtime Assignment

- Assigned At: 2026-08-13T12:15:33Z.
- Codex Task ID: `019ffb0c-4e81-73a2-abd5-a7fd6b76dd83`.
- Conversation ID: `019ffb0c-4e81-73a2-abd5-a7fd6b76dd83`.
- Host: `local`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Requested Title: `Starting — Reconcile Project Configurator Receipt Integrity`.
- Initial Action: The visible root launches one Dev Orchestrator subagent for this authoritative provider record and owns required Codex title and subagent messaging.
- Creation Outcome: Unique direct `threadId` and `hostId` success with no client or pending identity and no retry.
- Lifecycle Boundary: This assignment remains `Starting` until the nested Dev Orchestrator accepts and records `Starting -> Running`.
- Adoption Claims: `adopt-project-configurator-receipt-task`; event `9c50f3a7-9c69-458e-8ac7-420ade137454`. `adopt-project-configurator-receipt-provider`; event `c3ed1310-eff7-4c4d-8445-609738d00720`.
