# Replace the structured-design chain-of-thought output contract

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/replace-structured-design-chain-of-thought-output-contract.md

Completion: direct-main

## Summary

Replace the public chain-of-thought output contract in structured-design with concise observable design evidence.

## Context

The primary affected skill is skills/structured-design/SKILL.md. It requires public chain-of-thought output, which is not an appropriate durable artifact contract. The review companion may also need alignment if its instructions change.

## Source Evidence

The user authorized immediate Ready Defect creation for independently confirmed skill-lint findings on 2026-07-28. Accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records the output-contract finding for skills/structured-design/SKILL.md; skills/review-structured-artifact/SKILL.md is directly cited as the companion CHAIN-OF-THOUGHT review surface. Independent reviewer /root/confirm_critical_e accepted it as CONFIRMED_CRITICAL.

## Requirements

- Replace chain-of-thought output requirements with concise decision, evidence, and uncertainty artifacts.
- Preserve structured-design usefulness without requiring hidden reasoning disclosure.
- Align the review companion only if its contract actually conflicts.

## Acceptance Criteria

- Structured-design output contains observable design conclusions and supporting evidence without requiring chain-of-thought.
- The revised contract remains reviewable.
- Any changed review companion uses the same safe output boundary.

## Dependencies

None

## Verification

- Produce a representative structured-design artifact.
- Confirm it includes conclusions, evidence, and uncertainty without chain-of-thought.
- Run focused contract validation and git diff --check.
- Obtain independent review of the correction.

## Open Questions

None.

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/structured-design/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check. If skills/review-structured-artifact/SKILL.md changes, it requires separate exact-path approval and a separate accepted pre-mutation check.
