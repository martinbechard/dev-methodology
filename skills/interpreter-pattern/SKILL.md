---
name: interpreter-pattern
description: Design or review Interpreter when a small, stable language or grammar needs an explicit syntax representation and evaluation rules.
metadata:
  category: design-patterns
---

# Interpreter Pattern

Use with the implementation-language skill and its design-pattern examples when source code is in scope.

## Pattern Boundary

- Use Interpreter when a bounded grammar is part of the domain and syntax nodes can own evaluation rules.
- Define tokens, grammar, precedence, associativity, context, results, errors, and resource limits before implementation.
- Separate parsing from evaluation unless the language is deliberately trivial.
- Keep syntax representation immutable and evaluation context explicit.
- Add new grammar productions without weakening exhaustiveness or diagnostics.
- Prefer an existing parser, query language, regular expression, or direct data structure for complex or incidental syntax.

Read [Interpreter Pattern Guidelines](references/design-guidelines-interpreter-pattern.md) when deciding whether the pattern fits.

## Verification

- Prove parsing and evaluation for every production, precedence boundary, invalid form, and resource limit.
- Test syntax independently from evaluation context and side effects.
- Report the grammar size and the threshold for adopting parser tooling.

## Review Evidence

Read references/review-checklist-interpreter-pattern.md during design or code review. Use Code Review Evidence to synthesize the results.
