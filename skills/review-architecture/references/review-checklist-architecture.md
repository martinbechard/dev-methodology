# Architecture Review Checklist

## Purpose

Use this Review Checklist to verify an architecture artifact created from the methodology templates.

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

- Question: Does the review identify the system boundary, runtime assumptions, layers, components, and cross-cutting claims before assessment?
- Question: Does the completed review checklist name this checklist as review-checklist-architecture.md?
- Question: Does the completed review checklist save next to the artifact using artifact-name.review-checklist-architecture.md?
- Question: Does the review use verify-documentation-page with the artifact, source evidence, and completed review checklist?
- Question: Does the final assessment derive findings or pass status from the completed review checklist rather than memory?
- Question: Does the output lead with findings ordered by severity when problems exist?

## Shared Contract Questions

- Question: Does the artifact start with Current Understanding, Authoritative Sources, Related Code, Related Tests, Related Backlog Items, Related Wiki Pages, Open Questions, and Maintenance Notes?
- Question: Does Current Understanding state the system or cross-cutting concern as it exists now?
- Question: Do Authoritative Sources include source roots, tests, configuration, procedures, and related design documents?
- Question: Do Related Code and Related Tests identify evidence or say Not yet identified after a real search?
- Question: Do Open Questions capture unresolved system boundaries, ownership, behavior, or verification conflicts?
- Question: When evaluating Documentation Acceptance and Implementation Readiness, do you skip any leading retained explanatory note or notes, then require the first authored decisions to begin with ACCEPTED or BLOCKED and READY or BLOCKED, respectively, before any later explanatory prose, while Documentation Acceptance judges source evidence, accepted high-level-design prerequisites, and current reverse-engineering pass requirements without requiring intentionally absent later functional specifications or wiki pages?
- Question: Is documentation acceptance separate from implementation readiness, allowing accurate documentation of known defects, open design decisions, and current limitations while Implementation Readiness is BLOCKED for affected downstream work?

## Artifact-Specific Questions

- Question: Does the repository taxonomy classify the target path, filename pattern, identifier, and prefix as architecture rather than HLD?
- Question: Does the artifact state its canonical architecture path and identifier plus the child-HLD location and naming convention?
- Question: Do child HLDs reference this architecture as their parent, with authority flowing from architecture to HLD to component or module design without circular references?
- Question: Does the architecture remain authoritative without depending on a child HLD for its own normative authority, even when reverse-engineering evidence was gathered bottom up?
- Question: Are detailed operation contracts, leaf-module assignments, and implementation sequencing delegated to HLDs or component designs unless they establish a project-wide rule?
- Question: When durable Markdown architecture and a fixed structured workflow artifact share one directory, are their identities, owners, review routes, and lifecycles kept distinct?
- Question: Does System Purpose And Scope define what the system is and what it excludes?
- Question: Does the architecture prevent chaos in high-level designs by giving them one coherent system frame for runtime units, subsystem vocabulary, stack, repository roots, documentation homes, ownership, layers, dependency direction, data authority, integrations, trust boundaries, configuration, lifecycle, and implementation sequence?
- Question: Are undefined but resolvable architecture choices classified as justified architecture propositions with basis, necessity, and decision owner rather than avoidable open questions?
- Question: Does a system-frame ledger map each runtime unit, subsystem, layer, data owner, integration boundary, configuration owner, and documentation family to one stable name, responsibility, allowed dependencies, and complete repository-relative roots where applicable?
- Question: Do Runtime Assumptions identify technology stack, runtime environment, deployment assumptions, and key configuration?
- Question: Does File Organization name complete repository-relative source, test, configuration, resource, migration, generated, script, runtime-data, and documentation roots plus their ownership boundaries?
- Question: Are architecture-owned paths and names literal and directly usable, without `...`, Unicode ellipsis, wildcards, omitted intermediate directories, abbreviated names, `TBD`, or similar placeholders?
- Question: When File Organization names three or more repository paths that share a prefix, or paths spanning two or more folders, does it present their placement in one or more fenced text trees with complete repository-relative root and package segments?
- Question: When a path tree would become large or separate ownership areas need different metadata, is it split into named component or ownership subsections with one small fenced text tree and adjacent metadata in each, without multiline table cells, simulated HTML breaks, repeated common-prefix lists, or one row per full path?
- Question: Do Major Layers And Dependency Direction explain which layers may call which other layers?
- Question: Do Major Components And Ownership identify durable components and their responsibilities?
- Question: Does Data Flow And Lifecycle explain data movement, persistence, state transitions, startup, shutdown, and external handoffs when applicable?
- Question: Do Cross-Cutting Concerns cover errors, testing, configuration, security, privacy, observability, object creation, persistence, and UI composition when relevant?
- Question: Do Design Principles And Invariants state rules that should hold across modules or subsystems?
- Question: Do Risks And Trade-Offs describe real risks without becoming a change log?
- Question: Does Verification link tests, validation commands, or explicit gaps for architecture-level claims?
- Question: Whenever a section describes two or more ordered actions or phases, or any handoff, data movement, lifecycle transition, branch, retry, recovery path, startup or shutdown dependency, or dependent implementation phase, does it include an appropriate Mermaid sequence, state, or flow diagram instead of leaving the complete sequence only in prose, a numbered list, or a table?
- Question: Whenever a section defines a non-tabular topology in which one system-context, scope, ownership, layer, component, dependency, principle, risk, or verification node connects to two or more others, a path spans three or more nodes, a cycle exists, containment spans two or more levels, or an edge crosses a system, trust, or runtime boundary, does it include a structural diagram?
- Question: Do ordered diagrams use a sequence diagram for exchanges across actors or components, a state diagram for named states and transitions, or a flowchart for branches, recovery paths, ordered phases, and structural associations?
- Question: Are section-specific architecture diagram triggers treated as additive minimums under the shared route-documentation-work rule, without using one satisfied section trigger to waive another shared trigger?

## Findings

Report findings first. Treat a non-architecture taxonomy classification, HLD path or identifier reuse, missing canonical architecture identity, missing child-HLD convention or parent reference, circular or inverted authority, dependence on child HLD authority, architecture-owned leaf detail, conflated durable Markdown and fixed structured workflow artifacts, missing boundaries, unlabeled or unjustified propositions, avoidable open questions, conflicting system frames, incomplete or placeholder paths, a missing or malformed required path tree, missing complete repository-relative tree segments, unsplit large trees, tree metadata separated from its owning tree, table-cell or HTML-simulated trees, duplicated full paths or common prefixes, unstable component vocabulary, unsourced stack claims, unclear dependency direction, missing ownership, unclear data or configuration authority, unsupported cross-cutting rules, HLD coordination ambiguity, an ordered or structural relationship left only in prose, a numbered list, or a table, an inappropriate diagram type, a waived additive diagram trigger, and missing verification as review findings.
