# Rename Agent Claim To Resource Claim

Status: Completed

Owner: Unowned

Type: Feature

Provider: file

Provider Reference: backlog/completed-backlog/features/rename-agent-claim-to-resource-claim.md

Work Item ID: rename-agent-claim-to-resource-claim

Completion: direct-main

## Completion Evidence

- Provider: file. Completion selector: direct-main. Completion disposition: READY. Lifecycle disposition: Completed.
- Completed at: 2026-08-07T01:12:20Z.
- Completed provider reference: backlog/completed-backlog/features/rename-agent-claim-to-resource-claim.md.
- Accepted source commit: `140f0bbdbfe43925e54e89c1efd49facb30a3b81` on `codex/rename-agent-claim-to-resource-claim`; its private worktree was clean and its accepted manifest contains 137 exact paths with SHA-256 `b53b772d43fcaca86a169911a95107d15eabe6955b2e2039f8e6394e3663927d`.
- Independent acceptance: the fresh independent reviewer returned PASS with no remaining findings after the canonical and legacy claim-state corrections; the verifier returned VERIFIED for the exact accepted commit.
- Current-main reconciliation: the separately owned documentation line was committed as `731baf40ce11de4c279f3f4bd37c3c4e58d7e899`; Starting to Running was recorded at `375c0b15fe4879e87bac833e58e9fba68b11b2c1`; accepted candidate `140f0bbd` was replayed exactly once by cherry-pick onto that clean main and produced integration commit `0a78e0879f70c1b39e2b0fa1e13559013ffbfa9c`.
- Integration mapping: the accepted and integration commits have identical stable patch ID `0bab1ebb35a9fa2f4b69c209f238e378ef230da9`; `0a78e087` is the observed clean main tip before this provider-only archive transaction, and `design/skill-groups/concurrent-tasking.md` contains both the accepted resource-claim rename and the separately committed wording `a pull request workflow`.
- Integration-sensitive verification: Python 3.11 passed validation for all four renamed skill packages, `build-skill-docs.py --check`, five claim-snapshot tests, seven canonical/legacy claim-state evaluation fixtures, and Git diff validation. The integrated main checkout was clean after checks.
- Preserved baseline evidence: the source policy suite ran 140 tests with only the pre-existing report `KeyError: outcome`; the helper suite ran 26 tests with only the pre-existing inventory count `47 != 50`. No broad suite or live-model evaluation was rerun.
- Publication observation: the configured direct-main completion requires local main delivery; no remote publication operation was requested for this work item. Integration commit `0a78e087` is reachable from local main.
- Claim evidence: exact 137-path integration claim `rename-agent-claim-main-integration-019fd993` released normally at event `64858eb7-0f37-456a-9cb2-8a91fa50b756`. Terminal exact Work Item ID update claim `rename-agent-claim-complete-update-019fd993` and exact source/destination path claim `rename-agent-claim-complete-paths-019fd993` protect this provider-only archive commit and release immediately afterward.
- Cleanup eligibility: the source worktree is clean and its non-ancestral candidate content is durably mapped to main by identical patch ID, so its worktree and branch are eligible for cleanup after this archive commit and claim releases.

## Summary

Rename the agent-claim policy skill and its helper family to the resource-claim namespace so their names describe the shared resources being claimed rather than the agents performing the claims.

## Context

The current agent-claim name suggests that an agent itself is the object being claimed. The skill actually governs temporary ownership of files, work items, ports, databases, browser sessions, live-model capacity, installations, deployments, and other shared resources. Its helper interface and command and MCP providers use the same agent-claim stem, and the old identity appears throughout project configuration, agent definitions, generated adapters, documentation, tests, and evaluation fixtures.

The rename must preserve the existing separation of responsibilities: the policy skill decides when and what to claim, the helper Interface Skill defines operations and results, and one configured Provider Skill performs those operations.

## Source Evidence

On 2026-08-06, in Codex task 019faeef-e932-7352-a53d-fdb1535f5994, the user stated: “agent-claim is the wrong name anyway, it should be resource-claim because a resource is being claimed. We need to change that and create a workitem for the renaming including in tests.”

## Requirements

