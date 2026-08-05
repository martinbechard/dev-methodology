# High-Level Design Review Checklist

## Purpose

Use this Review Checklist to verify a high-level design artifact created from the methodology templates.

## Completion Format

For every question record:

- Status: pass, fail, question, or n/a.
- Question: copy the objective question being answered.
- Evidence type: exact quotation, summary, assessment, or not applicable.
- Evidence source: name the artifact, input, checklist, or retained response used.
- Evidence: record literal source text for an exact quotation, or a clearly labeled summary, assessment, or not-applicable explanation.
- Assessment: explain why the evidence passes, fails, is unclear, or is not applicable.

Do not mark pass without evidence. Use exact quotation only for literal source text that occurs in the named evidence source. For a mode-dependent n/a, use Evidence type: not applicable and explain why the question does not apply rather than fabricating a quotation. When a required contract is missing, use summary or assessment evidence to describe the gap and mark the item fail; there is no literal source text to quote.

## Skill Workflow Checks

- Question: Does the review identify subsystem scope, constituent components, interactions, data anchors, invariants, and verification claims before assessment?
- Question: Does the completed review checklist name this checklist as review-checklist-high-level-design.md?
- Question: Does the completed review checklist save next to the artifact using artifact-name.review-checklist-high-level-design.md?
- Question: Does the review use verify-documentation-page with the artifact, source evidence, and completed review checklist?
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
- Question: When evaluating Documentation Acceptance and Implementation Readiness, do you skip any leading retained explanatory note or notes, then require the first authored decisions to begin with ACCEPTED or BLOCKED and READY or BLOCKED, respectively, before any later explanatory prose, while Documentation Acceptance judges source evidence, accepted module prerequisites, and current reverse-engineering pass requirements without requiring intentionally absent later architecture, functional specifications, or wiki pages?
- Question: Is documentation acceptance separate from implementation readiness, allowing accurate documentation of known defects, open design decisions, and current limitations while Implementation Readiness is BLOCKED for affected downstream work?

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

- Question: Does Parent Architecture explain why the subsystem exists and how it fits an accepted parent architecture, or, during bottom-up reverse engineering before the architecture pass, state that the intentionally absent later parent is Not yet identified without inventing constraints or blocking current-pass documentation acceptance?
- Question: Do Scope And Non-Goals distinguish included components, excluded components, and deferred work?
- Question: Does each Data Anchors row identify a concrete anchor, its anchor type, its authority, its owner and representation, and an enforceable constraint for the next design layer rather than merely naming a value or access mechanism; and does the authority cite an exact accepted artifact plus requirement ID or section, or a justified HLD proposition with its basis and decision owner?
- Question: Do configuration anchors distinguish the exact configuration contract and decision authority from the environment, file, expression, or adapter used to access and validate it?
- Question: Do API, event, record, transient-state, and derived-state anchors state the fields or state boundary that must remain consistent, the owning representation, the downstream consumers, and the replace, append, clear, reset, recompute, lifetime, or persistence rules that later designs must preserve when applicable?
- Question: Do Constituent Components identify each component and responsibility without collapsing into implementation detail for every module?
- Question: Does the HLD prevent chaos at the next level of detail by giving module designers one consistent coordination frame for component vocabulary, ownership boundaries, contracts, dependencies, paths, packages or modules, integration seams, and implementation order?
- Question: Does an artifact-placement ledger map every planned source, test, configuration, migration, generated, and resource artifact to a complete repository-relative path and complete package or module namespace when applicable?
- Question: Are every proposed path and namespace literal and directly usable, with no `...`, Unicode ellipsis, wildcard, omitted intermediate directory, abbreviated package segment, `TBD`, or similar placeholder?
- Question: When Constituent Components or another placement section names three or more repository paths that share a prefix, or paths spanning two or more folders, does it present their placement in one or more fenced text trees with complete repository-relative root and package segments?
- Question: When a path tree would become large or separate components need different metadata, is it split into named component or ownership subsections with one small fenced text tree and adjacent metadata in each, without multiline table cells, simulated HTML breaks, repeated common-prefix lists, or one row per full path?
- Question: Does each justified HLD proposition state its basis, necessity, and decision owner, and are paths and namespaces precise enough to assign module work without interpretation?
- Question: Does Interaction Model explain calls, events, jobs, user actions, external handoffs, and sequencing?
- Question: Do Lifecycle And State describe meaningful states, transitions, retries, cleanup, and long-running behavior?
- Question: Whenever a section describes an ordered sequence of actions, handoffs, states, transitions, retries, recovery, scheduled phases, startup, shutdown, or dependent implementation steps, does it include an appropriate Mermaid sequence, state, or flow diagram instead of leaving the complete sequence only in prose, a numbered list, or a table?
- Question: Does each ordered-action diagram use a sequence diagram for exchanges across actors or components, a state diagram for named states and transitions, or a flowchart for branches, decisions, recovery paths, or ordered phases, with prose limited to constraints, ownership, concurrency, and exceptions?
- Question: Whenever component, contract, configuration, or verification relationships form a non-tabular topology in which one node connects to two or more others, a dependency or ownership path spans three or more nodes, a cycle exists, containment spans two or more levels, or an edge crosses a subsystem, trust, or runtime boundary, does the HLD include a structural diagram?
- Question: Does Interaction Model include a structural diagram for qualifying non-sequential collaboration while preserving sequence diagrams for ordered component collaboration, dependency handoffs, event flow, state flow, persistence flow, and external handoffs?
- Question: Do Data Contracts And Shapes identify inputs, outputs, persistence shape, messages, events, and validation expectations?
- Question: Does Configuration Ownership identify where configuration lives and who owns it?
- Question: Does Implementation Order give a credible sequence when the design is used for planned work?
- Question: Do Cross-Module Invariants state rules that must hold across components?
- Question: Do Definition Of Good And Verification link success criteria, tests, validation commands, and explicit gaps?
- Question: Do diagrams clarify scope, data anchors, component associations, interactions, lifecycle, data contracts, configuration ownership, implementation order, or coverage?

## Findings

Report findings first in separate Response Adequacy, Identity And Security, and Other Contract Or Evidence groups. Treat unaccounted requirements, unlabeled or unjustified specificity, avoidable open questions or readiness blockers, hidden omissions, unjustified out-of-scope requirements, unresolved identity or selector conflicts, collapsed authentication and authorization claims, unclear disclosure, validation, or state ownership, missing transaction or error timing, unsafe sensitive-data handling, false readiness, a missing accepted parent architecture when PLANNED_DEVELOPMENT requires it, incomplete or placeholder artifact paths, abbreviated package or module names, a missing or malformed required path tree, missing complete repository-relative tree segments, unsplit large trees, tree metadata separated from its owning tree, table-cell or HTML-simulated trees, duplicated full paths or common prefixes, an ordered action sequence left only in prose, a numbered list, or a table, a missing required structural diagram, an inappropriate diagram type that obscures an ordered or structural relationship, insufficient detail for module design, vague component responsibilities, unclear data contracts, unsupported interaction claims, missing invariants, and missing verification as findings. An intentionally absent later parent architecture during the current bottom-up EXISTING_IMPLEMENTATION reverse-engineering pass is not a documentation-acceptance finding when the artifact records it without inventing constraints and reports any readiness effect separately.
