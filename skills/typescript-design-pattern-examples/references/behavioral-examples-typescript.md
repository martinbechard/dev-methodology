# TypeScript Behavioral Pattern Examples

```typescript
// Chain of Responsibility
type Handler = (request: Request) => Promise<Response | undefined>

// Command
type Command = { kind: "submitOrder"; orderId: string }

// Interpreter
type Expr = { kind: "literal"; value: number } | { kind: "add"; left: Expr; right: Expr }

// Iterator
function* depthFirst(root: Node): IterableIterator<Node> { yield root }

// Mediator
interface CheckoutMediator { changed(source: Field): void }

// Memento
type EditorMemento = Readonly<{ text: string; cursor: number }>

// Observer
type Unsubscribe = () => void

// State
type OrderState = { kind: "draft" } | { kind: "paid"; paidAt: Date }

// Strategy
type PricingStrategy = (cart: Cart) => Money

// Template Method
abstract class ImportJob { async run() { await this.read(); await this.write(); } protected abstract read(): Promise<void> }

// Visitor
const visit = <R>(node: Node, visitor: Visitor<R>): R => node.kind === "leaf" ? visitor.leaf(node) : visitor.group(node)
```

- Functions and discriminated unions are often more idiomatic than one-class-per-role designs.
- Use exhaustive never checks for closed unions and AbortSignal for cancellation where applicable.
- Define subscription cleanup, promise rejection, execution ordering, and runtime validation explicitly.
