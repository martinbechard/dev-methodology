---
name: coordinate-work-items
description: Coordinate multiple provider-selected work items through one parent backlog coordinator and one root Dev Orchestrator execution per Starting or Running item. Use when a sustained queue needs provider-neutral scheduling, reviewed delivery, lifecycle closure, and recovery.
metadata:
  category: development-practice
---

# Coordinate Work Items

Work-item coordination connects a durable provider queue to bounded delivery executions. One Dev Backlog Coordinator schedules the queue, and one root Dev Orchestrator owns each accepted item through review, verification, Commit delivery, Persistence closure, and terminal handoff.

## Authority And Roles

- The effective Persistence-selected provider record is the durable work-item authority when a provider is selected. Provider none has no durable provider record.
- Git records branches, commits, delivery, and cleanup eligibility; it is not a work-item provider.
- Project guidance may load agent-claim. Its registry records active claims but does not prove review, verification, or delivery.
- Runtime state is execution evidence, not lifecycle authority.
- Dev Backlog Coordinator owns provider-routed queue inventory, priority, scheduling, Stalled and Blocked lifecycle decisions, stalled-delivery investigation, and terminal cleanup coordination.
- Dev Orchestrator owns one work item after its root execution accepts Starting -> Running. It retains the item through delivery or a truthful terminal outcome.
- Dev Backlog Coordinator and Dev Orchestrator apply the effective Persistence-selected management skill directly for lifecycle operations they are authorized to own.
- Dev Backlog Steward is optional. It owns provider-wide inventory, normalization, archival audit, and recovery that benefits from an independent backlog context.
- Dev Orchestrator applies the effective Commit-selected skill only after candidate review and verification accept a direct or combined commit.
- Dev Backlog Watchdog owns scheduled read-only observation and actionable alerts. It never owns provider lifecycle, scheduling, delivery, recovery, claims, or cleanup.

Do not create a separate parent ledger, baton registry, waiting-execution registry, or runtime database. Do not copy this procedure into project guidance or a Dev Orchestrator definition.

## Governed Definition Work-Item Authorization

An explicit user-authorized work item that names exact skill definition paths is sufficient user direction to create or modify those named skill definitions. Do not ask for a second approval for those same named definitions.

Each named path still requires an auditable provenance record and the supported per-path pre-mutation check before mutation. Preserve the authorizing work-item identity, exact named scope, and user-direction provenance in that record. Proceed only when every named path returns ALLOWED_APPROVED_DEFINITION_CHANGE.

A definition outside the work item's exact named scope is additional work and requires new explicit user approval, its own auditable provenance, and its own successful per-path pre-mutation check. Never widen named scope through a directory, wildcard, artifact category, generated mirror, related definition, failing test, or general repository mutation authority. Other governed definition categories continue to follow applicable project authority.

## Active Execution And Capacity

This skill is the single normative authority for active-execution eligibility and active-capacity accounting. Persistence managers record provider mutations and caller-supplied evidence. They do not determine whether execution is active, inspect runtime state, or calculate capacity.

Count no more than ten actively eligible work items. Ten is a hard ceiling, not a scheduling target. A provider state contributes one active-capacity slot only while it satisfies the matching evidence contract below. Reconcile every Starting and Running record against current runtime evidence before counting it and before reserving more work.

### Adaptive Capacity And Finish-Lane Priority

Before scheduling, choose an effective limit at or below ten from current evidence:

- expected path and shared-resource independence
- available Coordinator, reviewer, verifier, and integration capacity
- the current execution and context budget
- finish-lane work that another launch would delay

Reduce the limit when active items are likely to contend for the same generated outputs, shared tests, primary integration lane, provider transaction, reviewer capacity, or runtime resource. Do not fill capacity from provider count alone.

Finish-lane work has priority over new Ready scheduling when it includes an accepted candidate awaiting integration, one bounded correction awaiting its final gate, delivered work awaiting terminal provider closure, or a satisfied mechanical recovery that can immediately resume delivery. Finish the oldest compatible item first. This priority does not stop independent private-worktree work, but it prevents a new launch from taking a resource needed to finish preserved work.

### Starting Handoff And Recovery Contract

