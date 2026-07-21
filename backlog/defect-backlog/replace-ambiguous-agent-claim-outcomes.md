# Replace Ambiguous Agent Claim Outcomes

Status: Running

Type: Defect

Provider: file

Provider Reference: backlog/defect-backlog/replace-ambiguous-agent-claim-outcomes.md

Completion: direct-main

## Current Execution

- Owner: Dev Orchestrator
- Canonical task: 019f8635-04d8-76a3-a895-5b7c7aafb734
- Worktree: /Users/martinbechard/.codex/worktrees/169b/dev-methodology
- Branch: codex/replace-ambiguous-agent-claim-outcomes
- Starting main: 3749489f1fdab17d9055a2905ec5ed6185b33a93
- Phase: Exact approval checks, bounded cross-repository implementation, independent review, and focused Tier 3 verification.
- Started: 2026-07-21
- Running-record claim: start-ambiguous-outcomes-019f8635, acquired event 6567944e-5ec3-4b80-a7d0-3111acbbec38.
- Open issues: None. Preserve the approved governed scope, append-only journal compatibility, and command/MCP parity.
- Accepted candidate: Pending.

## User Action Required

### Question For The User

Do you approve changing exactly skills/agent-claim/SKILL.md, skills/create-file-work-item/SKILL.md, and skills/manage-file-work-items/SKILL.md in dev-methodology, together with only their supported generated skill mirrors and directly related non-governed Python implementation, tests, evaluation contracts, README/design/migration documentation, to replace the seven ambiguous claim outcomes with the canonical vocabulary and schema-v2 compatibility plan recorded below; and do you authorize the paired non-governed claim engine, MCP tool descriptions, tests, and migration documentation changes in /Users/martinbechard/dev/mcp-agent-ops required to keep MCP results identical to the portability command? No conceptual agent definition or other governed skill is included.

### Why User Input Is Required

The smallest coherent correction changes three governed skill definitions, and cross-repository MCP parity requires ordinary implementation changes in mcp-agent-ops. Repository policy requires exact scope-specific approval before governed mutation or expansion into the sibling repository.

### Options And Tradeoffs

- Approve the complete stated scope: keep command and MCP outcomes identical with one schema-v2 compatibility plan.
- Approve only dev-methodology: update portable semantics but leave MCP parity as an explicit blocked dependency.
- Narrow or defer: preserve the discovery result without implementation.

### Resolution

- Answer: Approved.
- User wording: "ok authorized".
- Date: 2026-07-21.
- Provenance: direct user response in parent backlog-coordination task 019f77f4-c4bd-7c91-b197-c987a7beb838 to the exact question recorded above.
- Approved governed scope: skills/agent-claim/SKILL.md, skills/create-file-work-item/SKILL.md, and skills/manage-file-work-items/SKILL.md.
- Approved dependent scope: supported generated mirrors; directly related non-governed Python implementation, tests, evaluation contracts, README/design/migration documentation in dev-methodology; and paired non-governed claim engine, MCP tool descriptions, tests, and migration documentation in /Users/martinbechard/dev/mcp-agent-ops.
- Exclusions: no conceptual agent definition and no other governed skill.
- Disposition: Ready for a fresh canonical Dev Orchestrator task.

### Unattended Work Boundary

Implementation is authorized only within the exact resolved scope above. Preserve the append-only journal compatibility decision and do not expand to another governed definition without separate approval.

### Canonical Vocabulary And Compatibility Plan

- PRIMARY becomes SHARED_CHECKOUT_ACQUIRED.
- ISOLATE becomes ISOLATED_CHECKOUT_ACQUIRED.
- RECOVER becomes DIRTY_CHECKOUT_RECOVERY_ACQUIRED.
- WAIT becomes CLAIM_SCOPE_CONFLICT_WAIT_REQUIRED.
- PRIMARY_REQUIRED splits into SHARED_CHECKOUT_REQUIRED and SHARED_CHECKOUT_RELEASE_REQUIRED while retaining exit code 3 and the legacy alias.
- ISOLATE_REQUIRED becomes ISOLATED_CHECKOUT_SETUP_REQUIRED with exit code 4.
- RECOVERY_REQUIRED becomes DIRTY_CHECKOUT_RECOVERY_AUTHORIZATION_REQUIRED with exit code 5.
- Existing explicit outcomes remain unchanged.
- Schema-v1 journal events remain append-only and unmodified. Schema-v2 results carry canonical outcome plus legacy_outcome where applicable; readers normalize aliases without erasing raw provenance.

### Discovery Evidence

- Canonical task: 019f85c8-626e-77b2-8b7e-09c393a1530a.
- Discovery branch/worktree were clean and removed after routing the question; fresh delivery must start from current main.
- UAR routing claim: route-ambiguous-outcomes-approval, acquired event 044ba28a-355a-4d14-9df9-192c45345826.
- Approval transaction claim: approve-ambiguous-outcomes-20260721, acquired event f89e11bf-d998-46d1-8ccd-3167198ee5ca.

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
