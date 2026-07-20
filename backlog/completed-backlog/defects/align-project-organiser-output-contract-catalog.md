# Align Project Organiser Output Contract Catalog

Status: Completed

Type: Defect

## Summary

Align the Project Organiser entry in the global agent scenario catalog with the conceptual role's exact output contract so catalog validation succeeds.

## Context

The conceptual source at agents/roles/project-setup/project-organiser.role.yaml defines the first output as approved path or placement blocker. The global catalog at evals/agent-scenarios.yaml currently records approved path, causing scripts/run-agent-skill-evals.py --validate-catalogs to report one exact mismatch. The failure is reproducible on main at 8a269a6c612a1e9b22f6ecf5d4877020cf974e7b.

This item is the first end-to-end pilot of the file-backed Dev Backlog Coordinator workflow. The work-item file is its only durable execution record.

## Execution Record

- Canonical Dev Orchestrator task: 019f7df2-ad96-7b03-bb1b-3127775ebf1b
- Branch: codex/align-project-organiser-output-contract-catalog
- Worktree: /Users/martinbechard/.codex/worktrees/ba6b/dev-methodology
- Current phase: Completed and archived after accepted direct main integration
- Accepted candidate commit: e1c926f292dce5164148b0d33b3701aeeeae7fcf
- Integration or completion wait: None; both claims acquired on their first attempt
- Claim attempts: Running transition acquired as PRIMARY with event 5998175b-58ad-4362-83ef-6ef96af85729 and released normally with event 53f4b279-6ff0-4b15-9bbb-1ecfbea5eae9; main integration acquired as PRIMARY with event a796e7ac-29f4-4731-8654-c4e1e21fe45d and released normally with event 4ccf10e2-dfe2-4c89-aab3-f6242bb69715; terminal completion acquired as PRIMARY with event b6d1125a-c923-4f3b-a2c5-54f9ace627d9
- Open issues: None

## Completion Evidence

- The catalog-only candidate commit e1c926f292dce5164148b0d33b3701aeeeae7fcf changed the Project Organiser first output field to approved path or placement blocker, exactly matching the conceptual source.
- Fresh independent review in task /root/catalog_review returned ACCEPTED with no findings after inspecting the exact candidate against main commit 188888b810dec33d0c33de72f8ae29c8eee084b8 and rerunning every focused check.
- Main fast-forwarded directly to accepted commit e1c926f292dce5164148b0d33b3701aeeeae7fcf under the exact evals/agent-scenarios.yaml integration claim. The integration claim was released normally in event 4ccf10e2-dfe2-4c89-aab3-f6242bb69715.
- Main verification passed: catalog validation reported CATALOGS VALID; scripts.test_eval_coverage_catalog passed 16 of 16 tests; the focused BundleContentTests.test_project_organiser_retains_filename_selection_authority regression passed 1 of 1; and git diff --check passed.
- The focused bundle-content command initially resolved to unsupported system Python 3.9 in the primary worktree and failed while importing standard-library tomllib. The complete focused matrix then passed with the task worktree's supported Python 3.11.10 interpreter. This was an environment-only failure and produced no repository change.
- Main was clean at e1c926f292dce5164148b0d33b3701aeeeae7fcf before terminal lifecycle recording. The task branch commit is an ancestor of main, the task worktree is clean, and both are safe to delete after this completion commit is preserved and the terminal claim releases normally.
- Terminal completion ownership is claim project-organiser-output-contract-completion-019f7df2, acquired as PRIMARY in event b6d1125a-c923-4f3b-a2c5-54f9ace627d9 for only the active and completed work-item paths. Its normal release follows the clean archive commit and is retained in the repository-global claim journal and parent handoff because the release event does not exist until after this file is committed.

## Requirements

- Make the Project Organiser outputContractFields list in evals/agent-scenarios.yaml exactly match the conceptual source.
- Keep the change limited to the catalog source unless focused evidence proves another correction is required.
- Use one canonical user-visible Dev Orchestrator task for implementation, fresh review, direct main integration, focused tests, work-item completion, and cleanup handoff.
- Do not run the complete agent catalog for this individual item.

## Acceptance Criteria

- The Project Organiser catalog entry uses approved path or placement blocker as its first output field.
- python3 scripts/run-agent-skill-evals.py --validate-catalogs passes.
- Focused catalog and Project Organiser contract tests pass.
- A fresh independent review accepts the candidate.
- The accepted commit is integrated on main under an exact main-file claim.
- This item records the main commit, focused verification, released integration and completion claims, and cleanup eligibility before archival.

## Dependencies

None.

## Verification

- python3 scripts/run-agent-skill-evals.py --validate-catalogs
- python3 -m unittest scripts.test_eval_coverage_catalog
- Focused Project Organiser output-contract regression from scripts.test_bundle_content
- git diff --check

## Notes

The complete agent catalog remains a final campaign-state gate and is outside this pilot item.
