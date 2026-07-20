# Agent-Owned Evaluation Suites

This is the steady-state organization for behavioral evaluation work. Each suite starts from one canonical conceptual agent definition, derives a small set of high-value scenarios, runs the standard generated target agent, and evaluates the result through a hardcoded independent Judge.

Suites are maintained in descending order of direct end-user value. The catalog contains one executable suite for every conceptual agent definition, from Dev Coder through Methodology Artifact Reviewer.

The common operating contract is in AGENTS.md. Suite order and concurrency policy are in suite-index.yaml. Shared project skills live under skills. Each named suite contains its own supervisor, Judge, one authoritative scenarios.yaml catalog, and target-specific contract skill.

Codex project-agent names use lowercase letters, digits, and underscores. Suite manifests hardcode the supervisor, target, and Judge runtime names separately from the portable conceptual role ids and generated adapter paths. A Codex run is valid only when retained session evidence proves that every child loaded the staged project-agent definition; task labels and final prose are insufficient.

The root coordinator may launch four supervisors concurrently. Each supervisor has only one active child at a time, so the normal execution ceiling is nine active agents including the root coordinator. A temporary tenth agent is allowed only for one canonical nested dependency declared by the active suite.

Durable governed-result summaries live under results. The initial identity-gated Codex execution is recorded in [the 2026-07-17 agent-suite report](results/2026-07-17-codex-agent-suites.md). The completed 26-suite, 78-scenario rollout is recorded in [the complete agent-suite execution report](results/2026-07-17-complete-agent-suites.md).

The existing catalogs and runner under evals remain the execution and evidence substrate while cases are migrated into this agent-owned layout. Skill probes become targeted diagnostic controls selected by an agent scenario; they are no longer the unit used to plan exhaustive coverage.

The bounded suite runner validates the complete catalog, accepts suite and scenario selections, groups at most four ordinary supervisors per coordinator batch, retains partial failures, records UTC and monotonic timing, and removes disposable workspaces and isolated authentication state after each batch.

The reporting command requires an explicit Codex or Junie harness, resolves a worker ceiling from selected suite count, processors, available memory, and the repository ceiling of four, and gives every suite a disjoint run, evidence, checkpoint, and report destination. Codex binds generated TOML agent definitions by digest. Junie stages only Junie Markdown custom agents through an isolated lookup location and retains a path- and SHA-256-bound staged manifest. Junie 2285.4 lifecycle events expose the custom-agent id and name, exact STARTED and FINISHED status, and step id, but no definition digest or parent relationship. The runner retains those name-level events and runtime diagnostics, then yields BLOCKED rather than claiming exact-definition or topology acceptance. Full Junie catalog execution additionally requires the explicit allow-full-junie option so smoke defaults cannot spend the complete Junie credit budget accidentally.

Terminal PASS or FAIL results require runner-verified receipt references beneath the retained scenario checkpoint root. Every configured deterministic check appears exactly once with catalog-matching criticality, an exact disposition, and a retained artifact path and SHA-256. For Codex, an invoked Judge must return the exact structured disposition as its terminal child response. The runner binds that response to the selected Judge session, parent, scenario order, rollout digest, extracted response digest, and byte-identical Judge output artifact before the receipt audit becomes verified. An absent, malformed, substituted, or mismatched response remains non-passing. Junie lifecycle evidence does not expose an equivalent response-to-topology binding, so Junie remains governed BLOCKED. An authorized Judge skip requires the exact failed critical check and skipped-critical-failure disposition. Diagnostic summary strings remain visible in reports but never prove a verdict.

Browser scenarios use the exact Playwright version recorded in package.json and package-lock.json. Install the local package and its repository-designated Chromium revision before running those suites:

```bash
cd evals/agent-tests
npm ci
npx playwright install chromium
```

Run one suite and update its independent report plus the global report:

```bash
python3 evals/agent-tests/runner.py reporting run --harness codex --suite dev-coder
```

Run several selected suites with a lower worker cap:

```bash
python3 evals/agent-tests/runner.py reporting run --harness codex --suite dev-coder --suite dev-code-reviewer --max-workers 2
```

Omit suite selectors to run the complete catalog for Codex:

```bash
python3 evals/agent-tests/runner.py reporting run --harness codex
```

Junie uses the same selector and report contract. A selected Junie smoke run does not require the full-catalog authorization:

```bash
python3 evals/agent-tests/runner.py reporting run --harness junie --suite dev-coder
```

