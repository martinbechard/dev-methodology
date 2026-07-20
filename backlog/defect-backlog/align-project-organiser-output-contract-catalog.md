# Align Project Organiser Output Contract Catalog

Status: Ready

Type: Defect

## Summary

Align the Project Organiser entry in the global agent scenario catalog with the conceptual role's exact output contract so catalog validation succeeds.

## Context

The conceptual source at agents/roles/project-setup/project-organiser.role.yaml defines the first output as approved path or placement blocker. The global catalog at evals/agent-scenarios.yaml currently records approved path, causing scripts/run-agent-skill-evals.py --validate-catalogs to report one exact mismatch. The failure is reproducible on main at 8a269a6c612a1e9b22f6ecf5d4877020cf974e7b.

This item is the first end-to-end pilot of the file-backed Dev Backlog Coordinator workflow. The work-item file is its only durable execution record.

## Execution Record

- Canonical Dev Orchestrator task: Pending dispatch
- Branch: Pending dispatch
- Worktree: Pending dispatch
- Current phase: Ready
- Accepted candidate commit: None
- Integration or completion wait: None
- Claim attempts: None
- Open issues: None

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
