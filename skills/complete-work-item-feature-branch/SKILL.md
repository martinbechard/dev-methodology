---
name: complete-work-item-feature-branch
description: Complete a normalized work item through one reviewable feature branch, provider-accurate pull-request or merge-request publication, accepted corrections, required checks, observed merge, and final provider lifecycle evidence. Use when the selected completion process is feature-branch or a request explicitly requires reviewed branch delivery through merge.
metadata:
  category: development-practice
---

# Complete Work Item Feature Branch

Carry one verified work item from branch creation through review publication and observed merge without confusing publication with completion.

## Dependencies

- Apply [agent-claim](../agent-claim/SKILL.md) for every repository mutation and shared resource.
- Apply [create-pull-request](../create-pull-request/SKILL.md) only for GitHub or another configured host whose contract accurately uses pull-request terminology.
- Use the configured GitLab merge-request capability and GitLab tools for GitLab publication, review, pipeline, and merge evidence. If no accurate capability exists, return BLOCKED instead of substituting create-pull-request or GitHub-shaped evidence.
- Send the final lifecycle update to the manager selected by the work-item provider. Do not mutate a provider record through an unselected provider capability.

## Inputs

Resolve these inputs before repository mutation:

- Normalized work-item identifier, provider, provider reference, title, requirements, acceptance criteria, dependencies, and verification expectations.
- Target repository, code host, remote, configured base branch, intended feature branch, and merge policy.
- Required review approvals, checks or pipelines, dependency merge order, and any user-requested draft state.
- Existing pull-request or merge-request identity when resuming publication or accepted corrections.
- Authority to create the branch, push it, publish or update the delivery record, and perform any requested merge action.

The work-item provider and code host are independent. A file or GitLab work item may be delivered through GitHub, and a file or GitHub work item may be delivered through GitLab, when project configuration explicitly selects that host. Do not infer either selection from remotes, templates, available tools, or existing records.

## Branch And Ownership

1. Inspect the configured base, work-item scope, dependency branches, existing publication, commits, worktree state, and remote state.
2. Acquire the narrow repository ownership and shared resources required for the current mutation phase. Preserve unrelated work and stop on overlapping ownership.
3. Create the intended feature branch from the assigned base before changing source files. When claim isolation creates the delivery branch, use that same branch instead of adding a parallel coordination branch.
4. Keep accepted review corrections on the same work item, feature branch, and publication record. A correction that changes the independent work-item boundary returns to the coordinator before scope expands.
5. Release ownership only after the phase is committed, verified, clean, and safely published or preserved. Reacquire the required scope when a later review cycle resumes mutation.

## Implementation And Publication

1. Implement the smallest complete work-item scope and focused regression coverage.
2. Run the checks required by the changed behavior and risk. Create coherent verified commits and confirm the worktree is clean.
3. Push only the intended feature branch and verify that the remote head resolves to the reviewed commit.
4. Publish or update one provider-accurate delivery record:
   - For GitHub, use create-pull-request and GitHub evidence. Call it a pull request.
   - For GitLab, use the configured merge-request capability and GitLab evidence. Call it a merge request.
   - For another host, use only a configured capability whose terminology, readiness, review, checks, and merge evidence are explicit.
5. Publish completed, verified work ready for review. Use draft only when the user requests it or concrete implementation, verification, or dependency work remains incomplete.
6. Record and verify the publication URL, code host, base, head, commit, dependencies, review order, required checks, and observed ready or draft state.

Successful publication returns AWAITING_REVIEW while any required approval, check, dependency merge, or configured merge remains outstanding. A ready publication is not READY delivery evidence.

## Review And Check Loop

1. Retrieve the existing pull request or merge request by its durable publication identity.
2. Classify review findings and apply accepted corrections on the same branch.
3. Rerun every check affected by the correction, commit coherently, push, and verify the existing publication now points to the corrected head.
4. Observe required approvals, checks or pipelines, and dependency order from the configured code host. Do not translate GitLab pipelines into GitHub checks or GitHub review evidence into GitLab approval evidence.
5. Preserve AWAITING_REVIEW while valid review or merge work is merely pending. Return BLOCKED only when a concrete failure, missing authority, unavailable capability, rejected check, ownership conflict, or unsatisfied dependency prevents safe progress.

## Merge And Completion Gate

Return READY only after all of the following are observed:

- Every required approval is accepted and current for the published head.
- Every required check or pipeline passes for the commit being merged.
- Dependencies merged in the configured order.
- The pull request or merge request reports a merged state rather than merely closed, approved, ready, or superseded.
- The recorded merge commit and resulting verified commit are reachable from the configured base branch in Git.
- Provider lifecycle completion evidence is prepared for the selected work-item manager.

A closed-unmerged, abandoned, replaced, or superseded publication cannot return READY. Follow an explicit replacement only after its relationship to the same work item and branch history is verified; otherwise return BLOCKED with both references.

After the merge gate passes, send the selected provider manager the work-item reference, completion disposition READY, branch and publication reference, final merged base commit, approvals, checks, dependencies, merge evidence, claim releases, and requested terminal lifecycle update. The provider-backed item remains nonterminal until that manager records lifecycle COMPLETED. When the selected provider is none, record the complete task-local terminal evidence and lifecycle COMPLETED before returning READY.

## Results

Return exactly one disposition with deciding evidence:

- AWAITING_REVIEW: branch, pushed commit, pull-request or merge-request URL, base and head, ready or draft state, review and dependency order, completed checks, and every outstanding review, check, dependency, or merge gate.
- READY: all publication evidence plus required approvals and checks, merged state, final merge commit, configured base-branch reachability, released ownership, and the provider lifecycle update this evidence authorizes.
- BLOCKED: preserved branch, commits, publication URL when one exists, provider-accurate state, released or retained ownership state, exact missing evidence or authority, and the next safe action.

Never report READY from branch publication alone, and never report provider lifecycle COMPLETED before the selected provider manager, or the provider-none task result, records the terminal update.
