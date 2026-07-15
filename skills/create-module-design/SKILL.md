---
name: create-module-design
description: Use when creating or substantially rewriting a module design artifact from the development-methodology module-design-template asset, including runtime path, parent context, responsibilities, callers, dependencies, public contracts, internal state, processing rules, invariants, configuration, external interfaces, UI behavior, error handling, and verification.
metadata:
  category: artifact-creation
---

# Create Module Design

Use this skill to create or substantially rewrite one module design artifact. The artifact defines one implementation unit precisely enough that code and tests can be understood or written without guessing.

## Template

Use skills/development-methodology/assets/templates/module-design-template.md as the starting asset.

Copy the template only when a local editable artifact is needed. Replace every TODO instruction with content supported by the authoritative inputs for the selected design mode.

Treat every level-two heading in the template as mandatory. Preserve the heading text and order exactly; do not rename, merge, reorder, or omit headings. When a section is not applicable, keep its heading and state why. Compare the candidate's ordered level-two headings with the template before production review. A mismatch is BLOCKED and must be corrected before spending a semantic-review pass.

The first nonblank content under Implementation Readiness must begin with READY or BLOCKED. Put the decision before explanatory prose so deterministic gates and downstream agents cannot mistake an unresolved design for an accepted one.

## Design Mode

Choose and state exactly one mode before writing:

- PLANNED_DEVELOPMENT defines intended behavior from accepted functional specifications, architecture, high-level designs, decisions, and backlog requirements. Code and tests may be Not yet identified.
- EXISTING_IMPLEMENTATION documents current behavior from executable source, configuration, migrations, tests, and retained runtime evidence.
- MIXED_CHANGE separates current behavior from the intended change and names the authority for each statement.

Use only the authoritative inputs permitted by the selected design mode. In planned development, names, framework conventions, generated defaults, and likely implementation patterns are not requirements evidence.

## Scope

Create one module design that defines:

- Runtime path.
- Parent context.
- Responsibilities.
- Callers.
- Dependencies.
- Public contracts.
- Requirements coverage.
- Trust and identity boundaries when applicable.
- Internal data and state.
- Processing rules.
- Processing diagram when useful.
- Invariants.
- Configuration.
- External interfaces.
- UI and notification behavior.
- Error handling.
- Verification.

Use create-high-level-design when the work spans several modules, components, tasks, services, or UI surfaces. Use create-architecture when the work defines project-wide boundaries, layers, technology choices, or cross-cutting rules.

Use documentation-reverse-engineer when the user asks to derive many module designs from an existing codebase.

## Workflow

