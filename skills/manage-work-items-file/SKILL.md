---
name: manage-work-items-file
description: Manage authoritative repository-backed work items through inventory, dispatch, lifecycle, recovery, completion, failure, and archival. Use when the effective provider is file or the user explicitly requests management of file-backed items.
metadata:
  category: development-practice
---
<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: 639b4b55-8ebe-4261-a949-70e9f680d49b
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

# Manage File Work Items

The Work-item content is the Work-item authority and is stored according to the Persistence provider's specific format.

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

## File Authority

Only the primary worktree on main may change canonical files under backlog. The file provider resolves an opaque Work Item ID to its current active or archive path. Moving the backing file does not change the Work Item ID.

Acquire the exact opaque Work Item ID before any work or provider mutation. Use activity work for outcome work and activity update for provider mutation. Release the work-item claim with disposition done, blocked, or handoff at the activity boundary. Blocked may include a bounded blocker reference; when present, it must be canonical, non-empty, single-line, and at most 200 characters. A handoff release must complete before the next owner acquires the same ID. Path and resource claims remain independently applicable. The lifecycle state in the Work-item content remains authoritative.

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
- backlog/completed-backlog grouped by type for delivered work.
- backlog/failed-backlog grouped by type for failed, incomplete, abandoned, or blocked terminal work.

Active typed folders contain dispatchable work, non-dispatchable unknown-cause Stalled
work, or work Blocked by an explicit non-user dependency. User Action Required and Holding
are separate non-dispatchable work queues.
Completed and failed archives are durable history, not fresh work. backlog/holding is for
intentionally deferred recognized work without an immediate user question.

## Future Ideas Exclusion

Future Ideas are not work items or lifecycle states. Do not scan, validate, count, report,
dispatch, own, transition, reconcile, or archive backlog/future-ideas through ordinary lifecycle
management. Route only an explicit Future Ideas, ideation, or promotion request to
manage-future-ideas. Do not load that skill as an unconditional lifecycle dependency.

## Series Folders

When an active folder contains a subfolder with index.md, treat it as one related item series. The index is a goal-level coordination artifact, not a runnable item unless it explicitly says otherwise. Child Markdown files in the same subfolder are the runnable items.

- Keep the index current as the series map.
- Preserve links between the index and every child.
- Use child Work Item IDs for dependencies and execution state.
- Archive each child according to its outcome.
- Derive the series as active while any required child remains Ready, Starting, Running, or
  Awaiting Review; stalled when every required nonterminal child is Stalled; blocked when
  every remaining required child is Blocked; failed when a required terminal failure prevents
  the goal; and completed only when all required children have terminal successful or
  intentionally abandoned outcomes. For a mixed set of nonterminal Stalled, Blocked, User
  Action Required, or Holding children, report the exact child-state inventory instead of
  collapsing it to one series state.

### Stored And Effective Child State

Treat Status as stored lifecycle. To derive a dependent child's current scheduling and
reporting view, apply Ordered Series Dependency State from coordinate-work-items. This file
provider resolves the index-defined required predecessor IDs and supplies their current stored
lifecycle and canonical locations. It does not redefine the resolver.

Inventory records stored lifecycle, effective state, and causal Work Item ID when effective
Blocked is derived. A derived Holding or Blocked result is a read-only normalized view. Do not
mutate a downstream record to persist derived Holding or Blocked. Recovery updates only the
child with the genuine preventing condition, then inventory recalculates every affected view.

Reject a new active cross-folder Work Item edge and require same-series migration before
dispatch. An archived terminal-successful predecessor remains resolvable through its stable
Work Item ID and canonical series-index link; retaining that historical edge does not authorize
a new cross-folder dependency.

The caller owns schedulability and capacity decisions. This manager must not calculate active
capacity or count a derived downstream Blocked result as another stored Blocked item.

### Terminal Series Archive

Keep a series index in its active typed backlog while any required child is nonterminal. This
includes an active, stalled, blocked, User Action Required, Holding, or mixed nonterminal
child-state inventory. Do not add an independent Status field to the series index; derive the
series outcome from its required children and use the index location as terminal evidence.

After the last required child reaches a terminal outcome, archive the coordination index:

- A completed series moves to
  backlog/completed-backlog/TYPE/SERIES-SLUG/index.md. Completed required children and
  intentionally abandoned children may contribute to this outcome only when no required
  terminal failure prevents the series goal.
