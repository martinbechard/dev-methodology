---
name: manage-file-work-items
description: Manage authoritative repository-backed work items through inventory, dispatch, lifecycle, recovery, completion, failure, and archival. Use when the effective provider is file or the user explicitly requests management of file-backed items.
metadata:
  category: development-practice
---

# Manage File Work Items

## Purpose

Manage file-provider work as a visible queue with explicit lifecycle state. Active folders
contain current work. Archive folders contain durable outcomes. Recovery data, logs, and
results are supporting evidence, not work items.

This skill records only caller-authorized file-provider mutations and their evidence. It
does not determine active-execution eligibility, calculate capacity, inspect runtime or
conversation state, or synchronize conversation titles. The calling coordination contract
supplies those decisions and any runtime evidence; this skill validates and persists only
the requested atomic provider transition.

## Provider Selection

- Apply this skill only when the effective provider is file or applicable project guidance permits an explicit request to select file for the named items.
- When durable provider management is required and the provider is UNSET, ask the user before mutation.
- When the effective provider is none or another provider, return the provider mismatch without changing backlog or falling back to file storage.
- Do not create, update, close, reopen, label, or mirror GitHub, GitLab, Azure DevOps, or Jira records.
- Durable Future Ideas are file-provider-only. With another provider selected, return BLOCKED without capturing, listing, validating, or promoting an idea unless the user explicitly selects file as the one-item provider override for that idea. Never represent a Future Idea as a provider issue or shadow file.

## File Authority

Only the primary worktree on main may change canonical files under backlog. The repository-relative active or archive path is work_item_id and provider_reference. After archival, the destination path becomes the provider_reference.

Another worktree may inspect backlog but must not create, transition, or archive an item. If the primary worktree is not on main, it must not change the item. Return BLOCKED with the observed worktree, branch, requested transition, and required handoff. Never create another queue elsewhere.

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

Active typed folders contain dispatchable work, non-dispatchable unknown-cause Stalled
work, or work Blocked by an explicit non-user dependency. User Action Required and Holding
are separate non-dispatchable work queues.
Future Ideas is not a work queue or lifecycle state. Completed and failed archives are
durable history, not fresh work.

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
- STARTING: the caller authorized and supplied evidence for one nonterminal launch reservation.
- RUNNING: the caller authorized and supplied evidence for accepted execution ownership.
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

- Read the exact current item and verify that its current state permits the requested
  caller-authorized transition.
- Require the caller's lifecycle decision, transition evidence, owner, next action, and
  provider reference. Reject a request that asks this file manager to infer runtime state,
  active eligibility, capacity, or a conversation disposition.
- For Ready -> Starting, record the caller-supplied parent coordination identity,
  reservation, normalized objective, dispatch time, and launch evidence atomically.
- For Starting -> Running, record the caller-supplied canonical conversation identity,
  canonical Task identity when applicable, root owner, branch, worktree, started-at
  evidence, and accepted execution evidence atomically.
- When the caller authorizes settlement without accepted Running ownership, atomically record
  Starting -> Ready. Refuse a request that combines a later Stalled, Blocked, User Action
  Required, or terminal disposition with that mutation; any such caller-authorized
  disposition requires a distinct subsequent provider transaction from Ready.
- For User Action Required -> Ready and every other authorized nonterminal transition,
  preserve prior evidence, record the decision provenance and next action, and mutate only
  the provider fields and path required by that transition.
- Never combine two lifecycle transitions into one provider mutation. A successful
  Ready -> Starting write does not imply Starting -> Running, and a successful provider
  mutation does not prove a runtime action or conversation-title update.
- Keep delivery ownership isolated from provider mutation ownership.
- Do not own, dispatch, implement, or resolve user-action-required work before the user
  answers its recorded question.

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
- Update the idea and promoted item in one primary-main transaction after duplicate detection succeeds. Create the destination with an exclusive create operation and stop if it already exists. Preserve enough file and index state to verify the commit or restore the attempt.

## Transition Evidence

Record durable evidence appropriate to every transition:

- READY: source evidence, requirements, acceptance criteria, dependencies, verification expectations, provider_reference, and completion selection.
- STARTING: caller-supplied parent coordination identity, dispatch reservation, normalized objective, dispatch time, intended root Dev Orchestrator Role, and launch evidence.
- RUNNING: caller-supplied owner, canonical conversation and Task identities when applicable, branch or worktree, phase, started-at evidence, and accepted execution evidence.
- STALLED: last known productive evidence, phase estimate and hard stop when present,
  anomaly or progress gap, canonical conversation and root Agent Task identities, current ownership
  and coordination state, diagnostic owner, and next investigation action.
