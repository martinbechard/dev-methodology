---
name: review-high-level-design
description: Use when reviewing a high-level design artifact for subsystem scope, component collaboration, data contracts, invariants, implementation order, and verification.
metadata:
  category: artifact-review
---

# High-Level Design Review

Use this skill to review a high-level design artifact created from the methodology templates. A high-level design should explain one coherent subsystem or feature family and how its constituent pieces collaborate.

For planned development, review the artifact as solution design. Accept a choice not stated verbatim upstream when it is a justified HLD proposition with explicit basis, necessity, and decision ownership. Treat unlabeled, contradictory, or unjustified specificity as a finding. Avoidable open questions and readiness blockers are findings.

Review whether the HLD prevents chaos at the next level of detail by providing one consistent coordination frame for components, ownership, contracts, dependencies, integration seams, implementation order, precise artifact placement, and complete package or module names. Reject placeholder paths and namespaces because they force downstream interpretation.

Require an appropriate Mermaid diagram whenever the HLD describes an ordered sequence of actions, handoffs, states, transitions, retries, recovery, scheduled phases, startup, shutdown, or dependent implementation steps. Accept prose and tables as supporting explanation, but treat a complete sequence carried only by prose, a numbered list, or a table as a readability and response-adequacy finding. Match the diagram to the relationship: sequence diagrams for ordered exchanges, state diagrams for named lifecycle states, and flowcharts for branches, decisions, recovery paths, or ordered phases.

## Required Inputs

- The high-level design artifact under review.
- The high-level design template from development-methodology assets when available.
- The authoritative inputs permitted by the artifact's selected design mode. For planned development this means accepted functional specifications, parent architecture, decisions, backlog requirements, project configuration, and relevant technology guidance. For existing behavior it also includes accepted module designs, source, tests, configuration, procedures, and runtime evidence.

For the high-level-design current reverse-engineering pass, accepted module designs, source, tests, configuration, procedures, runtime evidence, and project configuration are sufficient inputs. Intentionally absent later parent architecture, functional specifications, and wiki pages are not missing mandatory inputs.

## Workflow

1. Read the artifact and identify its design mode, authoritative inputs, requirements coverage, subsystem scope, constituent components, artifact-placement ledger, exact source and test paths, package or module namespaces, interactions, ordered action sequences and their diagrams, critical trust and identity boundaries, cross-module contract reconciliation, data anchors, principles, patterns, justified propositions, residual open questions, invariants, documentation acceptance, implementation readiness, and verification claims.
2. Read references/review-checklist-high-level-design.md.
3. Complete every applicable checklist question with status, quoted evidence, and assessment. Use exactly one allowed status: `pass`, `fail`, `question`, or `n/a`; never qualify a status with wording such as `pass with finding`. When a material finding applies, use `fail` or `question` and record any partial strengths in the assessment.
4. Save the completed review checklist next to the artifact using this form: artifact-name.review-checklist-high-level-design.md.
5. Use documentation-page-verify with the artifact, source evidence, and completed review checklist for shared page contract, source authority, link, diagram, and steady-state checks.
6. Verify high-level design sections against the checklist, especially requirements coverage, parent architecture, data anchors, constituent components, interaction model, trust boundaries, identity selectors, authorization, disclosure limits, cross-module contracts, validation and state ownership, transaction and asynchronous boundaries, error timing, configuration, implementation order, invariants, readiness, definition of good, and verification.
7. Perform operation inventory reconciliation before passing coverage. Enumerate every primary or supporting route, API, command, event, job, notification, and reference-data lookup named in any allowed input, then locate its Requirements Coverage row, owning component, boundary contract, and verification or its explicit out-of-scope authority. An unresolved facet does not justify omitting the supporting operation.
8. Judge documentation acceptance against source evidence, accepted module prerequisites, and current reverse-engineering pass requirements. Do not fail the artifact solely because later architecture, functional specifications, or wiki pages are intentionally absent, or because a known defect, open decision, or limitation is recorded accurately.
9. Judge implementation readiness separately. A review may accept the documentation while confirming BLOCKED implementation readiness; preserve the reason for downstream reconciliation and planning.
10. Return findings first, ordered by severity, with file paths and section names. Separate Response Adequacy findings from Identity And Security findings, then report other contract or evidence findings. Derive each finding or pass assessment from the completed review checklist.

## Output

When problems exist, lead with review findings. When no documentation-acceptance problems are found, say the artifact passes high-level design review, state its separate implementation-readiness result, and name any remaining subsystem, source, decision, or verification gaps. Do not pass a planned design with an unaccounted requirement or unsupported critical contract. An accurately recorded conflict or high-impact question may coexist with accepted documentation only when Implementation Readiness is BLOCKED for the affected downstream work.
