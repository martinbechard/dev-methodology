# Align Project Organiser Filename Selection

Status: Completed

Type: Defect

## Completion Evidence

- The accepted test-only integration commit is a28b0681723d22ff9f8512a21d296d7022f1fe1c, and its sole changed artifact is scripts/test_bundle_content.py. The accepted Project Organiser method is equal to 06d40324614a2be9b8d19404ea7f227d8a5c1ada, with current-main coordination bytes preserved.
- Integration ownership was acquired in event f0ef189d-3dd6-47a9-a550-2c41437520cc and released normally in event 353ddec9-6f5e-4630-9147-28b877940d9a.
- Fresh post-integration Dev Code Reviewer result: ACCEPTED with zero material findings.
- Fresh verifier ownership was acquired in event 26869cee-15f0-4755-b1fe-8391ca739895 and released with a no-change outcome in event 3ef7d9fd-6294-4608-ac37-6e1e6fc303f9.
- Focused Project Organiser verification passed 1 of 1; coordination assertions passed 3 of 3; full bundle-content verification passed 86 of 86; the independent boundary matrix covered 5,270 observations with zero failures; syntax, diff, and protected-surface checks passed; and both the verifier checkout and main were clean at a28b0681723d22ff9f8512a21d296d7022f1fe1c.
- External baseline catalog WARN exactly: agent-scenarios.yaml:project-organiser outputContractFields must exactly match its conceptual source. The same single exit-1 mismatch occurs on untouched baseline 8ec020659bc4d8530ce7088426eabdc605500e11 and integration a28b0681723d22ff9f8512a21d296d7022f1fe1c. The audit proves scripts/test_bundle_content.py has an open/import count of 0, so this is a pre-existing external defect and not an in-scope completion failure.

## Historical User Action Requirement (Resolved)

At that stage, the independently accepted regression was integrated, but the remaining behavioral correction changed a governed conceptual agent definition. Repository policy required explicit, scope-specific user approval before that definition could be changed. The approval was subsequently recorded in the resolution below.

## Historical Question for the User (Answered)

Do you approve changing only agents/roles/project-setup/project-organiser.role.yaml so Project Organiser must explicitly state purpose, owner, lifecycle, consumers, mutability, and artifact kind in every placement rationale or blocker, with only supported generated role mirrors and regression coverage updated?

## Historical Reason User Input Was Required

AGENTS.md requires explicit, scope-specific approval before any governed agent or skill definition change. A failing test, general repository authority, review work, verification work, and the desire to make validation pass are not sufficient authority.

## Resolution

Approved on 2026-07-19. The user confirmed, "I already approved this one so yes," in the parent coordination thread. This authorizes only the exact Project Organiser role-instruction change stated above, together with its supported generated role mirrors and regression coverage, including reconciling that regression coverage with current main without weakening the approved behavior.

## Historical Unattended Work Boundary

The approval boundary remains exact: unattended work may change only the named Project Organiser role definition, its supported generated role mirrors, and regression coverage needed to prove the approved behavior. It must not change a distributed skill definition or weaken the scenario or Judge contract to obtain a pass.

## Historical Delivery And Verification Evidence

- Accepted integrated commit: 6426a15c01c63dc7554c045618cd8a9a329c02d2.
- Fresh post-integration review: PASS.
- Project Organiser scenario known-runbook-placement: PASS.
- Project Organiser scenario authorized-taxonomy-extension: PASS.
- Project Organiser scenario ambiguous-ownership-boundary: independent Judge FAIL because the filename-selection classification omitted consumers and mutability and left purpose and lifecycle implicit.
- Resolved external technical blocker: [Correct agent-suite classification archive references](correct-agent-suite-classification-archive-references.md). This separate defect is not part of the approval scope.

## Historical Running Ownership

- Owner: Dev Orchestrator root task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Lifecycle claim: align-project-organiser-filename-selection-running-approved.
- Claim evidence: dev-backlog-steward acquired PRIMARY ownership of this exact backlog item on 2026-07-19 before recording the then-current Running transition.
- Approval provenance: on 2026-07-19 the user said, "I already approved this one so yes," authorizing only agents/roles/project-setup/project-organiser.role.yaml together with supported generated role mirrors and regression coverage; no skill definition change is authorized.
- Scope boundary: that lifecycle claim was released after the committed transition; separate project-artifact ownership was required before implementation.

## Historical Blocked Outcome (Superseded)

This section records a superseded blocked lifecycle result. The completion evidence above records the later accepted integration and terminal verification.

- Preserved initial contribution: 2dfbe08f31b130bc0d682a11ca00743a0e022e77.
- Preserved correction attempt 1: 242aca4922cda9e2a89ddfb0d299a3004df16e7b.
- Preserved correction attempt 2 and final contribution: 914872c0c91602c954f2cd640615eaa6e09ff033 on branch codex/align-project-organiser-approved-correction-2.
- Approval enforcement: every governed mutation passed ALLOWED_APPROVED_DEFINITION_CHANGE and stayed within the exact approved eight-file scope: the Project Organiser role, its supported generated role mirrors, and regression coverage. No skill definition, evaluation, backlog, or other project-artifact scope was included.
- Correction limit at that stage: both authorized correction attempts were used, so the correction loop was exhausted.
- Material result at that stage: the final Project Organiser role and generated adapters were judged materially correct.
- Fresh-review finding at that stage: the regression assertions could false-pass because the examples were classified independently, allowing one hybrid output to satisfy both success and blocker counts.
- Success-example gap at that stage: the regression did not assert that the success example was free of Blocker, Exact decision, Approved path omitted, and BLOCKED markers.
- Native-adapter gap at that stage: the regression rejected only one narrow stale Return string and did not reject standalone decision-output renderings in each native adapter format.
- Gates unperformed at that stage: no independent verifier, integration, post-integration review, post-integration verification, Project Organiser scenario rerun, or terminal completion had been started for the preserved final contribution.
- Delivery state at that stage: the final contribution remained off main on its preserved commit and branch.
- Historical unblock condition: fresh explicit parent or user ARTIFACT GO authorizing a new bounded correction lane beyond the exhausted loop, limited to regression-assertion strengthening from 914872c0c91602c954f2cd640615eaa6e09ff033 and the already-approved role and supported mirrors, with no skill or evaluation widening, followed by fresh review before verifier or integration work. That condition was later satisfied by the accepted correction and integration recorded above.
- Authority boundary: that unblock supplied technical and process authority only; it did not expand the approved governed-definition scope.

