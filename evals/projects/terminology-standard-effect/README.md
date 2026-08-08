# Terminology Standard Effect Fixture

This fixture measures whether a positive-only `terminology.md` attracts a Dev Documentation Writer toward preferred software-development terms without removing meaning.

The harness runs one frozen case in two variants:

- `target-omitted` is the red control. The Terminology Standard skill is unavailable, and project guidance forbids direct use of `terminology.md`.
- `treatment` is the green candidate. The skill is staged, project guidance activates it, and the skill may use its explicit project-only fallback when the reference provider is unavailable.

Both variants use the same Agent, prompt, source bytes, model profile, sandbox, and evaluator-owned verification command. The non-model-visible verifier enforces positive term use and preservation of semantic markers and protected literals. It reports scratchpad candidates separately; those observations do not become normative `Avoid` rules unless a treatment run still reproduces them.
