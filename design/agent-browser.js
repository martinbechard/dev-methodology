(() => {
  "use strict";

  const DATA_GLOBAL_NAME = "DEV_METHODOLOGY_ROLE_DEFINITIONS";
  const ENHANCE_SKILL_DEFINITIONS_EVENT = "dev-methodology:enhance-skill-definitions";
  const RUNTIME_LABELS = {
    codex: "Codex",
    "claude-code": "Claude Code",
  };
  const DEFINITION_SELECTOR = "[data-agent-definition]";
  const EDITOR_QUERY_PARAMETER = "editor";
  const REPOSITORY_ROOT_QUERY_PARAMETER = "repoRoot";
  const DEFAULT_EDITOR_SCHEME = "vscode";
  const DOM_READY_STATE_LOADING = "loading";
  const KEY_ESCAPE = "Escape";
  const EDIT_BUTTON_LABEL = "Edit";
  const EDIT_UNAVAILABLE_LABEL = "Edit requires repoRoot or a local file URL.";
  const EDITOR_SCHEME_PATTERN = /^[a-z][a-z0-9+.-]*$/i;
  const STYLE_TEXT = `
    .agent-card__heading {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: var(--space-2, 0.5rem);
    }

    .agent-card__heading h3 {
      margin-bottom: 0;
    }

    .agent-definition-button {
      min-height: 1.5rem;
      margin-left: auto;
      padding: 0.1rem 0;
      border: 0;
      border-radius: var(--radius-small, 0.35rem);
      background: transparent;
      color: var(--color-role, #5b4db7);
      font: inherit;
      font-size: var(--font-xs, 0.78rem);
      font-weight: 780;
      text-decoration: underline;
      text-decoration-thickness: 1px;
      text-underline-offset: 0.18em;
      cursor: pointer;
    }

    .agent-definition-button:hover,
    .agent-definition-button:focus-visible {
      box-shadow: 0 0 0 2px rgba(91, 77, 183, 0.2);
      outline: none;
      text-decoration-thickness: 2px;
    }

    .agent-modal[hidden] {
      display: none;
    }

    .agent-modal {
      position: fixed;
      inset: 0;
      z-index: 1000;
      display: grid;
      place-items: center;
      padding: min(5vw, 2rem);
    }

    .agent-modal__overlay {
      position: absolute;
      inset: 0;
      background: rgba(24, 33, 47, 0.58);
    }

    .agent-modal__panel {
      position: relative;
      display: grid;
      grid-template-rows: auto minmax(0, 1fr);
      width: min(980px, 100%);
      max-height: min(86vh, 920px);
      overflow: hidden;
      border: 1px solid var(--color-line, #d9e0ea);
      border-radius: var(--radius, 0.5rem);
      background: var(--color-panel, #ffffff);
      color: var(--color-ink, #18212f);
      box-shadow: 0 28px 72px rgba(24, 33, 47, 0.28);
    }

    .agent-modal__header {
      display: flex;
      justify-content: space-between;
      gap: 1rem;
      padding: 1rem 1.2rem;
      border-bottom: 1px solid var(--color-line, #d9e0ea);
      background: #f9fbfe;
    }

    .agent-modal__title-block {
      min-width: 0;
    }

    .agent-modal__category {
      margin: 0 0 0.35rem;
      color: var(--color-role, #5b4db7);
      font-size: var(--font-xs, 0.78rem);
      font-weight: 780;
      text-transform: uppercase;
    }

    .agent-modal__title {
      margin: 0;
      font-size: 1.3rem;
      letter-spacing: 0;
    }

    .agent-modal__source {
      margin: 0.35rem 0 0;
      color: var(--color-muted, #596579);
      font-size: var(--font-xs, 0.78rem);
      word-break: break-word;
    }

    .agent-modal__actions {
      display: flex;
      flex: 0 0 auto;
      align-items: flex-start;
      gap: 0.5rem;
    }

    .agent-modal__button {
      display: inline-flex;
      min-height: 2.25rem;
      align-items: center;
      justify-content: center;
      padding: 0.42rem 0.72rem;
      border: 1px solid var(--color-line, #d9e0ea);
      border-radius: var(--radius-small, 0.35rem);
      background: var(--color-panel, #ffffff);
      color: var(--color-ink, #18212f);
      font: inherit;
      font-size: var(--font-xs, 0.78rem);
      font-weight: 780;
      text-decoration: none;
      cursor: pointer;
    }

    .agent-modal__button:hover,
    .agent-modal__button:focus-visible {
      border-color: var(--color-role, #5b4db7);
      outline: none;
    }

    .agent-modal__button--primary {
      background: var(--color-soft-violet, #eeeafd);
      color: var(--color-role, #5b4db7);
    }

    .agent-modal__button[aria-disabled="true"] {
      opacity: 0.58;
      pointer-events: none;
    }

    .agent-modal__body {
      overflow: auto;
      padding: 1.2rem;
    }

    .agent-modal__definition {
      display: grid;
      gap: 1rem;
    }

    .agent-modal__description {
      margin: 0;
      color: var(--color-ink, #18212f);
      font-size: 1.02rem;
    }

    .agent-modal__section {
      display: grid;
      gap: 0.5rem;
    }

    .agent-modal__section h3,
    .agent-modal__section h4,
    .agent-modal__section p {
      margin: 0;
    }

    .agent-modal__section h3 {
      font-size: 0.78rem;
      font-weight: 780;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }

    .agent-modal__tag-row {
      display: flex;
      flex-wrap: wrap;
      gap: 0.45rem;
    }

    .agent-modal__pill {
      display: grid;
      flex: 1 1 13rem;
      gap: 0.25rem;
      padding: 0.6rem 0.7rem;
      border-radius: var(--radius-small, 0.35rem);
      background: var(--color-soft-amber, #fff1d8);
      color: #8a4609;
      font-size: var(--font-xs, 0.78rem);
      font-weight: 700;
    }

    .agent-modal__pill--output {
      background: var(--color-soft-green, #e4f7f4);
      color: #0f766e;
    }

    .agent-modal__pill--conditional {
      background: var(--color-soft-violet, #eeeafd);
      color: #6d28d9;
    }

    .agent-modal__pill-comment {
      color: var(--color-muted, #596579);
      font-size: 0.86rem;
      font-weight: 500;
      line-height: 1.38;
    }

    .agent-modal__scenario-grid {
      display: grid;
      gap: 0.75rem;
    }

    .agent-modal__scenario {
      display: grid;
      gap: 0.7rem;
      padding: 0.9rem;
      border: 1px solid var(--color-line, #d9e0ea);
      border-left: 0.3rem solid var(--color-role, #5b4db7);
      border-radius: var(--radius-small, 0.35rem);
      background: #f9fbfe;
    }

    .agent-modal__scenario-label {
      color: var(--color-role, #5b4db7);
      font-size: var(--font-xs, 0.78rem);
      font-weight: 780;
      text-transform: uppercase;
    }

    .agent-modal__scenario-field {
      display: grid;
      gap: 0.2rem;
    }

    .agent-modal__scenario-field strong {
      font-size: 0.82rem;
    }

    .agent-modal__scenario-field p {
      color: var(--color-muted, #596579);
    }

    .agent-modal__runtime-select {
      width: max-content;
      max-width: 100%;
      padding: 0.38rem 0.5rem;
      border: 1px solid var(--color-line, #d9e0ea);
      border-radius: var(--radius-small, 0.35rem);
      background: var(--color-panel, #ffffff);
      color: var(--color-ink, #18212f);
      font: inherit;
      font-size: 0.86rem;
    }

    .agent-modal__invocation-text {
      margin: 0;
      overflow-wrap: anywhere;
      padding: 0.65rem;
      border: 1px solid var(--color-line, #d9e0ea);
      border-radius: var(--radius-small, 0.35rem);
      background: #111827;
      color: #f9fafb;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 0.82rem;
      line-height: 1.45;
      white-space: pre-wrap;
    }

    .agent-modal__invocation-text code {
      padding: 0;
      border-radius: 0;
      background: transparent;
      color: inherit;
      font: inherit;
    }

    .agent-modal__yaml-details {
      margin-top: 1.25rem;
    }

    .agent-modal__yaml-details summary {
      cursor: pointer;
      color: var(--color-role, #5b4db7);
      font-size: var(--font-xs, 0.78rem);
      font-weight: 780;
    }

    .agent-modal__yaml {
      margin: 0.75rem 0 0;
      overflow: auto;
      padding: 1rem;
      border: 1px solid var(--color-line, #d9e0ea);
      border-radius: var(--radius-small, 0.35rem);
      background: #111827;
      color: #f9fafb;
      font-size: 0.86rem;
      line-height: 1.55;
      white-space: pre;
    }

    .agent-modal__yaml code {
      display: block;
      padding: 0;
      border-radius: 0;
      background: transparent;
      color: inherit;
      font: inherit;
    }

    @media (max-width: 700px) {
      .agent-modal {
        padding: 0.75rem;
      }

      .agent-modal__header {
        display: grid;
      }

      .agent-modal__actions {
        width: 100%;
      }

      .agent-modal__button {
        flex: 1 1 auto;
      }
    }
  `;

  let modalElements = null;
  let lastFocusedElement = null;

  function roleData() {
    const data = window[DATA_GLOBAL_NAME];
    if (!data || typeof data !== "object" || !data.roles) {
      return { roles: {} };
    }
    return data;
  }

  function selectedEditorScheme() {
    const configuredEditor = new URLSearchParams(window.location.search).get(EDITOR_QUERY_PARAMETER);
    if (configuredEditor && EDITOR_SCHEME_PATTERN.test(configuredEditor)) {
      return configuredEditor;
    }
    return DEFAULT_EDITOR_SCHEME;
  }

  function repositoryRootPath() {
    const configuredRoot = new URLSearchParams(window.location.search).get(REPOSITORY_ROOT_QUERY_PARAMETER);
    if (configuredRoot) {
      return configuredRoot.replace(/\/+$/, "");
    }

    if (window.location.protocol === "file:") {
      const designPath = decodeURIComponent(window.location.pathname);
      return designPath.replace(/\/design\/[^/]+$/, "");
    }

    return "";
  }

  function editorUrlForRole(role) {
    const repositoryRoot = repositoryRootPath();
    if (!repositoryRoot) {
      return "";
    }
    return `${selectedEditorScheme()}://file${encodeURI(`${repositoryRoot}/${role.sourcePath}`)}`;
  }

  function injectStyle() {
    if (document.getElementById("agent-browser-style")) {
      return;
    }

    const style = document.createElement("style");
    style.id = "agent-browser-style";
    style.textContent = STYLE_TEXT;
    document.head.appendChild(style);
  }

  function ensureModal() {
    if (modalElements) {
      return modalElements;
    }

    const modal = document.createElement("div");
    modal.className = "agent-modal";
    modal.hidden = true;
    modal.innerHTML = `
      <div class="agent-modal__overlay" data-agent-modal-close></div>
      <section class="agent-modal__panel" role="dialog" aria-modal="true" aria-labelledby="agent-modal-title">
        <header class="agent-modal__header">
          <div class="agent-modal__title-block">
            <p class="agent-modal__category"></p>
            <h2 class="agent-modal__title" id="agent-modal-title"></h2>
            <p class="agent-modal__source"></p>
          </div>
          <div class="agent-modal__actions">
            <a class="agent-modal__button agent-modal__button--primary" href="#" target="_blank" rel="noopener">${EDIT_BUTTON_LABEL}</a>
            <button class="agent-modal__button" type="button" data-agent-modal-close>Close</button>
          </div>
        </header>
        <div class="agent-modal__body">
          <div class="agent-modal__definition">
            <p class="agent-modal__description"></p>
            <section class="agent-modal__section">
              <h3>How this role works</h3>
              <p class="agent-modal__instructions"></p>
            </section>
            <section class="agent-modal__section">
              <h3>Skills used when applicable</h3>
              <div class="agent-modal__tag-row agent-modal__skills"></div>
            </section>
            <section class="agent-modal__section">
              <h3>Expected handoff</h3>
              <div class="agent-modal__tag-row agent-modal__outputs"></div>
            </section>
            <section class="agent-modal__section agent-modal__examples-section" hidden>
              <h3>Example scenarios</h3>
              <div class="agent-modal__scenario-grid"></div>
            </section>
          </div>
          <details class="agent-modal__yaml-details">
            <summary>View canonical role YAML</summary>
            <pre class="agent-modal__yaml"><code></code></pre>
          </details>
        </div>
      </section>
    `;
    document.body.appendChild(modal);

    modalElements = {
      modal,
      title: modal.querySelector("#agent-modal-title"),
      category: modal.querySelector(".agent-modal__category"),
      source: modal.querySelector(".agent-modal__source"),
      description: modal.querySelector(".agent-modal__description"),
      instructions: modal.querySelector(".agent-modal__instructions"),
      skills: modal.querySelector(".agent-modal__skills"),
      outputs: modal.querySelector(".agent-modal__outputs"),
      examplesSection: modal.querySelector(".agent-modal__examples-section"),
      examples: modal.querySelector(".agent-modal__scenario-grid"),
      code: modal.querySelector(".agent-modal__yaml code"),
      edit: modal.querySelector(".agent-modal__button--primary"),
      close: modal.querySelector("button[data-agent-modal-close]"),
    };

    modal.querySelectorAll("[data-agent-modal-close]").forEach((trigger) => {
      trigger.addEventListener("click", closeModal);
    });
    document.addEventListener("keydown", (event) => {
      if (
        !modal.hidden &&
        !document.querySelector(".skill-modal:not([hidden])") &&
        event.key === KEY_ESCAPE
      ) {
        closeModal();
      }
    });

    return modalElements;
  }

  function renderPills(
    container,
    values,
    comments,
    modifier = "",
    areSkillDefinitions = false,
    conditions = {},
  ) {
    container.replaceChildren();
    values.forEach((value) => {
      const pill = document.createElement("span");
      const condition = conditions[value];
      pill.className = `agent-modal__pill tag${modifier}${condition ? " agent-modal__pill--conditional" : ""}`;
      if (areSkillDefinitions) {
        pill.dataset.skillDefinition = value;
      }
      const label = document.createElement("span");
      label.textContent = value;
      pill.appendChild(label);
      const comment = comments[value];
      if (comment) {
        const detail = document.createElement("span");
        detail.className = "agent-modal__pill-comment";
        detail.textContent = comment;
        pill.appendChild(detail);
      }
      container.appendChild(pill);
    });
  }

  function renderExamples(container, examples) {
    container.replaceChildren();
    examples.forEach((example, index) => {
      const card = document.createElement("article");
      card.className = "agent-modal__scenario";

      const label = document.createElement("p");
      label.className = "agent-modal__scenario-label";
      label.textContent = `Scenario ${index + 1}`;
      card.appendChild(label);

      [["Purpose", example.purpose], ["Plausible response", example.plausibleResponse]].forEach(
        ([labelText, value]) => {
        const field = document.createElement("div");
        field.className = "agent-modal__scenario-field";
        const heading = document.createElement("strong");
        heading.textContent = labelText;
        const text = document.createElement("p");
        text.textContent = value;
        field.append(heading, text);
        card.appendChild(field);
        },
      );

      const invocations = example.runtimeInvocations || {};
      const invocation = document.createElement("div");
      invocation.className = "agent-modal__scenario-field";
      const invocationHeading = document.createElement("strong");
      invocationHeading.textContent = "How to invoke";
      const runtimeSelect = document.createElement("select");
      runtimeSelect.className = "agent-modal__runtime-select";
      Object.keys(invocations).forEach((runtimeId) => {
        const option = document.createElement("option");
        option.value = runtimeId;
        option.textContent = RUNTIME_LABELS[runtimeId] || runtimeId;
        runtimeSelect.appendChild(option);
      });
      if ("codex" in invocations) {
        runtimeSelect.value = "codex";
      }
      const invocationText = document.createElement("pre");
      invocationText.className = "agent-modal__invocation-text";
      const invocationCode = document.createElement("code");
      invocationText.appendChild(invocationCode);
      const showInvocation = () => {
        invocationCode.textContent = invocations[runtimeSelect.value] || "";
      };
      runtimeSelect.addEventListener("change", showInvocation);
      showInvocation();
      invocation.append(invocationHeading, runtimeSelect, invocationText);
      card.insertBefore(invocation, card.lastElementChild);

      container.appendChild(card);
    });
  }

  function openRoleDefinition(role, sourceElement) {
    const elements = ensureModal();
    const editUrl = editorUrlForRole(role);
    lastFocusedElement = sourceElement;
    elements.title.textContent = role.displayName || role.name;
    elements.category.textContent = role.groupLabel || role.group;
    elements.source.textContent = role.sourcePath;
    elements.description.textContent = role.description || "";
    elements.instructions.textContent = role.instructions || "";
    renderPills(
      elements.skills,
      role.skills || [],
      role.skillJustifications || {},
      "",
      true,
      role.skillConditions || {},
    );
    renderPills(
      elements.outputs,
      role.outputs || [],
      role.outputPurposes || {},
      " agent-modal__pill--output",
    );
    document.dispatchEvent(
      new CustomEvent(ENHANCE_SKILL_DEFINITIONS_EVENT, { detail: elements.skills }),
    );
    const examples = Array.isArray(role.examples) ? role.examples : [];
    elements.examplesSection.hidden = examples.length === 0;
    renderExamples(elements.examples, examples);
    elements.code.textContent = role.yaml || "";
    elements.edit.href = editUrl || "#";
    elements.edit.title = editUrl ? EDIT_BUTTON_LABEL : EDIT_UNAVAILABLE_LABEL;
    elements.edit.setAttribute("aria-disabled", String(!editUrl));
    elements.modal.hidden = false;
    elements.close.focus();
  }

  function closeModal() {
    const { modal } = ensureModal();
    modal.hidden = true;
    if (lastFocusedElement instanceof HTMLElement) {
      lastFocusedElement.focus();
    }
  }

  function initializeAgentBrowser() {
    const roles = roleData().roles;
    injectStyle();
    ensureModal();
    document.querySelectorAll(DEFINITION_SELECTOR).forEach((button) => {
      const role = roles[button.dataset.agentDefinition];
      if (role) {
        button.addEventListener("click", () => openRoleDefinition(role, button));
      }
    });
  }

  if (document.readyState === DOM_READY_STATE_LOADING) {
    document.addEventListener("DOMContentLoaded", initializeAgentBrowser);
  } else {
    initializeAgentBrowser();
  }
})();