- Rename the agent-claim skill package, frontmatter identity, title, metadata, and installation references to resource-claim.
- Rename the agent-claim-helper Interface Skill family and its command and MCP Provider Skills to the matching resource-claim-helper, resource-claim-helper-command, and resource-claim-helper-mcp identities.
- Preserve the policy, interface, and provider responsibility boundaries while updating their cross-references and explanatory vocabulary.
- Update every current exact-name reference in project configuration, generated project guidance, conceptual agent definitions, skill definitions, templates, scripts, design documents, generated documentation, adapters, evaluation suites, fixtures, and catalog data.
- Update focused unit tests and individual agent or skill evaluations that exercise resource coordination, helper selection, claim outcomes, configuration generation, installation, documentation freshness, and catalog membership.
- Regenerate every supported derived artifact from its canonical source rather than editing generated outputs as independent sources.
- Determine whether persistent runtime paths and record names such as .codex/agent-claim and agent-claims.json require an atomic migration, a compatibility reader, or an explicitly documented stable storage name. Preserve existing live claim state across any storage migration.
- Retain historical records and completed work-item evidence without rewriting history merely to remove the former name.

## Acceptance Criteria

- The installed skill catalog exposes resource-claim and the resource-claim-helper provider family with aligned directory, frontmatter, title, metadata, and provider-family names.
- Current project configuration and generated AGENTS.md guidance select resource-claim and one resource-claim-helper-* Provider Skill using the existing policy and dispatch semantics.
- Current agent definitions, skills, documentation, templates, generators, generated adapters, and active evaluation fixtures contain no operational dependency on the former skill identities.
- Any remaining agent-claim text is limited to deliberate historical evidence, compatibility handling, or migration documentation whose purpose is explicit.
- Existing claim policy, structured outcomes, provider selection, contention handling, and cleanup behavior remain unchanged apart from approved naming or migration effects.
- Focused resource-claim and helper tests pass, including configuration, generator freshness, bundle-content, role-contract, work-item coordination, and affected agent-evaluation tests.
- Skill validation, metadata synchronization, generated-document freshness checks, Markdown validation, and git diff checks pass.
- An independent review confirms that the rename is complete, semantically coherent, and does not strand live claim records or installed references.

## Dependencies

None.

## Verification

- Search the complete repository before and after the rename for agent-claim, Agent Claim, agent_claim, agent-claims, and the new resource-claim variants; classify every intentional residual occurrence.
- Run the focused claim policy and helper test modules, the affected configuration and generation tests, bundle-content assertions, role mutation tests, work-item coordination tests, and individual affected agent-evaluation suites.
- Run the supported skill metadata, technology detection, documentation, native-adapter, hierarchy, and support-checklist generators with their freshness checks.
- Validate every renamed skill package and confirm that every conceptual and generated agent skill reference resolves to an installed bundle identity.
- Verify any persistent-state migration or compatibility path using existing claim records from the primary worktree and a linked worktree without deleting or resetting live state.
- Run Markdown link validation and git diff checks on the completed change.

## Open Questions

- Resolve during implementation whether persistent storage names should move to the resource-claim namespace or remain stable compatibility names. Base the decision on state-safety and migration evidence, not merely textual consistency.
- Identify every individual agent evaluation whose scenario or fixture contains the old identity after regenerating the canonical catalog and adapters.

## Governed Definition Approval

### Governed Canonical Sources

- skills/agent-claim/SKILL.md
- skills/agent-claim-helper/SKILL.md
- skills/agent-claim-helper-command/SKILL.md
- skills/agent-claim-helper-mcp/SKILL.md
- skills/coordinate-work-items/SKILL.md
- skills/create-project-configuration/SKILL.md
- skills/create-work-item-file/SKILL.md
- skills/deliver-work-item-direct-main/SKILL.md
- skills/deliver-work-item-feature-branch/SKILL.md
- skills/integrate-agent-work/SKILL.md
- skills/verify-end-to-end-workflow/SKILL.md

### Allowed Dependent Artifacts

