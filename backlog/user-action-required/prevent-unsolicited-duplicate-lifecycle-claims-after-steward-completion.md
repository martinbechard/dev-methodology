# Prevent Unsolicited Duplicate Lifecycle Claims After Steward Completion

Status: User Action Required

Type: Defect

Owner: Unowned

Provider: file

Provider Reference: backlog/user-action-required/prevent-unsolicited-duplicate-lifecycle-claims-after-steward-completion.md

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
- Runtime Thread And Task Id: Pending canonical child task creation by the parent after this durable reservation.
- Authority Boundary: This reservation authorizes no governed-definition mutation.

## Reservation Coordination Evidence

- Backlog Claim: reserve-duplicate-lifecycle-claim-defect-20260725 acquired on primary main at 2026-07-25T13:16:35.538608Z; acquisition journal event 4a590b6c-b978-4ca4-a278-90237a3b4319.

## Summary

Prevent a completed Dev Backlog Steward transaction from executing an unsolicited duplicate lifecycle claim after its intended claim was released.

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

## User Action Required

External owner: Codex collaboration runtime.

## Question for the User

Will you provide or route this work to the Codex collaboration runtime source and regression environment that owns followup_task scheduling, child terminal-result state, and cleanup reconciliation?

## Why User Input Is Required

The required runtime source, scheduler implementation, terminal-result store, reconciliation API, and regression environment are outside this repository. This repository has no candidate implementation surface for the defect.

## Resolution

Pending. No external runtime source or delivery capability has been supplied.

## Unattended Work Boundary

Do not mutate repository proxy code, governed definitions, generated mirrors, or the claim engine to simulate an external fix.

## Permitted Resumption

When the user or external owner supplies the runtime source and capability, or confirms external delivery, resume this same canonical task through User Action Required -> Ready -> Starting -> Running. Do not create a replacement task.

## Notes

This external handoff clears the stale Running ownership. No active implementation claim exists to release. Existing launch, reservation, task, thread, and lifecycle evidence above remains canonical.
