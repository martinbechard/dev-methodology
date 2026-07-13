# Migration Report: Create Integration Tests for a Trading Workflow

## Source

- [Legacy procedure](../procedure-create-integration-tests-for-trading-workflow.md)

## Durable Guidance Worth Keeping

- Start from the applicable test plan, scenario specification, contract, and repository instructions. Inspect existing tests, fixtures, helpers, and configuration before inventing a parallel test pattern.
- Use the repository's established test location and conventions when they exist. Create missing test structure only when the project documentation or adjacent tests establish the intended shape.
- Build reusable fixtures and helpers around an observable scenario. Keep fixtures legible, configuration purposeful, and simulation behavior representative of the real boundary being exercised.
- Make integration scenarios independent: establish needed state explicitly, reset shared state and external resources through the runner-appropriate lifecycle, and assert the observable state transition, error path, or contract outcome.
- Cover the named success path, relevant failure paths, and meaningful edge cases. Match assertions to the scenario specification rather than merely checking that execution completes.
- Run the narrowest affected test first, then select broader tests and build or type checks according to the changed boundary and risk. Distinguish test failures from unavailable environments or dependencies.
- Explain only non-obvious scenario setup, timing, or assertions; readable test names and structure should carry the routine documentation burden.

## Mapping and Coverage

| Procedure point | Best current destination | Coverage | Migration recommendation |
| --- | --- | --- | --- |
| Read test plan, specifications, fixtures, configuration, and adjacent patterns before editing | Careful Coding; Coding Agent; Development Methodology templates | Partial | Add an explicit test-authoring preflight to runner skills: inspect the repository's test plan, scenario contract, existing fixtures, and commands before creating test structure. |
| Follow existing directories and complete existing test files | Coding Agent; project-local AGENTS.md or PROJECT.yaml | Partial | Keep as a project-local routing rule. Distributed skills should say to follow documented and adjacent-test conventions, not prescribe directory names. |
| Create fixtures, helpers, and realistic simulations | Jest; Vitest | Partial | Add scenario-oriented integration-fixture guidance to both runner skills. Preserve boundary mocks and readable fixtures; require simulation choices to be justified by the contract being tested. |
| Hierarchical test structure and setup or teardown | Jest; Vitest | Partial | Retain the intent: organize scenarios so failures are local and reset shared resources in lifecycle hooks. Do not mandate Jest syntax globally. |
| Mocks that reflect real component behavior and controlled time-based events | Jest; Vitest; Playwright when the workflow is browser-visible | Partial | Add runner-neutral language on deterministic clocks, queues, and external-boundary doubles. Require state or outcome assertions after simulated events. |
| Exact scenario expectations, state assertions, failures, and edge cases | Jest; Vitest; QA And Verification Agent | Complete | Existing guidance covers observable contracts, failure modes, workflow state, and coverage notes. No new agent or skill is necessary for this point. |
| Test purpose and complex-scenario comments | Jest; Vitest; Careful Coding | Partial | State that tests should be self-explanatory by name and arrangement; comments are for non-obvious timing, setup, or business constraints. Do not require JSDoc for every test. |
| Isolation, readability, and maintainability | Jest; Vitest; Coding Agent | Partial | Add explicit integration-test isolation language, including cleanup of stateful dependencies and prevention of order dependence. |
| Targeted then proportionate broader verification | Jest; Vitest; QA And Verification Agent | Complete | The current runner skills and QA role already specify this sequence and skipped-check reporting. |

## Recommendations

1. Improve Jest and Vitest rather than create a trading-integration-test skill or a dedicated integration-test agent. The durable guidance is runner-oriented and belongs with the existing test skills; QA And Verification Agent already owns integration-test execution and coverage reporting.
2. Add a small shared integration-scenario subsection to Jest and Vitest, with nearly identical framework-neutral wording. Keep runner API examples, fake-timer mechanics, and database or service setup in project-local guidance or companion stack skills.
3. Add one QA And Verification Agent instruction that asks it to confirm the scenario-to-evidence relationship for integration tests: setup boundary, simulated dependency or clock, asserted state transition, and relevant negative path.
4. Treat a project test plan as optional evidence, not a distributed prerequisite. Non-trivial projects can record scenario coverage in a test plan, functional specification, high-level design, module design, or issue; smaller changes may use a focused test description.

## Omit or Keep Project-Local

- The trading workflow as the target domain, including buy triggers, price patterns, market events, and the legacy numbered test directories.
- The fixed document names and former repository paths, including design/testing/trading-workflow-integration-test-plan.md and its referenced specifications.
- Any project-specific fixture schema, mock implementation, timing model, and trading state machine. These require the actual product contract and should live with that project.
- Jest describe and it syntax as a cross-runner instruction; Vitest and project-local runners may differ.
- A blanket JSDoc requirement for test files. It adds noise when well-named scenarios and readable fixtures explain the test.
- The instruction to update the legacy procedure whenever patterns change. In the current model, reusable changes belong in the relevant skill only after they have proved portable; product-specific patterns belong in that repository's documentation.

## Exact Suggested Additions

### Jest and Vitest

Add this section after Guidance in both skills:

## Integration scenarios

- Before adding an integration test, inspect the relevant scenario contract or test plan, repository guidance, existing fixtures, helpers, and adjacent tests.
- Make required starting state explicit. Use readable fixtures and mock only external boundaries that cannot be exercised reliably; the simulated boundary must preserve the behavior the scenario depends on.
- Control time, queues, network responses, files, connections, and other stateful dependencies through the runner or project-approved facilities. Reset or restore them in the appropriate lifecycle hooks so scenarios do not depend on execution order.
- Assert the observable transition or contract outcome after each important simulated event. Cover the intended path and the relevant failure or edge path named by the scenario.
- Keep routine tests self-explanatory through names and arrangement. Comment only non-obvious timing, setup, or domain constraints.

### QA And Verification Agent

Append this sentence to the instructions field:

For integration tests, confirm that the reported evidence identifies the scenario boundary, controlled dependency or time source when relevant, asserted outcome, and relevant negative path.

## Conclusion

The procedure's useful core is not trading-specific: evidence-led scenario selection, representative fixtures and simulations, explicit isolation, state-transition assertions, and layered verification. Jest, Vitest, and QA And Verification Agent already cover most of it, but the runner skills do not expressly connect integration scenarios to test-plan evidence, deterministic stateful dependencies, and order-independent cleanup. Add the concise integration-scenario subsection to those two skills and the QA reporting sentence. Do not create a new skill or agent, and keep all trading models, timing rules, and test-tree conventions within the owning product repository.
