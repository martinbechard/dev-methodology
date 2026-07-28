# Resolve the project-wiki template from the installed skill catalog

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/make-project-wiki-template-resolution-install-portable.md

Completion: direct-main

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
