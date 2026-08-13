---
name: resource-claim
description: Use when an event in this skill requires temporary protection for a shared file or resource.
metadata:
  category: development-practice
---
<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: be32b4bc-43bb-437f-8941-40671f28c7bd
Created-UTC: historical-unknown
Creating-Agent: historical-unknown
Runtime: historical-unknown
Dispatched-Model: historical-unknown
Reasoning-Effort: historical-unknown
Task-ID: historical-unknown
Artifact-ID-Evidence: migration-assigned
Created-UTC-Evidence: historical-unknown
Creating-Agent-Evidence: historical-unknown
Runtime-Evidence: historical-unknown
Dispatched-Model-Evidence: historical-unknown
Reasoning-Effort-Evidence: historical-unknown
Task-ID-Evidence: historical-unknown
-->

# Resource Claim

Claims prevent two agents from changing the same shared file or resource at the same time. Exact work-item claims also prevent concurrent activity on one opaque Work Item ID. A claim and its release do not prove that work is complete.

The claim system tracks declared ownership and scope overlap only. Acquisition, extension,
status, and release do not inspect or gate on staged, unstaged, untracked, renamed, or deleted
files. Git owns dirty-worktree protection, overwrite refusal, merge conflicts, and commit
contents.

Git provides one primary worktree for a repository. The primary worktree owns the backlog and the main branch. Other worktrees are private working copies.

## Project Configuration Gate

### Declared Backlog-Crisis Exception

When resolve-backlog-blockage records an active crisis epoch, its Coordinator uses regular SOLO mode and this skill is temporarily NOT_APPLICABLE for the entire crisis epoch. After the one required entry reset, do not load or invoke a claim helper and do not perform even read-only claim status, report, or journal-maintenance operations. The one active separate work-item task may mutate its crisis item without a claim; the Coordinator remains the dispatcher. This exception ends only after every crisis-set item is terminal and resolve-backlog-blockage records crisis exit and restoration of regular MULTITASK mode. Ordinary configured claim behavior then resumes; never reconstruct crisis-era live claims.

Before loading a claim helper or reading claim state, require a valid PROJECT.yaml at the repository root that explicitly selects resource-claim.

When the root file is absent, resource coordination is NOT_APPLICABLE. Do not load or invoke resource-claim-helper, a configured resource-claim-helper-* Provider Skill, or a claim registry. Do not read claim state, create claim state, or mutate claim state.

When the root file is valid and selects none, resource coordination is also NOT_APPLICABLE. Keep the helper and claim state untouched.

When the root file exists but fails its applicable validation gate, stop with the validation failure. Do not load a helper or access claim state.

The missing-file fallback establishes only the effective SOLO coordination mode. It does not select a Persistence or Commit default. This resource-coordination gate does not disable an explicitly selected Persistence or Commit Provider Skill; those provider families remain governed by their independent selectors.

A valid explicit resource-claim selection replaces the fallback. Preserve all configured claim events, helper behavior, deadlines, and stored state on that path.

## Coordinate Shared Resource

Use the Claim Events table to decide whether work requires temporary ownership. If a row matches, use its scope and release boundary, then apply the resource-claim-helper operation contract through the configured resource-claim-helper-* Provider Skill. If no row matches, continue without acquiring a claim.

This skill owns claim policy. resource-claim-helper owns the common operation, input, result, and uncertain-outcome contract. The selected resource-claim-helper-* Provider Skill explains only how to invoke that contract.

## Claim Events

Acquire a claim only for an event in this table. Acquire it immediately before starting that event. Release it at the boundary shown in the same row.

| No. | Event | Claim | Release |
|---:|---|---|---|
| 1 | Edit or move an existing backlog item in the primary worktree | Each current backlog path and each destination path. | After the backlog mutation event ends or ownership is handed off. |
| 2 | Perform any non-backlog work in the primary worktree | project-files: every path in the primary worktree except backlog. | After the primary-worktree event ends or ownership is handed off. |
| 3 | Use a shared browser session or its shared server | browser-test:&lt;id&gt;. | After the claimed session or server stops or is handed off. |
| 4 | Use a shared database | database:&lt;id&gt;. | After database work finishes and the claimed database is restored, stopped, or handed off. |
| 5 | Start or use a shared network listener | port:&lt;number&gt;. | After the claimed listener stops or is handed off. |
| 6 | Call a shared live model or run a suite against it | live-model:&lt;provider&gt;:&lt;suite&gt;. | After the claimed call or suite ends and its evidence is saved. |
| 7 | Change a shared installed runtime | shared-install:&lt;target&gt;. | After the claimed installation is verified and stable. |
| 8 | Change a shared deployment | deployment:&lt;environment&gt;. | After the claimed deployment or rollback reaches a verified final state. |
| 9 | Perform outcome work or mutate Work-item content through its selected Persistence provider | The exact opaque Work Item ID with activity work or update. | At the activity boundary, with disposition done, blocked, or handoff. |

## Shared Claim Records

In each example, &lt;project-root&gt; represents the primary worktree's absolute project-root path.

Store shared claim state under &lt;project-root&gt;/.agent-ops/resource-claim. The registry name agent-claims.json and history name agent-claim-events remain compatibility identifiers. The helper migrates only an empty rejected .codex/agent-claim registry while preserving its audit history; live or contradictory legacy state stops without mutation.

