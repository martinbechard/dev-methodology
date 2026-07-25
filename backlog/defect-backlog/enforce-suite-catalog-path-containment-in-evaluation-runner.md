# Enforce Suite-Catalog Path Containment In Evaluation Runner

Status: Ready

Type: Defect

Owner: Unassigned

Provider: file

Provider Reference: backlog/defect-backlog/enforce-suite-catalog-path-containment-in-evaluation-runner.md

Completion: direct-main

## Summary

Reject a suite-index path that is not a contained, non-symlink suite directory before the evaluation runner probes suite.yaml or scenarios.yaml outside the canonical suite root.

## Context

The evaluation runner validates selected suite IDs but _load_catalog joins each raw suite-index.yaml entry path directly to its suite root and then loads suite.yaml and scenarios.yaml. A safe suite ID paired with path: ../outside therefore makes the runner probe outside the suite root. This is a catalog-entry path-resolution defect, not the active suite/scenario identifier and scenario-audit-root containment defect.

## Source Evidence

Delegated user direction in canonical task 019f97d7-41ce-7763-a8fc-75f1be68a82d explicitly requires every additional confirmed distinct defect to be logged durably rather than as a warning. Fresh inspection of evals/agent-tests/runner.py confirms that _load_catalog validates IDs at lines 354 through 365, joins the raw entry path at line 366, and loads suite.yaml and scenarios.yaml at lines 367 and 368 without containment validation.

## Requirements

- Validate every suite-index entry path before constructing a suite manifest or scenario-catalog path.
- Reject traversal, absolute, empty, malformed, or resolved paths that escape the canonical suite root.
- Reject a suite path that resolves through a symlink outside the canonical suite root.
- Ensure rejection occurs before any filesystem probe of suite.yaml or scenarios.yaml outside the canonical suite root.
- Preserve loading of valid contained suite directories.

## Acceptance Criteria

- A valid suite ID paired with path: ../outside is rejected before any outside-root suite.yaml or scenarios.yaml probe.
- Absolute, separator-based traversal, and malformed catalog paths are rejected before an outside-root probe.
- A catalog path whose resolved directory escapes through a symlink is rejected before an outside-root probe.
- Valid suite-index entries whose resolved directories remain inside the canonical suite root continue to load and validate.
- Focused regressions prove rejection-before-probe and resolution containment for traversal and symlink cases.

## Dependencies

None.

## Verification

- Add focused evals/agent-tests/test_runner.py regressions using a temporary suite root and an instrumented loader or equivalent evidence that no outside-root manifest or scenario-catalog path is read.
- Run the focused evaluation-runner catalog-loading regressions.
- Run git diff --check.
- Obtain independent code and security review of the containment boundary.

## Open Questions

None.

## Notes

Coordinate any shared evals/agent-tests/runner.py ownership with backlog/defect-backlog/enforce-scenario-root-containment-in-evaluation-runner.md. This item must remain a separate delivery: it governs raw suite-index path resolution, while that active item governs suite/scenario identifiers and scenario audit roots. This transaction records the defect only and does not implement the runner change.
