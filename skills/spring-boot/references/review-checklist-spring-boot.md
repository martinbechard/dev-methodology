# Spring Boot Review Checklist

- Question: Are controller, service, domain, and persistence responsibilities placed at clear boundaries?
- Question: Are dependencies explicit, required, and injected through the project's established pattern?
- Question: Are request, configuration, and external data validated before entering trusted domain behavior?
- Question: Does transaction scope match one coherent business operation without proxy or lazy-loading surprises?
- Question: Are exceptions translated through the established API or messaging contract while preserving useful causes?
- Question: Are authentication, authorization, tenant, and data-access controls enforced at every material boundary?
- Question: Are configuration defaults, profiles, overrides, secrets, and startup validation handled safely?
- Question: Are AOT and native-image constraints for reflection, resources, serialization, proxies, and runtime bean registration handled when applicable?
- Question: Does logging use the existing facade, avoid sensitive payloads, and provide useful correlation and outcome evidence?
- Question: Do unit, slice, integration, and end-to-end tests cover the appropriate boundaries without redundant mocking?
- Question: Do build and test results cover wiring, serialization, security, persistence, transactions, packaged launch behavior, and native delivery affected by the change?
