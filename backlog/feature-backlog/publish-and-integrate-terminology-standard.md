# Publish and Integrate the Terminology Standard

Owner: Dev Orchestrator task 019fe3d6-2dd6-7322-a507-e8ca961e27d8

Canonical Conversation: `019fe3d6-2dd6-7322-a507-e8ca961e27d8`

Canonical Task: `019fe3d6-2dd6-7322-a507-e8ca961e27d8`

Branch: `codex/publish-and-integrate-terminology-standard-019fe3d6`

Worktree: `/Users/martinbechard/.codex/worktrees/940b/dev-methodology`

Phase: Implementing — Approved treatment-only provider contract

Status: Running

Type: Feature

Provider: file

Work Item ID: publish-and-integrate-terminology-standard

Completion: main-branch

## Summary

Publish the reviewed software-development Terminology Standard as the official project standard, integrate its application and review skills through production Agent routing, and convert the terminology-effect evaluation from temporary `AGENTS.md` injection to production routing with complete control evidence.

## Context

The reviewed draft and negative scratchpad are preserved under `evals/agent-tests/dev-documentation-writer/fixtures/terminology-standard-effect/review/`. The clean evaluation candidate is `evals/projects/terminology-standard-effect/terminology.md`.

The red/green experiment is retained in `evals/projects/terminology-standard-effect/evidence/experiment-results.md`. The target-omitted control preserved all meaning but used only 1 of 35 preferred terms. The positive-only treatment used 34 of 35 terms and independently removed the `receipt` and `rollout` candidates. It still used `campaign` for the stable Test suite concept. Commit `a85380e51b120d23cebe1259b9dbf17b37fcba89` added one scoped `Campaign` rule under `Test suite`; the second treatment then passed 35 of 35 terms, 35 of 35 semantic markers, and 10 of 10 protected literals with no remaining scratchpad observations.

The experimental fixture currently activates `terminology-standard` through `evals/projects/terminology-standard-effect/AGENTS.md`. That injection is intentionally temporary. Production evaluation must prove that the applicable Agent and skill routing activate the standard without fixture guidance while target-omitted and wrong-skill controls remain uncontaminated.

Current canonical Agent definitions already reference the terminology family in several writing and review roles. Delivery must audit those references against the accepted scope, update only proven gaps, and regenerate supported adapters from canonical sources rather than editing generated files.

## Source Evidence

The user requested this work on 2026-08-08 in task `019fe2b3-4bcd-7f00-88aa-90e281b8f8bf`: “Once we have something that seems plausible, we'll need a work item to update appropriate skills or agent definitions, as well as updating the evals not to inject the skills in AGENTS.md.” The same request authorized a red/green document-writer evaluation, positive-only definitions first, and evidence-based negative rules only when the preferred definitions were insufficient.

Supporting repository evidence:

- `74e2da0cbd2da8793dc5b069f9d9fc2957c13480` preserves the reviewed standard and scratchpad.
- `60354de8471576969f8115e5702f8141b726a21b` adds the paired terminology-effect evaluation.
- `a85380e51b120d23cebe1259b9dbf17b37fcba89` adds the one evidence-backed `Campaign` reinforcement.
- `3c82463b3b879e1fff076373bc0430144c046471` preserves the deterministic experiment summaries.

## Requirements

- Publish the accepted candidate as the project-root `terminology.md` through `terminology-standard-update`, including refresh, load, revision, and target-digest verification with the configured reference provider.
- Keep the standard positive-first. Retain exactly the evidenced `Campaign` rule under `Test suite`; do not add speculative `Receipt`, `Rollout`, or synonym rules.
- Preserve the distinctions among Test suite, Test run, Evaluation portfolio, Evaluation suite, Evaluation, Evaluation case, Evaluation run, Campaign, Evaluation result, and Evaluation decision.
- Review generated and hand-authored evaluation prose, including the source that owns `design/agent-and-skill-evaluations.html`, and use Test suite, Test run, Test report, Evaluation portfolio, or Campaign according to the defined concept. Preserve exact identifiers, schemas, commands, quotations, and source-native Evidence.
- Audit the approved canonical Terminology Standard skills and Agent definitions. Update only paths whose current routing or instructions do not implement the accepted application, review, or update boundary.
- Regenerate supported Agent adapters and methodology projections from canonical sources after any governed definition change. Do not hand-edit generated adapters.
- Remove the temporary terminology activation from `evals/projects/terminology-standard-effect/AGENTS.md`. Remove the file if no non-terminology fixture guidance remains.
- Update the terminology-effect case and scenario so the treatment receives `terminology-standard` through production Agent or evaluation routing, while `target-omitted` genuinely removes it and `wrong-skill` cannot reintroduce it.
- Add or link the negative-activation case required by the skill-probe framework. Preserve the same prompt, source, Agent, model, reasoning profile, sandbox, and deterministic verifier across comparable variants.
- Run the treatment, target-omitted, and wrong-skill variants and retain current receipts. Do not promote the probe to full coverage until the framework's paired-run and independent Judge requirements are satisfied.
- Keep the reviewed draft, scratchpad, positive-only result, reinforced result, and decision rationale available as durable evaluation evidence.
- Treat shared user publication as a separate explicit scope selection. This item authorizes project publication and methodology integration; it does not infer a shared user mutation target.

