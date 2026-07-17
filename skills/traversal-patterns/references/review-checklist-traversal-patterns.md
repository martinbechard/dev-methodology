# Traversal Patterns Review Checklist

- Question: Does traversal need encapsulation or does a stable element hierarchy need independently evolving operations?
- Question: Are iterator order, exhaustion, removal, mutation, concurrency, null, and resource semantics explicit?
- Question: Are native iterators, generators, streams, sequences, and collection views insufficient for a documented reason?
- Question: Does Visitor match the expected variation direction of new operations over new element types?
- Question: Is visitor dispatch exhaustive with explicit behavior for unknown types?
- Question: Are traversal ownership, recursion, cycles, depth, laziness, and short-circuiting controlled?
- Question: Do tests cover empty, nested, heterogeneous, exhausted, modified, cyclic, and deep structures as supported?
- Question: Are ordinary polymorphism or language pattern matching insufficient for a documented reason?
