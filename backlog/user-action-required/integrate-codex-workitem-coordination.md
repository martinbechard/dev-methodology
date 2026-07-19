# Integrate Codex Work-Item Coordination

Status: User Action Required

Type: Feature

## Summary

Promote the exercised Codex work-item coordination protocol into the supported bundle, add a parent backlog-agent conceptual role, route repository Codex coordination through the supported skill, and prove the complete lifecycle through generated adapters, evaluation, documentation, installation, and terminal evidence.

## Context

Commit 6f05441cce6d3c22614908fdc4fdbd54a110aee7 preserves a project-local codex-workitem-coordination skill on branch codex/codex-workitem-coordination-project-skill. That commit is not an ancestor of current main and must be reapplied against current sources rather than copied as an integration commit.

The protocol exercised on 2026-07-19 separates read-only preflight, brief primary-only lifecycle mutations, artifact work, waiting, resumption, review, verification, integration, and terminal lifecycle updates. Every evidence-bearing baton records the exact commit, claim release event, clean primary state, designated next owner, and precise next mutation. Waiting tasks stop without polling and resume only through the parent coordinator.

The dependency separate-project-and-backlog-claim-scopes completed and was archived at commit db82749e28b51f2cb9281e52b4d3ec587888e70a. The lifecycle HTML communication diagrams remain owned by the separate document-claims-and-worktrees-in-orchestrated-lifecycle item so this work does not create a duplicate explanation.

The repository requires explicit scope-specific user approval before any skill or conceptual agent definition mutation. The requested deliverable names the definitions to create, but the coordinating instruction also requires obtaining explicit definition approval rather than inferring it. No governed definition or generated mirror may change until the user answers the question below and the supported pre-mutation check accepts the recorded approval.

## Requirements

- Add the supported codex-workitem-coordination skill and aligned Codex metadata from the preserved project-local behavior, refined against current main.
- Make the primary-backlog baton explicit, including the current owner, designated next owner, lifecycle commit, release event, clean primary state, and precise next mutation.
- Define the exact phases READ-ONLY PREFLIGHT, LIFECYCLE START, ARTIFACT GO, ARTIFACT WAIT, and ARTIFACT RESUME.
- Refuse artifact orchestration from a mismatched isolated checkout while a primary-only backlog mutation is active or required.
- Require parent-mediated, non-polling wake chains whose resume evidence contains the exact accepted commit, release event, clean state, and next action.
- Serialize brief primary lifecycle mutations, release the backlog baton, and then permit concurrent non-overlapping artifact campaigns in canonical isolated worktrees.
- Apply adaptive dispatch backoff for shared generators, browsers and ports, verification resources, target-branch integration, and claim contention.
- Add the backlog-agent conceptual role as the Parent Backlog Coordinator. Keep queue ordering, task creation, parent ledger, baton designation, wake-ups, concurrency, and terminal reconciliation separate from Dev Backlog Steward backlog mutation and Dev Orchestrator single-item delivery ownership.
- Generate and inspect the Codex, Claude, Gemini, and Junie agent adapters and the generated skill, role, and manifest views from canonical sources.
- Add deterministic skill probes, workflow associations, a backlog-agent suite, and forward-test scenarios covering normal flow, PRIMARY_REQUIRED or WAIT, ARTIFACT WAIT and RESUME, serialized lifecycle starts, concurrent isolated lanes, bounded backoff, and truthful terminal state.
- Route the repository Codex coordination reference through the supported PROJECT.yaml and AGENTS.md rendering path rather than a divergent hand edit.
- Update README.md and the relevant design pages for the supported catalog, conceptual role boundary, adapter behavior, installation, and verification workflow.
- Hand the accepted skill and role contract to document-claims-and-worktrees-in-orchestrated-lifecycle for the integrated accessible communication sequence diagrams. Do not duplicate those diagrams in the skill documentation.
- Obtain fresh independent definition and documentation review, source review for scripts when changed, complete verification, deliberate main integration, and terminal backlog evidence.
- Run a Codex user-scope installation dry run, approved replacement, installed-source and manifest checks, and MCP skill refresh under a separate shared-install claim when distributable artifacts are accepted.
- Preserve commit 6f05441 as source evidence while integrating a clean contribution based on current main.

