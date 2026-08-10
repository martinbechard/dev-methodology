---
name: create-work-item-file
description: Create one authoritative repository-backed work item with typed placement, source evidence, user-action boundaries, and atomic no-overwrite creation when the effective provider is file.
metadata:
  category: development-practice
---

# Create Work Item File

## Create Work Item

Create one durable file-provider work item that is clear, typed, and safe to manage later.
Ordinary active items must be dispatchable without the original conversation. User-action-required
items must preserve the exact decision or information only the user can provide and must remain
separate from unattended work.

## Provider Selection

- Apply this skill only when the effective provider is file or applicable project guidance permits an explicit request to select file for this one item.
- When durable provider work is required and the provider is UNSET, ask the user to select a provider before mutation.
- When the effective provider is none or another provider, return the provider mismatch without creating a file or falling back to file storage.
- Do not create or update GitHub, GitLab, Azure DevOps, or Jira records and do not mirror their items under backlog.

## File Authority

Only the primary worktree on main may create canonical files under backlog. The file provider's Work Item ID is the immutable lowercase filename stem. It is unique across active, non-dispatchable, completed, and failed work-item folders. The current repository-relative path is provider-owned storage and diagnostic evidence, not generic identity.

Another worktree may inspect backlog but must not create the item. If the primary worktree is not on main, it must not create the item. Return BLOCKED with the observed worktree, branch, and required handoff. Do not create another queue elsewhere.

Keep backlog creation separate from implementation ownership. Record and commit the complete
canonical lifecycle first: Ready when no hard prerequisite remains, or Blocked when the
authorized item is waiting for one.

## File Provider Transaction

After validating the complete ordinary work item, use commit-file-provider-transaction with
operation ordinary-creation, the one exact absent destination path, the validated bytes, and
the Work Item ID. That skill is the sole source for no-overwrite creation, resource coordination,
exact Git scope, rollback, immutable proof, and unrelated-state preservation.

Return BLOCKED when the shared transaction reports a collision, unsafe rollback, proof mismatch,
or incomplete recovery. Do not duplicate or weaken its transaction rules in this skill.

## Future Ideas Boundary

Future Ideas are not work items. This skill does not capture, inventory, validate, or promote
them. Route an explicit Future Ideas, ideation, or promotion request to manage-future-ideas.
Ordinary creation excludes backlog/future-ideas from lifecycle processing and duplicate scans.

## Template Workflow

Start each item from [file-work-item-template.md](../route-documentation-work/assets/templates/file-work-item-template.md). Replace every TODO instruction with source-backed content. Remove every guidance comment before commit. Remove an optional Series, User Action Required, or Notes section when it does not apply; do not leave empty headings or placeholder boilerplate.

- Before assigning Ready, resolve every declared hard dependency by immutable Work Item ID
  across the active and terminal provider folders. Ready items have no unmet hard
  prerequisite and remain dispatchable while Open Questions contain only agent-resolvable
  technical uncertainty.
- When authorized work has an unmet hard dependency, create it in its typed active folder
  with Status: Blocked and Owner: Unowned. Record the dependency, the exact evidence that
  will satisfy it, the blocker owner, and the observable Blocked -> Ready condition. Do not
  create Ready and rely on a downstream dispatcher or report to reinterpret it.
- User Action Required items keep the complete user question, reason, resolution, and unattended-work boundary in the item body.
- Holding items keep Status: Holding and record the deferral authority and resumption condition without inventing a user question.
- Related series children keep the optional Series field with the canonical repository-relative index.md path; standalone items remove it.

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

backlog/holding and backlog/user-action-required are different. Holding contains recognized work
that is intentionally deferred without an immediate question. User Action Required contains
recognized work that cannot safely advance until the user answers one concrete question.

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

Before creating a User Action Required item, when resource-claim is loaded, apply resource-claim to the blocking condition and confirm that a separate genuine user-owned decision remains. Structured claim outcomes and technical claim cleanup or recovery remain agent-owned and do not justify User Action Required.

Do not use User Action Required merely to preserve an independently identified possibility.
Report that possibility ephemerally unless an explicit Future Ideas request routes it to
manage-future-ideas.

Also use User Action Required when all of these are true:

- The next safe action depends on a decision, approval, authority grant, value judgment, or information that belongs to the user.
- The item can state one concrete question whose answer changes what happens next.
- Proceeding without that answer would invent authority, product intent, risk acceptance, ownership, or source truth.

Do not place an item in backlog/user-action-required merely because the task is difficult, an ordinary dependency is unavailable, an agent lacks a tool, implementation failed, or more technical investigation is possible. Keep agent-actionable work in its typed active backlog and record ordinary dependencies there.

Do not turn a synthetic evaluation boundary into user-action-required work unless it represents a genuine unresolved project decision. A scenario designed to prove safe blocking is test evidence, not automatically a user obligation.

A direct user request or explicit user authorization is sufficient authority to create an item
in its typed active backlog. Authority does not satisfy a declared hard dependency. Assign
Status: Ready only when dependency resolution proves that no hard prerequisite remains;
otherwise assign Status: Blocked with the dependency and exact unblock condition. A predicted
governed-definition boundary or other possible future user-owned decision is not by itself a
hard dependency: record it as an implementation constraint or Note without manufacturing a
creation-time approval question for work the user already requested.

Use User Action Required at creation when an agent independently identifies definite work, such as a confirmed defect or necessary enhancement, while performing other work and the user has not requested or authorized that new work. Ask whether the newly identified work should proceed before moving it into a typed active backlog.

After creation, route a user-requested item to backlog/user-action-required only when execution
reaches a distinct concrete user-owned decision, authority grant, action, risk acceptance, or
user-held fact that the original request did not resolve. Keep it Ready while no hard
prerequisite remains, record it Blocked when an ordinary hard dependency prevents all bounded
work, or route it to backlog/holding when the user explicitly defers it.

Use Open Questions for unresolved technical matters. Agents resolve ordinary technical uncertainty through discovery, design, review, and verification. Technical questions do not make an otherwise authorized item non-dispatchable.

Treat a question as an invalid User Action Required classification when an agent can resolve it with available project evidence or authorized technical work. Reject vague permission questions such as May I continue designing? when the user already requested the design. Rewrite the item as Ready with the technical matter under Open Questions, or as Holding only when the user explicitly deferred it.

## Governed Definition Approval

When the user explicitly requests creation of a work item whose requested outcome creates or
modifies named skills, treat that request as approval for the exact named skill-definition
paths resolved from the request and recorded in the work item. Assign Ready only when no hard
prerequisite remains, or Blocked with the exact dependency and unblock condition otherwise.
Do not ask the user to approve those same requested skill definitions again, and do not route
the item to User Action Required solely because the recorded paths are governed.

Use source discovery to identify the smallest governed skill-definition sources needed for the requested named skills and produce an exact canonical-path manifest. Record the exact scope, exact user wording, date, and exact user-message provenance durably in the work-item body as approval granted at creation. List supported generated mirrors and non-governed dependent artifacts separately from the governed canonical sources. Do not substitute a directory, wildcard, artifact category, or general permission for exact path-specific approval.

If implementation later discovers an additional skill-definition path outside the recorded requested manifest, stop mutation of that additional path and obtain new explicit scope-specific approval for it. The additional-path requirement does not revoke or suspend approval for the originally requested manifest. Agent definitions, schemas, model inputs, and unrelated metadata definitions are not authorized by a request for named skills unless the user's request also explicitly names or unambiguously requests them.

When an agent independently proposes a governed definition change that the user did not request, record the smallest exact manifest before asking the user and use User Action Required only when that approval is the next safe user-owned action.

Keep change-control manifests out of Design Principles. They are approval evidence, not design rules. Do not mutate a governed definition until the applicable project check accepts an approval record for that exact canonical path.

## Filename And Duplicate Detection

Use a stable, lowercase, hyphen-separated filename ending in .md. Derive the slug from the filename stem. Prefer names that describe the durable work, not a temporary symptom, date, owner, status, or vague cleanup label.

Before writing, search every active typed folder, backlog/user-action-required, backlog/holding, and every completed or failed archive for the same Work Item ID. Also search active and non-dispatchable work for the same source evidence or overlapping outcome. Do not search backlog/future-ideas. Update an existing active item only when the new request is clearly the same work. Create a new item only when it has a distinct outcome or can be completed independently. Never use a second provider or a different repository path to bypass a duplicate.

