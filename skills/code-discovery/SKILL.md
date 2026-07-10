---
name: code-discovery
description: Inspect code structure, callers, contracts, configuration, tests, and runtime paths before implementation or review without requiring a particular search or analysis tool. Use when the relevant change boundary, ownership, dependencies, or impact must be established from live repository evidence.
metadata:
  category: development-practice
---

# Code Discovery

Establish the smallest evidence-backed code scope before changing or judging it.

## Workflow

1. Read project guidance, manifests, source roots, test roots, and generated-file rules.
2. Locate the named behavior, public contract, entry point, or failing path.
3. Trace callers, dependencies, state changes, error ownership, configuration, and relevant tests.
4. Prefer the repository's available search and navigation tools. Use structure-aware search when available and useful, but keep a text-search and direct-reading fallback.
5. Test uncertain search patterns on a small known example before trusting an empty result.
6. Record inspected paths, evidence, remaining uncertainty, and the resulting scope decision.

## Boundaries

- Do not stop solely because an optional search tool is unavailable.
- Do not infer behavior from names when source and tests are available.
- Do not expand into unrelated cleanup.
- Treat generated output as derived unless project guidance says otherwise.
