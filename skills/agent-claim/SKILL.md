---
name: agent-claim
description: Use when PROJECT.yaml selects agent-claim for repository paths or exclusive resources, including atomic scope extension, journals, contention reporting, worktree isolation, recovery, and clean release.
metadata:
  category: development-practice
---

# Agent Claim

Use this skill only when the project-wide resource_coordination selection is agent-claim and an event in the owning contract below occurs. When the selection is none, perform no claim operation and require no claim evidence. Apply the one claim-helper invocation interface selected by Project Configurator. The compatibility field agent_claim_transport records that implementation-interface selection. This skill owns coordination semantics and never chooses, probes, or changes the configured interface.

For the command-line interface, the implementation flow is Python claim command -> claim helper -> claim registry and journal. The command parser and helper functions live in skills/agent-claim-command/scripts/claim.py; the helper writes repository-global registry and journal state under the Git common directory.

## Goal

Claims temporarily protect shared mutation events. Work-item ownership, private-worktree delivery, commits, review, verification, and lifecycle records remain the durable authorities for completed work.

Start with the narrow scope supported by current evidence. Extend the same claim atomically when another file or resource becomes necessary. Do not speculate about entire directories merely because future scope is unknown.

## Event Contract

This table is the complete event-to-claim contract.

| Event | Claim rule |
|---|---|
| Update an existing work item | Claim the exact current backlog path and, for a move or rename, the destination path. |
| Perform any non-backlog work in the primary worktree | Claim project-files. |
| Use a shared browser | Claim browser-test:&lt;id&gt;. |
| Use a shared database | Claim database:&lt;id&gt;. |
| Use a shared port | Claim port:&lt;number&gt;. |
| Use a shared live model | Claim live-model:&lt;provider&gt;:&lt;suite&gt;. |
| Change a shared installed runtime | Claim shared-install:&lt;target&gt;. |
| Change a shared deployment | Claim deployment:&lt;environment&gt;. |

Creating a uniquely named new work-item file needs no claim and must use atomic no-overwrite creation.

Private-worktree editing, generation, build, test, commit, and rebase need no claim. Build outputs and caches must remain worktree-local, and unique work-item remote branches need no claim.

Live claims are presumed valid; only the watchdog investigates stale ownership. Interrupted private-worktree changes belong to their work item and are resumed there.

Before finish, release, or handoff, commit completed work and prove the applicable worktree clean.

## Coordination Registry Authority

The coordination registry is temporary conflict protection for shared mutation. It records which exact paths and exclusive resources currently require protection so concurrent owners do not collide. It does not decide whether reviewed, verified, committed product delivery exists, whether accepted bytes are integrated, or whether a work item is complete.

Treat acquisition, wait, heartbeat, release, and release-validation outcomes as coordination evidence. Reconcile those diagnostics with the durable work item, Git commits and content, review evidence, verification evidence, processes, worktrees, and resource state. A coordination failure does not erase evidence owned by those other records.

## Repository-Global State

The Git common directory is the default repository-global coordination boundary. The live agent-claims.json registry in that directory is authoritative across linked worktrees. Use a configured repository-global path supplied by applicable project instructions when Git worktrees are not the coordination boundary. The agent-claim-events directory beside the registry contains diagnostic history:

- hot contains today and yesterday as uncompressed UTC daily JSON Lines files under the default policy.
- archive contains immutable compressed daily JSON Lines history.
- journal contains compact daily summaries.

External agent transcripts are not claim history. The journal contains coordination identifiers, normalized scopes, modes, outcomes, conflicts, worktree identifiers, and relevant commit identifiers. It does not contain prompts, reasoning, responses, arbitrary tool output, or task descriptions.

Resolve the primary worktree from Git worktree metadata, even when the operation runs from a linked checkout. The canonical linked-checkout root is the .worktrees directory immediately beneath that primary worktree. Never derive it from the current linked worktree, never create it below another linked checkout, and never embed its machine-specific absolute path in portable project guidance.

## Claim Scope

Use one scope form for each intended ownership kind:

- file names one exact intended file. A future file that does not exist yet is valid.
- tree names one directory subtree and overlaps its descendants.
- project-files names every project file except backlog and ignored operational worktree state.
- backlog names the complete repository-root backlog subtree.
- all-files names the explicit union of project-files and backlog.
- resource names one exclusive repository-global runtime or integration resource.

