# Correct Resource-Claim Storage And Private Dispatcher Placement

Status: User Action Required

Type: Defect

Owner: Dev Orchestrator

Provider: file

Provider Reference: backlog/user-action-required/correct-resource-claim-storage-and-private-dispatcher-placement.md

Work Item ID: correct-resource-claim-storage-and-private-dispatcher-placement

Completion: main-branch

## Summary

Correct the resource-claim state location and configured MCP helper contract, move the Backlog Dispatcher skill from the distributable catalog into the project's private skill overlay, and publish only the portable repaired methodology and MCP artifacts before a required Codex restart and post-restart reconciliation.

## Context

The user identified the current primary-worktree `.codex/agent-claim` storage as an incorrect migration target and ordered SOLO operation until the claim system is corrected. The user also identified `skills/backlog-dispatcher` as an incorrectly distributed skill: mcp-agent-ops discovers project-private overlays under `.agents/skills` and `.codex/skills`, while `skill_load` does not resolve the committed distributed location. The current project must use the mcp-agent-ops Resource Claim Helper after the storage/configuration repair.

An interrupted pre-crisis execution left an uncommitted candidate in the primary checkout. Its in-scope paths are `AGENTS.md`, `PROJECT.yaml`, `design/generated/skill-definitions.js`, `scripts/test_bundle_content.py`, `scripts/test_resource_claim_helper.py`, `skills/resource-claim-helper-mcp/SKILL.md`, and the two untracked review artifacts beside that skill. The canonical repair must inspect and adopt valid candidate bytes instead of duplicating or discarding them. `scripts/test_audit_worktree_completion_links.py` and every other unrelated change are outside this Work item and must remain untouched.

The governing design authority is the complete `design/orchestrated-development-lifecycle.html` plus the documents under `design/agents/`. It assigns configuration selection to `PROJECT.yaml`, generated root guidance to the configurator workflow, project-private extensions to the project overlay, and global publication only to portable distributable skills and Agents.

## Source Evidence

- On 2026-08-12, the user explicitly authorized one destructive MCP claim-registry reset after preservation of audit history, authorized implementation and later publication, and required a fresh Codex restart before any later dispatch.
- The reset journal event `ec7b7de3-5164-412d-ae10-09ae16596730` records outcome `RESET`, a valid previous registry, and four removed live claims at `2026-08-12T11:30:13.425515Z`; the live registry then contains no claims and the prior journal remains present.
- Commit `710d9ed5` introduced the distributed `skills/backlog-dispatcher` placement; the current mcp-agent-ops overlay contract does not discover that location as a project-private skill.
- The external `/Users/martinbechard/dev/mcp-agent-ops` source currently selects `.codex/agent-claim` as claim state storage and must be corrected as part of the same end-to-end contract.

## Requirements

- Determine and implement the correct repository-associated, permission-safe resource-claim state location from the governing design and user direction; do not preserve `.codex/agent-claim` merely because it is the current implementation.
- Correct the mcp-agent-ops claim implementation, focused tests, migration behavior, and package/release metadata needed to support the chosen location without losing preserved audit evidence.
- Correct the canonical portable MCP claim-helper skill contract and regenerate its governed projections.
- Configure this project through `PROJECT.yaml` to select the verified mcp-agent-ops helper, then regenerate `AGENTS.md` and any runtime bridge through the owning configurator workflow.
- Move Backlog Dispatcher into `.agents/skills/backlog-dispatcher` as a project-private skill and remove it from the distributable skill catalog, generated distributable projections, README/catalog claims, and installer inputs.
- Update canonical coordination sources, design documentation, generated adapters, and focused tests needed to keep the private placement and caller-only runtime boundary consistent.
- Inspect the existing dirty candidate path by path, retain valid work and evidence, correct invalid assumptions, and commit only Work-item scope.
- Preserve `scripts/test_audit_worktree_completion_links.py`, all unrelated dirty state, the pre-reset claim files, and the complete claim audit journal.
- Perform all repair work without acquiring, reading, extending, heartbeating, releasing, reporting, maintaining, or resetting claims; the crisis reset has already occurred exactly once.
- Obtain fresh-context independent review and verification for both repositories and the installed runtime boundary.
- Publish or install only portable distributable skills, Agents, and the corrected mcp-agent-ops package/runtime. Keep Backlog Dispatcher project-private.
- After local delivery and publication, stop and require the user to restart Codex. Resume this same canonical execution after restart for runtime verification and crisis-exit reconciliation; do not dispatch any other work first.

