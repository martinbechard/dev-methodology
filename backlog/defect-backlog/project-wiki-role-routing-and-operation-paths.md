# Restore role-owned wiki verification routing and portable operation paths

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/project-wiki-role-routing-and-operation-paths.md

Completion: direct-main

## Summary

Make project-wiki role routing preserve independent verification and resolve operation paths portably.

## Context

The primary affected skill is skills/project-wiki/SKILL.md. Its routing can conflict with role-owned verification and its operation examples use an undefined or non-portable helper root. This undermines the required verification boundary and installed use.

## Source Evidence

The user authorized immediate Ready Defect creation for independently confirmed skill-lint findings on 2026-07-28. Accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records the role-routing and operation-path finding for skills/project-wiki/SKILL.md. Independent reviewer /root/confirm_critical_d accepted it as CONFIRMED_CRITICAL.

## Requirements

- Route verification to the role that owns independent verification.
- Preserve the required verification-before-move boundary.
- Replace undefined or source-specific operation paths with portable resolution.

## Acceptance Criteria

- Topic-writing and topic-verification roles have unambiguous separate responsibilities.
- Verification remains required before a source move that depends on its result.
- Every documented operation path resolves in source and installed contexts.

## Dependencies

None. Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

## Verification

- Exercise the role-routing workflow with independent verification.
- Resolve all documented operation paths from source and installed contexts.
- Run focused workflow validation and git diff --check.
- Obtain independent review of the correction.

## Open Questions

None.

## Notes

This record has one primary affected skill identity: skills/project-wiki/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check.
