<!--
Copyright (c) 2026 Martin.Bechard@DevConsult.ca
AI attribution: Generated with AI assistance.
Summary: Explains the sealed checklist-review corpus and offline comparison runner.
-->

# Reconstruction Review Evaluation

This corpus supports controlled comparisons between a lower-cost checklist reviewer and the current reference reviewer. It does not invoke either model and contains no benchmark result.

Each invocation is captured independently as one JSONL record. Candidate and reference reviewers receive the same artifact, source evidence, checklist questions, and adjudicated defect set in fresh contexts. Run each reviewer at least three times for every case.

The corpus ID binds the source baseline, artifact digest, checklist version, and adjudicated defect-set digest. The runner rejects result records that name different inputs.

The comparison derives defect recall and false positives from the adjudicated IDs rather than trusting caller-supplied scores. It also checks every checklist question and citation, then compares median elapsed time, tokens, and available monetary cost. Promotion requires every candidate run to find all blocking defects, answer and cite every checklist question, introduce no more false positives than the reference median, and reduce median elapsed time or tokens by at least twenty percent without increasing the other measure.

Run the comparison after collecting separate result files:

```bash
python3 evals/reconstruction-review/run_checklist_eval.py \
  --corpus evals/reconstruction-review/corpus.json \
  --candidate-results /evidence/candidate.jsonl \
  --reference-results /evidence/reference.jsonl
```

The recommendation is evaluation evidence for a human or routing-maintenance decision. The runner never changes model routing automatically.
