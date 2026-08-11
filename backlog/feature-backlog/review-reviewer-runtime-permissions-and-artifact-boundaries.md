# Review and Enforce Read-Only Reviewer Runtime Access

Status: Ready

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

## Requirements

- Compare the effective runtime, sandbox, permission, and tool configuration of independent reviewer roles with Dev Backlog Coordinator and Dev Orchestrator roles, including nested Codex collaboration contexts.
- Identify the mechanism that currently omits mcp-agent-ops reference_load or other required read capabilities from reviewer contexts.
- Define an enforceable reviewer boundary that permits reading any repository or project file and required configured external or reference source.
- Keep reviewers strictly read-only: they must not create, modify, overwrite, or delete files or artifacts, including review checklists, reports, fixtures, temporary outputs, or isolated review artifacts.
- Preserve prohibitions on provider lifecycle mutation, claim operations, integration, delivery, branch changes, worktree changes, task dispatch, and changes to another task's runtime state.
- Keep artifact-producer sandbox constraints unchanged.
- Implement only the smallest source-owned configuration or runtime changes supported by the evidence, regenerating owned projections rather than editing generated adapters directly.
- Preserve the distinction between runtime capability and reviewer authority: access to a read tool must not imply permission to mutate its source or any reviewed artifact.

## Acceptance Criteria

- A source-backed comparison identifies the earliest configuration or runtime divergence that prevents required reviewer read access.
- Every independent reviewer role that requires project or reference evidence can read repository and project files and invoke its configured read-only reference capability from the same nested runtime path used by real reviews.
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
