---
name: state-strategy-patterns
description: Design or review Strategy, State, or Template Method when algorithms vary, behavior depends on explicit states and transitions, or a stable workflow owns customizable steps.
metadata:
  category: development-practice
---

# State And Strategy Patterns

Use with the implementation-language skill and its design-pattern examples when source code is in scope.

## Pattern Boundary

- Use Strategy when callers or configuration select interchangeable algorithms under one contract.
- Use State when behavior and allowed transitions depend on an explicit current state with owned invariants.
- Use Template Method when one stable algorithm owns ordering and derived implementations customize constrained steps.
- Prefer composition for open-ended variation; use inheritance only when the base workflow is genuinely stable.
- Keep transitions explicit and atomic, and make strategy ownership clear.
- Prefer a function, table, enum, or small conditional when it already expresses closed behavior.

Read [State And Strategy Pattern Guidelines](references/design-guidelines-state-strategy-patterns.md) when selecting or comparing these patterns.

## Verification

- Prove every algorithm variant, transition, invalid transition, workflow invariant, and extension hook.
- Test behavior through the shared contract and verify substitutability.
- Report the variation axis and why a simpler representation was insufficient.

## Review Evidence

Read references/review-checklist-state-strategy-patterns.md during design or code review. Use Code Review Evidence to synthesize the results.
