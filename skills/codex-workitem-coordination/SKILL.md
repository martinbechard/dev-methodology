---
name: codex-workitem-coordination
description: Coordinate multiple provider-selected work items through one parent backlog coordinator and one Dev Orchestrator Thread per Starting or Running item. Use when Codex must sustain a queue, deliver reviewed work, close completed items, and recover stalled delivery without a separate task registry.
metadata:
  category: development-practice
---

# Codex Work-Item Coordination

Use one Dev Backlog Coordinator as the parent dispatcher. Reserve each selected work item as Starting, then give its one user-visible work-item conversation to a root Dev Orchestrator Agent that owns candidate production, independent review, verification, effective Commit delivery, Persistence closure, and terminal handoff after Starting -> Running acceptance.

## Authority And Roles

- The effective Persistence-selected provider record is the durable work-item authority when a provider is selected. Provider none has no durable provider record.
- Git records branches, commits, delivery, and cleanup eligibility; it is not a work-item provider.
- PROJECT.yaml may load agent-claim. Its registry records active claims but does not prove review, verification, or delivery.
- Runtime conversation state and the conversation title are display and execution state, not lifecycle authority.
- Dev Backlog Coordinator owns provider-routed queue inventory, priority, dispatch, Stalled
  and Blocked lifecycle decisions, stalled-delivery investigation, and terminal Thread cleanup.
- Dev Orchestrator owns one work item after its root Agent accepts Starting -> Running through delivery or a truthful terminal outcome. It may assign bounded Tasks to Dev Coder, independent reviewer, and verifier child Agents inside that Thread.
- Dev Backlog Steward applies the effective Persistence-selected management skill for provider inventory and lifecycle mutation. Dev Orchestrator applies the effective Commit-selected skill only after candidate review and verification accept a direct or combined commit.
- Dev Backlog Watchdog owns scheduled read-only observation and actionable alerts. It never
  owns provider lifecycle, dispatch, delivery, recovery, claims, or cleanup.

Do not create a separate parent ledger, baton registry, waiting-Task registry, or conversation database. Do not copy this procedure into AGENTS.md or a Dev Orchestrator definition.

## Governed Definition Work-Item Authorization

An explicit user-authorized work item that names exact skill definition paths is sufficient
user direction to create or modify those named skill definitions. Do not ask for a second
approval for those same named skill definitions.

Each named path still requires an auditable provenance record and the supported per-path
pre-mutation check before mutation. Preserve the authorizing work-item identity, exact named
scope, and user-direction provenance in that record. Proceed only when every named path
returns ALLOWED_APPROVED_DEFINITION_CHANGE.

A skill definition outside the work item's exact named scope is additional work and requires
new explicit user approval, its own auditable provenance, and its own successful per-path
pre-mutation check. Never widen named scope through a directory, wildcard, artifact category,
generated mirror, related skill, failing test, or general repository mutation authority.
Other governed definition categories continue to follow applicable project authority.

## Active Execution, Capacity, And Conversation Titles

This skill is the single normative authority for Codex active-execution eligibility,
active-capacity accounting, runtime and conversation reconciliation, and portable
conversation-title synchronization. Persistence managers record provider mutations and
evidence supplied by their callers. They do not determine whether execution is active,
inspect runtime state, calculate capacity, or rename conversations.

Count no more than ten actively eligible work items. Ten is a hard ceiling, not a dispatch
target. A provider state contributes one active-capacity slot only while it satisfies the
matching evidence contract below. Reconcile every Starting and Running record against
current runtime evidence before counting it and before reserving more work. A conversation
title never creates active eligibility.

### Adaptive Capacity And Finish-Lane Priority

Before dispatch, choose an effective dispatch limit at or below ten from current evidence:

- expected path and shared-resource independence
- available Coordinator, reviewer, verifier, and integration capacity
- the current execution and context budget
- finish-lane work that would be delayed by another launch

Reduce the limit when active items are likely to contend for the same generated outputs,
shared tests, primary integration lane, provider transaction, reviewer capacity, or runtime
resource. Do not fill capacity from provider count alone.