Tree, project-files, and all-files scope require a short coordination-only scope reason. Do not put prompts, sensitive company information, or personal information in the reason.

Select at most one broad file domain. Exact files and trees are classified into project-files or backlog ownership. A request that mixes project and backlog paths is rejected atomically with INVALID_SCOPE and mixed_file_domains. Explicit backlog paths remain compatible and produce the compat_backlog_path warning so status, journal events, and diagnostics make the normalization visible. Resources may accompany any one selected file domain.

An existing directory is not a valid exact-file scope, and an existing file is not a valid tree scope. Repository roots and wildcard exact-file scopes are invalid. A temporary compatibility mode may convert existing directories supplied as files into warned tree scopes, but still requires a scope reason. New callers use the explicit forms.

The repository-root backlog directory and all-files ownership are primary-worktree-only. An isolated claim extension into backlog returns SHARED_CHECKOUT_REQUIRED because the operation must be handed to the primary worktree. Non-overlapping primary-worktree claims may coexist.

Every claim and scope result records file_domain as project_files, backlog, all_files, or none and records the matching broad booleans. Explicit resource-only claims own no file domain and ignore unrelated worktree or index dirtiness. Legacy claims without a trustworthy file-domain baseline retain complete-worktree clean-release compatibility.

Status normalizes active claims written by an earlier registry schema for display without silently rewriting the registry. A legacy claim with paths in both domains is reported as legacy_mixed, cannot extend into another file scope, and retains complete-worktree release rules. A claim that lacks a trustworthy out-of-domain baseline also retains complete-worktree release rules.

The claim id also names the canonical isolated checkout directory. It must be one portable path component containing only letters, digits, dots, underscores, or hyphens. Invalid identifiers return INVALID_IDENTIFIER before any worktree is created.

## When To Claim

Use the Event Contract as the only trigger list. Read-only inspection and worktree-local activity need no claim.

## Coordination Outcomes

The structured outcome is authoritative. Result schema version 2 uses the canonical vocabulary and includes legacy_outcome only when a canonical name replaces a schema version 1 name.

| Canonical outcome | Meaning | Required next action | Legacy outcome |
|---|---|---|---|
| SHARED_CHECKOUT_ACQUIRED | Ownership was acquired in the repository's existing shared checkout. | Work only within the acquired scope there. | PRIMARY |
| ISOLATED_CHECKOUT_ACQUIRED | Ownership was acquired in a newly prepared isolated checkout. | Work only within the acquired scope in the returned checkout. | ISOLATE |
| DIRTY_CHECKOUT_RECOVERY_ACQUIRED | Recovery ownership was acquired over explicitly authorized dirty state. | Preserve the state in a checkpoint commit before cleanup. | RECOVER |
| CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED | No ownership was acquired because requested scope overlaps another owner. | Wait for a handoff or choose genuinely non-overlapping scope. | WAIT |
| SHARED_CHECKOUT_REQUIRED | No ownership was acquired because the operation must run from the shared checkout. | Hand the operation to that checkout and reconcile status there. | PRIMARY_REQUIRED |
| SHARED_CHECKOUT_RELEASE_REQUIRED | No ownership was acquired because another claim currently owns the shared checkout. | Wait for its release notification before retrying there. | PRIMARY_REQUIRED |
| ISOLATED_CHECKOUT_SETUP_REQUIRED | No ownership was acquired because an isolated branch and checkout must be prepared. | Repeat the acquisition with the required isolation arguments. | ISOLATE_REQUIRED |
| DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED | No ownership was acquired because dirty state requires explicit recovery authority. | Obtain authority before repeating with recovery enabled. | RECOVERY_REQUIRED |

Structured rejections such as INVALID_SCOPE, INVALID_IDENTIFIER, INVALID_WORKTREE_PATH, WORKTREE_ROOT_NOT_IGNORED, CLAIM_NOT_FOUND, and RELEASE_REJECTED are valid coordination results. Do not reinterpret an ownership state or rejection as an implementation-interface failure.

Schema version 1 journal events remain append-only and retain the original outcome strings. New PRIMARY_REQUIRED events include shared_checkout_claimed so reporting can distinguish the two canonical states. Historical PRIMARY_REQUIRED events without that field remain raw PRIMARY_REQUIRED and appear in outcome_normalization_gaps because active claim counts do not prove shared-checkout ownership.