Starting is the durable handoff between the parent Dev Backlog Coordinator and one new root Dev Orchestrator execution. The Coordinator selects one Ready item and directly applies the Persistence-selected management skill to record Ready -> Starting atomically. The selected provider resolves the Work Item ID, protects its required resources, commits or publishes the update, and releases its coordination resources. Only after that operation is durable does the Coordinator request runtime dispatch. The Coordinator's handoff ends after that request; it does not wait for or perform Starting -> Running.

The new root execution independently accepts the item. Its Dev Orchestrator directly applies the Persistence-selected management skill to record Starting -> Running with the canonical execution identity and Active Execution Evidence before implementation begins. The provider owns its resource protection, durable mutation, and cleanup.

Retain this evidence in the provider record:

```markdown
## Starting Handoff Evidence

Starting Recorded At: [UTC timestamp]
Coordinator: [parent execution identity]
Normalized Objective: [bounded objective]
Launch Result: [Not attempted, Requested, Started, Failed, or Unknown]
Canonical Execution: [runtime execution identity or None]
Last Contact At: [UTC timestamp or None]
Next Reconciliation At: [UTC timestamp no later than the next fifteen-minute parent review]
```

A failed or missing runtime launch, an execution that cannot claim the provider, or an execution that stops before Running leaves the provider in Starting. Do not automatically restore Ready. At or after Next Reconciliation At, the Watchdog reports the stale Starting item and its evidence to the Coordinator. The Coordinator may contact the same execution, stop it, request one replacement after duplicate reconciliation, or authorize a truthful provider transition. The Watchdog never mutates the item or launches a replacement.

Starting consumes active capacity until the provider records Running or the Coordinator records another truthful lifecycle state. A runtime launch response does not replace either provider transaction.

### Running Eligibility And Evidence

Running is actively eligible only while current evidence proves at least one condition:

- active root execution: the canonical root execution is currently working on the item
- live delegated work: a child execution is currently completing a bounded assignment
- bounded owned wait or progress condition: a named owner retains a necessary short wait or progress condition with a finite deadline, observable evidence, and a concrete next action

Every Running item retains exactly one current Active Execution Evidence section:

```markdown
## Active Execution Evidence

Condition Type: [root-execution, delegated-work, owned-wait, or progress-condition]
Owner: [responsible Agent or coordinator]
Evidence: [current runtime state, delegated assignment, retained output, or wait condition]
Observed At: [UTC timestamp]
Started At: [UTC timestamp]
Deadline or Expires At: [finite UTC timestamp]
Next Action: [concrete owned action]
Next Reconciliation At: [UTC timestamp]
```

Observed At and Started At are historical evidence timestamps. They do not expire the record. Validity is governed by two future boundaries: Deadline or Expires At and Next Reconciliation At. At evaluation time, both future boundaries must remain later than the current time. Evidence is invalid when current time is at or after either boundary. The owner must still own the condition, and the supporting state must remain true. Next Reconciliation At must be no later than the next fifteen-minute parent review. A review may refresh current observation evidence but must not extend the underlying condition automatically.

Running must leave active capacity when its evidence is absent, invalid, or expired. Restore Ready when ownership ended and ordinary redispatch is safe. Record Stalled when progress stopped for an unknown cause and preserved evidence needs diagnosis. Record Blocked for a known preventing cause, User Action Required for a genuine user-owned action, Awaiting Review for an accepted delivery that reached that provider state, or the applicable terminal outcome. The selected provider must record that truthful non-active state before replacement scheduling releases the capacity slot.

## Resource Coordination

When agent-claim is loaded, use its Claim Events table and supporting rules. Do not define claim behavior in this skill.

Acquire the exact opaque Work Item ID only when an applicable Claim Event requires it. Use activity work for outcome work and activity update for provider mutation. Release the work-item claim with disposition done, blocked, or handoff at the activity boundary. A handoff release must complete before the next owner acquires the same ID. Path and resource claims remain independently applicable. The provider remains the lifecycle authority.

At each mutation or integration event, supply the smallest currently known exact path or resource manifest to the selected coordination skill. Do not request a whole-project claim when a fixed subset is known. A broader request needs an evidence-backed reason and must be narrowed or released at the first safe boundary.

