# Reconcile Agent-Skill Hierarchy Category Order

Owner: Unowned pending accepted execution

Status: Starting

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

Asked At: 2026-08-10T01:44:01Z

Asked In: Parent coordination task 019fb057-1767-7ef2-b5fa-41f4417b20b3

## Why User Input Is Required

The current task authorized review and correction of page text. Resolving this defect can change a Python generator, a generated SVG, and a durable outline contract, so the work must not be added to the active queue without separate authority.

## Options and Tradeoffs

- Authorize: Move the item to the defect backlog as Ready and resolve the source-order contract through ordinary delivery.
- Defer: Move the item to Holding without changing the generator, SVG, outline, or tests.
- Decline: Archive the item as Abandoned with this review evidence retained.

## Resolution

Approved by the user on 2026-08-10 in parent coordination task 019fb057-1767-7ef2-b5fa-41f4417b20b3. The user confirmed that the generator and related tools may be updated where necessary.

## Unattended Work Boundary

Authorization is satisfied. Dispatch remains sequential: do not start this item until the currently running SOLO crisis work item reaches a terminal outcome.

## Notes

- Related Work Item: review-agent-and-skill-definitions-text.
- The dependent page-design alignment item remains separate.

## Starting Handoff Evidence

Starting Recorded At: 2026-08-11T20:21:30Z

Coordinator: Codex task 019ff271-bb29-7cd2-95da-7b4b9766a1e6

Normalized Objective: Establish and implement one source-backed category-order contract across the hierarchy generator, generated hierarchy, definitions outline, README guidance, and focused assertions while preserving catalog membership, accessibility, and interactive behavior; then complete independent review, verification, main-branch delivery, provider closure, and cleanup.

Intended Root Role: Dev Orchestrator

Launch Result: Requested

Canonical Execution: None

Last Contact At: 2026-08-11T20:21:30Z

Next Reconciliation At: 2026-08-11T20:36:30Z
