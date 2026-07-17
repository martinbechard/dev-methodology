# TypeScript Creational Pattern Examples

```typescript
// Factory Method
abstract class Creator { abstract create(): Product; run(): Product { return this.create(); } }

// Abstract Factory
interface UiFactory { button(): Button; field(): Field }

// Builder
const buildRequest = (parts: Partial<Request>): Request => validate({ timeout: 30, ...parts })

// Prototype
const copyRule = (rule: Rule): Rule => ({ ...rule, tags: [...rule.tags] })

// Singleton
export const metricsRegistry = new MetricsRegistry()
```

- A module-owned instance is often clearer than a class with a global accessor.
- Structural typing makes accidental compatibility possible; keep semantic contracts explicit.
- Builders may be functions when staged mutable identity is unnecessary.
