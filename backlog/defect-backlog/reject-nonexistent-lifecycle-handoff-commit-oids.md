# Reject Nonexistent Lifecycle Handoff Commit OIDs

Status: Running

Type: Defect

Owner: Dev Orchestrator

Provider: file

Provider Reference: backlog/defect-backlog/reject-nonexistent-lifecycle-handoff-commit-oids.md

Completion: direct-main

## Resumption Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Canonical Thread/Task: 019f978e-28b7-7561-be38-b535ab26850f
- Reservation: One parent-owned same-task resumption launch reservation; no replacement task is created.
- Normalized Objective: Reject nonexistent lifecycle handoff commit OIDs.
- Dispatched At: 2026-07-25T12:16:47Z
- Intended Root Role: Dev Orchestrator
- Preserved Evidence: Candidate branch codex/reject-nonexistent-lifecycle-handoff-oids-019f978e, worktree /Users/martinbechard/.codex/worktrees/215b/dev-methodology, accepted candidate a12babfc3b919b5e5334821703c8549fe40aa82a, and the approved exact governed-definition scope remain binding.
- Phase: Governed definition implementation.
- Resumed At: 2026-07-25T12:18:08Z

## Resumption Coordination Evidence

- Backlog Claim: resume-lifecycle-handoff-oid-019f978e acquired on primary main at 2026-07-25T12:16:47.368016Z; acquisition journal event 730270a6-96d9-4e28-9488-bf43dd958676.

## Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Canonical Thread/Task: 019f978e-28b7-7561-be38-b535ab26850f
- Reservation: One parent-owned launch reservation.
- Intended Root Role: Dev Orchestrator
- Isolated Checkout: /Users/martinbechard/.codex/worktrees/215b/dev-methodology
- Phase: Governed definition implementation.
- Dispatched At: 2026-07-25T04:36:08Z

## Execution Identity

- Canonical Thread/Task: 019f978e-28b7-7561-be38-b535ab26850f
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Root Role: Dev Orchestrator
- Branch: codex/reject-nonexistent-lifecycle-handoff-oids-019f978e
- Worktree: /Users/martinbechard/.codex/worktrees/215b/dev-methodology
- Started At: 2026-07-25T04:39:47Z

## Candidate Delivery Location

- Candidate Branch: codex/reject-nonexistent-lifecycle-handoff-oids-019f978e
- Candidate Worktree: /Users/martinbechard/.codex/worktrees/215b/dev-methodology
- Candidate Base Commit: 3642d791d04fc06e5c2f586bafc42e2e2795bb82
- Candidate Commit: a12babfc3b919b5e5334821703c8549fe40aa82a (accepted candidate on the clean private worktree)
- Earlier Project-File Claim: aa6826f1-62fd-4d00-933c-53aa1f8474bb, released no-change at event 1dd9a2b9-9618-420e-95a0-c50dcf1fe1ad before source writes due private-worktree relocation.

## Correction Attempt 1 Review

- Independent Reviewer: Dev Code Reviewer
- Verdict: CHANGES_REQUIRED
- Finding: High — a valid unrelated self-consistent commit can satisfy every lane, including terminal closeout, because expected parent, path, and state authority are not caller-bound.
- Disposition: Correction returned to the original Dev Coder.

## Correction Attempt 2 Review

- Independent Reviewer: Dev Code Reviewer
- Verdict: CHANGES_REQUIRED
- Finding: High — repeated candidate-controlled root baseline accepts fully rewritten history.
- Finding: High — Git replace refs can substitute content under the reported SHA.
- Related Defect: backlog/defect-backlog/disable-git-replace-refs-for-lifecycle-receipts.md, durably logged in commit 6842a4647f98a1afde4d41364e032ce006124c75.
- Disposition: Both findings returned to the original Dev Coder as the final bounded attempt.

## Verification Evidence

- Independent Reviewer: Dev Code Reviewer
- Verdict: ACCEPTED
- Material Findings: None.
- Focused Tests: 44/44 passed.
- Correction History: ef86acb -> 22fa421 -> 85e6a31 -> 1eab8bb -> 988bc4b -> a12babf.
- Verifier Task: /root/verify_oid_receipts dispatched.
- Governed-Definition Approval Gap: Open. This verification evidence does not imply terminal readiness or authorize governed-definition mutation.
- Independent Verifier: PASSED with 46/46 focused tests, 18/18 wiki checks, and freshness, compile, diff, and raw object checks.
- Delivery State: No Commit delivery or integration has been performed; the candidate remains on the clean private branch.

