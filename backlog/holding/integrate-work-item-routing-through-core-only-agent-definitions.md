# Integrate Work-Item Routing Through Core-Only Agent Definitions

Status: Holding

Type: Feature

Provider: file

Provider Reference: backlog/holding/integrate-work-item-routing-through-core-only-agent-definitions.md

Completion: direct-main

## Holding State

- Previous canonical Dev Orchestrator task: 019f80f3-41d5-7481-910e-6f54d43083ae.
- Previous worktree: /Users/martinbechard/.codex/worktrees/2c00/dev-methodology.
- Previous branch: codex/integrate-work-item-contracts-across-bundle.
- Previous starting main commit: 2ddedf5a83ca8567ac3de93867a3f90624a2e28c.
- Phase: Holding after approval resolution because the accepted core-only routing design depends on simplify-project-configuration-setup-and-skill-routing.
- Verification: focused provider, completion, selector, role, metadata, renderer, migration, stale-name, and evaluation checks first; then the item-required full repository, project-wiki, catalog, generated-adapter, disposable smoke, and install/refresh release gates.

## Resolved Approval

### Question for the User

Do you approve changing exactly skills/codex-workitem-coordination/SKILL.md so Dev Backlog Steward applies the management skill selected by the effective work-item provider, instead of hard-coding manage-backlog or manage-file-work-items, together with only its supported generated skill mirror and directly related tests and documentation?

### Why User Input Is Required

The final bundle integration must remove the retired manage-backlog caller from the coordination skill. Replacing it permanently with manage-file-work-items would couple the provider-neutral coordinator to the file provider and make future GitHub, GitLab, Jira, Azure DevOps, or other providers require another coordination definition change. The provider-neutral wording changes a governed distributed skill definition and therefore requires exact user approval before mutation.

### Options and Tradeoffs

- Approve the provider-neutral wording: one coordinator and one Dev Backlog Steward continue to work with the provider selected in PROJECT.yaml; provider-specific create and manage skills remain interchangeable capabilities rather than separate agents.
- Decline: the integration cannot truthfully remove the retired caller while preserving future provider support, so this final bundle-integration item remains unresolved.

### Resolution

Approved on 2026-07-21. In canonical task 019f80f3-41d5-7481-910e-6f54d43083ae, the user answered "ok agreed" in user message item-30 after the task presented the provider-neutral coordination wording and core-only agent-definition direction. The task acknowledged in item-32 that this resolves the provider-neutral coordination question.

Approved governed scope: change exactly skills/codex-workitem-coordination/SKILL.md so Dev Backlog Steward applies the management skill selected by the effective work-item provider instead of hard-coding manage-backlog or manage-file-work-items, together with only its supported generated skill mirror and directly related tests and documentation.

### Unattended Work Boundary

The approval is resolved, but this item is intentionally deferred. Do not dispatch it until backlog/holding/simplify-project-configuration-setup-and-skill-routing.md is accepted and supplies the final project binding and installation contracts. On resumption, create or assign one canonical Dev Orchestrator task and run the exact governed-definition pre-mutation check using this recorded provenance before mutating skills/codex-workitem-coordination/SKILL.md.

## Summary

Integrate the stabilized work-item persistence and commit contracts without placing technology-specific, persistence-specific, or commit-specific skills in conceptual agent definitions. Keep agent definitions limited to technology-agnostic core workflows, record project selections in PROJECT.yaml, and render selected concrete skills by reference through root or nested AGENTS.md guidance.

## Context

This is the final integration item in the Work-Item Provider And Completion Contracts series. Provider and completion capabilities remain independent, but conceptual agent definitions must stay reusable across technologies, persistence systems, and commit workflows. PROJECT.yaml records project-owned selections, and generated AGENTS.md guidance binds those selections to concrete provider, commit, and folder technology skills.

The current integration must not replace one hard-coded provider dependency with another. Dev Coder, Dev Orchestrator, and Dev Backlog Steward use generic core workflows; adding or changing a provider must not require a new agent or a conceptual role-definition change.

## Requirements

- Keep every conceptual agent definition limited to technology-agnostic core skills.
- Keep Dev Backlog Steward provider-neutral and route creation and lifecycle changes through the effective project binding rather than hard-coded provider skills.
- Keep Dev Coder independent of provider lifecycle mutation and provider-specific persistence skills.
- Keep Dev Orchestrator provider-neutral while preserving implementation, integration, and backlog ownership boundaries.
- Update project-configurator and any setup roles to preserve selector-only PROJECT.yaml and reference-only AGENTS.md behavior.
- Render the selected persistence create/manage skills and commit skill by reference through applicable AGENTS.md guidance.
- Keep confirmed technology skills independently routed at their applicable folder scopes.
- Require missing, unsupported, or mismatched bindings to return BLOCKED without fallback or shadow persistence.
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

- Every conceptual role contains only technology-agnostic core skills.
- Dev Coder, Dev Backlog Steward, and Dev Orchestrator contain no provider-specific persistence dependency.
- Changing a project's technology, Persistence, or Commit selection changes PROJECT.yaml and rendered AGENTS.md guidance rather than conceptual agent definitions.
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

- backlog/holding/simplify-project-configuration-setup-and-skill-routing.md.
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
- The user approved the provider-neutral coordination wording and the proposed core-only agent-definition direction in canonical task 019f80f3-41d5-7481-910e-6f54d43083ae.
- The prior waiting task should not consume a Running slot while this item is Holding.
- Live provider spending and mutation require explicit authority even when deterministic tests pass.
