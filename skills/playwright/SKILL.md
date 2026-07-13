---
name: playwright
description: Use when creating, reviewing, debugging, or running Playwright end-to-end tests, browser workflows, authenticated flows, dev server coordination, page objects, traces, or UI regression checks.
metadata:
  category: stack-and-domain
---

# Playwright

Use this pack for browser-level workflows and E2E verification.

## Routing

- Load with Dev Browser Operator when browser state, dev servers, authenticated sessions, traces, or exclusive runtime resources are involved.
- Load with Dev Coder for small test edits that do not require browser ownership.
- Combine with Next.js App Router, Clerk Auth, Tailwind Design System, and Jest.

## Guidance

- Prefer user-visible locators and stable workflow assertions.
- Avoid arbitrary sleeps. Wait for real UI, network, or state conditions.
- Keep authentication setup explicit and reusable.
- Capture traces, console errors, and screenshots when diagnosing failures.

## Verification

- Run the targeted Playwright spec first.
- Use the project-designated environment for E2E work.
- Report server, auth, data, or browser setup blockers distinctly from test failures.
