# Rename Direct Main To Main Branch

Status: Completed

Type: Feature

Provider: file

Provider Reference: backlog/completed-backlog/features/rename-direct-main-to-main-branch.md

Work Item ID: rename-direct-main-to-main-branch

Completion: direct-main

## Completion Evidence

- Provider: file. Historical dispatch selector: `direct-main`. Delivered Commit selector: `main-branch`. Completion disposition: READY. Lifecycle disposition: Completed.
- Completed at: 2026-08-07T01:49:16Z.
- Completed provider reference: `backlog/completed-backlog/features/rename-direct-main-to-main-branch.md`.
- Canonical execution: Root Dev Orchestrator task `019fd9c9-853a-7723-8990-3efe59cee655` under Dev Backlog Coordinator task `019fb057-1767-7ef2-b5fa-41f4417b20b3`.
- Accepted source: final immutable candidate `faf4a729ef46b8ed1d531f0a36f730467074b3a3` on `codex/rename-direct-main-to-main-branch`, including the reviewed correction to the initial candidate `0b467696c01f38dd9f2e2861ff14db4f35b88732`.
- Delivery: candidate `faf4a729ef46b8ed1d531f0a36f730467074b3a3` was integrated on authoritative local `main` by merge commit `0480f272547c2616daaab0cb37dd5c44c7b538b6`. Candidate reachability and the exact accepted-range-to-integration-range byte mapping passed before delivery was declared ready.
- Contract result: `deliver-work-item-main-branch` and Commit `main-branch` now name the stable destination while preserving primary-worktree delivery, separate-worktree integration, the feature-branch alternative, unrelated-dirty-file preservation, and an exact legacy `direct-main` configuration compatibility boundary. Historical provider records were not rewritten for terminology alone.
- Independent review: one fresh reviewer APPROVED the corrected final candidate, including the restored `direct-maintenance` term. No second reviewer or repeated review gate was used.
- Focused verification: one verifier passed 25 focused tests on the candidate, then verified only the changed correction evidence. On integrated `main`, the 14 renamed-contract cases, one legacy-alias case, supported metadata/document/hierarchy freshness checks, exact mapping, reachability, and diff hygiene passed. No broad suite, simulator, or framework was run.
- Baseline limitations: structured skill validation rejected both candidate and primary repository skill paths as outside its installed roots, so no forbidden fallback validator was used. Installer dry-run separately reported pre-existing incomplete `agent-claim` and `agent-claim-command` skill directories. Markdown validation separately reported three unchanged baseline findings: the README hierarchy anchor, one historical review-checklist target, and a structured-explanation example path. These were recorded without expanding scope.
- Claims: exact integration-path claim `rename-direct-main-to-main-branch-integration-paths` covered 59 path endpoints and released normally at event `a98636bb-20fc-47d6-9200-293dc212b264`. Exact work claim `rename-direct-main-to-main-branch-work` released with handoff at event `c27feeb4-97a3-4c8b-beed-59ba638819a4`. Terminal update claim `rename-direct-main-to-main-branch-complete-update` and exact active/completed provider-path claim `rename-direct-main-to-main-branch-complete-provider-paths` protect this single archive transaction and will release after its commit.
- Publication: delivery is complete on authoritative local `main`; no remote publication was requested.
- Cleanup eligibility: source candidate is fully merged and its linked worktree is clean. The linked worktree and fully merged source branch are eligible for removal after this archive commit and claim release.

## Summary

Replace direct-main terminology with main-branch terminology across the delivery provider, project Commit selection, documentation, generated artifacts, tests, and evaluations.

## Context

The current direct-main name is difficult to interpret because it combines a destination with an implied implementation mechanism. The delivery provider actually promises that accepted work reaches the main branch. Implementation may occur directly in the primary worktree or on a separate branch and worktree followed by integration, so main-branch describes the stable delivery destination more accurately.

The current name appears in the deliver-work-item-direct-main Provider Skill, the Commit selector, project templates, generated guidance and adapters, documentation, backlog examples, tests, evaluation fixtures, and a focused evaluation project. The rename must retain the distinction between main-branch delivery and feature-branch delivery while preserving both supported implementation paths to the main branch.

## Source Evidence

On 2026-08-06, in Codex task 019faeef-e932-7352-a53d-fdb1535f5994, the user stated: “Another bad name: direct-main should actually be main-branch” and then confirmed: “we need an item for that one too.”

## Requirements