1. Select PLANNED_DEVELOPMENT, EXISTING_IMPLEMENTATION, or MIXED_CHANGE. Record the authoritative input set and source-precedence rule before deriving behavior.
2. Inspect only the evidence permitted by that mode. For planned development, read accepted functional specifications, architecture, owning high-level design, decisions, backlog requirements, project configuration, and relevant technology guidance. For existing behavior, also read implementation, callers, imports, exported contracts, tests, procedures, configuration, and runtime evidence.
3. Build a requirements coverage ledger before prose. Account for every applicable requirement as DEFINED, OPEN, or OUT_OF_SCOPE, preserve whether it is CURRENT_BEHAVIOR, CURRENT_LIMITATION, INTENDED_BEHAVIOR, PROPOSED_CHANGE, or OPEN_QUESTION, and link it to the contract, rule, state, error path, and verification that satisfy it. Copy the target assignment and its owning-HLD constituent-component description into the ledger, decomposing every scope-bearing qualifier into a requirement facet instead of shortening the assignment to a generic module label.
4. Build an operation-contract ledger before prose. For every public operation, copy the most specific accepted wording for its selector, request and response type binding, response or disclosure shape, field-level input constraints, required or optional status, validation owner, state owner, side-effect initiator, submission owner, asynchronous execution or delivery owner, completion signal, failure timing, current limitations, intended target, and exceptions. Trace each entry to its authoritative source. Search every occurrence of the operation name, route, responsibility, and close synonym across the inputs before applying cross-cutting principles or marking a contract OPEN. Preserve scope-bearing qualifiers from the target assignment or owning-HLD component description—such as eligibility, audience, ownership, projection, paging, lifecycle, or best-effort modifiers—as operation facets; do not reduce a qualified operation to its generic noun. When compatible accepted inputs unambiguously describe different facets of the same exact operation, reconcile them into one contract and retain the source for each facet; do not require every fact to appear in one source sentence. For list or query operations, record client presentation state, request filter/page/sort inputs, server acceptance and validation, deterministic ordering, response rows and metadata, and reload behavior separately so one facet is not inferred from another.
5. Identify the module's single primary responsibility, runtime path, callers, dependencies, public contracts, internal state, processing rules, side effects, error behavior, and verification obligations.
6. For every route, event, command, job, UI guard, protected operation, or sensitive-data flow, define the actor and authentication source; authorization, role, ownership, tenancy, and data-filtering rules separately; identity selector and mismatch behavior; validation owner; response and disclosure shape; state owner and transition; transaction or asynchronous boundary; failure timing; logging; and sensitive-data handling. Keep the accepted security outcome separate from its implementation mechanism: an accepted authenticated-only or role-required outcome may be DEFINED while the exact filter, annotation, guard, or middleware remains OPEN. Names such as public API, public user, public projection, guest view, or open catalog do not prove anonymous access; require operation-specific authentication evidence and otherwise leave the authorization outcome OPEN.
7. Reconcile duplicate or conflicting selectors and contracts across path, body, token, session, message, and persistence identifiers. Do not choose one silently. Preserve the source's exact level of specificity: `body identity` does not authorize choosing body login, body ID, or another field. Keep the accepted wording and record the missing field or rule as OPEN. Bind evidence to the exact operation identity, such as method plus route, command, event, or job. Do not transfer a response, failure, validation, or side-effect contract from a sibling operation merely because names or responsibilities are similar. A high-impact unresolved conflict is a blocking open question.
8. Reconcile specific operation contracts before applying general principles. Within the accepted source-precedence rule, a more specific operation contract governs a general architecture or safety principle for that operation. Preserve the specific contract as CURRENT_BEHAVIOR or CURRENT_LIMITATION and describe a safer target separately; do not silently replace, sanitize, or generalize it. Preserve partial specificity: if the source establishes an entity-shaped response, a DTO projection, no body, or another shape category but not exact fields, record the known category and mark only the fields OPEN. Compatible operation-bound facts may be distributed across accepted functional, architecture, and high-level-design inputs; combine them when they name the same operation and do not conflict, while retaining each fact's authority. This is evidence reconciliation, not permission to transfer a sibling operation's contract. A type named in a data-shape catalog is not evidence that a particular operation uses it; require an operation-bound statement or leave the request or response type OPEN. Do not assume two routes, overloads, or sibling operations share a response or failure contract unless an accepted source states the shared rule. Treat actual contradictions between authoritative sources as open conflicts rather than resolving them by preference.
9. For credential, token, key, secret, or other sensitive inputs, define or explicitly leave open the input-only or write-only contract, field constraints, validation owner, forwarding boundary, encryption or hashing owner, response exclusion, failure timing, and logging prohibition. A general non-disclosure statement does not replace the operation-level input contract.
10. Copy the module design template into the target documentation location when a new artifact is needed, preserving every level-two heading exactly and in order.
11. Replace each TODO with authoritative content, an explicit inference, or an open question.
12. Keep the shared page contract sections first.
13. Verify dependency paths against existing source files or an accepted planned type registry. Do not invent paths.
14. Keep configuration, external interface, and UI behavior headings. When one does not apply, state that explicitly instead of removing or renaming the section.
15. Say Not yet identified for related code, tests, backlog items, or wiki pages that do not exist yet.
16. Keep the artifact steady-state. Do not describe it as new, revised, or enhanced unless the document is explicitly a change plan.
17. Treat owned files as the responsibility boundary, not the evidence boundary. Add direct links to non-owned callers, dependencies, schemas, configuration, security rules, error adapters, tests, procedures, and parent documents whenever the page relies on them.
18. Audit each behavioral sentence for evidence closure. Link the accepted requirement or source that proves it, label it as an inference, or record it as unverified/open; do not let an adjacent generic source list stand in for direct evidence.
19. In existing-implementation or mixed mode, verify that claimed tests are executable and exercise the named branch. Describe unannotated helpers, unused fixtures, manual commands, and desired tests as gaps rather than coverage.
20. Follow failure paths through nested causes, wrapper fallbacks, validation differences, retries, logging, rollback, and user-visible outcomes. Preserve any accepted upstream current behavior or limitation even in a planned design, then state the intended target separately. Do not silently replace a known defect or compatibility contract with the safer behavior under consideration.
21. For every external or asynchronous effect, build one phase ledger before writing processing prose. Use only phases established by accepted inputs. Record the trigger, state already committed, initiator, submission owner, executor or delivery owner, response visibility, failure outcome, retry or compensation, and completion evidence for each phase. For executor-backed work, place executor acceptance or rejection before any work assigned to that executor. Rendering, construction, persistence, or sending may precede acceptance only when an accepted input explicitly assigns that precomputation to the initiator or submission owner; otherwise leave the ordering and owner OPEN. Do not merge executor rejection with a later sender or provider rejection. Do not invent a provider-delivery phase when the source establishes only submission and later execution, and do not prescribe transaction ordering, preconstruction, or another implementation mechanism merely because it could satisfy the required observable outcome. Keep Public Contracts, Processing Rules, diagrams, Error Handling, Invariants, and Verification consistent with this one ledger.
22. For observable, promise, callback, stream, signal, store, or cached-result flows, record four effects separately: the value returned or emitted to the current caller, mutation of persistent or reactive state, cache creation/replacement/retention/invalidation, and subscriber-triggered side effects. A mapped, caught, or fallback emission does not prove that a signal, store, or cache was mutated. Preserve stale-state and failed-cache outcomes when accepted inputs establish them.
23. Treat the target as the installed documentation path when resolving links. Link only durable project artifacts that will exist from that location. Temporary inputs may guide the draft, but do not link or cite transient assembly or control files such as prompts, manifests, assignments, copied project context, evaluation case roots, or scratch files. When no durable project source exists, state that it is not yet identified instead of inventing a link.

