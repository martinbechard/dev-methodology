# Java Composition Pattern Guidelines

## Selection

| Pattern | Choose when | Main cost |
|---|---|---|
| Composite | Leaves and containers need a useful uniform contract | Some operations may not suit every node |
| Decorator | Responsibilities must stack dynamically per object | Order, identity, and diagnostics become layered |
| Proxy | Access to a subject needs control without changing its contract | Remote, lazy, or guarded behavior may not be transparent |

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
- For dynamic proxies, validate interface coverage, invocation-handler exception behavior, and default methods under the configured Java release.

## Java Verification

- Test composite trees for empty, leaf, nested, cyclic, and deep structures as supported.
- Test decorators individually and in supported order combinations.
- Test proxies against the real subject contract, including access denial and remote or lazy failure modes.

## Authoritative References

- [Composite](https://refactoring.guru/design-patterns/composite)
- [Decorator](https://refactoring.guru/design-patterns/decorator)
- [Proxy](https://refactoring.guru/design-patterns/proxy)
- [Java Dynamic Proxy](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/reflect/Proxy.html)
- [Java Design Patterns Repository](https://github.com/iluwatar/java-design-patterns)
