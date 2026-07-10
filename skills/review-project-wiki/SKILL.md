---
name: review-project-wiki
description: Use when reviewing a project wiki page or project-wiki-template artifact for source authority, wiki structure, maintenance rules, and code-aware navigation.
metadata:
  category: artifact-review
---

# Project Wiki Review

Use this skill to review a project wiki artifact created from the methodology templates. A project wiki page should help future humans and agents find authoritative sources, current understanding, code, tests, open questions, and maintenance obligations without replacing those sources.

## Required Inputs

- The project wiki artifact under review.
- The project wiki template from development-methodology assets when available.
- Related code, tests, procedures, backlog files, source documents, and existing wiki pages.
- Project-specific AGENTS.md or procedure guidance.

## Workflow

1. Read the artifact and identify the wiki page type, source scope, and intended maintenance role.
2. Read references/review-checklist-project-wiki.md.
3. Complete every applicable checklist question with status, quoted evidence, and assessment.
4. Save the completed review checklist next to the artifact using this form: artifact-name.review-checklist-project-wiki.md.
5. Use documentation-page-verifier with the artifact, source evidence, and completed review checklist for shared page contract, source authority, link, diagram, and steady-state checks.
6. Verify project-wiki-specific sections against the checklist, especially authority order, page subclassing, topic pages, code pages, local source links, update workflow, automation, and verification.
7. Return findings first, ordered by severity, with file paths and section names. Derive each finding or pass assessment from the completed review checklist.

## Output

When problems exist, lead with review findings. When no problems are found, say the artifact passes project wiki review and name any remaining source, test, automation, or ownership gaps.
