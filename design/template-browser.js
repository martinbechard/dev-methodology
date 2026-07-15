// Copyright (c) 2026 Martin.Bechard@DevConsult.ca
// AI attribution: Generated with AI assistance.
// Summary: Opens generated methodology templates in accessible source-view dialogs with repository-aware links.
// Design: design/documentation-templates.html

(() => {
  "use strict";

  const DATA_GLOBAL_NAME = "DEV_METHODOLOGY_TEMPLATE_DEFINITIONS";
  const TEMPLATE_SELECTOR = "[data-template-definition]";
  const EDITOR_QUERY_PARAMETER = "editor";
  const REPOSITORY_ROOT_QUERY_PARAMETER = "repoRoot";
  const DEFAULT_EDITOR_SCHEME = "vscode";
  const DOM_READY_STATE_LOADING = "loading";
  const KEY_ESCAPE = "Escape";
  const KEY_TAB = "Tab";
  const EDIT_BUTTON_LABEL = "Edit";
  const EDIT_UNAVAILABLE_LABEL = "Edit requires repoRoot or a local file URL.";
  const EDITOR_SCHEME_PATTERN = /^[a-z][a-z0-9+.-]*$/i;
  const STYLE_TEXT = `
    .template-definition-trigger {
      border-radius: 0.2rem;
      cursor: pointer;
    }

    .template-definition-trigger:hover,
    .template-definition-trigger:focus-visible {
      color: #5b21b6;
      outline: 2px solid #7c3aed;
      outline-offset: 2px;
      text-decoration-thickness: 2px;
    }

    .template-modal[hidden] {
      display: none;
    }

    .template-modal {
      position: fixed;
      inset: 0;
      z-index: 1000;
      display: grid;
      place-items: center;
      padding: min(5vw, 2rem);
    }

    .template-modal__overlay {
      position: absolute;
      inset: 0;
      background: rgba(24, 33, 47, 0.62);
    }

    .template-modal__panel {
      position: relative;
      display: grid;
      grid-template-rows: auto minmax(0, 1fr);
      width: min(1040px, 100%);
      max-height: min(88vh, 960px);
      overflow: hidden;
      border: 1px solid var(--color-line, #d9e1ea);
      border-radius: var(--radius, 0.5rem);
      background: var(--color-panel, #ffffff);
      color: var(--color-ink, #172033);
      box-shadow: 0 28px 72px rgba(24, 33, 47, 0.3);
    }

    .template-modal__header {
      display: flex;
      justify-content: space-between;
      gap: 1rem;
      padding: 1rem 1.2rem;
      border-bottom: 1px solid var(--color-line, #d9e1ea);
      background: #f9fbfe;
    }

    .template-modal__title-block {
      min-width: 0;
    }

    .template-modal__language {
      margin: 0 0 0.35rem;
      color: #6d28d9;
      font-size: var(--font-xs, 0.78rem);
      font-weight: 780;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }

    .template-modal__title {
      margin: 0;
      font-size: 1.3rem;
      letter-spacing: 0;
    }

    .template-modal__source {
      margin: 0.35rem 0 0;
      color: var(--color-muted, #5b6678);
      font-size: var(--font-xs, 0.78rem);
      overflow-wrap: anywhere;
    }

    .template-modal__actions {
      display: flex;
      flex: 0 0 auto;
      align-items: flex-start;
      gap: 0.5rem;
    }

    .template-modal__button {
      display: inline-flex;
      min-height: 2.25rem;
      align-items: center;
      justify-content: center;
      padding: 0.42rem 0.72rem;
      border: 1px solid var(--color-line, #d9e1ea);
      border-radius: var(--radius-small, 0.35rem);
      background: var(--color-panel, #ffffff);
      color: var(--color-ink, #172033);
      font: inherit;
      font-size: var(--font-xs, 0.78rem);
      font-weight: 780;
      text-decoration: none;
      cursor: pointer;
    }

    .template-modal__button:hover,
    .template-modal__button:focus-visible {
      border-color: #7c3aed;
      outline: 2px solid #7c3aed;
      outline-offset: 2px;
    }

    .template-modal__button--primary {
      background: var(--color-soft-purple, #f0e8ff);
      color: #5b21b6;
    }

    .template-modal__button[aria-disabled="true"] {
      opacity: 0.58;
      pointer-events: none;
    }

    .template-modal__body {
      overflow: auto;
      padding: 1.2rem;
      background: #f6f8fb;
    }

    .template-modal__content {
      min-height: 100%;
      margin: 0;
      overflow: visible;
      padding: 1rem;
      border: 1px solid #334155;
      border-radius: var(--radius-small, 0.35rem);
      background: #111827;
      color: #f9fafb;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.84rem;
      line-height: 1.55;
      tab-size: 2;
      white-space: pre;
    }

    .template-modal__content code {
      display: block;
      padding: 0;
      border-radius: 0;
      background: transparent;
      color: inherit;
      font: inherit;
    }

    body.template-modal-open {
      overflow: hidden;
    }

    @media (max-width: 700px) {
      .template-modal {
        padding: 0.75rem;
      }

      .template-modal__header {
        display: grid;
      }

      .template-modal__actions {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        width: 100%;
      }

      .template-modal__button {
        width: 100%;
      }
    }
  `;

  let modalElements = null;
  let lastFocusedElement = null;

  function templateData() {
    const data = window[DATA_GLOBAL_NAME];
    if (!data || typeof data !== "object" || !data.templates) {
      return { templates: {} };
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

  function editorUrlForTemplate(template) {
    const repositoryRoot = repositoryRootPath();
    if (!repositoryRoot) {
      return "";
    }
    return `${selectedEditorScheme()}://file${encodeURI(`${repositoryRoot}/${template.sourcePath}`)}`;
  }

  function sourceUrlForTemplate(template) {
    return new URL(`../${template.sourcePath}`, window.location.href).href;
  }

  function injectStyle() {
    if (document.getElementById("template-browser-style")) {
      return;
    }

    const style = document.createElement("style");
    style.id = "template-browser-style";
    style.textContent = STYLE_TEXT;
    document.head.appendChild(style);
  }

  function ensureModal() {
    if (modalElements) {
      return modalElements;
    }

    const modal = document.createElement("div");
    modal.className = "template-modal";
    modal.id = "template-modal";
    modal.hidden = true;
    modal.innerHTML = `
      <div class="template-modal__overlay" data-template-modal-close></div>
      <section class="template-modal__panel" role="dialog" aria-modal="true" aria-labelledby="template-modal-title">
        <header class="template-modal__header">
          <div class="template-modal__title-block">
            <p class="template-modal__language"></p>
            <h2 class="template-modal__title" id="template-modal-title"></h2>
            <p class="template-modal__source"></p>
          </div>
          <div class="template-modal__actions">
            <a class="template-modal__button" data-template-source-link href="#" target="_blank" rel="noopener">Open source</a>
            <a class="template-modal__button template-modal__button--primary" href="#" target="_blank" rel="noopener">${EDIT_BUTTON_LABEL}</a>
            <button class="template-modal__button" type="button" data-template-modal-close>Close</button>
          </div>
        </header>
        <div class="template-modal__body">
          <pre class="template-modal__content"><code></code></pre>
        </div>
      </section>
    `;
    document.body.appendChild(modal);

    modalElements = {
      modal,
      title: modal.querySelector("#template-modal-title"),
      language: modal.querySelector(".template-modal__language"),
      source: modal.querySelector(".template-modal__source"),
      content: modal.querySelector(".template-modal__content code"),
      sourceLink: modal.querySelector("[data-template-source-link]"),
      edit: modal.querySelector(".template-modal__button--primary"),
      close: modal.querySelector("button[data-template-modal-close]"),
    };

    modal.querySelectorAll("[data-template-modal-close]").forEach((trigger) => {
      trigger.addEventListener("click", closeModal);
    });
    document.addEventListener("keydown", handleModalKeydown);
    return modalElements;
  }

  function focusableModalElements() {
    const { modal } = ensureModal();
    return Array.from(
      modal.querySelectorAll('a[href]:not([aria-disabled="true"]), button:not([disabled])'),
    );
  }

  function handleModalKeydown(event) {
    const { modal } = ensureModal();
    if (modal.hidden) {
      return;
    }
    if (event.key === KEY_ESCAPE) {
      closeModal();
      return;
    }
    if (event.key !== KEY_TAB) {
      return;
    }

    const focusable = focusableModalElements();
    if (!focusable.length) {
      return;
    }
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  function openTemplate(template, sourceElement) {
    const elements = ensureModal();
    const editUrl = editorUrlForTemplate(template);
    lastFocusedElement = sourceElement;
    elements.title.textContent = sourceElement.dataset.templateTitle || template.name;
    elements.language.textContent = template.language || "Template";
    elements.source.textContent = template.sourcePath;
    elements.content.textContent = template.content || "";
    elements.sourceLink.href = sourceUrlForTemplate(template);
    elements.edit.title = editUrl ? EDIT_BUTTON_LABEL : EDIT_UNAVAILABLE_LABEL;
    elements.edit.setAttribute("aria-disabled", String(!editUrl));
    if (editUrl) {
      elements.edit.href = editUrl;
      elements.edit.removeAttribute("tabindex");
    } else {
      elements.edit.removeAttribute("href");
      elements.edit.setAttribute("tabindex", "-1");
    }
    elements.modal.hidden = false;
    document.body.classList.add("template-modal-open");
    elements.close.focus();
  }

  function closeModal() {
    const { modal } = ensureModal();
    modal.hidden = true;
    document.body.classList.remove("template-modal-open");
    if (lastFocusedElement instanceof HTMLElement) {
      lastFocusedElement.focus();
    }
  }

  function enhanceTemplateLinks() {
    const templates = templateData().templates || {};
    document.querySelectorAll(TEMPLATE_SELECTOR).forEach((link) => {
      const template = templates[link.dataset.templateDefinition];
      if (!template || link.classList.contains("template-definition-trigger")) {
        return;
      }

      link.classList.add("template-definition-trigger");
      link.setAttribute("aria-haspopup", "dialog");
      link.setAttribute("aria-controls", "template-modal");
      link.setAttribute("aria-label", `View ${link.dataset.templateTitle || template.name} template`);
      link.addEventListener("click", (event) => {
        event.preventDefault();
        openTemplate(template, link);
      });
    });
  }

  function initializeTemplateBrowser() {
    injectStyle();
    ensureModal();
    enhanceTemplateLinks();
  }

  if (document.readyState === DOM_READY_STATE_LOADING) {
    document.addEventListener("DOMContentLoaded", initializeTemplateBrowser);
  } else {
    initializeTemplateBrowser();
  }
})();
