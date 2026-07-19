# Enforce Runnable Type Eligibility In Backlog Report

Status: Ready

Type: Defect

## Summary

Require the styled backlog report to classify an active Ready item as runnable only when its explicit Type is Defect, Feature, Analysis, or Investigation.

## Context

[Add A Styled Backlog Report With User Input](../feature-backlog/add-styled-backlog-report-with-user-input.md) is blocked after its bounded correction loop found one remaining P1 defect. The final preserved source commit 32fd01a7fe214d7f5acb9a1ca2976073722c13ec validates Type values but still derives runnable eligibility from active placement, Ready status, satisfied dependencies, and required fields without requiring a dispatchable Type.

As a result, a complete active Ready item whose Type is Holding or an invalid value such as Epic can inflate Runnable now and appear in Runnable Work. These items must remain visible in active inventory and lifecycle findings without becoming dispatchable.

The rejected source chain remains preserved in commits 381f09f557b7e73d07a9b735508687b2c27ac5f7, 8f7eb183846744180ee0ea3377ccbc7b072c5c60, and 32fd01a7fe214d7f5acb9a1ca2976073722c13ec. The independently accepted README contribution remains preserved in commit 69f0461f94c56737d696c6ad3adc2f71207df977. This defect supplies fresh bounded correction authority; it does not itself authorize integration of those commits.

## Requirements

- Require runnable eligibility to include an explicit Type of exactly Defect, Feature, Analysis, or Investigation.
- Keep active Ready items with Type Holding visible in active inventory and lifecycle anomaly reporting while excluding them from Runnable now and Runnable Work.
- Keep active Ready items with an invalid Type such as Epic visible in active inventory and lifecycle anomaly reporting while excluding them from Runnable now and Runnable Work.
- Preserve existing validation findings, type and status inventory, dependency reconciliation, deterministic ordering, and offline report behavior.
- Limit the correction to scripts/generate-backlog-report.py and scripts/test_generate_backlog_report.py unless new evidence is returned to the work-item owner before scope expansion.
- Do not change README.md, backlog/examples/styled-backlog-report.html, backlog lifecycle files, agent definitions, skill definitions, generated adapters, or approval-directive surfaces as part of the correction lane.

## Acceptance Criteria

- Runnable eligibility is true only for an active Ready item with satisfied dependencies, complete required metadata, and Type Defect, Feature, Analysis, or Investigation.
- A complete active Ready fixture with Type Holding contributes zero to Runnable now and does not appear in Runnable Work.
- A complete active Ready fixture with Type Epic contributes zero to Runnable now and does not appear in Runnable Work.
- The Holding fixture remains traceable in active inventory and produces its applicable lifecycle anomaly.
- The Epic fixture remains traceable in active inventory and produces the invalid Type lifecycle anomaly.
- Focused tests bound their Runnable Work assertions to that section so visibility elsewhere cannot mask accidental runnable placement.
- Existing focused generator tests continue to pass without weakened assertions.

## Dependencies

- [Rename User Review State For Clarity](../completed-backlog/defects/rename-user-review-state-for-clarity.md)

## Verification

- Add focused complete-metadata fixtures for active Ready items with Type Holding and Type Epic and no unmet dependencies.
- Assert the exact Runnable now count and absence of both fixtures from the bounded Runnable Work section.
- Assert the expected Holding placement or Type mismatch finding and the invalid Epic Type finding remain visible.
- Run the focused backlog report generator tests.
- Run Python compilation, Ruff, and Mypy checks applicable to the changed source and test files.
- Generate a controlled report and inspect its runnable metric, Runnable Work section, active inventory, and lifecycle findings.
- Run the applicable repository script tests and git diff --check.

## Notes

- This is directly authorized technical correction work. It is not User Action Required and has no unresolved user-owned decision.
- The blocked feature remains blocked until the corrected cumulative source, accepted documentation, example update, fresh reviews, complete verification, integration, and browser accessibility gates succeed.
- Use the simple-workitem process and return a verified local correction commit from a clean released artifact claim before integration is considered.
