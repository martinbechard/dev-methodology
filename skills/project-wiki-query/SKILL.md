---
name: project-wiki-query
description: Answer questions from a repository docs/wiki synthesis layer and authoritative project files. Use when the agent is asked what the project knows, how a documented workflow works, what a wiki-covered concept means, or any repo question where docs/wiki should be checked first. Also use when an interactive answer reveals durable, source-backed project knowledge that is absent, scattered, or only implied in the wiki, so the agent can save a raw query fragment for later project-wiki ingest instead of editing docs/wiki immediately.
---

# Project Wiki Query

Use this skill for wiki-backed questions and lightweight exploration. It answers from the wiki first, verifies against authoritative files, and captures query-derived knowledge gaps as raw source fragments for the normal project-wiki ingest workflow.

## Read First

Read the shared project-wiki instructions before answering:

- ../project-wiki/SKILL.md
- ../project-wiki/references/source-priority.md when wiki content and source files may conflict.
- ../project-wiki/references/operations.md when raw fragments, processed raw links, or ingest boundaries are involved.

## Query Workflow

1. Run the wiki status command when a repository wiki is present.
2. Search docs/wiki for the user's topic before answering.
3. Read the most relevant wiki pages, then verify the answer against authoritative project files or public sources when the question requires freshness, precision, or source attribution.
4. Answer the user from the verified synthesis. Say when the wiki has no dedicated page or when the answer is inferred from scattered pages.
5. Decide whether the query uncovered durable missing knowledge using the raw-fragment trigger below.
6. If the trigger passes and mutation is allowed, create one raw query fragment under raw/query. If mutation is not allowed, say what fragment should be created and why.
7. Do not update docs/wiki directly unless the user explicitly asks for immediate wiki edits. The raw monitor owns later synthesis into docs/wiki.

## Raw Fragment Trigger

Create a raw query fragment when the answer reveals reusable, source-backed knowledge that is not yet captured cleanly in docs/wiki.

The trigger usually passes when at least one of these is true:

- A concept spans multiple existing pages, providers, products, models, techniques, workflows, decisions, or evaluation concerns.
- The wiki has only company, product, model, digest, or dated source coverage, but no durable concept page for the shared idea.
- The answer identifies a recurring implementation pattern, governance rule, evaluation question, workflow category, or source-routing rule that future agents should load independently.
- The query resolves or clarifies a durable relationship among existing leaves, such as a cross-provider category, local versus upstream ownership, or a missing hub page.

The trigger usually does not pass when the answer is only a one-off explanation, a purely conversational summary, a speculative idea without source evidence, or a fact already captured in a suitable durable page.

## Raw Fragment Location

Save query fragments under raw/query using a stable date-prefixed filename:

```text
raw/query/YYYY-MM-DD-short-topic.md
```

If raw/query does not exist and mutation is allowed, create it. Never place query fragments under raw/processed. The ingest automation moves only fully processed sources there after synthesis and lint.

## Raw Fragment Content

Use this structure:

```markdown
# Query Fragment: Short Topic

## Query Asked

## Answer Summary

## Wiki Pages Consulted

## Authoritative Sources Consulted

## Durable Concepts Detected

## Candidate Wiki Destinations

## Existing Pages To Link

## Open Questions

## Privacy And Sensitivity Notes

## Ingest Rationale
```

Keep the fragment factual and compact. It should preserve enough evidence for the raw monitor to decide what docs/wiki pages to create or update. Link local wiki pages and source files with paths that will remain portable within the repository. Do not include private, proprietary, sensitive, PII, or company-internal content unless the user explicitly instructed that material may be captured.

## Destination Guidance

Suggest candidate wiki destinations instead of forcing the final page design. Prefer the smallest durable topic boundary:

- update an existing leaf when the concept already has a home;
- create a new leaf when the concept can change independently;
- create or update a folder hub when several related leaves are forming;
- in a federated wiki, route broad upstream-owned entities to the upstream wiki and keep only the local practice, workflow, governance, implementation, evaluation, or adoption lens.

## Reporting

In the answer, mention whether a raw query fragment was created. If none was created, briefly say why when the user is asking about wiki coverage or maintainability.
