# Reconcile Project Terminology Reference Discovery

Status: User Action Required

Type: Defect

Provider: file

Work Item ID: reconcile-project-terminology-reference-discovery

Completion: main-branch

## Summary

Restore mcp-agent-ops discovery and publication verification through conventional project and
user reference roots that mirror skill discovery.

## Context

The configured reference provider successfully refreshes revision `89b418948b1bcfdc656fce1c2e50e8bc1fcc12126b6b1c21627e97d7d0e9c13c`, but its published names omit the tracked terminology reference. A revision-matched `reference_load` therefore returns `reference_not_found`. This is a valid ABSENT result for ordinary terminology application, but it cannot satisfy post-mutation publication verification because no returned digest can match the changed target.

The accepted design does not publish arbitrary files from the project root and does not
predefine allowed reference filenames. Like skill discovery, it authorizes conventional
locations and recursively discovers safe reference files beneath them. Project references
use `<project>/.agents/reference` and `<project>/.codex/reference`. User references use
`~/.agents/reference` and `~/.codex/reference`.

The preserved Work Item `replace-evaluation-oracle-terminology-with-judge` is Blocked with accepted candidate `6f8e617c2fdb36bac1dbb46a77410e384505437d` until this capability is restored.

## Requirements

- Reproduce refresh and revision-matched load from the configured dev-methodology project context.
- Add recursive project reference discovery beneath `<project>/.agents/reference` and
  `<project>/.codex/reference` when the active project is inside an authorized workspace.
- Add recursive user reference discovery beneath `~/.agents/reference` and
  `~/.codex/reference` through the supported user configuration and installation boundary.
- Use location-based authorization and safe relative names. Do not introduce a predefined
  reference-filename allowlist or recursively publish the project or user home root.
- Preserve project-before-user precedence and `.agents`-before-`.codex` precedence, matching
  the corresponding skill-discovery model.
- Place or project the maintained terminology reference into the appropriate conventional
  project reference root and keep one authoritative maintained source.
- Preserve configured user-reference roots, path-free scope labels, immutable snapshot behavior, allowed workspace boundaries, and `reference_not_found` semantics for genuinely absent references.
- Do not use filesystem fallback or arbitrary user-home search as publication proof.
- If mcp-agent-ops changes, verify and publish/install the supported package through its own repository and release workflow before project-runtime verification.
- Preserve the Oracle terminology candidate and do not reimplement its source changes.

## Acceptance Criteria

- `reference_refresh` recursively discovers safe UTF-8 references beneath project
  `.agents/reference` and `.codex/reference` roots and user `.agents/reference` and
  `.codex/reference` roots without a filename allowlist.
- `reference_refresh` in a fresh configured dev-methodology runtime publishes a revision whose names include `terminology.md`.
- Revision-matched `reference_load` returns the project reference scope and the validated SHA-256 digest of the maintained target without exposing a physical path.
- Genuine ABSENT behavior still returns only `reference_not_found` when neither configured project nor user scope contains the reference.
- Tests prove project-before-user and `.agents`-before-`.codex` ordering, recursive relative
  names, resolved-file deduplication, and the absence of arbitrary project-root publication.
- Workspace-root, aggregation, skipped-root, immutable-snapshot, symlink-containment, and path-redaction contracts remain intact.
- Focused Project Configurator and mcp-agent-ops reference discovery/publication tests pass.
- Fresh independent review and verification accept the correction and installed-runtime evidence.

## Dependencies

None.

## Verification

- Run focused reference refresh/load tests at the owning source boundary.
- Verify the configured project context and fresh-runtime catalog revision after any required publication/install/restart boundary.
- Confirm revision equality and target digest equality.
- Run applicable configuration rendering, typing, lint, package, and Git diff checks.
- Obtain independent source and runtime verification.

## Open Questions

- Which Persistence and Commit workflows should govern the required source work in
  `/Users/martinbechard/dev/mcp-agent-ops`? The pending A, B, or C delivery decision remains
  separate from the accepted reference-discovery design.

## Accepted Reference Discovery Design

User directive:

> ok that makes sense. let's add the reference directory at the project and user level under .agents/reference and .codex/reference like for skills.

Decision: discover references recursively from conventional `.agents/reference` and
`.codex/reference` locations at both project and user scope. Authorization is location-based;
individual reference filenames are not predefined. This decision supersedes the preserved
plan's proposed direct project-root `terminology.md` allowlist. The preserved plan must be
revised before implementation resumes.

## Notes

- This is the finish-lane recovery item for `replace-evaluation-oracle-terminology-with-judge`.
- Ordinary terminology application may continue with ABSENT status; mutation publication cannot.

## Starting Handoff Evidence

