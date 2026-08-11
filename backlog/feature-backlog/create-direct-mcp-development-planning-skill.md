# Create Direct MCP Development Planning Skill

Status: Running

Type: Feature

Provider: file

Work Item ID: create-direct-mcp-development-planning-skill

Completion: main-branch

Owner: Dev Orchestrator

Canonical Conversation: Not exposed by runtime

Canonical Task: /root/direct_mcp_planning_orchestrator

Parent Task: /root

Branch: main

Worktree: /Users/martinbechard/dev/dev-methodology

Phase: Implementing

## Summary

Replace the existing helper-driven complex-planning workflow with a concise Skill that lets an Agent create and update a hierarchically numbered development plan through the configured MCP hierarchy-plan tools.

## Context

The repository already contains manage-complex-development-plan, but its large local Python helper duplicates persistence, synchronization, recovery, locking, and validation responsibilities around functionality supplied by mcp-agent-ops. The intended workflow is more direct: the Agent decides the plan content, expresses it as the hierarchy accepted by the configured MCP tool, receives the authoritative plan path or returned plan, and uses the targeted update tool as work changes.

The planning Skill is for Dev Coder when an assignment asks it to produce an implementation plan. Dev Orchestrator remains responsible for ensuring the plan matches the bounded assignment and for deciding whether a plan is required. A user instruction to code without planning bypasses plan creation.

## Source Evidence

On 2026-08-10, the user requested a planning Skill similar to the direct MCP document-outline Skill. The user specified a hierarchically numbered plan such as:

```text
1. First item
2. Second item
2.1 First child of the second item
2.2 Second child of the second item
3. Third item
```

The user further clarified that the Skill is required when Dev Coder is asked to create a plan. Earlier direction established that direct MCP hierarchy tools should perform hierarchy persistence and rendering rather than a custom repository helper.

The mcp-agent-ops hierarchy documentation describes durable plan creation, one-based dotted numbering, JSON authority, synchronized HTML output, and targeted mutations by dotted path or unique title.

## Requirements

- Keep the portable Skill name manage-complex-development-plan unless repository discovery proves a rename is necessary; do not add a second overlapping planning Skill.
- Remove the repository-owned planning helper and its helper-specific tests, recovery protocol, hashes, locks, operation history, and filesystem transaction machinery.
- Instruct Dev Coder to turn its implementation plan into the hierarchy source accepted by the configured MCP plan-creation tool. The Agent owns the plan semantics and decomposition; the MCP tool owns plan persistence and rendering.
- Explain the correspondence between nested hierarchy input and one-based display numbering. A suitable generic hierarchy for the example is:

```json
{
  "Development plan": [
    "First item",
    {
      "Second item": [
        "First child of the second item",
        "Second child of the second item"
      ]
    },
    "Third item"
  ]
}
```

- Invoke the configured MCP plan-creation operation directly and return the authoritative plan path or plan result supplied by that operation. Do not import the server package or invoke a local substitute.
- Support targeted plan updates through the configured MCP update operation: mark an item complete or incomplete, change its text, add a child, replace children, or add a peer after an item.
- Before an update, read the current plan state and resolve the intended item by its current dotted path or exact unique title. After the update, read the result and confirm that the requested mutation occurred, unaffected items remain, and the synchronized plan artifact reported by the tool is current.
- Add newly discovered work as a child or peer instead of rewriting the complete plan. Mark work complete only when the corresponding development result is complete.
- Route the Skill to Dev Coder for assignments that require an implementation plan. Preserve Dev Orchestrator routing so it can require the plan, check it against the assignment, and follow material progress.
- If the configured creation, read, or targeted-update operation is unavailable, stop with a clear unavailable-tool result. Do not install packages, call the Python package directly, or recreate the missing capability.
- Update only directly affected metadata, Agent definitions, documentation, generated projections, and focused contract tests through repository-authorized generators.

## Acceptance Criteria

- Dev Coder can create the example hierarchy through the configured MCP operation and receives the authoritative plan path or plan result.
- The rendered plan uses the expected one-based hierarchy: 1, 2, 2.1, 2.2, and 3.
- Dev Coder can apply each supported targeted mutation without rewriting the full plan.
- Update checks prove the intended item changed, unrelated items were preserved, and the returned plan state or synchronized artifact reflects the update.
- Dev Orchestrator can require and inspect the same plan without creating a second planning record.
- The previous local planning helper, helper tests, and helper-specific operational protocol are absent.
- Missing configured plan tools produce a clear stop result without fallback implementation or installation.
- Focused Skill, Agent-routing, generator-freshness, and bundle contract checks pass.

## Dependencies

None.

## Verification

- Validate the updated Skill with the configured Skill validator.
- Exercise one creation example and focused targeted-update examples through the configured MCP tools.
- Verify the expected dotted numbering and the post-update state.
- Run only directly affected Dev Coder, Dev Orchestrator, Skill-routing, generated-projection, and bundle tests.
- Run repository-authorized generator freshness checks for changed projections.
- Run Git diff checks for the exact changed paths.

## Open Questions

- Resolve the exact configured MCP tool names and current argument schema from tool discovery and the installed mcp-agent-ops documentation during implementation. This is technical discovery and does not change the requested direct-tool boundary.

## Governed Definition Approval

### Governed Canonical Sources

- skills/manage-complex-development-plan/SKILL.md
- skills/manage-complex-development-plan/agents/openai.yaml
- agents/roles/dev-activities/dev-coder.role.yaml
- agents/roles/dev-activities/dev-orchestrator.role.yaml

### Allowed Dependent Artifacts

- skills/manage-complex-development-plan/scripts/plan.py
- skills/manage-complex-development-plan/scripts/test_plan_helper.py
- evals/skill-probes.yaml
- scripts/test_bundle_content.py
- README.md
- Repository-authorized generated Skill documentation, Agent adapters, hierarchy projections, and evaluation projections affected by the four governed sources.

### Approval Resolution

Approved at creation. On 2026-08-10, the user explicitly requested the planning Skill, its direct MCP hierarchy workflow, targeted updates, and its use when Dev Coder is asked to create a plan. This approval covers only the exact governed sources above and their listed dependent artifacts.

## Notes

- The plan is an implementation aid, not a duplicate work-item queue or lifecycle record.
- The Skill should remain concise. It should describe how the Agent uses the configured MCP operations, not reproduce the MCP server implementation.

## Starting Handoff Evidence

Starting Recorded At: 2026-08-11T14:32:00Z

Coordinator: Codex task 019fb057-1767-7ef2-b5fa-41f4417b20b3

Normalized Objective: Replace the helper-driven planning workflow with the concise direct MCP hierarchy-plan Skill, preserve the approved routing, and verify creation and targeted updates through the configured tools.

Launch Result: Requested

Canonical Execution: Pending

Last Contact At: 2026-08-11T14:32:00Z

Next Reconciliation At: 2026-08-11T14:47:00Z

## Active Execution Evidence

Condition Type: root-execution

Owner: Dev Orchestrator

Evidence: Canonical Codex task /root/direct_mcp_planning_orchestrator remains active. Main commit 670c273c removes the retired checker prerequisite and restores exact-manifest authorization for the bounded Dev Coder lane.

Observed At: 2026-08-11T14:44:01Z

Started At: 2026-08-11T14:34:23Z

Deadline or Expires At: 2026-08-11T14:59:00Z

Next Action: Resume the original Dev Coder on current main and obtain one clean verified candidate commit.

Next Reconciliation At: 2026-08-11T14:56:00Z
