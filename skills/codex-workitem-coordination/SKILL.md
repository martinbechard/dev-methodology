---
name: codex-workitem-coordination
description: Coordinate a repository work-item queue through canonical Codex tasks, serialized backlog transitions, isolated artifact lanes, evidence-bearing batons, non-polling wake-ups, and truthful terminal closeout. Use when the user explicitly asks Codex to delegate multiple backlog items to user-visible tasks and continue their coordinated delivery.
metadata:
  category: development-practice
---

# Codex Work-Item Coordination

Coordinate a queue from one Parent Backlog Coordinator while separate Dev Orchestrator tasks own active work items. Keep the file-backed backlog, repository claims, Git delivery evidence, and Codex task display state distinct.

## Authority And Roles

- Use user-visible Codex tasks only when the user or applicable project contract explicitly requests them. Use ordinary bounded subagents for ordinary in-task delegation.
- Treat the file-backed backlog as durable lifecycle authority, the repository-global claim registry as live mutation authority, Git as delivery evidence, and Codex task state as execution and display state only.
- Have Dev Backlog Steward perform serialized backlog transitions, Dev Orchestrator own one active item, artifact producers create changes, independent reviewers assess them, Dev Verifier run the required gates, and Dev Merge Coordinator integrate multiple accepted contributions or resolve target-specific collisions.
- Apply [manage-backlog](../manage-backlog/SKILL.md) for the complete backlog lifecycle contract. This skill adds Codex task coordination and does not replace that contract.
- Never treat an idle, silent, completed-turn, titled, archived, or stopped Codex task as proof of delivery.

## Parent Coordination Ledger

Maintain one compact parent-side record for each work item:

- canonical backlog path, normalized objective, dependencies, and queue priority
- source task identifier, parent task identifier, canonical child task identifier, creation time, status, current phase, and display title
- exact user answer and provenance when a decision gate was resolved
- current primary owner task identifier, role, claim, lifecycle commit, and release event
- designated successor task identifier, role, required release evidence, and precise next mutation
- predecessor release-notification state, parent receipt and acknowledgement, and successor notification and acknowledgement state
- active claims, isolated worktree, named resources, implementation and correction commits
- review, verification, integration, deployment, and refresh evidence as applicable
- current blocker, wake obligation, precise next mutation, and responsible owner
- terminal backlog commit, claim releases, clean-state evidence, archive eligibility, and any archive-tool result

Persist the canonical task identifier so later wake-ups, title updates, duplicate containment, and archival target identity rather than a mutable title.

## Reconcile Before Dispatch

At initial entry and after any interruption, rebuild the queue from live backlog files, active and archived Codex tasks, claim status, worktrees, Git branches and commits, user answers, and unread handoffs. Conversation memory and an old ledger are hints, not authority.

Inventory and prioritize the queue in the parent before creating tasks. Reconcile by canonical backlog path and normalized objective across active and archived tasks, including tasks with generic or obsolete titles. Resume unfinished owned work before new work and exclude unresolved user decisions, holding items, unmet dependencies, and terminal items.

Dispatch just in time:

- Do not create or keep a child active merely for preflight when it cannot enter LIFECYCLE START or ARTIFACT GO in the current baton window.
- After a read-only preflight handoff, persist the canonical task identifier and reversibly archive the dormant UI task when the host supports parking. Unarchive and wake only the selected next item.
- Do not create cross-task predecessor chains for independent items. The parent holds the single immediate-successor obligation.
- Do not run an active wait loop. An active child must own a claim or be performing a bounded running operation; otherwise it returns its handoff and stops or is parked.

## Dispatch Mutation Reconciliation

Treat an error, timeout, disconnect, or ambiguous response from task creation as an ambiguous mutation. It is not evidence that no task was created.

Before retrying, inspect the live task list and match candidates using all available identity evidence:

- source parent task identifier
- canonical backlog item path
- normalized objective or prompt identity
- creation time
- task status

Never rely on title alone. Resolve the result as follows:

