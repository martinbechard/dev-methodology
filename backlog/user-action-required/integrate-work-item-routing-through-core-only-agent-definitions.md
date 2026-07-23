# Integrate Work-Item Routing Through Core-Only Agent Definitions

Status: User Action Required

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/integrate-work-item-routing-through-core-only-agent-definitions.md

Completion: direct-main

## Blocked State

- Previous canonical Dev Orchestrator task: 019f80f3-41d5-7481-910e-6f54d43083ae.
- Previous worktree: /Users/martinbechard/.codex/worktrees/2c00/dev-methodology.
- Previous branch: codex/integrate-work-item-contracts-across-bundle.
- Previous starting main commit: 2ddedf5a83ca8567ac3de93867a3f90624a2e28c.
- Owner: Root Dev Orchestrator.
- Claim: None.
- Phase: Blocked after approval resolution because the accepted core-only routing design depends on simplify-project-configuration-setup-and-skill-routing.
- User approval: On 2026-07-21, in parent task 019f77f4-c4bd-7c91-b197-c987a7beb838, the user directed: "I approve the items in holding". The prior exact codex-workitem-coordination approval remains recorded below.
- Unblock condition: backlog/feature-backlog/simplify-project-configuration-setup-and-skill-routing.md is integrated, verified, and archived as Completed on main.
- Next action owner: Dev Backlog Coordinator.
- Resumption: Reconcile the completed dependency, transition through Ready, acquire a new canonical Dev Orchestrator, and only then record Running.
- Verification: focused provider, completion, selector, role, metadata, renderer, migration, stale-name, and evaluation checks first; then the item-required full repository, project-wiki, catalog, generated-adapter, disposable smoke, and install/refresh release gates.

## Current Execution / Ownership

- Owner: User Action Required.
- Canonical task: 019f8b4c-8fb9-7d23-9eed-7bbb4968e163.
- Claim: route-core-only-gitlab-manager-approval-019f8b4c, lifecycle transition only.
- Canonical worktree: /Users/martinbechard/.codex/worktrees/d9e0/dev-methodology, clean.
- Branch: codex/integrate-work-item-routing-core-only-019f8b4c at 14adbbfa70bb6640e90c8ec68b177557add29d48.
- Starting main: 83135ebc590c2c244cf42283ae3f760521c55ed0.
- Phase: User Action Required for the exact GitLab terminal-reconciliation approval.
- Lifecycle transition: Running -> User Action Required pending an exact governed-definition approval under canonical thread 019f8b4c-8fb9-7d23-9eed-7bbb4968e163.
- Accepted candidate: 14adbbfa70bb6640e90c8ec68b177557add29d48, clean and preserved unchanged pending the user decision.
- Integration wait started at: None.
- Integration wait attempts: 0.
- Completion wait started at: None.
- Completion wait attempts: 0.
- Open issues: User approval is required before changing the exact GitLab terminal-reconciliation scope below.
- Next owner: User, then the Root Dev Orchestrator after an approved resolution.

## Resumption Evidence — 2026-07-22

- Satisfied dependency: backlog/completed-backlog/features/simplify-project-configuration-setup-and-skill-routing.md, completed at a07ffb333db915294513c8ce798436d347d6dd98 with integrated delivery baff164e94557bff47a32b17fb64f3ecd4f6bf2a, recorded focused verification, integration-claim release, and cleanup evidence.
- Prior claim attempt: resume-core-only-work-item-routing-019f8b4c returned CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED, event 85cd9175-dfc1-460a-bf5a-fe828b0af090; it made no mutation.
- Fresh backlog claim: resume-core-only-work-item-routing-019f8b4c-2, acquired event ba5ae47a-ff1b-43e9-b7e4-6aa66e67ca37 from primary main.
- The exact prior approval remains authoritative.

## GitLab Terminal-Reconciliation Approval Gate — 2026-07-23

### Methodology Finding

Current Completion/Reconciliation lines 6-7 force RUNNING-or-BLOCKED after terminal failure. That contradicts approved durable AWAITING_REVIEW and coordinator capacity because it erases the durable review-wait state.

