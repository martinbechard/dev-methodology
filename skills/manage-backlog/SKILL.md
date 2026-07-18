---
name: manage-backlog
description: Manage a markdown backlog with typed active work, a separate user-review queue, holding, archives, explicit state, claims, recovery, and completion evidence. Use when inspecting status, choosing unattended work, surfacing user decisions, coordinating lifecycle transitions, or resuming interrupted backlog work.
metadata:
  category: development-practice
---

# Manage Backlog

## Purpose

Manage backlog work as a visible queue with explicit lifecycle state. The active folders are the human-facing source of work, archive folders are the durable outcome record, and hidden state is only supporting evidence for claims, recovery, logs, and results.

## Folder Model

Use these folders when present:

- backlog/defect-backlog for active defects.
- backlog/feature-backlog for active features.
- backlog/analysis-backlog for active analyses.
- backlog/investigation-backlog for active investigations.
- backlog/user-review for visible work whose next safe step requires a user answer.
- backlog/holding for visible work that should not be dispatched.
- backlog/completed-backlog grouped by item type for delivered work.
- backlog/failed-backlog grouped by item type for failed, incomplete, abandoned, or blocked terminal work.

Active typed backlog folders should contain only work that can still be dispatched or that is blocked by an explicit non-user dependency. backlog/user-review is a separate non-dispatchable queue. Completed and failed archives should not be scanned as fresh work.

backlog/holding is for intentionally deferred work that has no immediate user question. backlog/user-review is for an explicit user-owned decision or information boundary. Do not merge their counts or lifecycle rules.

## Series Folders

When an active backlog folder contains a subfolder with an index.md file, treat it as one related item series. The index is the goal-level coordination artifact and should not be claimed or dispatched as a runnable item unless it explicitly says it is the work item.

Use the index to understand purpose, non-goals, data or design anchors, implementation order, and links to child items. Treat the child markdown files in the same subfolder as the runnable backlog items.

When managing a series:

- Keep the index current as the map of the series.
- Prefer child-item status and archive location for execution state.
- Preserve links between index.md and child items.
- Use dependencies between child item slugs when order matters.
- Do not mark the whole series complete until every required child item is completed or intentionally abandoned.
- Derive the series status from child evidence: active while required children remain runnable or running, blocked when every remaining required child is blocked, failed when a required terminal failure prevents the goal, and completed only when all required children have terminal successful or intentionally abandoned outcomes.
- Archive child items according to their own outcomes. Move or mark the index according to project convention only when the series has reached a terminal state.

## State Principles

Use explicit states and do not infer success from silence:

- queued means active and eligible for dispatch.
- claimed means a specific agent or run owns the item.
- running means work is in progress.
- blocked means dependencies or prerequisites are unmet.
- user review means a user-owned decision or information prerequisite is unmet and the item is in backlog/user-review.
- target merge pending means implementation evidence exists but delivery is not complete.
- completed means delivery evidence exists and the item has been archived as completed.
- failed means work ended in a non-success terminal state and has been archived as failed.
- abandoned means the item is intentionally no longer being pursued.

Missing result evidence, missing logs, a stopped process, or absence of errors is never completion.

## Inventory Workflow

When asked about backlog status:

- Scan active folders, user review, holding, completed archives, failed archives, and any runner state folders that exist.
- Classify each markdown item by folder, slug, status header if present, dependencies, series membership, and archive location.
- Treat backlog/user-review/README.md as queue guidance rather than a backlog item.
- Validate that every user-review item records Status: User Review, an underlying work Type, one Question for the User, Why User Input Is Required, a Resolution, and an Unattended Work Boundary.
- Treat user-review items as visible but not dispatchable, even when their underlying Type would otherwise have high priority.
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
- Exclude backlog/user-review from runnable selection and unattended queue counts.
- Do not claim, dispatch, implement, or resolve user-review work before the user answers its recorded question.
- Do not dispatch holding items.
- Do not dispatch items with unmet dependencies.
- Do not create duplicate claims for the same item.
- Keep each claimed item isolated so concurrent work does not share mutable workspace state.

Claims should be durable and exclusive. A claimed item remains readable in its active folder; claiming should not move the item.

## User Review Workflow

When backlog/user-review contains one or more items:

1. Read the item and its current Resolution before asking anything.
2. Ask the user the exact question recorded in the item. Include the stated options and tradeoffs when present.
3. Do not infer approval from silence, prior unrelated decisions, repository access, or the ability to implement a technically plausible option.
4. Record the user's answer under Resolution with the date and the resulting disposition.
5. Move an approved or answered item into its typed active backlog folder only when the answer makes the work actionable, set its active status according to project convention, and preserve the user decision as authority evidence.
6. Move a deferred item to backlog/holding. Archive a rejected or abandoned item under the matching failed-backlog type only when the user clearly ends the work.
7. Keep a partially answered item in backlog/user-review with a narrowed Question for the User. Never claim its implementation scope while a material user decision remains open.

Claim only the files needed to record and move an answered item. Claim implementation scope separately after the item becomes active and dispatchable.

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

- Move successfully delivered defects under backlog/completed-backlog/defects.
- Move successfully delivered features under backlog/completed-backlog/features.
- Move completed analyses under backlog/completed-backlog/analyses.
- Move completed investigations under backlog/completed-backlog/investigations.
- Move failed or incomplete items under the matching backlog/failed-backlog type folder.
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
- A separate user-review count with each exact pending question; never combine it with blocked or holding.
- The next runnable items and why they are runnable.
- Blocked items and the dependency or prerequisite that blocks them.
- Recent completed or failed outcomes with evidence.
- Any stale claims, invalid filenames, unreadable files, or missing result evidence.

Keep the report grounded in current files and state, not prior conversation memory.
