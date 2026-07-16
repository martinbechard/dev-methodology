---
name: mockito
description: Create, diagnose, or review Mockito test doubles using explicit mock boundaries, strict stubbing, focused verification, argument matching, captors, spies, and lifecycle control.
metadata:
  category: stack-and-domain
---

# Mockito

Combine with Java, the detected test framework, and any application-framework testing skill. Mockito owns test-double mechanics; those skills own test lifecycle and framework runtime boundaries.

## Mockito Boundary

- Mock external, nondeterministic, slow, or otherwise controlled collaborators at an intentional boundary.
- Prefer real values and lightweight fakes when they express behavior more clearly than interaction scripts.
- Use strict stubbing and remove unused or over-broad stubs instead of weakening strictness globally.
- Verify only interactions that are part of the observable contract; do not restate every stub as a verification.
- Keep matchers consistent and captors focused on values that cannot be asserted through returned state.
- Treat spies, partial mocks, static mocks, construction mocks, deep stubs, and reset operations as exceptional design signals.

Read [Mockito Mocking Guidelines](references/mocking-guidelines-mockito.md) when implementation or diagnosis needs detailed stubbing, verification, matcher, captor, spy, or lifecycle rules.

## Verification

- Initialize mocks through the owning test framework's supported integration and preserve fresh mock state per test.
- Cover collaborator success, rejection, failure, retry, ordering, and non-interaction only when those behaviors are contractual.
- Run the narrow affected tests, then the owning module or project suite.
- Report which boundaries were mocked, which integrations remained real, and the exact commands executed.

## Review Evidence

Read references/review-checklist-mockito.md during test review. Use Code Review Evidence to extract and synthesize the results.
