---
name: agent-suite-supervision
description: Coordinate one agent-owned evaluation suite with frozen inputs, exactly one active child at a time, deterministic gates, independent judging, and durable terminal evidence.
metadata:
  category: evaluation
---

# Agent Suite Supervision

Use this project skill only for supervising an agent suite under evals/agent-tests.

## Workflow

1. Load the active suite's suite.yaml manifest and exactly one selected scenario from that suite's authoritative scenarios.yaml catalog. Treat suite.yaml scenarioCatalog as invalid when it names another file.
2. Verify the canonical role, native adapter, fixture, project agents, and project skills named by the manifest.
3. Resolve fixed and conditional target skills against the frozen task and allowed writes, then verify that every applicable skill is available to the target. Return preflight BLOCKED when one is missing; do not ask the target to work around the missing skill.
4. Freeze their digests, the applicable target-skill rule excerpts, and the allowed input, write, command, delegation, and terminal-status contracts. Obtain each digest directly from the hashing command output, validate it as exactly 64 lowercase hexadecimal characters, and rehash the named file before both target and Judge dispatch. Never shorten or manually transcribe a digest into an authority packet.
5. Invoke exactly one child: the standard target agent named by the suite. In Codex V1, pass agent_type exactly equal to targetInvocation and fork_context exactly false so the registered custom config is applied; a scenario label or inherited context creates an invalid identity and is an infrastructure failure. Supply the complete frozen task and authority packet in the child message.
6. Verify the direct spawn receipt and registered custom-agent type before accepting the child result. When the live supervisor API does not expose retained runtime developer input or a nested child's parent binding, preserve the exact target and dependency receipts, mark that evidence conditionally pending the runner post-audit, and continue to semantic judging. The runner must reject the batch if its retained-session audit later finds a missing binding or undeclared dependency. Do not treat the task label, child path, or final response alone as identity proof.
7. Capture governed evidence and finish that child before starting another. When a scenario or rubric depends on operation order, exactly-once execution, or absence of prohibited tools, network use, or delegation, include every supervisor-observable receipt and artifact transition in the Judge packet. The runner owns the final ordered target tool-call trace and retained-session audit when that raw trace is unavailable inside the supervisor context. Target self-report may identify evidence for that later audit but is not final trace proof by itself.
8. Run deterministic checks. Stop on a critical failure available at the supervisor boundary, including a missing direct spawn receipt or a receipt that names the wrong custom agent. A clearly recorded runner-owned post-audit obligation is not itself a critical failure.
9. Invoke the hardcoded suite Judge in a fresh context with the canonical role and every frozen rule excerpt needed to evaluate claims made under assigned target skills. In Codex V1, pass agent_type exactly equal to judgeInvocation and fork_context exactly false, then supply the complete Judge packet in the child message.
10. Verify the Judge direct spawn receipt before accepting its verdict and leave loaded-instruction binding to the same mandatory runner post-audit when the supervisor cannot inspect it directly.
11. Record PASS, FAIL, BLOCKED, or STALE and preserve the evidence needed to reproduce that classification.
12. Before starting another scenario or returning, write the terminal scenario result as JSON under the runner-provided checkpointRoot at suite-id/scenario-id.json. The object must contain suite, scenario, status, targetInvoked, judgeInvoked, identityEvidence as an array of strings, evidence as an array of strings, cleanup as clean or failed, and residualRisk as a string. Do not use nested objects for identityEvidence, evidence, or cleanup. This external runner-owned checkpoint is required even when later work may fail and must agree with the terminal response.
13. Clean every suite-owned resource.

When a supervisor-owned assertion command fails because of quoting, globbing, path construction, or another harness error, record the failed command as infrastructure evidence without classifying the target. Correct the command once, rerun the same frozen assertion, and preserve both outcomes. Do not weaken or replace the assertion after target execution.

Concurrent supervisors share one disposable batch workspace. Scope mutation assertions to the frozen scenario inputs, declared write boundary, task-owned resources, and retained session provenance. Do not use repository-global status as the sole mutation gate. Record concurrent out-of-suite changes as infrastructure evidence, preserve them, and never attribute or clean them without ownership proof.

## Finding Disposition

- During the run, record findings without editing the frozen scenario, target agent, distributed skill, generated adapter, or product implementation.
- Correct only test infrastructure such as a fixture, runner, staged project-agent definition, identity gate, deterministic assertion, Judge packet, evidence capture, or cleanup contract, and only through an authorized maintenance pass. Rerun the same frozen check afterward.
- Send agent-definition, distributed-skill, generated-target, and product-behavior findings to Dev Backlog Steward with the governed evidence reference. Use the configured backlog backend and ask the user when no backend is selected.
- Do not create a second backlog representation and do not patch the subject under test to manufacture a passing result.

## Concurrency

- Keep exactly one active child.
- Do not overlap target execution, evidence work, judging, or correction.
- Permit one nested child only when the suite manifest and canonical target definition both require that dependency.
- Wait for the nested child to finish before the active child continues or another dependency starts.

## Boundaries

- Do not evaluate another suite.
- Do not substitute a generic worker, alternate Judge, or unlisted skill.
- Do not change the scenario or rubric after target execution begins.
- Do not award semantic credit yourself.
- Do not claim PASS from a final response without matching trace and artifact evidence.
- For Codex, use underscore-safe custom-agent names, an isolated Codex home, and retained session identity metadata.
- For mutation scenarios, use a disposable permission profile that permits both declared worktree files and required Git metadata.

## Result

Return the suite, scenario, frozen digests, target and dependency identities, deterministic results, Judge verdict, terminal status, evidence locations, cleanup result, and residual risk. The terminal response and the runner-owned checkpoint must agree.
