# Support Configured Primary Branches In File Provider Transactions

Status: Completed

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

## Canonical Runtime Assignment

- Assigned At: 2026-08-13T22:47:00Z.
- Codex Task ID: `019ffd4d-f252-7e42-a6bc-f13d0c80c30e`.
- Conversation ID: `019ffd4d-f252-7e42-a6bc-f13d0c80c30e`.
- Host: `local`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Task: `/root/backlog_coordinator`.
- Project and Worktree: saved `dev-methodology` project at `/Users/martinbechard/dev/dev-methodology`.
- Creation Outcome: Unique direct ready identity; no client identity, pending ambiguity, retry, or duplicate.
- Requested Title: `Starting — Support Configured Primary Branches In File Provider Transactions`.
- Root Responsibility: The visible task supplies its own Codex title and required nested-execution messaging.
- Lifecycle Boundary: Creation does not imply Running. Provider remains `Starting` until the one nested Dev Orchestrator durably accepts `Starting -> Running` without claims.

## Running Acceptance Evidence

- Transition: `Starting -> Running`.
- Accepted At: 2026-08-13T22:47:26Z.
- Canonical Visible Task: `019ffd4d-f252-7e42-a6bc-f13d0c80c30e`.
- Canonical Conversation: `019ffd4d-f252-7e42-a6bc-f13d0c80c30e`.
- Parent Coordinator Task: `/root`.
- Root Dev Orchestrator: `/root/configured_primary_branches`.
- Delivery Branch: `main`.
- Delivery Worktree: `/Users/martinbechard/dev/dev-methodology`.
- Accepted Baseline: `92a75a791e6f45f33769a29e618951eec77169b1`.
- Phase: Implementation planning accepted.
- Crisis Authority: The active `blocked-crisis-20260813T223935Z` serial exception authorizes exactly this Work Item to mutate without claims.
- Claim Boundary: No claim operation is permitted or performed.
- Accepted Execution Evidence: The canonical visible task launched this one Dev Orchestrator collaboration subagent to execute the complete Work Item.

## Notes

- Do not rename the upstream branch as a shortcut.
- Do not infer provider authority solely from `origin/HEAD`, tracking configuration, or the currently checked-out branch.
- Do not broaden this item into delivery-branch naming or ordinary main-branch completion semantics outside file-provider transactions.

## Running Acceptance And Scope Decision

- Accepted At: 2026-08-13T22:49:00Z.
- Transition: `Starting -> Running` at provider commit `5ac6cb92`.
- Canonical Task and Conversation: `019ffd4d-f252-7e42-a6bc-f13d0c80c30e` on host `local`.
- Root Owner: The task's sole nested Dev Orchestrator.
- Crisis Execution: Exactly one serial work-item execution; no claim operation.
- Decision: Select boundary A. A prose-only contract cannot satisfy the user-authorized requirement to distinguish verified configured `main` or `master` from wrong, unset, linked, detached, or Git-inferred branch state.
- Required Configuration Boundary: Add and validate one explicit canonical-primary-branch configuration value through the existing project configuration source, template, renderer, and directly dependent consumers. Reuse existing configuration infrastructure; do not introduce a second configuration file or infer the value from Git.
- Approved Additional Governed Source: `skills/create-project-configuration/SKILL.md`, only for defining, validating, rendering, and preserving the canonical-primary-branch value required by this defect.
- Approved Additional Dependent Artifacts: `skills/route-documentation-work/assets/templates/project-template.yaml`, directly affected configuration fixtures and focused tests, and mechanically generated projections required by the four approved skill sources.
- Exclusions: Project Bootstrapper and Project Configurator role definitions, delivery skills, runtime adapters unrelated to the approved skill projections, `py-json-render`, and branch rename or remote-default mutation remain excluded unless a concrete implementation finding proves one is unavoidable and returns to the Coordinator before mutation.
- Plan Gate: Correct the existing plan to this boundary and obtain fresh technical acceptance before source mutation. Do not substitute static prose assertions for executable main/master/wrong/unset/worktree behavior.
- Required Runtime Title: `Implementing — Support Configured Primary Branches In File Provider Transactions`.

### Required Future-Ideas Consumer Expansion

- Recorded At: 2026-08-13T22:55:00Z.
- Decision: Approved as the smallest complete boundary. `manage-future-ideas` directly invokes `commit-file-provider-transaction` for capture and promotion and independently hard-codes primary-main authority. Leaving it unchanged would still reject a verified configured `master` before the corrected shared transaction runs.
- Additional Governed Canonical Source: `skills/manage-future-ideas/SKILL.md`, limited to consuming the same verified configured-primary-branch authority contract.
- Additional Dependent Scope: Only directly affected `README.md`, maintained design-contract statements, Future Ideas evaluation/probe assertions, and focused bundle/transaction tests that contain or enforce the obsolete literal-main authority. Mechanically generated projections remain generator-owned.
- Required Behavior: Future Ideas capture and promotion must accept verified configured `main` and `master`, and reject wrong, unset, linked, detached, or Git-inferred authority through the same shared resolver and transaction boundary.
- Exclusions: No change to Future Ideas lifecycle, provider selection, promotion semantics, duplicate rules, record format, or transaction mechanics beyond primary-branch authority.
- Review Gate: Update the authoritative plan with this exact consumer and dependent assertion manifest, then obtain one fresh architecture acceptance before source mutation.

## Completion Evidence

- Transition: `Running -> Completed`.
- Completed At: 2026-08-14T00:12:14Z.
- Completion Selector: `main-branch`.
- Accepted Source Commit: `ba2fe12a0b270326165f811caf7c2c31d4edbc2c`.
- Corrected Integration Commit: `de4005ca81d6f59029a11d25c0ae128b83e29e97`.
- Observed Primary Branch: `main`.
- Observed Delivery Tip: `de4005ca81d6f59029a11d25c0ae128b83e29e97`.
- Reachability: Both accepted commits are ancestors of the observed `main` tip.
- Manifest: The immutable candidate contains exactly 33 authorized paths. The earlier reference to 32 paths was a count error; no path was omitted or unauthorized.
- Architecture Review: Accepted the explicit `workflow_selection.canonical_primary_branch` scalar, existing renderer path, and pre-write authority gate.
- Source Review: Fresh corrected-tip review returned `PASS / GOOD` with no actionable findings.
- Independent Verification: `PASS`; 9 path-limited transaction tests, 23 Future Ideas contract tests, 105 renderer/configuration tests, focused bundle checks, skill validation, YAML parsing, Python compilation, generated-output checks, and `git diff --check` passed.
- Confirmed Issue Disposition: The obsolete `Primary-main-only` design statement was corrected in commit `de4005ca`, then independently re-reviewed and reverified. No issue was excluded.
- Baseline Checks: Four full-bundle failures were independently classified as pre-existing or workspace-only and outside the 33-path candidate.
- Unrelated State: The unstaged terminology-provider record remained byte-for-byte unchanged at SHA-256 `225521d25e131195093cfa182238e0cd7db106721c985bdae773f58d0328a18c`, mode `644`, size `11514`. Unrelated untracked files were preserved.
- Commit Result: `deliver-work-item-main-branch` is `READY`; the accepted corrected commit is already the configured `main` tip with no integration residue.
- Remote Observation: No publication was required by this file-provider Work Item.
- Coordination: Crisis execution completed without any claim operation.
- Archive Destination: `backlog/completed-backlog/defects/support-configured-primary-branches-in-file-provider-transactions.md`.