## Acquisition Workflow

Acquisition uses an exclusive registry lock. Its result includes the claim mode, branch, and target worktree.

### Shared Checkout Acquisition

Request only the scope selected by the Event Contract. Acquisition returns SHARED_CHECKOUT_ACQUIRED when no active claim overlaps that scope or names the same resource.

### Isolated Checkout Acquisition

Explicit isolation arguments may create an isolated claimed checkout beneath the primary worktree's .worktrees directory. The target is derived rather than caller-selected, and isolation arguments never bypass overlapping scope.

### Shared-Checkout-Only Backlog Acquisition

Updates and moves of existing work items run from the primary worktree under the exact source and destination paths required by the Event Contract. Non-overlapping backlog item claims may coexist, including alongside project-files.

### Claim Scope Conflict Wait

Overlapping scope returns CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED with the conflicting claim identifiers and exact overlap pairs. Do not edit, create a competing worktree, or add isolation arguments. Wait, coordinate a handoff, or choose genuinely non-overlapping scope.

## Atomic Scope Extension

Stop before touching newly discovered scope. Extend the existing claim while its original ownership remains active. Extension checks only net-new scope against every other active claim under the registry lock. All requested additions succeed together or a wait result leaves the live claim unchanged. Repeating scope already owned succeeds idempotently and separates added scope from already-owned scope.

Extension preserves the original worktree, branch, mode, baseline commit, and claim timestamp. An isolated claim cannot extend into backlog; SHARED_CHECKOUT_REQUIRED leaves the claim unchanged so that work can be handed to the primary worktree. Scope contraction is not supported.

## Heartbeat

Refresh the heartbeat during long work. A heartbeat is coordination liveness evidence, not proof that implementation, review, verification, or integration progressed. It never changes an expected release, hard stop, configured maximum, or cleanup-grace boundary.

## Resource Deadline Policy

Every named resource acquisition is bound to the project-owned resource_coordination.deadline_policy. The required resource classes are backlog-mutation, main-integration, browser-server, database-port, and live-model-evaluation. Each class supplies maximum_duration_seconds and cleanup_grace_seconds. The resource_overrides mapping uses one exact resource id as each key and supplies resource_class, maximum_duration_seconds, and cleanup_grace_seconds; an exact-id override replaces the named class values for that resource.

A claim may protect at most one named timed resource. Acquisition or atomic scope extension supplies that exact resource id and class together with expected_duration_seconds and requested_hard_stop_duration_seconds. The claim helper, not the caller, resolves the configured maximum and cleanup grace from PROJECT.yaml. It accepts only positive durations satisfying expected duration <= requested hard stop <= configured maximum, then records the resource id, class, expected duration, requested hard stop, configured maximum, expected release time, absolute hard-stop time, cleanup grace, cleanup-grace end time, and later extension evidence. Callers must not assert a configured maximum.

The initial methodology defaults are:

| Resource class | Maximum duration | Cleanup grace |
|---|---:|---:|
| backlog-mutation | 600 seconds | 120 seconds |
| main-integration | 2700 seconds | 600 seconds |
| browser-server | 3600 seconds | 600 seconds |
| database-port | 1800 seconds | 300 seconds |
| live-model-evaluation | 14400 seconds | 1800 seconds |

These are editable project policy, not inferred runtime constants. Later measured evidence may justify changing them through Project Configurator.

The Event Contract maps browser-test resources to browser-server, database and port resources to database-port, live-model resources to live-model-evaluation, and shared-install and deployment resources to main-integration. The exact resource-id override remains available when a project needs a different measured maximum or cleanup grace.

An owner may request extend-deadline only with explicit evidence and a larger requested hard-stop duration that remains within the immutable configured maximum recorded at acquisition. The extension is measured from the original acquisition time, updates the absolute hard stop and cleanup-grace end, and appends the evidence to the journal. Heartbeat alone never extends it.

Status is read-only. It reports whether the hard stop is overdue, whether cleanup grace is active or elapsed, and the inputs needed to judge stopped-owner actionability. An overdue entry is never auto-released. Cleanup grace is a bounded interval for truthful resource shutdown and evidence preservation, not authorization to continue normal work after the hard stop. A stopped owner with a live timed-resource entry is immediately actionable; inspect the actual resource and durable evidence, then use an authorized handoff, release, or administrative recovery path without inventing delivery or completion evidence.

