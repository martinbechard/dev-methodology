# Prevent Unsupported Review Findings

Status: Completed

Type: Defect

## Completion Evidence

- Accepted implementation bytes are integrated on main in commit ba86db7712b77a54dba525714ce70156b51f73a9. Its stable patch identity exactly matches accepted candidate commit 8482993557dc98dcfc6bd06ec83f8172d4090b7b.
- The integrated unsupported-review surface is carried by accepted cumulative contribution 8a661aeed49bc1a492263a858de50d156b2a24be, including the structured authority-boundary fixture and its final corrections.
- Focused verification passed 14 unsupported-review tests, and 2 bundle-contract tests passed for the combined candidate. The retained full-candidate evidence remains applicable by exact patch identity.
- Fresh post-integration review of the exact integrated candidate reported no findings.
- Integration ownership for main was released in event dfa15ec8-93d8-45ff-bada-57424517ae2a, and main was clean at 5514063bb51a56cbd8b667bcf49aa34fca329d06 before terminal lifecycle recording began.
- The earlier blocked and exhausted-correction evidence below is historical and superseded by the accepted resumed contribution, verification, integration, and review recorded here.

## Blocked Summary

- Preserved implementation commit: 4a31b337e6baf241de5ec81eb3a3c924096f3c82.
- Preserved correction commits: 68ea9d4d3d493c554dc128476fbc4fb6a2324b4c and 13217749a72467a4379e89ad2dbe9a433ef11ed4.
- Review loop: the bounded two-correction loop is exhausted. The first fresh review failed phrase-only structural coverage. The second fresh review failed visible prewritten and unregistered coverage plus the bundle scenario invariant. The final fresh review failed because evaluate_synthesis.py compares exact copied authority, target, and impact prose, rejects semantic paraphrase, and accepts expected strings without an explicit contradictory observation.
- Integration: no integration occurred.
- Unblock condition: a replacement correction must represent and independently evaluate structured semantic fields for the applicable authority source and location, target source and location, explicit observed contradiction, impact category and meaning, and uncertainty classification. It must accept semantically equivalent wording, reject copied-looking evidence that lacks the contradiction, pass fresh independent review, and then pass governed live target and Judge verification before integration.
- Ordering boundary: prevent-read-only-review-side-effects remains later in the series and untouched.

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
