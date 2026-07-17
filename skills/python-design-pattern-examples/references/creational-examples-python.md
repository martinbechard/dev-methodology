# Python Creational Pattern Examples

```python
# Factory Method
class Creator(ABC):
    @abstractmethod
    def create(self) -> Product: ...

# Abstract Factory
class UiFactory(Protocol):
    def button(self) -> Button: ...
    def field(self) -> Field: ...

# Builder
request = RequestBuilder().url(url).timeout(30).build()

# Prototype
copy_rule = dataclasses.replace(rule, tags=list(rule.tags))

# Singleton
metrics_registry = MetricsRegistry()
```

- A module-owned instance often expresses single ownership without a Singleton class.
- Class methods, callables, protocols, and dependency injection can replace factory hierarchies.
- Dataclasses and copy operations still require explicit deep-versus-shallow ownership.
