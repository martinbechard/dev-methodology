---
name: functional-spec-review
description: Use when reviewing a functional specification artifact for actor workflow, entry points, states, permissions, acceptance behavior, and verification evidence.
---

# Functional Spec Review

Use this skill to review a functional specification artifact created from the methodology templates. A functional specification should describe observable behavior from the actor's point of view and link the code and tests that support it.

## Required Inputs

- The functional specification under review.
- The functional specification template from development-methodology assets when available.
- Related product notes, source files, tests, routes, UI surfaces, procedures, and wiki pages.

## Workflow

1. Read the artifact and identify the actor, workflow, surfaces, states, and verification claims.
2. Read references/functional-spec-review-checklist.md.
3. Use documentation-page-verifier for shared page contract, source authority, link, diagram, and steady-state checks.
4. Verify functional sections against the checklist, especially actor goal, entry points, workflow steps, states, permissions, edge cases, acceptance behavior, and verification blocks.
5. Return findings first, ordered by severity, with file paths and section names.

## Output

When problems exist, lead with review findings. When no problems are found, say the artifact passes functional specification review and name any remaining behavior, source, or test gaps.
