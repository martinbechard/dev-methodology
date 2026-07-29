# Restore Agent And Skill Definitions Outline And Simplify Diagrams

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/restore-agent-and-skill-definitions-outline-and-diagram.md

Completion: direct-main

## Summary

Restore the intended structure of the Conceptual Agent and Skill Definitions documentation, make that structure durable in a tree-form outline contract, place Dev Activities before Backlog Management in both generated views, and remove the redundant backlog-focus and wiring-map surfaces.

## Context

The completed document-topic revision changed design/agent-and-skill-definitions.html so Conceptual Agent Definitions and Skill Definitions precede Agent-Skill Relationships, and it retained no standalone outline artifact. The current user-directed order requires Agent-Skill Relationships before Conceptual Agent Definitions.

The generated cards and design/agent-skill-hierarchy.svg currently place Backlog Management before Dev Activities because design/role-catalog-groups.yaml lists that catalog group first. The hierarchy generator also adds a Focus backlog management control, and the definitions page contains a paragraph explaining that control.

The page additionally links to design/agent-skill-explorer.html as a separate wiring map. That wiring-map surface has its own browser script, generated data, tests, support-checklist generation path, and README references. The requested documentation model retains the interactive agent-to-skill hierarchy and removes the separate wiring map.

## Source Evidence

Direct user request in Codex task 019fae77-d530-7361-b1c6-36f87f3d6e28 on 2026-07-29 identified unwanted changes to design/agent-and-skill-definitions.html and directed all of the following:

- Move Agent-Skill Relationships before Conceptual Agent Definitions.
- Create design/agent-and-skill-definitions.outline.md as a directory-tree-style outline and add a directive requiring the HTML documentation to follow it.
- Place Agents for Backlog Management after Agents for Dev Activities in the cards and graph.
- Remove the paragraph beginning "Use Focus backlog management".
- Remove the Focus backlog management diagram control.
- Remove the link to the wiring map and remove the wiring map itself, retaining only the agent-to-skill diagram.

Repository evidence confirms the current section order, catalog-group order, focus paragraph and control, wiring-map link, standalone explorer assets, and generator/test ownership described above.

## Requirements

- Move the complete Agent-Skill Relationships section before the complete Conceptual Agent Definitions section in design/agent-and-skill-definitions.html.
- Preserve the relationship section's interactive agent-to-skill hierarchy, explanatory legend, accessible object fallback, selection behavior, and agent-dependency display except for the explicitly removed backlog-focus behavior.
- Create design/agent-and-skill-definitions.outline.md.
- Put the complete intended page outline in that file using a directory-tree presentation.
- Include this normative directive in the outline file: design/agent-and-skill-definitions.html and its generated catalog and diagram surfaces must follow this outline and sibling order. Any intentional structural change must update the outline and its conformance tests in the same accepted change.
- Make the durable outline contain at least this exact ordered structure:

```text
Conceptual Agent and Skill Definitions
├── Conceptual Definition Scope
├── Agent-Skill Relationships
│   └── Interactive Agent And Skill Map
├── Conceptual Agent Definitions
│   ├── Agents for Dev Activities
│   ├── Agents for Backlog Management
│   ├── Agents for Wiki Activities
│   ├── Agents for Project Setup
│   └── Agents for Methodology Maintenance
├── Skill Definitions
│   └── Generated Skill Catalog
│       ├── Wiki and knowledge skills
│       ├── Documentation methodology skills
│       ├── Artifact creation skills
│       ├── Artifact review skills
│       ├── Development practice skills
│       ├── Design pattern skills
│       └── Stack and domain skills
├── Project-Selected Delivery and Technology Bindings
├── Provider-Independent Dev Coder Inputs
└── Work-Item Delivery Responsibilities
    ├── Delivery Workflow
    ├── Persistence Selection
    └── Codex Multi-Item Coordination
```

