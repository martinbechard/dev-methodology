# Migration Report: Mocking Rules

## Source

- [Legacy procedure](../procedure-mocking-rules.md)

## Purpose and Scope

The procedure sets rules for mocks in Jest unit and integration tests, including interface fidelity, complex test doubles, global setup, and control of time. Its strongest idea is that test doubles must preserve the purpose of the test: isolate a unit at an external boundary, but retain real collaboration in an integration scenario. Several rules are tied to a former trading application and some Jest claims are over-broad or inaccurate.

## Worthwhile Durable Guidance

- Use documented, supported test-runner APIs and avoid depending on undocumented implementation behavior.
- Give every test double a clear purpose. Model the observable contract needed by the scenario, including relevant success and failure behavior; do not invent behavior that the real dependency does not promise.
- In a unit test, isolate uncontrolled or collaborating dependencies at the smallest useful boundary. In an integration test, exercise the real components that form the integrated flow and replace only external, uncontrollable, costly, or deliberately out-of-scope boundaries.
- Do not replace an integrated component merely to count calls. Observe the real implementation with a spy when that preserves the scenario; use a mock or stub when the test must force a result, failure, or boundary condition.
- Keep test-specific doubles local and explicit. Do not create hidden global mocks of application modules that make an individual suite's dependencies unclear.
- Treat a reusable, stateful, or behavior-rich fake as production test infrastructure: keep its supported contract explicit and test it independently.
- Choose the clock-control technique from the behavior being tested, restore it after the test, and avoid tests whose timing or cleanup leaks into other tests.

## Mapping and Coverage

| Procedure point | Destination skill(s) or agent(s) | Coverage | Recommendation |
| --- | --- | --- | --- |
| Supported Jest mocking APIs; no undocumented internals | Jest | Partial | Add a concise instruction to use documented public runner APIs and runner-appropriate restoration hooks. Do not ban documented mock metadata such as mock instances. |
| Mock fidelity, including error behavior | Jest; Vitest; Coding Agent | Partial | Add contract-based guidance: configure only the behavior the scenario needs, covering relevant failures without recreating the full dependency. |
| Unit-test isolation through mocks | Jest; Vitest | Partial | Retain isolation but replace the blanket requirement to mock all dependencies with a smallest-useful-boundary rule. Pure collaborators may be real when that makes the unit's behavior clearer. |
| Real internal collaboration in integration tests; external-boundary mocks only | Jest; Vitest; QA And Verification Agent | Partial | Add an explicit unit-versus-integration selection rule, including a requirement to state the reason for an exceptional internal replacement. |
| Do not mock only to spy | Jest; Vitest | Missing | Add guidance to prefer a real-instance spy for observation when it does not change required behavior. |
| Explain each integration mock | Jest; QA And Verification Agent | Missing | Require a short local reason for each non-obvious integration boundary double. Preserve the rationale, not a mandatory BECAUSE-chain comment format. |
| Complex mock implements an interface and has design, plan, and tests | Jest; Vitest; Development Methodology | Partial | Require an explicit supported contract and independent tests for reusable complex doubles. Make formal design and test-plan artifacts conditional on repository methodology and complexity. |
| Do not globally mock project modules | Jest; Vitest | Missing | Add a prohibition on hidden global application-module mocks, with test-file-local setup as the default. |
| Fake timers prohibited; real timers and Date.now spying preferred | Jest; Vitest | Contradicted | Do not preserve a blanket timer ban. Choose real time, fake time, injected clocks, or a Date spy based on the behavior and framework; restore state and flush the intended queues deliberately. |
| Never mock the former Tracer utility | None | Omit | It is an application-specific observability and infinite-loop safeguard, not a portable rule. |

## Obsolete, Incorrect, or Project-Specific Guidance to Omit

- The former Tracer path, trace-log dependency, maxWrites mechanism, and deletion penalty. A project that depends on an observability utility should document that locally.
- The absolute claim that mock.instances is an internal Jest property. Jest documents mock-function call and instance metadata, so a portable rule should distinguish documented runner APIs from private implementation details.
- The blanket instruction to mock every dependency in every unit test. It can make simple logic tests implementation-coupled and needlessly obscure real collaboration.
- A mandatory nested BECAUSE-chain comment for every integration mock. A concise local rationale is enough and should follow the repository's documentation style.
- Mandatory design documents, test plans, directories, filenames, interface names, and retrospective TDD process for every complex mock. These are methodology and repository decisions, not a universal test-runner requirement.
- The blanket ban on Jest fake timers and its claim that assistants cannot use them. Fake timers are a supported Jest facility and are appropriate for some timer-driven behavior when their semantics and cleanup are understood.
- The prescribed use of global Jest setup for external-library mocks. Global setup should remain limited to truly universal environment setup; whether a library double belongs there depends on suite scope and repository conventions.

## Precise Suggested Additions

### Jest

Add these bullets to Guidance:

- Use documented Jest APIs. Configure a double around the observable contract required by the scenario, including relevant error behavior, and restore spies, replaced properties, timers, and shared state in appropriate lifecycle hooks.
- For unit tests, isolate external effects and collaborators at the smallest useful boundary. For integration tests, keep the components under integration real; replace only uncontrollable, costly, external, or explicitly out-of-scope boundaries. State the reason for a non-obvious replacement beside the test setup.
- Do not mock a component only to observe it. Prefer a spy on the real implementation when it preserves the behavior needed by the scenario; mock or stub when the scenario must control behavior or failure.
- Keep application-module mocks local to the suite that needs them. Avoid hidden global mocks that make a suite's dependencies or behavior non-obvious.
- Give reusable, stateful, or behavior-rich test doubles an explicit supported contract and independent tests. Use formal design or test-plan artifacts when the repository methodology requires them or the double's complexity warrants them.
- Select real timers, fake timers, an injected clock, or a Date spy according to the behavior under test. Use the runner's documented queue-control semantics and always restore time-related state after the test.

### Vitest

Add these runner-neutral bullets to Guidance:

- Keep mocks at the smallest useful external or collaborator boundary. Integration scenarios should retain real components in the flow and explain any non-obvious replacement.
- Prefer spies on real behavior for observation; use a mock or stub only when the scenario must control a result, failure, or boundary condition.
- Restore spies, clock controls, and shared state in lifecycle hooks. Treat reusable complex test doubles as supported test infrastructure with an explicit contract and independent tests.

### Agent Roles

- Coding Agent: identify whether the requested coverage is unit or integration coverage, name each non-obvious boundary double and its reason, and keep reusable complex doubles contract-tested.
- QA And Verification Agent: review whether mocks preserve the intended test boundary, whether integration tests retain the actual collaboration under test, and whether timer control is restored and deterministic.
- Code Review Agent: flag a mock that replaces behavior the test claims to verify, a global application-module mock without clear scope, or a complex fake without an independently verified contract.

No dedicated mocking skill or agent is warranted. Mock selection is a compact concern within the existing Jest and Vitest skills and implementation, QA, and review roles.

## Conclusion

Keep the procedure's distinction between unit isolation and integration realism, contract-aware doubles, explicit local mock rationale, spy-before-replacement preference, and disciplined complex test infrastructure. The live Jest and Vitest skills already establish boundary-oriented testing, but they need more precise mock-selection, local-scope, complex-double, and time-control guidance. Do not migrate project-specific Tracer rules, fixed file locations, mandatory commentary syntax, or the unsupported blanket ban on fake timers.
