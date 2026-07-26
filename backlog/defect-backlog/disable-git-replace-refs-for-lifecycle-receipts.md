# Disable Git Replace Refs for Lifecycle Receipts

Status: Blocked

Type: Defect

Owner: Unowned

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

## Current Running Acceptance

- Transition: Starting -> Running.
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a (preserved from the Starting reservation).
- Canonical Work-Item Thread: 019f9f66-7522-72d1-a673-227a6b0f3ed9.
- Canonical Root Agent Task: 019f9f66-7522-72d1-a673-227a6b0f3ed9.
- Root Dev Orchestrator: /root.
- Delivery Branch: Detached HEAD at 9ce6fd7c72f157f143a4ca159f3380f1452d0263.
- Delivery Worktree: /Users/martinbechard/.codex/worktrees/6767/dev-methodology.
- Phase: Delivery accepted; this provider transaction contains no implementation artifact mutation.
- Started At: 2026-07-26T17:10:51Z.
- Parent Reservation Commit: 1c6cc7c42eb2f14917ac78a28ddad73968c47111.
- Claim Evidence: accept-running-disable-git-replace-refs-019f95a9; acquire outcome SHARED_CHECKOUT_ACQUIRED; claim event 29e2ddf8-410d-49c7-b980-48ea2dabab6c.
- Dependency Classification: coordination-only. Reconcile exact overlapping implementation scope before integration.

## Identity Reconciliation — 2026-07-26

- Reconciled the placeholder Running identity to canonical work-item Thread and root Agent Task 019f9f66-7522-72d1-a673-227a6b0f3ed9. This corrects identity evidence only; it is not a lifecycle transition and preserves the existing Running acceptance evidence.

## Current Blocked Handoff

- Transition: Running -> Blocked.
- Blocked At: 2026-07-26T17:35:38Z.
- Canonical Work-Item Thread And Root Agent Task: 019f9f66-7522-72d1-a673-227a6b0f3ed9.
- Candidate Branch: codex/disable-git-replace-refs-lifecycle-019f9f66.
- Preserved Accepted Candidate: b2a38f7a73686d8f95f868a525051720cd810db8.
- Exact Candidate Delta: evals/agent-tests/test_lifecycle_handoff_receipts.py only.
- Rejected Base: da09f3d9 is non-ancestral to current main and must not be imported.
- Review Evidence: Fresh Dev Code Reviewer disposition ACCEPTED with no material findings.
- Verification Evidence: Independent verifier PASS — real-Git replacement 1/1, lifecycle module 19/19, compile 2/2, and diff check.
- Blocker: Current main at 029a376b546a5800a8c6c5e411ad53d5f691c0ad lacks evals/agent-tests/lifecycle_handoff_receipts.py and evals/agent-tests/test_lifecycle_handoff_receipts.py. No accepted source-to-integration mapping exists.
- Dependency Handoff: backlog/defect-backlog/reject-nonexistent-lifecycle-handoff-commit-oids.md is waiting for this baton and other sibling batons for the newly authorized bounded combined current-main foundation plan.
- Provider Closure: Not permitted. The direct-main completion disposition is not READY.
- Scope Evidence: No governed definitions changed. No implementation claim remains.
- Recovery Owner: Parent Dev Backlog Coordinator / canonical foundation task 019f978e-28b7-7561-be38-b535ab26850f.
- Unblock Condition: A direct accepted current-main foundation delivery/content-mapping baton contains the receipt module. Then resume through Blocked -> Ready -> Starting -> Running and replay, review, and verify only this focused delta.
- Claim Evidence: record-blocked-disable-git-replace-refs-019f9f66; acquire outcome SHARED_CHECKOUT_ACQUIRED; claim event 5aa2c827-a223-4305-aaa5-f1210a0254fe.

## Notes

This transaction records the defect only. Do not implement source changes as part of backlog creation.
