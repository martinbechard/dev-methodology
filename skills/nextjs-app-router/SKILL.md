---
name: nextjs-app-router
description: Use when coding, reviewing, or testing Next.js App Router projects, including app routes, layouts, loading and error boundaries, metadata, server actions, routing, and deployment build behavior.
metadata:
  category: stack-and-domain
---

# Next.js App Router

Use this pack for Next.js applications using the app directory and route segment model.

## Routing

- Load with Dev Coder for app routes, layouts, metadata, loading states, error boundaries, server actions, and route handlers.
- Load with Dev Code Reviewer when a change affects rendering mode, caching, auth boundaries, or deployment behavior.
- Combine with React Server Components, TypeScript Strict, Clerk Auth, Tailwind Design System, Jest, or Playwright.

## Guidance

- Prefer server components and server actions for application workflows when the project allows them.
- Use route handlers for external integrations, webhooks, machine clients, or explicit HTTP boundaries.
- Keep data fetching, auth checks, cache behavior, and mutation boundaries visible.
- Avoid duplicating business behavior across server actions and route handlers.

## Verification

- Run the project build after App Router structure, imports, metadata, or server action changes.
- Run focused tests for changed routes and affected user workflows.
- Smoke-test navigation, loading, error, and auth states when user-visible behavior changes.
