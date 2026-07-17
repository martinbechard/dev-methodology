---
name: typescript
description: Use when implementing, refactoring, testing, or reviewing TypeScript code across server, browser, CLI, or shared packages, including runtime validation, async behavior, side effects, errors, and review evidence.
metadata:
  category: stack-and-domain
---

# TypeScript

## Coding Guidance

- Read tsconfig, package metadata, runtime entry points, and the local module convention before editing.
- Model domain concepts with precise named types and keep missing, optional, nullable, and invalid states distinct.
- Accept unknown at untrusted boundaries, validate it, and narrow before use.
- Keep casts local and evidence-backed. Do not use any to bypass a contract.
- Make async ownership explicit. Await required work, propagate or translate errors intentionally, and avoid floating promises.
- Keep mutation and side effects at named boundaries. Prefer explicit inputs and results for domain logic.
- Preserve import, export, package, build, and test-runner compatibility.
- Use existing logging first. When runtime evidence is unavailable, temporary console output is acceptable with an identifiable prefix, safe values, and mandatory cleanup.
- Add focused behavior tests and run typecheck or build plus the relevant test command.
- When a Gang of Four pattern is explicit, combine its generic pattern skill with TypeScript Design Pattern Examples instead of treating a class-heavy Java shape as canonical.

## Review Evidence

Read references/review-checklist-typescript.md during code review. Use Code Review Evidence to extract and synthesize the results.

Combine with TypeScript Strict or TypeScript ESM when their narrower rules apply.
