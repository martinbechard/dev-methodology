# Terminology Effect Evaluation Guidance

This synthetic project temporarily injects the Terminology Standard at the project-guidance layer. The production Dev Documentation Writer definition is the subject of a later work item and must not be changed during this evaluation.

- Apply the Dev Documentation Writer role to the requested custom-document rewrite.
- When `terminology-standard` is present among the harness-supplied skills, load it completely and apply the project-root `terminology.md` through its project-only fallback if the reference provider is unavailable.
- When `terminology-standard` is absent, complete the rewrite without reading or applying `terminology.md`. Record the missing skill in `eval-result.md`; do not treat the intentional omission as a blocker.
- Preserve exact semantic markers, identifiers, commands, numbers, and factual claims from `source-document.md`.
- Do not edit `AGENTS.md`, `terminology.md`, or `source-document.md`.
- Review the rewrite against the source before finishing. The evaluator runs its own non-model-visible deterministic verification after the Agent returns.
