# Migration Review: Generate Trading Workflow Integration Tests

## Source

The [legacy procedure](../procedure-gen-workflow-int-test.md) assigns an AI
assistant to implement 60 integration tests for one Chrome-extension trading
workflow. It requires source and test-plan discovery, ordered incremental TDD,
fixtures and mocks, narrow test execution, repair of failures, coverage checks,
and a detailed status document.

The domain, test count, paths, section numbering, and status-file format are
specific to the former product. This review assesses the reusable execution
discipline against the live skill catalog and roles.

## Durable Guidance Worth Keeping

- Read the authoritative scenario plan, detailed specifications, target code,
  types, existing tests, runner configuration, fixtures, and project guidance
  before adding tests.
- Turn each scenario into an independently understandable test with an explicit
  start state, controlled boundary behavior, and observable expected outcome.
- Use readable, purposeful fixtures and mocks that preserve the behavior the
  scenario depends on. Keep the system's own business logic real whenever it
  can be exercised reliably.
- Work incrementally: add a focused test or coherent scenario group, run the
  narrowest relevant test command, diagnose failures, and only then advance.
- Treat a failing test as active implementation work until the cause is
  understood. Do not record a scenario as complete merely because the test was
  written.
- Run proportionate coverage and broader verification as a test area matures;
  record executed commands, results, skipped checks, and genuine blockers.
- Preserve recoverable progress and findings in the target repository's
  documented tracking mechanism when the work spans many scenarios or agents.

## Mapping And Coverage

| Legacy point | Live destination | Coverage | Recommendation |
| --- | --- | --- | --- |
| Read the plan, detailed test specifications, workflow implementation, and type definitions before starting | [careful-coding](../../skills/careful-coding/SKILL.md); Coding Agent | Partial | Add a portable test-authoring preflight to the runner skills: inspect project guidance, the scenario contract or plan when present, existing tests, fixtures, helpers, and runner configuration before creating test structure. |
| Implement all named scenarios with fixtures and mocks | [Jest](../../skills/jest/SKILL.md); [Vitest](../../skills/vitest/SKILL.md) | Partial | Preserve readable fixtures and boundary-oriented mocks, but add integration-scenario guidance that requires explicit starting state and assertions of the specified observable transition or outcome. |
| Begin with a named initial test and follow the status document's strict sequence | Project-local AGENTS.md, accepted test plan, or backlog item | Not portable | Retain ordered delivery only where scenarios genuinely depend on prior work. The global skills should not prescribe a scenario number, test path, or mandatory serial ordering. |
| Write a test, run the focused command, fix failures, and advance only after it passes | Jest; Vitest; [QA And Verification Agent](../../agents/roles/development-use/qa-and-verification-agent.role.yaml) | Complete | Keep focused-first verification and failure ownership. The current skills appropriately select the runner from the target repository rather than assuming npm test. |
| Update a status table with exact implementation and fix details after each test | [manage-backlog](../../skills/manage-backlog/SKILL.md) when a repository uses its backlog; project-local tracking otherwise | Partial | Preserve durable completion, verification, and blocker evidence for long-running suites, but do not require a per-test table or a particular filename. |
| Run coverage for major test sections | Jest; Vitest; QA And Verification Agent | Partial | Retain proportionate coverage review. State that coverage is evidence to interpret against scenario risk and gaps, not a universal per-section gate. |
| Split a test file after ten tests | Project-local test conventions | Not portable | Omit the fixed threshold. Split files when scenario cohesion, failure diagnosis, or runner performance benefits from it. |
| Keep tests moving immediately through the predefined 60-case campaign | Coding Agent; QA And Verification Agent; Manage Backlog | Partial | Preserve clear work boundaries and recovery evidence. Dispatch granularity, parallelism, and stopping points should follow dependencies, shared-state safety, and repository conventions. |

## Recommendations

Improve Jest and Vitest with the same short, runner-neutral integration-scenario
workflow. It should connect the existing advice on observable contracts,
readable fixtures, boundary mocks, failure modes, and focused verification into
one explicit path for integration work: inspect scenario evidence first, make
state and controlled dependencies explicit, reset stateful dependencies, and
assert the resulting contract or state transition including a relevant negative
path.

Add a narrow QA And Verification Agent reporting expectation for integration
work: its evidence should identify the scenario boundary, controlled external
dependency or time source when applicable, asserted outcome, relevant negative
case, and any blocked environment condition. This strengthens the agent's
existing coverage and skipped-check contract without creating another test role.

Use Manage Backlog only when the owning repository has adopted that work model.
For a large, ordered test campaign it can preserve claims, completion evidence,
and recovery state, but a distributed test skill must not require its folder
taxonomy or make a status document a prerequisite for ordinary test changes.

No dedicated workflow-integration-test skill, trading skill, or agent
is justified. The durable concerns are test-runner discipline and verification,
which already belong to Jest, Vitest, Coding Agent, and QA And Verification
Agent.

## Exact Suggested Additions

Add the following Integration scenarios section to both Jest and Vitest after
Guidance, adapting only runner-specific examples where necessary:

> Before adding an integration test, inspect repository guidance, the relevant
> scenario contract or test plan when one exists, existing fixtures and helpers,
> adjacent tests, and the runner configuration. Establish required starting
> state explicitly. Control external or stateful dependencies through
> project-approved facilities and reset or restore them so scenarios do not
> depend on execution order. Use readable fixtures and mock only unreliable
> external boundaries while preserving the behavior the scenario needs. Assert
> the observable contract or state transition after important simulated events,
> including the relevant failure or edge path. Use names and arrangement to
> explain routine tests; comment only non-obvious timing, setup, or domain
> constraints.

Append this sentence to the QA And Verification Agent instructions field:

> For integration tests, report the scenario boundary, any controlled external
> dependency or time source, the asserted outcome, the relevant negative path,
> and an explicit reason for any unavailable environment check.

## Guidance To Omit Or Keep Project-Local

- The CIBC Driver Chrome Extension, trading decisions, stock prices, buy and
  sell conditions, and all other product-domain behavior.
- The required total of 60 cases; fixed scenario identifiers such as 1.1.1;
  mandated first test; and a strict global execution order.
- The former paths under design, src, and test, including the named status
  document and its table columns.
- The npm test command, a specific JavaScript test-runner API, test-file naming,
  and the ten-tests-per-file limit.
- Any specific mock schema, market-event timing model, fixture implementation,
  coverage target, or failure-count reporting convention.

## Conclusion

Retire the procedure as a standalone portable workflow. Keep its evidence-led
scenario selection, realistic but bounded fixtures, incremental TDD loop,
failure ownership, layered verification, and recoverable progress tracking by
making small integration-scenario additions to Jest and Vitest and a focused
QA reporting addition. Leave test inventory, ordering, tracking format, and
trading behavior with the repository that owns them.
