# Procedure: Mocking Rules

This document outlines the rules for creating and using mocks in unit and integration tests, derived primarily from refactoring-plan-gemini.md. Correct mocking is crucial for effective testing.

## 1. General Mocking Principles

- **RULE:** Use **ONLY** official Jest mocking techniques documented in the Jest documentation (e.g., jest.mock(), jest.fn(), jest.spyOn(), mockResolvedValueOnce, mockImplementation).

    - **BECAUSE:** Relying on the public API ensures tests are stable, maintainable, and understandable across Jest versions.

        - **BECAUSE:** Public APIs are contractually stable (within major versions), unlike internal implementation details which can change without notice.

            - **BECAUSE:** Tests written against stable APIs are less likely to break when the testing framework is updated.

                - **BECAUSE:** Using documented features makes the tests easier for other developers (or the LLM) to understand and maintain, as they can refer to official documentation.

- **RULE:** **NEVER** attempt to access or rely on internal Jest properties or implementation details (e.g., mock.instances, properties starting with _).

    - **BECAUSE:** Internal details are not guaranteed to remain stable and can break tests unexpectedly between Jest updates, leading to brittle tests.

        - **BECAUSE:** The Jest team provides no guarantee that internal structures or properties will remain the same; they are implementation details subject to change.

            - **BECAUSE:** Tests that rely on these internals become tightly coupled to a specific Jest version and implementation, making upgrades difficult and risky.

                - **BECAUSE:** Such tests are harder to understand as they rely on undocumented behavior.

- **RULE:** When using mocks is necessary (see specific rules below), the mock **MUST** accurately reflect the interface and expected behavior (including error conditions) of the real component it replaces, as defined by the design or interface documents.

    - **BECAUSE:** Inaccurate mocks lead to misleading test results: tests might pass when the real interaction would fail, or fail when the real interaction would succeed.

        - **BECAUSE:** Tests rely on mocks to simulate the behavior of dependencies; if the simulation is wrong, the test is not accurately verifying the unit's interaction with those dependencies.

            - **BECAUSE:** This can lead to false confidence (passing tests despite underlying issues) or wasted time debugging tests that fail due to incorrect mocks rather than actual code problems.


## 2. Unit Test Mocking

- **RULE:** In unit tests, **mock ALL external dependencies** of the unit under test. This includes other classes/modules within the project, external services, APIs, file system, time (if manipulated), database interactions, etc.

    - **BECAUSE:** Unit tests must isolate the unit under test to verify its logic independently of its collaborators' behavior or state.

        - **BECAUSE:** Isolation ensures that a unit test failure points to a problem within the unit itself, not within its dependencies.

            - **BECAUSE:** This simplifies debugging by drastically narrowing down the location of the fault.

    - **BECAUSE:** Mocking ensures tests are fast, deterministic, and repeatable without relying on the availability or state of external systems.

        - **BECAUSE:** Real dependencies (like network calls or databases) can be slow, unreliable, or have changing state, making tests flaky and slow.

            - **BECAUSE:** Mocks provide instantaneous, predictable responses, allowing tests to run quickly and consistently every time.


## 3. Integration Test Mocking

- **RULE:** In integration tests, use **real instances** of the components being integrated whenever possible.

    - **BECAUSE:** The primary purpose of integration tests is to verify that multiple components work together correctly using their actual implementations, including their real interactions.

        - **BECAUSE:** Using real instances tests the actual communication paths, data transformations, and potential timing issues between components that mocks would hide.

            - **BECAUSE:** This provides higher confidence that the integrated parts of the system function correctly as a whole, catching bugs that unit tests (with mocks) cannot find.

