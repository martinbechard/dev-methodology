# Migration Report: Unit Test Plan From Existing Code

## Source

- [Legacy procedure](../procedure-unit-test-plan-from-code.md)

## Purpose And Scope

The procedure derives a detailed unit-test plan from an existing module. It inventories behavior and dependencies, identifies paths and edge cases, defines boundary mocks, compares implemented rules with design evidence, and produces scenarios plus a coverage map. It also embeds former trading-product requirements and a tracer-specific mocking prohibition.

## Worthwhile Durable Guidance

- Start from the actual source module and record its public and meaningful internal behavior: inputs, outputs, state changes, branches, iteration, dependencies, error paths, and business rules.
- Treat design documents and code as distinct evidence. When their behavior conflicts, document the discrepancy and seek a decision before encoding uncertain behavior in a test plan.
- Derive scenarios from meaningful behavior paths, including dependency outcomes and failure paths, rather than testing line execution for its own sake.
- Define mocks only at external boundaries. State the dependency contract, controlled return value or side effect, and interaction assertion needed for each scenario.
- Specify concrete inputs, expected observable behavior, and assertions; include empty, boundary, invalid, timing, persistence, and network cases when the module can exhibit them.
- Use a coverage map that connects scenarios to responsibilities, decision outcomes, and important failure modes. It should expose uncovered behavior instead of claiming blanket line coverage.
- Keep plans implementation-neutral: they describe tests to write and do not embed test code.

## Mapping And Coverage

| Procedure point | Destination skill(s) or agent(s) | Coverage | Recommendation |
| --- | --- | --- | --- |
| Inspect functions, branches, loops, dependencies, and business rules | Jest; Vitest; Coding Agent | Partial | Add a concise code-to-plan analysis workflow that records observable contracts, state transitions, decision outcomes, boundary dependencies, and failures. Do not require every private implementation detail to appear in the plan. |
| Reconcile code behavior with design documents and pause for a discrepancy decision | Careful Coding; Coding Agent; QA And Verification Agent | Partial | Careful Coding already requires explicit assumptions. Add a testing-specific rule: record code-versus-design disagreement as an open decision and do not select a behavior silently. |
| Identify every path and ensure every line is covered | Jest; Vitest; QA And Verification Agent | Partial / contradicted | Retain systematic path analysis but replace a universal line-coverage requirement with meaningful behavioral, decision-outcome, failure-mode, and risk-based coverage. Line coverage is a useful signal where configured, not a plan acceptance criterion. |
| Define dependency mocks, arguments, returns, side effects, and calls | Jest; Vitest | Partial | Expand both test skills with a brief mock-contract checklist. Their existing boundary-mocking guidance covers the central principle but not the plan-level details. |
| Create scenario records with purpose, paths, inputs, mocks, outputs, and assertions | New conditional test-planning capability shared by Jest and Vitest; Coding Agent | Missing | Create a small framework-neutral Test Planning skill, or a shared reference invoked by both runner skills, for producing and reviewing test-plan artifacts. |
| Cover null, empty, boundary, exception, race, network, and storage cases | Jest; Vitest; QA And Verification Agent | Partial | Add applicability-based edge-case selection. These cases should be considered from real module semantics, not mandated for modules with no such boundary. |
| Produce a plan with module scope, functions, mocks, scenarios, and coverage map | New Test Planning skill; QA And Verification Agent | Missing | The catalog has no dedicated plan-authoring workflow or plan review surface. Add one only if test plans are a durable artifact in supported target repositories. |
| Never mock Tracer and ignore tracer.js | None | Omit | This is a former product-specific dependency rule. Preserve it only in that product's local guidance or a domain skill. |
| Trading velocity, entry and exit, UI, persistence scenarios | None, unless a reusable trading domain bundle is later created | Omit | These are application-specific behavior examples, not portable test-planning rules. |

## Gaps And Recommended Additions

The existing Jest and Vitest skills are intentionally concise execution guides. They lack a reusable method for authoring a test-plan document from existing code, evidence-based disagreement handling, scenario-to-behavior mapping, and review of plan completeness.

Create a framework-neutral Test Planning skill only if the bundle intends to support repositories that keep test plans as maintained artifacts. Its trigger should cover requests to generate, review, or reconcile a unit-test plan from existing code or design. Keep runner-specific execution, mocking APIs, and command selection in Jest and Vitest.

If test plans are not a first-class bundle artifact, do not add a skill. Instead, add the narrow mock-contract and behavior-coverage guidance below to Jest and Vitest, and leave plan layout to repository-local procedures.

No new agent role is warranted. The Coding Agent can derive plans or implement them, the QA And Verification Agent can assess completeness and execution evidence, and the Code Review Agent can inspect whether tests prove behavior rather than mock choreography.

## Exact Suggested Additions

### Proposed New Skill: Test Planning

Add a framework-neutral skill with this core guidance:

> When asked to create or review a unit-test plan from code, read the module, its public contracts, callers, existing tests, and applicable design evidence. Record observable behavior, meaningful decision outcomes, state transitions, dependency boundaries, and failure paths.
>
> When code and authoritative design disagree, record the discrepancy, its affected scenarios, and the decision needed. Do not silently choose an unapproved interpretation.
>
> For each applicable scenario, state its purpose, setup and inputs, boundary mocks with their required contract, expected observable outcome, and assertions. Map scenarios to responsibilities, decision outcomes, and failure modes; mark uncovered or blocked behavior explicitly.
>
> Consider empty, boundary, invalid, timing, network, storage, and recovery cases when the module has that behavior. Do not add inapplicable cases or require line coverage as a substitute for behavioral coverage.
>
> Keep the plan free of framework test code unless the requesting repository explicitly requires executable examples.

### Jest And Vitest

Add the following shared guidance under Guidance:

> When planning tests, map each mock to an external boundary and specify the controlled return value, side effect, and interaction assertion required by the scenario. Do not mock the behavior the unit itself owns.
>
> Select scenarios from observable behavior, meaningful branch outcomes, state transitions, and realistic failure modes. Consider boundary and empty inputs only when the module contract makes them relevant, and report material uncovered behavior explicitly.

### Coding Agent And QA And Verification Agent

- Coding Agent: when an approved test plan exists, map every applicable scenario to a focused test or explicitly report why it is obsolete, blocked, or unsuitable for automation.
- QA And Verification Agent: for non-trivial planned testing, review the scenario map against source and design evidence, distinguish execution coverage from untested behavior, and report any unresolved discrepancy.

## Obsolete Or Project-Specific Guidance To Omit

- The test-directory mirroring convention and fixed plan filename. These belong in target-repository conventions.
- The universal every-line coverage requirement. It encourages tests coupled to incidental implementation and can leave important behavior untested.
- The Tracer rule and tracer.js exclusion. These are specific to the legacy trading application.
- The Quote Watch and Trading Workflow scenario catalogue. Preserve it only as local domain test guidance if the application remains maintained.
- Fixed example symbols, prices, exact history length, and output shape. They are illustrative product data, not a portable pattern.
- The claim that object-oriented testing practices are universally required. The bundle supports several paradigms and should instead require clear setup, exercise, and observable assertions.

## Conclusion

Keep the procedure's strongest ideas: source-and-design evidence, explicit discrepancy handling, boundary-aware mocks, concrete scenarios, and an honest coverage map. Current Jest and Vitest guidance partially covers behavior-first testing and boundary mocking, but neither supports durable test-plan authoring. Add a small framework-neutral Test Planning skill only where test plans are maintained artifacts; otherwise make the two shared Jest/Vitest additions and retain plan format, test location, and product-domain detail locally.