Finish-lane work has priority over new Ready dispatch when it includes an accepted candidate
awaiting integration, one bounded correction awaiting its final gate, delivered work awaiting
terminal provider closure, or a satisfied mechanical recovery that can immediately resume
delivery. Finish the oldest compatible item first. This priority does not stop independent
private-worktree work, but it prevents a new launch from taking a resource needed to finish
preserved work.

### Starting Settlement Contract

Starting is one live launch handshake. Its settlement window is exactly 60 seconds. The
window begins when the Ready -> Starting provider mutation succeeds and ends when the root
Dev Orchestrator accepts ownership, the launch is truthfully dispositioned, or the Starting
settlement deadline expires. A Thread-creation error, timeout, disconnect, ambiguous
response, stopped launch, missing launch, or immediate post-launch read without an accepted
owner triggers reconciliation within that same window. Never retry conversation creation.

Retain one evolving Starting Settlement Evidence record in the provider's supported evidence
fields, or task-locally for provider none. At reservation time, initialize the evolving record
truthfully before any runtime launch has been attempted:

```markdown
## Starting Settlement Evidence

Reservation Started At: [UTC timestamp]
Settlement Deadline: [UTC timestamp exactly 60 seconds later]
Runtime Launch Result: Not attempted
Canonical Conversation: None
Owner Acceptance: None
Reconciliation Result: Pending
Last Updated At: [UTC timestamp]
```

After each launch observation, update Runtime Launch Result, Canonical Conversation, Owner
Acceptance, and Last Updated At with only observed facts. Reconciliation Result remains
Pending while the handshake is live. Pending is valid only before Settlement Deadline and
must be final at or before Settlement Deadline.

A final Running result is invalid unless Runtime Launch Result records an observed successful
launch, Canonical Conversation records the observed stable identity, Owner Acceptance records
the accepting root owner and acceptance time, and valid Running eligibility evidence is
present. When all four conditions are true within the window, atomically record Starting ->
Running with Reconciliation Result: Running.

Every settlement that does not validly finalize Running must first atomically restore Starting
-> Ready with Reconciliation Result: Ready. Every non-Running Starting settlement result is
Ready, including an error, timeout, disconnect, ambiguous response, missing accepted owner,
stopped or missing launch, or deadline expiry. Never select Stalled, Blocked, User Action
Required, Completed, Failed, or Abandoned as the Starting settlement result. Preserve launch
and diagnostic evidence. Any proved later Stalled, Blocked, User Action Required, Completed,
Failed, or Abandoned disposition occurs only in a distinct subsequent provider transaction
from Ready under its normal authority.

Starting must leave active capacity when its 60-second settlement deadline expires. Release
the capacity slot after the selected provider records Ready, and fill the vacancy from fresh
inventory.

### Running Eligibility And Evidence

Running is actively eligible only while current evidence proves at least one of these
conditions:

- active root execution: the canonical root Agent is currently executing the work item
- live delegated work: a child Agent is currently executing a bounded assignment for the item
- bounded owned wait or progress condition: a named owner retains a necessary short wait or
  progress condition with a finite deadline, observable evidence, and a concrete next action

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

Observed At and Started At are historical evidence timestamps; they do not expire the record.
Validity is governed by two future boundaries: Deadline or Expires At and Next Reconciliation
At. At evaluation time, both future boundaries must remain later than the current time.
Evidence is invalid when current time is at or after Deadline or Expires At, or when current
time is at or after Next Reconciliation At. The owner must also still own the condition and
the supporting state must remain true. Next Reconciliation At must be no later than the next
fifteen-minute parent review. A review may refresh current observation evidence but must not
extend the underlying condition automatically. Quiet work may remain Running only when this
complete unexpired evidence proves one of the three eligible conditions.

Running must leave active capacity when its Active Execution Evidence is absent, invalid, or
expired. Restore Ready when ownership ended and ordinary redispatch is safe. Record Stalled
when progress stopped for an unknown cause and preserved evidence needs diagnosis. Record
Blocked for a known preventing cause, User Action Required for a genuine user-owned action,
Awaiting Review for an accepted delivery that has reached that provider state, or the
applicable terminal outcome. The selected provider must record that truthful non-active
state before replacement dispatch releases the capacity slot.

### Conversation Title Contract

