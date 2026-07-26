---
name: manage-file-work-items
description: Manage authoritative repository-backed work items through inventory, dispatch, lifecycle, recovery, completion, failure, and archival. Use when the effective provider is file or the user explicitly requests management of file-backed items.
metadata:
  category: development-practice
---

# Manage File Work Items

## Purpose

Manage file-provider work as a visible queue with explicit lifecycle state. Active folders contain current work. Archive folders contain durable outcomes. Claim records, recovery data, logs, and results are supporting evidence, not work items.

## Provider Selection

- Apply this skill only when the effective provider is file or applicable project guidance permits an explicit request to select file for the named items.
- When durable provider management is required and the provider is UNSET, ask the user before mutation.
- When the effective provider is none or another provider, return the provider mismatch without changing backlog or falling back to file storage.
- Do not create, update, close, reopen, label, or mirror GitHub, GitLab, Azure DevOps, or Jira records.
- Durable Future Ideas are file-provider-only. With another provider selected, return BLOCKED without capturing, listing, validating, or promoting an idea unless the user explicitly selects file as the one-item provider override for that idea. Never represent a Future Idea as a provider issue or shadow file.

## File Authority

Only the primary worktree on main may change canonical files under backlog. The repository-relative active or archive path is work_item_id and provider_reference. After archival, the destination path becomes the provider_reference.

Another worktree may inspect backlog but must not create, transition, or archive an item. If the primary worktree is not on main, it must not change the item. Return BLOCKED with the observed worktree, branch, requested transition, and required handoff. Never create another queue elsewhere.

Follow the Claim Events table in agent-claim when changing a provider record.

Each startup or terminal transition remains its own short primary-main provider transaction. Before finish or handoff, commit completed work and prove the applicable worktree clean.

## Folder Model

Use these folders when present:

- backlog/defect-backlog for active defects.
- backlog/feature-backlog for active features.
- backlog/analysis-backlog for active analyses.
- backlog/investigation-backlog for active investigations.
- backlog/user-action-required for visible work whose next safe step requires a user answer.
- backlog/holding for visible work that should not be dispatched.
- backlog/future-ideas for lightweight thoughts that are not yet actionable, approved, scheduled, or recognized as work.
- backlog/completed-backlog grouped by type for delivered work.
- backlog/failed-backlog grouped by type for failed, incomplete, abandoned, or blocked terminal work.

Active typed folders contain only dispatchable work or work blocked by an explicit non-user dependency. User Action Required and Holding are separate non-dispatchable work queues. Future Ideas is not a work queue or lifecycle state. Completed and failed archives are durable history, not fresh work.

backlog/holding is for intentionally deferred work without an immediate user question. It contains already-recognized work; backlog/future-ideas contains possibilities that have not become recognized work.

## Series Folders

When an active folder contains a subfolder with index.md, treat it as one related item series. The index is a goal-level coordination artifact, not a runnable item unless it explicitly says otherwise. Child Markdown files in the same subfolder are the runnable items.

- Keep the index current as the series map.
- Preserve links between the index and every child.
- Use child provider references for dependencies and execution state.
- Archive each child according to its outcome.
- Derive the series as active while any required child remains Ready, Starting, Running, or
  Awaiting Review; stalled when every required nonterminal child is Stalled; blocked when
  every remaining required child is Blocked; failed when a required terminal failure prevents
  the goal; and completed only when all required children have terminal successful or
  intentionally abandoned outcomes. For a mixed set of nonterminal Stalled, Blocked, User
  Action Required, or Holding children, report the exact child-state inventory instead of
  collapsing it to one series state.

## Lifecycle States

Use explicit provider lifecycle states and never infer success from silence:

- READY: authorized, complete enough to dispatch, and without unmet prerequisites.
- STARTING: a parent Coordinator has durably reserved capacity and dispatched exactly one work-item Thread, but its root Orchestrator has not yet accepted delivery ownership.
- RUNNING: one owner and execution identity have accepted the item.
- STALLED: current evidence indicates that the item is not making progress while the causal blocker or unblock condition remains unknown.
- BLOCKED: a known preventing cause awaits Dev Backlog Coordinator-owned coordination, recovery, or disposition.
- USER_ACTION_REQUIRED: a genuine user decision, authority grant, value judgment, or user-held fact is required.
- HOLDING: the work is intentionally deferred without an immediate user question.
- AWAITING_REVIEW: verified feature-branch publication exists but review, checks, configured merge, or main observation is incomplete.
- COMPLETED: the selected completion contract is satisfied and the file provider terminal update succeeds.
- FAILED: delivery ended without satisfying completion and terminal failure evidence is recorded.
- ABANDONED: authorized direction ends the work without delivery.

