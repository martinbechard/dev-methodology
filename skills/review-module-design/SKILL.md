---
name: review-module-design
description: Use when reviewing a module design artifact for runtime path, responsibilities, contracts, dependencies, processing rules, errors, and verification evidence.
metadata:
  category: artifact-review
---

# Module Design Review

Use this skill to review a module design artifact created from the methodology templates. A module design should define one implementation unit precisely enough that code and tests can be understood or written from it without guessing.

## Required Inputs

- The module design artifact under review.
- The module design template from development-methodology assets when available.
- The module source, callers, dependencies, tests, configuration, parent design documents, procedures, and related wiki pages.

## Workflow

1. Read the artifact and identify runtime path, responsibility, callers, dependencies, contracts, internal state, processing rules, error handling, and verification claims.
2. Read references/review-checklist-module-design.md.
3. Complete every applicable checklist question with status, quoted evidence, and assessment.
4. Save the completed review checklist next to the artifact using this form: artifact-name.review-checklist-module-design.md.
5. Use documentation-page-verify with the artifact, source evidence, and completed review checklist for shared page contract, source authority, link, diagram, and steady-state checks.
6. Verify module sections against the checklist, especially purpose, runtime path, responsibilities, callers, dependencies, public contracts, internal data, processing rules, invariants, configuration, external interfaces, UI behavior, errors, and verification.
7. Return findings first, ordered by severity, with file paths and section names. Derive each finding or pass assessment from the completed review checklist.

## Output

When problems exist, lead with review findings. When no problems are found, say the artifact passes module design review and name any remaining source, contract, or test gaps.
