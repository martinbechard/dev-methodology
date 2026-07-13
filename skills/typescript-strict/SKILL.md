---
name: typescript-strict
description: Use when coding, reviewing, or testing strict TypeScript projects that require precise domain types, no any usage, null safety, discriminated unions, or exact API contracts.
metadata:
  category: stack-and-domain
---

# TypeScript Strict

Use this pack when type quality is part of the project contract.

## Routing

- Load with Dev Coder for domain models, server code, UI props, API contracts, tests, and shared schemas.
- Load with Dev Code Reviewer when a change weakens typing, introduces casts, or moves data across boundaries.
- Combine with framework, persistence, auth, and test packs.
- Combine with TypeScript for general implementation and review evidence.

## Guidance

- Model groups of fields as named types.
- Prefer discriminated unions for variant states and explicit result shapes.
- Avoid any and broad casts. If unknown input is real, validate and narrow it.
- Keep nullable, optional, and missing values semantically distinct.

## Verification

- Run typecheck or build after type changes.
- Run focused tests where runtime validation narrows unknown data.
- Inspect public interfaces and shared types after changing contracts.

## Review Evidence

Read references/review-checklist-typescript-strict.md during code review and use Code Review Evidence to synthesize findings.
