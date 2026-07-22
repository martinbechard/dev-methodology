# Functional Specification Review Checklist

## Purpose

Use this Review Checklist to verify a functional specification artifact created from the methodology templates.

## Completion Format

For every question record:

- Status: pass, fail, question, or n/a.
- Question: copy the objective question being answered.
- Quoted evidence: quote the exact artifact or source text that supports the status.
- Assessment: explain why the quoted evidence passes, fails, is unclear, or is not applicable.

Do not mark pass without quoted evidence.

## Skill Workflow Checks

- Question: Does the review identify the actor, workflow, surfaces, states, and verification claims before assessment?
- Question: Does the completed review checklist name this checklist as review-checklist-functional-spec.md?
- Question: Does the completed review checklist save next to the artifact using artifact-name.review-checklist-functional-spec.md?
- Question: Does the review use documentation-page-verify with the artifact, source evidence, and completed review checklist?
- Question: Does the final assessment derive findings or pass status from the completed review checklist rather than memory?
- Question: Does the output lead with findings ordered by severity when problems exist?

## Shared Contract Questions

- Question: Does the artifact start with Current Understanding, Authoritative Sources, Related Code, Related Tests, Related Backlog Items, Related Wiki Pages, Open Questions, and Maintenance Notes?
- Question: Does Current Understanding describe the behavior as it should be understood now?
- Question: Do Authoritative Sources distinguish implemented behavior from intended behavior?
- Question: Do Related Code and Related Tests identify evidence or say Not yet identified after a real search?
- Question: Do Open Questions capture behavior, ownership, or acceptance conflicts that cannot be resolved from sources?
- Question: Does Documentation Acceptance begin with ACCEPTED or BLOCKED and judge source evidence, accepted design prerequisites, and current reverse-engineering pass requirements without requiring intentionally absent later wiki pages?
- Question: Does the first nonblank content under Documentation Acceptance begin with ACCEPTED or BLOCKED, and does the first nonblank content under Implementation Readiness begin with READY or BLOCKED, before any explanatory prose?
- Question: Is documentation acceptance separate from implementation readiness, allowing accurate documentation of known defects, unimplemented behavior, open design decisions, and current limitations while Implementation Readiness is BLOCKED for affected downstream work?

## Artifact-Specific Questions

- Question: Does User Or Actor Goal name the actor and the outcome they need?
- Question: Does the specification prevent chaos in architecture and design by giving downstream authors one coherent actor-visible contract for actors, operations, entry points, inputs, permissions, validation, states, ordering, visible results, errors, recovery, persistence outcomes, and acceptance scenarios?
- Question: Are details not established by authoritative inputs classified as justified functional propositions or open questions rather than presented as accepted requirements?
- Question: Does each justified functional proposition explain its supporting constraints or reasoning, why it is necessary to complete the workflow or unblock downstream design, and the role that owns or may revise it?
- Question: Before leaving a resolvable actor-visible detail open, does the specification make a reasonable effort to propose practical behavior?
- Question: Are exact actor-visible contracts free of `...`, Unicode ellipsis, wildcards, `TBD`, catch-all wording, unnamed variants, and omitted intermediate states?
- Question: Do Parent Workflow And Entry Points identify where the workflow starts and how users reach it?
- Question: Does Route Or Surface List cover relevant routes, screens, commands, APIs, notifications, or external surfaces?
- Question: When Related Code or another placement section names three or more repository paths that share a prefix, or paths spanning two or more folders, does it present their placement in one or more fenced text trees with complete repository-relative root and package segments?
- Question: When a path tree would become large or separate workflow surfaces need different metadata, is it split into named component or ownership subsections with one small fenced text tree and adjacent metadata in each, without multiline table cells, simulated HTML breaks, repeated common-prefix lists, or one row per full path?
- Question: Does a primary and supporting operation inventory cover every route, API, command, event, job, notification, and supporting reference-data lookup directly invoked by the workflow, with actor and authentication source; authorization, ownership, tenancy, and data filtering; selector, request, paging, and sort; response projection, disclosure, status, and error; state or side effects; and verification?
- Question: Do Scope And Non-Goals distinguish included behavior from excluded or deferred behavior?
- Question: Do Concepts define terms the actor must understand without drifting into module design?
- Question: Are Workflow Steps written from the actor's point of view and do they cover main, alternate, empty, error, and recovery paths?
- Question: Does every workflow with two or more ordered actor actions, or any branch, permission gate, alternate path, recovery path, state transition, or external handoff, include an appropriate Mermaid sequence, state, or flow diagram instead of leaving the complete workflow only in prose, a numbered list, or a table?
- Question: Does each workflow diagram use a sequence diagram for ordered actor-system exchanges, a state diagram for named states and transitions, or a flowchart for branches, decisions, or recovery paths, while treating verification-step lists as test procedures rather than workflow-diagram triggers?
- Question: Do States, Rules, Permissions, And Edge Cases identify status values, permission gates, validation rules, limits, and failure behavior?
- Question: Do Verification blocks name test type, test files, scenario, steps, assertions, and current status?
- Question: Do Related Documents link architecture, high-level design, module design, tests, and wiki pages that support the workflow?
- Question: Does technical implementation detail stay in related technical documents unless users need it to understand behavior?
- Question: When named scenarios are used, do they cover every material actor, entry point, state, permission, main path, alternate path, and recovery path?
- Question: Are scenario prose, workflow diagrams, state tables, and machine-readable contracts consistent with each other?
- Question: Does the artifact name the project-owned approval or acceptance authority when one exists, without inventing a universal gate?

## Findings

Report findings first. Treat missing actor goal, missing entry points, missing acceptance behavior, missing state or permission coverage, unlabeled or unjustified propositions, avoidable open questions, ambiguous shorthand, downstream behavior ambiguity, unsourced workflow claims, a missing or malformed required path tree, missing complete repository-relative tree segments, unsplit large trees, tree metadata separated from its owning tree, table-cell or HTML-simulated trees, duplicated full paths or common prefixes, a qualifying workflow left only in prose, a numbered list, or a table, an inappropriate diagram type, and missing verification as review findings.
