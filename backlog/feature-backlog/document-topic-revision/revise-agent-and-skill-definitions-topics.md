# Revise the Core Agent and Skills Document Topics

Status: Starting

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/document-topic-revision/revise-agent-and-skill-definitions-topics.md

Completion: direct-main

Owner: Unowned pending immediate root acceptance
Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758
Launch Reservation: reserve-nine-document-topic-revisions-019fa9bb-01; one bounded live launch handshake
Normalized Objective: Revise the Core Agent and Skills Document Topics.
Dispatch Time: 2026-07-29T03:31:55Z
Intended Root Role: Dev Orchestrator
Runtime Thread: 019fabe8-f6fe-71a3-9211-eefa149d3809
Root Agent Task: 019fabe8-f6fe-71a3-9211-eefa149d3809
Branch: codex/revise-agent-and-skill-definitions-topics
Worktree: /Users/martinbechard/.codex/worktrees/c63b/dev-methodology
Observed Launch Evidence: Parent Dev Backlog Coordinator confirmed the canonical Thread's clean bounded launch handshake; this reservation preserves Owner as Unowned pending immediate root acceptance.
Required Next Lifecycle Transition: The canonical root Dev Orchestrator must atomically record Starting -> Running for this same Thread and task before repository mutation.
Lifecycle Claim Evidence: reserve-nine-document-topic-revisions-019fa9bb; outcome SHARED_CHECKOUT_ACQUIRED; claim event cefebc44-68b8-427b-856e-52b485bc2f11; exact provider path claimed in the primary main checkout.

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
