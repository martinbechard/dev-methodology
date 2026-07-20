# Add The Wiki Skills And Project Context Page

Status: Completed

Type: Feature

## Current Execution

- Canonical Dev Orchestrator task: 019f7e76-9ff3-74d2-a73d-b4453a506dc2.
- Worktree: /Users/martinbechard/.codex/worktrees/b4ac/dev-methodology.
- Phase: completed delivery; branch and worktree are eligible for parent cleanup.

## Resolution

- Accepted candidate: 30cc2128dfad0d531e5d1ddb551b25c10e373c17 on branch codex/wiki-skills-project-context in /Users/martinbechard/.codex/worktrees/b4ac/dev-methodology.
- Source and scope boundary: implementation changed only README.md, index.html, design/documentation-templates.html, design/skills-modularization.html, design/wiki-skills-and-project-context.html, and scripts/test_bundle_content.py. No governed agent or skill definition changed, so no definition approval gate was required.
- Independent review: an initial fresh artifact review returned NEEDS_CORRECTION for one source overstatement, one false-pass link assertion, and 320-pixel overflow. All three were corrected. A new fresh-context review then returned ACCEPTED with no actionable findings after checking all eight skill sources and the Karpathy and OKF primary sources.
- Browser verification: exact resources browser:in-app and port:48763 were acquired at event 16ad8b90-b9bb-49a3-8592-e237e53b5aa2 and released at event 8db9bc74-e209-4701-b757-fc2c6f06085a. The page rendered at 1440 by 900, 390-pixel narrow width, and 320-pixel reflow. The 320-pixel check measured equal 305-pixel client and scroll widths, no missing assets, a single-column flow, and visible three-pixel skip-link focus. The controlled tab closed, viewport reset, browser session finalized, and local server stopped before release.
- Focused candidate verification: README routing, HTML ownership and navigation, exact local-link resolution, repeated-long-prose protection, Python compilation, ARIA label resolution, and git diff checks passed. The final reviewer additionally observed all 87 scripts.test_bundle_content tests passing.
- Main integration: e214237 integrated the accepted candidate. Commit 9403982df65064cd4a2f7431078fab2db5f2527e preserved the already-accepted documentation-settings.js contract from concurrent HTML Settings work. Four focused main selectors then passed: README routing, HTML information ownership and navigation, persistent documentation settings on every design page, and repeated-long-prose protection. Python compilation and git diff checks also passed.
- Integration ownership: the exact six-path claim wiki-context-integration-019f7e76 released normally at event ece48368-be4b-42ff-a599-79b10937c4db after main was clean.
- Cleanup ancestry: topology-only merge 96575621a8a7e39700377ce3db7a6497940f0319 made codex/wiki-skills-project-context an ancestor of main while preserving identical first-parent and result tree hash db4572b9eeda0c0e9274ce539ada933af4618ebc. The normal and no-change releases were rejected by the merge-parent audit at events 16cafcf3-9b91-44c2-a8f1-9fd825a10cfe, e113e2a4-e3bb-4b86-8457-927cd1b02c14, and 38b28ad9-7208-471b-9622-dd95c9c1c2c1. The parent independently verified clean main, identical tree hashes, and that wiki-context-topology-019f7e76 was the sole registry entry, then removed only that confirmed stuck entry through the supported recovery rule. Authoritative claim status was empty afterward.
- Completion ownership: exact active and completed work-item paths were acquired by wiki-context-completion-019f7e76-final at event 6239c7f7-2e4b-48ab-a9c6-52827620f550. This completed record is committed and the claim is released immediately afterward.

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
