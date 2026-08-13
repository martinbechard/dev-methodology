# Parse Nested User Action Required Report Fields

Status: Ready

Type: Defect

Provider: file

Work Item ID: parse-nested-user-action-required-report-fields

Completion: main-branch

## Summary

Make the backlog report read canonical nested User Action Required fields and distinguish provider lifecycle from observed canonical runtime activity.

## Source Evidence

On 2026-08-13, the user reported that the backlog report falsely renders both fields as Missing. Repository diagnosis confirmed that `scripts/generate-backlog-report.py::_parse_document` extracts only `##` sections, while canonical records place `### Question for the User` and `### Resolution` under `## User Action Required`.

## Requirements

- Change only `scripts/generate-backlog-report.py` and `scripts/test_generate_backlog_report.py`.
- Parse canonical nested `### Question for the User` and `### Resolution` fields within `## User Action Required`.
- Preserve existing top-level section parsing and non-UAR report behavior.
- Add focused regression cases for populated nested fields and genuinely missing fields.
- For every Work Item whose provider evidence assigns a canonical task, conversation, thread, or collaboration execution identity, render the latest supported runtime update time, observed runtime state, observation source, and a clear `Actually running` indicator.
- Resolve runtime observations only through exact canonical identities retained in authoritative Work Item assignment fields. Never infer or match identity from a title.
- Keep provider lifecycle and runtime observation separate: provider Running does not imply an execution is currently live, and a runtime status does not change provider lifecycle.
- Accept a supported runtime snapshot captured by the caller or report environment, with explicit snapshot time and source. Validate its bounded structure and exact identity keys before use.
- Preserve offline usefulness: when no snapshot exists, an identity is absent from it, or the runtime cannot expose a required field, render `Unavailable` with the snapshot/source boundary rather than guessing.
- Define `Actually running` only from a supported live/in-progress runtime state observed for the exact assigned identity. Render a truthful negative or unavailable result for idle, interrupted, terminal, archived/notLoaded, absent, or unobservable identities.
- Do not perform live task-control mutations, title lookup, or runtime polling from the report generator.
- After accepted delivery, regenerate only the user-requested temporary backlog report; do not commit the temporary report unless its owning contract explicitly requires that result.

## Acceptance Criteria

- Canonical UAR records render their actual question and resolution instead of Missing.
- A genuinely absent nested question or resolution still renders Missing.
- Assigned canonical identities display exact runtime identity, last update, state, observation source/time, and an unambiguous actually-running result.
- Provider Running paired with live/in-progress, idle, interrupted, terminal/notLoaded, missing, and unavailable runtime observations renders each distinction correctly.
- No runtime observation is attached through title similarity or another Work Item's identity.
- A report generated without runtime evidence remains complete offline and labels runtime fields unavailable.
- Existing report sections and lifecycle grouping remain unchanged.
- Focused parser/report tests and independent review and verification pass.

## Dependencies

None.

## Verification

- Run focused `scripts.test_generate_backlog_report` tests.
- Generate a temporary report from current provider records and a caller-supplied runtime snapshot; inspect both UAR cases and representative live, idle, terminal, missing, and unavailable assignments.
- Run Python compile and Git diff whitespace checks.
- Obtain fresh independent source review and verification.

## Open Questions

None.

## Notes

- This item may run concurrently after the already-Starting `document-external-terminal-cleanup` launch is reconciled because its exact parser/test paths do not overlap that item's governed documentation, role, adapter, or generated-projection paths.
- Exact source scope remains `scripts/generate-backlog-report.py` and `scripts/test_generate_backlog_report.py`. Runtime snapshot fixtures must be created inside test-owned temporary directories rather than added as durable source files.
- The user-requested temporary report is regenerated only after accepted delivery and remains an uncommitted output unless an owning contract explicitly requires otherwise.

## Scope Expansion Evidence

- Approved At: 2026-08-13T01:30:37Z.
- User Direction: Add exact-identity runtime update, state, and actually-running reporting while preserving truthful offline behavior.
- Concurrency Decision: Safe to run concurrently with `document-external-terminal-cleanup`; no exact source, test, generated-projection, or integration path overlap exists. The blocked dependency-policy item remains preserved and does not own these paths.
- Transition Claim: `expand-backlog-report-runtime-state-019ff2c3`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `06a0eca7-d485-4cae-8bea-7f643cc9fa9f`.
