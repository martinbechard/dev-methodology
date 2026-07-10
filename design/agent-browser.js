(() => {
  "use strict";

  const DATA_GLOBAL_NAME = "DEV_METHODOLOGY_ROLE_DEFINITIONS";
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

    .agent-modal__yaml {
      min-height: 100%;
      margin: 0;
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
          <pre class="agent-modal__yaml"><code></code></pre>
        </div>
      </section>
    `;
    document.body.appendChild(modal);

    modalElements = {
      modal,
      title: modal.querySelector("#agent-modal-title"),
      category: modal.querySelector(".agent-modal__category"),
      source: modal.querySelector(".agent-modal__source"),
      code: modal.querySelector(".agent-modal__yaml code"),
      edit: modal.querySelector(".agent-modal__button--primary"),
      close: modal.querySelector("button[data-agent-modal-close]"),
    };

    modal.querySelectorAll("[data-agent-modal-close]").forEach((trigger) => {
      trigger.addEventListener("click", closeModal);
    });
    document.addEventListener("keydown", (event) => {
      if (!modal.hidden && event.key === KEY_ESCAPE) {
        closeModal();
      }
    });

    return modalElements;
  }

  function openRoleDefinition(role, sourceElement) {
    const elements = ensureModal();
    const editUrl = editorUrlForRole(role);
    lastFocusedElement = sourceElement;
    elements.title.textContent = role.displayName || role.name;
    elements.category.textContent = role.groupLabel || role.group;
    elements.source.textContent = role.sourcePath;
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
