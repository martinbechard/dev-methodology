# Estimate Agent Work In Agent-Hours

Status: Starting

Type: Feature

Provider: file

Work Item ID: estimate-agent-work

Completion: main-branch

## Summary

Create a portable estimate-agent-work skill and assign it to Dev Coder so AI-delivered engineering work is estimated in generated tokens, complexity, turns, agent-hours, non-model runtime, and parallel wall-clock time instead of human person-days.

## Context

Human effort units do not describe the dominant cost and elapsed-time drivers of agentic delivery. The working throughput assumption is 50 generated output tokens per second, including reasoning. Generated-token effort therefore converts to agent-hours at 180,000 generated tokens per agent-hour. Parallelism reduces elapsed wall-clock time through the critical path but does not reduce total agent-hours.

The estimate must keep live evaluation consumption and external tool or test runtime separate from implementation-agent generation. Input and cached tokens may affect monetary cost and context pressure, but they must not be converted through the generated-output throughput rate.

## Source Evidence

The user explicitly requested on 2026-08-12 in Codex task 019ff660-663f-7271-a4da-c30e6c054cf7: "parallelism is a good point - I guess we need to qualify estimates as agent-hours. This would make an interesting skill for our Dev Coder agent - log a backlog item for that skill."

The same conversation established generated tokens, including reasoning, as the throughput basis and supplied the current planning assumption of 50 generated output tokens per second.

## Requirements

- Create the portable estimate-agent-work skill with a clear contract for estimating AI-delivered engineering work.
- Assign the skill to the Dev Coder conceptual agent without moving general work-planning authority away from the roles that own scope and dispatch decisions.
- Define complexity levels in terms of reasoning uncertainty, integration breadth, verification burden, correction risk, and coordination depth.
- Estimate generated tokens, including reasoning, and convert them to agent-hours using an explicit configurable throughput assumption that defaults to 50 generated tokens per second.
- Estimate autonomous turns as checkable work cycles rather than equal-duration time units or user-message counts.
- Report total agent-hours, critical-path agent-hours, expected parallelism, and expected wall-clock duration without claiming that parallelism reduces total model effort.
- Report tool, build, test, browser, live-evaluation, external-service, approval, and other non-model runtime separately.
- Separate implementation-agent generation from tokens consumed by executing live evaluation scenarios.
- State uncertainty, assumptions, range drivers, and confidence; avoid false precision.
- Include compact calculation examples and a reusable estimate output shape.
- Keep monetary token cost optional and distinct from effort unless current provider prices are supplied or verified.
- Regenerate supported native agent adapters and update affected catalog documentation and focused regression coverage through repository-supported generators.

## Acceptance Criteria

- The new skill produces estimates containing complexity, generated-token range, agent-hours, expected turns, non-model runtime, parallelism assumptions, and wall-clock range.
- The conversion is mathematically consistent: agent-hours equal generated tokens divided by the configured generated-token throughput and by 3,600 seconds per hour.
- The default 50-token-per-second assumption yields 180,000 generated tokens per agent-hour and is visibly identified as an assumption rather than a universal measured rate.
- Examples distinguish total agent-hours from critical-path elapsed time and distinguish implementation generation from live-evaluation consumption.
- The Dev Coder conceptual source and every supported generated adapter contain the assigned skill after supported regeneration.
- Focused contract tests cover conversions, parallel and serial examples, uncertainty ranges, excluded runtime, and protection against person-day estimates presented as the primary AI effort measure.
- Relevant skill, agent, generated-output freshness, catalog, documentation, and diff checks pass.
- Independent review finds no ownership confusion between estimation guidance and backlog, architecture, dispatch, or acceptance authority.

## Dependencies

None.

## Verification

- Validate the new skill package and metadata with the repository-supported skill checks.
- Run focused catalog assertions for the skill inventory and Dev Coder assignment.
- Run the supported conceptual-agent generation command and verify exact source-to-adapter consistency.
- Run focused tests for every added conversion or estimate-contract helper.
- Check affected README and design references for catalog consistency.
- Run Git diff whitespace validation.
- Obtain independent skill and generated-artifact review before delivery.

