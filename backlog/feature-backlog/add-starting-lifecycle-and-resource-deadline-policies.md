# Add Starting Lifecycle And Resource Deadline Policies

Status: Running

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/add-starting-lifecycle-and-resource-deadline-policies.md

Completion: direct-main

## Execution / Ownership

- Owner: Dev Orchestrator.
- Canonical thread: 019f8b51-f8ed-7c03-8193-9bbee1ccb7f2.
- Claim: approve-starting-lifecycle-deadline-scope-019f8b51, backlog transition only.
- Canonical worktree: /Users/martinbechard/.codex/worktrees/81ba/dev-methodology, clean and detached.
- Branch: Pending task-owned branch creation after LIFECYCLE START.
- Starting main: 2ba5dbd772ab80ad87f6db9c7ea4683488a823cf.
- Phase: current-main refresh, task-owned branch creation, path-by-path pre-mutation checks, then implementation.
- Lifecycle transition: User Action Required -> Ready after exact approval reconciliation -> Running under existing canonical Dev Orchestrator ownership.
- Accepted candidate: Pending.
- Integration wait started at: None.
- Integration wait attempts: 0.
- Completion wait started at: None.
- Completion wait attempts: 0.
- Open issues: Approved implementation, review, and verification within the exact ten-path scope.
- Next owner: Dev Orchestrator.

## Running Dispatch Evidence — 2026-07-22

- Backlog transition claim: start-starting-lifecycle-resource-deadlines-019f8b51, acquired event d4fca16b-0c33-410d-bdbf-8e382d3f9f54 from primary main.
- The full user-approved lifecycle, deadline, watchdog, terminology, and lifecycle-HTML behavior remains authoritative below.

## Discovery And Approval Gate — 2026-07-22

- Reconciled primary main at d1a3b768fc79a6d4f6ede4736229b12aa4c28562 and the live claim registry before this handoff; no active claim remained from the prior startup transition.
- Bounded discovery determined the smallest exact governed canonical definition manifest required for this outcome:
  - skills/agent-claim/SKILL.md
  - skills/agent-claim-command/SKILL.md
  - skills/agent-claim-mcp/SKILL.md
  - skills/codex-workitem-coordination/SKILL.md
  - skills/manage-file-work-items/SKILL.md
  - skills/create-project-configuration/SKILL.md
  - agents/roles/dev-activities/dev-backlog-coordinator.role.yaml
  - agents/roles/dev-activities/dev-orchestrator.role.yaml
  - agents/roles/dev-activities/dev-backlog-steward.role.yaml
  - agents/roles/project-setup/project-configurator.role.yaml
