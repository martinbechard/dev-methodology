---
name: name-methodology-artifacts
description: Name or rename methodology agent categories, canonical roles, and distributed skills with subject-based category membership, predictable prefixes, actor nouns, and object- or action-centered naming patterns. Use when creating, reviewing, grouping, or renaming agent categories, role definitions, skill categories, skill directories, or cross-references to those identifiers.
metadata:
  category: documentation-methodology
---

# Name Methodology Artifacts

Apply the naming rules before creating an identifier and during any catalog-wide rename.

## Name Agent Categories

- Start every category title with a short, distinctive word that is unique among agent categories.
- Use that first word as the required prefix for every role in the category.
- Prefer a broad nickname that still describes the category. Use Dev for general development work because it covers more than code alone.
- Keep category titles stable after their prefix is published.
- Reject a proposed category when its first word duplicates or could be confused with another category prefix.

Examples of aligned category prefixes include Methodology, Project, Wiki, and Dev.

## Name Roles

- Start every canonical role name with its category prefix.
- Describe an actor: a person or persona that performs the responsibility.
- Use a singular role noun such as maintainer, organiser, researcher, writer, reviewer, verifier, collector, coder, diagnostician, steward, coordinator, or orchestrator.
- Do not use agent anywhere in the role name.
- Do not end at an object or action noun when an actor form exists. Use wiki-researcher instead of wiki-research and wiki-verifier instead of wiki-verification.
- Keep the distinctive part short enough to scan in dispatch lists.
- Use or only when the role intentionally owns both personas and splitting the responsibility would weaken the operating model.

Examples include dev-coder, dev-code-reviewer, dev-backlog-steward, dev-orchestrator, methodology-maintainer, project-organiser, wiki-researcher, and wiki-topic-verifier.

## Name Skills

Choose category membership and naming pattern separately.

- Determine category membership from the skill's subject area and responsibility.
- Each skill category mostly follows one naming pattern, but this is not an absolute rule.
- Use best judgment to choose the most appropriate category and keep a naming-pattern exception when it expresses the skill's purpose more clearly for a good reason.
- Treat the naming pattern as a word-order convention, not as the definition of category membership.
- For an object-centered naming pattern, put the shared object first and the operation last. Use a base verb for the operation. Examples include project-wiki-create, project-wiki-query, project-wiki-research, project-wiki-topic-write, and project-wiki-topic-verify.
- For an action-centered naming pattern, put the shared verb first and the target object last. Examples include create-architecture, create-functional-spec, review-architecture, and review-functional-spec.
- Use verbs for operations, not actor nouns. Reserve writer, reviewer, and verifier forms for roles.
- Keep a well-scoped domain exception when its leading words express a distinct subject rather than an operation. Code-project-wiki is the code-project variant of project-wiki and may remain an exception.
- Do not rename a skill only to force superficial symmetry with the predominant pattern in its category.

## Apply A Rename

1. Inventory category titles and prefixes, canonical role names and filenames, skill directories and frontmatter names, role loadouts, companion-skill references, metadata, generated outputs, documentation, examples, tests, and explicit deployment manifests.
2. Choose the complete old-to-new map before moving files.
3. Rename canonical sources first. Keep each role name, filename field, source filename, skill directory, and skill frontmatter name aligned.
4. Update every source reference to the new identifiers and sweep for stale names.
5. Regenerate derived documentation and runtime adapters.
6. Run catalog validation, regression tests, and stale-output checks.
7. Sweep again for old identifiers and inspect generated adapter inventories for stale names.

Do not leave compatibility aliases unless the owning project explicitly requires a migration period.
