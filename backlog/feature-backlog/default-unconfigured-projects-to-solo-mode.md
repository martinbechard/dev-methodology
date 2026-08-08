# Default Unconfigured Projects to Solo Mode

Status: Ready

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