- A failed or abandoned series moves to
  backlog/failed-backlog/TYPE/SERIES-SLUG/index.md. Use this destination when a required
  Failed or Abandoned child prevents the series goal or authorized direction abandons the
  series itself.
- TYPE is the matching plural archive group: defects, features, analyses, or investigations.
  Preserve the stable series slug and index.md filename at the destination.

Keep the last child transition and the series archive as two serialized provider transactions.
Complete and commit the child's existing status-and-archive transaction first. Then re-read
every required child from its canonical provider reference and derive the series outcome. This
preserves child-level terminal evidence and prevents a series move from changing or replacing a
child outcome.

For the series transaction:

1. Preserve the source index bytes, every affected child backlink, and confirmed destination
   absence as recovery evidence.
2. Before mutation, claim the exact active index path, archive destination, and every child
   path whose explicit Series reference will change. Stop on a conflict or existing destination.
3. Move index.md to the terminal destination while preserving the stable series slug. Rewrite
   its child links to each child's canonical archive path, and update every explicit child Series
   reference to the index's canonical archive path.
4. Commit the index move and backlink updates together, without changing any child's terminal
   status, outcome, or evidence. Confirm every index link and explicit child backlink resolves,
   and confirm no index-only series folder remains under the active typed backlog.

If the series transaction fails after a child transaction succeeds, leave the child archives and
their provider outcomes intact. Restore the preserved series bytes when safe, retain explicit
recovery evidence, and retry the series transaction from the preserved terminal child evidence.
Do not move a nonterminal or mixed-state series merely to remove an active coordination folder.

## Lifecycle States

Use explicit Work-item lifecycle states and never infer success from silence:

- READY: authorized and complete enough for its own work, without a genuine preventing
  condition on that child. Required predecessor state is derived separately.
- STARTING: the Coordinator durably reserved the item and requested one root task launch.
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
lifecycle until manage-work-items-file records an authorized transition. Once AWAITING_REVIEW
is recorded for a feature-branch delivery, the same delivery identity remains lifecycle
AWAITING_REVIEW through review corrections and merge preparation. A provider terminal-update
failure after delivery disposition READY preserves the accepted delivery evidence but leaves
the current nonterminal lifecycle unchanged or records BLOCKED until reconciliation applies
the pending update.

Missing result evidence, missing logs, a stopped process, a commit, branch publication, or absence of errors is never completion.

## Inventory Work Items

When asked for status:

- Scan active folders, User Action Required, Holding, completed archives, failed archives, and applicable runner state.
- Classify each Markdown item by opaque Work Item ID, current diagnostic path, status, type, provider, dependency Work Item IDs, series, owner, phase, and archive location.
- For each series child, report stored lifecycle separately from derived effective state and
  include the causal Work Item ID for effective Blocked.
- Treat backlog/user-action-required/README.md and series index.md files as guidance or coordination artifacts unless explicitly runnable.
- Validate required user-action fields, Work Item ID uniqueness, and provider fields.
- Report invalid, unreadable, duplicated, shadow, or provider-mismatched items rather than silently skipping them.
- Separate backlog status from unrelated workspace status.
- Report Status: Proposed as invalid migration debt.
- Report Stalled inventory separately from Running and Blocked, including the diagnostic
  owner and next investigation action.
- Apply Future Ideas Exclusion without reading backlog/future-ideas.

If closed items remain in active folders, explicit status is the open or closed signal. If the repository moves closed items to archives, archive location is durable outcome evidence.

## Transition Work Item

- Read the exact current item and verify that its current state permits the requested
  caller-authorized transition.
- Require the caller's lifecycle decision, transition evidence, owner, next action, and
  opaque Work Item ID. Resolve that ID across active and archive folders before mutation.
  Reject a request that asks this file manager to infer runtime state,
  active eligibility, capacity, or a conversation disposition.
- Before any transition that would write Status: Ready, confirm that no genuine condition on
  that child prevents its own work. Resolve each required Work Item predecessor by immutable ID
  only to validate the same-series index contract and calculate the normalized effective view.
  A nonterminal required predecessor does not change stored Ready. Reject a new cross-folder
  Work Item edge and require same-series migration instead of storing Blocked downstream.
- For Ready -> Starting, record the caller-supplied parent coordination identity,
  reservation, normalized objective, dispatch time, and Starting handoff evidence atomically.