The canonical conversation keeps one stable identity. Its conversation title is display
state, never lifecycle authority, active-execution evidence, or delivery evidence. Use the
portable format phase label — short work-item title. A runtime adapter may map conversation
title to its platform-specific UI label.

Use this lifecycle and phase mapping:

- Ready: Ready — short work-item title.
- Starting: Starting — short work-item title.
- Running: Implementing —, Reviewing —, Verifying —, Integrating —, Waiting for Claim —,
  or Waiting for Help — short work-item title, matching the current eligible phase.
- User Action Required: Waiting for User — short work-item title.
- Stalled: Stalled — short work-item title.
- Blocked: Blocked — short work-item title.
- Holding: Holding — short work-item title.
- Awaiting Review: Awaiting Review — short work-item title.
- Completed: Done — short work-item title.
- Failed: Failed — short work-item title.
- Abandoned: Abandoned — short work-item title.

Dev Backlog Steward is accountable after every successful lifecycle transition. When the
runtime grants rename authority, it must directly rename the canonical conversation. When
it lacks that authority, it must send the exact required conversation title to the canonical
conversation owner or runtime coordinator and verify that handoff before reporting transition
coordination complete. Verification is a successful direct rename observation or an explicit
acknowledgement that names the stable conversation identity and exact requested title. A
failed title update does not roll back a durable lifecycle transition or change capacity;
preserve the successful provider mutation, report transition coordination incomplete, and
route title reconciliation to the canonical conversation owner.

## Resource Coordination

When agent-claim is loaded, use its Claim Events table and supporting rules. Do not define claim behavior in this skill.

At each mutation or integration event, supply the smallest currently known exact path or
resource manifest to the selected coordination skill. Do not request a whole-project claim
when a fixed subset is known. A broader request needs an evidence-backed reason that the
required paths cannot yet be bounded, and it must be narrowed or released at the first safe
boundary.

Before creating or transitioning work to User Action Required, apply agent-claim to the blocking condition and confirm that a separate genuine user-owned decision remains. Structured claim outcomes and technical claim cleanup or recovery remain agent-owned and do not justify User Action Required.

## Work-Item Execution Record

For a selected Persistence provider, use its management skill to record these phase-appropriate facts in the provider's supported ownership, open-issues, and evidence fields. For provider none, retain them in the canonical conversation result without creating a shadow record:

- canonical work-item conversation identifier, root Dev Orchestrator Agent, and canonical Task identifier for that root assignment when the runtime supplies one
- branch and worktree
- current phase
- Starting Settlement Evidence or Active Execution Evidence while the lifecycle requires it
- exact required conversation title and verified direct rename or handoff evidence
- accepted candidate commit
- delivery-wait or provider-closure-wait start time
- applicable claim result, notification, blocking evidence, and owner
- open issues and the owner of each next action
- review, verification, Commit disposition, claim release, provider closure, and cleanup evidence as those events occur
- for Stalled, last productive evidence, phase estimate and hard stop when present, anomaly
  or progress gap, canonical conversation and root Agent Task identities, current ownership and
  coordination state, diagnostic owner, and next investigation action
- for Blocked, exact blocker, blocker owner, unblock condition, next-action owner,
  dependencies and their current evidence, preserved candidate, review and verification
  evidence, canonical task state, Git state, applicable live claims, current disposition,
  and correction-attempt history

Use the effective Persistence-selected management skill to update a provider record when a material lifecycle state changes. Preserve the same canonical conversation identifier, root Agent assignment, and provider identity through corrections, delivery, and closeout. Never infer identity from the conversation title alone.

## Queue Target And Dispatch

Obtain queue inventory, lifecycle counts, provider identities, and dispatchable state only by applying the effective Persistence-selected management skill.

- Provider file: treat ordinary repository backlog paths as provider identities and use the selected file-provider skill for creation and mutation. Do not scan or count backlog/future-ideas unless the parent explicitly requests ideation or promotion.
- Provider github: use GitHub issue identities and provider lifecycle evidence; do not create or inspect file backlog paths.
- Provider gitlab: use GitLab issue identities and provider lifecycle evidence; do not translate them into GitHub or file records.
- Provider azure-devops or jira: apply the selected placeholder management skill, preserve its BLOCKED zero-mutation result, and do not fall back.
- Provider none: do not inventory, count, create, transition, or close durable provider records; coordinate only the explicit task and retain task-local evidence.
- Provider UNSET or an unavailable selected skill: stop before durable inventory or mutation and request the missing project selection or capability.

