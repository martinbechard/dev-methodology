# Keep topic verification read-only and make helper checks executable

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/project-wiki-topic-verify-read-only-helper-resolution.md

Completion: direct-main

## Summary

Keep project-wiki topic verification read-only and make its helper commands resolve from an executable installed location.

## Context

The primary affected skill is skills/project-wiki-topic-verify/SKILL.md. Its verification guidance invokes an operation that can mutate state despite the role’s read-only boundary and references an unresolved project-wiki-skill-root helper location.

## Source Evidence

The user authorized immediate Ready Defect creation for independently confirmed skill-lint findings on 2026-07-28. Accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records the read-only and helper-resolution finding for skills/project-wiki-topic-verify/SKILL.md. Independent reviewer /root/confirm_critical_d accepted it as CONFIRMED_CRITICAL.

## Requirements

- Remove or redirect mutating helper operations from the read-only verification route.
- Resolve all required helper paths from a documented executable skill location.
- Preserve topic verification coverage.

## Acceptance Criteria

- Topic verification completes without mutating wiki state.
- Every documented helper command resolves in source and installed contexts.
- Verification findings remain reportable without an implicit repair action.

## Dependencies

None

## Verification

- Run the topic-verification route against a fixture and confirm no mutation occurs.
- Resolve each documented helper command from source and installed contexts.
- Run focused verification tests and git diff --check.
- Obtain independent review of the correction.

## Open Questions

None.

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/project-wiki-topic-verify/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check.
