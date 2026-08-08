---
name: set-solo-mode
description: Disable dispatch to secondary threads while the current Agent continues work itself.
metadata:
  category: development-practice
---
<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: 792d36e6-5b37-4351-aeee-709c24a49ea1
Created-UTC: historical-unknown
Creating-Agent: historical-unknown
Runtime: historical-unknown
Dispatched-Model: historical-unknown
Reasoning-Effort: historical-unknown
Task-ID: historical-unknown
Artifact-ID-Evidence: migration-assigned
Created-UTC-Evidence: historical-unknown
Creating-Agent-Evidence: historical-unknown
Runtime-Evidence: historical-unknown
Dispatched-Model-Evidence: historical-unknown
Reasoning-Effort-Evidence: historical-unknown
Task-ID-Evidence: historical-unknown
-->

# Set Solo Mode

Use this skill when the current Agent must continue work without dispatching new work to secondary threads.

This procedure changes only the secondary-thread dispatch setting. It does not diagnose domain problems, select work-item states, or alter provider records.

Persistence and Commit selectors remain independent of the coordination mode. This procedure does not select or change either selector.

## Project Configuration Boundary

When PROJECT.yaml is absent from the repository root, the effective coordination mode is SOLO. Do not inspect or change a secondary-thread dispatch mechanism for this fallback. The current Agent continues the work itself.

A valid repository-root PROJECT.yaml replaces this fallback. When `project_setup` is present, use its validated `project_setup.concurrent_tasking` value:

- When project_setup.concurrent_tasking is false, keep secondary-thread dispatch disabled. If a configured mechanism has drifted to enabled, disable it and verify the correction.
- When project_setup.concurrent_tasking is true, temporarily disable the configured mechanism for the current coordination context.

A valid legacy configuration that passes the repository validation gate but has no `project_setup` remains supported. Preserve its configured runtime or coordination mechanism and apply the existing disable procedure; do not reinterpret the missing setup metadata as an unconfigured-project fallback.

If the root file exists but fails its applicable validation gate, do not infer a coordination mode or change dispatch. Return the validation failure to the owning workflow.

## Set Mode

1. Check for PROJECT.yaml at the repository root.
2. When the file is absent, use the effective SOLO fallback and return NOT_APPLICABLE without mutation.
3. Require the root file to pass its applicable validation gate.
4. If validated `project_setup.concurrent_tasking` is false, treat disabled dispatch as the configured target. If it is true, treat this request as a temporary override to SOLO. If valid legacy configuration omits `project_setup`, preserve its existing configured mechanism.
5. Determine whether the applicable runtime or coordination context has a secondary-thread dispatch mechanism.
6. When no secondary-thread dispatch mechanism is configured, return NOT_APPLICABLE without mutation.
7. Read the current dispatch setting before changing it.
8. When dispatch is already disabled, return ALREADY_SOLO without mutation.
9. Disable dispatch to secondary threads.
10. Verify that new secondary-thread dispatch is disabled for the intended coordination context.

Do not cancel, interrupt, reassign, or otherwise alter work already running in secondary threads. Do not stop the current Agent from continuing the work itself. Do not launch work as part of changing the mode.

## Result

Return the coordination context, mechanism or absence of one, previous setting, effective setting, and exactly one result: DISABLED, ALREADY_SOLO, or NOT_APPLICABLE.
