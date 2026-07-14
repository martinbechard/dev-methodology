---
name: organise-project-files
description: Determine and audit repository paths for new files and directories from live project guidance, the docs/project-taxonomy.md taxonomy, ownership, lifecycle, naming, and generated-output boundaries. Use before an agent creates a project file, chooses a destination or filename, extends a project taxonomy, mirrors a source file into tests, or audits whether generated artifacts were placed correctly.
metadata:
  category: development-practice
---

# Organise Project Files

Choose the destination before creating a file. Treat placement as a repository design decision grounded in current project evidence.

## Project Taxonomy

The project taxonomy is docs/project-taxonomy.md relative to the repository root. If the applicable project instructions name another taxonomy file, use that file instead. Read the complete taxonomy fresh before every placement decision.

Keep this structure:

- Project Taxonomy title: identifies the file as the repository placement authority.
- Conventions: defines ID prefixes and formats, filename casing, and test-mirroring rules.
- Top-Level Folder Principles: distinguishes repository, project, tool, sample, generated, and temporary ownership boundaries when the repository needs them.
- Categories: contains one entry per repository-relative directory or fixed filename. Each entry defines Purpose, Signals, and Filename pattern. Source categories may add Tests location; test categories may add Mirrors; entries may add Example.
- Change log: records taxonomy extensions newest first as date, category added, and one-line reason.

When docs/project-taxonomy.md is absent and project guidance names no alternative, use explicit repository conventions and report that no taxonomy exists. Create a taxonomy only when the user or project setup scope includes introducing one; do not invent it as a side effect of an ordinary placement decision.

## Placement Workflow

1. Apply the project instructions already in context and read any task-relevant placement procedure they reference.
2. Inspect the proposed content or a concrete description of it. Identify its purpose, owner, lifecycle, consumers, mutability, and whether it is source, test, fixture, configuration, documentation, generated output, cache, or operational evidence.
3. Read the project taxonomy described above when it exists. Also inspect adjacent files, repository shape, source and test roots, generated-file declarations, fixed filenames, and local naming patterns.
4. Apply explicit path bindings before general classification. A prescribed output path, colocated review-checklist rule, mirrored test rule, generator destination, or fixed project filename takes precedence over a broader taxonomy category.
5. Otherwise select the most specific category that matches the file purpose. Do not classify by extension alone.
6. Check the destination for collisions and overlapping artifacts. Reuse or update an existing file when it already owns the same purpose and the task permits editing it.
7. Choose the filename from local conventions. When the category uses numbered artifact IDs, inspect the complete target family and select the next free identifier without renumbering existing files.
8. If no category fits, update the project taxonomy before creating the file when project guidance permits autonomous taxonomy maintenance. If taxonomy changes require approval, return the proposed category and placement as a blocker instead of bypassing the taxonomy.
9. Audit the final choice against ownership, lifecycle, naming, source-versus-generated boundaries, and the nearest project guidance.

## Role Coordination

- When acting as Project Organiser, perform the classification directly and return the placement decision without creating the target file.
- When another role can delegate to Project Organiser, provide the proposed content or purpose and use its approved path before writing.
- When delegation is unavailable, apply this skill directly, then continue the larger task at the approved path.
- When the destination is already bound by explicit project guidance or a deterministic generator, confirm that binding and continue without a redundant placement consultation.

## Boundaries

- Read the taxonomy and nearby evidence fresh for each decision. Do not rely on remembered repository structure.
- Do not invent a new top-level folder while a specific existing category fits.
- Keep source files, generated outputs, caches, fixtures, reports, and runtime evidence in their declared ownership areas.
- Mirror source paths for tests only when the project test convention requires it.
- Do not move or rename existing files unless the request includes reclassification, relocation, or renaming.
- Do not use an external runtime wrapper solely to obtain a placement decision.
- Preserve unrelated files and local work when extending a taxonomy or resolving a collision.

## Result

Report:

- approved path and filename
- concise purpose-based rationale
- governing project evidence
- whether the taxonomy changed and what changed
- placement audit result or exact blocker
