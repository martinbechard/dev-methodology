# Migration Review: Documenting a New Design

## Source

[Legacy procedure](../procedure-document-new-design.md) defines a pre-implementation design document for one non-trivial module or feature. It asks the author to establish the intended runtime location and responsibility, inspect related designs, make callers and dependencies explicit, specify contracts and rules, plan testing, then verify and review the proposal.

## Durable Guidance Worth Keeping

- Start from requirements and current repository evidence, including relevant parent designs, callers, dependencies, type definitions, configuration, tests, and established project conventions.
- Select the smallest design artifact that owns the intended work: module design for one implementation unit, high-level design for a coherent multi-module feature or integration, and architecture for cross-cutting system decisions.
- Give the design a bounded responsibility, planned runtime path, parent context, direct callers, dependencies, contracts, state, processing rules, invariants, configuration, external interfaces, failure behavior, and verification evidence appropriate to its scope.
- Explain material relationships and trade-offs with concise, source-backed rationale. Treat unsupported facts and decisions still awaiting evidence as open questions rather than as settled design.
- Use editable diagrams only when they materially clarify caller and dependency topology, data movement, lifecycle, state transitions, branching, retries, or error paths.
- Plan verification before implementation, including important responsibilities, invalid input, integration boundaries, dependency failures, persistence, and observable outcomes.
- Complete the matching artifact review and preserve a traceable link from design intent to the code, tests, and parent documents that eventually substantiate it.

## Mapping And Coverage

| Legacy point | Live destination | Coverage | Recommendation |
| --- | --- | --- | --- |
| Understand requirements; inspect related designs and reusable components before drafting | [development-methodology](../../skills/development-methodology/SKILL.md), [create-module-design](../../skills/create-module-design/SKILL.md), and [create-high-level-design](../../skills/create-high-level-design/SKILL.md) | Covered | Retain the evidence-first workflow. The current router prevents a proposed feature from being forced into a module document when it is actually a subsystem or architecture concern. |
| Determine a unique module name and planned code location | [module design template](../../skills/development-methodology/assets/templates/module-design-template.md), Runtime Path and Related Code | Covered | State the planned project-relative path and ownership. Do not impose a universal class naming convention; use the target project convention. |
| Create a module-design file in a fixed directory and recreate obsolete documents from scratch | Target repository documentation convention; module-design template | Not portable | Let the target repository choose document home and filename. Update existing source-backed artifacts carefully rather than discarding history by default. |
| Record responsibilities and anticipate a possible split for a large module | [create-module-design](../../skills/create-module-design/SKILL.md), Responsibilities, and [review-module-design](../../skills/review-module-design/SKILL.md) | Covered | Preserve bounded, testable responsibilities. Review cohesion and independent change pressure instead of applying the legacy 300-line threshold. |
| Identify intended callers, show examples, and explain why each calls the module | Module design Callers and Public Contracts sections | Covered | Require actual or planned direct callers and their contract rationale. Use examples only where they make invocation or ownership less ambiguous. |
| Identify imported dependencies, named types, external systems, and why each is needed | Module design Dependencies, External Interfaces, and Authoritative Sources sections | Covered | Keep named dependency and external-boundary clarity; validate paths against source or a planned registry and do not invent links. |
| Draw module and key-function context diagrams | Module-design Processing Diagram and [documentation-page-verifier](../../skills/documentation-page-verifier/SKILL.md) diagram checks | Partly covered | The current path supports diagrams for real dependencies, flows, retries, and errors, but the module template does not explicitly prompt for a caller/dependency context diagram. Add a narrow conditional prompt. |
| State security, performance, integrity, and business invariants | Module design Invariants and review checklist | Covered | Retain source-backed invariants, categorized only when doing so helps review or verification. |
| Record decisions, alternatives, rationale, assumptions, and trade-offs | Open Questions and Maintenance Notes in the module and high-level templates; [structured-design](../../skills/structured-design/SKILL.md) for explicitly structured decision writing | Partly covered | Use Open Questions for unresolved assumptions and source conflicts. Add a concise optional Design Decisions subsection or decision-record link for material, reversible, or cross-module trade-offs. |
| Define proposed classes, interfaces, types, functions, signatures, and high-level processing | Module design Public Contracts, Internal Data And State, and Processing Rules | Covered | Keep only contract and logic detail required to remove implementation ambiguity. Do not require exhaustive private-member inventories or pseudocode for straightforward functions. |
| Describe state machines or complex workflows | Module design Processing Rules and Processing Diagram; high-level design Lifecycle | Covered | Route cross-module lifecycle and state ownership to high-level design; retain module-level states and transitions where the module owns them. |
| Specify externally owned HTTP calls, request and response data, authentication, and failures | Module design External Interfaces and Error Handling | Covered | Retain external contract detail only for interfaces the module directly owns. Avoid a mandatory endpoint inventory for modules with no external boundary. |
| Specify configuration values, defaults, validation, and ownership | Module design Configuration | Covered | Preserve this topic when the module reads or owns configuration; remove the section only when genuinely inapplicable. |
| Plan unit and integration scenarios, edges, mocks, and test challenges | Module design Verification; [Jest](../../skills/jest/SKILL.md) and [Vitest](../../skills/vitest/SKILL.md) | Partly covered | Verification already covers core scenarios and failure boundaries. Add a small conditional prompt to identify critical test seams, fixtures, or boundary doubles without placing framework-specific policy in the design template. |
| Verify dependencies, submit for review, resolve feedback, then establish the design as implementation reference | [review-module-design](../../skills/review-module-design/SKILL.md), its [review checklist](../../skills/review-module-design/references/review-checklist-module-design.md), and [documentation-page-verifier](../../skills/documentation-page-verifier/SKILL.md) | Partly covered | Keep path and source validation plus the completed review checklist. Do not require a repository-specific dependency script or file-header comment; require durable links among the design, source, tests, and parent documents where the target project supports them. |