Classify a candidate constraint as a hard prerequisite only when no bounded delivery phase can begin safely before it is satisfied. Treat a note that only predicts later overlap on an exact path, shared resource, or integration lane as coordination-only. An unmet hard prerequisite makes the item dispatch-ineligible. A coordination-only overlap note does not block a safe private-worktree start.

When a coordination-only note references a Blocked or Unowned item and no live claim protects the relevant exact conflict, the candidate remains dispatch-eligible; the referenced lifecycle and ownership state do not create a hard prerequisite.

Before dispatch, reconcile duplicate ownership or implementation evidence, preserve one canonical effort, and stop an additional duplicate launch. Coordinate an exact-path conflict at the relevant edit, shared-resource, or integration event named by the selected coordination procedure. Defer only that event; continue non-conflicting work in isolated private worktrees. A live exact conflict may defer only its relevant event; it does not defer unrelated private-worktree work.

For a provider that supports queue inventory and lifecycle transitions:

1. Reconcile every provider record in Starting or Running against the active-execution
   evidence contract, record every required truthful non-active transition, then count only
   the remaining actively eligible Starting or Running items.
2. Determine the effective dispatch limit from Adaptive Capacity And Finish-Lane Priority.
   Select eligible Ready items only while the active count is below that limit and no selected
   launch would delay compatible finish-lane work.
3. For each selection, have the parent Coordinator's Dev Backlog Steward child atomically
   record the Ready -> Starting reservation, Starting Settlement Evidence, and dispatch
   evidence through the effective Persistence-selected management skill before creating a
   runtime conversation.
4. Reconcile the reservation and existing runtime evidence, then create at most one
   user-visible work-item conversation for the Starting work item. When the item already has
   one canonical conversation preserved from a prior Running to User Action Required
   transition, adopt that same conversation instead of creating a replacement.
5. After the conversation's root Dev Orchestrator Agent accepts ownership and produces valid
   Active Execution Evidence, have that Orchestrator's Dev Backlog Steward child atomically
   record Starting -> Running with the canonical conversation identifier, root Agent Task
   identifier when applicable, branch, worktree, and applicable claim evidence.
6. Dispatch only work that can begin implementation or another bounded delivery phase. Do
   not create a conversation merely to wait for approval, a dependency, a reviewer, a shared
   resource, or a delivery window.
7. When an item leaves Starting or Running, reconcile finish-lane work and the effective
   dispatch limit before reserving a replacement. Never refill a vacancy from count alone.

Stalled, Blocked, User Action Required, Holding, Awaiting Review, Completed, Failed,
Abandoned, and Future Ideas do not count toward ten. A Starting or Running record without
valid matching active-execution evidence also does not count and must be reconciled to a
truthful non-active state before replacement dispatch. Future Ideas are not work-item states
and enter coordination only after deliberate promotion creates a complete typed work item.
If fewer than ten eligible items exist, activate all eligible items and report the shortage
instead of manufacturing placeholder work. Provider none does not synthesize a queue or a
target of ten from conversation state.

List or validate backlog/future-ideas only when the parent request explicitly includes ideation or promotion and file Persistence applies to that operation. A revisit trigger is free text and never schedules a conversation, fills capacity, or authorizes unattended work.

## New Work-Item Notification

After a provider creates a new work item successfully, it may send the provider reference to the existing Coordinator task through the runtime's normal task-message feature.

On receipt, reread current provider inventory before deciding whether to reserve or dispatch anything. Reconcile dependencies, capacity, lifecycle state, and existing canonical tasks. The message is not lifecycle authority and does not itself reserve capacity, create a delivery task, or start implementation.

Repeated messages are harmless because each message triggers the same fresh inventory reconciliation. A failed or duplicate no-op creation sends no message. When no Coordinator task is available, the committed provider item remains discoverable during the next Coordinator start.

## Dispatch Reconciliation

Treat a conversation-creation error, timeout, disconnect, or ambiguous response as an ambiguous mutation. Do not retry creation.

