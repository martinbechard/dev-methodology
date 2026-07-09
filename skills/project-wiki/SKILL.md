---
name: project-wiki
description: Use when creating, maintaining, or answering from a repository wiki; when work changes specs, architecture, plans, backlogs, user-visible behavior, reusable patterns, or project knowledge that should be synthesized under docs/wiki.
metadata:
  short-description: Maintain an opinionated project wiki
---

# Project Wiki

Use this skill when a repository has, needs, or should update a maintained wiki under docs/wiki.

The wiki is compiled understanding, not the source of truth. If the wiki conflicts with code, tests, specifications, procedures, backlog files, architecture, plans, or other source documents, update the wiki from the authoritative source.

## Standard Shape

Use docs/wiki as the wiki location. Do not invent a different structure per project unless the user explicitly asks for that.

Every project wiki should include:

- README.md
- schema.md
- topic-index.md
- glossary.md
- open-decisions.md
- known-defects.md
- maintenance-log.md
- digests folder when raw news or development sources are ingested
- domain topic pages as needed
- topic folders as needed, each with an index.md hub page
- operational folders when external sources, clippings, or helper scripts are part of the wiki workflow

Project wikis should be OKF-compatible. Non-reserved Markdown concept documents should have YAML frontmatter with a non-empty type field plus a useful title and description when available. Folder index.md and log.md files are OKF reserved files and should remain navigational without concept frontmatter. The normal project-wiki body sections remain required for topic pages.

During setup, do not ask vague blank-slate questions. Present a setup recommendation pack before asking setup questions. The pack must include the inferred wiki purpose, topic roots that fit the repository purpose, operational folders, any upstream or sibling wiki candidates, recommended wiki-related skills, workflows, and automations, and recommended public update feed topics. Ask the human to accept, remove, or edit the recommendations before collecting mappings.

Add AGENTS.md wiki workflow guidance during setup. The guidance should tell agents to use the project-wiki-query skill for wiki-backed questions and lightweight project knowledge lookups. It should tell agents to use the project-wiki-research skill for ad-hoc topic research when docs/wiki does not already answer the request. It should tell agents to check docs/wiki first when answering project questions, then verify against authoritative source files before replying because the wiki is a synthesis layer. It should also tell agents that when they extract durable project knowledge from project files, they save a raw wiki fragment under raw before synthesizing it into docs/wiki pages. It should tell agents to commit wiki changes with the source, test, or documentation changes that made them necessary after verification passes.

For source-driven wikis, propose raw, raw/processed, Clippings, and scripts. Use raw for unprocessed source artifacts, raw/processed for sources fully synthesized into wiki pages and digests, Clippings for human-saved source notes before ingest, and scripts for repository-local helper scripts that collect, validate, or inspect wiki source material. If a repository does not need one of these folders, ask the human to remove it from the setup pack rather than silently omitting it.

Useful wiki-related candidates to propose include page creation, raw-source ingest, entity leaf refresh, open-question review, source reconciliation, digest maintenance, public source collection, on-demand research, backlog or spec sync, and project-specific page creation workflows. Include the project-wiki-research skill when a repository needs ad-hoc topic research that checks docs/wiki first and saves missing coverage under raw. On-demand research: owns ad-hoc topic research when docs/wiki and any upstream wiki do not already answer the request; it saves a sourced synthesis report under raw for later ingest instead of editing docs/wiki directly. For each accepted skill, workflow, or automation, ask what wiki content it owns and which wiki root it should use. Ask one mapping at a time.

Also ask whether the wiki needs automated public update feeds, but propose likely topics of interest first. Pick topics from the repository purpose and name the wiki root that would own the entity leaves. For an AI-assisted development wiki, useful topic candidates include coding agents, coding assistant products, agent frameworks and SDKs, MCP servers, coding model families, software engineering evals and benchmarks, prompt and context engineering patterns, AI code review, CI and testing workflows, security, privacy, licensing, and team adoption practices. If feeds are accepted, gather feed topics one at a time. For each topic, ask what public topic should be scanned, then ask for the wiki root that owns those entity leaves. Do not collect a long topic list in one question.

