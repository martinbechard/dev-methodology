# Java Behavioral Pattern Examples

```java
// Chain of Responsibility
interface Handler { Optional<Response> handle(Request request); }

// Command
record SubmitOrder(OrderId id) implements Command<Result> {}

// Interpreter
sealed interface Expr permits Literal, Add { int eval(Context context); }

// Iterator
final class Tree implements Iterable<Node> { public Iterator<Node> iterator() { return new DepthFirstIterator(root); } }

// Mediator
interface CheckoutMediator { void changed(Field source); }

// Memento
record EditorMemento(String text, int cursor) {}

// Observer
interface Subscriber<E> { void onEvent(E event); }

// State
sealed interface OrderState { OrderState pay(Order order); }

// Strategy
interface PricingStrategy { Money price(Cart cart); }

// Template Method
abstract class ImportJob { final void run() { read(); validate(); write(); } abstract void read(); abstract void write(); }

// Visitor
interface NodeVisitor<R> { R visitLeaf(Leaf leaf); R visitGroup(Group group); }
```

- Use functional interfaces for single-operation strategies, commands, handlers, or observers when identity and lifecycle are unnecessary.
- Use sealed types, records, pattern matching, Iterable, Iterator, Flow, and Comparator only where their precise contracts fit.
- Preserve interruption, executor, transaction, diagnostic context, and resource ownership across asynchronous behavior.
