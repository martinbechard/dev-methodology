# Create an Effective Agent Communication Skill

Status: Running

Type: Feature

Owner: Dev Orchestrator

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
- Introduce a specific instance before referring to it with “the”. For example, introduce “a claim result” before writing “the result”.
- Define principles for concrete terminology and outcome-first reporting.
- Prefer familiar words over abstract labels. For example, say “claim helper” and “claim command-line interface” instead of unexplained “engine” or “transport”.
- Separate outcomes, evidence, blockers, decisions, and next actions so each is easy to identify.
- Keep user-facing messages understandable without requiring the user to know internal lifecycle, claim, task, or implementation terminology.
- Define concise agent-to-agent handoff content: exact identity, current state, preserved work, evidence, blocker, and next action.
- Avoid redundant status narration and procedural detail that does not help the recipient decide or act.
- Prefer a concrete example over a bare inventory when the example makes a structure, workflow, or file layout easier to understand.
- Explain simple ideas in direct, concrete language.
  - Write: “The table decides when to get a claim. Scope says what the claim covers.”
  - This replaces the abstract wording: “Scope describes a claim already required by the Event Contract. Scope does not authorize a claim.”
- Use tables or lists only when they make repeated mappings or choices clearer than prose.
- Align existing shared communication guidance with the new skill and remove material duplication where appropriate.
- Perform exact governed-source discovery before implementation and obtain scope-specific approval for every governed definition that must change.

## Acceptance Criteria

- One canonical communication skill contains the shared principles used by all agents.
- Agent definitions or shared dispatch guidance cause every applicable agent to use the skill without copying its full procedure.
- Examples demonstrate clear user-facing explanations, status updates, approval questions, blocker reports, and agent handoffs.
- Tests confirm that covered fixtures use explained terminology, explicit outcomes and questions, concise status narration, direct explanations, and one-rule sentences.
- Tests reject unexplained uses of “the” before the referenced common-noun instance has been introduced in context.
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

## Current Starting Reservation

- Parent Coordination Thread: /root.
- Reservation: One parent-owned Ready -> Starting launch reservation.
- Normalized Objective: Create an effective agent communication skill.
- Intended Root Role: Dev Orchestrator.
- Persistence And Completion: file provider; direct-main completion.
- Dispatched At: 2026-07-26T13:37:13Z.
- Launch Evidence: Parent Coordinator authorized this exact-item reservation. Runtime task creation and acceptance remain pending.
- Backlog Claim Event: 67199e90-0a97-446b-8dcb-a10a1f2bc149.
- Next Lifecycle Owner: the root Dev Orchestrator must record a distinct Starting -> Running acceptance before repository mutation.

## Running Acceptance

- Canonical Work-Item Thread And Root Agent Task: 019f9ea6-9f90-7551-835c-f35a5d5ed471.
- Root Role And Owner: Dev Orchestrator.
- Root Branch: codex/effective-agent-communication-019f9ea6.
- Root Worktree: /Users/martinbechard/.codex/worktrees/a68c/dev-methodology.
- Phase: exact governed-source discovery.
- Started At: 2026-07-26T13:49:17.061554Z.
- Starting Reservation Evidence: commit 6f803e5d36e7239495ed3c6e15bcdce7a83284f4 and the Current Starting Reservation above.
- Backlog Claim Evidence: Event 1 exact-file claim acquired as starting-running-effective-agent-communication-019f9ea6; acquisition event b620f13d-87ca-4b90-8437-700bfef41e51.
- Provider Transaction: primary main at baseline 1e20f503dd5afdd946564eb069934b980a81020b.

## Notes

This item authorizes creation and delivery of the communication capability. It does not pre-approve mutation of any governed agent or skill definition; implementation must discover and request the exact required scope.