## Acceptance Criteria

- The supported catalog contains codex-workitem-coordination with aligned metadata and no competing project-local source-of-truth claim.
- The backlog-agent role has a distinct parent-queue responsibility and does not absorb Dev Backlog Steward, Dev Orchestrator, producer, reviewer, verifier, or merge-coordinator ownership.
- The five named phases, evidence-bearing baton, mismatched-checkout refusal, parent wake chain, serialized lifecycle mutation, concurrent isolated lanes, and adaptive resource backoff are explicit and covered by deterministic evaluation evidence.
- Generated adapters and catalog views match their approved canonical sources and pass freshness checks.
- PROJECT.yaml and generated AGENTS.md reference the supported Codex coordination route without embedding the full skill procedure.
- The lifecycle documentation item contains three verified accessible communication sequences: normal lifecycle, WAIT or PRIMARY_REQUIRED wake and baton resumption, and serialized backlog batons followed by concurrent artifact lanes.
- Independent review accepts the skill, role, routing, evaluations, documentation, and generated outputs with no unresolved material finding.
- Focused checks and the complete repository validation required by AGENTS.md pass after integration.
- The user-scope Codex installation and MCP refresh are verified from installed manifests and source digests, or the terminal record names the explicit authority blocker that prevented deployment.
- The final main commit is clean, every artifact, generator, browser, verification, integration, install, and lifecycle claim is released, and the completed item is archived with exact evidence.

## Dependencies

- separate-project-and-backlog-claim-scopes, completed at db82749e28b51f2cb9281e52b4d3ec587888e70a

## Verification

- Run the supported definition-change pre-mutation check separately for the skill definition, its metadata, and the backlog-agent conceptual definition using the recorded approval evidence.
- Validate canonical skills and metadata, then regenerate skill and role documentation plus all supported adapters from source.
- Add and run focused deterministic bundle tests and the backlog-agent forward-test suite, including negative cases for polling, status-only wake-ups, isolated backlog mutation, premature artifact dispatch, and unbounded contention retries.
- Run every skill, generated-output, hierarchy, support-checklist, repository unit, project-wiki unit, and diff check required by AGENTS.md.
- Independently review each contribution before verification and repeat fresh review plus complete verification after multi-contribution integration.
- Run documentation-page verification and browser verification for the lifecycle diagrams at narrow, standard, and desktop widths, light and dark presentation, keyboard navigation, zoom, readable labels, and accessible alternatives.
- Verify the Codex install dry run, installed skill and agent sources, ownership manifest, MCP skill refresh revision, and clean release of the shared-install claim.

## User Action Required

### Question for the User

Do you explicitly approve creating or changing these governed definitions for this work item: skills/codex-workitem-coordination/SKILL.md, skills/codex-workitem-coordination/agents/openai.yaml, and agents/roles/dev-activities/backlog-agent.role.yaml, together with regeneration of only their supported generated mirrors?

### Why User Input Is Required

AGENTS.md requires explicit scope-specific user approval before any distributed skill definition, skill metadata, or conceptual agent definition mutation. The coordinating instruction says not to infer that approval from the requested outcome.

### Options And Tradeoffs

- Approve the exact definition scope: move this item into the Agent Skill Lifecycle feature series as Ready, record the approval provenance, run the supported pre-mutation checks, and begin LIFECYCLE START under a new brief backlog claim.
- Narrow the scope: identify which named definitions are approved and leave the remaining definition work blocked.
- Defer: move the item to holding without starting artifact work.
- Decline: archive the feature as abandoned without changing governed definitions.

### Resolution

Pending.

### Unattended Work Boundary

Do not create or change the named skill definition, metadata, conceptual role, or their generated mirrors. Do not start artifact claims, integration, installation, or lifecycle-documentation implementation until an explicit answer is recorded and the item is moved through Ready to a separately claimed Running transition.

## Notes

- Keep design/orchestrated-development-lifecycle.html as the integrated communication-flow owner.
- Treat the preserved commit as source evidence, not as a safe current-main integration unit.
- Generated mirrors are regenerated through supported generators and are never edited directly.
