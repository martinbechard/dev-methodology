# Add Dedicated Watchdog And Stalled Lifecycle

Status: Running

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/add-dedicated-watchdog-and-stalled-lifecycle.md

Completion: direct-main

Owner: Dev Orchestrator

## Summary

Define a dedicated read-only Dev Backlog Watchdog Role and distinguish suspected lack of progress from a known blocker. Add an explicit Orchestrator-to-Coordinator blocker handoff, make the Coordinator responsible for Stalled and Blocked lifecycle decisions, and document the complete interaction in the orchestrated development lifecycle.

## Context

The completed predecessor at backlog/completed-backlog/features/add-starting-lifecycle-and-resource-deadline-policies.md established a generic read-only watchdog Task. The current conceptual agent catalog does not define a dedicated watchdog Role or generated runtime agent.

The current Dev Orchestrator contract reports BLOCKED when a correction boundary is exhausted, a required dependency is unavailable, or ownership cannot be acquired safely. It does not define a universal blocked notification that transfers exact evidence and the requested next action to the parent Dev Backlog Coordinator.

The current watchdog contract can detect phase overruns, evidence gaps, stopped or missing tasks, and satisfied Blocked-item unblock conditions. It cannot mutate lifecycle state. The lifecycle currently has no Stalled state for an item that appears not to be progressing before a causal blocker is known.

The requested lifecycle distinguishes:

- Stalled: evidence indicates that work is not progressing, but the preventing cause or unblock condition is not yet established.
- Blocked: a recognized cause prevents progress and the Dev Backlog Coordinator owns the next coordination or recovery action.
- User Action Required: the Coordinator has determined that progress requires a concrete user decision, authority grant, action, or user-held information.

The user supplied the following standing watchdog prompt as the implemented operating baseline:

```text
Act as the dedicated read-only Dev Methodology backlog watchdog for parent task 019f8b00-e6d7-7841-854a-40a50ca4e7f2 in /Users/martinbechard/dev/dev-methodology.

Apply skills/codex-workitem-coordination/SKILL.md, especially Dedicated Read-Only Watchdog and Fifteen-Minute Parent Review. On each cycle, read current file-backed work items, Git state, configured claim registry state, and Codex task state. Evaluate Running capacity and vacancies, phases and age, estimates/hard stops/evidence progress, Blocked unblock conditions, accepted work stranded before integration, integrated work awaiting provider closeout, terminal cleanup anomalies, waits at or beyond 30 minutes, and unsafe/stale/broad shared ownership.

Remain strictly read-only. Do not mutate repository files, lifecycle state, claims, tasks, branches, worktrees, or shared resources; do not dispatch, integrate, clean up, or run expensive/live verification. Notify parent task 019f8b00-e6d7-7841-854a-40a50ca4e7f2 only when an actionable condition exists, with exact evidence and the smallest recommended parent action. When healthy, record only a concise no-action cycle result here.
```

Each scheduled cycle used this heartbeat instruction:

```text
Run one complete read-only watchdog cycle now using the task's standing contract. Notify parent task 019f8b00-e6d7-7841-854a-40a50ca4e7f2 only if an actionable condition exists; otherwise record a concise no-action cycle note here.
```

The permanent contract must parameterize the parent task identifier and repository path rather than embedding this historical execution identity.

## Source Evidence

- On 2026-07-24, the user supplied the exact standing watchdog prompt and fifteen-minute heartbeat instruction above and directed that one or more work items handle the identified lifecycle issues.
- The user directed that an Orchestrator which determines a work item is blocked must advise the Dev Backlog Coordinator.
- The user defined Blocked as a known preventing cause for which the Dev Backlog Coordinator owns the next action, with User Action Required used when the required next action belongs to the user.
- The user proposed Stalled as a separate state for work that appears not to be progressing before a preventing cause is recognized.
- The user explicitly required design/orchestrated-development-lifecycle.html to be updated as part of the delivery.
- On 2026-07-25, the user approved the exact six governed canonical source paths and the listed dependent artifacts by answering, “I approve the whole thing.”
- Live repository discovery on 2026-07-24 found no conceptual or generated watchdog agent definition. The existing contract assigns a dedicated watchdog Task to an unspecified Agent.

## Requirements

