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

## Technology Fallbacks

- TypeScript may use temporary console output when the project has no logger. Use an identifiable prefix and remove it before completion.
- Java may use temporary language-native output only when no project logging facade is available. Spring Boot code should prefer its established logging facade.
- SQL should use transaction-safe diagnostic queries or the database's normal plan and session facilities when available.

Do not require a custom Tracer API, fixed logging format, dedicated sink, or external observability product.
