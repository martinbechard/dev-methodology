# Define Functional Specification UX Mockup Criteria

Status: Completed

Type: Feature

Provider: file

Provider Reference: backlog/completed-backlog/features/define-functional-specification-ux-mockup-criteria.md

Completion: direct-main

## Execution / Ownership

- Owner: Dev Orchestrator
- Canonical task: 019f8b05-29c8-7a82-b962-1a347eebecc3
- Artifact claim: Integration claim functional-spec-ux-integration-019f8b05 released by event 64f27e75-1b84-400c-a2db-9c09db9b3fb9.
- Branch: codex/functional-spec-ux-integration-20260722
- Canonical worktree: /Users/martinbechard/.codex/worktrees/3362/dev-methodology
- Phase: Completed; integrated, verified on main, and archived through the file provider.
- Starting main: 1560326152977581d2c62711e9fb861e7f2cf8f0
- Lifecycle transition: Ready eligibility and exact approval were preserved before fresh ownership transitioned the item to Running.
- Candidate: 2398fdb3bcb0aed6a73b34e4b216bd315962d8c6 on codex/functional-spec-ux-resume-20260722.
- Accepted commit: 2398fdb3bcb0aed6a73b34e4b216bd315962d8c6.
- Claim wait started at: None.
- Claim wait attempts: 0.
- Integration wait started at: 2026-07-22T18:27:19Z.
- Integration wait attempts: Initial attempt and the five-minute retry returned SHARED_CHECKOUT_RELEASE_REQUIRED; the ten-minute retry acquired ownership. Blocking evidence preserved in events 9a87f285-75bd-4261-92d3-fb3c0aa9bf6b and 85f60977-584a-44be-abda-b7be224fee70; the second wait observed claim eval-playwright-629ee68.
- Completion wait started at: None.
- Completion wait attempts: 0.
- Open issues: None.
- Next owner: Parent coordinator for terminal task and clean worktree or branch cleanup.
- Delivery evidence: Accepted source 2398fdb3bcb0aed6a73b34e4b216bd315962d8c6 was replayed onto current main 817a34c31304312fb38f2e2c9c2a793306ecb646 as integration commit ca1b7960497251a75db97c80dc612f89ed8e4859, verified on main, and released from integration ownership.

## Cold-Start Recovery Execution — 2026-07-22

- Canonical task identity reconciled to 019f8b05-29c8-7a82-b962-1a347eebecc3.
- Backlog recovery claim: cold-start-backlog-reconcile-2-019f8b00, acquired event 66822334-e85a-41aa-b2ad-6a6c433b6798 from primary main.
- Recovery phase: cold-start current-main reconciliation.
- Prior exact approval evidence and acceptance criteria remain preserved.

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

## Completion Evidence — 2026-07-22

- Approval gate: The supported pre-mutation check returned ALLOWED_APPROVED_DEFINITION_CHANGE for skills/create-functional-spec/SKILL.md using the recorded exact delegated user direction. The supported generated skill mirror check returned ALLOWED_APPROVED_REGENERATION. The generated template mirror remained an ordinary generated companion of the approved template surface.
- Current-main reconciliation: The replacement task began from recorded main 5d6a2e60b8382888c5c53bc35bed686749d71912. Intervening main changes affected backlog-only surfaces until integration; no approved product path overlapped. The fresh integration branch was created from main 817a34c31304312fb38f2e2c9c2a793306ecb646.
- Accepted source: Candidate 2398fdb3bcb0aed6a73b34e4b216bd315962d8c6 changes exactly the approved creation skill, functional-specification template, review checklist, focused bundle test, and supported generated mirrors.
- Independent review: The first fresh reviewer found that the checklist would force each artifact to quote a global methodology disclaimer. The candidate was corrected so the checklist assesses proportionate selection while the global policy remains in skill and template guidance. A second fresh reviewer returned ACCEPT with no material findings on 2398fdb3bcb0aed6a73b34e4b216bd315962d8c6.
- Independent verification: A fresh verifier passed Agent Skill validation for create-functional-spec, review-functional-spec, and development-methodology; the focused interface-example regression; the supporting-operation-inventory regression; the objective diagram and repository path-tree regression; build-skill-docs freshness; changed-commit whitespace checks; exact six-file scope; and clean candidate state under Python 3.11.13.
- Environment note: The default Python 3.9 interpreter failed before test collection because tomllib was unavailable. The repository-compatible Python 3.11 interpreter ran every accepted Python check successfully.
- Verification tier: Tier 1 was selected because this is a bounded skill, template, checklist, generated-mirror, and focused-test change. The full scripts, project-wiki, and live catalog campaigns were not required for this item.
- Integration mapping: Source 2398fdb3bcb0aed6a73b34e4b216bd315962d8c6 was cherry-picked without conflict onto current main as ca1b7960497251a75db97c80dc612f89ed8e4859. Main fast-forwarded to that commit.
- Main observation: Local branch main was clean at ca1b7960497251a75db97c80dc612f89ed8e4859, and the integration commit was directly reachable from main. This repository's selected local direct-main contract did not require remote publication.
- Post-integration verification: From the primary main checkout, Agent Skill validation passed; the three focused Python 3.11 regressions passed; build-skill-docs reported current generated data; git diff --check passed; and the six integrated paths matched the accepted scope.
- Integration claim: functional-spec-ux-integration-019f8b05 acquired by event 2042a0ce-18bf-4db3-adb2-31b2eaf6512e and released cleanly by event 64f27e75-1b84-400c-a2db-9c09db9b3fb9 with resulting commit ca1b7960497251a75db97c80dc612f89ed8e4859.
- Provider transaction: functional-spec-ux-closeout-019f8b05 acquired the exact active and completed provider paths by event 25e8c480-9e3a-4613-8c92-5aac41503cc0. This terminal record and archive movement are committed under that claim before its clean release.
- Cleanup eligibility: codex/functional-spec-ux-integration-20260722 is fully merged into main. The clean task worktree may be removed and the merged integration branch deleted after provider release. The source mapping above preserves candidate provenance; codex/functional-spec-ux-resume-20260722 has no unique unintegrated content after that mapping is confirmed.
