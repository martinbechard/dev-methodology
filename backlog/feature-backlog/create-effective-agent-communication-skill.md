# Create an Effective Agent Communication Skill

Status: Ready

Type: Feature

Owner: Unowned

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

## Prior Starting Reservation Evidence

- Parent Coordination Thread: /root.
- Reservation: One parent-owned Ready -> Starting launch reservation.
- Normalized Objective: Create an effective agent communication skill.
- Intended Root Role: Dev Orchestrator.
- Persistence And Completion: file provider; direct-main completion.
- Dispatched At: 2026-07-26T13:37:13Z.
- Launch Evidence: Parent Coordinator authorized this exact-item reservation. Runtime task creation and acceptance remain pending.
- Backlog Claim Event: 67199e90-0a97-446b-8dcb-a10a1f2bc149.
- Next Lifecycle Owner: the root Dev Orchestrator must record a distinct Starting -> Running acceptance before repository mutation.

## Prior Running Acceptance Evidence

- Canonical Work-Item Thread And Root Agent Task: 019f9ea6-9f90-7551-835c-f35a5d5ed471.
- Root Role And Owner: Dev Orchestrator.
- Root Branch: codex/effective-agent-communication-019f9ea6.
- Root Worktree: /Users/martinbechard/.codex/worktrees/a68c/dev-methodology.
- Phase: exact governed-source discovery.
- Started At: 2026-07-26T13:49:17.061554Z.
- Starting Reservation Evidence: commit 6f803e5d36e7239495ed3c6e15bcdce7a83284f4 and the Current Starting Reservation above.
- Backlog Claim Evidence: Event 1 exact-file claim acquired as starting-running-effective-agent-communication-019f9ea6; acquisition event b620f13d-87ca-4b90-8437-700bfef41e51.
- Provider Transaction: primary main at baseline 1e20f503dd5afdd946564eb069934b980a81020b.

## User Action Required Resolution

- Canonical Work-Item Thread And Root Agent Task: 019f9ea6-9f90-7551-835c-f35a5d5ed471.
- Preserved Root Branch: codex/effective-agent-communication-019f9ea6.
- Preserved Root Worktree: /Users/martinbechard/.codex/worktrees/a68c/dev-methodology.
- Phase: exact governed-definition approval.
- Same-Task Resumption: after an answer, preserve this canonical Thread and resume through User Action Required -> Ready -> Starting -> Running.
- Claim State After This Transaction: None after the Event 1 claim is released.
- Prohibited Unattended Action: do not mutate artifacts, generate outputs, integrate, or publish until the user answers this question.

### Approval Question

Do you approve changing these three canonical definitions so every generated conceptual agent uses the new effective-communication skill?

### Resolution

On 2026-07-26, the user answered exactly “Approved” in canonical work-item Thread and root Agent Task 019f9ea6-9f90-7551-835c-f35a5d5ed471. This approves exactly these governed canonical definitions: skills/effective-communication/SKILL.md; skills/effective-communication/agents/openai.yaml; and agents/role-schema.yaml. The answer authorizes the shared communication contract and one role-schema shared fixed-skill default so every generated conceptual agent uses it without editing all 28 role files. Supported ordinary generator, test, README, design, and source-owned generated-mirror changes are dependent artifacts, not additional governed approval. Provenance: the user reply followed the exact recorded three-path approval question in the canonical task.

### Ready Resumption

- Transition: User Action Required -> Ready.
- Canonical Work-Item Thread And Root Agent Task: 019f9ea6-9f90-7551-835c-f35a5d5ed471.
- Preserved Root Branch: codex/effective-agent-communication-019f9ea6.
- Preserved Root Worktree: /Users/martinbechard/.codex/worktrees/a68c/dev-methodology.
- Owner: Unowned.
- Next Lifecycle Owner: parent Dev Backlog Coordinator must record a distinct Ready -> Starting reservation for this same canonical task; the root Dev Orchestrator must then record the distinct Starting -> Running acceptance before repository mutation.

### Reason

The requested capability is itself a new governed skill and making it universal needs one governed shared role default; unattended implementation cannot safely choose or mutate those definitions.

### Governed Definition Approval Manifest

1. skills/effective-communication/SKILL.md — a new shared communication contract.
2. skills/effective-communication/agents/openai.yaml — its Codex catalog metadata.
3. agents/role-schema.yaml — a shared fixed-skill default that makes every conceptual agent use effective-communication without editing all 28 role files.

No other canonical definition is included in this approval request.

### Supported Dependent Artifacts

These are ordinary implementation or generation outputs, not additional approval: scripts/build-skill-docs.py; focused communication and bundle tests; README.md; design/generic-agent-definitions-source.html; design/agent-and-skill-definitions.html; supported generated skill, role, native-adapter, hierarchy, explorer, and coverage outputs.

### Illustrative Options And Tradeoffs

- Approve (recommended): central shared default with no 28 repetitive role edits.
- Request role-by-role wiring: requires a separate much wider 28-role approval and repetitive source changes.
- Decline/defer: preserve discovery and make no definition changes.

These options are illustrative and are not an inferred answer.

## Notes

This item authorizes creation and delivery of the communication capability. It does not pre-approve mutation of any governed agent or skill definition; implementation must discover and request the exact required scope.