1. If exactly one matching task exists, adopt its stable identifier and continue without retrying.
2. If multiple tasks match, designate one canonical task. Explicitly stop every duplicate before it can claim or mutate, verify its stopped and no-mutation state, record the containment in the ledger, and archive the duplicate when supported. Do not rename duplicates as a substitute for containment.
3. If the first reconciliation finds no match, allow one configured bounded settlement interval, then perform a second reconciliation. Never infer absence from one immediate list read.
4. Only if the settled second reconciliation still finds no match may the parent retry creation once.
5. After that single retry, allow the same bounded settlement interval and reconcile again. Adopt or contain the observed tasks; if none appears, report dispatch as blocked. Do not enter another retry loop.

After every measured dispatch batch, audit the task list for duplicates, missing tasks, unexpected active tasks, stale preflights, scope that differs from the intended backlog item, and missing canonical identifiers. Correct the ledger before expanding concurrency.

## Work-Item Phases

Use these exact phase names in handoffs and record the current phase in the parent ledger.

### READ-ONLY PREFLIGHT

Inspect the current backlog item, dependencies, claim registry, Git and worktree state, likely source and generated surfaces, tests, review and verification needs, shared resources, and collisions. Acquire no claim and mutate nothing.

Reconcile the canonical task before changing its title. After preflight, use set_thread_title to set a concise canonical title when useful, such as Waiting — X, Implementing X, Correcting X, Verifying X, or Blocked — X. Keep the task identifier stable. A title is bounded display state, not identity, backlog state, or delivery evidence; update it only at material phase changes.

### LIFECYCLE START

Have Dev Backlog Steward use a brief primary-worktree-only claim for the exact backlog item. Record Running ownership, commit that lifecycle change, and release immediately. Keep Ready to Running separate from any decision-resolution to Ready transition.

Refuse to perform or authorize this primary-required mutation from a mismatched isolated checkout. A Codex-created worktree does not grant repository authority. When another owner holds the primary baton, return PRIMARY_REQUIRED without mutation and arrange the parent-mediated baton; do not start artifact orchestration while the task still owes LIFECYCLE START.

### ARTIFACT GO

Authorize artifact work only after the lifecycle commit is durable, its claim is released, the primary state is clean, and the parent sends an evidence-bearing GO. Each producer, reviewer, verifier, generator, and integrator acquires its own narrow claim or named resource. Use canonical isolated worktrees for non-overlapping artifact lanes.

### ARTIFACT WAIT

When a claim or named resource returns WAIT or PRIMARY_REQUIRED, make no conflicting mutation and do not poll. Preserve clean committed work, release unrelated ownership that is no longer needed, record one exact wake obligation with the parent, return ARTIFACT WAIT, and stop.

### ARTIFACT RESUME

Only the parent wakes the selected canonical task. The current primary owner or predecessor has release-notification duty to the parent only and never wakes the successor. The parent reconciles the notification, then sends the successor the exact commit, release event, clean primary state and HEAD, released claim or resource, designated successor, and precise next mutation. Resume at the applicable claim, correction, review, verification, or integration step rather than replaying completed phases.

## Primary Baton

Serialize every short primary-only backlog mutation. The current owner commits and releases before the designated successor starts. The evidence-bearing baton contains:

- exact commit identifier
- exact claim release event and released scope
- exact current-owner task identifier, role, and claim identifier
- clean primary worktree status and primary HEAD
- live registry state relevant to primary availability
- canonical successor task identifier, role, and designated next owner
- precise next mutation and any preserved user-decision provenance

The current owner reports release to the parent and has no successor-wake authority. The parent alone verifies the evidence, acknowledges the predecessor notification, records the baton state, and wakes exactly the designated successor. Waiting children do not poll, wake each other, or ask for early release.

After the serialized lifecycle mutation releases, run concurrent non-overlapping artifact campaigns in isolated worktrees. Never hold a backlog claim while acquiring project artifacts, generators, verification resources, or integration ownership.

## Parent Baton Scheduler Audit

