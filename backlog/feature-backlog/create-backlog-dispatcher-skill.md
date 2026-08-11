# Create the Backlog Dispatcher Skill

Status: Starting

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
- Integrate the new skill into the supported skill catalog, runtime metadata, relevant conceptual-agent skill routing only where separately authorized, documentation, generated projections, and focused regression coverage.

## Acceptance Criteria

- A caller using backlog-dispatcher can ask the Dev Backlog Coordinator for safe work, receive complete dispatch packets, create the canonical Codex tasks itself, and return task identities for provider reconciliation.
- A dispatcher receiving a work-coordination message from another agent consults the Backlog Coordinator before taking a coordination action.
- The dispatcher does not delegate actual Codex task creation to a Coordinator runtime that lacks the capability and does not report the overall dispatch as blocked while the caller can execute it.
- The Backlog Coordinator remains the authority for queue state, selection, capacity, dependencies, claims, finish lanes, lifecycle reconciliation, re-homing, and cleanup; the dispatcher does not create a second ledger or infer those decisions.
- Partial task-creation outcomes are reconciled without duplicate tasks, duplicate provider reservations, lost task identities, or unbounded Starting records.
- Existing Watchdog scheduling remains valid: its schedule wakes the canonical read-only Watchdog task, while no Coordinator wakeup is created merely to relay heartbeats.
- Focused tests cover successful multi-item dispatch, unavailable Coordinator-side task tools with available caller-side tools, inbound coordination messages, partial task creation, delayed worktree setup, duplicate prevention, and missing caller capability.
- Catalog, metadata, documentation, generated outputs, and focused tests are current and independently reviewed.

## Dependencies

None.

## Verification

- Validate the new skill and its runtime metadata through the configured skill catalog tooling.
- Run focused contract tests for Coordinator consultation, dispatch-packet completeness, caller-owned task creation, identity reconciliation, inbound coordination messages, partial failure, and duplicate prevention.
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

### Allowed Dependent Artifacts

- skills/backlog-dispatcher/agents/openai.yaml
- README.md
- design/skills-modularization.html
- design/orchestrated-development-lifecycle.html
- design/generated/skill-definitions.js
- scripts/test_bundle_content.py

### Approval Resolution

Approved at creation. On 2026-08-11, in Codex task 019ff2c3-1710-7aa1-89c4-9d6066f51fe4, the user explicitly requested creation of the named backlog-dispatcher-skill Work Item. This approval covers only skills/backlog-dispatcher/SKILL.md as the governed skill-definition source and the exact dependent artifacts listed above. Any additional governed skill or agent-definition source requires separate explicit approval.

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
