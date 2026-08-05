# Align Resource Coordination Skills

Status: Running

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/apply-object-oriented-skill-group-design/align-resource-coordination-skills.md

Completion: direct-main

Series: backlog/feature-backlog/apply-object-oriented-skill-group-design/index.md

## Current Dispatch Reservation

Transition: Ready -> Starting.
Parent Coordination Thread: /root/apply_skill_group_design_backlog.
Launch Reservation: One distinct bounded launch reservation for this provider record.
Normalized Objective: Align resource coordination skills with the approved object-oriented design and update their individual evaluations.
Dispatch Time: 2026-08-05T03:44:47Z.
Intended Root Dev Orchestrator Role: Dev Orchestrator.
Owner: Unowned pending accepted root.
Current Launch Evidence: Parent Coordinator authorized this exact reservation; exact-file backlog claim reserve-align-resource-coordination-skills acquired with outcome SHARED_CHECKOUT_ACQUIRED and event 33c1c09f-3104-4e23-85f9-cf9b159e7202. Runtime Thread creation and root acceptance have not occurred.
Required Next Lifecycle Transition: The root Dev Orchestrator must separately accept Starting -> Running before repository mutation.
Reconciliation: Pending.

## Current Running Acceptance

Transition: Starting -> Running.
Canonical Thread: /root/apply_skill_group_design_backlog/align_resource_coordination_skills.
Root Agent Task: /root/apply_skill_group_design_backlog/align_resource_coordination_skills.
Owner: Dev Orchestrator.
Branch: codex/align-resource-coordination-skills-019fb.
Worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/align-resource-coordination-skills-019fb.
Phase: Governed definition precheck and source implementation preparation.
Started At: 2026-08-05T03:48:55Z.
Claim Evidence: The private delivery lane requires no claim. This exact primary-main backlog mutation is protected by exact-file claim running-align-resource-coordination-skills-019fb, acquired with outcome SHARED_CHECKOUT_ACQUIRED and event d2c8c1ff-af01-424c-a70e-2bcec75fa3f0.
Preserved Coordination: Parent Coordination Thread /root/apply_skill_group_design_backlog and its Ready -> Starting launch reservation remain canonical.

## Summary

Align agent-claim, agent-claim-command, and agent-claim-mcp on explicit shared-resource and claim-operation headings while preserving the distinction between policy and transport implementations.

## Context

The Resource Coordination proposal keeps all three skill names. agent-claim owns coordination policy and the public shared-resource operations. The command and MCP skills implement transport-specific helper procedures. Their operation names should match where capabilities are equivalent, while agent-claim-mcp must remain visibly unavailable until verified deadline and reporting parity exists.

## Source Evidence

The user directed in the active Codex task on 2026-08-04: "create separate work items to update skills according to the new design, and update individual evals." The exact procedure recommendations are in design/skill-groups/concurrent-tasking.md at reviewed baseline commit c426c970153948f9d5d2d92f1b7b718613a8d4f7.

## Requirements

- Introduce the proposed policy headings in agent-claim and the matching helper-operation headings in both transport skills.
- Preserve the rule that agent-claim owns scope, conflict, deadline, uncertainty, and release policy while transports only explain invocation.
- Keep agent-claim-mcp unavailable unless this item produces verified capability parity; heading alignment alone must not mark it supported.
- Align operation inputs and results where the two transports implement the same procedure.
- Add individual evaluations for policy dispatch, command transport, and the MCP unavailable or parity boundary.

## Acceptance Criteria

- All proposed procedure names are explicit and coherent across the three definitions.
- No transport redefines claim policy or lets process exit status replace structured outcome handling.
- The MCP skill truthfully reports its supported or unsupported state from evidence.
- Individual evaluations cover status, acquire, extend, deadline extension, heartbeat, release, maintenance, reporting, and uncertain outcomes as applicable.
- Generated mirrors and focused claim tests pass.

## Dependencies

None.

## Verification

- Run the supported definition-change precheck for all three governed paths.
- Run individual skill probes plus scripts/test_agent_claim.py, scripts/test_agent_claim_transport.py, and focused coordination scenarios.
- Run scripts/test_agent_skill_evals.py, scripts/test_eval_coverage_catalog.py, scripts/test_bundle_content.py, and generated-output freshness checks.
- Compare policy and transport members against the proposed diagram and verify unavailable-state truthfulness.
- Run git diff --check and obtain independent methodology review and verification.

## Open Questions

Determine whether current MCP capability evidence is sufficient to expose maintenance and contention reporting; retain unavailable status when it is not.

## Governed Definition Approval

### Governed Canonical Sources

- skills/agent-claim/SKILL.md
- skills/agent-claim-command/SKILL.md
- skills/agent-claim-mcp/SKILL.md

### Allowed Dependent Artifacts

- approval-record-align-resource-coordination-skills.yaml
- evals/skill-probes.yaml
- evals/cases.yaml
- evals/workflow-packs.yaml
- evals/agent-tests/dev-backlog-coordinator
- evals/agent-tests/dev-orchestrator
- scripts/test_agent_claim.py
- scripts/test_agent_claim_transport.py
- scripts/test_codex_workitem_coordination.py
- scripts/test_agent_skill_evals.py
- scripts/test_eval_coverage_catalog.py
- scripts/test_bundle_content.py
- README.md
- design/agent-and-skill-definitions.html
- design/agent-and-skill-evaluations.html
- design/generated/skill-definitions.js
- generated/adapters files regenerated from only the approved canonical sources
- Directly related non-governed documentation, fixtures, and focused tests required to keep these approved definitions coherent

### Approval Resolution

Approved at creation on 2026-08-04 by the user statement in the active Codex task: "create separate work items to update skills according to the new design, and update individual evals." Approval is limited to the three governed canonical paths listed above. Any additional governed definition requires new explicit user approval recorded in this item.
