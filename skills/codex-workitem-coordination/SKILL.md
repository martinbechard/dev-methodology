---
name: codex-workitem-coordination
description: Coordinate multiple provider-selected work items through one parent backlog coordinator and one Dev Orchestrator Thread per Starting or Running item. Use when Codex must sustain a queue, deliver reviewed work, close completed items, and recover stalled delivery without a separate task registry.
metadata:
  category: development-practice
---

# Codex Work-Item Coordination

Use one Dev Backlog Coordinator as the parent dispatcher. Reserve each selected work item as Starting, then give its one user-visible work-item Thread to a root Dev Orchestrator Agent that owns candidate production, independent review, verification, effective Commit delivery, Persistence closure, and terminal handoff after Starting -> Running acceptance.

## Authority And Roles

- The effective Persistence-selected provider record is the durable work-item authority when a provider is selected. Provider none has no durable provider record.
- Git records branches, commits, delivery, and cleanup eligibility; it is not a work-item provider.
- PROJECT.yaml may load agent-claim. Its registry records active claims but does not prove review, verification, or delivery.
- Codex Thread state and title are display and execution state, not lifecycle authority.
- Dev Backlog Coordinator owns provider-routed queue inventory, priority, dispatch, Stalled
  and Blocked lifecycle decisions, stalled-delivery investigation, and terminal Thread cleanup.
- Dev Orchestrator owns one work item after its root Agent accepts Starting -> Running through delivery or a truthful terminal outcome. It may assign bounded Tasks to Dev Coder, independent reviewer, and verifier child Agents inside that Thread.
- Dev Backlog Steward applies the effective Persistence-selected management skill for provider inventory and lifecycle mutation. Dev Orchestrator applies the effective Commit-selected skill only after candidate review and verification accept a direct or combined commit.
- Dev Backlog Watchdog owns scheduled read-only observation and actionable alerts. It never
  owns provider lifecycle, dispatch, delivery, recovery, claims, or cleanup.

Do not create a separate parent ledger, baton registry, waiting-Task registry, or Thread database. Do not copy this procedure into AGENTS.md or a Dev Orchestrator definition.

## Resource Coordination

When agent-claim is loaded, use its Claim Events table and supporting rules. Do not define claim behavior in this skill.

## Work-Item Execution Record

For a selected Persistence provider, use its management skill to record these phase-appropriate facts in the provider's supported ownership, open-issues, and evidence fields. For provider none, retain them in the canonical Codex Thread result without creating a shadow record:

- canonical work-item Thread identifier, root Dev Orchestrator Agent, and canonical Task identifier for that root assignment when the runtime supplies one
- branch and worktree
- current phase
- accepted candidate commit
- delivery-wait or provider-closure-wait start time
- applicable claim result, notification, blocking evidence, and owner
- open issues and the owner of each next action
- review, verification, Commit disposition, claim release, provider closure, and cleanup evidence as those events occur
- for Stalled, last productive evidence, phase estimate and hard stop when present, anomaly
  or progress gap, canonical Thread and root Agent Task identities, current ownership and
  coordination state, diagnostic owner, and next investigation action

Use the effective Persistence-selected management skill to update a provider record when a material phase changes. Preserve the same canonical Thread identifier, root Agent assignment, and provider identity through corrections, delivery, and closeout. Never infer identity from the Thread title alone.

## Queue Target And Dispatch

Obtain queue inventory, lifecycle counts, provider identities, and dispatchable state only by applying the effective Persistence-selected management skill.

- Provider file: treat ordinary repository backlog paths as provider identities and use the selected file-provider skill for creation and mutation. Do not scan or count backlog/future-ideas unless the parent explicitly requests ideation or promotion.
- Provider github: use GitHub issue identities and provider lifecycle evidence; do not create or inspect file backlog paths.
- Provider gitlab: use GitLab issue identities and provider lifecycle evidence; do not translate them into GitHub or file records.
- Provider azure-devops or jira: apply the selected placeholder management skill, preserve its BLOCKED zero-mutation result, and do not fall back.
- Provider none: do not inventory, count, create, transition, or close durable provider records; coordinate only the explicit task and retain task-local evidence.
- Provider UNSET or an unavailable selected skill: stop before durable inventory or mutation and request the missing project selection or capability.

