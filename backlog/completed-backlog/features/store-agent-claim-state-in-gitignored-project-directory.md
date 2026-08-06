# Store Agent Claim State In Gitignored Project Directory

Status: Completed

Owner: Unowned

Type: Feature

Provider: file

Work Item ID: store-agent-claim-state-in-gitignored-project-directory

Completion: direct-main

Provider Reference: backlog/completed-backlog/features/store-agent-claim-state-in-gitignored-project-directory.md

## Current Dispatch Reservation

Transition: Ready -> Starting.

Parent Coordination Thread: /root (thread 019fb057-1767-7ef2-b5fa-41f4417b20b3).

Launch Reservation: One distinct parent-owned launch reservation for this provider record.

Normalized Objective: Move agent claim state into the primary worktree's gitignored .codex/agent-claim directory.

Dispatch Time: 2026-08-06T00:04:47Z.

Intended Root Dev Orchestrator Role: Dev Orchestrator.

Canonical Runtime Evidence: None at reservation time. No runtime task has been created.

Current Launch Evidence: Parent Coordinator authorized this exact reservation; exact-file backlog claim starting-store-agent-claim-state-in-gitignored-project-directory-019fb057 acquired with outcome SHARED_CHECKOUT_ACQUIRED and event 4bb2b1f7-39a8-4f95-9176-fa7e8946f779.

Required Next Lifecycle Transition: The canonical root Dev Orchestrator must separately accept Starting -> Running before repository mutation.

## User Action Required

### Question for the User

Do you explicitly approve permanently overwriting only a verified-empty, exclusively locked Windows legacy `.git/agent-claims.json` with the exact tombstone marker, with migration stopping without mutation if any live claim exists?

### Why User Input Is Required

Native Windows CI run 31068038651 proves that an open locked legacy registry cannot be unlinked. The narrow same-inode tombstone design avoids that unlink but permanently replaces the verified-empty legacy registry bytes. The execution safety gate requires direct risk-aware approval for that destructive boundary despite the earlier authorization to retire the disposable legacy state.

### Options and Tradeoffs

- Approve: resume the preserved correction at dev-methodology candidate d2744c62281b5fc2bfdabd0d95a72642aab2924e and external mcp-agent-ops candidate 660aef8be2cfc12926aef15c90250556760961a7, apply only the fail-closed empty-and-locked tombstone retirement, rerun fresh independent gates and native Windows CI, release mcp-agent-ops 0.6.0, and complete direct-main delivery.
- Decline: preserve both candidates and leave the legacy registry retirement—and therefore this delivery—unfinished while a different Windows-safe design is selected.

### Resolution

Approved. On 2026-08-06, the user directly answered in canonical task
019fd464-3875-75e2-aaa0-39a8e357d764: “I approve the verified-empty Windows legacy registry tombstone operation and the provider lifecycle resumption.” This approval applies only to the verified-empty, exclusively locked legacy registry boundary. Migration must stop without mutation if any live claim exists.

### Unattended Work Boundary

Do not retry or apply the retirement mutation, wake correction agents, run release gates, publish mcp-agent-ops 0.6.0, integrate to main, or close this item before the answer is recorded and the same canonical task resumes through User Action Required -> Ready -> Starting -> Running. Read-only inspection may continue; unrelated work remains independent.

## User Action Required Transition Evidence

Transition: Running -> User Action Required.

Transitioned At: 2026-08-06T03:57:14Z.

Decision Owner: Parent Coordinator 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Canonical Thread And Root Task: 019fd464-3875-75e2-aaa0-39a8e357d764; /root.

Preserved Branch And Worktree: codex/store-agent-claim-state; /Users/martinbechard/.codex/worktrees/b146/dev-methodology.

Preserved Candidate Evidence: dev-methodology d2744c62281b5fc2bfdabd0d95a72642aab2924e; external mcp-agent-ops 660aef8be2cfc12926aef15c90250556760961a7; fresh independent review approval and verification PASS remain preserved.

Windows Evidence: Native CI run 31068038651 isolated the remaining failure to unlinking the locked empty legacy registry. No retirement implementation was applied; the fail-closed empty-and-locked boundary remains mandatory.

Preserved Provider And Claim History: Provider commits 9a90a1da487794e5619f8cac0d38f9c614959b8e, bf82de39b24ff1eb781859048e13b74070717590, b2d4ae3ece8fc7aff3035db73f2d892bad08bcef, b8f80c31eadeccbc140d40e2988d1ae2c8e6f76e, and 694f5e3c2bbc34b3dbee377c021d00e701a4679e; work-claim incarnations d7c4a99e-cc43-4f31-83f9-ee182252027b, 880f8773-f043-4592-83fc-4200652ba74d, 3bb4f520-7788-453d-9c57-6b08c8b5aed1, and 48b317e9-70f2-4dc8-9335-8c50fa9422f0; all prior dispatch and Running evidence remain history.

