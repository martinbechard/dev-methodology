# Publish and Integrate the Terminology Standard

Status: Ready

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
