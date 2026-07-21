# Replace Ambiguous Agent Claim Outcomes

Status: Ready

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/replace-ambiguous-agent-claim-outcomes.md

Completion: direct-main

Creation Claim: capture-resource-coordination-dialogue-20260721

## Summary

Replace ambiguous agent-claim outcome vocabulary with names that communicate whether ownership was acquired, what location or scope is involved, and what action is required next.

## Context

During the user-reviewed dialogue on 2026-07-21, PRIMARY was identified as unclear and ISOLATE versus ISOLATE_REQUIRED as difficult to distinguish. PRIMARY currently means successful ownership in Git's existing primary worktree; it does not mean project-level ownership. Renaming it to another phrase containing primary would preserve the ambiguity.

The vocabulary is exposed through the Python command, MCP results, tests, documentation, journals, generated material, and potentially external callers. A direct unversioned rename could therefore break consumers and historical interpretation.

Candidate examples discussed were SHARED_CHECKOUT_ACQUIRED, ISOLATED_CHECKOUT_ACQUIRED, and ISOLATED_CHECKOUT_SETUP_REQUIRED. These are examples, not predetermined names.

## Source Evidence

- On 2026-07-21, the user identified PRIMARY as unclear and questioned the distinction between ISOLATE and ISOLATE_REQUIRED.
- The user explicitly requested a defect work item that highlights the ambiguous vocabulary and replaces it with more meaningful terms.
- On 2026-07-21, the user authorized creation of work items based on the resulting conversation.

## Requirements

- Inventory every public and persisted outcome, command term, exit-code mapping, test assertion, journal field, MCP schema, and documentation reference.
- Define each state first in plain language without using the existing PRIMARY or ISOLATE shorthand.
- Choose names that distinguish success, failure, required caller action, ownership scope, and checkout location.
- Avoid terminology that incorrectly implies project-wide ownership.
- Distinguish an unsuccessful operation from a successful operation that requires a different next step.
- Specify compatibility aliases or an explicit versioned migration for commands, MCP clients, journals, and external consumers.
- Keep exit-code interpretation deterministic during the compatibility period.
- Update source, tests, generated surfaces, design documentation, and migration guidance consistently.
- Obtain exact, scope-specific approval before changing the governed agent-claim skill definition.

## Acceptance Criteria

- A reader can understand every outcome without prior knowledge of Git worktree terminology or the old names.
- Successful acquisition names state that ownership was acquired and identify the relevant checkout mode.
- Required-action names state what input, setup, location, recovery authority, or waiting condition is required.
- No replacement uses primary as unexplained shorthand or mislabels checkout ownership as project-level ownership.
- Existing supported consumers receive deterministic compatibility or versioned failure guidance.
- Current and historical journal entries remain interpretable.
- Python, MCP, documentation, and tests agree on the same vocabulary and transition meanings.

## Dependencies

None.

## Verification

- Build an outcome-to-meaning-to-next-action inventory before selecting names.
- Search the repository and generated outputs for every old term before and after implementation.
- Test command and MCP compatibility, exit codes, journal reading, status normalization, and migration errors.
- Run the full shared claim-infrastructure regression appropriate to this Tier 3 change.
- Run Git diff validation and independent methodology review.

## Open Questions

- Which historical result aliases must remain accepted, and for how long or through which schema version?
- Should persisted journals retain original outcome strings with display normalization, or receive an explicit migration tool?