- Add a conceptual Dev Backlog Watchdog Role whose sole responsibility is the scheduled read-only observation contract.
- Generate the supported native Watchdog agent definitions from the conceptual source. Do not edit generated adapters or generated documentation data directly.
- Define canonical standing and heartbeat prompt templates that preserve the supplied wording exactly. The standing template may replace only parent task 019f8b00-e6d7-7841-854a-40a50ca4e7f2 with a parent-task placeholder and /Users/martinbechard/dev/dev-methodology with a repository-root placeholder. The heartbeat template may replace only the same parent task identifier. Provider and resource-coordination variation must be supplied through resolved task context without rewriting the canonical prompt text.
- Render the canonical templates with the historical parent task identifier and repository root and verify byte-for-byte equality with the two supplied prompts in this item.
- Define the watchdog output as either one concise no-action cycle result or one actionable parent alert containing the affected provider identity or task, observed evidence, reason attention is required, and smallest recommended Coordinator action.
- Keep the watchdog outside the provider queue and Starting-plus-Running capacity. It owns no Work item, mutation claim, branch, worktree, delivery, lifecycle transition, or cleanup.
- Keep every watchdog cycle read-only. The Watchdog must not mutate repository files, provider records, lifecycle state, claims, tasks, branches, worktrees, or shared resources; dispatch work; integrate changes; perform cleanup; or run expensive or live verification.
- Keep active quiet work healthy unless an explicit estimate, hard stop, evidence-progress boundary, stopped task, missing task, or other source-backed anomaly makes intervention actionable.
- Add Stalled as an explicit nonterminal lifecycle state. Stalled means current evidence indicates that the item is not making progress while the causal blocker or unblock condition remains unknown.
- Do not let the Watchdog set Stalled. The Watchdog reports evidence to the Dev Backlog Coordinator; the Coordinator decides whether the evidence justifies a lifecycle change and delegates the atomic provider mutation to Dev Backlog Steward.
- Define the Stalled evidence contract: last known productive evidence, phase estimate and hard stop when present, anomaly or progress gap, canonical Thread and Agent Task identities, current ownership and coordination state, diagnostic owner, and next investigation action.
- Exclude Stalled from runnable dispatch and from Starting-plus-Running active capacity while the Coordinator investigates it. Fill the resulting vacancy from fresh provider inventory when eligible Ready work exists.
- Define deterministic Stalled dispositions. The Coordinator may restore Running only when the same canonical owner demonstrably resumes safely, restore Ready when ownership has ended and normal redispatch is required, set Blocked when a concrete cause and Coordinator-owned next action are known, set User Action Required when a concrete user-owned action is required, or record an applicable terminal disposition from evidence.
- Require a Dev Orchestrator that recognizes a concrete blocker to preserve commits and evidence, stop unsafe work, obtain truthful resource disposition, and immediately notify the parent Dev Backlog Coordinator.
- Define the Orchestrator blocked notification fields: provider identity or provider-none task, canonical Thread and root Agent Task identifiers, current phase, exact blocker, blocker owner, unblock condition, requested Coordinator action, preserved commits and evidence, resource-ownership disposition, and whether the item remains safe to resume.
- Make the Dev Backlog Coordinator the lifecycle decision owner for Blocked. The Coordinator validates the handoff, chooses an authorized coordination or recovery action, and delegates the atomic Blocked transition to Dev Backlog Steward.
- Define Blocked as a known preventing cause awaiting Coordinator-owned coordination, recovery, or disposition. Do not use Blocked merely because a task is quiet or appears slow.
- Route Blocked to User Action Required only when investigation identifies one concrete decision, authority grant, action, risk acceptance, or user-held fact that belongs to the user. Coordinator inability alone must not manufacture a user obligation; an unresolved technical or external blocker remains Blocked with an exact owner and unblock condition.
- Require the Coordinator to acknowledge the Orchestrator blocker notification, remove the item from active capacity once the provider state changes, dispatch eligible replacement work, and retain responsibility until the blocker is resolved, routed to User Action Required, or terminally dispositioned.
- Require watchdog alerts for suspected stalls, satisfied Stalled or Blocked exit conditions, missing or stopped canonical tasks, and other existing actionable conditions. The Watchdog recommends action but never chooses the lifecycle result.
- Update file-provider inventory, reporting, validation, recovery, handoff, transition, resumption, archival, and series-state behavior for Stalled without weakening existing Blocked, User Action Required, Holding, Awaiting Review, Failed, or Abandoned semantics.
- Update design/orchestrated-development-lifecycle.html with the dedicated Watchdog Role, Stalled state, Orchestrator-to-Coordinator blocker notification, Coordinator triage, Watchdog alert boundary, and resulting transition paths.
- Keep the HTML wording concise and descriptive. Show that the Watchdog observes and alerts, the Orchestrator reports known blockers, the Coordinator decides recovery and lifecycle disposition, and the Steward performs provider mutation.
- Update README guidance, generated agent and skill documentation data, deterministic backlog-report output, and focused regression tests that own the affected behavior.
- Run the repository-supported pre-mutation approval check for every approved governed canonical source before changing it. Do not mutate a governed definition until the exact approval below is resolved and recorded.

