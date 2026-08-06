---
name: manage-work-items-github
description: Inventory, select, claim, update, recover, block, complete, reopen, and report authoritative GitHub issues through observed provider state. Use when the effective work-item provider is github or an explicit one-item request selects GitHub issue management.
metadata:
  category: development-practice
---

# Manage GitHub Work Items

Manage GitHub issues as authoritative work items while keeping provider lifecycle separate from delivery completion.

## Work Item ID

- Accept the GitHub Work Item ID as one opaque input. This provider resolves it to the observed repository identity and issue number, checks collisions through GitHub, and reports the URL only as diagnostic location evidence.
- Preserve the same Work Item ID across open, closed, reopened, transferred, and terminal lifecycle states. Generic callers must not parse its repository or number components.

Acquire the exact opaque Work Item ID before any work or provider mutation. Use activity work for outcome work and activity update for provider mutation. Release the work-item claim with disposition done, blocked, or handoff at the activity boundary. Blocked may include a bounded blocker reference; when present, it must be canonical, non-empty, single-line, and at most 200 characters. A handoff release must complete before the next owner acquires the same ID. Path and resource claims remain independently applicable. The provider remains the lifecycle authority.

## Inputs And Authority

- Resolve the repository owner and name, issue number or selection criteria, requested operation, expected current state, owner, dependencies, lifecycle evidence, delivery references, and fields authorized to change.
- Use this skill when applicable project guidance selects provider github or an explicit one-item request selects GitHub. A task override does not silently change the project default.
- Require an authenticated GitHub provider interface with every read and mutation capability needed by the operation. Return BLOCKED when authentication, repository authority, a required capability, or mutation permission is unavailable.
- Re-read provider state before a transition. Do not rely on conversation state, cached search output, local files, or a branch name as issue authority.

## Inventory Work Items

1. Read the target repository through the provider and confirm its observed identity.
2. Search or list issues using the requested state, labels, assignees, milestone or project fields, relationships, and text criteria.
3. Read every candidate needed to make the selection. Report ambiguous matches rather than guessing.
4. Map provider-native state and fields to the configured lifecycle without confusing a native open or closed value with lifecycle completion evidence.

## Transition Work Item

- Claim or start one item by recording the configured assignee, labels, project fields, canonical task identifier, branch, worktree, phase, and start evidence. Verify the observed ownership and lifecycle RUNNING state.
- Update requirements, acceptance criteria, dependencies, relationships, recovery notes, waits, attempts, blockers, or delivery evidence only when the requested workflow authorizes those fields. Preserve unrelated issue content and metadata.
- Record BLOCKED, USER_ACTION_REQUIRED, HOLDING, AWAITING_REVIEW, FAILED, or ABANDONED with the exact evidence and next action required by the configured lifecycle.
- Record branch, commit, pull-request, review, check, merge, and main-observation references when available. Keep GitHub pull-request terminology and do not treat publication or AWAITING_REVIEW alone as issue completion.
- After every mutation, re-read the issue through the provider and compare every authorized changed field, including body content, labels, assignees, milestone or project fields, relationships, comments, native state, and mapped lifecycle state. Return BLOCKED with the observed mismatch when any required change is absent or contradictory.

## Reconcile Work Item Completion

- Close an issue as lifecycle COMPLETED only after the selected completion process returns completion disposition READY and the configured terminal evidence is observed.
- Re-read the closed issue and verify its state, configured fields, terminal history, delivery references, and mapped lifecycle COMPLETED.
- If the terminal provider update fails after completion disposition READY, preserve the accepted delivery evidence and reconcile only the missing GitHub update. Do not rerun valid delivery work.

## Recover Work Item

- Represent dependencies with repository-supported issue links, task lists, labels, project fields, or comments while preserving the referenced repository and issue numbers.
- Do not dispatch an item whose unmet dependencies make it ineligible. Report the blocking issue references and their observed states.
- Resume interrupted work from the provider record: ownership, canonical task id, accepted candidate commit, branch, pull request, review and check evidence, waits, attempts, blockers, open issues, and recovery note.
- Reopen only when explicit workflow authority permits it. Record why the prior terminal state no longer governs and verify the observed reopened state.
- Treat a timeout, disconnect, or ambiguous mutation response as possibly applied. Re-read the issue, comments, labels, assignments, relationships, and native state before retrying only the missing authorized change.
- If a partial mutation leaves a contradictory state, preserve the observed issue identity and history, return BLOCKED with the mismatch, and identify the smallest reconciliation action.

## Boundaries

- Do not create repository backlog files, cached issue mirrors, or fallback local queues on success, provider failure, authentication failure, permission denial, or partial mutation.
- Do not create a new issue; creation and duplicate detection belong to create-work-item-github.
- Do not infer provider github from a remote, installed tool, existing issue, template, or hosting account.
- Do not alter unrelated labels, assignees, milestones, project fields, relationships, issue text, or comments.
- Do not expose unsuitable evidence in an issue whose visibility is not appropriate.

## Report Work Items

Return Work Item ID, the observed repository, issue number and diagnostic URL, native state, lifecycle status, ownership, dependencies, relationships, delivery and terminal evidence, fields changed, verification readback, and next runnable action. Return BLOCKED with the failed provider boundary and observed remote state when management cannot finish safely.