Next Action: Route the recorded approval through Ready -> Starting -> Running; do not perform outcome work before those transitions.

## User Action Required -> Ready Transition Evidence

Transition: User Action Required -> Ready.

Transitioned At: 2026-08-06T12:11:30Z.

Decision Owner: Parent Coordinator 019fb057-1767-7ef2-b5fa-41f4417b20b3.

Canonical Thread And Root Task: 019fd464-3875-75e2-aaa0-39a8e357d764; /root.

Decision Provenance: Direct user approval recorded in the canonical task conversation on 2026-08-06.

Next Action: Parent Coordinator may perform Ready -> Starting for the same canonical task after this provider commit is verified.

## Ready -> Starting Transition Evidence

Transition: Ready -> Starting.

Transitioned At: 2026-08-06T12:12:45Z.

Parent Coordination Thread: /root (thread 019fb057-1767-7ef2-b5fa-41f4417b20b3).

Launch Reservation: One distinct parent-owned launch reservation for this provider record.

Normalized Objective: Move agent claim state into the primary worktree's gitignored .codex/agent-claim directory.

Dispatch Time: 2026-08-06T12:12:45Z.

Intended Root Dev Orchestrator Role: Dev Orchestrator.

Canonical Runtime Evidence: None at reservation time. No runtime task has been created.

Current Launch Evidence: Parent Coordinator authorized this exact reservation; fresh exact provider path claim resume-starting-path-store-agent-claim-state-019fd464 acquired with outcome SHARED_CHECKOUT_ACQUIRED.

Required Next Lifecycle Transition: The canonical root Dev Orchestrator must separately accept Starting -> Running before repository mutation.

## Completion Evidence

Transition: Running -> Completed.

Disposition: READY.

Completion Selector: direct-main.

Completed At: 2026-08-06T13:23:19Z.

Canonical Thread And Root Agent Task: 019fd464-3875-75e2-aaa0-39a8e357d764; /root.

Accepted Dev Source Commit: 0648629ab96f12f79e43e966e3cdc6ef461d09c8.

Accepted External Source Commit: 89f2df0d80fc91f3944849b5387e4ac82ba79e40.

Integration Commit: 28aa154253a81fdb4d546faf054e1d63325462bf.

Integration Mapping: Current-main reconciliation proved content through d2744c62281b5fc2bfdabd0d95a72642aab2924e was already represented by 46b92c842693bb96b5e756632a8df35b241511bc and retargeted only 0648629ab96f12f79e43e966e3cdc6ef461d09c8 to the current renamed helper and focused test. The accepted source is non-ancestral, while helper blob afb34b0dc41e76899f3f41a6176fa139568e19a6 exactly matches the accepted source and the seven reviewed current-main adaptations are retained.

Main Observation: Integration commit 28aa154253a81fdb4d546faf054e1d63325462bf is an ancestor of current main 8dea65361e2dd476cb91ec574eed8bb776051520. Current main and origin/main were matched at 28aa before the unrelated current-main advance; the checkout was clean after integrated gates.

Independent Review: Fresh current-main review APPROVED with no findings.

Independent Verification: PASS.

Focused Integrated Checks: Eight tombstone and migration regressions passed; both changed Python files compiled; commit diff-check passed; the configured helper returned STATUS schema 2 at .codex/agent-claim.

Native Verification: External CI run 31103633065 and external-main CI run 31103775695 passed. Release workflow 31104384369 passed Windows and Python 3.11, 3.12, and 3.13 checks and published mcp-agent-ops v0.6.0 with wheel, runtime requirements, and SHA256SUMS at https://github.com/martinbechard/mcp-agent-ops/releases/tag/v0.6.0.

Preserved Approval And Safety Boundary: Direct user approval in canonical task 019fd464-3875-75e2-aaa0-39a8e357d764 authorized only the verified-empty, exclusively locked Windows legacy-registry tombstone operation. Migration remains fail-closed and nonmutating for live, extra-metadata, identity-mismatched, or contradictory state. Prior candidates d2744c62281b5fc2bfdabd0d95a72642aab2924e and 660aef8be2cfc12926aef15c90250556760961a7, and Windows run 31068038651, remain preserved history.

