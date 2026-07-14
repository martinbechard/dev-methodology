# Reconstruction Archive Schema Version 2

Use this reference when assembling or independently checking a reconstruction evaluation archive. The executable authority is reconstruction_run.py in the parent skill scripts directory.

## Version Policy

Schema-version-1 archives are readable for historical retention. Newly sealed runs use schema version 2. The run status describes the evaluation result; archive-manifest status VALID describes archive integrity and does not turn a failed run into a successful evaluation.

Every status named NOT_RUN includes all three fields below:

```json
{
  "failureEvidence": "execution/evidence/failure.json",
  "failureEvidenceSha256": "64 lowercase hexadecimal characters",
  "unmetGate": "The exact earlier gate that prevented execution"
}
```

The failure-evidence path stays inside the run archive and its digest must match the final bytes.

## Required Content

The version-1 required file set remains required. Version 2 adds:

```text
reset/git-reconciliation.json
parity/evaluator-manifest.json
execution/provenance.json
```

Successful runs contain non-empty accepted documentation under all of these directories:

```text
documentation/docs/architecture
documentation/docs/functional
documentation/docs/high-level
documentation/docs/modules
documentation/docs/wiki
```

Every documentation path and every root or nested PROJECT.yaml, AGENTS.md, and CLAUDE.md path exactly mirrors the validated seed file set and digest. An early failed or blocked run may instead put one bound NOT_RUN.json record in each documentation directory, record the same state in root PROJECT.yaml and AGENTS.md, and make seed/seed-manifest.json a bound NOT_RUN record.

Required JSON records are substantive objects. Empty objects and empty arrays used as whole required records are invalid. Execution commands are non-empty JSONL objects bound to the run ID and execution nonce. Usage metrics contain one entry per measured activity with elapsed seconds and either a token value or unavailability status and either a cost value or unavailability status.

## Run Identity

RUN.json has this minimum shape:

```json
{
  "executionNonce": "at least 16 characters and unique to this attempt",
  "finishedAt": "timezone-aware ISO-8601 timestamp",
  "runId": "exact archive directory name",
  "schemaVersion": 2,
  "sourceBaseline": "immutable source commit or digest",
  "startedAt": "timezone-aware ISO-8601 timestamp",
  "status": "READY, FAILED, or BLOCKED"
}
```

All execution proof timestamps fall inside this interval. READY requires passing documentation, isolation, native proof, report proof, and parity evidence.

## Git Reconciliation

reset/git-reconciliation.json has status PASS even when the evaluated run failed, because PASS means the Git evidence itself reconciles. It contains:

- One or more stages with unique IDs and command IDs.
- Before and after snapshots with Git head, tree, status digest, and full Git-metadata inventory digest.
- The complete expected change list and an empty unexpectedChanges list for each stage.
- A transientChanges entry for the agent-claims registry with resolution RELEASED or RESTORED.
- A claimLifecycle record proving acquire and release and binding the before and after registry digests.

Checking only Git config, Git status, or the application worktree is insufficient.

## Isolation Ledger

contamination/ledger.json contains exactly one builder environment and one verifier environment. A completed environment records a distinct sandbox identity, environment digest, mount inventory, originalSourceMounted false, and one denied-access probe for every channel below:

```text
canonical-path
alternate-path
parent-traversal
symlink
hardlink
cache
temporary-file
environment-variable
```

Each channel contains at least two independent readers. Every reader sets attemptedByteRead true, records DENIED, and links hashed evidence. A stage that did not run uses one bound NOT_RUN environment record. READY requires both environments to pass and zero unresolved contamination findings.

## Parity Catalog And Evaluator

parity/cases.json contains unique case IDs and the complete construction-neutral contract for each case:

```json
{
  "comparisonPolicy": "comparison rule",
  "id": "stable case ID",
  "inputs": ["input"],
  "mandatoryExecutionStrength": "required execution boundary",
  "originalCommand": "original command",
  "owner": "behavior or disposition",
  "preconditions": ["precondition"],
  "reconstructionCommand": "reconstruction command",
  "requiredEvidence": ["evidence"],
  "requiredNativeProofId": "optional native proof ID",
  "requiredProbeKind": "probe kind",
  "requiredReportKind": "required for browser, Cypress, or report probes"
}
```

The helper derives native-proof and report-proof inventories from the cases. parity/evaluator-manifest.json repeats those exact sets and binds five files by path and digest: caseCatalog, contract, evaluator, oracle, and probeInventory. Its sealedDigest is the null-delimited SHA-256 binding of those sorted names and digests.

When the evaluator stage did not run, cases and proof inventories are empty, both files use bound NOT_RUN records, and the evaluator digest is the null-delimited SHA-256 binding of run ID, execution nonce, and evaluator-not-run.

## Execution Provenance

execution/provenance.json contains exact nativeProofs and reportProofs sets. A completed native proof records:

- Run ID and execution nonce.
- Unique proof ID and status.
- Command ID and command digest.
- Target identity and target digest.
- Artifact digest and process identity.
- Start and finish timestamps inside the run interval.
- A hashed JSON evidence envelope whose run ID and nonce match the run.
- A proofBindingSha256 over run ID, nonce, native, proof ID, and evidence digest.

A completed report proof also records reporter name and version, raw report path and digest, normalized observation path and digest, and a proof binding over both report digests. The observation is a JSON envelope whose run ID and nonce match and whose rawReportSha256 equals the raw report bytes. A summarized browser observation without the raw report fails.

NOT_RUN provenance contains empty proof lists plus the bound unmet-gate record. READY requires every derived proof to pass.

## Parity Reconciliation

parity/reconciliation.json contains exactly one result for every case and no unknown case. Each result uses the case's required probe kind. PASS and FAIL results link hashed evidence. NOT_RUN results link the unmet-gate evidence.

The helper recomputes required, attempted, passed, failed, and notRun counts and derives the final reconciliation status. Caller-supplied counts or status that disagree with the result rows fail. The evaluator digest must match the sealed evaluator manifest. READY requires every required case to pass.

## Manifest And Detached Attestation

archive-manifest.json lists every file inside the run directory except itself, once, in sorted project-relative order with size and SHA-256 digest. It also records the aggregate content digest and semantic-contract digest.

The detached attestation is a sibling file named from the run directory plus .attestation.json. It is not a member of the archive manifest. It binds:

```json
{
  "archiveName": "run directory name",
  "contentAggregateSha256": "manifest content aggregate",
  "manifestSha256": "final archive-manifest digest",
  "runId": "run directory name",
  "schemaVersion": 2,
  "semanticContractSha256": "archive semantic contract digest",
  "status": "ATTESTED"
}
```

Validation requires the sibling attestation. The compare command verifies an independently stored copy byte for byte against the local sidecar and the archive. Retention validates every archive and sidecar before deletion, rejects stale native or normalized-report evidence reused across version-2 runs, then keeps exactly the newest configured number and removes matching old sidecars.