### Question for the User

Do you approve changing exactly skills/manage-gitlab-work-items/SKILL.md, with only its supported generated skill mirror and directly related tests/documentation, so a failed/partial terminal update preserves the current nonterminal lifecycle (AWAITING_REVIEW for feature-branch delivery, RUNNING for direct-main) or records BLOCKED, rather than always forcing RUNNING and erasing durable review-wait state?

### Why User Input Is Required

This changes a distributed skill definition. Repository policy requires explicit scope-specific user approval before the governed definition is mutated.

### Resolution

- Status: Pending.
- Pending user answer. The item transitioned from Running to User Action Required on 2026-07-23 under canonical task 019f8b4c-8fb9-7d23-9eed-7bbb4968e163.

### Unattended Work Boundary

Do not mutate skills/manage-gitlab-work-items/SKILL.md, its supported generated skill mirror, tests, documentation, or any other governed definition until the user answers the exact question. Preserve candidate 14adbbfa70bb6640e90c8ec68b177557add29d48 unchanged. No other governed scope is authorized.

## Feature-Branch Commit Ownership Approval Gate — 2026-07-23

### Methodology Finding

The current feature-branch completion skill still implements source and applies corrections itself. That contradicts the approved Dev Coder candidate -> review -> verification -> Commit ordering.

### Question for the User

Do you approve changing exactly skills/complete-work-item-feature-branch/SKILL.md, with only its supported generated skill mirror and directly related tests/documentation, so feature-branch Commit consumes an already accepted reviewed/verified candidate, owns only publication/review-check/merge/main observation, and returns source-correction requests to Dev Orchestrator for Dev Coder correction plus fresh review/verification before resuming the same delivery identity?

### Why User Input Is Required

This changes a distributed skill definition. Repository policy requires explicit scope-specific user approval before the governed definition is mutated.

### Resolution

- Date: 2026-07-22.
- Answer: Approved.
- User wording: "I approve".
- Provenance: direct response in parent coordination thread 019f8b00-e6d7-7841-854a-40a50ca4e7f2 to the latest recorded Core-only Routing feature-branch Commit ownership approval gate.
- Approved governed skill scope: exactly skills/complete-work-item-feature-branch/SKILL.md.
- Approved dependent scope: only its supported generated skill mirror and directly related tests and documentation.
- Approved goal: feature-branch Commit consumes an already accepted reviewed and verified candidate; owns publication, host review and checks, merge, and main observation only; returns source-correction requests to Dev Coder through the Orchestrator for fresh review and verification before resuming the same delivery identity; and does not modify source itself.
- Exclusion: no other governed scope is approved.
- Disposition: User Action Required -> Ready -> Running under canonical thread 019f8b4c-8fb9-7d23-9eed-7bbb4968e163.

### Unattended Work Boundary

Mutate only skills/complete-work-item-feature-branch/SKILL.md, its supported generated skill mirror, and directly related tests and documentation. Do not widen any scope. Preserve candidate evidence until the approved correction and verification supersede it.

### Handoff Evidence

- Approval-resolution claim: approve-core-only-feature-branch-019f8b4c, acquired event 313f765a-a698-4c2e-8da1-966a85947d42 from primary main.

## Durable AWAITING_REVIEW File-Manager Approval Gate — 2026-07-23

### Methodology Finding

Current file-manager wording says Running persists until Completed and correctable review returns AWAITING_REVIEW to Running. That contradicts the newly approved exactly-once durable AWAITING_REVIEW update and idempotent resumption.

### Question for the User

Do you approve changing exactly skills/manage-file-work-items/SKILL.md, with only its supported generated skill mirror and directly related tests/documentation, so durable AWAITING_REVIEW remains AWAITING_REVIEW through same-delivery review corrections and only the later Commit READY handoff permits terminal COMPLETED?

### Why User Input Is Required

This changes a distributed skill definition. Repository policy requires explicit scope-specific user approval before the governed definition is mutated.

### Resolution

