# Work-Item Provider And Completion Contracts

## Goal

Separate authoritative work-item storage from delivery completion so projects can independently select a file, GitHub, GitLab, Azure DevOps, or Jira provider and either direct-main or feature-branch completion without duplicated queues, inferred policy, or provider-inaccurate publication behavior.

## Purpose

PROJECT.yaml should record two independent selectors: where work items are created and managed, and how verified implementation reaches its terminal delivery state. Generated AGENTS.md guidance should reference only the selected workflow skill names. It must not inline workflow procedures or confuse those selectors with setup-time detected technology-skill inlining.

This series plans the transformation only. It does not implement, rename, delete, generate, publish, or deploy any skill. The prototype integration commit aeb7bc4 introduced execute-workitem, file-based-backlog, github-issues-backlog, and workflow-selection rendering. Its refined mainline form is commit c18d476 from pull request 8, merged by f7e247a. Implementers should reuse that evidence together with the existing create-backlog, manage-backlog, create-pull-request, agent-work-merge, and agent-claim contracts.

## Design Anchors

- Work-item provider and completion process are independent selectors.
- File-backed work items are authoritative only under backlog on the primary main worktree.
- GitHub and GitLab use their provider tools and never create shadow file-backed items.
- Azure DevOps and Jira remain explicit unsupported placeholders until separately implemented; they return BLOCKED without fallback or external mutation.
- Provider skills use symmetric create and manage names.
- Direct-main completion means the final verified commit is integrated into main.
- Feature-branch publication alone is not completion; work remains AWAITING_REVIEW until configured review and merge evidence exists.
- PROJECT.yaml owns selector intent. AGENTS.md references selected workflow skill names without copying or inlining their procedures.
- Technology-skill detection and inlining remain a separate setup concern.
- No selector is inferred from repository files, remotes, hosting metadata, available tools, or existing backlog artifacts.

## Migration Map

- create-backlog becomes create-file-work-item.
- manage-backlog becomes manage-file-work-items.
- file-based-backlog is absorbed into the file provider skills and retired.
- github-issues-backlog becomes create-github-work-item and manage-github-work-items.
- GitLab adds create-gitlab-work-item and manage-gitlab-work-items.
- Azure DevOps adds create-azure-devops-work-item and manage-azure-devops-work-items as unsupported placeholders.
- Jira adds create-jira-work-item and manage-jira-work-items as unsupported placeholders.
- execute-workitem process references become complete-work-item-direct-main and complete-work-item-feature-branch.
- create-pull-request remains a subordinate publication capability only when its final provider contract is accurate; GitLab delivery uses merge-request terminology and tools.

## Non-Goals

- Implementing an Azure DevOps or Jira integration in this series.
- Creating file mirrors of provider-backed work items.
- Inlining workflow skill bodies into PROJECT.yaml or AGENTS.md.
- Replacing technology detection or its folder-specific inlining behavior.
- Treating pull or merge request creation as evidence that implementation is merged.
- Inferring project policy from whichever provider tool happens to be available.

## Recommended Order

1. [Define provider and completion selector contracts](define-provider-and-completion-selector-contracts.md).
2. After the contract is accepted, proceed in parallel with:
   - [Transform file work-item skills](transform-file-work-item-skills.md).
   - [Split GitHub work-item skills](split-github-work-item-skills.md).
   - [Add GitLab work-item skills](add-gitlab-work-item-skills.md).
   - [Add Azure DevOps and Jira placeholders](add-azure-devops-and-jira-placeholders.md).
   - [Add direct-main completion](add-direct-main-completion-skill.md).
   - [Add feature-branch completion](add-feature-branch-completion-skill.md).
3. [Render selected work-item skills](render-selected-work-item-skills.md) after every provider and completion identifier stabilizes.
4. [Integrate work-item contracts across the bundle](integrate-work-item-contracts-across-bundle.md) after selector rendering is accepted.

## Definition Of Good

- Every provider has symmetric create and manage identifiers with one authoritative storage boundary.
- Unsupported providers block explicitly without fallback or mutation.
- Provider and completion choices compose independently.
- Direct-main and feature-branch completion have truthful, distinct terminal evidence.
- PROJECT.yaml validation rejects invalid combinations while preserving UNSET and user-decision behavior.
- Generated AGENTS.md names selected workflow skills without embedding them.
- Roles, metadata, adapters, documentation, evals, migration guidance, and installed behavior agree with the canonical contracts.
