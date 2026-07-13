---
name: typescript-esm
description: Use when coding, reviewing, or testing TypeScript projects that use ECMAScript modules, package module mode, modern imports and exports, Node ESM, or bundler ESM behavior.
metadata:
  category: stack-and-domain
---

# TypeScript ESM

Use this pack when TypeScript module format can affect runtime behavior, test execution, imports, exports, package metadata, or build output.

## Routing

- Load with Dev Coder for TypeScript source, scripts, tests, package metadata, and tsconfig changes.
- Load with Dev Code Reviewer when a change affects module boundaries, generated output, path aliases, or runtime startup.
- Combine with framework packs such as Electron, React Vite, Next.js, Node CLI, Jest, or Vitest.
- Combine with TypeScript for general implementation and review evidence.

## Guidance

- Treat compiler options, package metadata, bundler config, and runtime loader behavior as one boundary.
- Prefer explicit imports and exports that survive typecheck, bundling, and runtime execution.
- Check whether a value is type-only, runtime-only, or shared before changing imports.
- Avoid compatibility shims unless the project profile explicitly requires them.

## Verification

- Run the project typecheck or build command after module-boundary changes.
- Run focused tests for changed modules before broader test suites.
- Inspect startup paths when changing entrypoints, package exports, or generated output.

## Review Evidence

Read references/review-checklist-typescript-esm.md during code review and use Code Review Evidence to synthesize findings.
