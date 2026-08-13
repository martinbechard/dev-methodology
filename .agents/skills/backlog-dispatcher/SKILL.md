---
name: backlog-dispatcher
description: Execute backlog work dispatch through caller-owned runtime tools while a Dev Backlog Coordinator retains authoritative queue, lifecycle, capacity, ownership, and recovery decisions.
metadata:
  category: development-practice
---
<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: b6764ec5-f78f-48a0-ac39-8d6c0ba9f9d1
Created-UTC: 2026-08-11T23:18:56Z
Creating-Agent: Dev Orchestrator
Runtime: Codex
Dispatched-Model: gpt-5.6-sol
Reasoning-Effort: low
Task-ID: 019ff2c3-1710-7aa1-89c4-9d6066f51fe4
Artifact-ID-Evidence: runtime-supplied
Created-UTC-Evidence: runtime-supplied
Creating-Agent-Evidence: runtime-supplied
Runtime-Evidence: runtime-supplied
Dispatched-Model-Evidence: runtime-supplied
Reasoning-Effort-Evidence: runtime-supplied
Task-ID-Evidence: runtime-supplied
-->

# Backlog Dispatcher

Use this skill when the current caller must dispatch or resume coordinated backlog work, or when another Agent sends the caller a message that requires a work-coordination decision.

Apply coordinate-work-items for the portable coordination contract and the runtime-specific coordination skill for task creation, identity, follow-up, titles, waiting, automation, and archival. Apply the selected provider manager and resource-coordination procedure only through the authority assigned by those contracts.

## Authority Boundary

The Dev Backlog Coordinator decides what backlog action is safe. The dispatcher performs caller-owned runtime operations that realize that decision.

The Coordinator owns:

- authoritative provider inventory and lifecycle reconciliation;
- dependency, capacity, finish-lane, overlap, ownership, claim, Watchdog, re-homing, and cleanup decisions;
- Ready-to-Starting reservations and other Coordinator-owned provider transitions;
- selection of the canonical existing execution or authorization to create one;
- the reference-plus-delta launch packet as the entire launch payload, or authorization to resume the canonical existing execution without copied provider or selected-skill facts.

The dispatcher owns:

- invoking or resuming the Dev Backlog Coordinator with the complete current coordination question;
- creating, resuming, messaging, titling, waiting on, or archiving runtime tasks when the caller exposes those capabilities;
- preserving ambiguous runtime outcomes and reconciling them before retry;
- returning exact runtime task identities and operation results to the Coordinator;
- forwarding the Coordinator's decision to the canonical worker without weakening or expanding it.

The dispatcher is not a second Coordinator. It does not create a shadow queue, capacity ledger, mode record, ownership record, or Watchdog.

## Role Division

Reviewers are zero-write role owners. They inspect and report; they do not create, modify, overwrite, delete, integrate, deliver, claim, dispatch, re-home, or clean up artifacts or work-item state.

Coders, writers, and other producers create or correct artifacts within their assigned sandbox and claims. Reviewer zero-write authority is a role and instruction boundary. Do not reinterpret it as a requirement that every mutation-capable tool be absent from the reviewer runtime unless an explicit security requirement separately says so.

## Visible Work Item Task Launch

For Backlog Dispatcher launches, this project-private skill governs launch topology and takes precedence over the generic root Dev Orchestrator task wording in coordinate-codex-tasks. coordinate-codex-tasks supplies task-control mechanics only. The user-visible Codex task is the canonical Work Item runtime identity. The nested Dev Orchestrator collaboration subagent is not that canonical task.

The root Backlog Dispatcher creates exactly one user-visible Codex task. The root Dispatcher gives that visible task the exact Reference-Plus-Delta Launch Prompt below as its initial prompt. The visible task then launches exactly one nested Dev Orchestrator collaboration subagent for the authoritative provider record. The root Dispatcher must not directly launch that hidden collaboration subagent as the Work Item launch. The nested Dev Orchestrator independently records Starting -> Running before any source mutation.

Lifecycle and material Running-phase title operations remain on the visible Codex task and its retained user-visible context. They do not target the nested Dev Orchestrator collaboration subagent.

Preserve an already-live hidden Work Item execution as its existing owner until it stops or completes. Do not create a visible replacement task while that hidden execution is live, and do not launch duplicate implementation.

## Dispatch Workflow

