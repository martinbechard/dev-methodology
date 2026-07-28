# Bound Jest failure ownership to the current change

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/bound-jest-failure-ownership-to-current-change.md

Completion: direct-main

## Summary

Limit Jest repair ownership to failures attributable to the current change and preserve unrelated failures as separate evidence.

## Context

The primary affected skill is skills/jest/SKILL.md. It treats every failing test as belonging to the current task. This expands ownership to unrelated failures and can block an otherwise complete scoped change.

## Source Evidence

The user authorized immediate creation of independently dispatchable Defect records for every accepted skill-lint finding on 2026-07-28. The accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records this finding at skills/jest/SKILL.md:32. Independent reviewer /root/confirm_critical_b accepted it as CONFIRMED_CRITICAL.

## Requirements

- Require attribution to the current change before assigning repair ownership.
- Record unrelated or pre-existing failures separately.
- Preserve bounded verification and defect-reporting routes.

## Acceptance Criteria

- One attributable and one pre-existing failure produce repair ownership only for the attributable failure.
- The pre-existing failure is recorded without expanding the current task scope.
- A scoped change can complete when its own verification conditions pass.

## Dependencies

None. Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

## Verification

- Present one attributable and one pre-existing failure.
- Confirm repair ownership only for the attributable failure.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None.

## Notes

This record has one primary affected skill identity: skills/jest/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check.
