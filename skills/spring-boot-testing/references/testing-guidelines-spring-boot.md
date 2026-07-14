# Spring Boot Testing Guidelines

## Test Boundary Selection

- Start with the smallest boundary that can prove the behavior.
- Use plain JUnit and the project's mocking library for isolated business behavior that does not depend on Spring proxies or configuration.
- Use a web slice for controller mapping, validation, serialization, exception translation, and filter behavior with controlled collaborators.
- Use a persistence slice for mappings, repository queries, constraints, converters, and transaction behavior.
- Use a complete application context for auto-configuration, security chains, cross-layer transactions, application events, startup validation, or full workflow wiring.
- Avoid testing the same behavior through every layer without a distinct risk being proved.

## Version-Aware Test Support

- Read the configured Spring Framework and Spring Boot versions before selecting test annotations.
- Use MockitoBean and MockitoSpyBean where the configured Spring line provides them; preserve MockBean only in project lines where it remains the supported convention.
- Keep dynamic properties, service connections, context customization, and slice imports consistent with the configured Boot line.
- Do not add a mocking library, assertion library, or test runner solely because an example uses it.

## Databases And External Services

- Use an in-memory database only when its SQL, transaction, constraint, and type behavior are sufficient for the claim being tested.
- Use Testcontainers or another production-compatible service for dialect-specific queries, migrations, locking, collation, generated values, or integration protocols.
- Prefer service-connection support when available and established by the project; otherwise bind dynamic properties explicitly.
- Control container lifecycle and reuse so tests remain isolated and continuous integration can reproduce them.
- Replace external services only at an intentional boundary and document any behavior the replacement cannot prove.

## Context, Data, And Determinism

- Keep profiles and property overrides local to the test contract.
- Avoid unnecessary dirty-context markers; they defeat context caching and often hide shared-state problems.
- Reset mutable databases, message brokers, caches, clocks, and singleton test doubles between tests through owned fixtures.
- Avoid sleeps. Coordinate asynchronous behavior through observable completion, bounded polling, latches, or framework test support.
- Use fixed clocks and controlled identifiers or randomness where output depends on them.

## Security And Failure Behavior

- Cover unauthenticated, unauthorized, tenant-isolated, and permitted behavior for protected operations.
- Verify validation and exception translation through the actual web or messaging boundary.
- Assert committed and rolled-back state when transaction behavior is material.
- Verify event or side-effect timing when behavior depends on transaction completion.

## Reporting

- Name the tested boundary, context type, active profile, database or service implementation, and commands executed.
- Distinguish a mocked contract from a real integration and state any production behavior not exercised.
- Treat coverage as evidence of exercised code, not a substitute for meaningful behavior and failure assertions.
