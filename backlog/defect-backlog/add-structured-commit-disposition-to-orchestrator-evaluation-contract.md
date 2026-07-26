# Add A Clear Delivery Result To The Orchestrator Evaluation

Status: Running

Type: Defect

Owner: Dev Orchestrator

Provider: file

Provider Reference: backlog/defect-backlog/add-structured-commit-disposition-to-orchestrator-evaluation-contract.md

Completion: direct-main

## Problem

The Dev Orchestrator evaluation says that the configured delivery workflow returns `READY`.
That word is misleading because `Ready` normally means that work has not started.

The evaluation also describes this result with terms such as “Commit disposition” and
“receipt.” Those terms hide a simple decision: did delivery finish successfully?

## Required Change

The configured delivery workflow must return exactly one structured result:

- `COMPLETED`: delivery finished successfully.
- `NEEDS_REVIEW`: delivery is waiting for a required review or user decision.
- `BLOCKED`: delivery cannot continue because of a stated technical or external blocker.

The Dev Orchestrator must ask the Dev Backlog Steward to close the work item only after
the delivery workflow returns `COMPLETED`.

`NEEDS_REVIEW` and `BLOCKED` must leave the work item open.

Use the term “delivery result.” Do not call it a Commit receipt or Commit disposition.

## Acceptance Criteria

- The dependency-routing evaluation reports a structured delivery result.
- `COMPLETED` permits the existing closeout step.
- `NEEDS_REVIEW` prevents closeout.
- `BLOCKED` prevents closeout.
- A missing or unknown delivery result fails the evaluation.
- Focused tests cover all four cases.

## Scope

- Dev Orchestrator suite-local contract, scenario, fixture, and focused tests.
- The evaluator code needed to validate the structured delivery result.

No conceptual agent definition or distributed skill definition changes are required.

## Prior Attempts

Earlier candidates added extensive Git-history and provider-receipt validation. Reviews
rejected those candidates. Do not reuse or integrate them.

This implementation starts from current main and validates only the plain delivery-result
contract above.

## Verification

- Run the focused Dev Orchestrator fixture tests.
- Run the evaluator tests that directly consume the delivery result.
- Run Python compilation and `git diff --check`.

## Delivery Mode

The user directed temporary single-task delivery without claims or delegated agents.
