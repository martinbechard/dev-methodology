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
- PROJECT.yaml selects resource coordination independently as none or agent-claim. When enabled, its registry records temporary shared-mutation protection but does not determine whether reviewed, verified, committed delivery exists.
- Codex Thread state and title are display and execution state, not lifecycle authority.
- Dev Backlog Coordinator owns provider-routed queue inventory, priority, dispatch, stalled-delivery investigation, and terminal Thread cleanup.
- Dev Orchestrator owns one work item after its root Agent accepts Starting -> Running through delivery or a truthful terminal outcome. It may assign bounded Tasks to Dev Coder, independent reviewer, and verifier child Agents inside that Thread.
- Dev Backlog Steward applies the effective Persistence-selected management skill for provider inventory and lifecycle mutation. Dev Orchestrator applies the effective Commit-selected skill only after candidate review and verification accept a direct or combined commit.

Do not create a separate parent ledger, baton registry, waiting-Task registry, or Thread database. Do not copy this procedure into AGENTS.md or a Dev Orchestrator definition.

## Resource Coordination Selection

When PROJECT.yaml selects agent-claim, apply that enabled resource-coordination implementation for shared files and exclusive runtime resources. The claim-specific commands, outcomes, retry window, registry evidence, and release fields below apply only under that selection. When PROJECT.yaml selects none, load no coordination implementation; do not discover, acquire, heartbeat, mutate, inspect, hand off, reset, or release claims; and omit claim attempt counts, blocking claim identifiers, registry evidence, and claim-release evidence while preserving work-item ownership, commits, clean-state checks, review, verification, Commit delivery, Persistence completion, and cleanup.

## Work-Item Execution Record

For a selected Persistence provider, use its management skill to record these phase-appropriate facts in the provider's supported ownership, open-issues, and evidence fields. For provider none, retain them in the canonical Codex Thread result without creating a shadow record:

- canonical work-item Thread identifier, root Dev Orchestrator Agent, and canonical Task identifier for that root assignment when the runtime supplies one
- branch and worktree
- current phase
- accepted candidate commit
- delivery-wait or provider-closure-wait start time
- enabled resource-coordination attempt count, last outcome, next attempt time, and blocking ownership identifiers
- open issues and the owner of each next action
- review, verification, Commit disposition, enabled coordination release, provider closure, and cleanup evidence as those events occur

Use the effective Persistence-selected management skill to update a provider record when a material phase changes. Preserve the same canonical Thread identifier, root Agent assignment, and provider identity through corrections, delivery, and closeout. Never infer identity from the Thread title alone.

## Queue Target And Dispatch

Obtain queue inventory, lifecycle counts, provider identities, and dispatchable state only by applying the effective Persistence-selected management skill.

- Provider file: treat ordinary repository backlog paths as provider identities and use short backlog claims only for file-provider mutations. Do not scan or count backlog/future-ideas unless the parent explicitly requests ideation or promotion.
- Provider github: use GitHub issue identities and provider lifecycle evidence; do not create or inspect file backlog paths.
- Provider gitlab: use GitLab issue identities and provider lifecycle evidence; do not translate them into GitHub or file records.
- Provider azure-devops or jira: apply the selected placeholder management skill, preserve its BLOCKED zero-mutation result, and do not fall back.
- Provider none: do not inventory, count, create, transition, or close durable provider records; coordinate only the explicit task and retain task-local evidence.
- Provider UNSET or an unavailable selected skill: stop before durable inventory or mutation and request the missing project selection or capability.

For a provider that supports queue inventory and lifecycle transitions:

1. Count work items whose provider lifecycle state is Starting or Running.
2. When the count is below ten, select enough eligible Ready items to fill available capacity without exceeding ten active items.
3. For each selection, have the parent Coordinator's Dev Backlog Steward child atomically record the Ready -> Starting reservation and dispatch evidence through the effective Persistence-selected management skill before creating a runtime Thread.
4. Reconcile the reservation and existing runtime evidence, then create at most one user-visible work-item Thread for the Starting work item.
5. After the Thread's root Dev Orchestrator Agent accepts ownership, have that Orchestrator's Dev Backlog Steward child atomically record Starting -> Running with the canonical Thread identifier, root Agent Task identifier when applicable, branch, worktree, and enabled coordination evidence.
6. Dispatch only work that can begin implementation or another bounded delivery phase. Do not create a Thread merely to wait for approval, a dependency, a reviewer, resource ownership, or a delivery window.
7. When an item leaves Starting or Running, fill the active-capacity vacancy promptly through the same Ready -> Starting reservation sequence.