Start the first parent-side audit interval when the queue campaign starts. Complete another audit every 15 minutes from the prior audit completion while any queue work, active claim or task, baton, release notification, successor wake or acknowledgement, or accepted but unintegrated original or correction contribution remains unresolved. Continue after a predecessor or campaign turns terminal while any of those obligations remains unresolved. Stop only when the queue campaign is terminal and no queue work, active claim or task, baton, release notification, successor wake or acknowledgement, or accepted but unintegrated original or correction contribution remains.

For each completed interval, calculate these measurements from durable task and repository evidence:

- Terminal throughput is the count of backlog items that received a committed terminal disposition during the interval.
- Flow throughput is the count of distinct durable gate advances during the interval: a committed producer or correction contribution, accepted independent review, verifier verdict, integration commit, deployment or refresh completion, or terminal backlog commit. Count each gate advance once. Commentary, polls, retries, and duplicate evidence do not count.
- Average productive active tasks is the sum of task-seconds spent in claimed artifact work or another bounded running operation, divided by interval seconds. Exclude the parent coordinator, parked preflights, idle tasks, and wait-only tasks.
- Average blocked or waiting tasks is the sum of task-seconds spent blocked or waiting, divided by interval seconds. Report claim, baton, and shared-resource waits separately from technical blockers.

Record the interval boundary, queue counts, active claims and named resources, task-list anomalies, stale heartbeats, structured claim refusals, shared bottlenecks, and the exact commits and release events supporting each counted advance. Compare the current interval with the prior interval:

- Improving means terminal throughput and flow throughput are nondecreasing while average blocked or waiting tasks is nonincreasing, with at least one throughput increasing or the blocked average decreasing.
- Worsening means either throughput falls while the blocked average rises, or a baton drop, deadlock, repeated contention, stale activity, or overload appears.
- Stable means all three measurements are unchanged and none of the worsening conditions appears. Otherwise report mixed and explain the opposing movements.

Perform this baton lookup during every audit:

1. Reconcile live active and archived tasks, the authoritative claim registry, primary Git state, the file-backed backlog, unread handoffs, and the parent ledger.
2. Detect a predecessor release or terminal state without parent receipt, missing successor wake, missing acknowledgement, a successor still waiting after claim release, duplicate or mismatched tasks, or an ownerless pending mutation.
3. If the predecessor remains active or owns the claim, contact only that predecessor for its required release notification. Do not contact or poll the waiting successor.
4. If the predecessor is terminal and released but its notification is missing, reconstruct the exact commit, release event, owner task identifier, role, claim, clean primary state, and next mutation from live evidence. Record the missed notification duty.
5. If release evidence is complete and the successor wake is missing, reconcile the canonical successor identifier and have the parent send exactly one evidence-bearing wake. Record its delivery and acknowledgement so a later audit cannot duplicate it.
6. If acknowledgement remains absent, inspect recorded task state and messages at the next scheduled audit. Do not send a readiness probe and never instruct a child to poll.

The parent repairs missing notifications and baton deadlocks without transferring wake authority to a predecessor or child. After every audit, emit a concise user summary containing terminal throughput, flow throughput, both task averages, queue counts and claim state, named resources, task-list anomalies, stale heartbeats, structured claim refusals, shared bottlenecks, trend, baton result, cause, routing or concurrency adjustment, the next concurrency limit, and the supporting commits and release events.

### Post-Facto Scope And Work Reduction Audit

Treat claim reduction and targeted-work analysis as retrospective effectiveness practices, never as pre-dispatch, claim-acquisition, lifecycle, review, or verification gates. Do not delay ordinary narrow work to manufacture alternatives. Trigger this audit only after live evidence shows that a task held scope which delayed or blocked other work, or performed substantial broad work whose results were mostly unrelated to the changed surface.

When a claim caused measurable contention or an avoidable baton wait:

