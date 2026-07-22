# Deploy Skills And Agents To An Explicit Project Folder

Status: Completed

Type: Feature

Provider: file

Provider Reference: backlog/completed-backlog/features/deploy-skills-and-agents-to-explicit-project-folder.md

Completion: direct-main

## Execution / Ownership

- Owner: Dev Orchestrator
- Canonical task: 019f8b05-525f-7b10-bb66-9c6a3abcbc47
- Claim: complete-deploy-explicit-project-019f8b05 (terminal provider transaction)
- Branch: codex/deploy-explicit-project-integration-20260722
- Canonical worktree: /Users/martinbechard/.codex/worktrees/16de/dev-methodology
- Phase: Completed through direct-main integration and provider archival.
- Starting main: af0a3fe63404a793f2bf7dcf40dd2a3de563109e
- Accepted candidate: 20894fa8d5e69fd643de7d37eb31b324a53228f6.
- Claim wait started at: None.
- Claim wait attempts: 0.
- Open issues: None for the accepted scope. A reviewed low-severity empty parent-directory residual for failed creation of a brand-new MCP config is outside the stale-target-only unblock scope and was not expanded into this item.
- Next owner: None.
- Delivery evidence: Accepted source 20894fa8d5e69fd643de7d37eb31b324a53228f6 mapped byte-for-byte to main integration tip fa10176f8df7f76231c0ac46524e17aff384fc50; details follow.

Creation Claim: create-explicit-project-deployment-item-20260721

## Cold-Start Recovery Execution — 2026-07-22

- Lifecycle transition: Blocked -> Ready after reconciliation confirmed the recorded fresh-owner exact correction condition was accepted for execution -> Running under fresh ownership.
- Canonical task identity: 019f8b05-525f-7b10-bb66-9c6a3abcbc47.
- Backlog recovery claim: cold-start-backlog-reconcile-2-019f8b00, acquired event 66822334-e85a-41aa-b2ad-6a6c433b6798 from primary main.
- Recovery phase: target-only noninteractive regression recovery.
- The blocker, exact unblock condition, candidate chain, review evidence, and verification evidence below remain preserved.

## Completion Evidence — 2026-07-22

- Completion disposition: READY under direct-main; lifecycle persisted as Completed by this provider transaction.
- Preserved original candidate chain: d38efccbb86791e28ebd4d4f3d7b2139a5d8eac0 to 3dfdb18c9cb3cc373c4057a75769ab784edf9a46 to fceeb9f206b868272bf034f29312f36163a5a895.
- Current-main replay chain: b34a5ad to cf01e62 to 5b256c6 to fdcee57 to 6be4bf5 to accepted source 20894fa8d5e69fd643de7d37eb31b324a53228f6.
- Accepted source branch and worktree: codex/deploy-explicit-project-resume-20260722 at /Users/martinbechard/.codex/worktrees/16de/dev-methodology; source worktree clean.
- Fresh source review reproduced the exact blocker and prescribed target-only server counting. The first post-change review rejected incomplete managed-field matching and non-transactional MCP writes. The second review rejected contradictory success output. Final fresh review of 20894fa8d5e69fd643de7d37eb31b324a53228f6 passed with no material findings and confirmed no governed definition mutation.
- Independent candidate verification: seven of seven exact stale-target, backup-conflict, injected-write rollback, and unrelated-server candidate tests passed; all 76 installer tests passed; installer help, Python compilation, and git diff checks passed.
- Tier 3 verification: Python 3.11 ran 585 scripts tests. Eight failures were reproduced identically on exported lifecycle-start baseline 5d6a2e60b8382888c5c53bc35bed686749d71912 and were classified as unrelated claim-fixture, runtime-suite inventory, documentation phrase, line-wrapping, and lifecycle wording drift.
- Integration claim: integrate-deploy-explicit-project-019f8b05 acquired on clean main 2fbab0c05f27505ac68f6c90e470d4611903b4a1, event 2dcae378-a1c6-4cbd-a17b-108c95d6b044, for README.md, scripts/install-skills.py, scripts/test_install-skills.py, and merge:integration:main.
- Reconciliation branch: codex/deploy-explicit-project-integration-20260722, created from exact current main 2fbab0c05f27505ac68f6c90e470d4611903b4a1.
- Integration mapping: the six selected commits were replayed with source hashes recorded; their three path contents were byte-identical to accepted source 20894fa8d5e69fd643de7d37eb31b324a53228f6. Main fast-forwarded to fa10176f8df7f76231c0ac46524e17aff384fc50, which contains the reconciliation tip as an ancestor.
- Post-integration verification on main: seven of seven focused tests passed, all 76 installer tests passed, installer help passed, git diff checks passed, and the main worktree was clean.
- Integration claim release: RELEASED at clean main fa10176f8df7f76231c0ac46524e17aff384fc50, event 759c1bfa-4b67-4662-89b9-e1365b6fbfc7.
- Remote publication: not required by this local direct-main completion; origin/main was not changed.
- Terminal provider claim: complete-deploy-explicit-project-019f8b05, acquired event 3977aa5b-b780-4606-90a2-0bbf0a8a466a for the active and completed provider paths; commit and release evidence are returned in the terminal handoff.

