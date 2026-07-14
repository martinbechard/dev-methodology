# Java Design Review Checklist

- Question: Do the public types and operations express the required behavior and valid states without exposing unnecessary implementation detail?
- Question: Is ownership of mutable state, resources, concurrency, and lifecycle transitions explicit?
- Question: Are packages and modules cohesive, acyclic, and directed toward stable contracts?
- Question: Does every interface, inheritance relationship, and extension point correspond to demonstrated substitution or variation?
- Question: Are domain distinctions represented strongly enough to prevent invalid combinations, unit confusion, or primitive obsession?
- Question: Does the design preserve applicable source, binary, serialization, persistence, and behavioral compatibility?
- Question: Is the selected pattern simpler than the duplication or coupling it replaces?
- Question: Can representative callers and focused tests exercise the design without bypassing its invariants?