- **RULE:** Only mock dependencies that are **truly external** to the system under test (e.g., actual 3rd party APIs, database connections) or components explicitly outside the scope of the specific integration scenario if they are difficult to control or set up for the test.

    - **BECAUSE:** Mocking should be reserved for isolating the integrated system from uncontrollable external factors or for simulating specific, hard-to-reproduce external conditions needed for the test scenario.

        - **BECAUSE:** Mocking external APIs prevents tests from making real network calls, ensuring they are fast, repeatable, and don't incur costs or rate limits.

        - **BECAUSE:** Mocking components outside the test scope might be necessary if their setup is overly complex or introduces unwanted side effects irrelevant to the specific interaction being tested.

            - **BECAUSE:** This strategic mocking maintains the focus of the integration test on the interaction between the core components under scrutiny.

- **RULE:** **AVOID** mocking internal modules that are part of the integrated flow unless absolutely necessary for controlling specific edge cases or error conditions not easily reproducible otherwise. Prioritize testing the real interactions.

    - **BECAUSE:** Over-mocking internal components defeats the purpose of integration testing, essentially turning it back into a unit test.

        - **BECAUSE:** If you mock the components you are trying to integrate, you are not testing their actual interaction, only how the primary component interacts with your mock simulation.

            - **BECAUSE:** This significantly reduces the value of the integration test, as it fails to verify the real collaborative behavior of the system components.

- **RULE:** For each jest.mock() call in an integration test file, **ADD a comment** explaining why this specific module is being mocked for this test, using a BECAUSE chain.

    - **BECAUSE:** This clarifies the test's scope, justifies deviations from the principle of using real components, and aids maintainability.

        - **BECAUSE:** It forces the test author to consider why a mock is needed and communicates this reasoning to future readers (developers or LLMs).

            - **BECAUSE:** Understanding the reason for a mock helps when debugging test failures or refactoring the test setup.

- **RULE: DO NOT USE MOCKS JUST FOR SPYING.**

    - Only use mocks (jest.mock, jest.fn) when it is **CRUCIAL** to force specific behavior (e.g., simulate an error, control return values) needed for the test scenario.

    - To observe interactions or verify calls without altering behavior, use jest.spyOn() on the **real** instance whenever possible.

    - **BECAUSE:** Using mocks solely for spying obscures actual interactions between real components, reducing the integration test's value in verifying real collaboration. jest.spyOn() allows observation without replacing the actual implementation.

        - **BECAUSE:** Mocks replace the original implementation entirely, preventing the test from verifying how the real implementation behaves, even if you only care about observing calls.

        - **BECAUSE:** jest.spyOn wraps the real method, allowing calls to be tracked while still executing the original logic, providing a more accurate test of the interaction when behavior modification isn't needed.

            - **BECAUSE:** This reinforces the principle of using real components in integration tests unless behavior modification is explicitly required for the test case.


## 4. Complex Mocks (e.g., MockTradeService)

- **RULE:** If a complex mock implementation is needed (beyond simple Jest mocks):

    1. The mock **MUST** implement the interface of the real component it replaces (e.g., MockTradeService implements ITradeService).

    2. The mock **MUST** have its own design document (design/mocks/<MockName>-design.md) detailing its configurable behaviors, states, and error simulation capabilities.

    3. The mock **MUST** have its own test plan (design/mocks/<MockName>-test-plan.md) based on its design.

    4. The mock **MUST** have its own unit test suite (test/mocks/<MockName>.test.ts) verifying it behaves as designed according to its test plan.

    5. If retrofitting, generate the design from code, create the plan, and use TDD to ensure test coverage matches the plan.


    - **BECAUSE:** Treating complex mocks as first-class components with their own design and tests ensures they are reliable, maintainable, and accurately simulate the required behavior, preventing them from becoming sources of untracked complexity or test fragility themselves.

        - **BECAUSE:** Implementing the interface ensures the mock conforms to the expected contract.

        - **BECAUSE:** Design documents make the mock's intended behavior and configuration explicit and understandable.

        - **BECAUSE:** Test plans and unit tests verify that the mock actually behaves as designed, preventing the mock itself from being a source of errors in tests that use it.

            - **BECAUSE:** A reliable, well-documented mock increases confidence in the tests that depend on it.


## 5. Forbidden Mocks