- BLOCKED: exact known blocker, Coordinator-owned next action, blocker owner, unblock
  condition, blocking references, recovery note, and permitted resumption transition.
- USER_ACTION_REQUIRED: one exact question, why input is required, prohibited unattended action, and recorded resolution when answered.
- HOLDING: deferral authority and resumption condition.
- AWAITING_REVIEW: branch, accepted candidate commit, provider-accurate pull-request or merge-request delivery reference, publication evidence, completed local checks, and pending review or merge requirement.
- COMPLETED: accepted delivery commit, independent review, checks, merge evidence when applicable, main observation, terminal backlog commit, completed-at evidence, and the completed archive path.
- FAILED: failure evidence, preserved source and recovery context, checks attempted, terminal commit, and failed archive path.
- ABANDONED: abandonment authority, preserved context, terminal commit, and failed archive path.

Keep wait_started_at, attempt_count, last_attempt, next_attempt, open issues, and accepted_candidate_commit when bounded retry or interrupted recovery needs them.

For Status Stalled, record the evidence in this stable section:

```markdown
## Stalled Evidence

Last Known Productive Evidence: [exact evidence]
Phase Estimate: [estimate or Not present]
Hard Stop: [hard stop or Not present]
Anomaly or Progress Gap: [source-backed observation]
Canonical Conversation: [canonical conversation identity]
Root Agent Task: [root Agent Task identity]
Current Ownership and Coordination State: [owner and coordination state]
Diagnostic Owner: [diagnostic owner]
Next Investigation Action: [next action]
```

Every label is required and its value must be nonempty. When no phase estimate or hard stop
exists, write Not present rather than omitting the field. Source Evidence remains general
provenance and does not substitute for any Stalled Evidence field. Legacy top-level
Diagnostic Owner and Next Investigation Action values remain report-display compatibility
inputs, but do not satisfy Stalled validation; migrate current Stalled items to the canonical
section.

## Stalled Investigation And Disposition

Only Dev Backlog Coordinator decides that current evidence justifies Stalled. Its Dev
Backlog Steward child performs the atomic provider mutation. The Dev Backlog Watchdog may
report the evidence but cannot request or perform the transition independently.

Set Status to Stalled. Preserve the canonical conversation, root Agent Task, branch, worktree,
commits, current Owner, and coordination evidence as recovery context. Record the complete
STALLED transition evidence above. The caller owns any capacity reconciliation.

The Coordinator chooses one deterministic disposition and its Steward child performs the
provider mutation:

1. Stalled -> Running only when the caller supplies its authorized active-eligibility
   decision, renewed execution evidence, and same canonical owner. Keep the existing
   canonical identities.
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
3. In one short provider transaction, restore Status: Ready with Owner: Unowned while retaining the blocker, unblock condition, evidence, and acceptance criteria as recovery history. If this transaction fails, restore the byte-for-byte pre-attempt Blocked item and do not infer execution ownership.
4. When the parent Dev Backlog Coordinator authorizes Ready -> Starting, atomically record
   its supplied reservation and dispatch evidence. This provider transaction does not grant
   execution ownership.
5. If launch reconciliation does not authorize Running, atomically record Starting -> Ready
   first. Record any separately authorized later disposition only in a distinct provider
   transaction from Ready. Do not inspect runtime conversations or choose that disposition
   here.
6. When the root Dev Orchestrator authorizes Starting -> Running, atomically record its
   supplied canonical conversation identifier, root Agent Task id when applicable, owner,
   branch, worktree, and accepted execution evidence.

Blocked, Ready, or satisfaction of an unblock condition never authorizes a direct transition to Running. Provider mutation protection cannot substitute for delivery ownership.

Move Blocked to User Action Required only when investigation identifies one concrete
decision, authority grant, action, risk acceptance, or user-held fact that belongs to the
user. Coordinator inability alone does not create a user obligation. Keep an unresolved
technical or external blocker in Blocked with an exact owner and unblock condition.

## User Action Required Workflow