Delivery Claim Evidence: Integration path release 65e7a2b6-960e-405f-b8bc-6211ffd1c272; main resource release f79175a0-88a8-40ef-8825-00ee1252a9d7; work handoff release 2cd5d676-242b-4442-a6a9-5aa8cd80c736.

Archive Path: backlog/completed-backlog/features/store-agent-claim-state-in-gitignored-project-directory.md.

## Summary

Move the disposable agent-claim registry and event history out of the Git common directory into one shared, project-owned, gitignored runtime-state directory that ordinary Codex tasks can access without special `.git` permissions.

## Context

The current command helper stores `agent-claims.json` and `agent-claim-events/` under the Git common directory. In Codex worktrees this resolves to the primary repository's `.git` directory, which requires special permission even for a read-only status operation because the helper locks the registry file.

The claim registry and journal are disposable operational state, not Git metadata or durable project source. The repository already ignores `.codex/`, and target-project setup already owns creation of required operational ignore rules when agent-claim coordination is selected.

The preferred ownership split is:

- the claim helper resolves the primary worktree root and lazily creates `/.codex/agent-claim/` when claim state is first needed;
- project setup ensures the exact runtime-state directory is ignored when agent-claim is enabled;
- every linked worktree resolves the same primary-root directory rather than creating worktree-local registries;
- the legacy `.git` registry is migrated only at a safe empty-registry rollout boundary.

This avoids making project setup a runtime prerequisite for existing repositories while keeping ignore policy under project setup ownership.

## Source Evidence

Direct user request in the Dev Methodology dispatcher task on 2026-08-05: "I noticed that because the agent claim file was placed under the .git directory, it requires a special permission from Codex to access it. Also, this file is disposable. Could we not put this file in a separate gitignored folder? We just need to make sure we include this when creating the claim file. Or maybe we let the project setup agent create it and add it to git ignore. What's better? We'll need a workitem to do this change".

Repository evidence confirms that `skills/agent-claim-command/scripts/claim.py` derives the registry from `git rev-parse --git-common-dir`, `skills/agent-claim/SKILL.md` requires storage in the Git common directory, backlog reporting reads the same location, and the root `.gitignore` already ignores `.codex/`.

## Requirements

- Define one canonical operational state root at `<primary-worktree>/.codex/agent-claim/`.
- Store the live registry as `agent-claims.json` under that root and store `agent-claim-events/` beside it.
- Resolve the primary worktree root deterministically from Git worktree metadata. A helper invoked from the primary checkout or any linked worktree must resolve the same absolute state directory.
- Do not use the invoking linked worktree's `.codex` directory and do not fall back to per-worktree registries.
- Keep the existing exclusive lock-on-registry-file behavior and inode-preserving updates; moving the file must not introduce a separate lock file.
- Make the command helper lazily create the ignored state directory and registry so existing projects do not depend on rerunning project setup before the first claim operation.
- When agent-claim is selected during project setup, ensure the root `.gitignore` contains the exact anchored `/.codex/agent-claim/` rule. Do not require setup to commit an empty runtime directory.
- Keep `.codex/agent-claim/` disposable and excluded from project-files claims, Git delivery, generated source packages, and provider lifecycle evidence.
- Update backlog reporting and every claim transport to resolve the new state location consistently.
- Preserve command and MCP behavior parity. Update and release the external `mcp-agent-ops` implementation or shared claim runtime when its implementation does not consume the repository helper directly.
- Provide a safe legacy transition from `.git/agent-claims.json` and `.git/agent-claim-events/`. Do not migrate while the legacy registry contains a live claim. Preserve usable historical events when migration is performed.
- Reject or clearly diagnose a split-brain state in which both legacy and new locations contain live or contradictory claim state; do not silently choose one.
- Define a rollout boundary that prevents old and new helper versions from writing different registries concurrently. Refresh the configured command or MCP helper before enabling the new location.
- Remove the need for ordinary Codex permission escalation merely to read, acquire, heartbeat, release, reset, maintain, or report claims in an otherwise writable project.
- Update public documentation, generated skill mirrors, setup guidance, and focused tests from canonical sources.

## Acceptance Criteria

