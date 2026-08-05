# Prompt Contracts Review Checklist

- Question: Do instructions, input schemas, state, tools, outputs, and consumers agree on one contract?
- Question: Are tool arguments validated before authority or side effects are granted?
- Question: Are protected data and restricted operations excluded from model-facing context and tools?
- Question: Are retry, cancellation, resume, fallback, and terminal outcomes explicit and bounded?
- Question: Can repeated execution duplicate or partially apply a side effect?
- Question: Are parse, schema, tool, model, and downstream failures preserved and owned by the correct boundary?
- Question: Do evaluations cover malformed, adversarial, partial, repeated, and unavailable-dependency behavior?
- Question: Are assumptions and missing evidence separated from verified behavior?
