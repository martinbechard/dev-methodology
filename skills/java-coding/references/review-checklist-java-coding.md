# Java Coding Review Checklist

- Question: Do types, generics, interfaces, and visibility express valid domain states and ownership without raw or unchecked shortcuts?
- Question: Are nulls and external inputs handled explicitly at the correct boundary?
- Question: Are exception causes preserved and translated only where the public contract is owned?
- Question: Are resources closed deterministically on success and failure paths?
- Question: Are mutation, collection semantics, equality, hashing, ordering, and numeric behavior correct for the domain?
- Question: When concurrency exists, are thread ownership, shared state, synchronization, interruption, and cancellation explicit?
- Question: Are side effects and external dependencies isolated enough for meaningful tests?
- Question: Is diagnostic output safe, bounded, consistent with project logging, and free of temporary instrumentation?
- Question: Do focused tests and project-native build checks cover the changed behavior and failure paths?
