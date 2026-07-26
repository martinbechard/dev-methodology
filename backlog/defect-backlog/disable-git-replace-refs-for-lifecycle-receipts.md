# Disable Git Replace Refs for Lifecycle Receipts

Status: Starting

Type: Defect

Owner: Dev Backlog Coordinator (reservation pending root acceptance)

Provider: file

Provider Reference: backlog/defect-backlog/disable-git-replace-refs-for-lifecycle-receipts.md

Completion: direct-main

## Summary

Ensure lifecycle receipt Git inspection bypasses replace refs so a reported object ID always resolves to its raw immutable commit content.

## Context

Independent review reproduced a replace-ref substitution against candidate commit 22fa4219c2ee8f1f89da7cfeb8ccc9f027a00a70 in canonical task 019f978e-28b7-7561-be38-b535ab26850f. A commit whose raw tree changed innocent.txt was replaced with another commit, and create-plus-verify accepted expected.txt under the original reported SHA. The affected non-governed implementation Git calls in lifecycle_handoff_receipts.py do not disable replace refs with --no-replace-objects or GIT_NO_REPLACE_OBJECTS.

## Source Evidence

Standing user direction in root task 019f978e-28b7-7561-be38-b535ab26850f requires every additional distinct confirmed defect to be logged durably rather than as a warning. Fresh independent review supplied the reproduced replace-ref substitution and authorized this defect record on 2026-07-25.

## Requirements

- Make every lifecycle receipt object, parent, tree, diff, content, and ancestry read bypass Git replace refs.
- Verify the raw immutable object identity and content associated with every reported object ID.
- Reject replace-ref substitution through a structured error and recovery path.
- Do not mutate governed definitions without the required exact approval evidence.

## Acceptance Criteria

- A disposable-Git test proves a replace-ref substitution is rejected.
- Object, parent, tree, diff, content, and ancestry receipt reads all bypass replace refs.
- A lifecycle receipt cannot accept substituted content under an original reported SHA.
- Structured error and recovery behavior is covered by focused tests.
- No governed definition changes occur without required approval evidence.

## Dependencies

- backlog/defect-backlog/reject-nonexistent-lifecycle-handoff-commit-oids.md: coordinate to avoid duplicate overlapping lifecycle receipt edits.

## Verification

- Run focused real-Git replace-ref tests.
- Run relevant lifecycle handoff receipt runner regressions.
- Run git diff --check.
- Obtain independent review.

## Open Questions

None.

## Current Starting Reservation

- Transition: Ready -> Starting.
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a.
- Reservation: One parent-owned launch reservation.
- Normalized Objective: Disable Git replace refs for lifecycle receipts.
- Dispatched At: 2026-07-26T17:07:38Z.
- Intended Root Role: Dev Orchestrator.
- Runtime Thread And Task Id: Pending canonical child task creation by the parent after this durable reservation.
- Coordination Classification: The Dependencies entry is a coordination-only overlap note. Its referenced item is Blocked and Unowned, and the preflight registry has no live claim. Private-worktree implementation may begin; exact overlap scope and integration must be reconciled before the conflicting integration event.
- Next Lifecycle Owner: The root Dev Orchestrator must record a distinct Starting -> Running acceptance before repository mutation.

## Notes

This transaction records the defect only. Do not implement source changes as part of backlog creation.
