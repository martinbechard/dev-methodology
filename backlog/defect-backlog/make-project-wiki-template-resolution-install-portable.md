# Resolve the project-wiki template from the installed skill catalog

Status: Running

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/make-project-wiki-template-resolution-install-portable.md

Completion: direct-main

Owner: Dev Orchestrator / root task 019faa18-fde1-7690-ba81-7eb1a23bf4cf

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-seven-batch2-defects-019fa9bb

Normalized Objective: Resolve the project-wiki template from the installed skill catalog.

Dispatch Time: 2026-07-28T18:56:59Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019faa18-fde1-7690-ba81-7eb1a23bf4cf

Root Agent Task: 019faa18-fde1-7690-ba81-7eb1a23bf4cf

Canonical Branch: codex/project-wiki-template-resolution-portable-019faa18

Assigned Worktree: /Users/martinbechard/.codex/worktrees/c5e3/dev-methodology

Current Phase: Read-only analysis pending definition-change authority.

Started At: 2026-07-28T19:03:10Z

Claim Evidence: running-project-wiki-template-resolution-019faa18 acquired as SHARED_CHECKOUT_ACQUIRED at 2026-07-28T19:03:10.486935Z; claim event a7ae62a2-3ac9-411b-bb9a-21601bd1c398.

Next Lifecycle Owner: Root Dev Orchestrator

## Summary

Make project-wiki creation resolve its template from the installed skill catalog instead of a dev-methodology source-checkout path.

## Context

The primary affected skill is skills/project-wiki-create/SKILL.md. It names a template location that exists only in the source checkout, so an installed skill cannot reliably locate the template. The separately proposed review-routing subfinding was rejected and is excluded from this item.

## Source Evidence

The user authorized immediate Ready Defect creation for independently confirmed skill-lint findings on 2026-07-28. Accepted report candidate 54d860f1978d4cb403e59162cfb209fe45cc06a8, at evals/results/2026-07-28-methodology-skill-lint.md, records the non-portable template finding for skills/project-wiki-create/SKILL.md. Independent reviewer /root/confirm_critical_c accepted the template-resolution defect as CONFIRMED_CRITICAL and rejected the separate review-routing subfinding.

## Requirements

- Resolve the template from the installed project-wiki skill catalog.
- Keep source-checkout and installed-target paths supported without hard-coded repository assumptions.
- Do not alter review-routing behavior under this item.

## Acceptance Criteria

- A source checkout and installed target both resolve a valid template.
- No dev-methodology-only absolute or source-root template path is required.
- Review-routing text remains out of this correction scope.

## Dependencies

None

## Verification

- Resolve the template from a source checkout and an installed target fixture.
- Confirm both resolve the same required template artifact.
- Run focused contract validation and git diff --check.
- Obtain independent review of the correction.

## Open Questions

None.

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/project-wiki-create/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check.
