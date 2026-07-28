# Make agent-claim reset recover invalid JSON registry shapes

Status: Starting

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/agent-claim-reset-invalid-json-shapes.md

Completion: direct-main

Owner: Unowned pending acceptance

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-first-eight-lint-defects-019fa9bb

Normalized Objective: Make the agent-claim reset operation recover every invalid JSON registry shape that its contract promises to repair.

Dispatch Time: 2026-07-28T18:22:25Z

Intended Root Role: Dev Orchestrator

Runtime Thread: Pending

Root Agent Task: Pending

Next Lifecycle Owner: Root Dev Orchestrator

## Summary

Make the agent-claim reset operation recover every invalid JSON registry shape that its contract promises to repair.

## Context

The primary affected skill is skills/agent-claim-command/SKILL.md. Its reset contract promises recovery when the claim registry contains malformed contents. Independent review found that valid JSON with a non-object top-level value reaches a get call in skills/agent-claim-command/scripts/claim.py and can raise AttributeError instead of restoring a valid empty registry.

## Source Evidence

The user authorized immediate creation of independently dispatchable Defect records for every accepted skill-lint finding on 2026-07-28. The accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records this finding at skills/agent-claim-command/SKILL.md:153 and implementation confirmation at skills/agent-claim-command/scripts/claim.py:1999-2008. Independent reviewer /root/confirm_critical_a accepted it as CONFIRMED_CRITICAL.

## Requirements

- Define one recovery path for malformed JSON and valid JSON values that are not registry objects.
- Make reset return a valid empty registry for every supported invalid registry shape.
- Keep valid claim-registry behavior unchanged.

## Acceptance Criteria

- Reset succeeds for missing, malformed, non-object, and invalid claims-shape registries.
- Each supported reset leaves a valid empty registry.
- Existing valid registry reset behavior remains documented and tested.

## Dependencies

None. Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

## Verification

- Exercise missing, malformed, non-object, and invalid claims-shape registry inputs.
- Confirm a valid empty registry after each supported reset.
- Run focused command-helper tests and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None.

## Notes

This record has one primary affected skill identity: skills/agent-claim-command/SKILL.md. It does not authorize a skill-definition mutation. If the correction changes that governed SKILL.md, later implementation requires explicit scope-specific user approval naming the exact definition, a provenance approval record, and the supported pre-mutation definition-change check. A code-only correction to skills/agent-claim-command/scripts/claim.py remains subject to ordinary implementation review and verification.
