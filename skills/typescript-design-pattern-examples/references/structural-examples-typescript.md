# TypeScript Structural Pattern Examples

```typescript
// Adapter
const adaptGateway = (legacy: LegacyGateway): PaymentPort => ({ pay: input => legacy.send(map(input)) })

// Bridge
class Report { constructor(private readonly renderer: Renderer) {} }

// Composite
type Node = { kind: "leaf"; size: number } | { kind: "group"; children: Node[] }

// Decorator
const withRetry = (client: Client): Client => ({ call: request => retry(() => client.call(request)) })

// Facade
const checkout = (deps: CheckoutDeps, cart: Cart): Promise<Receipt> => complete(deps, cart)

// Flyweight
const styles = new Map<string, Readonly<GlyphStyle>>()

// Proxy
const guarded = new Proxy(document, { get: (target, key) => authorizeThenRead(target, key) })
```

- Prefer explicit wrappers over JavaScript Proxy when static discoverability and predictable receiver behavior matter.
- Freeze or treat shared flyweights as deeply immutable; readonly is compile-time only.
- Discriminated unions can express Composite without a class hierarchy.
