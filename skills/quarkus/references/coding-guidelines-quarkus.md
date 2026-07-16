# Quarkus Coding Guidelines

## Version, Platform, And Extensions

- Confirm the Quarkus platform version, Java release, extension set, build plugin, and packaging target from the owning Maven or Gradle build.
- Preserve platform-managed dependency versions. Add or pin an extension version only when the platform does not manage it and compatibility has been proved.
- Use the extension that owns the required integration instead of assembling parallel framework infrastructure without a demonstrated gap.
- Treat deprecations and renamed extensions as version-specific migration evidence rather than applying examples from another Quarkus line blindly.

## Arc CDI And Interception

- Prefer explicit required dependencies through constructor injection. Package-private injection points are acceptable when they match the project convention and avoid native-image reflection.
- Choose CDI scopes from lifecycle and sharing requirements. Do not turn application-scoped beans into mutable request state.
- Remember that interception requires an eligible CDI method boundary. Private intercepted methods are invalid, and internal calls can bypass the intended boundary.
- Account for build-time bean discovery and unused-bean removal when beans are selected dynamically or only through external integration.

## Configuration And Profiles

- Distinguish settings fixed at build time from values overridable at runtime before defining deployment overrides.
- Keep related settings in typed configuration mappings and validate required values when configuration is read or startup occurs.
- Use profile-specific configuration deliberately and test the exact build profile and runtime profile combination delivered to production.
- Keep credentials and tokens out of checked-in configuration, native images, build logs, health output, and diagnostic endpoints.

## REST And Execution Model

- Keep request mapping, validation, content negotiation, response status, and failure translation at the transport boundary.
- Treat event-loop code as non-blocking. Move blocking JDBC, filesystem, legacy client, or long-running work to a worker or an explicitly supported virtual-thread boundary.
- Do not infer that a reactive REST layer requires reactive persistence. Choose the complete execution model from workload, dependencies, and team support.
- Preserve context, cancellation, timeouts, and failure behavior across reactive pipelines rather than breaking the pipeline with hidden blocking calls.

## Transactions, Security, And Operations

- Define transactions around one coherent operation on an intercepted CDI boundary and make rollback behavior explicit for expected failures.
- Use the transaction model that belongs to the selected persistence stack; do not combine blocking and reactive transaction annotations casually.
- Use Quarkus security extensions and permission mechanisms when they satisfy the trust boundary, and enforce authorization near protected operations and data.
- Restrict management interfaces and avoid exposing secrets, full payloads, or high-cardinality values through logs, metrics, traces, or health details.

## Packaging And Verification

- Run the project wrapper and focused tests for the changed boundary, then verify application startup with the effective configuration.
- Test the packaged JAR or container when packaging, classpath resources, launch behavior, or deployment configuration changes.
- Build and test a native executable when native delivery is required or when reflection, proxies, serialization, resources, JNI, or dynamic class loading changed.
- Treat native metadata as a specific compatibility contract. Register only the reflection, proxy, serialization, and resource access that runtime behavior actually needs.

## Authoritative References

- [Quarkus CDI Reference](https://quarkus.io/guides/cdi-reference)
- [Quarkus Configuration Reference](https://quarkus.io/guides/config-reference)
- [Quarkus REST Reference](https://quarkus.io/guides/rest)
- [Quarkus Transaction Guide](https://quarkus.io/guides/transaction)
- [Building A Native Executable](https://quarkus.io/guides/building-native-image)
