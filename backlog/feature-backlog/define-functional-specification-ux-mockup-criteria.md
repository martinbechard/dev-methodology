# Define Functional Specification UX Mockup Criteria

Status: Running

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/define-functional-specification-ux-mockup-criteria.md

Completion: direct-main

## Execution / Ownership

- Owner: Dev Orchestrator
- Canonical task: /root/process_backlog/orch_functional_spec_ux
- Artifact claim: define-functional-spec-ux-mockup-criteria, pending ARTIFACT GO.
- Branch: codex/define-functional-spec-ux-mockup-criteria
- Canonical worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/define-functional-spec-ux-mockup-criteria
- Phase: Lifecycle Running committed; ARTIFACT GO pending.
- Starting main: 1560326152977581d2c62711e9fb861e7f2cf8f0
- Lifecycle transition: Ready eligibility and exact approval were preserved before fresh ownership transitioned the item to Running.
- Candidate: Pending.
- Accepted commit: Pending.
- Claim wait started at: None.
- Claim wait attempts: 0.
- Integration wait started at: None.
- Integration wait attempts: 0.
- Completion wait started at: None.
- Completion wait attempts: 0.
- Open issues: None for lifecycle dispatch; implementation must remain within the recorded approval.
- Next owner: Dev Orchestrator.
- Delivery evidence: Exact governed and ordinary companion scope approval preserved; implementation, review, verification, integration, and acceptance remain pending.

## Read-Only Discovery

- Completed: Current functional-specification guidance and companion surfaces were inspected without artifact mutation.
- Artifact claim: None acquired.
- Candidate: None accepted.
- Artifact mutation: None performed.

## User Action Required

### Question For The User

Do you explicitly approve changing skills/create-functional-spec/SKILL.md to require a proportionate UX mockup only when documented interaction/layout complexity triggers defined criteria, while requiring a concrete no-mockup rationale for simple or non-visual specifications, with supported generated skill mirrors regenerated from that approved source?

### Why User Input Is Required

The completed read-only discovery identified one governed skill-definition path. Repository policy requires explicit scope-specific approval before its mutation.

### Non-Governed Companion Surfaces

- skills/development-methodology/assets/templates/functional-spec-template.md
- skills/review-functional-spec/references/review-checklist-functional-spec.md
- scripts/test_bundle_content.py

### Options And Tradeoffs

- Approve the exact governed path: permit the criteria change and supported generated mirror regeneration.
- Narrow the scope: preserve excluded behavior as unresolved work.
- Defer: retain the discovery evidence without implementation.

### Resolution

Approved on 2026-07-22. The user answered "ok" directly after the exact Question For The User in the parent turn. Provenance: parent coordination conversation for /root/process_backlog/orch_functional_spec_ux.

The approval covers exactly the governed path skills/create-functional-spec/SKILL.md and regeneration only of its supported generated mirrors.

The only ordinary non-governed companion surfaces covered by this direction are:

- skills/development-methodology/assets/templates/functional-spec-template.md
- skills/review-functional-spec/references/review-checklist-functional-spec.md
- scripts/test_bundle_content.py

The answer does not authorize changes to skills/review-functional-spec/SKILL.md or any other governed path.

### Unattended Work Boundary

The item is Ready for a fresh dispatch but is not Running. No artifact claim has been acquired. Work must stay within skills/create-functional-spec/SKILL.md, its supported generated mirrors, and the three ordinary non-governed companion surfaces recorded in the Resolution. Changes to skills/review-functional-spec/SKILL.md or any other governed path remain prohibited without separate approval.

## Summary

Define deterministic, evidence-based criteria for proportionate interface examples in functional specifications.

## Context

Functional specifications describe user-visible behavior across UI, API, event or message, and CLI interfaces. Examples must be proportionate to the documented interface and complexity. A UI mockup is one possible example, not mandatory HTML for every functional specification.

## Source Evidence

- Direct user authorization in the 2026-07-22 parent coordination request to create this Ready Feature item.
- Current functional-specification guidance in skills/create-functional-spec/SKILL.md, skills/review-functional-spec/SKILL.md, and skills/development-methodology/assets/templates/functional-spec-template.md.
- Fresh parent direction on 2026-07-22 broadened the ordinary requirement from UI mockups to proportionate interface examples while preserving the approved governed and companion-file scope.

## Requirements

- Define deterministic criteria for requiring proportionate examples from documented interface type and complexity.
- For UI behavior, use a mockup, wireframe, or interaction diagram when documented interaction or layout complexity requires a visual example.
- For API behavior, include a sample method, path, query, headers, authentication, and request together with response status, headers, body, and key validation, authentication, and conflict cases.
- For event or message behavior, include a sample payload and producer-consumer sequence.
- For CLI behavior, include a sample invocation, output, and failure.
- Allow simple or non-interactive behavior to use an explicit no-example rationale.
- Do not require HTML or a UI mockup for every functional specification.
- Keep creation guidance, functional-specification template, and review checklist contracts compatible.
- Add focused tests that distinguish required interface examples from justified no-example cases.
- Before mutating any governed skill definition, obtain exact scope-specific user approval and run the supported pre-mutation approval check.

## Acceptance Criteria

- Criteria can be applied consistently from documented interface type, interaction, layout, and behavioral complexity.
- A UI specification with qualifying interaction or layout complexity provides a proportionate mockup, wireframe, or interaction diagram and identifies its contract role.
- An API specification provides a coherent request and response example plus key validation, authentication, and conflict cases.
- An event or message specification provides a representative payload and producer-consumer sequence.
- A CLI specification provides a representative invocation, output, and failure.
- A simple or non-interactive specification can pass with a concrete no-example rationale.
- The compatible template and review checklist make the same requirement observable.
- Focused tests cover UI, API, event or message, CLI, and no-example criteria cases.
- Any governed definition mutation has durable exact scope-specific approval evidence and passes the supported pre-mutation check.

## Dependencies

None.

## Verification

- Inspect the canonical functional-specification creation, template, review, and checklist contracts before implementation.
- Run focused tests and bundle checks for every approved changed surface.
- Run git diff --check and obtain independent review of the exact change.

## Notes

UI mockups remain one proportionate example form. This work item does not prescribe HTML unless the approved criteria and evidence require it.
