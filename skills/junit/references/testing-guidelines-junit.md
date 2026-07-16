# JUnit Testing Guidelines

## Version And Engine

- Read the owning Maven or Gradle configuration before using an annotation, extension, discovery selector, or launcher feature.
- Keep the API, engine, platform, and build-tool integration on compatible versions. Prefer the project's platform or bill of materials when one owns that alignment.
- Do not migrate legacy tests incidentally. When migration is in scope, preserve discovery and behavior while moving deliberately to the configured Jupiter model.

## Assertions And Scenarios

- Assert observable outcomes and state changes rather than private implementation structure.
- Use equality, collection, exception, timeout, and grouped assertions that express the contract directly.
- Use lazy failure messages when constructing the message is expensive.
- Use exception assertions around the smallest operation expected to fail, then inspect material exception state.
- Avoid multiple unrelated scenarios in one test. Group assertions only when they describe one outcome.

## Fixtures And Lifecycle

- Prefer the default per-method test-instance lifecycle so mutable instance state cannot leak between tests.
- If the project uses per-class lifecycle, reset mutable state explicitly and ensure IDE and build execution use the same configuration.
- Use setup and teardown callbacks for owned fixture lifecycle. Keep expensive shared fixtures immutable or safely resettable.
- Use temporary-directory support for filesystem tests and define cleanup behavior intentionally when artifacts must survive a failure.
- Do not depend on test method order. If an ordered workflow is genuinely the contract, make the state ownership and failure consequences explicit.

## Parameterized And Dynamic Tests

- Use parameterized tests when one behavior must hold across meaningful input partitions.
- Give each case enough display information to diagnose a failure without reproducing it locally.
- Keep argument sources deterministic, bounded, and close to the contract they represent.
- Use dynamic tests only when discovery-time generation adds real value and does not obscure lifecycle or reporting.

## Extensions

- Use registered or declarative extensions for reusable integration with external lifecycle, dependency injection, clocks, resources, or diagnostics.
- Keep extension ordering and inheritance explicit when behavior depends on them.
- Avoid extensions that silently mutate global state or turn unit tests into application integration tests.

## Timeouts And Concurrency

- Use a timeout only where bounded completion is part of the contract or protects the suite from a known hang risk.
- Prefer timeout execution that preserves the test thread when transactions, thread locals, security identity, or framework context depend on it.
- Treat separate-thread or preemptive timeout modes as behavior-changing and verify cleanup after interruption.
- Keep parallel execution disabled unless the project opts in deliberately.
- When parallel execution is enabled, declare execution mode and resource locks where shared files, ports, databases, system properties, or global state exist.
- Remove sleeps. Coordinate asynchronous behavior through observable completion, bounded polling, latches, virtual time, or framework support.

## Reporting

- Report the selected test task or launcher, engine, tags or filters, lifecycle overrides, parallel settings, and commands executed.
- Distinguish isolated JUnit evidence from application-context, container, packaged-artifact, or native-runtime evidence.
- Treat coverage as evidence of execution, not proof of meaningful assertions or boundary behavior.

## Authoritative References

- [JUnit User Guide](https://docs.junit.org/current/user-guide/)
- [Assertions](https://docs.junit.org/current/writing-tests/assertions.html)
- [Extension Model](https://docs.junit.org/current/extensions/overview.html)
- [Parallel Execution](https://docs.junit.org/current/writing-tests/parallel-execution.html)