Before creating or transitioning work to User Action Required, apply agent-claim to the blocking condition when it is loaded. Confirm that a separate genuine user-owned decision remains. Structured claim outcomes and technical claim cleanup or recovery remain agent-owned and do not justify User Action Required.

## Work-Item Execution Record

For a selected Persistence provider, use its management skill to record phase-appropriate facts in its supported ownership, open-issues, and evidence fields. For provider none, retain them in the root execution result without creating a shadow record:

- canonical root execution identity and root Dev Orchestrator
- branch and worktree
- current phase
- Starting Handoff Evidence or Active Execution Evidence while the lifecycle requires it
- accepted candidate commit
- delivery-wait or provider-closure-wait start time
- applicable claim result, notification, blocking evidence, and owner
- open issues and the owner of each next action
- review, verification, Commit disposition, claim release, provider closure, and cleanup evidence as those events occur
- for Stalled, last productive evidence, estimate and hard stop when present, progress gap, canonical execution, current ownership, diagnostic owner, and next investigation action
- for Blocked, exact blocker, blocker owner, unblock condition, next-action owner, dependencies, preserved candidate, review and verification evidence, runtime state, Git state, applicable live claims, current disposition, and correction-attempt history

Use the effective Persistence-selected management skill when a material lifecycle state changes. Preserve the same canonical root execution and provider identity through corrections, delivery, and closeout. Runtime-specific skills may add runtime identity fields without changing provider authority.

## Queue Target And Scheduling

Obtain queue inventory, lifecycle counts, provider identities, and dispatchable state only by applying the effective Persistence-selected management skill.

- Provider file uses ordinary repository backlog identities through its selected file-provider manager. Do not scan or count Future Ideas unless the parent explicitly requests ideation or promotion.
- Provider github uses GitHub issue identities and provider lifecycle evidence. Do not create file backlog records.
- Provider gitlab uses GitLab issue identities and provider lifecycle evidence. Do not translate them into GitHub or file records.
- Provider azure-devops or jira applies the selected placeholder management skill, preserves its BLOCKED zero-mutation result, and does not fall back.
- Provider none has no durable inventory, count, creation, transition, or closure. Coordinate only the explicit execution and retain task-local evidence.
- Provider UNSET or an unavailable selected skill stops before durable inventory or mutation and requests the missing project selection or capability.

An unmet hard prerequisite makes the item dispatch-ineligible. A constraint is a hard prerequisite only when no bounded delivery phase can begin safely before it is satisfied. Treat a note that predicts later overlap on an exact path, shared resource, or integration lane as coordination-only. Canonical Status: Ready means the provider already resolved every hard prerequisite. If a Ready record still has an unmet hard dependency, reject dispatch and have the provider reconcile that invalid lifecycle to Blocked with an exact unblock condition. A coordination-only overlap note does not block a safe private-worktree start. Do not invent an effective lifecycle beside the provider record.

When a coordination-only note references a Blocked or Unowned item and no live claim protects the exact conflict, the candidate remains dispatch-eligible. Before scheduling, reconcile duplicate ownership or implementation evidence, preserve one canonical effort, and stop an additional launch. Coordinate an exact-path conflict at the relevant edit, shared-resource, or integration event. Defer only that event; continue non-conflicting work in isolated private worktrees.

For a provider that supports inventory and lifecycle transitions:

1. Reconcile every Starting or Running record against the active-execution contract. Record every required truthful non-active transition. Count only the remaining actively eligible items.
2. Determine the effective scheduling limit from current evidence. Select eligible Ready items only below that limit and only when a launch will not delay compatible finish-lane work.
3. For each selection, the parent Coordinator directly applies the effective Persistence-selected management skill to record Ready -> Starting, Starting Handoff Evidence, and scheduling evidence before requesting runtime dispatch.
4. Request at most one root Dev Orchestrator execution for the Starting item through the applicable runtime mapping. Reuse an existing canonical execution when a prior lifecycle pause preserved it.
5. The root Dev Orchestrator accepts ownership, produces valid Active Execution Evidence, and directly applies the effective Persistence-selected management skill to record Starting -> Running before implementation.
6. Schedule only work that can begin implementation or another bounded delivery phase. Do not launch an execution merely to wait for approval, a dependency, a reviewer, a shared resource, or a delivery window.
7. When an item leaves Starting or Running, reconcile finish-lane work and the effective limit before reserving a replacement. Never refill a vacancy from count alone.

