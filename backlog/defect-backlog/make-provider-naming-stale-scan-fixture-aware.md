# Make Provider Naming Stale Scan Fixture-Aware

Status: Ready

Type: Defect

Provider: file

Work Item ID: make-provider-naming-stale-scan-fixture-aware

Completion: direct-main

## Summary

Make the work-item provider-name stale-reference check distinguish deliberate invalid-name fixtures from maintained canonical references without weakening detection of real retired identities.

## Context

The bundle-content check BundleContentTests.test_work_item_creation_interface_and_provider_names_are_canonical scans maintained repository text for retired creation-provider identities. The focused provider-family naming tests intentionally contain those same invalid identities as negative fixtures. The scanner currently treats all seven fixture literals as stale maintained references, so the canonical bundle assertion fails even though the provider-family validator is correctly testing rejection behavior.

The failure is in test-support classification, not in the current provider identities or the installed-skill synchronization outcome. The installation work item must preserve repository source and must not absorb this correction.

## Source Evidence

On 2026-08-06, canonical task 019fd919-a1d4-7471-b158-5068c1d7622d reproduced:

```text
python3.11 -m unittest scripts.test_bundle_content.BundleContentTests.test_work_item_creation_interface_and_provider_names_are_canonical
```

The assertion reported seven violations in scripts/test_provider_family_naming.py at lines 222, 236, 239, 271, 274, 298, and 301. Each occurrence is an intentional negative-test fixture for create-*-work-item or create-file-work-item. The user has an established direction that confirmed incorrect behavior must be logged rather than ignored, and the active task explicitly requested routing this source-test defect as a distinct work item.

## Requirements

- Make the stale-reference scanner recognize only explicitly identified deliberate negative-test literals or fixture regions.
- Keep production documentation, skills, generated artifacts, evaluation inputs, and ordinary test-support references subject to stale-name detection.
- Do not exclude the entire scripts/test_provider_family_naming.py module or introduce a broad filename, directory, or substring bypass.
- Keep allowance accounting exact so a removed fixture, duplicated allowance, or unexpected new retired identity remains observable.
- Preserve the canonical provider-family validator's negative cases and current provider identities unchanged unless a focused test proves a fixture correction is required.
- Keep this correction separate from installed-skill deployment, catalog refresh, and unrelated documentation wording.

## Acceptance Criteria

- The focused bundle-content test passes while all seven deliberate negative fixtures remain executable.
- The directly implicated provider-family naming module passes.
- A focused regression proves that an unapproved retired identity added outside the exact negative-fixture allowance still fails the stale-reference scan.
- A focused regression proves that broad exclusion of the whole provider-family naming test module is not accepted.
- No maintained canonical source or generated artifact gains a retired provider identity.

## Dependencies

None.

## Verification

- Run the focused bundle-content provider-name assertion before and after the correction.
- Run scripts.test_provider_family_naming under the repository Python 3.11 runtime.
- Run only the focused fixture-aware stale-reference regressions and git diff --check.
- Obtain fresh independent review and focused verification before direct-main delivery.

## Open Questions

None.

## Notes

The acknowledged unstaged wording change in design/skill-groups/concurrent-tasking.md is unrelated user-owned state and must remain untouched.
