# Composition Pattern Guidelines

## Selection

| Pattern | Choose when | Main cost |
|---|---|---|
| Composite | Leaves and containers need a useful uniform contract | Some operations may not suit every node |
| Decorator | Responsibilities must stack dynamically per object | Order, identity, and diagnostics become layered |
| Proxy | Access to a subject needs control without changing its contract | Remote, lazy, or guarded behavior may not be transparent |
| Flyweight | Many logical objects share stable intrinsic state | Separating intrinsic and extrinsic state complicates callers |

## Composite

- Model the tree because hierarchy is part of the problem, not to avoid writing a loop.
- Decide whether child management belongs on the component contract or only on composites.
- Define parent ownership, cycles, traversal order, mutation during traversal, and recursive failure behavior.
- Avoid no-op or unsupported leaf methods that make the common interface dishonest.

## Decorator

- Preserve the wrapped contract and document any intentional change to ordering, exceptions, identity, equality, or lifecycle.
- Make decorator order visible when behavior is not commutative.
- Forward every required operation, including close, flush, cancellation, metadata, and context propagation.
- Prefer a named composite service when a wrapper stack becomes difficult to inspect or configure.

## Proxy

- Name the access concern: remote location, lazy loading, authorization, caching, lifecycle, instrumentation, or another owned policy.
- Preserve contract semantics or make latency, partial failure, serialization, and identity differences explicit.
- Do not perform hidden blocking network or database work behind an apparently local cheap operation.
- For runtime-generated proxies, validate contract coverage, invocation failures, and language-specific dispatch behavior.

## Flyweight

- Separate immutable intrinsic state from caller-owned extrinsic state before introducing a cache or pool.
- Key shared instances by complete intrinsic identity and make cache ownership, eviction, concurrency, and lifetime explicit.
- Do not share mutable state or external handles whose ownership differs between logical objects.
- Measure memory or construction pressure; ordinary value objects are simpler when sharing has no material benefit.

## Verification

- Test composite trees for empty, leaf, nested, cyclic, and deep structures as supported.
- Test decorators individually and in supported order combinations.
- Test proxies against the real subject contract, including access denial and remote or lazy failure modes.
- Test Flyweight identity keys, shared immutability, extrinsic-state separation, concurrency, and eviction behavior.

## Authoritative References

- [Composite](https://refactoring.guru/design-patterns/composite)
- [Decorator](https://refactoring.guru/design-patterns/decorator)
- [Proxy](https://refactoring.guru/design-patterns/proxy)
- [Flyweight](https://refactoring.guru/design-patterns/flyweight)
