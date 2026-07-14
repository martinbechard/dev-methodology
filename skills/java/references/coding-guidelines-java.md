# Java Coding Guidelines

## Project And Language Baseline

- Read the owning build configuration for the Java release, preview-feature policy, compiler warnings, annotation processors, formatter, static analysis, and test tasks.
- Preserve the existing style when no formatter is configured. Do not impose a third-party style guide on an established project.
- Prefer the project wrapper and project-native tasks so local verification matches continuous integration.
- Use newer syntax only when it improves clarity without changing public behavior or excluding a supported runtime.

## Types And Declarations

- Use parameterized types and retain type information across collection, reflection, serialization, and persistence boundaries.
- Keep casts narrow and prove them from an explicit runtime check or owning API contract.
- Make fields final unless mutation is required by the object lifecycle.
- Use records for transparent value carriers only when record equality, construction, serialization, and framework behavior match the contract.
- Use sealed types only for a genuinely closed hierarchy whose permitted variants are owned together.
- Use local variable type inference only when the initializer makes the type and meaning evident.

## Nullness And Absence

- Follow the project nullness annotations and package defaults. Do not mix annotation families without an explicit migration.
- Validate external and framework-provided input at the boundary where invalid values can be rejected meaningfully.
- Use Optional for an absence-bearing result when that convention improves the caller contract. Avoid Optional fields, parameters, and collection elements unless an established API requires them.
- Return empty collections when the contract means no elements. Do not substitute an empty value when null has distinct domain meaning.
- Do not call Optional get without proving presence in the same control path.

## Collections And Object Contracts

- Preserve whether returned collections are mutable, immutable, live views, snapshots, ordered, sorted, or duplicate-preserving.
- Defensively copy mutable input and output when the owning object must control later mutation.
- Implement equals and hashCode together from stable state appropriate to the object lifecycle.
- Keep comparison and ordering consistent with equality when sorted collections or binary search depend on that relationship.
- Exclude secrets, credentials, personal data, and expensive lazy relationships from string representations.

## Numbers, Time, Text, And Identifiers

- Choose numeric types from range, precision, scale, and overflow requirements rather than convenience.
- Give BigDecimal operations an explicit rounding policy where division or scale conversion can lose information.
- Use compare semantics rather than equality when BigDecimal scale must not affect numeric equivalence.
- Use java.time types and make clock, time zone, and daylight-saving behavior explicit at testable boundaries.
- Specify charsets for byte and text conversion and locales for locale-sensitive parsing, formatting, or case conversion.
- Treat identifiers as opaque unless their format is part of the public contract.

## Exceptions And Resources

- Throw exceptions for exceptional outcomes, not routine branch control.
- Catch the narrowest useful type and preserve the original cause when translating.
- Add diagnostic context without duplicating sensitive input or logging the same failure at every layer.
- Use try-with-resources for every owned AutoCloseable and acquire multiple resources in an order that permits deterministic cleanup.
- Do not suppress cleanup failures silently when they affect correctness or recovery.

## Concurrency And Cancellation

- Identify the owner of every thread, executor, task, lock, and shared mutable value.
- Prefer immutable data and concurrency utilities over handwritten synchronization.
- Make compound operations atomic; a thread-safe collection does not make multi-step check-and-act logic atomic.
- Preserve interruption by propagating InterruptedException or restoring the interrupt status when translation is required.
- Bound queues, work, retries, and shutdown waits according to the owning lifecycle.
- Use virtual threads only on a supported Java release and only for workloads whose blocking and pinning behavior has been assessed.
- Keep thread-local and transaction context propagation explicit when tasks cross threads.

## Verification

- Compile with the configured release and address relevant warnings rather than hiding them.
- Run focused tests before the complete project-native verification task.
- Run configured formatters and analyzers such as Checkstyle, PMD, SpotBugs, Error Prone, NullAway, or equivalent tools when the project already owns them.
- Add no formatter, analyzer, annotation family, or coverage threshold solely because this guidance names it.
