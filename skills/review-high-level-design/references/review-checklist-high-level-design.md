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
- Question: Does Current Understanding select PLANNED_DEVELOPMENT, EXISTING_IMPLEMENTATION, or MIXED_CHANGE, and does the evidence set obey that mode?
- Question: In PLANNED_DEVELOPMENT mode, do Authoritative Sources include accepted functional specifications, parent architecture, decisions, backlog requirements, project configuration, and relevant technology guidance without requiring module designs, source, or tests that do not exist?
- Question: In EXISTING_IMPLEMENTATION or MIXED_CHANGE mode, do Authoritative Sources include the applicable accepted module designs, source, tests, configuration, procedures, and runtime evidence?
- Question: Do Related Code and Related Tests identify evidence permitted by the selected mode or say Not yet identified when planned implementation and tests do not exist?
- Question: Do Open Questions capture unresolved subsystem ownership, boundaries, contracts, identity, security, selectors, validation, state, response, or verification issues and classify each as blocking or non-blocking with a decision owner?

## Response Adequacy Questions

- Question: Does operation inventory reconciliation enumerate every primary or supporting route, API, command, event, job, notification, and reference-data lookup named by the allowed inputs, and map each supporting operation to Requirements Coverage, an owning component, boundary contracts, and verification or explicit out-of-scope authority without treating unresolved facets as permission to omit it?
- Question: Does Requirements Coverage account for every applicable functional and architecture requirement as DEFINED, OPEN, or OUT_OF_SCOPE and map it to concrete components, interactions, contracts, states, errors, and verification?
- Question: Does each DEFINED requirement identify its satisfying components, interaction, contract, state, error path, and verification rather than relying on vague subsystem prose?
- Question: Does each requirement preserve its CURRENT_BEHAVIOR, CURRENT_LIMITATION, INTENDED_BEHAVIOR, PROPOSED_CHANGE, or OPEN_QUESTION mode, with baseline and target stated separately when they differ?
- Question: Does every OUT_OF_SCOPE requirement name the authority, rationale, and owning artifact that accepts it instead of using status as an omission escape hatch?
- Question: Are unsupported specifics labeled as inferences or open questions instead of being presented as decided behavior?
- Question: Does Implementation Readiness say BLOCKED for affected downstream work when any applicable requirement is OPEN, any required cross-module contract is OPEN or CONFLICT, or any high-impact blocking question remains?

## Identity And Security Questions

- Question: Does Critical Trust And Identity Boundaries cover every applicable authenticated actor, protected operation, privileged background task, trust-boundary crossing, and sensitive-data flow?
- Question: Does each critical boundary distinguish authentication, authorization, roles, ownership, tenancy, and data filtering and define entrypoint, selector, protected asset, disclosure limit, failure posture, and sensitive-data handling?

## Cross-Module Reconciliation Questions

- Question: Does Cross-Module Contract Reconciliation cover every producer-consumer boundary with actor and authentication source; authorization, role, ownership, tenancy, and data filtering; selector mismatch behavior; payload and disclosure; validation owner; state owner and transition; and transaction, asynchronous, and error timing?
- Question: Does the design expose cross-module conflicts as OPEN or CONFLICT instead of silently selecting one contract or erasing the issue through generalization?
- Question: Does every explicit operation-specific response, selector, validation, state, or failure exception govern that boundary instead of being overwritten by a broader safety or consistency rule?

## Artifact-Specific Questions

- Question: Does Parent Architecture explain why the subsystem exists and how it fits an accepted parent architecture, or mark its absence as a blocking upstream design question?
- Question: Do Scope And Non-Goals distinguish included components, excluded components, and deferred work?
- Question: Do Data Anchors name planned or existing authoritative data sources, state owners, records, events, messages, or external systems?
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

Report findings first in separate Response Adequacy, Identity And Security, and Other Contract Or Evidence groups. Treat unaccounted requirements, unsupported specificity, hidden omissions, unjustified out-of-scope requirements, unresolved identity or selector conflicts, collapsed authentication and authorization claims, unclear disclosure, validation, or state ownership, missing transaction or error timing, unsafe sensitive-data handling, false readiness, a missing accepted parent architecture, vague component responsibilities, unclear data contracts, unsupported interaction claims, missing invariants, and missing verification as findings.