Reconcile active and archived conversations using all available identity evidence:

- source parent conversation identifier
- canonical provider identity and provider reference when one exists
- normalized objective
- creation time
- conversation status

If exactly one match exists, adopt it as the canonical work-item conversation. If multiple
matches exist, preserve one canonical conversation, stop every duplicate before mutation,
verify no unique work is lost, and archive the duplicates when supported. Reconcile again
before the Starting settlement deadline. At or before the deadline, record Running only for
an observed successful launch, stable canonical conversation, accepted owner, and valid
Running eligibility evidence. Otherwise finalize the evolving settlement as Ready and
atomically restore Starting -> Ready first. Any later disposition uses a distinct provider
transaction from Ready. Never retain Starting or Pending beyond the deadline, and never retry
conversation creation after an ambiguous response.

## Conversation Execution Compatibility

Create each Dev Orchestrator work-item conversation in an environment where its root Agent can perform ordinary repository work without asking the user to approve Git, shell, test, process-inspection, or selected resource-coordination commands. The dispatch prompt must state that these ordinary operations are already authorized by the work item and that the Agent must not open or wait on a user approval prompt for them.

- When agent-claim is loaded, use the claim helper configured in PROJECT.yaml.
- Keep implementation and focused tests in the work-item conversation's private worktree. The environment must permit ordinary writes to that worktree and the Git worktree metadata needed for local commits.
- When a work item depends on a special runtime capability, test that capability through the same nested execution path the real workload uses before assigning more equivalent work to that environment. A direct command is not sufficient evidence for a runner that invokes the command from a child process.
- Treat prior runtime-capability evidence as stale after any agent-definition or metadata generation, adapter installation, MCP refresh, Codex configuration change, permission-profile change, application update, or host restart. Before dispatching real work again, run one disposable worktree pilot through the effective child Agent runtime.
- The post-change pilot must prove the effective Agent profile and ordinary operations, not merely read the requested configuration or repeat permission wording in its prompt. Inspect the child Agent's effective approval, sandbox, and permission profile; create a harmless Git commit; invoke every selected special capability through the same nested helper used by the real workload; and, only when agent-claim with MCP is selected, read its registry through MCP.
- If the requested configuration and effective child runtime differ, or any representative operation fails, stop equivalent dispatch immediately. Record the exact requested and effective profiles, archive the failed pilot conversation, correct or replace the launch environment, and rerun the pilot. Do not treat a successful direct command, parent capability, config file, or earlier conversation as evidence for the failing child runtime.
- If an ordinary required operation fails because the Agent environment lacks a capability, the Agent stops immediately, preserves its work, and reports the exact failed operation to the parent. It must not request escalation from the user.
- The parent promptly re-homes the conversation or replaces its root Agent in a compatible
  environment, asks Dev Backlog Steward to update canonical identifiers through the selected
  Persistence manager, and reconciles active eligibility before filling any resulting
  vacancy. For provider none it updates only the task-local identity. Do not leave an
  approval prompt or an execution-incompatible Agent consuming active capacity.

Apply the Conversation Title Contract when the conversation is created, after every
lifecycle transition, and at each material Running phase change. Never use raw prompt text,
XML or delegation tags, error output, identifiers, or generic titles as the conversation
title.

## Starting And Work-Item Conversation Ownership

A work item is the durable provider record for an outcome, lifecycle, evidence, and
ownership. A conversation is one retained execution context. An Agent is a runtime instance
operating under a Role, which is a reusable responsibility and authority contract. A Task is
a bounded assignment to an Agent; it is never a synonym for conversation. A Handoff is a
lifecycle event that transfers evidence and the next action.

The parent coordination conversation has one root Agent under the Dev Backlog Coordinator
Role. Each actively eligible Starting or Running work item has exactly one work-item
conversation with one root Agent under the Dev Orchestrator Role. Producing, implementation,
independent review, verification, delivery, and stewardship Agents are children in that
work-item conversation.

Ready -> Starting is the parent Coordinator's dispatch and capacity-reservation decision.
Use its Dev Backlog Steward child to record the reservation through the selected manager
before launch. Count Starting only during the valid 60-second settlement window. Reconcile
existing reservation and runtime evidence before every launch. One work item must not create
a duplicate conversation after a timeout, conversation-creation error, or ambiguous startup.

