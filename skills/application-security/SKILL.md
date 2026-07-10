---
name: application-security
description: Review application trust boundaries, identity, authorization, validation, data exposure, secrets, dependency risk, logging, and side-effect authority without assuming a particular language, framework, identity provider, or persistence system. Use for security review, threat analysis, exploitability assessment, or security-focused code review.
metadata:
  category: development-practice
---

# Application Security

Trace plausible attack paths from untrusted input to protected data or side effects.

## Workflow

1. Identify assets, actors, trust boundaries, entry points, protected operations, and sensitive data.
2. Route specialized security, transport, identity, and persistence guidance from repository evidence.
3. Trace authentication, authorization, validation, state changes, logging, and failure behavior through the real path.
4. Confirm exploit preconditions and observable impact before assigning severity.
5. Record tight evidence, correction ownership, verification, and residual risk.

## Review Principles

- Keep authentication, authorization, tenancy, ownership, and data filtering distinct.
- Validate untrusted values before protected reads or side effects.
- Limit authority and data exposure to the minimum required scope.
- Prevent secrets and sensitive payloads from entering logs, errors, clients, or model-facing data.
- Preserve audit evidence without creating a second sensitive-data leak.
- Treat missing evidence as uncertainty, not proof of safety.

## Review Evidence

Read references/review-checklist-application-security.md during security review.