Stalled, Blocked, User Action Required, Holding, Awaiting Review, Completed, Failed, and Abandoned do not count toward ten. Future Ideas are not work-item states and enter coordination only after deliberate promotion creates a complete typed work item. A Starting or Running record without valid matching evidence also does not count and must be reconciled before replacement scheduling. Provider none does not synthesize a queue or capacity target from runtime state.

## New Work-Item Notification

After a provider creates a new item successfully, it may send the opaque Work Item ID to the existing Coordinator through the available runtime message mechanism. On receipt, reread current provider inventory before deciding whether to reserve or dispatch anything. Reconcile dependencies, capacity, lifecycle state, and the existing canonical execution. The message is not lifecycle authority and does not reserve capacity or start delivery.

Repeated messages are harmless because each triggers fresh inventory reconciliation. A failed or duplicate no-op creation sends no message. When no Coordinator execution is available, the provider item remains discoverable during the next inventory read.

## Effective Commit Delivery And Persistence Closure

Dev Orchestrator owns temporal delivery order. The selected Commit and Persistence skills own their respective procedures.

For direct-main integration, start from current main and designate this fresh branch as the Work-item integration and cleanup branch. Integrate only accepted commits or their exact accepted paths. Do not import cumulative branch ancestry merely to preserve provenance; record the source-to-integration mapping instead. Keep Git integration and terminal provider completion distinct. Cleanup is eligible only after the fresh Work-item integration branch is fully merged. A prior candidate branch used only as a non-ancestral content source is not the Work-item cleanup branch.

1. Require Dev Coder to return a clean verified candidate commit without applying terminal Commit delivery or provider mutation.
2. Obtain fresh independent source review and source verification for every candidate. Return correctable findings to the original Dev Coder and repeat those gates on the replacement.
3. When multiple accepted candidates must be combined, use Dev Merge Coordinator, then obtain fresh post-combination review and complete verification. A single accepted candidate remains the direct commit.
4. Apply or resume the effective Commit-selected skill only after candidate review and source verification accept the direct or combined commit.
5. Preserve AWAITING_REVIEW with the same delivery identity while review, checks, dependency order, correction, merge, or final observation remains pending.
6. When Commit first returns AWAITING_REVIEW for a selected provider, Dev Orchestrator applies the effective Persistence-selected management skill exactly once to record the nonterminal lifecycle AWAITING_REVIEW. Include delivery identity, publication reference, accepted commit, completed checks, and pending gates.
7. On a repeated observation of the same delivery identity and Commit handoff, reconcile the existing update instead of repeating it. Never request lifecycle COMPLETED from an AWAITING_REVIEW handoff.
8. Resume the same effective Commit-selected skill until it returns READY or BLOCKED.
9. Only after the effective Commit-selected skill returns READY, Dev Orchestrator applies the effective Persistence-selected management skill exactly once for the distinct terminal lifecycle COMPLETED update. Reconcile an already successful terminal update instead of repeating it.
10. Provider file closure uses its file manager. GitHub and GitLab closure use their own provider identities. Placeholder providers preserve BLOCKED. Provider none records terminal evidence only in the task result.
11. Notify the parent with candidate provenance, review and verification, final Commit disposition, provider results when selected, claims, delivery identity, worktree, and cleanup eligibility.
12. The parent performs only cleanup proven safe by the terminal handoff, then obtains fresh provider inventory and schedules eligible replacement work.

Keep claim release, Commit delivery, and Persistence closure as distinct operations. One cannot substitute for another. If a provider update fails or is ambiguous, preserve the Commit handoff and reconcile the same Persistence transaction before resuming delivery.

### Candidate Recovery

Preserve a candidate recovery receipt with its immutable commit, exact changed paths, accepted findings, review result, verification result, and commands already passed. After a mechanical or shared-resource unblock, reconcile the preserved candidate against current integration state once. Rerun only integration-sensitive checks and review required because combined bytes changed meaning.

### Review And Verification Availability

Assign one reviewer and one verifier with a finite response deadline. If either becomes unavailable or fails to return a terminal verdict, preserve partial evidence and replace the unavailable Agent once. If the replacement also fails, the parent Coordinator chooses one evidence-backed recovery disposition. Review availability failure is not a source finding.

