# Spring Boot Order Cancellation Evaluation

Add an order-cancellation endpoint and persistence operation.

Use the simple-workitem delivery process. Complete and commit the verified local change
without publishing a branch or pull request.

Requirements:

- Add POST /orders/{id}/cancel.
- Keep HTTP mapping in the controller, cancellation rules in the service, and SQL in the repository.
- Cancel PENDING orders and return the resulting order.
- Treat cancellation of an already CANCELLED order as an idempotent success.
- Reject FULFILLED orders with a conflict response.
- Preserve the existing not-found response.
- Make the read and state transition one coherent transaction.
- Update only the expected current state so concurrent changes cannot be overwritten silently.
- Use parameterized SQL and return the persisted state.
- Add focused service tests and a Spring integration test covering persistence and response mapping.
- Use the existing logging and test facilities; do not add a tracing API, mocking framework, or logging format.
- Run Maven tests.

Save eval-result.md with Skills Used, Evidence Packet, and Review Synthesis sections. Include JAVA-CONTRACT, SPRING-BOUNDARY, SPRING-TRANSACTION, SQL-STATE, JAVA-TESTS, and REVIEW-SYNTHESIS evidence identifiers.