The report-only rebuild reads durable suite metadata and never invokes a harness:

```bash
python3 evals/agent-tests/runner.py reporting rebuild --harness codex
```

Regenerating one selected suite writes only that suite's immutable generation and stable manifest, then deterministically updates aggregate counts and its global entry. The explicit update command rebuilds the global HTML from the same retained metadata without running or rewriting any suite report:

```bash
python3 evals/agent-tests/runner.py reporting update --harness codex
```

Each suite generation stores self-contained HTML, machine-readable metadata, and a content-addressed evidence bundle together under one immutable generation directory. Before publication, reporting resolves checkpoint and identity roots beneath the runner result, reopens and re-hashes every receipt, bound artifact, Codex Judge rollout, extracted response, and output artifact, and records complete or missing entries in the bundle manifest. The metadata and stable suite manifest bind the evidence manifest digest, and the generation digest covers the metadata, HTML, and evidence manifest. Reporting validates the complete pending generation and its bundled objects before replacing the stable suite manifest. Aggregate rebuild validates the same bundle again before counting CURRENT PASS or FAIL; missing or mutated evidence stays visibly non-passing. Missing, stale, malformed, duplicate, incompatible-revision, and mixed-harness inputs also remain visible as non-passing input states.

Scenarios declare exceptional runtime facilities through runtimeCapabilities. Offline Node fixtures receive only the selected project dependency tree after its installed TypeScript version matches the tracked lockfile. Offline Maven fixtures receive only checksum-pinned repository files named by the selected project manifest; the isolated home forces Maven offline and the runner proves the fixture tests before model execution. Loopback, descendant-process, and browser scenarios run as isolated single-supervisor batches through a managed permission profile that permits local binding, denies non-local network destinations, and keeps filesystem writes inside the disposable workspace.

Browser cases stage the pinned Playwright packages, safe interaction wrapper, and matching Playwright-managed Chromium revision into the isolated run home. The runner creates the fresh headless browser, fresh context, fresh page, and loopback fixture server for every preflight or target interaction. It does not select a Chrome channel, persistent profile, desktop browser, existing tab, or authentication state. Request interception blocks non-loopback HTTP and HTTPS destinations, and the managed permission profile independently denies non-local network access.

Before starting the coordinator, the runner launches Chromium, opens and observes the configured local target page, and explicitly closes the page, context, browser, and fixture server. A launch or observation failure returns an infrastructure-blocked batch result before any coordinator or target invocation and retains the preflight cleanup evidence. The runner then starts one authenticated broker on an operating-system-assigned loopback port for each scenario. Each target browser scenario remains the sole author and initiator: it writes its declarative interaction file, runs the exact validation command, and runs the bounded client only after validation writes a digest-bound success receipt. Validation failure removes stale validation evidence and leaves the one-shot broker available without launching a browser. The supervisor passes the browser assignment without renaming or paraphrasing schema fields. The broker validates the one-time token, scenario, exact interaction and validation-receipt paths, flat action schema, and both digests before launching Chromium outside the target command sandbox. The wrapper accepts only bounded actions with user-visible Playwright locators and deterministic waits; it has no arbitrary target-supplied evaluation or sleep action. A role name is an accessible name; alert or status content without an explicit accessible label uses the exact visible text locator. The bounded actions include focus and accessibility-attribute observations so a UX target can retain the observed value without turning an intentionally seeded defect into a harness failure.

A browser PASS requires the target-bound validation, runtime, and broker receipts and retained trace, final and target-requested screenshots, console events, browser-side request and response events, service-side route and status diagnostics, Playwright and Chromium versions, broker/browser/context/page identities, fixture root, selected loopback ports, interaction and receipt digests, and timestamped close receipts. The runner rejects missing receipts, supervisor-substituted or mismatched interactions, author-validation-client ordering drift, wrong broker authentication or path, non-loopback activity, version drift, missing evidence, or incomplete page, context, browser, fixture-server, or broker-server cleanup. Scenario evidence, broker identities, and ports are rooted independently, and browser-capable suites remain isolated single-supervisor batches so concurrent work cannot share context, profile, evidence, authority, or port state. The runner closes unused brokers on coordinator failure or interruption and preserves their closure receipts. The missing-runtime-evidence UX scenario remains a static-evidence BLOCKED path, and the blocked-route-owned-cleanup browser scenario still requires complete runtime cleanup before its BLOCKED result.
