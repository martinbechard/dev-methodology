#!/usr/bin/env node
// Copyright (c) 2026 Martin.Bechard@DevConsult.ca
// AI attribution: Generated with AI assistance.
// Executes target-authored browser interactions in a fresh, loopback-only Playwright runtime.
// Governing design: evals/agent-tests/implementation-plan.md
// Governing test plan: evals/agent-tests/test_runner.py

import { createHash, randomUUID, timingSafeEqual } from "node:crypto";
import { constants } from "node:fs";
import { lstat, mkdir, open, readFile, realpath, rm, stat, writeFile } from "node:fs/promises";
import { createServer } from "node:http";
import { dirname, extname, isAbsolute, join, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

import { chromium } from "playwright";

const runtimeRoot = dirname(fileURLToPath(import.meta.url));
const configPath = join(runtimeRoot, "runtime-config.json");
const mimeTypes = new Map([
  [".css", "text/css; charset=utf-8"],
  [".html", "text/html; charset=utf-8"],
  [".js", "text/javascript; charset=utf-8"],
  [".json", "application/json; charset=utf-8"],
  [".svg", "image/svg+xml"],
]);

function parseArguments(values) {
  const [mode, ...rest] = values;
  if (!new Set(["broker", "client", "inspect", "preflight", "run", "validate"]).has(mode)) {
    throw new Error("Usage: playwright-harness.mjs broker|client|inspect|preflight|run|validate [options]");
  }
  const options = { mode };
  for (let index = 0; index < rest.length; index += 2) {
    const flag = rest[index];
    const value = rest[index + 1];
    if (!flag?.startsWith("--") || !value) {
      throw new Error(`Invalid argument near ${flag ?? "end of command"}`);
    }
    options[flag.slice(2)] = value;
  }
  return options;
}

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function isLoopbackUrl(value) {
  const parsed = new URL(value);
  return ["127.0.0.1", "localhost", "[::1]"].includes(parsed.hostname);
}

function parseFixedPort(value) {
  if (value === undefined) return null;
  if (typeof value !== "string" || !/^[1-9]\d{0,4}$/.test(value)) {
    throw new Error("--port must be a canonical decimal integer from 1 to 65535");
  }
  const port = Number(value);
  if (port > 65535) {
    throw new Error("--port must be a canonical decimal integer from 1 to 65535");
  }
  return port;
}

async function validateFixtureBinding(binding) {
  if (!binding || typeof binding !== "object" || !isAbsolute(binding.configuredPath ?? "") ||
      !isAbsolute(binding.canonicalRoot ?? "") || !Array.isArray(binding.chain) || !binding.chain.length) {
    throw new Error("Fixture root binding is invalid");
  }
  const configuredMetadata = await lstat(binding.configuredPath);
  if (configuredMetadata.isSymbolicLink() || !configuredMetadata.isDirectory()) {
    throw new Error("Configured fixture root was replaced");
  }
  for (const expected of binding.chain) {
    const metadata = await lstat(expected.path);
    if (metadata.isSymbolicLink() || !metadata.isDirectory() ||
        metadata.dev !== expected.device || metadata.ino !== expected.inode) {
      throw new Error("Fixture root identity chain changed");
    }
  }
  const canonical = await realpath(binding.configuredPath);
  if (canonical !== binding.canonicalRoot) throw new Error("Fixture root canonical path changed");
  return canonical;
}

async function safeFixtureFile(fixtureBinding, requestUrl) {
  let handle;
  try {
    const parsed = new URL(requestUrl, "http://127.0.0.1");
    const decoded = decodeURIComponent(parsed.pathname);
    const relativePath = decoded === "/" ? "index.html" : decoded.replace(/^\/+/, "");
    const root = await validateFixtureBinding(fixtureBinding);
    const candidate = resolve(root, relativePath);
    if (candidate !== root && !candidate.startsWith(`${root}${sep}`)) return null;
    const candidateRelative = relative(root, candidate);
    let current = root;
    for (const component of candidateRelative.split(sep)) {
      if (!component || component === "." || component === "..") return null;
      current = join(current, component);
      if ((await lstat(current)).isSymbolicLink()) return null;
    }
    const canonicalCandidate = await realpath(candidate);
    if (canonicalCandidate !== root && !canonicalCandidate.startsWith(`${root}${sep}`)) return null;
    handle = await open(canonicalCandidate, constants.O_RDONLY | constants.O_NOFOLLOW);
    const openedMetadata = await handle.stat();
    if (!openedMetadata.isFile()) {
      await handle.close();
      return null;
    }
    await validateFixtureBinding(fixtureBinding);
    const currentCanonical = await realpath(candidate);
    const currentMetadata = await stat(currentCanonical);
    if (currentCanonical !== canonicalCandidate || currentMetadata.dev !== openedMetadata.dev ||
        currentMetadata.ino !== openedMetadata.ino) {
      await handle.close();
      return null;
    }
    return handle;
  } catch {
    if (handle) await handle.close().catch(() => {});
    return null;
  }
}

async function startFixtureServer(fixtureBinding, serviceEvents, requestedPort) {
  const server = createServer(async (request, response) => {
    const handle = await safeFixtureFile(fixtureBinding, request.url ?? "/");
    if (!handle || !new Set(["GET", "HEAD"]).has(request.method ?? "")) {
      if (handle) await handle.close().catch(() => {});
      serviceEvents.push({ method: request.method ?? null, route: request.url ?? null, status: 404 });
      response.writeHead(404, { "content-type": "text/plain; charset=utf-8" });
      response.end("Not found\n");
      return;
    }
    serviceEvents.push({ method: request.method ?? null, route: request.url ?? null, status: 200 });
    const requestPath = new URL(request.url ?? "/", "http://127.0.0.1").pathname;
    response.writeHead(200, {
      "cache-control": "no-store",
      "content-type": mimeTypes.get(extname(requestPath === "/" ? "index.html" : requestPath)) ??
        "application/octet-stream",
    });
    if (request.method === "HEAD") {
      await handle.close();
      response.end();
      return;
    }
    handle.createReadStream().pipe(response);
  });
  await new Promise((resolvePromise, reject) => {
    server.once("error", reject);
    server.listen(requestedPort ?? 0, "127.0.0.1", resolvePromise);
  });
  const address = server.address();
  if (!address || typeof address === "string") {
    throw new Error("Fixture server did not expose a TCP port");
  }
  if (requestedPort !== null && address.port !== requestedPort) {
    await closeServer(server);
    throw new Error(`Fixture server did not bind requested port ${requestedPort}`);
  }
  return { server, port: address.port };
}

function closeServer(server) {
  return new Promise((resolvePromise, reject) => {
    server.close((error) => (error ? reject(error) : resolvePromise()));
  });
}

function locatorFor(page, action) {
  const locatorKeys = ["role", "label", "text", "placeholder", "testId"];
  const present = locatorKeys.filter((key) => typeof action[key] === "string" && action[key]);
  if (present.length !== 1) {
    throw new Error(`Action ${action.type} must declare exactly one user-visible locator`);
  }
  const locator = present[0];
  if (locator === "role") {
    if (typeof action.name !== "string" || !action.name) {
      throw new Error("A role locator requires a visible accessible name");
    }
    return page.getByRole(action.role, { name: action.name, exact: action.exact !== false });
  }
  if (locator === "label") {
    return page.getByLabel(action.label, { exact: action.exact !== false });
  }
  if (locator === "text") {
    return page.getByText(action.text, { exact: action.exact !== false });
  }
  if (locator === "placeholder") {
    return page.getByPlaceholder(action.placeholder, { exact: action.exact !== false });
  }
  return page.getByTestId(action.testId);
}

function validateAction(action) {
  const supported = new Set([
    "check",
    "click",
    "expectChecked",
    "expectAttribute",
    "expectFocused",
    "expectText",
    "expectVisible",
    "fill",
    "goto",
    "observeAttribute",
    "observeFocused",
    "press",
    "reload",
    "screenshot",
    "setInputFiles",
    "setViewport",
    "uncheck",
  ]);
  if (!action || typeof action !== "object" || !supported.has(action.type)) {
    throw new Error(`Unsupported declarative browser action: ${action?.type ?? "missing"}`);
  }
  if (action.type === "goto") {
    if (typeof action.route !== "string" || !action.route.startsWith("/") || action.route.startsWith("//")) {
      throw new Error("goto actions require one loopback-relative route");
    }
    return;
  }
  if (new Set(["reload", "screenshot", "setViewport"]).has(action.type)) return;
  const locatorKeys = ["role", "label", "text", "placeholder", "testId"];
  if (locatorKeys.filter((key) => typeof action[key] === "string" && action[key]).length !== 1) {
    throw new Error(`Action ${action.type} must declare exactly one user-visible locator`);
  }
  if (action.role && (typeof action.name !== "string" || !action.name)) {
    throw new Error("A role locator requires a visible accessible name");
  }
  if (action.type === "setInputFiles" && (
    typeof action.fileName !== "string"
    || !action.fileName
    || typeof action.content !== "string"
  )) {
    throw new Error("setInputFiles requires distinct fileName and content strings");
  }
  if (action.type === "expectAttribute" && (
    typeof action.attribute !== "string"
    || !/^aria-[a-z-]+$/.test(action.attribute)
    || !(typeof action.value === "string" || action.value === null)
  )) {
    throw new Error("expectAttribute requires an aria-* attribute and a string or null value");
  }
  if (action.type === "observeAttribute" && (
    typeof action.attribute !== "string"
    || !/^aria-[a-z-]+$/.test(action.attribute)
  )) {
    throw new Error("observeAttribute requires one aria-* attribute");
  }
}

function parseInteraction(interactionBytes) {
  const interaction = JSON.parse(interactionBytes.toString("utf8"));
  if (!interaction || typeof interaction !== "object" || Array.isArray(interaction) ||
      Object.keys(interaction).length !== 1 || !Object.hasOwn(interaction, "actions") ||
      !Array.isArray(interaction.actions)) {
    throw new Error("Interaction must contain exactly one actions array");
  }
  interaction.actions.forEach(validateAction);
  return interaction;
}

async function performAction(page, action, baseUrl, evidenceRoot, index) {
  validateAction(action);
  if (action.type === "goto") {
    if (typeof action.route !== "string" || !action.route.startsWith("/") || action.route.startsWith("//")) {
      throw new Error("goto actions require one loopback-relative route");
    }
    const destination = new URL(action.route, baseUrl).toString();
    if (!isLoopbackUrl(destination)) {
      throw new Error("goto destination must remain loopback-only");
    }
    await page.goto(destination, { waitUntil: "domcontentloaded" });
    return { index, type: action.type, destination };
  }
  if (action.type === "reload") {
    await page.reload({ waitUntil: "domcontentloaded" });
    return { index, type: action.type };
  }
  if (action.type === "setViewport") {
    if (!Number.isInteger(action.width) || !Number.isInteger(action.height) || action.width < 240 || action.height < 240) {
      throw new Error("setViewport requires integer width and height of at least 240 pixels");
    }
    await page.setViewportSize({ width: action.width, height: action.height });
    return { index, type: action.type, width: action.width, height: action.height };
  }
  if (action.type === "screenshot") {
    const name = typeof action.name === "string" && /^[a-z0-9][a-z0-9-]*$/.test(action.name)
      ? action.name
      : `step-${index}`;
    const path = join(evidenceRoot, `${name}.png`);
    await page.screenshot({ path, fullPage: true });
    return { index, type: action.type, path };
  }
  const locator = locatorFor(page, action);
  if (action.type === "click") await locator.click();
  if (action.type === "check") await locator.check();
  if (action.type === "uncheck") await locator.uncheck();
  if (action.type === "fill") {
    if (typeof action.value !== "string") throw new Error("fill requires a string value");
    await locator.fill(action.value);
  }
  if (action.type === "press") {
    if (typeof action.key !== "string" || !action.key) throw new Error("press requires a key");
    await locator.press(action.key);
  }
  if (action.type === "setInputFiles") {
    await locator.setInputFiles({
      name: action.fileName,
      mimeType: typeof action.mimeType === "string" ? action.mimeType : "text/plain",
      buffer: Buffer.from(action.content, "utf8"),
    });
  }
  if (action.type === "expectVisible") await locator.waitFor({ state: "visible" });
  if (action.type === "expectText") {
    if (typeof action.value !== "string") throw new Error("expectText requires a string value");
    await locator.waitFor({ state: "visible" });
    const observed = (await locator.textContent())?.trim();
    if (observed !== action.value) throw new Error(`Expected visible text ${JSON.stringify(action.value)}, received ${JSON.stringify(observed)}`);
  }
  if (action.type === "expectChecked" && (await locator.isChecked()) !== Boolean(action.value)) {
    throw new Error(`Expected checked state ${Boolean(action.value)}`);
  }
  if (action.type === "expectFocused") {
    const focused = await locator.evaluate((element) => element === document.activeElement);
    if (!focused) throw new Error("Expected the user-visible locator to own keyboard focus");
  }
  if (action.type === "expectAttribute") {
    await locator.waitFor({ state: "visible" });
    const observed = await locator.getAttribute(action.attribute);
    if (observed !== action.value) {
      throw new Error(`Expected ${action.attribute} ${JSON.stringify(action.value)}, received ${JSON.stringify(observed)}`);
    }
  }
  if (action.type === "observeFocused") {
    return {
      index,
      type: action.type,
      locator: action.role ?? action.label ?? action.text ?? action.placeholder ?? action.testId,
      focused: await locator.evaluate((element) => element === document.activeElement),
    };
  }
  if (action.type === "observeAttribute") {
    await locator.waitFor({ state: "visible" });
    return {
      index,
      type: action.type,
      locator: action.role ?? action.label ?? action.text ?? action.placeholder ?? action.testId,
      attribute: action.attribute,
      value: await locator.getAttribute(action.attribute),
    };
  }
  return { index, type: action.type, locator: action.role ?? action.label ?? action.text ?? action.placeholder ?? action.testId };
}

async function readConfiguration() {
  const config = JSON.parse(await readFile(configPath, "utf8"));
  if (config.schema !== "dev-methodology-isolated-playwright-runtime" || config.version !== 1) {
    throw new Error("Playwright runtime configuration is invalid");
  }
  return config;
}

async function executeBrowser(options) {
  if (options.mode === "validate") {
    if (typeof options.scenario !== "string" || !options.scenario) throw new Error("Validation scenario is missing");
    if (typeof options.interaction !== "string" || !isAbsolute(options.interaction)) {
      throw new Error("Validation interaction path must be absolute");
    }
    if (typeof options.receipt !== "string" || !isAbsolute(options.receipt)) {
      throw new Error("Validation receipt path must be absolute");
    }
    await rm(resolve(options.receipt), { force: true });
    const interactionBytes = await readFile(resolve(options.interaction ?? ""));
    const interaction = parseInteraction(interactionBytes);
    const receipt = {
      schema: "dev-methodology-playwright-interaction-validation",
      version: 1,
      status: "validated",
      scenario: options.scenario,
      interaction: {
        path: resolve(options.interaction),
        sha256: sha256(interactionBytes),
        actionCount: interaction.actions.length,
      },
      validatedAt: new Date().toISOString(),
    };
    const receiptPath = resolve(options.receipt);
    await mkdir(dirname(receiptPath), { recursive: true });
    await writeFile(receiptPath, `${JSON.stringify(receipt, null, 2)}\n`);
    return receipt;
  }
  const config = await readConfiguration();
  if (options.mode === "inspect") {
    return {
      schema: config.schema,
      version: config.version,
      playwrightVersion: config.playwrightVersion,
      chromiumExecutable: join(runtimeRoot, config.chromiumExecutable),
    };
  }
  const scenario = config.scenarios?.[options.scenario];
  if (!scenario) throw new Error(`Unknown configured browser scenario: ${options.scenario ?? "missing"}`);
  const phase = options.mode === "preflight" ? "preflight" : "run";
  const requestedPort = parseFixedPort(options.port);
  const evidenceRoot = resolve(phase === "preflight" ? scenario.preflightEvidenceRoot : scenario.evidenceRoot);
  const fixtureRoot = await validateFixtureBinding(scenario.fixtureBinding);
  const interactionPath = options.mode === "run" ? resolve(options.interaction ?? "") : null;
  if (options.mode === "run") {
    const expectedInteraction = resolve(scenario.interactionPath);
    if (!interactionPath || interactionPath !== expectedInteraction || !isAbsolute(interactionPath)) {
      throw new Error(`Interaction path must be ${expectedInteraction}`);
    }
  }
  await mkdir(evidenceRoot, { recursive: true });
  const interactionBytes = options.mode === "run" ? await readFile(interactionPath) : Buffer.from("{\"actions\":[]}");
  const interaction = parseInteraction(interactionBytes);
  const browserId = randomUUID();
  const contextId = randomUUID();
  const pageId = randomUUID();
  const consoleEvents = [];
  const networkEvents = [];
  const serviceEvents = [];
  const actionEvents = [];
  const blockedRequests = [];
  const cleanup = Object.fromEntries(
    ["page", "context", "browser", "server"].map((resource) => [resource, {
      created: false,
      requested: false,
      closed: true,
      disposition: "not-created",
    }]),
  );
  let browser;
  let context;
  let page;
  let fixtureServer;
  let selectedPort;
  let failure;
  let browserVersion;
  try {
    await validateFixtureBinding(scenario.fixtureBinding);
    const service = await startFixtureServer(scenario.fixtureBinding, serviceEvents, requestedPort);
    fixtureServer = service.server;
    selectedPort = service.port;
    cleanup.server = { created: true, requested: false, closed: false };
    const baseUrl = `http://127.0.0.1:${selectedPort}`;
    browser = await chromium.launch({
      executablePath: join(runtimeRoot, config.chromiumExecutable),
      headless: true,
    });
    browserVersion = browser.version();
    cleanup.browser = { created: true, requested: false, closed: false };
    context = await browser.newContext();
    cleanup.context = { created: true, requested: false, closed: false };
    await context.tracing.start({ screenshots: true, snapshots: true, sources: false });
    await context.route("**/*", async (route) => {
      const requestUrl = route.request().url();
      if (["http:", "https:"].includes(new URL(requestUrl).protocol) && !isLoopbackUrl(requestUrl)) {
        blockedRequests.push(requestUrl);
        await route.abort("blockedbyclient");
        return;
      }
      await route.continue();
    });
    page = await context.newPage();
    cleanup.page = { created: true, requested: false, closed: false };
    page.on("console", (message) => consoleEvents.push({ type: message.type(), text: message.text() }));
    page.on("pageerror", (error) => consoleEvents.push({ type: "pageerror", text: error.message }));
    page.on("request", (request) => networkEvents.push({ event: "request", method: request.method(), url: request.url() }));
    page.on("response", (response) => networkEvents.push({ event: "response", status: response.status(), url: response.url() }));
    const configuredRoute = phase === "preflight" ? scenario.preflightRoute : scenario.initialRoute;
    const initialRoute = typeof configuredRoute === "string" ? configuredRoute : "/";
    const initialResponse = await page.goto(new URL(initialRoute, baseUrl).toString(), { waitUntil: "domcontentloaded" });
    actionEvents.push({ index: -1, type: "initialNavigation", route: initialRoute, status: initialResponse?.status() ?? null });
    if (phase === "preflight") await page.getByRole("heading").first().waitFor({ state: "visible" });
    for (let index = 0; index < interaction.actions.length; index += 1) {
      actionEvents.push(await performAction(page, interaction.actions[index], baseUrl, evidenceRoot, index));
    }
    await page.screenshot({ path: join(evidenceRoot, "final.png"), fullPage: true });
  } catch (error) {
    failure = error instanceof Error ? error.message : String(error);
  } finally {
    await writeFile(join(evidenceRoot, "console.json"), `${JSON.stringify(consoleEvents, null, 2)}\n`);
    await writeFile(join(evidenceRoot, "network.json"), `${JSON.stringify(networkEvents, null, 2)}\n`);
    await writeFile(join(evidenceRoot, "service.json"), `${JSON.stringify(serviceEvents, null, 2)}\n`);
    if (context) {
      try {
        await context.tracing.stop({ path: join(evidenceRoot, "trace.zip") });
      } catch (error) {
        failure ??= error instanceof Error ? error.message : String(error);
      }
    }
    if (page) {
      cleanup.page.requested = true;
      cleanup.page.requestedAt = new Date().toISOString();
      await page.close().then(() => {
        cleanup.page.closed = true;
        cleanup.page.closedAt = new Date().toISOString();
        cleanup.page.disposition = "closed";
      }).catch((error) => { failure ??= String(error); });
    }
    if (context) {
      cleanup.context.requested = true;
      cleanup.context.requestedAt = new Date().toISOString();
      await context.close().then(() => {
        cleanup.context.closed = true;
        cleanup.context.closedAt = new Date().toISOString();
        cleanup.context.disposition = "closed";
      }).catch((error) => { failure ??= String(error); });
    }
    if (browser) {
      cleanup.browser.requested = true;
      cleanup.browser.requestedAt = new Date().toISOString();
      await browser.close().then(() => {
        cleanup.browser.closed = true;
        cleanup.browser.closedAt = new Date().toISOString();
        cleanup.browser.disposition = "closed";
      }).catch((error) => { failure ??= String(error); });
    }
    if (fixtureServer) {
      cleanup.server.requested = true;
      cleanup.server.requestedAt = new Date().toISOString();
      await closeServer(fixtureServer).then(() => {
        cleanup.server.closed = true;
        cleanup.server.closedAt = new Date().toISOString();
        cleanup.server.disposition = "closed";
      }).catch((error) => { failure ??= String(error); });
    }
  }
  const receipt = {
    schema: "dev-methodology-isolated-playwright-evidence",
    version: 1,
    status: failure ? "failed" : "completed",
    phase,
    scenario: options.scenario,
    targetIdentity: scenario.targetIdentity,
    fixtureRoot,
    fixtureBinding: scenario.fixtureBinding,
    requestedPort,
    selectedPort,
    interaction: {
      path: interactionPath,
      sha256: sha256(interactionBytes),
      actions: actionEvents,
    },
    runtime: {
      playwrightVersion: config.playwrightVersion,
      chromiumExecutable: config.chromiumExecutable,
      browserVersion: browserVersion ?? null,
      browserId,
      contextId,
      pageId,
    },
    broker: options.brokerId ? {
      id: options.brokerId,
      port: Number(options.brokerPort),
    } : null,
    network: {
      requests: networkEvents.filter((event) => event.event === "request").length,
      responses: networkEvents.filter((event) => event.event === "response").length,
      blockedRequests: blockedRequests.length,
      nonLoopbackRequests: networkEvents.filter((event) => {
        try { return !isLoopbackUrl(event.url); } catch { return false; }
      }).length,
    },
    evidence: {
      trace: "trace.zip",
      screenshot: "final.png",
      console: "console.json",
      network: "network.json",
      service: "service.json",
    },
    cleanup,
    failure,
  };
  await writeFile(join(evidenceRoot, "receipt.json"), `${JSON.stringify(receipt, null, 2)}\n`);
  return receipt;
}

function tokensMatch(actual, expected) {
  const actualBytes = Buffer.from(actual ?? "", "utf8");
  const expectedBytes = Buffer.from(expected ?? "", "utf8");
  return actualBytes.length === expectedBytes.length && timingSafeEqual(actualBytes, expectedBytes);
}

async function readBrokerToken(options) {
  if (typeof options["token-file"] !== "string" || !isAbsolute(options["token-file"])) {
    throw new Error("Broker token file path must be absolute");
  }
  const token = (await readFile(resolve(options["token-file"]), "utf8")).trim();
  if (token.length < 32) throw new Error("Broker token is missing or too short");
  return token;
}

async function readRequestBody(request) {
  const chunks = [];
  let length = 0;
  for await (const chunk of request) {
    length += chunk.length;
    if (length > 65536) throw new Error("Broker request exceeds 64 KiB");
    chunks.push(chunk);
  }
  return JSON.parse(Buffer.concat(chunks).toString("utf8"));
}

async function writeBrokerReceipt(scenario, receipt) {
  const config = await readConfiguration();
  const configured = config.scenarios?.[scenario];
  if (!configured) throw new Error(`Unknown configured browser scenario: ${scenario ?? "missing"}`);
  const evidenceRoot = resolve(configured.evidenceRoot);
  await mkdir(evidenceRoot, { recursive: true });
  await writeFile(join(evidenceRoot, "broker.json"), `${JSON.stringify(receipt, null, 2)}\n`);
}

async function runBroker(options) {
  const config = await readConfiguration();
  const scenario = config.scenarios?.[options.scenario];
  if (!scenario) throw new Error(`Unknown configured browser scenario: ${options.scenario ?? "missing"}`);
  await validateFixtureBinding(scenario.fixtureBinding);
  const token = await readBrokerToken(options);
  if (typeof options["broker-id"] !== "string" || !options["broker-id"]) throw new Error("Broker identity is missing");
  const brokerId = options["broker-id"];
  const startedAt = new Date().toISOString();
  let selectedPort;
  let requestEvidence = null;
  let browserReceipt = null;
  let status = "closed-without-request";
  let failure = null;
  let requestState = "available";
  let requestAttempts = 0;
  let reservationRejections = 0;
  let consumedRequests = 0;
  let resolveDone;
  const done = new Promise((resolvePromise) => { resolveDone = resolvePromise; });
  const server = createServer(async (request, response) => {
    requestAttempts += 1;
    if (requestState !== "available") {
      reservationRejections += 1;
      response.writeHead(409, { "content-type": "application/json", connection: "close" });
      response.end(`${JSON.stringify({ status: "rejected", failure: "Broker request is reserved or consumed" })}\n`);
      return;
    }
    requestState = "validating";
    try {
      if (request.method !== "POST" || request.url !== "/execute") throw new Error("Broker accepts only POST /execute");
      const authorization = request.headers.authorization ?? "";
      if (!authorization.startsWith("Bearer ") || !tokensMatch(authorization.slice(7), token)) {
        throw new Error("Broker authentication failed");
      }
      const body = await readRequestBody(request);
      if (!body || typeof body !== "object" || Array.isArray(body) ||
          new Set(Object.keys(body)).size !== 5 ||
          !["scenario", "interactionPath", "interactionSha256", "validationReceiptPath", "validationReceiptSha256"]
            .every((key) => Object.hasOwn(body, key))) {
        throw new Error("Broker request schema is invalid");
      }
      const expectedPath = resolve(scenario.interactionPath);
      const expectedValidationReceipt = resolve(scenario.validationReceiptPath);
      const interactionPath = resolve(String(body.interactionPath ?? ""));
      const validationReceiptPath = resolve(String(body.validationReceiptPath ?? ""));
      if (body.scenario !== options.scenario || interactionPath !== expectedPath || !isAbsolute(interactionPath) ||
          validationReceiptPath !== expectedValidationReceipt || !isAbsolute(validationReceiptPath)) {
        throw new Error("Broker scenario, interaction path, or validation receipt path is invalid");
      }
      const interactionBytes = await readFile(interactionPath);
      const interactionSha256 = sha256(interactionBytes);
      if (body.interactionSha256 !== interactionSha256) throw new Error("Broker interaction digest is invalid");
      parseInteraction(interactionBytes);
      const validationReceiptBytes = await readFile(validationReceiptPath);
      const validationReceiptSha256 = sha256(validationReceiptBytes);
      if (body.validationReceiptSha256 !== validationReceiptSha256) {
        throw new Error("Broker validation receipt digest is invalid");
      }
      const validationReceipt = JSON.parse(validationReceiptBytes.toString("utf8"));
      if (validationReceipt.schema !== "dev-methodology-playwright-interaction-validation" ||
          validationReceipt.version !== 1 || validationReceipt.status !== "validated" ||
          validationReceipt.scenario !== options.scenario ||
          validationReceipt.interaction?.path !== interactionPath ||
          validationReceipt.interaction?.sha256 !== interactionSha256 ||
          validationReceipt.interaction?.actionCount !== parseInteraction(interactionBytes).actions.length) {
        throw new Error("Broker validation receipt is invalid");
      }
      requestEvidence = {
        scenario: body.scenario,
        interactionPath,
        interactionSha256,
        validationReceiptPath,
        validationReceiptSha256,
      };
      requestState = "consumed";
      consumedRequests += 1;
      browserReceipt = await executeBrowser({
        mode: "run",
        scenario: options.scenario,
        interaction: interactionPath,
        brokerId,
        brokerPort: String(selectedPort),
      });
      status = browserReceipt.status === "completed" ? "completed" : "failed";
      failure = browserReceipt.failure ?? null;
      response.writeHead(status === "completed" ? 200 : 500, {
        "content-type": "application/json",
        connection: "close",
      });
      response.end(`${JSON.stringify(browserReceipt)}\n`);
    } catch (error) {
      const beforeConsumption = requestState === "validating";
      if (beforeConsumption) requestState = "available";
      status = beforeConsumption ? "rejected" : "failed";
      failure = error instanceof Error ? error.message : String(error);
      response.writeHead(beforeConsumption ? 400 : 500, { "content-type": "application/json", connection: "close" });
      response.end(`${JSON.stringify({ status, failure })}\n`);
    } finally {
      if (requestState === "consumed") resolveDone();
    }
  });
  const stopWithoutRequest = () => resolveDone();
  process.once("SIGINT", stopWithoutRequest);
  process.once("SIGTERM", stopWithoutRequest);
  await new Promise((resolvePromise, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", resolvePromise);
  });
  const address = server.address();
  if (!address || typeof address === "string") throw new Error("Broker did not expose a TCP port");
  selectedPort = address.port;
  process.stdout.write(`${JSON.stringify({
    schema: "dev-methodology-playwright-broker-ready",
    version: 1,
    scenario: options.scenario,
    brokerId,
    selectedPort,
  })}\n`);
  await done;
  const requestedAt = new Date().toISOString();
  await closeServer(server);
  const closedAt = new Date().toISOString();
  const brokerReceipt = {
    schema: "dev-methodology-playwright-broker-evidence",
    version: 1,
    status,
    scenario: options.scenario,
    brokerId,
    selectedPort,
    startedAt,
    request: requestEvidence,
    browserReceiptSha256: browserReceipt
      ? sha256(await readFile(resolve(scenario.evidenceRoot, "receipt.json")))
      : null,
    requestAccounting: {
      attempts: requestAttempts,
      reservationRejections,
      consumed: consumedRequests,
    },
    authentication: { tokenDigest: sha256(token) },
    cleanup: {
      server: {
        created: true,
        requested: true,
        requestedAt,
        closed: true,
        closedAt,
        disposition: "closed",
      },
    },
    failure,
  };
  await writeBrokerReceipt(options.scenario, brokerReceipt);
  return brokerReceipt;
}

async function runClient(options) {
  if (typeof options.scenario !== "string" || !options.scenario) throw new Error("Client scenario is missing");
  if (typeof options.interaction !== "string" || !isAbsolute(options.interaction)) {
    throw new Error("Client interaction path must be absolute");
  }
  if (typeof options.endpoint !== "string" || !isLoopbackUrl(options.endpoint)) {
    throw new Error("Client endpoint must be loopback-only");
  }
  const token = await readBrokerToken(options);
  if (typeof options["validation-receipt"] !== "string" || !isAbsolute(options["validation-receipt"])) {
    throw new Error("Client validation receipt path must be absolute");
  }
  const interactionPath = resolve(options.interaction);
  const interactionBytes = await readFile(interactionPath);
  const validationReceiptPath = resolve(options["validation-receipt"]);
  const validationReceiptBytes = await readFile(validationReceiptPath);
  const response = await fetch(new URL("/execute", options.endpoint), {
    method: "POST",
    headers: {
      authorization: `Bearer ${token}`,
      "content-type": "application/json",
    },
    body: JSON.stringify({
      scenario: options.scenario,
      interactionPath,
      interactionSha256: sha256(interactionBytes),
      validationReceiptPath,
      validationReceiptSha256: sha256(validationReceiptBytes),
    }),
  });
  const result = await response.json();
  if (!response.ok) throw new Error(result.failure ?? `Broker returned HTTP ${response.status}`);
  return result;
}

async function execute(options) {
  if (options.mode === "broker") return runBroker(options);
  if (options.mode === "client") return runClient(options);
  return executeBrowser(options);
}

try {
  const result = await execute(parseArguments(process.argv.slice(2)));
  process.stdout.write(`${JSON.stringify(result)}\n`);
  if (result.status === "failed") process.exitCode = 1;
} catch (error) {
  process.stderr.write(`${error instanceof Error ? error.stack : String(error)}\n`);
  process.exitCode = 1;
}
