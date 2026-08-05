---
name: review-structured-artifact
description: |
  Use this skill when reviewing a structured design, plan, architecture,
  rules document, prompt module, or other structured artifact against
  structured inputs or directives. It runs a checklist from a predefined
  template, saves a completed checklist, then derives structured review
  findings from the completed checklist. Use it to check internal logic,
  directive coverage, terminology order, observable decision, evidence, and
  uncertainty quality, concise justification, and whether asserted
  requirements are actually supported by the inputs. It supports a generic
  base checklist first and allows artifact-specific checklist supplements when
  available.
metadata:
  category: artifact-review
---

# Structured Artifact Review

This skill is for reviewing structured artifacts in a deterministic,
inspectable way.

The review happens in two stages:

1. Complete a checklist from a predefined template.
2. Review the completed checklist and extract the important findings.

The completed checklist is the primary audit trail. The findings are a
compressed interpretation of that checklist.

Use a lower-cost model for evidence extraction when the conceptual agent definition assigns that stage to a simple model profile. Use the synthesis model for corrections, severity, and final judgment.

## When this skill applies

Use this skill when the task is one or more of:

- Reviewing a structured design document.
- Reviewing a structured plan or work breakdown structure.
- Checking whether a document applied all structured input directives.
- Checking whether requirements or claims are supported by the inputs.
- Auditing whether a structured document is internally coherent.
- Producing a disciplined review artifact rather than free-form comments.

## Required inputs

Do not start the checklist until you know:

- the review target
- the structured input documents or directives the target is supposed to
  reflect
- the intended review scope if the user constrained it

If the inputs are not already structured, first normalize them enough that
they can be traced during review.

## Bundled references

Always load the generic base checklist:

- references/review-checklist-structured.md

If a more specific checklist exists for the artifact type or technology,
load it in addition to the generic base checklist, not instead of it.

## Output artifacts

By default, write two files next to the review target:

- target-name.review-checklist-structured.md
- target-name.review-findings.md

If the user specifies different output paths, use those instead.

The completed review checklist comes first. The findings file must be derived
from the completed review checklist rather than written as an independent
opinion.

## Review Structured Artifact

### 1. Establish review trace

Before scoring checklist items, record:

- target artifact path
- input artifact paths
- review date
- review scope
- checklist set used

If the target uses structured-design conventions, prefer citing root-level
IDs such as REQ-1, ENTITY-3, or TASK-7. Otherwise cite the clearest
available headings, section names, or file-relative references.

### 2. Complete the checklist

Complete every applicable checklist item with:

- Status: pass, fail, question, or n/a
- Question: the objective question being answered
- Evidence type: exact quotation, summary, assessment, or not applicable
- Evidence source: the named target, input, checklist, or retained response
- Evidence: source text for an exact quotation, or clearly labeled summary or derived assessment text
- Assessment: short judgment grounded in the recorded evidence
- optional note if the item is blocked or uncertain

For every failed or questionable item also record the expected correction, the authority for that expectation, and the practical impact if it remains unresolved.

Do not skip failed items just because they will later appear in findings.
The checklist is the full audit record.

### 2A. Preserve evidence traceability

Use exact quotation only when every retained word and punctuation mark occurs in
the named evidence source. Normalize CRLF and LF line endings for comparison,
but do not rewrite whitespace, words, or punctuation. The literal [omitted]
marker may replace intervening source text only when the text before and after
it occurs exactly and in order.

Label paraphrases and compressed source meaning as summary. Label a judgment
derived from evidence as assessment. Do not put quotation marks around either
one as proof of verbatim support. For n/a, use Evidence type: not applicable
and explain why the question does not apply; do not invent self-referential
checklist or retained-response text to fill an evidence field.

Resolve every exact quotation against its named source before synthesis. If the
source or text cannot be resolved, change the affected item to question or fail
and record the evidence gap. Do not preserve a pass by relabeling unsupported
text after the fact.

### 2B. Separate extraction from synthesis

Evidence extraction records quotes, locations, status, and uncertainty without deciding final severity. Synthesis reconciles conflicting evidence, identifies the correction, and assigns severity from user, correctness, security, data, operability, or maintainability impact. Do not use writing preference alone as severity evidence.

### 2C. Review every sentence

Use documentation-page-verify to review every prose sentence. Apply its three sentence checks to complete claims and instructions in tables and lists as well. Record the results in the completed checklist before extracting findings.

### 3. Review directive coverage

For every structured input directive or requirement that the target was
supposed to apply:

- mark whether it is covered
- cite where it is covered
- mark it fail if it is missing or contradicted

