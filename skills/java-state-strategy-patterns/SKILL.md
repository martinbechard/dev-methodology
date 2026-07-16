---
name: java-state-strategy-patterns
description: Design or review Java Strategy, State, or Template Method patterns when algorithms vary, behavior depends on explicit state and transitions, or a stable workflow owns customizable steps.
metadata:
  category: stack-and-domain
---

# Java State And Strategy Patterns

Combine with Java Design and with Java when the design is implemented or reviewed in source.

## Pattern Boundary

- Use Strategy when callers or configuration select among interchangeable algorithms under one contract.
- Use State when behavior and allowed transitions depend on an explicit current state with owned invariants.
- Use Template Method when one stable algorithm owns ordering and subclasses customize constrained steps.
- Prefer composition for open-ended variation; use inheritance only when the base workflow is genuinely stable and protected hooks are sufficient.
- Keep state transitions explicit and atomic, and keep strategies stateless or clear about ownership.
- Do not replace a small conditional with a class hierarchy unless demonstrated variation justifies it.

Read [Java State And Strategy Guidelines](references/design-guidelines-java-state-strategy-patterns.md) when selecting, implementing, or comparing these patterns.

## Verification

- Prove every algorithm variant, state transition, invalid transition, workflow invariant, and extension hook.
- Test behavior through the shared contract and verify substitutability across variants.
- Report the variation axis and why a table, function, enum, or conditional was insufficient.

## Review Evidence

Read references/review-checklist-java-state-strategy-patterns.md during design or code review. Use Code Review Evidence to extract and synthesize the results.