READY as a completion disposition is not lifecycle READY. Starting, Running, unknown-cause
Stalled, and known-cause Blocked remain active typed work items in their existing type folder;
none moves to a holding or terminal queue solely because of that state. A file item remains in its current nonterminal
lifecycle until manage-file-work-items records an authorized transition. Once AWAITING_REVIEW
is recorded for a feature-branch delivery, the same delivery identity remains lifecycle
AWAITING_REVIEW through review corrections and merge preparation. A provider terminal-update
failure after delivery disposition READY preserves the accepted delivery evidence but leaves
the current nonterminal lifecycle unchanged or records BLOCKED until reconciliation applies
the pending update.

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
- Report Stalled inventory separately from Running and Blocked, including the diagnostic
  owner and next investigation action.
- Do not scan, validate, count, or report backlog/future-ideas unless the request explicitly opts into Future Ideas, ideation, or promotion.

If closed items remain in active folders, explicit status is the open or closed signal. If the repository moves closed items to archives, archive location is durable outcome evidence.

## Dispatch Workflow

- Reconcile interrupted work before assigning new items; private-worktree changes remain with their work item and are resumed there.
- Prefer unfinished owned work over new work.
- Apply configured priority; otherwise prefer defects, features, investigations, then analyses.
- Exclude Stalled, Blocked, User Action Required, Holding, and Future Ideas from runnable
  selection. Exclude Stalled from Starting-plus-Running active capacity while diagnosis
  proceeds.
- Do not dispatch items with unmet dependencies or duplicate ownership.
- Ready -> Starting is the parent Dev Backlog Coordinator's dispatch and capacity-reservation decision. Its Steward child records the parent coordination Thread, one launch reservation, normalized objective, dispatch time, and available launch evidence atomically before the runtime Thread is created.
- Starting counts against capacity exactly like Running, so ambiguous or slow startup cannot cause over-dispatch.
- Before creating a work-item Thread, reconcile the item, parent Thread, runtime task inventory, reservation evidence, and any canonical task id. The Coordinator must not create a duplicate after an ambiguous startup or timeout.
- When a previously Running item entered User Action Required from an existing canonical work-item Thread, preserve and adopt that same Thread after the answer is recorded and the item is reserved as Starting. Do not require the user to repeat the answer in the parent Thread and do not create a replacement Thread.
- Starting -> Running is owned by the root Dev Orchestrator after it accepts the item. Its Dev Backlog Steward child atomically records the canonical work-item Thread identifier, canonical task id, root Dev Orchestrator, branch, worktree, and applicable claim evidence.
- If startup fails or remains ambiguous, reconcile twice across the bounded settlement interval. When no root Orchestrator accepted ownership and no matching Thread exists, restore Ready and clear only the failed reservation fields. When ownership was accepted or evidence is inconsistent, preserve it and record Blocked or User Action Required with the exact recovery owner instead of restoring Ready.
- Keep each dispatched item isolated so concurrent work does not share mutable workspace state.
- Keep delivery ownership isolated from backlog mutation ownership.
- Do not own, dispatch, implement, or resolve user-action-required work before the user answers its recorded question.

Do not move an independently identified defect, enhancement, or idea into a typed active folder until the user explicitly authorizes that new work or deliberately authorizes Future Idea promotion. A direct request or explicit authorization to perform work creates Status: Ready even when implementation may later encounter a separate user-owned decision. A request only to capture an idea does not authorize promotion. Only after execution reaches a distinct concrete user-owned question that the original request did not resolve may the same item move from Ready to User Action Required. Ordinary dependencies stay with typed active work.

## Future Ideas Workflow

