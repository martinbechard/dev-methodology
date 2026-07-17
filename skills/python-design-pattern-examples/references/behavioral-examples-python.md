# Python Behavioral Pattern Examples

```python
# Chain of Responsibility
Handler = Callable[[Request], Response | None]

# Command
@dataclass(frozen=True)
class SubmitOrder: order_id: str

# Interpreter
Expr = Literal | Add

# Iterator
def depth_first(root: Node) -> Iterator[Node]: yield root

# Mediator
class CheckoutMediator(Protocol): ...

# Memento
@dataclass(frozen=True)
class EditorMemento: text: str; cursor: int

# Observer
Subscriber = Callable[[Event], None]

# State
class OrderState(Protocol): ...

# Strategy
PricingStrategy = Callable[[Cart], Money]

# Template Method
class ImportJob(ABC):
    def run(self): self.read(); self.write()

# Visitor
@singledispatch
def visit(node: Node): raise TypeError(type(node))
```

- Callables, generators, protocols, frozen dataclasses, singledispatch, and pattern matching often express behavioral roles directly.
- Define async versus sync behavior, context-manager ownership, unsubscribe cleanup, exception propagation, and mutation explicitly.
- Exhaustive visitor behavior and state transitions still require tests because Python does not enforce a closed hierarchy.
