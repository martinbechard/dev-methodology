# Interpreter Pattern Guidelines

## Selection

- Use Interpreter for a small language whose grammar and evaluation semantics belong to the domain.
- Prefer mature parser tooling when grammar size, ambiguity, recovery, performance, tooling, or security exceeds a simple syntax tree.
- Prefer structured data when callers do not need a language.

## Grammar And Evaluation

- Write the grammar and precedence rules before the object model.
- Give each syntax node one production-level responsibility and keep evaluation context explicit.
- Keep parsing, validation, optimization, and execution separable so each can fail clearly.
- Bound recursion, input size, execution time, memory, and side effects for untrusted expressions.
- Preserve source locations for useful errors and diagnostics.

## Verification

- Cover every production, precedence and associativity combination, whitespace rule, invalid token, incomplete form, and evaluation failure.
- Use generated or property-based cases when the grammar has combinatorial interactions.
- Test resource limits and side-effect permissions as contract behavior.

## Authoritative References

- [Design Patterns: Elements of Reusable Object-Oriented Software](https://www.informit.com/store/design-patterns-elements-of-reusable-object-oriented-software-9780201633610)
- [Interpreter](https://refactoring.guru/design-patterns/interpreter)
