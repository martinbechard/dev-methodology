# Java Composition Patterns Review Checklist

- Question: Is Composite, Decorator, or Proxy selected for a demonstrated structural or access requirement?
- Question: Does a Composite expose only operations meaningful to both leaves and containers?
- Question: Are tree ownership, cycles, traversal order, mutation, and recursive failure defined?
- Question: Does every Decorator preserve the wrapped contract and forward lifecycle operations?
- Question: Is decorator ordering understandable and tested?
- Question: Does a Proxy make remote, lazy, guarded, cached, or instrumented semantics explicit?
- Question: Are identity, equality, exceptions, concurrency, cleanup, and diagnostics preserved through wrappers?
- Question: Do tests compare representative wrapped and unwrapped behavior through the shared contract?