## Federated Wikis

Use federated wikis when a repository wiki should extend another maintained wiki instead of duplicating its durable entity analysis. Federation is a one-way reference unless the user explicitly asks for bidirectional synchronization.

During setup, identify likely upstream wikis from user input, sibling repository names, local paths, and existing wiki roots. Include a federation recommendation in the setup pack when another wiki already owns broad ecosystem entities, product catalogs, model families, companies, frameworks, MCP servers, techniques, or other reusable background.

Record accepted federation relationships in the downstream wiki, usually in docs/wiki/federation.md. Include the upstream wiki root, relationship direction, upstream-owned scopes, downstream-owned scopes, lookup rules, and feed boundaries.

Before creating or updating a durable entity page, search upstream topic indexes before creating local entity leaves. If the upstream wiki already owns the entity, link to the upstream page and keep only the downstream-owned lens locally. A downstream-owned lens may explain project-specific usage, operating practice, evaluation criteria, implementation guidance, governance, or decisions. It must not restate broad upstream analysis as a parallel encyclopedia entry.

Classify cross-wiki topics this way:

- Upstream-owned entity: link upstream, summarize only what is needed for local navigation, and do not duplicate analysis.
- downstream-owned lens: create or update the local page because it answers a local practice, workflow, design, adoption, or governance question.
- Shared concept with local decision: keep ecosystem facts upstream and keep the downstream recommendation, decision, or operating rule locally.
- Missing or conflicting upstream coverage: record an open question or create a local note only when the downstream wiki needs it; do not silently fork ownership.

Do not schedule duplicate public feeds for topics an upstream wiki already collects. Downstream feeds should watch local practice sources, project-specific sources, or topics not owned upstream. If a downstream source produces an upstream-owned entity update, save it as raw source for the appropriate owner or record an open question about routing.

Topic pages must include:

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

Additional topic-specific sections are allowed when they clarify the page. Useful examples include Reusable Implementations, Pattern Boundaries, Pattern Leaf Pages, Foundation Patterns, and Theme Layers.

## Topic Granularity And Folder Structure

Prefer granular, durable topics over monolithic omnibus pages. A broad domain such as agentic frameworks, payments, reporting, companies, authentication, deployment, data ingestion, or AI models should usually become a folder under docs/wiki with an index.md hub plus focused leaf pages.

Use this structure when a topic has several related concepts, providers, components, snapshots, workflows, decisions, or implementation surfaces:

```text
docs/wiki/
  topic-index.md
  digests/
    index.md
    YYYY-MM.md
  domain-name/
    index.md
    concept-a.md
    concept-b.md
    provider-or-component.md
    research-snapshot-YYYY-MM-DD.md
```

Folder index pages are hubs. They explain the stable domain, link to the leaves, and name the questions that belong in that domain. They should not be dated news pages, release notes, or source dumps.

Leaf pages are granular. Create separate leaf pages for specific frameworks, companies, model families, technologies, reusable patterns, product areas, workflows, source snapshots, evaluation questions, and decisions when those subjects can change independently.

A concept should usually become a leaf when it has its own title-like phrase, distinct source evidence, independent maintenance path, likely inbound links from other wiki pages, or reusable guidance that future agents may need to load without the rest of the parent page. This includes reusable practice patterns, operating agreements, governance rules, decisions, evaluation questions, team structures, named methods, and adoption patterns. Do not leave several such concepts bundled inside one broad topic page unless each concept is linked to an existing leaf, linked to upstream-owned coverage, or explicitly deferred with a reason.

Run the leaf-link pass after creating or updating a durable leaf page. Use repository grep to find existing wiki mentions of each leaf title before finishing. A page that mentions a durable leaf title should link the first unlinked mention to that leaf unless the mention is inside a heading, code fence, or existing link.

Dated research, news, meeting notes, raw-source synthesis, or migration history should be leaf pages under the most relevant durable folder. The hub should summarize stable current understanding and point to dated leaves only as evidence or provenance.

## Raw Source Ingest

