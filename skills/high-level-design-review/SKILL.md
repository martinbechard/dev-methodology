---
type: Skill
name: high-level-design-review
description: Use when reviewing a high-level design artifact for subsystem scope, component collaboration, data contracts, invariants, implementation order, and verification.
---

# High-Level Design Review

Use this skill to review a high-level design artifact created from the methodology templates. A high-level design should explain one coherent subsystem or feature family and how its constituent pieces collaborate.

## Required Inputs

- The high-level design artifact under review.
- The high-level design template from development-methodology assets when available.
- Parent architecture, related modules, source files, tests, configuration, procedures, functional specifications, and wiki pages.

## Workflow

1. Read the artifact and identify subsystem scope, constituent components, interactions, data anchors, invariants, and verification claims.
2. Read references/high-level-design-review-checklist.md.
3. Use documentation-page-verifier for shared page contract, source authority, link, diagram, and steady-state checks.
4. Verify high-level design sections against the checklist, especially parent architecture, data anchors, constituent components, interaction model, lifecycle, contracts, configuration, implementation order, invariants, definition of good, and verification.
5. Return findings first, ordered by severity, with file paths and section names.

## Output

When problems exist, lead with review findings. When no problems are found, say the artifact passes high-level design review and name any remaining subsystem, source, or verification gaps.