1. Record the oversized scope, affected tasks, wait duration or refusal evidence, and the work that actually required exclusivity.
2. Identify three concrete ways the claim could be reduced, such as replacing a tree with exact files, splitting unrelated files and named resources into separate claims, or releasing a completed stage before reacquiring only the next shared resource.
3. Compare the three options for ownership safety, preserved evidence, coordination cost, and expected throughput. Implement the best viable reduction for the resumed or next equivalent operation. If none is safe, retain the necessary scope and record why each reduction was rejected.

When an available full suite, broad runner, or large workflow consumed substantial effort while most checks were not applicable:

1. Record the broad command, duration or resource cost, relevant failures, and which evidence the work item actually required.
2. Identify three concrete targeted alternatives, including existing selectors or focused tests, a new focused script or runner selector, and a smaller fixture or preflight that proves the same boundary without launching unrelated work.
3. Compare evidence strength, false-negative risk, implementation cost, and reuse value. Implement the best viable targeted alternative before repeating the same broad work. Adding a focused script, test surface, fixture validator, or runner capability is valid optimization work when it preserves the required evidence.

This audit improves subsequent execution; it does not retroactively invalidate completed evidence, authorize mutation, weaken a required final gate, or require three-option analysis for work that remained narrow and did not create measurable waste. Retain full-suite or full-catalog verification for the risk-proportionate or final-state gate that genuinely requires it.

## Claims, Isolation, And Shared Resources

- Require every modifying owner to apply agent-claim before mutation and to inspect structured outcomes such as PRIMARY, ISOLATE, WAIT, PRIMARY_REQUIRED, ISOLATE_REQUIRED, and RECOVERY_REQUIRED.
- Never use isolation to bypass an overlapping scope. Extend ownership atomically before touching newly discovered files or resources.
- Preserve accepted sibling commits when regenerating or integrating shared outputs. Regenerate from accepted sources rather than copying derived files blindly.
- Release only from a clean committed worktree or a truthful explicit no-change result.
- Keep generators, browser profiles or ports, retained verification suites, target integration, deployment, installation, and similar cross-worktree state behind narrow named exclusive resources.

## Adaptive Artifact Concurrency

When at least three dependency-ready, non-overlapping items and runtime capacity exist, start with a floor of THREE active artifact campaigns. The floor applies to productive artifact work, not parked analysis or waiting tasks.

Use the 15-minute parent audit as the bounded health interval. When the audit reports Improving, active lanes are progressing, claims remain narrow, isolation succeeds, task-list audits are clean, and shared resources have capacity, add at most one productive campaign for the next interval. Scale by plus one again only after another healthy interval. Stable equality never authorizes scaling.

Back off immediately and record the evidence when a named bottleneck appears:

- generator contention: serialize the generated-output baton and rebase the latest accepted source
- browser contention: serialize the browser profile, port, or browser-verification resource
- verification contention: queue the retained suite or verification resource without blocking producers that no longer need it
- integration contention: serialize the target-specific merge resource and preserve accepted commits
- claim contention: narrow or reorder work; WAIT remains non-polling and overlapping scope never isolates around the conflict
- runtime pressure or stale heartbeats: stop new dispatch, reduce the next interval, and reconcile active tasks

Back off the affected resource or lane first. Reduce the global limit only when evidence shows system-wide pressure. When the trend is worsening, identify the cause and change routing or concurrency before dispatching another item.

Do not wait for an entire batch before routing finished work. Send each completed contribution into its next independent review, correction, verification, or integration step while other non-overlapping lanes continue.

## Review, Verification, And Integration

- Keep producer, independent reviewer, Dev Verifier, and integration ownership separate.
- Route material findings to the original producer and apply the configured bounded correction loop.
- Do not verify or integrate before required independent review accepts the contribution.
- Integrate a single accepted lane directly only when the selected delivery process permits it. Use Dev Merge Coordinator for multiple contributions, generated-output ordering, or conflicts.
- After integration, run fresh review and complete verification for the integrated state when affected surfaces require them.
- Rerun the full agent catalog only after every accepted correction is integrated. A focused green run before later fixes is not final catalog evidence.

## User Decision Gates

A user answer resolves a decision gate; it never proves implementation or delivery completion.