## Acceptance Criteria

- mcp-agent-ops no longer writes live claim state to the rejected primary-worktree `.codex/agent-claim` location, and focused migration, permission, audit-retention, and all claim-operation tests pass.
- Preserved audit history remains readable and no second reset event is created.
- `PROJECT.yaml` selects the mcp-agent-ops claim helper, generated `AGENTS.md` names only the verified MCP helper, and generated-root freshness checks pass.
- `mcp-agent-ops skill_load` resolves the project-private Backlog Dispatcher from `.agents/skills/backlog-dispatcher` in a fresh runtime, while the distributable catalog and user installation do not publish that private skill.
- Current maintained design, role, skill, README, generated projection, installer, and test references accurately distinguish private placement from portable publication.
- The pre-existing in-scope dirty candidate is explicitly reconciled; unrelated dirty files are byte-preserved and excluded from every repair commit.
- Fresh independent reviewers accept the resource-storage design, prompt/skill boundaries, security implications, generated outputs, and cross-repository changes.
- Focused and proportionate tests pass in both repositories, including configuration generation, bundle content, skill discovery, package/install, and claim state migration.
- Corrected portable artifacts are published or installed and their installed bytes or version are verified before the restart request.
- After the user confirms a fresh Codex restart, the same canonical execution verifies MCP startup, project-private skill discovery, and a safe claim lifecycle in the corrected storage, then supplies crisis-exit evidence. MULTITASK remains disabled until that verification is accepted.

## Dependencies

- The one authorized claim-registry reset must be durably evidenced before implementation begins. Satisfied by journal event `ec7b7de3-5164-412d-ae10-09ae16596730`.
- The external mcp-agent-ops repository at `/Users/martinbechard/dev/mcp-agent-ops` is an explicit cross-repository delivery boundary of this Work item.
- A user-performed Codex restart is required after corrected local publication and before final runtime verification.

## Verification

- Confirm the reset journal has exactly one crisis-entry reset event for this epoch, its prior registry was valid, four claims were removed, the live registry is empty, and earlier journal entries remain.
- Run focused mcp-agent-ops unit and integration coverage for storage resolution, migration, permissions, audit preservation, all Resource Claim Helper operations, overlay discovery, package construction, and installed-server startup.
- Run the project configurator and generated-output freshness checks; verify `PROJECT.yaml`, `AGENTS.md`, runtime bridges, bundles, catalogs, role adapters, and README projections against canonical sources.
- Run focused tests for `resource-claim-helper-mcp`, Backlog Dispatcher private discovery, bundle exclusion, and preservation of unrelated dirty files.
- Obtain fresh-context methodology, code, prompt/security, artifact, and final verification results. Treat any material finding as non-terminal.
- After user restart, invoke only bounded non-destructive runtime checks needed to prove MCP startup and project-private discovery, then exercise and release a disposable corrected-location claim before recommending crisis exit.

## Open Questions

None.

## Crisis Recovery Evidence

