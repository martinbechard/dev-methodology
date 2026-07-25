# Assert Strengthened Fixture Root Prompt Boundary

Status: Ready

Type: Defect

Owner: Unowned

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

## Notes

This transaction records the defect only. Do not implement source changes as part of backlog creation.
