# Split GitHub Work-Item Skills

Status: Proposed

Type: Feature

## Summary

Replace github-issues-backlog with symmetric create-github-work-item and manage-github-work-items skills that use GitHub provider tools as the sole authority and never create shadow backlog files.

## Context

This item is a provider lane in the [Work-Item Provider And Completion Contracts series](index.md). The current github-issues-backlog prototype combines creation and lifecycle management in one skill. Separating those responsibilities makes GitHub symmetric with other providers while keeping issue lifecycle distinct from pull-request delivery.

## Requirements

- Create create-github-work-item for duplicate search, issue creation, typed content, labels, relationships, acceptance criteria, and initial ownership evidence.
- Create manage-github-work-items for lookup, claim or assignment, lifecycle updates, dependencies, delivery references, blocking, completion, reopening, and reporting.
- Use the authenticated GitHub provider tools for every read and mutation that establishes issue authority.
- Verify the observed repository, issue number, URL, state, labels, assignees, relationships, and updated content after mutation.
- Preserve GitHub issue terminology and do not describe an issue as a pull request or merge request.
- Prohibit repository backlog files, cached issue mirrors, or fallback local queues when GitHub is selected.
- Return BLOCKED when authentication, repository authority, required provider capability, or mutation permission is unavailable.
- Keep issue completion independent from direct-main or feature-branch delivery completion and preserve configured lifecycle rules.
- Record branch, pull-request, commit, review, check, and merge references when available without treating publication alone as issue completion.
- Support one-item explicit GitHub requests without silently changing the project default.
- Retire github-issues-backlog after all procedures and references move to the canonical pair.
- Provide migration guidance for existing PROJECT.yaml and AGENTS.md references.

## Acceptance Criteria

- Creation and management route to distinct symmetric GitHub skills.
- Both skills use provider evidence and return the observed issue identity and state.
- Duplicate detection prevents a second issue for the same durable work.
- A missing provider tool or permission blocks without writing under backlog.
- Pull-request creation or an AWAITING_REVIEW delivery state does not automatically close the issue.
- Configured completion evidence can close the issue and is visible in its durable history.
- github-issues-backlog can be removed without losing behavior.
- No active GitHub provider path creates or instructs creation of a shadow file item.

## Dependencies

define-provider-and-completion-selector-contracts.

## Verification

- Add mocked provider tests for search, create, duplicate, update, dependency, block, reopen, close, permission denial, authentication failure, and partial mutation.
- Add authorized disposable-repository smoke tests for create and manage operations without using production work items.
- Add negative tests proving no backlog file is created on success or provider failure.
- Verify issue states remain independent from direct-main and feature-branch completion states.
- Run Agent Skill validation, metadata and generated-output checks, provider contract tests, full repository tests, project-wiki tests, and Git diff validation.

## Notes

- create-pull-request remains a subordinate delivery capability, not a GitHub work-item provider skill.
- Provider mutation smoke tests require explicit repository authority.
