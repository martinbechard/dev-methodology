---
name: create-high-level-design
description: Use when creating or substantially rewriting a high-level design artifact from the development-methodology high-level-design-template asset, including subsystem scope, parent architecture, data anchors, constituent components, interaction model, lifecycle, contracts, configuration, implementation order, invariants, and verification.
metadata:
  category: artifact-creation
---

# Create High-Level Design

Use this skill to create or substantially rewrite one high-level design artifact. The artifact explains a coherent subsystem, feature family, integration path, or multi-module implementation plan.

## Template

Use skills/development-methodology/assets/templates/high-level-design-template.md as the starting asset.

Copy the template only when a local editable artifact is needed. Replace every TODO instruction with source-backed content from the target repository.

## Scope

Create one high-level design that defines:

- Parent architecture.
- Scope.
- Current data anchors.
- Constituent components.
- Interaction model.
- Lifecycle.
- Data shapes and contracts.
- Configuration.
- Implementation order.
- Invariants.
- Non-goals.
- Definition of good.
- Verification.

Use create-architecture when the work defines a whole system, project-wide boundary, technology choice, layer model, or cross-cutting concern. Use create-module-design when the work is one module, service, component, task, utility, or tightly scoped implementation unit.

Use documentation-reverse-engineering when the user asks to derive subsystem designs from an existing codebase.

## Workflow

1. Inspect the target repository before writing. Read parent architecture, functional specifications, module designs, source roots, relevant code, tests, procedures, configuration, backlog files, wiki pages, and current worktree status.
2. Identify subsystem boundaries, components, data anchors, contracts, lifecycle, configuration ownership, implementation order, invariants, and verification evidence.
3. Copy the high-level design template into the target documentation location when a new artifact is needed.
4. Replace each TODO with source-backed subsystem content.
5. Keep the shared page contract sections first.
6. Link constituent module design documents when they exist and identify missing module designs when they are needed.
7. Use diagrams only where component collaboration, lifecycle, contracts, configuration, implementation order, or verification coverage are easier to inspect visually.
8. Say Not yet identified for related code, tests, backlog items, or wiki pages that do not exist yet.
9. Keep the artifact steady-state. Do not describe it as new, revised, or enhanced unless the document is explicitly a change plan.

## Verification

Before finishing:

1. Use review-high-level-design on the completed artifact.
2. Use documentation-page-verifier with the artifact, source evidence, and completed review checklist when the review skill calls for it.
3. Run project wiki status and lint when docs/wiki exists and the artifact lives in or links from docs/wiki.
4. Search the artifact for unresolved TODO markers that are not intentional.
5. Confirm every component, interaction, data contract, implementation step, and verification claim has source evidence or an open question.

Do not send private, proprietary, sensitive, PII, or company-internal material to an external service unless the user explicitly authorizes it.
