# Restore role-owned wiki verification routing and portable operation paths

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/project-wiki-role-routing-and-operation-paths.md

Completion: direct-main

Owner: Unowned

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Prior Launch Reservation: reserve-seven-batch2-defects-019fa9bb

Normalized Objective: Restore role-owned wiki verification routing and portable operation paths.

Dispatch Time: 2026-07-28T18:56:59Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019faa18-fe86-7110-9b9e-c7be3bdc8888

Root Agent Task: 019faa18-fe86-7110-9b9e-c7be3bdc8888

Branch: codex/project-wiki-role-routing-operation-paths-019faa18

Worktree: /Users/martinbechard/.codex/worktrees/4713/dev-methodology

Phase: Ready for parent dispatch reservation; preserved canonical root must accept Starting -> Running before repository mutation.

Started At: 2026-07-28T19:07:00Z

Claim Evidence: running-project-wiki-role-routing-operation-paths-019faa18-recovery; SHARED_CHECKOUT_ACQUIRED; claim event e64f1eb5-10e8-417f-980b-9e8e8b818b7e; recovery notification followed prior DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED event 38ae895b-7bfa-4366-86bc-a0c17bfa5be9.

Next Lifecycle Owner: Parent Coordinator, then the preserved root Dev Orchestrator

## Resumption Evidence

User Answer: approved

Answered At: 2026-07-28

Answer Provenance: Canonical work-item Thread 019faa18-fe86-7110-9b9e-c7be3bdc8888; exact user message immediately after the recorded User Action Required question.

Disposition: User Action Required -> Ready.

Approved Scope: skills/project-wiki/SKILL.md and agents/roles/wiki-activities/wiki-ingester.role.yaml only.

Approved Semantics: Make verifier dispatch and interruption role-owned, require role-owned BLOCKED evidence before and after a prospective move without bypassing the pre-move GOOD boundary, and resolve helper operations portably from the loaded skill directory.

Exclusions Preserved: No wiki-topic-verifier, wiki-writer, project-wiki-topic-write, project-wiki-topic-verify, other governed definition, or hand-edited generated mirror.

Approval-Record and Preflight Requirement: Before any governed-definition mutation, create a delegated-user-direction approval record covering both exact paths and run scripts/render-agents-technology-skills.py --project PROJECT.yaml --check-definition-change separately for each path using that record.

Preserved Canonical Thread and Root Agent Task: 019faa18-fe86-7110-9b9e-c7be3bdc8888.

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

## User Action Required

Question: Do you approve modifying exactly these two governed canonical definitions for this defect: skills/project-wiki/SKILL.md and agents/roles/wiki-activities/wiki-ingester.role.yaml? The change will make verifier dispatch/interruption role-owned, require BLOCKED evidence for pre- and post-move verifier interruption without bypassing the pre-move GOOD boundary, and resolve project-wiki helper operations portably from the loaded skill directory. Supported generated mirrors will be regenerated from those approved sources; no other skill or agent definition will be changed.

Why User Owns This: Repository governance requires explicit exact scope approval before a governed definition mutation.

Approved Scope Requested:

- skills/project-wiki/SKILL.md
- agents/roles/wiki-activities/wiki-ingester.role.yaml

Exclusions: No wiki-topic-verifier, wiki-writer, project-wiki-topic-write, project-wiki-topic-verify, or other governed definition may change. Generated mirrors must never be hand-edited.

Preflight After Approval: Create a delegated-user-direction approval record naming both exact definitions. Run scripts/render-agents-technology-skills.py --project PROJECT.yaml --check-definition-change separately for skills/project-wiki/SKILL.md and agents/roles/wiki-activities/wiki-ingester.role.yaml using that record.

Unattended Boundary: All definition, companion test/reference, regeneration, review, verification, and delivery work stops. Only read-only inspection may continue.

Resumption: Move through User Action Required -> Ready -> Starting -> Running in canonical Thread 019faa18-fe86-7110-9b9e-c7be3bdc8888 before mutation.

## Lifecycle Recovery Evidence

Canonical Runtime Thread: 019faa18-fe86-7110-9b9e-c7be3bdc8888

Canonical Root Agent Task: 019faa18-fe86-7110-9b9e-c7be3bdc8888

Parent Coordinator: 019fa9bb-1423-7e80-bcde-3caa765e3758

Branch: codex/project-wiki-role-routing-operation-paths-019faa18

Worktree: /Users/martinbechard/.codex/worktrees/4713/dev-methodology

Running Lifecycle Commit: 8fd05f6f22da49dbe0f9e09569307a42cc123ed7

Prior Rejection Event: 38ae895b-7bfa-4366-86bc-a0c17bfa5be9

Running Claim Acquire and Release Events: e64f1eb5-10e8-417f-980b-9e8e8b818b7e / c22ca0b4-7488-400b-a55c-1fefd05c2080

Read-Only Analysis Evidence: The primary affected governed definitions are skills/project-wiki/SKILL.md and agents/roles/wiki-activities/wiki-ingester.role.yaml. No governed definition mutation has occurred.