## Gaps And Precise Improvements

The catalog has no need for a separate new-design skill or a new agent. Creation is owned by the artifact-specific design skills and review by Artifact Review Agent through the matching review skill.

Two small improvements would retain the procedure's useful specificity without restoring its rigid format:

1. Add this conditional guidance to the module-design template Processing Diagram section and create-module-design:

   > Add a module context diagram when direct callers, dependencies, or owned external interfaces form a relationship set that is difficult to inspect in prose. Show only direct relationships and material contracts or handoffs; keep internal processing detail in Processing Rules.

2. Add this conditional sentence to the module-design template Verification section:

   > Identify the test seams, fixtures, or boundary doubles needed for important scenarios, and link applicable project or test-framework guidance when it exists.

A third, lower-priority refinement is an optional Design Decisions subsection or link to an existing decision record. It should capture only material decisions, alternatives, rationale, and invalidating assumptions. The current Open Questions section already owns unresolved matters, so this must not introduce a mandatory decision log for routine modules.

## Guidance To Omit Or Narrow

- Omit the fixed design/modules location, module-name-design filename, wiki-link syntax, central definitions file, and dependency-verification command. These are repository-local mechanisms, not portable skill rules.
- Omit PascalCase as a universal rule. Naming follows the language, export form, and target project's conventions.
- Omit the instruction to create a fresh document by default when an earlier draft exists. Preserve valid evidence and history; replace only unsupported or obsolete content.
- Omit the fixed size threshold, mandatory detailed class/type inventory, and prescribed pseudo-code syntax. Use contract, cohesion, and control-flow complexity to decide the necessary level of detail.
- Narrow BECAUSE chains from a mandated document-wide notation to a requirement for clear causal rationale at material decisions, relationships, invariants, and processing rules. Use structured-design only when that formal format is selected.
- Omit compulsory diagrams, all optional sections, and a separate API inventory. The selected template already correctly makes diagrams and interface sections conditional on real need.
- Omit a required code-header link to the design. Preserve traceability through project-relative links and the target project's source documentation convention instead.

## Conclusion

Retire Document New Design as a standalone distributed procedure. Its durable intent is already covered more completely by development-methodology routing, create-module-design, create-high-level-design, the methodology templates, and the artifact-specific review path. Implement the two narrow template refinements for context diagrams and test seams; consider optional material-decision recording only if repeated real designs demonstrate the need. No new skill, agent, or fixed universal procedure is recommended.
