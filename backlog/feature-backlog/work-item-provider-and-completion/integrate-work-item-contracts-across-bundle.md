# Integrate Work-Item Contracts Across The Bundle

Status: Proposed

Type: Feature

## Summary

Integrate the stabilized provider, completion, and selector contracts across conceptual roles, skill metadata, generated adapters, design documentation, evaluation catalogs, migration guidance, stale-name sweeps, and full repository verification.

## Context

This is the final integration item in the [Work-Item Provider And Completion Contracts series](index.md). Provider and completion lanes can proceed independently after the foundation contract, but the bundle is not coherent until every source-owned role, generated runtime, public explanation, evaluation, and installed artifact agrees with the final identifiers and terminal semantics.

## Requirements

- Update dev-backlog-steward to route creation and lifecycle changes through the selected provider-specific create and manage skills.
- Update dev-coder to use the selected direct-main or feature-branch completion skill without owning provider lifecycle mutation.
- Update dev-orchestrator to pass independent provider and completion selections, preserve implementation and backlog ownership boundaries, and route final lifecycle evidence to dev-backlog-steward.
- Update project-configurator and any setup roles to preserve selector-only PROJECT.yaml and reference-only AGENTS.md behavior.
- Update skill metadata and Codex interface descriptions for every added, renamed, retired, or conditionally loaded skill.
- Regenerate native adapters, manifests, skill definitions, role definitions, hierarchy, support checklist, and other derived data from canonical sources.
- Update README.md and every relevant design page with the provider/completion separation, supported matrix, unsupported placeholders, direct-main semantics, and AWAITING_REVIEW boundary.
- Update evaluation skill probes, agent scenarios, runnable cases, workflow packs, Agent-suite contracts, and regression tests for the final identifiers and behavior.
- Add positive and negative coverage for every provider, completion process, UNSET, unsupported provider, invalid combination, shadow-queue prohibition, main reachability, and merge-evidence boundary.
- Define compatibility and retirement behavior for create-backlog, manage-backlog, file-based-backlog, github-issues-backlog, execute-workitem, simple-workitem, and feature-branch-workitem.
- Decide whether create-pull-request remains GitHub-oriented, becomes code-host-qualified, or is paired with a GitLab merge-request capability, and keep terminology and tools accurate.
- Sweep canonical sources, generated artifacts, examples, tests, backlog fixtures, installation assets, and design pages for stale identifiers and contradictory terminal-state language.
- Preserve unrelated work and avoid hand-editing generated output.
- Publish and refresh installed bundle artifacts only after source, generated, evaluation, and migration gates pass.

## Acceptance Criteria

- Every conceptual role loads only the provider and completion skills appropriate to its authority.
- File, GitHub, and GitLab providers each support independent direct-main and feature-branch selection.
- Azure DevOps and Jira remain visible but consistently BLOCKED without fallback.
- Direct-main completion always names a commit reachable from main.
- Feature-branch publication remains AWAITING_REVIEW until required merge evidence exists.
- PROJECT.yaml and AGENTS.md contain selectors and skill references without duplicated procedures.
- Technology-skill inlining remains unchanged and separately testable.
- All source, metadata, generated, design, eval, and installed representations use the canonical identifiers.
- Retired names remain only in explicit migration tests or historical explanation.
- The support checklist distinguishes structural availability, implemented behavior, unsupported placeholders, and executed evidence truthfully.
- Full repository validation passes from a clean worktree and the integration is committed coherently.

## Dependencies

- render-selected-work-item-skills.
- transform-file-work-item-skills.
- split-github-work-item-skills.
- add-gitlab-work-item-skills.
- add-azure-devops-and-jira-placeholders.
- add-direct-main-completion-skill.
- add-feature-branch-completion-skill.

## Verification

- Run focused provider, completion, selector, role, metadata, renderer, migration, stale-name, and evaluation tests first.
- Run every repository-required skill validation and generated-output freshness check.
- Run the complete scripts unit-test suite with the supported Python interpreter.
- Run the complete project-wiki unit-test suite.
- Validate evaluation catalogs and inspect representative generated Codex, Claude, Gemini, and Junie definitions.
- Run authorized disposable provider and code-host smoke tests; keep unavailable external capability explicit rather than weakening gates.
- Install or refresh the bundle in a disposable target and verify selected workflow references and technology inlining from the loaded guidance.
- Run Git diff validation, confirm a clean worktree, and perform an independent source-versus-generated review.

## Notes

- This item integrates accepted lane outputs; it should not silently redesign the foundation contract.
- Live provider spending and mutation require explicit authority even when deterministic tests pass.