- Read backlog/future-ideas only for an explicit listing, ideation, validation, or promotion operation after confirming the file provider applies to that idea.
- Validate only a title, Synopsis, and Origin or Rationale. Notes and a free-text Revisit Trigger are optional. Do not require ordinary work-item fields or lifecycle evidence.
- Treat only resolved regular files contained by the canonical backlog/future-ideas root as idea records. Reject symlinked or otherwise resolved paths that escape that authority without reading the external bytes.
- Report ideas separately from Ready, Starting, Running, Blocked, User Action Required, Holding, terminal, runnable, and unattended counts.
- Never acquire implementation ownership for an idea or apply a lifecycle transition to it.
- For deliberate promotion, create a complete typed work item in an active, Holding, or User Action Required destination. Require Completion to be exactly direct-main, feature-branch, or UNSET. Holding accepts either the underlying dispatchable Type or Type: Holding; User Action Required retains the underlying dispatchable Type.
- Treat only a resolved regular work-item file contained by its canonical backlog queue as a promotion target. Reject a symlinked or otherwise resolved target that escapes authority without reading external bytes.
- Include the exact retained idea path in the promoted work item's Source Evidence section, and add Promoted To with the canonical work-item reference to the original idea.
- Preserve the original idea in place after promotion. Do not archive or delete it merely because typed work now exists.
- Update the idea and promoted item in one primary-main transaction after duplicate detection succeeds. Follow the Claim Events table in agent-claim for the retained idea update. Create the destination with an exclusive create operation and stop if it already exists. Preserve enough file and index state to verify the commit or restore the attempt.

## Transition Evidence

Record durable evidence appropriate to every transition:

- READY: source evidence, requirements, acceptance criteria, dependencies, verification expectations, provider_reference, and completion selection.
- STARTING: parent coordination Thread, dispatch reservation, normalized objective, dispatch time, intended root Dev Orchestrator Role, and any observed runtime creation response.
- RUNNING: owner, canonical task id when applicable, branch or worktree, phase, started-at evidence, and applicable claim evidence.
- STALLED: last known productive evidence, phase estimate and hard stop when present,
  anomaly or progress gap, canonical Thread and root Agent Task identities, current ownership
  and coordination state, diagnostic owner, and next investigation action.
- BLOCKED: exact known blocker, Coordinator-owned next action, blocker owner, unblock
  condition, blocking references, recovery note, and permitted resumption transition.
- USER_ACTION_REQUIRED: one exact question, why input is required, prohibited unattended action, and recorded resolution when answered.
- HOLDING: deferral authority and resumption condition.
- AWAITING_REVIEW: branch, accepted candidate commit, provider-accurate pull-request or merge-request delivery reference, publication evidence, completed local checks, and pending review or merge requirement.
- COMPLETED: accepted delivery commit, independent review, checks, merge evidence when applicable, main observation, applicable claim results, terminal backlog commit, completed-at evidence, and the completed archive path.
- FAILED: failure evidence, preserved source and recovery context, checks attempted, relevant claim results, terminal commit, and failed archive path.
- ABANDONED: abandonment authority, preserved context, relevant claim results, terminal commit, and failed archive path.

Keep wait_started_at, attempt_count, last_attempt, next_attempt, open issues, and accepted_candidate_commit when bounded retry or interrupted recovery needs them.

## Stalled Investigation And Disposition

Only Dev Backlog Coordinator decides that current evidence justifies Stalled. Its Dev
Backlog Steward child performs the atomic provider mutation. The Dev Backlog Watchdog may
report the evidence but cannot request or perform the transition independently.

Set Status to Stalled. Preserve the canonical Thread, root Agent Task, branch, worktree,
commits, current Owner, and coordination evidence as recovery context. Record the complete
STALLED transition evidence above. Stalled does not count toward Starting-plus-Running
capacity, so the parent Coordinator obtains fresh inventory and fills the vacancy with
eligible Ready work.

The Coordinator chooses one deterministic disposition and its Steward child performs the
provider mutation:

1. Stalled -> Running only when the same canonical owner demonstrably resumes safely and the
   Starting-plus-Running count is below ten. In the same serialized provider transaction,
   reconcile that current count, reject the transition and preserve Stalled when no slot is
   available, and otherwise record the new productive evidence without exceeding capacity
   while keeping the existing canonical identities.
