# Reconcile Dev Orchestrator Dependency-Routing Residual Gaps

Status: Ready

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