Blocked, User Action Required, Holding, Awaiting Review, Completed, Failed, Abandoned, and Future Ideas do not count toward ten. Future Ideas are not work-item states and enter coordination only after deliberate promotion creates a complete typed work item. If fewer than ten eligible items exist, activate all eligible items and report the shortage instead of manufacturing placeholder work. Provider none does not synthesize a queue or a target of ten from Thread state.

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

- When agent-claim is selected, use its configured transport exactly as rendered in AGENTS.md. When none is selected, do not probe either claim transport.
- Keep implementation and focused tests in the work-item Thread's private worktree. The environment must permit ordinary writes to that worktree and the Git worktree metadata needed for local commits.
- When a work item depends on a special runtime capability, test that capability through the same nested execution path the real workload uses before assigning more equivalent work to that environment. A direct command is not sufficient evidence for a runner that invokes the command from a child process.
- Treat prior runtime-capability evidence as stale after any agent-definition or metadata generation, adapter installation, MCP refresh, Codex configuration change, permission-profile change, application update, or host restart. Before dispatching real work again, run one disposable worktree pilot through the effective child Agent runtime.
- The post-change pilot must prove the effective Agent profile and ordinary operations, not merely read the requested configuration or repeat permission wording in its prompt. Inspect the child Agent's effective approval, sandbox, and permission profile; create a harmless Git commit; invoke every selected special capability through the same nested helper used by the real workload; and, only when agent-claim with MCP is selected, read its registry through MCP.
- If the requested configuration and effective child runtime differ, or any representative operation fails, stop equivalent dispatch immediately. Record the exact requested and effective profiles, archive the failed pilot Thread, correct or replace the launch environment, and rerun the pilot. Do not treat a successful direct command, parent capability, config file, or earlier Thread as evidence for the failing child runtime.
- If an ordinary required operation fails because the Agent environment lacks a capability, the Agent stops immediately, preserves its work, truthfully releases enabled resource ownership, and reports the exact failed operation to the parent. It must not request escalation from the user.
- The parent promptly re-homes the Thread or replaces its root Agent in a compatible environment, asks Dev Backlog Steward to update canonical identifiers through the selected Persistence manager, and fills any resulting Starting-plus-Running vacancy. For provider none it updates only the task-local identity. Do not leave an approval prompt or an execution-incompatible Agent consuming active capacity.

Set a concise plain-text title when the Thread is created and update it only at material phase changes. Use a phase prefix such as Implementing —, Reviewing —, Verifying —, Integrating —, Waiting for Claim —, Waiting for Help —, Waiting for User —, Done —, Blocked —, Failed —, or Abandoned — followed by a short work-item name. Never use raw prompt text, XML or delegation tags, error output, identifiers, or generic titles as the display title. Preserve the stable Thread identifier; the title remains display state and never becomes lifecycle authority or delivery evidence.

## Starting And Work-Item Thread Ownership

A work item is the durable provider record for an outcome, lifecycle, evidence, and ownership. A Thread is one execution context or conversation. An Agent is a runtime instance operating under a Role, which is a reusable responsibility and authority contract. A Task is a bounded assignment to an Agent; it is never a synonym for Thread. A Handoff is a lifecycle event that transfers evidence and the next action.

The parent coordination Thread has one root Agent under the Dev Backlog Coordinator Role. Each Starting or Running work item has exactly one work-item Thread with one root Agent under the Dev Orchestrator Role. Producing, implementation, independent review, verification, delivery, and stewardship Agents are children in that work-item Thread.

