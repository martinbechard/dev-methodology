---
name: manage-backlog
description: Manage a markdown backlog with typed active folders, holding, completed archives, failed archives, explicit item state, dependency blocking, claims, recovery, and completion evidence. Use when the user asks to inspect backlog status, choose runnable work, execute or coordinate backlog items, mark items completed or failed, resume interrupted backlog work, or clean up backlog lifecycle state.
---

# Manage Backlog

## Purpose

Manage backlog work as a visible queue with explicit lifecycle state. The active folders are the human-facing source of work, archive folders are the durable outcome record, and hidden state is only supporting evidence for claims, recovery, logs, and results.

## Folder Model

Use these folders when present:

- docs/defect-backlog for active defects.
- docs/feature-backlog for active features.
- docs/analysis-backlog for active analyses.
- docs/investigation-backlog for active investigations.
- docs/holding for visible work that should not be dispatched.
- docs/completed-backlog grouped by item type for delivered work.
- docs/failed-backlog grouped by item type for failed, incomplete, abandoned, or blocked terminal work.

Active backlog folders should contain only work that can still be dispatched or that is blocked by an explicit dependency. Completed and failed archives should not be scanned as fresh work.

## Series Folders

When an active backlog folder contains a subfolder with an index.md file, treat it as one related item series. The index is the goal-level coordination artifact and should not be claimed or dispatched as a runnable item unless it explicitly says it is the work item.

Use the index to understand purpose, non-goals, data or design anchors, implementation order, and links to child items. Treat the child markdown files in the same subfolder as the runnable backlog items.

When managing a series:

- Keep the index current as the map of the series.
- Prefer child-item status and archive location for execution state.
- Preserve links between index.md and child items.
- Use dependencies between child item slugs when order matters.
- Do not mark the whole series complete until every required child item is completed or intentionally abandoned.
- Archive child items according to their own outcomes. Move or mark the index according to project convention only when the series has reached a terminal state.

## State Principles

Use explicit states and do not infer success from silence:

- queued means active and eligible for dispatch.
- claimed means a specific agent or run owns the item.
- running means work is in progress.
- blocked means dependencies or prerequisites are unmet.
- target merge pending means implementation evidence exists but delivery is not complete.
- completed means delivery evidence exists and the item has been archived as completed.
- failed means work ended in a non-success terminal state and has been archived as failed.
- abandoned means the item is intentionally no longer being pursued.

Missing result evidence, missing logs, a stopped process, or absence of errors is never completion.

## Inventory Workflow

When asked about backlog status:

- Scan active folders, holding, completed archives, failed archives, and any runner state folders that exist.
- Classify each markdown item by folder, slug, status header if present, dependencies, series membership, and archive location.
- Treat holding items as visible but not dispatchable.
- Treat series index files as coordination artifacts unless project guidance makes them runnable.
- Treat completed and failed archive location as durable outcome evidence.
- Report invalid or unreadable items instead of silently skipping them.
- Separate backlog status from unrelated worktree or workspace status.

If a repository keeps closed items in active folders, use explicit status headers as the open or closed signal. If the repository moves closed items to archives, use archive location as the outcome signal.

## Dispatch Workflow

When choosing work:

- Reconcile existing claims and interrupted work before claiming new items.
- Prefer unfinished claimed work over new work.
- Apply folder priority from project guidance. If none exists, prefer defects, then features, then investigations, then analyses.
- Do not dispatch holding items.
- Do not dispatch items with unmet dependencies.
- Do not create duplicate claims for the same item.
- Keep each claimed item isolated so concurrent work does not share mutable workspace state.

Claims should be durable and exclusive. A claimed item remains readable in its active folder; claiming should not move the item.

## Completion Workflow

Only mark an item completed when all of these are true:

- The requested change, answer, or investigation result exists.
- Required verification was run or a clear blocked reason is recorded.
- Delivery evidence is recorded in the item, state, result, or related work artifact.
- Any shared finalization step has completed without conflict.
- The item is moved or marked according to the repository's completed outcome convention.

If the work failed, crashed, was incomplete, hit an unresolved conflict, or lacks result evidence, do not mark it completed. Move or mark it according to the failed outcome convention and preserve enough evidence for repair.

## Archive Rules

Archive movement is explicit and serialized:

- Move successfully delivered defects under docs/completed-backlog/defects.
- Move successfully delivered features under docs/completed-backlog/features.
- Move completed analyses under docs/completed-backlog/analyses.
- Move completed investigations under docs/completed-backlog/investigations.
- Move failed or incomplete items under the matching docs/failed-backlog type folder.
- Preserve claims, logs, result summaries, and failure reasons until the user no longer needs recovery evidence.

When the backlog and implementation live in the same repository, avoid mixing unrelated changes into archive commits or status updates. Archive movement should correspond to the item outcome being recorded.

## Recovery Workflow

When resuming interrupted backlog work:

- Read visible active items first.
- Reconcile claims, running state, result records, logs, and archive locations.
- Detect stale running state and classify it as resumable, blocked, crashed, or failed based on evidence.
- Resume recoverable claimed items before claiming new work.
- Keep failed delivery evidence available for diagnosis.
- Ask for human direction only when the next safe action cannot be inferred from state and evidence.

## Reporting

Report backlog state in operator terms:

- Counts by queued, claimed, running, blocked, completed, failed, holding, and invalid.
- The next runnable items and why they are runnable.
- Blocked items and the dependency or prerequisite that blocks them.
- Recent completed or failed outcomes with evidence.
- Any stale claims, invalid filenames, unreadable files, or missing result evidence.

Keep the report grounded in current files and state, not prior conversation memory.