## Acceptance Criteria

- A project-root `terminology.md` contains all 35 accepted preferred terms and exactly one `Avoid` entry: the scoped `Campaign` rule under `Test suite`.
- `reference_refresh` followed by `reference_load` reports the published project standard at the same catalog revision and includes a source digest matching the validated project file.
- `terminology-standard-review` passes the project standard and the rewritten evaluation document against the provider-returned snapshot.
- `design/agent-and-skill-evaluations.html` and its owning source use the accepted testing and evaluation terms according to concept, with no blind substring replacements.
- The approved Agent audit records every applicable writer and reviewer, the terminology skill each consumes, and either the exact canonical change or evidence that the current definition already conforms.
- Every generated adapter and maintained methodology projection affected by canonical changes is regenerated and passes stale-output checks.
- No terminology-effect evaluation depends on `evals/projects/terminology-standard-effect/AGENTS.md` to activate `terminology-standard`.
- The target-omitted control remains red for preferred terminology while preserving all 35 semantic markers and protected literals.
- The production-routed treatment is green for all 35 preferred terms and has no scratchpad candidate occurrence.
- The wrong-skill control receives no terminology credit, and a linked negative-activation case proves the skill does not activate for excluded raw evidence or exact identifiers.
- No `Receipt` or `Rollout` `Avoid` rule is added unless new retained evidence independently satisfies the promotion threshold.
- The complete focused and repository-wide verification set passes on the final main commit.

## Dependencies

None.

## Verification

- Run `python3 -m unittest -q scripts/test_terminology_standard_effect_fixture.py`.
- Run `python3 scripts/run-agent-skill-evals.py --validate-catalogs`.
- Run treatment, target-omitted, and wrong-skill terminology probe variants with the same supported harness and model profile; retain and validate their receipts and paired comparison evidence.
- Run the focused generator tests that own `design/agent-and-skill-evaluations.html` and rebuild the page from its source.
- Run `python3 scripts/test_bundle_content.py` and the applicable installer, adapter, stale-output, and repository bundle checks.
- Invoke `reference_refresh` and `reference_load` through the configured MCP server and retain the revision and source-digest evidence.
- Run `terminology-standard-review` against the published standard and the rewritten evaluation Artifact.

## Open Questions

- Which smallest evaluation-routing change can remove fixture-level `AGENTS.md` activation while preserving a truly omitted target-skill control?
- Do any currently listed canonical Agent definitions need byte changes, or do their existing terminology references already satisfy the accepted production routing contract?

## Governed Definition Approval

### Governed Canonical Sources

- `skills/terminology-standard/SKILL.md`
- `skills/terminology-standard-review/SKILL.md`
- `skills/terminology-standard-update/SKILL.md`
- `agents/roles/dev-activities/dev-artifact-reviewer.role.yaml`
- `agents/roles/dev-activities/dev-code-reviewer.role.yaml`
- `agents/roles/dev-activities/dev-coder.role.yaml`
- `agents/roles/dev-activities/dev-documentation-writer.role.yaml`
- `agents/roles/dev-activities/dev-prompt-reviewer.role.yaml`
- `agents/roles/dev-activities/dev-ux-specialist.role.yaml`
- `agents/roles/methodology-maintenance/methodology-artifact-reviewer.role.yaml`
- `agents/roles/methodology-maintenance/methodology-maintainer.role.yaml`
- `agents/roles/wiki-activities/wiki-architect.role.yaml`
- `agents/roles/wiki-activities/wiki-artifact-reviewer.role.yaml`
- `agents/roles/wiki-activities/wiki-ingester.role.yaml`
- `agents/roles/wiki-activities/wiki-topic-verifier.role.yaml`
- `agents/roles/wiki-activities/wiki-writer.role.yaml`

### Allowed Dependent Artifacts

