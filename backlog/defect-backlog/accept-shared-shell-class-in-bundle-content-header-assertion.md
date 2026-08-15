# Accept Shared Shell Class In Bundle Content Header Assertion

Status: Ready

Type: Defect

Provider: file

Work Item ID: accept-shared-shell-class-in-bundle-content-header-assertion

Completion: main-branch

## Summary

Correct the focused bundle-content header assertion so an HTML documentation page that adopts the accepted shared shell is recognized by its exact `site-header ds-header` class while legacy pages remain subject to their existing exact-shell validation.

## Context

The preserved candidate for `align-agent-and-skill-definitions-with-documentation-design-system` changes `design/agent-and-skill-definitions.html` from the legacy `site-header` shell to the accepted Documentation Design System `site-header ds-header` shell. Its source, artifact, Shared Documentation Design System, browser, and final verification gates all passed, but integration is deliberately blocked until the bundle-content test contract recognizes that accepted shell without weakening validation for either shell form.

This Defect owns only the obsolete assertion contract. It does not own the Definitions page, its browser scripts, its preserved candidate, or any broader Documentation Design System migration.

## Source Evidence

- The authoritative Definitions Work Item records preserved candidate `05b2bda3b929d8258a9a096b8dbc9870ab2d5629`, exact canonical task `019ffc29-0d20-78f1-b3d6-f0797e7bb5b6`, and PASS results for source review, artifact review, all ten Shared Documentation Design System checks, browser verification, and final verification.
- That provider record names the remaining integration prerequisite as one focused Defect for the obsolete exact-header assertion in `scripts/test_bundle_content.py`.
- The candidate uses exactly `<header class="site-header ds-header">` and `<footer class="site-footer ds-footer">`, while the bundle-content suite retains distinct validation for legacy `<header class="site-header">` pages and accepted shared-shell pages.
- On 2026-08-14, the Dev Backlog Coordinator authorized creation and immediate serialized delivery of this standalone Defect after the file-provider ordinary-creation capability became available.

## Requirements

- Change only the smallest assertion and focused test evidence required in `scripts/test_bundle_content.py`.
- Recognize the exact accepted shared-shell header class `site-header ds-header` where the corresponding page contract authorizes the shared shell.
- Preserve exact validation of the matching shared-shell footer and stylesheet ownership.
- Preserve the existing legacy-shell assertion for pages that have not adopted the shared shell.
- Add or retain negative coverage proving a missing, altered, duplicated, or misplaced shared-shell class is rejected where applicable.
- Do not weaken the page inventory, navigation, settings, accessibility, content-baseline, or shell-ownership assertions.
- Do not modify or recreate candidate `05b2bda3b929d8258a9a096b8dbc9870ab2d5629` or any of its four owned delivery paths.
- Keep the change independent from the blocked Definitions Work Item; delivery of this Defect is the observable trigger for that preserved task to resume integration.

## Acceptance Criteria

- The focused bundle-content assertion accepts an authorized page containing exactly one `<header class="site-header ds-header">` and its corresponding shared-shell footer and stylesheet.
- The same assertion rejects invalid shared-shell header variants and continues to reject legacy-shell drift.
- The preserved Definitions candidate can be evaluated against current main without an obsolete exact-header failure.
- No page, browser script, shared asset, generator, provider record other than this Work Item, or unrelated test contract changes.
- Fresh independent source review and focused verification accept the delivered correction.

## Dependencies

None.

## Verification

- Run the smallest focused `BundleContentTests` method that owns the documentation shell/header assertion.
- Run focused positive and adversarial cases for accepted shared-shell and legacy-shell classification.
- Evaluate the preserved Definitions page blob from candidate `05b2bda3b929d8258a9a096b8dbc9870ab2d5629` against the corrected assertion without mutating that candidate.
- Run `python -m py_compile scripts/test_bundle_content.py` and `git diff --check`.
- Obtain fresh independent source review before main-branch delivery.

## Open Questions

None.

## Coordination Notes

- Crisis epoch: `blocked-crisis-20260813T223935Z`.
- This Defect is the sole local serialized crisis execution after reservation.
- Crisis recovery is claim-free; do not perform any resource-claim operation.
- Preserve all unrelated dirty provider bytes, untracked plans and temporary evidence, historical worktrees, and crisis evidence.
