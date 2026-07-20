# Enforce Runnable Type Eligibility In Backlog Report

Status: Completed

Type: Defect

## Completion Evidence

- Accepted report bytes are integrated on main in commits ba86db7712b77a54dba525714ce70156b51f73a9 and 5514063bb51a56cbd8b667bcf49aa34fca329d06. Their stable patch identities exactly match accepted candidate commits 8482993557dc98dcfc6bd06ec83f8172d4090b7b and 6991c5daae2fa6cf01f8daa56b256f55d403121e.
- The final report corrections are carried by accepted contributions 095bbd9388be69df6b3250aed3c2a2d49ca705d9 and 4649a2fcfee5e88c3cef6048c3a7f8a0b0b1eb61.
- Focused verification passed 22 backlog-report tests. The retained full-candidate and browser evidence remains applicable by exact byte identity.
- Fresh post-integration review of the exact integrated candidate reported no findings.
- Integration ownership for main was released in event dfa15ec8-93d8-45ff-bada-57424517ae2a, and main was clean at 5514063bb51a56cbd8b667bcf49aa34fca329d06 before terminal lifecycle recording began.
- The earlier blocked and exhausted-correction evidence below is historical and superseded by the accepted resumed contribution, verification, integration, browser evidence, and review recorded here.

## Running Ownership

- Owner: Dev Orchestrator root task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Lifecycle claim: backlog-runnable-type-defect-start.
- Claim evidence: dev-backlog-steward acquired PRIMARY ownership of this exact backlog item at 2026-07-19T07:22:27.751764Z before recording the Running transition.
- Scope boundary: this lifecycle claim is released after the committed transition; project-artifact ownership must be acquired separately after ARTIFACT GO.

## Blocked Evidence

- Outcome: The bounded two-attempt post-integration correction authority ended with a failed fresh review. No third correction attempt was opened.
- Accepted source integration: commits 0c5f4022dcd7e31fed505226b5e67ebc83bc8833, 461cd758110a03da31951486d1d613f622e548ec, ef1cb76f30748f9c465dd160b4edd89feb3f312f, and 82bde3ec0557fb04015f8801bf4640ae7f5a1792 integrated the preserved source chain and exact runnable-Type correction on main.
- Accepted documentation integration: commit ebe0dc09a00364281002b73806c216dfa13cf1e3 integrated the independently reviewed README contribution.
- Post-integration correction one: source commit 3daa41db0ce7225fc0363f3c18335c75702c3619 passed fresh review and verification and was integrated on main as 634d7f6942b6b73c01436f7d21e37c213c3944e3.
- Example integration: commits 0abe77ba8dbea4f682e42fc934e9c7fbea1c7b29 and 07f2e5a8c99fa28398050e9a6ad923eab6f0ea01 refreshed and then curated the committed visual reference. Main remains at 07f2e5a8c99fa28398050e9a6ad923eab6f0ea01 before this lifecycle-only transition.
- Preserved failed correction: commit 792371d803a483cf7c6ce3239aad498be542a69a remains clean and unintegrated on branch codex/enforce-runnable-type-eligibility-post-integration-correction2. Its producer claim released under event 6674c4b1-ae6e-4b9c-ac27-acd9e2b1509d.
- Final fresh-review failure: an external prerequisite containing a local Markdown link inside larger prose can still be reduced to the local slug and falsely satisfied by a completed item. A query-bearing Markdown URL can still lose its original text and be reported as an invalid identifier instead of remaining a complete manual prerequisite.
- Missing regression boundary: the failed correction does not prove whole-declaration Markdown-link matching or preservation and manual classification of query-bearing Markdown URLs.
- Unrun gates: correction attempt two was not integrated, the example was not refreshed against it, browser and accessibility checks were not run, complete final primary-worktree verification was not accepted, and neither this defect nor the parent feature was archived as Completed.
- Lifecycle boundary: [Add A Styled Backlog Report With User Input](../feature-backlog/add-styled-backlog-report-with-user-input.md) was already Blocked and was not changed by this terminal transition.

## Unblock Condition

