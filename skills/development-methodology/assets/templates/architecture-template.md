<!--
Copyright (c) 2025 Martin Bechard [martin.bechard@DevConsult.ca]
This software is licensed under the MIT License.
File path: skills/development-methodology/assets/templates/architecture-template.md
1-line summary: Template for project-level architecture documentation.
-->

# TODO Architecture Name

## Current Understanding

> This section gives readers a reliable starting point so they do not interpret detailed decisions against the wrong system boundary or behavioral baseline. Architects, implementers, and reviewers use it during onboarding, handoffs, and design reviews to quickly understand what the architecture governs, why it matters, and whether it describes current or intended behavior.

TODO: Describe the system or cross-cutting concern this architecture document covers.

TODO: State why this architecture matters to the project and what decisions it makes authoritative.

TODO: State whether this architecture describes existing behavior, intended behavior, or a known mix of both.

## Authoritative Sources

> This section lets authors and reviewers distinguish evidence-backed architecture from assumption and resolve contradictions consistently. Architects, implementers, and reviewers use it when creating, reviewing, or maintaining the document to trace decisions to code, tests, specifications, and procedures and to determine which source wins when they disagree.

TODO: Link code, tests, procedures, README files, functional specifications, high-level designs, module designs, backlog records, and plan documents used to derive this architecture.

TODO: State which source wins when sources disagree.

## Related Code

> This section gives implementers a direct path from architectural decisions to the affected implementation and lets reviewers verify that the code still follows the design. Architects, implementers, and reviewers use it during implementation, change review, impact analysis, and reverse engineering to locate the exact code, configuration, migration, script, generated, and runtime paths governed by the architecture.

TODO: Link the source roots, entry points, configuration files, scripts, migrations, generated artifacts, or runtime files governed by this architecture.

TODO: Say Not yet identified when no code exists yet.

## Related Tests

> This section shows readers which architectural claims are actively proven and where confidence still depends on missing or manual checks. Architects, implementers, and reviewers use it during design review, regression analysis, and release assessment to find the automated and manual evidence that exercises the documented boundaries and behavior.

TODO: Link build checks, unit tests, integration tests, smoke tests, manual checks, fixtures, or generated verification artifacts that prove the architecture is followed.

TODO: Say Not yet identified when tests still need to be written.

## Related Backlog Items

> This section prevents architectural decisions, known defects, and planned changes from becoming detached from the work that motivated them. Architects, implementers, and reviewers use it during planning, triage, and maintenance to understand why the architecture has its current shape and which backlog work may invalidate or extend it.

TODO: Link active or historical backlog items that affect architectural direction, known defects, or planned cross-cutting work.

TODO: Say Not yet identified when no related backlog item is known.

## Related Wiki Pages

> This section helps readers move from the system-wide view to the deeper context needed for a specific question without duplicating that material here. Architects, implementers, and reviewers use it during design exploration, onboarding, and change-impact analysis to find related designs, functional behavior, terminology, decisions, defects, and adjacent architecture pages.

TODO: Link high-level design pages, module design pages, functional pages, glossary entries, open decisions, known defects, and adjacent architecture pages.

TODO: Say Not yet identified when no related wiki page is known.

## Open Questions

> This section makes unresolved architectural uncertainty visible so downstream teams do not unknowingly build on an assumption. Architects, implementers, and reviewers use it before design handoffs, implementation planning, and decision reviews to identify questions that reasonable architecture propositions cannot resolve and to state each question's blocking effect, decision owner, and required evidence.

TODO: Record unresolved source conflicts, ownership questions, dependency boundary questions, verification gaps, or architecture decisions.

TODO: If there are no unresolved questions, replace this section with a sentence saying no open questions are recorded.

## Maintenance Notes

> This section helps future maintainers recognize when the architecture may have become stale and what must be checked before trusting it again. Architects, implementers, and reviewers use it after changes to source roots, technologies, dependencies, tests, procedures, or runtime boundaries to guide revalidation and record the most recent meaningful source review.

TODO: Record what future maintainers should recheck when source roots, technology choices, dependencies, tests, procedures, or runtime boundaries change.

TODO: Include the last meaningful source review when known.

## Scope

> This section prevents responsibilities from being duplicated, omitted, or silently assigned to the wrong design artifact. Architects, implementers, and reviewers use it when selecting documentation ownership, planning changes, and reviewing boundaries to determine what this architecture governs, what it excludes, and where excluded concerns belong.

