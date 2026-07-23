---
name: manage-file-work-items
description: Manage authoritative repository-backed work items through inventory, dispatch, lifecycle, recovery, completion, failure, and archival with short primary-main backlog claims. Use when the effective provider is file or the user explicitly requests management of file-backed items.
metadata:
  category: development-practice
---

# Manage File Work Items

## Purpose

Manage file-provider work as a visible queue with explicit lifecycle state. Active folders are the human-facing source of work, archive folders are the durable outcome record, and hidden state is only supporting evidence for claims, recovery, logs, and results.

## Provider Selection

- Apply this skill only when the effective provider is file or applicable project guidance permits an explicit request to select file for the named items.
- When durable provider management is required and the provider is UNSET, ask the user before mutation.
- When the effective provider is none or another provider, return the provider mismatch without changing backlog or falling back to file storage.
- Do not create, update, close, reopen, label, or mirror GitHub, GitLab, Azure DevOps, or Jira records.

## File Authority And Claims

The only authoritative file-provider storage root is backlog in the primary worktree while that worktree is on main. The repository-relative active or archive path is work_item_id and provider_reference. Archive movement changes the terminal provider_reference to the destination path.

An isolated worktree, another linked worktree, or a primary worktree not on main may inspect available evidence but must not create, transition, or archive the canonical record. Return BLOCKED with the observed worktree and branch, required primary-main authority, exact requested transition, and next handoff. Never create a shadow queue.

Serialize each queue mutation with a short agent-claim backlog scope from the primary main worktree. SHARED_CHECKOUT_RELEASE_REQUIRED is a coordination outcome rather than a failed mutation. Arrange a direct handoff or completion notification and suspend without polling. SHARED_CHECKOUT_REQUIRED means the operation must be handed to the primary main worktree. Resume only after that notification or handoff, reconcile live status, then retry the exact transition.

Use one short backlog claim to record Status: Running and ownership evidence, commit that transition, and release immediately. Delivery then uses a separate exact, tree, or project-files claim without backlog ownership. After delivery, review, verification, and integration complete, acquire a later backlog claim to record result evidence and archive the item, then commit and release it.

## Folder Model

Use these folders when present:

- backlog/defect-backlog for active defects.
- backlog/feature-backlog for active features.
- backlog/analysis-backlog for active analyses.
- backlog/investigation-backlog for active investigations.
- backlog/user-action-required for visible work whose next safe step requires a user answer.
- backlog/holding for visible work that should not be dispatched.
- backlog/completed-backlog grouped by type for delivered work.
- backlog/failed-backlog grouped by type for failed, incomplete, abandoned, or blocked terminal work.

Active typed folders contain only dispatchable work or work blocked by an explicit non-user dependency. User Action Required and Holding are separate non-dispatchable queues. Completed and failed archives are durable history, not fresh work.

backlog/holding is for intentionally deferred work without an immediate user question.

## Series Folders

When an active folder contains a subfolder with index.md, treat it as one related item series. The index is a goal-level coordination artifact, not a runnable item unless it explicitly says otherwise. Child Markdown files in the same subfolder are the runnable items.

- Keep the index current as the series map.
- Preserve links between the index and every child.
- Use child provider references for dependencies and execution state.
- Archive each child according to its outcome.
- Derive the series as active while required children remain runnable or running, blocked when every remaining required child is blocked, failed when a required terminal failure prevents the goal, and completed only when all required children have terminal successful or intentionally abandoned outcomes.

## Lifecycle States

Use explicit provider lifecycle states and never infer success from silence:

- READY: authorized, complete enough to dispatch, and without unmet prerequisites.
- RUNNING: one owner and execution identity have accepted the item.
- BLOCKED: a technical, dependency, capability, claim, or provider prerequisite prevents safe progress.
- USER_ACTION_REQUIRED: a genuine user decision, authority grant, value judgment, or user-held fact is required.
- HOLDING: the work is intentionally deferred without an immediate user question.
- AWAITING_REVIEW: verified feature-branch publication exists but review, checks, configured merge, or main observation is incomplete.
- COMPLETED: the selected completion contract is satisfied and the file provider terminal update succeeds.
- FAILED: delivery ended without satisfying completion and terminal failure evidence is recorded.
- ABANDONED: authorized direction ends the work without delivery.

