# Align fix-explanation relationship examples with the six-type explanation model

Status: Starting

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/align-fix-explanation-item-taxonomy.md

Completion: direct-main

Owner: Unowned pending acceptance

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-first-eight-lint-defects-019fa9bb

Normalized Objective: Make fix-explanation relationship examples conform to the declared six-type structured-explanation model.

Dispatch Time: 2026-07-28T18:22:25Z

Intended Root Role: Dev Orchestrator

Runtime Thread: Pending

Root Agent Task: Pending

Next Lifecycle Owner: Root Dev Orchestrator

## Summary

Make fix-explanation relationship examples conform to the declared six-type structured-explanation model.

## Context

The primary affected skill is skills/fix-explanation/SKILL.md. Its relationship examples use TEST, FIX, PROBLEM, and BENEFIT as item types even though skills/structured-explanation/SKILL.md permits only QUERY, SUB-QUERY, FACT, HYPOTHESIS, UNKNOWN, and ANSWER. The conflicting example makes the output contract unsatisfiable.

## Source Evidence

The user authorized immediate creation of independently dispatchable Defect records for every accepted skill-lint finding on 2026-07-28. The accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records the conflicting examples at skills/fix-explanation/SKILL.md:152,191-196 and item-type authority at skills/structured-explanation/SKILL.md:30-37. Independent reviewer /root/confirm_critical_b accepted it as CONFIRMED_CRITICAL.

## Requirements

- Express relationship examples with permitted structured item types, or label those terms as ordinary concepts.
- Keep the six-type model authoritative.
- Preserve the intended fix-explanation relationships.

## Acceptance Criteria

- Every representative structured item uses one of the six declared item types.
- The relationship examples remain understandable without inventing additional types.
- The six-type model and fix-explanation examples no longer conflict.

## Dependencies

None. Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

## Verification

- Produce a representative fix explanation.
- Assert that every structured item uses the declared six-type model.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None.

## Notes

This record has one primary affected skill identity: skills/fix-explanation/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check. Discovery must separately justify any change to skills/structured-explanation/SKILL.md.
