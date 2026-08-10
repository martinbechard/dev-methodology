# Reconcile Agent-Skill Hierarchy Category Order

Owner: Unowned

Status: User Action Required

Type: Defect

Provider: file

Work Item ID: reconcile-agent-skill-hierarchy-category-order

Completion: main-branch

## Summary

Reconcile the generated agent-skill hierarchy category order with the repository's authoritative category-order and definitions-page outline contracts.

## Context

Fresh independent review of the agent-and-skill definitions text found that the generated hierarchy presents Development Practice before Wiki And Knowledge. The durable definitions-page outline and design/skill-categories.yaml list Wiki and knowledge skills first, and README.md states that the category file owns category order and display labels.

The hierarchy generator applies a separate HIERARCHY_SKILL_CATEGORY_PRIORITY before the source category order. Its focused test expects the development-first sequence. This disagreement predates the reviewed text candidate and requires generator, generated SVG, outline, or contract work beyond the current text-only correction lane.

## Source Evidence

Dev Artifact Reviewer finding FIND-1 in canonical Codex task 019fe928-e316-7833-bd7d-44af8c0bc89d on 2026-08-10 identified the conflict among design/agent-and-skill-definitions.outline.md, design/skill-categories.yaml, README.md, scripts/build-agent-skill-hierarchy.py, design/agent-skill-hierarchy.svg, and scripts/test_agent_skill_hierarchy.py while reviewing candidate 8726758fb721749928b25436994f77f1e113accf for Work Item review-agent-and-skill-definitions-text.

## Requirements

- Establish one explicit authoritative ordering contract for skill categories in the generated catalog and interactive hierarchy.
- If design/skill-categories.yaml governs both surfaces, remove the conflicting hierarchy-only priority, regenerate design/agent-skill-hierarchy.svg, and update focused assertions.
- If the hierarchy intentionally has a different reading order, document that separate ownership boundary in the definitions-page outline and source guidance, then update conformance tests to enforce both contracts without contradiction.
- Preserve current catalog membership, skill-to-Agent relationships, accessibility text, and interactive behavior.
- Keep page-wide Documentation Design System migration outside this defect.

## Acceptance Criteria

- design/skill-categories.yaml, README.md, the definitions-page outline, the hierarchy generator, the generated SVG, and focused tests state or enforce compatible ordering rules.
- The generated hierarchy matches its declared source order and passes generator freshness checks.
- The definitions-page outline and conformance tests no longer claim one sibling order while the hierarchy enforces another.
- Fresh independent review reports no unresolved category-order authority or source-traceability finding.

## Dependencies

None.

## Verification

- Run the focused hierarchy category-order and definitions-page outline tests.
- Run scripts/build-agent-skill-hierarchy.py with its check option after supported regeneration.
- Run directly affected bundle-content assertions and Git diff checks.
- Compare the generated SVG group order with the accepted authoritative category order.

## Open Questions

- Should the interactive hierarchy follow design/skill-categories.yaml exactly, or should it retain a separately documented development-first reading order?

## User Action Required

This independently identified defect is outside the authorized text-correction lane and needs an explicit disposition before active implementation.

## Question for the User

Do you authorize this category-order defect to enter active backlog work?

## Why User Input Is Required

The current task authorized review and correction of page text. Resolving this defect can change a Python generator, a generated SVG, and a durable outline contract, so the work must not be added to the active queue without separate authority.

## Options and Tradeoffs

- Authorize: Move the item to the defect backlog as Ready and resolve the source-order contract through ordinary delivery.
- Defer: Move the item to Holding without changing the generator, SVG, outline, or tests.
- Decline: Archive the item as Abandoned with this review evidence retained.

## Resolution

Pending.

## Unattended Work Boundary

Do not change the hierarchy generator, generated SVG, category source, outline order contract, or related category-order assertions for this defect until the user authorizes it. The current agent-and-skill definitions text review may continue through its independent correction, verification, delivery, and provider closeout because its candidate does not create this pre-existing conflict.

## Notes

- Related Work Item: review-agent-and-skill-definitions-text.
- The dependent page-design alignment item remains separate.
