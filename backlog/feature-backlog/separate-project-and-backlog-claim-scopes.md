# Separate Project And Backlog Claim Scopes

Status: Proposed

Type: Feature

## Summary

Separate ordinary project ownership from the primary-worktree-only backlog so broad implementation claims do not implicitly own backlog state, while backlog lifecycle work has one explicit serialized scope.

## Context

The claim engine currently supports exact files, directory trees, all-files ownership, and repository-global resources. The backlog is stored at the repository root and omitted from newly created isolated worktrees, but all-files still includes it. Dirty-worktree and release checks also inspect the complete checkout, so unrelated backlog changes can force an ordinary project claim into recovery or prevent its release.

The intended ownership model has three explicit broad file domains:

- project-files covers the repository file tree except backlog and ignored operational worktree state.
- backlog covers the complete backlog subtree and is available only from the primary worktree.
- all-files is the explicit union of project-files and backlog for exceptional repository-wide recovery or migration.

Backlog state transitions should use short serialized backlog claims. Implementation work should use separate exact, tree, resource, or project-files claims so an agent does not hold the backlog throughout delivery.

## Evidence

- skills/agent-claim/SKILL.md defines narrow ownership, all-files behavior, primary-only backlog access, sparse isolated worktrees, recovery, and release.
- skills/agent-claim/scripts/claim.py owns scope normalization, overlap detection, primary-worktree routing, dirty-state checks, isolated worktree creation, journaling, reporting, and release.
- scripts/test_agent_claim.py contains the deterministic claim-engine regression suite.
- skills/create-backlog/SKILL.md and skills/manage-backlog/SKILL.md own backlog creation, dispatch, lifecycle transitions, and archive guidance.
- The mcp-agent-ops claim tools expose the runtime claim contract and require a corresponding published schema and implementation.

## Requirements

- Add a first-class project-files scope that covers repository project files while excluding backlog and ignored operational worktree state.
- Add a first-class backlog scope that covers the complete backlog subtree without requiring callers to model it as an ordinary tree.
- Keep all-files as an explicit complete-repository scope that includes both project-files and backlog, requires a bounded reason, and remains primary-worktree-only.
- Make project-files, backlog, and all-files mutually exclusive broad file-domain selections.
- Reject one claim that mixes backlog-domain paths with project-domain paths. Permit repository-global resource scopes to accompany the selected file domain when required.
- Preserve compatibility for explicit backlog file and tree inputs by classifying them as backlog-domain ownership and applying the same primary-only rules.
- Return PRIMARY_REQUIRED without changing the registry when backlog ownership is requested while another claim owns the primary worktree or when an isolated claim attempts to extend into backlog ownership.
- Create isolated worktrees for eligible project claims beneath the primary worktree's ignored .worktrees directory and omit backlog through worktree-specific sparse checkout.
- Define overlap rules so project-files conflicts with project-domain files and trees, backlog conflicts with backlog-domain files and trees, all-files conflicts with both domains, and identical resources continue to conflict independently.
- Make acquisition, recovery, committed release, and no-change release checks domain-aware. Record out-of-domain baseline state, keep it outside the claim, and reject release if it changed during the claim without treating unchanged out-of-domain dirtiness as owned work.
- Prevent project claims from staging or committing backlog changes and prevent backlog claims from staging or committing project changes.
- Update create-backlog and manage-backlog guidance to use a short backlog claim for queue transitions, a separate implementation claim for delivery, and a later backlog claim for result recording and archival.
- Extend claim status, journal events, contention reports, and diagnostics so the selected file domain and any compatibility normalization are explicit.
- Update the fallback command, copied command, MCP claim acquisition and extension schemas, runtime implementation, help text, generated documentation, regression tests, and public operator guidance together.
- Publish and deploy compatible mcp-agent-ops and distributed Agent Skill versions so the exposed MCP contract advertises and enforces project-files, backlog, all-files, PRIMARY_REQUIRED, canonical worktree placement, and backlog sparse-checkout behavior.

## Acceptance Criteria

- A project-files claim never owns or overlaps backlog paths unless another requested scope independently conflicts through a shared resource.
- A backlog claim owns only backlog paths and never creates or enters an isolated worktree.
- An all-files claim explicitly owns both domains and cannot be mistaken for the ordinary broad project scope.
- Passing the repository root identifies the coordination registry without implicitly selecting all-files or backlog ownership.
- Explicit backlog file and tree inputs receive backlog-domain behavior and cannot bypass primary-only enforcement.
- Mixed backlog-domain and project-domain path requests fail atomically with structured guidance and leave the registry unchanged.
- Unchanged pre-existing backlog dirtiness does not force a project-files claim into recovery or prevent release, and unchanged pre-existing project dirtiness does not become owned by a backlog claim.
- Any out-of-domain change made after acquisition prevents release and is reported without being staged, committed, reverted, or cleaned by the claim owner.
- A second non-overlapping project writer receives a canonical sparse isolated checkout without a backlog directory.
- Backlog acquisition while the primary worktree is occupied returns PRIMARY_REQUIRED and does not create a linked checkout.
- Claim status and journal reports distinguish project-files, backlog, and all-files ownership.
- The live MCP tool schemas expose the new scopes and their primary-only and sparse-checkout outcomes after publication.
- Distributed skill content, generated documentation, bundle tests, claim-engine tests, MCP tests, and installation verification all pass.

## Dependencies

None.

## Verification

- Add focused unit tests covering scope normalization, mutual exclusion, compatibility inputs, overlap pairs, atomic rejection, acquisition, extension, recovery, and release.
- Add dirty-baseline tests for project-only, backlog-only, and changed out-of-domain state.
- Add worktree tests proving canonical placement and absence of backlog in new isolated project checkouts.
- Add MCP contract tests for project-files, backlog, all-files, PRIMARY_REQUIRED, and structured invalid-scope results.
- Run the complete claim-engine test module with the repository's supported Python interpreter.
- Run Agent Skill validation, generated-output freshness checks, repository script tests, project-wiki script tests, and Git diff validation required by AGENTS.md.
- Install the user-scope bundle with replacement, refresh the MCP skill catalog, and verify the installed skill and copied claim engine match the committed source.
- Inspect the live MCP tool descriptions and execute a disposable-repository smoke test for each broad scope before publication is considered complete.

## Notes

- The backlog claim serializes queue mutations; the backlog item's recorded owner and the implementation claim preserve delivery ownership between short queue transitions.
- Do not hold backlog ownership for the full duration of implementation work.
- Do not remove or rewrite legacy linked worktrees as part of scope normalization. Audit or retire them through a separate safe cleanup procedure that preserves active, dirty, or unintegrated work.
- Keep all-files available for deliberate recovery and true repository-wide migrations rather than changing its meaning to exclude backlog.
