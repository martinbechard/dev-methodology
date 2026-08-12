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

Review artifact identity before content depth. Confirm the repository taxonomy classifies the target path, filename pattern, identifier, and prefix as architecture; confirm it is not mislabeled or placed as an HLD. Verify that child HLDs reference this architecture as their parent and that the architecture does not depend on a child HLD for normative authority. Evidence may flow bottom up during reverse engineering, but accepted authority remains architecture to HLD to component or module design without circular references.

Treat detailed operation contracts, leaf-module assignments, and implementation sequencing as HLD or component-design responsibilities when they do not establish a project-wide rule. Their presence is a finding when it makes the architecture depend on child-detail ownership or obscures the system-wide authority boundary. A fixed structured workflow artifact such as docs/architecture/architecture-design.yaml is not the durable Markdown architecture merely because it shares the directory.

Require an appropriate Mermaid diagram whenever a section describes two or more ordered actions or phases, or any handoff, data movement, lifecycle transition, branch, retry, recovery path, startup or shutdown dependency, or dependent implementation phase. Require a structural diagram when a section defines a non-tabular topology: one system-context, scope, ownership, layer, component, dependency, principle, risk, or verification node connects to two or more others; a dependency or ownership path spans three or more nodes; a cycle exists; containment spans two or more levels; or an edge crosses a system, trust, or runtime boundary. Prose, numbered lists, and tables may support a diagram but must not carry the complete qualifying relationship alone. Treat architecture-template section-specific triggers as additive minimums under the shared route-documentation-work rule; satisfying one section-specific trigger does not waive another shared trigger.

## Required Inputs

- The architecture artifact under review.
- The repository placement taxonomy that classifies its path, identifier, and prefix.
- The architecture template from route-documentation-work assets when available.
- Related source roots, tests, configuration, runtime metadata, procedures, high-level designs, module designs, and wiki pages.

For the architecture current reverse-engineering pass, accepted high-level designs and confirmed cross-cutting source evidence are the required prerequisites. Intentionally absent later functional specifications and wiki pages are not missing mandatory inputs.

## Completed Checklist Evidence

For every applicable question record:

- Status: pass, fail, question, or n/a.
- Question: the objective question being answered.
- Evidence type: exact quotation, summary, assessment, or not applicable.
- Evidence source: the named artifact, input, checklist, or retained response.
- Evidence: literal source text for an exact quotation, or clearly labeled summary, assessment, or not-applicable explanation.
- Assessment: the judgment grounded in the recorded evidence.

Use exactly one allowed status and never qualify a status with wording such as pass with finding. Do not mark pass without evidence. When a material finding applies, use fail or question and record any partial strengths in the assessment. Use exact quotation only for literal source text that occurs in the named evidence source. For a mode-dependent n/a, use Evidence type: not applicable and explain why the question does not apply rather than fabricating a quotation. When a required contract is missing, use summary or assessment evidence to describe the gap and mark the item fail; there is no literal source text to quote.

## Workflow

1. Read the repository taxonomy and artifact, then identify its architecture path and identifier classification, child-HLD convention and references, authority direction, system boundary, runtime assumptions, system-frame ledger, repository roots, layers, components, ownership, dependencies, data authority, integrations, trust boundaries, configuration, lifecycle, implementation sequence, qualifying structural and ordered relationships and their diagrams, justified propositions, residual open questions, cross-cutting claims, documentation acceptance, implementation readiness, and verification claims.
2. Read references/review-checklist-architecture.md.
3. Complete every applicable checklist question with the Completed Checklist Evidence fields.
4. Save the completed review checklist next to the artifact using this form: artifact-name.review-checklist-architecture.md.
5. Use verify-documentation-page with the artifact, source evidence, and completed review checklist for shared page contract, source authority, link, diagram, and steady-state checks.
6. Verify architecture sections against the checklist, especially scope, stack, file organization, dependency direction, ownership, data movement, lifecycle, implementation sequence, diagrams, cross-cutting concerns, invariants, risks, and verification.
7. Judge documentation acceptance against source evidence, accepted HLD prerequisites, and current reverse-engineering pass requirements. Do not fail the artifact solely because later functional specifications or wiki pages are intentionally absent, or because a known defect, open decision, or limitation is recorded accurately.
8. Judge implementation readiness separately. A review may accept the documentation while confirming BLOCKED implementation readiness; preserve the reason for downstream reconciliation and planning.
9. Return findings first, ordered by severity, with file paths and section names. Derive each finding or pass assessment from the completed review checklist.

## Output

When problems exist, lead with review findings. When no documentation-acceptance problems are found, say the artifact passes architecture review, state its separate implementation-readiness result, and name any remaining source, boundary, decision, or verification gaps. A qualifying ordered or structural relationship left only in prose, a numbered list, or a table is a finding.
