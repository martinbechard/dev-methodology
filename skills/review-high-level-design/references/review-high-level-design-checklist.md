# High-Level Design Review Checklist

## Purpose

Use this Review Checklist to verify a high-level design artifact created from the methodology templates.

## Shared Contract

- The artifact starts with Current Understanding, Authoritative Sources, Related Code, Related Tests, Related Backlog Items, Related Wiki Pages, Open Questions, and Maintenance Notes.
- Current Understanding describes the subsystem or feature family as it exists or is intended now.
- Authoritative Sources include parent architecture, source files, tests, functional specifications, procedures, and related module designs.
- Related Code and Related Tests identify evidence or say Not yet identified after a real search.
- Open Questions capture unresolved subsystem ownership, boundaries, contracts, or verification issues.

## Artifact-Specific Checks

- Subsystem Purpose And Parent Architecture explain why the subsystem exists and how it fits the parent architecture.
- Scope And Non-Goals distinguish included components, excluded components, and deferred work.
- Current Data Anchors name authoritative data sources, state owners, records, events, messages, or external systems.
- Constituent Components identify each component and responsibility without collapsing into implementation detail for every module.
- Interaction Model explains calls, events, jobs, user actions, external handoffs, and sequencing.
- Lifecycle And State describe meaningful states, transitions, retries, cleanup, and long-running behavior.
- Data Contracts And Shapes identify inputs, outputs, persistence shape, messages, events, and validation expectations.
- Configuration Ownership identifies where configuration lives and who owns it.
- Implementation Order gives a credible sequence when the design is used for planned work.
- Cross-Module Invariants state rules that must hold across components.
- Definition Of Good And Verification link success criteria, tests, validation commands, and explicit gaps.
- Diagrams clarify scope, data anchors, component associations, interactions, lifecycle, data contracts, configuration ownership, implementation order, or coverage.

## Findings

Report findings first. Treat missing parent architecture, vague component responsibilities, unclear data contracts, unsupported interaction claims, missing invariants, and missing verification as review findings.
