---
name: create-file-work-item
description: Create one authoritative repository-backed work item with typed placement, source evidence, user-action boundaries, and atomic no-overwrite creation when the effective provider is file.
metadata:
  category: development-practice
---

# Create File Work Item

## Purpose

Create one durable file-provider work item that is clear, typed, and safe to manage later, or deliberately capture one lightweight Future Idea without misrepresenting it as work. Ordinary active items must be dispatchable without the original conversation. User-action-required items must preserve the exact decision or information only the user can provide and must remain separate from unattended work.

## Provider Selection

- Apply this skill only when the effective provider is file or applicable project guidance permits an explicit request to select file for this one item.
- When durable provider work is required and the provider is UNSET, ask the user to select a provider before mutation.
- When the effective provider is none or another provider, return the provider mismatch without creating a file or falling back to file storage.
- Do not create or update GitHub, GitLab, Azure DevOps, or Jira records and do not mirror their items under backlog.
- Durable Future Ideas are available only through the file provider. When another provider is selected, return BLOCKED without capturing, listing, or promoting the idea unless the user explicitly selects file as the one-item provider override for that idea. Never turn a Future Idea into a provider issue or create a shadow file beside another provider.

## File Authority

Only the primary worktree on main may create canonical files under backlog. The repository-relative backlog path is both work_item_id and provider_reference.

Another worktree may inspect backlog but must not create the item. If the primary worktree is not on main, it must not create the item. Return BLOCKED with the observed worktree, branch, and required handoff. Do not create another queue elsewhere.

Resolve the final canonical path first, then create it with the platform's exclusive-create operation so the write fails when the path already exists. Never preflight with an existence check followed by an ordinary overwrite-capable write. Write the complete intended bytes through that exclusive descriptor, synchronize and close it, validate the created item, and remove only that newly created path if validation or commit fails. An existing target means duplicate reconciliation is required; do not overwrite or retry with a different name.

Keep backlog creation separate from implementation ownership. When creation immediately authorizes delivery, record and commit the READY item first.

## Template Workflow

Start each item from [file-work-item-template.md](../development-methodology/assets/templates/file-work-item-template.md). Replace every TODO instruction with source-backed content. Remove every guidance comment before commit. Remove an optional Series, User Action Required, or Notes section when it does not apply; do not leave empty headings or placeholder boilerplate.

- Ready items keep Status: Ready and remain dispatchable while Open Questions contain only agent-resolvable technical uncertainty.
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
- Potentially useful thoughts that are not yet actionable, approved, scheduled, or recognized as work go in backlog/future-ideas.
- Do not create items directly in completed or failed archive folders.

If a repository has a documented taxonomy or placement rule, follow it before creating files within the authoritative backlog root. If the expected backlog folder does not exist, create the most specific standard folder that matches the item type unless project guidance says otherwise.

User Action Required is a queue state, not a work type. Preserve the underlying Type as Defect, Feature, Analysis, or Investigation so an answered item has a deterministic active destination. Use Status: User Action Required while the item remains in backlog/user-action-required.

backlog/future-ideas, backlog/holding, and backlog/user-action-required are different. Future Ideas contains thoughts that have not become recognized work. Holding contains already-recognized work intentionally deferred without an immediate question. User Action Required contains recognized work that cannot safely advance until the user answers a concrete question.

## Future Ideas Capture

Capture an idea only when the user explicitly asks to remember it or the active workflow explicitly includes an ideation capture step. Use one Markdown file under backlog/future-ideas with this minimal shape:

- One title heading.
- A Synopsis section with a short description of the possibility.
- An Origin or Rationale section explaining where the thought came from or why it may matter.
- Optional Notes and Revisit Trigger sections.
- An optional Promoted To field after deliberate promotion.

Do not require Status, Type, Owner, Provider, Provider Reference, Completion, Context, Source Evidence, Requirements, Acceptance Criteria, Dependencies, Verification, or a user decision merely to preserve an idea. Keep revisit triggers as free text; they are reminders for deliberate ideation, not machine schedules or dispatch conditions.

Future Ideas are not work items or lifecycle states. Do not include them in ordinary duplicate scans, inventory, runnable counts, unattended selection, dispatch, ownership, lifecycle transitions, dependency reconciliation, or archive movement. List or validate them only when the user explicitly requests Future Ideas, ideation, or promotion work.

A request to capture an idea authorizes only the lightweight record. It does not authorize implementation or promotion.

