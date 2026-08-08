# Default Unconfigured Projects to Solo Mode

Status: Running

Type: Feature

Provider: file

Work Item ID: default-unconfigured-projects-to-solo-mode

Completion: main-branch

## Summary

Treat a project without a root PROJECT.yaml as operating in SOLO mode. Agents must proceed without resource claims until project configuration explicitly enables a coordination mode that requires them.

## Context

Project configuration currently selects resource coordination and concurrent-task behavior explicitly. An unconfigured project has no PROJECT.yaml from which to resolve those selectors, so the fallback must be safe, predictable, and usable without requiring project setup first.

SOLO mode means the current agent works without dispatch to secondary tasks. In this fallback, resource claims are unnecessary because there is no configured concurrent coordination context to protect. The fallback must not override an existing PROJECT.yaml or a resource-coordination selection established after project configuration is created.

## Source Evidence

On 2026-08-08, the user requested this backlog item with the exact direction: "when a project doesn't have a PROJECT.yaml, assume we're in SOLO mode - no need for resource claims."

## Requirements

- Define the absence of a root PROJECT.yaml as an effective SOLO-mode fallback.
- Do not load, require, acquire, or mutate resource-claim state solely because PROJECT.yaml is absent.
- Keep the current task runnable in the unconfigured-project fallback without requiring project configuration or a claim-helper setup first.
- Preserve explicit configured behavior when PROJECT.yaml exists, including any selected concurrency and resource-coordination policy.
- Ensure that creating or materially updating PROJECT.yaml replaces the fallback with the selectors recorded in that configuration.
- Update the canonical methodology sources, supported generated artifacts, documentation, and focused regression coverage affected by this default.

## Acceptance Criteria

- In a project with no root PROJECT.yaml, the effective coordination mode is SOLO and secondary-task dispatch is disabled by default.
- In that unconfigured project, ordinary work proceeds without invoking resource-claim or a resource-claim helper and without creating or mutating a claim registry.
- Adding a valid PROJECT.yaml causes the configured coordination and resource-claim selectors to govern subsequent work.
- Existing configured projects retain their current behavior.
- Focused tests cover the absent-configuration fallback, the configured-project path, and the transition from fallback behavior to configured behavior.
- Maintained documentation and generated guidance describe the fallback consistently and pass the applicable repository validation and freshness checks.

## Dependencies

None.

## Verification

- Run focused unit or contract tests for project-configuration discovery and coordination-mode selection with PROJECT.yaml absent.
- Run focused regression tests proving that an existing PROJECT.yaml still controls concurrency and resource coordination.
- Verify that the absent-configuration scenario does not create or mutate resource-claim state.
- Run affected generated-output freshness and source-to-output consistency checks.
- Run documentation validation for changed maintained documents and git diff --check.

## Open Questions

- Which canonical runtime, project-setup, and generated-guidance entry points currently resolve coordination behavior before PROJECT.yaml exists?
- Should the fallback be represented only as derived runtime behavior, or also as an explicit pre-configuration state in user-facing setup guidance?

## Notes

- This item changes the default only while PROJECT.yaml is absent; it does not remove resource coordination from configured projects.
- SOLO is a coordination mode, not a Persistence or Commit selection. This fallback must not infer durable work-item storage or delivery behavior when those selectors are otherwise unresolved.

## Current Starting Handoff Evidence

Transition: Ready -> Starting.

Parent Coordination Thread: 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Launch Reservation: One Root Dev Orchestrator task for this exact work item.

Normalized Objective: Implement the safe unconfigured-project SOLO-mode fallback.

Dispatch Time: 2026-08-08T19:54:46Z.

Intended Root Role: Dev Orchestrator.

Launch Result: Not attempted.

Canonical Execution: None.

Owner: Dev Orchestrator (agent root; canonical task 019fe2f2-f195-7670-8367-15d9e5c79de7).

Last Contact At: 2026-08-08T19:54:46Z; parent Coordinator recorded the reservation.

Next Reconciliation At: 2026-08-08T20:08:46Z.

Required Next Lifecycle Transition: Starting -> Running is recorded below. The canonical task retains the exact Work Item ID activity=work claim and may begin the approved scoped implementation.

## Active Execution Evidence

Condition Type: root-execution.

Owner: Dev Orchestrator (agent root; canonical task 019fe2f2-f195-7670-8367-15d9e5c79de7).

Evidence: Starting -> Running is accepted for the canonical Root Dev Orchestrator task 019fe2f2-f195-7670-8367-15d9e5c79de7 under parent Coordinator 019fb057-1767-7ef2-b5fa-41f4417b20b3. The canonical branch is codex/default-unconfigured-projects-to-solo-mode and the private worktree is /Users/martinbechard/.codex/worktrees/75e6/dev-methodology. Current phase is independent discovery and private implementation. All overlapping docs, generated outputs, reviewer work, and integration are deferred while terminology task 019fe2b3-4bcd-7f00-88aa-90e281b8f8bf retains its live claim. The exact Work Item ID activity=work claim is live for default-unconfigured-projects-to-solo-mode.

Observed At: 2026-08-08T19:59:18Z.

Started At: 2026-08-08T19:59:18Z.

Deadline or Expires At: 2026-08-08T20:59:18Z.

Next Action: Continue independent discovery and private implementation in the canonical branch and worktree, while deferring overlapping docs, generated outputs, reviewer work, and integration until the terminology claim is released.

Next Reconciliation At: 2026-08-08T20:14:18Z.
