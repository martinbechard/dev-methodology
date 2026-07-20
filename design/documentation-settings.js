// Copyright (c) 2026 Martin.Bechard@DevConsult.ca
// AI attribution: Generated with AI assistance.
// Summary: Provides persistent, accessible harness and editor settings across HTML documentation pages.

(() => {
  "use strict";

  const API_GLOBAL_NAME = "DEV_METHODOLOGY_DOCUMENTATION_SETTINGS";
  const CHANGE_EVENT_NAME = "dev-methodology:documentation-settings-change";
  const STORAGE_KEYS = Object.freeze({
    harness: "dev-methodology.documentation.default-harness",
    editor: "dev-methodology.documentation.editor",
  });
  const DEFAULT_SETTINGS = Object.freeze({ harness: "codex", editor: "vscode" });
  const HARNESS_OPTIONS = Object.freeze([
    ["codex", "Codex"],
    ["claude-code", "Claude Code"],
    ["gemini-cli", "Gemini CLI"],
    ["junie-cli", "Junie CLI"],
    ["github-copilot", "GitHub Copilot"],
  ]);
  const EDITOR_OPTIONS = Object.freeze([
    ["vscode", "VS Code"],
    ["idea", "IntelliJ"],
  ]);
  const VALID_VALUES = Object.freeze({
    harness: new Set(HARNESS_OPTIONS.map(([value]) => value)),
    editor: new Set(EDITOR_OPTIONS.map(([value]) => value)),
  });
  const EDITOR_QUERY_PARAMETER = "editor";
  const EDITOR_SCHEME_PATTERN = /^[a-z][a-z0-9+.-]*$/i;
  const KEY_ESCAPE = "Escape";
  const KEY_TAB = "Tab";
  const DOM_READY_STATE_LOADING = "loading";
  const STYLE_TEXT = `
    .documentation-settings {
      margin-left: auto;
    }

    .documentation-settings__trigger {
      display: inline-grid;
      width: 2.5rem;
      height: 2.5rem;
      place-items: center;
      border: 1px solid rgba(255, 255, 255, 0.55);
      border-radius: 999px;
      background: transparent;
      color: inherit;
      font: inherit;
      font-size: 1.25rem;
      cursor: pointer;
    }

    .documentation-settings__trigger:hover,
    .documentation-settings__trigger:focus-visible {
      border-color: currentColor;
      outline: 2px solid currentColor;
      outline-offset: 2px;
    }

    .documentation-settings__dialog[hidden] {
      display: none;
    }

    .documentation-settings__dialog {
      position: fixed;
      inset: 0;
      z-index: 2000;
      display: grid;
      place-items: start end;
      padding: 4.75rem max(1rem, calc((100vw - 1180px) / 2));
      background: rgba(15, 23, 42, 0.48);
    }

    .documentation-settings__panel {
      width: min(24rem, calc(100vw - 2rem));
      padding: 1.25rem;
      border: 1px solid #d9e0ea;
      border-radius: 0.6rem;
      background: #ffffff;
      color: #18212f;
      box-shadow: 0 24px 60px rgba(15, 23, 42, 0.28);
    }

    .documentation-settings__heading {
      margin: 0;
      font-size: 1.25rem;
    }

    .documentation-settings__description {
      margin: 0.35rem 0 1rem;
      color: #596579;
      font-size: 0.88rem;
    }

    .documentation-settings__field {
      display: grid;
      gap: 0.35rem;
      margin-top: 0.85rem;
      font-weight: 700;
    }

    .documentation-settings__field select {
      width: 100%;
      min-height: 2.5rem;
      padding: 0.45rem 0.6rem;
      border: 1px solid #aeb8c6;
      border-radius: 0.35rem;
      background: #ffffff;
      color: #18212f;
      font: inherit;
      font-weight: 500;
    }

    .documentation-settings__close {
      min-height: 2.5rem;
      margin-top: 1.2rem;
      padding: 0.45rem 0.9rem;
      border: 1px solid #334155;
      border-radius: 0.35rem;
      background: #334155;
      color: #ffffff;
      font: inherit;
      font-weight: 700;
      cursor: pointer;
    }

    body.documentation-settings-open {
      overflow: hidden;
    }

    @media (max-width: 680px) {
      .documentation-settings__dialog {
        place-items: start center;
        padding: 4.75rem 1rem 1rem;
      }
    }
  `;

  let memorySettings = { ...DEFAULT_SETTINGS };
  let dialogElements = null;

  function resolveStorage() {
    try {
      return window.localStorage;
    } catch (_error) {
      return null;
    }
  }

  function readValue(storage, settingName) {
    const defaultValue = DEFAULT_SETTINGS[settingName];
    if (!storage) return memorySettings[settingName] || defaultValue;

    let storedValue;
    try {
      storedValue = storage.getItem(STORAGE_KEYS[settingName]);
    } catch (_error) {
      return memorySettings[settingName] || defaultValue;
    }
    if (VALID_VALUES[settingName].has(storedValue)) return storedValue;
    if (storedValue !== null) {
      try {
        storage.setItem(STORAGE_KEYS[settingName], defaultValue);
      } catch (_error) {
        // The documented default still applies even when invalid storage cannot be repaired.
      }
    }
    return defaultValue;
  }

  function readSettings(storage = resolveStorage()) {
    memorySettings = {
      harness: readValue(storage, "harness"),
      editor: readValue(storage, "editor"),
    };
    return { ...memorySettings };
  }

  function writeSetting(settingName, value, storage = resolveStorage()) {
    if (
      !Object.prototype.hasOwnProperty.call(DEFAULT_SETTINGS, settingName)
      || !VALID_VALUES[settingName].has(value)
    ) {
      return readSettings(storage);
    }

    memorySettings = { ...readSettings(storage), [settingName]: value };
    try {
      if (storage) storage.setItem(STORAGE_KEYS[settingName], value);
    } catch (_error) {
      // The in-memory choice still keeps the current page usable when storage is unavailable.
    }
    return { ...memorySettings };
  }

  function resolveHarness(availableHarnesses, fallbackHarness, storage = resolveStorage()) {
    const available = new Set(availableHarnesses || []);
    const preferredHarness = readSettings(storage).harness;
    return available.has(preferredHarness) ? preferredHarness : fallbackHarness;
  }

  function editorScheme(search = window.location.search, storage = resolveStorage()) {
    const configuredEditor = new URLSearchParams(search).get(EDITOR_QUERY_PARAMETER);
    if (configuredEditor && EDITOR_SCHEME_PATTERN.test(configuredEditor)) {
      return configuredEditor;
    }
    return readSettings(storage).editor;
  }

  function editorUrl(filePath, search = window.location.search, storage = resolveStorage()) {
    const scheme = editorScheme(search, storage);
    if (scheme === "idea") {
      return `idea://open?file=${encodeURIComponent(filePath)}`;
    }
    return `${scheme}://file${encodeURI(filePath)}`;
  }

  function dispatchChange(settings) {
    document.dispatchEvent(new CustomEvent(CHANGE_EVENT_NAME, { detail: settings }));
  }

  function createOptions(select, options) {
    options.forEach(([value, label]) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = label;
      select.appendChild(option);
    });
  }

  function closeDialog() {
    if (!dialogElements || dialogElements.dialog.hidden) return;
    dialogElements.dialog.hidden = true;
    dialogElements.trigger.setAttribute("aria-expanded", "false");
    document.body.classList.remove("documentation-settings-open");
    dialogElements.trigger.focus();
  }

  function focusableDialogElements() {
    return Array.from(dialogElements.panel.querySelectorAll("select, button"));
  }

  function handleDialogKeydown(event) {
    if (event.key === KEY_ESCAPE) {
      event.preventDefault();
      closeDialog();
      return;
    }
    if (event.key !== KEY_TAB) return;

    const focusable = focusableDialogElements();
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

  function openDialog() {
    const settings = readSettings();
    dialogElements.harness.value = settings.harness;
    dialogElements.editor.value = settings.editor;
    dialogElements.dialog.hidden = false;
    dialogElements.trigger.setAttribute("aria-expanded", "true");
    document.body.classList.add("documentation-settings-open");
    dialogElements.harness.focus();
  }

  function injectStyle() {
    if (document.getElementById("documentation-settings-style")) return;
    const style = document.createElement("style");
    style.id = "documentation-settings-style";
    style.textContent = STYLE_TEXT;
    document.head.appendChild(style);
  }

  function createSettingsControl(header) {
    const container = document.createElement("div");
    container.className = "documentation-settings";

    const trigger = document.createElement("button");
    trigger.type = "button";
    trigger.className = "documentation-settings__trigger";
    trigger.setAttribute("aria-label", "Settings");
    trigger.setAttribute("aria-haspopup", "dialog");
    trigger.setAttribute("aria-expanded", "false");
    trigger.setAttribute("aria-controls", "documentation-settings-dialog");
    trigger.innerHTML = '<span aria-hidden="true">&#9881;</span>';

    const dialog = document.createElement("div");
    dialog.id = "documentation-settings-dialog";
    dialog.className = "documentation-settings__dialog";
    dialog.setAttribute("role", "dialog");
    dialog.setAttribute("aria-modal", "true");
    dialog.setAttribute("aria-labelledby", "documentation-settings-title");
    dialog.hidden = true;

    const panel = document.createElement("div");
    panel.className = "documentation-settings__panel";
    const heading = document.createElement("h2");
    heading.id = "documentation-settings-title";
    heading.className = "documentation-settings__heading";
    heading.textContent = "Settings";
    const description = document.createElement("p");
    description.className = "documentation-settings__description";
    description.textContent = "These choices are reused across the HTML documentation.";

    const harnessLabel = document.createElement("label");
    harnessLabel.className = "documentation-settings__field";
    harnessLabel.textContent = "Default harness";
    const harness = document.createElement("select");
    harness.setAttribute("aria-label", "Default harness");
    createOptions(harness, HARNESS_OPTIONS);
    harnessLabel.appendChild(harness);

    const editorLabel = document.createElement("label");
    editorLabel.className = "documentation-settings__field";
    editorLabel.textContent = "Editor";
    const editor = document.createElement("select");
    editor.setAttribute("aria-label", "Editor");
    createOptions(editor, EDITOR_OPTIONS);
    editorLabel.appendChild(editor);

    const close = document.createElement("button");
    close.type = "button";
    close.className = "documentation-settings__close";
    close.textContent = "Close";
    panel.append(heading, description, harnessLabel, editorLabel, close);
    dialog.appendChild(panel);
    container.append(trigger, dialog);
    header.appendChild(container);

    dialogElements = { container, trigger, dialog, panel, harness, editor, close };
    trigger.addEventListener("click", openDialog);
    close.addEventListener("click", closeDialog);
    dialog.addEventListener("keydown", handleDialogKeydown);
    dialog.addEventListener("click", (event) => {
      if (event.target === dialog) closeDialog();
    });
    harness.addEventListener("change", () => {
      dispatchChange(writeSetting("harness", harness.value));
    });
    editor.addEventListener("change", () => {
      dispatchChange(writeSetting("editor", editor.value));
    });
  }

  function initializeSettings() {
    if (dialogElements) return;
    const header = document.querySelector(".site-header");
    if (!header) return;
    injectStyle();
    readSettings();
    createSettingsControl(header);
  }

  /**
   * Shared browser API for documentation viewers that need persistent display preferences.
   * Consumers may read or write validated settings, resolve a view-supported harness, and
   * build editor-specific file links while preserving an explicit editor query parameter.
   * Storage access failures are contained and return usable in-memory defaults.
   */
  window[API_GLOBAL_NAME] = Object.freeze({
    changeEventName: CHANGE_EVENT_NAME,
    defaults: DEFAULT_SETTINGS,
    storageKeys: STORAGE_KEYS,
    read: readSettings,
    set: writeSetting,
    resolveHarness,
    editorScheme,
    editorUrl,
  });

  if (document.readyState === DOM_READY_STATE_LOADING) {
    document.addEventListener("DOMContentLoaded", initializeSettings, { once: true });
  } else {
    initializeSettings();
  }
})();
