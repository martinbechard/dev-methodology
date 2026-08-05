---
name: create-functional-spec
description: Use when creating or substantially rewriting a functional specification artifact from the route-documentation-work functional-spec-template asset, including actors, entry points, workflows, states, edge cases, acceptance behavior, and verification evidence.
metadata:
  category: artifact-creation
---

# Create Functional Specification

Use this skill to create or substantially rewrite one functional specification artifact. The artifact describes observable behavior from the actor's point of view and links the code, tests, and source material that define the behavior.

For planned development, treat the functional specification as behavior design rather than only a restatement of upstream notes. Make reasonable, explicitly labeled justified functional propositions for undefined but resolvable actor-visible behavior. State each proposition's basis, why it is necessary to complete the workflow or unblock downstream design, and the role that owns or may revise it. Do not present propositions as accepted requirements.

## Template

Use skills/route-documentation-work/assets/templates/functional-spec-template.md as the starting asset.

Copy the template only when a local editable artifact is needed. Replace every TODO instruction with source-backed content from the target repository.

## Scope

A central goal of the functional specification is to avoid chaos in architecture and design. Give downstream authors one coherent actor-visible contract for actor vocabulary, stable operation identity, entry points, inputs and requiredness, permissions, validation, states, ordering, visible results, errors, recovery, persistence outcomes, and acceptance scenarios. Do not leave separate architecture or design authors to invent incompatible behavior.

Use authoritative constraints, project directives, product conventions, usability principles, and practical judgment to propose missing behavior. Reserve Open Questions for genuine conflicts or decisions that cannot be resolved satisfactorily within functional-specification authority. Where an exact actor-visible contract is required, reject `...`, a Unicode ellipsis, wildcards, `TBD`, catch-all wording, unnamed variants, and omitted intermediate states. Keep implementation paths and package structures in architecture and design documents.

Create one functional specification that defines:

- Parent workflow.
- Actors.
- Entry points.
- Scope.
- User-facing concepts.
- Workflows.
- Workflow diagrams for every workflow with two or more ordered actor actions, or with any branch, permission gate, alternate path, recovery path, state transition, or external handoff.
- Proportionate interface examples, or a concrete no-example rationale when no required-example condition applies.
- States and rules.
- Edge cases.
- Verification blocks.

Use project-wiki-topic-write instead when the task is a durable wiki topic page that summarizes existing functional knowledge without owning the functional specification.

Use reverse-engineer-project-documentation when the user asks to derive a set of functional specifications from an existing codebase.

## Interface Examples

Classify every documented interface as UI, API, event or message, CLI, or another non-interactive surface. Select examples from the interface type and the behavior that the specification makes contractually significant. This methodology does not require HTML or a UI mockup for every functional specification.

- UI behavior requires a proportionate mockup, wireframe, or interaction diagram when the contract depends on spatial placement, ordering, grouping, relative prominence, two or more view states that must be compared, an overlay or simultaneous region, responsive or conditional layout, or direct manipulation such as drag, drop, drawing, or spatial selection. Identify whether the visual example defines a layout, state-transition, or interaction contract. A workflow diagram satisfies this requirement only when it makes that same contract observable.
- API behavior requires one coherent example containing the method, path, query parameters, headers, authentication, and request body together with the response status, headers, and body. Include representative validation, authentication, and conflict cases.
- Event or message behavior requires a representative payload and a producer-consumer sequence that makes direction, ordering, acknowledgement, and failure behavior observable when applicable.
- CLI behavior requires a representative invocation, output, and failure, including relevant arguments, options, exit status, and diagnostic output.
- Simple or non-interactive behavior may use a concrete no-example rationale only when no required interface example above applies. Name the interface and behavior, explain why an additional example would add no contract information, and identify the exact prose, table, or verification block that already makes the observable behavior unambiguous.

One example may cover multiple operations only when the specification maps each operation to the example and preserves its distinct inputs, outcomes, and failures. Otherwise provide separate examples.

## Reverse-Engineering Acceptance

During the functional-specification current reverse-engineering pass, derive behavior from the accepted architecture and lower-level designs plus source, routes, UI surfaces, commands, jobs, tests, procedures, and runtime evidence. Wiki pages are intentionally created later and are not a mandatory current-pass input. Record their absence as Not yet identified where applicable; do not block documentation acceptance solely because wiki integration has not occurred.

