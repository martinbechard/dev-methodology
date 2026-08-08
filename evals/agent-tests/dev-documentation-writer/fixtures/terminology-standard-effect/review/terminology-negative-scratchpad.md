# Terminology Negative Scratchpad

This scratchpad records possible nonpreferred terms during the terminology test. It is not part of the Terminology Standard and has no normative force.

Do not publish this file with terminology.md. Promote a candidate only when a positive-only test still produces the candidate for a concept that the standard defines.

## Campaign

Status: Candidate for the positive-only test. Do not add an Avoid rule unless governed testing prose still uses campaign for a defined preferred concept.

Observed context:

Source sentence from design/agent-and-skill-evaluations.html:

> A static, source-reconciled view of how the bundle is evaluated, what the selected governed campaign established, and where definition freshness is unknown or current catalog evidence is missing.

Illustrative preferred wording:

> This page shows how the bundle is evaluated, what the selected test run established, and where evidence remains incomplete.

The source generator in scripts/build-agent-skill-evaluation-docs.py owns this wording. Focused assertions in scripts/test_agent_skill_evaluation_docs.py preserve it.

Possible preferred mappings:

- Test run for the execution of selected test suites.
- Test suite for a stable collection of related test cases.
- Test report for the retained summary of a test run.
- Test result, verdict, or evidence for information produced by the test run.

Boundary:

- Coordination phrases such as campaign-wide pause express a different concept. They are not evidence for a testing-language rule.

Promotion trigger:

- After terminology.md is loaded, test whether governed writing still uses campaign for one of the defined concepts.
- If the term persists, add a narrowly scoped Avoid entry to the matching preferred term and run a second pass.

## Rollout

Status: Candidate for the positive-only test. Do not add an Avoid rule unless governed testing prose still uses rollout for the defined test-run concept.

Observed context:

Source sentence from evals/agent-tests/README.md:

> The completed 26-suite, 78-scenario rollout is recorded in the complete agent-suite execution report.

Illustrative preferred wording:

> The completed test run of 26 suites and 78 scenarios is recorded in the complete agent-suite execution report.

Possible preferred mapping:

- Test run when the text means one execution of selected tests or test suites.

Boundary:

- Rollout can correctly describe a staged software release. A testing rule must not change that meaning.

Promotion trigger:

- Add an Avoid entry only if governed testing prose continues to use rollout for the defined test-run concept.

## Receipt

Status: Candidate for the positive-only test. Current evidence does not justify an Avoid rule because receipt also appears in exact evaluation contracts that terminology review must preserve.

Observed context:

Source sentence from evals/README.md:

> A receipt must reference the canonical instruction, manifest, candidate, governed evidence, and output artifacts; receipt summaries are compared with those artifacts rather than trusted directly.

Illustrative preferred wording for ordinary explanatory prose:

> An evidence record must reference the canonical instruction, manifest, candidate, governed evidence, and output artifacts. The evaluator compares the evidence-record summary with those artifacts instead of trusting the summary directly.

Evaluation schemas and exact identifiers also use receipt as part of their contract. Those names are outside the terminology rewrite scope.

Possible preferred mapping:

- Evidence record in ordinary explanatory prose.

Boundary:

- Preserve exact schema names, identifiers, field names, commands, and quoted evidence.

Promotion trigger:

- Add an Avoid entry only if ordinary prose continues to use receipt where evidence record expresses the defined concept more clearly.
