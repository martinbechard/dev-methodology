# MCP Agent Ops 0.2.3 Live Acceptance

## Scope

- Date: 2026-07-16
- Harness: Codex CLI 0.144.1
- Model: gpt-5.6-terra
- Case: project-configuration-routing
- MCP release: mcp-agent-ops v0.2.3
- MCP release commit: 162f311c6e212b25ceca87891fbc8a2143a8af88
- Junie live execution: deferred by user direction

## Result

- Outcome: PASS
- The live Codex invocation completed all thirteen required MCP operations exactly once and in the declared order.
- skill_validate returned the required VALID outcome.
- skill_refresh returned the required CATALOG outcome.
- Runtime availability, batch skill loading, resource loading, technology detection, claim acquisition, status, extension, heartbeat, YAML verification, Markdown link verification, and claim release all returned their required bounded outcomes.
- The Git commit completed within the harness policy.
- Functional isolation was verified. The changed product paths exactly matched the seven allowed output paths, with no ephemeral or out-of-contract changes.

## Evidence Identities

- Installed runtime digest: 86e8d2b0af7fe421e88e3aec18e035b005c33474c4351332c9d31830908e5193
- Audit digest: 3efd514b4019f993d3b99bd45a46913e7c8ab71253ad657c7ac5ac4909a6a3aa
- Catalog manifest digest: eaf37f7ff324e630eb7b02f1338cc38fe3d513a9850f119383989f3fee6defe7
- Configuration digest: 5402f4eb857a67363650794d3960fe1b92bff296cae4aa91cdf143b9c6ab22f8
- Output manifest digest: 3a4eb5d7a842f168c4b06d33525917490afd703ca665b2ec97f64c31a79e15a3
- Workspace before digest: 6738eb05a850b9cef8573d8131a04ebb9bf1c155bf57e2d18e251eca6cfca1a7
- Workspace after digest: 413e124a2340fbee0874d362d4b206f56ff44e2579de56067ea321dae8ffdd5f

## Evidence Boundaries

This is a durable acceptance summary of a runner-validated live capture. It is not a complete version-two evidence receipt, a Model Judge result, a calibrated-Judge result, or a security-containment claim. The local permission profile and functional-isolation audit protected host state and bounded product mutations, but the result does not claim hostile-code containment. Exact generated-agent attribution is not promoted beyond the invocation contract without a complete receipt.
