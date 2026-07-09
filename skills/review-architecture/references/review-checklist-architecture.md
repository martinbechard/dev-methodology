# Architecture Review Checklist

## Purpose

Use this Review Checklist to verify an architecture artifact created from the methodology templates.

## Completion Format

For every question record:

- Status: pass, fail, question, or n/a.
- Question: copy the objective question being answered.
- Quoted evidence: quote the exact artifact or source text that supports the status.
- Assessment: explain why the quoted evidence passes, fails, is unclear, or is not applicable.

Do not mark pass without quoted evidence.

## Skill Workflow Checks

- Question: Does the review identify the system boundary, runtime assumptions, layers, components, and cross-cutting claims before assessment?
- Question: Does the completed review checklist name this checklist as review-checklist-architecture.md?
- Question: Does the completed review checklist save next to the artifact using artifact-name.review-checklist-architecture.md?
- Question: Does the review use documentation-page-verifier with the artifact, source evidence, and completed review checklist?
- Question: Does the final assessment derive findings or pass status from the completed review checklist rather than memory?
- Question: Does the output lead with findings ordered by severity when problems exist?

## Shared Contract Questions

- Question: Does the artifact start with Current Understanding, Authoritative Sources, Related Code, Related Tests, Related Backlog Items, Related Wiki Pages, Open Questions, and Maintenance Notes?
- Question: Does Current Understanding state the system or cross-cutting concern as it exists now?
- Question: Do Authoritative Sources include source roots, tests, configuration, procedures, and related design documents?
- Question: Do Related Code and Related Tests identify evidence or say Not yet identified after a real search?
- Question: Do Open Questions capture unresolved system boundaries, ownership, behavior, or verification conflicts?

## Artifact-Specific Questions

- Question: Does System Purpose And Scope define what the system is and what it excludes?
- Question: Do Runtime Assumptions identify technology stack, runtime environment, deployment assumptions, and key configuration?
- Question: Does File Organization name important source paths, test paths, generated artifacts, and ownership boundaries?
- Question: Do Major Layers And Dependency Direction explain which layers may call which other layers?
- Question: Do Major Components And Ownership identify durable components and their responsibilities?
- Question: Does Data Flow And Lifecycle explain data movement, persistence, state transitions, startup, shutdown, and external handoffs when applicable?
- Question: Do Cross-Cutting Concerns cover errors, testing, configuration, security, privacy, observability, object creation, persistence, and UI composition when relevant?
- Question: Do Design Principles And Invariants state rules that should hold across modules or subsystems?
- Question: Do Risks And Trade-Offs describe real risks without becoming a change log?
- Question: Does Verification link tests, validation commands, or explicit gaps for architecture-level claims?
- Question: Do diagrams clarify actual boundaries, context, ownership, layers, component associations, data movement, lifecycle, concern ownership, or coverage?

## Findings

Report findings first. Treat missing boundaries, unsourced stack claims, unclear dependency direction, missing ownership, unsupported cross-cutting rules, and missing verification as review findings.
