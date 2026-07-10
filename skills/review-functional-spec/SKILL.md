---
name: review-functional-spec
description: Use when reviewing a functional specification artifact for actor workflow, entry points, states, permissions, acceptance behavior, and verification evidence.
metadata:
  category: artifact-review
---

# Functional Spec Review

Use this skill to review a functional specification artifact created from the methodology templates. A functional specification should describe observable behavior from the actor's point of view and link the code and tests that support it.

## Required Inputs

- The functional specification under review.
- The functional specification template from development-methodology assets when available.
- Related product notes, source files, tests, routes, UI surfaces, procedures, and wiki pages.

## Workflow

1. Read the artifact and identify the actor, workflow, surfaces, states, and verification claims.
2. Read references/review-checklist-functional-spec.md.
3. Complete every applicable checklist question with status, quoted evidence, and assessment.
4. Save the completed review checklist next to the artifact using this form: artifact-name.review-checklist-functional-spec.md.
5. Use documentation-page-verifier with the artifact, source evidence, and completed review checklist for shared page contract, source authority, link, diagram, and steady-state checks.
6. Verify functional sections against the checklist, especially actor goal, entry points, workflow steps, states, permissions, edge cases, acceptance behavior, and verification blocks.
7. Return findings first, ordered by severity, with file paths and section names. Derive each finding or pass assessment from the completed review checklist.

## Output

When problems exist, lead with review findings. When no problems are found, say the artifact passes functional specification review and name any remaining behavior, source, or test gaps.