Re-entry requires explicit fresh correction authority after this exhausted loop. The authorized correction must require a whole-declaration canonical Markdown-link match before a local backlog link can normalize to a slug, parse complete Markdown targets including query and fragment components, preserve every embedded-link prose declaration and external URI verbatim as a manual unmet prerequisite, and add adversarial tests proving neither case can become runnable through a completed same-stem local item. The corrected contribution must then pass new fresh source review and independent verification before deliberate integration, followed by a synchronized example refresh, fresh post-integration source, artifact, and UX reviews, complete primary verification, and the required browser and accessibility matrix. Until all of that evidence passes, this item remains Blocked and must not move to a Completed archive.

## Summary

Require the styled backlog report to classify an active Ready item as runnable only when its explicit Type is Defect, Feature, Analysis, or Investigation.

## Context

[Add A Styled Backlog Report With User Input](../feature-backlog/add-styled-backlog-report-with-user-input.md) is blocked after its bounded correction loop found one remaining P1 defect. The final preserved source commit 32fd01a7fe214d7f5acb9a1ca2976073722c13ec validates Type values but still derives runnable eligibility from active placement, Ready status, satisfied dependencies, and required fields without requiring a dispatchable Type.

As a result, a complete active Ready item whose Type is Holding or an invalid value such as Epic can inflate Runnable now and appear in Runnable Work. These items must remain visible in active inventory and lifecycle findings without becoming dispatchable.

The rejected source chain remains preserved in commits 381f09f557b7e73d07a9b735508687b2c27ac5f7, 8f7eb183846744180ee0ea3377ccbc7b072c5c60, and 32fd01a7fe214d7f5acb9a1ca2976073722c13ec. The independently accepted README contribution remains preserved in commit 69f0461f94c56737d696c6ad3adc2f71207df977. This defect supplies fresh bounded correction authority; it does not itself authorize integration of those commits.

## Requirements

- Require runnable eligibility to include an explicit Type of exactly Defect, Feature, Analysis, or Investigation.
- Keep active Ready items with Type Holding visible in active inventory and lifecycle anomaly reporting while excluding them from Runnable now and Runnable Work.
- Keep active Ready items with an invalid Type such as Epic visible in active inventory and lifecycle anomaly reporting while excluding them from Runnable now and Runnable Work.
- Preserve existing validation findings, type and status inventory, dependency reconciliation, deterministic ordering, and offline report behavior.
- Limit the correction to scripts/generate-backlog-report.py and scripts/test_generate_backlog_report.py unless new evidence is returned to the work-item owner before scope expansion.
- Do not change README.md, backlog/examples/styled-backlog-report.html, backlog lifecycle files, agent definitions, skill definitions, generated adapters, or approval-directive surfaces as part of the correction lane.

## Acceptance Criteria

- Runnable eligibility is true only for an active Ready item with satisfied dependencies, complete required metadata, and Type Defect, Feature, Analysis, or Investigation.
- A complete active Ready fixture with Type Holding contributes zero to Runnable now and does not appear in Runnable Work.
- A complete active Ready fixture with Type Epic contributes zero to Runnable now and does not appear in Runnable Work.
- The Holding fixture remains traceable in active inventory and produces its applicable lifecycle anomaly.
- The Epic fixture remains traceable in active inventory and produces the invalid Type lifecycle anomaly.
- Focused tests bound their Runnable Work assertions to that section so visibility elsewhere cannot mask accidental runnable placement.
- Existing focused generator tests continue to pass without weakened assertions.

## Dependencies

- [Rename User Review State For Clarity](../completed-backlog/defects/rename-user-review-state-for-clarity.md)

## Verification

- Add focused complete-metadata fixtures for active Ready items with Type Holding and Type Epic and no unmet dependencies.
- Assert the exact Runnable now count and absence of both fixtures from the bounded Runnable Work section.
- Assert the expected Holding placement or Type mismatch finding and the invalid Epic Type finding remain visible.
- Run the focused backlog report generator tests.
- Run Python compilation, Ruff, and Mypy checks applicable to the changed source and test files.
- Generate a controlled report and inspect its runnable metric, Runnable Work section, active inventory, and lifecycle findings.
- Run the applicable repository script tests and git diff --check.

## Notes

- This is directly authorized technical correction work. It is not User Action Required and has no unresolved user-owned decision.
- The blocked feature remains blocked until the corrected cumulative source, accepted documentation, example update, fresh reviews, complete verification, integration, and browser accessibility gates succeed.
- Use the simple-workitem process and return a verified local correction commit from a clean released artifact claim before integration is considered.
