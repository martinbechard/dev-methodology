# State And Strategy Patterns Review Checklist

- Question: Is the variation axis or state model explicit and demonstrated?
- Question: Are strategies cohesive, substitutable, and selected by a clear owner?
- Question: Are states, allowed transitions, rejected transitions, and invariants complete?
- Question: Does one component clearly own transition authorization and atomicity?
- Question: Is the Template Method workflow stable enough to justify inheritance?
- Question: Are protected hooks minimal and are invariant steps protected from reordering?
- Question: Do tests cover every strategy, transition, invalid transition, hook, and shared contract case?
- Question: Is a function, enum, table, conditional, or composition-only design insufficient for a documented reason?
