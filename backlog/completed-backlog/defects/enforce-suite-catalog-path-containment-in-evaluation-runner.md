# Enforce Suite-Catalog Path Containment In Evaluation Runner

Status: Completed

Type: Defect

Owner: Dev Orchestrator

Provider: file

Provider Reference: backlog/completed-backlog/defects/enforce-suite-catalog-path-containment-in-evaluation-runner.md

Completion: direct-main

## Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Canonical Thread/Task: 019f9801-cef3-7e61-a8db-939dd6912763
- Reservation: One parent-owned launch reservation for the selected higher-risk runner item.
- Intended Root Role: Dev Orchestrator
- Isolated Checkout: /Users/martinbechard/.codex/worktrees/97a9/dev-methodology
- Reservation Commit: eb1bc29bf48e4fb72a58e36f3e70f01d49352104
- Prior Reservation Claim: a44afa80-b0a5-407d-9b83-dcf20ff5d842, released before this lifecycle transition.
- Phase: Running.
- Dispatched At: 2026-07-25T06:40:40Z

## Execution Identity

- Canonical Thread/Task: 019f9801-cef3-7e61-a8db-939dd6912763
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Root Role: Dev Orchestrator
- Worktree: /Users/martinbechard/.codex/worktrees/97a9/dev-methodology
- Started At: 2026-07-25T06:42:55Z

## Coordination Evidence

- Reservation Backlog Claim: reserve-runner-suite-catalog-containment-019f95a9 acquired on primary main at 2026-07-25T06:40:40.196731Z; acquisition journal event 92fdfab9-ec67-428c-bba2-5ed873f50900.

## Completion Evidence

- Completed At: 2026-07-25T07:05:32Z.
- Canonical task: `019f9801-cef3-7e61-a8db-939dd6912763`; parent coordination thread: `019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a`.
- Starting -> Running transition: `f88312697e0522adbb39d3b59d897fefc1b9b8e1`.
- Accepted delivery source: `ab0c78fcadd9fef3786b7236c666aee7d79aff09`, following implementation commits `705bb916` and `ab0c78fc`. The implementation claims were normally released: initial final release `edd39482-3f72-4287-93ee-153f8c7395ee`; correction acquisition `dafbfb13-0682-4ce6-8e9c-0370213f1cfe` and release `516bc07b-dd18-49b7-afe2-df08eef6d93d`.
- Fresh independent code review: GOOD. Fresh independent security review: GOOD after the endpoint-link correction. Independent verification: PASS with 11 focused containment/scenario tests plus 2 additional scenario-root tests, Codex/Junie selected-list and validate-only checks, compile, diff, and clean-worktree evidence.
- Direct-main integration: `c7ed6ade3ea347245a8f7a3e1a09a16202bbfa1f`; the accepted source is graph-reachable. Integration claim `integrate-suite-catalog-containment-019f9801` acquired at event `3b1ed960-8eef-4812-921c-8ebc6cee4433` and released at event `2ff848fd-e7d2-48ce-8f10-1177ab33a227`.
- Post-integration checks passed: six focused tests, compile, selected dev-code-reviewer Codex/Junie list, diff, reachability, and clean-main checks.
- Scoped baseline and omission record: the full runner has the same 13 Playwright-unavailable failures as base; the full scripts suite has five role-mutation failures that map to active defect `decouple-dev-backlog-steward-contract-from-unconditional-claim-evidence.md`; the dev-coder native-skill mismatch is separately logged at `reconcile-dev-coder-native-skill-binding-with-suite-manifest.md` and is not absorbed here.
- Scope protection: `enforce-agent-claim-lifecycle-evidence-in-runner-resource-scenarios.md` remains active, outside this item’s scope, and unchanged.
- Provider closure claim `close-suite-catalog-containment-019f9801` acquired primary backlog ownership at event `3f5a3b9f-2630-4410-a54b-887be99bd5e7` before this archive transition.

## Summary

Reject a suite-index path that is not a contained, non-symlink suite directory before the evaluation runner probes suite.yaml or scenarios.yaml outside the canonical suite root.

## Context

The evaluation runner validates selected suite IDs but _load_catalog joins each raw suite-index.yaml entry path directly to its suite root and then loads suite.yaml and scenarios.yaml. A safe suite ID paired with path: ../outside therefore makes the runner probe outside the suite root. This is a catalog-entry path-resolution defect, not the active suite/scenario identifier and scenario-audit-root containment defect.

## Source Evidence

Delegated user direction in canonical task 019f97d7-41ce-7763-a8fc-75f1be68a82d explicitly requires every additional confirmed distinct defect to be logged durably rather than as a warning. Fresh inspection of evals/agent-tests/runner.py confirms that _load_catalog validates IDs at lines 354 through 365, joins the raw entry path at line 366, and loads suite.yaml and scenarios.yaml at lines 367 and 368 without containment validation.

## Requirements

- Validate every suite-index entry path before constructing a suite manifest or scenario-catalog path.
- Reject traversal, absolute, empty, malformed, or resolved paths that escape the canonical suite root.
- Reject a suite path that resolves through a symlink outside the canonical suite root.
- Ensure rejection occurs before any filesystem probe of suite.yaml or scenarios.yaml outside the canonical suite root.
- Preserve loading of valid contained suite directories.

## Acceptance Criteria

- A valid suite ID paired with path: ../outside is rejected before any outside-root suite.yaml or scenarios.yaml probe.
- Absolute, separator-based traversal, and malformed catalog paths are rejected before an outside-root probe.
- A catalog path whose resolved directory escapes through a symlink is rejected before an outside-root probe.
- Valid suite-index entries whose resolved directories remain inside the canonical suite root continue to load and validate.
- Focused regressions prove rejection-before-probe and resolution containment for traversal and symlink cases.

## Dependencies

None.

## Verification

- Add focused evals/agent-tests/test_runner.py regressions using a temporary suite root and an instrumented loader or equivalent evidence that no outside-root manifest or scenario-catalog path is read.
- Run the focused evaluation-runner catalog-loading regressions.
- Run git diff --check.
- Obtain independent code and security review of the containment boundary.

## Open Questions

None.

## Notes

Coordinate any shared evals/agent-tests/runner.py ownership with backlog/defect-backlog/enforce-scenario-root-containment-in-evaluation-runner.md. This item must remain a separate delivery: it governs raw suite-index path resolution, while that active item governs suite/scenario identifiers and scenario audit roots. This transaction records the defect only and does not implement the runner change.
