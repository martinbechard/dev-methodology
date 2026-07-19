# Add GitLab Work-Item Skills

Status: Proposed

Type: Feature

## Summary

Add symmetric create-gitlab-work-item and manage-gitlab-work-items skills that use GitLab provider tools as the sole issue authority and preserve GitLab merge-request terminology and lifecycle behavior.

## Context

This item is a provider lane in the [Work-Item Provider And Completion Contracts series](index.md). GitLab must be a first-class provider rather than a GitHub-shaped alias. Its issue references, labels, milestones, relationships, merge requests, approvals, pipelines, and merge evidence must be expressed through GitLab capabilities and terminology.

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