- Rename the deliver-work-item-direct-main Provider Skill package, frontmatter identity, title, metadata, and references to deliver-work-item-main-branch.
- Rename the project Commit selector value from direct-main to main-branch wherever the current configuration model, templates, generated guidance, validation, and user-facing explanations expose it.
- Preserve the delivery contract: the provider completes accepted work on the main branch whether implementation happened in the primary worktree or in a separate branch and worktree that must be integrated.
- Keep feature-branch as the alternative delivery provider and update comparisons, diagrams, tables, routing examples, and setup language so the two choices are coherent.
- Rename current source, generated, test, fixture, and evaluation artifacts whose filenames or directory names encode direct-main when their identity represents the renamed concept.
- Update focused tests and individual evaluations that exercise completion selection, main-branch integration, unrelated dirty-file preservation, provider-family naming, project configuration, work-item creation, documentation generation, and catalog membership.
- Regenerate every supported derived artifact from its canonical source rather than editing generated outputs as independent sources.
- Define and verify the upgrade behavior for existing PROJECT.yaml files and installed project guidance that still use direct-main. Do not silently reinterpret malformed or unrelated values.
- Retain historical completed and failed work-item evidence without rewriting historical records merely to remove the former name.

## Acceptance Criteria

- The installed skill catalog exposes deliver-work-item-main-branch with aligned directory, frontmatter, title, metadata, and provider-family naming.
- New project configuration and generated AGENTS.md guidance use Commit main-branch and select deliver-work-item-main-branch.
- The main-branch provider supports both direct primary-worktree implementation and integration of accepted separate-branch or worktree contributions without changing the established delivery safeguards.
- Current agent definitions, skills, templates, documentation, generators, generated adapters, tests, and active evaluation fixtures contain no operational dependency on direct-main.
- Any remaining direct-main text is limited to deliberate historical evidence, compatibility handling, or migration documentation whose purpose is explicit.
- Existing configurations using direct-main receive verified migration or compatibility behavior with an explicit supported boundary.
- Focused delivery, configuration, provider-family, work-item, generation, and affected agent-evaluation tests pass under the new terminology.
- Skill validation, metadata synchronization, generated-document freshness checks, Markdown validation, and git diff checks pass.
- An independent review confirms that main-branch consistently names the delivery destination and that no documentation incorrectly implies all implementation occurs directly on main.

## Dependencies

None.

## Verification

- Search the complete repository before and after the rename for direct-main, Direct Main, direct_main, and the new main-branch variants; classify every intentional residual occurrence.
- Run the renamed main-branch completion contract tests, provider-family naming tests, project configuration and technology-generation tests, bundle-content tests, work-item coordination tests, and affected individual agent-evaluation suites.
- Run the separate-branch and worktree integration cases together with unrelated dirty-primary-file preservation cases to prove that the destination rename did not narrow supported implementation paths.
- Run the supported skill metadata, documentation, native-adapter, hierarchy, and support-checklist generators with their freshness checks.
- Validate the renamed Provider Skill and confirm that every conceptual and generated agent skill reference resolves to an installed bundle identity.
- Verify existing PROJECT.yaml migration or compatibility behavior using focused valid, legacy, and invalid configuration fixtures.
- Run Markdown link validation and git diff checks on the completed change.

## Open Questions

- Resolve during implementation whether direct-main remains a temporary accepted configuration alias or requires an explicit migration step. Base the decision on upgrade safety and supported configuration policy.
- Determine which historical artifact filenames must remain unchanged as evidence and which current evaluation or documentation artifact identities should be renamed.

## Governed Definition Approval

### Governed Canonical Sources

- skills/deliver-work-item-direct-main/SKILL.md
- skills/coordinate-work-items/SKILL.md
- skills/create-project-configuration/SKILL.md
- skills/manage-future-ideas/SKILL.md
- skills/manage-work-items-gitlab/SKILL.md
- skills/verify-end-to-end-workflow/SKILL.md

### Allowed Dependent Artifacts

- skills/deliver-work-item-direct-main/agents/openai.yaml
- agents/roles/project-setup/project-configurator.role.yaml
- PROJECT.yaml
- AGENTS.md
- README.md
- skills/route-documentation-work/assets/templates/file-work-item-template.md
- skills/route-documentation-work/assets/templates/project-template.yaml
- scripts/generate-backlog-report.py
- scripts/render-agents-technology-skills.py
- scripts/test_bundle_content.py
- scripts/test_direct_main_completion_contract.py
- scripts/test_generate_backlog_report.py
- scripts/test_path_limited_backlog_git.py
- scripts/test_provider_family_naming.py
- scripts/test_role_mutation_policy.py
- scripts/test_ste_technical_writing.py
- scripts/test_technology_detection.py
- scripts/test_work_item_coordination.py
- evals/agent-scenarios.yaml
- evals/cases.yaml
- evals/skill-probes.yaml
- evals/workflow-packs.yaml
- evals/projects/direct-main-unrelated-dirty-contract/TASK.md
- evals/projects/file-work-item-template-contract/verify.py
- evals/agent-tests/dev-backlog-steward/fixtures/cases.yaml
- evals/agent-tests/dev-backlog-steward/scenarios.yaml
- evals/agent-tests/dev-backlog-steward/skills/dev-backlog-steward-suite-contract/SKILL.md
- evals/agent-tests/dev-backlog-steward/test_contract.py
- evals/agent-tests/dev-orchestrator/test_fixtures.py
- design/agent-and-skill-evaluations.html
- design/agent-skill-specialization-examples.html
- design/agent-skill-test-coverage-checklist.md
- design/object-oriented-agent-and-skill-model.md
- design/object-oriented-skill-group-models.md
- design/orchestrated-development-lifecycle.html
- design/skill-groups/concurrent-tasking.md
- design/skill-groups/direct-main-delivery.md
- design/skills-modularization.html
- design/wiki-skills-and-project-context.html
- design/work-item-provider-and-completion-contracts.md
- design/generated/role-definitions.js
- design/generated/skill-definitions.js
- design/generated/template-definitions.js
- generated/adapters/claude/agents/project-configurator.md
- generated/adapters/codex/agents/project-configurator.toml
- generated/adapters/gemini/agents/project-configurator.md
- generated/adapters/junie/agents/project-configurator.md
- Affected exact evaluation suite, scenario, fixture, and suite-contract files identified by the required repository-wide reference search.

