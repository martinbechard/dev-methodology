# Reconcile Offline Staging and Strict Result Schema

Status: Ready

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
