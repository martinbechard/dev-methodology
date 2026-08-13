---
name: manage-work-items-azure-devops
description: Report Azure DevOps work-item lifecycle management as unsupported and BLOCKED without provider, browser, network, GitHub, GitLab, or file mutation. Use when Azure DevOps is the selected work-item provider and an existing work item must be read or changed.
metadata:
  category: development-practice
---

# Manage Azure DevOps Work Items

The Work-item content is the Work-item authority and is stored according to the Persistence provider's specific format. Azure DevOps work-item management is not implemented in this bundle. This package preserves the selected provider and reports the capability boundary without substituting another provider.

## Work Item ID Boundary

A future implementation owns representation, lookup, collision checks, and stability for an Azure DevOps organization/project plus numeric work-item identity. Generic callers pass Work Item ID unchanged. This placeholder returns none and must not parse or fabricate one.

Acquire the exact opaque Work Item ID before any work or provider mutation. Use activity work for outcome work and activity update for provider mutation. Release the work-item claim with disposition done, blocked, or handoff at the activity boundary. Blocked may include a bounded blocker reference; when present, it must be canonical, non-empty, single-line, and at most 200 characters. A handoff release must complete before the next owner acquires the same ID. Path and resource claims remain independently applicable. The lifecycle state in the Work-item content remains authoritative. The current zero-mutation placeholder performs none of these claim events; a future supported implementation must apply them.

## Inventory Work Items

Return Required Result with Requested operation: inventory-work-items. Do not inspect Azure DevOps or any fallback source.

## Transition Work Item

Return Required Result with Requested operation: transition-work-item. Do not attempt a lifecycle mutation in Azure DevOps or any fallback source.

## Reconcile Work Item Completion

Return Required Result with Requested operation: reconcile-work-item-completion. Do not infer completion or attempt a terminal mutation.

## Recover Work Item

Return Required Result with Requested operation: recover-work-item. Do not inspect or mutate remote or local recovery state.

## Report Work Items

Return Required Result with Requested operation: report-work-items. Do not probe Azure DevOps or fabricate provider state for a report.

## Required Result

For every management request, return all of these fields:

- Status: BLOCKED.
- Provider: azure-devops.
- Requested operation: the requested public operation token from the matching procedure above; use manage only when no narrower operation was supplied.
- Missing capability: Azure DevOps work-item management is not implemented by this bundle.
- Work Item ID: none.
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

A request to reconcile completion for an Azure DevOps work item returns Status: BLOCKED, Provider: azure-devops, Requested operation: reconcile-work-item-completion, the missing implementation capability, no identifier, zero-mutation evidence, and the implementation decision required next. It does not inspect or update Azure DevOps or a local substitute.

## Implementation Boundary

A future implementation replaces this placeholder only through its owning source package and directly related tests. It must define Azure DevOps identifier and reference validation, supported lifecycle operations, authentication and authorization boundaries, concurrency behavior, failure recovery, mutation evidence, and no-shadow-queue guarantees before changing the required result.
