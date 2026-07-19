# Require Exact Review Quotation Traceability

Status: Ready

Type: Defect

## Summary

Require every review statement presented as an exact quotation to occur verbatim in the cited source or retained response.

## Context

The Wiki Artifact Reviewer accepted-artifact scenario correctly traced authority, verified the artifact, preserved read-only behavior, and avoided manufacturing findings. Its completed checklist nevertheless presented two self-referential paraphrases as exact quoted evidence. One sentence was attributed to the review basis and another to the completed checklist result, but neither sentence occurred in the retained response.

The deterministic structural gates passed because the expected checklist fields and quotation markers were present. The independent Judge inspected the retained response, found the missing source text, and returned FAIL for checklist integrity. The complete evaluation did not edit the distributed wiki review or documentation verification skills.

## Evidence

- evals/agent-tests/wiki-artifact-reviewer/scenarios.yaml defines the accepted-artifact scenario and exact-evidence contract.
- evals/agent-tests/wiki-artifact-reviewer/fixtures/wiki-artifacts contains the frozen artifact and authority sources used by the review.
- evals/agent-tests/results/2026-07-17-complete-agent-suites.md records the independent Judge verdict and retained run evidence.
- The retained response attributed Checklist set: review-checklist-project-wiki.md to its review basis even though that sentence was absent.
- The retained response attributed All applicable content checks are pass; none is fail or question to its checklist result even though that sentence was absent.

## Requirements

- Distinguish verbatim quotations from summaries, assessments, and derived review conclusions.
- Require a quotation to match the cited source text or retained response exactly, apart from explicitly marked omission.
- Prevent self-referential evidence from citing a sentence that the review never actually emitted.
- Keep checklist status and assessment valid when exact quotation is inapplicable by labeling the evidence as a summary or derived conclusion.
- Add deterministic verification that resolves each cited quotation against its named evidence source.
- Make the independent Judge treat an unsupported exact quotation as a checklist-integrity failure.
- Regenerate affected adapters and documentation from source rather than editing generated definitions directly.

## Acceptance Criteria

- Every phrase labeled as quoted evidence can be found verbatim in the cited artifact, authority source, checklist, or retained response.
- Paraphrased or synthesized evidence is labeled as an assessment or summary and does not use quotation marks as proof of verbatim support.
- A review can record not applicable without inventing self-referential text to satisfy the evidence field.
- Deterministic checks fail when a quotation marker is present but the quoted text is absent from the named source.
- The Wiki Artifact Reviewer accepted-artifact scenario passes repeatably without unsupported quotations.
- Repository skill validation, generated-output checks, and unit tests pass.

## Dependencies

None.

## Verification

- Run focused tests for the changed project-wiki review, structured review, and documentation verification contracts.
- Add a positive fixture with resolvable exact quotations and a negative fixture with plausible but absent paraphrases.
- Run the Wiki Artifact Reviewer accepted-artifact scenario multiple times and inspect completed checklist evidence, deterministic quotation resolution, independent Judge verdicts, and cleanup evidence.
- Run Agent Skill validation, every generated-output freshness check, repository unit tests, and Git diff validation.

## Notes

- The defect concerns evidence labeling, not the accepted artifact decision, which was otherwise source-supported.
- Exact quotation checks should normalize line endings but must not silently rewrite words or punctuation.