## Runtime And Integration Resources

Resource names are stable and descriptive. The complete Event Contract uses:

```text
port:3000
browser-test:primary
database:seed
shared-install:skills
deployment:production
```

Separate linked worktrees have independent indexes, branches, and commits. An isolated writer may commit to its unique branch without a repository-global commit resource.

## Overlap And Isolation

- Exact files overlap only the same exact file.
- Trees overlap descendants and intersecting ancestor or descendant trees.
- Project-files overlaps project files and trees but excludes backlog.
- Backlog overlaps backlog files and trees but excludes project files.
- All-files overlaps every exact file, tree, project-files claim, and backlog claim.
- Identical exclusive resources overlap even when file scope differs.
- Resource-only claims serialize only identical resources and never occupy a file or backlog domain.
- Non-overlapping primary-worktree claims may coexist.
- Different exact backlog items may be claimed concurrently.
- One project-files claim may coexist with exact backlog item claims.
- Overlap waits. Worktree isolation does not make conflicting changes logically safe.
- Never stage, commit, revert, or clean another claim owner's files unless acting as the explicit integration owner.

## Event Journal Safety

Acquire, extension, heartbeat, recovery, wait, and release outcomes append one versioned event under the same Git common directory. Event identifiers are created at operation execution, so replaying or forking an external task transcript cannot duplicate an event. Every successful new acquisition also creates one immutable claim incarnation identifier stored in the live claim and copied to each later event in that claim lifecycle.

The live registry remains authoritative. For a registry-changing operation, the claim helper writes the registry first and then appends one synchronized JSON line while still holding the registry lock. Except for evidence-gated release reconciliation, a journal failure produces a structured journal_write_failed warning without reversing or weakening the live coordination result. Reconciliation requires durable RELEASED evidence across the separate registry and journal files.

Before removing the claim, the claim helper durably records one pending transaction marker. The registry target has exact original and released snapshots; the journal target has exact original, prepared, and released snapshots. The prepared journal appends RELEASE_PENDING and never RELEASED. Every snapshot carries its existence state, digest, and exact bytes. Recovery validates the complete marker schema, immutable relationships, canonical target allowlist, target components, snapshots, and one-event transformations before writing either target. Symbolic links, redirected or duplicate targets, malformed data, unsupported versions, inconsistent snapshots, and target bytes outside the allowed transaction states retain the marker and return RECONCILIATION_RECOVERY_REQUIRED.

Prepared and committed markers have different authority:

1. A prepared marker protects the original claim. Recovery restores the exact original journal first and the exact original registry second, then removes the marker. Pending journal evidence is not a release.
2. A committed marker proves the registry release is authoritative. Recovery restores the exact released registry, finalizes the journal from its exact released snapshot so exactly one RELEASED event exists, then removes the marker.

Each replacement preserves the target mode, handles partial writes, synchronizes its temporary file, renames it, and synchronizes the containing directory. The marker is removed only after durable restoration or committed finalization. If any validation, restoration, finalization, or marker cleanup step fails, the marker remains and blocks scope mutation. No failed prepared transaction leaves a valid RELEASED event.

## Journal Maintenance And Reporting

Keep today and the preceding UTC calendar day hot, and archive every older complete day. Maintenance validates that compressed output exactly matches the hot source before removing it. Reruns are idempotent, and an interruption before validation leaves the hot source intact.

Journal maintenance acquires the registry and recovery gate before the maintenance lock. It recovers a valid marker first or returns RECONCILIATION_RECOVERY_REQUIRED before reading, archiving, summarizing, or removing journal data. Status uses the same registry gate and attempts deterministic recovery. Reporting acquires the registry gate but remains read-only: when a marker exists, it returns RECONCILIATION_RECOVERY_REQUIRED before loading journal events and never recovers, rewrites, archives, finalizes, or removes transaction state.

Contention reports use only the event journal and live registry. They count shared, isolated, and recovery acquisitions; waits and rejected transitions; correlated wait episodes; duration statistics; scope and resource hotspots; broad-scope reasons; open and incomplete claims; stale heartbeat evidence; integration-resource use; and journal coverage gaps. Reporting never parses agent harness transcripts.

When RECONCILIATION_RECOVERY_REQUIRED appears:

