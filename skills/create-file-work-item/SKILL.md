---
name: create-file-work-item
description: Create one authoritative repository-backed work item with typed placement, source evidence, user-action boundaries, and a short primary-main backlog claim. Use when the effective provider is file or the user explicitly requests one file-backed item.
metadata:
  category: development-practice
---

# Create File Work Item

## Purpose

Create one durable file-provider work item that is clear, typed, and safe to manage later. Ordinary active items must be dispatchable without the original conversation. User-action-required items must preserve the exact decision or information only the user can provide and must remain separate from unattended work.

## Provider Selection

- Apply this skill only when the effective provider is file or applicable project guidance permits an explicit request to select file for this one item.
- When durable provider work is required and the provider is UNSET, ask the user to select a provider before mutation.
- When the effective provider is none or another provider, return the provider mismatch without creating a file or falling back to file storage.
- Do not create or update GitHub, GitLab, Azure DevOps, or Jira records and do not mirror their items under backlog.

## File Authority

The only authoritative file-provider storage root is backlog in the primary worktree while that worktree is on main. The repository-relative backlog path is both work_item_id and provider_reference. A filename slug is only a display shorthand when it is unambiguous.

An isolated worktree, a linked worktree other than the primary worktree, or a primary worktree not on main has no authority to create the item. Return BLOCKED with the observed worktree and branch, the required primary-main authority, and the next handoff. Do not write a shadow queue elsewhere.

Before each creation mutation, acquire agent-claim backlog scope from the primary main worktree. PRIMARY_REQUIRED is a coordination outcome: arrange a direct handoff or completion notification and suspend without polling. After notification, reconcile live status before retrying. Commit the one queue mutation and release the short backlog-domain claim immediately.

After that commit, release that claim immediately.

Do not combine backlog creation with a project-files implementation claim. When creation immediately authorizes delivery, record the READY item first, release the backlog claim, and then acquire a separate exact, tree, or project-files implementation claim. A later backlog claim records terminal evidence and archive movement.

## Folder Model

Place new work items by work type:

- Defects go in backlog/defect-backlog.
- Features go in backlog/feature-backlog.
- Analyses go in backlog/analysis-backlog.
- Investigations go in backlog/investigation-backlog.
- Items whose next safe step requires a user decision, approval, authority grant, value judgment, or user-held information go in backlog/user-action-required.
- Items that should remain visible but not automatically worked go in backlog/holding.
- Do not create items directly in completed or failed archive folders.

If a repository has a documented taxonomy or placement rule, follow it before creating files within the authoritative backlog root. If the expected backlog folder does not exist, create the most specific standard folder that matches the item type unless project guidance says otherwise.

User Action Required is a queue state, not a work type. Preserve the underlying Type as Defect, Feature, Analysis, or Investigation so an answered item has a deterministic active destination. Use Status: User Action Required while the item remains in backlog/user-action-required.

backlog/holding and backlog/user-action-required are different. Holding contains work intentionally deferred without an immediate question. User Action Required contains work that cannot safely advance until the user answers a concrete question.

## Related Item Series

When one goal naturally contains multiple related work items, create a subfolder under the appropriate typed backlog folder instead of placing every item flat in the parent folder. The subfolder name should be the stable goal slug.

Create an index.md file inside the subfolder. The index describes the overall goal, purpose, current data or design anchors, non-goals, definition of good, and recommended implementation order. The index is a coordination artifact, not a runnable work item.

Create the smaller work items as separate Markdown files in the same subfolder. Each child item must remain independently dispatchable and link back to index.md. The index must link to every child item and group them by sequence or theme.

Use a series folder when:

- The work has one goal but multiple ordered phases.
- Different child items can be implemented, analyzed, or verified independently.
- The index can preserve context that would otherwise be duplicated across child items.
- A later agent needs to understand the whole goal before choosing the next item.

Avoid a series folder when a single work item can clearly express the work and all acceptance criteria.

## Item Classification

Classify by the outcome the work must produce:

- Defect: broken or regressed behavior must be corrected.
- Feature: new or expanded behavior must be delivered.
- Analysis: a question must be answered with evidence, options, or recommendations.
- Investigation: an unclear failure, risk, or system behavior must be traced until the next action is known.
- Holding: the item is real but intentionally not ready for dispatch.

When a request mixes types, split it only when the parts can be completed independently. Keep a single item when one coherent delivery outcome depends on all parts.

## User Action Required Classification