- Date: 2026-07-22.
- Answer: Approved.
- Clarification: the user's earlier wording, "ok sounds good - the task is still waiting for my confirmation to resume", was intended as approval.
- User wording: "In fact both are approved".
- Provenance: direct clarification and approval in parent coordinator thread 019f8b00-e6d7-7841-854a-40a50ca4e7f2 in response to this exact durable AWAITING_REVIEW file-manager question.
- Approved governed skill scope: exactly skills/manage-file-work-items/SKILL.md.
- Approved dependent scope: only its supported generated skill mirror and directly related tests and documentation.
- Approved goal: durable AWAITING_REVIEW survives same-delivery review corrections and only Commit READY permits terminal COMPLETED.
- Exclusion: no other governed scope is approved.
- Disposition: User Action Required -> Ready -> Running under canonical thread 019f8b4c-8fb9-7d23-9eed-7bbb4968e163.

### Unattended Work Boundary

Mutate only skills/manage-file-work-items/SKILL.md, its supported generated skill mirror, and directly related tests and documentation. Do not widen any scope. Preserve candidate evidence until the approved correction and verification supersede it.

### Handoff Evidence

- Approval-resolution claim: approve-core-only-file-manager-019f8b4c, acquired event df7db8e2-d4dd-4e67-a791-f155d1ab6287 from primary main.

## Commit AWAITING_REVIEW Persistence Approval Gate — 2026-07-23

### Methodology Finding

Existing manager, provider, and coordinator contracts require durable AWAITING_REVIEW state for inventory and capacity visibility. The current zero-Persistence orchestration leaves provider state Running and unobservable at the nonterminal Commit boundary.

### Question for the User

Do you approve changing exactly agents/roles/dev-activities/dev-orchestrator.role.yaml and skills/codex-workitem-coordination/SKILL.md, with only supported generated mirrors and directly related tests/documentation, so Commit AWAITING_REVIEW triggers one nonterminal Dev Backlog Steward Persistence update that records durable AWAITING_REVIEW, while Commit itself never dispatches Persistence and terminal COMPLETED closure still occurs exactly once only after Commit READY?

### Why User Input Is Required

This changes one conceptual role definition and one distributed coordination skill definition. Repository policy requires explicit scope-specific user approval before either governed definition is mutated.

### Resolution

- Date: 2026-07-22.
- Answer: Approved.
- User wording: "there are coding details I don't need to approve, but I approve the goal."
- Provenance: direct response in parent coordinator thread 019f8b00-e6d7-7841-854a-40a50ca4e7f2, followed by the user's quote of the exact Commit AWAITING_REVIEW persistence approval question.
- Approved governed scope: exactly agents/roles/dev-activities/dev-orchestrator.role.yaml and skills/codex-workitem-coordination/SKILL.md.
- Approved dependent scope: only their supported generated mirrors and directly related tests and documentation.
- Approved goal: Commit AWAITING_REVIEW triggers one nonterminal Persistence update recording durable AWAITING_REVIEW while terminal COMPLETED occurs exactly once only after Commit READY.
- Exclusion: unrelated coding details, any other governed definition, and the separate lifecycle evaluation-catalog path are not approved.
- Disposition: User Action Required -> Ready -> Running under canonical thread 019f8b4c-8fb9-7d23-9eed-7bbb4968e163.

### Unattended Work Boundary

Mutate only agents/roles/dev-activities/dev-orchestrator.role.yaml and skills/codex-workitem-coordination/SKILL.md, their supported generated mirrors, and directly related tests and documentation. Do not widen any other scope or the separate lifecycle evaluation-catalog path. Preserve candidate evidence until the approved correction and verification supersede it.

### Handoff Evidence

- Approval-resolution claim: approve-core-only-awaiting-review-019f8b4c, acquired event 2abcdd26-46ee-4066-9794-df8f2682e77b from primary main.

## Completion Skills Approval Gate