### Approval Resolution

Approved at creation. On 2026-08-06, in Codex task 019faeef-e932-7352-a53d-fdb1535f5994, the user requested that direct-main be changed to main-branch and explicitly requested a work item for that rename. This approval covers the exact governed canonical sources listed above only. Any additional governed skill-definition path discovered during implementation requires separate scope-specific approval; existing approval for the listed paths remains valid.

## Starting Handoff Evidence

Starting Recorded At: 2026-08-07T01:14:14Z

Coordinator: Dev Backlog Coordinator task `019fb057-1767-7ef2-b5fa-41f4417b20b3`

Normalized Objective: Rename the direct-main delivery provider and Commit selection to main-branch across approved operational sources, generated artifacts, focused tests, evaluations, and compatibility handling while preserving the established main-branch delivery safeguards and historical evidence.

Launch Result: Not attempted

Canonical Execution: None

Last Contact At: None

Next Reconciliation At: 2026-08-07T01:29:14Z

Intended Root Role: Dev Orchestrator

Scheduling Evidence: The overlapping resource-claim rename is Completed and archived at main commit `102c5fe6ae5b560befd6e9aac3485a51804508ca`; its shared source, generator, installation, and integration lanes are released.

## Historical Active Execution Evidence

Condition Type: root-execution.

Owner: Root Dev Orchestrator task 019fd9c9-853a-7723-8990-3efe59cee655.

Evidence: Immutable candidate `faf4a729ef46b8ed1d531f0a36f730467074b3a3` is integrated on authoritative `main` as `0480f272547c2616daaab0cb37dd5c44c7b538b6`, and the canonical task title is `Integrating — Rename Direct Main To Main Branch`. Integration-sensitive checks are active: exact candidate-to-main mapping, reachability, renamed-contract and legacy-alias focused tests, generated-artifact freshness, and diff hygiene have passed; terminal provider and cleanup reconciliation remains. Exact Work Item ID activity `work` claim `rename-direct-main-to-main-branch-work` was live for this execution and is in the required one-transaction handoff while exact activity `update` claim `rename-direct-main-to-main-branch-integrating-update` and exact provider-path claim `rename-direct-main-to-main-branch-integrating-provider-path` protect this refresh; it will be reacquired immediately afterward. Exact 59-endpoint integration-path claim `rename-direct-main-to-main-branch-integration-paths` remains live on authoritative `main` throughout this transaction.

Observed At: 2026-08-07T01:47:14Z.

Started At: 2026-08-07T01:17:12Z.

Deadline or Expires At: 2026-08-07T03:17:12Z.

Next Action: Commit only this provider evidence replacement, release the exact provider-path and activity update claims with handoff, reacquire the same exact Work Item ID activity `work` claim, then finish integration-sensitive terminal closeout without altering candidate or integration bytes or repeating green source gates.

Next Reconciliation At: 2026-08-07T02:02:14Z.

## Historical Running Evidence Refresh — 2026-08-07T01:32:44Z

Canonical Title: Reviewing — Rename Direct Main To Main Branch.

Current Phase: Independent review and focused verification.

Immutable Candidate: 0b467696c01f38dd9f2e2861ff14db4f35b88732 on branch codex/rename-direct-main-to-main-branch in /Users/martinbechard/.codex/worktrees/98eb/dev-methodology.

Execution Evidence: The candidate worktree is clean. One fresh independent review and one focused verifier are active against the immutable candidate. The same Root Dev Orchestrator retains canonical task 019fd9c9-853a-7723-8990-3efe59cee655 and exact Work Item ID ownership; no restart, duplicate dispatch, or candidate mutation occurred.

Claim Handoff Evidence: Exact activity work claim rename-direct-main-to-main-branch-work was released with handoff solely for this provider reconciliation. Exact activity update claim rename-direct-main-to-main-branch-review-update and exact provider-path claim rename-direct-main-to-main-branch-review-path both returned SHARED_CHECKOUT_ACQUIRED.

Next Action: Commit only this provider evidence refresh, release the provider-path and activity update claims with handoff, reacquire the same exact Work Item ID activity work claim, and continue the active review and verification without repeating green gates.
