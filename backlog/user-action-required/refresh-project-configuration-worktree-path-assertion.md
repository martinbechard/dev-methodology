# Refresh The Project Configuration Worktree Path Assertion

Status: User Action Required

Type: Defect

Provider: file

Work Item ID: refresh-project-configuration-worktree-path-assertion

Completion: main-branch

## Summary

Align the Project Configuration bundle assertion with the current portable rule for machine-specific worktree paths.

## Context

`BundleContentTests.test_project_configuration_routes_to_template_and_verifier` requires the obsolete sentence `Do not store a machine-specific absolute worktree path`. The current `create-project-configuration` skill preserves the rule with broader portable-path requirements, so the focused bundle test fails.

## Source Evidence

Dev Verifier confirmed this independent baseline defect on 2026-08-13 while verifying `establish-ste-technical-documentation-standard`. The failure reproduces on current `main` and is unchanged by STE correction candidate `6c6ee9ee193b89ba8aa3b92a29f4745e378efaea`.

## Requirements

- Identify the current canonical Project Configuration rule that prohibits machine-specific worktree paths.
- Update the stale bundle assertion to verify the current rule without weakening path-portability coverage.
- Keep Project Configuration behavior unchanged unless independent source evidence proves a contract defect.
- Keep this correction separate from the STE delivery.

## Acceptance Criteria

- The focused Project Configuration bundle test passes against current source.
- The assertion detects a regression that permits machine-specific absolute worktree paths.
- No unrelated bundle baseline is changed.
- Fresh code review and verification pass.

## Dependencies

None.

## Verification

- Run `python3 -m unittest scripts.test_bundle_content.BundleContentTests.test_project_configuration_routes_to_template_and_verifier`.
- Run applicable Project Configuration focused tests and Git diff checks.
- Obtain fresh independent review and verification.

## Open Questions

Which current sentence or semantic assertion gives the strongest stable coverage without binding the test to incidental wording?

## User Action Required

### Question for the User

Do you authorize implementation of this independently discovered Project Configuration test defect?

### Why User Input Is Required

The STE work item did not authorize unrelated Project Configuration corrections. Creating this record preserves the defect without expanding that delivery.

### Options and Tradeoffs

- Approve implementation: move this item to the active defect backlog and correct the stale assertion through normal review and verification.
- Defer implementation: move this item to Holding and preserve the known failing baseline.
- Reject implementation: archive the item as abandoned and retain the failure as accepted baseline behavior.

### Resolution

Pending.

### Unattended Work Boundary

Do not change Project Configuration source or tests until the user answers. Read-only diagnosis may continue.