## Open Questions

- Determine whether the skill should prescribe one fixed complexity scale or a small extensible rubric.
- Determine whether measured throughput overrides should be recorded per model, reasoning profile, harness, or execution environment.
- Determine whether a deterministic calculator belongs in the skill package or whether transparent formulas and examples are sufficient.

## Governed Definition Approval

### Governed Canonical Sources

- skills/estimate-agent-work/SKILL.md
- agents/roles/dev-activities/dev-coder.role.yaml

### Allowed Dependent Artifacts

- skills/estimate-agent-work/agents/openai.yaml
- generated/adapters/codex/agents/dev-coder.toml
- generated/adapters/claude/agents/dev-coder.md
- generated/adapters/gemini/agents/dev-coder.md
- generated/adapters/junie/agents/dev-coder.md
- README.md
- design/agent-and-skill-definitions.html
- design/agent-and-skill-evaluations.html
- scripts/test_bundle_content.py
- Additional generator-owned catalog projections and focused test files only when repository discovery proves they consume one of the approved canonical sources.

### Approval Resolution

Approved at creation. On 2026-08-12, in Codex task 019ff660-663f-7271-a4da-c30e6c054cf7, the user explicitly requested a skill for Dev Coder to qualify AI-work estimates as agent-hours and asked that the backlog item be logged. This approval covers only the two exact governed canonical sources listed above. Any additional governed skill or agent-definition source requires separate user approval.

## Notes

This item defines an estimation method, not a promise that generated-token throughput is constant. Implementers must preserve the distinction between an assumed planning rate, an observed rate, and a provider-specific billing rate.

## Starting Handoff Evidence

- Reserved At: 2026-08-13T08:28:14Z.
- Transition: `Ready -> Starting`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Coordinator Execution: `/root/backlog_coordinator`.
- Baseline: `9303d68370c706735fe437e4b801009bb4bbef3f` on primary `main`.
- Priority: Oldest eligible independent process-efficiency item with complete governed-definition approval. Older terminology items require scope-authority reconciliation before mutation and are not selected here.
- Effective Dependencies: None. Inspect AI downstream children remain effective Holding behind their ordered predecessor. HTML documentation series remains outside this independent process item.
- Overlap: Candidate `03a94762451efe4322fe781f77191b769bf6c7b1`, all three User Action Required records, and all four untracked plan artifacts remain excluded. Any shared generated or focused-test path must be based on current main and must not alter the preserved UAR record or candidate history.
- Historical Cleanup: The two unclaimed, unchecked-out STE integration branches remain outside this Work Item and are not authorized cleanup targets.
- Dispatch Architecture: Create one user-visible Codex task whose initial reference-plus-delta prompt starts one Dev Orchestrator collaboration subagent for this provider record.
- Transition Claim: `start-estimate-agent-work-019ff2c3`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `e9c27b39-0ace-4126-8720-75eab3725253`.
- Next Reconciliation: Adopt the exact visible task identity. Its nested Dev Orchestrator records Starting -> Running before mutation.

## Canonical Runtime Assignment

- Assigned At: 2026-08-13T08:29:10Z.
- Codex Task ID: `019ffa3d-191f-7343-aaeb-2499de1ad605`.
- Conversation ID: `019ffa3d-191f-7343-aaeb-2499de1ad605`.
- Host: `local`.
- Runtime Parent Task: `019ff2c3-1710-7aa1-89c4-9d6066f51fe4`.
- Requested Title: `Starting — Estimate Agent Work`.
- Initial Action: Start one Dev Orchestrator collaboration subagent for this authoritative provider record.
- Creation Outcome: Unique success with no pending client identity and no retry.
- Lifecycle Boundary: This assignment remains Starting until the nested Dev Orchestrator accepts and records Starting -> Running.

## Running Acceptance Evidence

