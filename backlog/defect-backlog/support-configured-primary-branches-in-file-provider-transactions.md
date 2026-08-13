# Support Configured Primary Branches In File Provider Transactions

Status: Starting

Type: Defect

Provider: file

Work Item ID: support-configured-primary-branches-in-file-provider-transactions

Completion: main-branch

## Summary

Allow atomic file-provider creation and lifecycle transactions from a repository's verified canonical primary worktree when its configured primary branch is `master` rather than `main`.

## Context

The Agent-Owned Evaluation Suites work selected file-backed persistence for authorized upstream work in `/Users/martinbechard/dev/py-json-render`. Bounded Project Configurator diagnosis confirmed that repository has no local or remote `main` branch; its primary `master` branch tracks `origin/master`. Git state alone is not provider authority, and current methodology contracts hard-code `main`, so the upstream work remains blocked.

The user explicitly authorized logging this defect and updating the governed file-provider transaction contract. The correction must retain primary-worktree-only authority and must not treat an arbitrary checked-out branch as canonical.

## Requirements

- Define one authoritative way to resolve the repository's configured canonical primary branch.
- Permit atomic file-provider creation and management transactions only from the primary worktree on that verified branch.
- Support both `main` and `master` when each is the verified configured canonical primary branch.
- Replace literal-`main` provider-authority wording in `create-work-item-file`, `manage-work-items-file`, and `commit-file-provider-transaction` with the configured-primary-branch contract.
- Preserve every snapshot, exact-manifest, immutable-commit, rollback, no-overwrite, and unrelated-byte guarantee.
- Do not authorize mutation from a linked worktree, detached HEAD, an unconfigured branch, or Git inference alone.
- Update directly dependent generated projections and focused contract tests mechanically from canonical sources.

## Acceptance Criteria

- A disposable repository whose configured canonical primary branch is `main` may perform the existing atomic file-provider transaction.
- The same transaction succeeds when the configured canonical primary branch is `master` and the primary worktree is on `master`.
- The transaction remains blocked on a branch that is not the configured canonical primary branch.
- The transaction remains blocked from a linked worktree or when provider authority is unset or unverified.
- Creation, lifecycle management, and the shared transaction skill use the same primary-branch rule.
- Existing rollback and unrelated-state preservation tests remain green.
- Generated projections are current and focused tests pass.

## Dependencies

- Backlog blockage crisis epoch `blocked-crisis-20260813T223935Z` must select this recovery item as the sole serial crisis task before source mutation.

## Verification

- Add focused disposable-repository tests for configured `main`, configured `master`, wrong branch, linked worktree, and unset authority.
- Run the exact creation, management, transaction, generated-output, skill-validation, and bundle consumers.
- Run `git diff --check` and obtain fresh independent source review and verification.

## Governed Definition Approval

### Governed Canonical Sources

- `skills/create-work-item-file/SKILL.md`
- `skills/manage-work-items-file/SKILL.md`
- `skills/commit-file-provider-transaction/SKILL.md`

### Allowed Dependent Artifacts

- Mechanically generated skill projections and manifests for the three approved sources.
- Focused tests that directly enforce configured-primary-branch file-provider authority.

### Approval Resolution

Approved by the user's 2026-08-13 instruction to log the defect and update all literal-`main` file-provider transaction references, with regression coverage for `main` and `master` and retained primary-worktree-only authority. No other governed skill or Agent definition is authorized.

## Crisis Recovery Evidence

- Crisis Epoch: `blocked-crisis-20260813T223935Z`.
- Added To Crisis Set: This defect is necessary to resolve `align-agent-owned-evaluation-suites-with-documentation-design-system` and is therefore part of the active crisis set.
- Current Disposition: `Blocked` pending selection as the exactly one serial crisis Work Item task.
- Recovery Owner: Dev Backlog Coordinator.
- Unblock Condition: Select this item as the sole crisis execution, clarify the configured-primary-branch authority source during bounded planning, and complete it without claims.
- No claim operation was used after the epoch's single reset.

## Crisis Starting Handoff

- Reserved At: 2026-08-13T22:46:00Z.
- Transitions: `Blocked -> Ready -> Starting` as two serialized provider decisions in this one committed crisis handoff.
- Crisis Epoch: `blocked-crisis-20260813T223935Z`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Intended Root Role: Dev Orchestrator.
- Canonical Visible Task: Pending unique caller-owned creation.
- Normalized Objective: Correct configured-primary-branch authority for atomic file-provider transactions, supporting verified `main` and `master` while retaining primary-worktree-only authority.
- Baseline: `73638187` on primary `main`.
- Dispatch Boundary: Exactly one separate visible Work Item task is permitted. Its initial prompt starts one Dev Orchestrator collaboration subagent. The crisis task performs all bounded implementation, review, verification, delivery, and provider completion without claims.
- Parallel Boundary: Every other mutating execution remains stopped and preserved. Do not resume Generic Definitions, Specialization, or another recovery item until this Work Item is terminal and cleaned up.
- Claim Policy: No claim operation is permitted during the crisis epoch.
- Next Action: The unique task records `Starting -> Running` without claims before source mutation.

## Notes

- Do not rename the upstream branch as a shortcut.
- Do not infer provider authority solely from `origin/HEAD`, tracking configuration, or the currently checked-out branch.
- Do not broaden this item into delivery-branch naming or ordinary main-branch completion semantics outside file-provider transactions.