## User Action Required

### Question for the User

Do you explicitly approve mutation of skills/manage-file-work-items/SKILL.md, agents/roles/dev-activities/dev-backlog-steward.role.yaml, skills/codex-workitem-coordination/SKILL.md, and agents/roles/dev-activities/dev-orchestrator.role.yaml, plus only their supported generated mirrors, to require immediate full commit-OID capture, raw commit-object verification, immutable provider-path/content/task/claim receipts, structured recovery, and end-to-end handoff propagation?

### Why User Input Is Required

These governed instruction sources own producer/provider and orchestrator handoff behavior; executable runner enforcement alone cannot make distributed agents comply.

### Prohibited Unattended Action

Do not mutate those definitions or mirrors, run pre-mutation approval checks using manufactured provenance, integrate a partial candidate, or close the provider without an explicit answer.

### Resolution

Approved on 2026-07-25 in canonical task 019f978e-28b7-7561-be38-b535ab26850f. Exact user messages: Approved; I approve. Provenance: direct answer to the recorded Question for the User.

### Approved Scope

- skills/manage-file-work-items/SKILL.md
- agents/roles/dev-activities/dev-backlog-steward.role.yaml
- skills/codex-workitem-coordination/SKILL.md
- agents/roles/dev-activities/dev-orchestrator.role.yaml
- Only the supported generated mirrors of those approved canonical sources.

### Resulting Disposition

Approved. The item is Ready and awaits the parent Coordinator's Ready -> Starting reservation. This transaction does not set Starting or Running.

### Resumption

The same canonical task preserves candidate a12babfc3b919b5e5334821703c8549fe40aa82a. After an answer, the parent must route User Action Required -> Ready -> Starting, and this root's Steward must record Starting -> Running before mutation resumes.

## Coordination Evidence

- Backlog Claim: reserve-lifecycle-handoff-oid-defect-019f978e acquired on primary main at 2026-07-25T04:36:08.080425Z; acquisition journal event 03c16c20-3fa5-40fd-a43b-61352ae4e3a7.
- Running Transition Claim: record-running-lifecycle-handoff-oids-019f978e acquired on primary main at 2026-07-25T04:39:41.479916Z; acquisition journal event aaa4b206-d60a-47a4-abf5-7ec4e9782c22. Earlier wait attempt: f769d7a1-2113-4390-a1a9-096dd7d6f720; direct release baton received after unrelated claim release event 0db72b9d-17c1-4d45-8c5a-cb4260689656.
- Material-Phase Claim: record-implementation-phase-handoff-oids-019f978e acquired on primary main at 2026-07-25T04:49:43.065533Z; acquisition journal event ffdd7539-8b43-42bd-9100-e89380e75484.
- Correction-Attempt Claim: record-correction-attempt-handoff-oids-019f978e acquired on primary main at 2026-07-25T05:14:47.330838Z; acquisition journal event eaf39685-ca41-40a2-bbe2-bf7ee29a848b.
- Correction-Attempt-2 Claim: record-correction-attempt2-handoff-oids-019f978e acquired on primary main at 2026-07-25T05:31:44.092988Z; acquisition journal event a9215dec-8cfc-46b3-aced-c5e055c15828.
- Verification-Phase Claim: record-verification-phase-handoff-oids-019f978e acquired on primary main at 2026-07-25T06:37:04.074955Z; acquisition journal event fc079bb0-4edb-4b90-ada1-3fb402a5c711.
- User-Action-Required Transition Claim: move-lifecycle-oid-to-uar-019f978e acquired on primary main at 2026-07-25T06:51:28.892456Z; acquisition journal event 27983099-ef32-45d1-9a76-cf2af3a9c6e1. Earlier wait attempt 9b5f91bc-2da1-4b64-bb6f-a8c53daef5f4 reconciled after direct release baton event d12478df-4ff5-41bf-96a2-212ae39081c8.
- Approval-Resolution Claim: record-governed-approval-resume-019f978e acquired on primary main at 2026-07-25T12:08:23.325017Z; acquisition journal event 000030dc-d420-4cb4-9f41-641810b63b93.
- Running-Resumption Claim: record-governed-implementation-running-019f978e acquired on primary main at 2026-07-25T12:17:54.518445Z; acquisition journal event dca2352f-6f77-4452-90d2-5f7414ffcd6d.
- Ambiguous-Commit-Provenance Claim: record-ambiguous-commit-provenance-019f978e acquired on primary main at 2026-07-25T13:02:28.343178Z; acquisition journal event c821b5ac-8169-4ed4-a732-161d374f9f11.