TODO: List what is included in this architecture.

TODO: List what is outside this architecture and should be handled by another document.

TODO: Add a Scope Boundary Diagram when included items, excluded items, local systems, external systems, or ownership boundaries need to be compared as a set.

TODO: The Scope Boundary Diagram should show the architecture boundary, included areas, excluded areas, and important external neighbors. It should not show low-level internals unless they define the boundary.

## System Context

> This section reveals how the system participates in its wider environment so integration, deployment, and trust-boundary consequences are visible before internal design is evaluated. Architects, implementers, and reviewers use it during architecture review, integration planning, and security analysis to identify actors, runtime surfaces, neighboring systems, environments, and external boundaries.

TODO: Describe the users, runtime surfaces, external systems, browser or server boundaries, and local development boundaries involved.

TODO: Link related architecture, high-level design, and module design documents.

TODO: Add a System Context Diagram when users, runtime surfaces, local systems, external providers, or environment boundaries form a meaningful association set.

TODO: The System Context Diagram should show actors and neighboring systems from outside-in. It should make local, browser, server, device, cloud, or third-party boundaries visible.

## Technology Stack

> This section prevents teams from making locally convenient technology choices that conflict with system-wide compatibility, support, or migration constraints. Architects, implementers, and reviewers use it during implementation planning, dependency upgrades, environment setup, and review to identify approved technologies, their architectural purpose, version authority, ownership, validation, and prohibited alternatives.

TODO: List the required runtime, language, package manager, build tools, test tools, browser platform, persistence tools, and important libraries.

TODO: Explain why each major stack choice is required for this system.

TODO: For each material technology choice, state the boundary need, approved version source, configuration owner, validation command, and fallback or migration constraint. Keep project-specific approved stacks in project guidance.

TODO: Identify stack choices that are forbidden or should not be introduced without a new architecture decision.

TODO: Add a Stack Association Diagram when stack items form more than one runtime, build, deployment, or forbidden-boundary group and an item relationship crosses a group boundary, or when a dependency path spans three or more stack items.

TODO: The Stack Association Diagram should group technologies by architectural role, not repeat every package name.

## File Organization

> This section makes placement and ownership predictable so contributors can find artifacts quickly and avoid creating competing folders or unclear boundaries. Architects, implementers, and reviewers use it during onboarding, implementation, refactoring, and code review to map source, tests, documentation, configuration, generated output, and runtime data to complete repository-relative paths.

TODO: Show the repository placement of source code, tests, design documents, runtime data, scripts, configuration, and generated artifacts as one fenced text tree. Do not repeat shared prefixes in a long list or table.

TODO: Describe the ownership rule for each folder.

TODO: Path tree example (replace every synthetic segment and file with complete repository-relative paths, and preserve all implementation-significant package segments):

```text
project-root/
├── backend/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/example/application/
│   │   │   └── resources/db/changelog/
│   │   └── test/java/com/example/application/
│   └── var/
├── frontend/
│   ├── src/
│   └── test/
├── docs/
│   ├── architecture/
│   ├── high-level-designs/
│   └── module-designs/
└── scripts/
```

TODO: If ownership, generated status, runtime mutability, or another property needs a table, key its rows by short labels from the tree and do not repeat every full path.

TODO: If the full repository tree would become a large blob, split it into named subsections by runtime unit or ownership area. Put one small fenced text tree in each subsection and its metadata immediately after the tree. Do not put multiline trees in Markdown table cells or simulate them with HTML breaks. Do not create one row per full path.

TODO: State where new architecture, high-level design, and module design documents belong.

TODO: Treat the fenced File Organization path tree as the ownership-containment diagram when logical ownership follows folder containment. Add a Mermaid Ownership Diagram only when logical ownership crosses or differs from the folder tree; do not duplicate the same containment in both forms.

TODO: A separate Ownership Diagram should show only the cross-folder ownership relationships that the path tree cannot express. It should not replace the source links in Related Code.

## Architectural Layers

> This section protects separation of responsibilities by making dependency direction reviewable before coupling spreads across the system. Architects, implementers, and reviewers use it during component design, implementation review, and refactoring to understand each layer's role and to detect allowed or forbidden dependencies.

TODO: Name each layer in dependency order from outer shell to core logic or from user-facing surface to persistence.

TODO: For each layer, describe its responsibility and what it may depend on.

TODO: State which dependency directions are not allowed.