2. Stalled -> Ready when ownership has ended and normal redispatch is required. Set Owner to
   Unowned, retain the diagnostic history, and require the later Ready -> Starting -> Running
   sequence.
3. Stalled -> Blocked when a concrete cause and Coordinator-owned next action are known.
4. Stalled -> User Action Required when a concrete user-owned action is required. Move the
   item to the user-action-required queue with one exact question and unattended-work boundary.
5. Stalled -> Completed, Failed, or Abandoned only when the applicable terminal evidence
   contract is independently satisfied.

Neither a watchdog observation nor Stalled state alone authorizes a lifecycle mutation.
A retained Stalled owner must not resume repository or provider mutation until Dev Backlog
Coordinator decides Stalled -> Running and Dev Backlog Steward records that transition.
Do not jump from Stalled to Running for a new owner, after ownership ended, or without
demonstrated resumed progress.

## Blocked Handoff And Resumption

Dev Backlog Coordinator is the lifecycle decision owner for Blocked. Dev Backlog Steward
performs the atomic provider mutation after the Coordinator validates a known preventing
cause and owns the next coordination or recovery action. Set Status to Blocked and Owner to Unowned.
Retain the blocker, blocker owner, unblock condition, requested Coordinator
action, evidence, and acceptance criteria. Commit those fields. Do not use Blocked merely
because an item is quiet, slow, or suspected to be stalled.

Resume blocked work through the same provider and startup boundaries as new work:

1. Read and retain the complete pre-attempt Blocked item bytes.
2. Reconcile the blocker and confirm that the recorded unblock condition is satisfied.
3. In one short provider transaction, restore Status: Ready with Owner: Unowned while retaining the blocker, unblock condition, evidence, and acceptance criteria as recovery history. Follow the Claim Events table in agent-claim for this provider update. If this transaction fails, restore the byte-for-byte pre-attempt Blocked item and do not infer execution ownership.
4. Let the parent Dev Backlog Coordinator select the Ready item through normal priority and Starting-plus-Running capacity rules. Its Dev Backlog Steward child atomically records Ready -> Starting reservation and dispatch evidence; this transaction does not grant delivery ownership.
5. Reconcile the Starting reservation against active and archived runtime Threads. Create at most one canonical work-item Thread. After an error, timeout, disconnect, or ambiguous response, do not retry creation; perform the bounded settlement read and either adopt the one matching Thread, restore Ready when no root Agent accepted ownership and no Thread exists, or record Blocked or User Action Required when ownership or evidence cannot safely be discarded.
6. Only after the work-item Thread's root Dev Orchestrator Agent accepts ownership may that Orchestrator use its own Dev Backlog Steward child for the atomic Starting -> Running transaction. Record the canonical Thread identifier, canonical root Agent Task id when applicable, owner, branch, worktree, and applicable claim evidence.

Blocked, Ready, or satisfaction of an unblock condition never authorizes a direct transition to Running. Provider mutation protection cannot substitute for delivery ownership.

Move Blocked to User Action Required only when investigation identifies one concrete
decision, authority grant, action, risk acceptance, or user-held fact that belongs to the
user. Coordinator inability alone does not create a user obligation. Keep an unresolved
technical or external blocker in Blocked with an exact owner and unblock condition.

## User Action Required Workflow

1. Read the item and current Resolution.
2. Ask the user the exact question recorded in the item and include stated options and tradeoffs.
3. Do not infer approval from silence, unrelated decisions, repository access, or technical plausibility.
4. Accept the answer in the canonical work-item Thread that asked the question or in the parent coordination Thread. Record the dated answer, provenance, resulting disposition, and existing canonical Thread identity exactly once.
5. When the answer arrives in the canonical work-item Thread, keep that Thread as the resumption context and send one lifecycle resumption request to the parent Coordinator. Do not require the user to switch Threads or repeat the answer.
6. Move an approved or answered item into its typed active backlog folder and set Status: Ready before any separately requested resource-coordination or running transition.
7. If the item is eligible under current priority and capacity, have the parent Coordinator reserve Ready -> Starting for the existing canonical Thread. After that Thread's root Dev Orchestrator accepts ownership, record Starting -> Running for the same Thread before further repository mutation or delivery.
8. Move a deferred item to backlog/holding. Archive a clearly rejected or abandoned item under the matching failed type.
9. Keep a partially answered item in User Action Required with a narrowed question.

