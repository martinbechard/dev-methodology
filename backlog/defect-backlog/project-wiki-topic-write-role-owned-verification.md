# Defer verifier orchestration to conceptual roles and resolve writer helper commands

Status: Starting

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/project-wiki-topic-write-role-owned-verification.md

Completion: direct-main

Owner: Unowned pending root acceptance

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-seven-batch2-defects-019fa9bb

Normalized Objective: Defer verifier orchestration to conceptual roles and resolve writer helper commands.

Dispatch Time: 2026-07-28T18:56:59Z

Intended Root Role: Dev Orchestrator

Runtime Thread: Pending canonical child Thread creation after this durable reservation.

Root Agent Task: Pending canonical root Dev Orchestrator acceptance.

Next Lifecycle Owner: Root Dev Orchestrator

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
