---
name: clerk-auth
description: Use when coding, reviewing, or testing Clerk authentication, sessions, organization context, protected routes, server-side user lookup, auth middleware, or permission boundaries.
metadata:
  category: stack-and-domain
---

# Clerk Auth

Use this pack for Clerk-backed identity and access control in application code.

## Routing

- Load with Coding Agent for protected routes, server actions, route handlers, middleware, user lookup, and organization context.
- Load with Code Review Agent when auth decisions, session data, or tenant boundaries change.
- Combine with Next.js App Router, React Server Components, API Routes, and Playwright.

## Guidance

- Check authentication and authorization on the server before protected data access.
- Keep user identity, organization identity, and application permissions distinct.
- Avoid leaking secrets, tokens, session internals, or private user data to the client.
- Treat unauthenticated, unauthorized, and missing setup states as different outcomes.

## Verification

- Run focused tests for authenticated, unauthenticated, unauthorized, and tenant-boundary cases.
- Smoke-test protected user workflows when auth state is user-visible.
- Run build after middleware, route, or server action changes.
