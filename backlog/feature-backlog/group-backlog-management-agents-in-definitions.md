# Group Backlog Management Agents In The Definitions HTML And Diagram

Status: Ready

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/group-backlog-management-agents-in-definitions.md

Completion: direct-main

## Summary

Add a distinct Backlog Management grouping to the agent-and-skill-definitions HTML, diagram, and data source, placing the clearly backlog-management roles in that group while preserving their identities and all navigation and search relationships.

## Context

The agent and skill definitions presentation currently exposes roles through its existing groupings. The user requested a dedicated grouping for backlog-management agents, explicitly naming Dev Backlog Coordinator and Dev Backlog Steward. The implementation must use source-backed role responsibilities to determine any additional members rather than changing identities or grouping roles by name alone.

## Source Evidence

Direct user request in parent Thread 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a: “In the agents and skill definitions html file and diagram, create a grouping for the backlog management agents and move those agents such as backlog coordinator, backlog steward etc. to that group”.

## Requirements

- Add a distinct Backlog Management grouping to design/agent-and-skill-definitions.html and its authoritative diagram/data source.
- Place Dev Backlog Coordinator and Dev Backlog Steward in the grouping.
- Include other roles only when their source-backed purpose and ownership establish backlog-management responsibility.
- Preserve each role’s existing identity, source link, navigation target, searchable metadata, and relationships.
- Regenerate derived views only through their owning generator after required canonical-path approval for any governed definition source.

## Acceptance Criteria

- The definitions HTML and diagram visibly present Backlog Management as a distinct grouping.
- Dev Backlog Coordinator and Dev Backlog Steward appear exactly once in the appropriate grouping with their existing role identity intact.
- Search, navigation, and role relationship links continue to resolve for every moved role.
- Any additional grouped role is justified by cited canonical role source evidence.

## Dependencies

None.

## Verification

- Run focused generation or freshness checks for the definitions HTML and data source.
- Verify the HTML structure, diagram labels, navigation, and search behavior for moved roles.
- Run applicable bundle-content or generated-definition regression checks.
- Obtain fresh independent review.

## Open Questions

- Which additional role definitions, if any, have source-backed backlog-management ownership beyond Dev Backlog Coordinator and Dev Backlog Steward?

## Notes

Do not change role identities, conceptual ownership, or governed definitions merely to create the presentation grouping. An exact canonical-path approval record remains required before any governed definition mutation.
