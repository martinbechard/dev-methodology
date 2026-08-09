# Use MCP Hierarchy Plans for Complex Development

Status: User Action Required

Type: Feature

Provider: file

Work Item ID: use-mcp-hierarchy-plans-for-complex-development

Completion: main-branch

## Summary

Add a portable planning skill for complex development work and route it to Dev Orchestrator. The skill must maintain an authoritative JSON execution plan and a synchronized, readable HTML projection, marking completed work and adding newly discovered tasks or subtasks throughout delivery.

## Context

The mcp-agent-ops repository at commit ebc26f060c4a70d82a3a0cd4495ed37f76fefe62 includes durable hierarchy-plan creation and mutation APIs in src/mcp_agent_ops/hierarchy/plan.py. The public examples create a JSON plan beside its HTML rendering, mark an item complete, add a child, replace children, and add a peer. Every mutation regenerates the HTML projection.

The complete reference at /Users/martinbechard/dev/mcp-agent-ops/docs/reference/hierarchy-html-renderer.md explicitly states that create_hierarchy_plan and update_hierarchy_plan are direct Python APIs, not MCP tools or CLI commands. The MCP tool reference does not list plan creation, plan mutation, or hierarchy rendering tools. The server therefore has the underlying behavior needed by this feature but cannot currently perform the requested workflow through the MCP protocol.

The plan is an execution aid for one complex delivery. It must not replace the file-provider work item, provider lifecycle, source-control evidence, or the Dev Orchestrator's responsibility for decomposition and handoffs.

## Source Evidence

The user requested this work on 2026-08-09 in canonical task 019fb057-1767-7ef2-b5fa-41f4417b20b3:

> the mcp-agent-ops server has new functionality to work with structured data such as a plan. Read the info including usage examples then create a work item to incorporate the use of the planning functions for complex development, by creating a json/html plan via the mcp server, updating it when tasks are completed, adding new tasks and subtasks when discovery happens. This is probably a skill that the Dev Orchestrator needs, to stay on top of complex work. Go into "User action required" if there is new functionality missing that would help with this planning work to be added to the mcp-agent-ops server.

Repository evidence:

- /Users/martinbechard/dev/mcp-agent-ops/README.md documents paired JSON and HTML creation and later mutations.
- /Users/martinbechard/dev/mcp-agent-ops/docs/reference/hierarchy-html-renderer.md documents exact path or unique-title targeting, completion changes, child and peer insertion, child replacement, and automatic HTML regeneration.
- /Users/martinbechard/dev/mcp-agent-ops/tests/unit/hierarchy/test_plan.py verifies plan creation, completion changes, renamed tasks, discovered children, peer insertion, and fail-closed ambiguous targeting.
- /Users/martinbechard/dev/mcp-agent-ops/docs/reference/mcp-tools.md and src/mcp_agent_ops/adapters/mcp/server.py expose no hierarchy-plan MCP tools.

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
- Expose the existing durable hierarchy-plan operations as typed MCP tools with configured workspace-root containment, safe output targeting, structured results, and tests before the new skill requires MCP use.
- Update the relevant skill catalog, Dev Orchestrator definition, generated adapters and documentation, and focused bundle assertions from canonical sources.

## Acceptance Criteria

- A complex-work example creates one canonical JSON plan and one synchronized standalone HTML plan through MCP, without Python or shell code generated by the model.
- The example marks a task complete, adds a newly discovered subtask, and adds a newly discovered peer task through typed MCP calls; both files reflect every accepted change.
- Ambiguous or missing targets, paths outside configured workspace roots, invalid plan documents, and multi-mutation requests fail without silently changing either artifact.
- The planning skill states when a plan is required, when it is unnecessary, which source is authoritative, and how Dev Orchestrator reconciles it with provider lifecycle and delivery evidence.
- The Dev Orchestrator consumes the planning skill for qualifying complex work and does not create a second work-item ledger.
- Focused tests prove creation, completion updates, child and peer discovery, HTML regeneration, target ambiguity, path containment, uncertain-result reconciliation, and final plan reconciliation.
- Generated skill documentation and Dev Orchestrator adapters are current, and affected catalog and bundle checks pass.
- Independent methodology review and verification accept the integrated behavior.

## Dependencies

None.

## Verification

- Run the mcp-agent-ops focused hierarchy-plan unit tests and new MCP server contract and stdio integration tests.
- Verify MCP plan creation and each supported mutation inside an allowed temporary workspace, including paired JSON and HTML byte changes.
- Verify structured rejection for workspace escape, ambiguous targets, missing targets, invalid schemas, and calls requesting more than one mutation.
- Validate skills/manage-complex-development-plan/SKILL.md through the configured skill validator.
- Regenerate and check affected skill documentation and Dev Orchestrator adapters from canonical sources.
- Run focused dev-methodology bundle assertions for the new skill, its Dev Orchestrator routing, and the planning examples.
- Run Markdown link validation and Git diff checks for the exact changed paths.

## Open Questions

- Should the MCP tools preserve the current dotted-path and unique-title targeting contract, or add stable item identifiers while retaining backward compatibility?
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

## User Action Required

### Question for the User

Do you approve adding typed hierarchy-plan creation and mutation tools to the mcp-agent-ops MCP server, limited to the existing create_hierarchy_plan and update_hierarchy_plan behavior plus workspace-root containment, structured results, documentation, and focused server tests?

### Why User Input Is Required

The requested workflow must create and update the plan through the MCP server, but the current mcp-agent-ops reference explicitly exposes the required operations only as direct Python APIs. Adding MCP tools changes a separately maintained server and its public tool contract. The original request directed this work item to User Action Required when such missing server functionality was found, but it did not itself grant cross-repository mutation authority.

### Options and Tradeoffs

- Approve the MCP tools. The work item can implement the requested model-facing workflow using typed server operations and retain the current tested plan semantics.
- Do not approve the MCP tools. The work item must remain paused or be revised to use direct Python calls, which would not satisfy the request to manage the plan through MCP.

### Resolution

Pending. After the answer, record the exact wording, date, and canonical-task provenance without expanding the approved dev-methodology governed manifest.

### Unattended Work Boundary

Do not mutate /Users/martinbechard/dev/mcp-agent-ops, implement the new dev-methodology planning skill, change Dev Orchestrator, or generate dependent artifacts until the user answers. Read-only design and exact-path discovery may continue. Creation of this work item does not dispatch it while backlog crisis recovery remains active.

## Notes

- The current server-side gap is protocol exposure, not core plan behavior. Existing direct APIs already create paired files, mark completion, rename tasks, add children, replace children, add peers, and regenerate HTML.
- The HTML completion markers are read-only by design. All durable changes must flow through the MCP plan mutation tool and authoritative JSON source.
- This item does not authorize shared installation, release, publication, or unrelated mcp-agent-ops changes.