When a Running work item pauses in User Action Required, preserve its canonical work-item
conversation, root Agent Task identity, branch, worktree, clean commits, and unresolved
question as non-owning resumption evidence. The user may answer and continue in that
canonical conversation. The parent must reuse it after the answer is durably routed through
Ready -> Starting; it must not require the user to repeat the answer in the parent
conversation or create a replacement work-item conversation.

After the work-item conversation's root Dev Orchestrator Agent accepts ownership and records
valid Active Execution Evidence, it uses its Dev Backlog Steward child for the atomic
Starting -> Running transition. The record includes the canonical conversation identifier,
canonical root Agent Task id when applicable, branch, worktree, applicable claim evidence,
and Active Execution Evidence. If launch fails or remains ambiguous, apply the Starting
Settlement Contract. A runtime anomaly cannot preserve active capacity without valid matching
evidence.

The work-item Orchestrator owns candidate production, review, verification, Commit delivery,
and terminal Persistence request. Its Steward child records the selected provider lifecycle
changes and verifies conversation-title synchronization. The parent Coordinator never
performs per-item delivery or completion; after the terminal Handoff it cleans the runtime
conversation and worktree, reconciles active capacity, and dispatches replacement work.

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
12. The parent removes only clean eligible worktrees and branches, verifies terminal
    conversation-title synchronization, archives terminal conversation UI state when
    supported, then obtains fresh provider inventory and fills eligible capacity through the
    selected management skill.

Keep claim release, Commit delivery, and Persistence closure as distinct operations. One cannot substitute for another. Dev Orchestrator applies the selected Commit skill because it owns the accepted commit, review, verification, and resumption context.

If the nonterminal AWAITING_REVIEW update fails or its result is ambiguous, preserve the Commit handoff and reconcile that same Persistence transaction before resuming delivery. Do not request terminal COMPLETED, repeat an already successful nonterminal update, or reinterpret the Commit disposition as terminal.

### Candidate Recovery

Preserve a candidate recovery receipt with its immutable commit, exact changed paths,
accepted findings, review result, verification result, and commands already passed. After a
mechanical or shared-resource unblock, reconcile the preserved candidate against current main
once. Re-run only integration-sensitive checks and any review needed because combined bytes
changed meaning. Do not repeat unchanged source review or verification merely because time,
lifecycle, a claim wait, or provider reconciliation passed.

### Review And Verification Availability

Assign one reviewer and one verifier with a finite response deadline. If either Agent becomes
unavailable or fails to return a terminal verdict, preserve its partial evidence and replace
the unavailable Agent once. If the replacement also fails to return a terminal verdict, the
parent Coordinator must choose one evidence-backed recovery disposition and must not launch
another replacement loop. Review availability failure is not a source finding and does not
invalidate a preserved candidate by itself.

## Verification

Follow the project's targeted-test policy. Before running commands, map each acceptance
criterion to the cheapest test that can prove it and record the distinct criterion for every
expensive or repeated check. Select tests from the changed behavior and its actual dependency
paths. Do not add a broad suite merely because several work items were delivered together.
Do not build a Git, claim, runtime, or provider simulator when a real disposable repository,
fixture, or focused contract assertion proves the boundary. A simulator is justified only
when the requested outcome is the simulator or the real boundary cannot be exercised safely,
and that reason must be explicit.

## Combined Regression Sets

Run focused tests, review, and verification for each work item. Merge each accepted item independently. Do not delay an accepted merge for a later system-wide regression.

The Dev Backlog Coordinator may group explicitly related work items into one combined regression set. Record the selected work items. After every selected item is present on main, run the system-wide regression once against the main commit that contains them all. Record that commit with the result.

If the combined regression finds a distinct defect, record the defect against the tested main commit and route it normally. Do not automatically invalidate focused evidence for unrelated work items.

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

## Blocker Classification

Classify a preventing condition before selecting lifecycle or recovery:

- requested-outcome blocker: the requested behavior cannot progress without a concrete
  external or Coordinator-owned action; use Blocked with that owner and observable trigger
