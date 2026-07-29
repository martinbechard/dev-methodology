# Incorporate the Document Topic Editor and Topic Skills

Status: Ready

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/document-topic-revision/incorporate-document-topic-agent-and-skills.md

Completion: direct-main

Series: backlog/feature-backlog/document-topic-revision/index.md

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

Anticipated governed canonical sources are skills/analyze-document-topics/SKILL.md, skills/revise-document-topics/SKILL.md, skills/analyze-document-topics/agents/openai.yaml, skills/revise-document-topics/agents/openai.yaml, and agents/roles/dev-activities/dev-document-topic-editor.role.yaml. This work item authorizes backlog capture and later implementation dispatch; it does not authorize mutation of those definitions. Implementation must record exact user approval and pass one supported pre-mutation check for each governed path.