Ready -> Starting is the parent Coordinator's dispatch and capacity-reservation decision. Use its Dev Backlog Steward child to record the reservation through the selected manager before launch, and count Starting against capacity exactly like Running. Reconcile existing reservation and runtime evidence before every launch. One work item must not create a duplicate Thread after a timeout, Thread-creation error, or ambiguous startup.

After the work-item Thread's root Dev Orchestrator Agent accepts ownership, it uses its Dev Backlog Steward child for the atomic Starting -> Running transition. The record includes the canonical Thread identifier, canonical root Agent Task id when applicable, branch, worktree, and enabled coordination evidence. If launch fails and no owner accepted, restore Ready. If ownership was accepted or evidence cannot safely be discarded, record Blocked or User Action Required with the exact recovery condition. Starting and Running stay in the provider's active queue.

The work-item Orchestrator owns candidate production, review, verification, Commit delivery, and terminal Persistence request. Its Steward child records the selected provider lifecycle changes. The parent Coordinator never performs per-item delivery or completion; after the terminal Handoff it cleans the runtime Thread and worktree, recounts Starting plus Running capacity, and dispatches replacement work.

## Private Worktree Work

Implementation, correction, review, and focused local tests on a work-item Thread's private branch and worktree do not require operational ownership when they cannot mutate shared repository state or a named shared resource.

When resource coordination is enabled, acquire ownership before mutating shared state, including:

- repository paths or target-branch integration resources required by the selected Commit skill
- the file backlog on primary main only when Persistence is file
- generated output or another shared output location
- shared installations, ports, browsers, databases, or test resources that cannot safely run concurrently

Keep every enabled ownership scope limited to the exact files and named resources required for that operation. Isolation never authorizes modification of another Thread's owned shared surface. With coordination none, skip this lifecycle and rely on the delivery process's explicit work-item scope and serialized main or provider transactions.

## Effective Commit Delivery And Persistence Closure

Dev Orchestrator owns temporal delivery order while the selected Commit and Persistence skills own their respective procedures.

For direct-main integration, start from current main and Designate this fresh branch as the Work-item integration and cleanup branch. Integrate only accepted commits or their exact accepted paths. Do not import cumulative branch ancestry merely to preserve provenance; record the source-to-integration mapping instead. When resource coordination selects agent-claim, keep administrative coordination-registry cleanup, Git integration, and terminal backlog completion as three distinct operations. Cleanup is eligible only after the fresh Work-item integration branch is fully merged. A prior candidate branch used only as a non-ancestral content source is not the Work-item cleanup branch.

1. Require Dev Coder to return a clean verified candidate commit without applying terminal Commit delivery or provider mutation.
2. Obtain fresh independent source review and source verification for every candidate. Return correctable source findings to the original Dev Coder and repeat those gates on the replacement candidate.
3. When multiple accepted candidates must be combined, use Dev Merge Coordinator, then obtain the required fresh post-combination review and complete verification. A single accepted candidate remains the direct commit.
4. Apply or resume the effective Commit-selected skill only after candidate review and source verification accept the direct or combined commit.
5. Preserve AWAITING_REVIEW with the same delivery identity while review, checks, dependency order, correction, merge, or final observation remains pending. A source correction returns through Dev Coder, independent review, and verification before the same Commit delivery resumes.
6. When Commit first returns AWAITING_REVIEW for a selected provider, ask Dev Backlog Steward exactly once to record the nonterminal lifecycle AWAITING_REVIEW through the effective Persistence-selected management skill. Include the delivery identity, publication reference, accepted commit, completed checks, and pending gates. Verify the recorded provider state before reporting AWAITING_REVIEW.
7. On a repeated observation of the same delivery identity and Commit handoff, reconcile the existing update instead of dispatching a duplicate. Never request lifecycle COMPLETED from an AWAITING_REVIEW handoff. Provider none retains the same nonterminal evidence task-locally without a steward dispatch.
8. Resume the same effective Commit-selected skill through review corrections, checks, dependency order, merge, and main observation until it returns READY or BLOCKED.
9. Only after the effective Commit-selected skill returns READY, ask Dev Backlog Steward exactly once for the distinct terminal lifecycle COMPLETED update through the effective Persistence-selected management skill. Verify the selected manager's recorded closure and reconcile an already successful terminal update instead of dispatching a duplicate.
10. Provider file closure may use a separate short primary-main backlog claim and the file manager's archive procedure. GitHub and GitLab closure use their own provider identities, concurrency behavior, and lifecycle evidence. Placeholder providers preserve BLOCKED without fallback. Provider none records terminal evidence only in the task result and performs no durable provider mutation.
11. Notify the parent with candidate provenance, independent review and verification, final Commit disposition, nonterminal and terminal provider results when selected, claims, branch or delivery identity, worktree, and cleanup eligibility.
12. The parent removes only clean eligible worktrees and branches, updates the task title, archives terminal task UI state when supported, then obtains fresh provider inventory and fills eligible capacity through the selected management skill.

