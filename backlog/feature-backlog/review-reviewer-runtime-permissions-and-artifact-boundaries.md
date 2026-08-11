# Review and Enforce Read-Only Reviewer Runtime Access

Status: Running

Owner: Dev Orchestrator task 019ff2f9-085e-7202-8099-8f35425278a0

Phase: Preserved candidate review and verification

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
- Define a reviewer role and instruction boundary that permits reading any repository or project file and required configured external or reference source while prohibiting reviewer mutation. Native read-only filesystem sandboxing may enforce file immutability; inherited tool availability does not grant reviewer authority to use mutation operations.
- Keep reviewers strictly read-only: they must not create, modify, overwrite, or delete files or artifacts, including review checklists, reports, fixtures, temporary outputs, or isolated review artifacts.
- Preserve prohibitions on provider lifecycle mutation, claim operations, integration, delivery, branch changes, worktree changes, task dispatch, and changes to another task's runtime state.
- Keep artifact-producer sandbox constraints unchanged.
- Implement only the smallest source-owned configuration or runtime changes supported by the evidence, regenerating owned projections rather than editing generated adapters directly.
- Preserve the distinction between runtime capability and reviewer authority: access to a read tool must not imply permission to mutate its source or any reviewed artifact.

## Acceptance Criteria

- A source-backed comparison identifies the earliest configuration or runtime divergence that prevents required reviewer read access.
- Every independent reviewer role that requires project or reference evidence can read repository and project files and invoke its configured read-only reference capability from the exact runtime path used by real reviews, whether that path is a collaboration child or a top-level reviewer task.
- Capability evidence from a coordinator, orchestrator, parent task, or different Agent profile is rejected as a substitute for an exact-path reviewer pilot.
- Reviewer executions create, modify, overwrite, or delete no file or artifact; focused negative checks demonstrate that attempted file mutation is rejected by the native read-only sandbox or refused by the reviewer role, including attempts to write review artifacts.
- Reviewer executions do not mutate provider lifecycle, claims, integration, delivery, branches, worktrees, or another task's runtime state. Tool presence alone is not a failure when the reviewer role prohibits its use and the exact-path pilot produces no mutation side effect.
- Artifact-producer sandbox and permission profiles are unchanged unless a separately authorized work item changes them.
- Conceptual role sources, runtime configuration, generated adapters, and documentation agree on the same read-only reviewer boundary.
- Focused regression coverage fails when required reviewer reference access is absent or when reviewer instructions, sandboxing, or exact-path behavior permit a prohibited mutation.
- Generated-output freshness, applicable configuration validation, focused runtime capability probes, and independent review and verification pass before main-branch delivery.

## Dependencies

None.

## Verification

- Run a nested reviewer capability probe that reads representative repository and project files and invokes mcp-agent-ops reference_load for an allowlisted reference.
- Run a fresh top-level reviewer capability probe after MCP configuration activation and compare its tool result with the collaboration-child path so runtime initialization and Agent-profile effects are explicit.
- Run focused negative permission tests for file creation, modification, overwrite, and deletion, including review-artifact paths.
- Run focused negative authority tests that confirm the reviewer refuses provider lifecycle, claim, integration, delivery, branch, worktree, and cross-task mutation operations and produces no mutation side effect.
- Confirm artifact-producer permission-profile fixtures and generated adapters remain byte-equivalent unless explicitly in the accepted manifest.
- Run the targeted conceptual-role, generated-adapter, configuration, and freshness tests selected by the changed source paths.
- Obtain fresh independent source review and independent verification of the final candidate.

## Open Questions

- Which source-owned Codex runtime or agent-profile setting controls nested reviewer MCP tool exposure independently from filesystem write authority?
- Do the reviewer role instructions and native read-only filesystem sandbox consistently preserve zero-write behavior across collaboration-child and top-level reviewer paths?

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

## Running Execution Evidence

Running Recorded At: 2026-08-11T22:40:30Z

Canonical Conversation: Codex task 019ff2f9-085e-7202-8099-8f35425278a0

Root Agent Task: 019ff2f9-085e-7202-8099-8f35425278a0

Root Owner: Dev Orchestrator

Branch: codex/reviewer-runtime-permissions-019ff2f9

Worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/review-reviewer-runtime-permissions-work-019ff2f9

Phase: Runtime and configuration divergence diagnosis

Started At Evidence: The configured claim helper returned ISOLATED_CHECKOUT_ACQUIRED for claim review-reviewer-runtime-permissions-work-019ff2f9 at 2026-08-11T22:40:14.068602Z from dispatch commit f1490b80e856df9cc08d24027acd3252734aac18.

