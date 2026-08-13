# Reconcile Project Organiser Filename-Selection Regression Gaps

Status: Running

Type: Defect

Provider: file

Work Item ID: reconcile-project-organiser-filename-selection-regression-gaps

Completion: main-branch

## Summary

Reassess four abandoned Project Organiser filename-selection regression branches against current main and retain only assertion and omission-boundary coverage that is still missing.

## Context

Current main contains the completed Project Organiser filename-selection correction and a substantially rewritten bundle-content test surface. Four later worktrees attempted to harden required and forbidden selection markers, structured omissions, sentinels, punctuation boundaries, container boundaries, and complete-field handling. Their patches conflict with current scripts/test_bundle_content.py and must not be replayed directly.

The preserved source branches are temporary evidence only:

- codex/align-project-organiser-filename-selection-oracle-correction at 41343b0327705504b1f9d50600b031dc5a8dbbed
- codex/align-project-organiser-filename-selection-oracle-review-correction-1 at 517679cec2b1fd0288b0dea803ada3838ef83844
- codex/align-project-organiser-filename-selection-oracle-omission-correction-2 at 6e7eb7460a7e133b6a7d7ce37a262a41eefce019
- codex/align-project-organiser-filename-selection-complete-field-correction-3 at 971bad6bc8a5ffe4b1aeafc49d49c88e48dc8da3

After this work item is committed and verified as self-contained, those branches and worktrees can be deleted. Git history and this record retain the investigation identity without presenting the old branches as active delivery candidates.

## Source Evidence

On 2026-08-12, the user approved combining the related Project Organiser correction branches into one replacement work item and directed that source branches be discarded after the work-item record is verified.

The worktree mergeability review in .codex/reports/worktree-related-main-merge-review.md found high overlap risk and recommended deriving any residual gaps from current main rather than merging the branches.

## Requirements

- Compare the four recorded branch commits with the current Project Organiser filename-selection assertions in scripts/test_bundle_content.py.
- Classify each branch case as already covered, obsolete because the contract changed, or a reproducible current-main gap.
- Preserve the current Project Organiser response-only behavior and filename/path-selection contract.
- Add only current, demonstrably missing regression cases.
- Use Judge only when referring to an Evaluation evaluator; use assertion, expected result, matcher, or test condition for deterministic test behavior.
- Do not restore stale skill names, generated-bundle expectations, or pre-rewrite test structure.

## Acceptance Criteria

- Every distinct behavior represented by the four branch commits has a recorded current-main disposition.
- Confirmed gaps have focused regression coverage in the current bundle-content structure.
- Already-covered and obsolete cases do not produce duplicate assertions.
- Current Project Organiser filename and path selection behavior remains consistent with its maintained contract.
- The implementation does not use Judge as a generic synonym for deterministic test assertions.

## Dependencies

None.

## Verification

- Inspect the four recorded commits and current scripts/test_bundle_content.py.
- Run the focused Project Organiser bundle-content tests affected by any accepted cases.
- Run current bundle-content validation for the modified assertion surface.
- Run git diff --check.
- Obtain independent review of the residual-gap classifications and terminology boundary.

## Open Questions

None.

## Notes

- This item concerns deterministic regression assertions. The separate replace-evaluation-oracle-terminology-with-judge item governs terminology for Evaluation evaluators and must not be broadened into a generic test-vocabulary rewrite.
- The four legacy branches are evidence inputs, not accepted implementation candidates.

## Starting Handoff Evidence

- Reserved At: 2026-08-13T15:52:49Z.
- Transition: `Ready -> Starting`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Baseline: `19287867c625a82e2001f01b2d271b43cdec73de` on primary `main`.
- Priority: Oldest eligible independent process-correctness defect after the terminology correction entered Blocked.
- Capacity: Runs alongside `reconcile-offline-staging-and-strict-result-schema`; Blocked and User Action Required items are excluded.
- Overlap: Offline owns only its exact evaluation runner, test, fixture, and plan paths. This task must claim its exact current regression-test and evidence scope before mutation and must not touch Offline paths or unrelated artifacts.
- Dispatch Architecture: Create one visible Codex task whose initial prompt launches one Dev Orchestrator subagent and assigns title and messaging responsibility to the visible root task.
- Transition Claims: Work Item `start-project-organiser-regression-work-item`; event `5dd010aa-956f-4eb2-ad85-d42956981895`. Provider `start-project-organiser-regression-provider`; event `cafe677b-b3cb-4794-8c73-8dec4eddb3cc`.
- Canonical Codex Task ID: `019ffbd4-33a1-7e91-8460-1f5ab8a10bcd`.
- Canonical Conversation ID: `019ffbd4-33a1-7e91-8460-1f5ab8a10bcd` (combined runtime identity).
- Runtime Host: `local`.
- Runtime Project: saved `dev-methodology` project at `/Users/martinbechard/dev/dev-methodology`.
- Runtime Created At: `2026-08-13T15:53:35Z` (`1786636415`).
- Requested Title: `Starting — Reconcile Project Organiser Filename Selection Regression Gaps`; the runtime preview is ellipsized only.
- Runtime Creation Outcome: Unique success with no client or pending identity. Creation does not imply Running.

## Running Acceptance Evidence

- Transition: `Starting -> Running`.
- Accepted At: 2026-08-13T15:55:20Z.
- Owner: Dev Orchestrator `/root/reconcile_project_organiser`.
- Canonical Task ID: `019ffbd4-33a1-7e91-8460-1f5ab8a10bcd`.
- Canonical Conversation ID: `019ffbd4-33a1-7e91-8460-1f5ab8a10bcd`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Accepted Branch: `main`.
- Accepted Worktree: `/Users/martinbechard/dev/dev-methodology` (primary worktree).
- Accepted Baseline: `e31b4ea5c69c7bb256bb40090598d4f7ee29b284`.
- Phase: implementation and TDD planning before source mutation.
- Commit Selection: `main-branch` through `deliver-work-item-main-branch`.
- Work-Item Update Claim: `reconcile-project-organiser-regression-update-019ffbd4`; acquisition event `05266bf0-fef3-4fe0-bc52-71f4fe803fc8`.
- Provider Path Claim: `reconcile-project-organiser-regression-backlog-019ffbd4`; acquisition event `9f5680b4-70e4-4270-ad6f-2084bc4f4c7a`.
- Accepted Execution: The canonical Codex task is running, the selected file-provider manager accepted this exact transition evidence, and source mutation remains gated on planning and independent architecture review.
