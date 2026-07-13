---
name: electron-preload
description: Use when coding, reviewing, or testing Electron preload scripts, context bridge APIs, renderer exposure, IPC client contracts, or desktop trust boundaries.
metadata:
  category: stack-and-domain
---

# Electron Preload

Use this pack for the narrow bridge between the untrusted renderer and privileged Electron main process.

## Routing

- Load with Dev Coder for preload scripts, context bridge APIs, renderer-facing desktop capabilities, and IPC clients.
- Load with Dev Code Reviewer when a change broadens renderer authority or exposes new data.
- Combine with Electron Main, React Vite Renderer, and TypeScript ESM.

## Guidance

- Expose the smallest stable API the renderer needs.
- Validate inputs before crossing the main-process boundary.
- Keep secrets, filesystem authority, and process control out of renderer reach.
- Keep preload API names stable and explicit so tests and docs can describe the contract.

## Verification

- Run focused preload, renderer, and IPC tests.
- Build the app after changing preload exports or global declarations.
- Inspect both sides of the bridge when a preload contract changes.
