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
- The authoritative inputs permitted by the artifact's selected design mode. For planned development this means accepted functional specifications, parent architecture, decisions, backlog requirements, project configuration, and relevant technology guidance. For existing behavior it also includes accepted module designs, source, tests, configuration, procedures, and runtime evidence.

## Workflow

1. Read the artifact and identify its design mode, authoritative inputs, requirements coverage, subsystem scope, constituent components, interactions, critical trust and identity boundaries, cross-module contract reconciliation, data anchors, invariants, implementation readiness, and verification claims.
2. Read references/review-checklist-high-level-design.md.
3. Complete every applicable checklist question with status, quoted evidence, and assessment. Use exactly one allowed status: `pass`, `fail`, `question`, or `n/a`; never qualify a status with wording such as `pass with finding`. When a material finding applies, use `fail` or `question` and record any partial strengths in the assessment.
4. Save the completed review checklist next to the artifact using this form: artifact-name.review-checklist-high-level-design.md.
5. Use documentation-page-verify with the artifact, source evidence, and completed review checklist for shared page contract, source authority, link, diagram, and steady-state checks.
6. Verify high-level design sections against the checklist, especially requirements coverage, parent architecture, data anchors, constituent components, interaction model, trust boundaries, identity selectors, authorization, disclosure limits, cross-module contracts, validation and state ownership, transaction and asynchronous boundaries, error timing, configuration, implementation order, invariants, readiness, definition of good, and verification.
7. Return findings first, ordered by severity, with file paths and section names. Separate Response Adequacy findings from Identity And Security findings, then report other contract or evidence findings. Derive each finding or pass assessment from the completed review checklist.

## Output

When problems exist, lead with review findings. When no problems are found, say the artifact passes high-level design review and name any remaining subsystem, source, decision, or verification gaps. Do not pass a planned design with an unaccounted requirement, an unresolved critical contract conflict, or a high-impact blocking question marked READY.
