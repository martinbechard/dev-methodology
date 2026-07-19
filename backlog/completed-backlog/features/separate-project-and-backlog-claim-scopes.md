# Separate Project And Backlog Claim Scopes

Status: Completed

Type: Feature

Lifecycle ownership: Dev Backlog Steward acquired PRIMARY claim separate-project-backlog-scopes-start for root task 019f77f4-c4bd-7c91-b197-c987a7beb838 under LIFECYCLE START authority from starting commit cc74356b7f16071ae8f41e1b28952f4eaafe81ae.

## Completion Evidence

- Running lifecycle: Dev Backlog Steward acquired the exact active-item PRIMARY claim at event 09460763-f9ab-4631-bc6d-90cdcbfcea1c, committed the Running transition as bd2f401306196ceb9575a1b83354a15e82b57c5b, and released at event 8d18dc4f-dae9-4189-b1bf-7dbbefc99e5d.
- Accepted methodology source: commits 416af6e8d4d85be3f436a066c5d1ecd226eea1a4, 30f4b7875e4cbd2dd3ed200c56e8766088126218, 4e211d4862250ac15ca2962b89b0840ddde4b418, and fb04b6a78737d0540f2ef22091208584554d4969 implemented domain-separated project-files, backlog, and all-files ownership. Independent review identified and drove corrections for path-safe status parsing, legacy registry compatibility, per-domain reporting, precise path handling, and complete commit-history release checks; the corrected source and 55 focused claim-engine tests were accepted. The final producer claim released at event ae996ac9-e75c-44c1-8edc-a78a8f5aaf00.
- Deliberate integration: the accepted source chain was integrated without absorbing unrelated artifact work. Generated skill documentation was rebuilt from approved canonical skill sources. A post-integration code review identified missing bundle-content assertions, correction commit 5e93e439093ea149f4da4c5e448505a78fc689fc added them, and fresh artifact and code re-reviews accepted the result. Integration ownership released at event 1814836a-3cca-4b3e-bb35-1f6aa066b405.
- Final verification: claim-engine tests passed 55 of 55; definition approval checks for agent-claim, create-backlog, and manage-backlog returned ALLOWED_APPROVED_DEFINITION_CHANGE; every deterministic generated-output and skill-validation gate passed; project-wiki tests passed 17 of 17; and the partitioned scripts suite passed 448 of 449 cases. The sole failure was the known unrelated stale active-path assertion in BundleContentTests.test_backlog_skills_separate_user_action_required_from_dispatchable_work, reproduced at baseline commit 4f643a993bbab63b18fe991a02e27d8220d8d457 and owned by a separate Running defect item. Final verifier ownership released at event 0ab748db-af5a-4ef3-b180-e1479a0435a9 with the feature accepted as PASS with that baseline warning.
- MCP publication: standalone mcp-agent-ops commit afbdfd66d97dc694d7c93cb34f595762765d3f3d published release v0.3.0 with passing 105-test, Ruff, mypy, checksum, installed-stdio, and disposable-repository broad-scope smoke evidence. The installed runtime identity contained 26 files with digest 314a780796740e8e31c375af7e5a3b1f8446d7566b2732846f266fe1cca13aeb, and the final smoke claim released at event 5832ab40-3bcf-41b6-bfae-fc8ff149d38a.
- User deployment: the user-scope Codex bundle replacement installed 110 skill entries and 26 agent definitions. Source-to-install file digests matched for agent-claim at 3d7037a154a1424883ef19466f8453782f044b3a47ecb7f6d5745a704dd7b3a8, create-backlog at 514b895a6e9dfbe19fe016545305a0dae1581ad05bdc185ff469a411fd5bf2c9, and manage-backlog at 9cdc121ac1327fb5b200b46b6569b909654a37944019ad378a8e68e9670741d2. Deployment claim separate-project-backlog-scopes-deploy acquired at event d1293d0f-fb74-499d-b0dd-8648a2a1819a and released at event b57118a9-f9a1-4aa9-a0c8-c163ec2afb1a.
- MCP refresh: atomic catalog refresh completed at revision 642b3ce8020aca1116046a94d1b8d0cd2299a86276bd8704bb3675c3ab65209e. One ordered all-or-nothing load returned ok true with no errors at that revision for agent-claim digest a3a487c3b359d0fe81260e0cee0547e0855d7d954e0b4c14f4817cf29cffb2c7, create-backlog digest b26e40dc6333c5e626ce05b148137ce32e21124a94fcb806a979a742d327a363, and manage-backlog digest 13ea2daecd94d52c83526d3e7c168a86818b274084f10f019201c9b59619b6b4.
- Worktree retirement: after accepted commits were preserved and integrated, cleanup claim separate-project-backlog-scopes-worktree-cleanup acquired at event b66ece1f-cbd0-4d6a-a102-678a1ed3a92b, removed only the two clean methodology producer worktrees, and released without repository-file changes at event d27aa51a-3b3f-4c6a-ac9e-a9c30a4b5e97.
- Serialized backlog baton: Project Organiser moved its separate item into User Action Required at commit 1579ce1199895fe90aecac0f4c5927796852f260; exact claim align-project-organiser-filename-selection-user-action-required-after-deploy acquired at event 3858f3f9-9d34-438d-ad28-d7e3c868e175 and released at event 0fef8ce4-aa6f-4424-a220-6a7eb106580d. No governed, artifact, or test surface changed in that queue transaction.
- Terminal lifecycle ownership: Dev Backlog Steward acquired PRIMARY claim separate-project-backlog-scopes-terminal-completed for only this active feature item and its completed-feature destination at event 23077b9b-b591-4142-8236-3abab6bd7df2. The claim is released immediately after this archive commit is validated and clean.

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
