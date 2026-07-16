# Agent And Skill Evaluations

The evaluation system exercises the distributed agents and skills with synthetic projects and supports Codex and Junie. A fixture pass proves only that project verification produced the expected result. Behavior verification additionally requires captured harness evidence, current source digests, Judge evidence, and a governed external verifier attestation. That verifier is not implemented, so current receipts can record execution but cannot become verified.

## Evaluation Layers

- Structural validation checks catalogs, source references, harness policy, executable-case links, and current digests.
- Skill probes check activation, negative activation, expected behavior, and ablation results.
- Agent scenarios check responsibility, output contracts, mutation policy, and failure handling.
- Workflow packs check delegation, handoffs, claims, integration, and terminal status across agents.

Deterministic Judges evaluate exact conditions such as tests, schemas, findings, hashes, allowed writes, and state transitions. Model Judges evaluate semantic qualities only after the Deterministic Judges finish. A critical Deterministic Judge failure skips Model Judge execution. Human Judges create and adjudicate calibration labels and resolve ambiguous high-risk results.

## Catalog Validation

Validate executable cases and every present framework catalog with:

```bash
python3 scripts/run-agent-skill-evals.py --validate-catalogs
```

The operational catalogs are cases.yaml, skill-probes.yaml, agent-scenarios.yaml, workflow-packs.yaml, judges.yaml, and sandbox-profiles.yaml. Skill-probe, agent-scenario, and workflow-pack selection resolves their linked executable cases rather than treating catalog declarations as execution evidence.

## Prepared Fixtures And Workspaces

Prepared fixtures are content addressed from the source tree, file modes, empty directories, symbolic-link targets, dependency manifests and lockfiles, preparation command, controlled-environment identity, explicit toolchain versions, operating-system release, and architecture. Prepared installs fail closed when toolchain versions are absent. Source hashing and initial cloning prune transient dependency, build, Git, cache, and run trees before traversal. A per-key ownership lock prevents parallel workers from installing the same prepared fixture twice, preserves a live long-running owner, and reclaims only dead or invalid stale owners.

Dependency installation occurs only during an explicit trusted preparation. Preparation rejects source-tree mutation and escaping symbolic links. Cache hits used for preflight verify the pruned source identity without rehashing dependency trees; live harness execution requires an existing prepared entry, verifies the full prepared-snapshot digest while holding the cache-key lock, and then clones it. This keeps iterative startup proportional to source size while retaining a full integrity gate before evidence-producing runs. The cache is integrity checked, not claimed as filesystem-immutable. Each run uses a copy-on-write clone when the platform supports it and a filtered full-copy fallback otherwise. The run workspace is initialized as an isolated Git repository with a deterministic synthetic baseline and its own claim registry. The writable workspace is removed after the run even when execution fails.

Prepare one case and populate its dependency cache with:

```bash
python3 scripts/run-agent-skill-evals.py \
  --prepare \
  --case typescript-order-pricing \
  --install \
  --toolchain node=24
```

Run the trusted, repository-owned fixture regression without invoking a harness with:

```bash
python3 scripts/run-agent-skill-evals.py \
  --case typescript-order-pricing
```

The install option is accepted only with prepare. Live execution never installs dependencies and fails closed when its governed prepared entry is missing or fails integrity validation.

## Harness Context And Privacy Preflight

Every invocation stages one selected generated agent definition and the pruned package for each selected skill into repository-native project locations inside the disposable workspace. The selected package includes its directly owned references, scripts, templates, and assets while excluding transient trees. A case skill resource allowlist may narrow an excessive package, but it must retain SKILL.md and every resource required by the behavior under evaluation. Codex mutation agents also receive the adapter-owned codex-harness-directives skill as harness-required context; this is recorded separately from treatment skills so ablation results remain interpretable.

The runner rejects missing, escaping, unapproved, or sensitive staged files before harness execution. It also rejects any non-runner fixture file omitted from the model-visible allowlist, because a process rooted at the workspace could otherwise read that file. It records each selected skill resource, its source and effective digest, sanitization actions, the context-pack digest, and the effective approved-input manifest digest. Dependency and build trees are excluded from source identity and model-input inventory. Evaluation fixtures must remain synthetic and free of personal, customer, company-confidential, credential, and secret material.

Harness and trusted-fixture commands receive controlled environments rather than the complete host environment. The default host allowlist contains process-location, locale, and temporary-directory names only. Harness authentication variables must be named explicitly with the approved environment option; receipts and dry-run records contain names, never values. Command execution has a default wall-clock limit, bounded retained output, and process-group teardown on timeout. The current subprocess adapter drains captured output before truncation, so operating-system or external-runner resource containment remains responsible for hard memory bounds. Harness event, final-message, scratch, and cache paths are constrained to one runner-owned evidence root that is disjoint from the product workspace and prepared cache. Symbolic-link escapes and arbitrary host destinations are rejected. Harness scratch directories are unique per disposable run and removed afterward. The runner never executes post-harness verification commands on the host: command evidence for a model-modified workspace must come from trusted external containment.