Resolve this directory from the primary worktree so every linked worktree uses the same registry and history.

Apply the exclusive OS lock directly to agent-claims.json. Read and update the registry through that locked file without replacing its inode. Do not create a separate claim lock file.

Store claim history in an agent-claim-events directory beside the registry. For example:

- &lt;project-root&gt;/.agent-ops/resource-claim/agent-claim-events/hot/2026-07-26.jsonl stores events from July 26 UTC.
- &lt;project-root&gt;/.agent-ops/resource-claim/agent-claim-events/archive/2026/07/2026-07-24.jsonl.gz stores compressed events from July 24 UTC.
- &lt;project-root&gt;/.agent-ops/resource-claim/agent-claim-events/journal/2026/07/2026-07-24.json stores a summary for July 24 UTC.

Store claim identifiers, scopes, outcomes, conflicts, and related commit identifiers in claim history.

Do not store prompts, reasoning, responses, arbitrary tool output, task descriptions, personal information, or sensitive company information.

## Claim Scope

Claim scope is the file, set of files, or shared resource that a claim protects.

Every claim request must specify a scope. Use the Claim column in the Claim Events table to select that scope.

A work-item scope contains one canonical non-empty single-line Work Item ID of at most 200 characters and activity exactly work or update. The ID is opaque: the claim system compares the complete value for equality and does not parse provider, path, repository, issue, or lifecycle metadata from it. A live claim conflicts with every request for the same Work Item ID regardless of activity. Distinct IDs coexist.

Keep work-item claims separate from path and resource claims. Path and resource claims remain independently applicable when their Claim Events occur; they do not replace the work-item claim and the work-item claim does not replace them.

A project-files claim must also include a short reason explaining why the work must occur in the primary worktree.

Request a claim for a backlog file from the primary worktree. A backlog request from a private worktree returns SHARED_CHECKOUT_REQUIRED and does not acquire a claim.

For example, a request for backlog/feature-backlog/item.md from &lt;project-root&gt;/.worktrees/task-123 returns SHARED_CHECKOUT_REQUIRED.

The same request from &lt;project-root&gt; can continue.

## Acquire Claim

Acquire a claim immediately before the matching event starts. Request the scope selected from the Claim Events table and supply every identity, reason, duration, and deadline field required for that scope.

Read the structured claim outcome and follow the applicable policy in this skill. Acquisition does not prove that work started or completed.

## Claim Conflicts

An overlapping request returns CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED when another live claim owns its file or resource. Save that result because it identifies an existing owner and a conflict.

Do not change a file or use a resource owned by that live claim.

Ask its owner for a release or recovery notification. Retry only after receiving that notification.

Do not poll, schedule retries, or acquire another claim to record that you are waiting.

Treat every live claim as valid. A configured watchdog decides whether a live claim is stale.

## Extend Claim

Extend an active claim before adding a net-new file or resource to the event. Request only the additional scope and its required resource fields. Do not use extension to replace an existing owner or bypass a conflict outcome.

For example, if a backlog update later requires another backlog file, extend the active claim with that file before editing it.

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

## Extend Claim Deadline

Extend a resource deadline only when concrete evidence explains why more time is needed. Measure an extension from the time its resource claim was acquired. Never extend beyond a configured maximum. A deadline extension changes no claim scope.

## Heartbeat Claim

Send a heartbeat during long resource use to show that the owner remains active. A heartbeat does not extend a deadline, change scope, or resolve an overdue claim.

## Read Claim Status

Read claim status to inspect live ownership and overdue resource claims. Status is read-only. It never acquires, extends, or releases a claim.

If a mutating claim operation has an uncertain outcome, do not repeat it. Read status through the same configured claim helper, reconcile the reported claim state, and continue from that state. If that helper cannot return status, ask Project Configurator to restore the configured helper instead of switching providers or guessing.

Status reports overdue resource claims but never releases one. A configured watchdog investigates an overdue claim whose owner has stopped.

## Release Claim

Release the exact named live claim when the matching event ends or ownership is handed off. Release no other claim and treat cleanup as separate from completion, delivery, and Work-item lifecycle state.

Release of a work-item claim requires disposition exactly done, blocked, or handoff. Blocked may include one blocker reference; when present, it must be a canonical non-empty single-line opaque value of at most 200 characters. A blocker reference is prohibited for done and handoff. Invalid combinations are rejected without changing the live registry. Release of a non-work-item claim keeps the legacy disposition-free behavior.

Use ordinary exclusivity for a strict handoff: the current owner releases with handoff, then the next owner acquires the same Work Item ID. Never acquire the successor while the prior claim remains live or use a path or resource claim to bypass same-ID contention.

## Release Cleanup

Release is claim cleanup only. While holding the registry lock, locate the exact named live claim, validate required work-item release evidence, remove only that claim, persist the registry through the locked file, and append a RELEASED journal event.

Release does not inspect or gate on worktree cleanliness, branches, baseline or current HEAD, ancestry, commits, file contents, delivery state, no-change evidence, or out-of-domain changes. Keep completion, delivery, Work-item lifecycle, and claim cleanup as separate operations.

Structured claim outcomes and technical claim cleanup or recovery remain agent-owned. Do not turn them into User Action Required unless a separate genuine user-owned decision remains after applying this skill.
