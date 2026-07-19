# Add The Wiki Skills And Project Context Page

Status: Proposed

Type: Feature

## Summary

Create an HTML design page that explains the repository's wiki-related skills through the Karpathy LLM-wiki pattern, Open Knowledge Format principles, agent-maintained project context, and the code-aware hybrid provided by code-project-wiki.

## Context

The repository distributes eight wiki and knowledge skills, but their shared operating model is spread across the skill catalog, project wiki templates, README guidance, generated agent views, and individual skill instructions. Readers can identify each skill separately without seeing how the family instantiates the broader LLM-maintained wiki idea or why project repositories need a stricter source-authority boundary.

[Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) describes a persistent, compounding Markdown wiki between immutable raw sources and the user, with an agent maintaining synthesis, cross-references, contradictions, indexes, query results, and lint health. [Google Cloud's Open Knowledge Format introduction](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) formalizes a portable Markdown and YAML-frontmatter representation for knowledge consumed by people and agents.

The local [project-wiki skill](../../skills/project-wiki/SKILL.md) applies those ideas to repository context while keeping code, tests, specifications, procedures, backlog items, architecture, and plans above the wiki in the authority order. The [code-project-wiki skill](../../skills/code-project-wiki/SKILL.md) adds the hybrid synchronization model: repository changes become source material, durable understanding is maintained under docs/wiki, and Related Code plus Related Tests keep the synthesis connected to implementation evidence.

The page belongs at design/wiki-skills-and-project-context.html. It is a design explanation for the distributed bundle, not a project wiki topic page and not a generated catalog replacement.

## Requirements

- Create design/wiki-skills-and-project-context.html using the visual language, navigation conventions, accessibility practices, and offline behavior of the existing design HTML pages.
- Explain the Karpathy LLM-wiki principles that matter to this bundle: immutable or authoritative sources, persistent compiled synthesis, incremental ingest, entity and concept pages, cross-linking, query results that compound, health checks, and agent-owned maintenance.
- Explain the relevant Open Knowledge Format principles without overstating conformance: portable Markdown, YAML frontmatter on non-reserved concept documents, a non-empty type field, reserved navigational files, links, and validation.
- Distinguish the Karpathy pattern, Open Knowledge Format representation, this repository's project-wiki methodology, and the code-project-wiki specialization. Do not present them as interchangeable names for one artifact.
- Explain project-wiki as compiled project understanding that helps agents recover and maintain durable context across tasks while authoritative project artifacts remain the source of truth.
- Explain code-project-wiki as a hybrid in which code, tests, commits, specifications, procedures, architecture, plans, and backlog items feed wiki synchronization, with skipped changes recorded when they do not alter durable understanding.
- Show the source-to-context flow from raw or authoritative sources through synthesis, topic leaves, hubs, indexes, verification, and agent query use. Show where code and tests enter the hybrid flow.
- Describe the responsibilities and collaboration boundaries of project-wiki, project-wiki-create, project-wiki-query, project-wiki-research, project-wiki-review, project-wiki-topic-write, project-wiki-topic-verify, and code-project-wiki.
- Explain the separation between raw collection, durable wiki synthesis, independent verification, and query-time use.
- Explain hub and leaf granularity, source authority, federation, open questions, linting, leaf linking, and bounded writer-verifier correction loops at the level needed to understand the operating model.
- Link every named local skill to its source SKILL.md file and link external principles to primary sources.
- Add navigation to the page from README.md and the most relevant existing design HTML pages without duplicating their current catalog or template content.
- Update scripts/test_bundle_content.py so repository regression checks require the page, its primary sections, its local skill links, and its navigation entry points.

## Acceptance Criteria

- A reader can explain how the repository's wiki methodology maps onto and extends the Karpathy LLM-wiki pattern.
- A reader can distinguish OKF-compatible representation from the project-wiki operating workflow.
- A reader can explain why project-wiki is durable agent context but not the highest source authority.
- A reader can explain when code-project-wiki applies and how it keeps wiki understanding synchronized with code and verification evidence.
- All eight wiki-related skills appear with accurate ownership boundaries and working source links.
- The page includes a clear visual model of the general wiki flow and the code-project hybrid without requiring network access.
- README and design-page navigation make the page discoverable.
- The page is keyboard accessible, readable at desktop and narrow viewport widths, and consistent with the repository's existing design pages.
- Repository content tests detect missing sections, missing skill coverage, broken expected links, and missing navigation.

## Dependencies

None.

## Verification

- Verify Karpathy and Open Knowledge Format claims against their primary published sources.
- Compare every local skill description and boundary against the current source SKILL.md files.
- Run the focused repository content tests with the supported Python interpreter.
- Run the applicable generated-output checks if implementation changes generated navigation or catalog data.
- Open the HTML page locally and inspect navigation, responsive layout, keyboard use, diagrams, and source links.
- Run git diff --check.

## Notes

- Keep the page conceptual and source-faithful. Do not turn it into another generated skill catalog.
- Keep customer-specific wiki examples and private repository context out of the page.
- Prefer one compact relationship diagram and focused comparison sections over a long inventory of repeated skill descriptions.
