# Agent Evaluations

The evaluation system exercises the distributed agents with synthetic projects and supports Codex and Junie. Agent-owned suites under agent-tests are the primary planning and orchestration unit. Each suite derives a compact scenario set from one canonical conceptual agent definition, hardcodes its supervisor, Judge, target agent, project skills, dependencies, and acceptance gates, and uses the common protocol in agent-tests/AGENTS.md.

Skill probes remain available as targeted diagnostic controls inside an agent scenario. They are not an exhaustive test-planning unit and do not require one test per assigned skill.

Ordinary cases run locally in disposable workspaces. This local tier isolates reproducibility and host state; it is not a sandbox for hostile code. A fixture pass, captured execution, Judge pass, Model Judge calibration status, security containment, and digest freshness are separate claims. External containment is reserved for cases explicitly classified as high risk.

## Agent-Owned Suites

The suite index covers all twenty-six conceptual agents in end-user value order. The root coordinator may run at most four suite supervisors concurrently. Each supervisor uses exactly one child at a time. One target child may temporarily create one additional nested agent only when its canonical workflow and suite manifest declare that dependency. This produces a normal ceiling of nine active agents and an exceptional ceiling of ten.

Every suite contains suite.yaml, scenarios.yaml, a hardcoded supervisor, a hardcoded read-only Judge, and a target-specific contract skill shared by those project agents. Cross-suite scenario, supervision, and judging methods live once under agent-tests/skills.

The [complete execution report](agent-tests/results/2026-07-17-complete-agent-suites.md) records governed terminal results for all 26 suites and 78 initial scenarios.

Ordinary suites may share a four-supervisor batch. A suite that needs loopback, descendant-process inspection, or browser automation runs alone with an explicit local-runtime permission profile. That profile allows local binding through a localhost-only managed proxy and denies non-local destinations. Offline ignored dependencies are copied into the disposable clone only after the installed package matches tracked lock evidence.

Validate the complete agent-owned catalog and bounded schedule without starting a model session with:

```bash
python3 evals/agent-tests/runner.py --harness codex --validate-only
```

Use the agent-tests/runner.py reporting entry point for resource-bounded one-suite, multi-suite, or complete-catalog execution and durable offline HTML reporting. The reporting commands, Junie full-catalog authorization, report-only rebuild, and incremental update workflow are documented in [the agent-owned suite strategy](agent-tests/README.md).

## Evaluation Layers

- Structural validation checks suite structure, catalogs, source references, harness policy, executable-case links, and current digests.
- Agent suites check responsibility, output contracts, mutation policy, decisions, delegation, failure handling, and terminal outcomes.
- Skill probes diagnose scenario behavior through activation, negative activation, expected behavior, and ablation controls when a selected scenario needs that evidence.
- Workflow evidence checks delegation, handoffs, claims, integration, verification, and terminal status across the dependencies allowed by the target agent definition.

Deterministic Judges evaluate exact conditions such as tests, schemas, findings, hashes, allowed writes, and state transitions. Model Judges evaluate semantic qualities only after the Deterministic Judges finish. A critical Deterministic Judge failure skips Model Judge execution. Human Judges create and adjudicate calibration labels and resolve ambiguous high-risk results.

## Catalog Validation

Validate executable cases and every present framework catalog with:

```bash
python3 scripts/run-agent-skill-evals.py --validate-catalogs
```

The operational catalogs are cases.yaml, skill-probes.yaml, agent-scenarios.yaml, workflow-packs.yaml, judges.yaml, and sandbox-profiles.yaml. They remain the runner and evidence substrate while cases move into agent-owned suites. Skill-probe, agent-scenario, and workflow-pack selection resolves linked executable cases rather than treating catalog declarations as execution evidence.

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