- **RULE:** **NEVER** mock the Tracer utility (src/utils/tracer.ts) or its methods (e.g., Tracer.log).

    - **BECAUSE:** Tracer provides essential runtime context for LLM troubleshooting and includes vital infinite loop detection via maxWrites. Mocking it disables these critical functions.

        - **BECAUSE:** The LLM relies on trace.log output to understand execution flow and diagnose failures; mocking Tracer removes this visibility.

        - **BECAUSE:** The maxWrites check prevents tests from hanging indefinitely in loops, which is crucial for automated test runs; mocking Tracer disables this safety net.

            - **PENALTY:**  your code will be DELETED if it is ddiscovered that Tracer is mocked. (External constraint reflecting importance).

- **RULE:** **NEVER** mock project-specific modules within the global Jest setup file (test/jest.setup.ts). Use this file only for global mocks of external libraries or environment APIs (like browser APIs if needed).

    - **BECAUSE:** Global mocks of project modules create implicit dependencies, can conflict with test-specific mocks, and make test setup harder to understand and debug. Module mocking should occur within the test file that requires it.

        - **BECAUSE:** Mocking a module globally affects all test files, even those that might need the real implementation or a different mock configuration, leading to unexpected behavior and difficult-to-trace failures.

            - **BECAUSE:** It hides the dependencies of individual test suites, making it unclear which mocks are actually needed or active for a specific test.

                - **BECAUSE:** Explicit, test-suite-level mocking (jest.mock within the *.test.ts file) makes dependencies clear and avoids unintended side effects across the entire test run.


## 6. Fake Timers & Time Mocking

- **RULE:** Fake timers (jest.useFakeTimers(), jest.runAllTimers(), jest.advanceTimersByTimeAsync(), etc.) are **FORBIDDEN**.

    - **BECAUSE:** They have proven unreliable and difficult to manage correctly with the complex asynchronous interactions (Promises, async/await, events) in this project, often leading to hangs, inaccurate trace logs, and hard-to-debug timing issues.

        - **BECAUSE:** Accurately simulating the interleaving of timers, Promises, and microtasks is complex, and fake timers can fail to capture the real-world behavior, causing tests to pass when they should fail or vice-versa.

            - **BECAUSE:** Debugging issues related to fake timer interactions can be extremely time-consuming and frustrating, often masking the underlying logic error.

- **RULE:** Rely on **real timers** (setTimeout, setInterval) for testing asynchronous code involving delays.

    - **BECAUSE:** Using real timers, while potentially slower, provides a much more accurate reflection of runtime behavior and simplifies debugging asynchronous flows compared to the complexities of fake timers.

        - **BECAUSE:** The test executes closer to how the actual application code runs, reducing the chance of discrepancies between test behavior and real-world behavior.

            - **BECAUSE:** Failures observed with real timers are more likely to represent genuine issues in the asynchronous logic.

- **RULE:** Adjust Jest test timeouts (jest.setTimeout()) globally or per test suite/case as needed to accommodate real delays used in tests.

    - **BECAUSE:** Tests using real timers inherently take longer to execute than synchronous code or code using fake timers, and may exceed Jest's default timeout period.

        - **BECAUSE:** Explicitly setting a longer timeout prevents tests from failing simply because they didn't complete within the default limit, ensuring failures are due to logic errors rather than insufficient time.

- **RULE:** When precise control over time is needed (e.g., testing timeouts, specific scheduling), **PREFER mocking `Date.now()`** using `jest.spyOn(Date, 'now').mockReturnValue(...)` over using fake timers.
    - **BECAUSE:** AI Coding assistants are unable to use jest fake timers correctly wasting hours to try to get them to work, which is not allowed and results in the code being deleted
    - **BECAUSE:** Mocking `Date.now()` directly provides deterministic control over the current time reported to the code under test without the complexities and potential unreliability associated with Jest's fake timer system.
        - **BECAUSE:** This approach avoids issues with asynchronous operations (Promises, async/await) that can interact poorly with fake timers.
            - **BECAUSE:** It allows tests to explicitly set the time for specific scenarios, making the test logic clearer and easier to reason about.