Accepted Execution Evidence: This canonical root execution accepted the Starting handoff, acquired the exact opaque Work Item ID with activity work, created the isolated task worktree through the repository-relative configured helper, and began source-backed diagnosis. The handoff-provided hash f1490b80d6df33fe92f88905e8b92cacb596967d was not present; the observed current-main dispatch commit was f1490b80e856df9cc08d24027acd3252734aac18.

## Runtime Divergence Evidence

Phase Changed At: 2026-08-11T22:51:08Z

Current Phase: Reviewer runtime boundary implementation

Earliest Configuration Divergence: Project-scope deployment configured only shared user reference roots and omitted the selected project root, so both exact-path reviewer pilots could call reference_load but received reference_not_found for the repository-root terminology.md.

Authority Divergence: The methodology-artifact-reviewer conceptual source declares repositoryMutation conditional, requires saved checklist and findings artifacts, and generates no Codex read-only sandbox. Both the collaboration-child and fresh top-level reviewer pilots exposed file, artifact, provider, claim, Git, integration, worktree, dispatch, and cross-task mutation operations.

Exact-Path Pilot Evidence: Both pilots read README.md and PROJECT.yaml successfully and invoked the configured mcp-agent-ops reference_load operation. Neither pilot invoked a mutation or created an artifact.

Accepted Candidate: Commit 08554484859c0bdb66d83ef973266f6765e49e58 corrects project reference-root precedence in scripts/install-skills.py with focused coverage in scripts/test_install_skills.py; 89 installer tests passed and the candidate worktree was clean.

Overlap Coordination: Conceptual reviewer sources, generated adapters, scripts/build-skill-docs.py, scripts/test_role_mutation_policy.py, and scripts/test_codex_task_control.py remain deferred until Work Item remediate-inherited-supported-test-baseline-failures returns its exact accepted changed-path and commit handoff.

## Blocked Evidence

Blocked At: 2026-08-11T22:53:58Z

Known Blocker: Codex 0.145 collaboration children inherit the parent tool inventory, and the supported per-agent TOML contract has no tool allowlist or denylist. A reviewer sandbox can reject filesystem writes, but it cannot make provider, claim, GitHub integration, task-dispatch, cross-task, or other state-changing tools unavailable.

Blocker Owner: Dev Backlog Coordinator

Unblock Condition: The Coordinator must choose either to preserve the hard capability-non-exposure requirement and defer this item until Codex supports per-agent tool scoping, or to authorize a revised acceptance boundary that permits inherited mutation tools when the reviewer has native read-only filesystem sandboxing and explicit instruction-level prohibitions.

Requested Coordinator Action: Decide whether hard runtime capability non-exposure remains mandatory. If mandatory, retain Blocked and route the missing Codex runtime feature separately. If instruction-level refusal is accepted as the negative authority proof, authorize bounded resumption from candidate 08554484859c0bdb66d83ef973266f6765e49e58 after the declared overlap item returns its exact accepted handoff.

Blocking References: codex-reviewer-tool-scoping-unavailable; Codex task 019ff2f9-085e-7202-8099-8f35425278a0; top-level pilot task 019ff300-d8be-7052-abeb-1a5c7d5148f5

Recovery Note: Preserve branch codex/reviewer-runtime-permissions-019ff2f9 and its clean isolated worktree. Commit 08554484859c0bdb66d83ef973266f6765e49e58 is a focused, verified reference-root correction but has not completed independent review, integrated verification, or main delivery. The unrelated primary-checkout modification scripts/test_audit_worktree_completion_links.py remained untouched.

Permitted Resumption Transition: Blocked to Ready only after the Coordinator records one of the two explicit runtime-enforcement dispositions and reconciles the overlap handoff.

## Coordinator Runtime-Enforcement Decision

Decision Recorded At: 2026-08-11T22:55:09Z

Decision Owner: Dev Backlog Coordinator task 019ff26f-25d0-7381-88f7-74d52717ff59

Decision: Preserve the hard reviewer mutation-capability non-exposure requirement. Instruction-level refusal plus a read-only filesystem sandbox is not sufficient because inherited provider, claim, Git integration, task-dispatch, and cross-task mutation tools remain callable by the reviewer runtime.

Lifecycle Action: Retain Status: Blocked and Owner: Unowned. Do not resume candidate 08554484859c0bdb66d83ef973266f6765e49e58 or perform further shared mutation for this item.

Rationale: The user-authorized policy requires reviewers to remain strictly read-only, and the acceptance criteria require reviewer runtimes to be unable to mutate provider lifecycle, claims, integration, delivery, branches, worktrees, or another task's state. Replacing capability non-exposure with instruction-only restraint would weaken the authorized requirement rather than verify it.

Technical Dependency: Codex runtime support for enforceable per-agent tool scoping, or an equivalent runtime boundary that makes every prohibited state-changing operation unavailable to reviewer executions while preserving required read access.

Dependency Owner: Codex runtime capability owner.

