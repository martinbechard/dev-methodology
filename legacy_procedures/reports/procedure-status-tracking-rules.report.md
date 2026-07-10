# Status Tracking Rules Procedure Migration Report

## Source

Source procedure: [procedure-status-tracking-rules.md](../procedure-status-tracking-rules.md)

## Purpose And Scope

The procedure uses a Markdown status file as the working agreement for a
multi-step development or refactoring effort. Its durable intent is sound:
make work visible, decomposed, ordered, linked to its supporting artifacts,
and truthful about completion, blocking, and verification.

The original format predates the current backlog, claim, and multi-agent model.
It treats one manually maintained status file as the universal execution
authority and requires an interactive edit-confirm cycle around every subtask.
That is too narrow for current work: a backlog series is the appropriate
durable work map, child items hold executable scope and evidence, claims govern
concurrent ownership, and ordinary tool operations do not require human
confirmation between every state transition.

## Durable Guidance Worth Keeping

- Keep work visible in Markdown with enough context, references, dependencies,
  acceptance criteria, and verification for another agent to resume it safely.
- Decompose a larger goal into independently understandable, dependency-ordered
  work items. Use an index or other coordination artifact to preserve the goal,
  order, and links to those children.
- Write actions and requirements so they are specific and verifiable. Link
  known designs, code, tests, and other evidence rather than relying on chat
  history.
- Treat execution state as evidence-backed: an attempted command is not a
  completed result, and a blocked or not-applicable outcome needs an explicit
  reason.
- Make dependencies and verification steps visible before dispatching work.
- Reconcile summary state with the authoritative child work and its outcome;
  update the plan when discovery adds required work or changes a dependency.

## Mapping To The Current Catalog

| Procedure point | Destination | Coverage | Recommendation |
| --- | --- | --- | --- |
| Markdown status file as shared, resumable execution context | [create-backlog](../../skills/create-backlog/SKILL.md) and [manage-backlog](../../skills/manage-backlog/SKILL.md) | Strong for backlog work: Markdown items contain context, dependencies, verification, and visible lifecycle state. | Use typed active backlog items as the durable source of runnable work; retain a project-specific status file only when a local contract explicitly requires it. |
| Descriptive -status.md filename | Create Backlog filename and slug rules | Superseded: durable lowercase slugs intentionally avoid status words, while folder and state convey lifecycle. | Omit the suffix convention from portable guidance. |
| Phases, tasks, subplans, and a short main plan | Create Backlog related-item series; Manage Backlog series folders | Strong: index.md is the coordination artifact and linked child files are independently dispatchable work. | Preserve the goal-to-child decomposition. Do not use a 200-line or 5-7-subtask threshold; split when independent dispatch, ownership, or recovery benefits. |
| Imperative, single-action subtasks with source links | Create Backlog required item shape and writing rules | Strong | Keep current requirements, acceptance criteria, source-reference, and verification fields rather than checkbox-only lists. |
| Pending, active, in-progress, completed, N/A, and missing-design indicators | Manage Backlog state principles | Partial but better-defined: queued, claimed, running, blocked, target merge pending, completed, failed, and abandoned distinguish ownership from work and delivery outcomes. | Keep lifecycle semantics, not the emoji vocabulary. Add the rollup clarification below. |
| Exactly one active subtask; safe concurrent ownership | [agent-claim](../../skills/agent-claim/SKILL.md) and Manage Backlog dispatch workflow | Strong | Use exclusive, durable claims and isolated mutable workspaces. Do not encode agent ownership only in a status glyph. |
| Update status immediately before and after every action, with confirmation waits | Manage Backlog completion and recovery workflows; Agent Claim completion | Partial: current skills require evidence and recoverable state but deliberately do not prescribe a write-confirm loop for every command. | Narrow to meaningful lifecycle transitions: claim, start/resume, block, handoff, result evidence, and terminal archive. Respect explicit user approval gates, but do not manufacture them. |
| Main-plan checkbox mirrors subplan progress | Manage Backlog series-folder rules | Partial: child-item status is authoritative and the index must remain current, but the rollup rule is implicit. | Add an explicit child-to-series status-rollup rule. |
| Ordered execution, declared dependencies, and explicit verification | Create Backlog dependencies and verification; Manage Backlog dispatch and completion workflows | Strong | Keep the current dependency and evidence gates. Sequence only where dependencies require it; independent children may run in parallel with claims. |
| Review the initial plan and keep it current as discoveries occur | Create Backlog final check; Manage Backlog recovery and reporting workflows | Strong | Keep current validation, reconciliation, and recovery practices. |

