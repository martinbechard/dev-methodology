# Structure Non-UTF-8 Git Path Receipt Errors

Status: Starting

Type: Defect

Owner: Dev Backlog Coordinator (reservation pending root acceptance)

Provider: file

Provider Reference: backlog/defect-backlog/structure-non-utf8-git-path-receipt-errors.md

Completion: direct-main

## Summary

Ensure lifecycle receipt changed-path and content processing handles arbitrary Git path bytes with a stable structured error or reversible JSON encoding.

## Context

Lifecycle receipt changed-path and content parsing decodes Git filename bytes directly as UTF-8. A disposable mktree and commit-tree path named bad-\xff raises an unstructured UnicodeDecodeError.

## Source Evidence

Fresh final review of candidate 85e6a31 in canonical task 019f978e-28b7-7561-be38-b535ab26850f confirmed this distinct defect on 2026-07-25. Standing user direction requires each additional confirmed defect to be logged durably.

## Requirements

- Handle arbitrary Git path bytes in lifecycle receipt changed-path and content processing.
- Return a stable LifecycleHandoffError or a reversible JSON encoding instead of an unstructured decode failure.
- Do not mutate governed definitions without required exact approval evidence.

## Acceptance Criteria

- A real-Git mktree and commit-tree test with a bad-\xff path does not raise UnicodeDecodeError.
- The outcome is a stable LifecycleHandoffError or reversible JSON encoding for the path bytes.
- Focused lifecycle receipt tests cover the behavior.
- No governed definition changes occur without required approval evidence.

## Dependencies

- backlog/defect-backlog/reject-nonexistent-lifecycle-handoff-commit-oids.md: coordinate to avoid duplicate overlapping lifecycle correction edits.

## Verification

- Run focused real-Git non-UTF-8 path receipt tests.
- Run relevant runner regressions.
- Run git diff --check.
- Obtain independent review.

## Open Questions

None.

## Current Starting Reservation

- Transition: Ready -> Starting.
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a.
- Reservation: One parent-owned launch reservation.
- Normalized Objective: Structure non-UTF-8 Git path receipt errors.
- Dispatched At: 2026-07-26T17:07:13Z.
- Intended Root Role: Dev Orchestrator.
- Runtime Thread And Task Id: Pending canonical child task creation by the parent after this durable reservation.
- Coordination Classification: The Dependencies entry is a coordination-only overlap note. Its referenced item is Blocked and Unowned, and the preflight registry has no live claim. Private-worktree implementation may begin; exact overlap scope and integration must be reconciled before the conflicting integration event.
- Next Lifecycle Owner: The root Dev Orchestrator must record a distinct Starting -> Running acceptance before repository mutation.

## Notes

This transaction records the defect only. Do not implement source changes as part of backlog creation.
