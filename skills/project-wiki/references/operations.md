# Project Wiki Operations

Run commands from the repository root.

## init

Use init when docs/wiki does not exist or is missing the standard files. It creates only missing pages and does not overwrite existing content.

During new wiki setup, ask whether any wiki-related skills, workflows, or automations need to be adapted to the repository's wiki content model. Include skills or workflows for raw-source ingest, leaf refresh, open-question review, source reconciliation, digest maintenance, source collection, on-demand research, and page creation.

Start with a setup recommendation pack rather than a vague blank-slate question. The pack should name the inferred wiki purpose, proposed topic roots, Operational folder candidates, any federated wiki recommendation, Useful wiki-related workflow candidates, and Useful public update feed topic candidates. Ask the human to accept, remove, or edit the pack before collecting mappings one at a time.

Add AGENTS.md wiki workflow guidance during setup. The guidance should tell agents to use the project-wiki-query skill for wiki-backed questions and lightweight project knowledge lookups. It should tell agents to use the project-wiki-research skill for ad-hoc topic research when docs/wiki does not already answer the request. It should tell agents to check docs/wiki first when answering project questions, then verify against authoritative source files before replying. It should also tell agents that when they extract durable project knowledge from project files, they save a raw wiki fragment under raw before synthesizing it into docs/wiki pages. It should tell agents to commit wiki changes with the source, test, or documentation changes that made them necessary after verification passes.

After creating or maintaining a project wiki, keep it OKF-compatible. Run okf-migrate to add or refresh YAML frontmatter on non-reserved concept documents, then run okf-validate to ensure each concept document has a non-empty type field. Folder index.md and log.md files are OKF reserved files; keep them navigational and do not add concept frontmatter to them.

Operational folder candidates for source-driven wikis usually include:

- raw: unprocessed source artifacts captured from public feeds, local notes, source clips, or manual research.
- raw/processed: source artifacts that have been fully synthesized into durable wiki pages and digests.
- Clippings: human-saved source notes and article or video clippings waiting for review or ingest.
- scripts: repository-local helper scripts for collecting, validating, inspecting, or preparing wiki source material.

Create the approved folders during setup before configuring ingest or feed workflows, using keep files if the folder would otherwise be empty.

A federated wiki recommendation should include the upstream wiki root, relationship direction, upstream-owned scopes, downstream-owned scopes, and the lookup rule. For one-way federation, the downstream wiki reads and links upstream pages but does not rewrite upstream content unless the user asks for that separate maintenance task.

Before creating local entity leaves in a federated wiki, search the upstream wiki root and topic-index.md for the entity, product, company, framework, model, MCP server, technique, or tool. If upstream owns it, create a local page only for the downstream lens: usage guidance, operating model, evaluation criteria, practice pattern, governance rule, or project decision. Do not schedule duplicate public feeds for upstream-owned topics.

Useful wiki-related workflow candidates often include:

- Page creation: owns new durable topic pages and topic-index entries under the approved wiki roots.
- Raw-source ingest: owns named-entity extraction from raw sources, durable leaf updates, monthly digest entries, and raw/processed moves.
- Entity leaf refresh: owns raw-only public update checks for existing leaf pages under approved roots.
- Open-question review: owns unresolved questions under docs/wiki and decision updates in open-decisions.md or topic leaves.
- Source reconciliation: owns conflicts between code, specs, procedures, backlog files, and wiki summaries.
- Digest maintenance: owns docs/wiki/digests/index.md and monthly digest pages.
- Public source collection: owns raw artifacts for approved public topics without direct docs/wiki edits.
- On-demand research: owns ad-hoc topic research when docs/wiki and any upstream wiki do not already answer the request; it saves a sourced synthesis report under raw for later ingest instead of editing docs/wiki directly. Use the project-wiki-research skill for this workflow.
- Backlog or spec sync: owns wiki updates when roadmap, defect, design, or requirements files change.

Useful public update feed topic candidates should fit the repository purpose. For an AI-assisted development wiki, propose topics such as coding agents, coding assistant products, agent frameworks and SDKs, MCP servers, coding model families, software engineering evals and benchmarks, prompt and context engineering patterns, AI code review, CI and testing workflows, security, privacy, licensing, and team adoption practices. Pair each proposed topic with a likely wiki root, such as docs/wiki/coding-agents, docs/wiki/products, docs/wiki/agent-frameworks, docs/wiki/mcp-servers, docs/wiki/models, docs/wiki/evals, docs/wiki/workflows, or docs/wiki/governance.

When an AI-assisted development wiki extends a broad AI ecosystem wiki, remove redundant roots such as products, models, agent-frameworks, mcp-servers, companies, and general developer-tools if the upstream wiki already owns those leaves. Prefer local roots such as context-architecture, ai-assisted-development, workflows, quality, governance, tools-as-used, and federation.

For each wiki-related skill or workflow, collect one mapping at a time:

