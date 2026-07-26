# Run Focused Tests Per Work Item And One Combined Regression

Status: Running

Type: Feature

Owner: Dev Orchestrator

Provider: file

Provider Reference: backlog/feature-backlog/adopt-campaign-candidate-integration-and-deployment.md

Completion: direct-main

## Summary

Run focused tests for each work item, merge each accepted change to main independently, and run one system-wide regression after the related set of changes has been integrated.

## Context

System-wide test suites can be much slower than the focused tests for one changed skill, API, or component. Running the complete suite for every individual work item wastes time without improving the evidence for that specific change.

For example, when work items change three APIs in a system containing twenty APIs, each API change should run its own focused tests and merge after acceptance. The full API or system regression should run once after all three changes are present on main.

## Requirements

- Have the Dev Orchestrator select focused tests from the behavior and dependency paths changed by its work item.
- Run the focused tests, review, and verification required for that individual change.
- Merge each accepted work item to main independently after its focused delivery checks pass.
- Do not require the full system-wide regression for every individual work item.
- Have the Dev Backlog Coordinator track the related work items that form one combined regression set.
- After every selected work item has merged successfully, have the Coordinator schedule one system-wide regression against the combined main state.
- Run the combined regression from the main commit containing all selected changes.
- Record the exact main commit and the selected work items covered by the combined regression.
- When the combined regression finds a distinct defect, record that defect against the integrated main state and route it normally.
- Do not use a special integration finalizer, delay otherwise-ready individual merges, or replace per-item focused verification with the later regression.

## Acceptance Criteria

1. Each work item runs tests focused on its changed behavior and direct consumers.
2. Each accepted work item can merge to main without running an unrelated full-system suite.
3. The Coordinator knows which related work items must merge before the combined regression starts.
4. The combined regression runs once against a main commit containing every selected change.
5. Regression evidence identifies the tested main commit and included work items.
6. A combined-regression failure is investigated and recorded without invalidating unrelated focused evidence automatically.
7. The workflow works for both methodology changes, such as several skills, and product changes, such as several APIs.

## Verification

- Test a related set in which each work item completes focused verification and merges independently.
- Test that the combined regression does not start before all selected items are on main.
- Test that the combined regression runs once after the final selected merge.
- Test recorded coverage of the exact integrated main commit and work-item set.
- Test routing of a distinct failure found only by the combined regression.
- Run git diff --check.

## Dependencies

None.

## Superseded Implementation History

Candidate 6ab5976a and the previous campaign-finalizer design treated combined delivery as a special integration and deployment transaction with relational receipts, hashes, and deployment sentinels. That design is superseded and must not be reused.

The revised work is about test scope and timing. Individual accepted changes still merge normally. The Coordinator schedules one broader regression only after the related changes are integrated.
