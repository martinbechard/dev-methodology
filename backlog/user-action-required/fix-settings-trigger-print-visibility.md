# Fix Settings Trigger Print Visibility

Status: User Action Required

Type: Defect

Provider: file

Work Item ID: fix-settings-trigger-print-visibility

Completion: main-branch

## Summary

Hide the injected documentation Settings trigger in printed output without weakening its interactive browser behavior.

## Context

Independent browser verification of `design/wiki-skills-and-project-context.html` confirmed that the injected Settings trigger remains visible in Letter-width print output. The injected class selector has greater specificity than the shared `button { display: none; }` print rule in `design/documentation-design-system/assets/design-system.css`.

This is a shared design-system defect. Correcting it in the page-specific alignment would broaden that Work Item beyond its accepted three-path plan and could affect every documentation page that loads `design/documentation-settings.js`.

## Source Evidence

Dev Verifier confirmed the print defect on 2026-08-13 while verifying candidate `da5f4f280454bc6962dc112f37761ca084786439` for Work Item `align-wiki-skills-and-project-context-with-documentation-design-system`.

## Requirements

- Correct the shared print rule so the injected Settings trigger is hidden in print output.
- Preserve the trigger's visible, keyboard-accessible behavior in interactive browser output.
- Apply the fix through the shared design-system source rather than a page-local override.
- Verify every maintained documentation page that loads the shared settings script.

## Acceptance Criteria

- Print preview and generated print output contain no Settings trigger.
- The Settings trigger remains visible and keyboard operable at supported interactive viewports.
- The settings dialog still moves, contains, and returns focus and closes with Escape.
- Shared design-system, settings, browser, print, and affected-page regression checks pass.

## Dependencies

None.

## Verification

- Run the focused design-system and settings unit tests.
- Verify interactive and print rendering on representative consuming documentation pages.
- Confirm no page-local print override is required.
- Obtain independent source review and browser verification.

## Open Questions

- Which shared selector provides the smallest specificity-safe correction without changing non-print behavior?

## User Action Required

### Question for the User

Do you authorize a separate shared design-system defect fix for the Settings trigger that remains visible in print output?

### Why User Input Is Required

The defect is confirmed, but its correction changes a shared asset outside the authorized page-specific alignment scope.

### Options and Tradeoffs

- Approve the separate defect: the shared print behavior can be corrected and verified across affected pages.
- Defer the defect: the current page alignment can remain delivered, while the known shared print issue remains recorded but inactive.

### Resolution

Pending.

### Unattended Work Boundary

Do not change the shared design-system CSS or settings script until the user approves this separate defect. Independent page-specific work may continue.

## Notes

- The originating page's table and content print within their wrapper without clipping.
- This item must not be used to reopen or broaden the completed page-specific content baseline.
