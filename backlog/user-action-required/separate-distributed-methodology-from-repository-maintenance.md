# Separate distributed methodology guidance from repository maintenance procedures

Status: User Action Required

Type: Defect

Provider: file

Provider Reference: backlog/user-action-required/separate-distributed-methodology-from-repository-maintenance.md

Completion: direct-main

Owner: Unowned pending user approval

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-first-eight-lint-defects-019fa9bb

Normalized Objective: Keep portable methodology-documentation guidance separate from dev-methodology source-checkout maintenance procedure.

Dispatch Time: 2026-07-28T18:22:25Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019fa9f9-60b1-74a2-998b-6b7efc913f02

Root Agent Task: 019fa9f9-60b1-74a2-998b-6b7efc913f02

Next Lifecycle Owner: Parent Dev Backlog Coordinator

## Running Acceptance

- Transition: Starting -> Running.
- Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758.
- Canonical Work-Item Thread: 019fa9f9-60b1-74a2-998b-6b7efc913f02.
- Canonical Root Agent Task Id: 019fa9f9-60b1-74a2-998b-6b7efc913f02.
- Owner: Root Dev Orchestrator.
- Delivery Branch: codex/separate-distributed-methodology-maintenance-019fa9f9.
- Delivery Worktree: /Users/martinbechard/.codex/worktrees/2a2c/dev-methodology.
- Phase: Read-only approval-boundary analysis.
- Started At: 2026-07-28T18:39:39Z.
- Started-At Evidence: The canonical root Dev Orchestrator accepted the parent-reserved work item and requested this distinct provider transition.
- Claim Evidence: running-acceptance-019fa9f9-60b1-74a2-998b-6b7efc913f02; claim outcome SHARED_CHECKOUT_ACQUIRED; claim event 9b3d677d-bb04-4fed-a4c6-8cbe5e10496b; claimed 2026-07-28T18:39:39.631163Z.

## User Action Required

- Transition: Running -> User Action Required.
- Coordinator Decision Owner: Parent Dev Backlog Coordinator 019fa9bb-1423-7e80-bcde-3caa765e3758.
- Canonical Work-Item Thread: 019fa9f9-60b1-74a2-998b-6b7efc913f02.
- Canonical Root Agent Task Id: 019fa9f9-60b1-74a2-998b-6b7efc913f02.
- Preserved Delivery Branch: codex/separate-distributed-methodology-maintenance-019fa9f9.
- Preserved Delivery Worktree: /Users/martinbechard/.codex/worktrees/2a2c/dev-methodology.
- Preserved Phase: Read-only approval-boundary analysis.
- Question: Do you approve changing only skills/maintain-methodology-documentation/SKILL.md and skills/maintain-methodology-documentation/agents/openai.yaml to remove dev-methodology checkout-specific paths and commands, retain portable methodology source and derived-output alignment guidance, and synchronize its Codex description metadata?
- Why User Input Is Required: Both paths are governed definition or metadata paths, and the required preflight returned BLOCKED_APPROVAL_REQUIRED.
- Unattended Boundary: No provider, source, definition, or delivery mutation may continue until explicit approval is recorded, routed User Action Required -> Ready -> Starting -> Running in this same canonical task, and both approval-record preflight checks pass. Read-only evidence is complete.
- Portability Proof Markers: The read-only analysis identified the dev-methodology checkout-specific paths and commands for removal while preserving portable methodology source and derived-output alignment guidance.
- Focused Verification Evidence: Three focused tests reported OK during the read-only analysis.
- Candidate Commit: None.
- Provider-Mutation Claim Evidence: uar-transition-019fa9f9-60b1-74a2-998b-6b7efc913f02; acquire outcome SHARED_CHECKOUT_ACQUIRED; acquire event 6152a8b5-0928-4ee1-88b9-32c747636027; destination extension outcome EXTENDED; extension event 777c27d4-9a02-4c96-ba6c-50d878a3b43d.

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

None

## Verification

- Validate the distributed package from an installation-oriented context.
- Confirm that no dev-methodology-only source path or command is required.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None.

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/maintain-methodology-documentation/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check.