The modelVisibleProjection field is an explicit, fail-closed exception for a fixture that must retain evaluator-only files. The field selects isolated-harness-workspace mode and declares every evaluatorOnlyPaths entry. The runner requires all relevant fixture entries to partition into modelVisiblePaths and evaluator-only paths. Each inventory records files, directories, empty directories, types, and modes. The runner rejects missing declarations, undeclared entries, overlaps, duplicate destinations, symbolic links, path escapes, and existing output destinations. It copies only the model-visible entries into a second disposable harness workspace. It then seals the exact runner-owned agent, skill, MCP, configuration, Git, and marker context before model execution. Evaluator-only files stay in the full disposable fixture and never enter the harness workspace.

After the model stops, the projection runner accepts only unchanged sealed inputs and declared create-only outputs. It inventories transient trees and detects mode-only changes. It rejects unexpected entries, runner-context changes, symbolic links, concurrent source changes, and destination collisions. An exclusive create operation prevents a late collision from replacing existing bytes. A failed multi-file application rolls back files and directories that the runner created.

Each run creates one owner-only receipt artifact directory outside both workspaces. Its stable file-marker references are relative to a receipt stored in that directory. The package retains the projection manifest, synchronization manifest, verifier evidence, projected input bytes, synchronized output bytes, and evaluator-owned verifier source. It does not retain the full fixture or evaluator-only experiment evidence. The projection manifest binds every projected entry to retained bytes when the entry is a file. The synchronization manifest binds every mutation to retained output bytes and records the post-sync full-fixture identity. Both manifests bind the prepared full-fixture snapshot.

Harness and trusted-fixture commands receive controlled environments rather than the complete host environment. The default host allowlist contains process-location, locale, and temporary-directory names only. Harness authentication variables must be named explicitly with the approved environment option and must use dedicated, revocable evaluation credentials rather than personal or production credentials. Approval is an explicit exception to environment isolation: the harness and its child tools may see the value, while redaction protects retained output rather than runtime access. Receipts and dry-run records contain names, never values; explicitly approved values are redacted from event streams, final responses, and printed diagnostics before retention. Command execution has a default wall-clock limit, bounded retained output, and runner-created process-group teardown after completion or timeout. Default event paths and transient harness state are unique to the disposable run. Caller-selected event and final-message destinations must be unused, distinct paths and are exclusively reserved for the duration of the run, so existing or concurrent evidence is never overwritten. Runner-owned evidence is disjoint from the product workspace and prepared cache. Symbolic-link escapes and arbitrary host destinations are rejected. Ordinary harness runs do not rerun verification commands against a model-modified workspace; required command outcomes come from captured harness evidence. The projection opt-in is narrower. After allowlisted synchronization, it runs one digest-bound evaluator-owned Python script against the exact post-sync full-fixture identity. The runner normalizes only the two governed terminology verifier forms. The execution command has one resolved interpreter and one retained evaluator-owned script. Interpreter options, environment wrappers, module execution, inline execution, model-write paths, and model-written code are not valid execution commands. Treatment and independent negative-activation runs require semantic-green verification. Target-omitted and wrong-skill red controls require the declared exit-three semantic-red result with a valid result object. A timeout, output-cap termination, signal, crash, malformed result, or semantic-green red control blocks the variant. An explicitly high-risk case requires the externally-contained tier.

For an existing Codex ChatGPT login, a live Codex run may instead name one tightly permissioned auth.json source with the Codex authentication option. The runner validates and copies only those bytes into a unique auth-only CODEX_HOME outside the product workspace, never records the source path or content, keeps user configuration ignored, and removes the temporary authentication home after the process exits. A dedicated, revocable evaluation login remains preferred.

Codex runs with ignored user configuration, JSON event output, and the disposable workspace root. Ordinary cases select the native read-only or workspace-write sandbox. The MCP Git-lifecycle case instead uses an exact custom permission profile because the legacy workspace-write sandbox always protects Git metadata as read-only. The profile is retained in the configuration digest, denies the host home and evidence root, disables network access, preserves staged agent and configuration trees as read-only, and grants writes only to the disposable workspace, its Git metadata, and the unique temporary directory. Custom-agent delegation requires session state, so the runner does not use the CLI ephemeral flag; instead it confines session state to the isolated HOME or auth-only CODEX_HOME and removes that complete location after the run. The selected project agent and skills are staged under the project Codex and shared skill locations. When structured final output is requested, the command builder accepts only the digest-bound codex-agent-output-schema.json JSON Schema; arbitrary files under evals and workspace-controlled schemas are rejected.

