---
name: typescript-strict
description: Use when coding, reviewing, or testing strict TypeScript projects that require precise domain types, no any usage, null safety, discriminated unions, or exact API contracts.
---

# TypeScript Strict

Use this pack when type quality is part of the project contract.

## Routing

- Load with Coding Agent for domain models, server code, UI props, API contracts, tests, and shared schemas.
- Load with Code Review Agent when a change weakens typing, introduces casts, or moves data across boundaries.
- Combine with framework, persistence, auth, and test packs.

## Guidance

- Model groups of fields as named types.
- Prefer discriminated unions for variant states and explicit result shapes.
- Avoid any and broad casts. If unknown input is real, validate and narrow it.
- Keep nullable, optional, and missing values semantically distinct.

## Verification

- Run typecheck or build after type changes.
- Run focused tests where runtime validation narrows unknown data.
- Inspect public interfaces and shared types after changing contracts.
