---
name: project-wiki-research
description: Use when a user asks for ad-hoc or on-demand research for a repository project wiki topic, asks whether the wiki already covers a topic before researching it, or wants a sourced report saved under raw for later project-wiki ingest.
metadata:
  category: wiki-and-knowledge
---

# Project Wiki Research

## Overview

Use this skill for one-off research requests that should feed a repository wiki without bypassing the raw-source boundary. First answer from existing wiki coverage when it is sufficient; only missing or stale coverage becomes a sourced raw report for later project-wiki ingest.

## Read First

- Read the shared project-wiki skill before changing wiki-related files.
- Read docs/wiki/federation.md when the repository has an upstream or sibling wiki relationship.
- Read project-wiki-query when the request is mainly a lightweight answer from existing wiki coverage.

## Workflow

1. Run project-wiki status from the repository root when docs/wiki exists.
2. Search docs/wiki for the requested topic, synonyms, aliases, and named entities. Read topic-index.md plus the most relevant hub and leaf pages.
3. In federated wikis, search the upstream wiki root and upstream topic index before declaring a gap.
4. If existing wiki coverage answers the request, reply with the relevant wiki page links and stop. Do not create a raw report just to duplicate existing coverage.
5. If the wiki lacks the information, choose research sources appropriate to the topic. Prefer official documentation, specifications, source repositories, papers, changelogs, primary announcements, standards, and reputable secondary analysis. Use web search when freshness or outside evidence matters.
6. Do not send private, proprietary, sensitive, PII, or company-internal content to an external service unless the user explicitly instructed that it may be used.
7. Save one raw report under raw using a stable filename:

```text
raw/project-wiki-research-YYYY-MM-DD-short-topic.md
```

8. Stop on a destination collision instead of overwriting an existing raw file.
9. Leave the report in raw, not raw/processed. Do not edit docs/wiki unless the user explicitly asks for immediate synthesis.
10. Report the raw path, the wiki pages checked, and the recommended ingest destination.

## Raw Report Template

Use this structure for the raw file:

```markdown
# Project Wiki Research: Short Topic

## Request

## Existing Wiki Check

## Research Scope

## Source Inventory

## Synthesis

## Named Entities And Concepts

## Candidate Wiki Destinations

## Existing Pages To Link

## Conflicts Or Uncertainties

## Excluded Sources Or Claims

## Privacy And Sensitivity Notes

## Follow-Up For Ingest
```

Keep the synthesis compact but evidence-rich. Include source URLs, visible publication or update dates when available, access date for volatile pages, and a short reliability note for each source. Mark facts that are inferred rather than directly stated.

## Existing Coverage Decision

Existing coverage is sufficient when the wiki has a durable page that answers the user's actual question, names the relevant source or authority, and does not obviously need freshness verification. A digest entry, raw source link, or scattered mentions may help discovery, but they are not sufficient when the request needs a durable concept explanation, comparison, decision, or current research synthesis.

## Research Boundaries

- For public ecosystem topics, search public sources only and capture public source links.
- For project-local behavior, verify from authoritative local files before using external sources.
- For federated wikis, route broad upstream-owned entity background to the upstream wiki and keep downstream reports focused on local practice, workflow, governance, implementation, evaluation, or adoption lens.
- For time-sensitive topics, record concrete dates and exclude date-only boundary items when the exact publication time matters and cannot be confirmed.

## Verification

Before replying:

- Confirm the report path is under raw and outside raw/processed.
- Confirm the report names the wiki pages and upstream pages checked.
- Confirm local links are repository-relative or otherwise portable.
- Run project-wiki lint only if docs/wiki changed. Raw-only research reports do not require docs/wiki lint.
- Run git diff --check when the repository has git and the task changed tracked or staged files.

## Common Mistakes

- Starting with web research before checking docs/wiki and upstream wiki coverage.
- Creating a docs/wiki page during a raw-only research task.
- Saving a one-off research report in a dated collector folder when the user asked for raw.
- Treating a digest mention as sufficient durable coverage.
- Omitting excluded sources, failed searches, or unresolved conflicts that the ingest agent will need later.
