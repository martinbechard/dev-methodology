# Review and Enforce Read-Only Reviewer Runtime Access

Status: Starting

Type: Feature

Provider: file

Work Item ID: review-reviewer-runtime-permissions-and-artifact-boundaries

Completion: main-branch

## Summary

Review and, where current evidence requires it, revise reviewer runtime permissions so independent reviewers can read every repository or project file and every required configured external reference while remaining strictly read-only.

## Context

An independent methodology reviewer for the preserved orchestrated-development-lifecycle candidate could not perform the mandatory terminology review because its nested runtime did not expose the configured mcp-agent-ops reference_load capability. The same capability was available to the Dev Backlog Coordinator runtime. Existing reviewer restrictions may therefore bind required read access together with write restrictions too broadly.

The intended authority boundary is asymmetric. Artifact producers remain sandbox-constrained. Independent reviewers may receive read access comparable to coordinators and orchestrators for repository, project, and required reference sources, but they receive no authority to create, modify, overwrite, or delete any file or artifact. They also remain prohibited from changing provider lifecycle, claims, integration, delivery, branches, worktrees, or another task's state.

## Source Evidence

On 2026-08-11, the user directed the Dev Backlog Coordinator to create a separate durable file-backed work item to review reviewer runtime permissions and artifact boundaries. The user then clarified the final policy before creation: reviewers are strictly read-only, may read any repository or project file and required external or reference source, and may not create, modify, overwrite, or delete files or artifacts, including review artifacts. This item is separate from the immediate recovery of Work Item review-orchestrated-development-lifecycle-text and does not authorize policy mutation before ordinary lifecycle dispatch.

## Recovery Findings

- A Dev Backlog Coordinator runtime exposing mcp-agent-ops reference_load did not prove that a collaboration child launched from that runtime exposed the same capability.
- Fresh methodology-reviewer, general-runtime, and code-reviewer collaboration children each omitted the configured reference operation while correctly retaining read-only authority. The absence was a runtime capability failure, not evidence that reviewer write authority was required.
- A valid capability pilot must run through the exact reviewer execution path used by the real review. A parent-only probe or a probe through a different Agent profile is insufficient evidence.
- A fresh top-level read-only reviewer task created after active MCP configuration initialization successfully invoked the configured terminology reference and continued the immutable candidate review.
- Every recovery attempt preserved zero write capability. Reviewer access to repository, project, and configured reference sources must remain independent from any ability to create or change files or artifacts.

## Requirements

- Compare the effective runtime, sandbox, permission, and tool configuration of independent reviewer roles with Dev Backlog Coordinator and Dev Orchestrator roles, including nested Codex collaboration contexts.
- Identify the mechanism that currently omits mcp-agent-ops reference_load or other required read capabilities from reviewer contexts.
- Distinguish parent-runtime capability, collaboration-child capability, Agent-profile capability, and fresh top-level task capability instead of treating one successful surface as proof for another.
- Define an enforceable reviewer boundary that permits reading any repository or project file and required configured external or reference source.
- Keep reviewers strictly read-only: they must not create, modify, overwrite, or delete files or artifacts, including review checklists, reports, fixtures, temporary outputs, or isolated review artifacts.
- Preserve prohibitions on provider lifecycle mutation, claim operations, integration, delivery, branch changes, worktree changes, task dispatch, and changes to another task's runtime state.
- Keep artifact-producer sandbox constraints unchanged.
- Implement only the smallest source-owned configuration or runtime changes supported by the evidence, regenerating owned projections rather than editing generated adapters directly.
- Preserve the distinction between runtime capability and reviewer authority: access to a read tool must not imply permission to mutate its source or any reviewed artifact.

## Acceptance Criteria

- A source-backed comparison identifies the earliest configuration or runtime divergence that prevents required reviewer read access.
- Every independent reviewer role that requires project or reference evidence can read repository and project files and invoke its configured read-only reference capability from the exact runtime path used by real reviews, whether that path is a collaboration child or a top-level reviewer task.
- Capability evidence from a coordinator, orchestrator, parent task, or different Agent profile is rejected as a substitute for an exact-path reviewer pilot.
- Reviewer runtimes have no file or artifact write capability; focused negative checks demonstrate that creation, modification, overwrite, and deletion are unavailable or rejected, including attempts to write review artifacts.
- Reviewer runtimes cannot mutate provider lifecycle, claims, integration, delivery, branches, worktrees, or another task's runtime state.
- Artifact-producer sandbox and permission profiles are unchanged unless a separately authorized work item changes them.
- Conceptual role sources, runtime configuration, generated adapters, and documentation agree on the same read-only reviewer boundary.
- Focused regression coverage fails when required reviewer reference access is absent and fails when any prohibited reviewer mutation capability is introduced.
- Generated-output freshness, applicable configuration validation, focused runtime capability probes, and independent review and verification pass before main-branch delivery.

## Dependencies

None.

## Verification

- Run a nested reviewer capability probe that reads representative repository and project files and invokes mcp-agent-ops reference_load for an allowlisted reference.
- Run a fresh top-level reviewer capability probe after MCP configuration activation and compare its tool result with the collaboration-child path so runtime initialization and Agent-profile effects are explicit.
- Run focused negative permission tests for file creation, modification, overwrite, and deletion, including review-artifact paths.
- Run focused negative authority tests for provider lifecycle, claim, integration, delivery, branch, worktree, and cross-task mutation operations.
- Confirm artifact-producer permission-profile fixtures and generated adapters remain byte-equivalent unless explicitly in the accepted manifest.
- Run the targeted conceptual-role, generated-adapter, configuration, and freshness tests selected by the changed source paths.
- Obtain fresh independent source review and independent verification of the final candidate.

## Open Questions

- Which source-owned Codex runtime or agent-profile setting controls nested reviewer MCP tool exposure independently from filesystem write authority?
- Can every required external/reference reader be expressed as an explicitly read-only tool allowlist without granting unrelated MCP operations?

## Notes

This item does not authorize changes to the preserved lifecycle-text candidate or its provider state. Immediate recovery may use an already-authorized read-capable reviewer runtime, but any durable reviewer policy or configuration change belongs to this work item's later lifecycle.

## Starting Handoff Evidence

Starting Recorded At: 2026-08-11T22:32:17Z

Coordinator: Codex task 019ff26f-25d0-7381-88f7-74d52717ff59

Normalized Objective: Identify and correct the exact runtime configuration boundary that prevents read-only reviewer roles from accessing required repository and configured reference sources, while preserving zero reviewer write or lifecycle authority; then complete exact-path capability pilots, independent review, focused verification, main-branch delivery, provider closure, and cleanup.

Intended Root Role: Dev Orchestrator

Launch Result: Requested after this durable reservation

Canonical Execution: None

Last Contact At: 2026-08-11T22:32:17Z

Next Reconciliation At: 2026-08-11T22:47:17Z
