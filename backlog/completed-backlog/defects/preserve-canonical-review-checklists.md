# Preserve Canonical Review Checklists

Status: Completed

Type: Defect

## Running Ownership

- Owner: Dev Orchestrator task 019f7e00-7b6e-7db1-a463-5e648ce79f89 under parent Dev Backlog Coordinator task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Lifecycle agent: Dev Backlog Steward.
- Lifecycle claim: preserve-canonical-review-checklists-lifecycle.
- Claim evidence: PRIMARY exact-file backlog ownership acquired at 2026-07-20T00:55:10.289057Z from clean baseline commit 439f638a0c752afa4acae42e3cd9c97eff84e443.
- Scope boundary: this claim owns only the Running transition and primary index resource and is released after its clean commit. Implementation artifacts, tests, review, verification, and integration require a separate canonical isolated claim.

## Execution Record

- Canonical Dev Orchestrator task: 019f7e00-7b6e-7db1-a463-5e648ce79f89
- Branch: accepted source branch codex/baton-8-canonical-checklists-current-main; delivery is integrated on main
- Worktree: /Users/martinbechard/.codex/worktrees/b27c/dev-methodology
- Current phase: Completed
- Accepted candidate commit: 6eede9c3c90526f12bf2442bacbc8c7215f000f6
- Integrated main commit: 2978cb2340c55cb18d4b49c97732d28c152094bd
- Integration or completion wait: None
- Claim attempts: Integration acquired on the first attempt at event 56b884c0-84d4-4f4e-a1a9-f1e3ca7ca774 and released at event 02ac3c1f-8fce-4eb4-ae97-4e51d0bc9023; task-record claim acquired at event 7bb440c7-4905-471d-b0cd-1f8882f30bd5 and released normally at event c10732b5-097e-4558-96ce-4f9e6f38f2d5; terminal work-item claim acquired on the first attempt at event 017135b8-886f-46b0-a701-095ed4a33b60 from clean main commit ac0ddc0900d0bb1b7974d16a6d3c4842b6a79a59
- Open issues: None

## Completion Evidence

- Canonical Dev Orchestrator task 019f7e00-7b6e-7db1-a463-5e648ce79f89 completed this Running item under parent Dev Backlog Coordinator task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- The canonical task record was committed on main as 0e5897a811bf30cd10f94d40c5fb0b95eaf2d18e after task-record claim event 7bb440c7-4905-471d-b0cd-1f8882f30bd5; the unrelated validate-only artifact that initially prevented release was preserved and removed by its owner before normal release event c10732b5-097e-4558-96ce-4f9e6f38f2d5.
- Accepted candidate 6eede9c3c90526f12bf2442bacbc8c7215f000f6 was integrated on main as 2978cb2340c55cb18d4b49c97732d28c152094bd under integration acquisition event 56b884c0-84d4-4f4e-a1a9-f1e3ca7ca774 and clean release event 02ac3c1f-8fce-4eb4-ae97-4e51d0bc9023.
- A fresh independent post-integration review accepted the exact seven integrated paths with no actionable findings or open questions. The reviewer confirmed that all seven current blobs still matched the integrated commit through terminal-claim baseline ac0ddc0900d0bb1b7974d16a6d3c4842b6a79a59.
- The reviewed paths were evals/agent-tests/dev-artifact-reviewer/agents/judge.toml, evals/agent-tests/dev-artifact-reviewer/agents/supervisor.toml, evals/agent-tests/dev-artifact-reviewer/checklist_contract.py, evals/agent-tests/dev-artifact-reviewer/scenarios.yaml, evals/agent-tests/dev-artifact-reviewer/skills/dev-artifact-reviewer-suite-contract/SKILL.md, evals/agent-tests/dev-artifact-reviewer/test_checklist_contract.py, and evals/judges.yaml.
- Suite-local Dev Artifact Reviewer tests passed: 9 tests ran successfully.
- Suite-only validate-only passed for Dev Artifact Reviewer with one job under Python 3.11. The runner wrote its retained summary outside the repository at /private/tmp/preserve-canonical-review-checklists.iwl35I/summary.json and reported one validated suite with one supervisor.
- The default Python 3.9 validate-only attempt exited before runner execution because tomllib was unavailable; rerunning the same focused check with the repository-supported Python 3.11 interpreter passed.
- Global catalog validation passed with CATALOGS VALID.
- The exact suite-contract skill passed scripts/validate-agent-skills.py. The MCP validator could not accept this eval-local path because it is outside the configured installed skill roots, so the repository validator supplied the applicable source validation.
- Git diff validation passed, main status was clean, and the exact seven paths remained byte-identical while unrelated commits advanced main.
- No broad, full, live, browser, generated-output, or complete agent-catalog suite was run during post-integration closeout.

## Summary

Require artifact reviewers to complete every canonical checklist question instead of replacing the checklist with a shorter thematic summary.

## Context

Two Dev Artifact Reviewer scenarios loaded the applicable canonical checklist but rewrote its objective questions into custom thematic items. The material-findings review reduced 36 generic and 25 functional-objective questions to 10 and 14 items. The missing-authority review produced 36 custom questions rather than the 36 canonical structured-review questions.

The resulting reviews identified the important material defect or authority boundary, preserved read-only behavior, and returned the intended readiness direction. They still failed the critical checklist-completeness gate because canonical workflow and correction fields were omitted or replaced. Semantic Judge execution was skipped under the governed critical-failure rule. The complete evaluation did not edit the distributed review skills.

## Evidence

- evals/agent-tests/dev-artifact-reviewer/scenarios.yaml defines canonical checklist completeness as a critical review contract.
- skills/review-structured-artifact and the artifact-specific review skills contain the canonical question sets.
- evals/agent-tests/results/2026-07-17-complete-agent-suites.md records both critical checklist-completeness failures.
- The material-findings target returned 24 thematic items where 61 canonical questions were required.
- The missing-authority target returned 36 custom items while omitting canonical workflow, citation, correction-authority, impact, and severity questions.

## Requirements

- Preserve the identifier, wording, order, and count of every applicable canonical checklist question.
- Complete generic and artifact-specific checklists independently before synthesizing findings.
- Allow additional observations only after the canonical questions are fully represented.
- Prevent thematic grouping from replacing workflow, evidence, correction-authority, impact, or severity fields.
- Treat an unavailable artifact-specific checklist as an authority boundary without rewriting the generic checklist.
- Add deterministic validation that compares the completed question sequence with the canonical source.
- Regenerate affected adapters and documentation from source rather than editing generated definitions directly.

## Acceptance Criteria

- A completed review contains every canonical question exactly once and in source order.
- Generic and artifact-specific question counts match their canonical files.
- A reviewer may summarize results after checklist completion but cannot substitute the summary for checklist evidence.
- Missing specialized authority preserves the complete generic checklist and produces an explicit blocker for the unreviewable dimensions.
- Both Dev Artifact Reviewer scenarios pass their critical checklist-completeness gates repeatably.
- Repository skill validation, generated-output checks, and unit tests pass.

## Dependencies

None.

## Verification

- Run focused tests for structured and artifact-specific review checklist loading and completion.
- Add deterministic comparisons for canonical question identifiers, wording, order, and counts.
- Run the Dev Artifact Reviewer material-findings and missing-authority scenarios multiple times.
- Inspect target checklist evidence, critical gates, independent Judge routing, cleanup, and retained source digests.
- Run Agent Skill validation, every generated-output freshness check, repository unit tests, and Git diff validation.

## Notes

- This requirement does not force unsupported artifact-specific judgments when authority is missing.
- Concision belongs in synthesis, not in destructive compression of the evidence checklist.