- For Starting -> Running, record the caller-supplied canonical conversation identity,
  canonical Task identity when applicable, root owner, branch, worktree, started-at
  evidence, and accepted execution evidence atomically.
- A failed or missing task launch, or a task that cannot claim this provider path, leaves the
  item Starting until the Coordinator authorizes a recovery transition. Do not infer or
  automatically record Starting -> Ready from elapsed time or a missing receipt.
- For User Action Required -> Ready and every other authorized nonterminal transition,
  preserve prior evidence, record the decision provenance and next action, and mutate only
  the provider fields and path required by that transition.
- Never combine two lifecycle transitions into one provider mutation. A successful
  Ready -> Starting write does not imply Starting -> Running, and a successful provider
  mutation does not prove a runtime action or conversation-title update.
- Keep delivery ownership isolated from provider mutation ownership.
- Do not own, dispatch, implement, or resolve user-action-required work before the user
  answers its recorded question.

Do not move an independently identified defect or enhancement into a typed active folder
until the user explicitly authorizes that new work. A confirmed independently discovered defect
without implementation authorization must receive one durable file-provider work item under
backlog/user-action-required. An ephemeral report or residual gap does not satisfy this
requirement. Use create-work-item-file to create the record; manage-work-items-file persists only
caller-authorized lifecycle transitions. The user and Dev Backlog Coordinator supply lifecycle
decisions within their respective authority. The user supplies the approval answer. Dev Backlog
Coordinator authorizes each provider transition. Neither record creation nor lifecycle
persistence grants implementation authority.

A direct request or explicit authorization permits active work. Store Blocked only when an
external or other genuine condition on that child prevents work. A required Work Item
predecessor leaves stored lifecycle unchanged; do not require every required predecessor to be
terminal before storing Ready. After creation, move an already authorized item to User Action
Required only when execution reaches a distinct concrete user-owned question that the original
request did not resolve.

## Transition Evidence

Record durable evidence appropriate to every transition:

- READY: source evidence, requirements, acceptance criteria, dependency Work Item IDs, verification expectations, Work Item ID, and completion selection.
- STARTING: caller-supplied parent coordination identity, dispatch reservation, normalized objective, dispatch time, intended root Dev Orchestrator Role, launch result, last contact, and next reconciliation time.
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

Only Dev Backlog Coordinator decides that current evidence justifies Stalled. The Coordinator
directly applies this skill for the atomic provider mutation. The Dev Backlog Watchdog may
report the evidence but cannot request or perform the transition independently.

Set Status to Stalled. Preserve the canonical conversation, root Agent Task, branch, worktree,
commits, current Owner, and coordination evidence as recovery context. Record the complete
STALLED transition evidence above. The caller owns any capacity reconciliation.

The Coordinator chooses one deterministic disposition and applies this skill for the
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
Coordinator decides and directly records Stalled -> Running through this skill.
Do not jump from Stalled to Running for a new owner, after ownership ended, or without
demonstrated resumed progress.

## Blocked Handoff And Resumption

Dev Backlog Coordinator is the lifecycle decision owner for Blocked and directly applies this
skill for the atomic provider mutation after validating a known preventing cause and owning
the next coordination or recovery action. Set Status to Blocked and Owner to Unowned.
Retain the blocker, blocker owner, unblock condition, requested Coordinator
action, evidence, and acceptance criteria. Commit those fields. Do not use Blocked merely
because an item is quiet, slow, or suspected to be stalled.

Resume blocked work through the same provider and startup boundaries as new work:

1. Read and retain the complete pre-attempt Blocked item bytes.
2. Require the Coordinator's bounded diagnosis and recovery receipt. It names the confirmed
   blocker, exact work-item or other authorized supporting-file corrections, preserved
   candidate and gate evidence, remaining risk, and restart decision. Correct stale,
   contradictory, over-scoped, or incomplete provider content before resumption.
3. Reconcile the blocker and confirm that the recorded unblock condition is satisfied.
4. Confirm that the blocked child's own unblock condition is satisfied. Resolve its required
   Work Item predecessors for the normalized effective view, but do not require them to be
   terminal before restoring the child's stored Ready state.
5. In one short provider transaction, restore Status: Ready with Owner: Unowned while retaining
   the blocker, unblock condition, evidence, and acceptance criteria as recovery history. If
   this transaction fails, restore the byte-for-byte pre-attempt Blocked item and do not infer
   execution ownership.