Codex runs with ephemeral execution, ignored user configuration, JSON event output, the selected native read-only or workspace-write sandbox, and the disposable workspace root. The selected project agent and skills are staged under the project Codex and shared skill locations. When structured final output is requested, the command builder accepts only the digest-bound codex-agent-output-schema.json JSON Schema; arbitrary files under evals and workspace-controlled schemas are rejected.

Junie runs with default configuration, model, MCP, skill, agent, and command locations disabled. The selected project agent and skills are supplied through explicit locations, and its cache and event output stay outside the disposable workspace. Junie exposes no filesystem containment flag. The current runner adapter accepts an identity-bound self-attestation for dry-run inspection only; that file is not a trust anchor, always reports containment-unverified, and cannot authorize live Junie execution or verified evidence. Live Junie remains refused until a governed external runner verifier exists.

Print a safe dry-run invocation without executing a paid harness or running fixture verification with:

```bash
python3 scripts/run-agent-skill-evals.py \
  --case typescript-order-pricing \
  --harness codex \
  --model configured-model \
  --print-invocation
```

Inspect a Junie wrapper identity in dry-run mode with an external runner executable and explicitly unverified self-attestation:

```bash
--junie-external-runner /path/to/contained-runner \
--junie-containment-attestation /path/to/attestation.json
```

The runner executable receives a separator followed by the Junie argument vector. The JSON self-attestation binds a runner digest and declared filesystem, process, network, CPU, memory, and time capabilities, but it does not independently prove them. The CLI never executes Junie directly or through this untrusted wrapper.

Prompt text requesting an agent is not agent-attribution evidence. Codex and Junie verification both require a normalized agent-start event that names the intended agent and carries the effective native-adapter digest. Receipts also bind the conceptual source digest, native adapter source and effective digests, and adapter sanitization actions. Codex and Junie invocations, fixture commands, and preparation commands execute from argument vectors without a shell interpretation layer.

Read-only Codex scenarios capture the final assistant response outside the product workspace through the harness last-message output option. The product snapshot must remain unchanged; event logs and the final review artifact live in the external evidence area.

## Functional Isolation And Containment

Evidence reports two separate properties:

- Functional isolation compares before and after complete workspace manifests, including dependency and build trees. It reports narrowly declared, recognized ephemeral compiler and test output separately from product changes, never permits a dependency or tool component to become ephemeral even beneath an allowed ancestor, enforces read-only behavior or allowed product paths, and reports every observed change. Only runner-owned context, metadata, and Git control artifacts are excluded.
- Security containment records the declared containment level, evidence verification status, enforcing boundary, and captured evidence.

Containment levels are externally-contained, workspace-isolated-only, and containment-unverified. Evidence status is separately reported as verified, unverified, or failed. Dry-run invocation records report containment-unverified because functional isolation has not yet been measured. Live Codex execution snapshots the complete auditable workspace before and after the harness, separates case-declared ephemeral build output from the product diff, compares product changes with the immutable case allowed-write and protected-path contract, and only then emits the functional-isolation result. A release verifier must discard ephemeral output, apply only the validated allowed product diff to a fresh full-integrity clone with pristine dependencies, and rerun command checks under external containment. Workspace-isolated-only and externally-contained claims require verified containment evidence; an unverified status cannot satisfy either level. Junie receipts remain unverified and never infer containment from a tool allowlist or caller-created JSON.

## Judge Calibration

The calibration metrics tool recomputes binary F1, linearly weighted kappa on the fixed zero-through-four scale, critical-defect recall, and sample count; caller-supplied metric values are rejected when they differ. Diagnostic calibration requires exactly the governed version-one policy: at least twenty-five examples, at least five examples in each class, at least two failed gold examples, and at least five critical failed gold examples. The five classes are clear-pass, clear-fail, boundary, incomplete-plausible, and adversarially-polished. Boundary or otherwise ambiguous examples require two distinct Human Judges plus an independent adjudicator whose result defines the gold label and score. Thresholds are binary F1 of at least 0.85, weighted kappa of at least 0.70, and critical-defect recall of exactly 1.0.

Calibration promotion is currently disabled. Self-reported labels and scores are sufficient for diagnostic metric calculation but cannot establish calibrated or verified Model Judge evidence. Promotion remains pending until each sample binds canonical Model Judge request and output artifacts, trusted harness, model, and reasoning identity, independent Human Judge and adjudication evidence, and coverage of every critical rubric dimension. Once that provenance contract is implemented, accepted calibration must be keyed by the complete execution identity rather than shared across Codex, Junie, models, or reasoning profiles.