1. Ask which skill, workflow, or automation needs wiki integration.
2. Ask what wiki content it owns or updates.
3. Ask which wiki root it should use, such as docs/wiki/products, docs/wiki/companies, docs/wiki/agentic-frameworks, docs/wiki/models, or a project-specific folder.
4. Ask what source inputs it should read and what outputs it should leave for normal wiki maintenance.
5. Confirm the mapping before asking for another one.

Do not assume another project's topic roots apply. Treat examples such as products, companies, frameworks, models, and MCP servers as prompts for discovery, not defaults.

During new wiki setup, ask whether automated public update feeds are required. If the answer is yes, collect update feed topics one at a time:

1. Ask what public topic should be scanned.
2. Ask which wiki root owns the entity leaves for that topic.
3. Confirm the pair before asking for another topic.
4. Stop collecting topics when the user says there are no more.

Examples of wiki roots include docs/wiki/products for product updates, docs/wiki/companies for company updates, docs/wiki/agentic-frameworks for framework updates, docs/wiki/models for model updates, and docs/wiki/mcp-servers for MCP server updates.

After collecting topics, propose raw-only topic collectors plus a leaf refresher if the user wants existing entity pages checked over time. Use the target environment's approved automation facility for approved scheduled feeds rather than inventing a hand-written scheduler workaround.

## status

Use status at the beginning of wiki maintenance. It reports recursive page count, missing required files, orphan topic pages, and lint findings.

## suggest

Use suggest when files changed or a task names source documents. It maps likely source paths to wiki pages and prints a maintenance checklist. The mapping is intentionally idiomatic and favors standard pages such as topic-index.md, known-defects.md, and open-decisions.md when no domain page exists yet.

## link-leaves

Use link-leaves after durable leaf pages are created or updated. Run the leaf-link pass after creating or updating a durable leaf page. Use repository grep to find existing wiki mentions of each leaf title before finishing. A page that mentions a durable leaf title should link the first unlinked mention to that leaf unless the mention is inside a heading, code fence, or existing link.

Run:

```bash
python3 project-wiki-skill-root/scripts/wiki_ops.py link-leaves
```

Pass one or more leaf page paths to scope the pass to the pages touched in the current task. Use dry-run first when the expected link volume is uncertain.

## ingest

Ingest is the human-directed process of reading source files and updating the affected wiki pages. The script does not rewrite source-derived understanding for the agent.

For raw source ingest:

1. Read each unprocessed raw source file.
2. Extract named entities, including products, companies, models, model families, frameworks, techniques, protocols, standards, workflows, notable features, and security issues.
3. Update or create the durable leaf page for each entity under the most relevant topic folder.
4. Use focused research when the raw source names an entity without enough baseline explanation for a useful leaf, and cite the research sources.
5. Run the leaf-link pass for the created or updated leaves.
6. Update docs/wiki/digests/index.md and the relevant docs/wiki/digests/YYYY-MM.md monthly digest.
7. A digest entry may keep the date when the information was added or modified, but the text must summarize the content change rather than list page or file changes. Use one digest entry per independently changing item or closely coupled product family; do not bundle unrelated items into one dated paragraph. Keep monthly digest Current Understanding entries in reverse chronological order by entry date, newest first. Keep each entry to at most three lines and link it to the entity leaf that holds the details.
8. When repairing an existing digest, inspect the current month page for bundled dated paragraphs and rewrite the requested date range into item-level synopsis entries instead of only appending new entries. Reorder the affected Current Understanding entries into reverse chronological order by entry date before finishing. Use durable leaf pages as the content anchor for digest prose; keep source files in Authoritative Sources as provenance rather than repeating source-log wording. Do not create separate digest entries for duplicate raw captures or repeated source-window sightings unless they add distinct content; fold them into the existing item or closely coupled product-family entry.
9. Raw-source ingest automation prompts must repeat the digest granularity and ordering rules directly: one digest entry per independently changing item or closely coupled product family; never group digest entries by raw source artifact, collector run, sweep category, or ingestion batch; keep monthly digest Current Understanding entries in reverse chronological order by entry date.
10. When a digest page changes, the automation closeout must report that digest granularity and ordering were checked with the project-wiki-topic-verify checklist, or that the full verifier returned GOOD.
11. High-volume raw sources may update many durable leaves without forcing every touched leaf into the digest; omit low-signal digest mentions rather than compress unrelated entities into a vague grouped bullet.
12. Audit the created or updated topic pages for bundled leaf concepts. Split reusable practice patterns, workflows, operating agreements, governance rules, decisions, team structures, source snapshots, and evaluation questions when they can change independently.
13. Track the complete list of docs/wiki topic pages created or updated for that raw source file.
14. Run lint, then invoke a fresh no-fork subagent using $project-wiki-topic-verify. Pass only the repository root, the created or updated topic-page list, the current raw source path as evidence, and lint output.
15. Apply the explicit caller or owning-role correction-attempt cap to the pre-move verification gate. When no cap is supplied, allow at most two corrected resubmissions after the initial verifier verdict; the initial verdict does not count as a correction attempt.
16. If the verifier returns NEEDS_CORRECTION and correction attempts remain, apply the in-scope corrections in the main ingest context, rerun lint when files changed, and invoke a fresh verifier again.
17. If the verifier still returns NEEDS_CORRECTION after the governing cap is exhausted, stop and report BLOCKED with the unresolved findings, completed correction-attempt count, and governing cap.
18. Move fully processed raw files under raw/processed only after the pre-move verifier returns GOOD, preserving useful date or source subfolders.
19. Update wiki source links to the processed raw paths and add those topic pages to the verification list for that source.
20. Run lint again, then invoke a fresh no-fork verifier with the updated topic-page list and processed source path as evidence when any docs/wiki link changed.
21. Apply the same explicit caller or owning-role correction-attempt cap to the post-move verification gate. When no cap is supplied, allow at most two corrected resubmissions after the initial post-move verdict; the initial verdict does not count as a correction attempt. If the post-move verifier returns NEEDS_CORRECTION and correction attempts remain, apply the in-scope corrections in the main ingest context, rerun lint, and invoke a fresh verifier. If the verdict remains NEEDS_CORRECTION after the governing cap is exhausted, stop and report BLOCKED with the unresolved findings, completed correction-attempt count, and governing cap.
22. Leave incomplete raw files in place.

