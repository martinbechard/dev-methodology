# Terminology Standard Effect Experiment

## Outcome

The positive-first strategy worked for 34 of 35 concepts without negative rules. The positive-only treatment replaced the scratchpad candidates `receipt` and `rollout` with their preferred terms but retained `campaign` for the stable Test suite concept. One narrowly scoped `Campaign` rule under `Test suite` removed that final substitution in a second treatment.

Do not add `Receipt` or `Rollout` rules from this experiment. Their positive definitions were sufficient.

## Frozen Comparison

The red control and positive-only treatment used:

- the `dev-documentation-writer` Agent;
- model `gpt-5.5` through Codex CLI 0.144.1;
- the same task, source document, project guidance, sandbox profile, and approved input-manifest digest `be5a04fcd4027dd4dbaffd550a075088015a84b01afc7a6b94d6c9259ef5b9ac`;
- probe comparison key `8cbfb52290460f5fc5625f87f3008b757e1450c88a793a31600d5f22a709222c`; and
- the same evaluator-owned deterministic verifier.

Only the staged `terminology-standard` skill differed. The reinforced treatment changed the standard bytes by adding the one evidence-backed rule, so its input-manifest digest is `e4767170ef87125b59048cae9efbb6a9d477e02a5ab4dca9035f0847f52e884b` and it is a second experimental phase rather than part of the frozen first comparison.

## Results

| Run | Standard phase | Meaning | Preferred terms | Scratchpad observations |
|---|---|---:|---:|---|
| Red control | Skill omitted | 35/35 markers and 10/10 literals | 1/35 | `receipt`, `rollout`, and `campaign` for Test suite persisted |
| Treatment 1 | Positive-only | 35/35 markers and 10/10 literals | 34/35 | Only `campaign` for Test suite persisted |
| Treatment 2 | One scoped Campaign rule | 35/35 markers and 10/10 literals | 35/35 | None |

The detailed deterministic summaries are:

- [red-control-verifier.json](red-control-verifier.json)
- [positive-only-treatment-verifier.json](positive-only-treatment-verifier.json)
- [reinforced-treatment-verifier.json](reinforced-treatment-verifier.json)

## Evidence Boundary

Each live invocation returned `HARNESS CAPTURE PASS` with only `rewritten-document.md` and `eval-result.md` changed inside its disposable workspace. The event-capture filenames and SHA-256 digests are retained in the JSON summaries.

The captures emitted one rejected initial full-history custom-Agent fork before retrying with a compatible fresh-context dispatch. The requested document-writer child then completed the rewrite. These runs establish a plausible terminology effect and deterministic artifact result; they are not full three-variant, independently judged skill-probe evidence, and they do not claim security containment or calibrated Model Judge approval.

## Decision

Keep the Terminology Standard compact and positive-first. Retain exactly one evidence-backed Avoid rule for Campaign under Test suite. This evidence supports project publication and production routing through the generated Agent and staged skill. Formal probe evidence must use that production route without fixture-level Agent guidance.
