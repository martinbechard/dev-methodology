# Add A Styled Backlog Report With User Input

Status: Blocked

Type: Feature

## Running Ownership

- Owner: Dev Orchestrator root task 019f77f4-c4bd-7c91-b197-c987a7beb838.
- Lifecycle claim: styled-backlog-report-start.
- Claim evidence: dev-backlog-steward acquired PRIMARY ownership of this exact backlog item at 2026-07-19T05:50:37.189571Z before recording the Running transition.
- Scope boundary: the lifecycle claim is released after this committed transition; project-artifact ownership must be acquired separately after ARTIFACT GO.

## Blocked Evidence

- Outcome: The bounded two-attempt correction loop ended with a repeated runnable-eligibility acceptance failure. No implementation or documentation contribution was integrated.
- Preserved source commits: 381f09f557b7e73d07a9b735508687b2c27ac5f7, 8f7eb183846744180ee0ea3377ccbc7b072c5c60, and 32fd01a7fe214d7f5acb9a1ca2976073722c13ec on the report code branches.
- Preserved documentation commit: 69f0461f94c56737d696c6ad3adc2f71207df977 on the report README branch; its fresh independent artifact review passed with no findings.
- Source claim releases: 822386cf-efb3-4aed-a7a4-6a4e4c0b5a71, 2c50e789-9ca1-428c-83e1-55094bdfa46e, and ce635544-f131-40a3-a3c4-94ccdc7f0296. Documentation claim release: 9eae6030-78f9-415e-9333-8f523ef61c4e.
- Review evidence: The initial fresh review rejected unsafe active-completion dependency satisfaction, unreadable index handling, output collision handling, metadata and archive validation, and unavailable claim snapshots. Correction attempt one resolved those findings but a second fresh review found incomplete underlying-Type and Proposed migration handling. Correction attempt two resolved those findings, but the final fresh review proved that active Ready items with Type Holding or another invalid Type still entered Runnable Work.
- Passing evidence: Ten focused generator tests, Python compilation, Ruff, Mypy, controlled live generation, and git diff checks passed on the final preserved source commit. The full isolated Python 3.11 scripts run reached 411 tests with only the expected sparse-worktree failure caused by backlog omission.
- Remaining correction: In scripts/generate-backlog-report.py, runnable eligibility must require the explicit Type to be Defect, Feature, Analysis, or Investigation before an active Ready item can affect runnable totals or appear in Runnable Work. Add focused assertions proving Holding and invalid types remain visible as validation findings but are excluded from runnable counts and sections.
- Re-entry gates: After the remaining correction is committed by the original producer, repeat fresh independent source review. Only after review passes may the preserved README and source contributions be integrated, the primary example be updated, post-integration source and artifact or UX reviews run, complete primary verification pass, and browser accessibility checks run at 320 pixels, 736 pixels, and desktop widths in light and dark modes.

## Summary

Add a deterministic, self-contained HTML report that turns the repository backlog into an accessible operator view of features, defects, dependencies, lifecycle anomalies, and work that needs user interaction.

## Context

The current backlog is a primary-worktree-only queue under backlog. Work may be flat or grouped into series, and existing series can contain child items whose explicit Type differs from the parent folder name. A useful report must therefore read item metadata and queue rules rather than infer type only from directory placement.

The initial manually assembled report demonstrated summary metrics, status distribution, feature gates, ordered work lists, and lifecycle reconciliation. It also exposed the need for a repeatable source-backed report: repository state can advance while the report is being prepared, completed items can remain in an active folder, declared status can drift from dependency state, and current claims are separate from backlog eligibility.

[User Action Required queue guidance](../user-action-required/README.md) defines a separate non-dispatchable queue for work that needs a user decision, approval, action, authority grant, or information. [Rename User Review To User Action Required](../completed-backlog/defects/rename-user-review-state-for-clarity.md) owns the canonical terminology correction. The report uses User Action Required while the underlying Type remains Feature, Defect, Analysis, or Investigation. Present it with the display heading Needs Your Input and a short explanation so it is not mistaken for ordinary code or document review.

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
- Report counts match an independent inventory of active typed items, User Action Required items, holding items, and archived outcomes.
- A User Action Required item appears under Needs Your Input, retains its underlying Type, displays its exact question and resolution, and is absent from runnable and blocked totals.
- The user-action-required README and every series index are excluded from work-item counts.
- A Defect stored inside a feature series is counted as a Defect and is visibly flagged as a folder and Type mismatch when the queue contract requires separate typed placement.
- Runnable totals include only dispatchable states with satisfied dependencies and exclude claim-only, holding, completed, failed, abandoned, and User Action Required work.
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