When processing raw source files, extract the granular entities first. Entities include products, companies, model families, specific models, frameworks, techniques, protocols, standards, workflows, notable features, security issues, and other named concepts that may recur independently.

Use judgement when sources name overlapping concepts. Normalize synonyms and aliases into the best existing durable entity page when they refer to the same thing. When multiple sources express the same underlying pattern, factor common ideas into the durable hub or leaf that owns the shared concept. Keep source-specific ideas tied to their source in the relevant leaf, scan page, digest note, or Maintenance Notes so one source's framing does not become a universal claim. Preserve conflicting ideas as Open Questions or clearly attributed source-specific notes until the authoritative source order or human direction resolves them.

When multiple sources inform the same paragraph, write the reader-facing synthesis. State the shared rule, the scope contrast, the tension, or the source-specific boundary instead of stacking source summaries. If the prose names a source artifact, deck, procedure, page, or external reference, link that source at the point of use. The Authoritative Sources section is required but is not enough for named source comparisons in prose.

For each extracted entity, update an existing durable leaf page or create one under the most relevant topic folder. If the raw source names an entity but does not explain it enough for a useful leaf, do focused research from reliable current sources and record those sources in Authoritative Sources or Maintenance Notes as appropriate. Keep the leaf page as the home for background, implications, adoption context, caveats, and source detail.

When linking raw or processed source artifacts from docs/wiki pages, use links relative to the wiki page, such as ../../../raw/processed/source-name.md from a topic folder leaf. Never use absolute filesystem paths for raw sources, including /Users/raw, /raw, or repository-absolute raw paths, because those links are machine-specific and not portable.

Dated scan pages are allowed only as source-synthesis leaves when they preserve provenance or explain a time-bounded scan. They must not be the only wiki surface for entities that can change independently. Promote entity-specific facts from scans into the matching leaf pages when the facts affect current understanding, selection criteria, adoption caveats, governance, security, or implementation relevance.

Create monthly development digests under docs/wiki/digests. Use docs/wiki/digests/index.md as the digest hub and docs/wiki/digests/YYYY-MM.md for each month. A digest entry may keep the date when the information was added or modified, but the text must summarize the content change rather than list page or file changes. Use one digest entry per independently changing item or closely coupled product family; do not bundle unrelated items into one dated paragraph. Monthly digest Current Understanding entries must appear in reverse chronological order by entry date, newest first; keep same-date entries in stable content order unless a clearer local grouping is needed. Each entry should give a short synopsis of the item, link to the relevant entity leaf page, stay at most three lines, and avoid carrying detailed background that belongs in the leaves.

When repairing an existing digest, inspect the current month page for bundled dated paragraphs and rewrite the requested date range into item-level synopsis entries instead of only appending new entries. Reorder the affected Current Understanding entries into reverse chronological order by entry date before finishing. Use durable leaf pages as the content anchor for digest prose; keep source files in Authoritative Sources as provenance rather than repeating source-log wording. Do not create separate digest entries for duplicate raw captures or repeated source-window sightings unless they add distinct content; fold them into the existing item or closely coupled product-family entry.

Raw-source ingest automation prompts must repeat the digest granularity and ordering rules directly: one digest entry per independently changing item or closely coupled product family; never group digest entries by raw source artifact, collector run, sweep category, or ingestion batch; keep monthly digest Current Understanding entries in reverse chronological order by entry date. When a digest page changes, the automation closeout must report that digest granularity and ordering were checked with the project-wiki-topic-verifier checklist, or that the full verifier returned GOOD. High-volume raw sources may update many durable leaves without forcing every touched leaf into the digest; omit low-signal digest mentions rather than compress unrelated entities into a vague grouped bullet.

