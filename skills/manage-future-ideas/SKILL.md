---
name: manage-future-ideas
description: Capture, inventory, validate, and deliberately promote lightweight file-backed Future Ideas without treating them as work items.
metadata:
  category: development-practice
---

# Manage Future Ideas

## Future Ideas Definition

Future Ideas are file-provider-only lightweight records for possibilities that are not yet
actionable, approved, scheduled, or recognized as work. They are not work items or lifecycle
states. They remain non-dispatchable until a deliberate promotion creates a complete work item.

Do not include Future Ideas in ordinary duplicate scans, lifecycle inventory, runnable or
unattended counts, dispatch, ownership, dependency reconciliation, transitions, or archives.
Use this skill only when the request or an explicitly authorized workflow selects Future Ideas
capture, inventory, validation, ideation, or promotion.

## Provider And File Authority

- Apply this skill only when the effective provider is file or applicable project guidance
  permits an explicit one-item file-provider override.
- When the provider is UNSET, ask the user to select a provider before durable mutation.
- When another provider applies, return BLOCKED without creating a provider issue, shadow file,
  or second queue.
- Only the primary worktree on main may create or change canonical records under
  backlog/future-ideas.
- Another worktree may perform explicitly requested read-only inventory or validation but must
  return BLOCKED for capture or promotion mutation.
- Treat only resolved regular files contained by the canonical backlog/future-ideas root as
  idea records. Reject a symlinked or otherwise resolved path that escapes this authority
  without reading external bytes.

## Capture Future Idea

Capture an idea only when the user explicitly asks to remember it or the active workflow
explicitly authorizes an ideation capture step. A capture request authorizes only the
lightweight record. It does not authorize implementation or promotion.

Create one uniquely named Markdown file under backlog/future-ideas with this shape:

- One title heading.
- A Synopsis section with a short description of the possibility.
- An Origin or Rationale section that records where the thought came from or why it may matter.
- Optional Notes and Revisit Trigger sections.
- An optional Promoted To field added only after deliberate promotion.

Do not require Status, Type, Owner, Provider, Work Item ID, Completion, Context, Source Evidence,
Requirements, Acceptance Criteria, Dependencies, Verification, or a user decision. Keep a
Revisit Trigger as free text. It is a reminder for deliberate ideation, not a schedule or
dispatch condition.

Before capture, search backlog/future-ideas only for an existing idea with the same durable
meaning. If one exists, return that record without creating a duplicate. Otherwise prepare the
complete validated bytes and use commit-file-provider-transaction with operation
ordinary-creation. The shared transaction owns no-overwrite creation, coordination, Git,
rollback, immutable proof, and unrelated-state preservation.

## Inventory And Validate Future Ideas

Read backlog/future-ideas only for an explicit inventory, validation, ideation, or promotion
request. Validate each requested record as follows:

- Require one title, Synopsis, and Origin or Rationale.
- Allow Notes, a free-text Revisit Trigger, and Promoted To.
- Do not require work-item or lifecycle fields.
- Report invalid, unreadable, duplicated, or authority-escaping records instead of skipping
  them.
- Report ideas separately from Ready, Starting, Running, Stalled, Blocked, User Action Required,
  Holding, Awaiting Review, terminal, runnable, and unattended counts.

Ordinary file-provider inventory stays with manage-work-items-file. That inventory excludes
backlog/future-ideas and does not route here unless the request explicitly opts into Future Ideas.

## Promote Future Idea

Promote one idea only after explicit authorization for that promotion. Promotion keeps the
source idea and creates one complete reciprocal work item in one atomic transaction.

1. Read the retained source idea and verify its canonical regular-file authority.
2. Search ordinary active, non-dispatchable, completed, and failed work-item folders for the
   same Work Item ID, source evidence, or overlapping outcome.
3. Resolve the canonical destination before mutation. An existing destination or matching
   ordinary work item blocks promotion without changing either record.
4. Prepare, but do not commit, a complete typed item that conforms to create-work-item-file.
   Use the file work-item template. Include Open Questions and every destination-specific
   section.
5. Set Completion to exactly direct-main, feature-branch, or UNSET. Resolve every hard
   dependency before selecting Ready or Blocked.
6. Put the exact retained idea path in the destination Source Evidence. Add Promoted To with
   the destination Work Item ID to the retained idea.
7. Validate the complete reciprocal Source Evidence and Promoted To records, canonical target
   authority, destination Work Item ID, lifecycle, Completion, and links in both directions.
8. Use commit-file-provider-transaction with operation future-idea-promotion, the retained
   source path and bytes, the absent destination path and bytes, and a nonempty rationale for
   their atomic commit.

The destination may be an active typed item, recognized Holding work, or User Action Required
work. Holding may retain its underlying dispatchable Type or use Type: Holding. User Action
Required retains the underlying dispatchable Type. Promotion does not turn an optional Revisit
Trigger into lifecycle scheduling.

## Result

Return the operation, provider file, canonical idea path, title, synopsis, Origin or Rationale,
and optional Revisit Trigger. For capture and promotion, also return the transaction commit and
immutable proof. For promotion, also return the promoted Work Item ID, current diagnostic
destination, reciprocal link evidence, and explicit authorization evidence.

State that an unpromoted Future Idea is not runnable or approved work. Return BLOCKED with the
preserved paths, bytes, transaction evidence, blocker, recovery owner, and next safe action when
authority, validation, collision, transaction, rollback, or immutable proof is incomplete.