Place an independently identified potentially valuable idea in backlog/user-action-required when the user has not requested or authorized the work. Preserve its underlying Type, set Status: User Action Required, and ask one concrete approval question before unattended work can continue.

Also use User Action Required when all of these are true:

- The next safe action depends on a decision, approval, authority grant, value judgment, or information that belongs to the user.
- The item can state one concrete question whose answer changes what happens next.
- Proceeding without that answer would invent authority, product intent, risk acceptance, ownership, or source truth.

Do not place an item in backlog/user-action-required merely because the task is difficult, an ordinary dependency is unavailable, an agent lacks a tool, implementation failed, or more technical investigation is possible. Keep agent-actionable work in its typed active backlog and record ordinary dependencies there.

Do not turn a synthetic evaluation boundary into user-action-required work unless it represents a genuine unresolved project decision. A scenario designed to prove safe blocking is test evidence, not automatically a user obligation.

A direct user request or explicit user authorization is sufficient authority to create an item in its typed active backlog with Status: Ready. Keep it there when ordinary evidence-backed dependencies remain. Route it to backlog/user-action-required only when a separate genuine user-owned question still prevents safe unattended work, or to backlog/holding when the user explicitly defers it.

## Filename And Duplicate Detection

Use a stable, lowercase, hyphen-separated filename ending in .md. Derive the slug from the filename stem. Prefer names that describe the durable work, not a temporary symptom, date, owner, status, or vague cleanup label.

Before writing, search every active typed folder, backlog/user-action-required, and backlog/holding for the same canonical path, slug, source reference, or overlapping outcome. Update an existing active item only when the new request is clearly the same work. Create a new item only when it has a distinct outcome or can be completed independently. Never use a second provider or a different repository path to bypass a duplicate.

## Required Item Shape

Write each item as a self-contained work package with these fields and sections:

- Title: one clear heading naming the work.
- Status: Ready for authorized active work, User Action Required for a user-owned answer, or Holding for explicit deferral.
- Type: Defect, Feature, Analysis, Investigation, or Holding.
- Provider: file.
- Provider Reference: the canonical repository-relative backlog path.
- Completion: the selected completion process when known, or UNSET.
- Summary: the desired outcome.
- Context: facts, current behavior, user impact, constraints, and source references.
- Source Evidence: the request, finding, or decision that authorizes creation.
- Requirements: concrete behavior or deliverables.
- Acceptance Criteria: observable completion conditions.
- Dependencies: canonical provider references or None.
- Verification: expected tests, builds, checks, review, or artifacts.
- Notes: optional edge cases, examples, non-goals, and open questions.

For an item in backlog/user-action-required, also include:

- User Action Required.
- Question for the User.
- Why User Input Is Required.
- Options and Tradeoffs when choices are known.
- Resolution, initially Pending.
- Unattended Work Boundary.

The creation commit and result must preserve work_item_id, provider_reference, source evidence, provider selection, completion selection, creation authority, creation time when the repository records it, and the released backlog claim reference. Keep Requirements, Acceptance Criteria, Dependencies, and Verification so the item remains complete after it moves into an active typed backlog.

## Writing Rules

- Include exact paths, screens, procedures, examples, or data only when current evidence supports them.
- Mark unknown facts as questions or assumptions instead of inventing them.
- Keep requirements testable and separate them from acceptance criteria.
- Use provider-accurate dependency references so blocked work can be detected mechanically.
- Phrase user questions neutrally and expose viable tradeoffs.
- Keep completed or failed outcomes out of newly created active items.
- Use imperative, steady-state language.

## Final Check And Result

Before reporting completion:

- Confirm the effective provider is file and the mutation occurred only under backlog in the primary main worktree.
- Confirm the backlog claim was short, committed, released, and separate from implementation ownership.
- Confirm the item is in the right typed folder and has a stable unique path.
- Confirm related multi-item goals have an index.md and linked independently runnable children.
- Confirm the complete required item shape, source evidence, dependencies, and verification expectations are present.
- Confirm user-action-required content has the complete question and unattended boundary.
- Confirm no provider issue, mirror, shadow queue, or duplicate file was created.

Return provider file, work_item_id and provider_reference, item type, lifecycle status, source evidence, dependencies, completion selection, creation commit, released claim reference, and next runnable action.

## Migration

create-file-work-item owns all file-provider creation behavior formerly split between create-backlog and file-based-backlog. Update PROJECT.yaml and generated guidance to select provider file and load create-file-work-item for creation. The legacy identifiers are migration-only shells until their separately governed callers move; they must not receive new procedure changes.
