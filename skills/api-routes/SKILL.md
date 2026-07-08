---
type: Skill
name: api-routes
description: Use when coding, reviewing, or testing API route handlers, HTTP request and response contracts, validation, auth boundaries, error semantics, or integration endpoints.
---

# API Routes

Use this pack for explicit HTTP boundaries. In Next.js projects, challenge new API routes unless an HTTP boundary is required.

## Routing

- Load with Coding Agent for route handlers, request parsing, response shaping, status codes, and integration endpoints.
- Load with Code Review Agent when a change affects external clients, auth, data validation, or error contracts.
- Combine with Next.js App Router, Clerk Auth, TypeScript Strict, Postgres Drizzle, Jest, and Playwright.

## Guidance

- Validate request data before side effects.
- Keep auth decisions close to the boundary.
- Return stable error shapes that callers can handle.
- Prefer server actions for in-app mutations when no external HTTP boundary is needed.

## Verification

- Run focused API tests for success, validation failure, auth failure, and domain errors.
- Run build or typecheck after route contract changes.
- Run affected E2E tests when API behavior is user-visible.
