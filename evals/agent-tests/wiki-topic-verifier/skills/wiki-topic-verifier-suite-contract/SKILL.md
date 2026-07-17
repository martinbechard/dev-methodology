---
name: wiki-topic-verifier-suite-contract
description: Share the canonical Wiki Topic Verifier evaluation contract between its supervisor and independent Judge.
metadata:
  category: evaluation
---

# Wiki Topic Verifier Suite Contract

Evaluate the target as a fresh-context read-only acceptance gate for supplied topic pages.

## Required Contract

- Require a complete created-or-updated page inventory and keep source files as evidence only.
- Check page sections, durable leaf granularity, navigational hubs, contextual source links, digests, federation, lint, and OKF when applicable.
- Require page-relative portable links for raw and processed evidence.
- Return exactly GOOD or NEEDS_CORRECTION with reviewed pages and concrete file-specific corrections.
- Treat a lint, OKF, stale-link, oversized-hub, or unresolved leaf defect as NEEDS_CORRECTION.
- Never edit the evaluated pages or evidence.

## Failure Conditions

- Verify the source artifact instead of the supplied topic pages.
- Return GOOD while an applicable deterministic or semantic gate fails.
- Accept bundled independently changing concepts without leaves or explicit deferral.
- Miss a stale or absolute source link.
- Perform a mutating repair from the read-only verifier.

## Semantic Dimensions

Judge page-scope discipline, leaf analysis, source and navigation integrity, check accuracy, correction actionability, and read-only compliance.
