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
- Project guidance may load resource-claim. Its registry records active claims but does not prove review, verification, or delivery.
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

Count no more than ten actively eligible work items. Ten is a hard ceiling, not a scheduling target. Reconcile Starting and Running records against current runtime state before counting them and before reserving more work. In concurrent mode, dispatch eligible Ready work from available capacity and satisfied dependencies. In SOLO mode, run exactly one separate work-item task and keep the dispatcher free of implementation work.

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

The new root execution independently accepts the item. Its Dev Orchestrator directly applies the Persistence-selected management skill to record Starting -> Running with the canonical execution identity before implementation begins. The provider owns its resource protection, durable mutation, and cleanup.

Retain this evidence in the provider record:

```markdown
## Starting Handoff Evidence

Starting Recorded At: [UTC timestamp]
Coordinator: [parent execution identity]
Normalized Objective: [bounded objective]
Launch Result: [Not attempted, Requested, Started, Failed, or Unknown]
Canonical Execution: [runtime execution identity or None]
```

A failed or missing runtime launch, an execution that cannot accept the provider, or an execution that stops before Running leaves the provider in Starting. Do not automatically restore Ready. The dispatcher observes the runtime task through runtime tools and reconciles the item when the task fails, disappears, or requires a decision. The Watchdog never mutates the item or launches a replacement.

Starting consumes active capacity until the provider records Running or the Coordinator records another truthful lifecycle state. A runtime launch response does not replace either provider transaction.

### Running Eligibility

Running is actively eligible only while current runtime state proves at least one condition:

- active root execution: the canonical root execution is currently working on the item
- live delegated work: a child execution is currently completing a bounded assignment
- bounded runtime wait: the canonical task remains active while awaiting a runtime operation required by the current phase

The provider records the canonical execution and current phase when Running begins or materially changes. It does not require routine progress refreshes, heartbeat timestamps, deadlines, or reconciliation timestamps.

Running must leave active capacity when runtime observation shows that ownership ended or execution cannot continue. Restore Ready when ordinary redispatch is safe. Record Stalled when progress stopped for an unknown cause and preserved evidence needs diagnosis. Record Blocked for a known preventing cause, User Action Required for a genuine user-owned action, Awaiting Review for an accepted delivery that reached that provider state, or the applicable terminal outcome. The selected provider must record that truthful non-active state before replacement scheduling releases the capacity slot.

## Resource Coordination

When resource-claim is loaded, use its Claim Events table and supporting rules. Do not define claim behavior in this skill.

Acquire the exact opaque Work Item ID only when an applicable Claim Event requires it. Use activity work for outcome work and activity update for provider mutation. Release the work-item claim with disposition done, blocked, or handoff at the activity boundary. A handoff release must complete before the next owner acquires the same ID. Path and resource claims remain independently applicable. The provider remains the lifecycle authority.

At each mutation or integration event, supply the smallest currently known exact path or resource manifest to the selected coordination skill. Do not request a whole-project claim when a fixed subset is known. A broader request needs an evidence-backed reason and must be narrowed or released at the first safe boundary.

Before creating or transitioning work to User Action Required, apply resource-claim to the blocking condition when it is loaded. Confirm that a separate genuine user-owned decision remains. Structured claim outcomes and technical claim cleanup or recovery remain agent-owned and do not justify User Action Required.

## Work-Item Execution Record

For a selected Persistence provider, use its management skill to record phase-appropriate facts in its supported ownership, open-issues, and evidence fields. For provider none, retain them in the root execution result without creating a shadow record:

- canonical root execution identity and root Dev Orchestrator
- branch and worktree
- current phase
- Starting handoff and canonical Running execution identity while the lifecycle requires them
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
5. The root Dev Orchestrator accepts ownership and directly applies the effective Persistence-selected management skill to record Starting -> Running with its canonical execution identity before implementation.
6. Schedule only work that can begin implementation or another bounded delivery phase. Do not launch an execution merely to wait for approval, a dependency, a reviewer, a shared resource, or a delivery window.
7. When an item leaves Starting or Running, reconcile finish-lane work and the effective limit before reserving a replacement. Never refill a vacancy from count alone.

Stalled, Blocked, User Action Required, Holding, Awaiting Review, Completed, Failed, and Abandoned do not count toward ten. Future Ideas are not work-item states and enter coordination only after deliberate promotion creates a complete typed work item. A Starting or Running record without valid matching evidence also does not count and must be reconciled before replacement scheduling. Provider none does not synthesize a queue or capacity target from runtime state.

## New Work-Item Discovery

The Coordinator discovers new work through current provider inventory. Item creation sends no routine task message and does not reserve capacity or start delivery. Before dispatch, reconcile dependencies, capacity, lifecycle state, and any existing canonical execution from authoritative records.

## Effective Commit Delivery And Persistence Closure

Dev Orchestrator owns temporal delivery order. The selected Commit and Persistence skills own their respective procedures.

