# Make the technology detector fallback prerequisites executable

Status: Running

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/make-technology-detector-fallback-prerequisites-executable.md

Completion: direct-main

Owner: Root Dev Orchestrator task 019fa9f9-33ef-7c73-872e-bd374d9108b2

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-first-eight-lint-defects-019fa9bb

Normalized Objective: Make the documented technology-detector fallback runnable on every declared supported runtime.

Dispatch Time: 2026-07-28T18:22:25Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019fa9f9-33ef-7c73-872e-bd374d9108b2

Root Agent Task: 019fa9f9-33ef-7c73-872e-bd374d9108b2

Branch: codex/make-technology-detector-fallback-prerequisites-executable

Worktree: /Users/martinbechard/.codex/worktrees/0f55/dev-methodology

Phase: Source analysis / code-only correction assessment

Started At: 2026-07-28T18:39:45.277192Z

Claim Evidence: lifecycle-running-019fa9f9-33ef-7c73-872e-bd374d9108b2 acquired as SHARED_CHECKOUT_ACQUIRED at 2026-07-28T18:39:45.277192Z; claim journal event 2b0184db-55bf-4163-b76a-c0007cb10a68.

## Summary

Make the documented technology-detector fallback runnable on every declared supported runtime.

## Context

The primary affected skill is skills/detect-technology-skills/SKILL.md. Its documented python3 fallback imports tomllib and PyYAML without declaring a compatible runtime or package prerequisite. An available Python 3.9 runtime can therefore fail before returning a detection outcome.

## Source Evidence

The user authorized immediate creation of independently dispatchable Defect records for every accepted skill-lint finding on 2026-07-28. The accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records the skill locations at skills/detect-technology-skills/SKILL.md:16,31-40 and import evidence at skills/detect-technology-skills/scripts/detect.py:15,18. Independent reviewer /root/confirm_critical_b accepted it as CONFIRMED_CRITICAL.

## Requirements

- Declare executable runtime and package prerequisites for the documented fallback, or provide a compatible fallback.
- Preserve deterministic READY, BLOCKED, and NO_VARIANT outcomes.
- Keep generated-mirror ownership boundaries intact.

## Acceptance Criteria

- The exact documented fallback runs on every declared supported runtime.
- Missing prerequisites produce a documented bounded result rather than an import failure.
- READY, BLOCKED, and NO_VARIANT cases remain covered.

## Dependencies

None

## Verification

- Run the fallback under every declared supported runtime.
- Cover READY, BLOCKED, and NO_VARIANT outcomes.
- Run focused detector tests and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None.

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/detect-technology-skills/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check. If a source change requires a supported mirror refresh, implementation must follow the approved source-category relationship.
