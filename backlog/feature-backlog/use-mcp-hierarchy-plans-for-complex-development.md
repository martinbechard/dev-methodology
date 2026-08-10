# Use MCP Hierarchy Plans for Complex Development

Owner: Dev Orchestrator (/root/mcp_hierarchy_plans)

Status: Running

Type: Feature

Provider: file

Work Item ID: use-mcp-hierarchy-plans-for-complex-development

Completion: main-branch

## Starting Handoff Evidence

Parent Coordination Task: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Dispatch Reservation: First normal multitask wave after terminology completion.

Normalized Objective: Incorporate MCP hierarchy planning into complex Dev Orchestrator work with maintained JSON and HTML plans.

Dispatch Requested At: 2026-08-10T00:44:00Z

Intended Root Role: Dev Orchestrator

Launch Result: Reserved; canonical root launch follows this committed transition.

Last Contact: 2026-08-10T00:44:00Z

Next Reconciliation At: 2026-08-10T00:59:00Z

## Active Execution Evidence

Condition Type: root-execution

Owner: Dev Orchestrator (/root/mcp_hierarchy_plans)

Evidence: Codex task /root/mcp_hierarchy_plans accepted the work-item claim and created the private source worktree from main commit 9488c71873e19c99b523927bce14ec64da634158.

Observed At: 2026-08-10T00:49:06Z

Started At: 2026-08-10T00:48:23Z

Deadline or Expires At: 2026-08-10T04:48:23Z

Next Action: Dispatch the bounded source implementation lane for the approved planning skill and Dev Orchestrator routing.

Next Reconciliation At: 2026-08-10T00:59:00Z

Codex Task ID: /root/mcp_hierarchy_plans

Conversation ID: 019fb057-1767-7ef2-b5fa-41f4417b20b3

Root Role: Dev Orchestrator

Parent Task ID: /root

Branch: codex/use-mcp-hierarchy-plans-for-complex-development

Worktree: /Users/martinbechard/dev/dev-methodology/.worktrees/use-mcp-hierarchy-plans-work-019fb057

Phase: implementation dispatch

## Summary

Add a portable planning skill for complex development work and route it to Dev Orchestrator. The skill must maintain an authoritative JSON execution plan and a synchronized, readable HTML projection, marking completed work and adding newly discovered tasks or subtasks throughout delivery.

## Context

The mcp-agent-ops repository at commit ebc26f060c4a70d82a3a0cd4495ed37f76fefe62 includes durable hierarchy-plan creation and mutation APIs in src/mcp_agent_ops/hierarchy/plan.py. The public examples create a JSON plan beside its HTML rendering, mark an item complete, add a child, replace children, and add a peer. Every mutation regenerates the HTML projection.

The user clarified on 2026-08-09 that the required structured-plan tools already exist and that this work needs a plan for using them, not new mcp-agent-ops functionality. Implementation must discover the configured server's exact current tool schemas and use the existing structured-plan creation, mutation, and HTML-rendering operations without changing the server's public contract.

The plan is an execution aid for one complex delivery. It must not replace the file-provider work item, provider lifecycle, source-control evidence, or the Dev Orchestrator's responsibility for decomposition and handoffs.

## Source Evidence

The user requested this work on 2026-08-09 in canonical task 019fb057-1767-7ef2-b5fa-41f4417b20b3:

> the mcp-agent-ops server has new functionality to work with structured data such as a plan. Read the info including usage examples then create a work item to incorporate the use of the planning functions for complex development, by creating a json/html plan via the mcp server, updating it when tasks are completed, adding new tasks and subtasks when discovery happens. This is probably a skill that the Dev Orchestrator needs, to stay on top of complex work. Go into "User action required" if there is new functionality missing that would help with this planning work to be added to the mcp-agent-ops server.

Repository evidence:

- /Users/martinbechard/dev/mcp-agent-ops/README.md documents paired JSON and HTML creation and later mutations.
- /Users/martinbechard/dev/mcp-agent-ops/docs/reference/hierarchy-html-renderer.md documents exact path or unique-title targeting, completion changes, child and peer insertion, child replacement, and automatic HTML regeneration.
- /Users/martinbechard/dev/mcp-agent-ops/tests/unit/hierarchy/test_plan.py verifies plan creation, completion changes, renamed tasks, discovered children, peer insertion, and fail-closed ambiguous targeting.
- /Users/martinbechard/dev/mcp-agent-ops/docs/reference/mcp-tools.md and src/mcp_agent_ops/adapters/mcp/server.py expose no hierarchy-plan MCP tools.

That repository documentation was the basis for the initial User Action Required state, but it is superseded for scope disposition by the user's direct clarification that the tools are already present. Any documentation or configured-server identity mismatch encountered during implementation is a technical discovery/configuration issue to reconcile against the existing tool implementation, not authority to add new server functionality.

## Requirements