## Verification

Before finishing:

1. Compare the ordered level-two headings with the module design template and verify that Implementation Readiness begins with READY or BLOCKED. If any required heading is missing, renamed, duplicated, merged, or reordered, or the readiness marker does not lead its section, stop with BLOCKED and correct the structure before invoking review-module-design.
2. After the template-conformance gate passes, use review-module-design on the completed artifact.
3. Use documentation-page-verify with the artifact, source evidence, and completed review checklist when the review skill calls for it.
4. Run project wiki status and lint when docs/wiki exists and the artifact lives in or links from docs/wiki.
5. Search the artifact for unresolved TODO markers that are not intentional.
6. Confirm every responsibility, dependency, public contract, processing rule, invariant, and verification claim has source evidence or an open question.
7. Confirm Runtime Path contains an explicit project-relative implementation path and folder entry point when applicable.
8. Confirm Authoritative Sources includes the direct evidence used by Callers, Dependencies, Configuration, Error Handling, and Verification, including evidence owned by other modules.
9. In existing-implementation or mixed mode, confirm every claimed test is discovered and executes the asserted branch; do not count helper methods, dormant fixtures, or prospective commands as coverage.
10. In existing-implementation or mixed mode, confirm error, wrapper, build-lifecycle, and validation prose matches the implemented failure branches rather than intended behavior.
11. Confirm every applicable functional requirement appears in Requirements Coverage with one explicit status and no high-impact omission hidden in prose.
12. Confirm every identity or security-sensitive contract distinguishes authentication, authorization, ownership or tenancy, data filtering, selector precedence, validation ownership, response disclosure, state ownership, error timing, and sensitive logging.
13. Confirm blocking open questions prevent implementation across the affected contract instead of being resolved by an unsupported guess.
14. Confirm every accepted current limitation remains visible beside any proposed target and every operation-specific exception survives broader security or response-shape generalization.
15. Confirm every public operation agrees with the pre-draft operation-contract ledger, including exact source specificity. A generic selector such as `body identity` must remain generic and OPEN unless an accepted source names its field.
16. Confirm a more specific accepted operation response or disclosure contract has not been replaced by a general safe-projection principle; preserve the baseline contract and state the safer target separately.
17. Confirm every OPEN contract is open only at the unresolved level. Do not mark an entire response or selector OPEN when its category, source, or current behavior is established but finer details are not.
18. Confirm each stated input constraint appears in the exact operation contract with required or optional status and validation ownership; do not collapse concrete limits into `validated payload`.
19. Confirm every failure and response claim traces to the same exact operation. Remove cross-operation transfers and unsupported route-equivalence claims.
20. Confirm sensitive input contracts cover validation, handoff, protection, response exclusion, failure timing, and logging or mark each unresolved element OPEN.
21. Confirm every external or asynchronous effect identifies the exact initiator, submission owner, executor or delivery owner, completion signal, and failure phase. Distinguish transaction commit, submission rejection, later execution or delivery failure, and durable receipt; do not collapse them into one asynchronous outcome.
22. Confirm every concrete request or response type is bound to that exact operation by an authoritative source rather than selected from a nearby type catalog or suggestive name.
23. Confirm compatible facts distributed across accepted inputs were reconciled for the same exact operation before marking the whole contract OPEN, while sibling-operation facts remain separate.
24. For list or query operations, confirm presentation sort state, request sort/page/filter inputs, server validation, deterministic ordering, response metadata, and reload behavior are each DEFINED, OPEN, or OUT_OF_SCOPE independently.
25. Confirm every external or asynchronous effect has one internally consistent phase ledger and that no prose or diagram moves work between phases, puts executor-owned work before executor acceptance, merges executor rejection with a later sender or provider rejection, invents a later delivery phase, or prescribes an unsupported transaction or construction mechanism.
26. Confirm every reactive or asynchronous failure distinguishes its returned or emitted value from signal/store mutation, cache replacement or retention, and subscriber side effects; do not convert a fallback emission into an unproved state transition.
27. Resolve every local Markdown link from the installed documentation path and remove links to transient assembly or control files before review.

Do not send private, proprietary, sensitive, PII, or company-internal material to an external service unless the user explicitly authorizes it.