- genuine user decision: execution discovered an unresolved choice that belongs to the user;
  use User Action Required with one exact question
- mechanical or infrastructure recovery: claim cleanup, provider reconciliation, dirty
  checkout, configured-root routing, generator baseline, or runtime repair that an Agent can
  perform; keep it agent-owned and run one bounded recovery instead of treating the mechanism
  as the requested outcome
- review availability failure: preserve candidate evidence and apply the bounded replacement
  rule rather than manufacturing a source defect
- unrelated baseline failure: retain evidence, but do not expand scope or keep an otherwise
  accepted item open solely to repair it

Use Blocked only when the requested outcome cannot safely progress in the current bounded
recovery and the record names the preventing cause, owner, and observable unblock condition.

## Stalled Investigation And Blocker Handoff

Stalled is a nonterminal provider lifecycle state for evidence that an item is not making
progress while the causal blocker or unblock condition remains unknown. Quiet or apparently
slow work is not Stalled by itself. A source-backed progress gap, crossed estimate or hard
stop, or other observed progress anomaly must support the classification.

A failed, stopped, or missing canonical Task is runtime evidence that requires immediate
active-eligibility reconciliation. It cannot preserve Starting or Running by itself. Apply
the Starting Settlement Contract or Running Eligibility And Evidence contract, retain
recovery evidence, and record the resulting truthful non-active state when active evidence
is absent or expired.

The Dev Backlog Watchdog reports suspected Stalled evidence but never chooses or mutates
the lifecycle result. Dev Backlog Coordinator decides whether the evidence justifies
Stalled and asks Dev Backlog Steward to perform the atomic provider mutation. Preserve:

- last known productive evidence
- phase estimate and hard stop when present
- the anomaly or evidence-progress gap
- canonical conversation and root Agent Task identities
- current ownership and coordination state
- diagnostic owner
- next investigation action

Stalled leaves active capacity immediately after the selected provider records the
transition. Fill the vacancy from fresh provider inventory when eligible Ready work exists.
The canonical conversation, root Agent Task, branch, worktree, commits, and ownership
evidence remain recovery context rather than active-execution authority.

Dev Backlog Coordinator chooses exactly one evidence-backed disposition:

1. Restore Running only when the same canonical owner demonstrably resumes safely, supplies
   complete unexpired Active Execution Evidence, and the current active count is below ten.
   Reconcile the count before the serialized provider transaction, reject the transition and
   preserve Stalled when no slot is available, and otherwise record the renewed evidence
   without exceeding capacity.
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

### Blocked Reconciliation And Disposition

On every Watchdog cycle, reconcile every Blocked item against its exact blocker, unblock
condition, next-action owner, dependencies, candidate, review and verification evidence,
canonical task state, Git state, and applicable live claims. Retain one concise per-item
reconciliation result for every Blocked item even when the parent receives only
the single aggregate actionable alert. The Watchdog never chooses a lifecycle outcome.

Alert the Coordinator when the reconciliation identifies:

- satisfied dependency or unblock evidence
- agent-actionable recovery
- exhausted correction attempts without a current disposition
- a missing, vague, malformed, expired, consumed, or lifecycle-inconsistent disposition receipt
- stale or contradictory lifecycle evidence
- an incorrect next-action owner

The Coordinator validates the retained evidence and chooses the smallest authorized route.
When correction attempts are exhausted, record exactly one evidence-backed outcome:

1. A concrete recovery action, owner, evidence, and links to every unresolved finding.
2. One fresh bounded retry plan with evidence linked to every specific unresolved finding.
   This is one new bounded attempt, not an indefinite correction loop. Consume its result
   before reconciling again, and never authorize a second retry from the same exhausted loop.
3. An explanation, genuine user-owned decision, exact User Action Required question,
   options, tradeoffs, and unattended-work boundary.
4. Continuing Blocked with a concrete external or technical dependency, its owner, and an
   observable trigger for reconciliation.

Reject a vague or indefinite Blocked outcome. A generic instruction to wait, keep trying,
investigate later, or ask the user without an exact user-owned decision is not a disposition.
Across resumption, preserve canonical task identity, candidate, review and verification,
Git state, claim, and attempt history. Dev Backlog Coordinator returns one immutable
decision without changing provider state. Dev Backlog Steward records only that delegated
decision through the already-selected Persistence manager.

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

