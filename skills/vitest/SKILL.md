---
name: vitest
description: Use when creating, reviewing, debugging, or running Vitest unit and integration tests for TypeScript, Vite, React, Electron-adjacent modules, or Node code.
metadata:
  category: stack-and-domain
---

# Vitest

Use this pack for Vitest test design, focused test execution, mocks, fixtures, and failure diagnosis.

## Routing

- Load with Dev Coder when adding or updating tests for behavior changes.
- Load with Dev Verifier when choosing focused test commands and interpreting failures.
- Combine with React Vite Renderer, TypeScript ESM, Electron Main, or Node CLI based on the code under test.

## Guidance

- Test behavior at the smallest useful boundary.
- Prefer real parsing, validation, and state transitions over broad mocks.
- Keep fixtures readable and tied to the contract under test.
- Treat failing tests as implementation work until the root cause is understood.
- For integration scenarios, connect setup, simulated dependency or clock, state transition, expected outcome, and negative path to source or plan evidence.
- Choose mocks only for real external or nondeterministic boundaries. Prefer spies for observation, keep doubles local, test complex fakes against their contract, and restore timers, globals, and mock state after each test.
- Reconcile generated tests with an existing unit test plan when the repository maintains one.

## Verification

- Run the focused Vitest target first.
- Run broader tests or build before completing code changes.
- Report skipped or environment-blocked tests explicitly.