1. Read the item and current Resolution.
2. If the Resolution already answers the question, do not ask it again. Route the recorded answer through normal resumption.
3. Confirm that the Coordinator selected User Action Required and that the provider records that state before presenting the request to the user.
4. Ask one plain-language question. Explain why the user owns the answer. Give real options or an illustrative example when they clarify the choice. State the practical consequence of each option.
5. State the unattended-work boundary. Name the work that must stop and any independent work that may safely continue.
6. Put the exact question first. Do not hide it inside background information. Do not invent options, risks, or consequences that current evidence does not support.
7. Do not turn a technical dependency, missing tool, implementation failure, or agent-resolvable question into a user choice.
8. Do not infer approval from silence, unrelated decisions, repository access, or technical plausibility.
9. Accept the answer in the canonical work-item conversation that asked the question or in
   the parent coordination conversation. Record the dated answer, provenance, resulting
   disposition, and existing canonical conversation identity exactly once.
10. When the answer arrives in the canonical work-item conversation, keep that conversation
   as the resumption context and send one lifecycle resumption request to the parent
   Coordinator. Do not require the user to switch conversations or repeat the answer.
11. Move an approved or answered item into its typed active backlog folder and set Status: Ready before any Running transition.
12. When the parent Coordinator authorizes resumption, record Ready -> Starting for the
    existing canonical conversation. When its root Dev Orchestrator separately authorizes
    accepted execution, record Starting -> Running for that same conversation before further
    repository mutation or delivery.
13. Move a deferred item to backlog/holding. Archive a clearly rejected or abandoned item under the matching failed type.
14. Keep a partially answered item in User Action Required with a narrowed question.

Work performed before User Action Required -> Ready -> Starting -> Running reconciliation is not automatically accepted or discarded. Preserve its diff, commits, branch, worktree, review, verification, and delivery evidence. Report the sequence problem to the parent. Do not continue delivery until the parent and the same root Orchestrator reconcile the provider state, commits, independent gates, and delivery state.

## Completion And Archive Workflow

Only the work-item conversation's root Dev Orchestrator may request terminal completion, and only its Dev Backlog Steward child performs the atomic status-and-archive mutation. Only record COMPLETED when all of these exist:

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

Record the destination as the terminal provider_reference. Preserve review, checks, source evidence, delivery evidence, recovery notes, and failure reasons. A conflict, missing proof, or terminal-update failure prohibits lifecycle COMPLETED.

## Recovery Workflow

- Read visible active items first.
- Reconcile the provider record's owner, parent and work-item conversation identifiers,
  canonical Task, reservation, branch, worktree, accepted candidate commit, logs, results,
  checks, delivery references, waits, and archive locations.
- Require the caller to supply the evidence-backed lifecycle decision. This skill must not
  inspect runtime state, infer active execution, choose a capacity result, or derive a
  conversation disposition from a task anomaly.
- Apply the requested authorized transition atomically. Preserve all prior runtime,
  ownership, diagnostic, and delivery evidence needed for later recovery.
- Apply Stalled Investigation And Disposition when the caller authorizes a Stalled
  transition and Blocked Handoff And Resumption when it authorizes a Blocked transition;
  provider state alone never supplies execution ownership.
- Preserve failed or partial delivery evidence for diagnosis.
- Do not rerun accepted delivery solely because a terminal provider update failed unless the evidence is stale or contradictory.
- Ask for human direction only when state and evidence cannot determine the next safe action.

## Reporting

For each considered work item, report dispatch eligibility, any unmet hard blocker, any coordination-only overlap constraint, and any deferred edit, shared-resource, or integration event as distinct facts.

Return the provider file, canonical active or archive path, lifecycle counts, separate Stalled inventory with diagnostic owners and next investigation actions, User Action Required questions, next runnable items, dependencies, blockers, owner, canonical task, delivery evidence, review and check results, main observation, archive evidence, commit references, invalid or duplicate records, and the next safe action. For an explicit Future Ideas operation, also return the idea paths, validation findings, revisit triggers, and promotion links without adding them to work-item counts.

Keep the report grounded in current files and state, not prior conversation memory.

## Migration

Callers migrated file-provider inventory, lifecycle, recovery, completion, failure, and archival behavior to manage-file-work-items, and the legacy shells were removed. Historical mapping: manage-backlog and file-based-backlog management behavior moved into this skill; PROJECT.yaml and generated guidance now select Persistence file and reference manage-file-work-items for management.
