# Agent And Skill Evaluations

These synthetic projects provide fixtures for agent and specialized skill evaluations without customer data. A fixture pass proves project behavior only; it does not prove which agent or skill produced the result.

Each case contains:

- A small buildable project.
- A bounded implementation task.
- Required fixed-role and folder skillsets.
- Review-evidence identifiers.
- Baseline verification commands.

Run fixture verification with:

```bash
python3 scripts/run-agent-skill-evals.py --install
```

To evaluate an agent, copy one project to a disposable working directory, capture the harness invocation and tool-call events, and save both eval-result.md and an evidence receipt matching evidence-schema.yaml. Then run:

```bash
python3 scripts/run-agent-skill-evals.py --case typescript-order-pricing --project-root /path/to/working-copy --result /path/to/working-copy/eval-result.md --evidence /path/to/working-copy/evidence.yaml
```

The receipt must identify the agent, harness, concrete model, current skill content digests, captured tool-call references for every required skill read, behavior assertions, command evidence, and independent verdict. Every evidence reference uses a relative file#marker value; the validator requires the referenced UTF-8 artifact and marker to exist beside or below the receipt. Invocation and skill-read references must identify exactly one JSON Lines harness event whose agent, harness, model, skill, and digest fields agree with the receipt. Read-only reviews also require equal before and after project hashes. Naming an agent or skill in a prompt or result is not evidence that it ran or loaded, and a receipt without its referenced artifacts is invalid.

The validator proves internal consistency, not the provenance of a trace file. Preserve the harness export or trusted continuous-integration artifact from which the normalized event ledger was derived, and have an independent evaluator attest that provenance before calling the run behavior-verified. Self-authored marker files or agent claims do not satisfy that trust boundary.

modelStages declarations are not execution evidence. Staged review is verified only when the receipt references separate evidence-extraction and synthesis invocations using the intended profiles.

The earlier observations in results/2026-07-09-live-agent-evaluations.md predate this proof contract and are not counted as verified behavior. Keep generated implementations in disposable working directories; retain reusable fixtures, receipts, independent verdicts, and concise result summaries in this repository.
