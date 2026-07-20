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
- Each confirmed finding cites applicable authority plus tight contradictory target evidence. Generic skill guidance is not repository-specific authority by itself.
- Confirmed defects, missing evidence, open questions, and residual risk remain separate.
- Final synthesis preserves fact, uncertainty, and judgment classifications. Missing, unknown, or conflicting policy stays outside confirmed findings unless supplied authority establishes the requirement.
- The authority-boundary staging executable creates one immutable candidate workspace from one selected case, rejects evaluator-fixture overlap, excludes oracle files, and emits the only allowed target read root. Target access outside that root is an infrastructure failure.
- Authority-boundary expected results and evaluator code remain outside the target candidate workspace. Finding precision and recall are decided from captured final synthesis by evaluator-owned executable controls.
- Each passing evaluator handoff binds its case and the exact captured synthesis, evaluator, and expectations identities and SHA-256 values. A fresh bound verification of that same handoff is required before Judge dispatch.
- Missing authority appears in exactly one structured openQuestions item, never as a confirmed finding or duplicated residual-risk item.
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
- A missing policy is promoted into a confirmed finding without applicable authority.
- Applicable authority and contradictory target evidence are present but the supported finding is omitted.

## Semantic Dimensions

Judge evidence grounding, finding recall and precision, prioritization, uncertainty separation, correction actionability, and residual-risk clarity.
