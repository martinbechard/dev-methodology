---
name: coordinate-codex-tasks
description: Map portable work-item coordination to Codex task creation, resumption, identity, titles, follow-up, reconciliation, watchdog operation, and archival. Use only when coordinated work runs through Codex tasks.
metadata:
  category: development-practice
---

# Coordinate Codex Tasks

Codex task control maps one portable work-item execution to one canonical Codex task and its retained user-visible context. Apply coordinate-work-items together with this skill. This skill does not create provider lifecycle authority, delivery authority, or resource ownership.

## Coordinator Subagent And Root Dispatcher

Run the Dev Backlog Coordinator as the coordination Agent. When it runs as a collaboration subagent, it retains authoritative provider, lifecycle, capacity, dependency, claim, finish-lane, recovery, re-homing, dispatch-packet, and reconciliation decisions even when Codex withholds user-visible task controls from that subagent.

The root calling task uses its project-private runtime dispatcher. The Coordinator returns an exact executable packet; the authorized root runtime dispatcher performs only the approved task creation, resumption, message, title, wait, archive, automation, or related caller-only operation and returns the exact result to the Coordinator. The authorized root runtime dispatcher does not adopt the Coordinator Role, independently select work, mutate Coordinator-owned lifecycle, or create a second coordination record.

When the Coordinator runtime itself exposes the required task control, it may execute its own approved operation directly unless the operation is terminal cleanup. The Coordinator must not execute terminal cleanup directly. Runtime placement changes the executor for ordinary operations, not coordination authority or the external terminal-cleanup boundary.

## Codex Capability Check

Create a coordinated Codex task only in an environment where its root Agent can perform the ordinary operations authorized by the work item. The dispatch prompt states that ordinary repository writes, Git operations, focused tests, process inspection, and selected resource-coordination commands are already authorized. The Agent must not open or wait on a user approval prompt for those operations.

When work depends on a special runtime capability, test it through the same nested execution path used by the real workload. Direct parent execution is not sufficient evidence for a child Agent. Treat prior capability evidence as stale after agent-definition generation, metadata generation, adapter installation, MCP refresh, Codex configuration changes, permission-profile changes, application updates, or host restart.

The capability pilot proves the effective Agent profile and ordinary operations. Inspect the child Agent's effective approval, sandbox, and permission profile. Create a harmless Git commit in a disposable worktree. Invoke each selected special capability through the same nested helper as the workload. If the requested configuration and effective child runtime differ, stop equivalent dispatch, record both profiles, archive the failed pilot, correct the environment, and rerun one pilot.

If an ordinary required operation fails because the Agent lacks a capability, the Agent stops, preserves work, and reports the exact failed operation to the dispatcher. It must not request escalation from the user. The dispatcher consults the Dev Backlog Coordinator. The Coordinator decides whether to re-home the task or replace its root Agent, reconciles the canonical identity, and returns any caller-only runtime instruction to the dispatcher. The dispatcher executes that instruction and returns current runtime evidence to the Coordinator for coordinate-work-items.

## Codex Task Creation And Resumption

The Dev Backlog Coordinator may authorize at most one root Dev Orchestrator task after coordinate-work-items records the Starting reservation and permits runtime dispatch. It supplies the complete task title, prompt, provider reservation, baseline, isolation, claim, authority, verification, reporting, and cleanup packet. The authorized runtime executor may create at most one root Dev Orchestrator task for that packet. The Coordinator executes creation directly only when its runtime exposes the required control; otherwise the authorized root runtime dispatcher executes that exact packet. Return the task or pending client identity and retained user-visible context to the Coordinator as runtime evidence; neither result changes provider lifecycle.

Collaboration subagent launches follow the Codex Harness Collaboration Subagent Launch Contract. A separate user-visible Codex work-item task is not a collaboration subagent launch. Create it only through explicit provider and canonical-task handoffs. Give it a self-contained dispatch prompt and no implicit parent-conversation inheritance.

When an existing canonical task was preserved through User Action Required, Stalled, Blocked, or another resumable state, resume that task. Do not create a replacement merely because the task is idle. The portable lifecycle owner first records the required Starting handoff. The task then accepts Running through the portable contract.

Do not create a task merely to wait for approval, a dependency, a reviewer, a shared resource, or a delivery window. Do not retry task creation after an error, timeout, disconnect, or ambiguous response. Reconcile the result first.

## Canonical Codex Task Identity

