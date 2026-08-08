# Default Unconfigured Projects to Solo Mode

Status: Running

Owner: Dev Orchestrator (agent root; canonical task 019fe2f2-f195-7670-8367-15d9e5c79de7)

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

Required Next Lifecycle Transition: Starting -> Running is recorded below for the same canonical task after approval resumption established accepted execution ownership.

## Prior Active Execution Evidence

Condition Type: root-execution.

Owner: Dev Orchestrator (agent root; canonical task 019fe2f2-f195-7670-8367-15d9e5c79de7).

Evidence: Starting -> Running is accepted for canonical Root Dev Orchestrator task 019fe2f2-f195-7670-8367-15d9e5c79de7 under parent Coordinator 019fb057-1767-7ef2-b5fa-41f4417b20b3. The canonical branch is codex/default-unconfigured-projects-to-solo-mode and the private worktree is /Users/martinbechard/.codex/worktrees/75e6/dev-methodology. Current bounded phase is independent discovery and private implementation. Exact overlapping terminology manifest, reviewer, and integration events remain deferred while terminology task 019fe2b3-4bcd-7f00-88aa-90e281b8f8bf retains its live claim. The exact Work Item ID activity=work claim is live for default-unconfigured-projects-to-solo-mode.

Observed At: 2026-08-08T20:04:35Z.

Started At: 2026-08-08T20:04:35Z.

Deadline or Expires At: 2026-08-08T21:04:35Z.

Next Action: Continue independent discovery and private implementation in the canonical branch and worktree. Defer overlapping terminology manifest, reviewer, and integration events until the terminology claim is released.

Next Reconciliation At: 2026-08-08T20:14:35Z.

## Active Execution Evidence

Condition Type: root-execution.

Owner: Root Dev Orchestrator canonical task 019fe2f2-f195-7670-8367-15d9e5c79de7.

Evidence: Clean immutable candidate 16a189b9c6cde179c039bd6357af574848246459 is atop 55b8c805fd8b06fb5687bfaa126cdc577c703a77, e67fa4ac1b2b872ba97a3b4b4b18912975065cbb, and c80a8a3802fb806bc16d5a73b1a48aa581b5688d against baseline f147eca9fe03683b362a58481cd0d1a5e473a483. The full range is exactly eight paths, and the latest correction changed only the role YAML plus the accepted scripted snapshot source digest path. Slot 2 is separately resumed READY multi-contribution after primary Configurator handoff with accepted commits, merge, named fresh-context reviewers, final verification, and final integration commit evidence. Slot 5 preserves missing-config terminal BLOCKED with PRIMARY_PROJECT_CONFIGURATOR_HANDOFF_REQUIRED, no secondary dispatch, and no claim. Green evidence includes BundleContent consumers 3/3, role mutation 17/17, Bootstrapper evaluation 29/29, adjacent selector/provider 4/4, default and legacy disabled/enabled CLIs, skill/provenance/YAML/Python/diff checks. Exactly seven stale generated projections remain deferred. Candidate worktree is clean. Fresh reviewer /root/review_role_matrix_solo_fallback is active read-only on the immutable candidate and full contract. No blocker is recorded. No ninth path is authorized. No terminology claim is relied on. Integration and verification remain deferred. Title is Reviewing.

Observed At: 2026-08-08T22:14:19Z.

Started At: 2026-08-08T20:20:06Z.

Deadline or Expires At: 2026-08-08T22:45:00Z.

Next Action: Receive the reviewer verdict. If correction is required, return exact findings to the fixed coder; otherwise dispatch a fresh verifier.

Next Reconciliation At: 2026-08-08T22:24:19Z.

## User Action Required Transition Evidence

Transition: Running -> User Action Required.

Recorded At: 2026-08-08T20:10:21Z.

Canonical Task: 019fe2f2-f195-7670-8367-15d9e5c79de7.

Branch: codex/default-unconfigured-projects-to-solo-mode.

Worktree: /Users/martinbechard/.codex/worktrees/75e6/dev-methodology.

Execution State: Stopped and waiting. No source changes or Dev Coder dispatch occurred. The canonical branch and private worktree remain clean at f147eca9.