- From the primary checkout and two linked worktrees, claim status reports the same registry path under the primary root and the same live claim set.
- A normal Codex project permission profile can run status and claim mutations without special `.git` filesystem authorization.
- The claim helper creates the runtime directory and registry on first use when they are absent, and Git reports the directory contents as ignored.
- Project setup with agent-claim selected adds the exact ignore rule; setup with resource coordination disabled does not add claim-state configuration.
- The live registry, event history, and maintenance outputs are no longer written beneath `.git` after migration.
- A legacy empty registry and its event history migrate deterministically to the new location; a live or contradictory legacy state produces a structured non-mutating stop.
- Command and MCP fixtures resolve identical state paths and preserve all existing structured outcomes.
- Backlog reporting reads the new registry and continues to report claim ownership and timeline evidence correctly.
- No linked worktree creates a divergent local claim registry.
- Focused tests, skill validation, generated-output freshness, Git ignore checks, and repository diff validation pass.

## Dependencies

claim-work-items-by-id-and-record-lifecycle-events

## Blocked Evidence

Blocker: Work Item ID `claim-work-items-by-id-and-record-lifecycle-events` is currently Running and changes the same claim engine, command and MCP contracts, reporting behavior, coordination skills, and focused tests.

Blocker Owner: Dev Backlog Coordinator.

Exact Unblock Condition: `claim-work-items-by-id-and-record-lifecycle-events` reaches a terminal successful disposition on current main, its implementation and provider claims are released, the legacy claim registry contains no live claims, and the new item can reconcile from that delivered claim contract without concurrent edits.

Permitted Resumption Transition: Blocked -> Ready after the Coordinator validates the exact unblock condition.

## Recovery History

### Blocked -> Ready — 2026-08-05

The Dev Backlog Coordinator validated the recorded unblock condition. Dependency Work Item ID claim-work-items-by-id-and-record-lifecycle-events reached its successful provider closure at commit 5650b569d726044a5254e43f01ee233707279472. Its direct-main delivery commit fd9467f81f524a002a7e28663c9387965d068860 is an ancestor of current main. The configured claim helper reported an empty registry and no live claims before this transition.

## Verification

- Add focused command-helper tests covering primary and linked-worktree path resolution, lazy creation, ignore behavior, locking, and identical registry visibility.
- Add migration tests for absent state, empty legacy state, preserved event history, live legacy claims, contradictory dual state, and interrupted migration recovery.
- Add command/MCP parity fixtures for the resolved registry path and structured migration failures.
- Update focused backlog-report tests to use the new project-state location.
- Add focused project-configuration tests proving the ignore rule is added only when agent-claim is selected and is idempotent.
- Validate every changed skill package and regenerate only supported documentation and adapter outputs.
- Run Git ignore probes, Python compilation for changed helpers, focused claim/report/setup tests, and `git diff --check`.
- Obtain fresh independent review and verification, including a check that no ordinary operation still requires `.git` access.

## Open Questions

- Determine the smallest versioned rollout mechanism that prevents an older installed command or MCP helper from continuing to write the legacy registry after migration.
- Confirm whether `mcp-agent-ops` imports the repository claim runtime or requires a coordinated external implementation and wheel release.
- Decide whether legacy event archives are moved once or read from both locations during a bounded compatibility period; live registry state must never be dual-read or dual-written.

## Governed Definition Approval

### Governed Canonical Sources

- skills/agent-claim/SKILL.md
- skills/agent-claim-command/SKILL.md
- skills/agent-claim-mcp/SKILL.md
- skills/create-project-configuration/SKILL.md

### Allowed Dependent Artifacts

- skills/agent-claim-command/scripts/claim.py
- scripts/generate-backlog-report.py
- scripts/render-agents-technology-skills.py
- scripts/test_agent_claim.py
- scripts/test_agent_claim_transport.py
- scripts/test_generate_backlog_report.py
- scripts/test_bundle_content.py
- focused project-configuration tests and fixtures that consume the approved setup contract
- README.md
- .gitignore
- design/generated/skill-definitions.js
- generated adapters produced from the approved canonical skill sources
- the external `mcp-agent-ops` implementation and package release only where required for parity with the approved `agent-claim-mcp` contract

### Approval Resolution

Approved at creation. On 2026-08-05 the user directly requested a work item to move the disposable claim file out of `.git`, place it in a gitignored project folder, ensure the folder is included when claim state is created, and assign project setup responsibility for the ignore rule where appropriate. This approval covers exactly the four named skill-definition paths above and their listed dependent artifacts. It does not authorize conceptual agent-definition changes or unrelated project-setup, claim-scope, provider, or lifecycle behavior.

## Notes

- Use `/.codex/agent-claim/` rather than `.agents/`: `.agents/` contains deployed skill sources, while `.codex/agent-claim/` is explicitly disposable project-operational state.
- The helper owns lazy directory creation. Project setup owns the durable ignore rule. This keeps existing projects functional and new projects consistently configured.
- Do not migrate or reset the currently active registry merely to implement this feature.
