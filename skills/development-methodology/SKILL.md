---
name: development-methodology
description: Use when creating or revising software project documentation, choosing a methodology template, or routing setup, reverse engineering, code wiki, or page verification work.
---

# Development Methodology

Use this skill as the router for software project documentation work from this bundle. It keeps the shared page contract, document type selection, and template asset policy in one place while delegating specialized workflows to focused skills.

## Required Companion Skills

- Use documentation-bootstrap for first-time setup in a target repository.
- Use documentation-reverse-engineering when deriving documentation from an existing codebase.
- Use code-project-wiki for code-aware docs/wiki maintenance, commit-range sync, Related Code upkeep, or Related Tests upkeep.
- Use project-wiki-review before finishing project wiki pages or project-wiki-template artifacts.
- Use functional-spec-review before finishing functional specification artifacts.
- Use architecture-review before finishing architecture artifacts.
- Use high-level-design-review before finishing high-level design artifacts.
- Use module-design-review before finishing module design artifacts.
- Use documentation-page-verifier for shared checks on mixed, unknown, or custom documentation artifacts.
- Use project-wiki before creating, maintaining, or validating docs/wiki content.
- Use project-wiki-query for wiki-backed project questions.
- Use project-wiki-research for sourced raw reports that should feed a wiki later.
- Use project-wiki-topic-writer and project-wiki-topic-verifier when editing or validating topic pages.

## Shared Page Contract

Every durable documentation page starts with these sections:

- Current Understanding
- Authoritative Sources
- Related Code
- Related Tests
- Related Backlog Items
- Related Wiki Pages
- Open Questions
- Maintenance Notes

Functional specifications, architecture documents, high-level designs, and module designs are page subclasses. They keep the shared sections first, then append the specialized sections from their matching template.

## Document Type Selection

Use the smallest document type that fully explains the work:

- Project wiki page: durable synthesis, navigation, code ownership, known defects, open decisions, glossary, or recurring topic knowledge.
- Functional specification: user-visible behavior, actor workflow, route behavior, acceptance criteria, permissions, status display, operational affordance, or error state.
- Architecture: project-wide boundary, technology choice, shared rule, cross-cutting concern, layer relationship, persistence, security, privacy, observability, or UI composition.
- High-level design: coherent subsystem, feature family, system slice, integration path, or multi-module implementation plan.
- Module design: one module, service, class, task, utility, UI component, or tightly scoped feature unit.

## Template Assets

Template assets live under skills/development-methodology/assets/templates.

- project-wiki-template.md defines project wiki setup and code-aware maintenance rules.
- functional-spec-template.md defines user-visible workflow and acceptance documentation.
- architecture-template.md defines project-wide and cross-cutting architecture documentation.
- high-level-design-template.md defines subsystem and feature-family documentation.
- module-design-template.md defines one-module design documentation.

When a target project needs a local editable document, copy only the matching template into that project's chosen documentation location and replace every TODO instruction with source-backed content. Do not create a second reusable template distribution in the target repository unless the user asks for local project-owned templates.

## Workflow

1. Inspect the target repository before writing documentation. Identify source roots, test roots, existing docs, wiki root, procedures, backlog files, build commands, and current worktree status.
2. Choose the document type from the source evidence and the user's requested outcome.
3. Copy the matching template asset only when a new or refreshed document is needed.
4. Replace every TODO instruction with project-specific content backed by source links.
5. Remove a section only when it is genuinely not applicable.
6. Write steady-state documentation. Do not frame the page around old versus new behavior unless the section is explicitly historical.
7. Link code, tests, procedures, backlog items, source documents, and wiki pages at the point where the prose depends on them.
8. Add diagrams only where a real relationship is easier to inspect visually, such as sequence, ownership, dependency, lifecycle, data flow, or verification coverage.

## Verification

Before finishing documentation or wiki work:

1. Use the artifact-specific review skill when the artifact type is project wiki, functional specification, architecture, high-level design, or module design.
2. Use documentation-page-verifier for mixed, unknown, or custom documentation artifacts.
3. Run project wiki status and lint when docs/wiki exists.
4. Run OKF validation when topic pages changed.
5. Run the repository agent-skill validator when skill files changed.
6. Refresh shared skill installs from this source repository when bundled skill files changed.
7. Run the target project build when code, imports, generated artifacts, or project metadata changed.
8. Search generated documents for unresolved TODO markers that are not intentional.
9. Confirm every created document names related source, tests, or Not yet identified.
10. Confirm wiki changes follow the project-wiki verifier checklist when topic pages changed.

Do not send private, proprietary, sensitive, PII, or company-internal material to an external service unless the user explicitly authorizes it.