- Crisis Epoch: `claim-coordination-repair-2026-08-12T11:30:13Z`.
- Trigger: user-declared resource-claim storage/configuration blockage with explicit instruction to serialize all delivery until repair, publication, restart, and reconciliation.
- Coordinator Task: Backlog Dispatcher `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`; canonical Dev Backlog Coordinator subtask `/root/backlog_coordinator`.
- Entry Inventory: Ready 12; Starting 0; Running 0; Stalled 0; Blocked 3; User Action Required 2; Future Ideas excluded.
- Crisis Set: this Work item only. Other provider items and all unrelated mutators remain preserved and undispatched.
- Dispatch Mode: SOLO; ordinary parallel dispatch capacity is zero. Exactly one separate canonical repair execution may run without claims.
- Pre-Reset Live Claims: four, owned by the interrupted root task `019ff3bd-87fa-72d2-a55a-ae25cf5397a4`; their identities, scopes, baselines, and audit events remain in the journal.
- Reset: exactly one MCP `claim_reset` call; journal event `ec7b7de3-5164-412d-ae10-09ae16596730`; outcome `RESET`; removed claim count 4; previous registry valid; live registry empty.
- Claim Suspension: every claim operation is prohibited until the post-fix restart verification completes and the crisis exit is accepted.
- Exit Gate: accepted cross-repository delivery and publication, user-confirmed fresh Codex restart, corrected MCP/helper and private-skill runtime verification, no unresolved crisis item, and explicit Coordinator reconciliation before MULTITASK is restored.

## Notes

- Creation authority is the user's explicit repair and publication request. Unique atomic file-provider creation is claim-free, and crisis recovery prohibits operational claim use.
- Historical completed Work items remain historical evidence and are not reopened or rewritten to represent this repair.
- The canonical execution must use the dirty primary checkout to adopt the preserved candidate. It must not manufacture a clean replacement that strands or erases those bytes.

## Current Starting Reservation

