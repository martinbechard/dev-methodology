# Defer verifier orchestration to conceptual roles and resolve writer helper commands

Status: Running

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/project-wiki-topic-write-role-owned-verification.md

Completion: direct-main

Owner: Root Dev Orchestrator

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-seven-batch2-defects-019fa9bb

Normalized Objective: Defer verifier orchestration to conceptual roles and resolve writer helper commands.

Dispatch Time: 2026-07-28T18:56:59Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019faa19-0275-7210-aaf6-45931b8079ab

Root Agent Task: 019faa19-0275-7210-aaf6-45931b8079ab

Next Lifecycle Owner: Root Dev Orchestrator

## Running Acceptance

- Transition: Starting -> Running.
- Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758.
- Canonical Work-Item Thread: 019faa19-0275-7210-aaf6-45931b8079ab.
- Canonical Root Agent Task: 019faa19-0275-7210-aaf6-45931b8079ab.
- Owner: Root Dev Orchestrator.
- Accepted At: 2026-07-28T19:05:53Z.
- Branch: codex/project-wiki-topic-write-role-owned-verification-019faa19.
- Worktree: /Users/martinbechard/.codex/worktrees/9a08/dev-methodology.
- Phase: Read-only analysis pending exact governed-definition approval.
- Reserved Base/Main Commit: c41405babcc4b80ecc5404f1e6908d201373fede.
- Provider-Mutation Claim Evidence: starting-running-project-wiki-topic-write-role-owned-verification-019faa19 acquired by dev-backlog-steward for this exact backlog file; claim outcome SHARED_CHECKOUT_ACQUIRED, claim event 32989a07-7358-4209-aac6-76fb8b3fa764, incarnation 0d412f08-24ec-4c03-8ce0-355fa896dbd0.
- Recovery History: The earlier claim attempt was rejected with DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED; claim event c606912d-4cf5-42c7-bcb4-84a3bb782572. The Coordinator reconciled the primary checkout before this accepted transaction.
- Current Main Observation: main was clean at 41e61c0a92fd8fe1d6bfbb696923a4abef8376d8 when this transaction began.

## Summary

Keep topic-writing responsibility separate from verifier orchestration and make writer helper commands executable.

## Context

The primary affected skill is skills/project-wiki-topic-write/SKILL.md. It directs the writer to spawn a verifier even though verification orchestration belongs to the conceptual roles, and it references helper commands through a non-portable path.

## Source Evidence

The user authorized immediate Ready Defect creation for independently confirmed skill-lint findings on 2026-07-28. Accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records the role-boundary and helper-resolution finding for skills/project-wiki-topic-write/SKILL.md. Independent reviewer /root/confirm_critical_d accepted it as CONFIRMED_CRITICAL.

## Requirements

- Defer verifier orchestration to the role that owns it.
- Keep writer responsibilities bounded to topic creation and handoff.
- Resolve writer helper commands from a documented executable location.
- Define interruption handling that preserves writer edits, keeps the verifier non-mutating, and leaves verifier orchestration role-owned.

## Acceptance Criteria

- The topic writer does not claim verifier-orchestration authority.
- Verification handoff names the role-owned route.
- Every writer helper command resolves in source and installed contexts.
- A simulated verifier interruption preserves writer edits, keeps the verifier non-mutating, and produces the required role-owned BLOCKED evidence without moving orchestration into the writer.

## Dependencies

None

## Verification

- Exercise writer creation and handoff without a writer-spawned verifier.
- Resolve documented helper commands in source and installed contexts.
- Simulate verifier interruption and confirm preserved edits, non-mutation, and role-owned BLOCKED evidence.
- Run focused contract validation and git diff --check.
- Obtain independent review of the correction.

## Open Questions

None.

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/project-wiki-topic-write/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check.