1. Invoke status through the same configured claim-helper interface so a valid marker can recover under the registry lock.
2. If the outcome persists, preserve the marker, registry, journal, command result, and relevant filesystem evidence.
3. Escalate the retained evidence for operator diagnosis. Do not manually edit or remove the marker, registry, journal, or protected claim.

## Completion And Release

A modifying task is not complete merely because implementation or tests are complete. A clean finish includes:

- Required verification passed or the blocker is documented.
- Task changes are committed, or the task explicitly produced no changes.
- The claimed worktree is clean.
- Long-running resources are stopped or explicitly handed off.
- The claim is released through the configured adapter.
- A clean released isolated checkout is removed only after its verified commit is preserved on a branch or integrated into the target.
- The final response reports the commit hash, verification, and terminal status.

Release validates operational coordination state, not committed content. It checks current owned-domain cleanliness and compares current out-of-domain worktree and index state with the acquisition baseline. Status inspection uses NUL-delimited records so spaces, quotes, non-ASCII text, newlines, rename records, and text resembling a rename arrow remain exact paths. Unchanged pre-existing out-of-domain dirtiness does not become owned work and does not block release. A changed staged, unstaged, or untracked out-of-domain path returns RELEASE_REJECTED with reason out_of_domain_changes and reports only paths whose current state differs from the baseline. The claim helper records the resulting commit and requires either a commit change or an explicit no-change declaration. Normal release does not traverse commit history, audit committed paths, enforce contribution scope, or interpret merge ancestry. The evidence-gated reconciliation variant performs only the bounded commit and ancestry proof described below. Independent review and integration own committed-content, changed-path, and provenance decisions beyond this bounded proof. The configured claim-helper interface never stages, commits, reverts, or cleans project paths.

Treat release-validation failures as coordination diagnostics, not automatic delivery verdicts. Preserve live ownership and reconcile the durable Git, review, verification, and work-item evidence without inventing a successful release.

An evidence-gated release reconciliation may resolve one retained primary scoped claim after a normal release rejected a peer-owned out-of-domain change. This variant is mutually exclusive with no-change and requires the full peer commit SHA plus the matching prior rejected release event reference. Under the registry lock, it revalidates a clean claimed domain, no resources, a clean current out-of-domain state, and the exact baseline-vs-current out-of-domain changed paths. The peer commit must be strictly after the claim baseline, be an ancestor of current HEAD, change exactly those out-of-domain paths without changing claimed-domain paths, and preserve the acquisition-time content for every reconciled path. Accepted descendant commits may later change those paths, so the current tree does not need to equal the peer snapshot. The referenced event must carry the active claim's immutable incarnation identifier and prove the same baseline, rejected path set, and out-of-domain rejection. For a legacy live claim and rejection without that field, reconciliation follows line order across the ordered daily archive and hot journal files without sorting events by timestamp. Acquisition state continues across daily-file boundaries, and reconciliation succeeds only when the active claim and referenced rejection uniquely resolve to the same acquisition event identifier. Reused event identifiers anywhere in the relevant claim history are ambiguous even when they occur in physically distinct lifecycle segments or use equal, reversed, or otherwise unreliable clocks. Missing, ambiguous, duplicate, malformed, or mismatched legacy evidence rejects the release while retaining the registry claim. A successful reconciliation removes only the named claim after durably recording the resolved incarnation, baseline snapshot and commit, peer commit, peer content evidence, reconciled paths, and prior rejection reference in the RELEASED event. Every failed proof or journal write restores or leaves authoritative ownership evidence and retains normal release rejection behavior. Reconciliation never resets Git, edits project paths, or substitutes for independent review, verification, integration, or work-item completion.

Contention reports count broad events by project_files, backlog, and all_files domain in addition to total broad events and reasons. This keeps ordinary project ownership, serialized backlog transitions, and exceptional repository-wide work distinguishable in historical diagnostics.

### Committed Release

After the claimed worktree is clean and contains the verified task commit, release normally. After the commit is preserved and the claim is released, the orchestration owner removes the isolated checkout from the primary worktree and prunes stale Git worktree metadata. Never remove a dirty, active, uncommitted, or unpreserved checkout.

### No-Change Release

When the task legitimately produced no repository change, first confirm the claimed worktree is clean, then declare no-change explicitly through the configured adapter. No-change is not permission to discard or ignore dirty files. If a safe commit or truthful no-change result cannot be produced, the work remains incomplete and the claim remains active or is handed off explicitly.
