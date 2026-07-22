# Simple Work-Item Process

Use this process for interactive local development where the requested handoff is a verified local commit rather than a remote pull request.

## Resource Coordination

- When agent-claim is selected, acquire the narrow required claim before mutation, follow any returned primary or isolated worktree decision, heartbeat or hand off ownership when required, and release the same claim from a clean worktree with its evidence.
- When none is selected, do not discover or load a coordination implementation or transport, inspect coordination state, acquire or heartbeat ownership, create a coordination branch, hand off or release a claim, or report coordination evidence. Perform no coordination operations or evidence collection; use the authorized delivery worktree and preserve the same clean commit and verification gates.

## Workflow

1. Resolve the normalized work item and its acceptance criteria.
2. Apply the applicable resource-coordination branch above before mutation.
3. Use the worktree selected by the authorized delivery context. Under agent-claim, use the primary or isolated worktree and local coordination branch returned by that implementation.
4. Implement the smallest complete change and regression coverage.
5. Run the checks required by the changed behavior and risk.
6. Commit the completed change locally.
7. Confirm the delivery worktree is clean. Under agent-claim, release the acquired claim and retain its evidence; under none, perform no release operation or evidence collection.
8. Report the commit, changed scope, verification, omissions, and required backlog lifecycle update interactively.

## Boundaries

- Do not push a branch or create a pull request.
- Do not treat an isolation branch as a feature branch. It exists only to keep concurrent local work separate.
- When isolation leaves the commit outside the requester's current branch, report the branch, worktree, and commit needed for later integration.
- Do not archive or close the source work item directly unless the configured backlog owner assigned that responsibility.

## Completion

Report READY only when the requested change and tests are committed, applicable checks passed or omissions are explicit, and the worktree is clean. When agent-claim is selected, also require released-claim evidence. When none is selected, require no coordination operations or evidence.