- Accepted At: 2026-08-13T08:30:51Z.
- Transition: `Starting -> Running`.
- Owner: Dev Orchestrator.
- Canonical Conversation: `019ffa3d-191f-7343-aaeb-2499de1ad605`.
- Canonical Task: `019ffa3d-191f-7343-aaeb-2499de1ad605`.
- Root Agent Execution: `/root/estimate_agent_work`.
- Branch: `main`.
- Worktree: `/Users/martinbechard/dev/dev-methodology`.
- Phase: Implementation and TDD planning.
- Accepted Execution: The nested Dev Orchestrator accepted the authoritative file-provider assignment and will preserve the dispatch exclusions while coordinating the required plan, implementation, independent review, verification, and main-branch delivery.
- Title Handoff: Unsynchronized because neither this execution nor its authorized caller path exposes conversation rename authority. The required title is `Implementing — Estimate Agent Work`.

## Bounded Plan-Review Recovery

- Authorized At: 2026-08-13T09:28:10Z.
- Review Attempt: One fresh finding-linked plan correction and re-review is authorized. This is the first plan-review correction for this Work Item; no repeated or exhausted finding exists.
- Finding: The plan omitted the direct evaluation-catalog dependency for the new skill. The package must add `probe-estimate-agent-work` and update only the exact inventory assertions that consume the registered skill and probe.
- Scope Decision: `evals/skill-probes.yaml` and mechanically required focused catalog/inventory assertions are allowed dependent test artifacts because repository-supported evaluation and inventory checks directly consume the new approved skill package. This does not authorize another governed skill or Agent definition.
- Correction Boundary: Update the preserved plan pair only for `probe-estimate-agent-work`, its exact executable association, and consuming inventory assertions. Obtain one fresh plan review before implementation.
- Preserved State: No source candidate or tracked dirty bytes exist. Claims are empty. Preserve the canonical visible task, nested Dev Orchestrator, plan pair, candidate `03a94762451efe4322fe781f77191b769bf6c7b1`, all User Action Required records, and the other four plan artifacts.
- Transition: Provider remains `Running`; no lifecycle transition or replacement execution is authorized.
- Transition Claim: `authorize-estimate-plan-review-retry-019ffa3d`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `3e39017a-abab-45c7-8aba-54c44fd47adc`.

## Final Mechanical Plan-Schema Correction

- Authorized At: 2026-08-13T09:44:14Z.
- Attempt Classification: The corrected plan still expresses the same first plan-review finding. It names the required probe but omits the repository-native probe fields. This authorizes the second and final bounded correction attempt, not a new finding.
- Correction Boundary: Update only the preserved plan pair for `probe-estimate-agent-work` so it specifies `evaluationCategory`, `evaluationKind`, `ablation`, `activationCondition`, `negativeCondition`, `expectedBehavior`, and `judgePlan`, together with the already authorized association and focused inventory assertions. Use existing `evals/skill-probes.yaml` entries as the schema source. Do not mutate source during this correction.
- Review Gate: Obtain one fresh plan review after the mechanical correction. Another occurrence of this same probe-schema or catalog-dependency finding exhausts the correction limit and requires a new Coordinator disposition; it does not authorize another retry.
- Preserved State: No source candidate or tracked dirty bytes exist. Claims were empty before this provider transaction. Preserve the canonical visible task, nested Dev Orchestrator, plan pair, candidate `03a94762451efe4322fe781f77191b769bf6c7b1`, all User Action Required records, and the other four plan artifacts.
- Transition: Provider remains `Running`; no lifecycle transition, title change, replacement execution, or source mutation is authorized.
- Transition Claims: `authorize-estimate-final-plan-schema-correction-019ffa3d`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `3f100a95-0b6e-48ce-ac02-35e1d62327b8`. `authorize-estimate-final-plan-schema-provider-019ffa3d`; outcome `SHARED_CHECKOUT_ACQUIRED`; event `922ca1cc-df4e-49f2-81ca-2d25daffa097`.

## Exhausted Correction Disposition

