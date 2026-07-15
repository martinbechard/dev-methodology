# Module Design Review Checklist

## Purpose

Use this Review Checklist to verify a module design artifact created from the methodology templates.

## Completion Format

For every question record:

- Status: pass, fail, question, or n/a.
- Question: copy the objective question being answered.
- Quoted evidence: quote the exact artifact or source text that supports the status.
- Assessment: explain why the quoted evidence passes, fails, is unclear, or is not applicable.

Do not mark pass without quoted evidence.

## Skill Workflow Checks

- Question: Does the review identify runtime path, responsibility, callers, dependencies, contracts, internal state, processing rules, error handling, and verification claims before assessment?
- Question: Does the completed review checklist name this checklist as review-checklist-module-design.md?
- Question: Does the completed review checklist save next to the artifact using artifact-name.review-checklist-module-design.md?
- Question: Does the review use documentation-page-verify with the artifact, source evidence, and completed review checklist?
- Question: Does the final assessment derive findings or pass status from the completed review checklist rather than memory?
- Question: Does the output lead with findings ordered by severity when problems exist?

## Shared Contract Questions

- Question: Does the artifact start with Current Understanding, Authoritative Sources, Related Code, Related Tests, Related Backlog Items, Related Wiki Pages, Open Questions, and Maintenance Notes?
- Question: Does Current Understanding describe the module as it exists or is intended now?
- Question: Does Current Understanding select PLANNED_DEVELOPMENT, EXISTING_IMPLEMENTATION, or MIXED_CHANGE, and does the evidence set obey that mode?
- Question: In PLANNED_DEVELOPMENT mode, do Authoritative Sources include accepted functional specifications, architecture, owning HLD, decisions, backlog requirements, project configuration, and relevant technology guidance without requiring source or tests that do not exist?
- Question: In EXISTING_IMPLEMENTATION or MIXED_CHANGE mode, do Authoritative Sources include the applicable module source, callers, tests, configuration, parent designs, procedures, and related wiki pages?
- Question: Do Related Code and Related Tests identify evidence permitted by the selected mode or say Not yet identified when planned implementation and tests do not exist?
- Question: Do Open Questions capture unresolved ownership, contracts, behavior, errors, identity, security, selectors, validation, state, response, or verification issues and classify each as blocking or non-blocking with a decision owner?

## Response Adequacy Questions

- Question: Does Requirements Coverage account for every applicable functional and parent-design requirement as DEFINED, OPEN, or OUT_OF_SCOPE and map it to concrete design and verification?
- Question: Does each DEFINED requirement identify its satisfying contract, rule, state, error path, and verification rather than relying on vague prose?
- Question: Does every OUT_OF_SCOPE requirement name the authority, rationale, and owning artifact that accepts it instead of using status as an omission escape hatch?
- Question: Are unsupported specifics labeled as inferences or open questions instead of being presented as decided behavior?
- Question: Does Implementation Readiness say BLOCKED for affected downstream work when any applicable requirement or required contract is OPEN or any high-impact blocking question remains?

## Identity And Security Questions

- Question: When several identifiers can select the same subject or record, does the design define precedence and mismatch behavior instead of silently choosing one?
- Question: Does Trust And Identity Boundaries cover every applicable route, event, command, job, UI guard, protected operation, and sensitive-data flow?
- Question: Does each applicable trust boundary distinguish authentication, authorization, roles, ownership, tenancy, and data filtering and name the evidence for each?
- Question: Does each applicable protected operation define disclosure limits, validation ownership, state transitions, failure timing, committed side effects, and sensitive logging behavior?

## Artifact-Specific Questions

- Question: Does Runtime Path name the module's project-relative runtime path and identify its entry point when the module is a folder?
- Question: Does Parent Context explain the subsystem, architecture, feature, or workflow that owns the module?
- Question: Are Responsibilities coherent, bounded, and not a mixed list of unrelated work?
- Question: Do Callers and Dependencies identify direct callers, imported dependencies, external systems, generated artifacts, and test seams?
- Question: Do Public Contracts describe actors, triggers, inputs, selectors, validation owners, outputs, response or disclosure shapes, side effects, state owners, transaction or asynchronous boundaries, and expected errors?
- Question: Do Internal Data And State describe maintained state, caches, derived values, persistence, and ownership rules?
- Question: Do Processing Rules describe main flow, branches, retries, validation, ordering, idempotency, and concurrency rules when applicable?
- Question: Do Invariants state rules that must always hold?
- Question: Are Configuration, External Interfaces, and UI And Notification Behavior covered when the module owns them?
- Question: Does Error Handling name expected failures, propagation, logging, retry, recovery, and user-visible outcomes?
- Question: Does Verification link unit, integration, end-to-end, lint, validation, or manual evidence for each important responsibility?
- Question: Does Processing Diagram exist only when it clarifies real branches, state transitions, retries, or error handling?

## Findings

Report findings first in separate Response Adequacy, Identity And Security, and Other Contract Or Evidence groups. Treat unaccounted requirements, unsupported specificity, hidden omissions, missing runtime path, broad or mixed responsibilities, missing callers, vague contracts, unresolved selector conflicts, collapsed authentication and authorization claims, unclear disclosure or validation ownership, incomplete error timing, unsafe sensitive logging, false readiness, unsourced processing rules, and missing verification as review findings.
