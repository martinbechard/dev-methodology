---
name: wiki-artifact-reviewer-suite-contract
description: Share the canonical Wiki Artifact Reviewer evaluation contract between its supervisor and independent Judge.
metadata:
  category: evaluation
---

# Wiki Artifact Reviewer Suite Contract

Evaluate the target as a checklist-first reviewer of project-wiki methodology artifacts.

## Required Contract

- Establish target, sources, scope, date, and checklist set before assessment.
- Complete every applicable project-wiki checklist item with status, labeled evidence, and assessment.
- Label checklist evidence as exact quotation, summary, assessment, or not applicable and name its evidence source.
- Apply the shared page verifier to source support, links, editable diagrams, selected format, and steady-state language.
- Check authority, page classes, navigation, local links, update workflow, automation, maintenance, and verification.
- Derive findings from failed or questionable checklist items and lead with severity-ordered corrections.
- Return the completed checklist, verifier assessment, and findings and corrections.

## Exact Quotation Gate

For the source-link-resolution check, resolve every exact quotation against its
named frozen artifact, authority source, checklist, or retained response. Use
the suite-local resolver on the retained review evidence:

```bash
python3 evals/agent-tests/wiki-artifact-reviewer/quotation_traceability.py --review REVIEW_PATH --evidence-root EVIDENCE_ROOT
```

Only CRLF and LF line endings normalize. The literal [omitted] marker may
replace intervening source text when the retained segments occur exactly and in
order. A plausible paraphrase, rewritten punctuation, unnamed source, missing
source, or self-referential sentence absent from the named retained response is
an unsupported exact quotation and a checklist-integrity failure.

Preserve summaries and derived assessments when their Evidence type is clear;
they are not exact quotations. A not-applicable item records a reason and does
not manufacture source text. Preserve an otherwise complete review when an
unrelated link is unresolved, put the link in Open Questions, and block only a
conclusion for which that exact linked evidence is indispensable.

## Failure Conditions

- Write findings before evidence extraction or retrofit a checklist afterward.
- Mark unsupported authority or ownership claims pass.
- Accept an unsupported exact quotation or relabel it after deterministic resolution fails.
- Manufacture criticism for a complete artifact.
- Collapse required corrections, questions, and residual risk into vague prose.
- Modify the artifact during a read-only review.

## Semantic Dimensions

Judge checklist integrity, authority tracing, structural review, source verification, finding quality, uncertainty discipline, and read-only compliance.
