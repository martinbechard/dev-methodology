# Enforce Scenario-Root Containment In Evaluation Runner

Status: Ready

Type: Defect

Owner: Unassigned

Provider: file

Provider Reference: backlog/defect-backlog/enforce-scenario-root-containment-in-evaluation-runner.md

Completion: direct-main

## Summary

Constrain evaluation-runner scenario roots to the canonical fixture root so untrusted suite or scenario identifiers cannot traverse through paths or symlinks into external Git metadata, expensive trees, or unrelated workspace state.

## Context

Pre-existing raw scenario identifiers have no safe path-component validation. Scenario audit roots can resolve or traverse outside the canonical fixture root through path escape or symlink escape. Fresh security review confirmed a risk of outside-workspace Git metadata probing, expensive traversal, and false evaluation failures. This defect is distinct from candidate-only none-audit bypasses and records current-main behavior only.

## Source Evidence

- Canonical user direction in task `019f979e-5330-7501-8340-92dfd593f6ef` requires every additional confirmed distinct defect to be logged durably.
- Fresh security review of the evaluation runner confirmed raw suite/scenario identifiers can influence scenario audit-root resolution without safe component validation.
- The review established path-traversal and symlink-escape routes outside the canonical fixture root.

## Requirements

- Validate suite and scenario identifiers as safe path components before any scenario-root construction.
- Precreate canonical scenario roots and reject roots that are symlinks.
- Enforce canonical fixture-root containment before execution and again after execution or audit-root resolution.
- Keep legitimate fixture scenarios runnable without probing unrelated workspace state.

## Acceptance Criteria

- Suite and scenario slugs that contain traversal, separators, absolute-path forms, or invalid components are rejected before filesystem probing outside the canonical fixture root.
- Canonical scenario roots are precreated as non-symlink directories.
- Resolved audit roots remain contained by the canonical fixture root before and after execution.
- Regression tests reject traversal and symlink escapes without outside-workspace Git metadata probing or expensive traversal.
- Valid in-root scenarios continue to pass their focused evaluation tests.

## Dependencies

None.

## Verification

- Run focused evaluation-runner scenario-root and audit tests.
- Add and run traversal, absolute-path, separator, and symlink-escape regressions.
- Verify valid fixture scenarios retain their expected results.
- Run `git diff --check` and obtain fresh independent security and code review.

## Open Questions

- Is the existing suite schema the narrowest authoritative place to define the portable suite and scenario slug grammar?

## Coordination Evidence

- Backlog claim `record-runner-review-defects-019f979e` acquired on primary main at 2026-07-25T05:39:43.871470Z; acquisition journal event `29dc95c6-c2ba-473b-8034-3420d7eecd6b`.

## Notes

This item is ready for independently scoped implementation. It does not authorize unrelated runner changes or governed-definition mutation without required approval evidence.
