---
type: Skill
name: development-methodology
description: Use when creating or revising software project documentation from this bundle's templates, setting up docs/wiki as a development project wiki, reverse-engineering documentation from code, choosing between functional specs, architecture, high-level design, module design, and project wiki pages, or copying template assets into a target repository.
---

# Development Methodology

Use this skill to apply the bundled development documentation methodology and templates to a software project.

The project wiki page contract is the base document shape. Functional specifications, architecture documents, high-level designs, and module designs extend that base shape with specialized sections.

## Read First

- Read references/documentation-methodology.md when choosing document types, folder layout, page inheritance, diagram policy, or project wiki operating model.
- Read references/procedure-reverse-engineer-project-documentation.md when deriving documentation from an existing codebase.
- Use $project-wiki before creating, maintaining, or validating docs/wiki content.
- Use $project-wiki-query for wiki-backed project questions.
- Use $project-wiki-research for sourced raw reports that should feed a wiki later.
- Use $project-wiki-topic-writer and $project-wiki-topic-verifier when editing or validating topic pages.

## Bundled Templates

Template assets live under assets/templates.

- project-wiki-template.md defines project wiki setup and maintenance rules.
- functional-spec-template.md defines user-visible workflow and acceptance documentation.
- architecture-template.md defines project-wide and cross-cutting architecture documentation.
- high-level-design-template.md defines subsystem and feature-family documentation.
- module-design-template.md defines one-module design documentation.

## Workflow

1. Inspect the target repository before writing documentation. Identify source roots, test roots, existing docs, wiki root, procedures, backlog files, build commands, and current worktree status.
2. Choose the smallest useful document type. Use functional specs for observable behavior, architecture for project-wide boundaries, high-level design for multi-module subsystems, module design for one implementation unit, and project wiki pages for durable synthesis and navigation.
3. Copy the matching template from assets/templates into the target project documentation location.
4. Replace every TODO instruction with source-backed project content. Remove sections only when they are genuinely not applicable.
5. Preserve the shared wiki-compatible sections at the start of each durable document: Current Understanding, Authoritative Sources, Related Code, Related Tests, Related Backlog Items, Related Wiki Pages, Open Questions, and Maintenance Notes.
6. Write steady-state documentation. Do not frame the page around old versus new behavior unless the section is explicitly historical.
7. Link code, tests, procedures, backlog items, and source documents at the point where the prose depends on them.
8. Use Mermaid diagrams only where a real relationship is easier to inspect visually, such as sequence, ownership, dependency, lifecycle, data flow, or verification coverage.

## Development Project Wiki Shape

For a code project wiki like gemma-chat-public, prefer this shape unless the target repository already has a stronger convention:

```text
docs/wiki/
  README.md
  schema.md
  topic-index.md
  glossary.md
  open-decisions.md
  known-defects.md
  maintenance-log.md
  technical/
  subsystems/
  modules/
  functional/
  code/
  digests/
raw/
  wiki-fragments/
  processed/
```

Use raw/wiki-fragments for durable project knowledge found while reading project files but not yet synthesized into docs/wiki. Keep fragments out of raw/processed until synthesis and wiki lint have passed.

## Verification

Before finishing documentation or wiki work:

1. Run project wiki status and lint when docs/wiki exists.
2. Run OKF validation when topic pages or skill files changed.
3. Run the target project build when code, imports, generated artifacts, or project metadata changed.
4. Search generated documents for unresolved TODO markers that are not intentional.
5. Confirm every created document names related source, tests, or Not yet identified.
6. Confirm wiki changes follow the project-wiki verifier checklist when topic pages changed.

Do not send private, proprietary, sensitive, PII, or company-internal material to an external service unless the user explicitly authorizes it.
