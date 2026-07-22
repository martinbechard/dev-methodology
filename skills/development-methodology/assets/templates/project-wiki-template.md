<!--
Copyright (c) 2025 Martin Bechard [martin.bechard@DevConsult.ca]
This software is licensed under the MIT License.
File path: skills/development-methodology/assets/templates/project-wiki-template.md
1-line summary: Template for project wiki setup and code-aware maintenance.
-->

# TODO Project Wiki Methodology

## Current Understanding

TODO: Describe why this project needs a maintained project wiki.

TODO: State which humans or agents will use the wiki and what decisions it should help them make.

TODO: State whether the wiki is already initialized, planned, partially maintained, or blocked by missing ownership decisions.

## Authoritative Sources

TODO: Link the installed development-methodology skill, project procedures, README files, source roots, test roots, backlog roots, existing docs, and wiki tooling that define how this wiki should work.

TODO: State which source wins when sources disagree.

## Related Code

TODO: Link wiki helper scripts, source folders, test folders, configuration files, or local source links that the wiki uses for navigation or maintenance.

TODO: Say Not yet identified when no related code is known.

## Related Tests

TODO: Link wiki lint commands, documentation checks, helper script tests, or sample sync verification commands.

TODO: Say Not yet identified when no related tests are known.

## Related Backlog Items

TODO: Link active or historical backlog items that affect wiki setup, maintenance, automation, or documentation coverage.

TODO: Say Not yet identified when no related backlog item is known.

## Related Wiki Pages

TODO: Link the wiki README, schema, topic index, glossary, open decisions, known defects, maintenance log, digest index, topic hubs, and subclass pages when they exist.

TODO: Say Not yet identified when no related wiki page is known.

## Open Questions

TODO: Record unresolved wiki ownership, source authority, sync cadence, automation, source-link, or page granularity questions.

TODO: If there are no unresolved questions, replace this section with a sentence saying no open questions are recorded.

## Maintenance Notes

TODO: Record what future maintainers should recheck when wiki tooling, source roots, test roots, documentation folders, automation, or page subclass rules change.

TODO: Include the last meaningful source review when known.

## Wiki Root

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

TODO: List the source authority order for this project.

TODO: Include code, tests, functional specifications, procedures, architecture, high-level designs, module designs, backlog files, and generated documentation as applicable.

TODO: State that wiki pages summarize and navigate source material, but do not outrank the source material.

## Base Page Contract

TODO: State that every durable documentation page starts with the shared wiki-compatible sections.

TODO: Include Current Understanding, Authoritative Sources, Related Code, Related Tests, Related Backlog Items, Related Wiki Pages, Open Questions, and Maintenance Notes.

TODO: State that the shared sections are the base page contract for topic pages and specialized documentation pages.

## Page Subclassing

TODO: Define how this project adds specialized documentation pages without changing the base page contract.

TODO: State that specialized page templates keep the shared sections first, then append their own extension sections.

TODO: State that the project wiki template does not list every specialized page type. The specialized template owns its own extension sections.

## Diagram Policy

TODO: State that wiki pages must include an appropriate Mermaid diagram whenever they describe two or more ordered actions or phases, or any handoff, branch, retry, recovery path, state transition, lifecycle transition, or data movement. Prose, numbered lists, and tables may add detail but must not carry the complete sequence alone.

TODO: State that wiki pages include a structural diagram when an ownership, dependency, boundary, data, or verification node connects to two or more others, a path spans three or more nodes, a cycle exists, containment spans two or more levels, or an edge crosses a system, trust, or runtime boundary.

TODO: State that Mermaid is the default editable diagram source.

TODO: State when rendered SVG artifacts are allowed for review or publishing surfaces that cannot render Mermaid reliably.

TODO: State that linked SVG artifacts are companion artifacts and do not replace the editable source.

## Topic Pages

TODO: Describe the general topic pages this project needs.

TODO: State when a broad topic becomes a folder with an index page and granular leaf pages.

TODO: State how topic pages summarize current understanding and link specialized pages when specialized documents own deeper detail.

## Code Pages

TODO: Describe how code ownership and runtime surfaces are mapped.

TODO: List the source folders, test folders, scripts, configuration folders, migrations, or generated artifacts that deserve wiki navigation.

## Local Source Link

TODO: State whether the project should link its source folder into the wiki root.

TODO: If the project uses a local source link, record the link path and the .gitignore rule that prevents tracking it.

TODO: State that wiki pages should still use portable project-relative links for durable references.

## Daily Commit Sync

TODO: State whether the wiki should run a daily commit sync.

TODO: Define the commit range source, last processed commit record, raw scan artifact location, changed-file classification rules, and skip-recording rules.

TODO: State that commit messages are discovery hints and not sufficient authority.

## Update Workflow

TODO: Describe the standard wiki update workflow.

TODO: Include status check, changed-file suggestion, authoritative source reading, page updates, related code updates, related test updates, open question handling, lint, and maintenance log updates.

## Automation

TODO: List scheduled automation, manual commands, or agent workflows used to maintain the wiki.

TODO: State what each automation may write and what it must not write.

## Verification

TODO: List the commands, lint checks, page review checks, link checks, and sample commit-sync checks required before a wiki maintenance pass is complete.

## Related Documents

TODO: Link the installed documentation skills, project procedures, subclass templates used by this project, and existing wiki pages.
