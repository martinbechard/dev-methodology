# Create the Backlog Dispatcher Skill

Status: Completed

Type: Feature

Provider: file

Work Item ID: create-backlog-dispatcher-skill

Completion: main-branch

## Summary

Create a portable backlog-dispatcher skill that delegates authoritative backlog reconciliation and work selection to the Dev Backlog Coordinator while retaining actual Codex task dispatch and coordination-message execution in the calling task.

## Context

The Dev Backlog Coordinator can reconcile provider lifecycle, dependencies, claims, capacity, finish lanes, path overlap, cleanup eligibility, and Watchdog state, but its delegated runtime may not expose canonical Codex task creation and task-management tools. The calling task may expose those tools. Treating the missing runtime capability as a Coordinator blocker leaves durably selected work undispatched even though the caller can perform the dispatch safely.

The intended boundary is explicit: the Backlog Coordinator decides what may run and prepares complete dispatch instructions; the backlog dispatcher executes the approved task operations and returns canonical task identities for reconciliation. When the dispatcher receives a message from another agent about work coordination, it must consult the Backlog Coordinator before making a backlog, capacity, ownership, lifecycle, re-homing, or cleanup decision.

This feature must preserve the existing read-only Watchdog contract. A configured Watchdog schedule must wake the canonical Watchdog task. The dispatcher must not reinterpret that wakeup as a Coordinator heartbeat relay.

## Source Evidence

On 2026-08-11, in Codex task 019ff2c3-1710-7aa1-89c4-9d6066f51fe4, the user requested: "we'll need to create a backlog-dispatcher-skill - and the backlog-coordinator will be called to find out what we need to do, letting the caller do the actual dispatching. If the dispatcher receives messages from other agents about work coordination, he should consult with the backlog-coordinator. Create a work item to do this".

## Requirements

- Add the portable skill backlog-dispatcher with a clear caller-facing activation contract for backlog dispatch and work-coordination messages.
- Require the dispatcher to invoke a Dev Backlog Coordinator for authoritative provider inventory, dependency, claim, capacity, finish-lane, path-overlap, Watchdog, re-homing, and cleanup decisions before dispatching work.
- Keep provider lifecycle authority, work selection, reservation decisions, and canonical dispatch-packet preparation with the Backlog Coordinator.
- Keep canonical Codex task creation, follow-up delivery, title synchronization, waiting, archival, automation changes, and other runtime operations with the calling dispatcher when those capabilities are available only to the caller.
- Require the Coordinator to return complete, independently executable dispatch packets that include the Work Item ID, provider location, role, title, prompt, baseline, isolation requirements, claim instructions, lifecycle handoff, reviewer authority, verification expectations, and reporting destination.
- Require the dispatcher to execute only the Coordinator-approved packets, preserve their canonical Work Item identities, and return created task identifiers and runtime outcomes to the Coordinator for Starting-to-Running or recovery reconciliation.
- Require the dispatcher to consult the Backlog Coordinator whenever another agent sends a message that requests or implies work selection, capacity changes, ownership changes, lifecycle mutation, task re-homing, conflict resolution, claim recovery, finish-lane prioritization, Watchdog action, or terminal cleanup.
- Distinguish ordinary progress or final-result forwarding from coordination decisions so the dispatcher does not create unnecessary Coordinator traffic.
- Define safe partial-dispatch behavior: preserve successful task identities, reconcile failed or pending task creation individually, and never duplicate a task merely because worktree setup or task discovery is delayed.
- Preserve normal concurrent dispatch, provider and claim authority, reviewer zero-write authority, producer sandbox constraints, the single canonical read-only Watchdog, and the prohibition on shadow backlog or mode records.
- Define an explicit blocked result when the caller lacks a required runtime capability after Coordinator reconciliation, naming the missing capability without moving additional Ready items into an unexecutable lifecycle state.
- Integrate the new skill into the supported skill catalog, runtime metadata, relevant conceptual-agent skill routing only where separately authorized, documentation, generated projections, and focused skill validation.
- Implement and live-test the skill now. Do not create a dedicated Evaluation suite for this item; the user defers that suite until the current backlog is complete. During this delivery, improve the canonical skill when subsequent coordination discussions expose a concrete, source-backed rule within the approved scope.

## Acceptance Criteria

