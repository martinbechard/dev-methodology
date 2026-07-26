---
name: agent-claim
description: Use when an event in this skill requires temporary protection for a shared file or resource.
metadata:
  category: development-practice
---

# Agent Claim

Claims prevent two agents from changing the same shared file or resource at the same time. A claim does not prove that work is complete.

Git provides one primary worktree for a repository. The primary worktree owns the backlog and the main branch. Other worktrees are private working copies.

## Claim Events

Acquire a claim only for an event in this table. Acquire it immediately before starting that event. Release it at the boundary shown in the same row.

| No. | Event | Claim | Release |
|---:|---|---|---|
| 1 | Edit or move an existing backlog item in the primary worktree | Each current backlog path and each destination path. | After the backlog commit succeeds, or after a verified no-change result. |
| 2 | Perform any non-backlog work in the primary worktree | project-files: every path in the primary worktree except backlog. | After changes are committed or a verified no-change result is recorded. |
| 3 | Use a shared browser session or its shared server | browser-test:&lt;id&gt;. | After the claimed session or server stops or is handed off. |
| 4 | Use a shared database | database:&lt;id&gt;. | After database work finishes and the claimed database is restored, stopped, or handed off. |
| 5 | Start or use a shared network listener | port:&lt;number&gt;. | After the claimed listener stops or is handed off. |
| 6 | Call a shared live model or run a suite against it | live-model:&lt;provider&gt;:&lt;suite&gt;. | After the claimed call or suite ends and its evidence is saved. |
| 7 | Change a shared installed runtime | shared-install:&lt;target&gt;. | After the claimed installation is verified and stable. |
| 8 | Change a shared deployment | deployment:&lt;environment&gt;. | After the claimed deployment or rollback reaches a verified final state. |

## Shared Claim Records

In each example, &lt;project-root&gt; represents an absolute project-root path.

Git stores repository-wide metadata in a directory called the Git common directory.

For example, &lt;project-root&gt; and &lt;project-root&gt;/.worktrees/task-123 both use &lt;project-root&gt;/.git.

Store a claim registry named agent-claims.json in the Git common directory. Every worktree connected to that Git common directory uses this registry.

Store claim history in an agent-claim-events directory next to the registry. For example:

- &lt;project-root&gt;/.git/agent-claim-events/hot/2026-07-26.jsonl stores events from July 26 UTC.
- &lt;project-root&gt;/.git/agent-claim-events/archive/2026/07/2026-07-24.jsonl.gz stores compressed events from July 24 UTC.
- &lt;project-root&gt;/.git/agent-claim-events/journal/2026/07/2026-07-24.json stores a summary for July 24 UTC.

Store claim identifiers, scopes, outcomes, conflicts, and related commit identifiers in claim history.

Do not store prompts, reasoning, responses, arbitrary tool output, task descriptions, personal information, or sensitive company information.

## Claim Scope

Claim scope is the file, set of files, or shared resource that a claim protects.

Every claim request must specify a scope. Use the Claim column in the Claim Events table to select that scope.

A project-files claim must also include a short reason explaining why the work must occur in the primary worktree.

Request a claim for a backlog file from the primary worktree. A backlog request from a private worktree returns SHARED_CHECKOUT_REQUIRED and does not acquire a claim.

For example, a request for backlog/feature-backlog/item.md from &lt;project-root&gt;/.worktrees/task-123 returns SHARED_CHECKOUT_REQUIRED.

The same request from &lt;project-root&gt; can continue.

If a backlog update later requires another backlog file, add that file to the active claim before editing it.

## Claim Conflicts

An overlapping request returns CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED when another live claim owns its file or resource. Save that result because it identifies an existing owner and a conflict.

Do not change a file or use a resource owned by that live claim.

Ask its owner for a release or recovery notification. Retry only after receiving that notification.

Do not poll, schedule retries, or acquire another claim to record that you are waiting.

Treat every live claim as valid. A configured watchdog decides whether a live claim is stale.

## Timed Resource Claims

A heartbeat is a signal that a claim owner is active. Send heartbeats during long resource use. A heartbeat does not extend a deadline.

PROJECT.yaml sets two limits for each resource class:

- A maximum duration limits how long active resource work may continue.
- A cleanup grace period allows only shutdown, evidence preservation, and release after the maximum duration.

These claim resources use the listed resource classes:

| Claim resource | Resource class |
|---|---|
| browser-test | browser-server |
| database and port | database-port |
| live-model | live-model-evaluation |
| shared-install and deployment | main-integration |

Supply an expected duration and a requested hard-stop duration. The expected duration must not exceed the requested hard-stop duration. The requested hard-stop duration must not exceed the configured maximum.

Extend a resource deadline only when concrete evidence explains why more time is needed. Measure an extension from the time its resource claim was acquired. Never extend beyond a configured maximum.

Claim status is read-only. It reports overdue resource claims but never releases one. A configured watchdog investigates an overdue claim whose owner has stopped.

## Claim Helper Recovery

RECONCILIATION_RECOVERY_REQUIRED means that an earlier claim operation did not finish safely.

Run claim status once. If the same result returns, stop claim mutations. Send that status result, the claim registry, and claim history to Project Configurator. Do not edit or remove those records or the protected claim.
