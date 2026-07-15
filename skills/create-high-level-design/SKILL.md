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

Copy the template only when a local editable artifact is needed. Replace every TODO instruction with content supported by the authoritative inputs for the selected design mode.

## Design Mode

Choose and state exactly one mode before writing:

- PLANNED_DEVELOPMENT defines an intended subsystem from accepted functional specifications, architecture, decisions, and backlog requirements. Module designs, code, and tests may be Not yet identified.
- EXISTING_IMPLEMENTATION documents current subsystem behavior from accepted lower-level designs, executable source, configuration, tests, and retained runtime evidence.
- MIXED_CHANGE separates current behavior from the intended change and names the authority for each statement.

Use only the authoritative inputs permitted by the selected design mode. Names, framework conventions, generated defaults, and likely implementation patterns are not requirements evidence.

## Scope

Create one high-level design that defines:

- Parent architecture.
- Scope.
- Current data anchors.
- Constituent components.
- Interaction model.
- Lifecycle.
- Data shapes and contracts.
- Requirements coverage.
- Cross-module contract reconciliation.
- Configuration.
- Implementation order.
- Invariants.
- Non-goals.
- Definition of good.
- Verification.

Use create-architecture when the work defines a whole system, project-wide boundary, technology choice, layer model, or cross-cutting concern. Use create-module-design when the work is one module, service, component, task, utility, or tightly scoped implementation unit.

Use documentation-reverse-engineer when the user asks to derive subsystem designs from an existing codebase.

## Workflow

1. Select PLANNED_DEVELOPMENT, EXISTING_IMPLEMENTATION, or MIXED_CHANGE. Record the authoritative input set and source-precedence rule before deriving behavior.
2. Inspect only the evidence permitted by that mode. Build a source-category inventory covering accepted functional specifications, parent architecture, decisions, backlog requirements, project configuration, and relevant technology guidance; for existing behavior also cover accepted module designs, source, tests, procedures, configuration, and runtime evidence. Record each available durable source, or state that the category is not yet identified in the permitted input set, instead of silently omitting the category.
3. Build an operation-and-obligation inventory before prose. Give every user or runtime operation, scheduled or privileged background task, event, external effect, cache or derived-state effect, and authoritative source open question its own row. Record its source, claim mode, actor or trigger and schedule, selector or predicate, state transition, exact response status or error when accepted, applicable configuration, default, lifetime, or timing, side effects, verification, and accountable decision role. When governance evidence does not name an owner, name the required project role and escalation path without inventing a person. A contract asked as a source open question remains OPEN_QUESTION and OPEN; never promote it to defined intended behavior.
4. Build a requirements coverage ledger before prose and reconcile it one-to-one with the operation-and-obligation inventory. Account for every applicable requirement as DEFINED, OPEN, or OUT_OF_SCOPE, preserve whether it is CURRENT_BEHAVIOR, CURRENT_LIMITATION, INTENDED_BEHAVIOR, PROPOSED_CHANGE, or OPEN_QUESTION, and map it to components, contracts, interactions, state transitions, error behavior, and verification.
5. Identify subsystem boundaries, components, data anchors, contracts, lifecycle, configuration ownership, implementation order, invariants, and verification obligations. Build a boundary-edge inventory from every caller-callee or producer-consumer edge named by the parent architecture, constituent components, interactions, lifecycle, data shapes, configuration, error translation, token issuance, scheduled work, or caches. Map every edge to Cross-Module Contract Reconciliation and every privileged or sensitive edge to Critical Trust And Identity Boundaries before writing prose.
6. Reconcile every cross-module contract. For each producer-consumer boundary, define actor and authentication source; authorization, ownership, tenancy, and data filtering; selector and mismatch behavior; payload and response disclosure; state owner and transition; validation owner; transaction or asynchronous boundary; error timing; and sensitive-data handling.
7. Do not resolve missing critical facts by generalization. Record a conflicting or absent high-impact identity, security, persistence, public-response, state-ownership, or failure-timing contract as a blocking open question.
8. Reconcile specific operation and cross-module contracts before applying general principles. An explicit route, response, selector, validation, state, or failure exception governs that boundary unless an authoritative source identifies a real conflict. Preserve current limitations beside proposed targets instead of silently normalizing them.
9. Copy the high-level design template into the target documentation location when a new artifact is needed.
10. Replace each TODO with authoritative content, an explicit inference, or an open question.
11. Keep the shared page contract sections first.
12. Link constituent module design documents when they exist and identify missing module designs when they are needed.
13. Use diagrams only where component collaboration, lifecycle, contracts, configuration, implementation order, or verification coverage are easier to inspect visually.
14. Say Not yet identified for related code, tests, backlog items, or wiki pages that do not exist yet.
15. Keep the artifact steady-state. Do not describe it as new, revised, or enhanced unless the document is explicitly a change plan.
16. Treat the target as the installed documentation path when resolving links. Link only durable project artifacts that will exist from that location. Temporary inputs may guide the draft, but do not link or cite transient assembly or control files such as prompts, manifests, assignments, copied project context, evaluation case roots, or scratch files. When no durable project source exists, state that it is not yet identified instead of inventing a link.

## Verification

Before finishing:

1. Use review-high-level-design on the completed artifact.
2. Use documentation-page-verify with the artifact, source evidence, and completed review checklist when the review skill calls for it.
3. Run project wiki status and lint when docs/wiki exists and the artifact lives in or links from docs/wiki.
4. Search the artifact for unresolved TODO markers that are not intentional.
5. Confirm every component, interaction, data contract, implementation step, and verification claim has source evidence or an open question.
6. Confirm every applicable functional requirement appears in Requirements Coverage with one explicit status and no high-impact omission hidden in general subsystem prose.
7. Confirm Cross-Module Contract Reconciliation detects conflicting actor, selector, authorization, validation, response, state, transaction, asynchronous, and error-timing claims instead of choosing one silently.
8. Confirm every critical trust boundary identifies protected assets, entry points, identities, authority checks, disclosure limits, and sensitive-data handling.
9. Confirm blocking open questions prevent dependent module implementation until the affected contract is decided.
10. Confirm every accepted current limitation remains visible beside any proposed target and every operation-specific exception survives broader security or response-shape generalization.
11. Resolve every local Markdown link from the installed documentation path and remove links to transient assembly or control files before review.
12. Confirm the source-category inventory accounts for every mode-permitted category and the Requirements Coverage table accounts for every operation-and-obligation inventory row, including source open questions, schedules, predicates, cache effects, and boundary verification.
13. Confirm every boundary-edge inventory row appears in Cross-Module Contract Reconciliation and every privileged or sensitive row also appears in Critical Trust And Identity Boundaries.
14. Preserve accepted exact validation commands and map them to the components, operations, boundaries, or risks they verify. Do not replace an available executable command with a generic future-test description.

Do not send private, proprietary, sensitive, PII, or company-internal material to an external service unless the user explicitly authorizes it.
