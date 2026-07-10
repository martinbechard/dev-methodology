# TypeScript Coding Review Checklist

- Question: Do changed public and domain contracts use precise named types without unjustified any or broad casts?
- Question: Are unknown, optional, nullable, and missing values validated and handled according to their distinct meanings?
- Question: Are async operations awaited, returned, cancelled, or deliberately detached with explicit ownership?
- Question: Are errors propagated, translated, logged, or recovered at the correct boundary?
- Question: Are mutation, I/O, global state, time, randomness, and other side effects isolated and testable?
- Question: Do imports, exports, package mode, compiler settings, and runner behavior agree?
- Question: Do tests cover observable behavior, invalid boundaries, failures, and relevant state transitions?
- Question: Is temporary console or diagnostic instrumentation safe, identifiable, bounded, and removed before completion?
- Question: Do typecheck, focused tests, and the applicable build provide evidence for the changed scope?
