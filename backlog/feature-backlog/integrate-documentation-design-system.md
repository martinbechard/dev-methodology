# Integrate The Documentation Design System

Status: Running

Owner: Dev Orchestrator task `019fe3cd-577c-76b1-965c-06fb8793ae42`

Canonical Conversation: `019fe3cd-577c-76b1-965c-06fb8793ae42`

Canonical Task: `019fe3cd-577c-76b1-965c-06fb8793ae42`

Branch: `codex/integrate-documentation-design-system-019fe3cd`

Worktree: `/Users/martinbechard/.codex/worktrees/df8a/dev-methodology`

Phase: Prototype analysis and exact-path planning

Type: Feature

Provider: file

Work Item ID: integrate-documentation-design-system

Completion: main-branch

## Summary

Introduce one versioned, reusable design system for the dev-methodology HTML documentation and a portable, evidence-based conformance-review workflow. Adapt the approved prototype from docs-design-system into authoritative methodology sources, conceptual roles, runtime adapters, documentation, evaluation coverage, and regression checks without migrating existing HTML pages or publishing to user-level locations.

## Context

The HTML documentation contains shared visual and interaction patterns alongside inconsistent variations that reduce quality and make conformance difficult to assess. The local docs-design-system project was derived from current dev-methodology pages and contains the design candidate, page-type checklists, two read-only conceptual-role prototypes, a portable review proposal, and model tournament evidence.

The prototype is candidate input, not an authoritative methodology source. Adapt it to this repository's schemas, category naming, semantic model profiles, generators, catalogs, tests, and source-first ownership boundaries.

```text
/Users/martinbechard/dev/docs-design-system/
├── docs/design-system/
├── skills/review-documentation-design-system/
├── agents/
│   ├── documentation-design-system-checklist-runner.role.yaml
│   └── documentation-design-system-review-coordinator.role.yaml
├── docs/portable-review-system-proposal.md
└── evals/results/
    ├── tournament-report.md
    └── coordinator-tournament-report.md
```

This item covers repository-local source integration and verification only. Existing dev-methodology HTML pages remain unchanged unless a separate migration is authorized. User-level installation and publication require originating-task confirmation after implementation and a later explicit user instruction.

## Source Evidence

Direct user request in the current Codex task on 2026-08-08: "We want to create a work item to introduce a design system for the html documentation, because there are inconsistencies that reduce the quality. The new design system is in ~/dev/docs-design-system and was based on the work done in dev-methdology. Here is a request from the owner."

The attached Prompt for the dev-methodology Owner authorizes source implementation of the approved Documentation Design System and portable conformance-review workflow. It requires preservation of the prototype's design coverage, accessible SVG rules, checklist contract, runner and coordinator boundaries, tournament-backed model settings, catalogs, generators, multi-runtime adapters, evaluation coverage, browser verification, and confirmation-before-publication boundary.

## Requirements

