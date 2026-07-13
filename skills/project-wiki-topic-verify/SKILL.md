---
name: project-wiki-topic-verify
description: Verify created or updated repository docs/wiki topic pages against project-wiki quality rules after raw source ingest or wiki maintenance. Use when the agent needs an independent, read-only review of created or updated topic pages, durable leaf coverage, hub versus leaf granularity, source links, digest updates, federation boundaries, and project-wiki lint before accepting wiki content. The verifier judges the topic pages, not the source material.
metadata:
  category: wiki-and-knowledge
---

# Project Wiki Topic Verify

Use this skill as a fresh-context verifier. The verifier checks created or updated docs/wiki topic pages and reports whether those pages are acceptable. The verifier must not edit files. Source files are evidence only; the verification verdict is never about whether the source material itself is good.

## Required Context

The caller must provide:

- Repository root.
- Complete list of created or updated docs/wiki topic pages to verify.
- Raw source path, processed source path, or other authoritative source paths only when they are needed as evidence for the topic pages.
- Any lint output already available.

If the caller does not provide the created or updated topic page paths, stop and request them. Do not verify only the raw source file. Do not infer success from a broad repository scan alone.

## Shared Checklist

Read the shared checklist before reviewing files:

../project-wiki/references/topic-page-verification-checklist.md

Use that checklist as the acceptance contract. Also read these project-wiki references if the relevant issue is in scope:

- ../project-wiki/references/page-schema.md when page structure or section requirements are being judged.
- ../project-wiki/references/operations.md when raw ingest, digests, or raw/processed moves are being judged.
- ../project-wiki/references/source-priority.md when sources conflict.

## Review Workflow

Non-reserved Markdown concept documents should have YAML frontmatter with a non-empty type field. Folder index.md and log.md files are OKF reserved files and should stay navigational without concept frontmatter.

1. Read every created or updated docs/wiki topic page supplied by the caller.
2. Read the raw source path, processed source path, or other authoritative source paths only as evidence for evaluating the topic pages.
3. Read docs/wiki/topic-index.md, relevant folder index.md hub pages, relevant digest pages, and docs/wiki/federation.md when present and relevant.
4. Check whether the topic pages account for independently changing entities that should have durable leaf pages.
5. Run the leaf concept audit below on every created or updated topic page.
6. Check whether created or updated hubs stayed navigational instead of absorbing leaf details.
7. Check named source references in prose. They must link to the source at the point of use when the prose names or compares source artifacts.
8. Check multi-source paragraphs for a synthesis, contrast, tension, or source-specific boundary instead of stacked source summaries.
9. Check that the leaf-link pass was run for created or updated durable leaves. Run the leaf-link pass after creating or updating a durable leaf page. Use repository grep to find existing wiki mentions of each leaf title before finishing. A page that mentions a durable leaf title should link the first unlinked mention to that leaf unless the mention is inside a heading, code fence, or existing link.
10. Check source links, digest links, topic-index links, and federation boundaries. Raw and raw/processed source links must be relative to the wiki page, not absolute filesystem paths.
11. Run the project-wiki lint command from the repository root when available.
12. Run python3 project-wiki-skill-root/scripts/wiki_ops.py okf-migrate only when the caller asks for repair; otherwise stay read-only and report missing or stale frontmatter as a finding.
13. Run python3 project-wiki-skill-root/scripts/wiki_ops.py okf-validate from the repository root when available.
14. Return a verdict about the created or updated topic pages. Do not edit files.

## Leaf Concept Audit

Treat a page as over-bundled when it contains multiple reusable concepts that can change independently and those concepts are not represented by existing leaf pages, upstream links, or explicit deferrals.

A concept is a leaf candidate when it has its own title-like phrase and at least one of these traits:

- It describes a reusable practice pattern, workflow, operating agreement, governance rule, decision, evaluation question, team structure, source snapshot, technology, model family, framework, product, protocol, standard, security issue, or named method.
- It has source evidence that differs from the rest of the page.
- It would be useful for another page to link directly to it.
- It could be updated, contradicted, replaced, or expanded without changing the whole parent page.
- It carries guidance that a future agent would need to load independently.

