# Spring Boot Design Review Checklist

- Question: Are application modules and public interactions aligned with cohesive business responsibilities?
- Question: Are controller, application, domain, persistence, messaging, and external-client responsibilities placed at boundaries that own the required knowledge?
- Question: Does transaction ownership match the required local consistency boundary without spanning avoidable remote work?
- Question: Are event delivery, ordering, duplication, and recovery guarantees explicit where modules communicate asynchronously?
- Question: Is the imperative, reactive, asynchronous, or virtual-thread execution model supported by the complete dependency chain?
- Question: Are authentication, authorization, tenant, data, and administrative trust boundaries explicit?
- Question: Are JVM, AOT, native-image, and container deployment constraints explicit where they affect dynamic behavior or operations?
- Question: Does the chosen architecture solve demonstrated coupling, deployment, scaling, ownership, or testability needs without speculative layers?
- Question: Are module dependencies, architecture rules, and the selected packaged deployment form verifiable through source, tests, Spring Modulith, ArchUnit, or equivalent evidence?
