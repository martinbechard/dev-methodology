(() => {
  "use strict";

  const DATA_GLOBAL_NAME = "DEV_METHODOLOGY_SKILL_DEFINITIONS";
  const EMPTY_INDEX = 0;
  const NEXT_INDEX = 1;
  const KEY_ENTER = "Enter";
  const KEY_SPACE = " ";
  const KEY_ESCAPE = "Escape";
  const EDITOR_QUERY_PARAMETER = "editor";
  const REPOSITORY_ROOT_QUERY_PARAMETER = "repoRoot";
  const DEFAULT_EDITOR_SCHEME = "vscode";
  const DOM_READY_STATE_LOADING = "loading";
  const EDIT_BUTTON_LABEL = "Edit";
  const EDIT_UNAVAILABLE_LABEL = "Edit requires repoRoot or a local file URL.";
  const EDITOR_SCHEME_PATTERN = /^[a-z][a-z0-9+.-]*$/i;
  const STYLE_TEXT = `
    .skill-definition-trigger {
      cursor: pointer;
      transition: box-shadow 160ms ease, transform 160ms ease;
    }

    .skill-definition-trigger:hover,
    .skill-definition-trigger:focus-visible {
      box-shadow: 0 0 0 2px rgba(180, 83, 9, 0.22);
      outline: none;
      transform: translateY(-1px);
    }

    .skill-modal[hidden] {
      display: none;
    }

    .skill-modal {
      position: fixed;
      inset: 0;
      z-index: 1000;
      display: grid;
      place-items: center;
      padding: min(5vw, 2rem);
    }

    .skill-modal__overlay {
      position: absolute;
      inset: 0;
      background: rgba(24, 33, 47, 0.58);
    }

    .skill-modal__panel {
      position: relative;
      display: grid;
      grid-template-rows: auto minmax(0, 1fr);
      width: min(980px, 100%);
      max-height: min(86vh, 920px);
      border: 1px solid var(--color-line, #d9e0ea);
      border-radius: var(--radius, 0.5rem);
      background: var(--color-panel, #ffffff);
      color: var(--color-ink, #18212f);
      box-shadow: 0 28px 72px rgba(24, 33, 47, 0.28);
      overflow: hidden;
    }

    .skill-modal__header {
      display: flex;
      justify-content: space-between;
      gap: 1rem;
      padding: 1rem 1.2rem;
      border-bottom: 1px solid var(--color-line, #d9e0ea);
      background: #f9fbfe;
    }

    .skill-modal__title-block {
      min-width: 0;
    }

    .skill-modal__category {
      margin: 0 0 0.35rem;
      color: var(--color-skill, #b45309);
      font-size: var(--font-xs, 0.78rem);
      font-weight: 780;
      text-transform: uppercase;
    }

    .skill-modal__title {
      margin: 0;
      font-size: 1.3rem;
      letter-spacing: 0;
    }

    .skill-modal__source {
      margin: 0.35rem 0 0;
      color: var(--color-muted, #596579);
      font-size: var(--font-xs, 0.78rem);
      word-break: break-word;
    }

    .skill-modal__actions {
      display: flex;
      flex: 0 0 auto;
      align-items: flex-start;
      gap: 0.5rem;
    }

    .skill-modal__button {
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

    .skill-modal__button:hover,
    .skill-modal__button:focus-visible {
      border-color: var(--color-skill, #b45309);
      outline: none;
    }

    .skill-modal__button--primary {
      background: var(--color-soft-amber, #fff1d8);
      color: var(--color-skill, #b45309);
    }

    .skill-modal__button[aria-disabled="true"] {
      opacity: 0.58;
      pointer-events: none;
    }

    .skill-modal__body {
      overflow: auto;
      padding: 1.2rem;
    }

    .skill-modal__summary {
      margin: 0 0 1rem;
      padding: 0.85rem;
      border: 1px solid var(--color-line, #d9e0ea);
      border-radius: var(--radius-small, 0.35rem);
      background: var(--color-soft-amber, #fff1d8);
      color: var(--color-ink, #18212f);
    }

    .skill-modal__content > * + * {
      margin-top: 0.9rem;
    }

    .skill-modal__content h2,
    .skill-modal__content h3,
    .skill-modal__content h4,
    .skill-modal__content h5,
    .skill-modal__content h6 {
      margin: 1.35rem 0 0.5rem;
      letter-spacing: 0;
    }

    .skill-modal__content p,
    .skill-modal__content li {
      color: var(--color-muted, #596579);
    }

    .skill-modal__content ul,
    .skill-modal__content ol {
      padding-left: 1.35rem;
    }

    .skill-modal__content li + li {
      margin-top: 0.35rem;
    }

    .skill-modal__content pre {
      overflow: auto;
      padding: 0.9rem;
      border: 1px solid var(--color-line, #d9e0ea);
      border-radius: var(--radius-small, 0.35rem);
      background: #111827;
      color: #f9fafb;
      font-size: 0.86rem;
      line-height: 1.55;
    }

    .skill-modal__content pre code {
      display: block;
      padding: 0;
      border-radius: 0;
      background: transparent;
      color: inherit;
      font: inherit;
    }

    @media (max-width: 700px) {
      .skill-modal {
        padding: 0.75rem;
      }

      .skill-modal__header {
        display: grid;
      }

      .skill-modal__actions {
        width: 100%;
      }

      .skill-modal__button {
        flex: 1 1 auto;
      }
    }
  `;

  let modalElements = null;
  let lastFocusedElement = null;

  function skillData() {
    const data = window[DATA_GLOBAL_NAME];
    if (!data || typeof data !== "object" || !data.skills) {
      return { skills: {} };
    }
    return data;
  }

  function escapeHtml(value) {
    return value
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
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

  function editorUrlForSkill(skill) {
    const repositoryRoot = repositoryRootPath();
    if (!repositoryRoot) {
      return "";
    }
    return `${selectedEditorScheme()}://file${encodeURI(`${repositoryRoot}/${skill.sourcePath}`)}`;
  }

  function injectStyle() {
    if (document.getElementById("skill-browser-style")) {
      return;
    }

    const style = document.createElement("style");
    style.id = "skill-browser-style";
    style.textContent = STYLE_TEXT;
    document.head.appendChild(style);
  }

  function ensureModal() {
    if (modalElements) {
      return modalElements;
    }

    const modal = document.createElement("div");
    modal.className = "skill-modal";
    modal.hidden = true;
    modal.innerHTML = `
      <div class="skill-modal__overlay" data-skill-modal-close></div>
      <section class="skill-modal__panel" role="dialog" aria-modal="true" aria-labelledby="skill-modal-title">
        <header class="skill-modal__header">
          <div class="skill-modal__title-block">
            <p class="skill-modal__category"></p>
            <h2 class="skill-modal__title" id="skill-modal-title"></h2>
            <p class="skill-modal__source"></p>
          </div>
          <div class="skill-modal__actions">
            <a class="skill-modal__button skill-modal__button--primary" href="#" target="_blank" rel="noopener">${EDIT_BUTTON_LABEL}</a>
            <button class="skill-modal__button" type="button" data-skill-modal-close>Close</button>
          </div>
        </header>
        <div class="skill-modal__body" id="skill-modal-body"></div>
      </section>
    `;
    document.body.appendChild(modal);

    modalElements = {
      modal,
      title: modal.querySelector("#skill-modal-title"),
      category: modal.querySelector(".skill-modal__category"),
      source: modal.querySelector(".skill-modal__source"),
      body: modal.querySelector("#skill-modal-body"),
      edit: modal.querySelector(".skill-modal__button--primary"),
      close: modal.querySelector("button[data-skill-modal-close]"),
    };

    modal.querySelectorAll("[data-skill-modal-close]").forEach((trigger) => {
      trigger.addEventListener("click", closeModal);
    });

    document.addEventListener("keydown", (event) => {
      if (!modal.hidden && event.key === KEY_ESCAPE) {
        closeModal();
      }
    });

    return modalElements;
  }

  function openSkillDefinition(skill, sourceElement) {
    const elements = ensureModal();
    const editUrl = editorUrlForSkill(skill);
    lastFocusedElement = sourceElement;
    elements.title.textContent = skill.displayName || skill.name;
    elements.category.textContent = skill.categoryLabel || skill.category;
    elements.source.textContent = skill.sourcePath;
    elements.body.innerHTML = `
      <p class="skill-modal__summary">${escapeHtml(skill.description || skill.shortDescription || "")}</p>
      <div class="skill-modal__content">${skill.html || ""}</div>
    `;
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

  function enhanceSkillBadges() {
    const skills = skillData().skills || {};
    document.querySelectorAll(".tag").forEach((tag) => {
      const skillName = (tag.textContent || "").trim();
      const skill = skills[skillName];
      if (!skill || tag.dataset.skillDefinition) {
        return;
      }

      tag.dataset.skillDefinition = skillName;
      tag.classList.add("skill-definition-trigger");
      tag.setAttribute("role", "button");
      tag.setAttribute("tabindex", "0");
      tag.setAttribute("aria-haspopup", "dialog");
      tag.setAttribute("aria-label", `Open ${skillName} skill definition`);
      tag.addEventListener("click", () => openSkillDefinition(skill, tag));
      tag.addEventListener("keydown", (event) => {
        if (event.key !== KEY_ENTER && event.key !== KEY_SPACE) {
          return;
        }
        event.preventDefault();
        openSkillDefinition(skill, tag);
      });
    });
  }

  function initializeSkillBrowser() {
    injectStyle();
    ensureModal();
    enhanceSkillBadges();
  }

  if (document.readyState === DOM_READY_STATE_LOADING) {
    document.addEventListener("DOMContentLoaded", initializeSkillBrowser);
  } else {
    initializeSkillBrowser();
  }
})();
