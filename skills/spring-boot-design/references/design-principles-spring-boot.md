# Spring Boot Design Principles

## Application Modules

- Organize responsibilities around cohesive business capabilities when that makes ownership and change boundaries clearer than global technical layers.
- Keep the main application class in an intentional root package so component and entity scanning do not escape the application boundary.
- Define which types and events form each module's public interface and keep implementation packages inaccessible to other modules where practical.
- Use Spring Modulith or ArchUnit when the project needs executable module-boundary verification; do not add them only to decorate an undocumented architecture.
- Reject module dependency cycles and shared common packages that become an unowned integration surface.

## Web And Application Boundaries

- Keep HTTP, messaging, scheduling, and command-line adapters responsible for transport concerns and delegation.
- Place business orchestration where one component can own the complete use case, its authorization, and its consistency boundary.
- Keep persistence and remote-client details behind boundaries that allow the application behavior to be tested independently when that separation has value.
- Do not require a service interface, implementation pair, DTO, mapper, or repository for every class. Introduce each boundary for a demonstrated contract difference.

## Data And Transaction Design

- Define the consistency boundary before placing transactions. One transaction should protect one coherent local operation.
- Keep remote calls out of local database transactions unless the latency and failure coupling are deliberately accepted.
- Use optimistic or pessimistic coordination according to contention, invariant, and retry behavior rather than as a universal default.
- Use events to decouple modules only when event ownership, ordering, delivery, duplication, and failure recovery are defined.
- Use an outbox or equivalent durable handoff when a database change and external publication must survive process failure together.

## Execution Model

- Choose Spring MVC for imperative request handling and WebFlux for a genuinely reactive dependency chain and workload.
- Do not treat asynchronous annotations, reactive types, or virtual threads as interchangeable solutions.
- Define concurrency limits, backpressure, cancellation, context propagation, and blocking isolation for the chosen model.

## Security And Operations

- Define trust boundaries, identities, tenant boundaries, data authorization, and audit requirements before selecting filters or annotations.
- Separate authentication from authorization and enforce authorization close to the protected operation and data.
- Define health, readiness, metrics, tracing, logging, and administrative access as part of the operational contract.
- Keep deployment topology, scaling, caching, and resilience decisions tied to measured failure and workload characteristics.

## Architecture Options

- Use a simple layered application while the responsibilities are clear and change together.
- Use package-by-feature or a modular monolith when independent capabilities need explicit APIs and dependency rules inside one deployment.
- Use ports and adapters when volatile infrastructure or multiple adapters justify a stable application-facing boundary.
- Split services only when independent deployment, scaling, ownership, availability, or regulatory boundaries outweigh distributed-system cost.