- Canonical thread 019f8b4c-8fb9-7d23-9eed-7bbb4968e163 is idle after fresh review.
- Fresh review found a new governed contradiction requiring exactly skills/complete-work-item-direct-main/SKILL.md and skills/complete-work-item-feature-branch/SKILL.md.
- No mutation to either completion-skill path has occurred.
- Recovery evidence: clean preserved candidate 8a5cce44 on branch codex/integrate-work-item-routing-core-only-019f8b4c; private worktree /Users/martinbechard/.codex/worktrees/d9e0/dev-methodology is clean.

### Question For The User

Do you approve changing exactly skills/complete-work-item-direct-main/SKILL.md and skills/complete-work-item-feature-branch/SKILL.md, together with only their supported generated mirrors and directly related tests and documentation, to resolve the reviewed completion-workflow contradiction in the provider-neutral Core-only Routing candidate? No other governed definition is approved.

### Why User Input Is Required

Repository policy requires exact scope-specific approval before these two governed completion-skill mutations.

### Resolution

- Date: 2026-07-22.
- Answer: Approved.
- User wording: "approved to proceed".
- Provenance: direct response in parent coordinator thread 019f8b00-e6d7-7841-854a-40a50ca4e7f2 to the separately stated completion-skills approval question.
- Approved governed skill scope: exactly skills/complete-work-item-direct-main/SKILL.md and skills/complete-work-item-feature-branch/SKILL.md.
- Approved dependent scope: only their supported generated mirrors and directly related tests and documentation.
- Exclusion: no other governed definition is approved.
- Disposition: User Action Required -> Ready -> Running under canonical thread 019f8b4c-8fb9-7d23-9eed-7bbb4968e163.

### Unattended Work Boundary

Mutate only the approved completion-skill paths, their supported generated mirrors, and directly related tests and documentation. Do not widen any other governed scope. Preserve every prior approval and evidence.

### Handoff Evidence

- Backlog handoff claim: route-core-only-completion-skills-019f8b4c, acquired event 08400cca-910f-4dab-a177-ef07efcfbcc7 from primary main.
- Approval-resolution claim: approve-core-only-completion-skills-019f8b4c, acquired event 118edd20-35a1-4979-b404-20fe256dd24f from primary main.

## Dev Backlog Coordinator Role Approval Gate

- Canonical thread 019f8b4c-8fb9-7d23-9eed-7bbb4968e163 received the prior metadata approval, passed its check, and committed clean correction 1f7f1e5587bb63eef54202cd91bab501d5e68e37.
- Fresh review found exactly one further governed gap: agents/roles/dev-activities/dev-backlog-coordinator.role.yaml remains file-only while the coordination skill is provider-selected.
- No mutation to this role has occurred.
- Recovery evidence: branch codex/integrate-work-item-routing-core-only-019f8b4c at 1f7f1e5587bb63eef54202cd91bab501d5e68e37 and private worktree /Users/martinbechard/.codex/worktrees/d9e0/dev-methodology are clean.

### Question For The User

Do you approve changing exactly agents/roles/dev-activities/dev-backlog-coordinator.role.yaml, together with only its supported generated mirrors and directly related tests and documentation, so Dev Backlog Coordinator supports the selected Persistence and Commit workflows instead of remaining file-only?

### Why User Input Is Required

Repository policy requires exact scope-specific approval before this conceptual role definition mutation.

### Resolution

- Date: 2026-07-22.
- Answer: Approved.
- User wording: "ok I approve of it".
- Provenance: direct response in parent coordinator thread 019f8b00-e6d7-7841-854a-40a50ca4e7f2 to the separately stated Dev Backlog Coordinator role approval question.
- Approved governed role scope: exactly agents/roles/dev-activities/dev-backlog-coordinator.role.yaml.
- Approved dependent scope: only its supported generated mirrors and directly related tests and documentation.
- Exclusion: no other governed scope is approved.
- Disposition: User Action Required -> Ready -> Running under canonical thread 019f8b4c-8fb9-7d23-9eed-7bbb4968e163.

### Unattended Work Boundary

Mutate only the approved agents/roles/dev-activities/dev-backlog-coordinator.role.yaml role path, supported mirrors, and directly related tests and documentation. Do not widen any other governed scope. Preserve every prior approval and evidence.

