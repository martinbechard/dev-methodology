// Copyright (c) 2026 Martin.Bechard@DevConsult.ca
// AI attribution: Generated with AI assistance.
// Responsibility: Provides accessible dialog, filtering, preference, and form demonstrations for the interaction page.
// Design: design/documentation-design-system/forms-and-actions.html
// Tests: scripts/test_documentation_design_system.py

(() => {
  "use strict";

  const triggers = Array.from(document.querySelectorAll("[data-dialog-open]"));
  const dialog = document.querySelector("[data-dialog]");
  const close = document.querySelector("[data-dialog-close]");
  const preference = document.querySelector("[data-preference]");
  const preferenceStatus = document.querySelector("[data-preference-status]");
  const demoForm = document.querySelector("[data-demo-form]");
  const email = document.querySelector("[data-email]");
  const emailError = document.querySelector("[data-email-error]");
  const formStatus = document.querySelector("[data-form-status]");
  const filterForm = document.querySelector("[data-filter-form]");
  const resultCount = document.querySelector("[data-result-count]");
  let activeTrigger = null;

  function focusableElements() {
    if (!dialog) return [];
    return Array.from(
      dialog.querySelectorAll(
        'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
      )
    ).filter((element) => !element.hidden);
  }

  function closeDialog() {
    if (!dialog || dialog.hidden) return;
    dialog.hidden = true;
    document.body.classList.remove("dialog-open");
    triggers.forEach((trigger) => trigger.setAttribute("aria-expanded", "false"));
    if (activeTrigger) activeTrigger.focus();
  }

  function openDialog(event) {
    activeTrigger = event.currentTarget;
    dialog.hidden = false;
    document.body.classList.add("dialog-open");
    activeTrigger.setAttribute("aria-expanded", "true");
    dialog.querySelector("select, button").focus();
  }

  if (triggers.length && dialog && close) {
    triggers.forEach((trigger) => trigger.addEventListener("click", openDialog));
    close.addEventListener("click", closeDialog);
    dialog.addEventListener("click", (event) => {
      if (event.target === dialog) closeDialog();
    });
    dialog.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        event.preventDefault();
        closeDialog();
        return;
      }
      if (event.key === "Tab") {
        const focusable = focusableElements();
        if (!focusable.length) {
          event.preventDefault();
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
    });
  }

  if (filterForm && resultCount) {
    filterForm.addEventListener("submit", (event) => {
      event.preventDefault();
      const values = Array.from(new FormData(filterForm).values());
      const activeFilters = values.filter((value) => String(value).trim()).length;
      const count = Math.max(3 - activeFilters, 1);
      resultCount.textContent = `${count} ${count === 1 ? "result" : "results"}`;
    });
  }

  if (preference && preferenceStatus) {
    preference.addEventListener("change", () => {
      preferenceStatus.textContent = preference.checked
        ? "Weekly summary enabled"
        : "Weekly summary disabled";
    });
  }

  if (demoForm && email && emailError && formStatus) {
    demoForm.addEventListener("submit", (event) => {
      event.preventDefault();
      const valid = email.validity.valid;
      emailError.hidden = valid;
      formStatus.hidden = !valid;
      if (valid) {
        formStatus.focus();
      } else {
        email.focus();
      }
    });
  }
})();
