# Transform File Work-Item Skills

Status: Proposed

Type: Feature

## Summary

Replace the generic create-backlog and manage-backlog names with symmetric file-provider skills, absorb the redundant file-based-backlog wrapper, and preserve backlog on main as the only authoritative file-backed queue.

## Context

This item is a provider lane in the [Work-Item Provider And Completion Contracts series](index.md). The current create-backlog and manage-backlog skills contain the mature typed-item and lifecycle procedures. The newer file-based-backlog skill mostly selects those procedures. The transformation should preserve the mature behavior under provider-specific names rather than layer another wrapper around it.

## Requirements

- Create the canonical create-file-work-item and manage-file-work-items skill packages from the existing create-backlog and manage-backlog contracts.
- Keep each skill's frontmatter name, directory name, Codex metadata, descriptions, examples, and evaluation identifiers aligned.
- Preserve typed item placement, related-series indexes, unique slugs, user-action boundaries, lifecycle transitions, recovery evidence, archive behavior, and dispatchability rules.
- Make backlog under the primary main worktree the only authoritative file-provider storage root.
- Prohibit file-backed work-item creation or lifecycle mutation from isolated worktrees and non-main authorities.
- Use agent-claim's backlog scope for each file mutation and preserve PRIMARY_REQUIRED behavior when the primary worktree is unavailable.
- Keep implementation claims separate from short backlog transition claims.
- Require durable source, dependency, ownership, delivery, verification, completion, blocked, and archival evidence appropriate to each transition.
- Absorb the provider-selection content of file-based-backlog into the two canonical skills.
- Retire file-based-backlog after all source and generated references move to the canonical create and manage identifiers.
- Provide migration guidance for repositories and PROJECT.yaml files that still name create-backlog, manage-backlog, or file-based-backlog.
- Do not create provider issues or mirror file items into GitHub, GitLab, Azure DevOps, or Jira.

## Acceptance Criteria

- New file-backed work-item creation routes through create-file-work-item.
- Existing file-backed item state changes route through manage-file-work-items.
- Every file-backed item remains under backlog on the primary main worktree.
- An isolated or non-primary mutation request blocks without writing a shadow queue.
- The transformed skills preserve the complete existing typed-item, series, user-action, recovery, and archive contracts.
- file-based-backlog has no remaining independent behavior and can be removed without losing a procedure.
- Migration guidance maps every retired identifier to one canonical replacement.
- Provider-backed projects never load the file skills unless the file provider is selected or explicitly requested for one item.

## Dependencies

define-provider-and-completion-selector-contracts.

## Verification

- Add focused tests for file creation, duplicate detection, series placement, claim acquisition, lifecycle transitions, recovery, completion, failure, archive, and invalid primary-worktree state.
- Add negative tests proving isolated worktrees and provider-backed projects do not create backlog files.
- Compare transformed skill behavior with the complete create-backlog and manage-backlog regression inventory.
- Sweep source, metadata, generated output, templates, evals, and documentation for stale file-based-backlog and ambiguous backlog identifiers.
- Run Agent Skill validation, metadata alignment, generated-output checks, focused backlog tests, full repository tests, project-wiki tests, and Git diff validation.

## Notes

- This is a behavior-preserving provider qualification, not a new backlog taxonomy.
- Cross-bundle role and documentation migration is finalized by integrate-work-item-contracts-across-bundle.
