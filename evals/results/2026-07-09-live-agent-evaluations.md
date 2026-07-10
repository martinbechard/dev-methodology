# Live Agent Evaluation Results

## TypeScript Order Pricing

- Outcome: PASS
- Agent behavior: implemented the coupon boundary with a behavior-first loop, then produced a checklist-backed evidence packet and review synthesis.
- Verification: eight tests passed and the TypeScript project built successfully.
- Required evidence: TS-BOUNDARY, TS-CONTRACT, TS-ASYNC, TS-TESTS, and REVIEW-SYNTHESIS were present.
- Residual note: the project is deliberately synthetic and does not evaluate framework-specific HTTP behavior.

## Spring Boot Order Cancellation

- Outcome: PASS
- Agent behavior: implemented controller, service, transaction, repository, and conditional SQL behavior with service and Spring integration tests, then produced a checklist-backed evidence packet and review synthesis.
- Verification: ten Maven tests passed, including persisted-state, success, conflict, and not-found scenarios.
- Required evidence: JAVA-CONTRACT, SPRING-BOUNDARY, SPRING-TRANSACTION, SQL-STATE, JAVA-TESTS, and REVIEW-SYNTHESIS were present.
- Residual note: the conditional state transition was tested against H2; a true two-connection race and database-specific isolation behavior remain outside this fixture.

## TypeScript Code Review

- Outcome: PASS
- Agent behavior: independently reviewed a deliberately defective implementation in a read-only sandbox, loaded the applicable coding checklists, extracted evidence before synthesis, and did not modify the project.
- Findings: correctly identified the unawaited coupon result, swallowed provider failure, and missing percentage range validation as three high-impact correctness defects.
- Verification: strict typechecking passed while all three focused runtime tests failed for the expected behavioral reasons.
- Review quality: findings were prioritized, tied to tight source and test locations, supported by observed runtime evidence, and separated from residual risk.
- Adapter discovery: the friendly Codex alias luna was rejected by the CLI. The adapter mapping was corrected to the concrete gpt-5.6-luna identifier before the passing run.

## Execution Context

- Date: 2026-07-09
- Agent harness: Codex CLI 0.144.1 with concrete Codex model identifiers
- Fixture versions: TypeScript 7.0.2 and Spring Boot 4.1.0
- Repository sources were mounted read-only for the live agents. Implementations and full evidence packets remained in disposable working directories under /tmp.