1. Send the Dev Backlog Coordinator the user's requested dispatch outcome and the caller's known runtime capabilities. Include relevant incoming coordination messages without treating their assertions as authoritative state.
2. Require the Coordinator to reconcile the provider, active and archived runtime tasks, dependencies, capacity, claims, finish lanes, path overlap, preserved candidates, worktrees, Watchdog, and cleanup eligibility.
3. Require one decision for each selected Work Item: reserve and dispatch, resume the canonical execution, retain a truthful non-active state, or identify one concrete user decision.
4. Do not launch until the provider locator resolves to durable reservation evidence and the Coordinator returns the reference-plus-delta packet as the entire launch payload. Treat canonical resumption as a distinct runtime operation without copied provider or selected-skill facts.
5. For a new dispatch, create the visible task defined above with the reference-plus-delta packet as its initial prompt. Require the visible wrapper only for a new dispatch. For a resumption, resume the canonical existing execution, including an already-live hidden execution preserved as the existing owner. Do not ask the Coordinator's delegated runtime to create tasks when that runtime lacks the capability and the caller has it.
6. Return every successful, failed, pending, or ambiguous runtime outcome to the Coordinator with the exact Work Item ID and runtime identity. The Coordinator reconciles provider lifecycle; the dispatcher does not infer that task creation means Running.
7. Observe the created or resumed task until its identity is stable enough for reconciliation. Use runtime waiting and inspection rather than heartbeat or progress messages.
8. Forward only a final outcome or one specific Coordinator decision between workers and the Coordinator.

## Dispatch Packet

A launch prompt contains only one execution action, the authoritative provider locator, and dispatch-time delta only. The action must launch one Dev Orchestrator subagent for the identified Work Item. Dispatch-time delta is limited to launch-only facts that cannot already be authoritative in the provider record.

Persist every stable assignment fact missing from the provider record before launch. A launch is invalid while a stable assignment fact is absent from the provider record.

### Reference-Plus-Delta Launch Prompt

```text
Launch one Dev Orchestrator subagent to execute Work Item <opaque Work Item ID>.
Authoritative provider: <provider locator>
Dispatch-time delta: <launch-only facts absent from the provider, or none>
```

Reject a launch prompt that copies provider requirements, scope, acceptance criteria, or verification expectations. Reject a launch prompt that copies lifecycle, claim, review, verification, delivery, cleanup, or recovery procedures from selected skills. Reject generic task or worker wording and any instruction to reconstruct root awareness.

Reject a title-only packet, an instruction to rediscover the originating conversation, or a packet that leaves the caller to choose backlog state or work-item identity. A resumption targets the canonical existing execution through the runtime-specific coordination skill; it does not reconstruct or replace the launch prompt.

## Incoming Coordination Messages

Consult the Dev Backlog Coordinator before acting on any Agent message that requests or implies:

- new work selection or replacement capacity;
- lifecycle or provider mutation;
- ownership, claim, dependency, or path-overlap resolution;
- candidate acceptance, finish-lane priority, integration ordering, or delivery sequencing;
- task replacement, re-homing, resumption, or duplicate reconciliation;
- Watchdog scheduling or response;
- branch, worktree, claim, task, or provider cleanup;
- a change to reviewer or producer authority.

Pass the message as evidence and ask the Coordinator to verify it against authoritative runtime and durable records. Do not accept the sending Agent's requested disposition merely because it supplied detailed evidence.

Ordinary final results may be forwarded to the Coordinator without a second decision request. Routine progress, heartbeat, title-only, and repeated evidence messages remain prohibited.

## Project Runtime Boundary

A local claim or modified files do not extend runtime-control authority outside the current project or working-directory coordination context. Do not send a coordination, stop, resume, cleanup, or lifecycle-control message to a task outside that context, even when one of its subagents owns a local claim or modified files in the current repository.

When the exact owning subagent is not directly addressable, do not use a cross-project parent task as a relay. Treat the ownership as unaddressable or stranded. Preserve the bytes and evidence, perform no cross-project runtime mutation, and return the limitation to the Dev Backlog Coordinator for an explicitly authorized recovery decision.

## Terminal Cleanup

Terminal cleanup begins only after the Dev Orchestrator returns terminal evidence and cleanup eligibility and the Dev Backlog Coordinator authorizes exact targets. The cleanup packet names the authorized task, worktree, and branch. The root Backlog Dispatcher executes only that packet.

