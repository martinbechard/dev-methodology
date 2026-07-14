# Reconstruction Readiness Review Checklist

## Purpose

Use this Review Checklist to verify that a reverse-engineered documentation set was independently used to reconstruct the application and prove parity without original-source contamination.

## Completion Format

For every question record:

- Status: pass, fail, question, or n/a.
- Question: copy the objective question being answered.
- Quoted evidence: quote the exact artifact, manifest, command result, sandbox definition, or source text that supports the status.
- Assessment: explain why the quoted evidence passes, fails, is unclear, or is not applicable.

Do not mark pass without quoted evidence. A file name, claimed command, or agent statement is not evidence that the file is valid, the command ran, or isolation was enforced.

## Skill Workflow Checks

- Question: Does the review name review-checklist-reconstruction-readiness.md as its governing checklist?
- Question: Is the completed checklist saved under the evaluation root as reviews/reconstruction-readiness.review-checklist-reconstruction-readiness.md?
- Question: Does the review independently reconcile exact path, seed-file, generator-output, parity-case, and archive-file sets rather than relying on reported counts?
- Question: Does the review re-run deterministic validation and denied-access probes where the environment permits it?
- Question: Does the review use documentation-page-verify on the readiness report and completed checklist?
- Question: Does the final assessment derive findings or pass status from this completed checklist and lead with findings ordered by severity?

## Reset Baseline And Path Dispositions

- Question: Does immutable evidence identify the exact original source baseline, reset commit or digest, and source inventory used as the oracle authority?
- Question: Does reset evidence prove the documentation folder was deleted before reverse engineering began and routing files were also removed when routing reconstruction was in scope?
- Question: Does mechanical set comparison prove every baseline path appears exactly once in the reconstruction-disposition ledger with no missing, duplicate, blank, or extra entry?
- Question: Is every path assigned exactly one allowed disposition: MUST_DOCUMENT, PUBLIC_GENERATOR, or PARITY_TEST_ONLY?
- Question: Does every MUST_DOCUMENT entry link the self-contained construction facts, contracts, data, configuration, and behavior needed without treating an original-source link as sufficient instruction?
- Question: Does every PUBLIC_GENERATOR entry identify a generator obtainable without original-source access, its locked version or digest, public inputs, invocation, output contract, and comparison policy?
- Question: Does every PARITY_TEST_ONLY entry link one or more executable parity case IDs that observe the behavior it is allowed to omit from construction detail?
- Question: Are generated paths still given one of the three reconstruction dispositions, with no GENERATED classification treated as a sufficient exemption?

## Documentation Seed And Reconstruction Package

- Question: Was the build root absent before initialization and created as a new empty destination outside the original source project?
- Question: Do copy-phase evidence and hashes prove docs/wiki was copied first before any other documentation, configuration, generator input, or reconstruction code?
- Question: Does exact file reconciliation prove the complete documentation tree was copied by value rather than only the subset reachable from wiki links?
- Question: Does recursive link reconciliation prove the copied seed contains the complete linked documentation and configuration corpus with no unresolved local dependency?
- Question: Does the seed manifest record every project-relative source-evidence reference without copying its target, and does each target reconcile to the baseline path ledger?
- Question: Does the seed include accepted wiki, functional, architecture, high-level, module, PROJECT.yaml, AGENTS.md, declared public-generator, and declared parity-contract inputs needed by the builder?
- Question: Does the seed manifest record every copied file, its project-relative path, phase, origin, size, SHA-256 digest, source baseline, and aggregate phase digest?
- Question: Was seed validation executed inside the copied destination and did it prove the copied file set and hashes match the approved inputs?
- Question: Do validation and direct inspection prove the seed contains no symbolic link, hard link, absolute original-source path, source-root escape, or undeclared file?
- Question: Are repository evidence paths project-relative and are genuine external paths expressed with portable variables or declared container roots, with no POSIX or Windows user-home, checkout, worktree, cache, or temporary-directory path embedded in PROJECT.yaml or another seed file?
- Question: Is the package self-contained enough that the builder needs only the copied seed and declared external toolchain, with no original repository lookup or undocumented private dependency?

## Public Generator Differential

- Question: Was each PUBLIC_GENERATOR run against the original baseline and in the reconstructed project with the locked generator, inputs, environment, and invocation recorded?
- Question: Does a machine-readable delta ledger reconcile the exact expected and actual generated file sets in both directions?
- Question: Does each delta row record generator ID, output path, original digest or normalized result, reconstructed digest or normalized result, comparison policy, status, evidence, and resolution?
- Question: Are intentional nondeterministic fields normalized by an explicit source-backed comparison rule rather than ignored informally?
- Question: Are there zero missing outputs, unexpected outputs, unresolved deltas, failed generator invocations, or generated paths accepted only because they were classified as generated?

## Original Oracle And Parity Case Reconciliation

