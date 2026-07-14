# High-Level Design Review Checklist

## Purpose

Use this Review Checklist to verify a high-level design artifact created from the methodology templates.

## Completion Format

For every question record:

- Status: pass, fail, question, or n/a.
- Question: copy the objective question being answered.
- Quoted evidence: quote the exact artifact or source text that supports the status.
- Assessment: explain why the quoted evidence passes, fails, is unclear, or is not applicable.

Do not mark pass without quoted evidence.

## Skill Workflow Checks

- Question: Does the review identify subsystem scope, constituent components, interactions, data anchors, invariants, and verification claims before assessment?
- Question: Does the completed review checklist name this checklist as review-checklist-high-level-design.md?
- Question: Does the completed review checklist save next to the artifact using artifact-name.review-checklist-high-level-design.md?
- Question: Does the review use documentation-page-verify with the artifact, source evidence, and completed review checklist?
- Question: Does the final assessment derive findings or pass status from the completed review checklist rather than memory?
- Question: Does the output lead with findings ordered by severity when problems exist?

## Shared Contract Questions

- Question: Does the artifact start with Current Understanding, Authoritative Sources, Related Code, Related Tests, Related Backlog Items, Related Wiki Pages, Open Questions, and Maintenance Notes?
- Question: Does Current Understanding describe the subsystem or feature family as it exists or is intended now?
- Question: Do Authoritative Sources include the accepted parent architecture, or an explicit Pass 3 parent target during ordered bottom-up reverse engineering, plus source files, tests, functional specifications, procedures, and related module designs?
- Question: Do Related Code and Related Tests identify evidence or say Not yet identified after a real search?
- Question: Do Open Questions capture unresolved subsystem ownership, boundaries, contracts, or verification issues?

## Artifact-Specific Questions

- Question: Does Subsystem Purpose And Parent Architecture explain why the subsystem exists and how it fits the accepted parent architecture, or explicitly record the provisional target, inherited constraints, and backfill obligation during ordered bottom-up reverse engineering?
- Question: Do Scope And Non-Goals distinguish included components, excluded components, and deferred work?
- Question: Do Current Data Anchors name authoritative data sources, state owners, records, events, messages, or external systems?
- Question: Do Constituent Components identify each component and responsibility without collapsing into implementation detail for every module?
- Question: Does Interaction Model explain calls, events, jobs, user actions, external handoffs, and sequencing?
- Question: Do Lifecycle And State describe meaningful states, transitions, retries, cleanup, and long-running behavior?
- Question: Do Data Contracts And Shapes identify inputs, outputs, persistence shape, messages, events, and validation expectations?
- Question: Does Configuration Ownership identify where configuration lives and who owns it?
- Question: Does Implementation Order give a credible sequence when the design is used for planned work?
- Question: Do Cross-Module Invariants state rules that must hold across components?
- Question: Do Definition Of Good And Verification link success criteria, tests, validation commands, and explicit gaps?
- Question: Do diagrams clarify scope, data anchors, component associations, interactions, lifecycle, data contracts, configuration ownership, implementation order, or coverage?

## Findings

Report findings first. Treat a missing parent architecture without the explicit ordered reverse-engineering provisional state, vague component responsibilities, unclear data contracts, unsupported interaction claims, missing invariants, and missing verification as review findings. After Pass 3 creates the parent architecture, treat any remaining provisional target or missing resolving parent link as a finding.
