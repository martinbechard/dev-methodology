# Add Structured Commit Disposition To Orchestrator Evaluation Contract

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/add-structured-commit-disposition-to-orchestrator-evaluation-contract.md

Completion: direct-main

## Summary

Make the Dev Orchestrator evaluation contract represent the structured effective-Commit disposition that its suite skill promises, rather than binding final verification directly to Dev Backlog Steward closeout without a Commit receipt.

## Context

The Dev Orchestrator suite skill promises a structured effective-Commit disposition. Its scenario and report schema contain no Commit receipt, however, and deterministically bind final verification directly to Dev Backlog Steward closeout. This makes the evaluated contract unable to demonstrate the promised Commit decision boundary.

## Source Evidence

Fresh independent prompt-review finding from canonical task 019f96ce-b1a0-7633-97ab-336ba7d188e4. Read-only search found no matching active or completed record. This item records the finding only and authorizes no unrelated fix.

## Requirements

- Identify the suite skill, scenario, report schema, and judge/supervisor surfaces that promise or consume the effective-Commit disposition.
- Add an explicit structured Commit receipt or equivalent evidence boundary before final verification and Dev Backlog Steward closeout.
- Preserve the existing separation between implementation, review, verification, Commit application, and provider lifecycle mutation.
- Keep closeout blocked when the required effective-Commit disposition is absent or inconsistent.
- Obtain exact canonical-path approval before changing any governed definition source.

## Acceptance Criteria

- The Dev Orchestrator evaluation can observe and judge a structured effective-Commit disposition.
- Final verification and Dev Backlog Steward closeout are ordered after the recorded Commit disposition.
- A missing, rejected, or inconsistent Commit receipt produces an evidence-backed non-success verdict.
- Focused scenarios and report-schema checks cover the receipt and ordering contract.

## Dependencies

None.

## Verification

- Run focused Dev Orchestrator suite scenarios and report-schema tests.
- Run the relevant evaluator, bundle-content, and generated-definition freshness checks.
- Obtain fresh independent review.

## Open Questions

- Which existing structured handoff schema is the narrowest authoritative representation for the effective-Commit disposition?

## Notes

Do not implement this finding as part of unrelated candidate work. Governed-definition changes require a successful exact-path approval-manifest check before mutation.