Work Claim: Released with disposition blocked, blocker reference governed-definition-approval-required, event e268be77-dfcb-45d6-9b18-ae399e964eed. No task-owned claim remains live.

Blocker: The approved outcome did not name exact governed definition paths. The methodology requires exact-path approval and a successful per-path pre-mutation result before any governed definition mutation.

Discovery Evidence: The minimum canonical sources requiring approval are skills/set-solo-mode/SKILL.md, skills/set-multitask-mode/SKILL.md, skills/resource-claim/SKILL.md, and agents/roles/project-setup/project-bootstrapper.role.yaml. The expected noncanonical dependents are generated project-bootstrapper adapters, role definitions and manifest, focused claim/mode/bootstrapper tests, maintained documentation, and generator freshness. Exact terminology overlaps remain deferred.

## User Action Required

### Question for the User

Do you approve this work item modifying exactly skills/set-solo-mode/SKILL.md, skills/set-multitask-mode/SKILL.md, skills/resource-claim/SKILL.md, and agents/roles/project-setup/project-bootstrapper.role.yaml to implement the unconfigured-project SOLO fallback?

### Why User Input Is Required

The current approved outcome does not name exact governed definition paths. Exact-path approval and a successful per-path pre-mutation result are required before those definitions may change.

### Options and Tradeoffs

- Yes approves only the four exact canonical definition paths listed in the question, subject to ALLOWED_APPROVED_DEFINITION_CHANGE on each path. The same canonical task may resume after the answer is recorded and the provider routes User Action Required -> Ready -> Starting -> Running.
- No leaves implementation stopped and requires a different disposition. No governed definition or dependent artifact mutation may proceed under this item.

### Resolution

Approved.

## User Action Resolution Evidence

Exact Answer: yes I approve all four paths.

Observed At: 2026-08-08.

Provenance: Direct user message in canonical task/conversation 019fe2f2-f195-7670-8367-15d9e5c79de7, answering the recorded four-path approval question.

Approved Canonical Definition Scope:

- skills/set-solo-mode/SKILL.md
- skills/set-multitask-mode/SKILL.md
- skills/resource-claim/SKILL.md
- agents/roles/project-setup/project-bootstrapper.role.yaml

No other governed definition path is approved by this answer. Generated and other noncanonical dependents remain subject to the existing work-item scope, repository rules, live claim manifests, and independent gates.

Resulting Disposition: Ready for the same canonical execution after provider reconciliation.

Preserved Canonical Execution: Task 019fe2f2-f195-7670-8367-15d9e5c79de7; branch codex/default-unconfigured-projects-to-solo-mode; worktree /Users/martinbechard/.codex/worktrees/75e6/dev-methodology; prior provider and execution evidence remains preserved below.

Owner: Unowned.

Next Action: Parent Coordinator reserves this same task through Ready -> Starting. The root Dev Orchestrator then records Starting -> Running and performs per-path pre-mutation checks before any source mutation.

## Resumption Starting Handoff Evidence

Transition: Ready -> Starting.

Parent Coordination Thread: 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Launch Reservation: 2026-08-08T20:15:31Z.

Normalized Objective: Implement the safe unconfigured-project SOLO-mode fallback.

Dispatch Time: 2026-08-08T20:15:31Z.

Intended Root Role: Dev Orchestrator.

Launch Result: Started.

Canonical Execution: 019fe2f2-f195-7670-8367-15d9e5c79de7.

Last Contact At: 2026-08-08T20:15:31Z.

Next Reconciliation At: 2026-08-08T20:29:31Z.

Owner: Unowned pending Starting -> Running.

Next Action: The root Dev Orchestrator records Starting -> Running for this same canonical task, then performs per-path pre-mutation checks before source mutation.

### Unattended Work Boundary

No source mutation, coder dispatch, review, verification, generated artifact update, integration, or delivery may proceed until the answer is recorded with its provenance and the same canonical task resumes through User Action Required -> Ready -> Starting -> Running. Read-only evidence preservation may continue. Expected noncanonical dependents and exact terminology overlaps remain deferred until their applicable release and reconciliation evidence exists.
