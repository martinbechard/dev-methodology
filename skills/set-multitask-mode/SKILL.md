---
name: set-multitask-mode
description: Enable dispatch to secondary threads after the condition requiring solo work has ended.
metadata:
  category: development-practice
---
<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
Artifact-ID: e8edc1ee-3dd9-4a6e-9925-32185f02f513
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

# Set Multitask Mode

Use this skill when dispatch to secondary threads may resume after a condition requiring solo work has ended.

This procedure changes only the secondary-thread dispatch setting. It does not diagnose domain problems, select work-item states, or alter provider records.

Persistence and Commit selectors remain independent of the coordination mode. This procedure does not select or change either selector.

## Project Configuration Boundary

When PROJECT.yaml is absent from the repository root, do not enable secondary-thread dispatch. The effective coordination mode remains SOLO without a dispatch-mechanism read or mutation.

A valid repository-root PROJECT.yaml replaces this fallback. Re-evaluate the configuration on each later request; do not cache the missing-file result. When `project_setup` is present, use its validated `project_setup.concurrent_tasking` value:

- When project_setup.concurrent_tasking is false, do not enable secondary-thread dispatch. Return NOT_APPLICABLE without reading or mutating a dispatch mechanism.
- When project_setup.concurrent_tasking is true, enable the configured mechanism after the condition requiring SOLO ends.

A valid legacy configuration that passes the repository validation gate but has no `project_setup` remains supported. Preserve its configured runtime or coordination mechanism and apply the existing enable procedure; do not reinterpret the missing setup metadata as an unconfigured-project fallback.

If the root file exists but fails its applicable validation gate, do not infer configured behavior or change dispatch. Return the validation failure to the owning workflow.

## Set Mode

1. Check for PROJECT.yaml at the repository root.
2. When the file is absent, preserve the effective SOLO fallback and return NOT_APPLICABLE without mutation.
3. Require the root file to pass its applicable validation gate.
4. If validated `project_setup.concurrent_tasking` is false, return NOT_APPLICABLE without reading or mutating a dispatch mechanism. If it is true, continue. If valid legacy configuration omits `project_setup`, preserve its existing configured mechanism and continue.
5. Determine whether the applicable runtime or coordination context has a secondary-thread dispatch mechanism.
6. When no secondary-thread dispatch mechanism is configured, return NOT_APPLICABLE without mutation.
7. Read the current dispatch setting before changing it.
8. When dispatch is already enabled, return ALREADY_MULTITASK without mutation.
9. Enable dispatch to secondary threads.
10. Verify that new secondary-thread dispatch is enabled for the intended coordination context.

Do not create, select, or launch secondary-thread work as part of changing the mode. Do not change capacity, priority, provider, or work-item state.

## Result

Return the coordination context, mechanism or absence of one, previous setting, effective setting, and exactly one result: ENABLED, ALREADY_MULTITASK, or NOT_APPLICABLE.
