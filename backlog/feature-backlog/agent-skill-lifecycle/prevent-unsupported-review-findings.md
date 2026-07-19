# Prevent Unsupported Review Findings

Status: Ready

Type: Defect

## Summary

Prevent review synthesis from converting an explicitly unknown policy requirement into a confirmed finding.

## Context

The Dev Code Reviewer executable TypeScript scenario supplied three seeded behavioral defects and no authoritative provenance or copyright-header rule. The target evidence packet correctly classified header wording and provenance authority as unknown. Its final synthesis nevertheless added a fourth confirmed finding stating that the public source required a header and AI attribution.

The independent Judge confirmed complete recall and grounding for the three seeded defects but returned FAIL for precision and uncertainty separation. The unsupported fourth finding violated the scenario rule against treating missing evidence as a confirmed defect. The same failure mode appeared in an earlier rollout before a focused rerun happened not to reproduce it.

The target loaded code-review-evidence, review-structured-artifact, careful-coding, code-comments, TypeScript, TypeScript Strict, and TypeScript ESM. The complete evaluation did not edit those distributed skills.

## Evidence

- evals/agent-tests/dev-code-reviewer/scenarios.yaml defines the seeded-defects scenario and prohibits unsupported findings.
- evals/projects/typescript-code-review contains the frozen candidate, tests, and task authority used by the review.
- evals/agent-tests/results/2026-07-17-complete-agent-suites.md records the independent Judge verdict and retained run evidence.
- The target evidence packet marked provenance and copyright wording unknown before final synthesis promoted the missing header to a confirmed low-priority defect.

## Requirements

- Require every confirmed review finding to cite the authority that makes the observed condition defective.
- Keep unknown, missing, or conflicting policy evidence in questions, residual risk, or missing-evidence sections unless a supplied contract makes it a defect.
- Prevent generic comment or header guidance from creating a repository-specific requirement without applicable authority.
- Require synthesis to preserve the evidence packet classification of fact, uncertainty, and judgment.
- Add deterministic or Judge coverage for the transition from evidence collection to final findings.
- Regenerate affected adapters and documentation from source rather than editing generated definitions directly.

## Acceptance Criteria

- A review with unknown header policy does not report a missing header or provenance statement as a confirmed finding.
- The reviewer may still identify an undocumented public behavioral contract when source evidence establishes concrete user or maintainer impact.
- A confirmed policy finding includes a source-backed applicable rule and tight location evidence.
- Generated Codex review adapters preserve the same evidence-authority boundary.
- The Dev Code Reviewer seeded-defects scenario passes repeatably without adding unsupported findings.
- Repository skill validation, generated-output checks, and unit tests pass.

## Dependencies

None.

## Verification

- Run focused tests for the changed review, code-comment, and structured-review contracts.
- Run Agent Skill validation and every generated-output freshness check.
- Run the Dev Code Reviewer seeded-defects scenario multiple times and inspect evidence packets, final findings, independent Judge verdicts, and cleanup evidence.
- Add a negative fixture where header policy is absent and a positive fixture where an explicit applicable policy requires a header.
- Run repository unit tests and Git diff validation.

## Notes

- Do not suppress evidence-backed documentation defects; suppress only the unsupported promotion of uncertainty into a confirmed requirement.
- Keep material behavioral findings ahead of low-impact documentation observations.
