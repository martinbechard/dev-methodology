# Store Agent Claim State In Gitignored Project Directory

Status: Blocked

Owner: Unowned

Type: Feature

Provider: file

Work Item ID: store-agent-claim-state-in-gitignored-project-directory

Completion: direct-main

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
