---
name: review-unit-test-plan
description: Use when reviewing a unit test plan for source authority, behavior coverage, boundary contracts, scenario precision, failure coverage, traceability, and implementation independence.
metadata:
  category: artifact-review
---

# Review Unit Test Plan

## Workflow

1. Read the plan, its authoritative behavior or design sources, relevant implementation, dependencies, and existing tests.
2. Read references/review-checklist-unit-test-plan.md.
3. Complete every applicable checklist question with status, question, Evidence type, Evidence source, evidence, and assessment. Use exact quotation for verbatim source text, summary for paraphrased source meaning, assessment for a derived finding, and not applicable with a reason when the question does not apply.
4. Save the checklist next to the plan using artifact-name.review-checklist-unit-test-plan.md.
5. Resolve every exact quotation against its named source before synthesis. If the named source or text cannot be resolved, mark the item question or fail and record the evidence gap instead of preserving a pass.
6. Use documentation-page-verify with the plan, source evidence, and completed review checklist.
7. Return findings first, ordered by impact, and derive every finding or pass assessment from the completed checklist.

Keep detailed language, framework, mocking, and persistence rules in the applicable coding skills and their code-review checklists.
