---
name: electron-main
description: Use when coding, reviewing, or testing Electron main-process code, app lifecycle, windows, IPC handlers, background tasks, native resources, or desktop runtime startup.
metadata:
  category: stack-and-domain
---

# Electron Main

Use this pack for the trusted desktop runtime that owns application startup, windows, filesystem access, process lifecycle, and privileged integration points.

## Routing

- Load with Coding Agent for main-process source, preload registration, IPC handlers, menus, background jobs, and app startup.
- Load with Code Review Agent when a change affects trust boundaries, filesystem access, process execution, or user data locations.
- Combine with TypeScript ESM, Node CLI, local model integration, and project-specific runtime packs.

## Guidance

- Keep renderer concerns out of main-process modules unless the boundary is explicit.
- Treat IPC as a contract with validation, error semantics, and clear ownership.
- Prefer small lifecycle functions over hidden startup side effects.
- Keep paths, cache locations, and process management compatible with the host operating system rules.

## Verification

- Run focused main-process tests and the project build.
- Smoke-test app startup when lifecycle, window, IPC, or preload wiring changes.
- Inspect logs and user data paths when debugging startup or background runtime failures.
