---
name: create-architecture
description: Use when creating or substantially rewriting an architecture artifact from the development-methodology architecture-template asset, including system scope, context, technology stack, file organization, layers, components, data flow, lifecycle, cross-cutting concerns, risks, invariants, and verification.
---

# Create Architecture

Use this skill to create or substantially rewrite one architecture artifact. The artifact explains a whole system, project-wide boundary, or cross-cutting concern without duplicating every module detail.

## Template

Use skills/development-methodology/assets/templates/architecture-template.md as the starting asset.

Copy the template only when a local editable artifact is needed. Replace every TODO instruction with source-backed content from the target repository.

## Scope

Create one architecture artifact that defines:

- Scope.
- System context.
- Technology stack.
- File organization.
- Architectural layers.
- Key components.
- Diagram authoring rules.
- Data flow.
- Lifecycle flow.
- Cross-cutting concerns.
- Design principles.
- Invariants.
- Risks and trade-offs.
- Verification.

Use create-high-level-design when the work is one subsystem or feature family. Use create-module-design when the work is one module, service, component, task, utility, or tightly scoped implementation unit.

Use documentation-reverse-engineering when the user asks to derive an architecture set from an existing codebase.

## Workflow

1. Inspect the target repository before writing. Read README files, agent instructions, procedures, package metadata, build configuration, runtime entry points, source roots, tests, scripts, docs, wiki pages, backlog files, and current worktree status.
2. Identify the system boundary, runtime assumptions, ownership boundaries, dependency directions, persistence boundaries, external systems, and verification evidence.
3. Copy the architecture template into the target documentation location when a new artifact is needed.
4. Replace each TODO with source-backed architecture content.
5. Keep the shared page contract sections first.
6. Use diagrams only where boundaries, dependencies, data movement, lifecycle states, ownership, or verification coverage are easier to inspect visually.
7. Say Not yet identified for related code, tests, backlog items, or wiki pages that do not exist yet.
8. Keep risks, trade-offs, and open questions concrete enough to guide future implementation and review.
9. Keep the artifact steady-state. Do not describe it as new, revised, or enhanced unless the document is explicitly a change plan.

## Verification

Before finishing:

1. Use review-architecture on the completed artifact.
2. Use documentation-page-verifier with the artifact, source evidence, and completed review checklist when the review skill calls for it.
3. Run project wiki status and lint when docs/wiki exists and the artifact lives in or links from docs/wiki.
4. Search the artifact for unresolved TODO markers that are not intentional.
5. Confirm every architectural claim names source evidence, a verification path, or an open question.

Do not send private, proprietary, sensitive, PII, or company-internal material to an external service unless the user explicitly authorizes it.
