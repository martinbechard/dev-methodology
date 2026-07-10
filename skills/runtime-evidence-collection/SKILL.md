---
name: runtime-evidence-collection
description: Use when a defect or execution path requires temporary runtime observations from existing logs, debuggers, language-native output, processes, requests, or data while avoiding proprietary tracing dependencies.
metadata:
  category: development-practice
---

# Runtime Evidence Collection

## Workflow

1. State the runtime question and the minimum observations needed to answer it.
2. Prefer existing project logging, diagnostics, tests, and process output.
3. If evidence is still missing, add the smallest temporary language-native observation at meaningful boundaries.
4. Capture correlation, branch choice, relevant state, outcome, and error information without secrets, PII, tokens, or unnecessary payloads.
5. Bound event count, payload size, depth, duration, and retention.
6. Reproduce the behavior and preserve the evidence needed for diagnosis.
7. Remove temporary instrumentation and rerun the relevant test or build.

## Portable Fallbacks

- Prefer the project's established logging and diagnostic facilities.
- When none exist, use temporary language-native output with an identifiable prefix, safe values, bounded volume, and mandatory cleanup.
- For persistence behavior, use transaction-safe diagnostic reads and the data store's normal plan or session facilities when available.

Do not require a custom Tracer API, fixed logging format, dedicated sink, or external observability product.
