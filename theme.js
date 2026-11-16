// Applies a saved light/dark choice before first paint. Without a saved choice the site follows the system.
(function () {
  try {
    // ?theme=light|dark previews a theme for this view only (not saved).
    var q = new URLSearchParams(location.search).get("theme");
    if (q === "light" || q === "dark") { document.documentElement.setAttribute("data-theme", q); return; }
    var t = localStorage.getItem("theme");
    if (t === "light" || t === "dark") document.documentElement.setAttribute("data-theme", t);
  } catch (e) { /* storage blocked: follow the system */ }
})();
