---
name: create-module-design
description: Use when creating or substantially rewriting a module design artifact from the development-methodology module-design-template asset, including runtime path, parent context, responsibilities, callers, dependencies, public contracts, internal state, processing rules, invariants, configuration, external interfaces, UI behavior, error handling, and verification.
metadata:
  category: artifact-creation
---

# Create Module Design

Use this skill to create or substantially rewrite one module design artifact. The artifact defines one implementation unit precisely enough that code and tests can be understood or written without guessing.

## Template

Use skills/development-methodology/assets/templates/module-design-template.md as the starting asset.

Copy the template only when a local editable artifact is needed. Replace every TODO instruction with source-backed content from the target repository.

## Scope

Create one module design that defines:

- Runtime path.
- Parent context.
- Responsibilities.
- Callers.
- Dependencies.
- Public contracts.
- Internal data and state.
- Processing rules.
- Processing diagram when useful.
- Invariants.
- Configuration.
- External interfaces.
- UI and notification behavior.
- Error handling.
- Verification.

Use create-high-level-design when the work spans several modules, components, tasks, services, or UI surfaces. Use create-architecture when the work defines project-wide boundaries, layers, technology choices, or cross-cutting rules.

Use documentation-reverse-engineer when the user asks to derive many module designs from an existing codebase.

## Workflow

1. Inspect the target repository before writing. Read the implementation file or planned runtime path, callers, imports, exported contracts, tests, parent designs, procedures, backlog files, wiki pages, and current worktree status.
2. Identify the module's single primary responsibility, source path, callers, dependencies, public contracts, internal state, processing rules, side effects, error behavior, and verification evidence.
3. Copy the module design template into the target documentation location when a new artifact is needed.
4. Replace each TODO with source-backed module content.
5. Keep the shared page contract sections first.
6. Verify dependency paths against existing source files or a planned type registry. Do not invent paths.
7. Remove configuration, external interface, or UI behavior sections only when they genuinely do not apply.
8. Say Not yet identified for related code, tests, backlog items, or wiki pages that do not exist yet.
9. Keep the artifact steady-state. Do not describe it as new, revised, or enhanced unless the document is explicitly a change plan.
10. Treat owned files as the responsibility boundary, not the evidence boundary. Add direct links to non-owned callers, dependencies, schemas, configuration, security rules, error adapters, tests, procedures, and parent documents whenever the page relies on them.
11. Audit each behavioral sentence for evidence closure. Link the source that proves it, label it as an inference, or record it as unverified/open; do not let an adjacent section's generic file list stand in for direct evidence.
12. Verify that claimed tests are executable and exercise the named branch. Check test discovery annotations or registration, disabled state, injected doubles, fixtures, assertions, and actual calls. Describe unannotated helpers, unused fixtures, manual commands, and desired tests as gaps rather than coverage.
13. Follow failure paths through nested causes, wrapper fallbacks, validation differences, retries, logging, rollback, and user-visible outcomes. State actual behavior even when it exposes a defect; do not silently document the safer behavior the code should have.

## Verification

Before finishing:

1. Use review-module-design on the completed artifact.
2. Use documentation-page-verify with the artifact, source evidence, and completed review checklist when the review skill calls for it.
3. Run project wiki status and lint when docs/wiki exists and the artifact lives in or links from docs/wiki.
4. Search the artifact for unresolved TODO markers that are not intentional.
5. Confirm every responsibility, dependency, public contract, processing rule, invariant, and verification claim has source evidence or an open question.
6. Confirm Runtime Path contains an explicit project-relative implementation path and folder entry point when applicable.
7. Confirm Authoritative Sources includes the direct evidence used by Callers, Dependencies, Configuration, Error Handling, and Verification, including evidence owned by other modules.
8. Confirm every claimed test is discovered and executes the asserted branch; do not count helper methods, dormant fixtures, or prospective commands as coverage.
9. Confirm error, wrapper, build-lifecycle, and validation prose matches the implemented failure branches rather than intended behavior.

Do not send private, proprietary, sensitive, PII, or company-internal material to an external service unless the user explicitly authorizes it.