## Required Item Shape

Write each item as a self-contained work package with these fields and sections:

- Title: one clear heading naming the work.
- Status: Ready for authorized active work without unmet hard prerequisites, Blocked for
  authorized queued work waiting on a hard dependency, User Action Required for a user-owned
  answer, or Holding for explicit deferral.
- Type: Defect, Feature, Analysis, Investigation, or Holding.
- Provider: file.
- Work Item ID: the immutable filename stem, without `.md`.
- Completion: the selected completion process when known, or UNSET.
- Summary: the desired outcome.
- Context: facts, current behavior, user impact, constraints, and source references.
- Source Evidence: the request, finding, or decision that authorizes creation.
- Requirements: concrete behavior or deliverables.
- Acceptance Criteria: observable completion conditions.
- Dependencies: opaque Work Item IDs or None.
- Verification: expected tests, builds, checks, review, or artifacts.
- Open Questions: unresolved agent-resolvable technical matters, or None.
- Governed Definition Approval: optional exact canonical sources, allowed dependent artifacts, and approval resolution when governed definitions are expected to change.
- Notes: optional edge cases, examples, and non-goals.

For an item in backlog/user-action-required, also include:

- User Action Required.
- Question for the User.
- Why User Input Is Required.
- Options and Tradeoffs when choices are known.
- Resolution, initially Pending.
- Unattended Work Boundary.

The creation commit and result must preserve Work Item ID, current provider-owned location evidence, source evidence, provider selection, completion selection, creation authority, creation time when the repository records it, and applicable coordination evidence. Keep Requirements, Acceptance Criteria, Dependencies, and Verification so the item remains complete after it moves into an active typed backlog.

## Writing Rules

- Include exact paths, screens, procedures, examples, or data only when current evidence supports them.
- Reject Source Evidence that only says See the conversation above, As discussed, or equivalent context-dependent wording. Preserve the concrete request, finding, or decision and its provenance so the item stands alone.
- Mark unknown facts as questions or assumptions instead of inventing them.
- Keep requirements testable and separate them from acceptance criteria.
- Use opaque Work Item IDs for dependencies so the provider can resolve them after movement.
- Phrase user questions neutrally and expose viable tradeoffs.
- Keep completed or failed outcomes out of newly created active items.
- Use imperative, steady-state language.

## Coordinator Discovery

Do not send a routine task message after creating a work item. The Dev Backlog Coordinator discovers committed items by reading the authoritative provider inventory when scheduling or reconciling capacity. A specific Coordinator decision that creation cannot resolve may still be requested through the ordinary task-message contract.

## Final Check And Result

Before reporting completion:

- Confirm the effective provider is file and the mutation occurred only under backlog in the primary main worktree.
- Confirm commit-file-provider-transaction returned successful immutable proof for the exact
  ordinary-creation destination and preserved unrelated state.
- Confirm the item is in the right typed folder and has a stable globally unique Work Item ID.
- Confirm related multi-item goals have an index.md and linked independently runnable children.
- Confirm the complete required item shape, source evidence, dependencies, and verification expectations are present.
- Confirm every declared hard dependency was resolved before lifecycle assignment, Ready has
  none unmet, and Blocked dependency waits name the exact unblock condition.
- Confirm Open Questions contain only agent-resolvable uncertainty and do not create a false user-action gate.
- Confirm governed-definition approval evidence names exact canonical paths and user-message provenance before mutation.
- Confirm user-action-required content has the complete question and unattended boundary.
- Confirm no provider issue, mirror, shadow queue, or duplicate file was created.

Return a concise final outcome with provider file, opaque Work Item ID, current diagnostic
location, lifecycle status, and next runnable action. Keep commit identity, transaction proof,
and other durable evidence in the provider and Git records instead of duplicating them in the
task message.

## Migration

Callers migrated file-provider creation to create-work-item-file, and the legacy shells were removed. Historical mapping: create-backlog and file-based-backlog creation behavior moved into this skill; PROJECT.yaml and generated guidance now select Persistence file and reference create-work-item-file for creation.
