# Enforce Methodology Review Checklist Completion

Owner: Unowned

Status: Ready

Type: Defect

Provider: file

Work Item ID: enforce-methodology-review-checklist-completion

Completion: main-branch

## Summary

Require Methodology Artifact Reviewer results to complete and save the existing structured-review checklist before returning findings.

## Context

The reviewer loaded the required checklist but returned NEEDS_CORRECTION findings without saving a completed checklist. Its findings also omitted the checklist question, authority, evidence, correction, and impact required by the existing template. The checklist already defines the required review method; this defect must enforce it without redesigning or expanding the checklist.

## Source Evidence

The user identified the incomplete Methodology Artifact Review on 2026-08-10 and clarified: “I only want it to use the existing checklist.”

## Requirements

- Clarify that read-only review prohibits changing the candidate, not writing the authorized checklist and findings artifacts.
- Add the completed existing checklist to the Methodology Artifact Reviewer output contract.
- Require every NEEDS_CORRECTION finding to reference its checklist question and retain the existing authority, evidence, correction, and impact fields.
- Treat a missing or incomplete saved checklist as an invalid review result.
- Do not add, redesign, or expand checklist questions.

## Acceptance Criteria

- A Methodology Artifact Reviewer cannot return a valid verdict before saving the completed existing checklist.
- Focused contract coverage rejects findings that are not derived from the saved checklist or omit its required fields.
- The existing structured-review checklist questions remain unchanged.

## Dependencies

None.

## Verification

- Run focused Methodology Artifact Reviewer role and evaluation-contract tests.
- Regenerate affected role projections through the repository-authorized generator and check freshness.
- Run Git diff checks.

## Open Questions

None.
