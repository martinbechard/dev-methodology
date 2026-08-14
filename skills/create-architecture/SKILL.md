---
name: create-architecture
description: Use when creating or substantially rewriting an architecture artifact from the route-documentation-work architecture-template asset, including system scope, context, technology stack, file organization, layers, components, data flow, lifecycle, cross-cutting concerns, risks, invariants, and verification.
metadata:
  category: artifact-creation
---
<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: 858c50d3-95a2-4a5f-a549-bfabc1b4843a
Created-UTC: 2026-07-09T15:36:02Z
Creating-Agent: historical-unknown
Runtime: historical-unknown
Dispatched-Model: historical-unknown
Reasoning-Effort: historical-unknown
Task-ID: historical-unknown
Artifact-ID-Evidence: migration-assigned
Created-UTC-Evidence: git-derived
Creating-Agent-Evidence: historical-unknown
Runtime-Evidence: historical-unknown
Dispatched-Model-Evidence: historical-unknown
Reasoning-Effort-Evidence: historical-unknown
Task-ID-Evidence: historical-unknown
-->

# Create Architecture

Use this skill to create or substantially rewrite one architecture artifact. The artifact explains a whole system, project-wide boundary, or cross-cutting concern without duplicating every module detail.

For planned development, treat architecture as solution design rather than only a summary of upstream decisions. Make reasonable, explicitly labeled justified architecture propositions for undefined but resolvable technology, boundary, ownership, topology, or file-organization choices. State each proposition's basis, why it is necessary to complete the system frame or unblock HLD work, and the role that owns or may revise it. Do not present propositions as accepted requirements.

When planned work creates or materially revises one of these technical choices, Dev Architect selects or reviews the choice before document acceptance. Dev Architect traces it to requirements, constraints, repository evidence, or an explicit assumption and compares materially larger proposals with the smallest viable approach. Dev Documentation Writer retains document structure, source use, template conformance, and prose quality. Dev Artifact Reviewer retains independent artifact review.

Material infrastructure is a new harness, runner, simulator, service, or equivalent durable execution facility. Architecture may authorize material infrastructure only from explicit user approval. Approval exists only when the original user request explicitly includes the exact infrastructure outcome or a later recorded User Action Required answer explicitly approves it. Technical justification, reviewer acceptance, architecture acceptance, broad scope language, implementation need, convenience, test coverage goals, and an agent recommendation do not provide approval.

Ordinary fixtures, helpers, and focused tests remain within normal implementation authority when they do not introduce material infrastructure. Return an unjustified outsized choice for correction.

When approval is absent, preserve the proposed architecture and do not authorize infrastructure implementation. Return exactly one contextual, plain-language User Action Required question through Dev Orchestrator. The question must identify the proposed infrastructure, explain why approval is required, give concrete options and practical tradeoffs, and ask for one decision. Until the user answers, do not authorize infrastructure implementation.

## Template

Use skills/route-documentation-work/assets/templates/architecture-template.md as the starting asset.

Copy the template only when a local editable artifact is needed. Replace every TODO instruction with source-backed content from the target repository.

## Pre-Write Placement Gate

Complete this gate before copying the template or creating the artifact:

1. Resolve the exact target path through organise-project-files and the repository's live placement taxonomy.
2. Confirm that the selected category, path, filename pattern, and identifier prefix are classified as architecture.
3. Confirm that the target is outside every HLD category and does not use an HLD prefix or identifier.
4. Record the child-HLD location and naming convention that this architecture governs.
5. Confirm the authority direction is architecture to child HLD to child component or module design, with each child referencing its parent and no circular authority reference.
6. If the taxonomy lacks a distinct architecture category, have Project Organiser extend it before writing. Do not assign the artifact an HLD identity as a fallback.

Stop when architecture and HLD would receive the same path category, identifier, prefix, or authority role. A fixed structured workflow output such as docs/architecture/architecture-design.yaml may share the architecture directory, but it retains the filename, owner, and lifecycle of that generating workflow and is not the durable Markdown architecture artifact.

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
2. Complete the Pre-Write Placement Gate and retain the architecture path, identifier, child-HLD convention, and authority direction as creation evidence.
3. Identify the system boundary, runtime assumptions, ownership boundaries, dependency directions, persistence boundaries, external systems, and verification evidence.
4. Copy the architecture template into the validated target documentation location when a new artifact is needed.
5. Replace each TODO with source-backed architecture content.
6. Keep the shared page contract sections first.
7. Add Mermaid diagrams from objective relationship triggers. Whenever a section describes two or more ordered actions or phases, or any handoff, data movement, lifecycle transition, branch, retry, recovery path, startup or shutdown dependency, or dependent implementation phase, include an appropriate sequence, state, or flow diagram; prose, numbered lists, and tables may add constraints but must not carry the complete sequence alone. Add a structural diagram when a section defines a non-tabular topology: one system-context, scope, ownership, layer, component, dependency, principle, risk, or verification node connects to two or more others; a dependency or ownership path spans three or more nodes; a cycle exists; containment spans two or more levels; or an edge crosses a system, trust, or runtime boundary. Treat every architecture-template section-specific diagram trigger as an additive minimum under the shared route-documentation-work rule; satisfying one section-specific trigger does not waive another shared trigger.
8. Say Not yet identified for related code, tests, backlog items, or wiki pages that do not exist yet.
9. Keep risks, trade-offs, and open questions concrete enough to guide future implementation and review.
10. Keep the artifact steady-state. Do not describe it as new, revised, or enhanced unless the document is explicitly a change plan.

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
11. Confirm the artifact states its canonical architecture path and identifier, the child-HLD location and naming convention, and the non-circular architecture-to-HLD-to-component-or-module authority direction.

Do not send private, proprietary, sensitive, PII, or company-internal material to an external service unless the user explicitly authorizes it.