TODO: Add a Layered Dependency Diagram whenever the architecture defines more than one layer.

TODO: The Layered Dependency Diagram should show allowed dependency direction, forbidden crossings, and adapter boundaries. It should make layer order reviewable without reading every bullet.

## Key Components

> This section gives teams a shared vocabulary and ownership map for the system's major building blocks, reducing ambiguity in designs and handoffs. Architects, implementers, and reviewers use it during high-level design decomposition, collaboration, and change-impact analysis to identify each component's role and locate its lower-level design.

TODO: List the major services, UI surfaces, workflow components, data stores, scripts, and external integrations.

TODO: For each component, describe its role in one or two sentences and link its lower-level design document when available.

TODO: Add a Component Association Diagram when major components collaborate, share runtime services, adapt common behavior, or enforce cross-cutting concerns together.

TODO: The Component Association Diagram should show the structural association between major components and link mentally to the high-level design pages. It should not duplicate implementation details owned by module designs.

## Diagram Authoring Rules

> This section helps authors and reviewers recognize when prose would hide important structure, ordering, state, or boundary relationships. Architects, implementers, and reviewers use it while authoring and reviewing the architecture to choose diagrams that make real relationships inspectable without adding decorative or duplicate visuals.

TODO: Keep only the diagram sections that match real structural relationships in this architecture.

TODO: Whenever any section describes two or more ordered actions or phases, or any handoff, data movement, lifecycle transition, branch, retry, recovery path, startup or shutdown dependency, or dependent implementation phase, add an appropriate Mermaid sequence, state, or flow diagram. Prose, numbered lists, and tables may add constraints but must not carry the complete sequence alone.

TODO: Add a structural diagram when a section defines a non-tabular topology: one system-context, scope, ownership, layer, component, dependency, principle, risk, or verification node connects to two or more others; a dependency or ownership path spans three or more nodes; a cycle exists; containment spans two or more levels; or an edge crosses a system, trust, or runtime boundary.

TODO: Treat the diagram triggers attached to individual architecture sections as additive minimums under the shared development-methodology rule. Satisfying one section-specific trigger does not waive another shared trigger.

TODO: Prefer Mermaid flowchart for association, aggregation, dependency, ownership, and data-flow diagrams. Prefer Mermaid sequence diagrams for ordered actor handoffs. Prefer Mermaid state diagrams for lifecycle state machines.

TODO: Place each diagram immediately after the section it clarifies unless one combined diagram serves several adjacent sections better.

TODO: If an SVG artifact is maintained, link it only when a review or publishing surface cannot render Mermaid and record its source relationship in Maintenance Notes.

## Data Flow

> This section exposes where information is owned, transformed, persisted, or exposed so integration, privacy, consistency, and debugging risks can be assessed. Architects, implementers, and reviewers use it during interface design, security review, incident analysis, and change-impact analysis to trace inputs, handoffs, transformations, persistence, serialization, and user-visible outputs.

TODO: Describe the main data flow through the system from input to output.

TODO: Include state ownership, persistence points, serialization boundaries, and UI update paths.

TODO: Add a Data Flow Diagram when requests, commands, events, persisted records, streams, logs, or UI updates move through multiple components.

TODO: The Data Flow Diagram should show the data shape or event at each handoff when the shape matters. It should identify where data becomes persisted, derived, serialized, or user-visible.

## Lifecycle Flow

> This section prevents initialization, shutdown, failure, and recovery assumptions from becoming hidden sources of runtime defects. Architects, implementers, and reviewers use it during workflow design, operational review, and incident analysis to understand required ordering across startup, steady operation, failure handling, shutdown, and recovery.

TODO: Describe startup, steady-state operation, error handling, shutdown, and recovery.

TODO: Identify the ordering constraints that must be preserved during initialization or workflow execution.

TODO: Add a Lifecycle Diagram when startup, ready state, steady operation, error, abort, recovery, or shutdown depends on ordered states.

TODO: The Lifecycle Diagram should show states and transitions. Use a state diagram when state names are the main concept, and use a flowchart when ordered steps are the main concept.

## Cross-Cutting Concerns

> This section prevents shared policies from being implemented inconsistently or left without a clear enforcement owner. Architects, implementers, and reviewers use it during subsystem design, security and performance review, and cross-component changes to determine how concerns such as errors, tracing, state, persistence, testing, privacy, and performance are enforced across the architecture.

TODO: Document the project-wide rules for error handling, tracing, notifications, settings, state, persistence, testing, security, privacy, and performance.

