# Add A Portable Skill For Evidence-Based Agent Tournaments

Owner: Dev Orchestrator task 019fe4cb-b4f3-7563-8ece-a60e567aae29

Canonical Conversation: 019fe4cb-b4f3-7563-8ece-a60e567aae29

Canonical Task: 019fe4cb-b4f3-7563-8ece-a60e567aae29

Branch: codex/add-portable-agent-tournament-skill

Worktree: /Users/martinbechard/.codex/worktrees/1bbe/dev-methodology

Phase: Implementing — Final review corrections

Status: Running

Type: Feature

Provider: file

Work Item ID: add-portable-agent-tournament-skill

Completion: main-branch

## Summary

Add a small portable Agent Skill named run-agent-tournament that helps agents plan, authorize, execute, score, resume, rescore, verify, and report controlled comparisons among agent or model candidates. Keep tournament methodology reusable while leaving domain tasks, fixtures, ground truth, and scoring semantics with the calling task or its evaluation package.

## Context

Agents sometimes need to select a model, reasoning effort, semantic model profile, prompt, or agent configuration for a repeatable task. Informal comparisons can confound runner and coordinator behavior, change more than one factor at a time, reward speed over correctness, double count cached-input cost, or overstate a small synthetic evaluation.

The documentation-design-system experiment demonstrated a concrete need for a reusable procedure that freezes the comparison contract, asks for material missing decisions before spending credits, preserves auditable evidence, and reports a selection with honest limitations. Its domain-specific integration is tracked separately by Work Item ID integrate-documentation-design-system. That item and its candidate artifacts are evidence for this methodology feature, not a hard dependency or part of this feature's delivery scope.

The new skill owns tournament methodology, clarification gates, evidence requirements, staged advancement, ranking policy, and selection reporting. It does not own the domain-specific task, fixtures, reviewed ground truth, output semantics, universal scoring logic, provider choice, deployment, or publication.

## Source Evidence

- On 2026-08-09, the user stated, "here's a new backlog item," and supplied Work-Item Notes titled Portable Agent Tournament Skill in the current Codex task.
- The supplied objective is: "Add a small, portable Agent Skill that helps an agent plan, execute, score, and report a staged tournament among agent or model candidates."
- The notes identify run-agent-tournament as the preferred skill ID, provide the trigger and clarification boundary, define the workflow and ranking rules, list required outputs and regression scenarios, and authorize use of the local documentation-design-system evaluation artifacts as implementation evidence.
- The attached source note is /Users/martinbechard/.codex/attachments/03a696f5-78d4-4efe-99bb-8aebde970b89/pasted-text.txt.
- The implementation owner may inspect these user-designated local evidence sources:
  - /Users/martinbechard/dev/docs-design-system/evals/README.md
  - /Users/martinbechard/dev/docs-design-system/evals/eval_harness.py
  - /Users/martinbechard/dev/docs-design-system/evals/test_eval_harness.py
  - /Users/martinbechard/dev/docs-design-system/evals/coordinator/
  - /Users/martinbechard/dev/docs-design-system/evals/results/tournament-report.md
  - /Users/martinbechard/dev/docs-design-system/evals/results/coordinator-tournament-report.md

## Requirements

