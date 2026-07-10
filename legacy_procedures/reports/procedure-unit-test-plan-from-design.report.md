# Migration Report: Unit Test Plan From Design

## Source

- [Legacy procedure](../procedure-unit-test-plan-from-design.md)

## Durable Guidance Worth Keeping

- Derive the test plan from the design's stated responsibilities, public contracts, processing rules, invariants, configuration, external interfaces, UI behavior, and error handling before implementation exists.
- For each testable behavior, specify a scenario name, purpose, activating condition, concrete inputs, external-boundary setup, expected observable behavior, expected result or state change, and assertions.
- Maintain a traceability map from design requirements, business rules, decisions, and error paths to planned tests. Expose uncovered or untestable items instead of implying complete coverage.
- Treat mocks as explicit contracts: name the external dependency, the response or side effect needed, expected calls, and the assertion that proves the module's observable behavior.
- Cover meaningful decision outcomes, input and state variants, dependency failures, persistence failures, and user-visible behavior when the design says they apply.
- Keep test plans executable in intent but free of test-framework code. The plan should guide implementation without duplicating it.
- Tie every scenario to a concise design-supported reason. Use the repository's structured-design format when that format is required; otherwise use direct rationale rather than mandatory repeated five-why chains.

## Mapping And Coverage

| Procedure point | Destination skill(s) or agent(s) | Coverage | Recommendation |
| --- | --- | --- | --- |
| Read a design and identify module functionality, owned behavior, dependencies, inputs, outputs, state, and optional behavior | Create Module Design; Create High-Level Design | Partial | The design templates provide the source sections, but no skill translates them into a test-plan artifact. Add a design-to-test-plan workflow. |
| Create concrete scenario records with purpose, activating condition, inputs, mocks, behavior, outputs, and assertions | Jest; Vitest | Partial | Both skills mention test design, mocks, and fixtures, but neither defines a framework-neutral plan format before code is written. |
| Define mock calls, returns, side effects, and call verification | Jest; Vitest | Partial | Retain explicit mock contracts, but add the boundary rule that mocks must not substitute for the module's own decision logic. |
| Cover both outcomes of conditional decisions and relevant combinations | Jest; Vitest; QA And Verification Agent | Partial | Add decision-coverage guidance that selects meaningful combinations proportionate to risk and state space, rather than promising exhaustive combinations. |
| Cover UI, integrations, persistence, recovery, errors, timing, network, and storage when applicable | Create Module Design; Create High-Level Design; Jest; Vitest | Partial | The design templates identify these concerns and test skills note failures, but applicability and planned coverage are not recorded in one place. |
| Produce a coverage map from pseudocode paths to scenarios | None | Missing | Replace pseudocode-line coverage with a design-item coverage matrix that maps stable design headings, identifiers, rules, and decision descriptions to scenarios. |
| Do not embed JavaScript test code in the plan | None | Missing | Include this output boundary in a dedicated test-plan skill. |
| Place plans in a test hierarchy and use a fixed module-name.plan.md name | Project-local guidance | Omit | Derive location and names from the target repository's conventions; a portable skill must not prescribe a source-tree layout. |
| Never mock Tracer methods or tracer.js | Project-local guidance | Omit | The Tracer class and file are former-project details. Preserve only the general observable-behavior and external-boundary mock discipline. |
| Require five nested BECAUSE statements for every significant choice | Structured Design | Contradicted | Retain concise evidence-linked rationale. Do not mandate a fixed depth; structured-design already requires each BECAUSE to justify its immediate parent assertion. |
| Require every pseudocode path to have a test | Jest; Vitest; QA And Verification Agent | Partial | Preserve the intent as traceable decision, rule, and failure coverage. Do not require exhaustive paths where combinations are unbounded or belong to integration or end-to-end tests. |

## Recommendations

Create a dedicated, framework-neutral Create Unit Test Plan skill. It fills a distinct artifact-creation gap: turning a design into an auditable plan before code and a particular runner exist. Keep Jest and Vitest focused on framework-specific implementation, execution, fixtures, and diagnosis.

