---
name: review-architecture
description: Use when reviewing an architecture artifact for system scope, runtime assumptions, boundaries, dependency direction, cross-cutting concerns, and verification.
metadata:
  category: artifact-review
---

# Architecture Review

Use this skill to review an architecture artifact created from the methodology templates. An architecture document should explain the whole system or a cross-cutting concern without duplicating every module detail.

For planned development, review architecture as solution design. Accept undefined architectural choices as justified propositions when compatible with authoritative constraints and accompanied by basis, necessity, and decision ownership. Treat unlabeled, contradictory, or unjustified choices as findings.

Review whether the architecture prevents chaos in high-level designs by giving them one coherent frame for runtime units, subsystem vocabulary, stack, repository roots, documentation homes, ownership, layers, dependency direction, data authority, integrations, trust boundaries, configuration, lifecycle, and implementation sequence. Avoidable open questions, conflicting frames, incomplete paths, and placeholder locations are findings.

Require an appropriate Mermaid diagram whenever a section describes two or more ordered actions or phases, or any handoff, data movement, lifecycle transition, branch, retry, recovery path, startup or shutdown dependency, or dependent implementation phase. Require a structural diagram when a section defines a non-tabular topology: one system-context, scope, ownership, layer, component, dependency, principle, risk, or verification node connects to two or more others; a dependency or ownership path spans three or more nodes; a cycle exists; containment spans two or more levels; or an edge crosses a system, trust, or runtime boundary. Prose, numbered lists, and tables may support a diagram but must not carry the complete qualifying relationship alone. Treat architecture-template section-specific triggers as additive minimums under the shared development-methodology rule; satisfying one section-specific trigger does not waive another shared trigger.

## Required Inputs

- The architecture artifact under review.
- The architecture template from development-methodology assets when available.
- Related source roots, tests, configuration, runtime metadata, procedures, high-level designs, module designs, and wiki pages.

For the architecture current reverse-engineering pass, accepted high-level designs and confirmed cross-cutting source evidence are the required prerequisites. Intentionally absent later functional specifications and wiki pages are not missing mandatory inputs.

## Workflow

1. Read the artifact and identify the system boundary, runtime assumptions, system-frame ledger, repository roots, layers, components, ownership, dependencies, data authority, integrations, trust boundaries, configuration, lifecycle, implementation sequence, qualifying structural and ordered relationships and their diagrams, justified propositions, residual open questions, cross-cutting claims, documentation acceptance, implementation readiness, and verification claims.
2. Read references/review-checklist-architecture.md.
3. Complete every applicable checklist question with status, quoted evidence, and assessment.
4. Save the completed review checklist next to the artifact using this form: artifact-name.review-checklist-architecture.md.
5. Use documentation-page-verify with the artifact, source evidence, and completed review checklist for shared page contract, source authority, link, diagram, and steady-state checks.
6. Verify architecture sections against the checklist, especially scope, stack, file organization, dependency direction, ownership, data movement, lifecycle, implementation sequence, diagrams, cross-cutting concerns, invariants, risks, and verification.
7. Judge documentation acceptance against source evidence, accepted HLD prerequisites, and current reverse-engineering pass requirements. Do not fail the artifact solely because later functional specifications or wiki pages are intentionally absent, or because a known defect, open decision, or limitation is recorded accurately.
8. Judge implementation readiness separately. A review may accept the documentation while confirming BLOCKED implementation readiness; preserve the reason for downstream reconciliation and planning.
9. Return findings first, ordered by severity, with file paths and section names. Derive each finding or pass assessment from the completed review checklist.

## Output

When problems exist, lead with review findings. When no documentation-acceptance problems are found, say the artifact passes architecture review, state its separate implementation-readiness result, and name any remaining source, boundary, decision, or verification gaps. A qualifying ordered or structural relationship left only in prose, a numbered list, or a table is a finding.
