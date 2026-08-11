# Minimize Collaboration Subagent Context Inheritance

Status: Ready

Type: Defect

Provider: file

Work Item ID: minimize-collaboration-subagent-context-inheritance

Completion: main-branch

## Summary

Make no inherited conversation history the default for collaboration subagents and require each assignment to carry the bounded information needed for independent work.

## Context

Current repository guidance does not state the requested context-inheritance rule. Collaboration launches can therefore inherit an entire parent conversation even when durable files and a bounded assignment already provide the necessary context, consuming unnecessary model tokens. Separate user-visible Codex work-item tasks are a different coordination mechanism and must continue through explicit provider and task handoffs.

## Source Evidence

The user directed in the parent task that collaboration subagents default to fork_turns none; a small positive number of recent turns is allowed only for conversation-only information unavailable in durable files or the dispatch prompt; and full inheritance is allowed only with an explicit task-specific justification. The user also required self-contained assignments, one concise launch announcement, and no routine progress receipts, heartbeat messages, lifecycle-history summaries, or repeated evidence messages.

## Requirements

- Make fork_turns none the default for every collaboration subagent launch.
- Permit a small positive number of recent turns only when the assignment depends on conversation-only information that is unavailable in durable files and cannot be stated adequately in the dispatch prompt.
- Permit fork_turns all only with an explicit task-specific justification recorded in the launch announcement.
- Require each collaboration assignment to state its objective, exact scope, relevant durable references, required checks, expected result, and prohibitions.
- Require one concise user-visible launch announcement containing the subagent name, assignment, and context inheritance. Include role and model only when overridden.
- Prohibit routine progress receipts, heartbeat messages, lifecycle-history summaries, and repeated evidence messages from collaboration subagents. Require only the final outcome or one specific decision the owning Agent cannot make.
- Keep separate user-visible Codex work-item tasks governed by explicit provider and task handoffs. Do not give those tasks implicit parent-conversation inheritance.
- Update codex-harness-directives, coordinate-codex-tasks, and conceptual Agents that directly dispatch collaboration subagents.
- Use repository-authorized generators for generated Agent projections and documentation.
- Preserve existing independent-review and fresh-context requirements; fresh context means no inherited conversation unless the bounded exception applies.

## Acceptance Criteria

- Focused contract checks prove collaboration launches default to fork_turns none.
- Positive-turn inheritance requires a stated conversation-only dependency and remains bounded to a small recent-turn count.
- Full inheritance requires an explicit task-specific justification.
- A launch assignment is invalid when it omits the objective, scope, durable references, checks, expected result, or prohibitions.
- Launch announcements contain only the required concise fields.
- Collaboration guidance does not reintroduce progress receipts, heartbeat messages, lifecycle reconstruction, or repeated durable evidence.
- Separate Codex work-item tasks retain explicit provider and canonical-task handoffs without implicit conversation inheritance.
- Generated Agent projections are current and focused tests pass.

## Dependencies

None.

## Verification

- Run focused Codex harness, task-coordination, conceptual-Agent, and generated-projection contract tests.
- Run the repository-authorized Agent projection generator and its freshness check.
- Run Git diff checks for the exact changed paths.

## Open Questions

None.

## Governed Definition Approval

### Governed Canonical Sources

- skills/codex-harness-directives/SKILL.md
- skills/coordinate-codex-tasks/SKILL.md
- agents/roles/dev-activities/dev-backlog-coordinator.role.yaml
- agents/roles/dev-activities/dev-orchestrator.role.yaml
- agents/roles/methodology-maintenance/methodology-maintainer.role.yaml
- agents/roles/methodology-maintenance/methodology-design-system-review-coordinator.role.yaml
- agents/roles/project-setup/project-bootstrapper.role.yaml
- agents/roles/wiki-activities/wiki-ingester.role.yaml
- agents/roles/wiki-activities/wiki-writer.role.yaml

### Allowed Dependent Artifacts

- scripts/test_bundle_content.py
- scripts/test_codex_task_control.py
- design/generated/role-definitions.js
- design/generated/skill-definitions.js
- generated/adapters/agent-generation-manifest.json
- Generated native Agent projections owned by scripts/build-skill-docs.py for the listed roles.

### Approval Resolution

Approved at creation by the user's explicit request to update Codex subagent-dispatch guidance, directly affected conceptual Agents, generated projections, and focused tests. Approval is limited to the exact governed sources and dependent artifacts listed above.

## Notes

- This item changes dispatch context, not the responsibility or authority of any Agent.
- The implementation should remain concise and centralized; role changes should reference the common rule rather than duplicate its full procedure.
