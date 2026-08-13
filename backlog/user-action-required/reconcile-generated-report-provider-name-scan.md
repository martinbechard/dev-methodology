# Reconcile The Generated Report Provider Name Scan

Status: User Action Required

Type: Defect

Provider: file

Work Item ID: reconcile-generated-report-provider-name-scan

Completion: main-branch

## Summary

Make the canonical work-item creation-name test handle generated backlog reports without accepting retired provider identities in maintained source.

## Context

`BundleContentTests.test_work_item_creation_interface_and_provider_names_are_canonical` currently scans generated reports under `.agents/temp/backlog-dispatcher` and `.codex/reports`. Those reports contain retired creation-provider names, so the focused bundle test fails even though the STE candidate changed only test expectations.

## Source Evidence

Dev Verifier confirmed this independent baseline defect on 2026-08-13 while verifying `establish-ste-technical-documentation-standard`. The same six generated-report matches reproduce without the STE correction.

## Requirements

- Determine whether generated backlog reports must be regenerated, excluded as ephemeral output, or validated through a separate generated-output contract.
- Preserve the negative scan for retired provider identities in maintained current source.
- Prevent local report timing from making the bundle test nondeterministic.
- Keep this correction separate from the STE delivery.

## Acceptance Criteria

- The canonical creation-provider-name test passes with current generated reports present.
- Retired provider identities in maintained source still fail the test.
- The chosen boundary is deterministic across clean and report-populated checkouts.
- Fresh code review and verification pass.

## Dependencies

None.

## Verification

- Run `python3 -m unittest scripts.test_bundle_content.BundleContentTests.test_work_item_creation_interface_and_provider_names_are_canonical` with and without generated reports present.
- Run focused provider-family naming and backlog-report tests.
- Run Git diff checks and obtain fresh independent review and verification.

## Open Questions

Should the test ignore ephemeral report roots, or should report generation replace retired provider names before the scan runs?

## User Action Required

### Question for the User

Do you authorize implementation of this independently discovered provider-name scan defect?

### Why User Input Is Required

The STE work item did not authorize unrelated report-generation or provider-scan corrections. Creating this record preserves the defect without expanding that delivery.

### Options and Tradeoffs

- Approve implementation: move this item to the active defect backlog and correct the boundary through normal review and verification.
- Defer implementation: move this item to Holding and preserve the known failing baseline.
- Reject implementation: archive the item as abandoned and retain the generated-report failure.

### Resolution

Pending.

### Unattended Work Boundary

Do not change report generation, provider-name scans, or generated reports until the user answers. Read-only diagnosis may continue.
