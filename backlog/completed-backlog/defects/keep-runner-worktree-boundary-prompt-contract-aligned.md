# Keep Runner Worktree Boundary Prompt Contract Aligned

Status: Completed

Type: Defect

Owner: Unowned

Provider: file

Provider Reference: backlog/completed-backlog/defects/keep-runner-worktree-boundary-prompt-contract-aligned.md

Completion: direct-main

## Summary

Synchronize the runner worktree-boundary prompt source and focused regression contract without weakening the established boundary.

## Context

Candidate 85e6a31 changes the established phrase from lowercase never under to Never work under, leaving the focused prompt contract assertion red.

## Source Evidence

Fresh final review of candidate 85e6a31 in canonical task 019f978e-28b7-7561-be38-b535ab26850f confirmed this distinct defect on 2026-07-25. Standing user direction requires each additional confirmed defect to be logged durably.

## Requirements

- Synchronize the runner worktree-boundary prompt source and its focused regression contract.
- Preserve the established boundary without weakening it.
- Do not mutate governed definitions without required exact approval evidence.

## Acceptance Criteria

- The focused prompt contract assertion passes.
- The source and regression contract express the same worktree boundary.
- The resulting contract does not weaken the established boundary.
- No governed definition changes occur without required approval evidence.

## Dependencies

- backlog/defect-backlog/reject-nonexistent-lifecycle-handoff-commit-oids.md: coordinate to avoid duplicate overlapping lifecycle correction edits.

## Verification

- Run the focused prompt contract regression.
- Run relevant runner regressions.
- Run git diff --check.
- Obtain independent review.

## Open Questions

None.

## Current Starting Reservation

- Transition: Ready -> Starting.
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a.
- Reservation: One parent-owned launch reservation.
- Normalized Objective: Keep runner worktree boundary prompt contract aligned.
- Dispatched At: 2026-07-26T16:59:16Z.
- Intended Root Role: Dev Orchestrator.
- Runtime Thread And Task Id: Pending canonical child task creation by the parent after this durable reservation.
- Coordination Classification: The Dependencies entry is a coordination-only overlap note. Its referenced item is Blocked and Unowned, and the preflight registry has no live claim. Private-worktree implementation may begin; exact overlap scope and integration must be reconciled before the conflicting integration event.
- Next Lifecycle Owner: The root Dev Orchestrator must record a distinct Starting -> Running acceptance before repository mutation.

## Current Running Acceptance

- Transition: Starting -> Running.
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a (preserved from the Starting reservation).
- Root Dev Orchestrator Thread: 019f9f5f-8959-7b72-a67e-38f843e9e720.
- Canonical Root Agent Task Id: 019f9f5f-8959-7b72-a67e-38f843e9e720.
- Accepted At: 2026-07-26T17:03:23Z.
- Phase: Implementation accepted; no repository artifact mutation is included in this provider transaction.
- Branch: Detached HEAD at 51132889f3453a1196457713bea55c01878a175b.
- Worktree: /Users/martinbechard/.codex/worktrees/5766/dev-methodology (private worktree).
- Primary Main Observation: main at ba80dd685ab78d131349c028d06025fc06c207d0 when this acceptance was recorded.
- Claim Evidence: running-keep-runner-worktree-boundary-019f9f5f, acquired as SHARED_CHECKOUT_ACQUIRED at 2026-07-26T17:03:23.140010Z; claim event 45ae4143-9ef4-4aaf-8139-48c456ff0640.

## Completion Evidence

- Completed At: 2026-07-26T17:30:57Z.
- Completion Disposition: READY for direct-main closure.
- Accepted Candidate: 83e31b98e98d061bee7139d8e8b6c2a68db5e7e8.
- Main Delivery: the candidate was integrated as b1e3743201ff1e8de53f7eb1f27feb0d89209f2b, with parent f58290fac280b58d2ef7aa6a8338b28e5ba5781d. The delivery commit changed only evals/agent-tests/test_runner.py.
- Main Observation: b1e3743201ff1e8de53f7eb1f27feb0d89209f2b is an ancestor of primary main 6b753d2601bc3a3b8f6a23c2c5005068d5d180ed at the terminal provider preflight.
- Independent Review: the candidate Dev Code Review ACCEPTED with no findings. Fresh post-integration Dev Code Review ACCEPTED with no findings.
- Verification: final Dev Verifier PASS: 2/2 focused prompt regressions, 2/2 compile targets, exact sentence source/test match, and diff check. Broad suites were intentionally omitted as unrelated.
- Integration: Dev Merge Coordinator reconciled the conflict by retaining current-main scenarioRoots assertion and the candidate's exact full boundary sentence.
- Claim Evidence: the Running provider claim released at event 5e02fda3-c5e8-4bb4-b30b-ed883a3246f0. The integration project-files claim acquired at event 0720300b-91e8-4ca2-b3c0-5ef3d1003d70 and released normally at event e11c09f2-c0f7-4592-a527-7deccaa913c0. The terminal backlog claim complete-keep-runner-worktree-boundary-019f9f5f acquired at event caed3e1c-f7bb-4ec3-813e-639886c32839.
- Terminal Archive Path: backlog/completed-backlog/defects/keep-runner-worktree-boundary-prompt-contract-aligned.md.

## Notes

This transaction records the defect only. Do not implement source changes as part of backlog creation.
