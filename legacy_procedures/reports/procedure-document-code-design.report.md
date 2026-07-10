# Module Design Documentation Procedure Migration Report

## Source

Source procedure: [procedure-document-code-design.md](../procedure-document-code-design.md)

## Purpose And Scope

The procedure defines a comprehensive, source-informed design document for one code module. Its durable purpose is to make a module's responsibility, runtime relationships, contracts, state, rules, interfaces, failures, and verification understandable before implementation or maintenance work proceeds.

This is now the core purpose of the module-design artifact route. The legacy procedure should not remain as a parallel document format: it lacks the current shared page contract and hard-codes a repository-specific location and filename.

## Durable Guidance Worth Keeping

- Begin from the actual module, related designs, callers, dependencies, contracts, configuration, and tests rather than inventing design behavior.
- Give each module design one bounded responsibility and flag an oversized module as a possible decomposition concern rather than silently documenting unrelated work together.
- Explain why direct callers and dependencies exist, not only that they exist.
- Document public contracts, authoritative and derived state, processing and error paths, invariants, configuration, external interfaces, and verification at the module's actual boundary.
- Use diagrams selectively to clarify real caller/dependency relationships, state transitions, branching, retries, or error paths.
- Keep test planning connected to module responsibilities, edge cases, dependency failures, and the test seams or boundary doubles needed to exercise them.
- Record unsupported or unresolved facts as open questions.

## Mapping To The Current Catalog

| Procedure point | Destination | Coverage | Recommendation |
| --- | --- | --- | --- |
| Inspect designs, implementation, callers, imports, exports, tests, configuration, and runtime context before documenting | [documentation-reverse-engineering](../../skills/documentation-reverse-engineering/SKILL.md) | Complete. Its authority order and module-design pass require source and test inspection, callers, imports, exported contracts, configuration use, and related documents. | Retain this evidence-first discovery workflow. |
| Create one module document covering path, parent context, responsibilities, callers, dependencies, contracts, state, rules, invariants, configuration, interfaces, UI behavior, errors, and verification | [create-module-design](../../skills/create-module-design/SKILL.md) and its [module design template](../../skills/development-methodology/assets/templates/module-design-template.md) | Complete. The current artifact has all durable topic areas and also adds source authority, related evidence, open questions, and maintenance notes. | Use the template as the sole portable module-design shape. |
| Explain why callers and dependencies exist with a reasoning chain | [module design template](../../skills/development-methodology/assets/templates/module-design-template.md) | Complete. The Callers and Dependencies sections require an explanation of why each relationship exists. | Keep the explanatory requirement, but use concise source-backed prose; a fixed BECAUSE-chain syntax is optional. |
| Describe classes, types, functions, inputs, outputs, side effects, and failure behavior | [create-module-design](../../skills/create-module-design/SKILL.md) and [review-module-design](../../skills/review-module-design/SKILL.md) | Complete. Public Contracts, Internal Data And State, Processing Rules, and Error Handling replace the legacy class-by-class inventory with a boundary-focused contract. | Keep function or type detail only where it is part of the public contract or necessary to explain a complex processing rule. |
| Add flow, state, and error diagrams when relationships are complex | [module design template](../../skills/development-methodology/assets/templates/module-design-template.md), [documentation-page-verifier](../../skills/documentation-page-verifier/SKILL.md) | Partial. The Processing Diagram supports branches, retries, errors, and state transitions, and the verifier permits dependency diagrams, but the module template has no explicit conditional caller/dependency context-diagram prompt. | Add a narrow optional context-diagram instruction to the module template and creation skill. |
| Capture rules that must always hold | [module design template](../../skills/development-methodology/assets/templates/module-design-template.md) and [review-module-design](../../skills/review-module-design/SKILL.md) | Complete. Both include invariants as a required module-design concern. | Preserve source-backed invariants; categorize only when it improves actionability. |
| Plan tests, edge cases, mocks, and dependency failures | [module design template](../../skills/development-methodology/assets/templates/module-design-template.md), [Jest](../../skills/jest/SKILL.md), and [Vitest](../../skills/vitest/SKILL.md) | Partial. Verification covers test layers, edge cases, invalid input, dependency failures, persistence, and user-visible behavior; Jest and Vitest supply boundary-mock guidance. The module template does not expressly ask authors to identify critical test seams or doubles. | Add that small prompt to Verification, while keeping framework-specific mock mechanics in test skills. |
| Verify the document is complete, bounded, source-backed, and reviewable | [review-module-design](../../skills/review-module-design/SKILL.md), its [checklist](../../skills/review-module-design/references/review-checklist-module-design.md), and [Artifact Review Agent](../../agents/roles/development-use/artifact-review-agent.role.yaml) | Complete. The review route requires evidence, a completed checklist, and shared verification. | No new agent is needed. |

## Coverage Assessment

The current catalog already preserves the procedure's substantive module-documentation model, in a stronger form: the module-design template defines the technical content, documentation-reverse-engineering establishes source authority, and the review route makes evidence and completeness checkable. The legacy pseudo-code format, fixed location, and fill-every-section rule should not drive a new skill.

Two small omissions remain. First, complex caller and dependency topology may be clearer as a module context diagram rather than a processing diagram. Second, module verification should name necessary test seams or boundary doubles without importing framework-specific mocking policy into design documentation.

## Precise Suggested Additions

Add the following conditional instruction to the Processing Diagram area of the module-design template and to the diagram guidance in create-module-design:

> Add a module context diagram when direct callers, dependencies, or owned external interfaces form a relationship set that is difficult to inspect in prose. Show only real direct relationships, label important contracts or handoffs, and keep processing detail in Processing Rules.

Add the following sentence to the Verification section of the module-design template:

> Identify the test seams, fixtures, or boundary doubles needed for important scenarios, and link the applicable test-framework guidance when one exists.

These are template and creation-skill refinements. They do not require a new skill, agent, or specialized diagram tool.

## Guidance To Omit Or Narrow

- Omit the fixed design/modules location and module-file-name-design.md filename. Target repositories own their documentation placement and naming.
- Omit deleting an existing document before rewriting it. Preserve useful source-backed material, replace only what evidence invalidates, and use version control for history.
- Omit the universal requirement to complete every section. The current route correctly removes configuration, external-interface, or UI sections when genuinely inapplicable.
- Narrow the greater-than-300-lines threshold. Size can prompt a decomposition review, but responsibility, cohesion, change independence, and testability—not a universal line count—should determine a split.
- Omit mandatory pseudocode for every function and its prescribed PROCEDURE syntax. Use source-backed processing rules or pseudocode only where complex control flow cannot be understood from contracts and prose.
- Omit exhaustive data-member and member-function lists for every class or type. Document owned state and public contracts; leave private implementation inventory to source navigation unless it clarifies behavior.
- Omit separate API-call documentation for every call as a mandatory module section. External Interfaces already owns direct request, response, and error shapes when relevant.
- Narrow mandatory future-evolution speculation. Record a concrete open question, risk, decision, or maintenance trigger instead of guessing how a module may evolve.
- Omit BECAUSE-chain formatting as a universal syntax rule. Preserve the underlying causal explanation, and use structured-design only when that explicit format is selected for the artifact.

## Conclusion

Retire this procedure as an independent format and route module documentation through create-module-design, documentation-reverse-engineering, and review-module-design. Add the two small conditional prompts for context diagrams and test seams. No new skill or agent is warranted; the migration is an improvement to the existing module-design template and its creation guidance.
