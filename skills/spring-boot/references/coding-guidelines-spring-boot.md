# Spring Boot Coding Guidelines

## Version And Stack Awareness

- Confirm the exact managed platform and use documentation and APIs for that supported line.
- Preserve the project web, data, serialization, validation, security, and testing stack rather than introducing an alternative starter for convenience.
- Treat deprecation warnings as migration evidence. Do not replace an API until the target line and project compatibility plan support the replacement.

## Beans And Configuration

- Prefer constructor injection for required collaborators and keep optional dependencies explicit.
- Keep configuration classes focused and use non-proxied bean methods when inter-bean method calls are not required.
- Bind related settings through the established configuration-properties model and validate required values during startup.
- Keep secrets outside source and diagnostic output. Preserve the deployment environment's established secret provider.
- Avoid scattered value injection when one validated configuration type owns the settings.

## Web And Error Handling

- Keep transport mapping, validation, content negotiation, and HTTP status selection at the web boundary.
- Use request and response types that protect the public contract when entities or internal models differ.
- Preserve the application's Problem Details or other established error shape and prevent internal exception messages from leaking by default.
- Bound pagination and sorting input and map persistence results to stable response contracts.
- Keep blocking work out of WebFlux pipelines and keep reactive operations in one composed pipeline.

## Transactions And Asynchronous Work

- Apply transactional behavior through an intercepted Spring bean boundary; self-invocation does not create a separate proxy interaction.
- Account for default rollback behavior and declare checked-exception behavior when the business operation requires rollback.
- Do not assume thread-bound transactions, security context, logging context, or request context follow newly started threads.
- Use the appropriate imperative or reactive transaction manager for the method return type and data stack.
- Keep irreversible external side effects outside a database transaction unless an outbox, after-commit listener, or equivalent delivery contract owns consistency.

## Security And Operations

- Prefer Spring Security's supported authentication mechanisms, including OAuth2 Resource Server, over handwritten token filters when they satisfy the requirement.
- Select CSRF behavior from the credential transport and client model rather than from the word API.
- Enforce authorization at every material route, method, tenant, and data boundary.
- Restrict CORS origins, methods, headers, and credentials to the deployed trust boundary.
- Expose only required Actuator endpoints and secure any endpoint that can reveal operational or sensitive information.
- Preserve trace and correlation context across supported asynchronous boundaries without logging tokens or personal data.

## Verification

- Run the project wrapper and the focused test slice for the changed boundary.
- Add context tests only when auto-configuration, bean wiring, serialization, security, persistence, or transaction behavior must be proved.
- Verify startup configuration when properties, profiles, conditional beans, or auto-configuration change.
- Verify both success and translated failure behavior at the framework boundary.