- Parent Coordination Task: Backlog Dispatcher `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Reservation: one crisis-authorized Ready -> Starting reservation for the only separate canonical repair execution.
- Normalized Objective: correct resource-claim storage and private Backlog Dispatcher placement, reconcile the preserved candidate, deliver both repositories, publish only portable artifacts, and stop for a fresh Codex restart before post-restart verification.
- Intended Root Role: Dev Orchestrator.
- Provider Identity: file; Work Item ID `correct-resource-claim-storage-and-private-dispatcher-placement`; Provider Reference `backlog/defect-backlog/correct-resource-claim-storage-and-private-dispatcher-placement.md`.
- Persistence And Completion: file provider; main-branch completion.
- Baseline Before Reservation: `050b92036496557016c64d25bbd494980c21a25f` on primary `main`.
- Checkout: primary `/Users/martinbechard/dev/dev-methodology`, required to adopt the preserved dirty candidate; external boundary `/Users/martinbechard/dev/mcp-agent-ops`.
- Reserved At: 2026-08-12T11:32:02Z.
- Canonical Codex Task ID: `019ff5c1-05a2-7551-bcf2-812f61776a7e`; host `local`.
- Canonical Conversation ID: `019ff5c1-05a2-7551-bcf2-812f61776a7e`; this runtime returned one combined task/thread identity.
- Runtime Creation Evidence: caller-owned launch succeeded directly in the saved dev-methodology primary checkout at 2026-08-12T11:35:16Z; no duplicate execution and no claim call occurred.
- Conversation Title: `Starting — Correct Resource Claims and Private Dispatcher`; synchronized with the durable Starting lifecycle at launch. The title remains display evidence only.
- Resource Coordination: no claim. Crisis epoch `claim-coordination-repair-2026-08-12T11:30:13Z` prohibits all claim operations after the one reset.
- Next Lifecycle Owner: the newly created root Dev Orchestrator must use this same provider item and directly record Starting -> Running before artifact mutation. No second execution or concurrent dispatch is authorized.

## Running Acceptance Evidence

- Accepted At: 2026-08-12T11:35:54Z.
- Canonical Codex Task ID: `019ff5c1-05a2-7551-bcf2-812f61776a7e`.
- Canonical Conversation ID: `019ff5c1-05a2-7551-bcf2-812f61776a7e`.
- Root Agent Task: `/root`.
- Owner: Dev Orchestrator.
- Phase: governing-contract and preserved-candidate reconciliation before implementation.
- Checkout: primary `/Users/martinbechard/dev/dev-methodology`; external delivery boundary `/Users/martinbechard/dev/mcp-agent-ops`.
- Resource Coordination: claim-free under crisis epoch `claim-coordination-repair-2026-08-12T11:30:13Z`; no claim operation occurred during acceptance.
- Conversation Title: `Implementing — Correct Resource Claims and Private Dispatcher`.

## Storage Boundary Correction

- Corrected At: 2026-08-12T11:49:00Z.
- Decision Owner: Dev Backlog Coordinator for crisis epoch `claim-coordination-repair-2026-08-12T11:30:13Z`.
- Canonical Root: `<primary-worktree>/.agent-ops/resource-claim/`, resolved identically from primary and linked worktrees.
- Ignore Rule: exact anchored `/.agent-ops/resource-claim/`, added when resource-claim is selected.
- Rejected Roots: `<git-common-dir>/agent-claim/` because Git-metadata access recreates the permission defect; `<primary-worktree>/.codex/agent-claim/` because the user superseded the harness-owned location; `.worktrees` because it owns linked checkouts and cleanup.
- Migration: move the empty live registry and preserved audit journal from `.codex/agent-claim` atomically and fail closed; never dual-write or mutate contradictory or live legacy state.
- Verification Addition: exercise every helper operation with `.git` and `.codex` denied while the primary-worktree operational root remains writable.
- Phase: resumed implementation under this corrected boundary, claim-free throughout the active crisis.

## Publication Phase Evidence

- Entered At: 2026-08-12.
- Phase: publishing accepted cross-repository candidates `4ea18ea7` and `ca69c6fe`.
- Accepted dev-methodology Candidate: `4ea18ea743bb86f548e1eb849485db2dffc9ce13`.
- Accepted mcp-agent-ops Candidate: `ca69c6fe901c4d24da546bbad846699791a5f2fe`.
- Review Disposition: GOOD; no prior finding survives.
- Conversation Title: `Publishing — Correct Resource Claims and Private Dispatcher`.
- Resource Coordination: claim-free under the active crisis; publication and installation must not invoke any claim operation.

## Windows Publication Correction

- Phase: publication correction — Windows fresh barrier contract.
- Trigger: exact-head CI run `31598572186` rejected a fresh directory barrier because one compatibility assertion selected barrier form only from `os.name`.
- Authoritative Fresh Contract: every platform installs a directory barrier at `.codex/agent-claim/agent-claims.json` containing the exact `state.json` registry-marker payload; the legacy event path is an exact regular-file barrier.
- Authoritative Legacy Contract: migration of an existing empty legacy registry retains a same-inode regular-file tombstone on Windows; POSIX may replace it with the directory barrier.
- Candidate Under Correction: mcp-agent-ops `ca69c6fe901c4d24da546bbad846699791a5f2fe`; this commit must not receive tag `v0.12.0`.
- Conversation Title: `Correcting — Windows Resource Claim Barrier`.
- Resource Coordination: claim-free under the active crisis; no claim operation is authorized during correction.

## Corrected Publication Candidate

- Accepted mcp-agent-ops Candidate: `c22fc9362cb46c44948d25da7771c72dfecbb28b`.
- Correction Review: GOOD; no findings.
- Local Gate: 168 passed, 1 configured-source skip; Ruff, mypy, compilation, and diff checks passed; worktree clean.
- Exact-Head CI: successful run `31599149795`, including Python 3.11, 3.12, 3.13, and native Windows verification.
- CI URL: `https://github.com/martinbechard/mcp-agent-ops/actions/runs/31599149795`.
- Phase: publishing accepted cross-repository candidates with corrected external tip `c22fc93`.
- Conversation Title: `Publishing — Correct Resource Claims and Private Dispatcher`.