Keep coordination-registry cleanup, Commit delivery, and Persistence closure as distinct operations. Each has its own authority, evidence, and outcome; none can manufacture or replace another. Do not leave an accepted commit for a separate delivery task: Dev Orchestrator applies the effective Commit-selected skill because it owns the accepted commit, review, verification, and resumption context.

When resource coordination selects agent-claim, keep administrative coordination-registry cleanup separate from Commit delivery and Persistence closure. When none is selected, omit coordination-registry cleanup and coordination evidence.

If the nonterminal AWAITING_REVIEW update fails or its result is ambiguous, preserve the Commit handoff and reconcile that same Persistence transaction before resuming delivery. Do not request terminal COMPLETED, repeat an already successful nonterminal update, or reinterpret the Commit disposition as terminal.

## Agent-Claim Retry Window

This section applies only when resource_coordination selects agent-claim. When a shared Commit resource, file-provider backlog claim, or selected provider mutation guard is unavailable, Dev Orchestrator asks Dev Backlog Steward to record the wait through the effective Persistence management skill when a provider exists, retains task-local evidence for provider none, and owns this bounded retry schedule:

1. Attempt immediately.
2. Retry at five, ten, fifteen, twenty, twenty-five, and thirty minutes.
3. Before each retry, inspect the blocker and update the selected provider record, or the provider-none task result, with the outcome and next attempt.
4. Stop retrying as soon as the claim succeeds.

This is one initial attempt plus no more than six retries. Do not create a waiting Task, transfer the wait through a Task chain, poll more frequently, or ask the user to approve ordinary Git or shell commands already covered by the work item. Under resource coordination none, this entire retry and registry-recovery section is inapplicable.

At thirty minutes, Dev Backlog Coordinator investigates instead of allowing another passive wait. Identify the blocking owner, verify whether its claim is active or stale, and choose a safe remedy: request prompt release, narrow or split an unnecessarily broad claim, complete the blocking integration first, or route a genuine technical or user-decision blocker. Never release or override a claim whose owner has uncommitted or otherwise unpreserved work.

An evidence-backed administrative reset is available only for an inactive coordination-registry entry. Before reset, inspect the task and logs, matching processes, claimed worktrees, Git cleanliness and preserved commits, every claimed shared resource, other registry entries, and journal evidence. Retain a readable snapshot or journal reference. Reset only registry state after proving the owner inactive, all work completed or preserved, all resources stopped or handed off, and no active protection affected. A live owner, dirty unpreserved worktree, resource in use, or unclear evidence blocks reset.

Perform the reset only through a host-supported targeted atomic operation that names the exact entry, locks the coordination registry, revalidates those safeguards at mutation time, removes no peer entry, and journals the administrative outcome. The bundled portable claim command has no reset operation. If a supported atomic operation is unavailable, stop and route the reset instead of editing the registry file manually.

Treat inactive-entry release problems as coordination diagnostics. Claim release does not audit commit history or interpret merge ancestry; independent review and integration own committed-content, changed-path, and provenance decisions. Reconcile each evidence owner separately and never invent a successful release.

If the wait remains unresolved after investigation, record the precise open issue through the selected Persistence manager and request the truthful Blocked or User Action Required transition so it no longer consumes active Starting-plus-Running capacity. For provider none, preserve the BLOCKED Thread result without a provider mutation. Reserve and dispatch a replacement Ready item through Ready -> Starting from fresh selected-provider inventory when available.

