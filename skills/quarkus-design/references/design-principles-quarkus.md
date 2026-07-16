# Quarkus Design Principles

## Application And Module Boundaries

- Organize responsibilities around cohesive capabilities when that makes ownership and change boundaries clearer than global technical layers.
- Define which types, commands, events, and endpoints form each module's public contract before choosing CDI beans or extension APIs.
- Keep application behavior independent of transport and infrastructure details when that separation supports real variants or focused testing.
- Reject shared utility packages that become unowned integration surfaces and module cycles that hide responsibility.

## Extensions And Build-Time Augmentation

- Prefer supported Quarkus extensions for framework integration and native metadata, but do not add an extension when a smaller existing dependency already owns the behavior.
- Identify which configuration and bean decisions are fixed during augmentation and which remain adjustable at runtime.
- Treat reflection, dynamic proxies, resource discovery, serialization, and classpath scanning as deployment constraints when native executables are required.
- Keep custom build steps or extension code outside application modules unless the project genuinely owns reusable Quarkus build-time integration.

## Execution Model

- Choose blocking code for straightforward imperative dependencies and reactive code for a complete non-blocking chain with demonstrated concurrency needs.
- Do not select Hibernate Reactive merely because Quarkus REST supports reactive endpoints; standard Hibernate ORM remains appropriate for ordinary blocking persistence.
- Place blocking-to-reactive, reactive-to-blocking, and virtual-thread transitions at explicit adapter boundaries with concurrency and context limits.
- Define cancellation, backpressure, timeouts, context propagation, worker-pool capacity, and failure behavior for asynchronous work.

## Transactions, Events, And Side Effects

- Define one local consistency boundary before placing transaction annotations.
- Keep remote calls outside local database transactions unless latency and failure coupling are deliberately accepted.
- Use messaging or events only when delivery, ordering, duplication, retry, dead-letter, and recovery responsibilities are explicit.
- Use an outbox or equivalent durable handoff when database state and external publication must survive process failure together.

## Security And Operations

- Define identities, trust boundaries, tenant and data authorization, administrative access, and audit requirements before choosing mechanisms.
- Treat health, readiness, metrics, tracing, logging, configuration, and management endpoints as application contracts.
- Tie native versus JVM packaging, container topology, scaling, caching, and resilience to measured workload and deployment requirements.
- Verify the actual packaged form because build-time augmentation and native compilation can expose failures absent from unit tests.

## Authoritative References

- [Quarkus CDI Reference](https://quarkus.io/guides/cdi-reference)
- [Quarkus REST Execution Model](https://quarkus.io/guides/rest#execution-model-blocking-non-blocking)
- [Quarkus Configuration Reference](https://quarkus.io/guides/config-reference)
- [Quarkus Native Executable Guide](https://quarkus.io/guides/building-native-image)
