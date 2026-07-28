# Keep Quarkus persistence companion selection setup-owned

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/keep-quarkus-persistence-companion-selection-setup-owned.md

Completion: direct-main

## Summary

Keep Quarkus persistence companion selection setup-owned.

## Context

The primary affected skill is skills/quarkus-persistence/SKILL.md. The package repeatedly directs ordinary runtime actors to select a blocking persistence companion from source evidence even though setup-time detection owns that decision and intentionally distinguishes blocking from reactive Panache.

## Source Evidence

The user authorized this independently dispatchable Ready Defect record on 2026-07-28. The accepted methodology skill-lint report at evals/results/2026-07-28-methodology-skill-lint.md, commit 54d860f1978d4cb403e59162cfb209fe45cc06a8, records this finding at 16; skills/quarkus-persistence/references/persistence-guidelines-quarkus.md:20; skills/quarkus-persistence/references/review-checklist-quarkus-persistence.md:4. Independent reviewer /root/confirm_new_routing_findings accepted it as CONFIRMED_CRITICAL.

## Requirements

- Consume only an active-scope companion already supplied by setup and report missing or stale routing.
- Preserve the documented ownership boundary and avoid unrelated provider, source, report, analysis, generated, or lifecycle mutation.

## Acceptance Criteria

- Runtime work never invents a persistence companion.
- Setup-owned blocking and reactive routing remains distinct in the skill, guideline, and direct checklist.
- The correction remains limited to the smallest source-backed scope.

## Dependencies

None

## Verification

- Preserve blocking and reactive detector cases.
- Assert that runtime work never invents a companion.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/quarkus-persistence/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check. Any additionally changed governed SKILL.md requires its own separate exact-path approval and check.
