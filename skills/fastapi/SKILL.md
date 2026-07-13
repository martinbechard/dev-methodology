---
name: fastapi
description: Implement, review, test, or diagnose FastAPI applications, routers, dependencies, validation, exception handling, lifespan behavior, and async boundaries. Use when Python scope is owned by a FastAPI project.
metadata:
  category: stack-and-domain
---

# FastAPI

Load Python with this skill.

## Application Boundaries

- Keep request and response models explicit and separate persistence or internal domain shapes when their contracts differ.
- Use dependency injection for request-scoped collaborators and cross-cutting policies.
- Translate domain failures to HTTP responses at the API boundary without losing useful causes in logs.
- Keep blocking work out of asynchronous request paths unless it is isolated behind an appropriate executor or synchronous endpoint.
- Put startup and shutdown ownership in lifespan handling.

## Routing And Validation

- Make status codes, response models, validation constraints, authentication requirements, and error bodies observable in the route contract.
- Avoid hidden side effects in dependencies and validators.
- Preserve framework-generated validation behavior unless the API contract intentionally replaces it.

## Verification

- Test routes through the ASGI application boundary with dependency overrides scoped to the test.
- Cover successful responses, invalid input, authorization failure, and translated domain failures.
- Verify asynchronous tests and lifespan behavior with the project's chosen test client and event-loop tooling.
