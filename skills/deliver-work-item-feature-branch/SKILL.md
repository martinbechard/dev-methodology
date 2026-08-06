---
name: deliver-work-item-feature-branch
description: Complete a normalized work item through one reviewable feature branch, provider-accurate pull-request or merge-request publication, accepted corrections, required checks, observed merge, and final provider lifecycle evidence. Use when the selected completion process is feature-branch or a request explicitly requires reviewed branch delivery through merge.
metadata:
  category: development-practice
---

# Deliver Work Item Feature Branch

Carry one accepted candidate from branch publication through host review and observed merge without confusing publication with implementation or completion.

## Deliver Work Item

Deliver the accepted work item through candidate publication, the review and check loop, and the observed merge and completion gate defined below.

## Interface Conformance

This Provider Skill realizes the deliver-work-item interface. It consumes the accepted commit without modifying it, preserves one delivery identity through publication, correction, review, and merge, and returns READY, AWAITING_REVIEW, or BLOCKED with state-keyed evidence and the prepared Persistence handoff. It does not select the Commit provider and does not mutate Persistence or dispatch a provider manager.

## Dependencies

- Follow the Claim Events table in agent-claim during publication.
- Apply [create-pull-request](../create-pull-request/SKILL.md) only for GitHub or another configured host whose contract accurately uses pull-request terminology.
- Use the configured GitLab merge-request capability and GitLab tools for GitLab publication, review, pipeline, and merge evidence. If no accurate capability exists, return BLOCKED instead of substituting create-pull-request or GitHub-shaped evidence.
- Prepare the final lifecycle update for the caller. This skill must not dispatch a provider manager, Dev Backlog Steward, or any Persistence mutation.

## Inputs

Resolve these inputs before repository mutation:

- Opaque Work Item ID, provider selector, title, requirements, acceptance criteria, dependencies, and verification expectations.
- Target repository, code host, remote, configured base branch, intended feature branch, and merge policy.
- Accepted candidate commit plus fresh independent review, verification, changed-path, and clean-worktree evidence.
- Required review approvals, checks or pipelines, dependency merge order, and any user-requested draft state.
- Existing pull-request or merge-request identity when resuming publication after a source correction.
- Authority to create the branch, push it, publish or update the delivery record, and perform any requested merge action.

The work-item provider and code host are independent. A file or GitLab work item may be delivered through GitHub, and a file or GitHub work item may be delivered through GitLab, when applicable project configuration or explicit task-level user direction selects that host. Do not infer either selection from remotes, templates, available tools, or existing records.

Consume an already accepted, independently reviewed and verified candidate commit. This skill must not modify source files or implement review corrections.

## Branch And Ownership

1. Inspect the configured base, work-item scope, dependency branches, existing publication, commits, worktree state, and remote state.
2. Create or reuse the intended feature branch for the accepted candidate.
3. Preserve the same work item, feature branch, publication record, and delivery identity across correction cycles.
4. Return a correction that changes the work-item boundary to the coordinator before expanding scope.

## Candidate Publication

1. Verify that the supplied candidate commit matches the accepted independent review and verification evidence and that its source worktree is clean.
2. Point the intended feature branch at that accepted candidate without editing its source content.
3. Push only the intended feature branch and verify that the remote head resolves to the accepted candidate.
4. Publish or update one provider-accurate delivery record:
   - For GitHub, use create-pull-request and GitHub evidence. Call it a pull request.
   - For GitLab, use the configured merge-request capability and GitLab evidence. Call it a merge request.
   - For another host, use only a configured capability whose terminology, readiness, review, checks, and merge evidence are explicit.
5. Publish accepted work ready for host review. Use draft only when the user requests it or a concrete publication, host-check, or dependency gate remains incomplete.
6. Record and verify the opaque Work Item ID and provider selector without parsing the ID, plus publication URL, code host, base, head, commit, dependencies, review order, required checks, and observed ready or draft state.

Successful publication returns AWAITING_REVIEW while any required approval, check, dependency merge, or configured merge remains outstanding. A ready publication is not READY delivery evidence. AWAITING_REVIEW performs no Persistence mutation.

## Review And Check Loop

1. Retrieve the existing pull request or merge request by its durable publication identity.
2. Classify host findings and identify every accepted request that requires a source correction.
3. Return every source correction request to the caller for Dev Orchestrator to route to the original Dev Coder.
4. Preserve the existing branch and publication identity while Dev Coder produces a replacement candidate and Dev Orchestrator repeats fresh independent review and verification.
5. Resume the same branch, publication, and delivery identity only after the replacement candidate passes fresh independent review and verification.
6. Push the accepted replacement candidate and verify the existing publication now points to it without authoring or amending its source changes.
7. Observe required approvals, checks or pipelines, and dependency order from the configured code host. Do not translate GitLab pipelines into GitHub checks or GitHub review evidence into GitLab approval evidence.
8. Preserve AWAITING_REVIEW while valid review or merge work is merely pending. Return BLOCKED only when a concrete failure, missing authority, unavailable capability, rejected check, ownership conflict, or unsatisfied dependency prevents safe progress.

