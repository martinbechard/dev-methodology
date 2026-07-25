# Preserve Malformed Checkpoint Fallback Without Fixture Contract

Status: Ready

Type: Defect

Owner: Unowned

Provider: file

Provider Reference: backlog/defect-backlog/preserve-malformed-checkpoint-fallback-without-fixture-contract.md

Completion: direct-main

## Summary

Preserve the documented structured retained-evidence boundary for receipt-bearing malformed-checkpoint scenarios that do not declare a fixture contract.

## Context

Candidate 85e6a31 runner baseline staging indexes scenario fixtureContract even though validation permits receipt-bearing malformed-checkpoint scenarios without it. Five existing cases raise KeyError before runtime and lose their retained evidence envelope.

## Source Evidence

Fresh final review of candidate 85e6a31 in canonical task 019f978e-28b7-7561-be38-b535ab26850f confirmed this distinct defect on 2026-07-25. Standing user direction requires each additional confirmed defect to be logged durably.

## Requirements

- Align staging or validation with the documented structured evidence boundary for receipt-bearing malformed-checkpoint scenarios without fixtureContract.
- Preserve the retained evidence envelope when the scenario is valid under that boundary.
- Do not mutate governed definitions without required exact approval evidence.

## Acceptance Criteria

- The five affected cases no longer raise KeyError before runtime.
- Receipt-bearing malformed-checkpoint scenarios without fixtureContract preserve the documented structured evidence boundary.
- A focused five-case regression covers the behavior.
- No governed definition changes occur without required approval evidence.

## Dependencies

- backlog/defect-backlog/reject-nonexistent-lifecycle-handoff-commit-oids.md: coordinate to avoid duplicate overlapping lifecycle correction edits.

## Verification

- Run the focused five-case regression.
- Run relevant runner regressions.
- Run git diff --check.
- Obtain independent review.

## Open Questions

None.

## Notes

This transaction records the defect only. Do not implement source changes as part of backlog creation.
