---
name: react-server-components
description: Use when coding, reviewing, or testing React Server Components, client component boundaries, server actions, serialization, data fetching, or component composition in Next.js.
metadata:
  category: stack-and-domain
---

# React Server Components

Use this pack when React component placement across server and client boundaries affects behavior.

## Routing

- Load with Dev Coder for server components, client components, server actions, form flows, and serialized props.
- Load with Dev Code Reviewer when moving logic across the server-client boundary.
- Combine with Next.js App Router, Clerk Auth, Postgres Drizzle, and Tailwind Design System.

## Guidance

- Keep server-only data access in server components, actions, or server modules.
- Add client boundaries only for browser APIs, local interactivity, or client state.
- Ensure props crossing into client components are serializable and intentionally shaped.
- Avoid fetching the same data in parallel boundaries without a reason.

## Verification

- Run build or typecheck after boundary changes.
- Run tests for server actions, forms, and affected routes.
- Smoke-test interactive paths after adding or moving client components.