- Add a versioned, single-entry HTML design system under the repository's hand-authored design sources.
- Preserve the prototype version and require conforming pages to declare their target design-system version.
- Document the normal page shell, official brand and logo, badges, document-sequence navigation, section navigation, page-top link, regular default hero, optional two-column hero, responsive behavior, and accessibility.
- Cover foundations, content, data display, forms and actions, diagrams, source inventory, and variation auditing.
- Give every variation an inline visual example, source-page attribution, advantages, disadvantages, and standardization status. Keep source-observed variations distinct from adopted standards.
- Document reusable accessible SVG connector and short-stem block-entry-arrow patterns for ordinary and stronger combined flows, fan-out, and fan-in.
- End connectors at the arrow stem; do not carry marker-end into destination blocks. Make stem length equal arrowhead depth, align connector, stem, arrowhead, and block entrance, and place the tip on the block boundary.
- Include reusable symbol and use examples, explained Do and Don't examples, curve routing, convergence, line weight, whitespace, label clearance, clipping, overflow, narrow rendering, title, and description guidance.
- Add review-documentation-design-system with one shared checklist and one checklist per page type. Give every item a stable unique ID and an evidence-backed PASS, FAIL, or NOT TESTED result.
- Add a small read-only Methodology checklist runner that receives exactly one page and checklist, loads only the review skill, records each assigned item exactly once, cannot mutate or delegate, and makes no integrated acceptance decision.
- Add a read-only Methodology review coordinator that depends on the runner, dispatches one page-checklist assignment per invocation, validates completeness, de-duplicates evidence, preserves contradictions, and alone returns ACCEPTED, REJECTED, or BLOCKED.
- Keep checklist procedure in the skill and coordination procedure in the coordinator; do not duplicate checklist methodology in the runner.
- Rank candidates by accuracy first, estimated cost only within equal accuracy with plus-or-minus 15 percent treated as equivalent, then wall-clock speed. Never invent a price for an unpriced candidate.
- Express the tested Luna-medium runner and Terra-low Codex coordinator through semantic model-profile sources and runtime mappings, never provider IDs in conceptual definitions. Add the smallest new semantic profile only if required.
- Update the required authoritative skills, roles, profile sources and mappings, catalogs, suites, scenarios, hand-authored documentation, schemas, inventories, generators, installers, and regression tests.
- Regenerate repository-owned Codex, Claude Code, Gemini CLI, and Junie CLI adapters, generated documentation data, and generation manifests. Verify authority, dependencies, skill assignment, output contracts, and semantic mappings.
- Keep all implementation and verification repository-local. Do not write user-home skill or role locations.
- After source verification, send the originating docs-design-system task a dossier containing commit and worktree, authoritative and generated paths, regeneration commands, semantic profiles and mappings, test totals, edge-case evidence, browser evidence, deviations, limitations, and failed gates.
- Request originating-task confirmation and stop. Publication requires that confirmation and a subsequent explicit user instruction.

## Acceptance Criteria

- The design-system index discovers every page, and the review skill discovers every page-type checklist.
- Pages preserve versioning, shell, navigation, hero patterns, foundations, content, data display, forms, accessibility, responsive behavior, diagrams, source inventory, and variation auditing.
- Variations have visual examples, attribution, advantages, disadvantages, and status, with observed and adopted patterns clearly separated.
- SVG examples have accessible titles and descriptions and satisfy connector, stem, arrowhead, block-boundary, fan-out, fan-in, routing, clearance, clipping, overflow, and narrow-width checks.
- Every checklist ID is unique and resolves exactly once.
- The runner loads only the review skill, receives one page and checklist, is read-only and non-delegating, records every item once, and returns only PASS, FAIL, or NOT TESTED evidence.
- The coordinator never substitutes its own checklist review and alone owns ACCEPTED, REJECTED, or BLOCKED.
- Focused cases prove complete pass, confirmed failure, missing report, malformed report, unavailable runner, duplicate finding, and irreconcilable conflict behavior.
- Ranking tests prove accuracy precedence, the 15 percent cost boundary, speed tie-breaking, cached-input accounting, and unpriced handling.
- Conceptual definitions contain semantic profiles only, and runtime mappings reproduce the tested Codex settings.
- All four generated adapter families preserve mutation authority, dependencies, skill assignments, output contracts, and model mappings.
- Pages render without broken navigation, clipping, or horizontal overflow at desktop and narrow widths.
- Generated freshness, Markdown, links, Agent Skill validation, focused evaluations, dependency-directed regression tests, and git diff --check pass.
- No existing HTML source page is migrated and no user-home installation or publication occurs.
- The originating task receives the complete dossier and confirmation request before closure.

## Dependencies

None.

## Verification

- Validate the skill, every checklist, unique checklist IDs, and checklist resolution.
- Add focused runner and coordinator contract tests for every required success and failure boundary.
- Add ranking tests for accuracy, both 15 percent edges, cost outside the band, speed, cached input, and unpriced candidates.
- Regenerate and freshness-check all four adapters and generated documentation data.
- Compare adapters with conceptual sources for authority, dependencies, skills, output fields, and semantic mappings.
- Run implicated schema, inventory, generator, installer, catalog, suite, scenario, and regression tests.
- Run markup, navigation, link, accessibility, and overflow checks for every design-system page.
- Browser-verify representative desktop and narrow widths, navigation, examples, SVG geometry, clipping, overflow, titles, and descriptions.
- Run git diff --check and produce the required implementation dossier with exact commands and totals.

## Open Questions

- Determine the smallest semantic profile name and cross-runtime meaning for the tested Terra-low coordinator without changing unrelated roles.
- Determine whether the current role schema and installer already express every runner and coordinator boundary.
- Determine the exact hand-authored design-system entry link while preserving current page sequence and generator ownership.

