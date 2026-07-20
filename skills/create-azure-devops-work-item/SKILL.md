---
name: create-azure-devops-work-item
description: Report Azure DevOps work-item creation as unsupported and BLOCKED without provider, browser, network, GitHub, GitLab, or file mutation. Use when Azure DevOps is the selected work-item provider and a new durable work item is requested.
metadata:
  category: development-practice
---

# Create Azure DevOps Work Item

Azure DevOps work-item creation is not implemented in this bundle. This package preserves the selected provider and reports the capability boundary without substituting another provider.

## Required Result

For every creation request, return all of these fields:

- Status: BLOCKED.
- Provider: azure-devops.
- Requested operation: create.
- Missing capability: Azure DevOps work-item creation is not implemented by this bundle.
- Work-item identifier: none.
- Mutation evidence: no Azure DevOps, Jira, generic HTTP, browser, GitHub, GitLab, or file mutation was attempted.
- Next authority or implementation decision: explicitly authorize and implement the Azure DevOps provider contract, tools, authentication boundary, and focused tests before retrying.

Do not report READY, success, or a success-shaped identifier.

## No-Fallback Boundary

- Do not call Azure DevOps, Jira, generic HTTP, browser, GitHub, GitLab, or filesystem mutation tools.
- Do not create a repository backlog item, placeholder ticket, local cache, queued request, or synthetic URL.
- Do not replace azure-devops with file, github, gitlab, jira, none, or UNSET.
- Do not treat an installed connector, authenticated session, environment variable, or incidental credential as implemented support or mutation authority.
- Do not probe provider availability when the only supported outcome is BLOCKED.

## Example

A request to create an Azure DevOps work item for a defect returns Status: BLOCKED, Provider: azure-devops, Requested operation: create, the missing implementation capability, no identifier, zero-mutation evidence, and the implementation decision required next. It does not call a provider or create a local substitute.

## Implementation Boundary

A future implementation replaces this placeholder only through its owning source package and directly related tests. It must define Azure DevOps organization and project inputs, numeric work-item identifier and reference shapes, authentication and authorization boundaries, creation behavior, failure recovery, mutation evidence, and no-shadow-queue guarantees before changing the required result.