## Coverage Assessment

The current catalog fully replaces the procedure's central function for durable
development work. Create Backlog supplies self-contained work packages and
series decomposition; Manage Backlog supplies evidence-based lifecycle,
dispatch, recovery, and archive behavior; Agent Claim supplies safe ownership
under parallel execution. The only material clarity gap is that Manage Backlog
states that an index must remain current without explicitly defining when a
series-level summary may be advanced from its child evidence.

This is an improvement to Manage Backlog, not a reason to create a generic
status-file skill. A generic tracker would duplicate the backlog lifecycle
model while losing its typed folders, dispatch constraints, recovery evidence,
and archive semantics.

## Precise Suggested Addition

### Manage Backlog

Add this paragraph under Series Folders, after the rules for child-item
outcomes:

> Treat child-item state, dependencies, and recorded evidence as authoritative
> for a series. Keep the index current as a summary, but never advance a
> series-level status from intent alone: show it as active only after at least
> one child is claimed or running, show it as blocked when a required child has
> an unmet dependency or recorded blocker, and show it as complete only after
> every required child has completed delivery evidence or has an explicitly
> recorded terminal abandonment. Reconcile the index after each meaningful
> child handoff or terminal outcome; do not require a status-file edit before
> and after every tool command.

No Create Backlog change is needed. Its series index, child linking,
dependencies, and self-contained verification contract already preserve the
useful planning shape.

## Agent Recommendations

- Keep [Backlog Steward](../../agents/roles/development-use/backlog-steward.role.yaml) as the owner of backlog creation, status transitions, recovery, and archive evidence.
- Keep [Development Orchestrator](../../agents/roles/development-use/development-orchestrator.role.yaml) as the owner of cross-agent decomposition, handoffs, claims, and integrated verification.
- Do not create a status-tracking agent. These responsibilities are already correctly divided between the two existing roles, with Agent Claim loaded where concurrent edits or resources are involved.

## Guidance To Omit Or Narrow

- Omit the mandatory -status.md suffix, universal Markdown checkbox format, and fixed emoji meanings. Lifecycle needs portable semantics, not a presentation-specific syntax.
- Omit the 200-line and 5-7-subtask thresholds. Split a plan according to independent dispatch, ownership, recovery, and navigation needs rather than arbitrary size.
- Omit the rule that exactly one plan subtask may be active. Parallel independent child items are valid when their files and resources are exclusively claimed.
- Omit mandatory read-diff-confirm waits before and after every command. They add latency and do not prevent races; claims, narrow writes, evidence, and reconciliation do.
- Narrow N/A and MISSING to the current terminal and blocked states. A blocked item needs its actual unmet dependency or reason, not a special design-only token.
- Omit the assumption that all work must execute in file order. Enforce declared dependencies and preserve intentional sequencing, while allowing safely independent work to proceed concurrently.
- Omit the procedure's dependency on refactoring-plan-gemini.md, which is neither present nor portable.

## Conclusion

Retire this procedure as a standalone distributed workflow. Preserve its
visibility, decomposition, traceability, dependency, verification, and honest
completion principles through Create Backlog, Manage Backlog, and Agent Claim.
Add one concise series-rollup paragraph to Manage Backlog, use the existing
Backlog Steward and Development Orchestrator roles, and do not add a new skill
or agent for status files.