- Enforce the outline with focused tests that compare the HTML section order and the generated catalog and diagram group order with the durable outline contract.
- Change the shared role-catalog group order so Dev Activities precedes Backlog Management while preserving the remaining catalog-group order.
- Regenerate the card data and agent-to-skill hierarchy so both views display Agents for Dev Activities before Agents for Backlog Management.
- Remove the complete paragraph beginning "Use Focus backlog management" from design/agent-and-skill-definitions.html.
- Remove the Focus backlog management control and all dedicated focus-role constants, styling, script behavior, accessibility state, and tests from the hierarchy generator and generated SVG.
- Keep ordinary agent and skill selection, reset, dependency visibility, and accessible interaction in the hierarchy.
- Remove the wiring-map link from design/agent-and-skill-definitions.html.
- Retire the standalone wiring-map page, browser script, generated explorer data, dedicated tests, generation path, README references, and other repository references that exist only to support that map.
- Preserve the agent, skill, technology, and test coverage checklist; relocate any valid coverage assertions that currently depend on the wiring-map data to authoritative catalogs or the checklist model instead of discarding their semantic coverage.
- Remove broken links, stale generation outputs, stale checks, and obsolete documentation created by retiring the wiring map.
- Do not modify conceptual agent definitions or distributed skill definitions as part of this defect.

## Acceptance Criteria

- Agent-Skill Relationships appears before Conceptual Agent Definitions in the rendered page and source order.
- design/agent-and-skill-definitions.outline.md exists, uses a directory-tree outline, contains the required directive, and matches the rendered section hierarchy.
- The generated cards list Agents for Dev Activities before Agents for Backlog Management.
- The generated agent-to-skill hierarchy lists the Dev Activities group before the Backlog Management group.
- The specified Focus backlog management explanatory paragraph does not appear.
- The Focus backlog management button, focus-only styling, script behavior, accessible state, and generator/test contract do not exist.
- The definitions page contains the agent-to-skill hierarchy and no link to a separate wiring map.
- The standalone wiring-map page, its dedicated browser script, generated explorer data, and wiring-map-only generation and test surfaces no longer exist.
- No README, design page, script, generated output, or test links to or requires the retired wiring map.
- The retained hierarchy remains keyboard operable, preserves accurate agent-to-skill relationships, and passes generator freshness checks.
- The coverage checklist and its valid evidence-boundary assertions remain current and tested without relying on retired wiring-map data.
- Focused outline-conformance tests fail when the relationship section moves after agent definitions or when Backlog Management moves before Dev Activities.

## Dependencies

None.

## Verification

- Add focused positive and negative outline-conformance tests for section order, catalog-group order, hierarchy-group order, and outline drift.
- Run scripts/build-skill-docs.py and scripts/build-agent-skill-hierarchy.py with their freshness checks.
- Run directly affected bundle-content, hierarchy, support-checklist, coverage-catalog, effective-communication, and STE documentation tests after removing wiring-map dependencies.
- Search the repository for the removed focus text, control identifiers, wiring-map filenames, generated schema, and links; require no unintended references.
- Run documentation link, markup, accessibility, and generated-output checks for the retained definitions page and hierarchy.
- Verify the retained diagram in a browser at representative desktop and narrow viewport widths, including keyboard selection, reset, and dependency controls.
- Run git diff validation for the implementation change.
- Obtain independent documentation-structure and source-ownership review.

## Open Questions

None.

## Notes

Coordinate implementation with backlog/defect-backlog/fix-documentation-header-layout-and-index-navigation.md and backlog/defect-backlog/integrate-evaluation-evidence-into-documentation-navigation.md because they may modify the same HTML page or navigation tests. These are source-overlap considerations, not delivery dependencies.

The retained agent-to-skill hierarchy is design/agent-skill-hierarchy.svg and its owning generator. This item does not remove its optional agent-dependency overlay; it removes only the separate wiring-map product and the backlog-specific focus shortcut.