Work performed before User Action Required -> Ready -> Starting -> Running reconciliation is not automatically accepted or discarded. Preserve its diff, commits, branch, worktree, claims, review, verification, and delivery evidence. Report the sequence problem to the parent. Do not continue delivery until the parent and the same root Orchestrator reconcile the provider state, applicable claims, commits, independent gates, and delivery state.

## Completion And Archive Workflow

Only the work-item Thread's root Dev Orchestrator may request terminal completion, and only its Dev Backlog Steward child performs the atomic status-and-archive mutation. Only record COMPLETED when all of these exist:

- The requested delivery or result exists.
- Required verification and independent review succeeded or an explicitly accepted omission is recorded.
- The configured completion process returned disposition READY.
- The accepted delivery commit is observed on main.
- Provider terminal evidence is ready to commit under a new short backlog transaction.

For feature-branch completion, publication alone records AWAITING_REVIEW. During same-delivery review corrections, the same delivery identity remains lifecycle AWAITING_REVIEW. Do not change lifecycle back to RUNNING for same-delivery corrections. Only a later Commit READY permits the distinct terminal COMPLETED update. That terminal update also requires the accepted review, checks, merge, and main-observation evidence.

Archive movement is explicit and serialized:

- Delivered defects go under backlog/completed-backlog/defects.
- Delivered features go under backlog/completed-backlog/features.
- Completed analyses go under backlog/completed-backlog/analyses.
- Completed investigations go under backlog/completed-backlog/investigations.
- Failed, incomplete, blocked-terminal, or abandoned items go under the matching
  backlog/failed-backlog type folder. Stalled is nonterminal and cannot be archived directly;
  first record Failed or Abandoned with the applicable terminal evidence.

Record the destination as the terminal provider_reference. Preserve claim evidence, review, checks, source evidence, delivery evidence, recovery notes, and failure reasons. A conflict, missing proof, or terminal-update failure prohibits lifecycle COMPLETED.

## Recovery Workflow

- Read visible active items first.
- Reconcile owner, parent and work-item Thread identifiers, canonical task, Starting reservation, claims, branch, worktree, accepted candidate commit, logs, results, checks, delivery references, waits, and archive locations.
- For a Starting item, adopt one matching Thread when evidence proves it exists; restore Ready only when no ownership was accepted; otherwise preserve ownership evidence and use Blocked or User Action Required. Never create a replacement until duplicate reconciliation proves there is no accepted canonical Thread.
- Classify stale running state as resumable, Stalled, Blocked, crashed, Failed, or already
  delivered but pending provider update from concrete evidence. Use Stalled only while the
  cause remains unknown and Blocked only after the preventing cause is known.
- Resume recoverable owned work before selecting new work.
- Apply Stalled Investigation And Disposition when the item is Stalled and Blocked Handoff
  And Resumption when the item is Blocked; state alone never supplies ownership.
- Preserve failed or partial delivery evidence for diagnosis.
- Do not rerun accepted delivery solely because a terminal provider update failed unless the evidence is stale or contradictory.
- Ask for human direction only when state and evidence cannot determine the next safe action.

## Reporting

Return the provider file, canonical active or archive path, lifecycle counts, separate
Stalled inventory with diagnostic owners and next investigation actions, User Action
Required questions, next runnable items, dependencies, blockers, owner, canonical task,
delivery evidence, review and check results, main observation, archive evidence, claim and
commit references, invalid or duplicate records, and the next safe action. For an explicit
Future Ideas operation, also return the idea paths, validation findings, revisit triggers,
and promotion links without adding them to work-item counts.

Keep the report grounded in current files and state, not prior conversation memory.

## Migration

Callers migrated file-provider inventory, lifecycle, recovery, completion, failure, and archival behavior to manage-file-work-items, and the legacy shells were removed. Historical mapping: manage-backlog and file-based-backlog management behavior moved into this skill; PROJECT.yaml and generated guidance now select Persistence file and reference manage-file-work-items for management.