### Handoff Evidence

- Backlog handoff claim: route-core-only-coordinator-role-019f8b4c, acquired event 62d7cd79-a256-47aa-9d7a-c648fc22f7b3 from primary main.
- Prior blocked no-mutation claim attempt: b351f3c8-93bd-498b-bd6d-51430f8cd2de, SHARED_CHECKOUT_RELEASE_REQUIRED.
- Bounded-release evidence: child release event 2533c4ea-9223-4cc9-ab3d-8a075584a700 after clean preserved commit 92d4e328a279e3f2e6fea693412e2810a5d7d7f1; root no-change release event b9ada40e-da6f-4267-8ee8-18e16cad3b62.
- Approval-resumption claim: approve-core-only-coordinator-role-019f8b4c, acquired event d03860c9-d6f0-452c-82c0-5ac3b06a5330 from primary main.

## Codex Metadata Approval Gate

- Canonical thread 019f8b4c-8fb9-7d23-9eed-7bbb4968e163 is idle.
- Latest correction and focused checks completed; no metadata mutation occurred.
- Recovery evidence: branch codex/integrate-work-item-routing-core-only-019f8b4c is at c9b9a2d, with preserved uncommitted correction bytes in private worktree /Users/martinbechard/.codex/worktrees/d9e0/dev-methodology. Do not describe this worktree as clean.
- Remaining exact governed metadata source: skills/codex-workitem-coordination/agents/openai.yaml.

### Question For The User

Do you approve changing skills/codex-workitem-coordination/agents/openai.yaml so its Codex-facing description matches the now provider-neutral coordination skill?

### Why User Input Is Required

Repository policy requires exact scope-specific approval before this governed metadata mutation.

### Resolution

- Date: 2026-07-22.
- Answer: Approved.
- User wording: "yes".
- Provenance: direct response in parent coordinator thread 019f8b00-e6d7-7841-854a-40a50ca4e7f2 to the separately stated Codex metadata approval question.
- Approved governed metadata scope: exactly skills/codex-workitem-coordination/agents/openai.yaml.
- Exclusion: no other governed or metadata scope is authorized by this answer.
- Separate boundary: this approval does not resolve the lifecycle and deadline ten-path question.
- Disposition: User Action Required -> Ready -> Running under canonical thread 019f8b4c-8fb9-7d23-9eed-7bbb4968e163.

### Unattended Work Boundary

Mutate only the approved skills/codex-workitem-coordination/agents/openai.yaml metadata path within the preserved prior approvals and evidence. Do not widen any other governed or metadata scope. The lifecycle and deadline ten-path question remains unresolved and prohibited.

### Handoff Evidence

- Backlog handoff claim: route-core-only-codex-metadata-019f8b4c, acquired event 803aa720-2333-4461-8514-555f70b17e51 from primary main.
- Approval-resumption claim: approve-core-only-codex-metadata-019f8b4c, acquired event 618e04bf-56f1-4554-b290-e10e7880cb2b from primary main.
- Ownership-record correction claim: correct-core-only-routing-current-owner-019f8b4c, acquired event b8f6a0ab-28fc-4056-a15f-76ee31c7e18c from primary main.

## Resolved Approval

### Question for the User

Do you approve changing exactly skills/codex-workitem-coordination/SKILL.md so Dev Backlog Steward applies the management skill selected by the effective work-item provider, instead of hard-coding manage-backlog or manage-file-work-items, together with only its supported generated skill mirror and directly related tests and documentation?

### Why User Input Is Required

The final bundle integration must remove the retired manage-backlog caller from the coordination skill. Replacing it permanently with manage-file-work-items would couple the provider-neutral coordinator to the file provider and make future GitHub, GitLab, Jira, Azure DevOps, or other providers require another coordination definition change. The provider-neutral wording changes a governed distributed skill definition and therefore requires exact user approval before mutation.

### Options and Tradeoffs

