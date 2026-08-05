---
name: set-solo-mode
description: Disable dispatch to secondary threads while the current Agent continues work itself.
metadata:
  category: development-practice
---

# Set Solo Mode

Use this skill when the current Agent must continue work without dispatching new work to secondary threads.

This procedure changes only the secondary-thread dispatch setting. It does not diagnose domain problems, select work-item states, or alter provider records.

## Set Mode

1. Determine whether the current runtime or coordination context has a secondary-thread dispatch mechanism.
2. When no secondary-thread dispatch mechanism is configured, return NOT_APPLICABLE without mutation.
3. Read the current dispatch setting before changing it.
4. When dispatch is already disabled, return ALREADY_SOLO without mutation.
5. Disable dispatch to secondary threads.
6. Verify that new secondary-thread dispatch is disabled for the intended coordination context.

Do not cancel, interrupt, reassign, or otherwise alter work already running in secondary threads. Do not stop the current Agent from continuing the work itself. Do not launch work as part of changing the mode.

## Result

Return the coordination context, mechanism or absence of one, previous setting, effective setting, and exactly one result: DISABLED, ALREADY_SOLO, or NOT_APPLICABLE.
