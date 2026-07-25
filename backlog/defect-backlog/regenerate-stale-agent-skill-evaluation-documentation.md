# Regenerate stale agent-skill evaluation documentation

Status: Running

Type: Defect

Owner: Dev Orchestrator

Provider: file

Provider Reference: backlog/defect-backlog/regenerate-stale-agent-skill-evaluation-documentation.md

Completion: direct-main

## Launch Reservation

- Parent Coordination Thread: 019f95a9-7eb5-7bf1-8c1b-bb4a40a8006a
- Canonical Thread/Task: 019f979e-5330-7501-8340-92dfd593f6ef
- Reservation: One parent-owned launch reservation.
- Intended Root Role: Dev Orchestrator
- Isolated Checkout: /Users/martinbechard/.codex/worktrees/5c5a/dev-methodology
- Phase: Awaiting root acceptance.
- Dispatched At: 2026-07-25T04:53:32Z

## Coordination Evidence

- Backlog Claim: reserve-stale-evaluation-documentation-defect-019f979e acquired on primary main at 2026-07-25T04:53:32.705924Z; acquisition journal event a03bd3f2-6561-4920-8fab-ada4cc43121c.
- Starting Baton: primary-main commit 1ec0d3e67009f43f671f5bbef7a6f625547cc539.
- Running Backlog Claim: 019f979e-steward-running acquired on primary main at 2026-07-25T04:55:33.857392Z; acquisition journal event 911addc4-59fc-4d68-a7fe-10f9fc4a6d36.
- Artifact Overlap Resolution: prior claim 019f96f1-steward-correction2-isolated is released; release journal event a0a41f34-a1c8-4a82-bcfa-94aff56de2d6 and semantic artifact baton commit f30bbb84c47359a84f7e798c3a875b5657f0f923.

## Running Acceptance

- Accepted Root Identity: Dev Orchestrator task 019f979e-5330-7501-8340-92dfd593f6ef.
- Branch: codex/regenerate-stale-evaluation-docs-019f979e.
- Worktree: /Users/martinbechard/.codex/worktrees/5c5a/dev-methodology.
- Phase: Reconciling released semantic artifact baton.
- Started At: 2026-07-25T04:55:33.857392Z.

## Summary

Restore freshness of the generated agent-skill evaluation documentation so the evaluation-document generator check passes on current primary main.

## Context

The repository regression command python3 -m unittest discover scripts fails at scripts.test_agent_skill_evaluation_docs.AgentSkillEvaluationDocsTests.test_generator_check_reports_current_output. The check reports Evaluation documentation is stale because design/agent-and-skill-evaluations.html does not match the current generator output.

The failure was reproduced during the canonical topology task 019f977f-8bf5-77a1-b3c8-b55a113736d7 broad gate on its topology candidate and independently on clean current primary main. A git-archive snapshot could not execute this case because required backlog operational inputs are untracked; the primary-main reproduction is therefore the authoritative reproduction evidence.

## Source Evidence

- User direction on 2026-07-25: every additional confirmed distinct defect must be logged durably, not left as a warning.
- Canonical topology task 019f977f-8bf5-77a1-b3c8-b55a113736d7 broad gate: confirmed failure of scripts.test_agent_skill_evaluation_docs.AgentSkillEvaluationDocsTests.test_generator_check_reports_current_output on the topology candidate and clean current primary main.

## Requirements

- Restore generator freshness for design/agent-and-skill-evaluations.html.
- Identify why the current primary output drifted from the generator output.
- Keep the correction scoped to the stale evaluation-documentation defect and avoid unrelated regeneration.
- Add or adjust a regression only when the investigation shows existing coverage is insufficient.

## Acceptance Criteria

- The focused agent-skill evaluation-document generator check reports current output.
- The recorded implementation evidence identifies the cause of the output drift.
- The delivered change contains no unrelated generated-output refresh.
- Any needed regression coverage protects the identified drift path.

## Dependencies

None.

## Verification

- Run the focused agent-skill evaluation-document generator freshness check.
- Run the appropriate regression for the evaluation-document generator and its stale-output behavior.
- Run git diff --check.

## Open Questions

Determine whether the drift arose from an omitted generator invocation, an incomplete prior integration, or a generator/input change that was not accompanied by its generated HTML output.

## Notes

Do not dispatch or implement this item as part of its creation. Governed-source approval remains required before any mutation of a governed canonical definition.
