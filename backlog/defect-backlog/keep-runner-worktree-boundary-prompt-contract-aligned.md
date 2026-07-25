# Keep Runner Worktree Boundary Prompt Contract Aligned

Status: Ready

Type: Defect

Owner: Unowned

Provider: file

Provider Reference: backlog/defect-backlog/keep-runner-worktree-boundary-prompt-contract-aligned.md

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

## Notes

This transaction records the defect only. Do not implement source changes as part of backlog creation.