For main-branch integration, start from current main and designate this fresh branch as the Work-item integration and cleanup branch. Integrate only accepted commits or their exact accepted paths. Do not import cumulative branch ancestry merely to preserve provenance; record the source-to-integration mapping instead. Keep Git integration and terminal provider completion distinct. Cleanup is eligible only after the fresh Work-item integration branch is fully merged. A prior candidate branch used only as a non-ancestral content source is not the Work-item cleanup branch.

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
11. Send the parent only the final outcome or one specific Coordinator decision the Orchestrator cannot make. Keep provenance, review, verification, Commit, provider, claim, and cleanup evidence in their authoritative durable records.
12. The parent consults those records when needed, performs only cleanup proven safe by the terminal result, then obtains fresh provider inventory and schedules eligible replacement work.

Keep claim release, Commit delivery, and Persistence closure as distinct operations. One cannot substitute for another. If a provider update fails or is ambiguous, preserve the Commit handoff and reconcile the same Persistence transaction before resuming delivery.

### Candidate Recovery

Preserve candidate recovery evidence in the authoritative Git, review, verification, and provider records. Do not copy that history into task messages. After a mechanical or shared-resource unblock, reconcile the preserved candidate against current integration state once. Rerun only integration-sensitive checks and review required because combined bytes changed meaning.

### Review And Verification Availability

Assign one reviewer and one verifier with a finite response deadline. If either becomes unavailable or fails to return a terminal verdict, preserve partial evidence and replace the unavailable Agent once. If the replacement also fails, the parent Coordinator chooses one evidence-backed recovery disposition. Review availability failure is not a source finding.

## Verification

Follow the project's targeted-test policy. Map each acceptance criterion to the cheapest test that proves it. Select tests from changed behavior and actual dependency paths. Do not add a broad suite merely because several items were delivered together. Do not build a simulator when a real disposable repository, fixture, or focused assertion proves the boundary.

### Combined Regression Sets

Run focused tests, review, and verification for each item. Merge each accepted item independently. Do not delay an accepted merge for a later system-wide regression.

The Coordinator may group explicitly related items into one combined regression set. Record the selected items. After every selected item is present on main, run the system-wide regression once against the main commit that contains them all. Record that commit with the result.

If the combined regression finds a distinct defect, record it against the tested main commit and route it normally. Do not automatically invalidate focused evidence for unrelated work items.

## Long-Running Execution Control

Before starting a command or phase expected to take more than five minutes, Dev Orchestrator records locally:

- the exact active unit and later units not started
- expected duration or best evidence-based estimate
- a hard stop condition and retained evidence path
- the distinct acceptance criterion that requires the expensive operation

This is local operational control, not a progress message, provider transaction, or approval gate. The dispatcher observes runtime state through runtime tools.

After an expensive failure, classify the failure before repeating anything. Reuse retained output, add the smallest offline replay or deterministic regression, and make it pass before another equivalent expensive run. Stop a unit when it reaches its hard stop, repeats the same failure, or stops producing useful evidence. Preserve its work and follow resource-claim for any triggered claim. Two unproductive attempts require parent investigation and a revised plan.

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

1. Restore Running only when the same canonical owner resumes safely, runtime tools show active execution, durable records are consistent where needed, and capacity remains below the effective limit.
2. Restore Ready when ownership ended and normal redispatch is required.
3. Set Blocked when a concrete cause and Coordinator-owned next action are known.
4. Set User Action Required when a concrete user-owned action and exact question exist.
5. Record an applicable terminal disposition when matching evidence exists.

A retained Stalled owner must not resume repository or provider mutation until the Coordinator records Stalled -> Running.

When Dev Orchestrator recognizes a concrete blocker, it stops unsafe work, preserves durable evidence, obtains truthful resource disposition, and sends one decision request to the Coordinator containing only the affected Work Item ID, blocker, owner, unblock condition, requested Coordinator action, and whether resumption is safe. The Coordinator consults durable records when more evidence is needed.

## Blocked Reconciliation And Disposition

Reconcile a Blocked item when runtime or provider observation shows a changed unblock condition, missing disposition, or required Coordinator decision. Consult only the durable evidence needed for that decision. The Watchdog never chooses a lifecycle outcome.

### Mandatory Ordinary Blocked Recovery

Outside a declared backlog crisis, Dev Backlog Coordinator owns the complete recovery loop for every Blocked item. Blocked is an instruction to diagnose and act, not a storage destination.

