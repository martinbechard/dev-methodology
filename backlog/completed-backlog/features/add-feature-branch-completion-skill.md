# Add Feature-Branch Completion Skill

Status: Completed

Type: Feature

## Current Execution

- Canonical Dev Orchestrator task: 019f7f8c-e6ed-7331-a7e1-9f5a32ebcb32.
- Branch: codex/add-feature-branch-completion-skill.
- Worktree: /Users/martinbechard/.codex/worktrees/ccd1/dev-methodology.
- Started from approved Ready commit 547e2159e5621351adb9a4e975b7659bc1993671.
- Scope remains limited to the approved feature-branch completion skill, its metadata, supported generated mirrors, and directly related non-governed tests and documentation.

## Completion Evidence

- Governed approval checks: the exact source paths skills/complete-work-item-feature-branch/SKILL.md and skills/complete-work-item-feature-branch/agents/openai.yaml each returned ALLOWED_APPROVED_DEFINITION_CHANGE from the recorded user-message provenance before mutation.
- Accepted candidate: dbaba08943320b24b7387ac621a4ae5cad0424f3 on codex/add-feature-branch-completion-skill, preserving the same branch through every accepted review correction.
- Independent methodology review: the final exact-candidate review passed with no actionable findings after corrections for task-level host selection, resumable work-item evidence, independently causal host-state tests, Git reachability, evaluation-probe boundaries, provider lifecycle handoff, and reciprocal workflow assertions.
- Independent focused verification: six feature-specific tests passed, including mocked GitHub and GitLab state transitions plus a disposable Git graph that rejects publication-only ancestry and accepts the published commit after merge. Python compilation, metadata freshness, skill documentation freshness, support-checklist freshness, and diff integrity also passed.
- Integrated delivery: candidate behavior was reconciled with the already integrated direct-main and provider skill catalog, then committed on main as a301068f32323472d24b13760c691faccae445f8 and 2a7aa7f7720f39a47536d003f6eb80dfbc49ddb5. Main remained clean.
- Focused post-integration verification: seven combined feature-branch, direct-main, pull-request, package, and metadata tests passed. Skill metadata, skill documentation, support-checklist and explorer output were current; Git diff validation passed. Structured YAML validation passed for the Codex metadata and both evaluation catalogs, and the feature skill's Markdown links passed.
- Validator boundary: MCP skill_validate rejected both the private and primary source checkout paths as outside its configured installed-skill roots. That structured boundary was not bypassed. Independent repository-native source validation passed during review and verification, while primary YAML, Markdown-link, generator, focused behavior, and compilation checks supplied the accepted source evidence.
- Integration ownership: exact project paths and merge:integration:main were held under claim feature-branch-completion-integration and released cleanly at event 574c9391-0261-4a80-aaa1-29fc8c396233.
- Terminal lifecycle ownership: exactly this active path and backlog/completed-backlog/features/add-feature-branch-completion-skill.md are held under claim feature-branch-completion-backlog. The claim is released immediately after this completion commit from clean main.
- Verification tier: focused Tier 1 checks plus the supported generated skill and support-data mirrors were selected for this bounded catalog item. No full live agent catalog or project-wiki regression was run solely for this item.
- Cleanup evidence: main contains the reviewed feature skill, metadata, dedicated host-state and Git-graph test, focused bundle assertions, evaluation probe and workflow membership, README and design explanation, and generator-current mirrors. The private worktree is clean; its two source commits are preserved by the two integration commits above, including semantic conflict reconciliation with sibling provider and completion additions, so the parent may perform patch-equivalent branch and worktree cleanup after this terminal claim releases.

## Approval Resolution

The user approved the exact governed definition scope as part of the originally requested work-item completion skills.

## Approved Scope

Do you approve creating skills/complete-work-item-feature-branch/SKILL.md with its agents/openai.yaml metadata, together with only its supported generated mirrors and directly related non-governed tests and documentation?

## Approval Evidence

- Basis: explicit-user-direction.
- Exact answer: “Ok - I approve all of the skills that I orignianlly requested”.
- Provenance: thread 019f77f4-c4bd-7c91-b197-c987a7beb838, message item-2093, applying to the exact feature-branch skill question above.

The decision gate is resolved. Delivery completion still requires implementation, the exact governed pre-mutation check, supported regeneration, independent review, focused verification, integration, and terminal backlog evidence.

## Summary

Add complete-work-item-feature-branch so implementation, provider-accurate pull or merge request publication, review, checks, merge, and final delivery evidence form one truthful completion process.

## Context

This item is a completion lane in the [Work-Item Provider And Completion Contracts series](../feature-backlog/work-item-provider-and-completion/index.md). The current feature-branch-workitem prototype correctly publishes completed work as ready for review, but AWAITING_REVIEW is a handoff state rather than backlog completion. The final contract must resume after review and verify merge evidence before the selected work-item provider is asked to close the item.

## Requirements

- Add the complete-work-item-feature-branch skill with provider-independent work-item inputs and explicit code-host and base-branch context.
- Create the feature branch before source mutation and preserve the same branch for accepted review corrections.
- Acquire and release repository ownership through agent-claim without absorbing unrelated work.
- Require coherent verified commits and a clean pushed branch before publication.
- Use create-pull-request as a subordinate capability only for a GitHub or other code host whose contract uses pull requests accurately.
- Use GitLab merge-request terminology and provider tools for GitLab publication, review, pipeline, and merge evidence.
- Define a provider-qualified publication capability when create-pull-request cannot accurately own both pull and merge requests.
- Publish completed work ready for review unless the user requests draft or concrete incomplete work requires it.
- Record base, head, dependencies, review order, checks, work-item reference, and observed ready or draft state.
- Return AWAITING_REVIEW after successful publication while approval, required checks, dependency merge, or final merge remains outstanding.
- Resume the same work item and branch for accepted review corrections, rerun affected checks, and update the existing pull or merge request.
- Return READY only after required review and check gates pass, the configured merge is observed on the base branch, the final merge commit is recorded, and provider lifecycle completion evidence is ready.
- Return BLOCKED with preserved branch, commits, publication URL, and exact missing evidence when publication, review, checks, merge, ownership, or authority cannot complete safely.

## Acceptance Criteria

- GitHub delivery uses pull-request terminology and GitHub evidence.
- GitLab delivery uses merge-request terminology and GitLab evidence.
- A ready published branch returns AWAITING_REVIEW, not READY, while merge evidence is absent.
- Accepted review corrections update the same branch and publication record.
- Required review, checks, dependency order, and merge are all observed before READY.
- A closed-unmerged or superseded publication cannot close the work item as completed.
- File, GitHub, and GitLab work-item providers can independently select the same feature-branch completion process.
- The final result identifies the merged base commit and the provider lifecycle update it authorizes.

## Dependencies

define-provider-and-completion-selector-contracts.

## Verification

- Add mocked code-host tests for branch creation, ready publication, explicit draft, review correction, check failure, approval, dependency order, merge, closed-unmerged, supersession, and missing authority.
- Add Git graph tests proving the published commit is present on the configured base after merge.
- Add provider terminology tests that reject GitHub-shaped GitLab output and merge-request-shaped GitHub output.
- Add negative tests proving publication alone cannot return READY or close a work item.
- Run authorized disposable-repository smoke tests for each implemented code host.
- Run Agent Skill validation, generated-output checks, focused publication and claim tests, full repository tests, project-wiki tests, and Git diff validation.

## Notes

- Human review may span multiple runs; durable publication identity and state are required for resumption.
- This completion skill coordinates delivery evidence but does not own the provider work-item queue.