## Verification

Follow the project's targeted-test policy. Map each acceptance criterion to the cheapest test that proves it. Select tests from changed behavior and actual dependency paths. Do not add a broad suite merely because several items were delivered together. Do not build a simulator when a real disposable repository, fixture, or focused assertion proves the boundary.

### Combined Regression Sets

Run focused tests, review, and verification for each item. Merge each accepted item independently. Do not delay an accepted merge for a later system-wide regression.

The Coordinator may group explicitly related items into one combined regression set. Record the selected items. After every selected item is present on main, run the system-wide regression once against the main commit that contains them all. Record that commit with the result.

If the combined regression finds a distinct defect, record it against the tested main commit and route it normally. Do not automatically invalidate focused evidence for unrelated work items.

## Long-Running Execution Control

Before starting a command or phase expected to take more than five minutes, Dev Orchestrator exposes:

- the exact active unit and later units not started
- expected duration or best evidence-based estimate
- a hard stop condition and retained evidence path
- the distinct acceptance criterion that requires the expensive operation

This update is operational telemetry, not a provider transaction or approval gate. Observe long-running work at phase start, first failure, timeout, and completion. Distinguish active serial work from selected or queued work.

After an expensive failure, classify the failure before repeating anything. Reuse retained output, add the smallest offline replay or deterministic regression, and make it pass before another equivalent expensive run. Stop a unit when it reaches its hard stop, repeats the same failure, or stops producing useful evidence. Preserve its work and follow agent-claim for any triggered claim. Two unproductive attempts require parent investigation and a revised plan.

## Blocker Classification

Classify a preventing condition before selecting lifecycle or recovery:

- requested-outcome blocker: use Blocked with the concrete external or Coordinator-owned action, owner, and observable trigger
- genuine user decision: use User Action Required with one exact question
- mechanical or infrastructure recovery: keep claim cleanup, provider reconciliation, dirty checkout, configured-root routing, generator baseline, or runtime repair agent-owned
- review availability failure: preserve candidate evidence and apply the bounded replacement rule
- unrelated baseline failure: retain evidence without expanding current scope

Use Blocked only when the requested outcome cannot safely progress in the current bounded recovery and the record names cause, owner, and unblock condition.

## Stalled Investigation And Blocker Handoff

Stalled is a nonterminal provider state for an item that is not making progress while the causal blocker remains unknown. Quiet or slow work is not Stalled by itself. A source-backed progress gap, crossed estimate, hard stop, or other observed anomaly must support the classification.

A failed, stopped, or missing canonical execution requires immediate reconciliation. It leaves a Starting item in Starting until the Coordinator selects recovery, but it cannot preserve Running by itself. Dev Backlog Watchdog reports suspected Stalled evidence but never chooses or mutates the lifecycle result. Dev Backlog Coordinator decides and directly applies the selected manager.

The Coordinator chooses exactly one evidence-backed disposition:

1. Restore Running only when the same canonical owner resumes safely, supplies complete unexpired evidence, and capacity remains below the effective limit.
2. Restore Ready when ownership ended and normal redispatch is required.
3. Set Blocked when a concrete cause and Coordinator-owned next action are known.
4. Set User Action Required when a concrete user-owned action and exact question exist.
5. Record an applicable terminal disposition when matching evidence exists.

A retained Stalled owner must not resume repository or provider mutation until the Coordinator records Stalled -> Running.

When Dev Orchestrator recognizes a concrete blocker, it stops unsafe work, preserves commits and evidence, obtains truthful resource disposition, and immediately notifies the Coordinator. Include provider identity or provider-none execution, canonical execution identity, phase, blocker, owner, unblock condition, requested action, preserved evidence, resource disposition, and whether resumption is safe.

## Blocked Reconciliation And Disposition

On every Watchdog cycle, reconcile every Blocked item against its blocker, unblock condition, next-action owner, dependencies, candidate, review and verification, runtime state, Git state, live claims, and correction history. Retain one concise result for every Blocked item. The Watchdog never chooses a lifecycle outcome.

Alert the Coordinator when evidence shows a satisfied unblock condition, agent-actionable recovery, exhausted corrections without a disposition, malformed or inconsistent evidence, or an incorrect next-action owner. After exhausted corrections, the Coordinator records exactly one outcome:

1. A concrete recovery action, owner, evidence, and links to unresolved findings.
2. One fresh bounded retry plan linked to every unresolved finding.
3. A genuine user-owned decision with an exact question, options, tradeoffs, and unattended boundary.
4. Continuing Blocked with a concrete dependency, owner, and observable reconciliation trigger.

Reject a vague or indefinite outcome. Preserve execution identity, candidate, review, verification, Git, claim, and attempt history across resumption.

## Parent Review

Dev Backlog Coordinator obtains fresh inventory and reviews the queue when:

- an item enters or leaves Starting, Running, Stalled, or Blocked
- an execution stops, fails, times out, or reports a blocker
- a review, verification, Commit, or Persistence result arrives
- a user answers a recorded question
- a claim owner sends a release or recovery notification
- the Watchdog reports an actionable condition

During review, reconcile active capacity, eligible Ready work, Stalled and Blocked inventory, dependencies, accepted commits awaiting delivery, completed deliveries awaiting closeout, execution identity, and applicable claim results. Do not create a second registry.

## Dedicated Read-Only Watchdog

When the user requests background supervision for a sustained queue, the parent may assign one dedicated watchdog execution under the Dev Backlog Watchdog Role. The watchdog never performs scheduling or recovery. It observes and reports. It remains outside the provider queue and active capacity and is not a durable record or substitute Coordinator.

The Watchdog reads provider inventory, Git state, runtime evidence, and applicable resource coordination state. For provider none, it reads only task-local evidence. It evaluates:

- overdue Starting reconciliation
- absent or expired Running evidence
- estimates, hard stops, and latest evidence-bearing progress
- suspected stalls and recorded Stalled exit conditions
- every Blocked item's blocker, unblock condition, owner, dependencies, candidate, review and verification, runtime and Git state, claims, attempts, and disposition
- accepted work stranded before Commit delivery
- READY Commit delivery awaiting provider closeout
- terminal work awaiting cleanup
- stale, unsafe, or unnecessarily broad claims when agent-claim is loaded

The Watchdog is read-only. It must not change repository files, provider records, lifecycle state, claims, runtime state, branches, worktrees, or shared resources. It must not schedule work, integrate changes, perform cleanup, or run expensive or live verification.

Notify the coordinator only when action is required. Identify the affected provider identity or provider-none execution, observed evidence, reason attention is required, and smallest recommended action. Treat quiet work as healthy only while its current evidence remains valid. When no intervention is needed, emit one concise no-action cycle result without messaging the parent. If the Watchdog is unavailable, the parent performs the review directly and does not create a replacement ledger.

## User Decisions And Terminal State

A user answer resolves a decision gate once; it does not prove delivery. Record the exact answer and provenance through the selected Persistence manager. Route approved work to Ready, deferred work to Holding, and declined work to the applicable terminal disposition. Provider none retains the answer in task-local evidence.

For approved work with an existing canonical execution:

1. Preserve the execution identity and existing evidence, then send one resumption request to the Coordinator.
2. For a selected provider, the Coordinator records User Action Required -> Ready and, when scheduling permits, Ready -> Starting for that same execution.
3. The same root Dev Orchestrator accepts Running and records Starting -> Running before repository mutation resumes.
4. The parent acknowledges reconciliation in the existing execution context. The user does not repeat the answer elsewhere.

Preserve out-of-sequence work as evidence. Reconcile provider state, claims, commits, review, verification, and delivery. Resume only after Running is durable and ordinary gates still pass.

Completed requires Commit READY, required independent review, focused verification, and terminal evidence through the effective Persistence-selected management skill when a provider exists. Provider none records equivalent evidence in the execution result. Runtime cleanup is eligible only after this terminal contract is satisfied.

## Reporting

For each considered item, report canonical lifecycle state, any invalid Ready dependency, unmet hard blocker, coordination-only overlap, and deferred edit, resource, or integration event as distinct facts. Do not invent an effective lifecycle beside the provider record.

Also return provider identity, owner and canonical execution, dependency and claim evidence, current phase, branch and worktree, accepted commit, review and verification results, Commit and Persistence dispositions, cleanup eligibility, and next safe action.
