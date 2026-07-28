# Align module-design optional-section instructions with the mandatory heading contract

Status: Completed

Type: Defect

Provider: file

Provider Reference: backlog/completed-backlog/defects/align-module-design-mandatory-heading-contract.md

Completion: direct-main

Owner: Dev Orchestrator

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Parent Agent Task: 019fa9bb-1423-7e80-bcde-3caa765e3758

Launch Reservation: reserve-six-ready-refill-019fa9bb

Normalized Objective: Align module-design optional-section instructions with the mandatory heading contract.

Dispatch Time: 2026-07-28T20:53:27Z

Intended Root Role: Dev Orchestrator

Runtime Thread: 019faa83-9a42-7e11-9c24-2086a4bcec29

Root Agent Task: 019faa83-9a42-7e11-9c24-2086a4bcec29

Branch: codex/align-module-design-mandatory-heading-019faa83

Worktree: /Users/martinbechard/.codex/worktrees/24c8/dev-methodology

Started At: 2026-07-28T21:00:16Z

Phase: Completed after direct-main delivery, independent review, and independent verification.

Claim Evidence: SHARED_CHECKOUT_ACQUIRED acceptance claim accept-running-align-module-design-mandatory-heading-019faa83; acquisition journal event f9ac1d4e-e79c-4989-833a-0ac22a394ae2. Prior reservation claim reserve-six-ready-refill-module-heading-019fa9bb-retry; acquisition journal event 827364ca-c7e4-44ab-869e-5a55c5892d58.

## Completion Evidence

- Canonical Runtime Thread and Root Agent Task: 019faa83-9a42-7e11-9c24-2086a4bcec29.
- Completion: direct-main. Accepted source tip: ffc21902b149f590431f141c1899d0bbc834d205. Candidate commits: 000a68481fde3f4e2421ec79393e176f95edaddf and ffc21902b149f590431f141c1899d0bbc834d205.
- Integration mapping: 000a6848 -> 20681f61; ffc21902 -> 25d314f0. Delivered integration commit: 25d314f0fcaf062c66b8344648e7a9bd02bddf9f.
- Main observation: delivered integration commit 25d314f0 is an ancestor of main at clean backlog baton a79c661f450281ac8d0eea9c968a3fa137c186e9. Changed delivery paths: skills/development-methodology/assets/templates/module-design-template.md, design/generated/template-definitions.js, and scripts/test_bundle_content.py.
- Independent source review: APPROVED with no findings. Independent verification: VERIFIED.
- Post-integration verification passed with Python 3.11: test_planned_hld_and_module_creation_contracts, test_generated_template_definition_data_is_current, and test_dev_backlog_steward_requires_starting_blocked_work_resumption. scripts/build-skill-docs.py --check and git diff --check passed.
- Lifecycle acceptance provider commit: 557ea4fb3e1434926abb9ed99c5236896e86b49d; claim acquisition event f9ac1d4e-e79c-4989-833a-0ac22a394ae2; release event aaee6b7a-b064-4458-85a6-4934ae07ffca.
- Main integration claim acquisition event: bb2a490b-04cf-4fbe-801c-d725cdb52149; release event: 50cdfab5-f879-4671-832e-e84982f61ffb.
- Commit disposition: READY. Work-item integration and cleanup branch codex/align-module-design-mandatory-heading-integration-019faa83 is fully merged and cleanup-eligible. Source branch codex/align-module-design-mandatory-heading-019faa83 remains preserved provenance.
- Terminal archive claim: SHARED_CHECKOUT_ACQUIRED claim complete-align-module-design-mandatory-heading-019faa83; acquisition journal event 9d678729-9ce8-49c9-81dc-0d36ba403492.
- Completed At: 2026-07-28T21:32:24Z. Terminal Provider Reference: backlog/completed-backlog/defects/align-module-design-mandatory-heading-contract.md.

## Summary

Align module-design optional-section instructions with the mandatory heading contract.

## Context

The primary affected skill is skills/create-module-design/SKILL.md. The creation and review gates require every level-two heading, while the template directs authors to remove Configuration, External Interfaces, and UI And Notification Behavior when inapplicable. Following the template creates an artifact the required gates reject.

## Source Evidence

The user authorized this independently dispatchable Ready Defect record on 2026-07-28. The accepted methodology skill-lint report at evals/results/2026-07-28-methodology-skill-lint.md, commit 54d860f1978d4cb403e59162cfb209fe45cc06a8, records this finding at 20,85; skills/development-methodology/assets/templates/module-design-template.md:285,295,303; skills/review-module-design/SKILL.md:28; skills/development-methodology/SKILL.md:123. Independent reviewer /root/confirm_create_module_design accepted it as CONFIRMED_CRITICAL.

## Requirements

- Preserve the three mandatory headings and record why each is not applicable; make artifact-specific heading contracts override the generic section-removal rule.
- Preserve the documented ownership boundary and avoid unrelated provider, source, report, analysis, generated, or lifecycle mutation.

## Acceptance Criteria

- Modules with no applicable content retain Configuration, External Interfaces, and UI And Notification Behavior with explicit not-applicable text.
- Creation and review gates accept the retained headings.
- The correction remains limited to the smallest source-backed scope.

## Dependencies

None

## Verification

- Cover all three headings with a module that has no applicable content.
- Require creation and review gates to accept retained not-applicable sections.
- Run focused contract validation and git diff --check.
- Obtain independent review of the defect correction.

## Open Questions

None

## Notes

Collision reconciliation before creation found no active item with this provider reference, slug, affected skill, or overlapping accepted outcome.

This record has one primary affected skill identity: skills/create-module-design/SKILL.md. It does not authorize a skill-definition mutation. Each governed SKILL.md changed later requires its own exact scope-specific user approval, provenance record, and accepted pre-mutation check. The template is a separate supporting path and must remain aligned with approved skill changes.
