---
type: Skill
name: project-wiki-topic-writer
description: Create, rewrite, split, and verify repository docs/wiki topic pages. Use when the agent needs a topic writer to correct verifier findings, split broad pages into durable leaf pages, update folder hubs and topic indexes, preserve source-backed wiki content, run project-wiki lint, invoke $project-wiki-topic-verifier, and apply verifier corrections in a loop until the updated topic pages are accepted.
---

# Project Wiki Topic Writer

## Overview

Use this skill when editing docs/wiki content. The writer owns file edits, while the verifier stays read-only and independently judges the created or updated topic pages.

## Required Context

The caller must provide:

- Repository root.
- Write scope, such as one docs/wiki folder or a specific page set.
- Pages to review or correct.
- Any verifier findings already known.
- Any source paths that are authoritative evidence for the assigned pages.

If the write scope is missing or overlaps with another active writer, stop and request a clearer assignment.

## Read Before Editing

Read these shared instructions before changing topic pages:

- ../project-wiki/SKILL.md
- ../project-wiki/references/page-schema.md
- ../project-wiki/references/topic-page-verification-checklist.md
- ../project-wiki/references/operations.md when raw or processed source links are involved.
- ../project-wiki/references/source-priority.md when sources conflict.
- ../project-wiki-topic-verifier/SKILL.md

## Writing Workflow

Non-reserved Markdown concept documents should have YAML frontmatter with a non-empty type field. Folder index.md and log.md files are OKF reserved files and should stay navigational without concept frontmatter.

1. Inspect the assigned pages, folder hub, topic-index, relevant digest pages, federation page, and source evidence.
2. Identify bundled leaf concepts before editing. A concept usually deserves a leaf when it is reusable, independently changing, source-backed, likely to be linked by another page, or useful for future agents to load separately.
3. Create or update durable leaf pages for those concepts. Keep folder index pages short and navigational.
4. Update the original broad page into a hub, overview, or narrower leaf that links to the new or existing leaves.
5. Run the leaf-link pass after creating or updating a durable leaf page. Use repository grep to find existing wiki mentions of each leaf title before finishing. A page that mentions a durable leaf title should link the first unlinked mention to that leaf unless the mention is inside a heading, code fence, or existing link.
6. Update folder index pages, topic-index, related wiki links, digests, and source links as needed. Digest entries may keep dates, but they must summarize what changed in the content instead of listing which pages or files changed. Use one digest entry per independently changing item or closely coupled product family; do not bundle unrelated items into one dated paragraph. Keep monthly digest Current Understanding entries in reverse chronological order by entry date, newest first. Never group digest entries by raw source artifact, collector run, sweep category, or ingestion batch. When repairing an existing digest, inspect the current month page for bundled dated paragraphs and rewrite the requested date range into item-level synopsis entries instead of only appending new entries. Reorder the affected Current Understanding entries into reverse chronological order by entry date before finishing. Use durable leaf pages as the content anchor for digest prose; keep source files in Authoritative Sources as provenance rather than repeating source-log wording. Do not create separate digest entries for duplicate raw captures or repeated source-window sightings unless they add distinct content; fold them into the existing item or closely coupled product-family entry. High-volume raw sources may update many durable leaves without forcing every touched leaf into the digest; omit low-signal digest mentions rather than compress unrelated entities into a vague grouped bullet. Raw and raw/processed source links must be relative to the wiki page, never absolute filesystem paths.
7. Preserve OKF frontmatter on concept documents and standard topic sections on every topic page. Folder index.md and log.md files stay reserved and do not carry concept frontmatter.
8. Use steady-state language. Do not describe the page as enhanced, revised, old, or new unless documenting history in Maintenance Notes.
9. Link named source artifacts, decks, procedures, pages, and external references at the point of use in prose.
10. When multiple sources inform a paragraph, synthesize or contrast them. State the integrated rule, scope difference, tension, or source-specific boundary instead of listing what each source says.
11. Do not invent source paths, code paths, tests, backlog status, behavior, fallback, or compatibility claims.

## Verifier Loop

The writer must run the verifier loop on every created or updated topic page before finishing.

1. Run project-wiki lint from the repository root.
2. Run python3 project-wiki-skill-root/scripts/wiki_ops.py okf-migrate when frontmatter may be missing or stale.
3. Run python3 project-wiki-skill-root/scripts/wiki_ops.py okf-validate.
4. Run python3 project-wiki-skill-root/scripts/wiki_ops.py link-leaves when any durable leaf was created or updated.
5. Spawn a fresh subagent without forking context and ask it to use $project-wiki-topic-verifier.
6. Pass the repository root, the complete list of created or updated topic pages, evidence source paths if any, and lint plus OKF validation output.
7. If the verifier returns NEEDS_CORRECTION, apply the corrections in the writer context.
8. Rerun lint and OKF validation, then invoke a fresh verifier again.
9. Repeat until the verifier returns GOOD for the created or updated topic pages.

The verifier must not edit files. The writer owns all corrections.

## Output

Return:

- Pages created, updated, or deleted.
- Leaf concepts split out or intentionally deferred.
- Verifier verdicts.
- Lint and OKF validation result.
- Any remaining blockers.