For a provider that supports queue inventory and lifecycle transitions:

1. Count work items whose provider lifecycle state is Starting or Running.
2. When the count is below ten, select enough eligible Ready items to fill available capacity without exceeding ten active items.
3. For each selection, have the parent Coordinator's Dev Backlog Steward child atomically record the Ready -> Starting reservation and dispatch evidence through the effective Persistence-selected management skill before creating a runtime Thread.
4. Reconcile the reservation and existing runtime evidence, then create at most one user-visible work-item Thread for the Starting work item. When the item already has one canonical Thread preserved from a prior Running to User Action Required transition, adopt that same Thread instead of creating a replacement.
5. After the Thread's root Dev Orchestrator Agent accepts ownership, have that Orchestrator's Dev Backlog Steward child atomically record Starting -> Running with the canonical Thread identifier, root Agent Task identifier when applicable, branch, worktree, and applicable claim evidence.
6. Dispatch only work that can begin implementation or another bounded delivery phase. Do not create a Thread merely to wait for approval, a dependency, a reviewer, a shared resource, or a delivery window.
7. When an item leaves Starting or Running, fill the active-capacity vacancy promptly through the same Ready -> Starting reservation sequence.

Stalled, Blocked, User Action Required, Holding, Awaiting Review, Completed, Failed,
Abandoned, and Future Ideas do not count toward ten. Stalled does not count toward
Starting-plus-Running capacity while the Coordinator investigates it. Future Ideas are
not work-item states and enter coordination only after deliberate promotion creates a
complete typed work item. If fewer than ten eligible items exist, activate all eligible
items and report the shortage instead of manufacturing placeholder work. Provider none
does not synthesize a queue or a target of ten from Thread state.

List or validate backlog/future-ideas only when the parent request explicitly includes ideation or promotion and file Persistence applies to that operation. A revisit trigger is free text and never schedules a Thread, fills capacity, or authorizes unattended work.

## Dispatch Reconciliation

Treat a Thread-creation error, timeout, disconnect, or ambiguous response as an ambiguous mutation. Do not retry creation.

Reconcile active and archived Threads using all available identity evidence:

- source parent Thread identifier
- canonical provider identity and provider reference when one exists
- normalized objective
- creation time
- Thread status

If exactly one match exists, adopt it as the canonical work-item Thread. If multiple matches exist, preserve one canonical Thread, stop every duplicate before mutation, verify no unique work is lost, and archive the duplicates when supported. If no match is immediately visible, allow one bounded settlement interval and reconcile once more. When the settled read still shows no Thread and no root Agent accepted ownership, ask the parent Coordinator's Steward child to restore Ready and clear only failed reservation fields through the effective Persistence-selected management skill. When ownership was accepted or evidence remains inconsistent, preserve the evidence and record Blocked or User Action Required with the exact recovery owner. Never retry Thread creation after an ambiguous response.

## Thread Execution Compatibility And Titles

Create each Dev Orchestrator work-item Thread in an environment where its root Agent can perform ordinary repository work without asking the user to approve Git, shell, test, process-inspection, or selected resource-coordination commands. The dispatch prompt must state that these ordinary operations are already authorized by the work item and that the Agent must not open or wait on a user approval prompt for them.

