# Java Creational Pattern Examples

These are shape sketches, not copy-ready frameworks.

```java
// Factory Method
abstract class Creator { abstract Product create(); Product run() { return create(); } }

// Abstract Factory
interface UiFactory { Button button(); Field field(); }

// Builder
record Request(String url, int timeout) {
    static final class Builder { String url; int timeout = 30; Request build() { return new Request(url, timeout); } }
}

// Prototype
record Rule(String name, List<String> tags) { Rule copy() { return new Rule(name, List.copyOf(tags)); } }

// Singleton
enum MetricsRegistry { INSTANCE }
```

- Factory Method often uses an abstract method or injected supplier; Abstract Factory may use an interface plus providers.
- Records suit immutable products and snapshots; builders still need one authoritative validation boundary.
- Enum Singleton is one Java option, not a reason to choose the pattern.
