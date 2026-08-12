# Reconcile Documentation Template Parser Candidate

Status: Ready

Type: Defect

Provider: file

Work Item ID: reconcile-documentation-template-parser-candidate

Completion: main-branch

## Summary

Reassess the abandoned documentation-template parser hardening against current main and port only behavior that remains missing.

## Context

The branch codex/enforce-documentation-template-conformance-b948-correction3 at 6fd28466768643c05d1332a101df994089e2b3cb contains four parser and fixture commits. It covers context grammar, container boundaries, readiness parsing, command inventory, path resolution, contradiction checks, and deterministic regression cases.

The branch was previously judged mergeable, but a fresh non-mutating merge against current main now conflicts in validate_fixture.py and test_fixtures.py. Current main changed those same maintained surfaces after the review baseline. The branch must not be merged through automatic conflict selection.

## Source Evidence

On 2026-08-12, the user approved preserving the branch's useful outcome before deleting legacy worktrees. Fresh integration reconciliation found content conflicts against current main, requiring a replacement work item rather than direct integration.

## Requirements

- Compare all four branch commits with the current documentation-writer template-conformance fixture and tests.
- Classify each parser rule and regression case as already covered, obsolete, or a current defect.
- Port only confirmed current-main gaps using the present parser structure.
- Preserve current template, context, readiness, command, path, and contradiction semantics.
- Do not restore stale fixture structure or resolve conflicts by selecting an entire branch version.

## Acceptance Criteria

- Every distinct candidate behavior has a recorded disposition.
- Confirmed gaps have focused current-main regression tests.
- Existing accepted documentation-template behavior remains intact.
- The legacy branch is unnecessary for future implementation after this record is committed.

## Dependencies

None.

## Verification

- Inspect commits f016c8619d68d535e274b4bba8d6b9c0284a3c07, 0483c6d117503370d4371ba5d8f8ca909538d0b2, b9483a3997c720352edcfa2e98e87f894ae34bcc, and 6fd28466768643c05d1332a101df994089e2b3cb.
- Run the focused Dev Documentation Writer template-conformance fixture tests.
- Run git diff --check.
- Obtain independent review of every retained or rejected behavior.

## Open Questions

None.

## Notes

- The legacy branch and worktree can be deleted after this work item is committed and verified.