- Add one portable manage-complex-development-plan skill and route it to Dev Orchestrator for work whose scope, dependency structure, duration, or discovery risk makes an externalized plan materially useful.
- Define a complexity gate so routine one-step or otherwise easily tracked work does not create plan artifacts.
- Create the initial plan through the configured mcp-agent-ops server as a canonical JSON file with a synchronized sibling HTML file.
- Represent the delivery objective, ordered tasks, subtasks, dependencies, current state, and relevant evidence references without duplicating the complete provider record.
- Update the plan through the MCP server when a task or subtask completes.
- Add a child task when discovery expands an existing task and add a peer task when discovery introduces a new workstream.
- Preserve completed work and prior structure when discovery adds work. Do not rewrite history merely to make the plan appear linear.
- Regenerate the HTML projection after every accepted JSON mutation and keep the JSON source authoritative.
- Require exact, unambiguous mutation targets and reconcile plan drift before continuing after a failed or uncertain update.
- Keep provider lifecycle, work-item status, review verdicts, verification results, and Commit delivery authoritative when they differ from the plan. Reconcile the plan to those sources rather than treating it as a shadow backlog.
- Define plan initialization, update cadence, recovery, final reconciliation, retention, and cleanup responsibilities for Dev Orchestrator.
- Exclude credentials, personal information, proprietary content not authorized for the configured server, and unnecessary source or prompt payloads from plan artifacts.
- Discover and record the exact schemas of the existing structured-plan MCP tools before the skill invokes them; do not add, redesign, or publish mcp-agent-ops server functionality under this work item.
- Update the relevant skill catalog, Dev Orchestrator definition, generated adapters and documentation, and focused bundle assertions from canonical sources.

## Acceptance Criteria

- A complex-work example creates one canonical JSON plan and one synchronized standalone HTML plan through MCP, without Python or shell code generated by the model.
- The example marks a task complete, adds a newly discovered subtask, and adds a newly discovered peer task through typed MCP calls; both files reflect every accepted change.
- Ambiguous or missing targets, paths outside configured workspace roots, invalid plan documents, and multi-mutation requests fail without silently changing either artifact.
- The planning skill states when a plan is required, when it is unnecessary, which source is authoritative, and how Dev Orchestrator reconciles it with provider lifecycle and delivery evidence.
- The Dev Orchestrator consumes the planning skill for qualifying complex work and does not create a second work-item ledger.
- Focused tests prove skill-level use of the existing tools for creation, completion updates, child and peer discovery, HTML regeneration, target ambiguity, path containment, uncertain-result reconciliation, and final plan reconciliation.
- Generated skill documentation and Dev Orchestrator adapters are current, and affected catalog and bundle checks pass.
- Independent methodology review and verification accept the integrated behavior.

## Dependencies

None.

## Verification

- Read the configured mcp-agent-ops structured-plan tool schemas and verify that the skill maps its creation and mutation operations to those existing inputs and structured results.
- Verify plan creation and each supported existing-tool mutation inside an allowed temporary workspace, including paired JSON and HTML byte changes.
- Verify structured rejection for workspace escape, ambiguous targets, missing targets, invalid schemas, and calls requesting more than one mutation.
- Validate skills/manage-complex-development-plan/SKILL.md through the configured skill validator.
- Regenerate and check affected skill documentation and Dev Orchestrator adapters from canonical sources.
- Run focused dev-methodology bundle assertions for the new skill, its Dev Orchestrator routing, and the planning examples.
- Run Markdown link validation and Git diff checks for the exact changed paths.

## Open Questions

- Which project-relative task-owned folder should hold transient JSON and HTML plans so they remain reviewable without becoming a second provider queue?

## Governed Definition Approval

### Governed Canonical Sources

- skills/manage-complex-development-plan/SKILL.md
- agents/roles/dev-activities/dev-orchestrator.role.yaml

### Allowed Dependent Artifacts

- skills/manage-complex-development-plan/agents/openai.yaml
- README.md
- scripts/test_bundle_content.py
- Generated skill documentation and Dev Orchestrator adapters produced by repository-authorized generators
- Focused non-governed planning fixtures and tests whose exact paths are resolved during implementation

### Approval Resolution

Approved at creation. The user explicitly requested on 2026-08-09 in canonical task 019fb057-1767-7ef2-b5fa-41f4417b20b3 that the planning workflow probably be a skill used by Dev Orchestrator. This approval covers exactly the two governed canonical sources above. It does not authorize another governed skill or Agent definition.

## Approval Resolution

Resolved on 2026-08-09 by the user's direct clarification in canonical parent task 019fb057-1767-7ef2-b5fa-41f4417b20b3:

> the tools are already there - you just need a plan to use them

The work item therefore requires no mcp-agent-ops source mutation, new tool contract, server release, or cross-repository publication. It may proceed by discovering and using the configured server's existing structured-plan tools. The approved dev-methodology governed manifest and all prior exclusions remain unchanged.

## Notes

- Existing structured-plan behavior is the implementation dependency. This work item owns the Dev Orchestrator usage plan and skill integration, not server capability development.
- The HTML completion markers are read-only by design. All durable changes must flow through the MCP plan mutation tool and authoritative JSON source.
- This item does not authorize mcp-agent-ops source changes, shared installation, release, publication, or unrelated server work.
