# Architecture Review Checklist

## Purpose

Use this Review Checklist to verify an architecture artifact created from the methodology templates.

## Shared Contract

- The artifact starts with Current Understanding, Authoritative Sources, Related Code, Related Tests, Related Backlog Items, Related Wiki Pages, Open Questions, and Maintenance Notes.
- Current Understanding states the system or cross-cutting concern as it exists now.
- Authoritative Sources include source roots, tests, configuration, procedures, and related design documents.
- Related Code and Related Tests identify evidence or say Not yet identified after a real search.
- Open Questions capture unresolved system boundaries, ownership, behavior, or verification conflicts.

## Artifact-Specific Checks

- System Purpose And Scope defines what the system is and what it excludes.
- Runtime Assumptions identify technology stack, runtime environment, deployment assumptions, and key configuration.
- File Organization names important source paths, test paths, generated artifacts, and ownership boundaries.
- Major Layers And Dependency Direction explain which layers may call which other layers.
- Major Components And Ownership identify durable components and their responsibilities.
- Data Flow And Lifecycle explain data movement, persistence, state transitions, startup, shutdown, and external handoffs when applicable.
- Cross-Cutting Concerns cover errors, testing, configuration, security, privacy, observability, object creation, persistence, and UI composition when relevant.
- Design Principles And Invariants state rules that should hold across modules or subsystems.
- Risks And Trade-Offs describe real risks without becoming a change log.
- Verification links tests, validation commands, or explicit gaps for architecture-level claims.
- Diagrams clarify actual boundaries, context, ownership, layers, component associations, data movement, lifecycle, concern ownership, or coverage.

## Findings

Report findings first. Treat missing boundaries, unsourced stack claims, unclear dependency direction, missing ownership, unsupported cross-cutting rules, and missing verification as review findings.
