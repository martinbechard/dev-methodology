---
name: review-module-design
description: Use when reviewing a module design artifact for runtime path, responsibilities, contracts, dependencies, processing rules, errors, and verification evidence.
metadata:
  category: artifact-review
---

# Module Design Review

Use this skill to review a module design artifact created from the methodology templates. A module design should define one implementation unit precisely enough that code and tests can be understood or written from it without guessing.

## Required Inputs

- The module design artifact under review.
- The module design template from development-methodology assets when available.
- The authoritative inputs permitted by the artifact's selected design mode. For planned development this means accepted functional specifications, architecture, owning high-level design, decisions, backlog requirements, project configuration, and relevant technology guidance. For existing behavior it also includes source, callers, dependencies, tests, configuration, procedures, and runtime evidence.

## Workflow

1. Read the artifact and identify its design mode, authoritative inputs, requirements coverage, runtime path, responsibility, callers, dependencies, contracts, trust and identity boundaries, internal state, processing rules, error handling, implementation readiness, and verification claims.
2. Read references/review-checklist-module-design.md.
3. Build a source-traced operation-contract ledger independently from the candidate. Search every occurrence of each operation name, route, responsibility, and close synonym across the authoritative inputs before accepting any candidate OPEN claim. Bind every evidence item to the exact method and route, command, event, or job it names; do not transfer a sibling operation's response, validation, side effect, or failure contract.
4. Complete every applicable checklist question with status, quoted evidence, and assessment.
5. Save the completed review checklist next to the artifact using this form: artifact-name.review-checklist-module-design.md.
6. Use documentation-page-verify with the artifact, source evidence, and completed review checklist for shared page contract, source authority, link, diagram, and steady-state checks.
7. Verify module sections against the checklist, especially requirements coverage, runtime path, responsibilities, callers, dependencies, public contracts, identity selectors, authorization, response disclosure, validation ownership, state transitions, failure timing, sensitive logging, internal data, processing rules, invariants, configuration, external interfaces, UI behavior, readiness, and verification.
8. Preserve partial specificity during review. A source may establish an entity-shaped response, DTO projection, no body, or another category while leaving exact fields open. Treat a candidate that marks the entire response OPEN, or substitutes a general safer projection, as a finding.
9. Verify every stated field constraint and required or optional status, every claimed equivalence between similar routes, and every sensitive-input validation, handoff, protection, response-exclusion, failure-timing, and logging rule against the exact operation evidence. Unsupported cross-operation transfer is a review defect, including when it appears only as an open blocker.
10. Return findings first, ordered by severity, with file paths and section names. Separate Response Adequacy findings from Identity And Security findings, then report other contract or evidence findings. Derive each finding or pass assessment from the completed review checklist.

## Output

When problems exist, lead with review findings. When no problems are found, say the artifact passes module design review and name any remaining source, contract, decision, or test gaps. Do not pass a planned design with an unaccounted requirement, an unsupported critical contract, or a high-impact blocking question marked READY.