- When agent-claim is loaded, use the claim helper configured in PROJECT.yaml.
- Keep implementation and focused tests in the work-item Thread's private worktree. The environment must permit ordinary writes to that worktree and the Git worktree metadata needed for local commits.
- When a work item depends on a special runtime capability, test that capability through the same nested execution path the real workload uses before assigning more equivalent work to that environment. A direct command is not sufficient evidence for a runner that invokes the command from a child process.
- Treat prior runtime-capability evidence as stale after any agent-definition or metadata generation, adapter installation, MCP refresh, Codex configuration change, permission-profile change, application update, or host restart. Before dispatching real work again, run one disposable worktree pilot through the effective child Agent runtime.
- The post-change pilot must prove the effective Agent profile and ordinary operations, not merely read the requested configuration or repeat permission wording in its prompt. Inspect the child Agent's effective approval, sandbox, and permission profile; create a harmless Git commit; invoke every selected special capability through the same nested helper used by the real workload; and, only when agent-claim with MCP is selected, read its registry through MCP.
- If the requested configuration and effective child runtime differ, or any representative operation fails, stop equivalent dispatch immediately. Record the exact requested and effective profiles, archive the failed pilot Thread, correct or replace the launch environment, and rerun the pilot. Do not treat a successful direct command, parent capability, config file, or earlier Thread as evidence for the failing child runtime.
- If an ordinary required operation fails because the Agent environment lacks a capability, the Agent stops immediately, preserves its work, and reports the exact failed operation to the parent. It must not request escalation from the user.
- The parent promptly re-homes the Thread or replaces its root Agent in a compatible environment, asks Dev Backlog Steward to update canonical identifiers through the selected Persistence manager, and fills any resulting Starting-plus-Running vacancy. For provider none it updates only the task-local identity. Do not leave an approval prompt or an execution-incompatible Agent consuming active capacity.

Set a concise plain-text title when the Thread is created and update it only at material phase changes. Use a phase prefix such as Implementing —, Reviewing —, Verifying —, Integrating —, Waiting for Claim —, Waiting for Help —, Waiting for User —, Stalled —, Done —, Blocked —, Failed —, or Abandoned — followed by a short work-item name. Never use raw prompt text, XML or delegation tags, error output, identifiers, or generic titles as the display title. Preserve the stable Thread identifier; the title remains display state and never becomes lifecycle authority or delivery evidence.

## Starting And Work-Item Thread Ownership

A work item is the durable provider record for an outcome, lifecycle, evidence, and ownership. A Thread is one execution context or conversation. An Agent is a runtime instance operating under a Role, which is a reusable responsibility and authority contract. A Task is a bounded assignment to an Agent; it is never a synonym for Thread. A Handoff is a lifecycle event that transfers evidence and the next action.

The parent coordination Thread has one root Agent under the Dev Backlog Coordinator Role. Each Starting or Running work item has exactly one work-item Thread with one root Agent under the Dev Orchestrator Role. Producing, implementation, independent review, verification, delivery, and stewardship Agents are children in that work-item Thread.

Ready -> Starting is the parent Coordinator's dispatch and capacity-reservation decision. Use its Dev Backlog Steward child to record the reservation through the selected manager before launch, and count Starting against capacity exactly like Running. Reconcile existing reservation and runtime evidence before every launch. One work item must not create a duplicate Thread after a timeout, Thread-creation error, or ambiguous startup.

When a Running work item pauses in User Action Required, preserve its canonical work-item Thread, root Agent Task identity, branch, worktree, clean commits, and unresolved question as non-owning resumption evidence. The user may answer and continue the conversation in that canonical Thread. The parent must reuse it after the answer is durably routed through Ready -> Starting; it must not require the user to repeat the answer in the parent Thread or create a replacement work-item Thread.

After the work-item Thread's root Dev Orchestrator Agent accepts ownership, it uses its Dev Backlog Steward child for the atomic Starting -> Running transition. The record includes the canonical Thread identifier, canonical root Agent Task id when applicable, branch, worktree, and applicable claim evidence. If launch fails and no owner accepted, restore Ready. If ownership was accepted or evidence cannot safely be discarded, record Blocked or User Action Required with the exact recovery condition. Starting and Running stay in the provider's active queue.