TODO: Link the specific architecture or module documents that own deeper detail for each concern.

TODO: Add a Concern Ownership Map when concerns are enforced by several components or layers.

TODO: The Concern Ownership Map should connect each concern to the component, layer, or rule that enforces it. It should make shared responsibilities and ownership boundaries visible.

## Design Principles

> This section gives teams stable decision rules for situations the architecture cannot enumerate in advance, helping independent choices remain coherent. Architects, implementers, and reviewers use it during design trade-offs, implementation, and review to evaluate whether a proposed choice follows the architecture's intent and practical constraints.

TODO: List the principles this architecture requires. Each principle should be concrete enough to guide implementation and review.

TODO: Explain the practical consequence of each principle.

TODO: Add a Principle Traceability Diagram when one principle governs two or more layers, components, risks, or verification checks; one governed item is constrained by two or more principles; or a principle-to-verification path spans three or more nodes.

TODO: The Principle Traceability Diagram should show which architectural items each principle governs.

## Invariants

> This section identifies the non-negotiable properties that implementations and future changes must preserve, even when internal designs evolve. Architects, implementers, and reviewers use it during implementation, testing, code review, and change assessment to detect violations of ownership, dependency, persistence, privacy, and user-visible behavior guarantees.

TODO: List rules that must always remain true across the architecture.

TODO: Include ownership boundaries, dependency boundaries, persistence guarantees, privacy constraints, and user-visible state rules.

## Risks And Trade-Offs

> This section makes the consequences of architectural choices explicit so decision-makers can judge whether accepted compromises remain reasonable. Architects, implementers, and reviewers use it during architecture approval, planning, mitigation work, and later design changes to connect risks and trade-offs to affected components, boundaries, dependencies, and future decision points.

TODO: List the major risks created by this architecture.

TODO: List the trade-offs accepted by this architecture and why they are acceptable.

TODO: Identify areas where future work may require a new architecture decision.

TODO: Add a Risk Association Diagram only when risks cluster around components, boundaries, external dependencies, or accepted trade-offs.

TODO: The Risk Association Diagram should connect each risk to the architectural item that creates or mitigates it.

## Documentation Acceptance

> This distinguishes an evidence-backed architecture for the current reverse-engineering pass from permission to begin architecture-dependent work. Architects, implementers, and reviewers use it during review and handoff to record whether source evidence, accepted high-level-design prerequisites, and current-pass requirements are reconciled without concealing defects, open decisions, or limitations.

TODO: After any leading retained explanatory note or notes, begin the first authored decision with **ACCEPTED.** or **BLOCKED.** State ACCEPTED when the artifact accurately reconciles source evidence, accepted high-level-design prerequisites, and current-pass requirements. During bottom-up reverse engineering, do not fail documentation acceptance solely because later functional specifications or wiki pages are intentionally absent, or because an accurately recorded defect, open decision, or limitation blocks implementation.

TODO: When BLOCKED, name the missing accepted prerequisite, insufficient evidence, unresolved current-pass review finding, or unavailable mandatory dependency.

## Implementation Readiness

> This section prevents a reviewed document from being mistaken for authorization to begin unsafe downstream work. Architects, implementers, and reviewers use it during planning and design handoff to record READY or BLOCKED for architecture-dependent work and to identify any critical unresolved boundary, decision, defect, or verification gap.

TODO: After any leading retained explanatory note or notes, begin the first authored decision with **READY.** or **BLOCKED.** State READY only when architecture-dependent downstream work can proceed without an unresolved critical boundary, decision, defect, or verification gap. Otherwise state BLOCKED for the affected downstream work. A BLOCKED result does not make an accurately documented limitation an automatic review failure.

## Verification

> This section turns architectural intent into observable evidence so teams can detect drift instead of relying on confidence or documentation alone. Architects, implementers, and reviewers use it during implementation, release review, regression analysis, and maintenance to map architectural rules and components to builds, tests, reviews, runtime evidence, and known coverage gaps.

TODO: Define how this architecture will be verified through builds, tests, linting, manual checks, runtime logging, or design review.

TODO: List the evidence that proves implementations still follow this architecture.

TODO: Add a Verification Coverage Map when several tests, checks, logs, or manual reviews prove different layers, components, or workflows.

TODO: The Verification Coverage Map should connect architecture items to evidence. It should expose missing coverage instead of implying that every item is covered.
