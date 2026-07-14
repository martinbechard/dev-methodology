# Migration Report: Design Review Procedure

## Source

- Procedure: [procedure-design-review.md](../procedure-design-review.md)

## Purpose And Scope

This short procedure coordinates a design review: it assigns a review artifact
name and location, requires the legacy checklist and feedback-guideline
procedures, and asks for periodic maintenance of the process.

The live catalog has replaced that generic wrapper with artifact-specific
review skills. Review-architecture, review-high-level-design,
review-module-design, review-functional-spec, and review-project-wiki each
select the relevant checklist, require source evidence, save a completed
checklist beside the target, and derive findings from it. Review-structured is
the generic path for other structured artifacts. The
artifact-review-agent already composes this review family.

## Worthwhile Durable Guidance

- A review needs a durable audit artifact located with the reviewed document.
- A review should use an explicit checklist rather than unstructured opinion.
- Feedback should be constructive, specific, actionable, and tied to the
  reviewed evidence.
- The review process and its templates need occasional maintenance as the
  methodology changes.

## Mapping

| Procedure point | Destination skill(s) or agent(s) | Current coverage | Recommendation |
| --- | --- | --- | --- |
| Conduct design reviews through a standard process | review-architecture; review-high-level-design; review-module-design; review-functional-spec; review-project-wiki; review-structured; artifact-review-agent | Complete | Keep the artifact-specific dispatch model. It is more precise than one generic design-review procedure. |
| Keep a review artifact beside its source design | All artifact-specific review skills; review-structured | Complete | Retain co-location, using each live skill's completed-checklist filename. |
| Name the review document by appending `-review.md` | All review skills | Superseded | Do not restore this convention. Live skills use `artifact-name.review-checklist-<target>.md` and, where applicable, a separate `target-name.review-findings.md`, which distinguishes evidence from conclusions. |
| Apply a standard design-review checklist | Artifact-specific review checklists; review-structured/references/review-checklist-structured.md | Complete | Preserve the required completed-checklist workflow. Use the checklist that matches the artifact level, with review-structured for generic structured artifacts. |
| Apply feedback guidelines | review-structured; artifact-review-agent | Partial | Preserve only the durable feedback discipline: evidence-based, actionable, respectful, severity-ordered findings. See the companion feedback-guidelines migration report for its detailed additions. |
| Review and update the procedure as the practice changes | maintain-methodology-documentation; methodology-maintainer role | Partial | Add a concise catalog-maintenance reminder to the methodology maintenance path: when review workflows or templates change, keep review skills, their checklists, role composition, metadata, tests, README, and design documentation aligned. |

## What Is Already Covered Well

The replacement workflow is stronger than the legacy procedure in several
material ways:

- It separates the completed checklist, which is the audit trail, from the
  concise findings that are derived from it.
- It requires quoted evidence, a status, and an assessment for every
  applicable question rather than merely requiring a review document.
- It selects architecture, high-level-design, module-design, functional-spec,
  or project-wiki criteria according to the target's scope.
- It requires findings first, ordered by severity, and connects each finding
  to a checklist item and target location.
- It uses documentation-page-verifier alongside the artifact-specific review
  skills for shared evidence, source-authority, link, diagram, and
  steady-state checks.

## Missing Or Partial Coverage

The legacy document itself contains little review substance. Its only
independent gap is governance of the review catalog: no currently identified
review skill says explicitly that a change to the review process must be
propagated across the related review skills, checklist references,
review-agent composition, interface metadata, regression tests, README, and
design explanations. That is repository-maintenance guidance, not a
reviewer-facing runtime rule.

The legacy reference to feedback guidance is only partially represented in
the generic review output. Review-structured already requires evidence,
assessments, material findings, severity, targets, and a reason each finding
matters. Its companion procedure report identifies the remaining narrowly
useful additions, such as an action-oriented recommendation and a more
explicit constructive-feedback standard. Those additions belong in
review-structured, not in a new generic design-review skill.

## Obsolete Or Project-Specific Guidance To Omit

- Do not create one `-review.md` document per design as the sole review
  artifact. It collapses evidence, checklist completion, and findings into an
  ambiguous file and conflicts with the live artifact naming contract.
- Do not create a generic design-review checklist or a generic design-review
  skill. It would duplicate the artifact-specific checklists and lose
  architecture-, subsystem-, and module-level distinctions.
- Do not preserve the legacy wiki-link dependency on two procedure files.
  Live skills link directly to versioned bundled checklist references and make
  feedback behavior part of their output contract.
- Do not distribute a vague periodic-review cadence. A team can set cadence
  locally; the portable catalog only needs maintenance triggers when the
  workflow or templates actually change.

## Precise Suggested Additions

### maintain-methodology-documentation/SKILL.md

In the workflow for review-related maintenance, add one concise rule:

> When a review workflow, checklist, or findings contract changes, update all
> affected artifact-specific review skills and reference checklists; verify
> artifact-review-agent composition, relevant role documentation and adapters,
> metadata, README, design HTML, and regression tests remain aligned.

This is a maintenance-routing rule, so it should stay in the maintainer skill
rather than in an end-user review skill.

### review-structured/SKILL.md

Adopt only the feedback additions validated by
[design-review-feedback-guidelines.report.md](design-review-feedback-guidelines.report.md):
require material findings to name a concrete recommendation or decision owner
when the evidence supports one, and phrase findings about the artifact and
its effect rather than about a person. Keep the existing evidence-first,
severity-ordered findings format.

## Skill And Agent Recommendation

No new skill and no new agent are warranted. The procedure is an
obsolete index over a workflow that is now deliberately split across the
existing review skills and artifact-review-agent. Retain only the catalog
maintenance trigger in maintain-methodology-documentation and the narrowly
useful feedback refinements in review-structured.

## Conclusion

Retire the legacy design-review procedure as a portable workflow. Its durable
intent is already covered by the live artifact-specific review stack, with a
clearer evidence model and better scope selection. Do not migrate its generic
filename or cross-procedure-link conventions. The only independent improvement
is a small review-catalog alignment rule for methodology maintainers.
