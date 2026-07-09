---
name: tailwind-design-system
description: Use when coding, reviewing, or testing Tailwind CSS design systems, tokens, responsive layouts, component styling, accessibility states, or consistent UI surfaces.
---

# Tailwind Design System

Use this pack for Tailwind-based UI styling that should remain consistent across an application.

## Routing

- Load with Coding Agent for component styling, layout, responsive states, tokens, themes, and visual variants.
- Load with UX Reviewer when the work needs independent usability or visual review.
- Combine with React Server Components, React Vite Renderer, Next.js App Router, Jest, and Playwright.

## Guidance

- Use existing tokens, spacing, typography, and component patterns before adding new ones.
- Keep repeated visual decisions in shared components or variants.
- Verify responsive behavior for dense operational screens and mobile views.
- Preserve visible focus, disabled, loading, empty, and error states.

## Verification

- Run component or E2E tests for changed workflows when available.
- Inspect affected breakpoints and interaction states.
- Run build after Tailwind config, class generation, or component import changes.
