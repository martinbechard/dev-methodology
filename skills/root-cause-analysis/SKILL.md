---
name: root-cause-analysis
description: Use when diagnosing a reproducible defect, failing test, runtime failure, data error, or recurrence risk before proposing or implementing a fix.
metadata:
  category: development-practice
---

# Root Cause Analysis

## Workflow

1. Reproduce one failure and capture the exact symptom, inputs, environment, and expected behavior.
2. Confirm that the expectation or test contract is valid.
3. Build a bounded evidence packet from source, tests, configuration, logs, processes, data, and recent changes.
4. Identify the earliest verified divergence between expected and actual behavior.
5. Test a small set of competing hypotheses and record disconfirming evidence.
6. State the mechanism-level cause, contributing conditions, and why existing controls did not catch it.
7. Propose the narrowest correction and a regression test or verification that would fail without it.
8. Check whether the cause can recur elsewhere before broadening the fix.

Use Code Execution Tracing for source paths and Runtime Evidence Collection for missing runtime facts. Do not patch first and call the patch an explanation.
