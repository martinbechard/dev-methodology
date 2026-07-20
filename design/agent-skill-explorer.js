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
    if ((coverage.verifiedCases || []).length) return "verified";
    if ((coverage.staleByDigestCases || []).length) return "blocked";
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
    const modeHarnesses = new Set(
      (data.loadingModes || [])
        .filter((item) => !active.loadingMode || item.mode === active.loadingMode)
        .filter((item) => !active.harness || item.harness === active.harness || item.harness === "all")
        .map((item) => item.harness)
    );
    const modeEdgeKinds = new Set(
      (data.loadingModes || [])
        .filter((item) => !active.loadingMode || item.mode === active.loadingMode)
        .filter((item) => !active.harness || item.harness === active.harness || item.harness === "all")
        .flatMap((item) => item.edgeKinds || [])
    );
    let roles = (data.roles || []).filter((role) =>
      (!active.agent || role.id === active.agent) &&
      (!active.modelProfile || role.modelProfile === active.modelProfile) &&
      (!active.folderScope || (active.folderScope === "dynamic") === Boolean(role.dynamicFolderSkills)) &&
      (!active.harness || (role.generatedAdapters || []).some((item) => item.harness === active.harness)) &&
      (!active.loadingMode || modeHarnesses.has("all") || (role.generatedAdapters || []).some((item) => modeHarnesses.has(item.harness))) &&
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
    const graphEdges = (data.edges || []).filter((edge) =>
      !active.loadingMode || modeEdgeKinds.has(edge.kind)
    );

    if (active.loadingMode) {
      const adjacentSkills = new Set(
        graphEdges.filter((edge) => roleIds.has(edge.role)).map((edge) => edge.skill)
      );
      skills = skills.filter((skill) => adjacentSkills.has(skill.id));
      skillIds = new Set(skills.map((skill) => skill.id));
      const adjacentRoles = new Set(
        graphEdges.filter((edge) => skillIds.has(edge.skill)).map((edge) => edge.role)
      );
      roles = roles.filter((role) => adjacentRoles.has(role.id));
      roleIds = new Set(roles.map((role) => role.id));
    }

    if (active.agent) {
      const adjacent = new Set(graphEdges.filter((edge) => roleIds.has(edge.role)).map((edge) => edge.skill));
      skills = skills.filter((skill) => adjacent.has(skill.id));
      skillIds = new Set(skills.map((skill) => skill.id));
    }
    if (active.technology || active.capability || active.category) {
      const adjacent = new Set(graphEdges.filter((edge) => skillIds.has(edge.skill)).map((edge) => edge.role));
      roles = roles.filter((role) => adjacent.has(role.id));
      roleIds = new Set(roles.map((role) => role.id));
    }
    const edges = graphEdges.filter((edge) => roleIds.has(edge.role) && skillIds.has(edge.skill));
    return {
      roles: roles.slice().sort((a, b) => a.id.localeCompare(b.id)),
      skills: skills.slice().sort((a, b) => a.id.localeCompare(b.id)),
      edges,
    };
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

  const api = { filterGraph, nextIndex, nodeStatus };
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
  let focusNodes = [];
  let selectedKey = "";

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
    const routes = data.loadingModes.filter((item) => item.harness === "all" || (node.generatedAdapters || []).some((adapter) => adapter.harness === item.harness));
    selection.innerHTML = `<span class="utility">${kind}</span><h2>${node.label || node.id}</h2><span class="status-chip status-${status}">${status}</span><p>${node.description || "Generated from the canonical repository contract."}</p><ul class="detail-list">${linkList("Canonical source", sourcePaths)}${linkList("Generated adapters", adapters)}${adapterModels.length ? `<li><strong>Model routes</strong><br>${adapterModels.join("<br>")}</li>` : ""}</ul><h2>Evaluation evidence</h2><ul class="detail-list">${evidenceList(cases) || "<li>No associated evaluation case.</li>"}</ul><h2>Applicable loading routes</h2><ul class="detail-list">${routes.map((item) => `<li><span class="status-chip status-${item.status}">${item.status}</span><br><strong>${item.label}</strong><br>${item.mode}${item.evidenceCase ? `<br><a href="../evals/cases.yaml">Evidence case: ${item.evidenceCase}</a>` : ""}</li>`).join("")}</ul>`;
    focusNodes.forEach((item) => item.setAttribute("data-selected", String(item.getAttribute("data-key") === selectedKey)));
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
    });
    group.appendChild(svgElement("rect", { width: 330, height: 38, rx: 8 }));
    const text = svgElement("text", { x: 13, y: 24 });
    text.textContent = node.label || node.id;
    group.appendChild(text);
    group.addEventListener("click", () => showDetails(kind, node));
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
        focusNodes[target].focus();
      }
    });
    svg.appendChild(group);
    focusNodes.push(group);
  }

  function render() {
    const filtered = filterGraph(data, activeFilters());
    svg.replaceChildren();
    focusNodes = [];
    const row = 48;
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
        d: `M 365 ${start + 19} C 560 ${start + 19}, 640 ${end + 19}, 835 ${end + 19}`,
      });
      svg.appendChild(path);
    });
    filtered.roles.forEach((node) => addNode(node, "agent", 35, roleY.get(node.id)));
    filtered.skills.forEach((node) => addNode(node, "skill", 835, skillY.get(node.id)));
    focusNodes.forEach((node, index) => node.setAttribute("tabindex", index === 0 ? "0" : "-1"));
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
        .map((item) => `<li><span class="status-chip status-${item.status}">${item.status}</span><br><strong>${item.label}</strong><br>${item.mode}</li>`)
        .join("");
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

  filterNames.forEach((name) => document.getElementById(`filter-${name}`).addEventListener("change", render));
  document.getElementById("reset-filters").addEventListener("click", () => {
    filterNames.forEach((name) => { document.getElementById(`filter-${name}`).value = ""; });
    render();
  });
  render();
})(typeof window !== "undefined" ? window : undefined);
