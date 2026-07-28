# Allow typed evidence in architecture review checklists

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/allow-typed-evidence-review-architecture.md

Completion: direct-main

## Summary

Allow typed evidence in architecture review checklists.

## Context

The primary affected skill is skills/review-architecture/SKILL.md. The package requires exact quotation for every applicable result, including absence-based and derived structural conclusions that have no literal target text.

## Source Evidence

The user authorized this independently dispatchable Ready Defect record on 2026-07-28. The accepted methodology skill-lint report at evals/results/2026-07-28-methodology-skill-lint.md, commit 54d860f1978d4cb403e59162cfb209fe45cc06a8, records this finding at 30; skills/review-architecture/references/review-checklist-architecture.md:9-16; skills/documentation-page-verify/SKILL.md:58-60,67-70; skills/review-structured-artifact/SKILL.md:95-122. Independent reviewer /root/confirm_review_evidence_findings accepted it as CONFIRMED_CRITICAL.

## Requirements

- Use the shared typed-evidence model and allow explained not-applicable results without quotation.
- Preserve the documented ownership boundary and avoid unrelated provider, source, report, analysis, generated, or lifecycle mutation.

## Acceptance Criteria

- The skill and direct checklist accept typed evidence.
- Literal quotation, absence-based findings, and explained not-applicable results are represented truthfully.
- The correction remains limited to the smallest source-backed scope.

## Dependencies

None

## Verification

- Cover a literal quotation, an absence-based failure, and a conditional not-applicable result.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/review-architecture/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check. Any additionally changed governed SKILL.md requires its own separate exact-path approval and check.
