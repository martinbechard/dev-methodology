# Enforce Documentation Template Conformance

Status: Blocked

Type: Defect

## Running Ownership

- Owner: Dev Orchestrator root task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Lifecycle agent: Dev Backlog Steward.
- Lifecycle claim: enforce-documentation-template-conformance-start.
- Claim evidence: PRIMARY exact-file backlog ownership acquired at 2026-07-19T11:50:25.523351Z from clean baseline commit 1ee72be549619d0eb3fe3e0a769d1d97865d6ba4.
- Scope boundary: this claim owns only the Running transition and is released after its clean commit. Project source, evaluation artifacts, generated outputs, verification, and integration remain gated on a later ARTIFACT GO.

## Blocked Evidence

- Outcome: the bounded two-attempt post-integration correction authority ended with two failed fresh reviews. No third correction attempt is authorized.
- Accepted contribution chain: commits 503a787decb68a8f575338835509d31c3a4a5191, 1e5642eb78b8652629be3a68db820a9ce096031d, 57e906985eed0cad9d1075a9fede69a5b0930ac7, and 3ae73817974fd23db90d911691a451443d1af910 were deliberately integrated on main through commits 1eac75f504c728295e475117ae271e1aa532219f, c72b35ff92c6333c9f611d0ccaf295785565b1c3, eaf148d472ee2a0ea6d282ecbaf8e966a459066f, and c1b551f0874dae1a6bda0b3d306880f634af2d6c.
- Preserved correction chain: correction attempts are preserved in commits 12edbbcab5a683c69f6817a1e5272a5f9f11a41d and e2f80255dab559de87aaea7538a38a896f98c60e on branch codex/enforce-documentation-template-conformance-postintegration-correction-1. The correction claim released normally under event de47203b-dd7e-42a7-8d63-159d295dc217.
- Final Methodology Artifact Review failure: the contribution references deterministic check IDs that are not defined in evals/judges.yaml; command detection still misses executable forms such as node tools/check.js; reference-style external Markdown destinations bypass evidence validation; and contradictory coverage claims remain incompletely detected through anaphora, HTML comments, and nested blockquotes.
- Final Dev Code Review failure: command inventory still both accepts prose as commands and rejects valid prefixed or wrapped commands; coverage synonyms and anaphora remain incomplete; Markdown reference destinations can bypass validation while unrelated URI forms are over-rejected; and HTML-comment and nested-blockquote visibility remains misclassified.
- Verification boundary: 36 focused tests, the fixture-source test, selected and full suite validate-only checks, and diff, scope, and bytecode-cache audits passed. Those deterministic results do not override the two failed fresh reviews or authorize integration.
- Authority boundary: the original producers used both authorized attempts for the same finding set. Correction, review, integration, live-suite execution, and terminal completion remain stopped.

## Unblock Condition

A fresh parent message beginning ARTIFACT RESUME must explicitly reopen a bounded correction budget after the exhausted two-attempt loop, name a clean current-main baseline and released non-overlapping claims, and authorize the exact remaining surfaces. That authority must cover either defining every referenced deterministic check ID in evals/judges.yaml or replacing those references with defined scenario IDs, together with the five preserved Dev Documentation Writer fixture and suite files needed to correct command grammar, reference-style Markdown destinations, contradictory coverage and anaphora, HTML-comment and nested-blockquote visibility, and mutation-sensitive regression coverage. The corrected result must receive entirely fresh Methodology Artifact and Dev Code acceptance and deterministic verification before integration or live-suite work can resume. Until that exact ARTIFACT RESUME arrives, this item remains Blocked.

## Summary

Require Dev Documentation Writer to produce complete canonical methodology artifacts on the first bounded contribution attempt.

## Context

The Project Bootstrapper missing-configuration evaluation required a new module design derived from the canonical module design template. Dev Documentation Writer initially omitted required template sections, including Implementation Readiness, and described boundary tests that were absent from the fixture. Repeated correction consumed the contribution budget before the integrated project could reach an accepted steady state.

The complete evaluation did not edit the distributed Dev Documentation Writer or documentation creation skills.

## Evidence

- evals/agent-tests/project-bootstrapper/scenarios.yaml defines the missing-configuration multi-contribution contract.
- evals/agent-tests/project-bootstrapper/fixtures/missing-configuration contains the frozen bootstrap fixture.
- skills/create-module-design and its canonical template define the required module design structure.
- evals/agent-tests/results/2026-07-17-complete-agent-suites.md records the bounded correction failure.
- The live run required two documentation corrections because the first drafts omitted canonical headings and asserted tests not present in the fixture.

## Requirements

- Load and apply the canonical artifact template before drafting the requested document.
- Emit every required heading and readiness section in template order unless the template explicitly marks it optional.
- Ground test, verification, and implementation statements in supplied repository evidence.
- Do not invent boundary tests, completed verification, or implementation state.
- Make a deterministic template-conformance check part of the writer handoff.
- Add focused coverage for complete first-attempt module design generation.

## Acceptance Criteria

- A missing module design contains every canonical required section on the first bounded contribution attempt.
- Implementation Readiness is present and evidence-backed.
- Test descriptions match files and commands present in the fixture.
- The Project Bootstrapper missing-configuration scenario no longer spends correction rounds on template omissions or invented tests.
- Repository skill validation, generated-output checks, and unit tests pass.

## Dependencies

None.

## Verification

- Run focused template-conformance tests for Dev Documentation Writer.
- Compare the generated module design headings with the canonical template.
- Run the Project Bootstrapper missing-configuration scenario and inspect contribution count, reviewer evidence, and cleanup.
- Run Agent Skill validation, generated-output freshness checks, repository unit tests, and Git diff validation.

## Notes

- This item concerns source-faithful completeness, not prose length.