A Codex task is the canonical runtime execution identity for one root Dev Orchestrator assignment. A conversation is the retained user-visible context for that assignment. The task identifier and conversation identifier are distinct, even when the runtime exposes one combined surface.

Record these fields when the runtime supplies them:

```markdown
Codex Task ID: [opaque task identifier]
Conversation ID: [opaque retained-context identifier]
Root Role: Dev Orchestrator
Runtime Parent Task ID: [opaque authorized root runtime dispatcher or direct creator task identifier]
Coordinator Task ID: [opaque Dev Backlog Coordinator task or subagent identifier]
```

The runtime parent is the task that actually invokes Codex task creation. The Coordinator task is the execution that authorizes the operation and receives its result. Record both even when one root task performs both functions and the values are equal. Use Runtime Parent Task ID for runtime lookup and ambiguous-creation reconciliation. Use Coordinator Task ID for decision routing. Do not infer either identity from the conversation title, prompt text, branch, worktree, or provider record path. Preserve the same canonical task and conversation through corrections, review, verification, delivery, and resumable lifecycle pauses. A replacement requires explicit duplicate reconciliation and a recorded identity handoff.

## Conversation Title Contract

The canonical conversation keeps one stable identity. Its conversation title is display state, never lifecycle authority, active-execution evidence, or delivery evidence. Use the format phase label — short work-item title.

Use this lifecycle and phase mapping:

- Ready: Ready — short work-item title.
- Starting: Starting — short work-item title.
- Running: Implementing —, Reviewing —, Verifying —, Integrating —, Waiting for Claim —, or Waiting for Help — short work-item title.
- User Action Required: Waiting for User — short work-item title.
- Stalled: Stalled — short work-item title.
- Blocked: Blocked — short work-item title.
- Holding: Holding — short work-item title.
- Awaiting Review: Awaiting Review — short work-item title.
- Completed: Done — short work-item title.
- Failed: Failed — short work-item title.
- Abandoned: Abandoned — short work-item title.

The owning Coordinator or Orchestrator is accountable after every successful lifecycle transition. When its runtime exposes rename authority, it renames the canonical conversation directly. Otherwise it supplies the exact title operation to the authorized root runtime dispatcher and reconciles the returned outcome. When neither authorized path exposes rename authority, leave the title unsynchronized and retain that limitation in the durable record; do not send a title-only task message. A failed title update does not roll back a durable lifecycle transition.

Apply the title contract when the task is created, after each successful lifecycle transition, and at each material Running phase change. Never use raw prompt text, markup, error output, identifiers, or a generic title.

## Codex Runtime Reconciliation

Treat a task-creation error, timeout, disconnect, or ambiguous response as an ambiguous runtime mutation. Reconcile active and archived Codex tasks using all available evidence:

- runtime parent task identifier
- Coordinator task identifier
- provider selector and opaque Work Item ID when present
- normalized objective
- creation time
- task and conversation state

If exactly one match exists, the Coordinator must adopt it as the canonical task. If multiple matches exist, the Coordinator decides which task to preserve and requires the authorized runtime executor to stop every duplicate before mutation; the executor returns those outcomes before work continues. Verify that no unique work is lost. Do not infer, inherit, carry forward, or persist an archival pause from another conversation, task, or earlier campaign direction. A launch failure leaves the portable provider record in Starting for Watchdog and Coordinator recovery.

Map Codex task states into portable evidence without inventing lifecycle. A running Codex process can support active-root-execution evidence. A running child can support delegated-work evidence. An idle, completed, failed, interrupted, or missing task requires portable reconciliation and cannot choose a provider transition by itself.

## Task Follow-Up

When the canonical task is idle but remains the selected resumable execution, the Coordinator may authorize the runtime executor to send one follow-up only to resume an authorized bounded next action or deliver a Coordinator decision. The Coordinator sends it directly only when its runtime exposes follow-up control; otherwise the authorized root runtime dispatcher sends the exact authorized message and returns the outcome. Never use follow-up for routine status, heartbeat, lifecycle history, capacity evidence, provider mutation, or proof of progress.

Do not create a replacement task merely because the task is idle, slow, or has not produced a recent message. After a follow-up, preserve the original task identity and reconcile the returned runtime state. If the task cannot resume, report that evidence to the portable lifecycle owner before any replacement decision.

## Watchdog Task Mapping

When coordinate-work-items permits a dedicated read-only Watchdog, create one Codex task under the Dev Backlog Watchdog Role. The standing prompt supplies the runtime parent task identifier, Coordinator task identifier, repository root, selected provider context, and applicable resource-coordination context. It instructs the Watchdog to apply coordinate-work-items for read-only criteria and this skill only for Codex runtime identity, title, follow-up, and archival observations.

