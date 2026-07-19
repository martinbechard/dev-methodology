# Add Feature-Branch Completion Skill

Status: Proposed

Type: Feature

## Summary

Add complete-work-item-feature-branch so implementation, provider-accurate pull or merge request publication, review, checks, merge, and final delivery evidence form one truthful completion process.

## Context

This item is a completion lane in the [Work-Item Provider And Completion Contracts series](index.md). The current feature-branch-workitem prototype correctly publishes completed work as ready for review, but AWAITING_REVIEW is a handoff state rather than backlog completion. The final contract must resume after review and verify merge evidence before the selected work-item provider is asked to close the item.

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