## Historical Target Merge Pending (Superseded)

- Delivery contribution: commit 2d636dd0f240793820778031ab9d38db6c11ee60 on branch codex/align-project-organiser-filename-selection-impl, based on sibling commit 4a31b337e6baf241de5ec81eb3a3c924096f3c82.
- Review: fresh independent review passed with no findings.
- Verification: focused tests passed 3 of 3; repository validation and freshness checks passed; project-wiki tests passed 17 of 17; all three Project Organiser scenarios retained deterministic and independent Judge PASS evidence.
- Integration boundary at that stage: the contribution was not present on main and required deliberate integration without overwriting its sibling base change before completion.

## Historical Integration Blocker (Resolved)

- Attempted integration: dev-merge-coordinator acquired PRIMARY ownership of the exact integration file scripts/test_bundle_content.py plus merge:integration:main in event 0143a4da-7519-4e61-aabe-1c5409f56840 and attempted accepted commit 2d636dd0f240793820778031ab9d38db6c11ee60, stable patch id cd87d184bb55153bb0b3a27033fe915adb89c00b, against clean main baseline b0410174ce8127686ce89b3d1e1faefde8b6b112.
- Conflict evidence: cherry-pick produced a content conflict in scripts/test_bundle_content.py, and an independent git apply --check failed at the accepted patch's old line-2203 context.
- Scope boundary: the explicit user direction required stopping on applicability ambiguity rather than adapting the accepted test or absorbing sibling content.
- Restoration evidence: the coordinator aborted the cherry-pick, restored the exact clean baseline, created no integration commit, ran no post-integration tests, and released ownership with no change in event 6082defa-4b29-4cdf-80c8-a87548ac4ec6.
- Excluded content: rejected commits 4a31b337e6baf241de5ec81eb3a3c924096f3c82, 68ea9d4, and 13217749 remain non-ancestors of main; none of their content was integrated by this attempt.
- Historical next action: a fresh explicit user decision had to authorize adapting the accepted regression test to current main, or provide a replacement accepted commit. That authority was not inferred from the failed integration assignment; the later accepted integration is recorded in the completion evidence above.

## Summary

Remove the generated Project Organiser adapter conflict that simultaneously requires the agent to choose an approved artifact path and prohibits it from choosing filenames.

## Context

The Project Organiser conceptual role owns repository placement decisions. Its contract requires choosing an approved destination, validating the filename against repository guidance, and returning the selected path with placement-audit evidence.

The generated Codex adapter also inlines the structured-design response-only rule that says not to choose filenames. That prohibition is valid for response-only design work, but it contradicts the Project Organiser role when filename and destination selection are the requested output.

The complete conceptual-agent suite rollout confirmed the conflict while freezing the Project Organiser role, generated adapter, and assigned skill rules. The evaluation infrastructure did not edit the subject contract.

## Evidence

- agents/roles/project-setup/project-organiser.role.yaml lines 4 through 7 require repository placement decisions.
- agents/roles/project-setup/project-organiser.role.yaml lines 19 through 23 require filename validation.
- agents/roles/project-setup/project-organiser.role.yaml lines 49 through 54 require the approved path and placement audit in the result.
- generated/adapters/codex/agents/project-organiser.toml lines 624 through 627 contain the conflicting prohibition against choosing filenames.
- evals/agent-tests/project-organiser contains the frozen executable suite that exposed the conflict.

## Requirements

- Preserve response-only structured-design behavior when no artifact authoring or placement decision is requested.
- Permit Project Organiser to choose a filename and destination when its canonical role owns that decision.
- Express the exception in the reusable source contract rather than editing generated adapters by hand.
- Regenerate all native adapters and documentation derived from the changed source.
- Add regression coverage proving that the Project Organiser contract and inlined skills contain no contradictory filename rules.

## Acceptance Criteria

- The canonical Project Organiser role still requires an approved path and placement audit.
- The generated Codex Project Organiser adapter permits required filename selection.
- Response-only structured-design requests continue to avoid unauthorized artifact creation.
- Generated adapters are fresh and repository contract tests pass.
- The Project Organiser executable scenarios can be rerun without freezing contradictory authority.

## Dependencies

None.

## Verification

- Run the focused generated-adapter and bundle-content tests.
- Run Agent Skill validation and every generated-output freshness check.
- Run the Project Organiser suite scenarios and inspect retained identity and Judge evidence.
- Run repository unit tests and Git diff validation.

## Notes

- Do not patch generated/adapters/codex/agents/project-organiser.toml directly.
- Keep the correction scoped to mode-aware filename authority; do not broaden artifact-writing permission.