- Reserved At: 2026-08-13T13:54:14Z.
- Transition: `Ready -> Starting`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Baseline: `7322557a0e5841b2a432a6fdb1db7dc80feabf33` on primary `main`.
- Priority: Mandatory finish-lane recovery for the preserved Blocked Oracle terminology candidate.
- Capacity: Replaces the slot released by `replace-evaluation-oracle-terminology-with-judge` entering Blocked. Active usage remains four of five.
- Overlap: Diagnose before mutation. Do not touch Oracle candidate paths, active Project Configurator receipt files, provider-terminology paths, Index alignment paths, or unrelated plan artifacts. Any mcp-agent-ops source work must use its repository's own provider, claims, review, release, and publication boundary.
- Dispatch Architecture: Create one visible Codex task whose initial prompt launches one Dev Orchestrator subagent and states the visible root title-and-messaging responsibility.
- Transition Claims: Work Item `start-terminology-reference-discovery-work-item`; event `c3b646c6-3be4-4ad1-8d90-e94fba536ddf`. Provider `start-terminology-reference-discovery-provider`; event `cc4ae5c5-884c-4f05-ba21-3dfafa5e8929`.
- Runtime Identity: Pending caller-owned visible task creation. Creation does not imply Running.

## Canonical Runtime Assignment

- Assigned At: 2026-08-13T13:55:15Z.
- Codex Task ID: `019ffb67-9ecc-7c53-8412-c486d62d06c2`.
- Conversation ID: `019ffb67-9ecc-7c53-8412-c486d62d06c2`.
- Host: `local`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Requested Title: `Starting — Reconcile Project Terminology Reference Discovery`.
- Initial Action: The visible root starts one Dev Orchestrator subagent for this authoritative Work Item and owns required Codex title and subagent messaging.
- Creation Outcome: Unique direct `threadId` and host success in the saved dev-methodology project, with no client or pending identity and no retry.
- Lifecycle Boundary: This assignment remains `Starting` until the nested Dev Orchestrator accepts and records `Starting -> Running`.
- Adoption Claims: Work Item `adopt-terminology-reference-discovery-task`; event `18b6eb70-c19b-4dbe-99ac-37877f84e211`. Provider `adopt-terminology-reference-discovery-provider`; event `60cc1726-3cd2-4396-a536-74dc3d84d2c9`.

## Running Acceptance Evidence

- Accepted At: 2026-08-13T13:58:06Z.
- Transition: `Starting -> Running`.
- Root Owner: Dev Orchestrator `/root/reconcile_terminology/terminology_reference_orchestrator`.
- Canonical Codex Task ID: `019ffb67-9ecc-7c53-8412-c486d62d06c2`.
- Canonical Conversation ID: `019ffb67-9ecc-7c53-8412-c486d62d06c2`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Runtime Parent Delta: The nested Dev Orchestrator executes under canonical visible task `019ffb67-9ecc-7c53-8412-c486d62d06c2`; the durable upstream runtime parent remains `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Branch: `main`.
- Worktree: `/Users/martinbechard/dev/dev-methodology`.
- Baseline: `91337d5db54f533ea0867772b3b9567c7c3c3074`.
- Accepted Execution: The nested Dev Orchestrator loaded the configured workflow, Commit, Persistence, resource-coordination, repository-maintenance, and terminology skills; verified the canonical runtime identity, provider state, Git state, and claim state; and accepted the provider-scoped execution.
- Runtime Display Handoff: The visible root task owns the Codex conversation title change to `Running — Reconcile Project Terminology Reference Discovery` before implementation dispatch.
- Transition Claims: Work Item `run-reconcile-project-terminology-reference-discovery-work-item`; event `2603c20f-3c85-4163-8b01-64abe4574f21`. Provider `run-reconcile-project-terminology-reference-discovery-provider`; event `adeb5f98-c7fc-41bb-a416-79c233a7ac0d`.

## User Action Required

### Question for the User

Which Persistence and Commit workflows should govern the required source work in `/Users/martinbechard/dev/mcp-agent-ops`?

- **A — GitHub + feature branch (recommended):** Use the existing GitHub repository identity for durable work and deliver through an independently reviewed pull-request branch.
- **B — File + main branch:** Add project configuration and a repository file backlog, then deliver verified work directly to `main`.
- **C — None + main branch:** Keep only task-local work evidence and deliver verified work directly to `main`; this external repository will have no durable provider inventory for the repair.

The repository has a GitHub `origin`, a `.github` directory, no `PROJECT.yaml`, and no file backlog. No source mutation can begin until both selectors are explicit.

### Resolution

Pending the user's selection of A, B, or C.

## User-Decision Handoff

- Requested At: 2026-08-13T14:11:13Z.
- Transition: `Running -> User Action Required`.
- Preserved Plan: `reconcile-project-terminology-reference-discovery-plan-019ffb67.json` with synchronized sibling HTML.
- Source Mutation: None.
- External Repository State: `/Users/martinbechard/dev/mcp-agent-ops` is on `main`, has no `PROJECT.yaml`, and contains unrelated untracked files that must remain untouched.
- Canonical Task: Preserve Task/Conversation `019ffb67-9ecc-7c53-8412-c486d62d06c2`; it asks the question and adopts the answer.
- Resume Boundary: A clear A, B, or C answer is persisted here, then the same task performs `User Action Required -> Ready -> Starting -> Running`, configures or applies the selected workflows, reacquires claims, and continues. Ambiguous or expanded authority returns to the Coordinator.
- Transition Claims: Work Item `uar-terminology-reference-workflows-work-item`; event `22e3727b-b6f5-4666-b201-1d24617b94ef`. Provider `uar-terminology-reference-workflows-provider`; event `44a1d63f-7293-422a-a283-52ffa8f78c9b`.