- `terminology.md`
- `README.md`
- `design/agents/terminology-standard.md`
- `design/agent-and-skill-evaluations.html`
- `scripts/build-agent-skill-evaluation-docs.py`
- `scripts/test_agent_skill_evaluation_docs.py`
- `scripts/test_bundle_content.py`
- `evals/agent-scenarios.yaml`
- `evals/cases.yaml`
- `evals/skill-probes.yaml`
- `evals/workflow-packs.yaml`
- `evals/projects/terminology-standard-effect/AGENTS.md`
- `evals/projects/terminology-standard-effect/README.md`
- `evals/projects/terminology-standard-effect/TASK.md`
- `evals/projects/terminology-standard-effect/source-document.md`
- `evals/projects/terminology-standard-effect/terminology.md`
- `evals/projects/terminology-standard-effect/evidence/experiment-results.md`
- `scripts/test_terminology_standard_effect_fixture.py`
- Generator-owned mirrors under `generated/adapters/claude/agents`, `generated/adapters/codex/agents`, `generated/adapters/gemini/agents`, and `generated/adapters/junie/agents` for canonical Agent definitions changed by this item.

### Approval Resolution

Approved at creation. On 2026-08-08, user message provenance task `019fe2b3-4bcd-7f00-88aa-90e281b8f8bf` explicitly requested “a work item to update appropriate skills or agent definitions, as well as updating the evals not to inject the skills in AGENTS.md.” This approval covers only the exact canonical sources listed above and their listed dependent artifacts. Additional governed definition paths require separate scope-specific approval.

## Notes

The experiment is evidence for compactness: positive definitions corrected 33 of the 34 initially nonpreferred concepts without negative rules. The single `Campaign` rule corrected the remaining persistent substitution. Keep this evidence-to-rule threshold as the maintenance default.

## Starting Handoff Evidence

Starting Recorded At: 2026-08-09T00:04:08Z

Coordinator: Dev Backlog Coordinator task `019fb057-1767-7ef2-b5fa-41f4417b20b3`

Normalized Objective: Publish the accepted software-development Terminology Standard as the official project standard, integrate its approved application and review routing into production methodology sources, remove temporary evaluation injection, and verify treatment, target-omitted, and wrong-skill controls without inferring shared user publication.

Launch Result: Requested

Canonical Execution: None

Runtime Request: `client-new-thread:37b63398-6a78-48dd-a146-6b7b97b7a38b` (worktree setup queued; not a canonical task identifier)

Last Contact At: 2026-08-09T00:04:58Z

Next Reconciliation At: 2026-08-09T00:19:58Z

Intended Root Role: Dev Orchestrator

Scheduling Evidence: One other provider item, `integrate-documentation-design-system`, is Running in an independent private worktree. This item may begin private terminology publication, exact governed-path prechecks, production-routing analysis, and fixture work. Defer exact overlapping edits or shared events involving `README.md`, evaluation catalogs, `scripts/test_bundle_content.py`, generated adapters, live-model evaluation, shared installation, or main integration until the active owners exchange a direct release/reconciliation notification. Do not poll, overwrite, absorb, or duplicate the documentation-design-system work.

## Preserved Running Execution Evidence

Condition Type: root-execution

Owner: Dev Orchestrator task 019fe3d6-2dd6-7322-a507-e8ca961e27d8

Evidence: canonical combined Codex task/thread surface 019fe3d6-2dd6-7322-a507-e8ca961e27d8 remains the current active root execution in branch codex/publish-and-integrate-terminology-standard-019fe3d6 and worktree /Users/martinbechard/.codex/worktrees/940b/dev-methodology; all 16 exact approved governed-definition paths returned ALLOWED_APPROVED_DEFINITION_CHANGE and all 13 approved Agent definitions conform without mutation. Dev Coder commits ec35759032051479bda3518cd892a4480119c41b, 38825214eaee66433ae50c7cbafd3f6af407a2da, and 2ee1d3968f710175810131c60d88def629e89d99 remove the fixture-only AGENTS.md injection, define a byte-preserving negative fixture, and begin correcting evaluation-document terminology. Fresh follow-up review confirms the premature proof claims and tautological negative check are corrected but identifies two remaining generated-copy corrections. Read-only production-routing analysis also proves that provider-backed treatment cannot run through the current probe runner without changing runner and evidence-contract paths outside the exact Allowed Dependent Artifacts; those paths remain unmutated pending explicit scope reconciliation. The configured mcp-agent-ops 0.5.1 provider still lacks reference_refresh and reference_load, and the acknowledged overlap owner has not released shared catalogs, generated output, installation, live-model evaluation, or main integration, so terminology.md publication remains correctly unmutated.