Apply skills/codex-workitem-coordination/SKILL.md, especially Active Execution, Capacity, And Conversation Titles, Dedicated Read-Only Watchdog, and Fifteen-Minute Parent Review. On each cycle, read current file-backed work items, Git state, configured claim registry state, and Codex runtime state. Evaluate active eligibility and capacity, Starting settlement deadlines, Running Active Execution Evidence, conversation-title synchronization, phases and age, estimates/hard stops/evidence progress, Blocked unblock conditions, accepted work stranded before integration, integrated work awaiting provider closeout, terminal cleanup anomalies, waits at or beyond 30 minutes, and unsafe/stale/broad shared ownership.

Remain strictly read-only. Do not mutate repository files, lifecycle state, claims, tasks, branches, worktrees, or shared resources; do not dispatch, integrate, clean up, or run expensive/live verification. Notify parent task {parent_task_id} only when an actionable condition exists, with exact evidence and the smallest recommended parent action. When healthy, record only a concise no-action cycle result here.
```

#### Canonical Heartbeat Prompt Template

```text
Run one complete read-only watchdog cycle now using the task's standing contract. Notify parent task {parent_task_id} only if an actionable condition exists; otherwise record a concise no-action cycle note here.
```

Substitute only the resolved parent task identifier and repository root shown by these
placeholders. Supply provider and resource-coordination variation through resolved task
context without rewriting the canonical prompt text.

When the watchdog runs, it reads provider inventory, Git state, runtime state, and current
conversation titles. For provider none, it reads only task-local runtime state. When
agent-claim is loaded, it also reads the claim registry. It alerts on every expired Starting
settlement, absent or expired Running Active Execution Evidence, stopped task with a live
claim, terminal item with a live claim, and conversation title that does not match the
central mapping. It also evaluates:

- every Starting item against its 60-second settlement deadline
- every Running phase against its complete Active Execution Evidence, published estimate,
  hard stop, and latest evidence-bearing progress
- every suspected stall and every Stalled item's diagnostic evidence and exit conditions
- every Blocked item's exact blocker and unblock condition, next-action owner, dependencies,
  candidate, review and verification evidence, canonical task state, Git state, applicable
  live claims, correction-attempt history, and current disposition
- accepted work stranded before Commit delivery, READY Commit delivery awaiting provider closeout, and terminal work awaiting cleanup
- stale, unsafe, or unnecessarily broad claims when agent-claim is loaded

The Watchdog is read-only. It reports evidence and recommended actions. It must not change repository files, provider records, lifecycle state, claims, task state, branches, worktrees, or shared resources. It must not dispatch work, integrate changes, perform cleanup, or run expensive or live verification.

When a progress anomaly has a known preventing cause, recommend the Blocked path rather than
Stalled. Recommend Stalled investigation only while the causal blocker or unblock condition
remains unknown.

Notify the parent only when action is required. Identify the affected provider identity or
task, observed evidence, reason attention is required, and smallest recommended Coordinator
action. Examples include suspected Stalled work, a satisfied Stalled or Blocked exit
condition, agent-actionable recovery, exhausted correction attempts without a disposition,
stale or contradictory lifecycle evidence, an incorrect next-action owner, conversation-title
drift, unused capacity
with eligible Ready work, overdue work, stranded accepted work, pending terminal closeout,
an unsafe claim, or a task-identity or cleanup problem. The Watchdog recommends action but
never chooses the lifecycle result.

Treat quiet work as healthy only while its current Active Execution Evidence remains valid.
Silence, conversation-title age, or lack of a recent message is not evidence of failure.
When a configured hard stop is overdue or active evidence expires, report the read-only
deadline and smallest required reconciliation without deciding delivery state.

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

## Reporting

For each considered work item, report dispatch eligibility, any unmet hard blocker, any coordination-only overlap constraint, and any deferred edit, shared-resource, or integration event as distinct facts. Also return the provider identity, lifecycle state, owner and canonical task, dependency and claim evidence, current phase, branch and worktree, accepted commit, review and verification results, Commit and Persistence dispositions, cleanup eligibility, and next safe action.