## Future Idea Promotion

Promote an idea only through a deliberate user-authorized operation:

1. Read the retained source idea, resolve its canonical regular-file authority, and search ordinary queues for an existing matching work item.
2. Resolve the intended canonical target path and preflight target collisions before any promotion write. An existing target or matching ordinary work item blocks promotion without changing either record.
3. Remain on primary main. Follow the Claim Events table in agent-claim for the retained Future Idea update. Create the promoted file with an exclusive create operation. Stop if the target already exists. Before editing, save the source idea, target, and Git index state needed to restore the attempt.
4. Create one complete typed work item in its applicable active, Holding, or User Action Required destination with every field and section required by Required Item Shape, including Open Questions, and any destination-specific sections. Holding may retain its underlying dispatchable Type or declare Type: Holding; User Action Required must retain its underlying dispatchable Type.
5. Set Completion to exactly direct-main, feature-branch, or UNSET.
6. Include the exact canonical source idea path in the promoted work item's Source Evidence section.
7. Retain the original idea in backlog/future-ideas and add Promoted To with the promoted item's canonical provider reference.
8. Validate both files, the complete item shape, destination rules, and links in both directions.
9. Stage exactly the idea and target paths without clearing, replacing, or committing unrelated staged state. Use a path-limited commit for exactly those two paths.
10. Capture the new commit OID immediately after commit creation. Re-read that exact immutable object rather than mutable HEAD and require its changed-path set and reciprocal record bytes to contain exactly the intended pair. Verify unrelated staged state remains staged before reporting success.

The promotion must either succeed completely or restore the previous state. If writing, validation, staging, or the pre-commit step fails, restore the source idea and Git index. Remove only the new target created by this attempt. Verify the restored state before returning.

If the commit result is unknown, inspect Git history before deciding whether to restore files. Read the resulting commit ID directly from Git.

If restoration fails, or if the commit does not contain the two linked records, return BLOCKED. Identify the saved recovery evidence and the Dev Backlog Steward responsible for recovery. Do not report success until the commit contains exactly those two files and unrelated staged files remain unchanged.

Promotion does not copy the idea's optional revisit trigger into lifecycle scheduling. The promoted work item receives Status: Ready in its typed active folder when promotion authorizes active work, Status: Holding when the user deliberately defers the recognized work, or Status: User Action Required when a separate genuine user-owned question prevents safe work.

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

Do not use User Action Required merely to preserve an independently identified possibility. If the active workflow explicitly authorizes idea capture, place that possibility in backlog/future-ideas without asking for approval to perform work. Otherwise report it ephemerally rather than creating an unauthorized durable record.

Also use User Action Required when all of these are true:

- The next safe action depends on a decision, approval, authority grant, value judgment, or information that belongs to the user.
- The item can state one concrete question whose answer changes what happens next.
- Proceeding without that answer would invent authority, product intent, risk acceptance, ownership, or source truth.

Do not place an item in backlog/user-action-required merely because the task is difficult, an ordinary dependency is unavailable, an agent lacks a tool, implementation failed, or more technical investigation is possible. Keep agent-actionable work in its typed active backlog and record ordinary dependencies there.

Do not turn a synthetic evaluation boundary into user-action-required work unless it represents a genuine unresolved project decision. A scenario designed to prove safe blocking is test evidence, not automatically a user obligation.

A direct user request or explicit user authorization is sufficient authority to create an item in its typed active backlog with Status: Ready. This creation classification remains Ready even when discovery predicts that implementation may later reach a governed-definition approval boundary or another separate user-owned decision. Record that anticipated boundary as an implementation constraint or Note without framing it as a pending user question; do not manufacture a creation-time approval question for work the user already requested.

Use User Action Required at creation when an agent independently identifies definite work, such as a confirmed defect or necessary enhancement, while performing other work and the user has not requested or authorized that new work. Ask whether the newly identified work should proceed before moving it into a typed active backlog. Preserve an uncertain possibility as a Future Idea only when the active workflow explicitly authorizes lightweight capture.

After creation, route a user-requested Ready item to backlog/user-action-required only when execution reaches a distinct concrete user-owned decision, authority grant, action, risk acceptance, or user-held fact that the original request did not resolve. Keep it Ready when ordinary evidence-backed dependencies remain, or route it to backlog/holding when the user explicitly defers it.

