# Parse Nested User Action Required Report Fields

Status: Ready

Type: Defect

Provider: file

Work Item ID: parse-nested-user-action-required-report-fields

Completion: main-branch

## Summary

Make the backlog report read canonical nested User Action Required questions and resolutions.

## Source Evidence

On 2026-08-13, the user reported that the backlog report falsely renders both fields as Missing. Repository diagnosis confirmed that `scripts/generate-backlog-report.py::_parse_document` extracts only `##` sections, while canonical records place `### Question for the User` and `### Resolution` under `## User Action Required`.

## Requirements

- Change only `scripts/generate-backlog-report.py` and `scripts/test_generate_backlog_report.py`.
- Parse canonical nested `### Question for the User` and `### Resolution` fields within `## User Action Required`.
- Preserve existing top-level section parsing and non-UAR report behavior.
- Add focused regression cases for populated nested fields and genuinely missing fields.
- After accepted delivery, regenerate only the user-requested temporary backlog report; do not commit the temporary report unless its owning contract explicitly requires that result.

## Acceptance Criteria

- Canonical UAR records render their actual question and resolution instead of Missing.
- A genuinely absent nested question or resolution still renders Missing.
- Existing report sections and lifecycle grouping remain unchanged.
- Focused parser/report tests and independent review and verification pass.

## Dependencies

None.

## Verification

- Run focused `scripts.test_generate_backlog_report` tests.
- Generate a temporary report from current provider records and inspect both UAR cases.
- Run Python compile and Git diff whitespace checks.
- Obtain fresh independent source review and verification.

## Open Questions

None.

## Notes

- This item may run concurrently after the already-Starting `document-external-terminal-cleanup` launch is reconciled because its exact parser/test paths do not overlap that item's governed documentation, role, adapter, or generated-projection paths.