Documentation acceptance asks whether the specification accurately records observable behavior and satisfies current-pass requirements. Implementation readiness separately asks whether the workflow is sufficiently decided and supported for downstream implementation or change. Known defects, unimplemented behavior, open design decisions, and current limitations may remain visible in ACCEPTED documentation while making downstream implementation BLOCKED.

## Workflow

1. Inspect the target repository before writing. Read product requirements, README files, task-relevant procedures, routes, UI surfaces, commands, integrations, services, tests, backlog files, existing docs, wiki pages, and current worktree status.
2. Identify the actor goal, entry points, states, permissions, visible outcomes, and verification evidence.
3. Build a primary and supporting operation inventory before prose. Include every route, API, command, event, job, notification, and supporting reference-data lookup directly invoked by the workflow, even when it is not the workflow's main subject. For each operation record actor and authentication source; authorization, ownership, tenancy, and data filtering; selector, request, paging, and sort; response projection, disclosure, status, and error; state or side effects; and verification. Preserve supported facts and mark only unresolved facets open.
4. Copy the functional specification template into the target documentation location when a new artifact is needed.
5. Replace each TODO with behavior grounded in authoritative source material.
6. Keep the shared page contract sections first.
7. Write workflow steps from the actor's point of view.
8. Include disabled states, error states, empty states, unavailable states, confirmation behavior, redirects, persistence outcomes, and important negative behavior when source evidence supports them.
9. When scenario-heavy behavior is involved, map actors, entry points, states, permissions, main paths, alternate paths, and recovery paths to named scenarios. Keep diagrams, prose, tables, and machine-readable contracts consistent.
10. Add a Mermaid workflow diagram whenever a workflow has two or more ordered actor actions, or any branch, permission gate, alternate path, recovery path, state transition, or external handoff. Use a sequence diagram for ordered actor-system exchanges, a state diagram for named states and transitions, and a flowchart for branches, decisions, or recovery paths. Prose, numbered lists, and tables may explain details but must not carry the complete workflow alone. Verification-step lists are test procedures and do not independently trigger a workflow diagram.
11. Classify every documented interface and provide each required interface example or its permitted concrete no-example rationale.
12. Record the project-owned approval or acceptance authority when one exists. Do not invent a universal approval gate.
13. Say Not yet identified for related code, tests, backlog items, or wiki pages that do not exist yet.
14. Keep the artifact steady-state. Do not describe it as new, revised, or enhanced unless the document is explicitly a change plan.

## Verification

Before finishing:

1. Use review-functional-spec on the completed artifact.
2. Use verify-documentation-page with the artifact, source evidence, and completed review checklist when the review skill calls for it.
3. Run project wiki status and lint when docs/wiki exists and the artifact lives in or links from docs/wiki.
4. Search the artifact for unresolved TODO markers that are not intentional.
5. Confirm every workflow, state group, edge case, and acceptance claim has source evidence or a clearly recorded open question.
6. Reconcile every primary and supporting operation inventory row with Entry Points, Workflows, States And Rules, Edge Cases, and Verification. Do not omit a supporting operation merely because its most specific filter, projection, paging, or error detail remains open.
7. For Documentation Acceptance, skip any leading retained explanatory note or notes, then confirm the first authored decision begins with ACCEPTED or BLOCKED and judges source evidence, accepted design prerequisites, and current reverse-engineering pass requirements without requiring intentionally absent wiki pages.
8. For Implementation Readiness, skip any leading retained explanatory note or notes, then confirm the first authored decision begins with READY or BLOCKED as a separate downstream decision and preserves known defects, unimplemented behavior, open decisions, and current limitations.
9. Confirm every undefined but resolvable actor-visible detail is covered by a justified functional proposition with basis, necessity, and decision owner rather than an avoidable open question.
10. Confirm exact actors, operation identities, inputs, states, statuses, outcomes, and acceptance scenarios contain no ellipsis, wildcard, `TBD`, catch-all wording, unnamed variant, or omitted intermediate state that would force downstream invention.
11. Confirm every workflow with two or more ordered actor actions, or any branch, permission gate, alternate path, recovery path, state transition, or external handoff, has an appropriate Mermaid diagram and is not left only in prose, a numbered list, or a table.
12. Confirm every documented interface has its required proportionate example, or a concrete no-example rationale only when no required-example condition applies.

Do not send private, proprietary, sensitive, PII, or company-internal material to an external service unless the user explicitly authorizes it.
