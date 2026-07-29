# Incorporate the Document Topic Editor and Topic Skills

Status: Ready

Type: Feature

Owner: Unowned

Provider: file

Provider Reference: backlog/feature-backlog/document-topic-revision/incorporate-document-topic-agent-and-skills.md

Completion: direct-main

Series: backlog/feature-backlog/document-topic-revision/index.md

## Resumption Record

Transition: User Action Required -> Ready.

Recorded At: 2026-07-29T02:42:17Z.

Direct User Direction and Provenance: In the parent coordination thread on 2026-07-29, the user said: “If something OTHER than what I asked is needed, THEN we need more approval. Cleanup the workitem then get to it.”

Resolution: The existing work item authorizes mutation of exactly these governed definitions: skills/analyze-document-topics/SKILL.md; skills/revise-document-topics/SKILL.md; skills/analyze-document-topics/agents/openai.yaml; skills/revise-document-topics/agents/openai.yaml; and agents/roles/dev-activities/dev-document-topic-editor.role.yaml.

Artifact Policy: Caller-requested only; do not retain a durable before-and-after topic-analysis artifact unless the caller requests it.

Approval Boundary: Any additional skill, agent, metadata, schema, or other governed definition outside the exact five-path manifest requires new explicit, scope-specific user approval before mutation.

Superseded Clarification: The prior User Action Required gate incorrectly stated that work-item authorization did not authorize the requested five definitions. It is retained below as history only. This direct user direction supersedes that assertion.

Required Next Lifecycle Transition: The parent Dev Backlog Coordinator may reserve this same canonical task through Ready -> Starting. The canonical task's root Dev Orchestrator must then record Starting -> Running before any preflight, definition, source, generated, test, or other repository mutation.

## Preserved Dispatch Reservation History

Parent Coordination Thread: 019fa9bb-1423-7e80-bcde-3caa765e3758

Canonical Work-Item Thread: 019fab9e-44bf-7571-9fbb-d9d63d3fa9da

Canonical Root Agent Task: 019fab9e-44bf-7571-9fbb-d9d63d3fa9da

Launch Reservation: One bounded live handshake for the canonical work-item Thread.

Dispatch Time: 2026-07-29T02:10:25.998414Z

Normalized Objective: Incorporate the Document Topic Editor and Topic Skills.

Intended Root Role: Dev Orchestrator

Branch: codex/incorporate-document-topic-agent-and-skills-019fab9e

Worktree: /Users/martinbechard/.codex/worktrees/350a/dev-methodology

Observed Launch Evidence: Parent Dev Backlog Coordinator authorized one bounded launch reservation for canonical Runtime Thread and root Agent Task 019fab9e-44bf-7571-9fbb-d9d63d3fa9da; this transaction preserves Owner as Unowned pending root acceptance.

Dependencies Observed: None.

Required Next Lifecycle Transition: The same canonical task's root Dev Orchestrator must record Starting to Running before governed-scope discovery, definition approval, or implementation mutation.

## Preserved Running Evidence

Transition: Starting -> Running.

Root Dev Orchestrator: Root Dev Orchestrator for canonical task 019fab9e-44bf-7571-9fbb-d9d63d3fa9da.

Canonical Work-Item Thread: 019fab9e-44bf-7571-9fbb-d9d63d3fa9da.

Canonical Root Agent Task: 019fab9e-44bf-7571-9fbb-d9d63d3fa9da.

Branch: codex/incorporate-document-topic-agent-and-skills-019fab9e.

Worktree: /Users/martinbechard/.codex/worktrees/350a/dev-methodology.

Started At: 2026-07-29T02:13:56Z.

Phase: Analyzing.

Starting Reservation Commit: 2afc03e64d8ed45053900e8ae1e12a1055d8e6f4.

Claim Evidence: SHARED_CHECKOUT_ACQUIRED claim starting-running-019fab9e-44bf-7571-9fbb-d9d63d3fa9da; incarnation 687e34f1-ab98-4b88-8625-6144c6985975; claim journal event 15b4f135-6274-42d0-822b-cb89d25c4968; exact path backlog/feature-backlog/document-topic-revision/incorporate-document-topic-agent-and-skills.md in the primary main checkout.

## Superseded User Action Required Clarification

Question: Do you explicitly approve creating exactly the five governed definitions listed above for the read-only analyze-document-topics skill, the separately authorized revise-document-topics skill, and the conceptual Document Topic Editor—and, for each revision, should the durable before-and-after topic-analysis artifact be recorded by default or only when the caller requests it?

Why User Approval Was Requested: The prior provider record treated backlog creation and dispatch as insufficient approval. The later direct user direction recorded in Resumption Record supersedes that conclusion for the exact five-path manifest only.

Options and Consequences:

- A. Approve + record by default: permits exact approval records and preflights, bounded implementation, supported same-category regeneration, ordinary tests, evaluation, and documentation; every revision is auditable by default.
- B. Approve + caller-requested only: permits the same exact governed scope but omits the durable before-and-after artifact unless requested, reducing routine evidence and storage.
- C. Defer: preserves this task, branch, and worktree in User Action Required with no definition mutation.
- D. Decline: ends this proposed governed-definition addition without reframing backlog creation as approval.

Display Name: Document Topic Editor.

Canonical Filename: agents/roles/dev-activities/dev-document-topic-editor.role.yaml.

Exact Governed Definition Manifest:

1. skills/analyze-document-topics/SKILL.md
2. skills/revise-document-topics/SKILL.md
3. skills/analyze-document-topics/agents/openai.yaml
4. skills/revise-document-topics/agents/openai.yaml
5. agents/roles/dev-activities/dev-document-topic-editor.role.yaml

Concrete Example: Analysis of design/agentic-configuration.html may report a low-coherence parent without changing bytes. Only a separately authorized revision may move headings, and the selected artifact policy controls whether its before-and-after outline is durably retained.

Exclusions: No other agent, skill, or metadata definition; no hand-edited generated mirror; no cross-family regeneration; and no document-revision child work.

Historical Unattended Work Boundary: The prior hold stopped delivery pending an answer. The answer is now recorded above; work remains stopped until this same task is separately reserved through Ready -> Starting and accepted through Starting -> Running.

Preserved Execution and Scope Evidence: Running acceptance commit 83bdaba2ebb3fea8c776d4be619186380881abb0; canonical task and Thread 019fab9e-44bf-7571-9fbb-d9d63d3fa9da; branch codex/incorporate-document-topic-agent-and-skills-019fab9e; worktree /Users/martinbechard/.codex/worktrees/350a/dev-methodology; clean no-candidate state; migration sources .agents/skills/create-document-outline/SKILL.md and .agents/skills/improve-document-outline/SKILL.md; supported regeneration surfaces, evaluation/test/documentation companions, and semantic documentation model-profile evidence remain preserved for later authorized work.

## Summary

Add a distributed read-only topic-analysis skill, a distributed document-topic revision skill, and one conceptual document-topic editor that uses both alongside the existing methodology agents and skills.

## Context

The project-local create-document-outline skill now performs source-grounded topic reconstruction, hierarchy scoring, and justification review. The project-local improve-document-outline skill applies structural recommendations. Their current names blur the boundary between analysis and document mutation. The accepted responsibility split is analyze-document-topics for read-only analysis and revise-document-topics for source mutation. A dedicated conceptual agent should own their combined editorial workflow and use the documentation model profile, whose Codex mapping uses high reasoning effort.

## Source Evidence

Direct user request in task 019fa9bf-1e81-7a70-87e5-a747ce97318f on 2026-07-28: “create a workitem to incorporate the agent and skills with the others, then add one workitem for each document to revise it.” The same task established the accepted responsibility names analyze-document-topics and revise-document-topics.

## Requirements

- Add skills/analyze-document-topics/SKILL.md as the distributed read-only topic inventory, hierarchy reconstruction, source-grounded scoring, and editorial diagnosis contract.
- Add skills/revise-document-topics/SKILL.md as the distributed mutation contract that consumes topic analysis and revises document structure while preserving complete content.
- Add agents/roles/dev-activities/dev-document-topic-editor.role.yaml as the conceptual owner of the combined analysis-and-revision workflow.
- Use the semantic documentation model profile so the generated Codex agent uses high reasoning effort without embedding a provider model identifier in the conceptual role.
- Add Codex metadata for both distributed skills when direct invocation metadata is applicable.
- Retire the obsolete project-local create-document-outline and improve-document-outline identifiers after migrating all required behavior and references.
- Preserve the scoring system, source-entailment rules, topic-to-justification coherence checks, honest partial scores, and safeguards against artificial score improvement.
- Keep analysis read-only until revision is explicitly requested and authorized.
- Regenerate supported skill catalogs, role documentation, and native agent adapters through their owning generators.
- Add focused contract tests and evaluation coverage for read-only analysis, authorized revision, generated ownership, and semantic preservation.
- Update README.md and the applicable design documentation to place the agent and skills with the existing catalog.

## Acceptance Criteria

- The two distributed skills have distinct names, triggers, mutation boundaries, inputs, outputs, and success evidence.
- The conceptual document-topic editor loads both skills, declares appropriate mutation authority, and renders to every supported native adapter.
- Generated Codex output uses the documentation profile with high reasoning effort.
- No stale create-document-outline or improve-document-outline definition or dependency remains.
- A representative document can be analyzed without mutation and revised only through the separate revision phase.
- Focused tests detect invented justification content, topic-to-why scope mismatch, artificial score improvement, and direct editing of generated mirrors.

## Dependencies

None.

## Verification

- Run the supported definition-change preflight for every exact governed source after obtaining explicit scope-specific approval.
- Validate both complete skill packages and the conceptual role.
- Run scripts/openai_metadata.py for the new skill metadata.
- Run scripts/build-skill-docs.py and its freshness check.
- Run focused bundle, role-generation, skill-catalog, and evaluation tests.
- Run git diff --check.
- Obtain independent methodology review and verification.

## Open Questions

- Determine the final user-facing display name for dev-document-topic-editor while preserving the canonical filename.
- Determine whether the revision skill should retain a durable before-and-after topic-analysis artifact by default or only when the caller requests one.

## Notes

Authorized governed canonical sources are skills/analyze-document-topics/SKILL.md, skills/revise-document-topics/SKILL.md, skills/analyze-document-topics/agents/openai.yaml, skills/revise-document-topics/agents/openai.yaml, and agents/roles/dev-activities/dev-document-topic-editor.role.yaml. The direct user direction recorded in Resumption Record authorizes only those requested definitions. Implementation must record that approval and pass one supported pre-mutation check for each governed path. Any definition outside this exact manifest needs new explicit approval.
