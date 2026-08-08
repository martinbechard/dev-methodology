# Default Unconfigured Projects to Solo Mode

Status: Starting

Owner: Unowned

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

## Recovery Evidence

Transition: Running -> Ready.

Recorded At: 2026-08-08T20:02:36Z.

Reason: The canonical execution was stopped before source work began. The prior Starting -> Running provider commit was already durable, but its execution ownership ended during reconciliation. This recovery records the truthful non-active state without rewriting either prior commit.

Canonical Task: 019fe2f2-f195-7670-8367-15d9e5c79de7.

Branch: codex/default-unconfigured-projects-to-solo-mode.

Worktree: /Users/martinbechard/.codex/worktrees/75e6/dev-methodology.

Prior Provider Commits: f147eca9fe03683b362a58481cd0d1a5e473a483 (Starting evidence) and e2afa73eab4a46cf434277b41c5a0b8ba8e546b5 (invalid direct Ready -> Running sequence).

Released Claim Events: 96f5f988-40ac-4f99-9e47-80ba16ee3e87 (provider path) and 80c9cdff-c142-4bfc-a7f0-057312f61105 (work claim handoff).

Source Mutation: None. The canonical branch and worktree remain clean and resumable.

Owner: Unowned.

Active Execution Evidence at recovery: None. The item was Ready and had no active execution ownership before this new Starting reservation.

## Current Starting Handoff Evidence

Transition: Ready -> Starting.

Parent Coordination Thread: 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Launch Reservation: 2026-08-08T20:00:59Z.

Normalized Objective: Implement the safe unconfigured-project SOLO-mode fallback.

Dispatch Time: 2026-08-08T20:00:59Z.

Intended Root Role: Dev Orchestrator.

Launch Result: Started.

Canonical Execution: 019fe2f2-f195-7670-8367-15d9e5c79de7.

Owner: Unowned pending Starting -> Running.

Last Contact At: 2026-08-08T20:00:59Z.

Next Reconciliation At: 2026-08-08T20:14:59Z.

Required Next Lifecycle Transition: Starting -> Running for the same canonical task after accepted execution ownership is established.
