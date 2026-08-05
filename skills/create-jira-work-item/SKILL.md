---
name: create-jira-work-item
description: Report Jira issue creation as unsupported and BLOCKED without provider, browser, network, GitHub, GitLab, or file mutation. Use when Jira is the selected work-item provider and a new durable issue is requested.
metadata:
  category: development-practice
---

# Create Jira Work Item

Jira issue creation is not implemented in this bundle. This package preserves the selected provider and reports the capability boundary without substituting another provider.

## Work Item ID Boundary

A future implementation owns representation, lookup, collision checks, and stability for the Jira site/project issue key. Generic callers pass Work Item ID unchanged. This placeholder returns none and must not fabricate an ID or diagnostic URL.

## Create Work Item

For every creation request, return all of these fields:

- Status: BLOCKED.
- Provider: jira.
- Requested operation: create.
- Missing capability: Jira issue creation is not implemented by this bundle.
- Work Item ID: none.
- Mutation evidence: no Jira, Azure DevOps, generic HTTP, browser, GitHub, GitLab, or file mutation was attempted.
- Next authority or implementation decision: explicitly authorize and implement the Jira provider contract, tools, authentication boundary, and focused tests before retrying.

Do not report READY, success, or a success-shaped issue key or URL.

## No-Fallback Boundary

- Do not call Jira, Azure DevOps, generic HTTP, browser, GitHub, GitLab, or filesystem mutation tools.
- Do not create a repository backlog item, placeholder issue, local cache, queued request, synthetic issue key, or synthetic URL.
- Do not replace jira with file, github, gitlab, azure-devops, none, or UNSET.
- Do not treat an installed connector, authenticated session, environment variable, or incidental credential as implemented support or mutation authority.
- Do not probe provider availability when the only supported outcome is BLOCKED.

## Example

A request to create a Jira issue for a feature returns Status: BLOCKED, Provider: jira, Requested operation: create, the missing implementation capability, no identifier, zero-mutation evidence, and the implementation decision required next. It does not call a provider or create a local substitute.

## Implementation Boundary

A future implementation replaces this placeholder only through its owning source package and directly related tests. It must define Jira site and project inputs, issue-key and browse-reference shapes, authentication and authorization boundaries, creation behavior, failure recovery, mutation evidence, and no-shadow-queue guarantees before changing the required result.
