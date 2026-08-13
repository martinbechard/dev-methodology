<!--
{{COPYRIGHT}}
Artifact-ID: {{ARTIFACT_ID}}
Created-Local: {{CREATED_LOCAL}}
Creating-Agent: {{CREATING_AGENT}}
Runtime: {{RUNTIME}}
Dispatched-Model: {{DISPATCHED_MODEL}}
Reasoning-Effort: {{REASONING_EFFORT}}
-->

# TODO Project Wiki Methodology

## Current Understanding

> This section gives maintainers a shared starting point so they can choose the right wiki work without repeating discovery. Wiki maintainers use it during setup and maintenance to record the wiki's purpose, intended users, decisions it supports, and current state.

TODO: Describe why this project needs a maintained project wiki.

TODO: State which humans or agents will use the wiki and what decisions it should help them make.

TODO: State whether the wiki is already initialized, planned, partially maintained, or blocked by missing ownership decisions.

## Authoritative Sources

> This section prevents the wiki from becoming a competing source of truth. Wiki authors and reviewers use it when researching or resolving conflicting information to identify the controlling project sources and their precedence.

TODO: Link the installed route-documentation-work skill, project procedures, README files, source roots, test roots, backlog roots, existing docs, and wiki tooling that define how this wiki should work.

TODO: State which source wins when sources disagree.

## Related Code

> This section lets readers move from an explanation to the implementation surfaces they may need to inspect or change. Wiki readers and maintainers use it during navigation and maintenance to link the code, configuration, scripts, and source roots relevant to the wiki.

TODO: Link wiki helper scripts, source folders, test folders, configuration files, or local source links that the wiki uses for navigation or maintenance.

TODO: Say Not yet identified when no related code is known.

## Related Tests

> This section helps maintainers verify that wiki tooling and documented behavior still work as claimed. Wiki reviewers use it before accepting a wiki change to link the checks and tests that provide relevant evidence.

TODO: Link wiki lint commands, documentation checks, helper script tests, or sample sync verification commands.

TODO: Say Not yet identified when no related tests are known.

## Related Backlog Items

> This section preserves the delivery context behind wiki decisions so later readers can distinguish planned, active, and historical work. Coordinators and wiki maintainers use it during triage and maintenance to link the work items that affect this wiki.

TODO: Link active or historical backlog items that affect wiki setup, maintenance, automation, or documentation coverage.

TODO: Say Not yet identified when no related backlog item is known.

## Related Wiki Pages

> This section keeps knowledge discoverable across the wiki instead of duplicating it in one page. Wiki readers and maintainers use it while reading or updating this methodology to link pages that provide deeper context, shared definitions, decisions, defects, or history.

TODO: Link the wiki README, schema, topic index, glossary, open decisions, known defects, maintenance log, digest index, topic hubs, and subclass pages when they exist.

TODO: Say Not yet identified when no related wiki page is known.

## Open Questions

> This section makes unresolved decisions visible before they cause inconsistent pages or unsafe automation. Wiki planners and reviewers use it during planning and review to record questions that still need an owner or authoritative answer.

TODO: Record unresolved wiki ownership, source authority, sync cadence, automation, source-link, or page granularity questions.

TODO: If there are no unresolved questions, replace this section with a sentence saying no open questions are recorded.

## Maintenance Notes

> This section reduces future rediscovery by telling maintainers what events can make the methodology stale. Wiki maintainers use it after meaningful reviews or structural changes to record recheck triggers and the last relevant source review.

TODO: Record what future maintainers should recheck when wiki tooling, source roots, test roots, documentation folders, automation, or page subclass rules change.

TODO: Include the last meaningful source review when known.

## Wiki Root

> This section gives tools and contributors one predictable home and navigable layout for durable project knowledge. Wiki owners and tooling authors use it during initialization and structural review to define the root pages, folders, hubs, leaves, digests, and source-processing locations.

TODO: Confirm that the wiki lives at docs/wiki, or explain the project-specific exception.

TODO: List the required root pages, including README, schema, topic index, glossary, open decisions, known defects, and maintenance log.

TODO: Show the wiki root, hubs, leaves, digests, raw inputs, and processed-source locations as a fenced text tree whenever three or more paths share a prefix or span two or more folders. Do not repeat the docs/wiki prefix in a long list.

