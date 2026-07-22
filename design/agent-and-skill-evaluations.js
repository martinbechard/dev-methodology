// Copyright (c) 2026 Martin.Bechard@DevConsult.ca
// AI attribution: Generated with AI assistance.
// Summary: Adds optional accessible text and evidence-state filtering to the static evaluation catalogs.

(() => {
  "use strict";

  /**
   * Returns the cards matching one normalized text query and evidence-state selection.
   * Callers provide card-like objects exposing dataset.search and dataset.status; the
   * function performs no DOM mutation and returns the matching objects in source order.
   */
  function filterCards(cards, query, status) {
    const normalizedQuery = String(query || "").trim().toLowerCase();
    const normalizedStatus = String(status || "all");
    return Array.from(cards).filter((card) => {
      const searchMatches = !normalizedQuery
        || String(card.dataset.search || "").includes(normalizedQuery);
      const statusMatches = normalizedStatus === "all"
        || card.dataset.status === normalizedStatus;
      return searchMatches && statusMatches;
    });
  }

  /**
   * Formats the live-region result count for one catalog kind.
   * The returned text always includes the visible and total counts.
   */
  function resultMessage(kind, visibleCount, totalCount) {
    const noun = kind === "agent" ? "agents" : "skills";
    return `Showing ${visibleCount} of ${totalCount} ${noun}.`;
  }

  /**
   * Applies filter state to supplied DOM-like elements and returns the visible count.
   * This boundary is separately testable without requiring a browser implementation.
   */
  function applyFilterElements(kind, elements) {
    const cards = Array.from(elements.cards || []);
    const matches = new Set(
      filterCards(cards, elements.search.value, elements.status.value),
    );
    cards.forEach((card) => {
      card.hidden = !matches.has(card);
    });
    elements.count.textContent = resultMessage(kind, matches.size, cards.length);
    return matches.size;
  }

  /**
   * Resets one catalog's controls, reapplies the static all-items view, and restores focus.
   * Native button keyboard activation invokes the same click handler as pointer activation.
   */
  function clearFilterElements(kind, elements) {
    elements.search.value = "";
    elements.status.value = "all";
    const visibleCount = applyFilterElements(kind, elements);
    elements.search.focus();
    return visibleCount;
  }

  /**
   * Applies the current controls for an agent or skill catalog and reports the visible count.
   * The static HTML owns all content; this enhancement changes only each card's hidden state
   * and the associated live-region text.
   */
  function applyFilter(kind) {
    const search = document.querySelector(`[data-filter-search="${kind}"]`);
    const status = document.querySelector(`[data-filter-status="${kind}"]`);
    const cards = Array.from(document.querySelectorAll(`[data-kind="${kind}"]`));
    const count = document.getElementById(`${kind}-result-count`);
    if (!search || !status || !count) return 0;

    return applyFilterElements(kind, { cards, search, status, count });
  }

  /**
   * Connects keyboard-operable search, status, and clear controls after the DOM is ready.
   * Repeated initialization is harmless because each scope is marked after binding.
   */
  function initializeFilters() {
    document.querySelectorAll("[data-filter-scope]").forEach((container) => {
      if (container.dataset.filterInitialized === "true") return;
      const kind = container.dataset.filterScope;
      const search = container.querySelector(`[data-filter-search="${kind}"]`);
      const status = container.querySelector(`[data-filter-status="${kind}"]`);
      const clear = container.querySelector(`[data-filter-clear="${kind}"]`);
      if (!search || !status || !clear) return;

      search.addEventListener("input", () => applyFilter(kind));
      status.addEventListener("change", () => applyFilter(kind));
      clear.addEventListener("click", () => {
        const cards = Array.from(document.querySelectorAll(`[data-kind="${kind}"]`));
        const count = document.getElementById(`${kind}-result-count`);
        if (count) clearFilterElements(kind, { cards, search, status, count });
      });
      container.dataset.filterInitialized = "true";
    });
  }

  if (typeof module !== "undefined" && module.exports) {
    module.exports = {
      applyFilterElements,
      clearFilterElements,
      filterCards,
      resultMessage,
    };
  }
  if (typeof document !== "undefined") {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", initializeFilters, { once: true });
    } else {
      initializeFilters();
    }
  }
})();
