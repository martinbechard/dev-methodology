# Agent Skill Lifecycle

## Goal

Make definition-owned skill loading, project technology detection, generated project guidance, harness-specific activation, behavioral verification, and interactive exploration coherent and truthful across supported runtimes.

## Purpose

Conceptual agent definitions declare their generic definition-owned skills. Project setup detects stable technology guidance for analyzed folders and records it in PROJECT.yaml and AGENTS.md. Runtime adapters express definition-owned skills according to their native semantics. Evaluation proves actual activation before the support checklist marks behavior verified. The mind map exposes these relationships and their evidence.

## Design Anchors

- Conceptual agent definition sources under agents/roles own generic definition-owned skills.
- Claude skills properties preload definition-owned skill content.
- Codex developer instructions require enabled skills to be discovered and loaded; skills.config is optional availability configuration, not preloading.
- Restrictive Claude tool allowlists must include Skill when dynamic folder skills are required.
- Technology detection runs during project setup, not on every coding or review task.
- PROJECT.yaml is the reviewable setup artifact.
- AGENTS.md is the operational folder guidance loaded during normal work.
- Behavior verification requires captured harness evidence rather than agent claims.

## Non-Goals

- Generating a project-local variant of every agent for every technology combination.
- Loading every bundled technology skill into every agent at startup.
- Treating availability configuration as proof that a skill was read.
- Marking manual observations as behavior-verified.

## Recommended Order

1. [Replace task-time routing with setup-time technology detection](replace-router-with-setup-detector.md).
2. [Verify Codex CLI skill activation](verify-codex-skill-activation.md).
3. [Document the cross-harness skill lifecycle](document-cross-harness-skill-lifecycle.md).
4. [Build the agent and skill mind map](build-agent-skill-mind-map.md).
5. [Align Project Organiser filename selection](align-project-organiser-filename-selection.md).
6. [Enforce behavioral regression assertions](enforce-behavioral-regression-assertions.md).
7. [Prevent unsupported review findings](prevent-unsupported-review-findings.md).
8. [Prevent unauthorized contract narrowing](prevent-unauthorized-contract-narrowing.md).
9. [Preserve authoritative configuration evidence](preserve-authoritative-configuration-evidence.md).
10. [Prevent read-only review side effects](prevent-read-only-review-side-effects.md).
11. [Require exact review quotation traceability](require-exact-review-quotation-traceability.md).
12. [Preserve canonical review checklists](preserve-canonical-review-checklists.md).
13. [Require claimed backlog resumption](require-claimed-backlog-resumption.md).
14. [Preserve Configurator runtime bridges](preserve-configurator-runtime-bridges.md).

The detector is the foundation. Codex verification must run against the stable generated definitions and project guidance. Documentation must distinguish designed behavior from behavior proven by the CLI suite. The mind map should consume the final detection and evidence data rather than adapting to an obsolete routing schema.

## Definition Of Good

- Definition-owned and detected-folder skills have distinct, explicit lifecycle semantics.
- Project setup creates durable, source-backed technology bindings.
- Codex behavior claims are backed by captured activation evidence.
- Claude preload and Skill tool requirements are represented accurately.
- Documentation and generated views agree with implementation.
- The mind map lets a user trace agents, skills, detection evidence, loading mode, harness behavior, and verification status.
