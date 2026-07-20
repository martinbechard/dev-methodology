# Render Selected Work-Item Skills

Status: Running

Type: Feature

## Current Execution

- Canonical Dev Orchestrator task: 019f80a4-8c6a-7a50-9a0a-636053ce5710.
- Worktree: /Users/martinbechard/.codex/worktrees/bc99/dev-methodology.
- Intended branch: codex/render-selected-work-item-skills.
- Owner: Dev Orchestrator.
- Phase: Completed and integrated on main.
- Verification: focused selector and renderer tests, applicable generated freshness checks, governed-definition approval gates where required, and Git diff validation before independent review.

## Completion Evidence

- Accepted candidate: 9d84ce39c5efae6871060293bf6505ee43779ab5.
- Independent review: two fresh final ACCEPT reviews found no material findings.
- Independent candidate verification: GO.
- Governed definition gates: exact skill and role checks returned ALLOWED_APPROVED_DEFINITION_CHANGE; supported generated preflights also passed.
- Main delivery commits: a5636b3, 176ef60, and a71823bb6e2bf6e156705e5b8067904250ec8e56.
- Post-integration GO: 88/88 renderer tests, 2/2 focused bundle tests, 17/17 fixtures, skill and generated-output freshness checks, Git diff validation, 21/21 matrix checks, 8/8 collision checks, 2/2 combined diagnostics, and clean main.
- Runtime boundary: system Python 3.9 lacked tomllib; supported Python 3.11 was used for the applicable checks.
- Verification tier: bounded Tier 1/2 scope. Broad repository, project-wiki, and live-agent-catalog suites were intentionally omitted. The unchanged broad-bundle phrase warning was independently confirmed as a baseline condition outside this candidate scope.
- Integration ownership: claim acquired at event 10b2a2c6-4c16-4a1f-83b5-8024a0c70936 and released at event 9d96dda7-52fd-4d89-bd37-26567f98c13b. The earlier event 513411a6-a747-4851-9478-81dbc3d32ace was an invalid worktree-path attempt corrected before acquisition; it did not establish ownership.
- Terminal backlog ownership: claim render-selected-work-item-skills-completion-019f80a4 acquired PRIMARY at event 1d292e41-c57c-4d16-a1b2-c6691d799b2c for exactly this source and completed destination. It will be released immediately after this committed archive transaction from clean main.
- Cleanup eligibility: the private worktree and intended branch are preserved for parent cleanup after this terminal claim releases. The parent next action is to verify merge/patch-equivalence, remove the clean worktree, safely delete the merged branch, prune worktree metadata, and update the task display state.
- Open issues: none for this work item.

## Summary

Update PROJECT.yaml configuration and AGENTS.md rendering so independent provider and completion selectors validate against the canonical matrix and emit reference-only selected workflow skill names without changing technology-skill inlining.

## Context

This item is the selector integration stage in the [Work-Item Provider And Completion Contracts series](index.md). It begins only after provider and completion identifiers stabilize. The current prototype stores work-item and backlog selectors and renders selector guidance, but its identifiers reflect the pre-migration wrappers. The new contract must avoid copying workflow procedures into project files while retaining setup-time inlining of detected technology skills.

## Requirements

- Replace the prototype work-item and backlog selector shape with independent work-item-provider and work-item-completion selectors.
- Support file, github, gitlab, azure-devops, jira, none, and UNSET provider values.
- Support direct-main, feature-branch, and UNSET completion values.
- Support documented folder overrides only where project evidence and user intent establish a different process.
- Validate every provider and completion value against the canonical identifier and compatibility matrix.
- Preserve unsupported Azure DevOps and Jira selections and route them to their BLOCKED placeholder skills.
- Preserve UNSET when the user defers a decision and require the pertinent task agent to ask before the operation needs it.
- Do not infer selectors from files, remotes, hosting metadata, templates, installed plugins, or available tools.
- Update the project template, create-project-configuration skill, project configurator role, and renderer source from the same selector contract.
- Generate root and nested AGENTS.md guidance that names the selected create, manage, and completion skills.
- Keep generated workflow guidance reference-only and do not inline workflow skill bodies or copy their procedures.
- Keep detected folder technology skills statically inlined by default under their existing separate mechanism.
- Make workflow references and technology inlining visibly distinct in generated guidance and tests.
- Preserve valid maintainer edits and report invalid or unsupported selector combinations instead of silently replacing them.
- Define migration and validation behavior for existing PROJECT.yaml files using simple-workitem, feature-branch-workitem, file-based-backlog, github-issues-backlog, none, or UNSET.

## Acceptance Criteria

- PROJECT.yaml records provider and completion choices independently.
- File plus feature-branch and GitHub plus direct-main are both valid combinations.
- Azure DevOps or Jira generates reference guidance to the matching unsupported skills and does not fall back.
- UNSET remains explicit and generates an ask-before-operation boundary.
- Invalid identifiers and combinations fail validation with actionable messages.
- AGENTS.md contains selected workflow skill names but none of their procedure bodies.
- Detected technology skill content remains inlined exactly as configured and is not converted to reference-only workflow guidance.
- No selector changes merely because a remote, backlog directory, provider tool, or template is present.
- Existing configuration receives deterministic migration guidance rather than silent semantic changes.

## Dependencies

- transform-file-work-item-skills.
- split-github-work-item-skills.
- add-gitlab-work-item-skills.
- add-azure-devops-and-jira-placeholders.
- add-direct-main-completion-skill.
- add-feature-branch-completion-skill.

## Verification

- Add renderer fixtures for every provider, both completion values, UNSET, none, folder overrides, unsupported placeholders, and invalid combinations.
- Assert generated AGENTS.md contains exact workflow references and no copied workflow headings or procedures.
- Assert detected technology skills remain fully inlined under matching folder routes.
- Add migration fixtures for every prototype selector value and maintainer-edited configuration.
- Run project configuration validation, renderer tests, Agent Skill validation, generated-output checks, full repository tests, project-wiki tests, and Git diff validation.

## Notes

- Reference-only workflow guidance is a deliberate exception from technology-skill inlining, not a global change to skill loading.
- The selector contract records user intent; it does not prove provider authentication or runtime capability.