Do not accept a broad page just because the prose is coherent. A good broad page can still fail when it bundles leaf concepts.

For each created or updated topic page, report NEEDS_CORRECTION when meaningful leaf candidates remain only as paragraphs or bullets inside that page. Name the proposed leaf pages and the folder where they should live. If the page keeps a concept in place, the page should make the reason clear, such as one-off local context, insufficient source detail, upstream-owned coverage, or a deliberate open question.

For adoption and operating model pages, common leaf candidates include workflow-before-model selection, human-agent approval boundaries, durable instruction and skill-file management, tier-specific assistant behavior, outcome alignment versus process standardization, senior-led agentic execution pods, and junior learning paths in agentic teams.

## Verdict Format

Start the final response with exactly one of these lines:

VERDICT: GOOD

VERDICT: NEEDS_CORRECTION

For GOOD, list the topic pages reviewed, evidence sources consulted if any, and lint result.
Include the OKF validation result when the command is available.

For NEEDS_CORRECTION, list only actionable findings. Each finding must name the file, describe the problem, and state the correction needed. Focus on durable leaf gaps, oversized hubs, missing page contract sections, stale source links, digest problems, federation duplication, unsupported claims, and lint findings.

## Acceptance Rules

Return GOOD only when all applicable checklist items pass for the created or updated topic pages and lint has no findings.

Return NEEDS_CORRECTION when any independently changing entity remains trapped in a hub, omnibus page, or dated scan page without an entity leaf or justified upstream link.

Return NEEDS_CORRECTION when a created or updated topic page contains multiple meaningful leaf candidates but the page does not split them, link existing leaves, link upstream-owned coverage, or record an explicit deferral.

Return NEEDS_CORRECTION when source links still point to the wrong raw location after processing.

Return NEEDS_CORRECTION when raw or raw/processed source links use absolute filesystem paths, including /Users/raw, /raw, or repository-absolute raw paths. These links must be relative to the topic page.

Return NEEDS_CORRECTION when prose names or compares source artifacts, decks, procedures, pages, or external references without linking those sources at the point of use.

Return NEEDS_CORRECTION when a paragraph uses multiple sources but only stacks source summaries instead of stating the shared rule, scope contrast, tension, or source-specific boundary.

Return NEEDS_CORRECTION when a created or updated durable leaf was not followed by python3 project-wiki-skill-root/scripts/wiki_ops.py link-leaves or equivalent repository grep coverage.

Return NEEDS_CORRECTION when a digest entry uses its dated text mainly to list page or file changes instead of summarizing the content that was added or modified.

Return NEEDS_CORRECTION when unrelated digest items are bundled into one dated paragraph instead of separate item-level synopsis entries.

Return NEEDS_CORRECTION when digest entries are grouped by raw source artifact, collector run, sweep category, or ingestion batch instead of independently changing item or closely coupled product family.

Return NEEDS_CORRECTION when dated Current Understanding entries in a monthly digest are not in reverse chronological order by entry date, newest first.

When repairing an existing digest, inspect the current month page for bundled dated paragraphs and rewrite the requested date range into item-level synopsis entries instead of only appending new entries.

Reorder the affected Current Understanding entries into reverse chronological order by entry date before finishing.

Use durable leaf pages as the content anchor for digest prose; keep source files in Authoritative Sources as provenance rather than repeating source-log wording.

Do not create separate digest entries for duplicate raw captures or repeated source-window sightings unless they add distinct content; fold them into the existing item or closely coupled product-family entry.

High-volume raw sources may update many durable leaves without forcing every touched leaf into the digest; omit low-signal digest mentions rather than compress unrelated entities into a vague grouped bullet.

Return NEEDS_CORRECTION when a created or updated topic page omits required sections or uses invented paths, tests, backlog status, behavior, fallback, or compatibility claims.

Return NEEDS_CORRECTION when lint fails, even if the prose looks acceptable.

Return NEEDS_CORRECTION when OKF validation fails for any created or updated topic page.
