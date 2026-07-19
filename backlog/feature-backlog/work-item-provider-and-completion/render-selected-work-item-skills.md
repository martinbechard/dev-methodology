# Render Selected Work-Item Skills

Status: Proposed

Type: Feature

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
