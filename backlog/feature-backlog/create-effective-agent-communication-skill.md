# Create an Effective Agent Communication Skill

Status: Ready

Type: Feature

Provider: file

Provider Reference: backlog/feature-backlog/create-effective-agent-communication-skill.md

Completion: direct-main

## Summary

Create a reusable communication skill that gives all agents concise, practical principles for communicating clearly with users and other agents.

## Context

Agent messages frequently become difficult to understand because they use internal terminology, long sentences, unexplained abstractions, vague status language, or excessive procedural detail. The methodology needs one shared communication contract instead of repeating inconsistent writing guidance across roles and skills.

The skill must improve both user-facing communication and agent-to-agent handoffs while preserving exact technical evidence where it matters.

## Source Evidence

Direct user request in the active coordinator task on 2026-07-25: “we need to create a communication skill that all agents should use in which we put principles for effective communication - create a work item for that”.

## Requirements

- Create one reusable communication skill for all agents.
- Use plain language and short sentences. Put one rule or idea in each sentence.
- Use technical terms only when they name an actual command, field, outcome, file, or resource. Explain specialized or project-specific terms when they are first used.
- Define principles for concrete terminology and outcome-first reporting.
- Prefer familiar words over abstract labels. For example, say “claim helper” and “claim command-line interface” instead of unexplained “engine” or “transport”.
- Separate outcomes, evidence, blockers, decisions, and next actions so each is easy to identify.
- Keep user-facing messages understandable without requiring the user to know internal lifecycle, claim, task, or implementation terminology.
- Define concise agent-to-agent handoff content: exact identity, current state, preserved work, evidence, blocker, and next action.
- Avoid redundant status narration and procedural detail that does not help the recipient decide or act.
- Prefer a concrete example over a bare inventory when the example makes a structure, workflow, or file layout easier to understand.
- Do not replace a simple explanation with an abstract restatement.
  - Avoid: “Scope describes a claim already required by the Event Contract. Scope does not authorize a claim.”
  - Prefer: “The table decides when to get a claim. Scope says what the claim covers.”
- Use tables or lists only when they make repeated mappings or choices clearer than prose.
- Align existing shared communication guidance with the new skill and remove material duplication where appropriate.
- Perform exact governed-source discovery before implementation and obtain scope-specific approval for every governed definition that must change.

## Acceptance Criteria

- One canonical communication skill contains the shared principles used by all agents.
- Agent definitions or shared dispatch guidance cause every applicable agent to use the skill without copying its full procedure.
- Examples demonstrate clear user-facing explanations, status updates, approval questions, blocker reports, and agent handoffs.
- Tests reject unexplained jargon, vague outcomes, hidden questions, redundant procedural narration, abstract restatements, and overly long multi-rule sentences in covered fixtures.
- Tests preserve exact identifiers, paths, commits, claim references, and error outcomes when those details are operationally necessary.
- Relevant README, agent-and-skill HTML documentation, generated mirrors, and bundle assertions remain source-aligned.
- Independent review confirms that the skill improves clarity without removing required evidence or authority boundaries.

## Dependencies

None.

## Verification

- Run the exact governed-definition approval checks for every affected canonical skill or agent definition before mutation.
- Validate the new skill and any changed metadata.
- Run focused bundle, generated-definition, and communication-contract tests.
- Regenerate only supported mirrors from approved canonical sources.
- Verify relevant HTML documentation and README alignment.
- Run git diff --check.
- Obtain independent methodology and user-experience review.

## Open Questions

- Determine through implementation discovery which agent definitions or shared generation surfaces should reference the communication skill.
- Determine whether existing writing guidance should remain as specialized extensions or be replaced by references to the canonical communication skill.

## Notes

This item authorizes creation and delivery of the communication capability. It does not pre-approve mutation of any governed agent or skill definition; implementation must discover and request the exact required scope.