Do not silently forgive omitted directives.

### 3A. Review observable decisions, evidence, and uncertainty

When the target uses structured-design decision records, specifically check
whether:

- the stated decision is clear and authorized by the inputs
- the recorded evidence is observable, traceable, and supports its immediate parent
- material uncertainty is explicit about its impact and how it can be resolved
- BECAUSE remains a concise justification rather than a request for private reasoning
- the artifact reports the reviewable result without requesting or exposing
  hidden reasoning or private deliberation

Record a failed or questionable item when a decision is unsupported, evidence
cannot be inspected, or material uncertainty is omitted. Do not infer private
reasoning to fill an evidence gap.

### 4. Review unsupported assertions

Specifically check for:

- requirements asserted by the target but not supported by the inputs
- design decisions presented as requirements
- claims that rely on implied inputs rather than actual inputs

When one of these appears, record it in the checklist and then elevate it
into findings if it materially affects correctness or reviewability.

### 4A. Review workflow-versus-skill boundaries

When the target is a component design or prompt-chain design, specifically
check whether:

- the component design explains the full workflow rather than only the final
  artifact contract
- skills are treated as compact operational artifacts rather than as the place
  where the whole component workflow is explained
- skills are nested with the prompts or processes that use them when that
  structure is available
- repeated skill usage is handled by reference rather than by duplicated full
  definitions
- a short summary section exists only when it adds real compression value

Record boundary problems in the checklist and elevate them into findings when
they weaken clarity, authority, or maintainability.

### 4AA. Review architecture-versus-component-design scope

When the target is an architecture or component design document, specifically
check whether:

- an architecture document stays focused on system shape, boundaries,
  interactions, responsibilities, and major boundary-shaping technology choices
- an architecture document avoids drifting into low-level implementation detail
  unless that detail is needed to explain a boundary or major tradeoff
- a component design document explains the chosen component or workflow in
  detail rather than silently redesigning the system boundary
- a component design document covers workflow, information flow, constraints,
  definition of good, and test or review checks when those are relevant
- the target does not mix architecture and component design concerns so
  heavily that the reader cannot tell what decisions are already fixed and
  what decisions are still local to the component or process

Record scope-blur problems in the checklist and elevate them into findings when
they weaken correctness, authority, or maintainability.

### 4B. Review writing quality and document completeness

Specifically check whether:

- the document uses plain English, short sentences, and simple words
- jargon, buzzwords, and abstract phrasing are avoided unless clearly needed
- technical terms are defined once when first introduced
- vague words such as robust, seamless, optimize, leverage, and enhance are
  removed or made specific
- the document stays concrete and actionable
- the document includes finality, technical directives, constraints,
  definition of good, and test cases when those sections are relevant to the
  artifact

### 4C. Review section model for component design docs

When the target is a component design document, specifically check whether:

- Finality is used for why the component exists
- Technical Directives is used for implementation-shaping technical choices
  and best-practice rules
- Definition Of Good is used for pass-quality or success conditions
- a top-level Requirements section is only present when it is genuinely the
  right model for that artifact, rather than a default carry-over
- the document does not blur finality, technical directives, and definition of
  good into one mixed section

Record writing-quality, completeness, and section-model problems in the
checklist and elevate them into findings when they weaken clarity,
reviewability, or execution.

### 4CA. Review section model for architecture docs

When the target is an architecture document, specifically check whether:

- Finality is used for why the architecture exists
- System Shape is used for the main parts of the system and their roles
- Boundaries And Interactions is used for real boundaries and interaction
  surfaces, or explicitly says there are none
- Constraints is used for architecture-shaping limits and prohibitions
- Definition Of Good is used for architecture pass conditions
- Test Cases is used only when architecture-level checks are relevant
- the document does not quietly fall back to an ordinary prose outline when it
  claims to use the structured-design skill
- if the target is YAML, the top-level keys stay:
  - finality
  - system_shape
  - boundaries_and_interactions
  - constraints
  - definition_of_good
  - test_cases when relevant
- if the target is YAML, semantic substitutes such as architecture_scope,
  boundary_decision, or technology_choices are treated as section-model
  drift unless the prompt explicitly asked for a different schema

Record architecture-section-model problems in the checklist and elevate them
into findings when they weaken clarity, reviewability, or execution.

### 4D. Review markdown-versus-YAML form

When the target is a YAML structured-design document or a markdown/YAML pair,
specifically check whether:

- markdown remains the authority unless the user explicitly asked for YAML as
  the primary form