Observed At: 2026-08-09T00:57:02Z

Started At: 2026-08-09T00:09:34Z

Deadline or Expires At: 2026-08-09T02:09:34Z

Next Action: Complete the two bounded evaluation-copy corrections and fresh review, obtain explicit reconciliation for the out-of-scope provider-backed probe paths, then use the direct owner release to reconcile shared catalogs and generated output, restore the configured reference provider, publish the project standard, and run the bounded controls

Next Reconciliation At: 2026-08-09T01:12:02Z

## User Action Required

Recorded At: 2026-08-09T01:03:19Z

Question: Do you approve adding exactly `scripts/run-agent-skill-evals.py`, `scripts/agent_skill_evals/invocations.py`, `scripts/agent_skill_evals/staging.py`, `scripts/agent_skill_evals/validation.py`, `scripts/test_agent_skill_evals.py`, `evals/evidence-schema.yaml`, and `evals/README.md` to this work item's dependent scope so the production-routed terminology treatment can use a staged reference provider while the target-omitted and wrong-skill controls remain provider-free?

Why User Input Is Required: These seven paths change the shared evaluation runner, shared invocation/staging/validation behavior, the shared evidence schema, and the authoritative runner guide. They are outside the exact approved dependent manifest and exceed the standing exemption for non-distributed suite-local evaluation artifacts. The Coordinator cannot infer authority for this cross-suite framework change.

Approval Consequence: Approval authorizes only the seven exact paths above for the treatment-only provider contract, exact control stripping, matching evidence validation, focused tests, and corresponding runner documentation. It does not authorize another governed definition, shared user publication, unrelated framework work, or absorption of baseline failures. The same canonical task resumes through User Action Required -> Ready -> Starting -> Running before mutation.

Decline Consequence: Declining leaves the provider-backed production treatment unavailable. The preserved candidate cannot meet the current acceptance criteria without a separately authorized design or a revised terminal disposition.

Unattended Work Boundary: Stop all source mutation, generator-copy correction, catalog reconciliation, shared installation, live-model evaluation, provider publication, review completion, main integration, and provider completion for this item. Preserve the clean candidate and review evidence. The independent documentation-design-system item may continue.

Resolution: Approved. Resume the same canonical task through Ready -> Starting -> Running before any source mutation.

Approval Resolution: On 2026-08-09, the user answered `approved` in parent task `019fe2b3-4bcd-7f00-88aa-90e281b8f8bf`, approving exactly the seven paths named in the question. This approval authorizes only the treatment-only provider contract, control stripping, evidence validation, focused tests, and runner documentation on those paths. It does not authorize shared-user publication, unrelated framework scope, another governed definition, or baseline absorption.

## Scope Decision Preservation Evidence

Canonical Task: `019fe3d6-2dd6-7322-a507-e8ca961e27d8`

Branch: `codex/publish-and-integrate-terminology-standard-019fe3d6`

Worktree: `/Users/martinbechard/.codex/worktrees/940b/dev-methodology`

Preserved Candidate Commits: `ec35759032051479bda3518cd892a4480119c41b`, `38825214eaee66433ae50c7cbafd3f6af407a2da`, and `2ee1d3968f710175810131c60d88def629e89d99` (clean HEAD)

Uncommitted Bytes: None

Review State: NEEDS CORRECTION. Premature production-proof claims and the tautological negative check are corrected. Two generator-copy corrections remain unstarted. The high boundary is that current probe preflight still references the deleted fixture `AGENTS.md` and cannot support the provider-backed treatment without the seven-path scope above.

Focused Evidence: Terminology fixture 10/10 passed; focused copy tests 2/2 passed; documentation tests 27/29 with one disclosed stale generated HTML result and one unrelated historical-ID baseline failure; `git diff --check` passed. No live-model, provider publication, shared installation, final review PASS, integration, or delivery evidence exists.

Work Claim Release: Exact activity=work claim `publish-and-integrate-terminology-standard-019fe3d6-root-work` released with disposition handoff, event `cacfdbc6-e440-4e21-845f-8307b1fc07c1`; no claim for this Work Item ID remained at handoff.

Already Approved Related Paths: `evals/projects/terminology-standard-effect/README.md` and `design/agent-and-skill-evaluations.html` remain approved dependents. `evals/cases.yaml`, `evals/agent-scenarios.yaml`, and `evals/skill-probes.yaml` remain deferred until the documentation-design-system owner releases the overlapping shared boundary. No change to `evals/workflow-packs.yaml` is currently required.