After each raw source file is synthesized, run an independent topic-page verification loop before treating that source as complete. Spawn a fresh subagent without forking the main context, ask it to use $project-wiki-topic-verifier, and pass only the repository root, the complete list of docs/wiki topic pages created or updated for that source, the raw or processed source path as evidence, and any lint output. The verifier must review the topic pages with its own context and return GOOD or NEEDS_CORRECTION about those pages. It must not verify the source material as the target artifact. If it returns NEEDS_CORRECTION, the main ingest agent applies the corrections, reruns lint when files changed, and invokes a fresh verifier again with the updated topic-page list. Repeat until the verifier returns GOOD. Do not let the verifier edit files directly. Run this loop before moving the raw source into raw/processed. After the move and source-link updates, rerun lint and invoke a fresh verifier with the updated topic-page list and processed source path as evidence when any docs/wiki link changed.

After a raw source file has been fully processed into the relevant entity leaves and monthly digest, move it under raw/processed so future ingest passes do not process it again. Preserve useful date or source subfolders when moving files. Update wiki source links to the processed raw path using links relative to each wiki page. Do not move raw files when ingest is incomplete, source links are stale, source links are absolute filesystem paths, or wiki lint has not passed.

## Automated Update Feeds

Use automated update feeds only when the user wants the wiki to keep watching public sources after initial setup.

Set up feeds in two layers:

- Topic source collectors search public web sources for user-approved topics, save dated raw artifacts under raw, and do not update docs/wiki directly.
- A leaf refresher checks existing durable entity leaves under the approved wiki roots. It rebuilds the entity universe from leaf pages, keeps a local state ledger, checks new or oldest-unchecked leaves first, and saves qualifying public updates as raw artifacts for normal ingest.

Each feed must preserve the source-first boundary. It should include source URLs, visible publication or update dates, factual summaries, relevance notes, named entities, excluded candidates with reasons, and follow-up notes. It must avoid private, proprietary, sensitive, PII, or company-internal local content.

When the user approves a scheduled feed, use the target environment's approved automation facility instead of inventing a hand-written scheduler workaround. Keep update collectors raw-only; the ingest workflow owns docs/wiki changes.

## Authority Order

1. Code and tests describe actual behavior.
2. Functional specifications and requirements describe intended behavior.
3. AGENTS.md, README files, and procedure files describe workflow obligations.
4. Defect and feature backlog files describe tracked work. Status headings or explicit status fields outrank file presence.
5. Architecture and plan documents describe design intent.
6. Help, RAG, or generated documentation describe the current documentation surface.
7. Wiki pages summarize and navigate the above sources.

## Workflow

1. Run wiki status or initialize the wiki if it does not exist.
2. Use wiki suggest to map changed or named source files to likely wiki pages.
3. Read the authoritative source files before editing or answering from the wiki.
4. For raw source ingest, identify named entities, update or create their durable leaf pages, update the monthly digest, run the independent $project-wiki-topic-verifier loop for each ingested source file, then move fully processed raw files to raw/processed only after pre-move verification and lint pass. After processed-source links change, rerun lint and the verifier before completion.
5. For new wiki setup, present a recommendation pack with likely wiki roots, upstream wiki candidates, candidate wiki-related workflows or automations, and public feed topics of interest before asking the human to choose mappings.
6. If federation is accepted, record the upstream relationship and ownership boundaries before creating local topic folders.
7. Ask whether automated update feeds are required after showing likely feed topics and excluding upstream-owned feed topics. If they are, collect each scan topic and its wiki root one at a time before proposing source collectors or a leaf refresher.
8. Choose the smallest durable topic boundary: update an existing leaf, create a downstream lens, create a new leaf, or create a folder with an index.md hub when related pages are forming.
9. Run the leaf-link pass when a durable leaf was created or updated.
10. Preserve contradictions in Open Questions instead of inventing a resolution.
11. Run wiki lint and OKF validation, then fix findings before finishing.
12. When committing a task, include docs/wiki pages, raw fragments, raw/processed moves, wiki helper scripts, and related AGENTS.md guidance in the same coherent commit as the source, test, or documentation changes that made them necessary. If a task changes only wiki artifacts, commit that verified wiki-only slice on its own. Do not leave docs/wiki, raw fragments, or raw/processed moves unstaged after committing the related task. If repository or user instructions forbid committing, report the remaining wiki artifacts explicitly.

## Open Questions Review