The work-item Orchestrator owns candidate production, review, verification, Commit delivery, and terminal Persistence request. Its Steward child records the selected provider lifecycle changes. The parent Coordinator never performs per-item delivery or completion; after the terminal Handoff it cleans the runtime Thread and worktree, recounts Starting plus Running capacity, and dispatches replacement work.

## Effective Commit Delivery And Persistence Closure

Dev Orchestrator owns temporal delivery order while the selected Commit and Persistence skills own their respective procedures.

For direct-main integration, start from current main and designate this fresh branch as the Work-item integration and cleanup branch. Integrate only accepted commits or their exact accepted paths. Do not import cumulative branch ancestry merely to preserve provenance; record the source-to-integration mapping instead. Keep Git integration and terminal backlog completion as distinct operations. Cleanup is eligible only after the fresh Work-item integration branch is fully merged. A prior candidate branch used only as a non-ancestral content source is not the Work-item cleanup branch.

1. Require Dev Coder to return a clean verified candidate commit without applying terminal Commit delivery or provider mutation.
2. Obtain fresh independent source review and source verification for every candidate. Return correctable source findings to the original Dev Coder and repeat those gates on the replacement candidate.
3. When multiple accepted candidates must be combined, use Dev Merge Coordinator, then obtain the required fresh post-combination review and complete verification. A single accepted candidate remains the direct commit.
4. Apply or resume the effective Commit-selected skill only after candidate review and source verification accept the direct or combined commit.
5. Preserve AWAITING_REVIEW with the same delivery identity while review, checks, dependency order, correction, merge, or final observation remains pending. A source correction returns through Dev Coder, independent review, and verification before the same Commit delivery resumes.
6. When Commit first returns AWAITING_REVIEW for a selected provider, ask Dev Backlog Steward exactly once to record the nonterminal lifecycle AWAITING_REVIEW through the effective Persistence-selected management skill. Include the delivery identity, publication reference, accepted commit, completed checks, and pending gates. Verify the recorded provider state before reporting AWAITING_REVIEW.
7. On a repeated observation of the same delivery identity and Commit handoff, reconcile the existing update instead of dispatching a duplicate. Never request lifecycle COMPLETED from an AWAITING_REVIEW handoff. Provider none retains the same nonterminal evidence task-locally without a steward dispatch.
8. Resume the same effective Commit-selected skill through review corrections, checks, dependency order, merge, and main observation until it returns READY or BLOCKED.
9. Only after the effective Commit-selected skill returns READY, ask Dev Backlog Steward exactly once for the distinct terminal lifecycle COMPLETED update through the effective Persistence-selected management skill. Verify the selected manager's recorded closure and reconcile an already successful terminal update instead of dispatching a duplicate.
10. Provider file closure uses the file manager's archive procedure. GitHub and GitLab closure use their own provider identities, concurrency behavior, and lifecycle evidence. Placeholder providers preserve BLOCKED without fallback. Provider none records terminal evidence only in the task result and performs no durable provider mutation.
11. Notify the parent with candidate provenance, independent review and verification, final Commit disposition, nonterminal and terminal provider results when selected, claims, branch or delivery identity, worktree, and cleanup eligibility.
12. The parent removes only clean eligible worktrees and branches, updates the task title, archives terminal task UI state when supported, then obtains fresh provider inventory and fills eligible capacity through the selected management skill.

Keep claim release, Commit delivery, and Persistence closure as distinct operations. One cannot substitute for another. Dev Orchestrator applies the selected Commit skill because it owns the accepted commit, review, verification, and resumption context.

If the nonterminal AWAITING_REVIEW update fails or its result is ambiguous, preserve the Commit handoff and reconcile that same Persistence transaction before resuming delivery. Do not request terminal COMPLETED, repeat an already successful nonterminal update, or reinterpret the Commit disposition as terminal.

## Verification

Follow the project's targeted-test policy. Select tests from the changed behavior and its actual dependency paths. Do not add a broad suite merely because several work items were delivered together.

