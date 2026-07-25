# Prevent Unsolicited Duplicate Lifecycle Claims After Steward Completion

Status: Ready

Type: Defect

Owner: Unowned

Provider: file

Provider Reference: backlog/defect-backlog/prevent-unsolicited-duplicate-lifecycle-claims-after-steward-completion.md

Completion: direct-main

## Summary

Prevent a completed Dev Backlog Steward transaction from executing an unsolicited duplicate lifecycle claim after its intended claim was released.

## Context

For canonical task 019f9783-31a0-7e91-9704-08cde7886b3a, the intended lifecycle claim acquired event 5e41129d-f6a1-4078-ae3d-1644edc5b14e and released event d2e56af1-c9dd-47a2-be3e-4f27cb012016. After completion, an unrequested child claim 019f9783-supplemental-approval-steward acquired event 49cfb40c-dc85-4b38-a201-a8fc28f77aa9. The parent found no changes since baseline and released it with no-change event 8128b101-8acd-43dc-be2e-064ae773c931.

## Source Evidence

The canonical exact-file item was User Action Required and Unowned at commit 5e93546366f68ea4ff3e8b6879769798c3bdae6b. The cited task and journal events are durable evidence of the post-completion duplicate claim.

## Requirements

- A completed Steward follow-up must not execute an unsolicited duplicate lifecycle claim.
- Make child completion and final-answer dispatch single-dispatch and idempotent.
- Reconcile ambiguous completion without issuing a duplicate acquire or mutation.
- Preserve exact task and journal evidence for the intended transaction.
- Do not fix this behavior as part of this record-creation transaction.

## Acceptance Criteria

- One requested lifecycle transaction produces exactly one intended claim and mutation.
- A later duplicate action is suppressed or reconciled without a second claim acquisition.
- No extra claim-journal event is written for a suppressed duplicate.
- An existing completed result is returned idempotently.
- Focused tests reproduce delayed post-completion child execution and prove duplicate acquire and mutation are rejected.

## Dependencies

None.

## Verification

- Run focused Steward dispatch and completion tests.
- Run delayed-child and ambiguous-completion duplicate-claim regressions.
- Run git diff --check and obtain independent review.

## Notes

This record captures the confirmed defect only. Do not dispatch, implement, or alter the canonical task in this creation transaction.
