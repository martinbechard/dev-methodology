# Prevent Read-Only Review Side Effects

Status: Completed

Type: Defect

## Current Execution

- Canonical Dev Orchestrator task: 019f7e76-aea4-7b00-8afa-2ad589baff95.
- Worktree: /Users/martinbechard/.codex/worktrees/954a/dev-methodology.
- Phase: integrated, focused verification passed, and terminal backlog completion committed.

## Completion Evidence

- Accepted private candidate: 5efe1c4 on branch codex/prevent-read-only-review-side-effects in /Users/martinbechard/.codex/worktrees/954a/dev-methodology.
- Independent review: the bounded final cleanup-safety review returned ACCEPT with no material findings after three earlier review-driven correction commits.
- Main integration: candidate commits were patch-equivalently cherry-picked as f55ddb5, f32a313, 2c9db4e, and 4656a4b. No topology-only merge was created.
- Focused post-integration verification: 8 workspace inventory tests and 91 runner tests passed with Python bytecode writes disabled; Git diff validation passed and main was clean.
- Integration claim: integrate-readonly-review-side-effects-019f7e76 acquired at event e4f262d7-7292-47a9-b6d8-b44c2ff2a39b and released at event f2602fc6-3d0b-4157-ba41-26c488bad802.
- Terminal backlog claim: complete-readonly-review-side-effects-019f7e76 acquired for only this active path and completed-defect destination at event 24fe3343-5a86-46e6-b3a0-3e4e567ebaf7; release follows the clean terminal commit.

## Summary

Prevent read-only review agents from leaving generated interpreter artifacts or claiming that no files were created when the final workspace inventory proves otherwise.

## Context

The Dev Code Reviewer incomplete-evidence scenario required read-only analysis. The target correctly withheld a compatibility conclusion because the version-one export and authoritative conversion contract were unavailable. During its evidence work, however, Python execution generated two ignored bytecode files under the fixture. The target then stated that no files were created.

The deterministic mutation gate found both files and the independent Judge returned FAIL. The suite supervisor removed only those generated files and their empty directory, then proved that the final fixture hash and four-file inventory matched the baseline. The complete evaluation did not edit the distributed review or execution skills.

## Evidence

- evals/agent-tests/dev-code-reviewer/scenarios.yaml defines the incomplete-evidence scenario and its read-only mutation boundary.
- evals/projects/python-migration-review contains the frozen source, tests, and incomplete authority packet used by the review.
- evals/agent-tests/results/2026-07-17-complete-agent-suites.md records the independent Judge verdict and retained run evidence.
- The retained scenario checkpoint identifies migration.cpython-311.pyc and test_migration.cpython-311.pyc as the only generated files.

## Requirements

- Make read-only agents run Python evidence collection without writing bytecode into reviewed workspaces.
- Require final mutation claims to be derived from a deterministic tracked and untracked inventory rather than agent recollection.
- Treat ignored generated artifacts as workspace mutations even when tracked-file hashes are unchanged.
- Remove only artifacts generated and owned by the active task when cleanup is necessary.
- Preserve evidence of any detected side effect and cleanup action in the final review result.
- Add deterministic or Judge coverage for false no-mutation claims.
- Regenerate affected adapters and documentation from source rather than editing generated definitions directly.

## Acceptance Criteria

- A read-only review that executes Python does not leave bytecode or cache directories in the reviewed workspace.
- The reviewer never states that no files were created when the final inventory contains task-generated ignored or untracked artifacts.
- Pre-existing ignored and untracked files remain untouched and are reported separately from task-owned side effects.
- Cleanup, when required, names the exact owned artifacts removed and proves that the final inventory matches the baseline.
- The Dev Code Reviewer incomplete-evidence scenario passes repeatably with clean mutation evidence.
- Repository skill validation, generated-output checks, and unit tests pass.

## Dependencies

None.

## Verification

- Run focused tests for the changed review, execution, and evidence-collection contracts.
- Run a read-only Python review with bytecode suppression enabled and verify the exact final inventory.
- Run a negative fixture that deliberately creates ignored bytecode and confirm that the mutation gate and final report expose it.
- Run the Dev Code Reviewer incomplete-evidence scenario multiple times and inspect target evidence, deterministic mutation gates, independent Judge verdicts, and cleanup evidence.
- Run Agent Skill validation, every generated-output freshness check, repository unit tests, and Git diff validation.

## Notes

- Environment-level bytecode suppression is preferable when evidence execution does not require cache files.
- Do not broadly delete cache directories because they may predate the task or belong to another agent.