## Long-Running Task Control

When a command or phase is expected to take more than five minutes, the Dev Orchestrator exposes before starting it:

- the exact currently active unit and any later units that have not started
- the expected duration or best evidence-based estimate
- a hard stop condition and the retained evidence path
- the distinct acceptance criterion that requires the expensive operation

This is non-blocking operational telemetry in the task update, not a new provider transaction or parent approval gate. Persist it through the selected Persistence manager at the next already-authorized material phase transition, or retain it task-locally for provider none. The task may start without waiting for parent acknowledgement.

The parent observes long-running work at phase start, first failure, timeout, and completion. This observation must not serialize healthy work. Inspect the actual process, elapsed time, latest evidence-bearing output, and remaining work. Status messages must distinguish one active serial case from selected or queued cases and must not describe queued work as running.

After an expensive failure, classify its failure signature before repeating anything. Reuse retained output, add the smallest offline replay or deterministic regression that reproduces the boundary, and make that focused check pass before another equivalent live or broad run. Run one cheapest representative first. Start a second expensive representative only when it covers a distinct acceptance criterion that retained evidence and deterministic checks cannot prove.

If the active unit reaches its hard stop, repeats the same failure, or stops producing useful evidence, stop that unit. Preserve or commit its work. Stop or hand off its shared resources. Follow agent-claim for any active claim. Two unproductive attempts require parent investigation and a revised plan.

## Stalled Investigation And Blocker Handoff

Stalled is a nonterminal provider lifecycle state for evidence that an item is not making
progress while the causal blocker or unblock condition remains unknown. Quiet or apparently
slow work is not Stalled by itself. A source-backed progress gap, crossed estimate or hard
stop, stopped or missing canonical task, or other observed anomaly must support the
classification.

The Dev Backlog Watchdog reports suspected Stalled evidence but never chooses or mutates
the lifecycle result. Dev Backlog Coordinator decides whether the evidence justifies
Stalled and asks Dev Backlog Steward to perform the atomic provider mutation. Preserve:

- last known productive evidence
- phase estimate and hard stop when present
- the anomaly or evidence-progress gap
- canonical Thread and root Agent Task identities
- current ownership and coordination state
- diagnostic owner
- next investigation action

Stalled leaves Starting-plus-Running capacity immediately after the selected provider
records the transition. Fill the vacancy from fresh provider inventory when eligible Ready
work exists. The canonical Thread, root Agent Task, branch, worktree, commits, and ownership
evidence remain recovery context rather than active-capacity authority.

Dev Backlog Coordinator chooses exactly one evidence-backed disposition:

1. Restore Running only when the same canonical owner demonstrably resumes safely and the
   Starting-plus-Running count is below ten. In the same serialized provider transaction,
   reconcile that current count, reject the transition and preserve Stalled when no slot is
   available, and otherwise record the renewed evidence without exceeding capacity.
2. Restore Ready when ownership has ended and normal redispatch is required. Any later
   execution proceeds through Ready -> Starting -> Running.
3. Set Blocked when a concrete cause and Coordinator-owned next action are known.
4. Set User Action Required when a concrete user-owned action is required and the record
   contains the exact question and unattended-work boundary.
5. Record an applicable terminal disposition when delivery or failure evidence satisfies
   that terminal contract.

A retained Stalled owner must not resume repository or provider mutation until Dev Backlog
Coordinator decides Stalled -> Running and Dev Backlog Steward records that transition.

Blocked is a known preventing cause awaiting Coordinator-owned coordination, recovery, or
disposition. Dev Backlog Coordinator is the lifecycle decision owner for Blocked. Dev
Backlog Steward performs the atomic provider mutation. Do not use Blocked because a task is
quiet, appears slow, or lacks a recognized cause.

When Dev Orchestrator recognizes a concrete blocker, it stops unsafe work, preserves commits
and evidence, obtains truthful resource disposition, and immediately notifies the parent Dev
Backlog Coordinator. The notification contains:

- provider identity or provider-none task
- canonical Thread and root Agent Task identifiers
- current phase
- exact blocker and blocker owner
- unblock condition
- requested Coordinator action
- preserved commits and evidence
- resource-ownership disposition
- whether the item remains safe to resume

The Coordinator acknowledges the notification, validates the handoff, chooses an authorized
coordination or recovery action, and asks Dev Backlog Steward to record Blocked when that is
the truthful provider disposition. After the provider state changes, remove the item from
active capacity, dispatch eligible replacement work, and retain Coordinator responsibility
until the blocker is resolved, routed to User Action Required, or terminally dispositioned.
Coordinator inability alone does not create a user obligation; an unresolved technical or
external blocker remains Blocked with an exact owner and unblock condition.

## Fifteen-Minute Parent Review

Dev Backlog Coordinator obtains fresh inventory and reviews the queue when:

- a work item enters or leaves Starting, Running, Stalled, or Blocked;
- a task stops, fails, times out, or reports a blocker;
- a review, verification, Commit, or Persistence result arrives;
- a user answers a recorded question;
- a claim owner sends a release or recovery notification; or
- the watchdog reports an actionable condition.

During that review, reconcile active capacity, eligible Ready work, Stalled and Blocked
inventory, actionable Stalled evidence, dependencies, accepted commits awaiting delivery,
completed deliveries awaiting closeout, task identity, and applicable claim results. Make
any scheduling or recovery adjustment supported by the evidence. The selected provider
records hold durable follow-up facts; provider none retains only task-local evidence. Do
not create a second registry.

### Dedicated Read-Only Watchdog

When the user requests background supervision for a sustained queue, the parent may assign one dedicated watchdog Task to an Agent operating under the Dev Backlog Watchdog Role. The watchdog never performs scheduling or recovery. It observes and reports; it is not a Work-item owner, queue entry, active-capacity slot, durable record, or substitute Coordinator.

#### Canonical Standing Prompt Template

```text
Act as the dedicated read-only Dev Methodology backlog watchdog for parent task {parent_task_id} in {repository_root}.

Apply skills/codex-workitem-coordination/SKILL.md, especially Dedicated Read-Only Watchdog and Fifteen-Minute Parent Review. On each cycle, read current file-backed work items, Git state, configured claim registry state, and Codex task state. Evaluate Running capacity and vacancies, phases and age, estimates/hard stops/evidence progress, Blocked unblock conditions, accepted work stranded before integration, integrated work awaiting provider closeout, terminal cleanup anomalies, waits at or beyond 30 minutes, and unsafe/stale/broad shared ownership.

Remain strictly read-only. Do not mutate repository files, lifecycle state, claims, tasks, branches, worktrees, or shared resources; do not dispatch, integrate, clean up, or run expensive/live verification. Notify parent task {parent_task_id} only when an actionable condition exists, with exact evidence and the smallest recommended parent action. When healthy, record only a concise no-action cycle result here.
```

#### Canonical Heartbeat Prompt Template

```text
Run one complete read-only watchdog cycle now using the task's standing contract. Notify parent task {parent_task_id} only if an actionable condition exists; otherwise record a concise no-action cycle note here.
```

Substitute only the resolved parent task identifier and repository root shown by these
placeholders. Supply provider and resource-coordination variation through resolved task
context without rewriting the canonical prompt text.

When the watchdog runs, it reads provider inventory, Git state, and task state. For provider none, it reads only task state. When agent-claim is loaded, it also reads the claim registry. It alerts on every stopped, failed, or missing canonical task for a Starting or Running item, every stopped task with a live claim, and every terminal item with a live claim. It also evaluates:

- every Running phase against its published estimate, hard stop, and latest evidence-bearing progress
- every suspected stall and every Stalled item's diagnostic evidence and exit conditions
- every Blocked item's exact blocker and unblock condition against current evidence
- accepted work stranded before Commit delivery, READY Commit delivery awaiting provider closeout, and terminal work awaiting cleanup
- stale, unsafe, or unnecessarily broad claims when agent-claim is loaded