## Summary

Allow the skills and agents installer to accept an explicit project folder and deploy the selected adapter bundle there instead of using user-level destinations or requiring the caller to change the current working directory.

## Context

The installer currently supports user and project scopes. User scope derives destinations from the user home directory. Project scope derives skill, agent, MCP configuration, and workspace-root paths from the current working directory. The internal destination helper can already accept a project root, but the command-line interface does not expose that choice and other project-scoped path derivation still reads the current working directory directly.

This makes deployment to another project awkward and error-prone: callers must change directories before invoking the installer, and a partial implementation could send skills, agents, MCP configuration, ownership manifests, or allowed workspace roots to different projects.

The user directly requested a backlog item to let the skills and agents deployer specify a project folder instead of deploying at user level.

## Source Evidence

- scripts/install-skills.py defines user and project scopes, but project scope defaults to Path.cwd() at the command boundary.
- scripts/install-skills.py already has an internal project_root parameter in default_destinations, showing that explicit-root destination derivation is compatible with the current design.
- README.md documents project deployment only for the current project.
- scripts/test_install_skills.py covers project-scope deployment by mocking Path.cwd(), not by passing a project folder through the public command interface.

## Requirements

- Add an explicit project-folder command option for project-scoped skill and agent deployment. Prefer the name --project-root unless repository CLI conventions establish a clearer name during implementation.
- Require project scope when the explicit project folder is supplied, and reject combinations whose destination ownership would be ambiguous.
- Preserve current project-scope behavior when the option is omitted: the current working directory remains the project root.
- Resolve the selected project folder once and use that same canonical root for every project-scoped default.
- Derive adapter-specific skill and native-agent destinations beneath the selected project folder.
- Derive the scoped Codex or Junie MCP configuration path beneath the selected project folder when installer-managed MCP configuration is enabled.
- Use the selected project folder as the default MCP workspace root unless the caller supplies explicit workspace roots.
- Keep explicit skill, agent, and MCP configuration destinations authoritative where the existing command contract permits them, while retaining one unambiguous project identity for remaining scoped defaults.
- Apply the same selected project root to install, replace, cleanup, ownership-manifest, remove-owned, dry-run, and rollback behavior.
- Validate that the selected project root exists and is a directory before staging or mutating any destination.
- Do not fall back to user-level destinations when an explicit project root was requested or when its validation fails.
- Support every adapter whose project-scope destinations are currently supported.
- Update command help, README deployment examples, and directly related installer documentation so a caller can deploy to a different project without changing directories.
- Before changing any governed skill or agent definition discovered during implementation, identify the exact canonical paths and obtain separate scope-specific user approval. The backlog request itself does not authorize governed-definition mutation.

## Acceptance Criteria

- A caller can invoke the installer from the methodology repository, specify another existing project folder, and install both skills and native agents into that project's adapter-specific directories.
- The resulting MCP configuration, catalog paths, detection-registry path, and default allowed workspace root all refer to the selected project rather than the invocation directory or user home.
- The destination ownership manifests record the deployed artifacts under the selected project directories and retain the durable methodology source identity.
- Omitting the explicit project folder with project scope preserves current-working-directory behavior.
- Supplying the project folder with user scope, an invalid scope combination, a missing path, or a non-directory path fails before any destination or configuration is changed.
- Explicit destination overrides retain their documented precedence without causing the remaining generated paths to switch to another project root.
- Dry-run reports the same resolved project paths that a real deployment would use and performs no mutation.
- Refresh, cleanup, remove-owned, staging failure, and rollback operate only within the selected project and preserve unowned or customized content according to the existing installer contract.
- Focused tests cover Codex, Junie, Claude, Gemini, and generic adapter destination derivation where applicable, plus MCP configuration behavior for Codex and Junie.
- User-level deployment behavior remains unchanged.

## Dependencies

None.

## Verification