- Question: Was the original baseline oracle captured from the reset source before the builder received its isolated environment?
- Question: Does the oracle package record commands, inputs, fixtures, environment, exit status, observable outputs, digests, and timestamps needed to replay or audit each case?
- Question: Do exact inventory and content checks prove the oracle contains no original application source, source excerpt, absolute original-source path, source-derived cache, or undeclared artifact that could serve as a reconstruction input?
- Question: Is the oracle package immutable and hash-verified before it is provided to the isolated verifier?
- Question: Does the machine-readable parity case catalog give every case a unique stable ID, owner or disposition link, preconditions, inputs, original command, reconstruction command, comparison policy, required probe kind, mandatory execution strength, and required evidence?
- Question: Does one digest seal the evaluator implementation, governing contract, accepted case and probe inventories, and immutable oracle, and does detached final attestation recompute that digest from the final bytes instead of trusting a stale embedded or self-referential hash?
- Question: Does the evaluator fail closed on unknown, duplicate, missing, unattempted, wrong-kind, weak, provenance-unbound, or synthetic evidence and recompute all statuses, aliases, dispositions, counts, and the final verdict rather than accepting caller-supplied READY labels?
- Question: Is every runtime result bound by verifier-derived evidence to an immutable source tree, built artifact, process or container, exact command, target root, and run ID so one result cannot be relabeled for both lanes?
- Question: Does exact set reconciliation prove every declared case has one original oracle result and one reconstructed result, with no missing, duplicate, unexpected, skipped, or silently unrun case?
- Question: Does every PARITY_TEST_ONLY path map to at least one reconciled parity case, and does every parity case map back to a documented behavior or disposition entry?
- Question: Do parity cases collectively cover build, tests, public routes, actor workflows, data and migration behavior, authentication and authorization, errors and validation, integrations, configuration, operations, and deployment where those surfaces exist?
- Question: Does each reconciliation row record case ID, original digest or normalized result, reconstructed digest or normalized result, status, evidence, and any resolved delta?
- Question: Are every required case and every required behavioral category PASS, with no UNRUNNABLE, SKIPPED, missing-evidence, or expected-failure result converted into parity?

## Builder, Verifier, And Contamination Isolation

- Question: Are builder and verifier separate owners in separate fresh processes or containers, with the verifier independent from builder implementation context?
- Question: Do operating-system sandbox or container definitions prove the builder can read only the new reconstruction root and declared external toolchain, not the original repository or its parent workspace?
- Question: Do operating-system sandbox or container definitions prove the verifier can read only the reconstructed application, immutable oracle package, parity contracts, generator contracts, and declared external toolchain, not the original repository or builder-private workspace?
- Question: Do mount, environment, working-directory, temporary-directory, cache, credential, network, and dependency-provenance inventories expose every possible contamination channel?
- Question: Do denied-access probes from inside both isolated environments fail when attempting to read the original repository by canonical path, alternate path, parent traversal, symlink, hardlink, cache, temporary file, and environment variable?
- Question: Does every denial probe attempt an actual content open and byte read through at least two independent readers, with no `test -r`, metadata lookup, or permission predicate accepted as proof that bytes are inaccessible?
- Question: Did the exact production image, mounts, environment, user, and nested sandbox policy first prove both source denial and acquire/release of the required agent claim in a disposable repository, with only the narrow required reconstruction metadata write surface granted?
- Question: Does the contamination ledger record each checked channel, command, result, evidence digest, finding owner, resolution, and final status?
- Question: Are there zero unresolved contamination findings, undeclared mounts, inherited source paths, reused source worktrees, source-derived caches, or copied application files outside the approved seed?
- Question: Is isolation enforced by the operating system or container runtime rather than by instructions, agent promises, working-directory convention, or honor-system compliance?

## Reconstruction And Independent Verification

- Question: Was the full project built in the initialized destination from the copied seed before any original-source access was possible?
- Question: Does the reconstructed output include all source, configuration, migrations, assets, tests, scripts, and operational files required by the documentation and dispositions?
- Question: Did the independent verifier run the documented build, test, route, workflow, data, security, integration, operational, and deployment checks against the reconstruction?
- Question: Did every required native build, lint, unit, integration, browser, performance, packaging, container, TLS, operations, and deployment gate execute at its real boundary, with no source inspection or OWNED_SMOKE label substituted for runtime evidence?
- Question: Do imported suite results prove the complete expected identity, reject unmatched failures, skips, partial suites, and synthetic fixtures, and bind the artifact to the recorded command and target?
- Question: Do verifier results reconcile every parity case and generator delta against the immutable original oracle without accepting builder self-reports as final evidence?
- Question: Is the claimed parity scope identical to the original full-codebase scope, with every known limitation reported as a failure or blocker rather than silently excluded?

## Archive Integrity And Retention

- Question: Is every attempted run, including a failed or blocked run, archived with its status and failure evidence before another attempt begins?
- Question: Does the archive contain RUN.json; reset/source-baseline.json; configuration/PROJECT.yaml; configuration/AGENTS.md; documentation/docs/wiki; the full accepted documentation corpus; the completed readiness checklist; seed/seed-manifest.json; oracle/original-baseline.json; reconstruction output; parity/cases.json; parity/reconciliation.json; generators/delta-ledger.json; contamination/ledger.json; execution commands and results; and usage metrics, using explicit non-empty NOT_RUN records for stages that never started in failed or blocked attempts?
- Question: Does archive-manifest.json enumerate the exact archive file set with sizes and SHA-256 digests, and does independent validation reproduce every digest with no missing or unexpected file?
- Question: Does generator evidence capture and reconcile a full pre/post Git metadata inventory, including transient claim-registry changes, instead of checking only `.git/config`?
- Question: Are immutable input manifests separate from post-run evidence, with final detached attestations computed only after the attested bytes are frozen?
- Question: Does the usage record report elapsed time and available token or cost measurements by activity, while recording unavailable measurements explicitly rather than estimating them as facts?
- Question: Was the new archive fully validated before any retention deletion began?
- Question: After validation, are exactly the newest three complete run archives retained unless the user explicitly selected another count?

## Findings

Report findings first. Treat any missing or duplicate disposition, source-dependent seed, generated-only exemption, unclosed link, inode or absolute-path contamination, missing original oracle, honor-system isolation, builder self-verification, unreconciled case, failed required parity outcome, unresolved generator delta, invalid archive, or pre-validation pruning as a blocking finding.