## Summary

Make lifecycle and provider handoffs derive each commit OID from Git after commit creation and verify the immutable object before reporting it as durable evidence.

## Context

A lifecycle Steward handoff reported commit OID `9cc052194342bddd471425ab9840f35aaf51ddf6`, but the committed lifecycle object is `9cc05219fbb2c10b80ef3300568398dd44f5f8a2`. On 2026-07-25, direct Git reproduction showed `git cat-file -t` rejects the reported OID and identifies the actual OID as a commit. A nonexistent or mistyped OID must not become durable lifecycle evidence.

## Source Evidence

Canonical task `019f9783-31a0-7e91-9704-08cde7886b3a` handoff and the direct Git reproduction on 2026-07-25. Standing user direction requires every confirmed defect to be logged durably.

## Ambiguous Commit Dispatch and Provenance Evidence

During exact-claims candidate work on 2026-07-25, the Dev Coder reported that it did not invoke a commit, but the candidate branch HEAD advanced to raw commit 0f3dcab5d539ea1aca197e1fc28fab574e2746b4. The claim release journal event 4f2e543a-91e7-4798-b1aa-b9a817fa1d0b recorded that resulting_commit and all committed scope paths. Reflog evidence shows an ordinary commit at 2026-07-25 08:56:08 -0400 authored and committed by configured user Martin Bechard. No responsible process or dispatch identity was identified; afterward the worktree was clean and the registry was empty.

This is ambiguous commit-dispatch and provenance evidence, not proof that the reporting agent created the commit and not a nonexistent OID.

## Requirements

- Capture the actual commit OID immediately from Git after commit creation.
- Use Git object inspection to verify the reported OID exists and is a commit before reporting it.
- Bind handoff changed-path and content evidence to that exact immutable commit object.
- Reject absent, non-commit, stale, or mismatched reported OIDs with structured error and recovery behavior.
- Preserve exact provider paths, canonical task identity, and claim-event evidence.
- Do not fabricate a correction by prefix matching or substitution.
- Reconcile the raw Git object, claim release evidence, reflog, process identity, and dispatch identity after ambiguous commit dispatch.
- Report unknown creator truthfully; never attribute an unknown commit to an agent or reject a verified object merely because creator identity is unknown.

## Acceptance Criteria

- A normal lifecycle commit reports the OID read back from Git and passes object inspection.
- A mistyped or nonexistent OID is rejected and cannot be persisted as handoff evidence.
- A non-commit or mismatched OID is rejected with the applicable structured recovery outcome.
- Tests cover stale HEAD movement and ambiguous commit dispatch without attributing mutable HEAD to the handoff.
- Terminal and source-move transactions bind their provider paths and content evidence to the verified immutable object.
- No prefix-based guessed correction is accepted.
- Ambiguous commit-dispatch recovery reconciles the raw object, claim release, reflog, process identity, and dispatch identity.
- Unknown creator identity is reported truthfully without attributing the commit to an agent or rejecting a verified object.

## Dependencies

None.

## Verification

- Run focused Steward and lifecycle handoff tests.
- Run real disposable-Git tests for normal commit, mistyped OID, stale HEAD, ambiguous dispatch, and terminal/source-move transactions.
- Run relevant handoff schema and evaluation tests.
- Run `git diff --check` and obtain fresh independent review.

## Open Questions

- Which existing handoff schema field should carry the verified object type and immutable changed-path receipt without duplicating Git metadata?

## Notes

This record captures the confirmed defect only. Do not implement unrelated lifecycle corrections or mutate governed definitions without the required exact approval evidence.