## Governed Definition Approval

### Governed Canonical Sources

```text
skills/review-documentation-design-system/
├── SKILL.md
└── references/
    ├── review-checklist-documentation-design-system-accessibility.md
    ├── review-checklist-documentation-design-system-content.md
    ├── review-checklist-documentation-design-system-data-display.md
    ├── review-checklist-documentation-design-system-diagrams.md
    ├── review-checklist-documentation-design-system-forms-and-actions.md
    ├── review-checklist-documentation-design-system-foundations.md
    ├── review-checklist-documentation-design-system-index.md
    ├── review-checklist-documentation-design-system-page-shell.md
    ├── review-checklist-documentation-design-system-shared.md
    ├── review-checklist-documentation-design-system-source-inventory.md
    └── review-checklist-documentation-design-system-variations.md
agents/
├── model-profiles.yaml
└── roles/methodology-maintenance/
    ├── methodology-design-system-checklist-runner.role.yaml
    └── methodology-design-system-review-coordinator.role.yaml
```

The Methodology-prefixed role names adapt the prototype to the repository naming contract. A replacement governed role path requires new exact-path approval before mutation.

### Allowed Dependent Artifacts

The approved definition work may update these exact dependent paths when required:

```text
skills/review-documentation-design-system/agents/openai.yaml
agents/role-schema.yaml
adapters/codex/model-profiles.yaml
adapters/claude/model-profiles.yaml
adapters/gemini/model-profiles.yaml
adapters/junie/model-profiles.yaml
design/skill-categories.yaml
design/role-catalog-groups.yaml
design/agent-skill-hierarchy.svg
design/agent-skill-test-coverage-checklist.md
design/agent-and-skill-evaluations.html
design/documentation-design-system/VERSION
design/documentation-design-system/index.html
design/documentation-design-system/page-shell.html
design/documentation-design-system/foundations.html
design/documentation-design-system/content.html
design/documentation-design-system/data-display.html
design/documentation-design-system/forms-and-actions.html
design/documentation-design-system/accessibility.html
design/documentation-design-system/diagrams.html
design/documentation-design-system/source-inventory.html
design/documentation-design-system/variations.html
design/documentation-design-system/assets/design-system.css
design/documentation-design-system/assets/design-system.js
design/documentation-design-system/assets/dev-methodology-logo.png
evals/agent-scenarios.yaml
evals/agent-tests/suite-index.yaml
evals/cases.yaml
evals/skill-probes.yaml
evals/workflow-packs.yaml
README.md
scripts/build-skill-docs.py
scripts/install-skills.py
scripts/test_bundle_content.py
design/generated/skill-definitions.js
design/generated/role-definitions.js
generated/adapters/agent-generation-manifest.json
generated/adapters/codex/agents/methodology-design-system-checklist-runner.toml
generated/adapters/codex/agents/methodology-design-system-review-coordinator.toml
generated/adapters/claude/agents/methodology-design-system-checklist-runner.md
generated/adapters/claude/agents/methodology-design-system-review-coordinator.md
generated/adapters/gemini/agents/methodology-design-system-checklist-runner.md
generated/adapters/gemini/agents/methodology-design-system-review-coordinator.md
generated/adapters/junie/agents/methodology-design-system-checklist-runner.md
generated/adapters/junie/agents/methodology-design-system-review-coordinator.md
```

### Coordinator Dependent-Scope Disposition

The Coordinator authorizes these exact four non-governed dependent paths because new conceptual roles require `evals/agent-tests/suite-index.yaml` registration, while approved sources and generators own `design/agent-skill-hierarchy.svg`, `design/agent-skill-test-coverage-checklist.md`, and `design/agent-and-skill-evaluations.html` projections. Generated outputs remain generator-owned and must not be hand-edited. This authorizes no fifth path, no additional governed definition, and no absorption of unrelated baseline support-checklist or evaluation-HTML stale defects.

Focused test and evaluation fixture files may be added in established locations when directly traceable to acceptance criteria. Generated files remain generator-owned. Any additional governed skill or conceptual-role definition path requires separate approval.

### Approval Resolution

