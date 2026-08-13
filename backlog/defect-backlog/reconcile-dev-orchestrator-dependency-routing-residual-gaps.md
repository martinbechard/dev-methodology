# Reconcile Dev Orchestrator Dependency-Routing Residual Gaps

Status: Running

Type: Defect

Provider: file

Work Item ID: reconcile-dev-orchestrator-dependency-routing-residual-gaps

Completion: main-branch

## Summary

Verify three residual dependency-routing protections against current main and implement only confirmed gaps: linked-worktree containment, malformed handoff-receipt evidence retention, and exact producer-identity validation.

## Context

The completed deterministic dependency-routing fixture is already present on main. The abandoned follow-up branch codex/deterministic-orchestrator-routing-resume-correction2 at 6c598418892e784c9ea3a145f4e8307f93d85147 contains five commits, four of which are not patch-equivalent to current main. Direct replay is unsafe because the fixture, contract, scenarios, and tests have materially changed and conflict with the branch.

The branch nevertheless records three behaviors that require an explicit current-main audit:

- release-journal paths must remain within the fixture Git metadata boundary, including when symlinks are present in linked-worktree layouts;
- malformed handoffReceipts structures and missing required receipt lanes must fail explicitly while retaining bounded diagnostic evidence;
- required producer identities must be validated exactly rather than accepted through ambiguous or substituted evidence.

After this work item is committed and verified as self-contained, the source branch and worktree can be deleted.

## Source Evidence

On 2026-08-12, the user requested preservation work before legacy-worktree cleanup and directed that replacement work items contain enough evidence to permit deletion of their source branches. The annotated mergeability report records the three residual behaviors above and rejects direct integration of the five-commit branch.

## Requirements

- Test each recorded residual behavior against current main before changing implementation.
- Reproduce linked-worktree and symlink containment behavior without relying on the legacy worktree.
- Reject handoffReceipts values that are not arrays of objects and receipts with missing or non-string lane identities.
- Preserve bounded diagnostic evidence for malformed receipts without accepting invalid evidence.
- Fail explicitly when required receipt lanes are absent.
- Validate exact required producer identity at the evidence boundary.
- Implement only behaviors that are absent or defective on current main.
- Do not restore superseded fixture structure or blindly replay any branch commit.

## Acceptance Criteria

- Each of the three residual behaviors has a recorded current-main disposition: already correct, obsolete, or confirmed defect.
- Every confirmed defect has a focused regression test and a bounded correction.
- Linked-worktree and symlink cases cannot escape the authorized fixture metadata boundary.
- Malformed or incomplete handoff receipts fail with bounded, useful diagnostics.
- Producer-identity validation rejects substitution or ambiguity.
- Existing accepted dependency-routing behavior remains intact.

## Dependencies

None.

## Verification

- Inspect commit 6c598418892e784c9ea3a145f4e8307f93d85147 and its four non-equivalent predecessors as historical evidence.
- Run focused Dev Orchestrator dependency-routing fixture and runner tests.
- Add negative cases for each confirmed gap.
- Run git diff --check.
- Obtain independent review of the evidence boundary and residual-gap classifications.

## Open Questions

None.

## Notes

- The completed specify-deterministic-dev-orchestrator-dependency-routing-fixtures item remains the original delivery record. This item covers only residual gaps found after that delivery.
- The legacy branch is an evidence source, not an accepted implementation candidate.

## Starting Handoff Evidence

- Reserved At: 2026-08-13T11:43:11Z.
- Transition: `Ready -> Starting`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Baseline: `e8923f2cb1fe967806a0542359d15af01d94ac19` on primary `main`.
- Capacity: Slot 4 of 5. Independent Dev Orchestrator evaluation-fixture scope; exclude private Backlog Dispatcher, provenance, evaluation-terminology targets, and documentation-template parser paths.
- Transition Claims: `start-reconcile-dev-orchestrator-dependency-routing-residual-gaps-work-item`; event `6304333c-89a7-4665-8dee-4d6b913bded1`. `start-reconcile-dev-orchestrator-dependency-routing-residual-gaps-provider`; event `968c81d8-b150-444a-9b01-53c10e2ac578`.
- Runtime Identity: Pending caller-owned visible task creation. Creation does not imply Running.

## Canonical Runtime Assignment

- Assigned At: 2026-08-13T11:46:27Z.
- Codex Task ID: `019ffaf1-81d3-7b82-9e97-20fad7cf56ba`.
- Conversation ID: `019ffaf1-81d3-7b82-9e97-20fad7cf56ba`.
- Host: `local`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Requested Title: `Starting — Reconcile Dev Orchestrator Dependency Routing Gaps`.
- Initial Action: Launch one Dev Orchestrator subagent for this authoritative provider record.
- Creation Outcome: Unique success decoded from a complete JSON-string envelope, with no client or pending identity and no retry.
- Lifecycle Boundary: This assignment remains `Starting` until the nested Dev Orchestrator accepts and records `Starting -> Running`.
- Adoption Claims: `adopt-reconcile-dev-orchestrator-dependency-routing-residual-gaps-visible-task`; event `015759a3-1ca2-44cd-8922-0d09f6ff58ab`. `adopt-reconcile-dev-orchestrator-dependency-routing-residual-gaps-provider`; event `3dc87295-54f0-4b2f-9174-5e0c9671ab72`.

## Running Acceptance

- Accepted At: 2026-08-13T11:48:24Z.
- Transition: `Starting -> Running`.
- Dev Orchestrator Task: `019ffaf1-81d3-7b82-9e97-20fad7cf56ba`.
- Accepted Baseline: `b1e10c9881a9a1a011ae049118f28562ebb1a9db` on `main`.
- Work Claim: `reconcile-dev-orchestrator-dependency-routing-residual-gaps-work`; event `8281a2ab-94f6-4aa9-a674-a17730e00b3a`.
- Provider Mutation Claim: `run-reconcile-dev-orchestrator-dependency-routing-residual-gaps-provider`; event `7d8b1234-45d9-4919-8d5c-0f6166550b3f`.
- Complex Development Plan Gate: Not yet evaluated.
