---
name: manage-file-work-items
description: Manage authoritative repository-backed work items through inventory, dispatch, lifecycle, recovery, completion, failure, and archival with project-selected resource coordination. Use when the effective provider is file or the user explicitly requests management of file-backed items; agent-claim uses short primary-main backlog claims, while none uses no claim lifecycle or evidence.
metadata:
  category: development-practice
---

# Manage File Work Items

## Purpose

Manage file-provider work as a visible queue with explicit lifecycle state. Active folders are the human-facing source of work, archive folders are the durable outcome record, and hidden state is only supporting evidence for enabled resource coordination, recovery, logs, and results.

## Provider Selection

- Apply this skill only when the effective provider is file or applicable project guidance permits an explicit request to select file for the named items.
- When durable provider management is required and the provider is UNSET, ask the user before mutation.
- When the effective provider is none or another provider, return the provider mismatch without changing backlog or falling back to file storage.
- Do not create, update, close, reopen, label, or mirror GitHub, GitLab, Azure DevOps, or Jira records.

## File Authority And Resource Coordination

The only authoritative file-provider storage root is backlog in the primary worktree while that worktree is on main. The repository-relative active or archive path is work_item_id and provider_reference. Archive movement changes the terminal provider_reference to the destination path.

An isolated worktree, another linked worktree, or a primary worktree not on main may inspect available evidence but must not create, transition, or archive the canonical record. Return BLOCKED with the observed worktree and branch, required primary-main authority, exact requested transition, and next handoff. Never create a shadow queue.

Apply the project-wide resource_coordination selection independently from this provider. When agent-claim is selected, serialize each queue mutation with a short backlog scope from the primary main worktree. SHARED_CHECKOUT_RELEASE_REQUIRED is a coordination outcome rather than a failed mutation. Arrange a direct handoff or completion notification and suspend without polling. SHARED_CHECKOUT_REQUIRED means the operation must be handed to the primary main worktree. Resume only after that notification or handoff, reconcile live status, then retry the exact transition. When none is selected, perform no claim discovery, acquisition, heartbeat, registry mutation, handoff, or release and require no claim-specific evidence anywhere in this skill.

When coordination is enabled, use one short backlog ownership transaction for each startup transition. The parent Dev Backlog Coordinator owns the dispatch decision and has a Dev Backlog Steward child commit Ready -> Starting with reservation evidence, then releases immediately. After the work-item Thread's root Dev Orchestrator accepts ownership, that root uses its own Dev Backlog Steward child to commit Starting -> Running with the canonical Thread identifier, canonical task id, branch, worktree, and claim evidence, then releases immediately. Delivery obtains separate implementation ownership without backlog scope. After delivery, review, verification, and integration complete, the work-item Orchestrator uses its Steward child for the atomic terminal provider transaction that records result evidence, sets Completed, moves the archive, commits, and releases. With coordination none, preserve the same separate commits and provider transitions without coordination transactions or evidence.

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
- STARTING: a parent Coordinator has durably reserved capacity and dispatched exactly one work-item Thread, but its root Orchestrator has not yet accepted delivery ownership.
- RUNNING: one owner and execution identity have accepted the item.
- BLOCKED: a technical, dependency, capability, resource-coordination, or provider prerequisite prevents safe progress.
- USER_ACTION_REQUIRED: a genuine user decision, authority grant, value judgment, or user-held fact is required.
- HOLDING: the work is intentionally deferred without an immediate user question.
- AWAITING_REVIEW: verified feature-branch publication exists but review, checks, configured merge, or main observation is incomplete.
- COMPLETED: the selected completion contract is satisfied and the file provider terminal update succeeds.
- FAILED: delivery ended without satisfying completion and terminal failure evidence is recorded.
- ABANDONED: authorized direction ends the work without delivery.

READY as a completion disposition is not lifecycle READY. Starting and Running remain active typed work items in their existing type folder; neither moves to a holding or terminal queue. A RUNNING item remains RUNNING until manage-file-work-items records terminal evidence and lifecycle COMPLETED. A provider terminal-update failure after delivery disposition READY preserves the accepted delivery evidence but leaves lifecycle RUNNING or BLOCKED until reconciliation applies the pending update.

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

