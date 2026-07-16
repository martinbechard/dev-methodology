# Spring Boot Testing Review Checklist

- Question: Is each test using the smallest Spring or non-Spring boundary that proves its claimed behavior?
- Question: Are test annotations and bean-replacement mechanisms supported by the configured Spring line?
- Question: Do database and external-service replacements provide enough fidelity for the behavior under test?
- Question: Are profiles, properties, contexts, ports, clocks, identifiers, and mutable fixtures deterministic and isolated?
- Question: Do tests cover validation, authentication, authorization, translated failures, transaction outcomes, and side-effect timing where applicable?
- Question: Are assertions about observable behavior rather than incidental implementation calls?
- Question: Does context reuse remain safe without unnecessary dirty-context resets or order dependence?
- Question: Does container lifecycle remain valid for the cached application context and dependent bean shutdown behavior?
- Question: Do packaged JAR, container, AOT, or native-image tests cover delivery-specific risks when applicable?
- Question: Does the reported evidence identify the test layer, application context, artifact form, database engine, external services, and commands that actually ran?