Observable Unblock Trigger: A supported Codex release and exact-path reviewer pilot demonstrate required repository, project, and configured-reference reads while each prohibited mutation capability is absent or rejected by the runtime boundary.

Preserved Evidence: Keep canonical task 019ff2f9-085e-7202-8099-8f35425278a0, branch codex/reviewer-runtime-permissions-019ff2f9, its clean isolated worktree, and candidate 08554484859c0bdb66d83ef973266f6765e49e58. The candidate remains unreviewed and undelivered. Its project-reference-root correction may be resumed only after this runtime dependency and the recorded overlap are reconciled.

## User Policy Clarification And Recovery

Clarification Recorded At: 2026-08-11T23:13:54Z

Authority: Direct user clarification relayed through parent Coordinator task 019ff26f-25d0-7381-88f7-74d52717ff59

Clarified Boundary: Reviewer zero-write authority is a role-division and instruction boundary. It is not a security policy requiring mutation-capable tools to be absent from the reviewer tool inventory. Reviewers must still create, modify, overwrite, or delete no artifact and must perform no provider, claim, Git integration, task-dispatch, cross-task, branch, or worktree mutation. Producers remain sandbox-constrained.

Superseded Decision: The Coordinator Runtime-Enforcement Decision above is retained as history but is superseded. Codex per-agent tool scoping is not an unblock prerequisite.

Confirmed Blocker Resolution: The false runtime tool-scoping blocker is removed. Candidate 08554484859c0bdb66d83ef973266f6765e49e58 remains clean and focused on scripts/install-skills.py and scripts/test_install_skills.py. The concurrently Running baseline-remediation item owns no live path claim on either file, and its declared 49-identity scope does not include either file. Exact-path overlap is therefore not present for bounded candidate review and verification.

Recovery Action: Blocked -> Ready with Owner: Unowned. Preserve canonical task 019ff2f9-085e-7202-8099-8f35425278a0, branch codex/reviewer-runtime-permissions-019ff2f9, clean isolated worktree, candidate 08554484859c0bdb66d83ef973266f6765e49e58, and all prior evidence. Resume only through a separate Ready -> Starting reservation followed by the same root Dev Orchestrator accepting Starting -> Running.

## Canonical Resumption Handoff

Starting Recorded At: 2026-08-11T23:14:35Z

Coordinator: Codex task 019ff26f-25d0-7381-88f7-74d52717ff59

Normalized Objective: Resume the preserved reference-root candidate under the clarified reviewer role-division policy; maintain zero reviewer mutation behavior and producer sandboxing; reconcile only exact current path overlap; then complete fresh independent review, focused verification, main-branch delivery, provider closure, and cleanup.

Intended Root Role: Dev Orchestrator

Launch Result: Requested for preserved canonical execution

Canonical Execution: Codex task 019ff2f9-085e-7202-8099-8f35425278a0

Preserved Candidate: 08554484859c0bdb66d83ef973266f6765e49e58

Preserved Branch: codex/reviewer-runtime-permissions-019ff2f9

Preserved Worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/review-reviewer-runtime-permissions-work-019ff2f9

Overlap Decision: The Running baseline-remediation item owns no live claim or declared historical repair on scripts/install-skills.py or scripts/test_install_skills.py. Bounded candidate review and verification may resume. Reconcile again before any later overlapping source, generated-output, or integration event.

Last Contact At: 2026-08-11T23:14:35Z

Next Reconciliation At: 2026-08-11T23:29:35Z

## Resumed Running Execution Evidence

Running Recorded At: 2026-08-11T23:15:59Z

Canonical Conversation: Codex task 019ff2f9-085e-7202-8099-8f35425278a0

Root Agent Task: 019ff2f9-085e-7202-8099-8f35425278a0

Root Owner: Dev Orchestrator

Branch: codex/reviewer-runtime-permissions-019ff2f9

Worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/review-reviewer-runtime-permissions-work-019ff2f9

Phase: Preserved candidate review and verification

Preserved Candidate: 08554484859c0bdb66d83ef973266f6765e49e58

Started At Evidence: The configured helper returned SHARED_CHECKOUT_ACQUIRED for exact Work Item ID review-reviewer-runtime-permissions-and-artifact-boundaries with activity work at 2026-08-11T23:15:49.635926Z. The clean preserved worktree remained at candidate 08554484859c0bdb66d83ef973266f6765e49e58.

Accepted Execution Evidence: The same canonical Dev Orchestrator accepted the durable Starting reservation at main commit 0288eb0b5de86f77c0457dbcffefeefd49bb55fc under the user clarification recorded in provider commit 7f5eec27. Reviewers retain zero mutation authority by instruction and role division; inherited tool presence is not itself a failure. Exact current overlap reconciliation found no live claim or declared baseline-remediation scope on scripts/install-skills.py or scripts/test_install_skills.py.
