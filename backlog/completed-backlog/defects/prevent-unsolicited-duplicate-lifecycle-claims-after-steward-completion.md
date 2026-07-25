# Prevent Overlapping Steward Follow-Up Cleanup Races

Status: Completed

Type: Defect

Owner: Unowned

Provider: file

Provider Reference: backlog/completed-backlog/defects/prevent-unsolicited-duplicate-lifecycle-claims-after-steward-completion.md

Completion: direct-main

## Execution Acceptance

- Canonical Work-Item Thread: 019f996c-1d89-7ad3-bd4f-c3a9dc7708fd
- Canonical Task Id: 019f996c-1d89-7ad3-bd4f-c3a9dc7708fd
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Root Role: Dev Orchestrator
- Delivery Worktree: /Users/martinbechard/.codex/worktrees/e1d4/dev-methodology
- Delivery Branch: detached HEAD
- Delivery Checkout State: Detached HEAD at d19829abc54a331eb0493d44046737ef05d312fc.
- Starting-to-Running Phase: accepted.
- Authority Boundary: This accepted transition authorizes no governed-definition mutation.

## Execution Coordination Evidence

- Launch reservation claim: reserve-duplicate-lifecycle-claim-defect-20260725 acquired at journal event 4a590b6c-b978-4ca4-a278-90237a3b4319 and released at journal event e35a4e0d-c13e-465e-b15a-916cf785d741.
- Starting-to-Running backlog claim: starting-running-prevent-duplicate-lifecycle-019f996c acquired on primary main at 2026-07-25T13:19:19.623969Z; acquisition journal event ce9c2011-2958-4083-9da1-aa0e665c37f1.

## Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Reservation: One parent-owned launch reservation.
- Normalized Objective: Prevent unsolicited duplicate lifecycle claims after Steward completion.
- Dispatched At: 2026-07-25T13:16:35Z
- Intended Root Role: Dev Orchestrator
- Runtime Thread And Task Id: Historical reservation record; the canonical child task was subsequently created and accepted under the canonical work-item Thread above.
- Authority Boundary: This reservation authorizes no governed-definition mutation.

## Reservation Coordination Evidence

- Backlog Claim: reserve-duplicate-lifecycle-claim-defect-20260725 acquired on primary main at 2026-07-25T13:16:35.538608Z; acquisition journal event 4a590b6c-b978-4ca4-a278-90237a3b4319.

## Summary

Prevent overlapping or queued Dev Backlog Steward follow-ups from exposing misleading terminal state or allowing external cleanup while a child turn is still active.

## Context

For canonical task 019f9783-31a0-7e91-9704-08cde7886b3a, the intended first transaction acquired lifecycle claim event 5e41129d-f6a1-4078-ae3d-1644edc5b14e and released event d2e56af1-c9dd-47a2-be3e-4f27cb012016. The root explicitly called followup_task twice for the same Steward target while the first turn was active. The second call was a distinct supplemental requested operation, not an autonomous or unrequested duplicate.

The queued second child turn acquired event 49cfb40c-dc85-4b38-a201-a8fc28f77aa9. Before that child had stopped, the parent incorrectly issued a premature no-change release, event 8128b101-8acd-43dc-be2e-064ae773c931. The child later committed 7515d5df349b0674b07c40eeabebb5923e5195df, then its release returned CLAIM_NOT_FOUND at event c4c4b0aa-2f36-4678-b9f3-196b8dda13d8. This is an external Codex collaboration runtime scheduling, child-terminal-state, and cleanup-reconciliation concern; it is not evidence of an unsolicited child operation.

## Source Evidence

The canonical exact-file item was User Action Required and Unowned at commit 5e93546366f68ea4ff3e8b6879769798c3bdae6b. The cited task and journal events are durable evidence of the two explicit followup_task requests and the unsafe cleanup race.