## Acceptance Criteria

- The conceptual agent catalog contains one Dev Backlog Watchdog Role and generated runtime definitions derived from it.
- The Watchdog Role uses canonical standing and heartbeat templates whose only substitutions are the permitted parent-task and repository-root placeholders; rendering the historical values reproduces the supplied prompt text byte for byte.
- Watchdog tests prove strict read-only behavior, no capacity consumption, actionable-only parent alerts, concise no-action cycles, healthy quiet work, stall detection, and prohibition of lifecycle or coordination mutation.
- File-provider lifecycle documentation and behavior distinguish Stalled, Blocked, User Action Required, and Holding with no ambiguous overlap.
- A source-backed lack-of-progress condition can be recorded as Stalled without inventing a blocker.
- A watchdog observation alone cannot change provider, claim, task, branch, worktree, or delivery state.
- A Dev Orchestrator with a known blocker sends the complete blocked notification to the parent Coordinator and does not silently leave the parent to discover the condition later.
- The Coordinator acknowledges the blocker notification, delegates the provider mutation to Dev Backlog Steward, frees active capacity, and either performs a safe recovery action or records the next truthful lifecycle disposition.
- A Stalled item follows one explicit evidence-backed path to Running, Ready, Blocked, User Action Required, or a terminal disposition. Neither Stalled nor Blocked jumps directly to Running without the ownership and provider transitions defined for that path.
- A Blocked item moves to User Action Required only when the record contains one exact user-owned question or action and the unattended-work boundary.
- The fifteen-minute parent review and dedicated Watchdog cycle both recognize Stalled counts and actionable Stalled evidence without creating a second registry.
- Backlog inventory and deterministic reports display Stalled separately from Running and Blocked and identify the diagnostic owner and next action.
- design/orchestrated-development-lifecycle.html visibly documents the Watchdog Role and the Stalled, Blocked, Coordinator, Orchestrator, Steward, and User Action Required flow.
- Generated adapters and generated documentation data are fresh and contain no direct manual edits.
- Focused lifecycle, coordination, role-generation, backlog-report, bundle-content, and HTML checks pass.
- Independent source, methodology, artifact, and UX review accept the exact change, and git diff --check passes.

## Dependencies

[Add Starting Lifecycle And Resource Deadline Policies](../completed-backlog/features/add-starting-lifecycle-and-resource-deadline-policies.md)

## Verification

- Run the approval checker separately for each approved governed canonical source with the recorded approval evidence.
- Add focused tests in scripts/test_codex_workitem_coordination.py for Orchestrator notification, Coordinator acknowledgment, Stalled classification and transitions, watchdog stall alerts, read-only enforcement, capacity exclusion, and actionable-only messaging.
- Add exact rendered-template tests proving the historical parent task identifier and repository root reproduce both supplied watchdog prompts byte for byte.
- Add focused file-provider tests for Stalled series-state derivation and evidence-backed terminal archival under the matching failed-backlog type.
- Add focused tests in scripts/test_generate_backlog_report.py for separate Stalled inventory and rendering.
- Update scripts/test_bundle_content.py assertions for lifecycle states, agent catalog membership, generated freshness, source ownership, and HTML content.
- Run scripts/test_agent_identity_generation.py and relevant generated-role checks for the Watchdog Role.
- Run the applicable role and skill generators in write mode only for supported mirrors, then run their freshness checks.
- Verify design/orchestrated-development-lifecycle.html with documentation-page verification, link and anchor checks, narrow and wide viewport inspection, and independent UX review.
- Run the lowest repository verification tier justified by the final affected surfaces, escalating when shared generators, provider management, or final campaign gates require it.
- Run git diff --check and obtain independent review of the complete approved diff.

## Open Questions

- Confirm during implementation whether Stalled retains the same owner while diagnosis proceeds or always ends ownership and returns through Ready before resumption. The selected behavior must preserve duplicate-start prevention and make capacity accounting deterministic.
- Confirm whether the deterministic backlog report needs a dedicated Stalled section or a distinct Stalled badge within active non-runnable work. The report must not merge Stalled into Blocked.
- Select an existing model profile for Dev Backlog Watchdog from live model-profile evidence; do not add or change a model profile unless separately approved.

