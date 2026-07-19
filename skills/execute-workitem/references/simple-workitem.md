# Simple Work-Item Process

Use this process for interactive local development where the requested handoff is a verified local commit rather than a remote pull request.

## Workflow

1. Resolve the normalized work item and its acceptance criteria.
2. Acquire the narrow required claim.
3. Use the primary worktree when claim coordination permits it. Use the isolated worktree and local coordination branch returned by claim coordination when concurrent work requires isolation.
4. Implement the smallest complete change and regression coverage.
5. Run the checks required by the changed behavior and risk.
6. Commit the completed change locally.
7. Confirm the owned worktree is clean and release the claim.
8. Report the commit, changed scope, verification, omissions, and required backlog lifecycle update interactively.

## Boundaries

- Do not push a branch or create a pull request.
- Do not treat an isolation branch as a feature branch. It exists only to keep concurrent local work separate.
- When isolation leaves the commit outside the requester's current branch, report the branch, worktree, and commit needed for later integration.
- Do not archive or close the source work item directly unless the configured backlog owner assigned that responsibility.

## Completion

Report READY only when the requested change and tests are committed, applicable checks passed or omissions are explicit, the worktree is clean, and the claim is released.