TODO: Path tree example (replace every synthetic page and folder with the project's complete wiki layout):

```text
docs/
└── wiki/
    ├── README.md
    ├── schema.md
    ├── topics/
    │   ├── topic-index.md
    │   └── feature/
    │       ├── index.md
    │       └── behavior.md
    ├── digests/
    └── raw/
        └── processed/
```

TODO: Add a short annotation or link index only for facts the tree cannot express; use leaf labels as visible text instead of repeating full paths.

TODO: When topic families need different owners or maintenance rules, split them into named subsections by topic family. Put one small fenced text tree in each subsection and its metadata immediately after the tree. Do not put multiline trees in Markdown table cells or simulate them with HTML breaks.

## Authority Order

> This section lets readers resolve disagreements without treating summaries or generated pages as stronger than their sources. Wiki authors and reviewers use it whenever sources conflict to state the project's precedence rules and the wiki's subordinate role.

TODO: List the source authority order for this project.

TODO: Include code, tests, functional specifications, procedures, architecture, high-level designs, module designs, backlog files, and generated documentation as applicable.

TODO: State that wiki pages summarize and navigate source material, but do not outrank the source material.

## Base Page Contract

> This section makes pages predictable for humans and automation, so essential evidence and maintenance context are not omitted. Wiki authors, reviewers, and tooling use it when creating or reviewing durable pages to define the shared sections every page must retain.

TODO: State that every durable documentation page starts with the shared wiki-compatible sections.

TODO: Include Current Understanding, Authoritative Sources, Related Code, Related Tests, Related Backlog Items, Related Wiki Pages, Open Questions, and Maintenance Notes.

TODO: State that the shared sections are the base page contract for topic pages and specialized documentation pages.

## Page Subclassing

> This section allows specialized documentation to grow without fragmenting the shared navigation and evidence contract. Template authors and wiki architects use it when adding a page type to explain how its extension sections follow the common base sections.

TODO: Define how this project adds specialized documentation pages without changing the base page contract.

TODO: State that specialized page templates keep the shared sections first, then append their own extension sections.

TODO: State that the project wiki template does not list every specialized page type. The specialized template owns its own extension sections.

## Diagram Policy

> This section helps readers understand relationships and flows that prose alone can obscure, while keeping diagrams maintainable. Wiki authors and reviewers use it when pages describe multi-step behavior, boundaries, structure, or data movement to decide when Mermaid or a companion rendering is required.

TODO: State that wiki pages must include an appropriate Mermaid diagram whenever they describe two or more ordered actions or phases, or any handoff, branch, retry, recovery path, state transition, lifecycle transition, or data movement. Prose, numbered lists, and tables may add detail but must not carry the complete sequence alone.

TODO: State that wiki pages include a structural diagram when an ownership, dependency, boundary, data, or verification node connects to two or more others, a path spans three or more nodes, a cycle exists, containment spans two or more levels, or an edge crosses a system, trust, or runtime boundary.

TODO: State that Mermaid is the default editable diagram source.

TODO: State when rendered SVG artifacts are allowed for review or publishing surfaces that cannot render Mermaid reliably.

TODO: State that linked SVG artifacts are companion artifacts and do not replace the editable source.

## Topic Pages

> This section keeps broad project knowledge decomposed into pages that readers can find, own, and maintain. Wiki architects and topic owners use it during information architecture work to define topic coverage, when a topic needs a hub, and how specialized documents supply deeper detail.

TODO: Describe the general topic pages this project needs.

TODO: State when a broad topic becomes a folder with an index page and granular leaf pages.

TODO: State how topic pages summarize current understanding and link specialized pages when specialized documents own deeper detail.

## Code Pages

> This section gives maintainers a durable map from system concepts to runtime and ownership surfaces. Code-aware wiki maintainers use it when organizing navigation to identify the code, tests, configuration, migrations, and generated artifacts that deserve dedicated coverage.

TODO: Describe how code ownership and runtime surfaces are mapped.

TODO: List the source folders, test folders, scripts, configuration folders, migrations, or generated artifacts that deserve wiki navigation.

## Local Source Link

> This section can make local source exploration convenient without creating nonportable tracked references. Wiki maintainers and local contributors use it during wiki setup to decide whether to add a local link, record its ignore rule, and preserve project-relative links in durable pages.

TODO: State whether the project should link its source folder into the wiki root.

TODO: If the project uses a local source link, record the link path and the .gitignore rule that prevents tracking it.

TODO: State that wiki pages should still use portable project-relative links for durable references.

## Daily Commit Sync

> This section defines how recent code changes become discoverable wiki-maintenance inputs without treating commit messages as truth. Automation owners and wiki maintainers use it when operating or configuring recurring sync to specify the scan boundary, classification, state tracking, and skip rules.

TODO: State whether the wiki should run a daily commit sync.

TODO: Define the commit range source, last processed commit record, raw scan artifact location, changed-file classification rules, and skip-recording rules.

TODO: State that commit messages are discovery hints and not sufficient authority.

## Update Workflow

> This section gives maintainers a repeatable path from detected change to verified documentation, reducing partial or inconsistent updates. Wiki maintainers use it for each maintenance pass to define source review, page updates, question handling, validation, and logging.

TODO: Describe the standard wiki update workflow.

TODO: Include status check, changed-file suggestion, authoritative source reading, page updates, related code updates, related test updates, open question handling, lint, and maintenance log updates.

## Automation

> This section makes automated maintenance auditable and bounds what each process may change. Automation owners and reviewers use it when scheduling or reviewing wiki jobs to record their triggers, commands, write scope, and prohibited effects.

TODO: List scheduled automation, manual commands, or agent workflows used to maintain the wiki.

TODO: State what each automation may write and what it must not write.

## Verification

> This section provides the evidence needed to trust that a wiki change is structurally valid, linked correctly, and operationally complete. Wiki reviewers and maintainers use it before accepting a maintenance pass to list the required checks and their expected results.

TODO: List the commands, lint checks, page review checks, link checks, and sample commit-sync checks required before a wiki maintenance pass is complete.

## Related Documents

> This section connects the methodology to the procedures and templates that govern its use, so maintainers can find the full operating contract. Wiki maintainers and reviewers use it during setup and review to link installed skills, project procedures, subclass templates, and existing wiki pages.

TODO: Link the installed documentation skills, project procedures, subclass templates used by this project, and existing wiki pages.
