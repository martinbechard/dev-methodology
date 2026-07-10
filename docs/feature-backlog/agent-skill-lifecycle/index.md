# Agent Skill Lifecycle

## Goal

Make fixed-role skill loading, project technology detection, generated project guidance, harness-specific activation, behavioral verification, and interactive exploration coherent and truthful across supported runtimes.

## Purpose

Canonical roles know their generic fixed-role skills. Project setup detects stable technology guidance for analyzed folders and records it in AGENTS-PLAN.yaml and AGENTS.md. Runtime adapters express fixed-role skills according to their native semantics. Evaluation proves actual activation before the support checklist marks behavior verified. The mind map exposes these relationships and their evidence.

## Design Anchors

- Canonical role files under agents/roles own fixed-role generic skills.
- Claude skills properties preload fixed-role skill content.
- Codex developer instructions require enabled skills to be discovered and loaded; skills.config is optional availability configuration, not preloading.
- Restrictive Claude tool allowlists must include Skill when dynamic folder skills are required.
- Technology detection runs during project setup, not on every coding or review task.
- AGENTS-PLAN.yaml is the reviewable setup artifact.
- AGENTS.md is the operational folder guidance loaded during normal work.
- Behavior verification requires captured harness evidence rather than agent claims.

## Non-Goals

- Generating a project-local variant of every canonical agent for every technology combination.
- Loading every bundled technology skill into every agent at startup.
- Treating availability configuration as proof that a skill was read.
- Marking manual observations as behavior-verified.

## Recommended Order

1. [Replace task-time routing with setup-time technology detection](replace-router-with-setup-detector.md).
2. [Verify Codex CLI skill activation](verify-codex-skill-activation.md).
3. [Document the cross-harness skill lifecycle](document-cross-harness-skill-lifecycle.md).
4. [Build the agent and skill mind map](build-agent-skill-mind-map.md).

The detector is the foundation. Codex verification must run against the stable generated definitions and project guidance. Documentation must distinguish designed behavior from behavior proven by the CLI suite. The mind map should consume the final detection and evidence data rather than adapting to an obsolete routing schema.

## Definition Of Good

- Fixed-role and detected-folder skills have distinct, explicit lifecycle semantics.
- Project setup creates durable, source-backed technology bindings.
- Codex behavior claims are backed by captured activation evidence.
- Claude preload and Skill tool requirements are represented accurately.
- Documentation and generated views agree with implementation.
- The mind map lets a user trace agents, skills, detection evidence, loading mode, harness behavior, and verification status.
