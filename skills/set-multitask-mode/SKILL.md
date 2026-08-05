---
name: set-multitask-mode
description: Enable dispatch to secondary threads after the condition requiring solo work has ended.
metadata:
  category: development-practice
---

# Set Multitask Mode

Use this skill when dispatch to secondary threads may resume after a condition requiring solo work has ended.

This procedure changes only the secondary-thread dispatch setting. It does not diagnose domain problems, select work-item states, or alter provider records.

## Set Mode

1. Determine whether the current runtime or coordination context has a secondary-thread dispatch mechanism.
2. When no secondary-thread dispatch mechanism is configured, return NOT_APPLICABLE without mutation.
3. Read the current dispatch setting before changing it.
4. When dispatch is already enabled, return ALREADY_MULTITASK without mutation.
5. Enable dispatch to secondary threads.
6. Verify that new secondary-thread dispatch is enabled for the intended coordination context.

Do not create, select, or launch secondary-thread work as part of changing the mode. Do not change capacity, priority, provider, or work-item state.

## Result

Return the coordination context, mechanism or absence of one, previous setting, effective setting, and exactly one result: ENABLED, ALREADY_MULTITASK, or NOT_APPLICABLE.