1. Read current provider, canonical execution, candidate, worktree, review, verification, dependency, acceptance-criteria, Git, and resource-coordination evidence.
2. Reproduce or otherwise confirm the preventing condition. Correct stale, contradictory, over-scoped, or incomplete work-item content before changing implementation.
3. Complete bounded technical investigation and mechanical recovery. The Coordinator may directly correct other files already authorized by the original request and standing directives when those corrections are necessary to make the item runnable. Do not widen the requested outcome or governed-definition authority.
4. Reuse preserved candidates and accepted gates where their bytes and assumptions remain valid. Record the recovery decision in the provider; do not send or reconstruct a separate recovery-history receipt.
5. Use User Action Required only when bounded diagnosis isolates one concrete user-owned decision, authority grant, action, risk acceptance, or fact. Record one exact question and synchronize the canonical task to a Waiting for User title. Technical uncertainty or Coordinator inexperience is not user work.
6. When recovery makes dispatch safe, preserve the same canonical execution and record Blocked -> Ready, then Ready -> Starting as two serialized provider transitions. A direct Blocked -> Running transition is prohibited.
7. The preserved root Dev Orchestrator independently records Starting -> Running when capable of proceeding. If it still cannot proceed, it records a new Blocked handoff with the current exact cause, owner, evidence, and observable unblock condition.
8. The Coordinator remains responsible until the item has accepted Running, returned a new truthful Blocked handoff, entered User Action Required, or reached a justified terminal disposition.

Lifecycle-only churn, a replacement canonical task, an unchanged vague blocker, or another retry without a finding-linked recovery plan does not satisfy this procedure. Declared backlog-crisis recovery follows resolve-backlog-blockage instead of this ordinary restart loop.

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

The Watchdog observes runtime state first. It reads provider, Git, and applicable resource records only when a specific anomaly or Coordinator decision requires them. For provider none, it reads only task-local evidence. It evaluates:

- overdue Starting reconciliation
- provider Running without active runtime execution
- estimates, hard stops, and latest evidence-bearing progress
- suspected stalls and recorded Stalled exit conditions
- every Blocked item's blocker, unblock condition, owner, dependencies, candidate, review and verification, runtime and Git state, claims, attempts, and disposition
- accepted work stranded before Commit delivery
- READY Commit delivery awaiting provider closeout
- every terminal task associated with the observed Coordinator campaign
- terminal provider evidence, live and released claims, worktree disposition, delivery and cleanup branch disposition, source-branch disposition, unresolved notifications, and runtime archival state
- stale, unsafe, or unnecessarily broad claims when resource-claim is loaded

Reconcile a terminal task only when runtime observation indicates incomplete cleanup or another specific decision. Consult its durable provider, Git, claim, and archival records as needed; do not construct a repeated cycle history.

A source branch may remain deliberately preserved only when current evidence proves that it is non-ancestral or non-equivalent. Retain that evidence-backed disposition without another alert after the Coordinator acknowledges the same evidence and required action. Alert again when the evidence or required action changes. A preserved source branch never suppresses an independently authorized alert to remove its clean terminal worktree.

When a runtime mapping supports execution archival, an archival pause may suppress only archival for the exact named runtime executions validated by that mapping. It never suppresses provider closeout, claim reconciliation, worktree cleanup, delivery-branch cleanup, source-branch cleanup, notification, or another terminal action.

The Watchdog is read-only. It must not change repository files, provider records, lifecycle state, claims, runtime state, branches, worktrees, or shared resources. It must not schedule work, integrate changes, perform cleanup, or run expensive or live verification.

Notify the Coordinator only when a specific decision is required. Send the affected Work Item ID, reason, and smallest recommended action without copying durable evidence into the message. When no decision is required, send nothing. If the Watchdog is unavailable, the parent performs the review directly and does not create a replacement ledger.

## User Decisions And Terminal State

A user answer resolves a decision gate once; it does not prove delivery. Record the exact answer and provenance through the selected Persistence manager. Route approved work to Ready, deferred work to Holding, and declined work to the applicable terminal disposition. Provider none retains the answer in task-local evidence.

For approved work with an existing canonical execution:

1. Preserve the execution identity and existing evidence, then send one resumption request to the Coordinator.
2. For a selected provider, the Coordinator records User Action Required -> Ready and, when scheduling permits, Ready -> Starting for that same execution.
3. The same root Dev Orchestrator accepts Running and records Starting -> Running before repository mutation resumes.
4. The parent acknowledges reconciliation in the existing execution context. The user does not repeat the answer elsewhere.

Preserve out-of-sequence work as evidence. Reconcile provider state, claims, commits, review, verification, and delivery. Resume only after Running is durable and ordinary gates still pass.

Completed requires Commit READY, required independent review, focused verification, and terminal evidence through the effective Persistence-selected management skill when a provider exists. Provider none records equivalent evidence in the execution result. Runtime cleanup is eligible only after this terminal contract is satisfied.

## Task Communication

Workers communicate only a final outcome or one specific Coordinator decision they cannot make themselves. Routine progress, heartbeat, title-only, repeated evidence, and lifecycle-history messages are prohibited. Messages do not duplicate commit hashes, claim events, test history, deadlines, branches, worktrees, or other durable evidence. The dispatcher observes runtime status through runtime tools and consults provider, Git, review, verification, and claim records only when needed.
