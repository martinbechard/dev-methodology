# Make file-provider claim events conditional on configured resource coordination

Status: Starting

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/respect-resource-coordination-none-in-manage-file-work-items.md

Completion: direct-main

Owner: Unowned pending acceptance

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-first-eight-lint-defects-019fa9bb

Normalized Objective: Make file-provider work-item procedures valid when a project selects resource coordination none as well as when it selects agent-claim.

Dispatch Time: 2026-07-28T18:22:25Z

Intended Root Role: Dev Orchestrator

Runtime Thread: Pending

Root Agent Task: Pending

Next Lifecycle Owner: Root Dev Orchestrator

## Summary

Make file-provider work-item procedures valid when a project selects resource coordination none as well as when it selects agent-claim.

## Context

The primary affected skill is skills/manage-file-work-items/SKILL.md. Its clauses require agent-claim even when a valid project selects resource_coordination: none. In that configuration there is no enabled claim procedure for the mandatory operation, leaving no valid provider route.

## Source Evidence

The user authorized immediate creation of independently dispatchable Defect records for every accepted skill-lint finding on 2026-07-28. The accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records the affected clauses at skills/manage-file-work-items/SKILL.md:28,150,244. Independent reviewer /root/confirm_critical_c accepted it as CONFIRMED_CRITICAL.

## Requirements

- Make provider claim directions conditional on the configured coordination implementation.
- Define the valid no-claim route when resource coordination is none.
- Preserve the agent-claim route when it is configured.

## Acceptance Criteria

- Identical provider transitions have a valid documented route under agent-claim and none configurations.
- The none configuration does not require an unavailable claim procedure.
- The agent-claim configuration retains conflict protection.

## Dependencies

None. Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

## Verification

- Exercise identical provider transitions under agent-claim and none configurations.
- Confirm a valid route in both cases.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None.

## Notes

This record has one primary affected skill identity: skills/manage-file-work-items/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check.
