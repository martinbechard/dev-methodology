---
name: create-architecture
description: Use when creating or substantially rewriting an architecture artifact from the route-documentation-work architecture-template asset, including system scope, context, technology stack, file organization, layers, components, data flow, lifecycle, cross-cutting concerns, risks, invariants, and verification.
metadata:
  category: artifact-creation
---

# Create Architecture

Use this skill to create or substantially rewrite one architecture artifact. The artifact explains a whole system, project-wide boundary, or cross-cutting concern without duplicating every module detail.

For planned development, treat architecture as solution design rather than only a summary of upstream decisions. Make reasonable, explicitly labeled justified architecture propositions for undefined but resolvable technology, boundary, ownership, topology, or file-organization choices. State each proposition's basis, why it is necessary to complete the system frame or unblock HLD work, and the role that owns or may revise it. Do not present propositions as accepted requirements.

## Template

Use skills/route-documentation-work/assets/templates/architecture-template.md as the starting asset.

Copy the template only when a local editable artifact is needed. Replace every TODO instruction with source-backed content from the target repository.

## Scope

A central goal of architecture is to avoid chaos in high-level designs. Establish one shared system frame for runtime units, subsystem and component vocabulary, technology choices, repository roots, documentation homes, layers, ownership, dependency direction, data authority, integrations and trust boundaries, configuration ownership, lifecycle, and implementation sequence.

Build a system-frame ledger that maps each runtime unit, subsystem, layer, data owner, integration boundary, configuration owner, and documentation family to a stable name, responsibility, allowed dependencies, and complete repository-relative paths and roots where applicable. Architecture-owned paths and names must be literal and directly usable: reject `...`, a Unicode ellipsis, wildcards, omitted intermediate directories, abbreviated names, `TBD`, and similar placeholders. When sources do not define a needed choice, select a coherent proposition rather than forcing separate HLD authors to invent conflicting answers.

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

Use reverse-engineer-project-documentation when the user asks to derive an architecture set from an existing codebase.

## Reverse-Engineering Acceptance

During the architecture current reverse-engineering pass, derive the artifact from accepted high-level designs and confirmed cross-cutting source evidence. Functional specifications and wiki pages are intentionally created later and are not mandatory current-pass inputs. Record their absence as Not yet identified where applicable; do not block documentation acceptance solely because those later artifacts do not exist yet.

Documentation acceptance asks whether the architecture accurately reconciles the accepted HLD set and current-pass evidence. Implementation readiness separately asks whether architecture-dependent design or implementation can proceed safely. Known product defects, unimplemented behavior, open design decisions, and current limitations may remain visible in ACCEPTED documentation while making downstream implementation BLOCKED.

## Workflow

1. Inspect the target repository before writing. Read README files, task-relevant procedures, package metadata, build configuration, runtime entry points, source roots, tests, scripts, docs, wiki pages, backlog files, and current worktree status.
2. Identify the system boundary, runtime assumptions, ownership boundaries, dependency directions, persistence boundaries, external systems, and verification evidence.
3. Copy the architecture template into the target documentation location when a new artifact is needed.
4. Replace each TODO with source-backed architecture content.
5. Keep the shared page contract sections first.
6. Add Mermaid diagrams from objective relationship triggers. Whenever a section describes two or more ordered actions or phases, or any handoff, data movement, lifecycle transition, branch, retry, recovery path, startup or shutdown dependency, or dependent implementation phase, include an appropriate sequence, state, or flow diagram; prose, numbered lists, and tables may add constraints but must not carry the complete sequence alone. Add a structural diagram when a section defines a non-tabular topology: one system-context, scope, ownership, layer, component, dependency, principle, risk, or verification node connects to two or more others; a dependency or ownership path spans three or more nodes; a cycle exists; containment spans two or more levels; or an edge crosses a system, trust, or runtime boundary. Treat every architecture-template section-specific diagram trigger as an additive minimum under the shared route-documentation-work rule; satisfying one section-specific trigger does not waive another shared trigger.
7. Say Not yet identified for related code, tests, backlog items, or wiki pages that do not exist yet.
8. Keep risks, trade-offs, and open questions concrete enough to guide future implementation and review.
9. Keep the artifact steady-state. Do not describe it as new, revised, or enhanced unless the document is explicitly a change plan.

## Verification

Before finishing:

1. Use review-architecture on the completed artifact.
2. Use verify-documentation-page with the artifact, source evidence, and completed review checklist when the review skill calls for it.
3. Run project wiki status and lint when docs/wiki exists and the artifact lives in or links from docs/wiki.
4. Search the artifact for unresolved TODO markers that are not intentional.
5. Confirm every architectural claim names source evidence, a verification path, or an open question.
6. For Documentation Acceptance, skip any leading retained explanatory note or notes, then confirm the first authored decision begins with ACCEPTED or BLOCKED and judges only source evidence, accepted HLD prerequisites, and current reverse-engineering pass requirements.
7. For Implementation Readiness, skip any leading retained explanatory note or notes, then confirm the first authored decision begins with READY or BLOCKED as a separate downstream decision and does not turn an accurately documented defect or open decision into an automatic documentation failure.
8. Confirm every justified architecture proposition states basis, necessity, and decision owner and that no resolvable system-frame gap remains open.
9. Confirm complete repository-relative source, test, configuration, resource, migration, generated, script, runtime-data, and documentation roots are explicit and contain no placeholder segments.
10. Confirm every qualifying ordered relationship has an appropriate Mermaid diagram, every qualifying structural relationship has a diagram, and no data, lifecycle, or implementation sequence remains only in prose, a numbered list, or a table.

Do not send private, proprietary, sensitive, PII, or company-internal material to an external service unless the user explicitly authorizes it.