READY as a completion disposition is not lifecycle READY. A file item remains in its current nonterminal lifecycle until manage-file-work-items records an authorized transition. Once AWAITING_REVIEW is recorded for a feature-branch delivery, the same delivery identity remains lifecycle AWAITING_REVIEW through review corrections and merge preparation. A provider terminal-update failure after delivery disposition READY preserves the accepted delivery evidence but leaves the current nonterminal lifecycle unchanged or records BLOCKED until reconciliation applies the pending update.

Missing result evidence, missing logs, a stopped process, a commit, branch publication, or absence of errors is never completion.

## Inventory Workflow

When asked for status:

- Scan active folders, User Action Required, Holding, completed archives, failed archives, and applicable runner state.
- Classify each Markdown item by canonical path, slug, status, type, provider, dependencies, series, owner, phase, and archive location.
- Treat backlog/user-action-required/README.md and series index.md files as guidance or coordination artifacts unless explicitly runnable.
- Validate required user-action fields and canonical provider fields.
- Report invalid, unreadable, duplicated, shadow, or provider-mismatched items rather than silently skipping them.
- Separate backlog status from unrelated workspace status.
- Report Status: Proposed as invalid migration debt.

If closed items remain in active folders, explicit status is the open or closed signal. If the repository moves closed items to archives, archive location is durable outcome evidence.

## Dispatch Workflow

- Reconcile existing claims and interrupted work before claiming new items.
- Prefer unfinished claimed work over new work.
- Apply configured priority; otherwise prefer defects, features, investigations, then analyses.
- Exclude User Action Required and Holding from runnable selection and unattended counts.
- Do not dispatch items with unmet dependencies or duplicate ownership.
- Keep each dispatched item isolated so concurrent work does not share mutable workspace state.
- Keep delivery ownership isolated from backlog mutation ownership.
- Do not claim, dispatch, implement, or resolve user-action-required work before the user answers its recorded question.

Do not move an independently identified idea into a typed active folder until the user explicitly authorizes it. A direct request or explicit authorization creates Status: Ready unless the user defers it or a separate genuine user-owned question remains. Ordinary dependencies stay with typed active work.

## Transition Evidence

Record durable evidence appropriate to every transition:

- READY: source evidence, requirements, acceptance criteria, dependencies, verification expectations, provider_reference, and completion selection.
- RUNNING: owner, canonical task id when applicable, branch or worktree, phase, started-at evidence, and backlog claim reference.
- BLOCKED: exact blocker, owner of the next action, blocking references, recovery note, and permitted resumption transition.
- USER_ACTION_REQUIRED: one exact question, why input is required, prohibited unattended action, and recorded resolution when answered.
- HOLDING: deferral authority and resumption condition.
- AWAITING_REVIEW: branch, accepted candidate commit, provider-accurate pull-request or merge-request delivery reference, publication evidence, completed local checks, and pending review or merge requirement.
- COMPLETED: accepted delivery commit, independent review, checks, merge evidence when applicable, main observation, released delivery and integration claims, terminal backlog claim and commit, completed-at evidence, and the completed archive path.
- FAILED: failure evidence, preserved source and recovery context, checks attempted, terminal claim and commit, and failed archive path.
- ABANDONED: abandonment authority, preserved context, terminal claim and commit, and failed archive path.

Keep wait_started_at, attempt_count, last_attempt, next_attempt, open issues, and accepted_candidate_commit when bounded retry or interrupted recovery needs them.

## Blocked Handoff And Resumption

A blocked handoff ends the prior ownership transaction. While that transaction still owns the backlog mutation, set Status to Blocked, replace the prior owner with Owner: Unowned, replace the prior claim with Claim: None, and retain the exact blocker, unblock condition, accumulated evidence, and acceptance criteria. Commit those durable item fields before releasing the prior claim, then release it promptly. Do not report the handoff complete until both the committed item and claim registry are unowned. Neither the BLOCKED state nor satisfaction of the unblock condition authorizes execution or a direct transition to RUNNING.

Resume blocked work through one serialized backlog transaction:

1. Read and retain the complete pre-attempt Blocked item bytes.
2. Reconcile the blocker and confirm that the recorded unblock condition is satisfied.
3. Set the item to Ready without removing or rewriting its blocker, unblock condition, evidence, or acceptance criteria.
4. Acquire a new exclusive claim for the resuming agent.
5. Only after a successful claim, record the new claim and owner, then set Status to Running and commit the transaction.

If no claim is attempted, no successful claim result exists, or acquisition returns CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED, a structured rejection, or another non-success outcome, do not infer ownership. Restore the byte-for-byte pre-attempt Blocked item, leave it unowned and not Running, and preserve all prior blocker, unblock, evidence, and acceptance data. Release any partially acquired ownership truthfully before reporting the unchanged Blocked outcome.

## User Action Required Workflow

1. Read the item and current Resolution.
2. Ask the user the exact question recorded in the item and include stated options and tradeoffs.
3. Do not infer approval from silence, unrelated decisions, repository access, or technical plausibility.
4. Record the dated answer and resulting disposition.
5. Move an approved or answered item into its typed active backlog folder and set Status: Ready before any separately requested claim or running transition.
6. Move a deferred item to backlog/holding. Archive a clearly rejected or abandoned item under the matching failed type.
7. Keep a partially answered item in User Action Required with a narrowed question.

Claim only the backlog files needed for the answer and move. Claim implementation scope separately after the item becomes active and dispatchable.

## Completion And Archive Workflow

Only record COMPLETED when all of these exist:

- The requested delivery or result exists.
- Required verification and independent review succeeded or an explicitly accepted omission is recorded.
- The configured completion process returned disposition READY.
- The accepted delivery commit is observed on main.
- Delivery and integration claims are released.
- Provider terminal evidence is ready to commit under a new short backlog claim.

For feature-branch completion, publication alone records AWAITING_REVIEW. During same-delivery review corrections, the same delivery identity remains lifecycle AWAITING_REVIEW. Do not change lifecycle back to RUNNING for same-delivery corrections. Only a later Commit READY permits the distinct terminal COMPLETED update. That terminal update also requires the accepted review, checks, merge, and main-observation evidence.

Archive movement is explicit and serialized:

- Delivered defects go under backlog/completed-backlog/defects.
- Delivered features go under backlog/completed-backlog/features.
- Completed analyses go under backlog/completed-backlog/analyses.
- Completed investigations go under backlog/completed-backlog/investigations.
- Failed, incomplete, blocked-terminal, or abandoned items go under the matching backlog/failed-backlog type folder.

Record the destination as the terminal provider_reference. Preserve claims, review, checks, source evidence, delivery evidence, recovery notes, and failure reasons. A conflict, missing proof, or terminal-update failure prohibits lifecycle COMPLETED.

## Recovery Workflow

- Read visible active items first.
- Reconcile owner, canonical task, claims, branch, worktree, accepted candidate commit, logs, results, checks, delivery references, waits, and archive locations.
- Classify stale running state as resumable, blocked, crashed, failed, or already delivered but pending provider update from concrete evidence.
- Resume recoverable claimed work before selecting new work.
- Apply the Blocked Handoff And Resumption workflow when the item is Blocked; state alone never supplies ownership.
- Preserve failed or partial delivery evidence for diagnosis.
- Do not rerun accepted delivery solely because a terminal provider update failed unless the evidence is stale or contradictory.
- Ask for human direction only when state and evidence cannot determine the next safe action.

## Reporting

Return provider file; canonical active or archive path; counts by lifecycle state; separate User Action Required questions; next runnable items; dependencies and blockers; owner and canonical task; delivery, review, check, main-observation, and archive evidence; claim and commit references; invalid or duplicate records; and the next safe action.

Keep the report grounded in current files and state, not prior conversation memory.

## Migration

Callers migrated file-provider inventory, lifecycle, recovery, completion, failure, and archival behavior to manage-file-work-items, and the legacy shells were removed. Historical mapping: manage-backlog and file-based-backlog management behavior moved into this skill; PROJECT.yaml and generated guidance now select Persistence file and reference manage-file-work-items for management.