6. When the parent Dev Backlog Coordinator authorizes Ready -> Starting, claim the exact
   provider path, atomically record and commit its supplied reservation and dispatch
   evidence, then release the claim. This provider transaction does not grant execution
   ownership.
7. If the preserved canonical task fails to start or cannot claim the provider, leave the item Starting.
   Record a recovery transition only after the Coordinator supplies its Watchdog-informed
   decision. Do not inspect runtime conversations or choose that disposition here.
8. When the root Dev Orchestrator authorizes Starting -> Running for the preserved canonical task, claim the exact provider
   path, atomically record and commit its
   supplied canonical conversation identifier, root Agent Task id when applicable, owner,
   branch, worktree, and accepted execution evidence, then release the claim.

Blocked, Ready, or satisfaction of an unblock condition never authorizes a direct transition to Running. Provider mutation protection cannot substitute for delivery ownership.

Move Blocked to User Action Required only when investigation identifies one concrete
decision, authority grant, action, risk acceptance, or user-held fact that belongs to the
user. Coordinator inability alone does not create a user obligation. Keep an unresolved
technical or external blocker in Blocked with an exact owner and unblock condition.

## User Action Required Workflow

1. Read the item and current Resolution.
2. If the Resolution already answers the question, do not ask it again. Route the recorded answer through normal resumption.
3. Confirm that the Coordinator selected User Action Required and that the selected Persistence manager stores that state before presenting the request to the user.
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
11. Move an approved or answered item into its typed active backlog folder and set Status: Ready before any Running transition. For an approved confirmed defect, move the same record to backlog/defect-backlog with Status: Ready. Preserve Ready -> Starting -> Running before implementation.
12. When the parent Coordinator authorizes resumption, record Ready -> Starting for the
    existing canonical conversation. When its root Dev Orchestrator separately authorizes
    accepted execution, record Starting -> Running for that same conversation before further
    repository mutation or delivery.
13. Move a deferred item to backlog/holding. For a deferred confirmed defect, use backlog/holding with Status: Holding. For a rejected or abandoned confirmed defect, use backlog/failed-backlog/defects with Status: Abandoned.
14. Keep a partially answered item in User Action Required with a narrowed question.

Work performed before User Action Required -> Ready -> Starting -> Running reconciliation is not automatically accepted or discarded. Preserve its diff, commits, branch, worktree, review, verification, and delivery evidence. Report the sequence problem to the parent. Do not continue delivery until the parent and the same root Orchestrator reconcile the provider state, commits, independent gates, and delivery state.

## Reconcile Work Item Completion

Only the work-item conversation's root Dev Orchestrator may perform terminal completion. It directly applies this skill for the atomic status-and-archive mutation after Commit returns READY. Only record COMPLETED when all of these exist:

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

Preserve the same Work Item ID at the terminal destination and report that destination only as provider-owned diagnostic location evidence. Preserve review, checks, source evidence, delivery evidence, recovery notes, and failure reasons. A conflict, missing proof, or terminal-update failure prohibits lifecycle COMPLETED.

## Recover Work Item

- Read visible active items first.
- Reconcile the Work-item content's owner, parent and work-item conversation identifiers,
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

## Report Work Items

For each considered work item, report stored canonical lifecycle and derived effective state as
distinct fields. Include the causal Work Item ID for effective Blocked, any genuine condition on
the item, any coordination-only overlap constraint, and any deferred edit, shared-resource, or
integration event. Derived state is a normalized read-only view, not a second copy of the Work-item content.

Return provider file, each opaque Work Item ID with its current diagnostic active or archive path, lifecycle counts, separate Stalled inventory with diagnostic owners and next investigation actions, User Action Required questions, next runnable items, dependency Work Item IDs, blockers, owner, canonical task, delivery evidence, review and check results, main observation, archive evidence, commit references, invalid or duplicate records, and the next safe action.

Keep the report grounded in current files and state, not prior conversation memory.

## Migration

Callers migrated file-provider inventory, lifecycle, recovery, completion, failure, and archival behavior to manage-work-items-file, and the legacy shells were removed. Historical mapping: manage-backlog and file-based-backlog management behavior moved into this skill; PROJECT.yaml and generated guidance now select Persistence file and reference manage-work-items-file for management.