No repository candidate or commit exists for this runtime defect. Private branch codex/prevent-duplicate-lifecycle-claim-019f996c is clean at 0673262864c6a9f46d2d93246ac4a2eb4ff0d074. No implementation claim was ever acquired, no governed definition was mutated, and repository search found FOLLOWUP_TASK_FILES=0.

## Requirements

- Provide the Codex collaboration runtime source and regression environment that owns the external behavior; do not simulate a fix in this repository.
- Required external surfaces: followup_task schema and handler; per-target child scheduler; queued, running, and completed terminal-result store; ambiguous dispatch and status-reconciliation API; delayed or overlapping child regression suite.
- Required behavior priority: (1) per-target turn serialization or one active turn equivalent; (2) truthful queued, running, and completed visibility across first-turn FINAL; (3) reconcile status before retry or cleanup; (4) reject cleanup until the owning child is proven stopped; (5) stable caller transaction idempotency key with payload-conflict handling; (6) same-transaction completed-result replay.
- Preserve exact task and journal evidence for both requested transactions.

## Acceptance Criteria

- The external runtime source and regression environment can reproduce and correct the scheduling and cleanup race without a repository proxy fix.
- Per-target turn serialization and terminal-result visibility make cleanup and retry decisions truthful across a first-turn FINAL response.
- Cleanup is rejected until the owning child is proven stopped, and ambiguous dispatch is reconciled before any retry.
- Stable caller transaction idempotency keys reject payload conflicts and replay a completed result for the same transaction.
- Delayed and overlapping child regressions cover the two requested operations and their cleanup ordering.

## Dependencies

None.

## Verification

PASS. The repository-side coordination evidence passed: 36 focused tests, consisting of PYTHONDONTWRITEBYTECODE=1 python3 evals/agent-tests/dev-backlog-coordinator/test_coordination_simulator.py (20/20) and PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_codex_workitem_coordination.py (16/16), plus git diff --check, clean branch, and zero live claims. These tests do not verify the unavailable external scheduler implementation or API.

Fresh Dev Code Reviewer evidence FAILed the original incident wording, PASSed the no-repository-implementation conclusion, and required this durable correction.

## User Authority And Closure

On 2026-07-25, the user explicitly directed in this canonical task that the safeguard will be a different work item in a different project and that no user action remains on this original work. This is scope-specific terminal completion authority, not abandonment.

The original item outcome is accepted as the corrected investigation, verified incident chronology, repository-ownership conclusion, and external handoff conclusion. The runtime safeguard itself is intentionally out of scope for this repository and is being handled as a separate work item in another project and agent. The user accepted the omission of an in-repository runtime implementation.

## Completion Evidence

- Completed At: 2026-07-25T16:26:55Z
- Completion Disposition: READY for direct-main closure.
- Accepted Result Commit: 2b7f5ba23d43a1f2e8629567e0f122ba0e942fb7.
- Main Observation: accepted result commit is an ancestor of primary main observed at 25429bb1af1398cd09fd0df77573cb82abe89e16 before the terminal provider transaction; no source integration was necessary because the accepted conclusion and provider evidence were already on main.
- Independent Review: original causal wording FAIL; corrected no-repository-implementation conclusion PASS; corrected external handoff accepted.
- Verification: PASS — 36 focused tests (20/20 coordination simulator and 16/16 codex-workitem coordination), git diff --check, exact rollout, journal, and ancestry evidence, clean worktrees, and zero live claims before terminal completion.
- Provider Closure: atomic User Action Required to Completed archive move under the short primary-main backlog claim terminal-complete-019f996c, acquired at journal event 8eac924e-1151-4e78-bd06-14c53fcf2ce8.
- Terminal Archive Path: backlog/completed-backlog/defects/prevent-unsolicited-duplicate-lifecycle-claims-after-steward-completion.md.

## Notes

This completion clears the former User Action Required state. No active implementation claim exists to release. Existing launch, reservation, task, thread, lifecycle, and exact journal evidence above remains canonical.

The historical provider filename is retained as the canonical identity but is not the corrected causal description.