Explicit Exclusions: `README.md`, `design/agentic-configuration.html`, `evals/agent-tests/README.md`, `design/agent-skill-test-coverage-checklist.md`, `scripts/build-support-checklist.py`, runtime receipt paths, `scripts/test_bundle_content.py`, generated adapters, shared installation, live-model evaluation, catalogs, and main integration receive no new scope from this question.

## Provider Transaction Recovery Evidence

The initial exact commit attempt stopped before creating a commit because the moved source path no longer matched a worktree pathspec. Recovery then staged the claimed destination only. Commit `0e32c034` durably created the complete User Action Required destination but, because `git commit --only` selected only that destination, left the already-staged source deletion pending. The immediately following recovery commit records this evidence and removes only the claimed active source path. No unrelated file was staged or committed, and the final provider state has one unique Work Item ID at this User Action Required path.

## Approval Resumption Evidence

Approval Recorded At: 2026-08-09T04:24:00Z

Approval Provenance: Direct user answer `approved` in parent task `019fe2b3-4bcd-7f00-88aa-90e281b8f8bf` on 2026-08-09, answering the exact pending seven-path question.

Approved Additional Dependent Paths:

- `scripts/run-agent-skill-evals.py`
- `scripts/agent_skill_evals/invocations.py`
- `scripts/agent_skill_evals/staging.py`
- `scripts/agent_skill_evals/validation.py`
- `scripts/test_agent_skill_evals.py`
- `evals/evidence-schema.yaml`
- `evals/README.md`

Approval Boundary: Preserve all prior candidate commits, exact governed approvals, existing exclusions, and deferred overlap evidence. This answer does not authorize shared-user publication, unrelated framework changes, additional governed definitions, or absorption of baseline failures.

Canonical Resumption: Preserve canonical task `019fe3d6-2dd6-7322-a507-e8ca961e27d8`, branch `codex/publish-and-integrate-terminology-standard-019fe3d6`, worktree `/Users/martinbechard/.codex/worktrees/940b/dev-methodology`, and commits `ec35759032051479bda3518cd892a4480119c41b`, `38825214eaee66433ae50c7cbafd3f6af407a2da`, and `2ee1d3968f710175810131c60d88def629e89d99`. Ready does not authorize source mutation; the same task must pass Ready -> Starting -> Running first.

## Approval Resumption Starting Handoff

Starting Recorded At: 2026-08-09T04:25:00Z

Coordinator: Dev Backlog Coordinator task `019fb057-1767-7ef2-b5fa-41f4417b20b3`

Canonical Execution: `019fe3d6-2dd6-7322-a507-e8ca961e27d8`

Launch Result: Existing canonical task requested to resume.

Approved Resumption Scope: The exact seven-path approval recorded in commit `967cc228d5cee11f64eb1e9866482ec4a6bc0a54`, together with the original governed sources and dependent boundaries. Shared-user publication, unrelated framework scope, additional governed definitions, and baseline absorption remain excluded.

Preservation Boundary: Retain the clean canonical worktree, branch, three preserved candidate commits, existing review evidence, and all prior exclusions. Do not repeat completed corrections or accepted gates. Do not mutate source before this same canonical task independently records Starting -> Running with fresh bounded evidence and an exact activity=work claim.

Next Reconciliation At: 2026-08-09T04:40:00Z

## Active Execution Evidence

Condition Type: root-execution

Owner: Dev Orchestrator task 019fe3d6-2dd6-7322-a507-e8ca961e27d8

Evidence: The same canonical root execution remains active on the preserved branch and worktree. Dev Coder commit ae70fda537537b2df45193447d73b0de6c1e9605 cleanly changes exactly the seven newly approved treatment-only provider paths; its full focused runner module passed 123 of 123 tests, focused reference and MCP regressions passed 13 of 13, post-commit new tests passed 5 of 5, catalogs validated, and all changed Python paths compile. One direct exact-manifest narrowing notice was sent to the independent add-portable-agent-tournament-skill task at this clean boundary while retaining future shared-surface reconciliation. A fresh Dev Code Reviewer is reviewing only the seven-path delta, and the original Dev Coder is separately correcting exactly the two previously unresolved generator-copy findings without touching generated HTML or another shared surface.

Observed At: 2026-08-09T05:08:40Z

Started At: 2026-08-09T04:27:45Z

Deadline or Expires At: 2026-08-09T06:27:45Z

Next Action: Reconcile the fresh seven-path source review and the exact two-file generator-copy correction, then obtain independent source verification without repeating accepted fixture gates or entering deferred shared surfaces

Next Reconciliation At: 2026-08-09T05:23:40Z
