# Quarkus Design Review Checklist

- Question: Are module responsibilities and public interactions aligned with cohesive business capabilities?
- Question: Are REST, messaging, scheduling, domain, persistence, and external-client responsibilities placed at boundaries that own the required knowledge?
- Question: Is the blocking, reactive, or virtual-thread execution model supported by the complete dependency chain?
- Question: Does transaction ownership match the required consistency boundary without spanning avoidable remote work?
- Question: Are event delivery, ordering, duplication, retry, and recovery guarantees explicit?
- Question: Are build-time augmentation, runtime configuration, reflection, resources, proxies, and native-image constraints accounted for?
- Question: Are authentication, authorization, tenant, data, and administrative trust boundaries explicit?
- Question: Do architecture and packaged-runtime checks verify the selected module and deployment design?