- Reconcile enabled coordination ownership and interrupted work before assigning new items.
- Prefer unfinished owned work over new work.
- Apply configured priority; otherwise prefer defects, features, investigations, then analyses.
- Exclude User Action Required and Holding from runnable selection and unattended counts.
- Do not dispatch items with unmet dependencies or duplicate ownership.
- Ready -> Starting is the parent Dev Backlog Coordinator's dispatch and capacity-reservation decision. Its Steward child records the parent coordination Thread, one launch reservation, normalized objective, dispatch time, and available launch evidence atomically before the runtime Thread is created.
- Starting counts against capacity exactly like Running, so ambiguous or slow startup cannot cause over-dispatch.
- Before creating a work-item Thread, reconcile the item, parent Thread, runtime task inventory, reservation evidence, and any canonical task id. The Coordinator must not create a duplicate after an ambiguous startup or timeout.
- Starting -> Running is owned by the root Dev Orchestrator after it accepts the item. Its Dev Backlog Steward child atomically records the canonical work-item Thread identifier, canonical task id, root Dev Orchestrator, branch, worktree, and claim evidence.
- If startup fails or remains ambiguous, reconcile twice across the bounded settlement interval. When no root Orchestrator accepted ownership and no matching Thread exists, restore Ready and clear only the failed reservation fields. When ownership was accepted or evidence is inconsistent, preserve it and record Blocked or User Action Required with the exact recovery owner instead of restoring Ready.
- Keep each dispatched item isolated so concurrent work does not share mutable workspace state.
- Keep delivery ownership isolated from backlog mutation ownership.
- Do not own, dispatch, implement, or resolve user-action-required work before the user answers its recorded question.

Do not move an independently identified idea into a typed active folder until the user explicitly authorizes it. A direct request or explicit authorization creates Status: Ready unless the user defers it or a separate genuine user-owned question remains. Ordinary dependencies stay with typed active work.

## Transition Evidence

Record durable evidence appropriate to every transition:

- READY: source evidence, requirements, acceptance criteria, dependencies, verification expectations, provider_reference, and completion selection.
- STARTING: parent coordination Thread, dispatch reservation, normalized objective, dispatch time, intended root Dev Orchestrator Role, and any observed runtime creation response.
- RUNNING: owner, canonical task id when applicable, branch or worktree, phase, started-at evidence, and enabled coordination reference.
- BLOCKED: exact blocker, owner of the next action, blocking references, recovery note, and permitted resumption transition.
- USER_ACTION_REQUIRED: one exact question, why input is required, prohibited unattended action, and recorded resolution when answered.
- HOLDING: deferral authority and resumption condition.
- AWAITING_REVIEW: branch, accepted candidate commit, provider-accurate pull-request or merge-request delivery reference, publication evidence, completed local checks, and pending review or merge requirement.
- COMPLETED: accepted delivery commit, independent review, checks, merge evidence when applicable, main observation, enabled coordination releases, terminal backlog commit, completed-at evidence, and the completed archive path.
- FAILED: failure evidence, preserved source and recovery context, checks attempted, enabled coordination disposition, terminal commit, and failed archive path.
- ABANDONED: abandonment authority, preserved context, enabled coordination disposition, terminal commit, and failed archive path.

Keep wait_started_at, attempt_count, last_attempt, next_attempt, open issues, and accepted_candidate_commit when bounded retry or interrupted recovery needs them.

## Blocked Handoff And Resumption

A blocked handoff ends the prior ownership transaction. Set Status to Blocked, replace the prior owner with Owner: Unowned, clear any enabled coordination reference, and retain the exact blocker, unblock condition, accumulated evidence, and acceptance criteria. Commit those durable item fields before releasing enabled ownership, then release it promptly. Do not report the handoff complete until the committed item and any enabled coordination registry are unowned. Neither the BLOCKED state nor satisfaction of the unblock condition authorizes execution or a direct transition to RUNNING.

Resume blocked work through the same provider and startup boundaries as new work:

1. Read and retain the complete pre-attempt Blocked item bytes.
2. Reconcile the blocker and confirm that the recorded unblock condition is satisfied.
3. In one short provider transaction, restore Status: Ready with Owner: Unowned while retaining the blocker, unblock condition, evidence, and acceptance criteria as recovery history. When coordination is enabled, use only short backlog ownership for this transaction and release it immediately. If this transaction fails, restore the byte-for-byte pre-attempt Blocked item and do not infer execution ownership.
4. Let the parent Dev Backlog Coordinator select the Ready item through normal priority and Starting-plus-Running capacity rules. Its Dev Backlog Steward child atomically records Ready -> Starting reservation and dispatch evidence; this transaction does not grant delivery ownership.
5. Reconcile the Starting reservation against active and archived runtime Threads. Create at most one canonical work-item Thread. After an error, timeout, disconnect, or ambiguous response, do not retry creation; perform the bounded settlement read and either adopt the one matching Thread, restore Ready when no root Agent accepted ownership and no Thread exists, or record Blocked or User Action Required when ownership or evidence cannot safely be discarded.
6. Only after the work-item Thread's root Dev Orchestrator Agent accepts ownership may that Orchestrator use its own Dev Backlog Steward child for the atomic Starting -> Running transaction. Record the canonical Thread identifier, canonical root Agent Task id when applicable, owner, branch, worktree, and enabled coordination evidence.

