# Bound MySQL production verification to safe test environments

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/bound-mysql-production-verification-to-safe-targets.md

Completion: direct-main

## Summary

Prevent MySQL verification guidance from directing destructive or state-changing checks against production targets.

## Context

The primary affected skill is skills/mysql/SKILL.md. Its production-verification direction can encourage commands that mutate or inspect live targets without a bounded safety gate. The accepted correction must preserve useful verification while restricting it to safe test environments or explicitly authorized read-only evidence.

## Source Evidence

The user authorized immediate Ready Defect creation for independently confirmed skill-lint findings on 2026-07-28. Accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records the finding at skills/mysql/SKILL.md:44. Batch g5 reported a contradictory raw summary, while the detailed MySQL finding was CRITICAL. The root Dev Orchestrator ran a focused Luna/high adjudication that resolved the outcome as CRITICAL. Independent reviewer /root/confirm_critical_c accepted it as CONFIRMED_CRITICAL.

## Requirements

- Bound state-changing verification to safe, non-production test environments.
- Require explicit, separately granted authority for any production-facing action.
- Preserve read-only evidence collection where safely authorized.

## Acceptance Criteria

- Production verification guidance does not prescribe state-changing commands by default.
- Safe test-environment verification remains executable.
- Any production-facing route states its authority and safety boundary.

## Dependencies

None

## Verification

- Exercise safe test-environment verification.
- Inspect production-facing guidance for explicit non-mutation and authority boundaries.
- Run focused contract validation and git diff --check.
- Obtain independent review of the correction.

## Open Questions

None.

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/mysql/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check.
