---
name: jest
description: Use when creating, reviewing, debugging, or running Jest tests for TypeScript, React, Next.js, server logic, database boundaries, mocks, fixtures, or regression coverage.
metadata:
  category: stack-and-domain
---

# Jest

Use this pack for Jest unit and integration tests.

## Routing

- Load with Coding Agent when behavior changes need Jest coverage.
- Load with QA And Verification Agent when choosing focused commands, interpreting failures, or expanding coverage.
- Combine with TypeScript Strict, Next.js App Router, API Routes, Clerk Auth, Postgres Drizzle, and LangGraph.

## Guidance

- Test observable behavior and domain contracts.
- Keep mocks close to external boundaries, not internal logic.
- Prefer readable fixtures over sprawling setup.
- Cover failure modes when validating input, auth, persistence, or workflow state.
- For integration scenarios, connect setup, simulated dependency or clock, state transition, expected outcome, and negative path to source or plan evidence.
- Choose mocks only for real external or nondeterministic boundaries. Prefer spies for observation, keep doubles local, test complex fakes against their contract, and restore timers, globals, and mock state after each test.
- Reconcile generated tests with an existing unit test plan when the repository maintains one. Treat the plan as evidence, not as authority over live behavior and source.

## Verification

- Run focused Jest tests for the changed area first.
- Run broader Jest suites and build before completing code changes when the blast radius is wider.
- Treat failing tests as the current task until explained and fixed.
- Run repository-native commands and confirm aliases, transforms, environment, and module configuration before changing imports to satisfy the runner.
