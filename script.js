// Theme toggle and mobile menu. Everything works without JavaScript (the menu just stays visible on wide screens).
(function () {
  var root = document.documentElement;

  // One toggle in the header bar, one inside the menu on narrow phones; both flip the same theme.
  var toggles = document.querySelectorAll(".theme-toggle");
  function isDark() {
    return (root.getAttribute("data-theme") ||
      (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light")) === "dark";
  }
  function sync() { toggles.forEach(function (t) { t.setAttribute("aria-pressed", String(isDark())); }); }
  toggles.forEach(function (toggle) {
    toggle.addEventListener("click", function () {
      var next = isDark() ? "light" : "dark";
      root.setAttribute("data-theme", next);
      sync();
      try { localStorage.setItem("theme", next); } catch (e) { /* not saved; fine */ }
    });
  });
  sync();

  var menuBtn = document.querySelector(".menu-btn");
  var nav = document.getElementById("site-nav");
  if (menuBtn && nav) {
    menuBtn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) {
        nav.classList.remove("open");
        menuBtn.setAttribute("aria-expanded", "false");
        menuBtn.focus();
      }
    });
  }
})();
