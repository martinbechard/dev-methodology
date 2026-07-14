---
name: jhipster-project
description: Use when implementing, reviewing, testing, or regenerating a Java and Spring Boot JHipster application, including generator configuration, generated-code boundaries, build wrappers, profiles, and upgrade-safe changes.
metadata:
  category: stack-and-domain
---

# JHipster Project

Combine with Java and Spring Boot.

## Project Contract

- Inspect the generator version, .yo-rc.json, build files, package scripts, application profiles, and existing JHipster needles before changing generated areas.
- Treat JDL files and .jhipster entity definitions as generator inputs when they exist. Keep custom business behavior in the project-established extension points rather than relying on edits that regeneration will silently replace.
- Use the checked-in Maven or Gradle wrapper and package-manager lockfile. Preserve the generated build integration unless the task explicitly changes it.
- Keep development, test, and production profiles distinct. Change a shared default only when every affected profile and deployment path has been evaluated.
- Preserve generator needles and configuration anchors that later generation or upgrade steps require.

## Change Workflow

1. Record the current generator version and the files that own the requested behavior.
2. Decide whether the change belongs in generator inputs, generated output, or custom application code.
3. Run the narrow generator command only when generation is part of the requested change.
4. Inspect the complete generated diff before accepting it. Do not use a force option until overwrites are understood and recoverable.
5. Run the project-native backend and frontend checks affected by the change.

## Verification

- Verify that regeneration does not discard custom behavior or duplicate generated declarations.
- Verify the active development path and the production build path when profiles, build integration, or runtime configuration changed.
- Report the generator version, commands used, generated files changed, and any regeneration or upgrade risk.