- Recorded At: 2026-08-13T11:35:41Z.
- Transition: `Running -> User Action Required`.
- Preserved Candidate: `e6931e2a9bbdf28db7fd1fc59cd01c7f188b0850` on primary `main`, following correction commits `8d8a44a6` and `562dfe5d`.
- Finding: The accepted reusable example and output-shape contract still lacks explicit cross-path concurrency semantics and validation that rejects malformed `expected_parallelism` values.
- Attempt History: Two bounded correction attempts are consumed. Another correction and fresh independent review require explicit user authorization.
- Preserved Runtime: Canonical Task and Conversation `019ffa3d-191f-7343-aaeb-2499de1ad605`; nested Dev Orchestrator `/root/estimate_agent_work`; completed estimate plan pair. Do not replace this execution.
- Claim Handoff: Project-files claim `estimate-agent-work-files-019ffa3d` released at event `85356a32-d747-4bb3-bc67-d6ed7f2eeece`. Work Item claim `estimate-agent-work-outcome-019ffa3d` released with disposition `blocked` and blocker `estimate-agent-work-correction-limit-exhausted` at event `5005ac24-db9f-49b1-8cf6-602f799e4abf`.
- Capacity: User Action Required does not consume active execution capacity. The canonical visible task remains the user-facing decision context and must not be replaced or counted as Running.

## User Action Required

### Question for the User

Do you authorize one exceptional additional correction and fresh independent review cycle to define and validate cross-path concurrency and reject malformed `expected_parallelism` values?

### Why User Input Is Required

The normal correction limit is exhausted. Continuing would require new authority. Excluding the finding would accept a known gap in a required reusable output shape.

### Options and Tradeoffs

- **Authorize one exceptional correction and review (recommended):** Preserve all accepted requirements. Define how parallel work paths combine and add negative validation for malformed values such as zero, negative, non-numeric, or structurally inconsistent `expected_parallelism` data.
- **Exclude the finding and create a follow-up defect:** Accept candidate `e6931e2a9bbdf28db7fd1fc59cd01c7f188b0850` without this validation. Record the residual risk and defer the gap to a separate defect.

### Resolution

Answered on 2026-08-13 in canonical Task and Conversation `019ffa3d-191f-7343-aaeb-2499de1ad605`.

Exact user answer: `ok I approve two more cycles`

Disposition: Authorized. The answer permits at most two additional correction-and-fresh-independent-review cycles addressing cross-path concurrency and malformed `expected_parallelism` validation. The accepted reusable output-shape requirement remains in scope.

### Unattended Work Boundary

Do not modify, review, verify, deliver, or close this Work Item until the user answers in canonical Task and Conversation `019ffa3d-191f-7343-aaeb-2499de1ad605`. Unrelated eligible Work Items may continue.

## User Decision Recovery

- Recorded At: 2026-08-13T11:55:04Z.
- Transition: `User Action Required -> Ready`.
- Decision Provenance: Exact answer received in canonical Task and Conversation `019ffa3d-191f-7343-aaeb-2499de1ad605`.
- Preserved Candidate: `e6931e2a9bbdf28db7fd1fc59cd01c7f188b0850`.
- Authorized Correction Budget: At most two additional correction-and-fresh-independent-review cycles for cross-path concurrency and malformed `expected_parallelism` validation.
- Capacity Decision: Five other Work Items remain `Starting` or `Running`. This item waits in `Ready` for the first released slot and does not consume active capacity.
- Next Action: This same canonical Dev Orchestrator records `Ready -> Starting -> Running` when one active slot becomes available, then reacquires required implementation claims before mutation.

## Correction Resumption Starting Evidence

- Reserved At: 2026-08-13T12:09:28Z.
- Transition: `Ready -> Starting`.
- Capacity Wait: Satisfied. One reserved active slot is available within the five-item limit.
- Canonical Task and Conversation: `019ffa3d-191f-7343-aaeb-2499de1ad605`.
- Root Agent Execution: `/root/estimate_agent_work`.
- Preserved Candidate: `e6931e2a9bbdf28db7fd1fc59cd01c7f188b0850`.
- Normalized Objective: Complete correction cycle 1 of 2 by defining cross-path concurrency, rejecting malformed `expected_parallelism`, obtaining fresh independent review, and preserving every accepted reusable-output requirement.
- Launch Result: Existing canonical execution resumed; no replacement execution created.
- Next Action: The same Dev Orchestrator records `Starting -> Running`, then acquires outcome and project-files claims before mutation.