Junie runs with default configuration, model, MCP, skill, agent, and command locations disabled. The selected project agent and skills are supplied through explicit locations. The runner pins the installed version-specific executable before replacing user state, supplies a unique JUNIE_HOME, HOME, cache, temporary directory, and JSON event path, and stages an owner-only action policy. The MCP case permits ordinary read-only commands, Git add and Git commit, and fifteen exact mcp-agent-ops operations; every unmatched action retains the ask behavior. It requires a non-empty terminal result event and removes transient state afterward. Junie exposes no native filesystem sandbox flag, so an ordinary local Junie run reports no security-containment claim. This does not block local execution.

The project-configuration-routing base case additionally evaluates mcp-agent-ops 0.4.0 through Codex and Junie. The pinned source-verified runtime identity advertises canonical claim result schema version 2; the published 0.4.0 artifact does not satisfy this runtime digest or claim-result contract. The runner requires an explicit executable, verifies its launcher and installed-runtime digests against the case, and makes the server verify the runtime digest again before stdio starts. It stages an exact separate availability catalog beneath the disposable evaluation context: execution skills expose their effective instructions plus explicitly approved MCP resources, while other available skills expose frontmatter only so the catalog cannot inject unrelated instructions. The project template is deliberately absent from harness-preloaded skill content and available only through the required skill_resource_load call. Exact host configuration, catalog, authorization policy, audit identity, and allowed candidate outputs are retained in a runner-owned evidence directory outside the disposable workspace. Codex receives CLI-only server and permission-profile configuration with a noninteractive fifteen-operation allowlist. Junie receives one explicit external configuration folder while all default MCP locations remain disabled.

The evaluator reserves a disjoint audit path and a random run session identity. Parent and custom-agent MCP processes write separately identified, process-local streams into one owner-only file. The runner rejects failed or incomplete calls and requires one call-bearing MCP process stream; any completed call in another stream invalidates exact-once session evidence. Every required tool is bound to the privacy-safe digest of its exact expected arguments and its bounded outcome on the same completed call. An outcome-less completed call is not semantic evidence. The case accepts VALID from skill_validate and CATALOG from skill_refresh; FINDINGS, EMPTY, and missing outcomes fail. Detection accepts READY when a specialized route is selected and NO_VARIANT when every representative scope correctly falls back to general model training; EMPTY and BLOCKED do not satisfy this case. The exact configuration, staged catalog, audit, identity, optional Junie authorization and name-level lifecycle, and bounded allowed outputs survive workspace cleanup with digests. These are deterministic Judge checks and require no Model Judge calibration. Semantic artifact quality still uses the calibrated Model Judge path. A base-case-only contract remains MCP-disabled in every skill-probe variant, so its complete availability catalog cannot reintroduce an intentionally omitted treatment skill.

A version-five probe-treatment-only contract is the narrow exception to that default. The ordinary terminology treatment stages only the declared terminology.md bytes in an isolated runner-owned reference root and exposes reference_load as its only MCP tool. The exact MCP_AGENT_OPS_REFERENCE_ROOTS and MCP_AGENT_OPS_REFERENCE_NAMES values are retained in the configuration evidence. The treatment keeps the ordinary case sandbox and ignored user configuration; it does not use the Git-lifecycle permission profile or a complete skill catalog. The reference_refresh capability remains recognized by framework validation for publication workflows, but reference_refresh remains disabled for this ordinary treatment. The target-omitted and wrong-skill controls remove the complete MCP server contract and forbid terminology-standard while preserving the same probe comparison key.

Print the MCP-enabled Codex or Junie base-case invocation without starting the server or a model session with:

```bash
python3 scripts/run-agent-skill-evals.py \
  --case project-configuration-routing \
  --harness codex \
  --mcp-agent-ops-executable /absolute/path/to/mcp-agent-ops \
  --print-invocation
```

Print a safe dry-run invocation without executing a paid harness or running fixture verification with:

```bash
python3 scripts/run-agent-skill-evals.py \
  --case typescript-order-pricing \
  --harness codex \
  --model configured-model \
  --print-invocation
```

Prompt text requesting an agent is not agent-attribution evidence. A receipt may claim exact selected-agent attribution only when a captured agent-start event names the intended agent and carries the effective native-adapter digest. Junie 26.7.13 session ledgers can provide a matching custom-agent STARTED and FINISHED lifecycle for the selected name, which the runner retains as name-level evidence. Those events do not carry the adapter digest, so a local Junie run remains unverified for exact-definition attribution even when its harness, MCP, skill, and named-agent integration evidence passes. Receipts also bind the conceptual source digest, native adapter source and effective digests, and adapter sanitization actions when those claims are available. Codex and Junie invocations, fixture commands, and preparation commands execute from argument vectors without a shell interpretation layer.

Read-only Codex scenarios capture the final assistant response through the harness last-message output option. Read-only Junie scenarios extract the single terminal result from its validated JSON stream. In both cases the final review artifact lives in the runner-owned evidence area and the product snapshot must remain unchanged.

## Functional Isolation And Containment

Evidence reports two separate properties:

- Functional isolation compares before and after complete workspace manifests, including dependency and build trees. It reports narrowly declared, recognized ephemeral compiler and test output separately from product changes, never permits a dependency or tool component to become ephemeral even beneath an allowed ancestor, enforces read-only behavior or allowed product paths, and reports every observed change. Only runner-owned context, metadata, and Git control artifacts are excluded.
- Security containment records the declared containment level, evidence verification status, enforcing boundary, and captured evidence.

Containment levels are externally-contained, workspace-isolated-only, and containment-unverified. Containment evidence status is verified, unverified, or failed; it is not the overall run verdict. Dry-run invocation records report containment-unverified because functional isolation has not yet been measured. Live execution snapshots the complete auditable workspace before and after the harness, separates case-declared ephemeral build output from the product diff, and compares product changes with the immutable case allowed-write and protected-path contract. Codex may additionally report its native legacy sandbox or its exact custom permission profile. Ordinary Junie runs report containment-unverified and never infer security containment from a tool allowlist. The externally-contained tier remains required only for explicitly high-risk cases or an explicit security-contained claim.

## Judge Calibration

The calibration metrics tool recomputes binary F1, linearly weighted kappa on the fixed zero-through-four scale, critical-defect recall, and sample count; caller-supplied metric values are rejected when they differ. Diagnostic calibration requires exactly the governed version-one policy: at least twenty-five examples, at least five examples in each class, at least two failed gold examples, and at least five critical failed gold examples. The five classes are clear-pass, clear-fail, boundary, incomplete-plausible, and adversarially-polished. Boundary or otherwise ambiguous examples require two distinct Human Judges plus an independent adjudicator whose result defines the gold label and score. Thresholds are binary F1 of at least 0.85, weighted kappa of at least 0.70, and critical-defect recall of exactly 1.0.

Calibration promotion is currently disabled. Self-reported labels and scores are sufficient for diagnostic metric calculation but cannot establish a calibrated Model Judge. A raw Judge pass and calibration status are reported separately. Promotion remains pending until each sample binds canonical Model Judge request and output artifacts, trusted harness, model, and reasoning identity, independent Human Judge and adjudication evidence, and coverage of every critical rubric dimension. Once that provenance contract is implemented, accepted calibration must be keyed by the complete execution identity rather than shared across Codex, Junie, models, or reasoning profiles.