- A caller using backlog-dispatcher can ask the Dev Backlog Coordinator for safe work, receive complete dispatch packets, create the canonical Codex tasks itself, and return task identities for provider reconciliation.
- A dispatcher receiving a work-coordination message from another agent consults the Backlog Coordinator before taking a coordination action.
- The dispatcher does not delegate actual Codex task creation to a Coordinator runtime that lacks the capability and does not report the overall dispatch as blocked while the caller can execute it.
- The Backlog Coordinator remains the authority for queue state, selection, capacity, dependencies, claims, finish lanes, lifecycle reconciliation, re-homing, and cleanup; the dispatcher does not create a second ledger or infer those decisions.
- Partial task-creation outcomes are reconciled without duplicate tasks, duplicate provider reservations, lost task identities, or unbounded Starting records.
- Existing Watchdog scheduling remains valid: its schedule wakes the canonical read-only Watchdog task, while no Coordinator wakeup is created merely to relay heartbeats.
- Focused skill and contract validation plus recorded live usage cover successful multi-item dispatch, unavailable Coordinator-side task tools with available caller-side tools, inbound coordination messages, partial task creation, delayed worktree setup, duplicate prevention, and missing caller capability.
- Catalog, metadata, documentation, generated outputs, focused validation, and live-usage evidence are current and independently reviewed. A dedicated Evaluation suite is not required for this item and remains deferred until the current backlog is complete.

## Dependencies

None.

## Verification

- Validate the new skill and its runtime metadata through the configured skill catalog tooling.
- Run focused skill and contract validation for Coordinator consultation, dispatch-packet completeness, caller-owned task creation, identity reconciliation, inbound coordination messages, partial failure, and duplicate prevention.
- Exercise the skill through current live backlog dispatch and coordination-message handling, retain the observed outcomes, and update the canonical skill when that usage exposes a concrete in-scope rule. Do not create or run a dedicated Evaluation suite for this item.
- Regenerate and verify every supported projection affected by the skill catalog change.
- Review the authority split against coordinate-work-items, coordinate-codex-tasks, the Dev Backlog Coordinator role, the Dev Backlog Watchdog role, and resource-claim guidance.
- Perform a fresh prompt/skill review that confirms the dispatcher cannot silently assume Coordinator authority or bypass provider and claim evidence.
- Run git diff --check and the repository's smallest applicable skill-bundle checks.

## Open Questions

- Determine during implementation whether existing portable coordination skills should reference backlog-dispatcher or whether caller activation metadata alone provides the cleanest dependency direction.
- Determine the smallest structured dispatch-packet result contract that supports current Codex tools without coupling the portable skill to one runtime schema.

## Governed Definition Approval

### Governed Canonical Sources

- skills/backlog-dispatcher/SKILL.md
- skills/coordinate-codex-tasks/SKILL.md
- agents/roles/dev-activities/dev-backlog-coordinator.role.yaml

### Allowed Dependent Artifacts

- skills/backlog-dispatcher/agents/openai.yaml
- README.md
- design/skills-modularization.html
- design/orchestrated-development-lifecycle.html
- design/generated/skill-definitions.js
- design/generated/role-definitions.js
- design/agent-skill-test-coverage-checklist.md
- generated/adapters/agent-generation-manifest.json
- generated/adapters/claude/agents/dev-backlog-coordinator.md
- generated/adapters/codex/agents/dev-backlog-coordinator.toml
- generated/adapters/gemini/agents/dev-backlog-coordinator.md
- generated/adapters/junie/agents/dev-backlog-coordinator.md
- scripts/test_agent_identity_generation.py
- scripts/test_bundle_content.py
- scripts/test_codex_task_control.py
- scripts/test_role_mutation_policy.py
- scripts/test_work_item_coordination.py

### Approval Resolution

Approved at creation and explicitly expanded on 2026-08-11 in canonical Codex task 019ff2c3-1710-7aa1-89c4-9d6066f51fe4. The expanded approval covers exactly the three governed canonical sources and the mechanically required dependent artifacts listed above. It does not authorize another skill definition, Agent definition, Evaluation suite, or unrelated generated or documentation artifact.

Exact user architecture clarification and approval:

> The Coordinator runs as a subagent and some Codex functionality is unavailable there. Therefore the Coordinator must tell the root task agent exactly what to do; the root has the tools and performs operations such as starting user-visible tasks. Previously the Coordinator was run as a root task that was merely aware of the Coordinator role but did not actually run it; that pattern is replaced. Treat this as explicit approval to expand create-backlog-dispatcher-skill to modify exactly skills/coordinate-codex-tasks/SKILL.md and agents/roles/dev-activities/dev-backlog-coordinator.role.yaml plus mechanically required generated adapters, documentation, focused expectations, and the generated structural checklist.

Architecture Decision: The Dev Backlog Coordinator runs as the decision-authority subagent. It reconciles authoritative state, records Coordinator-owned lifecycle transitions, and tells the root Backlog Dispatcher exactly which caller-only runtime operations to perform. The root Backlog Dispatcher is the execution authority for caller-only Codex tools, including starting user-visible tasks, and returns exact outcomes for Coordinator reconciliation. The former pattern in which a root task was merely aware of the Coordinator Role without running a Coordinator subagent is replaced.