## Tiered Verification

Per-item verification is proportional to changed behavior and risk:

- run changed-module and directly related regression tests first
- add generated-output freshness, shared-resource, or integration tests only when the changed surfaces require them
- expand after a focused failure or evidence-backed cross-cutting risk
- do not run the complete agent catalog for an individual work item

Run the complete accepted agent catalog once against the final integrated campaign state after every accepted work-item fix is on main. Retain the final per-suite and global reports and disposition every failure.

## Long-Running Task Control

Treat a heartbeat as ownership evidence only. It does not prove useful progress, justify the current command, or make an expensive phase healthy.

When a command or phase is expected to take more than five minutes, the Dev Orchestrator exposes before starting it:

- the exact currently active unit and any later units that have not started
- the expected duration or best evidence-based estimate
- a hard stop condition and the retained evidence path
- the distinct acceptance criterion that requires the expensive operation

This is non-blocking operational telemetry in the task update, not a new provider transaction or parent approval gate. Persist it through the selected Persistence manager at the next already-authorized material phase transition, or retain it task-locally for provider none. When Persistence is file, do not acquire a backlog claim solely to record timing. The task may start without waiting for parent acknowledgement.

The parent observes long-running work at phase start, first failure, timeout, and completion rather than waiting for the fifteen-minute periodic review. This observation must not serialize healthy work. Inspect the actual process, elapsed time, latest evidence-bearing output, and remaining work. Status messages must distinguish one active serial case from selected or queued cases and must not describe queued work as running.

After an expensive failure, classify its failure signature before repeating anything. Reuse retained output, add the smallest offline replay or deterministic regression that reproduces the boundary, and make that focused check pass before another equivalent live or broad run. Run one cheapest representative first. Start a second expensive representative only when it covers a distinct acceptance criterion that retained evidence and deterministic checks cannot prove.

If the active unit reaches its hard stop, repeats the same failure signature, or stops producing evidence-bearing progress within its declared bound, stop that exact unit, preserve or commit owned work, stop or hand off every exclusive resource, and prove the applicable worktree clean before releasing enabled ownership. If safe release is not yet possible, retain and heartbeat enabled ownership or hand it off explicitly rather than releasing unsafely. Return to focused correction only after truthful ownership disposition. Do not let later serial cases start automatically after a shared-boundary failure. Two unproductive attempts or fifteen minutes beyond the declared phase estimate require immediate parent investigation and a revised plan rather than another retry.

## Fifteen-Minute Parent Review

Every fifteen minutes while queue work remains, Dev Backlog Coordinator obtains fresh inventory through the effective Persistence-selected management skill and reviews:

- Starting plus Running count and vacancies against the target of ten
- work items by phase and age of the current phase
- Commit-delivery and Persistence-closure waits, especially every wait at or beyond thirty minutes
- active resource ownership when enabled, including exact scopes, owners, and heartbeat freshness
- accepted commits awaiting Commit delivery
- completed Commit deliveries awaiting Persistence closeout
- Thread or Agent Task anomalies, duplicate Threads, stopped Agents, and missing canonical identifiers
- interval delivery counts: accepted commits, reviews, verifier gates, Commit dispositions, terminal transitions, and completed items
- average productively active and blocked task counts using the available interval samples

Make a scheduling or recovery adjustment during the same review whenever delivery worsens, vacancies remain, or a wait exceeds its limit. The selected provider records hold durable follow-up facts; provider none retains only task-local evidence. The review must not create a second registry.

### Dedicated Read-Only Watchdog

When the user requests background supervision for a sustained queue, the parent may assign one dedicated watchdog Task to an Agent and schedule it to observe the fifteen-minute review checks. The watchdog never performs the parent review's scheduling or recovery adjustment. It is an observer, not a Work-item owner, queue entry, active-capacity slot, durable record, or substitute Coordinator.

