# Assert Strengthened Fixture Root Prompt Boundary

Status: Starting

Type: Defect

Owner: Dev Backlog Coordinator (reservation pending root acceptance)

Provider: file

Provider Reference: backlog/defect-backlog/assert-strengthened-fixture-root-prompt-boundary.md

Completion: direct-main

## Summary

Align the focused prompt regression with the strengthened fixture-root boundary so the full clause cannot silently regress.

## Context

The strengthened prompt requires every suite-owned path below fixtureRoot, but the focused test asserts only the pre-existing never-under-/tmp phrase. A regression could revert the strengthened clause unnoticed.

## Source Evidence

Fresh review of candidate 1eab8bb66c2eb24d841d53c4b136f0638527c1c3 in canonical task 019f978e-28b7-7561-be38-b535ab26850f confirmed this distinct defect on 2026-07-25. Standing user direction requires each additional confirmed defect to be logged durably.

## Requirements

- Assert the full strengthened fixture-root prompt boundary in the focused regression.
- Keep the existing never-under-/tmp boundary assertion where it remains applicable.
- Do not weaken the established boundary.
- Do not mutate governed definitions without required exact approval evidence.

## Acceptance Criteria

- The focused regression distinguishes and asserts the full strengthened fixtureRoot clause.
- The focused prompt contract passes.
- The resulting contract does not weaken the established boundary.
- No governed definition changes occur without required approval evidence.

## Dependencies

- backlog/defect-backlog/reject-nonexistent-lifecycle-handoff-commit-oids.md: coordinate to avoid duplicate overlapping lifecycle correction edits.

## Verification

- Run the focused fixture-root prompt contract regression.
- Run relevant runner regressions.
- Run git diff --check.
- Obtain independent review.

## Open Questions

None.

## Current Starting Reservation

- Transition: Ready -> Starting.
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a.
- Reservation: One parent-owned launch reservation.
- Normalized Objective: Assert strengthened fixture-root prompt boundary.
- Dispatched At: 2026-07-26T16:58:35Z.
- Intended Root Role: Dev Orchestrator.
- Runtime Thread And Task Id: Pending canonical child task creation by the parent after this durable reservation.
- Coordination Classification: The Dependencies entry is a coordination-only overlap note. Its referenced item is Blocked and Unowned, and the preflight registry has no live claim. Private-worktree implementation may begin; exact overlap scope and integration must be reconciled before the conflicting integration event.
- Next Lifecycle Owner: The root Dev Orchestrator must record a distinct Starting -> Running acceptance before repository mutation.

## Notes

This transaction records the defect only. Do not implement source changes as part of backlog creation.