Add the skill to Development Methodology's artifact route table as the test-planning route, positioned after a design is available and before Coding Agent implements tests. A small test-plan template asset is warranted because the output fields and coverage matrix should stay consistent across repositories.

Update existing roles rather than adding a dedicated agent:

- Coding Agent should use an approved plan as an input, implement the applicable scenarios, and report plan items it cannot automate safely.
- QA And Verification Agent should check plan-to-suite coverage for non-trivial changes, distinguishing covered, missing, obsolete, blocked, and intentionally higher-level scenarios.
- Code Review Agent should verify that tests prove the design rule or observable contract, not only mock invocation or implementation detail.

## Omits And Project-Specific Guidance

- The test folder hierarchy, src mirroring rule, and fixed module-name.plan.md filename.
- The Tracer and tracer.js exceptions.
- A required object-oriented style; test style must follow the target language, framework, and repository conventions.
- Mandatory UI, persistence, network, storage, race-condition, and timing scenarios when the design has no such behavior.
- Mandatory five-why depth and its formatting instructions.
- Blanket every-path and every-combination coverage. These can create infeasible plans and obscure risk-based testing.

## Exact Additions

### Create Unit Test Plan Skill

Create skills/create-unit-test-plan/SKILL.md with this scope and workflow:

> Use when creating or substantially revising a unit test plan from a module design, high-level design, functional specification, or source-backed behavioral contract. Produce a framework-neutral markdown plan, not test code.
>
> Read the authoritative design and repository test conventions. Extract testable responsibilities, contracts, rules, invariants, decision outcomes, state transitions, dependency boundaries, errors, persistence, and user-visible behavior. Mark every concern as unit-testable, integration-owned, end-to-end-owned, deferred, or not applicable.
>
> For each applicable unit scenario, record: identifier, synopsis, design source, purpose, activating condition, inputs and starting state, boundary mocks or fakes, expected observable behavior, expected result or state change, and assertions. Use concrete values where the design supports them; record an open question rather than inventing values.
>
> Mock only external boundaries needed to control the scenario. Specify their expected calls, returns, side effects, and verification. Do not mock the unit's own decision logic or assert mocks in place of observable behavior.
>
> Add a coverage matrix mapping each design rule, contract, decision outcome, and failure path to one or more scenario identifiers. Mark gaps, higher-level coverage, and not-applicable items explicitly. Select conditional combinations by risk, equivalence classes, boundaries, and state transitions; do not claim exhaustive path coverage unless the finite paths are enumerated and justified.
>
> Keep the plan free of runner-specific test code. Use the target repository's plan location and naming conventions when they exist; otherwise ask before creating a file.

Add a template asset with sections for Scope And Sources, Testable Behavior Inventory, Boundary Mock Contracts, Scenario Records, Coverage Matrix, Open Questions, and Implementation Handoff.

### Development Methodology

Add Create Unit Test Plan to Required Companion Skills, Document Type Selection, Artifact Creation Routes, and Template Assets. Route it when a user asks for an implementation-independent unit-test plan based on a design or behavioral artifact; route to Jest or Vitest only when authoring, running, or diagnosing runner-specific tests.

### Jest And Vitest

Add this shared conditional guidance to both skills:

> When an approved unit test plan exists, read its scenario and coverage matrix before writing tests. Implement applicable unit scenarios at the smallest useful boundary, preserve its observable assertions, and report scenarios that are obsolete, blocked, or belong to integration or end-to-end coverage. Keep framework-specific fixtures and mocks aligned with the plan's declared external boundaries.

## Conclusion

Keep the procedure's design-derived scenario detail, explicit boundary mock contracts, applicability-aware failure coverage, and traceability matrix. The current catalog has strong design inputs and runner-specific test skills, but it lacks the durable artifact workflow between them. Add one small framework-neutral Create Unit Test Plan skill and route it through existing Coding, QA, and Code Review roles. Omit former-project paths, Tracer rules, mandated five-why depth, and unbounded exhaustive-path promises.