Blocked, Ready, or satisfaction of an unblock condition never authorizes a direct transition to Running. Under enabled coordination, each provider mutation uses its own short backlog ownership transaction and cannot substitute for delivery ownership. With coordination none, preserve the same provider transactions and state sequence without coordination operations or evidence.

## User Action Required Workflow

1. Read the item and current Resolution.
2. Ask the user the exact question recorded in the item and include stated options and tradeoffs.
3. Do not infer approval from silence, unrelated decisions, repository access, or technical plausibility.
4. Record the dated answer and resulting disposition.
5. Move an approved or answered item into its typed active backlog folder and set Status: Ready before any separately requested resource-coordination or running transition.
6. Move a deferred item to backlog/holding. Archive a clearly rejected or abandoned item under the matching failed type.
7. Keep a partially answered item in User Action Required with a narrowed question.

When resource coordination is enabled, acquire only the backlog scope needed for the answer and move. Acquire implementation scope separately after the item becomes active and dispatchable. With coordination none, perform the same provider transactions without operational ownership evidence.

## Completion And Archive Workflow

Only the work-item Thread's root Dev Orchestrator may request terminal completion, and only its Dev Backlog Steward child performs the atomic status-and-archive mutation. Only record COMPLETED when all of these exist:

- The requested delivery or result exists.
- Required verification and independent review succeeded or an explicitly accepted omission is recorded.
- The configured completion process returned disposition READY.
- The accepted delivery commit is observed on main.
- Enabled delivery and integration ownership is released.
- Provider terminal evidence is ready to commit under a new short backlog transaction.

For feature-branch completion, publication alone records AWAITING_REVIEW. Only required review, checks, merge, and main observation permit COMPLETED. A correctable review finding returns the same item and branch to RUNNING.

Archive movement is explicit and serialized:

- Delivered defects go under backlog/completed-backlog/defects.
- Delivered features go under backlog/completed-backlog/features.
- Completed analyses go under backlog/completed-backlog/analyses.
- Completed investigations go under backlog/completed-backlog/investigations.
- Failed, incomplete, blocked-terminal, or abandoned items go under the matching backlog/failed-backlog type folder.

Record the destination as the terminal provider_reference. Preserve enabled coordination, review, checks, source evidence, delivery evidence, recovery notes, and failure reasons. A conflict, missing proof, or terminal-update failure prohibits lifecycle COMPLETED.

## Recovery Workflow

- Read visible active items first.
- Reconcile owner, parent and work-item Thread identifiers, canonical task, Starting reservation, enabled coordination, branch, worktree, accepted candidate commit, logs, results, checks, delivery references, waits, and archive locations.
- For a Starting item, adopt one matching Thread when evidence proves it exists; restore Ready only when no ownership was accepted; otherwise preserve ownership evidence and use Blocked or User Action Required. Never create a replacement until duplicate reconciliation proves there is no accepted canonical Thread.
- Classify stale running state as resumable, blocked, crashed, failed, or already delivered but pending provider update from concrete evidence.
- Resume recoverable owned work before selecting new work.
- Apply the Blocked Handoff And Resumption workflow when the item is Blocked; state alone never supplies ownership.
- Preserve failed or partial delivery evidence for diagnosis.
- Do not rerun accepted delivery solely because a terminal provider update failed unless the evidence is stale or contradictory.
- Ask for human direction only when state and evidence cannot determine the next safe action.

## Reporting

Return provider file; canonical active or archive path; counts by lifecycle state; separate User Action Required questions; next runnable items; dependencies and blockers; owner and canonical task; delivery, review, check, main-observation, and archive evidence; enabled coordination and commit references; invalid or duplicate records; and the next safe action.

Keep the report grounded in current files and state, not prior conversation memory.

## Migration

manage-file-work-items owns all file-provider inventory, lifecycle, recovery, completion, failure, and archival behavior formerly split between manage-backlog and file-based-backlog. Update PROJECT.yaml and generated guidance to select provider file and load manage-file-work-items for management. The legacy identifiers are migration-only shells until their separately governed callers move; they must not receive new procedure changes.