- the YAML preserves the markdown document's real section structure
- section names stay as section keys rather than being converted into item
  names
- grouped items such as goals, rules, processes, files, or entities
  remain grouped in YAML
- stable IDs are preserved in the YAML entries
- the YAML avoids generic type fields unless the task explicitly called for
  that style
- the YAML companion is not harder to understand than the markdown authority

Record markdown/YAML mapping defects in the checklist and elevate them into
findings when they distort the source structure or make the artifact harder to
review.

### 5. Extract findings

After the checklist is complete, write the findings file.

The findings file should:

- include only important failures, risks, contradictions, and missing
  directive applications
- order findings by severity
- cite the relevant checklist item IDs
- cite the relevant target location
- say what is wrong and why it matters

If there are no material findings, say so explicitly and still keep the
completed checklist file.

## Checklist discipline

The checklist is not a formality. It is the review method.

- Do not write findings first and retrofit the checklist later.
- Do not collapse several failures into one vague checklist note.
- Do not mark an item pass without evidence.
- Do not mark an item n/a unless the item truly does not apply.
- Use question when the evidence is genuinely ambiguous.

## Findings format

Use this shape for the findings file:

```markdown
# Review Findings: <Target title or filename>

## Scope

- Target: <path>
- Inputs:
  - <path>
  - <path>
- Checklist:
    - review-checklist-structured.md

## Findings

- **FINDING: FIND-1** <short title>
  - **SEVERITY:** critical | high | medium | low
  - **CHECKS:** <check-id>, <check-id>
  - **TARGET:** <root-level id or heading>
  - **SYNOPSIS:** <what is wrong>
  - **BECAUSE:** <why it matters>
```

If there are no material findings:

```markdown
# Review Findings: <Target title or filename>

## Scope

...

## Findings

No material findings.
```

## Generic review priorities

When deciding what becomes a finding, prioritize:

1. missing or contradicted input directives
2. internally inconsistent logic
3. undefined or misordered concepts that create blind spots
4. unclear decisions or decisions not authorized by the inputs
5. evidence that is not observable, traceable, or supportive of its parent
6. material uncertainty that is omitted or does not state its impact and
   resolution path
7. BECAUSE clauses that do not concisely justify their parent
8. requirements that are really solution choices
9. unsupported requirements or claims
10. stale or retired references mixed into active design
11. skill definitions that are detached from the prompts or processes that use
   them
12. design sections that mix finality, technical directives, and definition of
    good in a way that weakens the structure
13. low-value summary sections that repeat the document without adding useful
   compression
14. vague, abstract, or buzzword-heavy wording that hides what the target
    actually requires
15. missing finality, technical directives, constraints, definition of good,
    or test cases when they are needed for the artifact type
16. architecture documents that drift into design-level detail without need
17. component design documents that silently redesign architecture boundaries
18. YAML companions that distort the markdown structure or force a generic
    type schema without justification

## Self-review before returning

Check all of these:

1. The generic checklist template was loaded.
2. The completed checklist exists before findings are written.
3. Every applicable checklist item has a status, Evidence type, Evidence source, evidence, and assessment.
4. Input directives were traced explicitly.
5. Observable decisions are clear and authorized by the inputs.
6. Evidence is inspectable, traceable, and supports the assertion it is nested under.
7. Material uncertainty states its impact and how it can be resolved.
8. BECAUSE remains concise and no review step requests or infers private reasoning.
9. Unsupported requirements or claims were checked explicitly.
10. Workflow-versus-skill boundaries were checked when the target was a
   component or prompt-execution design.
11. Writing quality and document completeness were checked when relevant.
12. The design-doc section model was checked when the target was a design.
13. Findings were derived from failed or questionable checklist items.
14. Findings cite checklist IDs and target locations.
15. The review did not skip the checklist and jump straight to prose.
16. The output artifacts are concise and inspectable.
17. If there were no material findings, the checklist still exists.
18. Every exact quotation resolves against its named source after line-ending normalization and any omission uses the literal [omitted] marker.
19. Summaries, assessments, and not-applicable explanations are not presented as exact quotations.
20. The completed checklist records the shared three-part sentence review from documentation-page-verify.

## Do not

- Do not invent checklist items on the fly when the template already covers
  the issue.
- Do not treat the findings file as the primary artifact.
- Do not silently ignore missing directive coverage.
- Do not accept unsupported requirements just because they sound plausible.
- Do not collapse evidence and judgment into one vague sentence.
- Do not infer or request hidden reasoning to justify a decision.
- Do not ignore vague wording just because the structure looks correct.
