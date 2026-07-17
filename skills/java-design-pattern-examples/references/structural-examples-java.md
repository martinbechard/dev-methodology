# Java Structural Pattern Examples

```java
// Adapter
final class PaymentAdapter implements PaymentPort { private final LegacyGateway gateway; }

// Bridge
record Report(Renderer renderer) { String render(Data data) { return renderer.render(data); } }

// Composite
sealed interface Node permits Leaf, Group { int size(); }
record Group(List<Node> children) implements Node { public int size() { return children.stream().mapToInt(Node::size).sum(); } }

// Decorator
record RetryingClient(Client next) implements Client { public Result call(Request r) { return retry(() -> next.call(r)); } }

// Facade
record CheckoutFacade(Inventory stock, Payments payments) { Receipt checkout(Cart cart) { return complete(cart); } }

// Flyweight
record GlyphStyle(String font, int size) {}
final class StylePool { private final Map<Key, GlyphStyle> shared = new ConcurrentHashMap<>(); }

// Proxy
record AuthorizedDocument(Document target, Authorizer auth) implements Document { public Data read(User u) { auth.check(u); return target.read(u); } }
```

- Delegation is normally clearer than inheritance for Adapter, Bridge, Decorator, and Proxy.
- Dynamic proxies are appropriate only when interface dispatch and reflective failure semantics fit.
- Flyweight values should be immutable and keyed by complete intrinsic identity.
