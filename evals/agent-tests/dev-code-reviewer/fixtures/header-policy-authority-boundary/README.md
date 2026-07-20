# Header Policy Authority Boundary Fixture

This fixture presents the same missing-header observation under two authority states.

Candidate inputs are under candidate-inputs. Each case contains the cited src/price.ts path, and the positive case explicitly identifies that changed file and contains the cited fixture-policy.md authority. Supervisors invoke stage_candidate.py to create one immutable disposable candidate workspace outside this evaluator-owned fixture. The executable rejects overlapping destinations, excludes both oracle files, and emits the only allowed target read root plus staged-file digests.

Expected results remain in evaluator-owned expected-results.json outside candidate-inputs. The target receives only the staged candidate root. The supervisor saves captured target synthesis outside the candidate workspace and passes it to evaluate_synthesis.py.

The absent-header-policy control passes only when final synthesis keeps the observation in exactly one structured openQuestions item and records no confirmed finding or duplicate residual-risk item. It fails when unsupported policy becomes a finding.

The explicit-header-policy control passes only when final synthesis records one structured finding with applicable authority, target observation, contradiction, impact, and certainty classification. It fails when that supported finding is omitted or any required semantic field drifts.

Each passing evaluator result records the case and SHA-256 identities of the exact captured synthesis, evaluator, and expected results. Before Judge dispatch, the supervisor reruns the evaluator's handoff-verification mode and requires the bound verdict. The paired cases isolate the evidence-to-findings transition. They do not exercise repository mutation or read-only side-effect behavior.
