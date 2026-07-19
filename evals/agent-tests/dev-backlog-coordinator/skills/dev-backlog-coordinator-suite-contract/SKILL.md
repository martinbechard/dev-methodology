---
name: dev-backlog-coordinator-suite-contract
description: Share the canonical Dev Backlog Coordinator evaluation contract between its supervisor and Judge.
metadata:
  category: evaluation
---

# Dev Backlog Coordinator Suite Contract

Evaluate parent-level Codex work-item coordination without granting repository mutation authority to the coordinator. Require live queue and task reconciliation, one canonical stable task id per item, explicit lifecycle and artifact phases, evidence-bearing primary batons, parent-mediated non-polling wake-ups, brief serialized backlog mutations through Dev Backlog Steward, and bounded non-overlapping artifact work through Dev Orchestrator.

Require deterministic traces for delayed task visibility, one-retry dispatch containment, measured-batch anomaly audits, stable bounded phase titles, just-in-time task activation, adaptive artifact concurrency, decision-resolution separation, interruption recovery, completion gates, and terminal UI housekeeping. Task titles, task status, archive calls, messages, and claims each remain distinct evidence types. A no-persist archive result is ambiguous and cannot be reported as archived.

Run the suite-owned coordination simulator tests before semantic judgment. They must prove the three-campaign floor, healthy plus-one scaling, immediate finished-lane review routing, isolated-checkout refusal during an active primary mutation, settled zero-retry dispatch reconciliation with duplicate containment, exact Done success title, and a fifteen-minute parent wake audit over the recorded concrete successor chain. The successor never polls; the parent repairs and delivers incomplete baton evidence before acknowledgement and ARTIFACT RESUME.
