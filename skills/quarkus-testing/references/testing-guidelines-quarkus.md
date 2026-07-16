# Quarkus Testing Guidelines

## Test Boundary Selection

- Start with the smallest boundary that can prove the behavior.
- Use plain JUnit and the project mocking library for behavior that does not depend on CDI, interception, configuration, extensions, or launch mode.
- Use Quarkus component tests when a focused CDI component boundary is sufficient and the configured Quarkus line supports that facility.
- Use QuarkusTest when injection, configuration, REST integration, security, persistence, transactions, Dev Services, or extension wiring must run in the test-mode application.
- Use QuarkusIntegrationTest to exercise the built artifact outside the test JVM, including JAR, container, or native deployment forms supported by the project.

## Profiles, Mocks, And Resources

- Keep profile overrides and enabled alternatives inside the test contract and avoid multiplying profiles for data variations that fixtures can express.
- Order or group profile-dependent tests to limit Quarkus restarts without creating order-dependent state.
- Replace CDI beans only through mechanisms supported by their scope and the configured test extension; distinguish a proxy from the installed mock during verification.
- Use Dev Services when automatic provisioning, image version, configuration, and lifecycle match the behavior under test.
- Use explicit test resources or externally managed services when startup, shared state, topology, credentials, failure injection, or lifecycle must be controlled directly.

## Persistence And Transactions

- Use the production database engine when dialect, migrations, constraints, locking, generated values, or reactive driver behavior matters.
- Distinguish standard Hibernate ORM test transactions from reactive session and transaction support.
- Assert committed or rolled-back database outcomes rather than assuming a test transaction models production timing.
- Reset databases, brokers, caches, and other mutable services through owned fixtures between tests.

## Packaged And Native Verification

- Run the built artifact when classpath layout, resources, configuration, ports, launch scripts, container metadata, or startup behavior changes.
- Run native integration tests when native delivery is required or code changes affect reflection, resources, proxies, serialization, JNI, dynamic loading, or native-only configuration.
- Keep build-time configuration used for the artifact distinct from runtime overrides supplied to the integration test.
- Treat JVM tests as insufficient evidence for a native deployment claim.

## Determinism And Reporting

- Avoid sleeps; coordinate asynchronous behavior through observable completion, bounded polling, or framework test support.
- Control clocks, identifiers, ports, randomness, and external responses when assertions depend on them.
- Cover successful behavior, validation, authentication, authorization, tenant isolation, translated failures, transaction outcomes, and event timing where applicable.
- Report the test boundary, launch mode, profile, artifact type, service implementations, database engine, and exact command results.

## Authoritative References

- [Quarkus Testing Guide](https://quarkus.io/guides/getting-started-testing)
- [Quarkus Dev Services](https://quarkus.io/guides/dev-services)
- [Quarkus Continuous Testing](https://quarkus.io/guides/continuous-testing)
- [Quarkus Native Executable Guide](https://quarkus.io/guides/building-native-image)
