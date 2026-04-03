/**
 * Interactive Checkboxes — GitHub-backed persistence
 * 
 * Clicking a checkbox edits the actual markdown file via GitHub API
 * and commits the change. Works across all devices.
 * 
 * First visit: prompts for a GitHub Fine-Grained PAT (stored in localStorage).
 * Token scope needed: Contents (read/write) on the my-memory repo only.
 */
(function () {
  const REPO_OWNER = "AyushSonuu";
  const REPO_NAME = "my-memory";
  const BRANCH = "main";
  const TOKEN_KEY = "gh-pat-my-memory";

  // Debounce: collect multiple clicks before committing
  let pendingChanges = {};
  let commitTimeout = null;
  const DEBOUNCE_MS = 2000; // Wait 2s after last click before committing

  function getToken() {
    return localStorage.getItem(TOKEN_KEY);
  }

  function promptToken() {
    const token = prompt(
      "🔑 Enter your GitHub Fine-Grained PAT for my-memory repo.\n\n" +
        "Create one at: github.com/settings/tokens?type=beta\n" +
        "Scope: Contents (read/write) on AyushSonuu/my-memory only.\n\n" +
        "This is stored in your browser only, never in the repo."
    );
    if (token && token.trim()) {
      localStorage.setItem(TOKEN_KEY, token.trim());
      return token.trim();
    }
    return null;
  }

  function getFilePath() {
    // Convert URL path to file path in repo
    // /my-memory/plans/dsa-tracker/ → plans/dsa-tracker.md
    let path = window.location.pathname;
    // Remove site prefix
    path = path.replace(/^\/my-memory\//, "");
    // Remove trailing slash and index.html
    path = path.replace(/\/?(index\.html)?$/, "");
    // Add .md extension
    if (path && !path.endsWith(".md")) {
      path = path + ".md";
    }
    return path;
  }

  async function fetchFile(filePath, token) {
    const res = await fetch(
      `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${filePath}?ref=${BRANCH}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: "application/vnd.github.v3+json",
        },
      }
    );
    if (!res.ok) {
      throw new Error(`Failed to fetch ${filePath}: ${res.status}`);
    }
    return res.json();
  }

  async function commitFile(filePath, content, sha, token, message) {
    const res = await fetch(
      `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contents/${filePath}`,
      {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: "application/vnd.github.v3+json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: message,
          content: btoa(unescape(encodeURIComponent(content))),
          sha: sha,
          branch: BRANCH,
        }),
      }
    );
    if (!res.ok) {
      const err = await res.json();
      throw new Error(`Commit failed: ${err.message}`);
    }
    return res.json();
  }

  function toggleCheckboxInMarkdown(content, checkboxIndex, checked) {
    // Find all markdown checkboxes: - [ ] or - [x]
    let count = -1;
    return content.replace(/^(\s*-\s*\[)[ xX](\])/gm, (match, prefix, suffix) => {
      count++;
      if (count === checkboxIndex) {
        return prefix + (checked ? "x" : " ") + suffix;
      }
      return match;
    });
  }

  async function flushChanges() {
    const token = getToken();
    if (!token) return;

    const filePath = getFilePath();
    if (!filePath) return;

    // Copy and clear pending
    const changes = { ...pendingChanges };
    pendingChanges = {};

    try {
      // Fetch current file
      const file = await fetchFile(filePath, token);
      let content = decodeURIComponent(escape(atob(file.content.replace(/\n/g, ""))));

      // Apply all pending changes
      const indices = Object.keys(changes)
        .map(Number)
        .sort((a, b) => a - b);
      
      for (const idx of indices) {
        content = toggleCheckboxInMarkdown(content, idx, changes[idx]);
      }

      // Count what changed
      const checked = indices.filter((i) => changes[i]).length;
      const unchecked = indices.length - checked;
      let msg = "✅ tracker: ";
      if (checked > 0) msg += `checked ${checked} item${checked > 1 ? "s" : ""}`;
      if (checked > 0 && unchecked > 0) msg += ", ";
      if (unchecked > 0) msg += `unchecked ${unchecked} item${unchecked > 1 ? "s" : ""}`;

      // Commit
      await commitFile(filePath, content, file.sha, token, msg);

      // Visual feedback
      showToast(`Saved! ${msg.replace("✅ tracker: ", "")}`);
    } catch (err) {
      console.error("Checkbox commit failed:", err);
      showToast("❌ Save failed: " + err.message, true);
      // If auth failed, clear token so user can re-enter
      if (err.message.includes("401") || err.message.includes("403")) {
        localStorage.removeItem(TOKEN_KEY);
      }
    }
  }

  function scheduleCommit() {
    if (commitTimeout) clearTimeout(commitTimeout);
    commitTimeout = setTimeout(flushChanges, DEBOUNCE_MS);
  }

  function showToast(message, isError) {
    // Remove existing toast
    const existing = document.getElementById("cb-toast");
    if (existing) existing.remove();

    const toast = document.createElement("div");
    toast.id = "cb-toast";
    toast.textContent = message;
    toast.style.cssText = `
      position: fixed; bottom: 20px; right: 20px; z-index: 9999;
      padding: 12px 20px; border-radius: 8px; font-size: 14px;
      color: white; font-weight: 500;
      background: ${isError ? "#f44336" : "#4caf50"};
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      transition: opacity 0.3s;
    `;
    document.body.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = "0";
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }

  function init() {
    const checkboxes = document.querySelectorAll(
      '.task-list-control input[type="checkbox"], li.task-list-item input[type="checkbox"]'
    );

    if (checkboxes.length === 0) return;

    checkboxes.forEach((cb, index) => {
      // Make clickable
      cb.disabled = false;
      cb.style.cursor = "pointer";
      cb.style.pointerEvents = "auto";

      cb.addEventListener("change", function () {
        // Ensure token exists
        let token = getToken();
        if (!token) {
          token = promptToken();
          if (!token) {
            // Revert
            cb.checked = !cb.checked;
            return;
          }
        }

        // Visual feedback on parent li
        const li = cb.closest("li");
        if (li) {
          li.style.opacity = cb.checked ? "0.6" : "1";
          li.style.textDecoration = cb.checked ? "line-through" : "none";
        }

        // Queue change
        pendingChanges[index] = cb.checked;
        scheduleCommit();
      });

      // Apply initial styling for checked items
      const li = cb.closest("li");
      if (li && cb.checked) {
        li.style.opacity = "0.6";
        li.style.textDecoration = "line-through";
      }
    });
  }

  // Run on load
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  // MkDocs Material instant navigation
  document.addEventListener("DOMContentSwitch", init);
  if (typeof document$ !== "undefined") {
    document$.subscribe(init);
  }
})();
