# Allow typed evidence in functional-specification review checklists

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/allow-typed-evidence-review-functional-spec.md

Completion: direct-main

## Summary

Allow typed evidence in functional-specification review checklists.

## Context

The primary affected skill is skills/review-functional-spec/SKILL.md. Quote-only evidence cannot truthfully represent missing behavior, absent examples, derived inventory reconciliation, or non-applicable interface conditions.

## Source Evidence

The user authorized this independently dispatchable Ready Defect record on 2026-07-28. The accepted methodology skill-lint report at evals/results/2026-07-28-methodology-skill-lint.md, commit 54d860f1978d4cb403e59162cfb209fe45cc06a8, records this finding at 30; skills/review-functional-spec/references/review-checklist-functional-spec.md:9-16,47-68; skills/documentation-page-verify/SKILL.md:58-60,67-70; skills/review-structured-artifact/SKILL.md:95-122. Independent reviewer /root/confirm_review_evidence_findings accepted it as CONFIRMED_CRITICAL.

## Requirements

- Use typed evidence and require literal resolution only when the evidence type is exact quotation.
- Preserve the documented ownership boundary and avoid unrelated provider, source, report, analysis, generated, or lifecycle mutation.

## Acceptance Criteria

- The skill and direct checklist accept typed evidence.
- Literal resolution is required only for exact-quotation evidence.
- The correction remains limited to the smallest source-backed scope.

## Dependencies

None

## Verification

- Cover quotation-backed evidence, an absence-based failure, and a conditional not-applicable result.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/review-functional-spec/SKILL.md. It does not authorize a skill-definition mutation. If correction changes this governed SKILL.md, later implementation requires explicit scope-specific user approval naming that exact definition, a provenance approval record, and the supported pre-mutation definition-change check. Any additionally changed governed SKILL.md requires its own separate exact-path approval and check.
