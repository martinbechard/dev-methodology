---
name: react-vite-renderer
description: Use when coding, reviewing, or testing React renderer code in a Vite application, including Electron renderers, browser state, component composition, assets, and client-side interaction.
---

# React Vite Renderer

Use this pack for React user interfaces built through Vite, including Electron renderer surfaces.

## Routing

- Load with Coding Agent for components, hooks, renderer state, routing, assets, styles, and browser APIs.
- Load with Code Review Agent when a change affects user workflows, preload usage, state ownership, or client persistence.
- Combine with Electron Preload when the UI calls desktop APIs.

## Guidance

- Keep state ownership visible and local unless shared state is necessary.
- Prefer accessible controls and predictable interaction states.
- Treat preload and browser storage as external contracts.
- Avoid hiding runtime errors behind optimistic UI state.

## Verification

- Run focused component or renderer tests.
- Run the project build after imports, assets, or Vite config changes.
- Smoke-test changed workflows in the browser or Electron renderer when practical.