## Definition Change Approval

## Current Running Acceptance

- Resumption: User Action Required -> Ready committed at 46f4437dd9aa6fb64275058c820cc2697a83f1f9, then the parent Coordinator recorded the distinct Ready -> Starting reservation at 93d84231d9a22b580ea2522b4101088d9cb83650. This acceptance preserves the same canonical identity and creates no replacement Thread.
- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a.
- Canonical Thread/Task: 019f9a91-b1a9-7ea0-9c90-35f0ed78c1be.
- Root Agent: Dev Orchestrator for canonical task 019f9a91-b1a9-7ea0-9c90-35f0ed78c1be.
- Lifecycle Acceptance: Starting -> Running accepted by the root Dev Orchestrator through its Dev Backlog Steward child.
- Normalized Objective: Add dedicated watchdog and stalled lifecycle.
- Persistence And Completion: file provider; direct-main completion.
- Started At: 2026-07-26T15:43:24Z.
- Parent Reservation Commit: 93d84231d9a22b580ea2522b4101088d9cb83650.
- Approval Evidence: governed six-source approval recorded at df2d861a715b9563c2b504ef9e674d4918f99055; User Action Required resolution and approved seven-path supplemental scope recorded at 46f4437dd9aa6fb64275058c820cc2697a83f1f9. The user’s exact approvals, scope, and durable provenance remain in Definition Change Approval.
- Delivery Identity: Branch codex/watchdog-stalled-lifecycle-019f9a91; private worktree .worktrees/watchdog-stalled-lifecycle-019f9a91.
- Backlog Acceptance Claim: c6d1dc57-43bf-4b8d-adb1-2bf4c77bbE53; acquisition event bbab86e4-fb17-4264-bdaa-853f4b77f69e.
- Prior Reservation Claim Evidence: Ready -> Starting acquisition and release events c89fe91b-dc00-45e8-898f-7d3adeb11213 and 2407e33c-b8e0-4d3a-835f-5267feae2d1c.
- Next Lifecycle Owner: the root Dev Orchestrator owns delivery; Dev Backlog Steward performs later provider transitions on this canonical item.

## Current Starting Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a.
- Canonical Thread/Task: 019f9a91-b1a9-7ea0-9c90-35f0ed78c1be; the preserved canonical identity is reserved and no replacement Thread is authorized.
- Lifecycle Reservation: Ready -> Starting recorded by the parent Dev Backlog Coordinator through its Dev Backlog Steward child.
- Normalized Objective: Add dedicated watchdog and stalled lifecycle.
- Dispatched At: 2026-07-26T15:41:04.169467Z.
- Launch Reservation: one parent-owned launch reservation; capacity was available at reservation time.
- Reservation Evidence: parent instruction for the distinct Ready -> Starting transaction after the approved User Action Required -> Ready transaction committed and released; backlog claim event c89fe91b-dc00-45e8-898f-7d3adeb11213.
- Intended Root Dev Orchestrator: Dev Orchestrator for canonical task 019f9a91-b1a9-7ea0-9c90-35f0ed78c1be.
- Next Lifecycle Owner: the same root Dev Orchestrator must accept Starting -> Running before implementation or further repository mutation.
- Owner: Unowned pending root Dev Orchestrator acceptance.

## Definition Change Approval

The user approved the exact governed role and skill sources below for this work item.

## Governed Canonical Sources

- agents/roles/dev-activities/dev-backlog-watchdog.role.yaml
- agents/roles/dev-activities/dev-backlog-coordinator.role.yaml
- agents/roles/dev-activities/dev-orchestrator.role.yaml
- agents/roles/dev-activities/dev-backlog-steward.role.yaml
- skills/codex-workitem-coordination/SKILL.md
- skills/manage-file-work-items/SKILL.md

## Allowed Dependent Artifacts

