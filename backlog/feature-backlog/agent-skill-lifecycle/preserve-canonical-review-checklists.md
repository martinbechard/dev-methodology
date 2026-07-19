# Preserve Canonical Review Checklists

Status: Ready

Type: Defect

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