## Host State Decision Table

Apply these outcomes to provider-accurate host evidence. Do not convert a pending gate into success or a concrete failure into an indefinite review wait.

| Scenario | Required observed evidence | Disposition |
| --- | --- | --- |
| Ready publication | Ready pull request or merge request; review or merge remains pending | AWAITING_REVIEW |
| Explicit draft | User-requested draft, or named incomplete implementation, check, or dependency work | AWAITING_REVIEW |
| Review correction | Existing publication points to the independently re-reviewed and re-verified replacement candidate on the same branch; affected host checks reran | AWAITING_REVIEW |
| Checks pending | Required checks or pipelines have not completed for the current head | AWAITING_REVIEW |
| Check failure | A required check or pipeline failed for the current head | BLOCKED |
| Approval pending | Required current-head approval has not arrived | AWAITING_REVIEW |
| Dependency pending | Required dependency has not merged in the configured order | AWAITING_REVIEW |
| Merge pending | Host remains open even when other merge evidence is present | AWAITING_REVIEW |
| Merge complete | Required approvals and checks passed; dependencies merged; host reports merged; final merged commit is reachable from the configured base | READY |
| Merge evidence mismatch | Host reports merged but the resulting verified commit is not reachable from the configured base | BLOCKED |
| Closed unmerged | Host reports closed without merge evidence | BLOCKED |
| Superseded | Publication was replaced without a verified same-work-item relationship and preserved branch history | BLOCKED |
| Missing authority | Required branch, push, publication, update, or requested merge authority is absent | BLOCKED |
| Terminology mismatch | GitHub evidence is shaped as a merge request or GitLab evidence is shaped as a pull request | BLOCKED |

## Merge And Completion Gate

Return READY only after all of the following are observed:

- Every required approval is accepted and current for the published head.
- Every required check or pipeline passes for the commit being merged.
- Dependencies merged in the configured order.
- The pull request or merge request reports a merged state rather than merely closed, approved, ready, or superseded.
- The recorded merge commit and resulting verified commit are reachable from the configured base branch in Git.
- Provider lifecycle completion evidence is prepared for the caller.

For a merge strategy that preserves the published head, verify both the published commit and final merge commit with the project-supported equivalent of these read-only ancestry checks:

```bash
git merge-base --is-ancestor PUBLISHED_HEAD CONFIGURED_BASE
git merge-base --is-ancestor FINAL_MERGED_COMMIT CONFIGURED_BASE
```

When the configured strategy rebases or squashes, record the provider-observed mapping from the published head to the resulting verified commit, then apply the final-commit ancestry check. Never treat the missing published-head ancestry expected from that configured strategy as silent success.

A closed-unmerged, abandoned, replaced, or superseded publication cannot return READY. Follow an explicit replacement only after its relationship to the same work item and branch history is verified; otherwise return BLOCKED with both references.

After the merge gate passes, prepare the work-item reference, completion disposition READY, branch and publication reference, final merged base commit, approvals, checks, dependencies, merge evidence, applicable claim results, and requested terminal lifecycle update. Return the prepared terminal handoff to the caller; the owning orchestrator decides whether and when to dispatch the selected provider manager. This skill neither performs that dispatch nor waits for its result. The provider-backed item remains nonterminal until the separate Persistence phase records lifecycle COMPLETED. When the selected provider is none, record lifecycle COMPLETED in the task-local result before returning READY, together with the complete terminal evidence.

A provider-backed Persistence recording failure happens after this skill returns. It does not change Commit READY into BLOCKED or erase the delivery evidence; the owning orchestrator reports and reconciles the Persistence failure separately.

## Results

Return exactly one disposition with deciding evidence:

- AWAITING_REVIEW: Work Item ID and provider selector, branch, pushed commit, pull-request or merge-request URL, base and head, ready or draft state, review and dependency order, completed checks, and every outstanding review, check, dependency, or merge gate.
- READY: all publication evidence plus required approvals and checks, merged state, final merge commit, configured base-branch reachability, applicable claim results, and the provider lifecycle update this evidence authorizes.
- BLOCKED: preserved branch, commits, publication URL when one exists, provider-accurate state, applicable claim results, exact missing evidence or authority, and the next safe action.

Never report READY from branch publication alone. The owning orchestrator may later select a provider manager for Persistence; only that manager or the provider-none task result records lifecycle COMPLETED. This skill does not dispatch the manager.
