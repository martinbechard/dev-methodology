# Preserve Integrated Documentation Steady State

Status: Completed

Type: Defect

## Approval Resolution

The original proposal assigned a broad cross-artifact audit to Dev Documentation Writer and applied it to ordinary project setup. The user rejected both boundaries, then approved the corrected two-role scope. The completed behavior applies only when Project Bootstrapper is reverse engineering an existing project, and Wiki Ingester owns the final read-only evidence audit. Dev Documentation Writer remains responsible only for writing or updating assigned non-wiki documents.

## Approval Evidence

- Basis: explicit user direction after two ownership-boundary corrections.
- Exact answer: “ok”.
- Provenance: parent thread 019f77f4-c4bd-7c91-b197-c987a7beb838 on 2026-07-20, answering the corrected two-role scope recorded at 9d9716c.
- The approval applies only to whole-project reverse engineering. It does not add the audit to ordinary project setup and does not make Dev Documentation Writer the audit owner.

## Resolution

Resolved. The exact answer “ok” authorized the corrected Project Bootstrapper and Wiki Ingester changes and supported mirror regeneration. No further user decision is required for this item.

## Unattended Work Authority

The recorded exact approval authorized the governed two-role implementation, supported mirror regeneration, focused correction and verification, direct main integration, terminal backlog completion, and cleanup. It did not authorize the rejected Documentation Writer audit ownership or an audit during ordinary project setup.

## Current Execution

- Canonical Dev Orchestrator task: 019f7e7b-e949-7fb0-916b-0a8b932198ca.
- Worktree: /Users/martinbechard/.codex/worktrees/60e7/dev-methodology.
- Phase: Completed; terminal cleanup handoff pending parent worktree and branch removal.
- Corrected resumption scope: reverse-engineering-only Wiki Ingester audit with artifact creation and updates routed to existing owners, including Dev Documentation Writer for supported documents.

## Delivery Evidence

- Accepted private candidate: bfe14a4, after fresh independent review returned PASS with no material findings.
- Main integration: 53f32fe, a single-parent exact-path integration commit based on the claimed current-main baseline.
- Integration claim: preserve-integrated-docs-integration-019f7e7b, released at event 13e093ee-bc31-4c92-b8d2-d445223e0283.
- Terminal backlog claim: preserve-integrated-docs-completion-019f7e7b, acquired separately for only the source and completed destination paths and scheduled for immediate clean release after this commit.
- Focused verification passed: 23 Project Bootstrapper orchestration and fixture tests, 9 strict workspace-inventory and dependency tests, 8 bundle contract tests, Wiki Ingester suite validation, Python compilation, Agent Skill validation, generated role and adapter freshness, hierarchy freshness, support-explorer freshness, and Git diff validation.
- Cleanup eligibility: the accepted branch is fully integrated into main by tree content, the private worktree is clean, and no implementation work remains.

## Summary

During whole-project reverse engineering, require a Wiki Ingester-owned final evidence audit to find stale contribution-phase and future-work wording after referenced artifacts have been integrated, while keeping document authorship and correction ownership with the existing specialized owners.

## Context

The Project Bootstrapper missing-configuration evaluation successfully created and integrated configuration, module documentation, and wiki contributions. Its final bounded review still found PROJECT.yaml, AGENTS.md, the wiki README, the module catalog, and module pages describing now-present artifacts as absent, excluded, or future work. Links and ownership statements therefore contradicted the final repository state.

The complete evaluation did not edit the distributed Project Bootstrapper, Project Configurator, Dev Documentation Writer, or Wiki Architect skills.

## Evidence

- evals/agent-tests/project-bootstrapper/scenarios.yaml defines the integrated steady-state acceptance contract.
- evals/agent-tests/project-bootstrapper/fixtures/missing-configuration contains the frozen multi-contribution fixture.
- evals/agent-tests/results/2026-07-17-complete-agent-suites.md records the final correction-cap failure.
- The final live review found present wiki pages still labeled as excluded or future contributions and configuration guidance still stating that required documentation was absent.

## Requirements

- Apply this final audit only when Project Bootstrapper is reverse engineering an existing project; do not add it to ordinary project setup.
- Have Wiki Ingester inspect the integrated repository state after all accepted reverse-engineering contributions and before final verification.
- Replace contribution-phase, absent-artifact, exclusion, and future-work wording when the referenced artifact now exists.
- Keep PROJECT.yaml, AGENTS.md, wiki navigation, module catalogs, manifests, and module pages mutually consistent.
- Resolve links and ownership statements against the final tree rather than an earlier contribution snapshot.
- Keep Dev Documentation Writer out of the broad repository audit, but use it to create or update every assigned document type supported by its definition and templates during reverse engineering.
- When Wiki Ingester finds that source evidence requires a missing module design or another supported non-wiki artifact, report that exact gap so Project Bootstrapper can assign it to Dev Documentation Writer.
- Route PROJECT.yaml and AGENTS.md corrections to Project Configurator, wiki corrections to their existing wiki owner, and non-wiki document corrections to Dev Documentation Writer.
- Require fresh independent review of every corrected artifact before final verification.
- Add deterministic checks for stale phase wording and contradictions about present files.

## Acceptance Criteria

- Ordinary project setup does not trigger the reverse-engineering final audit.
- Whole-project reverse engineering assigns the integrated-tree evidence audit to Wiki Ingester.
- Final configuration and documentation describe the same integrated repository state.
- No present wiki or module artifact is labeled absent, excluded, or future work.
- Navigation and manifests include every accepted contribution with valid links.
- Dev Documentation Writer creates or updates assigned supported documents, including missing module designs discovered by the audit, without becoming the audit owner.
- The Project Bootstrapper missing-configuration scenario reaches final acceptance within its bounded correction policy.
- Repository skill validation, generated-output checks, and unit tests pass.

## Dependencies

- Enforce Documentation Template Conformance.

## Verification

- Add focused integration tests that distinguish ordinary setup from whole-project reverse engineering and transition a reverse-engineering fixture from contribution phase to steady state.
- Verify Wiki Ingester owns the final audit and that correction or missing-artifact routing preserves existing artifact ownership, including a missing-module-design case assigned to Dev Documentation Writer.
- Search final artifacts for fixture-specific absent, excluded, and future-work markers.
- Run the Project Bootstrapper missing-configuration scenario and inspect every accepted contribution and the final review packet.
- Run Agent Skill validation, generated-output freshness checks, repository unit tests, and Git diff validation.

## Notes

- A correct intermediate contribution does not satisfy the final integrated-state contract.
- Dev Documentation Writer writes and updates every supported assigned document needed by reverse engineering; it does not perform the final cross-artifact audit.
