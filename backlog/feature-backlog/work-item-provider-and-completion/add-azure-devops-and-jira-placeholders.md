# Add Azure DevOps And Jira Placeholders

Status: Proposed

Type: Feature

## Summary

Add symmetric Azure DevOps and Jira create and manage skill packages that make the selectors and migration matrix complete while explicitly returning unsupported and BLOCKED without fallback or external mutation.

## Context

This item is a provider lane in the [Work-Item Provider And Completion Contracts series](index.md). Azure DevOps and Jira are required selector placeholders, not implemented providers. Explicit packages let project validation name the intended provider and report a truthful capability boundary instead of silently selecting files, GitHub, GitLab, or an arbitrary external API.

## Requirements

- Add create-azure-devops-work-item and manage-azure-devops-work-items skill packages.
- Add create-jira-work-item and manage-jira-work-items skill packages.
- Keep every directory name, frontmatter name, description, Codex metadata record, example, and eval identifier symmetric and provider-qualified.
- State that creation and management are unsupported in the current bundle.
- Return BLOCKED with the selected provider, requested operation, missing capability, and next authority or implementation decision.
- Do not call an Azure DevOps, Jira, generic HTTP, browser, GitHub, GitLab, or file mutation as fallback.
- Do not create a backlog file, placeholder external ticket, local cache, or success-shaped identifier.
- Do not treat an installed connector or incidental credential as authorization or implemented support.
- Keep the placeholders discoverable in the supported identifier matrix without claiming behavioral support.
- Define the source and verification changes required when either provider is implemented later.

## Acceptance Criteria

- All four symmetric skill identifiers exist and validate structurally.
- Each create or manage request returns a clear BLOCKED result and no work-item identifier.
- File, GitHub, GitLab, Azure DevOps, Jira, browser, and network mutation spies record no calls.
- PROJECT.yaml can preserve an Azure DevOps or Jira selection without replacing it with another provider.
- Generated guidance names the selected placeholder and its unsupported status truthfully.
- Support documentation distinguishes catalog availability from implemented provider behavior.
- A later implementation has one explicit source package and regression boundary to replace rather than an implicit fallback to unwind.

## Dependencies

define-provider-and-completion-selector-contracts.

## Verification

- Add deterministic tests for create and manage requests against both providers.
- Assert exact BLOCKED status fields and zero mutation or fallback calls.
- Validate source skills and Codex metadata, regenerate affected catalogs, and inspect support-status wording.
- Add selector tests proving values remain stable and are not normalized to file, GitHub, or GitLab.
- Run full repository tests, project-wiki tests, and Git diff validation.

## Notes

- These packages are intentional unsupported adapters, not stubs that report READY.
- Installing a future provider connector does not activate support until the owning skill contract and tests are implemented.