### Canonical Standing Prompt Template

```text
Act as the dedicated read-only Dev Methodology backlog watchdog created by runtime parent task {runtime_parent_task_id} for Dev Backlog Coordinator task {coordinator_task_id} in {repository_root}.

Apply skills/coordinate-work-items/SKILL.md for portable capacity, lifecycle reconciliation, Blocked, Stalled, and read-only Watchdog criteria. Apply skills/coordinate-codex-tasks/SKILL.md only for Codex task identity, conversation-title observation, bounded resumption, and archival mapping. Observe task state through runtime tools. Consult provider, Git, and resource records only for a lifecycle decision, anomaly, dependency, delivery, or cleanup question; do not reconstruct lifecycle history on every cycle.

Remain strictly read-only. Do not mutate repository files, provider lifecycle, claims, tasks, branches, worktrees, or shared resources. Do not dispatch, integrate, clean up, archive, or run expensive or live verification. Notify Coordinator task {coordinator_task_id} only when a specific Coordinator decision is required. State the affected item, decision, and smallest recommended action without copying durable evidence into the message. When healthy, send nothing.
```

Substitute only the resolved runtime parent task identifier, Coordinator task identifier, and repository root. Supply provider and resource-coordination variation through resolved task context without rewriting the canonical prompt.

When a Watchdog schedule is configured, it must wake the canonical Watchdog task to run its own read-only observation cycle. Do not schedule the Coordinator to wake merely to send routine heartbeat or progress follow-ups to a worker or Watchdog task, and do not use a Watchdog wakeup to request progress from another task. The dispatcher observes worker runtime state through runtime tools. A Watchdog reports only a specific Coordinator decision it cannot make itself; otherwise it sends nothing.

If the Watchdog task is unavailable, the Dev Backlog Coordinator performs the portable review directly. Do not make the authorized root runtime dispatcher choose the review outcome and do not create a second ledger or duplicate observer.

## Task Archival

Task archival is mandatory by default after the applicable ordinary terminal gates pass. Completed requires merged delivery before default archival. Failed and Abandoned require valid terminal evidence and do not require or imply merged delivery. Every terminal status still requires a canonical task identity, terminal provider or task-local disposition, claim reconciliation, safe branch and worktree disposition, preservation acknowledgement, and no unresolved notification.

An archival pause is valid only when explicit current user direction names the exact Codex task, limits its scope to Codex task archival, records the exact direction and scope as evidence, and has a recorded acknowledgement. Do not infer, inherit, carry forward, or persist a campaign-wide pause from earlier conversation. A valid pause suppresses archival only for its named tasks. It never suppresses provider closeout, claim reconciliation, worktree cleanup, delivery-branch cleanup, source-branch cleanup, notification, or another terminal reconciliation action.

The Dev Orchestrator returns the complete terminal evidence and cleanup eligibility. It must not archive its active Codex task, remove its current worktree, or delete its checked-out branch.

Before cleanup authorization, the Dev Backlog Coordinator verifies the terminal conversation title, canonical task identity, terminal provider and delivery evidence, released claims, worktree cleanliness, branch-to-delivery equivalence, and preservation acknowledgement. If no valid current named-task pause exists, it authorizes archival after every ordinary gate passes. Only the authorized root Backlog Dispatcher executes terminal cleanup, even when the Coordinator runtime exposes the required task controls. It executes the exact authorized worktree, branch, and task operations, archives the task last, and returns every outcome to the Coordinator. The Coordinator reconciles capacity only after those outcomes return. If archival fails or no authorized runtime supports it, record the limitation and do not report archival success. An idle, stopped, titled, or archived Codex task proves none of those facts.

Task archival is a runtime cleanup mapping. It does not close a provider record, prove Commit delivery, release a claim, delete a worktree, or delete a branch.

## Task Message Contract

Workers send the dispatcher only one of these messages:

- a final outcome after the work-item task reaches its current terminal delivery result; or
- one specific Coordinator decision the worker cannot make itself.

Do not send routine progress receipts, heartbeat messages, repeated evidence summaries, title-only handoffs, or lifecycle-history reconstructions. Do not copy commit hashes, claim events, test history, deadlines, branches, worktrees, or other durable evidence into task messages. The dispatcher observes runtime state through runtime tools and consults the authoritative provider, Git, review, verification, or claim record only when a decision requires it.