Approved at creation on 2026-08-08 by the current user request and attached owner prompt. The owner directs dev-methodology to "Implement the approved Documentation Design System and its portable conformance-review workflow" and specifically requires review-documentation-design-system, a checklist runner, a review coordinator, and necessary semantic model-profile sources or mappings. Approval is limited to the exact governed sources and dependent artifacts above. It does not authorize migration of existing HTML pages or user-level deployment, installation, or publication.

## Notes

- The prototype remains candidate evidence; dev-methodology sources and schemas are authoritative.
- No docs/project-taxonomy.md exists. Placement follows repository maintenance guidance and adjacent conventions.
- Preserve unrelated working-tree changes and exclude them from creation and implementation commits unless separately in scope.
- Originating-task confirmation is a post-implementation acceptance and publication boundary, not a hard dependency for starting this Ready item.
- Existing HTML documentation migration requires a separate work item.

## Starting Handoff Evidence

Starting Recorded At: 2026-08-08T23:54:28Z

Coordinator: Dev Backlog Coordinator task `019fb057-1767-7ef2-b5fa-41f4417b20b3`

Normalized Objective: Integrate the approved versioned Documentation Design System and portable read-only conformance-review workflow into authoritative methodology sources, semantic profiles, generated adapters, focused evaluations, and repository-local documentation without migrating existing HTML pages or publishing to user-level locations.

Launch Result: Requested

Canonical Execution: None

Runtime Request: `client-new-thread:9b914695-68ee-40ec-b8d6-7cd178ea9428` (worktree setup queued; not a canonical task identifier)

Last Contact At: 2026-08-08T23:55:24Z

Next Reconciliation At: 2026-08-09T00:10:24Z

Intended Root Role: Dev Orchestrator

Scheduling Evidence: The older `default-unconfigured-projects-to-solo-mode` finish lane is Completed at provider commit `51aaf33d7122e8e70d2ff5ab4a3bbc23c35d7d58`; its claims are released, clean source and integration worktrees are removed, and its canonical task is archived. Primary main is clean and the resource-claim registry is empty. Begin with private-worktree prototype analysis and exact governed-path prechecks; defer any later shared installation or unrelated publication beyond the work item's explicit boundaries.

## Active Execution Evidence

Condition Type: root-execution

Owner: Dev Orchestrator task 019fe3cd-577c-76b1-965c-06fb8793ae42

Evidence: canonical root execution owns clean candidate commit `b45719f78c1dcd74f704998e4553a1bc973f140e` (unchanged branch/worktree, 73 authorized files) and six fresh paused read-only lanes. UX and maintained-document reviews are complete `NEEDS_CORRECTION`; code, methodology, prompt, and verifier lanes are substantively complete and paused. Material findings require correction: runner one-supplied-checklist versus skill Shared+page-type contradiction; strict validator accepts wrong page/checklist, malformed limits, empty assignment, and can crash on `findings=None`; FAIL+NOT TESTED is incorrectly REJECTED instead of BLOCKED; +1e-12 ranking tolerance admits just-outside 115%; output schema/simulator mismatch and underspecified generated nested schema; suite-specific skill/eval wiring and empty-field issues. Independent verifier has 24 focused passes, 22/22 provenance with Root envelope, and freshness passes; full bundle has one deferred support assertion; `scripts.test_agent_skill_evaluation_docs` has six failures (five candidate-induced count updates, one pre-existing future-ideas mismatch). Docs/UX findings include printable controls, snapshot/current wording and stale metrics, duplicate h1 specimen, abbreviated production nav class, one SVG title/desc, stale folder tree, and incomplete semantic-profile README documentation. Existing HTML pages remain an explicit no-edit boundary. All 15 governed receipts remain terminal `ALLOWED_APPROVED_DEFINITION_CHANGE`, and the exact four dependent paths remain reconciled. No source mutation has begun. The direct overlap boundary with `publish-and-integrate-terminology-standard` is acknowledged; both tasks defer shared overlap events and preserve each other.

Observed At: 2026-08-09T01:26:55Z

Started At: 2026-08-08T23:57:32Z

Deadline or Expires At: 2026-08-09T03:15:00Z

Next Action: Batch corrections through the original coder, reconcile exact dependent scope for any newly implicated existing test path before mutation, then obtain fresh re-review, re-verification, and browser checks without widening scope.

Next Reconciliation At: 2026-08-09T01:41:00Z