- Approve the provider-neutral wording: one coordinator and one Dev Backlog Steward continue to work with the provider selected in PROJECT.yaml; provider-specific create and manage skills remain interchangeable capabilities rather than separate agents.
- Decline: the integration cannot truthfully remove the retired caller while preserving future provider support, so this final bundle-integration item remains unresolved.

### Resolution

Approved on 2026-07-21. In canonical task 019f80f3-41d5-7481-910e-6f54d43083ae, the user answered "ok agreed" in user message item-30 after the task presented the provider-neutral coordination wording and core-only agent-definition direction. The task acknowledged in item-32 that this resolves the provider-neutral coordination question.

Approved governed scope: change exactly skills/codex-workitem-coordination/SKILL.md so Dev Backlog Steward applies the management skill selected by the effective work-item provider instead of hard-coding manage-backlog or manage-file-work-items, together with only its supported generated skill mirror and directly related tests and documentation.

### Unattended Work Boundary

The approval is resolved, but this item is intentionally deferred. Do not dispatch it until backlog/holding/simplify-project-configuration-setup-and-skill-routing.md is accepted and supplies the final project binding and installation contracts. On resumption, create or assign one canonical Dev Orchestrator task and run the exact governed-definition pre-mutation check using this recorded provenance before mutating skills/codex-workitem-coordination/SKILL.md.

## Expanded Governed-Definition Approval — 2026-07-22

### Question for the User

Do you approve changing exactly the three conceptual role definitions and retiring exactly the execute-workitem skill and metadata paths listed above, together with its references and only supported generated mirrors and directly related tests and documentation, so Persistence and Commit routing comes exclusively from PROJECT.yaml and AGENTS.md?

### Resolution

Approved on 2026-07-22. In canonical task 019f8b4c-8fb9-7d23-9eed-7bbb4968e163, the user answered "approved" directly after the question above.

Approved governed scope:

- agents/roles/dev-activities/dev-coder.role.yaml.
- agents/roles/dev-activities/dev-orchestrator.role.yaml.
- agents/roles/dev-activities/dev-backlog-steward.role.yaml.
- skills/execute-workitem/SKILL.md.
- skills/execute-workitem/agents/openai.yaml.
- References to execute-workitem, only the supported generated mirrors for those governed sources, and directly related tests and documentation.

Authorized outcome: Persistence and Commit routing comes exclusively from PROJECT.yaml and AGENTS.md. Run the required governed-definition pre-mutation check with an approval record that cites this provenance before each approved canonical definition mutation. This approval does not authorize unrelated governed definitions, product files, or changes outside the listed scope.

## Summary

Integrate the stabilized work-item persistence and commit contracts without placing technology-specific, persistence-specific, or commit-specific skills in conceptual agent definitions. Keep agent definitions limited to technology-agnostic core workflows, record project selections in PROJECT.yaml, and render selected concrete skills by reference through root or nested AGENTS.md guidance.

## Context

This is the final integration item in the Work-Item Provider And Completion Contracts series. Provider and completion capabilities remain independent, but conceptual agent definitions must stay reusable across technologies, persistence systems, and commit workflows. PROJECT.yaml records project-owned selections, and generated AGENTS.md guidance binds those selections to concrete provider, commit, and folder technology skills.

The current integration must not replace one hard-coded provider dependency with another. Dev Coder, Dev Orchestrator, and Dev Backlog Steward use generic core workflows; adding or changing a provider must not require a new agent or a conceptual role-definition change.

## Requirements

