# Define Provider And Completion Selector Contracts

Status: Proposed

Type: Feature

## Summary

Establish the canonical provider, completion, identifier, authority, state, and migration contracts that every later work-item skill and project selector must implement.

## Context

This is the foundation item in the [Work-Item Provider And Completion Contracts series](index.md). Commit c18d476 supplies a working selector prototype, while aeb7bc4 preserves the earlier integration evidence named by the planning request. The prototype combines some provider and completion responsibilities under execute-workitem, file-based-backlog, and github-issues-backlog. Later items must not rename or split those skills independently without one accepted cross-provider contract.

## Requirements

- Define supported provider selector values for file, github, gitlab, azure-devops, jira, none, and UNSET.
- Define supported completion selector values for direct-main, feature-branch, and UNSET.
- Keep provider and completion selectors independent and define their valid combination matrix.
- Define the canonical symmetric create and manage skill identifiers for every provider.
- Define complete-work-item-direct-main and complete-work-item-feature-branch as the canonical completion identifiers.
- Define creation, ownership, lifecycle, recovery, delivery-reference, terminal-state, and evidence fields shared across providers.
- Define provider-specific identifiers and URL or reference shapes without flattening GitHub issues, GitLab issues, Azure DevOps work items, Jira issues, pull requests, and merge requests into inaccurate terminology.
- Define file authority exclusively under backlog on the primary main worktree.
- Define GitHub and GitLab provider-tool authority and prohibit shadow repository files.
- Define Azure DevOps and Jira placeholder behavior as unsupported and BLOCKED without fallback, local queue creation, or external mutation.
- Define direct-main completion as successful only when the final verified commit is integrated into main and observed there.
- Define feature-branch completion states so publication returns AWAITING_REVIEW until required review, checks, and merge evidence exist, followed by completion only after the configured merge is observed.
- Preserve UNSET and explicit user-decision behavior. Prohibit inference from remotes, files, templates, provider tools, or hosting metadata.
- Define the migration map from create-backlog, manage-backlog, file-based-backlog, github-issues-backlog, execute-workitem, and create-pull-request.
- Define compatibility, deprecation, stale-name sweep, generated-artifact, and installed-bundle expectations before implementation begins.

## Acceptance Criteria

- One reviewed contract lists every supported selector, provider skill pair, completion skill, state transition, evidence field, and invalid combination.
- File-backed, GitHub-backed, and GitLab-backed examples can each combine with direct-main or feature-branch completion.
- Azure DevOps and Jira examples terminate BLOCKED without creating a file item or calling an external mutation.
- Direct-main examples end only after the commit is present on main.
- Feature-branch examples distinguish branch publication, AWAITING_REVIEW, merge evidence, and final completion.
- The migration map assigns one owner and disposition to every prototype and legacy identifier.
- No contract infers a selector from repository or tool evidence.
- Downstream provider, completion, renderer, role, and eval items can cite the contract without inventing additional policy.

## Dependencies

None.

## Verification

- Review the contract against create-backlog, manage-backlog, create-pull-request, agent-work-merge, agent-claim, execute-workitem, file-based-backlog, github-issues-backlog, and PROJECT.yaml selector sources.
- Walk every provider and completion combination through creation, execution, review, merge, backlog update, failure, unsupported, and recovery states.
- Verify all identifiers follow the methodology naming contract and remain symmetric across providers.
- Verify the migration map covers source skills, role references, metadata, generated adapters, design pages, evals, tests, examples, and installed artifacts.
- Run documentation and Markdown validation plus Git diff validation for the planning artifact.

## Notes

- This item defines contracts and migration decisions; it does not perform the renames or implement provider tools.
- Provider-specific terminology may differ while the shared lifecycle fields remain compatible.
