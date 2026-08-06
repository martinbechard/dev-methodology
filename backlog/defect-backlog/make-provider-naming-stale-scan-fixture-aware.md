# Make Provider Naming Stale Scan Fixture-Aware

Status: Running

Type: Defect

Provider: file

Work Item ID: make-provider-naming-stale-scan-fixture-aware

Completion: direct-main

Owner: Dev Orchestrator task 019fd939-f5eb-7743-b023-6e9dc98c555e

Phase: Verifying

Branch: codex/make-provider-naming-stale-scan-fixture-aware-019fd939

Worktree: /Users/martinbechard/.codex/worktrees/6c31/dev-methodology

Canonical Conversation: Retained conversation for Codex task 019fd939-f5eb-7743-b023-6e9dc98c555e; the runtime exposes no separate conversation identifier.

Codex Task ID: 019fd939-f5eb-7743-b023-6e9dc98c555e

Root Role: Dev Orchestrator

Parent Task ID: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Accepted Candidate Commit: e22f92ccb992cc8a121f84096c6a159cc02caf69

Independent Review: GOOD; no material findings; exact scope, seven fixture allowances, exact accounting, unexpected-identity regression, fixture preservation, and focused candidate evidence accepted.

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

## Starting Handoff Evidence

Starting Recorded At: 2026-08-06T22:37:10Z

Coordinator: Dev Backlog Coordinator task 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Normalized Objective: Make the provider-name stale-reference scan recognize only exact deliberate negative-test fixtures while continuing to reject real retired identities and broad test-module exclusions.

Launch Result: Started.

Canonical Execution: Codex task 019fd939-f5eb-7743-b023-6e9dc98c555e.

Last Contact At: 2026-08-06T22:40:32Z.

Next Reconciliation At: 2026-08-06T22:52:10Z.

Intended Root Role: Dev Orchestrator.

## Active Execution Evidence

Condition Type: root-execution

Owner: Dev Orchestrator task 019fd939-f5eb-7743-b023-6e9dc98c555e

Evidence: The canonical Codex task accepted immutable candidate e22f92ccb992cc8a121f84096c6a159cc02caf69 after one fresh independent GOOD review and is actively dispatching the one focused verifier.

Observed At: 2026-08-06T22:54:15Z

Started At: 2026-08-06T22:40:32Z

Deadline or Expires At: 2026-08-06T23:54:15Z

Next Action: Dispatch one independent verifier against the immutable candidate, then reconcile current main once for direct-main delivery if verification passes.

Next Reconciliation At: 2026-08-06T23:09:15Z
