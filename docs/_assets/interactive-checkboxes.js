/**
 * Interactive Checkboxes for MkDocs Material
 * Makes all task list checkboxes clickable and persists state in localStorage.
 * State is keyed by page path + checkbox index for uniqueness.
 */
(function () {
  const STORAGE_KEY = "my-memory-checkboxes";

  function getState() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
    } catch {
      return {};
    }
  }

  function saveState(state) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }

  function getPageKey() {
    return window.location.pathname.replace(/\/index\.html$/, "/");
  }

  function updateProgressBars() {
    document.querySelectorAll(".progress-track").forEach((track) => {
      const checkboxes = track.querySelectorAll('input[type="checkbox"]');
      if (checkboxes.length === 0) return;
      const checked = Array.from(checkboxes).filter((cb) => cb.checked).length;
      const pct = Math.round((checked / checkboxes.length) * 100);
      const bar = track.querySelector(".progress-bar-fill");
      const label = track.querySelector(".progress-label");
      if (bar) bar.style.width = pct + "%";
      if (label) label.textContent = `${checked}/${checkboxes.length} (${pct}%)`;
    });

    // Also update any standalone progress counters
    document.querySelectorAll("[data-progress-for]").forEach((el) => {
      const targetId = el.getAttribute("data-progress-for");
      const container = document.getElementById(targetId);
      if (!container) return;
      const cbs = container.querySelectorAll('input[type="checkbox"]');
      const checked = Array.from(cbs).filter((cb) => cb.checked).length;
      const pct = Math.round((checked / cbs.length) * 100);
      el.textContent = `${checked}/${cbs.length} (${pct}%)`;
    });
  }

  function init() {
    const state = getState();
    const pageKey = getPageKey();
    const pageState = state[pageKey] || {};

    // Find all task-list checkboxes
    const checkboxes = document.querySelectorAll(
      '.task-list-indicator, .task-list-control input[type="checkbox"], li input[type="checkbox"]'
    );

    checkboxes.forEach((cb, index) => {
      const key = `cb-${index}`;

      // Restore state
      if (pageState[key] !== undefined) {
        cb.checked = pageState[key];
      }

      // Make clickable
      cb.disabled = false;
      cb.style.cursor = "pointer";
      cb.style.pointerEvents = "auto";

      // Add click handler
      cb.addEventListener("change", function () {
        const currentState = getState();
        if (!currentState[pageKey]) currentState[pageKey] = {};
        currentState[pageKey][key] = cb.checked;
        saveState(currentState);
        updateProgressBars();

        // Visual feedback - strike through parent li text
        const li = cb.closest("li");
        if (li) {
          if (cb.checked) {
            li.style.opacity = "0.6";
            li.style.textDecoration = "line-through";
          } else {
            li.style.opacity = "1";
            li.style.textDecoration = "none";
          }
        }
      });

      // Apply initial styling for already checked items
      const li = cb.closest("li");
      if (li && cb.checked) {
        li.style.opacity = "0.6";
        li.style.textDecoration = "line-through";
      }
    });

    updateProgressBars();
  }

  // Run on page load and on MkDocs instant navigation
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  // Re-init on MkDocs instant navigation
  document.addEventListener("DOMContentSwitch", init);
  // MkDocs Material uses this event name
  if (typeof document$ !== "undefined") {
    document$.subscribe(init);
  }
})();
