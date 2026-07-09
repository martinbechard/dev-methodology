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
- Use create-agents-plan when creating or substantially rewriting an AGENTS-PLAN.yaml project agent and skill routing plan.
- Use create-project-wiki when creating or substantially rewriting a project wiki methodology artifact from the project wiki template.
- Use create-functional-spec when creating or substantially rewriting a functional specification artifact from the functional specification template.
- Use create-architecture when creating or substantially rewriting an architecture artifact from the architecture template.
- Use create-high-level-design when creating or substantially rewriting a high-level design artifact from the high-level design template.
- Use create-module-design when creating or substantially rewriting a module design artifact from the module design template.
- Use review-project-wiki before finishing project wiki pages or project-wiki-template artifacts.
- Use review-functional-spec before finishing functional specification artifacts.
- Use review-architecture before finishing architecture artifacts.
- Use review-high-level-design before finishing high-level design artifacts.
- Use review-module-design before finishing module design artifacts.
- Use documentation-page-verifier for shared checks on mixed, unknown, or custom documentation artifacts.
- Use project-wiki before creating, maintaining, or validating docs/wiki content.
- Use project-wiki-query for wiki-backed project questions.
- Use project-wiki-research for sourced raw reports that should feed a wiki later.
- Use project-wiki-topic-writer and project-wiki-topic-verifier when editing or validating topic pages.

## Loading Discipline

Load only the skills needed for the current job. Use this skill to choose the artifact type and route, then load the matching creation skill or review skill for that artifact. Do not load every creation or review skill just because the catalog contains them.

For a normal creation job, load this skill and exactly one artifact creation skill, plus source-domain skills that the repository evidence requires. Load the matching review skill only when the artifact is ready to review. Use documentation-page-verifier for mixed, unknown, or custom artifacts, or when an artifact review skill calls for it.

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
- AGENTS-PLAN.yaml: project agent and skill setup, root AGENTS.md routing reference, nested plan placement, role loadouts, folder routing, validation evidence, proprietary validation notes, or customer-safe fictitious examples.
- Functional specification: user-visible behavior, actor workflow, route behavior, acceptance criteria, permissions, status display, operational affordance, or error state.
- Architecture: project-wide boundary, technology choice, shared rule, cross-cutting concern, layer relationship, persistence, security, privacy, observability, or UI composition.
- High-level design: coherent subsystem, feature family, system slice, integration path, or multi-module implementation plan.
- Module design: one module, service, class, task, utility, UI component, or tightly scoped feature unit.

## Artifact Creation Routes

Use this route table when the task is to create or substantially rewrite a methodology artifact:

- Project wiki methodology artifact: use create-project-wiki, template project-wiki-template.md, and review-project-wiki.
- Agent and skill routing plan: use create-agents-plan, template agents-plan-template.yaml, and documentation-page-verifier.
- Functional specification artifact: use create-functional-spec, template functional-spec-template.md, and review-functional-spec.
- Architecture artifact: use create-architecture, template architecture-template.md, and review-architecture.
- High-level design artifact: use create-high-level-design, template high-level-design-template.md, and review-high-level-design.
- Module design artifact: use create-module-design, template module-design-template.md, and review-module-design.

Use project-wiki-topic-writer for ordinary docs/wiki topic pages that summarize or link source material without becoming one of the specialized methodology artifacts. Use documentation-reverse-engineering when the user asks for a source-derived documentation set rather than one artifact.

## Template Assets

Template assets live under skills/development-methodology/assets/templates.

- project-wiki-template.md defines project wiki setup and code-aware maintenance rules.
- agents-plan-template.yaml defines project agent roles, skill loadouts, AGENTS.md routing references, folder routing, nested plan placement, proprietary validation notes, and customer-safe example boundaries.
- functional-spec-template.md defines user-visible workflow and acceptance documentation.
- architecture-template.md defines project-wide and cross-cutting architecture documentation.
- high-level-design-template.md defines subsystem and feature-family documentation.
- module-design-template.md defines one-module design documentation.

When a target project needs a local editable document, copy only the matching template into that project's chosen documentation location and replace every TODO instruction with source-backed content. Do not create a second reusable template distribution in the target repository unless the user asks for local project-owned templates.

## Workflow

1. Inspect the target repository before writing documentation. Identify source roots, test roots, existing docs, wiki root, procedures, backlog files, build commands, and current worktree status.
2. Choose the document type from the source evidence and the user's requested outcome.
3. Load the matching artifact creation skill from the route table when creating or substantially rewriting a methodology artifact.
4. Copy the matching template asset only when a new or refreshed document is needed.
5. Replace every TODO instruction with project-specific content backed by source links.
6. Remove a section only when it is genuinely not applicable.
7. Write steady-state documentation. Do not frame the page around old versus new behavior unless the section is explicitly historical.
8. Link code, tests, procedures, backlog items, source documents, and wiki pages at the point where the prose depends on them.
9. Add diagrams only where a real relationship is easier to inspect visually, such as sequence, ownership, dependency, lifecycle, data flow, or verification coverage.

## Verification

Before finishing documentation or wiki work:

1. Use the artifact-specific review skill when the artifact type is project wiki, functional specification, architecture, high-level design, or module design.
2. Use documentation-page-verifier for mixed, unknown, or custom documentation artifacts.
3. Run project wiki status and lint when docs/wiki exists.
4. Run OKF validation when topic pages changed.
5. Run the repository agent-skill validator when skill files changed.
6. When a bundled skill is renamed or deleted, sweep the source repository for the old skill id and update or remove references in skills, companion-skill lists, Codex metadata, role definitions, dispatch profiles, aggregate workflow examples, design documents, scripts, and tests.
7. Run scripts/openai_metadata.py skills after bundled skill name or description changes so Codex interface metadata stays aligned with SKILL.md while policy and dependencies remain hand-authored.
8. Refresh shared skill installs from this source repository when bundled skill files changed. When a skill was renamed or deleted, confirm the refresh reports the obsolete owned skill as pruned or reports that prune was skipped because no ownership manifest existed. Do not remove unowned local skills manually. If standalone agent definition folders are added later, track them in the ownership manifest before enabling prune behavior for them.
9. Run the target project build when code, imports, generated artifacts, or project metadata changed.
10. Search generated documents for unresolved TODO markers that are not intentional.
11. Confirm every created document names related source, tests, or Not yet identified.
12. Confirm wiki changes follow the project-wiki verifier checklist when topic pages changed.

Do not send private, proprietary, sensitive, PII, or company-internal material to an external service unless the user explicitly authorizes it.
