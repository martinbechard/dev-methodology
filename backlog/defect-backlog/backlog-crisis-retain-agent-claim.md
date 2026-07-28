# Preserve agent-claim ownership during backlog crisis delivery

Status: Running

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/backlog-crisis-retain-agent-claim.md

Completion: direct-main

Owner: Root Dev Orchestrator

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-first-eight-lint-defects-019fa9bb

Normalized Objective: Keep shared-path claim acquisition and conflict handling active while backlog crisis guidance permits delivery work.

Dispatch Time: 2026-07-28T18:22:25Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019fa9f9-3418-7b72-87e0-02e68efe0792

Root Agent Task: 019fa9f9-3418-7b72-87e0-02e68efe0792

Branch: codex/backlog-crisis-retain-agent-claim-019fa9f9

Worktree: /Users/martinbechard/.codex/worktrees/f213/dev-methodology

Current Phase: Root Dev Orchestrator accepted delivery ownership; implementation has not started.

Started At Evidence: Root acceptance recorded by Dev Backlog Steward on 2026-07-28T18:39:45Z after the parent reservation, against Runtime Thread and Root Agent Task 019fa9f9-3418-7b72-87e0-02e68efe0792.

Claim Evidence: SHARED_CHECKOUT_ACQUIRED claim backlog-crisis-retain-agent-claim-running-019fa9f9; incarnation 36d1be40-b734-427a-aa74-2a5fd0c4f61b; claim journal event 2e2dd569-b6fa-467a-ab70-22bfe2e00809; exact provider path claimed in the primary main checkout.

Next Lifecycle Owner: Root Dev Orchestrator

## Summary

Keep shared-path claim acquisition and conflict handling active while backlog crisis guidance permits delivery work.

## Context

The primary affected skill is skills/backlog-crisis-mode/SKILL.md. Its crisis procedure stops claim operations while continuing delivery around unrelated changes. That contradicts the owning claim contract in skills/agent-claim/SKILL.md for shared-path mutation and overlap handling, creating an unsafe permission to bypass live ownership.

## Source Evidence

The user authorized immediate creation of independently dispatchable Defect records for every accepted skill-lint finding on 2026-07-28. The accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records the contradiction at skills/backlog-crisis-mode/SKILL.md:32,44 and claim-rule evidence at skills/agent-claim/SKILL.md:20-21,69-75. Independent reviewer /root/confirm_critical_a accepted it as CONFIRMED_CRITICAL.

## Requirements

- Retain the configured agent-claim acquisition and conflict outcomes during crisis delivery.
- Preserve crisis triage behavior without granting a bypass around live shared-path claims.
- State the recovery or wait route when a claimed path overlaps crisis work.

## Acceptance Criteria

- Crisis guidance requires claim handling before a shared-path mutation.
- An overlapping live claim produces the owning wait or recovery outcome.
- Crisis delivery can still proceed for non-overlapping work.

## Dependencies

None

## Verification

- Apply crisis guidance to an overlapping live claim and confirm the documented wait or recovery outcome.
- Apply it to non-overlapping work and confirm bounded delivery remains possible.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None.

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/backlog-crisis-mode/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check. Discovery must separately justify any additional governed source.