## Notes

- This Work Item creates the dispatcher skill; it does not transfer backlog authority from the Dev Backlog Coordinator to the caller.
- The dispatcher is an execution bridge for runtime capabilities, not a replacement Coordinator, shadow scheduler, or second queue owner.

## Starting Handoff Evidence

Starting Recorded At: 2026-08-11T23:16:29Z

Coordinator: Dev Backlog Coordinator delegated by canonical Codex caller task 019ff2c3-1710-7aa1-89c4-9d6066f51fe4

Normalized Objective: Create and integrate the portable backlog-dispatcher skill with its exact approved dependent artifacts, prove the Coordinator-to-caller dispatch boundary through focused validation and live usage, preserve current queue and Watchdog authority, then complete independent review, main-branch delivery, provider closure, and cleanup. Defer a dedicated Evaluation suite until the current backlog finishes, as directed by the user.

Intended Root Role: Dev Orchestrator operating in the canonical caller task

Launch Result: Requested for existing canonical execution

Canonical Execution: Codex task 019ff2c3-1710-7aa1-89c4-9d6066f51fe4

Dispatch Baseline: ef01cc13f4b503de40f700033ca009b7e0a27962

Capacity Evidence: Three actively eligible items occupy concurrent capacity before this reservation: two Running items and one Starting canonical resumption. This user-prioritized item is the fourth active item and remains below the evidence-based concurrent limit of five.

Overlap Constraints: The active lifecycle-design item may own design/orchestrated-development-lifecycle.html. Defer changes or integration for that exact file until its owner releases or hands off the path. The baseline-remediation item has no live path claim but may later touch scripts/test_bundle_content.py; reconcile its accepted changed-path handoff before editing or integrating that file. The new skills/backlog-dispatcher subtree and skills/backlog-dispatcher/agents/openai.yaml are currently independent. Reconcile README.md, design/skills-modularization.html, design/generated/skill-definitions.js, and every other approved dependent artifact immediately before its edit or integration event.

Reviewer And Producer Boundary: Reviewers remain zero-write role owners and must not mutate artifacts or lifecycle state. Artifact producers remain sandbox-constrained.

Last Contact At: 2026-08-11T23:16:29Z

Next Reconciliation At: 2026-08-11T23:31:29Z

## Running Execution Evidence

Running Recorded At: 2026-08-11T23:18:00Z

Codex Task ID: 019ff2c3-1710-7aa1-89c4-9d6066f51fe4

Conversation ID: 019ff2c3-1710-7aa1-89c4-9d6066f51fe4

Root Role: Dev Orchestrator

Parent Task ID: 019ff2c3-1710-7aa1-89c4-9d6066f51fe4

Branch: codex/create-backlog-dispatcher-skill-019ff2c3

Worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/create-backlog-dispatcher-skill-019ff2c3

Accepted Baseline: ed203bdf56cf16ade738b1e4a6d54f6a471b3bdc

Phase: Implementing

Execution Evidence: The canonical caller accepted the Coordinator reservation, acquired work-item ownership, created the isolated full-history worktree, and began the user-prioritized skill implementation. Focused validation and live dispatch usage replace a dedicated Evaluation suite until the current backlog is complete.

## Completion Evidence

Completed At: 2026-08-11T23:49:00Z

Accepted Candidate: 4b420325

Main Integration: 710d9ed5

Review: Fresh zero-write Dev Skill Lint Reviewer verdict GOOD after correction of task-control ownership and runtime-parent identity findings.

Verification: Independent Dev Verifier verdict PASS. Both skills and YAML sources validated; OpenAI metadata, generated adapters, generated documentation data, and structural checklist were current; all 16 focused Codex task-control tests passed; five affected bundle checks passed; provenance validated against the runtime envelope; and git diff checks passed. The full bundle suite retained one unrelated pre-existing terminology role-routing failure.

Live Usage: The root caller used the Coordinator subagent to reserve work, execute five caller-owned task creations, route an incoming coordination decision, correct a false reviewer-security interpretation, resume the canonical worker, reconcile this Work Item's scope, and return runtime outcomes. These operations directly exercised the initial dispatcher contract without creating a dedicated Evaluation suite.

Delivered Outcome: The Dev Backlog Coordinator now runs as the decision-making subagent. The root Backlog Dispatcher performs caller-only Codex runtime operations from exact Coordinator packets and returns distinct Runtime Parent Task ID and Coordinator Task ID evidence for reconciliation. Reviewer zero-write remains a role-division boundary. The canonical Watchdog remains read-only and its configured schedule wakes it directly.

Claims: Work, integration, update, and exact provider-path claims were reconciled and released at their operation boundaries.
