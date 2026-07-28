# Restore role-owned wiki verification routing and portable operation paths

Status: Starting

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/project-wiki-role-routing-and-operation-paths.md

Completion: direct-main

Owner: Unowned pending root acceptance

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-seven-batch2-defects-019fa9bb

Normalized Objective: Restore role-owned wiki verification routing and portable operation paths.

Dispatch Time: 2026-07-28T18:56:59Z

Intended Root Role: Dev Orchestrator

Runtime Thread: Pending canonical child Thread creation after this durable reservation.

Root Agent Task: Pending canonical root Dev Orchestrator acceptance.

Next Lifecycle Owner: Root Dev Orchestrator

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
- Define role-owned handling for an interrupted verifier without bypassing the verification-before-move boundary.

## Acceptance Criteria

- Topic-writing and topic-verification roles have unambiguous separate responsibilities.
- Verification remains required before a source move that depends on its result.
- Every documented operation path resolves in source and installed contexts.
- Pre-move and post-move interruption checks preserve the verification-before-move boundary and record the required role-owned BLOCKED evidence.

## Dependencies

None

## Verification

- Exercise the role-routing workflow with independent verification.
- Resolve all documented operation paths from source and installed contexts.
- Simulate verifier interruption before and after a prospective move and confirm the verification-before-move boundary and role-owned BLOCKED evidence.
- Run focused workflow validation and git diff --check.
- Obtain independent review of the correction.

## Open Questions

None.

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/project-wiki/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check.
