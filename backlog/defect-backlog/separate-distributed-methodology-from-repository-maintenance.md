# Separate distributed methodology guidance from repository maintenance procedures

Status: Starting

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/separate-distributed-methodology-from-repository-maintenance.md

Completion: direct-main

Owner: Unowned pending acceptance

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-first-eight-lint-defects-019fa9bb

Normalized Objective: Keep portable methodology-documentation guidance separate from dev-methodology source-checkout maintenance procedure.

Dispatch Time: 2026-07-28T18:22:25Z

Intended Root Role: Dev Orchestrator

Runtime Thread: Pending

Root Agent Task: Pending

Next Lifecycle Owner: Root Dev Orchestrator

## Summary

Keep portable methodology-documentation guidance separate from dev-methodology source-checkout maintenance procedure.

## Context

The primary affected skill is skills/maintain-methodology-documentation/SKILL.md. It embeds dev-methodology source-checkout paths and repository procedure that the repository-maintenance skill already owns. Distributed installations cannot reliably execute those repository-only directions.

## Source Evidence

The user authorized immediate creation of independently dispatchable Defect records for every accepted skill-lint finding on 2026-07-28. The accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records the affected clauses at skills/maintain-methodology-documentation/SKILL.md:3,14-23,33-63 and the repository-only boundary at .agents/skills/dev-methodology-repository-maintenance/SKILL.md:24-40. Independent reviewer /root/confirm_critical_c accepted it as CONFIRMED_CRITICAL.

## Requirements

- Keep repository procedure in the project-maintenance skill.
- Retain only portable methodology-documentation guidance in the distributed skill.
- Avoid dev-methodology-only source paths and commands in distributed instructions.

## Acceptance Criteria

- The distributed package requires no dev-methodology-only source path or command.
- Repository maintenance procedure remains available through its project skill.
- The distributed skill remains usable in an installed target project.

## Dependencies

None. Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

## Verification

- Validate the distributed package from an installation-oriented context.
- Confirm that no dev-methodology-only source path or command is required.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None.

## Notes

This record has one primary affected skill identity: skills/maintain-methodology-documentation/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check.
