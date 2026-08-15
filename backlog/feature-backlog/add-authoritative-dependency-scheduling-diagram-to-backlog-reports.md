# Add Authoritative Dependency Scheduling Diagram To Backlog Reports

Status: Ready

Type: Feature

Provider: file

Work Item ID: add-authoritative-dependency-scheduling-diagram-to-backlog-reports

Completion: main-branch

## Summary

Make every backlog report present a current, authoritative, validated inventory together with a Mermaid dependency and scheduling diagram that reconciles provider lifecycle, blockers, user decisions, ordered work, external dependencies, and crisis scheduling.

## Context

Current backlog coordination requires readers to reconstruct lifecycle counts, technical dependencies, ordered series, crisis priority, and external recovery state from separate records. A generated report can appear complete while omitting Ready work, repeating a resolved question, confusing a scheduling constraint with a technical dependency, or counting an uncommitted draft as an authoritative Work Item.

The report must read the current effective provider rather than infer state from task titles, runtime activity, working-tree drafts, or historical commentary. It must make discrepancies explicit without creating a second ledger.

## Source Evidence

On 2026-08-14 in the active Backlog Dispatcher conversation, the user explicitly requested one authoritative file-provider backlog item to improve the backlog report tool. The request requires a timestamped provider inventory and a Mermaid `flowchart LR` with status classes, source-backed dependency and scheduling edges, blocker and user-decision context, ordered-series coverage, external dependency treatment, crisis scheduling, count reconciliation, and focused report-contract tests.

## Requirements

- Read the current authoritative provider selected by project configuration for every report.
- Emit a short timestamped inventory with exact lifecycle counts and one Mermaid `flowchart LR` grouped into meaningful work domains.
- Render Running nodes in green, Ready and Starting nodes in blue, Blocked nodes in red, User Action Required nodes in amber, Completed nodes in gray, and external dependencies in purple or with an equally explicit external marker.
- Include one visible exact legend that explains every status class, the external marker, solid dependency edges, and dashed scheduling edges.
- Use solid edges only for source-backed technical, delivery, or ordered-series dependencies.
- Use dashed edges only for source-backed scheduling, crisis, or priority relationships.
- Give every current Blocked node its controlling reason in five words or fewer and reconcile the displayed Blocked count with the authoritative inventory.
- Give every User Action Required node its current pending decision and never repeat a resolved question.
- Include all current members of an ordered series and include completed predecessors when they materially explain the current state.
- Preserve verified external dependency status and edges while keeping external work outside local capacity counts.
- During crisis scheduling, identify the sole or highest-priority active item and show the next eligible preserved finish lane only when its gates are satisfied.
- Validate that the report contains exactly one node for every authoritative Work Item in scope, with its current stored status, and does not count uncommitted drafts or runtime-only tasks as Work Items.
- Reconcile node counts, lifecycle counts, archived-versus-active truth, and Ready inclusion.
- Explain any intentionally omitted Ready item from a bounded view.
- Output discrepancies only when authoritative provider, Git, dependency, or runtime evidence actually conflicts.
- Keep the provider record as the sole durable Work Item authority; do not create a report-side task ledger, dependency database, or lifecycle cache.

## Acceptance Criteria

- A generated report contains a timestamped authoritative inventory, exact lifecycle counts, one valid Mermaid `flowchart LR`, and the required legend sentence.
- Every authoritative Work Item in the report scope appears exactly once with its current stored status.
- Running, Ready, Starting, Blocked, User Action Required, Completed, and external nodes use the required distinct visual classes or marker.
- Every Blocked reason contains no more than five words and every User Action Required node shows only its unresolved current decision.
- Solid and dashed edges match the defined dependency-versus-scheduling semantics and are backed by provider or coordination evidence.
- Ordered series include all current members and explanatory completed predecessors.
- External dependencies remain outside local lifecycle and capacity counts.
- Crisis scheduling shows only truthfully eligible active and next work.
- Counts reconcile exactly across the textual inventory, diagram nodes, and authoritative provider.
- Uncommitted provider-like drafts and runtime-only tasks are excluded from authoritative Work Item counts.
- Mermaid syntax and the complete report contract validate successfully.

## Dependencies

None.

## Verification

- Add focused report-generator or reporting-tool tests that prove authoritative provider state takes precedence over task titles, runtime commentary, and uncommitted drafts.
- Test every required lifecycle class and the external marker.
- Test solid technical, delivery, and ordered-series edges separately from dashed scheduling, crisis, and priority edges.
- Test five-word Blocked reasons, current User Action Required decisions, and suppression of resolved questions.
- Test complete ordered-series membership including explanatory completed predecessors.
- Test verified external completion without adding the external item to local capacity.
- Test crisis sole-item and next-eligibility rendering.
- Test count reconciliation, Ready inclusion, and explicit explanations for intentionally omitted Ready work.
- Parse the emitted Mermaid and validate the node, edge, class, legend, and direction contract.
- Run the focused report-generator or reporting-tool suite, relevant bundle and freshness checks, and `git diff --check`.
- Obtain fresh independent source and artifact review before delivery.

## Open Questions

- Which existing report generator or backlog-report command is the smallest canonical implementation owner? Resolve through source discovery before mutation.
- Which stable domain grouping produces the clearest diagram without encoding a second taxonomy? Derive groups from authoritative Work Item scope and series evidence.

## Notes

- Token estimates shown by a report are planning estimates, not measured usage, cost, or billing evidence.
- A completed or external node is included only when it materially explains current dependency or scheduling state.
- Diagram presentation must not alter provider lifecycle or dependency authority.
