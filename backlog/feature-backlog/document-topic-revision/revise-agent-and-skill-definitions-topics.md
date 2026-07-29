# Revise the Core Agent and Skills Document Topics

Status: Ready

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/document-topic-revision/revise-agent-and-skill-definitions-topics.md

Completion: direct-main

Series: backlog/feature-backlog/document-topic-revision/index.md

## Summary

Analyze and revise design/agent-and-skill-definitions.html so its topic hierarchy clearly explains conceptual agents, skills, their relationships, and their generated catalog surfaces.

## Context

The page is a primary catalog entry point and combines authored explanation with generated role and skill data. Its topic hierarchy must distinguish definitions, responsibilities, relationships, model profiles, and generated presentation without hiding catalog subjects inside broad headings.

## Source Evidence

Direct user request in task 019fa9bf-1e81-7a70-87e5-a747ce97318f on 2026-07-28 to create one work item for each document to revise it after integrating the document-topic agent and skills.

## Requirements

- Produce a fresh source-grounded scored topic outline for design/agent-and-skill-definitions.html.
- Verify that topic names enunciate every constituent used by their parent and sequence justifications.
- Revise headings, grouping, order, and explanatory transitions where the analysis identifies missing, compound, or misplaced topics.
- Preserve every conceptual agent and skill catalog subject, generated-data ownership, filters, identifiers, links, and accessibility behavior.
- Update owning sources or generators when a displayed topic comes from generated data.
- Record before-and-after topic placement evidence and explain every retained partial score.

## Acceptance Criteria

- Every substantive source block remains represented.
- Agent definitions, skill definitions, agent-skill relationships, model profiles, and generated catalog behavior have clear topic ownership.
- No topic placement relies on invented purpose, chronology, dependency, or outcome.
- Existing anchors, navigation, filtering, generated counts, and accessible names continue to work.

## Dependencies

backlog/feature-backlog/document-topic-revision/incorporate-document-topic-agent-and-skills.md

## Verification

- Run document link, markup, accessibility, and generated-data freshness checks applicable to this page.
- Run focused bundle-content tests covering the definitions page.
- Run git diff --check.
- Obtain independent editorial review against the scored outline.

## Open Questions

None.