- Supported generated mirrors are limited to generated/adapters/** outputs derived from those approved role or skill sources, design/generated/role-definitions.js, and design/generated/skill-definitions.js.
- Ordinary companion scope, not governed-definition approval: PROJECT.yaml; AGENTS.md; README.md; skills/development-methodology/assets/templates/project-template.yaml; skills/agent-claim-command/scripts/claim.py; scripts/render-agents-technology-skills.py; focused claim, transport, work-item lifecycle, watchdog, renderer/configuration, bundle, and lifecycle-documentation tests; design/orchestrated-development-lifecycle.html; and design/agentic-configuration.html only if source-backed configuration explanation is required.
- Discovery rationale: codex-workitem-coordination owns Ready/Starting dispatch, capacity, duplicate-start reconciliation, and read-only watchdog; manage-file-work-items owns the file-provider Starting state and atomic transitions/recovery; agent-claim owns transport-neutral hard-stop, extension, heartbeat, overdue, no-auto-release, and cleanup-grace semantics; command and MCP adapter definitions own the two invocation envelopes; create-project-configuration owns project policy/default/override validation; the three dev roles own parent dispatch, root work-item-thread orchestration, and steward lifecycle boundaries; project-configurator owns persisted policy setup.
- Excluded governed sources: create-file-work-item because creation still terminates at Ready; completion skills because delivery semantics remain unchanged; role schema/model profiles and OpenAI metadata because no schema, model, name, activation description, or tool dependency needs to change.
- Resolution: Approved on 2026-07-22. The user answered "ok approved" in canonical work-item thread 019f8b51-f8ed-7c03-8193-9bbee1ccb7f2 directly in response to the exact ten-path approval question. No other governed source is approved.
- Why user input is required: repository policy requires exact scope-specific user approval before any skill or role definition mutation.
- Unattended work boundary: mutate only the exact ten approved governed sources and recorded dependent scope after path-by-path pre-mutation checks. Do not widen the approval.

## Approval Resolution — 2026-07-22

- Answer: Approved.
- User wording: "ok approved".
- Provenance: canonical work-item thread 019f8b51-f8ed-7c03-8193-9bbee1ccb7f2, directly responding to the exact ten-path question.
- Approved governed canonical sources, exactly:
  - skills/agent-claim/SKILL.md
  - skills/agent-claim-command/SKILL.md
  - skills/agent-claim-mcp/SKILL.md
  - skills/codex-workitem-coordination/SKILL.md
  - skills/manage-file-work-items/SKILL.md
  - skills/create-project-configuration/SKILL.md
  - agents/roles/dev-activities/dev-backlog-coordinator.role.yaml
  - agents/roles/dev-activities/dev-orchestrator.role.yaml
  - agents/roles/dev-activities/dev-backlog-steward.role.yaml
  - agents/roles/project-setup/project-configurator.role.yaml
- Approved dependent scope: only the supported generated mirrors and ordinary companions recorded in Discovery And Approval Gate.
- Exclusion: no other governed source is approved.
- Resumption claim: approve-starting-lifecycle-deadline-scope-019f8b51, acquired event 54a48623-5ad9-4cef-8e21-8cf1e98fac75 from primary main.
- The original discovery starting main d1a3b768fc79a6d4f6ede4736229b12aa4c28562 remains preserved above; current execution starts from refreshed main 2ba5dbd772ab80ad87f6db9c7ea4683488a823cf.

## User Action Required

Do you approve changing exactly the ten governed canonical definition paths listed in this item to add the Starting lifecycle bridge, mechanical read-only watchdog rules, project-configured resource deadline and cleanup-grace policy, and the required Work item, Thread, Agent, Role, Task, and Handoff ownership distinctions, together with only the listed supported generated mirrors and ordinary companion implementation, tests, and documentation? No other governed definition will change without separate approval.

## Summary

Add an explicit Starting lifecycle bridge, bounded resource-operation deadline policy, and read-only watchdog behavior so multi-item task startup, ownership, recovery, capacity, and resource cleanup are mechanically observable without inferring delivery readiness.

## Context

Asynchronous user-visible task creation needs a durable bridge between a parent coordinator selecting a Ready item and the per-item Dev Orchestrator accepting delivery ownership. Resource coordination also needs project-configured hard stops and cleanup-grace semantics that distinguish liveness from authorization to continue.

The work must preserve the separation between parent coordination, per-item delivery, backlog lifecycle mutation, and selected resource-coordination policy. A watchdog may surface unhealthy state but must not decide whether delivery is integrated, accepted, or ready for terminal completion.

## Source Evidence

- Direct user direction in parent expert task 019f77f4-c4bd-7c91-b197-c987a7beb838 on 2026-07-22 authorized this enhancement and sensible initial defaults with later project optimization.
- On 2026-07-22, the user added required lifecycle HTML documentation, role and execution-context terminology, and focused documentation verification to this same enhancement.
- Current core-only work-item routing and resource-coordination items supply related binding and lifecycle evidence; they do not replace this distinct starting, watchdog, and deadline outcome.

## Requirements

- Add a Starting lifecycle bridge for asynchronous task creation. The parent coordinator owns Ready -> Starting and records dispatch or reservation evidence; Starting counts against capacity.
- Require the per-item Codex task root agent to operate as Dev Orchestrator, accept ownership, and use its internal Dev Backlog Steward child for Starting -> Running with canonical task id, branch, worktree, and claim evidence.
- On failed or ambiguous startup, restore Ready when no ownership was accepted, or truthfully record Blocked or User Action Required when evidence requires it. Do not create duplicate tasks.
- Define root Dev Orchestrator ownership for each user-visible task. Dev Coder, reviewer, verifier, and steward roles are children. The per-item orchestrator owns delivery, integration, and terminal work-item transaction; its Steward atomically marks Completed and moves the archive. The parent owns task cleanup, recount, and replacement dispatch, not per-item completion.
- Add a mechanical read-only watchdog. Each cycle immediately alerts on a stopped, failed, or missing canonical task while an item is Starting or Running; a stopped task that retains a live coordination entry; or a terminal item that retains one. No extra grace timeout applies beyond the detection interval.
- Keep active quiet tasks healthy unless an explicit deadline or hard stop applies. The watchdog must emit evidence and advice only; the coordinator diagnoses branch, worktree, commits, processes, and claims, then chooses replacement, Blocked, User Action Required, terminal reconciliation, or failure.
- Prohibit watchdog semantic inference of integration readiness, accepted delivery, or completion readiness, and prohibit watchdog mutation of backlog, claims, or task state.
- Add project-configured maximum duration and cleanup grace for each named resource class or id. Acquisition records expected duration, requested hard stop, configured maximum, expected release, and cleanup grace. Validate expected duration <= requested hard stop <= configured maximum.
- Treat heartbeat only as liveness. It must never extend a hard stop. Allow explicit evidence-backed extensions only within the configured maximum. Overdue resources never auto-release; a stopped owner is immediately actionable.
- Provide initial methodology defaults subject to later measured optimization: short backlog mutation maximum 10 minutes with 2-minute cleanup grace; main integration 45 minutes with 10-minute cleanup grace; browser or server 60 minutes with 10-minute cleanup grace; database or port 30 minutes with 5-minute cleanup grace; long live or model evaluation 4 hours with 30-minute cleanup grace.
- Keep Starting and Running items in active typed folders with canonical task ids. Replacement orchestrators recover from durable branch, commit, worktree, and claim evidence.
- Update relevant lifecycle, claim, and project-configuration documentation and supported generated mirrors only after exact governed-source discovery and approval gates. Do not mutate any governed skill or role definition until a fresh smallest exact canonical path manifest receives scope-specific user approval.
- Update required lifecycle HTML documentation, especially design/orchestrated-development-lifecycle.html. Rename the visible Agents And Handoffs section with id agents-title to Agents, and separate concise plain-language role descriptions from lifecycle handoff sequences.
- Define Role as the reusable responsibility and authority contract applied to an Agent. The Agents section lists roles and gives each one concise sentence; it must not present a role definition as an execution instance.
- Use these terms consistently: Work item is the durable backlog record, outcome, lifecycle, evidence, and ownership; Thread is an execution context or conversation with a root and possible child agents; Agent is a runtime instance under a named role inside a thread; Task is a bounded assignment to an agent and never a synonym for thread; Handoff is a lifecycle event transferring evidence and next action.
- In the Agents section distinguish Dev Backlog Coordinator, Dev Orchestrator, Dev Backlog Steward, implementation or producing agents, independent reviewers, Dev Verifier, and optional integration specialists with concise role cards or a table.
- Add a concise Threads And Execution Contexts explanation: a parent coordination thread has a root Coordinator; each active work item has one work-item thread with a root Orchestrator; child agents handle coding, writing, review, verification, and stewardship.
- Move handoffs outside Agents into a lifecycle or interaction section or sequence diagram covering dispatch and start acceptance, implementation evidence, review and verification, integration, terminal provider update, and parent cleanup. Do not call threads agents or tasks in visible prose, labels, cards, diagrams, captions, or anchors.

## Acceptance Criteria

- A parent coordinator records Ready -> Starting dispatch or reservation evidence, counts Starting against capacity, and cannot create a duplicate task for the same item after an ambiguous startup.
- A per-item root Dev Orchestrator records Starting -> Running atomically through its Dev Backlog Steward child with canonical task, branch, worktree, and claim evidence.
- Failed startup produces an observable Ready restoration or a truthful Blocked or User Action Required record, with no duplicate active canonical task.
- Parent and per-item ownership boundaries are observable: the per-item Steward atomically completes and archives its item, while the parent only cleans up tasks, recounts capacity, and dispatches replacements.
- Each watchdog cycle immediately reports every stopped, failed, or missing Starting or Running task, every stopped task with a live coordination entry, and every terminal item with one; it reports active quiet tasks only when an explicit deadline or hard stop applies.
- Watchdog output contains evidence but makes no integration-readiness, accepted-delivery, or completion decision and makes no lifecycle or coordination mutation.
- Acquisition evidence records expected duration, requested hard stop, configured maximum, expected release, and cleanup grace; invalid expected, hard-stop, and maximum ordering is rejected.
- Heartbeats do not extend hard stops; evidence-backed extensions stay within the maximum; overdue coordination state is visible without auto-release; stopped owners are immediately actionable.
- All five initial resource-class defaults are rendered or otherwise observable, project overrides validate, and later optimization can change defaults through the approved configuration path.
- Replacement orchestration can recover a Starting or Running item from durable branch, commit, worktree, task, and claim evidence.
- No governed definition changes occur before discovery produces the smallest exact path manifest and the user provides scope-specific approval.
- The lifecycle documentation visibly uses the required Work item, Thread, Agent, Task, Handoff, and Role distinctions; no visible prose combines Agents And Handoffs or calls a thread a task.
- The Agents section contains concise one-sentence role descriptions and a compact visual role table or cards, while handoff sequences are separately visible through a lifecycle interaction section or sequence diagram.
- The Threads And Execution Contexts explanation visibly shows parent coordination, one work-item thread per active item, one root Orchestrator per work-item thread, and child producing, review, verification, and stewardship agents.

## Dependencies

- [Integrate Work-Item Routing Through Core-Only Agent Definitions](integrate-work-item-routing-through-core-only-agent-definitions.md)
- [Select Resource Coordination Per Project](selectable-resource-coordination.md)

These are ordinary evidence-backed dependencies. Bounded discovery for this item may start while their delivery proceeds.

## Verification

- Add focused lifecycle tests for transition ownership, Starting capacity counting, duplicate-start prevention, and failed or ambiguous startup recovery.
- Add focused watchdog tests for stopped-task, missing-task, live-coordination, terminal-coordination, quiet-active, and no-semantic-inference behavior.
- Add focused resource-deadline tests for heartbeat versus hard stop, bounded extensions, overdue status, no auto-release, cleanup grace, generated defaults, and override validation.
- Verify recovery from durable task, branch, commit, worktree, and claim evidence.
- Run focused project-configuration, claim, lifecycle, renderer, generator freshness, and skill-validation checks for changed surfaces after approval.
- Run documentation-page verification, link and anchor checks, terminology assertions, independent UX and readability review, and independent source and methodology review for the lifecycle HTML changes.
- Run git diff --check and obtain independent review of the exact approved change.

## Open Questions

- Confirm the exact configuration field names and resource class identifiers from current source discovery.
- Confirm whether named-resource overrides use a class-plus-id map or a separate policy list while retaining deterministic validation.
- Produce the smallest exact governed canonical-path manifest and supported generated-mirror list before requesting mutation approval.

## Notes

- Creation authority: direct user direction on 2026-07-22.
- Creation claim: create-starting-lifecycle-resource-deadlines-019f8b00, acquired event fc704e86-952c-49f8-9310-a0bc314020af from primary main.
- This item authorizes Ready-state discovery only. It does not authorize governed skill or role definition mutation.