- Keep every conceptual agent definition limited to technology-agnostic core skills.
- Keep Dev Backlog Steward provider-neutral and route creation and lifecycle changes through the effective project binding rather than hard-coded provider skills.
- Keep Dev Coder independent of provider lifecycle mutation and provider-specific persistence skills.
- Keep Dev Orchestrator provider-neutral while preserving implementation, integration, and backlog ownership boundaries.
- Update project-configurator and any setup roles to preserve selector-only PROJECT.yaml and reference-only AGENTS.md behavior.
- Render the selected persistence create/manage skills and commit skill by reference through applicable AGENTS.md guidance.
- Keep confirmed technology skills independently routed at their applicable folder scopes.
- Require missing, unsupported, or mismatched bindings to return BLOCKED without fallback or shadow persistence.
- Update skill metadata and Codex interface descriptions for every added, renamed, retired, or conditionally loaded skill.
- Regenerate native adapters, manifests, skill definitions, role definitions, hierarchy, support checklist, and other derived data from canonical sources.
- Update README.md and every relevant design page with the provider/completion separation, supported matrix, unsupported placeholders, direct-main semantics, and AWAITING_REVIEW boundary.
- Update evaluation skill probes, agent scenarios, runnable cases, workflow packs, Agent-suite contracts, and regression tests for the final identifiers and behavior.
- Add positive and negative coverage for every provider, completion process, UNSET, unsupported provider, invalid combination, shadow-queue prohibition, main reachability, and merge-evidence boundary.
- Define compatibility and retirement behavior for create-backlog, manage-backlog, file-based-backlog, github-issues-backlog, execute-workitem, simple-workitem, and feature-branch-workitem.
- Decide whether create-pull-request remains GitHub-oriented, becomes code-host-qualified, or is paired with a GitLab merge-request capability, and keep terminology and tools accurate.
- Sweep canonical sources, generated artifacts, examples, tests, backlog fixtures, installation assets, and design pages for stale identifiers and contradictory terminal-state language.
- Preserve unrelated work and avoid hand-editing generated output.
- Publish and refresh installed bundle artifacts only after source, generated, evaluation, and migration gates pass.

## Acceptance Criteria

- Every conceptual role contains only technology-agnostic core skills.
- Dev Coder, Dev Backlog Steward, and Dev Orchestrator contain no provider-specific persistence dependency.
- Changing a project's technology, Persistence, or Commit selection changes PROJECT.yaml and rendered AGENTS.md guidance rather than conceptual agent definitions.
- File, GitHub, and GitLab providers each support independent direct-main and feature-branch selection.
- Azure DevOps and Jira remain visible but consistently BLOCKED without fallback.
- Direct-main completion always names a commit reachable from main.
- Feature-branch publication remains AWAITING_REVIEW until required merge evidence exists.
- PROJECT.yaml and AGENTS.md contain selectors and skill references without duplicated procedures.
- Technology-skill inlining remains unchanged and separately testable.
- All source, metadata, generated, design, eval, and installed representations use the canonical identifiers.
- Retired names remain only in explicit migration tests or historical explanation.
- The support checklist distinguishes structural availability, implemented behavior, unsupported placeholders, and executed evidence truthfully.
- Full repository validation passes from a clean worktree and the integration is committed coherently.

## Dependencies

- backlog/holding/simplify-project-configuration-setup-and-skill-routing.md.
- render-selected-work-item-skills.
- transform-file-work-item-skills.
- split-github-work-item-skills.
- add-gitlab-work-item-skills.
- add-azure-devops-and-jira-placeholders.
- add-direct-main-completion-skill.
- add-feature-branch-completion-skill.

## Verification

- Run focused provider, completion, selector, role, metadata, renderer, migration, stale-name, and evaluation tests first.
- Run every repository-required skill validation and generated-output freshness check.
- Run the complete scripts unit-test suite with the supported Python interpreter.
- Run the complete project-wiki unit-test suite.
- Validate evaluation catalogs and inspect representative generated Codex, Claude, Gemini, and Junie definitions.
- Run authorized disposable provider and code-host smoke tests; keep unavailable external capability explicit rather than weakening gates.
- Install or refresh the bundle in a disposable target and verify selected workflow references and technology inlining from the loaded guidance.
- Run Git diff validation, confirm a clean worktree, and perform an independent source-versus-generated review.

## Notes

- This item integrates accepted lane outputs; it should not silently redesign the foundation contract.
- The user approved the provider-neutral coordination wording and the proposed core-only agent-definition direction in canonical task 019f80f3-41d5-7481-910e-6f54d43083ae.
- The prior waiting task should not consume a Running slot while this item is Holding.
- Live provider spending and mutation require explicit authority even when deterministic tests pass.