- skills/agent-claim/agents/openai.yaml
- skills/agent-claim-helper/agents/openai.yaml
- skills/agent-claim-helper-command/agents/openai.yaml
- skills/agent-claim-helper-mcp/agents/openai.yaml
- skills/agent-claim-helper-command/scripts/claim.py
- agents/roles/dev-activities/dev-merge-coordinator.role.yaml
- agents/roles/project-setup/project-configurator.role.yaml
- PROJECT.yaml
- AGENTS.md
- README.md
- skills/route-documentation-work/assets/templates/project-template.yaml
- scripts/build-skill-docs.py
- scripts/generate-backlog-report.py
- scripts/render-agents-technology-skills.py
- scripts/agent_skill_evals/validation.py
- scripts/test_agent_claim.py
- scripts/test_agent_claim_helper.py
- scripts/test_agent_skill_evaluation_docs.py
- scripts/test_bundle_content.py
- scripts/test_generate_backlog_report.py
- scripts/test_role_mutation_policy.py
- scripts/test_technology_detection.py
- scripts/test_work_item_coordination.py
- design/agent-and-skill-evaluations.html
- design/agentic-configuration.html
- design/generic-agent-definitions-source.html
- design/object-oriented-agent-and-skill-model.md
- design/object-oriented-skill-group-models.md
- design/orchestrated-development-lifecycle.html
- design/skill-groups/backlog-management.md
- design/skill-groups/concurrent-tasking.md
- design/skill-groups/direct-main-delivery.md
- design/skill-groups/review-and-verification.md
- design/skills-modularization.html
- design/work-item-provider-and-completion-contracts.md
- design/generated/role-definitions.js
- design/generated/skill-definitions.js
- design/generated/template-definitions.js
- generated/adapters/claude/agents/dev-merge-coordinator.md
- generated/adapters/claude/agents/project-configurator.md
- generated/adapters/codex/agents/dev-merge-coordinator.toml
- generated/adapters/codex/agents/project-configurator.toml
- generated/adapters/gemini/agents/dev-merge-coordinator.md
- generated/adapters/gemini/agents/project-configurator.md
- generated/adapters/junie/agents/dev-merge-coordinator.md
- generated/adapters/junie/agents/project-configurator.md
- Affected exact evaluation suite, scenario, fixture, and suite-contract files identified by the required repository-wide reference search.

### Approval Resolution

Approved at creation. On 2026-08-06, in Codex task 019faeef-e932-7352-a53d-fdb1535f5994, the user requested that agent-claim be changed to resource-claim and that the rename include tests. This approval covers the exact governed canonical sources listed above only. Any additional governed skill-definition path discovered during implementation requires separate scope-specific approval; existing approval for the listed paths remains valid.

## Prior Starting Handoff Evidence

Starting Recorded At: 2026-08-07T00:14:24Z

Coordinator: Dev Backlog Coordinator task `019fb057-1767-7ef2-b5fa-41f4417b20b3`

Normalized Objective: Rename the resource-claim policy and helper family throughout current operational sources, generated artifacts, focused tests, evaluations, installation references, and any required state-safe compatibility boundary, while preserving historical evidence and the existing policy/interface/provider separation.

Launch Result: Not attempted

Canonical Execution: None

Last Contact At: None

Next Reconciliation At: 2026-08-07T00:29:24Z

Intended Root Role: Dev Orchestrator

Scheduling Evidence: Selected as the older of two overlapping Ready rename features. `rename-direct-main-to-main-branch` remains Ready until this item's shared source, generator, and integration lanes clear.

## Active Execution Evidence

Condition Type: root-execution

Owner: Root Dev Orchestrator task `019fd993-01d4-7380-b722-b7c328bdb637`

Evidence: The same canonical task resumes accepted candidate commit `140f0bbdbfe43925e54e89c1efd49facb30a3b81` on branch `codex/rename-agent-claim-to-resource-claim` in `/Users/martinbechard/.codex/worktrees/e800/dev-methodology`; the candidate worktree is clean, the independent review is PASS with no remaining findings, and the verifier accepted the exact commit. Authoritative main is clean at `df715f12c9b78c55d8ed29453fef488c9d76a1d4`. The former overlapping documentation bytes were committed separately as `731baf40ce11de4c279f3f4bd37c3c4e58d7e899`, with the sole changed path `design/skill-groups/concurrent-tasking.md` and committed blob SHA-256 `1d6e7b6e6157e4e8cd53d32e5f26b77a199a309a5c9ee1a9f598ffa894a76ad6`. Provider Blocked to Ready is durable at `b8867489`; Ready to Starting is durable at `df715f12`. This transaction accepts Starting to Running before one current-main reconciliation.

Observed At: 2026-08-07T01:09:35Z

Started At: 2026-08-07T01:09:25Z

Deadline or Expires At: 2026-08-07T03:09:35Z

Next Action: Commit only this Starting to Running provider transaction, release the exact provider path and activity `update` claims, acquire exact Work Item ID activity `work`, then reconcile accepted candidate `140f0bbd` against current main exactly once and run only integration-sensitive focused checks before terminal provider closure.

Next Reconciliation At: 2026-08-07T01:24:35Z

## Blocked Evidence

Blocked At: 2026-08-07T01:04:06Z

