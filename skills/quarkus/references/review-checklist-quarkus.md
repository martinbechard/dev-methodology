# Quarkus Review Checklist

- Question: Are the Quarkus platform, Java release, extensions, and packaging targets read from the owning build rather than assumed?
- Question: Are build-time-fixed and runtime-overridable configuration handled according to their actual lifecycle?
- Question: Are CDI scopes, injection points, bean discovery, unused-bean removal, and intercepted method boundaries correct?
- Question: Does every REST, messaging, scheduling, and persistence path keep blocking work off event-loop threads?
- Question: Does transaction behavior match the blocking or reactive persistence model and the intended rollback contract?
- Question: Are validation, error translation, authentication, authorization, tenant isolation, and data controls enforced at material boundaries?
- Question: Are logs, metrics, traces, health endpoints, and management surfaces bounded and free of sensitive data?
- Question: Do focused tests, startup checks, packaged-runtime checks, and native checks cover the deployment forms affected by the change?
