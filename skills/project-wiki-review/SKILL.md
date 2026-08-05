---
name: project-wiki-review
description: Use when reviewing a project wiki page or project-wiki-template artifact for source authority, wiki structure, maintenance rules, and code-aware navigation.
metadata:
  category: wiki-and-knowledge
---

# Project Wiki Review

Use this skill to review a project wiki artifact created from the methodology templates. A project wiki page should help future humans and agents find authoritative sources, current understanding, code, tests, open questions, and maintenance obligations without replacing those sources.

## Required Inputs

- The project wiki artifact under review.
- The project wiki template from route-documentation-work assets when available.
- Related code, tests, procedures, backlog files, source documents, and existing wiki pages.
- Applicable project-specific guidance already present in the task context.

## Workflow

1. Read the artifact and identify the wiki page type, source scope, and intended maintenance role.
2. Read references/review-checklist-project-wiki.md.
3. Complete every applicable checklist question with status, Evidence type, Evidence source, evidence, and assessment. Use exact quotation only for verbatim source text. Use summary for paraphrase, assessment for a derived judgment, and not applicable with a reason when exact evidence does not apply.
4. Save the completed review checklist next to the artifact using this form: artifact-name.review-checklist-project-wiki.md.
5. Resolve each exact quotation against its named artifact, authority source, checklist, or retained response. Normalize CRLF and LF line endings only. Permit the literal [omitted] marker only when the retained source segments occur exactly and in order; do not rewrite words or punctuation.
6. Use verify-documentation-page with the artifact, source evidence, and completed review checklist for shared page contract, source authority, link, diagram, and steady-state checks.
7. Verify project-wiki-specific sections against the checklist, especially authority order, page subclassing, topic pages, code pages, local source links, update workflow, automation, and verification.
8. Return findings first, ordered by severity, with file paths and section names. Derive each finding or pass assessment from the completed review checklist.

Do not cite a self-referential sentence as exact evidence unless that sentence
actually occurs in the named completed checklist or retained response. An
unsupported exact quotation is a checklist-integrity failure. A summary or
assessment may support a valid status when its label makes clear that it is not
verbatim evidence.

## Output

When problems exist, lead with review findings. When no problems are found, say the artifact passes project wiki review and name any remaining source, test, automation, or ownership gaps.
