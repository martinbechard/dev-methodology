---
name: manage-jira-work-items
description: Report Jira issue lifecycle management as unsupported and BLOCKED without provider, browser, network, GitHub, GitLab, or file mutation. Use when Jira is the selected work-item provider and an existing issue must be read or changed.
metadata:
  category: development-practice
---

# Manage Jira Work Items

Jira issue management is not implemented in this bundle. This package preserves the selected provider and reports the capability boundary without substituting another provider.

## Required Result

For every management request, return all of these fields:

- Status: BLOCKED.
- Provider: jira.
- Requested operation: the requested read, inspect, update, transition, assign, comment, link, close, reopen, reconcile, or other management operation; use manage when no narrower operation was supplied.
- Missing capability: Jira issue management is not implemented by this bundle.
- Work-item identifier: none.
- Mutation evidence: no Jira, Azure DevOps, generic HTTP, browser, GitHub, GitLab, or file mutation was attempted.
- Next authority or implementation decision: explicitly authorize and implement the Jira provider contract, tools, authentication boundary, and focused tests before retrying.

Do not report READY, COMPLETED, a persisted lifecycle transition, or a success-shaped issue key or URL.

## No-Fallback Boundary

- Do not call Jira, Azure DevOps, generic HTTP, browser, GitHub, GitLab, or filesystem tools, including for read-only discovery that would imply provider support.
- Do not create or update a repository backlog item, placeholder issue, local cache, queued request, synthetic issue key, or synthetic URL.
- Do not replace jira with file, github, gitlab, azure-devops, none, or UNSET.
- Do not treat an installed connector, authenticated session, environment variable, or incidental credential as implemented support or mutation authority.
- Do not infer remote state, lifecycle state, or completion from request text, a stopped task, a branch, or a commit.

## Example

A request to transition a Jira issue returns Status: BLOCKED, Provider: jira, Requested operation: transition, the missing implementation capability, no identifier, zero-mutation evidence, and the implementation decision required next. It does not inspect or update Jira or a local substitute.

## Implementation Boundary

A future implementation replaces this placeholder only through its owning source package and directly related tests. It must define Jira issue-key and browse-reference validation, supported lifecycle operations, authentication and authorization boundaries, concurrency behavior, failure recovery, mutation evidence, and no-shadow-queue guarantees before changing the required result.
