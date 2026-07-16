# Mockito Mocking Guidelines

## Boundary Selection

- Mock a collaborator when the unit owns the interaction and the real collaborator would cross an external, nondeterministic, slow, destructive, or deliberately isolated boundary.
- Prefer real domain values, collections, and pure collaborators. Use a lightweight fake when stateful behavior matters more than exact calls.
- Avoid mocking value objects, the type under test, data-transfer shapes, or implementation details that can be constructed directly.
- Treat a test requiring many collaborators or extensive interaction scripts as evidence that the production boundary may be too broad.

## Initialization And Strictness

- Use the owning test framework's supported Mockito integration so mocks are initialized and validated consistently.
- Keep strict stubbing enabled. Resolve unused, mismatched, or shadowed stubs by simplifying the test or correcting the contract.
- Scope leniency to the smallest necessary stub and record why the collaborator legitimately varies.
- Create fresh mocks per test. Do not reset mocks mid-test or share mutable mock state between test instances.

## Stubbing

- Stub only behavior needed to reach the scenario under test.
- Prefer simple return, exception, or answer behavior over broad default answers and deep stubs.
- Use argument matchers only when exact values are irrelevant or deliberately variable. When one argument uses a matcher, keep the invocation's matcher usage consistent.
- Use an answer only when the returned behavior genuinely depends on invocation data; keep it deterministic and side-effect controlled.
- Model sequential returns or failures only when retry, polling, or state progression is part of the contract.

## Verification

- Verify an interaction when its occurrence, arguments, count, absence, or order is a required outcome.
- Do not verify every stubbed call. Successful state or returned-value assertions usually prove ordinary collaboration more clearly.
- Avoid blanket no-more-interactions checks. Use them only when absence of any additional call is itself contractual.
- Use ordered verification only when ordering affects correctness, not to freeze incidental implementation sequence.
- Verify no interaction for rejected or short-circuited flows when preventing the side effect is an explicit requirement.

## Captors, Spies, And Advanced Mocking

- Use an argument captor for verification when a created or transformed value cannot be observed another way. Do not use captors as a default stubbing mechanism.
- Prefer a real object over a spy. A spy calls real methods unless safely stubbed, so avoid stubbing syntax that invokes the real method during setup.
- Treat partial, static, construction, final-type, and deep-stub mocking as compatibility-sensitive. Confirm support under the configured Mockito, Java, test runner, and runtime instrumentation.
- Keep advanced mocking local and explain why an injectable boundary or real implementation is not more suitable.

## Failure Diagnosis And Reporting

- Read strict-stubbing and verification failures as contract mismatches before loosening matchers or invocation counts.
- Distinguish a mock configuration failure from a production assertion failure and preserve the original cause.
- Report mocked boundaries, real integrations, strictness or mock-maker changes, and commands executed.

## Authoritative References

- [Mockito Documentation](https://javadoc.io/doc/org.mockito/mockito-core/latest/org.mockito/org/mockito/Mockito.html)
- [Mockito JUnit Jupiter Extension](https://javadoc.io/doc/org.mockito/mockito-junit-jupiter/latest/org.mockito.junit.jupiter/org/mockito/junit/jupiter/MockitoExtension.html)
- [Mockito Project](https://github.com/mockito/mockito)
