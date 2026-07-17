# Python Structural Pattern Examples

```python
# Adapter
class PaymentAdapter:
    def __init__(self, legacy: LegacyGateway): self._legacy = legacy

# Bridge
@dataclass
class Report:
    renderer: Renderer

# Composite
Node = Leaf | Group

# Decorator
def with_retry(client: Client) -> Client: return RetryingClient(client)

# Facade
class CheckoutFacade: ...

# Flyweight
@functools.lru_cache
def glyph_style(font: str, size: int) -> GlyphStyle: return GlyphStyle(font, size)

# Proxy
class AuthorizedDocument:
    def __getattr__(self, name: str): return getattr(self._target, name)
```

- Protocols and delegation preserve intent without requiring inheritance.
- Python decorators are language syntax and call wrappers; use the pattern name only when object responsibilities are composed.
- Shared flyweights should be immutable, and dynamic proxying must not obscure important API or failure behavior.