The versioned Judge prompt and strict output schema are judge-prompt-v1.md and judge-output-schema.yaml. The agent_skill_judge_contract.py tool builds separate trusted instruction and untrusted input-manifest messages, validates every returned evidence reference and digest binding, and recomputes dimension thresholds, overall pass, and critical failure. The canonical request binds the selected case, run, harness, candidate-output artifact, and every governed evidence artifact. A receipt must reference the canonical instruction, manifest, candidate, governed evidence, and output artifacts; receipt summaries are compared with those artifacts rather than trusted directly.

The current case Judge plan is executable policy. Receipts must contain every configured Deterministic Judge check exactly once with catalog-matching criticality. A critical failure skips the Model Judge and prevents a verified pass. A non-null model rubric requires exact zero-through-four dimension scores with evidence; the framework derives pass or fail from the current no-compensation and per-dimension rules. An independent Judge must use a distinct invocation and context, link the evaluated run, bind its prompt and input manifest, record model and reasoning identity, and declare blindness to treatment, expected winner, and evaluated-model identity.

## Skill Probe Variants

Harness-backed skill probes run one frozen variant at a time: treatment, target-omitted, or wrong-skill. The dry-run record and receipt bind the probe id, variant, and one comparison key. A positive base case or any single variant remains incomplete probe evidence. Reporting may promote paired-control coverage only after all three comparable receipts are verified, critical gates pass, and the paired-run Judge confirms treatment lift without target credit in either control. Full probe coverage additionally requires a linked negative-activation case. The current catalog has positive cases but no negative-activation fixtures, so it truthfully reports zero full probes.

Select a variant with:

```bash
python3 scripts/run-agent-skill-evals.py \
  --skill-probe probe-typescript \
  --probe-variant target-omitted \
  --harness codex \
  --print-invocation
```

Validate a diagnostic calibration record and print its recomputed metrics with:

```bash
python3 scripts/run-agent-skill-evals.py --validate-calibration /path/to/calibration.yaml
```

Build canonical Judge messages, validate a Judge response, or construct a calibration binding with:

```bash
python3 scripts/agent_skill_judge_contract.py --help
```

Selected cases currently execute serially. Bounded parallel case execution, hard external resource containment, read-only dependency mounts or copy-on-write delta enumeration in place of two full dependency-tree hashes, and warm-worker pooling remain follow-on performance work after the isolation and evidence boundaries are stable.

## Evidence Receipts

Receipt version 2 records:

- Harness and model identity evidence, conceptual agent digest, native adapter source and effective digests, digest-bound agent-start evidence, attribution status, and complete normalized event ledger.
- Required skill source and effective digests, selected resource manifest and sanitization actions, captured effective-digest read events, rejection of receipt skills outside the case, and forbidden-skill detection from the event ledger.
- Context-pack and approved-input manifest digests.
- Budget limits and measured turns, tokens, seconds, and tool calls.
- Current case-definition identity plus prepared source, full prepared-snapshot, dependency, controlled-environment, toolchain, platform, architecture, and prepared-key identity.
- Functional-isolation and containment evidence.
- Complete ordered Deterministic Judge checks, current-rubric Model Judge dimensions, calibrated verdict evidence, and separately identified Human Judge evidence when applicable.
- Behavior assertions, findings, shell-free command evidence, and independent Judge provenance.

Every evidence reference uses normalized relative file#marker syntax and must resolve to a non-symlink UTF-8 artifact inside the receipt directory. Absolute paths, traversal, escaping symbolic links, and missing targets fail before any artifact read. Invocation and skill-read references identify exactly one matching JSON Lines event. Naming an agent or skill in a result is not evidence that it ran or loaded.

Validate captured candidate evidence and classify it as executed, verified, or stale by digest with:

```bash
python3 scripts/run-agent-skill-evals.py \
  --case typescript-order-pricing \
  --project-root /path/to/disposable-working-copy \
  --result /path/to/evidence/eval-result.md \
  --evidence /path/to/evidence/evidence.yaml
```

Evidence classification reads and validates the captured artifacts; it does not execute the case verification command against the supplied project root. A structurally complete local or human-attested capture may classify as executed, but every current case declares external-runner-required and therefore remains unverified until the governed verifier trust anchor exists.

Receipt version 1 remains accepted for validation compatibility, but it does not satisfy the complete version 2 execution contract for current evaluation evidence. The observations in results/2026-07-09-live-agent-evaluations.md predate the receipt proof contract and do not count as verified behavior.
