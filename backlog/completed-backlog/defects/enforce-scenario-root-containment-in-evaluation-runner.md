# Enforce Scenario-Root Containment In Evaluation Runner

Status: Completed

Type: Defect

Owner: Dev Orchestrator

Provider: file

Provider Reference: backlog/completed-backlog/defects/enforce-scenario-root-containment-in-evaluation-runner.md

Completion: direct-main

## Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Canonical Thread/Task: 019f97d7-41ce-7763-a8fc-75f1be68a82d
- Reservation: One parent-owned launch reservation for this higher-risk runner defect.
- Intended Root Role: Dev Orchestrator
- Phase: Root acceptance recorded; implementation may begin in the isolated checkout.
- Dispatched At: 2026-07-25T05:54:12Z
- Task Creation Boundary: The parent will create exactly one canonical task immediately after this durable reservation. Its identity will be recorded only by that task's own Starting -> Running transaction.

## Coordination Evidence

- Reservation Backlog Claim: reserve-runner-scenario-root-containment-019f95a9 acquired on primary main at 2026-07-25T05:54:12.371610Z; acquisition journal event bbff5d22-5707-4346-9ccb-dd80e47a572c.
- Running Backlog Claim: 019f97d7-scenario-root-running-backlog acquired on primary main at 2026-07-25T05:56:32.870561Z; acquisition journal event b8d7d398-7e0c-4c5e-9fc0-aad704295d63.

## Running Acceptance

- Accepted Root Identity: Dev Orchestrator task 019f97d7-41ce-7763-a8fc-75f1be68a82d.
- Branch: detached at 1c19d95cc2f361953b91119db71919216fe9d974.
- Worktree: /Users/martinbechard/.codex/worktrees/1e13/dev-methodology.
- Phase: Scenario-root containment implementation and focused regression planning.
- Started At: 2026-07-25T05:56:32.870561Z.

## Accepted Integration Candidate

- Candidate Commit: `81a2c556344a35b57493f552af9417f1a7faee9c`.
- Source Branch: `codex/enforce-scenario-root-containment-019f97d7`.
- Clean Source Worktree: `/Users/martinbechard/.codex/worktrees/1e13/dev-methodology`.
- Phase: Ready for direct-main integration. Status remains Running and ownership remains with Dev Orchestrator until that integration and its later lifecycle evidence are complete.
- Fresh Security Review: ACCEPTED with no findings.
- Fresh Code Review: ACCEPTED with no findings.
- Independent Verification: VERIFIED/PASS for focused Python 3.11 containment, Junie, handoff, and authority tests.
- Additional Validation: Validation-only pass, compile pass, and diff-hygiene pass.
- Baseline Caveats: Unrelated Playwright and catalog baseline caveats remain outside this candidate's scope.
- Distinct Follow-up: Catalog-path containment is separately recorded at `backlog/defect-backlog/enforce-suite-catalog-path-containment-in-evaluation-runner.md` in commit `0a3b8b2a`; it remains outside this item's scope.

## Completion Evidence

- Completed At: 2026-07-25T06:38:01Z.
- Accepted delivery source: `81a2c556344a35b57493f552af9417f1a7faee9c` on `codex/enforce-scenario-root-containment-019f97d7`. Its source worktree was clean.
- Direct-main integration: `8b7db47d75bad03bdfffd78102705160e8a67894`, an exact non-ancestral replay of the accepted source on parent `587955ccd1e8011b7f7722a41a190a0c79dd9015`. The four owned source and integration blobs are identical, and the integration commit is reachable from main.
- Fresh independent security review: ACCEPTED with no findings. Fresh independent code review: ACCEPTED with no findings. Independent verification: VERIFIED/PASS.
- Post-main checks passed: 10 focused Python 3.11 containment, Junie, handoff, and authority tests; header-policy validation-only; py_compile; changed SKILL.md backtick scan; and `git diff --check`.
- Integration claim `integrate-scenario-containment-019f97d7` acquired at event `2f1c6a68-c9c3-437a-a9e9-8d916c52d945` and released at event `80e65ac1-70c9-474c-8774-691f9ae2b097`; the live registry was empty after release.
- Completion reconciliation observed clean primary main at `680780c4c105666f131ee306932659cc7d4227cb`, with the integration commit reachable. No remote publication is configured or required.
- Provider closure claim `close-scenario-root-containment-019f97d7` acquired primary backlog ownership at event `e099a2f6-e00a-4174-ae51-0272fbc32839` before this archive transition.

## Summary

Constrain evaluation-runner scenario roots to the canonical fixture root so untrusted suite or scenario identifiers cannot traverse through paths or symlinks into external Git metadata, expensive trees, or unrelated workspace state.

## Context

Pre-existing raw scenario identifiers have no safe path-component validation. Scenario audit roots can resolve or traverse outside the canonical fixture root through path escape or symlink escape. Fresh security review confirmed a risk of outside-workspace Git metadata probing, expensive traversal, and false evaluation failures. This defect is distinct from candidate-only none-audit bypasses and records current-main behavior only.

## Source Evidence

- Canonical user direction in task `019f979e-5330-7501-8340-92dfd593f6ef` requires every additional confirmed distinct defect to be logged durably.
- Fresh security review of the evaluation runner confirmed raw suite/scenario identifiers can influence scenario audit-root resolution without safe component validation.
- The review established path-traversal and symlink-escape routes outside the canonical fixture root.

## Requirements

- Validate suite and scenario identifiers as safe path components before any scenario-root construction.
- Precreate canonical scenario roots and reject roots that are symlinks.
- Enforce canonical fixture-root containment before execution and again after execution or audit-root resolution.
- Keep legitimate fixture scenarios runnable without probing unrelated workspace state.

## Acceptance Criteria

- Suite and scenario slugs that contain traversal, separators, absolute-path forms, or invalid components are rejected before filesystem probing outside the canonical fixture root.
- Canonical scenario roots are precreated as non-symlink directories.
- Resolved audit roots remain contained by the canonical fixture root before and after execution.
- Regression tests reject traversal and symlink escapes without outside-workspace Git metadata probing or expensive traversal.
- Valid in-root scenarios continue to pass their focused evaluation tests.

## Dependencies

None.

## Verification

- Run focused evaluation-runner scenario-root and audit tests.
- Add and run traversal, absolute-path, separator, and symlink-escape regressions.
- Verify valid fixture scenarios retain their expected results.
- Run `git diff --check` and obtain fresh independent security and code review.

## Open Questions

- Is the existing suite schema the narrowest authoritative place to define the portable suite and scenario slug grammar?

## Coordination Evidence

- Backlog claim `record-runner-review-defects-019f979e` acquired on primary main at 2026-07-25T05:39:43.871470Z; acquisition journal event `29dc95c6-c2ba-473b-8034-3420d7eecd6b`.

## Notes

This item is ready for independently scoped implementation. It does not authorize unrelated runner changes or governed-definition mutation without required approval evidence.
