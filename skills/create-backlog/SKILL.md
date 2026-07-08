---
type: Skill
name: create-backlog
description: Create structured markdown backlog items from requests, notes, bug reports, feature ideas, investigations, or analysis needs. Use when the user asks to add something to a backlog, capture work for later, split work into backlog items, classify work as a defect, feature, analysis, or investigation, or prepare backlog files that another agent can execute later.
---

# Create Backlog

## Purpose

Create backlog items that are clear, typed, dispatchable, and safe to manage later. A backlog item is a single markdown file in the correct active folder with enough context, acceptance criteria, dependencies, and verification expectations for a future agent to execute it without relying on the original conversation.

## Folder Model

Place new backlog items by work type:

- Defects go in docs/defect-backlog.
- Features go in docs/feature-backlog.
- Analyses go in docs/analysis-backlog.
- Investigations go in docs/investigation-backlog.
- Items that should remain visible but not automatically worked go in docs/holding.
- Do not create items directly in completed or failed archive folders.

If a repository has a documented taxonomy or placement rule, follow it before creating files. If the expected backlog folder does not exist, create the most specific standard folder that matches the item type unless project guidance says otherwise.

## Related Item Series

When one goal naturally contains multiple related backlog items, create a subfolder under the appropriate typed backlog folder instead of placing every item flat in the parent folder. The subfolder name should be the stable goal slug.

Create an index.md file inside the subfolder. The index describes the overall goal, purpose, current data or design anchors, non-goals, definition of good, and recommended implementation order. The index is a coordination artifact, not a runnable backlog item.

Create the smaller backlog items as separate markdown files in the same subfolder. Each child item should remain independently dispatchable and should link back to index.md. The index should link to every child item and group them by sequence or theme.

Use a series folder when:

- The work has one goal but multiple ordered phases.
- Different child items can be implemented, analyzed, or verified independently.
- The index can preserve context that would otherwise be duplicated across child items.
- A later agent needs to understand the whole goal before choosing the next item.

Avoid a series folder when a single backlog item can clearly express the work and all acceptance criteria.

## Item Classification

Classify by the outcome the work must produce:

- Defect: broken or regressed behavior must be corrected.
- Feature: new or expanded behavior must be delivered.
- Analysis: a question must be answered with evidence, options, or recommendations.
- Investigation: an unclear failure, risk, or system behavior must be traced until the next action is known.
- Holding: the item is real but intentionally not ready for dispatch.

When a request mixes types, split it into separate backlog items only when the parts can be completed independently. Keep a single item when one coherent delivery outcome depends on all parts.

## Filename And Slug

Use a stable, lowercase, hyphen-separated filename ending in .md. Derive the slug from the filename stem.

Prefer names that describe the durable work, not the temporary symptom report. Avoid dates, owner names, status words, and vague names such as cleanup, fixes, or improvements unless project guidance requires them.

Before writing a new file, check the target folder for an existing matching or overlapping item. Update an existing active item when the new request is clearly the same work; create a new item when it has a different outcome or can be completed independently.

## Required Item Shape

Write each backlog item as a self-contained work package with these sections:

- Title: one clear heading naming the work.
- Status: Proposed for new items unless the user gives a different explicit state.
- Type: Defect, Feature, Analysis, Investigation, or Holding.
- Summary: one short paragraph explaining the desired outcome.
- Context: facts, current behavior, user impact, constraints, and source references needed to understand the work.
- Requirements: concrete behavior or deliverables that must be true when complete.
- Acceptance Criteria: observable checks that decide whether the item is done.
- Dependencies: backlog slugs or external prerequisites. Use None when there are none.
- Verification: tests, builds, manual checks, review evidence, or artifacts expected from completion.
- Notes: optional edge cases, examples, non-goals, and open questions.

Use imperative, steady-state language. Do not describe the item as revised, enhanced, or updated unless the work itself is specifically about revision history.

## Writing Rules

Make the item executable by a future agent:

- Include exact paths, screens, procedures, examples, or data only when they are known from current evidence.
- Mark unknown facts as questions or assumptions instead of inventing them.
- Keep requirements testable and avoid broad wishes such as make it better.
- Separate requirements from acceptance criteria: requirements state what must exist, acceptance criteria state how completion is recognized.
- Include dependencies by slug so blocked work can be detected mechanically.
- Keep completed or failed outcomes out of new active items.

## Final Check

Before reporting completion:

- Confirm the item is in the right typed folder.
- Confirm related multi-item goals have a goal subfolder with index.md and child item links.
- Confirm the filename slug is stable and unique.
- Confirm the item contains Status, Type, Summary, Requirements, Acceptance Criteria, Dependencies, and Verification.
- Confirm the item can be understood without the chat history.