Exact Blocker: Direct-main delivery cannot reconcile accepted candidate path `design/skill-groups/concurrent-tasking.md` while authoritative main contains a pre-existing user-owned unstaged edit to that same path.

Blocker Owner: Dev Backlog Coordinator must coordinate the existing documentation owner without staging, absorbing, reverting, or overwriting the user-owned edit in this work item.

Coordinator Next Action: Ask canonical documentation task `019faeed-f816-7d43-819d-814bad4e309c` to commit or explicitly disposition its already-authorized one-line `pull request workflow` edit as a distinct scoped transaction, then reconcile the clean-main boundary.

Unblock Condition: The user-owned `design/skill-groups/concurrent-tasking.md` edit reaches a committed or explicitly restored clean-main disposition outside this work item, with exact release notification and no loss of its bytes.

Permitted Resumption: Preserve canonical task `019fd993-01d4-7380-b722-b7c328bdb637` and resume through Blocked -> Ready -> Starting -> Running before delivery. Reconcile accepted candidate `140f0bbdbfe43925e54e89c1efd49facb30a3b81` against then-current main once and rerun only integration-sensitive checks.

Accepted Candidate: `140f0bbdbfe43925e54e89c1efd49facb30a3b81` on `codex/rename-agent-claim-to-resource-claim`; private worktree clean.

Accepted Path Manifest: 137 exact paths; SHA-256 `b53b772d43fcaca86a169911a95107d15eabe6955b2e2039f8e6394e3663927d`.

Review And Verification: Independent review PASS with no findings after correction; verifier VERIFIED. Focused skill, metadata, generation, bundle, coordination, fixture, and diff checks passed. Two broader-suite failures are recorded unrelated baselines: policy `KeyError: outcome` and helper count `47 != 50`.

Preserved User Edit Evidence: Worktree SHA-256 `1d6e7b6e6157e4e8cd53d32e5f26b77a199a309a5c9ee1a9f598ffa894a76ad6`; binary diff SHA-256 `25c3b9e05c8b390e4af39f2b92bbf02eee76161a5615389901cf08f321d93ff5`; index blob `ecdd6f2a3eed360f2f3aec1085ad8cbac37105e5`.

Claim Disposition: The canonical task released exact work claim disposition `blocked` with blocker reference `direct-main-overlap:design/skill-groups/concurrent-tasking.md`; registry was empty before this provider transition.

## Unblock Reconciliation

Resolved At: 2026-08-07T01:08:04Z

Resolution Evidence: Canonical documentation task `019faeed-f816-7d43-819d-814bad4e309c` committed only `design/skill-groups/concurrent-tasking.md` as `731baf40ce11de4c279f3f4bd37c3c4e58d7e899`. The commit's parent is `eaecb61ab673ec2724daaaefd836a8abe9a53596`, its changed-path set is exactly that documentation path, and its blob equals the preserved user bytes with SHA-256 `1d6e7b6e6157e4e8cd53d32e5f26b77a199a309a5c9ee1a9f598ffa894a76ad6`.

Claim And Checkout Evidence: Documentation claim release event `05be4286-41e2-453e-83b4-701c0af80c19`; primary main clean at `731baf40ce11de4c279f3f4bd37c3c4e58d7e899`; registry empty before this transition.

Next Action: Dev Backlog Coordinator records Ready -> Starting for the same canonical task `019fd993-01d4-7380-b722-b7c328bdb637`; that task then records Starting -> Running and reconciles accepted candidate `140f0bbdbfe43925e54e89c1efd49facb30a3b81` against current main once.

## Starting Handoff Evidence

Starting Recorded At: 2026-08-07T01:08:36Z

Coordinator: Dev Backlog Coordinator task `019fb057-1767-7ef2-b5fa-41f4417b20b3`

Normalized Objective: Resume the accepted resource-claim rename candidate `140f0bbdbfe43925e54e89c1efd49facb30a3b81` after the overlapping user-owned documentation edit was committed separately, reconcile once against current main, and complete focused integration and terminal provider closure.

Launch Result: Requested

Canonical Execution: `019fd993-01d4-7380-b722-b7c328bdb637`

Last Contact At: 2026-08-07T01:08:36Z

Next Reconciliation At: 2026-08-07T01:23:36Z

Intended Root Role: Dev Orchestrator

Scheduling Evidence: Reuse the preserved canonical task and candidate; do not create a replacement. The overlapping `rename-direct-main-to-main-branch` item remains Ready until this delivery and shared generated paths are terminally reconciled.