- Create the portable skill run-agent-tournament with a trigger that covers controlled comparative evaluation of agent definitions, semantic model profiles, provider models, reasoning efforts, and prompts for one fixed task contract, while excluding ordinary single-model testing.
- Keep the main skill concise. Use the approved tournament-contract reference only when the complete reusable contract would otherwise make the main skill unwieldy, and use the approved example configuration only when it remains runtime-portable and provider-neutral.
- Before any live model call, freeze the decision, constants, allowed variables, candidate matrix, availability, fixtures, reviewed ground truth, strict output schema, metrics, ranking priority, equivalence tolerances, tie-breakers, tournament stages, repeated trials, evidence location, budget boundary, authorization, pricing treatment, stop conditions, and data-safety boundary.
- Ask the smallest useful set of concise clarification questions before live execution whenever missing information could change the candidate set, attribution, validity, ranking, cost, or data exposure. Explain why each answer changes the experiment.
- Support plan-only work without requesting live-run authorization. Permit explicit assumptions for non-blocking planning gaps, but never silently carry them into paid or otherwise consequential execution.
- Require a dry-run matrix that enumerates every candidate-fixture invocation and states the expected number of live calls before authorization.
- Hold case inputs byte-equivalent across candidates. Vary one factor at a time unless the frozen contract explicitly declares multiple varying factors and the resulting attribution limitation.
- Keep runner and coordinator tournaments separate when they are distinct roles. When evaluating a coordinator, freeze runner reports and verify their identity or hashes so runner variation cannot affect the comparison.
- Validate fixtures, ground truth, runtime schema support, transport, and output capture independently from candidate outputs before scoring.
- Record infrastructure, transport, schema, and missing-artifact failures as invalid runs rather than model inaccuracy unless the frozen task contract explicitly assigns that failure to the candidate.
- Preserve exact configuration, raw responses, usage events, stderr or transport evidence, elapsed time, validity, scores, stage rankings, and advancement evidence in a declared durable evidence location.
- Resume by reusing only completed schema-valid runs. Deterministic rescore must use retained evidence and make zero new live calls.
- Advance candidates only through frozen stage rules. Offer a wide round, smaller semifinal, and multi-case final as a useful default without imposing it when the caller declares another valid shape.
- Require repeated leading-candidate trials when variance matters and label one run per case as screening evidence rather than statistical proof.
- Require an independent reviewer or deterministic verifier to audit advancement, scoring, and the winner when the decision is material.
- Require an explicit ranking policy. When the user supplies none, offer accuracy first with no implicit equivalence, estimated cost second within the same accuracy tier, costs within 15 percent of the cheaper candidate treated as equivalent, and lower wall-clock time used only within that equivalent-cost band.
- Calculate uncached input without double counting cached usage:

```text
uncached input = max(total input - cached input, 0)
```

- Price uncached input, cached input, and output separately. Never invent pricing; retain an unpriced candidate's accuracy and token evidence and mark any cost-dependent win provisional unless the user supplied an accepted comparison rule.
- Report the winner, complete ranking, costs, timing, misses, invalid runs, limitations, confidence, and provisional status. Map the selected provider configuration to a semantic model profile without placing provider IDs in reusable conceptual agent definitions.
- Include data-safety language that prevents prohibited PII or company-confidential material from being sent to candidate models unless its use was explicitly authorized.
- Do not build a universal domain scorer, prescribe a model family or reasoning effort, treat synthetic fixtures as real-world completeness proof, replace domain reviewers or ground-truth owners, duplicate harness instructions, or install, deploy, publish, or activate a selected configuration automatically.

## Acceptance Criteria

- The skill triggers for comparative agent or model selection and does not trigger for ordinary single-model testing.
- Material ambiguity in the varied factor, constants, candidates, ground truth, ranking policy, budget authority, or data-safety boundary stops live calls and produces concise clarification.
- Plan-only and deterministic-rescore modes work without live-run approval; deterministic rescore makes zero live calls.
- Case inputs remain byte-equivalent and controls vary one factor at a time unless the frozen contract explicitly records a multi-factor exception and its limitation.
- Infrastructure, schema, transport, and missing-artifact failures remain invalid runs and are not silently scored as candidate false negatives.
- Completed schema-valid evidence can be resumed without rerunning it, and raw evidence is sufficient to audit validity, scoring, usage, timing, advancement, and selection.
- The default ranking keeps accuracy first, applies the declared 15 percent cost-equivalence tolerance only within the same accuracy tier, and uses speed only inside the equivalent-cost band.
- Cached input is priced only at its cached-input rate, uncached input cannot become negative, and an unpriced candidate remains visible with a provisional cost-dependent disposition.
- The workflow calls for repeated final trials when variance matters and labels a one-run result as limited evidence.
- Coordinator comparisons prove frozen runner evidence remained identical across candidates.
- Selection output maps provider configuration to a semantic model profile without hardcoding provider IDs into conceptual agent definitions.
- The skill prevents unauthorized PII or company-confidential data from entering tournament fixtures or model calls.
- The package remains concise and portable, with any reference, example asset, or execution helper justified against runtime neutrality and domain independence.
- Agent Skill validation, links, inventory assertions, generated documentation freshness, focused decision regressions, and the explicitly requested repository regression tests pass.

## Dependencies

None.

## Verification

