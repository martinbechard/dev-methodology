---
name: project-wiki-topic-write
description: Create, rewrite, split, and verify repository docs/wiki topic pages. Use when writing topics to correct verifier findings, split broad pages into durable leaf pages, update folder hubs and topic indexes, preserve source-backed wiki content, run local project-wiki checks, apply role-supplied corrections, and prepare a complete handoff for role-owned independent verification.
metadata:
  category: wiki-and-knowledge
---

# Project Wiki Topic Write

## Overview

Use this skill when editing docs/wiki content. The writer owns file edits, corrections, and local validation. The owning conceptual role orchestrates the independent read-only verifier and owns correction-attempt counting, interruption handling, and terminal status.

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
- ../project-wiki-topic-verify/SKILL.md

## Writing Workflow

Non-reserved Markdown concept documents should have YAML frontmatter with a non-empty type field. Folder index.md and log.md files are OKF reserved files and should stay navigational without concept frontmatter.

1. Inspect the assigned pages, folder hub, topic-index, relevant digest pages, federation page, and source evidence.
2. Identify bundled leaf concepts before editing. A concept usually deserves a leaf when it is reusable, independently changing, source-backed, likely to be linked by another page, or useful for future agents to load separately.
3. Create or update durable leaf pages for those concepts. Keep folder index pages short and navigational.
4. Update the original broad page into a hub, overview, or narrower leaf that links to the new or existing leaves.
5. Run the leaf-link pass after creating or updating a durable leaf page. Use repository grep to find existing wiki mentions of each leaf title before finishing. A page that mentions a durable leaf title should link the first unlinked mention to that leaf unless the mention is inside a heading, code fence, or existing link.
6. Update folder index pages, topic-index, related wiki links, digests, and source links as needed. Digest entries may keep dates, but they must summarize what changed in the content instead of listing which pages or files changed. Use one digest entry per independently changing item or closely coupled product family; do not bundle unrelated items into one dated paragraph. For example, do not discuss multiple companies in one digest entry unless they are part of the same joint story, such as a partnership, acquisition, coordinated release, or directly comparative event; appearing in the same source article or collection batch is not enough. Keep monthly digest Current Understanding entries in reverse chronological order by entry date, newest first. Never group digest entries by raw source artifact, collector run, sweep category, or ingestion batch. When repairing an existing digest, inspect the current month page for bundled dated paragraphs and rewrite the requested date range into item-level synopsis entries instead of only appending new entries. Reorder the affected Current Understanding entries into reverse chronological order by entry date before finishing. Use durable leaf pages as the content anchor for digest prose; keep source files in Authoritative Sources as provenance rather than repeating source-log wording. Do not create separate digest entries for duplicate raw captures or repeated source-window sightings unless they add distinct content; fold them into the existing item or closely coupled product-family entry. High-volume raw sources may update many durable leaves without forcing every touched leaf into the digest; omit low-signal digest mentions rather than compress unrelated entities into a vague grouped bullet. Raw and raw/processed source links must be relative to the wiki page, never absolute filesystem paths.
7. Preserve OKF frontmatter on concept documents and standard topic sections on every topic page. Folder index.md and log.md files stay reserved and do not carry concept frontmatter.
8. Use steady-state language. Do not describe the page as enhanced, revised, old, or new unless documenting history in Maintenance Notes.
9. Link named source artifacts, decks, procedures, pages, and external references at the point of use in prose.
10. When multiple sources inform a paragraph, synthesize or contrast them. State the integrated rule, scope difference, tension, or source-specific boundary instead of listing what each source says.
11. Do not pack a sequence or enumeration into a long paragraph. Treat three or more distinct steps or items in one paragraph as a list-structure trigger. Introduce the group with a short sentence, use a numbered list for ordered steps and a bulleted list for unordered items, and keep one coherent step or item in each entry.
12. Do not invent source paths, code paths, tests, backlog status, behavior, fallback, or compatibility claims.

When the owning conceptual role supplies verifier findings for a correction pass, apply only the requested in-scope corrections and rerun the applicable local checks. The role, not this skill, counts correction attempts and decides whether another independent verification pass is allowed.

## Local Validation

Run commands from the repository root. Use python3 unless the environment clearly provides python.

Resolve PROJECT_WIKI_SKILL_ROOT as the absolute directory containing the loaded project-wiki/SKILL.md. Do not assume a source checkout or fixed home catalog. Verify both the loaded skill and operation script before invoking a command:

```bash
PROJECT_WIKI_SKILL_ROOT="/absolute/path/to/the/loaded/project-wiki"
test -f "$PROJECT_WIKI_SKILL_ROOT/SKILL.md"
test -f "$PROJECT_WIKI_SKILL_ROOT/scripts/wiki_ops.py"
python3 "$PROJECT_WIKI_SKILL_ROOT/scripts/wiki_ops.py" lint
python3 "$PROJECT_WIKI_SKILL_ROOT/scripts/wiki_ops.py" okf-migrate
python3 "$PROJECT_WIKI_SKILL_ROOT/scripts/wiki_ops.py" okf-validate
python3 "$PROJECT_WIKI_SKILL_ROOT/scripts/wiki_ops.py" link-leaves
```

Run lint and OKF validation for every changed page set. Run okf-migrate only when frontmatter may be missing or stale. Run link-leaves when any durable leaf was created or updated.

## Verification Handoff

After local validation, preserve the written page set and prepare one complete handoff containing:

- Repository root.
- The complete created, updated, and deleted page inventory.
- Authoritative evidence paths needed to judge those pages.
- Current lint, OKF validation, and leaf-link results.
- Any role-supplied findings applied during the current correction pass.
- The preserved writer state, using a commit identifier when already committed or the write-scope status and diff digest when uncommitted.

Return the handoff to the owning conceptual role. The skill does not spawn or invoke the verifier, count correction attempts, interpret verifier availability or interruption, or issue a terminal GOOD or BLOCKED status.

The owning conceptual role routes the handoff to a fresh wiki-topic-verifier, captures the invocation and returned receipt, and compares the write-scope state immediately before and after that read-only invocation. That comparison is the before-and-after no-mutation evidence proving the verifier did not change writer-owned files.

Leave the writer edits intact if the verifier is interrupted or returns an unavailable non-verdict, and return no invented verdict or findings from this skill. The owning conceptual role uses the preserved writer state, invocation receipt, before-and-after no-mutation evidence, page inventory, validation results, completed correction attempts, governing cap, and exact unresolved interruption as role-owned BLOCKED evidence.

## Output

Return:

- The complete created, updated, and deleted page inventory.
- Leaf concepts split out or intentionally deferred.
- Any role-supplied corrections applied.
- Lint, OKF validation, and leaf-link results.
- The complete verification handoff and preserved writer state.
- Any remaining writer-owned blocker, such as missing scope or authoritative evidence.
