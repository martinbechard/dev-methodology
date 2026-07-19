# Add A Styled Backlog Report With User Input

Status: Proposed

Type: Feature

## Summary

Add a deterministic, self-contained HTML report that turns the repository backlog into an accessible operator view of features, defects, dependencies, lifecycle anomalies, and work that needs user interaction.

## Context

The current backlog is a primary-worktree-only queue under backlog. Work may be flat or grouped into series, and existing series can contain child items whose explicit Type differs from the parent folder name. A useful report must therefore read item metadata and queue rules rather than infer type only from directory placement.

The initial manually assembled report demonstrated summary metrics, status distribution, feature gates, ordered work lists, and lifecycle reconciliation. It also exposed the need for a repeatable source-backed report: repository state can advance while the report is being prepared, completed items can remain in an active folder, declared status can drift from dependency state, and current claims are separate from backlog eligibility.

[User Review queue guidance](../user-review/README.md) currently defines a separate non-dispatchable queue for work that needs a user decision, approval, action, authority grant, or information. [Rename User Review To User Action Required](../defect-backlog/rename-user-review-state-for-clarity.md) owns the canonical terminology correction. The report uses the resulting User Action Required state while the underlying Type remains Feature, Defect, Analysis, or Investigation. Present it with the display heading Needs Your Input and a short explanation so it is not mistaken for ordinary code or document review.

[Styled backlog report example](../examples/styled-backlog-report.html) is the committed visual and formatting reference for this feature. It includes the complete responsive styling and a formatted snapshot with the Needs Your Input section.

## Requirements

- Add a deterministic repository-owned command that reads the live backlog tree and produces a standalone HTML report without network access.
- Scan typed active folders, backlog/user-action-required, backlog/holding, completed archives, failed archives, series indexes, and applicable claim state according to the current create-backlog and manage-backlog contracts.
- Treat series index files and backlog/user-action-required/README.md as guidance or coordination artifacts rather than runnable work items.
- Classify work from its explicit Type, Status, queue folder, dependencies, and archive location. Do not infer Defect or Feature solely from the immediate parent directory.
- Show counts by underlying Type and lifecycle status, plus a separate count for items that need user input.
- Exclude User Action Required items from runnable, blocked, holding, and unattended-work counts.
- Render backlog/user-action-required under the display heading Needs Your Input with the explanation Waiting for a decision, approval, action, or information from you.
- Preserve the canonical User Action Required badge or status label alongside the clearer display heading.
- For every User Action Required item, show its underlying Type, exact Question for the User, current Resolution, and enough context to identify the requested interaction.
- Never infer a user answer, dispatch User Action Required work, or turn the report into an approval control.
- Show feature and defect items with title, declared status, summary, dependencies, series membership, recommended order when defined, and source path.
- Distinguish declared status from effective dispatch eligibility. Identify unmet dependencies, satisfied dependencies that leave stale blocked status, completed items still in active folders, invalid dependency identifiers, folder and Type mismatches, missing required fields, and unreadable items.
- Keep claim and worktree information separate from backlog lifecycle state. If claim state is shown, label it as a time-stamped workspace snapshot and do not silently convert claim contention into backlog status.
- Include the source commit, generation time, scanned folders, ignored guidance files, and validation findings so readers can judge freshness and scope.
- Produce deterministic ordering: queue category, series order when available, declared priority when introduced, then stable path or slug.
- Keep the report useful without JavaScript. Any optional interaction must progressively enhance a complete first render and remain keyboard accessible.
- Use self-contained responsive CSS with light and dark color support, readable contrast, visible text labels for every color encoding, and layouts that work from 320 pixels through desktop widths.
- Keep the generated report offline-capable and free of external fonts, scripts, stylesheets, telemetry, and API calls.
- Preserve backlog/examples/styled-backlog-report.html as the full formatted reference. Update the example whenever the report's visual contract changes materially.

## Acceptance Criteria

- One documented command produces a standalone report from the current primary-worktree backlog.
- Report counts match an independent inventory of active typed items, User Review items, holding items, and archived outcomes.
- A User Action Required item appears under Needs Your Input, retains its underlying Type, displays its exact question and resolution, and is absent from runnable and blocked totals.
- The user-action-required README and every series index are excluded from work-item counts.
- A Defect stored inside a feature series is counted as a Defect and is visibly flagged as a folder and Type mismatch when the queue contract requires separate typed placement.
- Runnable totals include only dispatchable states with satisfied dependencies and exclude claim-only, holding, completed, failed, abandoned, and User Review work.
- Lifecycle reconciliation identifies stale status, dependency, placement, and archive anomalies without rewriting source files.
- Every displayed item can be traced to its backlog source path.
- The report remains readable and unclipped at 320 pixels, 736 pixels, and a desktop viewport, in both light and dark color schemes.
- The report is usable with keyboard navigation and does not depend on color alone.
- The committed example contains the complete markup and styling needed to inspect the intended result offline.
- Repeated generation from unchanged inputs produces equivalent ordered content apart from explicitly time-varying snapshot metadata.

## Dependencies

- rename-user-review-state-for-clarity

## Verification

- Add focused fixtures covering flat items, series children, a series index, Defect and Feature types, User Action Required with an underlying Analysis type, holding, completed and failed archives, missing metadata, unresolved dependencies, and folder and Type mismatch.
- Verify exact counts, ordering, dependency eligibility, ignored guidance files, source paths, and anomaly messages against the fixtures.
- Verify that the User Action Required question and resolution are reproduced exactly and remain excluded from unattended-work selection.
- Compare a generated report with backlog/examples/styled-backlog-report.html for the required visual sections and responsive behavior.
- Open the example and a generated report locally at narrow, standard, and desktop widths in light and dark modes.
- Run the repository script tests and every applicable generated-output freshness check.
- Run git diff --check.

## Notes

- Needs Your Input is display language. backlog/user-action-required and Status: User Action Required are the target machine-readable queue contract owned by the dependency defect.
- The example is a visual reference, not the authoritative current backlog. Generated reports must always read live repository state.
- Do not add controls that imply an answer, approval, claim, archive movement, or dispatch unless a separate authorized workflow owns those mutations.