- Validate the new skill package and its OpenAI metadata with repository-supported Agent Skill and metadata checks.
- Add a trigger regression that distinguishes comparative selection from ordinary single-model testing.
- Prove missing reviewed ground truth stops before live calls or produces a plan-only fixture proposal for approval.
- Prove ambiguous runner-versus-coordinator attribution triggers clarification.
- Prove missing live-run authority still permits a dry-run plan but makes no model call.
- Prove a malformed response is retained as an invalid run and is not scored as a false negative.
- Prove deterministic rescore reuses valid evidence and makes zero live calls.
- Prove cached usage receives only the cached-input rate for that portion and uncached input uses the nonnegative formula.
- Prove the best-accuracy unpriced candidate is reported as a provisional winner when ranking depends on cost.
- Prove equal-accuracy candidates inside the 15 percent cost band are ordered by speed, while a candidate outside the band loses on cost before speed.
- Prove frozen runner evidence is byte-identical across coordinator candidates.
- Prove a one-run final report states that variance is unmeasured.
- Run the affected catalog, inventory, link, documentation-generation, generated-freshness, and bundle-content checks; then run the repository regression scope explicitly requested by the source notes and git diff --check.
- Obtain independent methodology review and verification focused on clarification safety, attribution controls, invalid-run handling, deterministic reuse, cost arithmetic, data safety, portability, and honest confidence claims.

## Open Questions

- Determine whether the concise skill alone can express the full contract or whether the approved tournament-contract reference materially improves usability.
- Determine whether the optional example configuration adds portable value without implying provider-specific defaults.
- Determine whether a generic execution helper can remain runtime-portable and domain-agnostic; omit it if it would own domain scoring or duplicate harness behavior.
- Determine the smallest existing evaluation and catalog surfaces that can prove the required decision scenarios without creating a generic evaluation framework.

## Governed Definition Approval

### Governed Canonical Sources

- skills/run-agent-tournament/SKILL.md
- skills/run-agent-tournament/agents/openai.yaml
- skills/run-agent-tournament/references/tournament-contract.md

The tournament-contract reference is approved as an optional exact source path, not a mandatory artifact. Creating a differently named skill or any additional governed definition requires separate exact-path approval.

### Allowed Dependent Artifacts

- skills/run-agent-tournament/assets/tournament.example.yaml
- README.md
- design/skills-modularization.html
- design/agent-and-skill-evaluations.html
- design/agent-skill-hierarchy.svg
- design/agent-skill-test-coverage-checklist.md
- design/generated/agent-skill-explorer-data.js
- design/generated/skill-definitions.js
- evals/skill-probes.yaml
- evals/workflow-packs.yaml
- scripts/test_bundle_content.py

The example asset is optional. Generated artifacts remain generator-owned and must be regenerated from approved sources rather than hand-edited. The listed evaluation and test surfaces may change only for decision scenarios directly required by this item. No conceptual agent definition, model-profile source, role schema, existing skill definition, or user-level installation path is authorized by implication.

### Approval Resolution

Approved at creation on 2026-08-09. The user directly requested creation of this backlog item and supplied notes whose preferred package names skills/run-agent-tournament/SKILL.md, skills/run-agent-tournament/references/tournament-contract.md, and skills/run-agent-tournament/assets/tournament.example.yaml. The requested trigger also requires the standard skills/run-agent-tournament/agents/openai.yaml metadata source used by this repository. User-message provenance is the direct message and attached Work-Item Notes in the Codex task that created this item. Approval is limited to the exact governed sources and dependent artifacts listed above and does not authorize publication or changes to other governed definitions.

## Notes

- Treat the documentation-design-system harness and tournament reports as requirements evidence, not code that must be copied into the portable package.
- Preserve the experiment's lessons: runner and coordinator attribution must remain separate, schema support must be validated before spending credits, cached-token corrections must be deterministically rescored, and five synthetic single-run cases support screening rather than a high-confidence claim.
- Return the final skill name and trigger, authoritative and generated paths, clarification examples, verification outputs, portability rationale for optional artifacts, deviations with reasons, and the source-review commit hash before any user-level publication.
- Do not absorb or mutate Work Item ID integrate-documentation-design-system as part of this feature.

## Starting Handoff Evidence

Starting Recorded At: 2026-08-09T04:32:00Z

Coordinator: Dev Backlog Coordinator task `019fb057-1767-7ef2-b5fa-41f4417b20b3`

Normalized Objective: Implement the approved portable `run-agent-tournament` skill and its exact optional reference, metadata, focused decision scenarios, and repository-owned projections while preserving domain ownership, clarification and data-safety gates, deterministic evidence reuse, ranking semantics, and the no-publication boundary.

Launch Result: Requested after this durable reservation.

Canonical Execution: None

Intended Root Role: Dev Orchestrator

