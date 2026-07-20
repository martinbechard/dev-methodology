---
name: manage-azure-devops-work-items
description: Report Azure DevOps work-item lifecycle management as unsupported and BLOCKED without provider, browser, network, GitHub, GitLab, or file mutation. Use when Azure DevOps is the selected work-item provider and an existing work item must be read or changed.
metadata:
  category: development-practice
---

# Manage Azure DevOps Work Items

Azure DevOps work-item management is not implemented in this bundle. This package preserves the selected provider and reports the capability boundary without substituting another provider.

## Required Result

For every management request, return all of these fields:

- Status: BLOCKED.
- Provider: azure-devops.
- Requested operation: the requested read, inspect, update, transition, assign, comment, link, close, reopen, reconcile, or other management operation; use manage when no narrower operation was supplied.
- Missing capability: Azure DevOps work-item management is not implemented by this bundle.
- Work-item identifier: none.
- Mutation evidence: no Azure DevOps, Jira, generic HTTP, browser, GitHub, GitLab, or file mutation was attempted.
- Next authority or implementation decision: explicitly authorize and implement the Azure DevOps provider contract, tools, authentication boundary, and focused tests before retrying.

Do not report READY, COMPLETED, a persisted lifecycle transition, or a success-shaped identifier.

## No-Fallback Boundary

- Do not call Azure DevOps, Jira, generic HTTP, browser, GitHub, GitLab, or filesystem tools, including for read-only discovery that would imply provider support.
- Do not create or update a repository backlog item, placeholder ticket, local cache, queued request, or synthetic URL.
- Do not replace azure-devops with file, github, gitlab, jira, none, or UNSET.
- Do not treat an installed connector, authenticated session, environment variable, or incidental credential as implemented support or mutation authority.
- Do not infer remote state, lifecycle state, or completion from request text, a stopped task, a branch, or a commit.

## Example

A request to close an Azure DevOps work item returns Status: BLOCKED, Provider: azure-devops, Requested operation: close, the missing implementation capability, no identifier, zero-mutation evidence, and the implementation decision required next. It does not inspect or update Azure DevOps or a local substitute.

## Implementation Boundary

A future implementation replaces this placeholder only through its owning source package and directly related tests. It must define Azure DevOps identifier and reference validation, supported lifecycle operations, authentication and authorization boundaries, concurrency behavior, failure recovery, mutation evidence, and no-shadow-queue guarantees before changing the required result.
