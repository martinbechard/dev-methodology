// Copyright (c) 2026 Martin.Bechard@DevConsult.ca
// AI attribution: Generated with AI assistance.
// Summary: Filters and renders the generated agent-skill relationship contract with accessible browser interactions.

(function explorerModule(globalScope) {
  "use strict";

  /**
   * Return the conservative display status for one generated role or skill node.
   * @param {object} node Generated role or skill with a coverage mapping.
   * @returns {string} One status-vocabulary identifier without promoting declarations.
   */
  function nodeStatus(node) {
    const coverage = node.coverage || {};
    if ((coverage.staleByDigestCases || []).length) return "blocked";
    if ((coverage.verifiedCases || []).length) return "verified";
    if ((coverage.executableCases || []).length || coverage.structural) return "declared";
    return "missing";
  }

  function matchesVerified(node, filterValue) {
    if (!filterValue) return true;
    const verified = nodeStatus(node) === "verified";
    return filterValue === "verified" ? verified : !verified;
  }

  /**
   * Filter generated roles, skills, and edges while preserving only adjacent graph nodes.
   * @param {object} data Complete version-three explorer payload.
   * @param {object} filters Current select values; empty values leave that dimension open.
   * @returns {object} Sorted roles and skills plus edges whose endpoints remain visible.
   */
  function filterGraph(data, filters) {
    const active = filters || {};
    const matchingModes = (data.loadingModes || [])
      .filter((item) => !active.loadingMode || item.mode === active.loadingMode)
      .filter((item) => !active.harness || item.harness === active.harness || item.harness === "all");
    const modeEdgeKinds = new Set(matchingModes.flatMap((item) => item.edgeKinds || []));
    const constrainByMode = Boolean(modeEdgeKinds.size && (active.harness || active.loadingMode));
    let roles = (data.roles || []).filter((role) =>
      (!active.agent || role.id === active.agent) &&
      (!active.modelProfile || role.modelProfile === active.modelProfile) &&
      (!active.harness || (role.generatedAdapters || []).some((item) => item.harness === active.harness)) &&
      (!active.declarationStatus || nodeStatus(role) === active.declarationStatus) &&
      matchesVerified(role, active.verifiedBehavior)
    );
    let skills = (data.skills || []).filter((skill) =>
      (!active.category || skill.category === active.category) &&
      (!active.technology || skill.id === active.technology) &&
      (!active.capability || (skill.capabilities || []).includes(active.capability)) &&
      (!active.declarationStatus || nodeStatus(skill) === active.declarationStatus) &&
      matchesVerified(skill, active.verifiedBehavior)
    );
    let roleIds = new Set(roles.map((role) => role.id));
    let skillIds = new Set(skills.map((skill) => skill.id));
    const graphEdges = (data.edges || [])
      .filter((edge) => !active.folderScope || (active.folderScope === "dynamic" ? edge.kind === "detected-folder" : edge.kind !== "detected-folder"))
      .filter((edge) => !constrainByMode || modeEdgeKinds.has(edge.kind));
    const pruneDisconnected = Boolean(
      active.agent || active.category || active.technology || active.capability ||
      active.folderScope || active.harness || active.modelProfile ||
      (active.loadingMode && modeEdgeKinds.size)
    );

    if (pruneDisconnected) {
      const eligibleEdges = graphEdges.filter((edge) => roleIds.has(edge.role) && skillIds.has(edge.skill));
      const adjacentRoles = new Set(eligibleEdges.map((edge) => edge.role));
      const adjacentSkills = new Set(eligibleEdges.map((edge) => edge.skill));
      roles = roles.filter((role) => adjacentRoles.has(role.id));
      skills = skills.filter((skill) => adjacentSkills.has(skill.id));
      roleIds = new Set(roles.map((role) => role.id));
      skillIds = new Set(skills.map((skill) => skill.id));
    }
    const edges = graphEdges.filter((edge) => roleIds.has(edge.role) && skillIds.has(edge.skill));
    return {
      roles: roles.slice().sort((a, b) => a.id.localeCompare(b.id)),
      skills: skills.slice().sort((a, b) => a.id.localeCompare(b.id)),
      edges,
    };
  }

  /**
   * Return loading routes supported by the relationships adjacent to one node.
   * @param {object} data Complete explorer payload.
   * @param {string} kind Node kind, either agent or skill.
   * @param {string} nodeId Selected node identifier.
   * @param {object} filters Current harness and loading-mode filters.
   * @returns {object[]} Loading-mode records whose edge kinds touch the node.
   */
  function routesForNode(data, kind, nodeId, filters) {
    const active = filters || {};
    const selectedRole = kind === "agent" ? (data.roles || []).find((role) => role.id === nodeId) : null;
    const hasAvailabilityOverrides = Boolean(selectedRole && (selectedRole.skillAvailability || []).length);
    const adjacentKinds = new Set(
      (data.edges || [])
        .filter((edge) => kind === "agent" ? edge.role === nodeId : edge.skill === nodeId)
        .filter((edge) => !active.folderScope || (active.folderScope === "dynamic" ? edge.kind === "detected-folder" : edge.kind !== "detected-folder"))
        .map((edge) => edge.kind)
    );
    return (data.loadingModes || [])
      .filter((item) => !active.harness || item.harness === active.harness || item.harness === "all")
      .filter((item) => !active.loadingMode || item.mode === active.loadingMode)
      .filter((item) =>
        (item.edgeKinds || []).some((edgeKind) => adjacentKinds.has(edgeKind)) ||
        (hasAvailabilityOverrides && item.mode === "availability-override")
      );
  }

  /**
   * Preserve a selection only while its node remains visible after filtering.
   * @param {string} selectedKey Current kind-and-id selection key.
   * @param {string[]} visibleKeys Keys present in the filtered graph.
   * @returns {string} The preserved key or an empty selection.
   */
  function reconcileSelection(selectedKey, visibleKeys) {
    return (visibleKeys || []).includes(selectedKey) ? selectedKey : "";
  }

  /**
   * Resolve a bounded roving-focus index for arrow, Home, and End keyboard input.
   * @param {number} current Zero-based active node index.
   * @param {string} key KeyboardEvent key value.
   * @param {number} count Number of focusable nodes.
   * @param {number} columns Row step used by vertical arrows.
   * @returns {number} Bounded next index, or minus one for an empty node list.
   */
  function nextIndex(current, key, count, columns) {
    if (!count) return -1;
    if (key === "Home") return 0;
    if (key === "End") return count - 1;
    const step = key === "ArrowDown" ? columns : key === "ArrowUp" ? -columns : key === "ArrowRight" ? 1 : key === "ArrowLeft" ? -1 : 0;
    return Math.max(0, Math.min(count - 1, current + step));
  }

  const api = { filterGraph, nextIndex, nodeStatus, reconcileSelection, routesForNode };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  if (!globalScope || !globalScope.document) return;

  const document = globalScope.document;
  const data = globalScope.DEV_METHODOLOGY_AGENT_SKILL_EXPLORER_DATA;
  if (!data) return;
  const svg = document.getElementById("relationship-map");
  const selection = document.getElementById("selection-detail");
  const empty = document.getElementById("empty-state");
  const namespace = "http://www.w3.org/2000/svg";
  const filterNames = ["agent", "category", "technology", "capability", "folder-scope", "harness", "model-profile", "loading-mode", "declaration-status", "verified-behavior"];
  const settings = globalScope.DEV_METHODOLOGY_DOCUMENTATION_SETTINGS;
  const settingsChangeEvent = settings ? settings.changeEventName : "dev-methodology:documentation-settings-change";
  const settingsHarnessToFilter = {
    codex: "codex",
    "claude-code": "claude",
    "gemini-cli": "gemini",
    "junie-cli": "junie",
  };
  const filterHarnessToSettings = Object.fromEntries(
    Object.entries(settingsHarnessToFilter).map(([settingValue, filterValue]) => [filterValue, settingValue])
  );
  const emptySelectionMarkup = '<span class="utility">Selection</span><h2>Choose a node</h2><p>Use a filter or select a node to inspect its canonical source, generated adapters, loading route, and evidence.</p>';
  let focusNodes = [];
  let selectedKey = "";
  let rovingKey = "";

  function appendOptions(id, values) {
    const select = document.getElementById(`filter-${id}`);
    values.forEach((value) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = value;
      select.appendChild(option);
    });
  }

  appendOptions("agent", data.roles.map((item) => item.id));
  appendOptions("category", [...new Set(data.skills.map((item) => item.category))].sort());
  appendOptions("technology", data.skills.filter((item) => item.detection).map((item) => item.id));
  appendOptions("capability", [...new Set(data.skills.flatMap((item) => item.capabilities || []))].sort());
  appendOptions("harness", [...new Set(data.modelProfiles.flatMap((item) => item.adapters.map((adapter) => adapter.harness)))].sort());
  appendOptions("model-profile", data.modelProfiles.map((item) => item.id));
  appendOptions("loading-mode", [...new Set(data.loadingModes.map((item) => item.mode))].sort());
  appendOptions("declaration-status", data.statusVocabulary.map((item) => item.id));

  if (settings) {
    const preferredHarness = settings.resolveHarness(Object.keys(settingsHarnessToFilter), "codex");
    document.getElementById("filter-harness").value = settingsHarnessToFilter[preferredHarness] || "codex";
  }

  const legend = document.getElementById("status-legend");
  data.statusVocabulary.forEach((status) => {
    const chip = document.createElement("span");
    chip.className = `status-chip status-${status.id}`;
    chip.textContent = status.id;
    chip.title = status.description;
    legend.appendChild(chip);
  });

  function activeFilters() {
    const values = {};
    filterNames.forEach((name) => {
      const key = name.replace(/-([a-z])/g, (_match, letter) => letter.toUpperCase());
      values[key] = document.getElementById(`filter-${name}`).value;
    });
    return values;
  }

  function svgElement(name, attributes) {
    const element = document.createElementNS(namespace, name);
    Object.entries(attributes || {}).forEach(([key, value]) => element.setAttribute(key, String(value)));
    return element;
  }

  function linkList(label, paths) {
    if (!paths.length) return "";
    return `<li><strong>${label}</strong><br>${paths.map((path) => `<a href="../${path}">${path}</a>`).join("<br>")}</li>`;
  }

  function routeExplanation(route) {
    if (route.mode === "native-preload") return "Claude preloads fixed skills when static inlining is disabled.";
    if (route.mode === "skill-tool") return "Claude loads applicable conditional and detected-folder skills through its Skill tool.";
    if (route.mode === "instruction-driven") return "Codex follows repository and folder instructions that activate applicable conditional and detected-folder skills.";
    if (route.mode === "static-inline") return "Definition-owned fixed skills are inserted into the agent instructions.";
    if (route.mode === "request-driven") return "Definition-owned conditional skills apply when their request trigger matches.";
    if (route.mode === "availability-override") return "Per-agent availability can explicitly enable or disable optional Codex skills.";
    if (route.mode === "app-server-injection") return "App-server injection remains separately inspectable even though it defines no graph relationship.";
    return route.label;
  }

  function routeMarkup(route) {
    return `<li><span class="status-chip status-${route.status}">${route.status}</span><br><strong>${route.label}</strong><br>${route.harness} · ${route.mode}<br>${routeExplanation(route)}${route.sourcePath ? `<br><a href="../${route.sourcePath}">Loading source: ${route.sourcePath}</a>` : ""}</li>`;
  }

  function evidenceList(caseIds) {
    return (data.evidence || [])
      .filter((record) => caseIds.includes(record.id))
      .map((record) => {
        const paths = [record.sourcePath, ...(record.receiptPaths || [])].filter(Boolean);
        return `<li><span class="status-chip status-${record.status}">${record.status}</span><br><strong>${record.id}</strong><br>${paths.map((path) => `<a href="../${path}">${path}</a>`).join("<br>")}</li>`;
      })
      .join("");
  }

  function showDetails(kind, node) {
    selectedKey = `${kind}:${node.id}`;
    const status = nodeStatus(node);
    const sourcePaths = [node.sourcePath, node.detectionPath].filter(Boolean);
    const adapters = (node.generatedAdapters || []).map((item) => item.path);
    const cases = (node.coverage && node.coverage.executableCases) || [];
    const adapterModels = (node.generatedAdapters || []).map((item) => `${item.harness}: ${item.model || item.modelProfile}`);
    const routes = routesForNode(data, kind, node.id, activeFilters());
    const availability = (node.skillAvailability || []).map((item) => `${item.enabled ? "Enabled" : "Disabled"}: ${item.name || item.path}`);
    selection.innerHTML = `<span class="utility">${kind}</span><h2>${node.label || node.id}</h2><span class="status-chip status-${status}">${status}</span><p>${node.description || "Generated from the canonical repository contract."}</p><ul class="detail-list">${linkList("Canonical source", sourcePaths)}${linkList("Generated adapters", adapters)}${adapterModels.length ? `<li><strong>Model routes</strong><br>${adapterModels.join("<br>")}</li>` : ""}${availability.length ? `<li><strong>Skill availability overrides</strong><br>${availability.join("<br>")}</li>` : ""}</ul><h2>Evaluation evidence</h2><ul class="detail-list">${evidenceList(cases) || "<li>No associated evaluation case.</li>"}</ul><h2>Applicable loading routes</h2><ul class="detail-list">${routes.map(routeMarkup).join("") || "<li>No loading route is adjacent to this node under the current harness and mode filters.</li>"}</ul>`;
    focusNodes.forEach((item) => {
      const pressed = item.getAttribute("data-key") === selectedKey;
      item.setAttribute("data-selected", String(pressed));
      item.setAttribute("aria-pressed", String(pressed));
    });
  }

  function setRovingNode(node, shouldFocus) {
    focusNodes.forEach((item) => item.setAttribute("tabindex", "-1"));
    if (!node) return;
    rovingKey = node.getAttribute("data-key");
    node.setAttribute("tabindex", "0");
    if (shouldFocus) node.focus();
  }

  function addNode(node, kind, x, y) {
    const group = svgElement("g", {
      class: `map-node status-${nodeStatus(node)}`,
      role: "button",
      tabindex: "-1",
      transform: `translate(${x} ${y})`,
      "aria-label": `${kind} ${node.label || node.id}, ${nodeStatus(node)}`,
      "data-key": `${kind}:${node.id}`,
      "data-selected": selectedKey === `${kind}:${node.id}`,
      "aria-pressed": selectedKey === `${kind}:${node.id}`,
    });
    group.appendChild(svgElement("rect", { width: 330, height: 48, rx: 8 }));
    const text = svgElement("text", { x: 13, y: 20 });
    text.textContent = node.label || node.id;
    group.appendChild(text);
    const statusText = svgElement("text", { x: 13, y: 38, class: "node-status" });
    statusText.textContent = nodeStatus(node);
    group.appendChild(statusText);
    group.addEventListener("click", () => {
      setRovingNode(group, false);
      showDetails(kind, node);
    });
    group.addEventListener("focus", () => setRovingNode(group, false));
    group.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        showDetails(kind, node);
        return;
      }
      const index = focusNodes.indexOf(group);
      const target = nextIndex(index, event.key, focusNodes.length, 1);
      if (target !== index) {
        event.preventDefault();
        setRovingNode(focusNodes[target], true);
      }
    });
    svg.appendChild(group);
    focusNodes.push(group);
  }

  function render() {
    const filtered = filterGraph(data, activeFilters());
    svg.replaceChildren();
    focusNodes = [];
    const row = 58;
    const top = 58;
    const roleY = new Map(filtered.roles.map((item, index) => [item.id, top + index * row]));
    const skillY = new Map(filtered.skills.map((item, index) => [item.id, top + index * row]));
    const height = Math.max(560, top + Math.max(filtered.roles.length, filtered.skills.length) * row + 30);
    svg.setAttribute("viewBox", `0 0 1200 ${height}`);
    const leftLabel = svgElement("text", { x: 35, y: 30, class: "column-label" });
    leftLabel.textContent = `AGENTS / ${filtered.roles.length}`;
    svg.appendChild(leftLabel);
    const rightLabel = svgElement("text", { x: 835, y: 30, class: "column-label" });
    rightLabel.textContent = `SKILLS / ${filtered.skills.length}`;
    svg.appendChild(rightLabel);
    filtered.edges.forEach((edge) => {
      const start = roleY.get(edge.role);
      const end = skillY.get(edge.skill);
      const path = svgElement("path", {
        class: `map-edge edge-${edge.kind}`,
        d: `M 365 ${start + 24} C 560 ${start + 24}, 640 ${end + 24}, 835 ${end + 24}`,
      });
      svg.appendChild(path);
    });
    filtered.roles.forEach((node) => addNode(node, "agent", 35, roleY.get(node.id)));
    filtered.skills.forEach((node) => addNode(node, "skill", 835, skillY.get(node.id)));
    const visibleKeys = focusNodes.map((node) => node.getAttribute("data-key"));
    selectedKey = reconcileSelection(selectedKey, visibleKeys);
    rovingKey = reconcileSelection(rovingKey, visibleKeys) || visibleKeys[0] || "";
    setRovingNode(focusNodes.find((node) => node.getAttribute("data-key") === rovingKey), false);
    if (selectedKey) {
      const [kind, id] = selectedKey.split(":");
      const nodes = kind === "agent" ? filtered.roles : filtered.skills;
      const selectedNode = nodes.find((node) => node.id === id);
      if (selectedNode) showDetails(kind, selectedNode);
    } else {
      selection.innerHTML = emptySelectionMarkup;
    }
    empty.hidden = Boolean(filtered.roles.length || filtered.skills.length);
    svg.hidden = !empty.hidden;
    document.getElementById("result-count").textContent = `${filtered.edges.length} links`;
    document.getElementById("result-summary").textContent = `${filtered.roles.length} agents · ${filtered.skills.length} skills`;
    const routeList = document.getElementById("loading-route-list");
    if (routeList) {
      const filters = activeFilters();
      routeList.innerHTML = data.loadingModes
        .filter((item) => !filters.harness || item.harness === filters.harness || item.harness === "all")
        .filter((item) => !filters.loadingMode || item.mode === filters.loadingMode)
        .map(routeMarkup)
        .join("") || "<li>No route matches this harness and mode.</li>";
    }
    const evidence = document.getElementById("evidence-list");
    if (evidence) {
      const filters = activeFilters();
      evidence.innerHTML = data.evidence
        .filter((item) => !filters.harness || !item.harnesses.length || item.harnesses.includes(filters.harness))
        .filter((item) => !filters.declarationStatus || item.status === filters.declarationStatus)
        .map((item) => `<li><span class="status-chip status-${item.status}">${item.status}</span><br><a href="../${item.sourcePath}">${item.id}</a>${(item.receiptPaths || []).map((path) => `<br><a href="../${path}">receipt</a>`).join("")}</li>`)
        .join("");
    }
  }

  filterNames.forEach((name) => document.getElementById(`filter-${name}`).addEventListener("change", () => {
    if (name === "harness" && settings && filterHarnessToSettings[document.getElementById("filter-harness").value]) {
      settings.set("harness", filterHarnessToSettings[document.getElementById("filter-harness").value]);
    }
    render();
  }));
  document.getElementById("reset-filters").addEventListener("click", () => {
    filterNames.forEach((name) => { document.getElementById(`filter-${name}`).value = ""; });
    render();
  });
  if (settings) {
    document.addEventListener(settingsChangeEvent, (event) => {
      document.getElementById("filter-harness").value = settingsHarnessToFilter[event.detail.harness] || "codex";
      render();
    });
  }
  render();
})(typeof window !== "undefined" ? window : undefined);
