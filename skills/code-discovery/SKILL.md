---
name: code-discovery
description: Inspect code structure, callers, contracts, configuration, tests, and runtime paths before implementation or review without requiring a particular search or analysis tool. Use when the relevant change boundary, ownership, dependencies, or impact must be established from live repository evidence.
metadata:
  category: development-practice
---

# Code Discovery

Establish the smallest evidence-backed code scope before changing or judging it.

## Discover Code Context

1. Apply the project instructions already in context, then inspect manifests, source roots, test roots, and generated-file rules.
2. Locate the named behavior, public contract, entry point, or failing path.
3. Trace callers, dependencies, state changes, error ownership, configuration, and relevant tests.
4. Prefer the repository's available search and navigation tools. Use structure-aware search when available and useful, but keep a text-search and direct-reading fallback.
5. Test uncertain search patterns on a small known example before trusting an empty result.

## Determine Change Scope

Use the discovered context to record inspected paths, evidence, remaining uncertainty,
and the resulting scope decision.

## Contract Authority

- Separate explicit public constraints in accepted authority from implementation conveniences, representation choices, and inferred preferences.
- Record the complete allowed input and output domains before designing validation. An inclusive numeric range permits fractional values unless accepted authority explicitly limits values to integers or a stated precision.
- Treat a material public constraint that remains ambiguous as an open decision. If the broader authorized behavior cannot be preserved safely, report the required decision as a blocker instead of inventing a validation rule.

## Boundaries

- Do not stop solely because an optional search tool is unavailable.
- Do not infer behavior from names when source and tests are available.
- Do not expand into unrelated cleanup.
- Treat generated output as derived unless project guidance says otherwise.
