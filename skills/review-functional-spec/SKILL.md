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

For the functional-specification current reverse-engineering pass, accepted architecture and lower-level designs plus source, routes, UI surfaces, commands, jobs, tests, procedures, and runtime evidence are the required inputs. Intentionally absent later wiki pages are not missing mandatory inputs.

## Workflow

1. Read the artifact and identify the actor, workflow, surfaces, states, documentation acceptance, implementation readiness, and verification claims.
2. Read references/review-checklist-functional-spec.md.
3. Complete every applicable checklist question with status, quoted evidence, and assessment.
4. Save the completed review checklist next to the artifact using this form: artifact-name.review-checklist-functional-spec.md.
5. Use documentation-page-verify with the artifact, source evidence, and completed review checklist for shared page contract, source authority, link, diagram, and steady-state checks.
6. Verify functional sections against the checklist, especially actor goal, entry points, workflow steps, states, permissions, edge cases, acceptance behavior, and verification blocks. Perform operation inventory reconciliation across every primary and supporting route, API, command, event, job, notification, and reference-data lookup named by the artifact or authoritative sources.
7. Judge documentation acceptance against source evidence, accepted design prerequisites, and current reverse-engineering pass requirements. Do not fail the artifact solely because later wiki pages are intentionally absent, or because a known defect, unimplemented behavior, open decision, or limitation is recorded accurately.
8. Judge implementation readiness separately. A review may accept the documentation while confirming BLOCKED implementation readiness; preserve the reason for downstream reconciliation and planning.
9. Return findings first, ordered by severity, with file paths and section names. Derive each finding or pass assessment from the completed review checklist.

## Output

When problems exist, lead with review findings. When no documentation-acceptance problems are found, say the artifact passes functional specification review, state its separate implementation-readiness result, and name any remaining behavior, source, decision, or test gaps.
