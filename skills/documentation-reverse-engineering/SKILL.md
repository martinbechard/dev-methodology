---
type: Skill
name: documentation-reverse-engineering
description: Use when deriving functional, architecture, high-level design, module design, README, or wiki documentation from an existing codebase.
---

# Documentation Reverse Engineering

Use this skill to derive a source-backed documentation set from an existing codebase. Work from the smallest implementation units outward: modules, subsystems, architecture, functional behavior, then README and wiki integration.

## Source Authority

Use this authority order when sources disagree:

1. Code and tests describe actual behavior.
2. Functional specifications and requirements describe intended behavior.
3. Project procedures and agent instructions describe workflow obligations.
4. Backlog files describe tracked work and known status.
5. Architecture, high-level design, module design, and plan documents describe design intent.
6. Wiki pages summarize and navigate the sources above.

Do not invent behavior to fill gaps. Record an open question when the repository does not provide enough evidence.

## Pass 0: Repository Orientation

1. Identify source roots, test roots, application entry points, scripts, configuration files, migrations, public routes, command entry points, and generated artifacts.
2. Identify existing documentation roots and note whether they contain functional, architecture, high-level design, module design, or wiki pages.
3. Identify build, test, lint, and documentation commands from project metadata and procedures.
4. Identify current worktree status when the project is a Git repository.
5. Record documentation gaps and conflicts for later passes.

Completion gate:

- Documentation root is known.
- Source and test roots are known.
- Existing documentation is inventoried.
- Verification commands are known or recorded as not yet identified.

## Pass 1: Module Designs

1. Walk source roots and identify modules by runtime responsibility.
2. For each meaningful module, read implementation, callers, imports, exported contracts, tests, configuration use, persistence use, and user-visible behavior.
3. Create or update one module design document per meaningful module or tightly coupled module folder.
4. Use the module design template from development-methodology assets.
5. Add a Processing Diagram only when conditional flow, retries, error handling, or state transitions are difficult to understand from prose alone.
6. Link related tests and source files from each module document.
7. Record missing tests, ambiguous ownership, and undocumented side effects as open questions.

Prefer one module document for one coherent responsibility. Split only when separate responsibilities can change independently.

## Pass 2: High-Level Designs

1. Review module design documents and identify clusters that collaborate to deliver one subsystem, feature family, workflow engine, integration, UI area, or operational capability.
2. Create or update one high-level design document per subsystem.
3. Use the high-level design template from development-methodology assets.
4. Add diagrams for structural relationships inside the sections they clarify.
5. Link every constituent component document from the subsystem document.
6. Link functional specifications when a subsystem directly serves user-visible workflows.
7. Record overlapping ownership and missing subsystem boundaries as open questions.

Subsystems should be based on runtime collaboration and ownership, not only folder layout.

## Pass 3: Architecture

1. Review the full set of high-level design documents.
2. Read module documents where subsystem boundaries, dependency direction, state ownership, technology choices, or cross-cutting rules need evidence.
3. Create or update the architecture document using the architecture template.
4. Document system purpose, scope, context, technology stack, file organization, architectural layers, key components, data movement, lifecycle, cross-cutting concerns, design principles, invariants, risks, trade-offs, and verification.
5. Link all high-level design documents from the architecture document.
6. Record architecture-level contradictions as open questions.

Architecture must describe the system that exists. It may call out drift and risk, but it must not silently rewrite behavior.

## Pass 4: Functional Specifications

1. Review architecture, high-level designs, module designs, routes, UI components, command entry points, integration points, tests, and existing product documents.
2. Identify user-visible workflows, admin workflows, operator workflows, external-system workflows, route behavior, permissions, statuses, error states, and acceptance behavior.
3. Create or update functional specifications using the functional specification template.
4. Write workflows from the actor's point of view.
5. Add a Workflow Diagram when actor paths, branching states, permissions, or external handoffs are clearer visually.
6. Link technical documents and modules that implement each workflow.
7. Link tests that verify each workflow, state, edge case, and permission rule.
8. Record mismatches between intended behavior and actual code behavior as open questions or known defects.

Functional specifications describe observable behavior. Technical implementation details belong in related technical documents unless users need that detail to understand behavior.

## Pass 5: README And Wiki Integration

Create or update the project README after the documentation set exists. Keep it compact and route readers to deeper pages.

When the project uses docs/wiki:

1. Treat generated functional and technical documents as wiki page subclasses when they live under docs/wiki.
2. Create or update hub and index pages that summarize the documentation set.
3. Ensure durable wiki pages and subclasses include Related Code and Related Tests.
4. Link functional specs, architecture, high-level designs, module designs, source files, tests, procedures, known defects, and open decisions.
5. Record unresolved contradictions in wiki Open Questions.
6. Run wiki lint when available.

## Verification

After the passes:

1. Use documentation-page-verifier on created or changed specialized documents.
2. Run the project's build command when documentation work changed code, generated artifacts, or project metadata that can affect the build.
3. Run documentation or wiki lint when available.
4. Search new documentation for unresolved TODO markers that are not intentional.
5. Search new steady-state documentation for stale comparative language such as enhanced, revised, old, and new.
6. Confirm every created document has related source, related test, or Not yet identified entries.
7. Confirm every diagram represents a real sequence, association, aggregation, containment, ownership, dependency, lifecycle, coverage, or data movement relationship.
8. Confirm every open question is specific enough for a human or future agent to answer.

Stop and ask for human input when source conflicts cannot be resolved, business ownership would be guessed, private systems are needed, verification cannot run for environmental reasons, or the work would send private material to an external service without explicit authorization.
