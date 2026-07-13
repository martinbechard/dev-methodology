# Topic Page Verification Checklist

Use this checklist when verifying created or updated docs/wiki topic pages, especially after raw source ingest. The goal is to prevent broad topic files from absorbing facts that belong in durable leaf pages. The verifier judges the topic pages, not the source material. Source material is evidence only.

## Inputs

- The verifier received the repository root.
- The verifier received the complete list of created or updated docs/wiki topic pages.
- The verifier received raw source paths, processed source paths, or other authoritative source paths only as evidence for those topic pages.
- The verifier inspected the relevant topic-index, folder hub pages, digest pages, and federation page when they affect the created or updated topic pages.

## Granularity

- Broad domains are represented as folders with an index.md hub when several concepts, sources, workflows, providers, or decisions can change independently.
- Hubs stay short and navigational. They define the domain, link to leaf pages, and record domain-level questions.
- Leaf pages exist for recurring or independently changing entities, including products, companies, model families, specific models, frameworks, techniques, protocols, standards, workflows, security issues, and durable practice patterns.
- Leaf pages exist for reusable practice patterns, operating agreements, governance rules, decisions, evaluation questions, team structures, source snapshots, and named methods when those concepts can be updated or linked independently.
- Dated scan pages or source-synthesis pages are not the only wiki surface for independently changing entities.
- Facts that affect current understanding, selection criteria, adoption caveats, governance, security, or implementation relevance are promoted from dated scans into the matching durable leaf page.
- No created or updated hub or omnibus topic file is growing mainly because new entities were appended there instead of being split into leaves.

## Leaf Concept Audit

- The verifier identifies title-like phrases, bullets, and paragraphs that describe reusable concepts.
- A concept is a leaf candidate when it can change independently, has distinct source evidence, would be useful to link from another page, or carries guidance a future agent may need to load independently.
- Created or updated pages do not bundle multiple meaningful leaf candidates unless the page links existing leaves, links upstream-owned coverage, or records a clear deferral.
- For every unsplit leaf candidate, the verifier returns NEEDS_CORRECTION with the candidate name, the proposed folder, and the reason it deserves a leaf.
- For adoption and operating model pages, likely leaf candidates include workflow-before-model selection, human-agent approval boundaries, durable instruction and skill-file management, tier-specific assistant behavior, outcome alignment versus process standardization, senior-led agentic execution pods, and junior learning paths in agentic teams.

## Topic Page Coverage Against Source Evidence

- Each named entity from the source evidence that affects the created or updated topic pages was either mapped to an existing durable leaf, used to create a new durable leaf, linked to an upstream-owned page, or explicitly deferred with a reason in Open Questions or Maintenance Notes.
- Synonyms and aliases were normalized into the best existing entity page when they refer to the same thing.
- Source-specific framing is attributed to the source and is not converted into a universal claim without support.
- Paragraphs that use multiple sources state the shared rule, scope distinction, tension, or source-specific boundary. They do not merely stack source summaries.
- Conflicts between sources are preserved as Open Questions or attributed notes rather than flattened into false consensus.
- If an entity is mentioned without enough explanation for a useful leaf, the page includes a compact baseline from reliable focused research or records why the baseline is still missing.

## Page Contract

- Non-reserved Markdown concept documents should have YAML frontmatter with a non-empty type field.
- Every non-reserved created or updated Markdown concept document has OKF YAML frontmatter with a non-empty type field.
- Folder index.md and log.md files are OKF reserved files and do not carry concept frontmatter.
- Every created or updated topic page has one H1 title.
- Every created or updated topic page has the standard sections: Current Understanding, Authoritative Sources, Related Code, Related Tests, Related Backlog Items, Related Wiki Pages, Open Questions, and Maintenance Notes.
- Missing source, code, test, or backlog evidence is stated as Not yet identified.
- A page with no unresolved questions says No open wiki questions are recorded for this topic.
- Additional topic-specific sections clarify the topic without replacing the standard contract.
- Maintenance Notes explain why the page changed and what should be checked next.

## Sources And Links

