# Structure Non-UTF-8 Git Path Receipt Errors

Status: Blocked

Type: Defect

Owner: Unowned

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

## Current Running Acceptance

- Transition: Starting -> Running.
- Canonical Work-Item Thread: 019f9f66-52ad-7963-88e3-8b4b7d72f2f6.
- Canonical Root Agent Task: 019f9f66-52ad-7963-88e3-8b4b7d72f2f6.
- Parent Coordinator: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a.
- Root Dev Orchestrator: Root Dev Orchestrator.
- Delivery Branch: detached HEAD at ab6a21b7.
- Delivery Worktree: /Users/martinbechard/.codex/worktrees/96e3/dev-methodology.
- Phase: Implementation accepted.
- Started At: 2026-07-26T17:10:26Z.
- Claim Evidence: accept-running-019f9f66-structure-non-utf8; acquire event e701b26c-3db7-40c6-b164-a0eaafe232c0.

## Current Blocked Handoff

- Transition: Running -> Blocked.
- Recorded At: 2026-07-26T17:34:16Z.
- Canonical Work-Item Thread: 019f9f66-52ad-7963-88e3-8b4b7d72f2f6.
- Parent Coordinator: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a.
- Owner: Unowned.
- Preserved Candidate: 00f6aa59a060c4b16e08723b6bf5423259654283 on codex/structure-non-utf8-git-path-receipts-019f9f66, based on 85e6a31db1dcd144b5d0bfed84f218fb2905d726.
- Delivery Evidence: Fresh Dev Code Reviewer result GOOD with no material findings. Dev Verifier result PASS: 9/9 focused tests, 1/1 runner consumer, real-Git both decode boundaries, py_compile, diff check, and JSON roundtrip. The candidate changes two files only and is clean. No governed definitions changed.
- Blocker: No authorized accepted lifecycle-receipt foundation exists on main. Main at c0a4774afa5c2170e31c0aaf21d0d21d522eaff0 contains neither evals/agent-tests/lifecycle_handoff_receipts.py nor evals/agent-tests/test_lifecycle_handoff_receipts.py, and neither 00f6aa59a060c4b16e08723b6bf5423259654283 nor 85e6a31db1dcd144b5d0bfed84f218fb2905d726 is ancestral to main. Direct-main integration would import rejected ancestry.
- Canonical Lifecycle Evidence: Task 019f978e-28b7-7561-be38-b535ab26850f confirms 85e6a31 was never accepted and prohibits merge, cherry-pick, reconstruction, or import of 85e6a31, 1eab8bb6, or da09f3d9.
- Recovery Owner: Parent Coordinator plus the canonical lifecycle-receipt foundation task.
- Unblock Trigger: A newly authorized, accepted lifecycle-receipt foundation commit is on main and contains the two callable receipt files.
- Permitted Resumption: Parent-owned Blocked -> Ready -> Starting on this same canonical task, followed by root-owned Starting -> Running. Combine the exact 00f6aa59 behavior and test with the accepted foundation, then obtain fresh combined review and verification before direct-main delivery.
- Disposition: This is not a failed correction or terminal completion. Preserve the candidate and all review and verification evidence.
- Backlog Claim Evidence: record-blocked-structure-non-utf8-019f9f66; acquire event 6ea8608e-861d-442b-af45-f08b2fefc4aa.

## Notes

This transaction records the defect only. Do not implement source changes as part of backlog creation.