Use the questions command when the user asks to review, close, answer, or list open wiki questions.

1. Run questions from the repository root.
2. Ask the human the first unresolved question only, including the file and line from the command output.
3. Wait for the human answer before asking another question.
4. Treat the human answer as authoritative for that question.
5. Update the relevant wiki page in steady-state language.
6. Remove or rewrite the answered Open Questions item so it no longer appears unresolved.
7. If the answer creates a project decision, update open-decisions.md or the relevant durable topic page.
8. Run questions again to confirm the answered question is gone.
9. Repeat until no open wiki questions remain or the human stops the review.
10. Run wiki lint before finishing.

## Hub And Leaf Pages

Use hub pages for broad navigation and leaf pages for reusable or independently changing concepts.

A hub page should usually be named index.md inside a topic folder. Keep it short: define the domain, list the important leaves, cross-link related folders, and record domain-level open questions.

A leaf page should describe a concept that can recur across surfaces, such as tables, dialogs, file references, error handling, deployment environments, provider pages, product areas, workflow families, source snapshots, or data import flows. A component or workflow used by only one page usually belongs in a domain topic page unless it establishes a reusable pattern.

When reviewing a topic page, audit for bundled leaf concepts before accepting it. If the page contains multiple reusable practice patterns, decisions, workflows, operating agreements, team structures, governance rules, or evaluation questions, split them into leaves or record explicit deferrals. A broad page that is well written can still be the wrong granularity.

For reusable UI, API, data, or operational patterns, classify by pattern first and by implementation second. Keep hubs short and put details in leaf pages.

## Writing Rules

- Write steady-state explanations. Avoid enhanced, revised, old, or new unless documenting history in Maintenance Notes.
- Mention local files and wiki pages as Markdown links, not bare paths.
- Prefer contextual links inside explanations. Use Related Wiki Pages only when the cross-reference adds navigation value.
- Link named source artifacts, decks, procedures, pages, and external references at the point of use. Do not make the reader infer named sources from the Authoritative Sources section.
- Link raw and raw/processed source artifacts with paths relative to the current wiki page. Do not use absolute filesystem paths for raw sources.
- When a paragraph uses multiple sources, synthesize or contrast them. State the integrated rule, scope difference, tension, or source-specific boundary instead of listing what each source says.
- If a source, test, or code path is missing, say Not yet identified.
- If there are no unresolved questions, say No open wiki questions are recorded for this topic.
- Do not invent source paths, tests, backlog status, behavior, fallbacks, or compatibility constraints.
- Keep pages compact enough for agents to load together with the source documents.

## Operations

Run commands from the repository root. Use python3 unless the environment clearly provides python.

```bash
python3 project-wiki-skill-root/scripts/wiki_ops.py init
python3 project-wiki-skill-root/scripts/wiki_ops.py status
python3 project-wiki-skill-root/scripts/wiki_ops.py suggest --changed
python3 project-wiki-skill-root/scripts/wiki_ops.py lint
python3 project-wiki-skill-root/scripts/wiki_ops.py okf-migrate
python3 project-wiki-skill-root/scripts/wiki_ops.py okf-validate
python3 project-wiki-skill-root/scripts/wiki_ops.py link-leaves
python3 project-wiki-skill-root/scripts/wiki_ops.py sources docs/wiki/topic-index.md
python3 project-wiki-skill-root/scripts/wiki_ops.py questions
python3 project-wiki-skill-root/scripts/wiki_ops.py questions --format json
```

Read references/page-schema.md before creating or substantially rewriting a wiki page.

Read references/topic-page-verification-checklist.md when verifying topic page quality, raw-source leaf coverage, hub versus leaf granularity, digest updates, federation boundaries, or source links.

Read references/source-priority.md when reconciling conflicts between wiki content and source documents.

Read references/operations.md when deciding which operation fits the current task.

## Output Expectations

When reporting completion, mention which wiki pages changed, whether wiki lint and OKF validation passed, and whether the wiki artifacts were committed with the related task or intentionally left uncommitted because repository or user instructions required that.