The Watchdog is read-only. It reports evidence and recommended actions. It must not change repository files, provider records, lifecycle state, claims, task state, branches, worktrees, or shared resources. It must not dispatch work, integrate changes, perform cleanup, or run expensive or live verification.

When a progress anomaly has a known preventing cause, recommend the Blocked path rather than
Stalled. Recommend Stalled investigation only while the causal blocker or unblock condition
remains unknown.

Notify the parent only when action is required. Identify the affected provider identity or
task, observed evidence, reason attention is required, and smallest recommended Coordinator
action. Examples include suspected Stalled work, a satisfied Stalled or Blocked exit
condition, unused capacity with eligible Ready work, overdue work, stranded accepted work,
pending terminal closeout, an unsafe claim, or a task-identity or cleanup problem. The
Watchdog recommends action but never chooses the lifecycle result.

Treat active quiet tasks as healthy absent an explicit deadline or hard stop. Silence, title age, or lack of a recent message is not evidence of failure. When a configured hard stop is overdue, report the read-only deadline and cleanup-grace evidence without deciding delivery state.

When no intervention is needed, the watchdog emits one concise no-action cycle result without messaging or interrupting the parent; this self-report is its only task-state exception. The parent retains every scheduling, lifecycle, ownership, recovery, dispatch, Commit-application, Persistence-closure, integration, and cleanup decision. If the Watchdog or its schedule is unavailable, the parent performs the review directly; it does not create a replacement ledger or duplicate Watchdog.

## User Decisions And Terminal State

A user answer resolves a decision gate once; it does not prove delivery. The user may supply that answer in the canonical work-item Thread that asked the question. Record the exact answer and provenance through the selected Persistence manager and never ask it again. Route approved work to Ready, deferred work to Holding, and declined work to the applicable terminal disposition. For provider none, retain the answer in task-local evidence without creating durable provider state.

For approved work whose canonical Thread already exists:

1. The canonical Thread records the answer, preserves its existing identity and evidence, and sends one resumption request to the parent Coordinator.
2. For a selected provider, the parent Coordinator's Dev Backlog Steward child records User Action Required -> Ready. If the item is eligible under current priority and capacity, the parent Coordinator decides and reserves dispatch for that same Thread, and its Dev Backlog Steward child records Ready -> Starting rather than creating another Thread. Provider none records equivalent Ready and Starting evidence task-locally for its explicit task without Dev Backlog Steward, provider mutation, inventory, or capacity inference.
3. For a selected provider, the same root Dev Orchestrator accepts Running and its own Dev Backlog Steward child records Starting -> Running before repository mutation or delivery resumes. Provider none records equivalent Running acceptance task-locally in the same root Thread without a provider or Steward operation.
4. The parent acknowledges the lifecycle reconciliation in the canonical Thread. The user does not need to move to the parent Thread or repeat the answer there.

If the canonical Thread produced work before lifecycle reconciliation completed, preserve that work as out-of-sequence evidence. Do not accept, reject, delete, duplicate, or reimplement it merely because of its timing. Reconcile the provider state, applicable claims, commits, review, verification, and delivery evidence. Resume the same Thread only after Running is durable and the ordinary review and verification gates still pass.

Completed requires effective Commit disposition READY, required independent review, focused verification, and terminal evidence recorded through the effective Persistence-selected management skill when a provider exists. Provider none records the equivalent terminal evidence in the task result without a provider operation. Dev Orchestrator supplies the selected Commit skill's cleanup eligibility and candidate-to-delivery provenance. An idle, stopped, titled, or archived Codex task proves none of those facts.

Archive a terminal Thread only after the provider disposition is recorded, the worktree is removed or deliberately preserved, the delivery branch is safely deleted when eligible, and no unresolved notification remains. If archival fails, record the limitation and do not report success.