On every cycle, the watchdog applies the selected provider's read-only management inventory, then reads Git state and task state. For provider none it reads only explicit task state and does not invent provider inventory. When resource coordination selects agent-claim, it also reads coordination-registry state and evaluates shared-resource ownership. When resource coordination selects none, it omits coordination-registry reads, shared-resource ownership evaluation, and coordination alerts or evidence. It immediately alerts on every stopped, failed, or missing canonical task for a Starting or Running item, every stopped task that retains a live coordination entry, and every terminal item that retains a live coordination entry. Detection has no extra grace timeout beyond the cycle interval. In addition to the applicable parent-review checks above, it evaluates:

- every Running phase against its published estimate, hard stop, and latest evidence-bearing progress
- every Blocked item's exact blocker and unblock condition against current evidence
- accepted work stranded before Commit delivery, READY Commit delivery awaiting provider closeout, and terminal work awaiting cleanup
- when resource coordination selects agent-claim, stale, unsafe, or unnecessarily broad shared-resource ownership

The watchdog is mechanical read-only evidence and advice only. It must remain read-only and does not mutate repository files or lifecycle state. It must not mutate backlog, claims, or task state; acquire, extend, reset, release, or override coordination entries; dispatch work; change work-item or parent task state, branches, or worktrees; perform cleanup; or run expensive or live verification. It must not infer integration readiness, accepted delivery, or completion readiness.

Notify the parent only when an actionable condition exists. The alert identifies the affected item or task, the observed evidence, why attention is required now, and the smallest recommended parent action. Actionable conditions include a satisfied Blocked-item unblock condition, a Starting-plus-Running vacancy with eligible Ready work, a phase overrun or evidence gap, a wait at or beyond thirty minutes, stranded accepted work, pending terminal closeout, unsafe coordination state when resource coordination selects agent-claim, or a task-identity or cleanup anomaly.

Treat active quiet tasks as healthy absent an explicit deadline or hard stop. Silence, title age, or lack of a recent message is not evidence of failure. When a configured hard stop is overdue, report the read-only deadline and cleanup-grace evidence; never auto-release the claim or decide delivery state.

When no intervention is needed, the watchdog may emit its own concise no-action cycle result without messaging or interrupting the parent; this self-report is its only task-state exception. The parent retains every scheduling, lifecycle, ownership, recovery, dispatch, Commit-application, Persistence-closure, integration, and cleanup decision. If the watchdog or its schedule is unavailable, the parent performs the review directly; it does not create a replacement ledger or duplicate watchdog.

## Post-Facto Efficiency Audit

These audits improve the next equivalent operation. They are not pre-dispatch, resource-ownership, review, verification, Commit-delivery, or Persistence-closure gates.

After evidence shows that enabled coordination scope was broad enough to delay other work:

1. Record the actual contention and exclusive work.
2. Identify three concrete scope reductions.
3. Implement the best safe reduction for the next or resumed equivalent operation.

After evidence shows that a broad suite or workflow performed substantial mostly unrelated work:

1. Record the broad command, cost, and evidence actually required.
2. Identify three targeted alternatives, including a focused selector and, when useful, a new script, test surface, or fixture validator.
3. Implement the best alternative before repeating that broad work.

Do not retroactively invalidate valid evidence or weaken the final campaign-wide catalog gate.

## User Decisions And Terminal State

A user answer resolves a decision gate once; it does not prove delivery. Record the exact answer and provenance through the selected Persistence manager and never ask it again. Route approved work to Ready, deferred work to Holding, and declined work to the applicable terminal disposition. For provider none, retain the answer in task-local evidence without creating durable provider state.

Completed requires effective Commit disposition READY, required independent review, focused verification, released delivery ownership, and terminal evidence recorded through the effective Persistence-selected management skill when a provider exists. Provider none records the equivalent terminal evidence in the task result without a provider operation. Dev Orchestrator supplies the selected Commit skill's cleanup eligibility and candidate-to-delivery provenance. An idle, stopped, titled, or archived Codex task proves none of those facts.

Archive a terminal Thread only after the provider disposition is persisted when selected, all enabled resource ownership is released, the worktree is removed or deliberately preserved, the delivery branch is safely deleted when eligible, and no unresolved notification remains. If Thread archival does not persist, record the tool limitation through the selected provider manager or provider-none Thread result and do not report success.