Use Open Questions for unresolved technical matters. Agents resolve ordinary technical uncertainty through discovery, design, review, and verification. Technical questions do not make an otherwise authorized item non-dispatchable.

Treat a question as an invalid User Action Required classification when an agent can resolve it with available project evidence or authorized technical work. Reject vague permission questions such as May I continue designing? when the user already requested the design. Rewrite the item as Ready with the technical matter under Open Questions, or as Holding only when the user explicitly deferred it.

## Governed Definition Approval

Before requesting approval for a governed definition change, use source discovery to identify the smallest required governed sources and produce an exact canonical-path manifest. Record that manifest in the work-item body before asking the user. Do not substitute a directory, wildcard, artifact category, or general permission for exact path-specific approval.

Record the exact approval scope, exact user wording, date, and exact user-message provenance durably in the work-item body. List any allowed generated mirrors or other dependent artifacts separately from the governed canonical sources.

Keep change-control manifests out of Design Principles. They are approval evidence, not design rules. Do not mutate a governed definition until the applicable project check accepts an approval record for that exact canonical path.

## Filename And Duplicate Detection

Use a stable, lowercase, hyphen-separated filename ending in .md. Derive the slug from the filename stem. Prefer names that describe the durable work, not a temporary symptom, date, owner, status, or vague cleanup label.

Before writing, search every active typed folder, backlog/user-action-required, and backlog/holding for the same canonical path, slug, source reference, or overlapping outcome. Search backlog/future-ideas only during explicit idea capture or promotion. Update an existing active item only when the new request is clearly the same work. Create a new item only when it has a distinct outcome or can be completed independently. Never use a second provider or a different repository path to bypass a duplicate.

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
- Open Questions: unresolved agent-resolvable technical matters, or None.
- Notes: optional edge cases, examples, and non-goals.

For an item in backlog/user-action-required, also include:

- User Action Required.
- Question for the User.
- Why User Input Is Required.
- Options and Tradeoffs when choices are known.
- Resolution, initially Pending.
- Unattended Work Boundary.

The creation commit and result must preserve work_item_id, provider_reference, source evidence, provider selection, completion selection, creation authority, creation time when the repository records it, and applicable claim evidence. Keep Requirements, Acceptance Criteria, Dependencies, and Verification so the item remains complete after it moves into an active typed backlog.

## Writing Rules

- Include exact paths, screens, procedures, examples, or data only when current evidence supports them.
- Reject Source Evidence that only says See the conversation above, As discussed, or equivalent context-dependent wording. Preserve the concrete request, finding, or decision and its provenance so the item stands alone.
- Mark unknown facts as questions or assumptions instead of inventing them.
- Keep requirements testable and separate them from acceptance criteria.
- Use provider-accurate dependency references so blocked work can be detected mechanically.
- Phrase user questions neutrally and expose viable tradeoffs.
- Keep completed or failed outcomes out of newly created active items.
- Use imperative, steady-state language.

## Final Check And Result

Before reporting completion:

- Confirm the effective provider is file and the mutation occurred only under backlog in the primary main worktree.
- Confirm uniquely named atomic no-overwrite creation succeeded.
- Confirm the item is in the right typed folder and has a stable unique path.
- Confirm related multi-item goals have an index.md and linked independently runnable children.
- Confirm the complete required item shape, source evidence, dependencies, and verification expectations are present.
- Confirm Open Questions contain only agent-resolvable uncertainty and do not create a false user-action gate.
- Confirm governed-definition approval evidence names exact canonical paths and user-message provenance before mutation.
- Confirm user-action-required content has the complete question and unattended boundary.
- For Future Ideas, confirm the minimal idea shape, exclusion from ordinary work-item scans, resolved regular-file authority within backlog/future-ideas, and any reciprocal Promoted To and exact Source Evidence link.
- Confirm no provider issue, mirror, shadow queue, or duplicate file was created.

For an ordinary work item, return provider file, work_item_id and provider_reference, item type, lifecycle status, source evidence, dependencies, completion selection, creation commit, and next runnable action. For a Future Idea, return its path, synopsis, origin or rationale, optional revisit trigger, capture commit, and the fact that it is not runnable or approved work.

## Migration

Callers migrated file-provider creation to create-file-work-item, and the legacy shells were removed. Historical mapping: create-backlog and file-based-backlog creation behavior moved into this skill; PROJECT.yaml and generated guidance now select Persistence file and reference create-file-work-item for creation.
