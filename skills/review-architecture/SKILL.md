---
name: review-architecture
description: Use when reviewing an architecture artifact for system scope, runtime assumptions, boundaries, dependency direction, cross-cutting concerns, and verification.
---

# Architecture Review

Use this skill to review an architecture artifact created from the methodology templates. An architecture document should explain the whole system or a cross-cutting concern without duplicating every module detail.

## Required Inputs

- The architecture artifact under review.
- The architecture template from development-methodology assets when available.
- Related source roots, tests, configuration, runtime metadata, procedures, high-level designs, module designs, and wiki pages.

## Workflow

1. Read the artifact and identify the system boundary, runtime assumptions, layers, components, and cross-cutting claims.
2. Read references/review-architecture-checklist.md.
3. Use documentation-page-verifier for shared page contract, source authority, link, diagram, and steady-state checks.
4. Verify architecture sections against the checklist, especially scope, stack, file organization, dependency direction, ownership, data movement, lifecycle, cross-cutting concerns, invariants, risks, and verification.
5. Return findings first, ordered by severity, with file paths and section names.

## Output

When problems exist, lead with review findings. When no problems are found, say the artifact passes architecture review and name any remaining source, boundary, or verification gaps.