During ingest, use judgement when sources contain synonyms, aliases, overlapping concepts, or conflicting ideas. Normalize synonyms into the best durable entity page when they refer to the same thing. Use the agent's judgement to factor common ideas into the hub or leaf that owns the shared concept. Keep source-specific ideas clearly attributed to their source in the relevant leaf, scan page, digest note, or Maintenance Notes. Record unresolved conflicting ideas as Open Questions instead of flattening them into a false consensus.

The verifier is read-only. It verifies the created or updated topic pages, not the source material. It reports GOOD or NEEDS_CORRECTION and file-specific findings. The ingest agent owns all edits and repeats verification after corrections so the verifier's context remains independent from the main synthesis context.

## update-feeds

Use update-feeds when a wiki should keep watching public sources after setup.

Topic collectors should search public sources for approved topics, save dated raw artifacts under raw, and leave docs/wiki unchanged. They should include source URLs, visible dates, factual summaries, relevance notes, named entities, exclusions, and follow-up notes.

The leaf refresher should check entities already represented by durable leaf pages. Build the entity universe from the approved wiki roots, use each relative leaf path as the stable entity id, maintain a local state ledger, check new leaves first, then the oldest last-checked leaves, and break ties by stable path sort. A typical daily batch should be small enough to keep the run cheap while sweeping all leaves regularly.

Leaf refresher output is raw source material. Save qualifying updates under raw, validate structured JSON artifacts when possible, and let the normal ingest workflow update entity leaves, digests, and raw/processed links.

Do not send private, proprietary, sensitive, PII, or company-internal local content to an external service. Search with public entity names, aliases, and public source URLs rather than whole local wiki pages when possible.

## reconcile

Use reconcile when code, specs, plans, tests, and backlog items may disagree. Read source-priority.md first, then update the wiki with the resolved current understanding or an explicit open question.

## lint

Use lint before finishing any task that creates or edits docs/wiki pages. It scans topic folders recursively. Fix missing sections, broken local links, and orphan topic pages before completion.

## okf-migrate

Use okf-migrate when a wiki needs OKF frontmatter or when topic titles, descriptions, or folder placement changed enough that frontmatter should be refreshed.

Run:

```bash
python3 project-wiki-skill-root/scripts/wiki_ops.py okf-migrate
```

Use --dry-run first when you want to inspect the number of concept documents that would change.

## okf-validate

Use okf-validate after okf-migrate and before finishing wiki maintenance. It verifies that non-reserved Markdown concept documents have YAML frontmatter with a non-empty type field and that reserved index.md and log.md files keep their OKF reserved shape.

Run:

```bash
python3 project-wiki-skill-root/scripts/wiki_ops.py okf-validate
```

## commit handling

When committing a task, include docs/wiki pages, raw fragments, raw/processed moves, wiki helper scripts, and related AGENTS.md guidance in the same coherent commit as the source, test, or documentation changes that made them necessary. If a task changes only wiki artifacts, commit that verified wiki-only slice on its own. Do not leave docs/wiki, raw fragments, or raw/processed moves unstaged after committing the related task. If repository or user instructions forbid committing, report the remaining wiki artifacts explicitly.

## sources

Use sources when answering questions from a wiki page. It extracts the local source paths named by that page so the agent can verify the current source before answering.

## questions

Use questions when the user asks to review, answer, close, or list unresolved wiki questions. It scans Open Questions sections under docs/wiki and prints each unresolved question with file and line. Ask the human one listed question at a time, update the relevant wiki page from the answer, run questions again to confirm the item is gone, then run lint before finishing.
