# Make the technology detector fallback prerequisites executable

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/make-technology-detector-fallback-prerequisites-executable.md

Completion: direct-main

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

None. Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

## Verification

- Run the fallback under every declared supported runtime.
- Cover READY, BLOCKED, and NO_VARIANT outcomes.
- Run focused detector tests and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None.

## Notes

This record has one primary affected skill identity: skills/detect-technology-skills/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check. If a source change requires a supported mirror refresh, implementation must follow the approved source-category relationship.
