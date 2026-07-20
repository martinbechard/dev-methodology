# Add GitLab Work-Item Skills

Status: Completed

Type: Feature

## Completed Execution

- Canonical Dev Orchestrator task: 019f7f89-2eb3-74c2-bb87-191d19a9efe4.
- Branch: codex/add-gitlab-work-item-skills.
- Worktree: /Users/martinbechard/.codex/worktrees/6e52/dev-methodology.
- Started from approved Ready commit 4a7cb49119def8dde665f8a2f9f5508adb9edd86.
- Scope remains limited to the two approved GitLab skill packages, their metadata, supported generated mirrors, and directly related non-governed tests and documentation.

## Completion Evidence

- Exact governed pre-mutation checks returned ALLOWED_APPROVED_DEFINITION_CHANGE for both SKILL.md paths and both agents/openai.yaml paths using the user-message provenance recorded below.
- Accepted private candidate: a642928f8a6798cb3d3d71f78acecb01ab4ed920 on codex/add-gitlab-work-item-skills.
- Independent methodology review: ACCEPTED after correcting terminal sequencing so READY and delivery evidence precede the GitLab terminal update, and observed terminal state precedes terminal evidence and lifecycle COMPLETED.
- Independent focused verifier: PASS for the exact seven-path cumulative diff, metadata freshness, supported generated-document freshness, two GitLab package and contract tests, diff integrity, clean worktree, and generated-mirror scope.
- Main integration claim: integrate-gitlab-work-item-skills-019f7f89 acquired at journal event 2de66243-ae84-4ec9-b252-74d9173732ad for exactly the seven integrated paths and merge:integration:main.
- Integrated main commit: e249af9f995545eb15fea548cfa2402d0eb10013.
- Post-integration verification passed on main: exact-package metadata check, build-skill-docs freshness, two focused bundle tests, commit diff integrity, main reachability, and byte-for-byte equality between all accepted candidate paths and the integrated paths.
- Integration claim released normally at journal event da1181a8-b7e7-4b01-b3b0-b04224a24c23 from clean main.
- Work-item completion claim: complete-gitlab-work-item-skills-019f7f89 acquired at journal event 70881bd1-2759-4598-86e2-3330bca96889 for only this active path and its completed destination.
- Full catalog, project-wiki, hierarchy, support-checklist, and live GitLab smoke suites were not run because this is a bounded Tier 1/2 skill addition and no authorized disposable GitLab project or provider runtime is available.
- The preferred MCP package and YAML validators rejected this linked worktree as outside their configured roots. The corrected independent gate preserved that structured rejection and did not bypass it.
- Cleanup eligibility: the private worktree is clean and the accepted seven-path candidate is patch-equivalent to main commit e249af9f995545eb15fea548cfa2402d0eb10013.

## Deferred Follow-Up

The shared metadata generator currently derives Gitlab rather than canonical GitLab in display names. The exact two-file proposal in candidate commit fca057871b3772c83665cef5e8e8bd044078014b adds the brand map in scripts/openai_metadata.py and its focused test in scripts/test_openai_metadata.py. That proposal passed its focused test but is deliberately excluded from this integrated item pending a separate scope-specific user decision.

## Approval Resolution

The user approved the exact governed definition scope.

## Approved Scope

Do you approve creating skills/create-gitlab-work-item/SKILL.md and skills/manage-gitlab-work-items/SKILL.md with their agents/openai.yaml metadata, together with only their supported generated mirrors and directly related non-governed tests and documentation?

## Approval Evidence

- Basis: explicit-user-direction.
- Exact answer: “Ok”.
- Provenance: thread 019f77f4-c4bd-7c91-b197-c987a7beb838, message item-2089, directly answering the exact question above.

The decision gate is resolved. Delivery completion still requires implementation, exact governed pre-mutation checks, supported regeneration, independent review, focused verification, integration, and terminal backlog evidence.

## Summary

Add symmetric create-gitlab-work-item and manage-gitlab-work-items skills that use GitLab provider tools as the sole issue authority and preserve GitLab merge-request terminology and lifecycle behavior.

## Context

This item is a provider lane in the [Work-Item Provider And Completion Contracts series](../feature-backlog/work-item-provider-and-completion/index.md). GitLab must be a first-class provider rather than a GitHub-shaped alias. Its issue references, labels, milestones, relationships, merge requests, approvals, pipelines, and merge evidence must be expressed through GitLab capabilities and terminology.

## Requirements

- Create create-gitlab-work-item for duplicate search, issue creation, typed content, labels, milestones or relationships when configured, acceptance criteria, and initial ownership evidence.
- Create manage-gitlab-work-items for lookup, assignment, lifecycle updates, dependencies, delivery references, blocking, completion, reopening, and reporting.
- Use authenticated GitLab provider tools for every read and mutation that establishes issue authority.
- Verify the observed namespace, project, issue internal identifier, URL, state, labels, assignees, relationships, and updated content after mutation.
- Use merge request, approval, pipeline, and merge terminology accurately.
- Prohibit repository backlog files, cached issue mirrors, GitHub fallbacks, or generic external mutation when GitLab is selected.
- Return BLOCKED when authentication, project authority, required provider capability, or mutation permission is unavailable.
- Keep issue completion independent from delivery completion while recording branch, commit, merge-request, approval, pipeline, and merge references.
- Support one-item explicit GitLab requests without silently changing the project default.
- Define provider-tool absence as BLOCKED rather than routing to GitHub or the file provider.

## Acceptance Criteria

- Creation and management route to distinct symmetric GitLab skills.
- Both skills use GitLab provider evidence and return the observed project, issue identity, URL, and state.
- Duplicate detection prevents a second issue for the same durable work.
- A missing GitLab provider tool or permission blocks without writing under backlog or calling another provider.
- Merge-request publication does not automatically close the issue.
- Configured completion evidence can close the issue and remains visible in GitLab history.
- GitLab examples and outputs never use pull request where merge request is meant.
- No active GitLab provider path creates a shadow file item.

## Dependencies

define-provider-and-completion-selector-contracts.

## Verification

- Add mocked provider tests for search, create, duplicate, update, relationship, block, reopen, close, permission denial, authentication failure, missing tool, and partial mutation.
- Add authorized disposable-project smoke tests when a GitLab test project and provider tools are available.
- Add negative tests proving no backlog, GitHub issue, or other fallback record is created on success or failure.
- Verify merge-request terminology and evidence independently from issue lifecycle.
- Run Agent Skill validation, metadata and generated-output checks, provider contract tests, full repository tests, project-wiki tests, and Git diff validation.

## Notes

- GitLab support is not implemented by translating GitHub commands or output labels.
- Live provider smoke tests require explicit project authority and may remain skipped with a documented capability blocker.
