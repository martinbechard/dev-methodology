// Copyright (c) 2026 Martin.Bechard@DevConsult.ca
// AI attribution: Generated with AI assistance.
// Summary: Verifies persistent documentation setting defaults, validation, and view fallbacks.

"use strict";

const assert = require("node:assert/strict");
const test = require("node:test");

global.window = {
  location: { search: "" },
  localStorage: null,
};
global.document = {
  readyState: "loading",
  addEventListener() {},
};

require("./documentation-settings.js");

const settings = global.window.DEV_METHODOLOGY_DOCUMENTATION_SETTINGS;

function memoryStorage(initialValues = {}) {
  const values = new Map(Object.entries(initialValues));
  return {
    getItem(key) {
      return values.has(key) ? values.get(key) : null;
    },
    setItem(key, value) {
      values.set(key, value);
    },
    value(key) {
      return values.get(key);
    },
  };
}

test("first visit uses Codex and VS Code defaults", () => {
  assert.deepEqual(settings.read(memoryStorage()), { harness: "codex", editor: "vscode" });
});

test("saved values persist across independent page reads", () => {
  const storage = memoryStorage();
  settings.set("harness", "claude-code", storage);
  settings.set("editor", "idea", storage);
  assert.deepEqual(settings.read(storage), { harness: "claude-code", editor: "idea" });
  assert.deepEqual(settings.read(storage), { harness: "claude-code", editor: "idea" });
});

test("invalid stored values are restored to documented defaults", () => {
  const storage = memoryStorage({
    [settings.storageKeys.harness]: "unsupported",
    [settings.storageKeys.editor]: "unknown",
  });
  assert.deepEqual(settings.read(storage), { harness: "codex", editor: "vscode" });
  assert.equal(storage.value(settings.storageKeys.harness), "codex");
  assert.equal(storage.value(settings.storageKeys.editor), "vscode");
});

test("invalid values still default when storage repair is denied", () => {
  const storage = {
    getItem() {
      return "unsupported";
    },
    setItem() {
      throw new Error("denied");
    },
  };
  assert.deepEqual(settings.read(storage), { harness: "codex", editor: "vscode" });
});

test("unavailable saved harness uses the view fallback", () => {
  const storage = memoryStorage({ [settings.storageKeys.harness]: "gemini-cli" });
  assert.equal(settings.resolveHarness(["codex", "claude-code"], "codex", storage), "codex");
  assert.equal(settings.resolveHarness(["codex", "gemini-cli"], "codex", storage), "gemini-cli");
});

test("editor setting supports VS Code, IntelliJ, and explicit query overrides", () => {
  const storage = memoryStorage({ [settings.storageKeys.editor]: "idea" });
  assert.equal(settings.editorScheme("", storage), "idea");
  assert.equal(settings.editorScheme("?editor=vscode", storage), "vscode");
  assert.equal(settings.editorScheme("?editor=idea", memoryStorage()), "idea");
});

test("editor links use editor-specific URL formats for Markdown and YAML", () => {
  const vscodeStorage = memoryStorage({ [settings.storageKeys.editor]: "vscode" });
  const ideaStorage = memoryStorage({ [settings.storageKeys.editor]: "idea" });
  const markdownPath = "/repo/skills/example/SKILL.md";
  const roleYamlPath = "/repo/agents/roles/example.role.yaml";
  const templateYamlPath = "/repo/skills/example/assets/template.yaml";

  assert.equal(
    settings.editorUrl(markdownPath, "", vscodeStorage),
    "vscode://file/repo/skills/example/SKILL.md",
  );
  for (const filePath of [markdownPath, roleYamlPath, templateYamlPath]) {
    assert.equal(
      settings.editorUrl(filePath, "", ideaStorage),
      `idea://open?file=${encodeURIComponent(filePath)}`,
    );
  }
});

test("inaccessible storage cannot prevent usable settings", () => {
  settings.read(memoryStorage());
  const storage = {
    getItem() {
      throw new Error("denied");
    },
    setItem() {
      throw new Error("denied");
    },
  };
  assert.deepEqual(settings.read(storage), { harness: "codex", editor: "vscode" });
  assert.deepEqual(settings.set("editor", "idea", storage), { harness: "codex", editor: "idea" });
});
