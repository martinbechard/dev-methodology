# Feature-Branch Work-Item Process

Use this process when the requested handoff is a remotely reviewable feature branch and pull request.

## Workflow

1. Resolve the normalized work item, target repository, integration base, dependencies, and acceptance criteria.
2. Acquire ownership before creating or switching branches.
3. Create the feature branch from the assigned base before implementation. When claim isolation requires a worktree, use one branch for both the owned worktree and remote feature delivery rather than creating parallel coordination and delivery branches.
4. Implement the smallest complete change and regression coverage.
5. Run the checks required by the changed behavior and risk.
6. Commit the completed contribution and confirm the worktree is clean.
7. Push the feature branch, then apply create-pull-request to publish the pull request with the repository template and correct dependency order.
8. Set the pull request ready for review when the scoped implementation and required checks are complete. Use draft status only when requested or when known implementation, verification, or dependency work remains incomplete.
9. Verify the published base, head, title, body, readiness, checks, and links from the hosting service.
10. Release the claim and report AWAITING_REVIEW with the work-item, branch, commit, pull-request, and verification references.
11. When review comments arrive, resume the same work item and branch, classify the comments, apply accepted corrections, rerun affected checks, commit, push, and verify the updated pull request.

## Review Loop

- Do not keep an agent process alive indefinitely while waiting for human review. Leave a resumable AWAITING_REVIEW handoff unless the request explicitly authorizes monitoring.
- Do not create a replacement pull request for ordinary corrections.
- Keep completed pull requests ready for review after corrections. Do not return them to draft merely because another review pass is pending.
- Route a correction that changes the independent work-item boundary back to the coordinator before expanding the branch.
- Do not merge the pull request unless the request separately authorizes merging.

## Completion

Use AWAITING_REVIEW after verified publication. Report READY only when the workflow's requested review outcome is complete. Report BLOCKED when branch publication, required checks, review authority, or correction ownership prevents safe continuation.