Read and record the exact answer and provenance once. Never ask the resolved question again. Route it through manage-backlog immediately when primary ownership is available:

- approved becomes Status Ready in the applicable typed active backlog
- deferred becomes Holding
- declined or ended becomes the applicable terminal archive

Ready to Running is a separate brief primary-only transaction. If WAIT or PRIMARY_REQUIRED prevents either transition, preserve the answer and provenance in the ledger, mark the question resolved there, retain exactly one parent-owned non-polling wake obligation, and require the current primary owner only to return its commit and release notification to the parent. Resume after the parent verifies that evidence and wakes the successor. Contention does not make the answer missing and never authorizes re-asking.

Completed is permitted only after implementation or delivery, required independent review, verification, integration or shared finalization, clean released claims and worktrees, and terminal backlog evidence. Approval alone satisfies none of those gates.

## Interruption Recovery

After interruption, rebuild the queue from the live backlog, claims, Git history and worktrees, task list including archived tasks, canonical identifiers, unread messages, and durable review or verification results. Reconcile ambiguous dispatches and user decisions before creating or waking anything. Preserve accepted commits and resume at the first unmet gate; do not replay approval, Ready, Running, or already released artifact phases.

## Terminal Backlog And Task Archival

Finish repository lifecycle before terminal UI cleanup:

1. Ensure required commits or explicit no-change evidence are durable.
2. Record accepted review and verification, or truthful terminal blocker evidence.
3. Finish integration, deployment, installation, or refresh when required.
4. Release every descendant, artifact, root, generator, verification, and integration claim or resource.
5. Confirm each worktree is clean or intentionally preserved and no baton, wake-up, notification, or lifecycle obligation remains.
6. Have Dev Backlog Steward commit the truthful terminal backlog disposition through a brief primary claim and release it.

Completed, Failed, Abandoned, and durably Blocked tasks become terminal-archive eligible only after the corresponding backlog disposition is committed. Blocked without terminal backlog evidence is not archive eligible.

Do not terminally archive a task parked for user approval, waiting for a claim or baton, preserving corrections for authorized resumption, in Target Merge Pending, or still responsible for a downstream notification. Before terminal archival, reconcile the canonical identifier and live task list, contain duplicates, and record terminal commit and release evidence in the parent ledger. For a successful terminal outcome, set the final title to exactly Done — <concise item>; never use Completed —. Waiting —, Blocked —, Failed —, and Abandoned — remain valid material state titles. A title may expose the durable outcome but does not replace the gates.

Archive eligible terminal tasks promptly and run periodic housekeeping audits so the visible task list reflects current work. UI archival is lifecycle cleanup; it does not delete commits, branches, backlog evidence, claims journals, or the stable task identifier.

If set_thread_archived returns exactly “Inactive thread archive did not persist”, treat it as ambiguous and no persisted mutation. Do not retry blindly or claim the task is archived. Reconcile task state once, record the attempted canonical identifier and tool result, retain durable repository and backlog evidence, and surface the app limitation for a later safe retry only when a supported archival path exists.

Reversible dormant-preflight parking is not terminal archival. Keep its canonical identifier and preflight handoff in the ledger, and unarchive it only when the parent selects that item just in time.

## Coordination Report

After every 15-minute parent audit, report both throughputs, both task averages, queue counts and claim state, named resources, task-list anomalies, stale heartbeats, structured claim refusals, shared bottlenecks, trend, baton lookup result, cause, adjustment, next concurrency limit, and supporting commits and release events.

Report:

- queue counts, priorities, canonical tasks, phases, and task-list anomalies
- active claims, worktrees, named resources, and current concurrency limit
- lifecycle commits, release events, exact baton successor, and wake obligations
- contributions awaiting review, correction, verification, integration, deployment, or refresh
- blocked items with precise blocker and owner
- resolved user decisions without repeating their questions
- recent terminal backlog evidence, archive eligibility, archive attempts, and app limitations
- final full-catalog result only after all accepted fixes are integrated
