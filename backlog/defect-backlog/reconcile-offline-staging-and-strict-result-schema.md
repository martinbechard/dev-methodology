# Reconcile Offline Staging and Strict Result Schema

Status: Running

Type: Defect

Provider: file

Work Item ID: reconcile-offline-staging-and-strict-result-schema

Completion: main-branch

## Summary

Reconcile linked-worktree offline dependency staging with the current strict coordinator-result schema and integrate the behavior only after all focused invariants pass together.

## Context

The branch codex/runner-offline-schema-correction-019f77f4 at 276ce9c0efd583bda9505e3823f59cbfd8e12271 adds canonical-primary-worktree fallback for ignored JavaScript dependencies, lockfile and version validation, symlink containment, diagnostic improvements, and strict coordinator-result schema checks.

A direct integration attempt on 2026-08-12 passed four focused offline-staging tests but failed the strict-object schema invariant because current main later added deliveryResult and claimRelease properties without listing them in their containing required arrays. The attempted integration was reverted by ae36443c after candidate commit c35d6a7e so main did not retain a knowingly failing result.

The earlier branch codex/verify-offline-staging-482f85a at 482f85afb3f301319392c0e02c51d969d706d056 is a narrower predecessor and requires no separate preservation.

## Source Evidence

On 2026-08-12, the user approved the stricter successor branch and directed that replacement work items preserve enough evidence to delete legacy branches. Focused integration verification exposed a current-main schema incompatibility that cannot be accepted as-is.

## Requirements

- Reproduce linked-worktree offline dependency absence using a disposable evaluation workspace.
- Preserve canonical-primary-worktree fallback only when selected lockfile, installed version, containment, and symlink checks pass.
- Reject absolute and escaping symlinks while preserving safe relative internal symlinks.
- Reconcile deliveryResult and claimRelease with the strict-object schema invariant and their conditional runtime semantics.
- Ensure coordinator prompts, schema, checkpoint loading, report auditing, and tests agree on omitted, null, required, and unexpected evidence behavior.
- Do not reapply either legacy branch wholesale.

## Acceptance Criteria

- Offline evaluation from a linked worktree can reuse valid primary-worktree dependencies without network access.
- Lockfile mismatch, version mismatch, missing dependencies, absolute symlinks, and escaping symlinks fail with bounded diagnostics.
- Every strict object declares all of its properties through an accepted strict-schema representation.
- Conditional deliveryResult and claimRelease semantics remain explicit and validated.
- All focused offline-staging and strict-schema tests pass together on current main.

## Dependencies

None.

## Verification

- Inspect 276ce9c0efd583bda9505e3823f59cbfd8e12271 and predecessor 482f85afb3f301319392c0e02c51d969d706d056.
- Run the five focused tests introduced by the stricter candidate plus current delivery-result and claim-release tests.
- Validate the coordinator schema through the supported structured-output path.
- Run git diff --check.
- Obtain independent review of filesystem containment and schema semantics.

## Open Questions

None.

## Notes

- The integration and revert commits document the failed current-main gate; neither establishes delivery.
- Both legacy branches and worktrees can be deleted after this work item is committed and verified.

## Starting Handoff Evidence

- Reserved At: 2026-08-13T15:10:07Z.
- Transition: `Ready -> Starting`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Baseline: `e5491bb6c20b68a662830db63a53779c1de21a0d` on primary `main`.
- Priority: Oldest eligible process-correctness defect after receipt-integrity delivery completed and released its runner/evaluation claims.
- Capacity: Uses one available slot alongside the active Index alignment lane; User Action Required and Blocked items remain excluded.
- Overlap: Index owns only `index.html`, documentation-design-system tests, bundle-content tests, and one shared CSS asset. This item must limit initial diagnosis and claims to offline runner/staging and strict-result schema paths, preserve all plan artifacts, and return any newly discovered overlap before mutation.
- Dispatch Architecture: Create one visible Codex task whose initial prompt launches one Dev Orchestrator subagent and states the visible root title-and-messaging responsibility.
- Transition Claims: Work Item `start-offline-staging-strict-schema-work-item`; event `198251b6-5468-42f4-92d0-a829582c9d9e`. Provider `start-offline-staging-strict-schema-provider`; event `3172aaa9-ed3c-46e5-8842-b7df75e61c27`.
- Runtime Identity: Pending caller-owned visible task creation. Creation does not imply Running.

## Canonical Runtime Assignment

- Assigned At: 2026-08-13T15:11:59Z.
- Codex Task ID: `019ffbae-1b4f-7f02-99af-5502621100d3`.
- Conversation ID: `019ffbae-1b4f-7f02-99af-5502621100d3`.
- Host: `local`.
- Created At: 2026-08-13T15:11:59Z (`1786633919`).
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Requested Title: `Starting — Reconcile Offline Staging And Strict Result Schema`.
- Initial Action: The visible root starts one Dev Orchestrator subagent for this authoritative Work Item and owns required Codex title and subagent messaging.
- Creation Outcome: Unique direct `threadId` and host success in the saved dev-methodology project, with no client or pending identity and no retry. The UI display ellipsized the requested title without changing its requested value.
- Lifecycle Boundary: This assignment remains `Starting` until the nested Dev Orchestrator accepts and records `Starting -> Running`.
- Adoption Claim: Work Item `adopt-offline-staging-task`; event `8c96c8d6-85f1-4030-b0f5-8ded6d922bf2`.

## Running Acceptance Evidence

- Accepted At: 2026-08-13T15:14:13Z.
- Transition: `Starting -> Running`.
- Root Dev Orchestrator Task: `019ffbae-1b4f-7f02-99af-5502621100d3`.
- Canonical Task/Conversation: `019ffbae-1b4f-7f02-99af-5502621100d3`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Branch: `main`.
- Worktree: `/Users/martinbechard/dev/dev-methodology`.
- Accepted Baseline: `2aa811a9bde3ee0b3f8b204c743ee0287e2e305c`.
- Phase: premise reconciliation and bounded implementation planning.
- Selected Commit Skill: `deliver-work-item-main-branch`.
- Work-Item Claim: `reconcile-offline-staging-strict-schema-work`; event `b0a20c22-1181-4c7c-af0d-b68d4028d318`.
- Provider File Claim: `reconcile-offline-running-provider-file`; event `5a6c253c-a56c-4746-bb37-6b0cf6025725`.
- Backlog Resource Claim: `reconcile-offline-running-backlog-resource`; event `572190af-0ce9-41cc-8441-eb345015d3b1`.
- Overlap Boundary: The active Index lane owns only `index.html`, `scripts/test_documentation_design_system.py`, `scripts/test_bundle_content.py`, and `design/documentation-design-system/assets/design-system.css`. Diagnose and plan only within offline runner staging and strict coordinator-result schema paths. Preserve all unrelated plan artifacts.