- generated/adapters/** outputs derived from the approved conceptual role and skill sources
- design/generated/role-definitions.js
- design/generated/skill-definitions.js
- design/orchestrated-development-lifecycle.html
- README.md
- backlog/examples/styled-backlog-report.html
- scripts/generate-backlog-report.py
- scripts/test_generate_backlog_report.py
- scripts/test_codex_workitem_coordination.py
- scripts/test_bundle_content.py
- scripts/test_agent_identity_generation.py
- scripts/test_agent_skill_evaluation_docs.py
- evals/agent-scenarios.yaml
- evals/skill-probes.yaml
- evals/workflow-packs.yaml
- evals/agent-tests/suite-index.yaml
- evals/agent-tests/dev-backlog-watchdog/suite.yaml
- evals/agent-tests/dev-backlog-watchdog/scenarios.yaml
- evals/agent-tests/dev-backlog-watchdog/requirements-matrix.md
- evals/agent-tests/dev-backlog-watchdog/fixtures/cases.yaml
- evals/agent-tests/dev-backlog-watchdog/agents/supervisor.toml
- evals/agent-tests/dev-backlog-watchdog/agents/judge.toml
- evals/agent-tests/dev-backlog-watchdog/skills/dev-backlog-watchdog-suite-contract/SKILL.md
- evals/agent-tests/dev-backlog-watchdog/watchdog_simulator.py
- evals/agent-tests/dev-backlog-watchdog/test_watchdog_simulator.py
- design/agent-and-skill-evaluations.html
- scripts/build-skill-docs.py
- scripts/build-agent-skill-hierarchy.py
- scripts/test_role_mutation_policy.py
- scripts/test_agent_skill_hierarchy.py
- design/agent-skill-hierarchy.svg
- design/agent-skill-test-coverage-checklist.md
- design/generated/agent-skill-explorer-data.js

## Approval Resolution

On 2026-07-25, the user answered exactly:

> I approve the whole thing.

The answer approves exactly the six paths in Governed Canonical Sources and only the dependent artifacts listed above. The resulting lifecycle disposition is Ready with Owner: Unowned. No Starting reservation or implementation ownership was created by this approval transaction.

On 2026-07-26, the user answered exactly:

> Approved

The answer approves exactly the seven additional dependent artifacts listed above: scripts/build-skill-docs.py; scripts/build-agent-skill-hierarchy.py; scripts/test_role_mutation_policy.py; scripts/test_agent_skill_hierarchy.py; design/agent-skill-hierarchy.svg; design/agent-skill-test-coverage-checklist.md; and design/generated/agent-skill-explorer-data.js. The answer was provided in the canonical task 019f9a91-b1a9-7ea0-9c90-35f0ed78c1be and relayed by the parent Dev Backlog Coordinator. It resolves the recorded question without creating a replacement Thread, Starting reservation, or implementation ownership.

## Notes

- Creation authority: direct user request on 2026-07-24 to create one or more work items for the supplied watchdog contract, blocker handoff, Stalled state, Coordinator-owned Blocked disposition, and required lifecycle HTML update.
- Approval provenance: the parent Dev Backlog Coordinator relayed the user’s exact answer for the canonical 019f9a91 work-item context on 2026-07-25.
- Duplicate check: the completed predecessor introduced generic read-only watchdog behavior but did not define a Watchdog Role, Stalled lifecycle state, or universal Orchestrator-to-Coordinator blocked notification.
- Non-goal: the Watchdog does not become an autonomous recovery, dispatch, integration, cleanup, or lifecycle-mutation agent.

## User Action Required Resolution

### Exact Question

Do you approve adding exactly these seven dependent artifacts to this item's scope: scripts/build-skill-docs.py; scripts/build-agent-skill-hierarchy.py; scripts/test_role_mutation_policy.py; scripts/test_agent_skill_hierarchy.py; design/agent-skill-hierarchy.svg; design/agent-skill-test-coverage-checklist.md; and design/generated/agent-skill-explorer-data.js?

### Why Input Is Required

The original approval covers exactly six governed canonical sources and the listed dependent artifacts. Live catalog tracing shows these seven additional paths are required for actor-suffix loader acceptance, the required Backlog Management focus and Coordinator-to-Watchdog edge, the hard-coded 27-role mutation-policy count, focused hierarchy role-and-edge assertions, and the three supported generated freshness outputs. No other source expansion is required.

### Options And Tradeoffs

- Approve: resume the same canonical task with the seven paths added to its dependent-artifact scope.
- Narrow: revise the role identity or implementation plan, then recheck the approval scope.
- Defer: leave the feature unimplemented in User Action Required.
- Decline: do not add the Watchdog role.

### Unattended-Work Boundary

The required answer is recorded. The preserved canonical task 019f9a91-b1a9-7ea0-9c90-35f0ed78c1be must resume through Ready -> Starting -> Running before implementation continues.

### Preserved Running Evidence

- The canonical task identity, root Dev Orchestrator, parent coordination thread, branch, private worktree, existing commits, approval evidence, and current running acceptance above are preserved as out-of-sequence evidence.
- This transition does not create a replacement Thread or discard prior delivery evidence.
