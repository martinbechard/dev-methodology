---
name: review-reconstruction-readiness
description: Use when independently reviewing whether a reverse-engineered documentation package can reconstruct an application under enforced source isolation and prove functional parity against the original baseline.
metadata:
  category: artifact-review
---

# Reconstruction Readiness Review

Use this skill to review the complete evidence package for the mandatory reconstruction-readiness pass. File presence is not acceptance. The review must prove that the documentation seed is self-contained, the reconstruction was built without original-source access, and every declared parity case and generated-output delta reconciles against the original baseline oracle.

## Required Inputs

- The exact reset source baseline and path inventory.
- The path coverage ledger with one reconstruction disposition per path.
- The accepted wiki, functional, architecture, high-level, module, configuration, and routing documents.
- The seed manifest, run metadata, copied seed, and seed-validation result.
- The public-generator specifications, original and reconstructed generator results, and machine-readable delta ledger.
- The parity case catalog, original baseline oracle, reconstructed outcomes, and machine-readable reconciliation.
- The builder and verifier sandbox or container definitions, mount and environment inventories, denied-access probes, and contamination ledger.
- The reconstructed application and its build, test, route, workflow, data, security, and operational results.
- The run archive, exact archive manifest, and retention result.

## Workflow

1. Read references/review-checklist-reconstruction-readiness.md.
2. Confirm the reset baseline and independently reconcile its exact path set against the reconstruction-disposition ledger.
3. Re-run the portable seed validator inside the new build root and compare its file inventory, copy phases, hashes, link closure, and contamination checks with the recorded seed manifest.
4. Inspect operating-system or container isolation evidence for both builder and verifier. Re-run denied-access probes where the environment permits it. An instruction-only promise is a failure.
5. Reconcile public-generator outputs and parity case IDs mechanically in both directions. Independently sample the underlying commands and evidence, but never replace exact set reconciliation with sampling.
6. Verify the original baseline oracle was captured before builder isolation and that the independent verifier compared reconstructed results against that immutable oracle.
7. Validate the archive manifest and newest-three retention result. No older archive may be pruned before the newly archived run validates.
8. Complete every checklist question with status, quoted evidence, and assessment.
9. Save the completed checklist under the evaluation root as reviews/reconstruction-readiness.review-checklist-reconstruction-readiness.md.
10. Use documentation-page-verify on the readiness report and completed checklist for source authority, links, steady-state language, and unresolved-question checks.
11. Return findings first, ordered by severity. A missing path disposition, unenforced isolation boundary, contaminated seed, unresolved generator delta, unreconciled parity case, failed parity result, or invalid archive is blocking.

## Acceptance Rule

Pass only when every checklist question is pass or evidence-backed not applicable, every path and parity case reconciles exactly, all required parity outcomes pass, both builder and verifier isolation are enforced outside the model prompt, the contamination ledger has no unresolved finding, and the newly archived run validates before retention pruning.

Report BLOCKED when the runtime cannot enforce or expose the required isolation and verification evidence. Do not convert missing evidence into a pass, and do not accept builder self-verification as independent parity evidence.

## Output

Lead with blocking and non-blocking findings. When no problem remains, state that the reconstruction-readiness package passes and name the source baseline, seed digest, reconstructed output, oracle digest, parity case count, generator delta count, isolation evidence, archive digest, and retained run set.
