---
name: dev-code-reviewer-suite-contract
description: Share the canonical Dev Code Reviewer evaluation contract between its suite supervisor and independent Judge.
metadata:
  category: development-practice
---

# Dev Code Reviewer Suite Contract

Evaluate the Dev Code Reviewer as an evidence-first defect detector with a read-only default.

## Required Contract

- Evidence extraction precedes finding synthesis.
- Each finding identifies a material defect, its impact, and the smallest useful file location.
- Confirmed defects, missing evidence, open questions, and residual risk remain separate.
- The review checks regressions, tests, verification, abstraction safety, applicable rules, comments, and documentation drift without adding style-only noise.
- Applicable rules include the frozen instructions of skills assigned by the canonical reviewer definition; the Judge packet must include the excerpts governing any rule-based finding.
- The product change remains unmodified unless the request explicitly asks to save a separate review artifact.
- The result includes the completed evidence packet, prioritized findings, file references, open questions, and residual risk.

## Failure Conditions

- The reviewer edits the candidate to make the review pass.
- A claim is presented as a finding without source, test, trace, or contract evidence.
- A seeded material defect is missed while lower-value style feedback is emphasized.
- Missing runtime evidence is mislabeled as proof of correctness or failure.
- A clean change receives a manufactured finding unsupported by impact.

## Semantic Dimensions

Judge evidence grounding, finding recall and precision, prioritization, uncertainty separation, correction actionability, and residual-risk clarity.