Scheduling Evidence: Provider inventory has one Running item, `publish-and-integrate-terminology-standard`, one Blocked item, and no duplicate tournament task or claim. The tournament item has Dependencies: None and may begin the non-overlapping private `skills/run-agent-tournament/**` package and focused planning lane. Defer shared or overlapping mutation involving `README.md`, `design/agent-and-skill-evaluations.html`, `design/agent-skill-hierarchy.svg`, `design/agent-skill-test-coverage-checklist.md`, generated skill catalogs, `evals/skill-probes.yaml`, `evals/workflow-packs.yaml`, `scripts/test_bundle_content.py`, shared review, installation, or main integration until the active terminology owner provides direct release/reconciliation evidence. The Blocked documentation-design-system candidate is evidence only and must not be mutated or absorbed.

Preservation Boundary: Use one new isolated canonical worktree and task. Do not reuse source task `019fe4be-9c87-7823-8594-80b432af6237`; it only notified the Coordinator that the backlog changed and has no provider reservation. No source mutation is authorized until the new canonical Root Dev Orchestrator independently records Starting -> Running with fresh bounded Active Execution Evidence and an exact activity=work claim.

Next Reconciliation At: 2026-08-09T04:47:00Z

## Active Execution Evidence

Condition Type: delegated-work

Owner: Dev Coder execution /root/tournament_skill_coder under Dev Orchestrator task 019fe4cb-b4f3-7563-8ece-a60e567aae29

Evidence: Fresh read-only Dev Code Reviewer execution /root/tournament_source_review and Methodology Artifact Reviewer execution /root/tournament_methodology_review both returned NEEDS_CORRECTION for replacement candidate 310fd8b09c04004132d3c332f3c924d87af46a87. The original six review themes are substantially closed, but the independent verdicts identify five bounded consistency defects: retry attempts must be exactly enumerable and authorized; complete candidate coverage must consistently permit an explicit partial order and prohibit a cost-dependent unpriced tie from being reported as winner or advancement; frozen variance policy mode must be separated from observed state with aligned provisional-stage advancement semantics; zero-call transport preflight needs caller-owned proof equivalent to deterministic-rescore proof; and every example matrix row needs an explicit nondeterminism control. Original Dev Coder execution /root/tournament_skill_coder is applying correction attempt 2 of at most 2 to exactly skills/run-agent-tournament/SKILL.md, skills/run-agent-tournament/agents/openai.yaml, skills/run-agent-tournament/references/tournament-contract.md, and skills/run-agent-tournament/assets/tournament.example.yaml while preserving the accepted provenance envelope and adding focused assertions. Configured MCP validation remains the known outside-configured-root deferred gate and is not counted as a pass. README, design, generated catalogs and projections, adapters, eval catalogs, scripts/test_bundle_content.py, shared installation, live-model evaluation, and main integration remain retained by terminology and excluded. Exact Work Item activity=work claim add-portable-agent-tournament-skill-019fe4cb-root-work remains live and was heartbeated at 2026-08-09T06:07:00.618412Z, journal event c24fdd83-be42-4f02-b75e-640ccfb40290. This final-correction refresh is protected by exact backlog-path claim add-portable-agent-tournament-skill-019fe4cb-correction-evidence-2, outcome SHARED_CHECKOUT_ACQUIRED, journal event 1ce82b05-f7cc-4660-89ab-6806ff6cc37c.

Observed At: 2026-08-09T06:07:07Z

Started At: 2026-08-09T06:06:00Z

Deadline or Expires At: 2026-08-09T06:35:00Z

Next Action: Collect the clean final correction commit from original Dev Coder execution /root/tournament_skill_coder, then dispatch both independent reviewers for the last exact-manifest re-review before any focused verifier work

Next Reconciliation At: 2026-08-09T06:21:00Z

## Running Resource Claim Evidence

Work Claim: add-portable-agent-tournament-skill-019fe4cb-root-work; Work Item ID add-portable-agent-tournament-skill; activity work; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T04:37:15.407440Z; journal event 8ed3dca6-9a12-40a7-ac10-8f2b6bb5e4b4; retained through bounded outcome work

Provider Path Claim: add-portable-agent-tournament-skill-019fe4cb-running-backlog; path backlog/feature-backlog/add-portable-agent-tournament-skill.md; outcome SHARED_CHECKOUT_ACQUIRED; acquired at 2026-08-09T04:37:20.997294Z; journal event 7170bb08-1505-4da5-9961-3f9fa9646af1; release immediately after the Running provider transaction
