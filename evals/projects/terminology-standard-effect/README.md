# Terminology Standard Effect Fixture

This fixture measures whether a positive-first Terminology Standard attracts a Dev Documentation Writer toward preferred software-development terms without removing meaning.

The production evaluation route selects the generated Dev Documentation Writer Agent. The Agent conditionally loads the terminology-standard skill when the harness stages that skill. The treatment loads `terminology.md` through the configured reference provider. The fixture does not inject project-level Agent guidance.

The probe runner derives three variants from one frozen case:

- treatment stages the terminology-standard skill and enables its reference-provider contract;
- target-omitted removes and forbids that skill and removes the provider contract; and
- wrong-skill removes and forbids that skill, removes the provider contract, and stages quartz as the control.

All variants retain the same Agent, prompt, source bytes, model profile, sandbox, and evaluator-owned verification command. The non-model-visible verifier checks preferred terms, semantic markers, and protected literals. It reports scratchpad candidates separately. Those observations do not become normative Avoid rules without retained reinforcement evidence.

The independently selectable negative-activation case stages the same production Agent without terminology-standard. Its deterministic verifier proves that raw evidence, exact identifiers, commands, quotations, and source-native wording remain byte-faithful and outside terminology rewriting.

The retained [experiment results](evidence/experiment-results.md) record the red control, positive-only treatment, and reinforced treatment. The accepted standard keeps exactly one evidence-backed Avoid rule for Campaign under Test suite. The concise JSON summaries preserve the deterministic outcomes without promoting the local harness captures to full Judge-passed probe evidence.