For each authorized operation, the root Backlog Dispatcher must:

1. remove the authorized worktree;
2. safely delete the authorized branch after worktree removal;
3. archive the authorized task after every other authorized cleanup operation;
4. return every cleanup outcome, including failed, pending, or ambiguous outcomes.

The Coordinator reconciles capacity only after those outcomes return. The dispatcher does not infer cleanup eligibility, substitute another target, or reconcile capacity itself.

## Partial And Ambiguous Runtime Outcomes

Treat a timeout, disconnect, delayed worktree setup, pending client identifier, or incomplete task-creation response as an ambiguous runtime mutation.

- Preserve every returned client, task, conversation, and host identity.
- Use the actual runtime parent identity for task lookup and the Coordinator identity for decision routing.
- Do not issue a duplicate create or resume operation.
- Inspect active and archived runtime tasks using the authoritative provider locator, returned runtime identity, creation time, source parent, and dispatch-time delta.
- Report matched, unmatched, and still-pending outcomes separately to the Coordinator.
- Let the Coordinator decide whether a Starting reservation remains valid, returns to Ready, resumes an existing task, or requires recovery.

Successful visible task creation is not Running evidence. The nested Dev Orchestrator accepts Running through the provider workflow before repository mutation.

## Bounded Successor Execution

For an unusable canonical task, execute only the Coordinator's exact one-successor authorization. Before launch, require the authoritative provider record to show the observed failure of an ordinary required capability during the active workload and exhausted bounded identity-preserving recovery through the same canonical task. A capability-pilot mismatch is not successor evidence and remains on the pilot correction path. Idle, slow, quiet, or an ordinary bounded wait never permits this operation.

Persist all stable recovery evidence in the authoritative provider record before launch. Use the reference-plus-delta launch prompt without copying that evidence. Preserve the old task identity and return the successor or pending identity so the Coordinator can record the durable old-to-new identity handoff. Do not infer either identity from a title, prompt, branch, worktree, or provider path.

Before successor creation, reconcile any prior ambiguous runtime outcome. After an error, timeout, disconnect, or incomplete creation response, reconcile active and archived runtime tasks using the packet evidence. Adopt the one matching successor or stop every duplicate as the Coordinator directs. Do not issue another create operation.

Prevent concurrent mutation by the old execution, a duplicate, or the successor. Successful creation is not Running. The successor records Starting -> Running through the provider before any repository or shared-work mutation. This required provider update is the sole lifecycle mutation permitted before Running becomes durable. Before the successor accepts Running, the old execution and every duplicate must be stopped or permanently barred from repository and shared-work mutation. After Running acceptance, only the accepted successor may mutate repository or shared work.

If the sole successor cannot accept Running or later fails, return that outcome for the Coordinator's truthful non-active provider disposition. Never create or request another successor.

## Capability Boundary

Before reservation, tell the Coordinator which required runtime operations the caller can perform. If the Coordinator's delegated runtime lacks task controls but the caller has them, continue through the caller-owned dispatch workflow.

Return BLOCKED only when a required operation is unavailable across the authorized caller path, or when authoritative provider, claim, dependency, overlap, or runtime evidence prevents safe work. Do not move additional Ready items into Starting when their execution cannot be attempted.

## Watchdog Boundary

Retain one canonical read-only Watchdog outside queue capacity. When a Watchdog schedule is configured, it must wake the Watchdog task to perform its own observation cycle.

Do not schedule the Coordinator merely to relay routine heartbeat or progress prompts. A Watchdog message that requests a coordination decision is handled through the incoming-message workflow above.

## Live Refinement

Use real dispatch and coordination discussions as the initial validation loop. When the user clarifies a dispatcher rule or a live operation exposes a concrete ambiguity:

1. Apply the clarified rule to the current coordination decision.
2. Preserve the resulting provider and runtime evidence.
3. Update this skill in the authorized canonical source so the same mistake is not repeated.
4. Run focused validation for the changed contract.

Do not create a dedicated Evaluation suite until the user authorizes that phase after the current backlog is complete. Deferring the suite does not defer skill validation, focused contract checks, independent review, or correction of observed failures.

## Result

Return the Coordinator decision, executed runtime operations, Work Item-to-task identity mapping, capacity and Watchdog state, ambiguous or partial outcomes, and one specific unresolved blocker or user decision. State whether work is continuing.