The versioned Judge prompt and strict output schema are judge-prompt-v1.md and judge-output-schema.yaml. The agent_skill_judge_contract.py tool builds separate trusted instruction and untrusted input-manifest messages, validates every returned evidence reference and digest binding, and recomputes dimension thresholds, overall pass, and critical failure. The canonical request binds the selected case, run, harness, candidate-output artifact, and every governed evidence artifact. A receipt must reference the canonical instruction, manifest, candidate, governed evidence, and output artifacts; receipt summaries are compared with those artifacts rather than trusted directly.

The current case Judge plan is executable policy. Receipts must contain every configured Deterministic Judge check exactly once with catalog-matching criticality. A critical failure skips the Model Judge and prevents a Judge-passed result. A non-null model rubric requires exact zero-through-four dimension scores with evidence; the framework derives pass or fail from the current no-compensation and per-dimension rules. An independent Judge must use a distinct invocation and context, link the evaluated run, bind its prompt and input manifest, record model and reasoning identity, and declare blindness to treatment, expected winner, and evaluated-model identity.

## Skill Probe Variants

Harness-backed skill probes run one frozen variant at a time: treatment, target-omitted, or wrong-skill. The dry-run record and receipt bind the probe id, variant, and one comparison key. A positive base case or any single variant remains incomplete probe evidence. Reporting may promote paired-control coverage only after all three comparable receipts are current and Judge-passed, critical gates pass, and the paired-run Judge confirms treatment lift without target credit in either control. Full probe coverage additionally requires a linked negative-activation case. The current catalog links `terminology-standard-negative-activation` through its Agent scenario and documentation-methodology Workflow relationships while keeping `probe-terminology-standard.executableCases` positive-only. Catalog linkage alone does not promote negative-case or full-probe coverage; current valid receipts and paired treatment, target-omitted, and wrong-skill controls remain required. The catalog therefore still reports zero full probes.

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
- For a model-visible projection run, the complete prepared-source identity, exact visible and evaluator-only partition, projected input records, applied mutation records, projection and synchronization artifacts with content and internal manifest digests, and the evaluator-only verification command and result.
- For MCP-enabled runs, release and launcher identity, session and selected process stream, exact host configuration and staged catalog artifacts, required tool sequences with same-call argument digests and bounded outcomes, optional Junie authorization and name-level lifecycle evidence, and a replayable manifest of retained allowed outputs.
- Budget limits and measured turns, tokens, seconds, and tool calls.
- Current case-definition identity plus prepared source, full prepared-snapshot, dependency, controlled-environment, toolchain, platform, architecture, and prepared-key identity.
- Functional-isolation and containment evidence.
- Complete ordered Deterministic Judge checks, current-rubric Model Judge dimensions, calibrated verdict evidence, and separately identified Human Judge evidence when applicable.
- Behavior assertions, findings, shell-free command evidence, and independent Judge provenance.

Every evidence reference uses normalized relative file#marker syntax and must resolve to a non-symlink UTF-8 artifact inside the receipt directory. Absolute paths, traversal, escaping symbolic links, and missing targets fail before any artifact read. Invocation and skill-read references identify exactly one matching JSON Lines event. Naming an agent or skill in a result is not evidence that it ran or loaded.

Validate captured candidate evidence and classify execution, Judge outcome, security containment, calibration, and digest staleness with:

```bash
python3 scripts/run-agent-skill-evals.py \
  --case typescript-order-pricing \
  --project-root /path/to/disposable-working-copy \
  --result /path/to/evidence/eval-result.md \
  --evidence /path/to/evidence/evidence.yaml
```

Evidence classification reads and validates the captured artifacts; it does not execute the case verification command against the supplied project root. All current cases are ordinary local cases. A local receipt may establish execution and a Judge result without making a security-contained claim. The legacy verified field remains accepted for compatibility but is not a primary reporting status.

Receipt version 1 remains accepted for validation compatibility, but it does not satisfy the complete version 2 execution contract for current evaluation evidence. The observations in results/2026-07-09-live-agent-evaluations.md predate the receipt proof contract and do not count as current receipt-backed behavior evidence.