- Authoritative Sources point to the source artifacts, procedures, specifications, code, tests, or upstream wiki pages that support the page.
- Named source artifacts, decks, procedures, pages, and external references are Markdown links at the point of use in prose.
- The Authoritative Sources section does not substitute for contextual links when prose names or compares sources.
- Local source links use the correct location after processing. Fully processed sources point under raw/processed.
- Raw and raw/processed source links are relative to the wiki page. Absolute filesystem paths for raw sources are invalid, including /Users/raw, /raw, and repository-absolute raw paths.
- Local wiki links are Markdown links and resolve from the page where they appear.
- Monthly digest entries link to the durable leaves that hold the details.
- The relevant topic-index entry or folder hub links any newly created durable leaf.
- Run the leaf-link pass after creating or updating a durable leaf page.
- Run python3 project-wiki-skill-root/scripts/wiki_ops.py link-leaves from the repository root for the leaf-link pass.
- Run python3 project-wiki-skill-root/scripts/wiki_ops.py okf-migrate when concept frontmatter is missing or stale.
- Run python3 project-wiki-skill-root/scripts/wiki_ops.py okf-validate before accepting topic pages.
- Use repository grep to find existing wiki mentions of each leaf title before finishing.
- A page that mentions a durable leaf title should link the first unlinked mention to that leaf unless the mention is inside a heading, code fence, or existing link.
- No source path, code path, test path, backlog item, behavior, fallback, or compatibility constraint is invented.

## Digest And Raw Boundaries

- docs/wiki/digests/index.md remains a hub when digests are used.
- The relevant docs/wiki/digests/YYYY-MM.md entry may keep the date when information was added or modified, but it summarizes the content change instead of listing page or file changes.
- The relevant docs/wiki/digests/YYYY-MM.md page uses one digest entry per independently changing item or closely coupled product family; it does not bundle unrelated items into one dated paragraph.
- The relevant docs/wiki/digests/YYYY-MM.md Current Understanding entries appear in reverse chronological order by entry date, newest first; same-date entries keep a stable content order unless a clearer local grouping is needed.
- The relevant docs/wiki/digests/YYYY-MM.md entry is at most three lines for the source and leaves detailed background in the relevant leaf page.
- When repairing an existing digest, inspect the current month page for bundled dated paragraphs and rewrite the requested date range into item-level synopsis entries instead of only appending new entries.
- Reorder the affected Current Understanding entries into reverse chronological order by entry date before finishing.
- Use durable leaf pages as the content anchor for digest prose; keep source files in Authoritative Sources as provenance rather than repeating source-log wording.
- Do not create separate digest entries for duplicate raw captures or repeated source-window sightings unless they add distinct content; fold them into the existing item or closely coupled product-family entry.
- Raw-source ingest automation prompts must repeat the digest granularity and ordering rules directly: one digest entry per independently changing item or closely coupled product family; never group digest entries by raw source artifact, collector run, sweep category, or ingestion batch; keep monthly digest Current Understanding entries in reverse chronological order by entry date.
- When a digest page changes, the automation closeout must report that digest granularity and ordering were checked with the project-wiki-topic-verify checklist, or that the full verifier returned GOOD.
- High-volume raw sources may update many durable leaves without forcing every touched leaf into the digest; omit low-signal digest mentions rather than compress unrelated entities into a vague grouped bullet.
- Raw source files stay outside raw/processed until the source has been synthesized into leaves and digests, lint passes, and pre-move verification has accepted the content.
- After a processed-source move changes source links, the verifier checks the processed source path and the updated links before the ingest is complete.
- Source collection artifacts remain raw-only. Ingest owns docs/wiki changes.

## Federation

- When docs/wiki/federation.md declares an upstream wiki owner, the verifier checks whether created or updated local pages duplicate upstream-owned entity analysis.
- Upstream-owned entities are linked upstream and summarized only as needed for local navigation.
- Local pages for upstream-owned entities keep a downstream lens: usage guidance, operating model, evaluation criteria, practice pattern, governance rule, or project decision.
- Missing or conflicting upstream coverage is recorded as an open question when the downstream wiki needs it.

## Writing Quality

- Explanations use steady-state language.
- Comparative words such as enhanced, revised, old, or new are avoided unless documenting history in Maintenance Notes.
- Pages stay compact enough for agents to load with source documents.
- Claims are concrete, attributed, and useful for future maintenance.
- The content reads as company-facing project context when the wiki is for AI-assisted development practice, not as a personal scratchpad.

## Verification Outcome

- The verifier ran the project-wiki lint command from the repository root when available.
- The verifier ran project-wiki OKF validation from the repository root when available.
- The verifier returns GOOD only when every applicable checklist item passes for the created or updated topic pages and lint has no findings.
- The verifier returns NEEDS_CORRECTION when any applicable item fails, including unsplit leaf candidates, with file-specific corrections the main agent can apply.