## Publication And Pre-Restart Evidence

- Published mcp-agent-ops Commit: `c22fc9362cb46c44948d25da7771c72dfecbb28b`.
- Main CI: successful exact-head run `https://github.com/martinbechard/mcp-agent-ops/actions/runs/31599149795`, including Python 3.11, 3.12, 3.13, and Windows.
- Release: `https://github.com/martinbechard/mcp-agent-ops/releases/tag/v0.12.0`.
- Release Workflow: `https://github.com/martinbechard/mcp-agent-ops/actions/runs/31599288583`; successful verification, Windows, build, and publish jobs.
- Release Assets: `mcp_agent_ops-0.12.0-py3-none-any.whl`, `runtime-requirements.txt`, and `SHA256SUMS`.
- Wheel SHA-256: `7542132b3f4063e025302d525c4428d7d2c90377eab5682a2366750ee46e7f00`; downloaded assets passed `SHA256SUMS` verification.
- Installed Runtime: mcp-agent-ops `0.12.0`; runtime digest `11529a24781de540bac489710ba39272dfc4d45a7a9ceda2ee0062b691eac2bc`.
- Portable Publication: dev-methodology `main` published through `fb6d5e4b21a5f6c8c97479a59a64860bb49214fc`; accepted source candidate `4ea18ea743bb86f548e1eb849485db2dffc9ce13` remains its implementation ancestor.
- Installation: Codex user-scope portable skills and generated agents installed with replacement; MCP candidate inspected and activated through the installer's interactive acceptance path; prior config saved at `/Users/martinbechard/.codex/config.toml.bak`.
- Installed Byte Evidence: `resource-claim`, `resource-claim-helper`, `resource-claim-helper-mcp`, `coordinate-codex-tasks`, `dev-backlog-coordinator`, and `dev-orchestrator` match their published source bytes.
- Installed Manifests: 146 portable skills and 33 generated agents; neither manifest contains `backlog-dispatcher`.
- Private Dispatcher: absent from installed user skills and distributable `skills/`; retained only at `.agents/skills/backlog-dispatcher` and discovered from the project overlay.
- Non-Claim MCP Catalog: `skill_refresh`, `skill_list`, and `skill_load` succeeded at revision `2ce5a06a1a9d1eba511d8beaa4b1b3e5a50249ae73b4b1de631408deb91d6cd8` for the private dispatcher and portable claim skills.
- Catalog Digests: backlog-dispatcher `75ac03f54ce8c89d436159182fc89a8a5863715045a276287c4deffb79086919`; resource-claim `f16aca5f649de818c51073779df1d64d3215e8a5fc9cfee69318e4631cb9cbdc`; resource-claim-helper `d8431e082964173a1087916b8b5e6cbaf1071b714f3122b387fa1a4d9dd7428b`; resource-claim-helper-mcp `dc0803a1e2adc075ee1d08f5ab2c5a3ad724fd7d567bbabd978bbd94fb56c8a0`; coordinate-codex-tasks `e1cdab99cf994ef91b326c126babab3dc455e7683217cb19ee97bce38c64dbaf`.
- Claim Suspension: no claim operation occurred during correction, release, installation, or pre-restart verification.

## User Action Required

- Transitioned At: 2026-08-12.
- Exact User Action: Restart Codex now so it starts mcp-agent-ops 0.12.0 and reloads the corrected project/private catalog, then reply in this same conversation that the restart is complete.
- Conversation Title: `User Action Required — Restart Codex for Corrected Resource Claims`.
- Resume Boundary: after user confirmation, this same canonical execution performs bounded post-restart MCP startup, private-dispatcher discovery, and disposable corrected-storage acquire/release verification before crisis-exit reconciliation.
- Prohibited Before Confirmation: claim operations, post-restart verification, crisis exit, MULTITASK restoration, completion, and cleanup.
