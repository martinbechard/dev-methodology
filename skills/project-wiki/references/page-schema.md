# Project Wiki Page Schema

Every repository wiki lives under docs/wiki and uses a small standard page set plus topic folders and domain topic pages.

Project wiki pages are also OKF-compatible concept documents. Non-reserved Markdown concept documents should have YAML frontmatter with a non-empty type field. Use title, description, and tags when they help agents route and preview the page. Folder index.md and log.md files are OKF reserved files and should stay navigational without concept frontmatter.

## Required Files

- README.md introduces the wiki and links to the main pages.
- schema.md records the authority order, topic-page sections, and maintenance rules.
- topic-index.md maps primary topics and source neighborhoods.
- glossary.md defines recurring project terms.
- open-decisions.md records unresolved source conflicts and decisions.
- known-defects.md explains how to interpret defect records.
- maintenance-log.md records notable wiki maintenance events.
- digests/index.md introduces monthly development digests when raw news or development sources are ingested.
- digests/YYYY-MM.md records the month digest with short entries that link to entity leaves.

## Topic Folders

Use topic folders when related pages share a durable domain. Each topic folder should have an index.md hub page plus granular leaves.

Example structure:

```text
docs/wiki/
  digests/
    index.md
    YYYY-MM.md
  companies/
    index.md
    microsoft-ai-model-family.md
  agentic-frameworks/
    index.md
    langchain-stack.md
    production-patterns.md
    research-snapshot-YYYY-MM-DD.md
```

Folder index pages are hubs. They describe the stable domain, link to leaves, cross-reference related folders, and keep domain-level open questions. They are not dated news pages or source dumps.

Leaf pages should be as granular as practical. Split separate frameworks, companies, technologies, reusable patterns, model families, workflows, source snapshots, and evaluation questions when those subjects can change independently.

A concept should usually be split into a leaf when it has a title-like name, distinct source evidence, likely inbound links from other pages, an independent maintenance path, or reusable guidance that future agents may need to load separately. This includes reusable practice patterns, operating agreements, governance rules, decisions, team structures, named methods, and adoption patterns.

Run the leaf-link pass after creating or updating a durable leaf page. Use repository grep to find existing wiki mentions of each leaf title before finishing. A page that mentions a durable leaf title should link the first unlinked mention to that leaf unless the mention is inside a heading, code fence, or existing link.

Do not accept a broad page just because it is coherent. If it contains several meaningful leaf candidates, either create the leaves, link existing leaves, link upstream-owned coverage, or record explicit deferrals.

Raw source ingest should produce entity leaves for products, companies, model families, specific models, frameworks, techniques, protocols, standards, workflows, notable features, security issues, and other named concepts that may recur independently. If a raw source mentions an entity without enough explanation, add a compact baseline from focused research and cite the sources used.

Monthly digests live under docs/wiki/digests. Each month page may keep dated entries for when information was added or modified, but the entry text should summarize the content that changed instead of listing page or file changes. Use one digest entry per independently changing item or closely coupled product family; do not bundle unrelated items into one dated paragraph. Monthly digest Current Understanding entries must appear in reverse chronological order by entry date, newest first; keep same-date entries in stable content order unless a clearer local grouping is needed. Each entry should stay at most three lines, link to the relevant entity leaf, and leave detailed background in that leaf.

When repairing an existing digest, inspect the current month page for bundled dated paragraphs and rewrite the requested date range into item-level synopsis entries instead of only appending new entries. Reorder the affected Current Understanding entries into reverse chronological order by entry date before finishing. Use durable leaf pages as the content anchor for digest prose; keep source files in Authoritative Sources as provenance rather than repeating source-log wording. Do not create separate digest entries for duplicate raw captures or repeated source-window sightings unless they add distinct content; fold them into the existing item or closely coupled product-family entry.

Raw-source ingest automation prompts must repeat the digest granularity and ordering rules directly: one digest entry per independently changing item or closely coupled product family; never group digest entries by raw source artifact, collector run, sweep category, or ingestion batch; keep monthly digest Current Understanding entries in reverse chronological order by entry date. When a digest page changes, the automation closeout must report that digest granularity and ordering were checked with the project-wiki-topic-verifier checklist, or that the full verifier returned GOOD. High-volume raw sources may update many durable leaves without forcing every touched leaf into the digest; omit low-signal digest mentions rather than compress unrelated entities into a vague grouped bullet.

## Topic Page Contract

Topic pages should include:

```markdown
---
type: Topic
title: Topic Name
description: One sentence summary of the topic.
tags: [topic-folder]
---

# Topic Name

## Current Understanding

## Authoritative Sources

## Related Code

## Related Tests

## Related Backlog Items

## Related Wiki Pages

## Open Questions

## Maintenance Notes
```

## Section Rules

- Current Understanding states what is true now in steady-state language.
- Authoritative Sources links to specs, requirements, architecture docs, procedures, backlog files, plans, source artifacts, or source neighborhoods used to maintain the page.
- Related Code names code paths that implement the behavior.
- Related Tests names tests that verify the behavior.
- Related Backlog Items lists active or historically relevant backlog files and their current status when known.
- Related Wiki Pages lists sibling wiki pages that help answer adjacent questions only when those links add navigation value beyond contextual links in the body.
- Open Questions captures unresolved decisions, source conflicts, or missing verification.
- Maintenance Notes records why the page changed and what should be checked next.

## Topic-Specific Sections

Additional sections are allowed when they clarify the topic without replacing the required contract.

Common useful sections:

- Reusable Implementations
- Pattern Boundaries
- Pattern Leaf Pages
- Foundation Patterns
- Theme Layers

Use hub pages for navigation and leaf pages for reusable or independently changing concepts. Do not create leaf pages for one-off business components unless they expose a reusable pattern.

During review, audit for bundled leaf concepts before accepting a topic page. A page that mixes multiple reusable patterns, workflows, decisions, operating agreements, governance rules, team structures, or evaluation questions should usually become a hub plus leaves or a smaller leaf with links to sibling leaves.

## Writing Rules

- Mention local files and wiki pages as Markdown links, not as bare filenames or paths.
- Prefer contextual links where the related concept is discussed.
- Run the leaf-link pass after creating or updating a durable leaf page.
- Run python3 project-wiki-skill-root/scripts/wiki_ops.py link-leaves from the repository root for the leaf-link pass.
- Run python3 project-wiki-skill-root/scripts/wiki_ops.py okf-migrate when concept frontmatter is missing or stale.
- Run python3 project-wiki-skill-root/scripts/wiki_ops.py okf-validate before finishing wiki maintenance.
- Use repository grep to find existing wiki mentions of each leaf title before finishing.
- A page that mentions a durable leaf title should link the first unlinked mention to that leaf unless the mention is inside a heading, code fence, or existing link.
- Move fully processed raw sources under raw/processed and update wiki source links to that processed path.
- Do not use comparative steady-state language such as enhanced, revised, old, or new unless describing a historical migration.
- Do not invent fallback behavior, source paths, test names, or backlog status.
- If a source is missing or unresolved, say Not yet identified.
- If there are no unresolved questions, say No open wiki questions are recorded for this topic.
- Keep pages concise enough for agents to load together with the source documents.
