---
name: review-high-level-design
description: Use when reviewing a high-level design artifact for subsystem scope, component collaboration, data contracts, invariants, implementation order, and verification.
metadata:
  category: artifact-review
---

# High-Level Design Review

Use this skill to review a high-level design artifact created from the methodology templates. A high-level design should explain one coherent subsystem or feature family and how its constituent pieces collaborate.

## Required Inputs

- The high-level design artifact under review.
- The high-level design template from development-methodology assets when available.
- Parent architecture, related modules, source files, tests, configuration, procedures, functional specifications, and wiki pages.

## Workflow

1. Read the artifact and identify subsystem scope, constituent components, interactions, data anchors, invariants, and verification claims.
2. Read references/review-checklist-high-level-design.md.
3. Complete every applicable checklist question with status, quoted evidence, and assessment.
4. Save the completed review checklist next to the artifact using this form: artifact-name.review-checklist-high-level-design.md.
5. Use documentation-page-verifier with the artifact, source evidence, and completed review checklist for shared page contract, source authority, link, diagram, and steady-state checks.
6. Verify high-level design sections against the checklist, especially parent architecture, data anchors, constituent components, interaction model, lifecycle, contracts, configuration, implementation order, invariants, definition of good, and verification.
7. Return findings first, ordered by severity, with file paths and section names. Derive each finding or pass assessment from the completed review checklist.

## Output

When problems exist, lead with review findings. When no problems are found, say the artifact passes high-level design review and name any remaining subsystem, source, or verification gaps.