- Add command-parser and destination-resolution tests for an explicit absolute and relative project root.
- Add focused install and dry-run tests proving the invocation directory remains untouched while the selected project receives skills and agents.
- Add Codex and Junie tests for MCP configuration path, installed skill root, detection registry, and default workspace root under the selected project.
- Add rejection tests for user scope, missing paths, non-directory paths, and ambiguous explicit-destination combinations, asserting zero mutation.
- Re-run focused ownership, cleanup, remove-owned, staged transaction, and rollback tests against an explicit project root.
- Run the installer help and README content assertions affected by the new option.
- Run the applicable installer regression suite, Python compilation or static checks required by the repository, and git diff --check.
- Obtain an independent review of the command contract, path containment, rollback safety, documentation, and focused tests before direct-main completion.

## Notes

- This item exposes a project root through the public deployment interface; it does not change the adapter-specific directory names.
- This item does not make project deployment the default and does not authorize automatic deployment during ordinary repository maintenance.
- Project-scoped installation should remain an explicit caller action with a caller-supplied target.

## Historical Delivery Evidence Update — 2026-07-22

- Superseded by the Blocked Handoff below.
- Current phase: Candidate preserved; correction attempt 1 is active for review findings.
- Candidate commit: d38efccbb86791e28ebd4d4f3d7b2139a5d8eac0, preserved.
- Original artifact claim: Released.
- Verification: 66 of 66 installer tests passed; installer help, Python compilation, and git diff checks were clean.
- Deployment evidence: No real deployment was performed.
- Review findings: High — default-destination and MCP-path symlink escape; Medium — stale existing MCP split identity; Low — inaccurate --mcp-config help.
- Documentation finding: Workspace-root override replacement remains ambiguous.
- Correction lane: codex/deploy-explicit-project-correction-1-20260722 at /Users/martinbechard/dev/dev-methodology/.worktrees/deploy-explicit-project-correction-1-20260722 with scripts-only claim deploy-explicit-project-correction-1-20260722.
- README correction: Deferred behind project-skill-extensions-20260722.
- Claim wait started at: 2026-07-22T14:25:09Z.
- Claim wait attempts: 1.
- Exact conflict owner: project-skill-extensions-20260722 on README.md.
- Wait behavior: No polling; the correction lane continues on its proven non-overlapping scripts scope.
- Next owner: Dev Orchestrator.

## Blocked Handoff — 2026-07-22

- Canonical task: /root/process_backlog/orch_deploy_explicit_project.
- Candidate chain: d38efccbb86791e28ebd4d4f3d7b2139a5d8eac0 to 3dfdb18c9cb3cc373c4057a75769ab784edf9a46 to fceeb9f206b868272bf034f29312f36163a5a895.
- Original lane: codex/deploy-explicit-project-20260722 at /Users/martinbechard/dev/dev-methodology/.worktrees/deploy-explicit-project-20260722.
- Correction attempt 1 lane: codex/deploy-explicit-project-correction-1-20260722 at /Users/martinbechard/dev/dev-methodology/.worktrees/deploy-explicit-project-correction-1-20260722.
- Correction attempt 2 lane: codex/deploy-explicit-project-correction-2-20260722 at /Users/martinbechard/dev/dev-methodology/.worktrees/deploy-explicit-project-correction-2-20260722.
- Original claim release: deploy-explicit-project-20260722 released at d38efccbb86791e28ebd4d4f3d7b2139a5d8eac0, event 5ebf5833-8f0c-40d9-a990-ee6599a15de9.
- Correction attempt 1 claim release: deploy-explicit-project-correction-1-20260722 released at 3dfdb18c9cb3cc373c4057a75769ab784edf9a46, event 2aabb429-7d5a-4ee0-9241-af8f318c369c.
- Correction attempt 2 claim release: deploy-explicit-project-correction-2-20260722 released at fceeb9f206b868272bf034f29312f36163a5a895, event 3f5379a8-4cd2-429e-9d46-b5f0b125c33d.
- Final documentation review: PASS.
- Final verification: 72 of 72 installer tests passed; installer help, Python compilation, and git diff checks passed.
- Correction limit: The bounded two-attempt correction loop is exhausted.
- Integration authorization: None.
- Completion authorization: None.

### Exact Blocker

After correction attempt 2, fresh source review reproduced the medium same one-project-identity defect when stale mcp-agent-ops is the only configured server; configured_server_count includes it, so noninteractive Codex/Junie exits 0, leaves active config stale, writes candidate only, no backup; the suite misses the target-only case.

### Exact Unblock Condition

Fresh newly dispatched owner must add Codex+Junie target-only noninteractive regressions that require fail-before-mutation or deterministic active reconciliation consistent with acceptance criteria, correct behavior, fresh review and verification before integration.

### Recovery And Resumption

- Preserve the complete candidate chain, branches, worktrees, review findings, checks, and claim releases.
- Do not integrate, complete, or archive this item from the current evidence.
- Resume only through a new serialized backlog transaction after a fresh owner is dispatched and the exact unblock condition is accepted for execution.
