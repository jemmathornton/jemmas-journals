/* Jemma’s Journals family: the parts every site shares (research/family-rules.md). One copy, here in Jemma’s Journals;
   every site loads it as  <script src="/family/family.js" defer></script>  (after /family/mode.js in <head>).
   Each site keeps its own look: this file only does the behaviour, and family.css the shared layout (colours come from the site).

   What it does, by markup (works for pages drawn later too):
     <button data-jj-mode></button>             the Dark mode / Light mode button (moon or sun icon, aria-pressed)
     <a href="#top" data-jj-top>…</a>           Back to top: scrolls up and moves keyboard focus to #top
                                                (or to the element named in data-jj-top="#somewhere")
     <p data-jj-line1></p>                       footer line 1, the same words on every site
     <p data-jj-credits>…</p>                    the credits: a “·” never starts or ends a line (it is hidden where the line breaks)
     <meta name="theme-color" content="#light" data-dark="#dark">   the phone bar follows the mode
     <link rel="icon" href="…" data-dark="…">    the tab icon follows the mode (where a site has a dark one)

   And for the Menu drawer on narrow screens (sites with a sidebar):
     JJFamily.menu({button, drawer, scrim, outside: [...], current: () => element, main: element})
   See README.md next to this file. */
(function () {
  "use strict";
  var root = document.documentElement;
  var LINE1 = "No cookies, no tracking, no ads. Made with HTML, CSS and JavaScript, kept on GitHub.";
  var SVG = function (paths) { return '<svg class="jj-i" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' + paths + "</svg>"; };
  var ICON = {   // Lucide
    moon: SVG('<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>'),
    sun: SVG('<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>'),
    up: SVG('<path d="m5 12 7-7 7 7"/><path d="M12 19V5"/>'),
    menu: SVG('<path d="M4 12h16"/><path d="M4 6h16"/><path d="M4 18h16"/>')
  };
  var changeListeners = [];

  /* ---------- dark mode (section 1) ---------- */
  function getMode() { return root.getAttribute("data-mode") === "dark" ? "dark" : "light"; }
  function setMode(m) {
    m = m === "dark" ? "dark" : "light";
    root.setAttribute("data-mode", m);
    try { localStorage.setItem("jj-mode", m); } catch (e) {}
    if (root.hasAttribute("data-jj-server-mode")) {   // on her PC: the family server keeps it for every app window
      root.setAttribute("data-jj-server-mode", m);
      try { fetch("/family/mode", { method: "POST", headers: { "X-Family": "1", "Content-Type": "text/plain" }, body: m, keepalive: true }); } catch (e) {}
    }
    paint(true);
    changeListeners.forEach(function (f) { try { f(m); } catch (e) {} });
  }
  function chrome() {
    var dark = getMode() === "dark";
    var tc = document.querySelector('meta[name="theme-color"]');
    if (tc && tc.hasAttribute("data-dark")) {
      if (!tc.hasAttribute("data-light")) tc.setAttribute("data-light", tc.getAttribute("content"));
      tc.setAttribute("content", tc.getAttribute(dark ? "data-dark" : "data-light"));
    }
    document.querySelectorAll('link[rel~="icon"][data-dark], link[rel="apple-touch-icon"][data-dark]').forEach(function (l) {
      if (!l.hasAttribute("data-light")) l.setAttribute("data-light", l.getAttribute("href"));
      var want = l.getAttribute(dark ? "data-dark" : "data-light");
      if (l.getAttribute("href") !== want) l.setAttribute("href", want);
    });
  }

  /* ---------- painting the shared bits (idempotent, so it can run after any redraw) ---------- */
  function paint(force) {
    var mode = getMode();
    chrome();
    document.querySelectorAll("[data-jj-mode]").forEach(function (b) {
      if (!force && b.getAttribute("data-jj-painted") === mode) return;
      var dark = mode === "dark";
      b.innerHTML = (dark ? ICON.sun : ICON.moon) + "<span>" + (dark ? "Light mode" : "Dark mode") + "</span>";
      b.setAttribute("aria-pressed", dark ? "true" : "false");
      if (b.tagName === "BUTTON" && !b.hasAttribute("type")) b.setAttribute("type", "button");
      b.setAttribute("data-jj-painted", mode);
    });
    document.querySelectorAll("[data-jj-top]").forEach(function (a) {
      if (a.getAttribute("data-jj-painted")) return;
      if (!a.textContent.trim()) a.innerHTML = ICON.up + "<span>Back to top</span>";
      a.setAttribute("data-jj-painted", "1");
    });
    document.querySelectorAll("[data-jj-line1]").forEach(function (p) {
      if (p.textContent !== LINE1) p.textContent = LINE1;
    });
    fitCredits();
  }

  /* a “·” between credits never starts or ends a line: hide the ones where the line breaks (section 2) */
  function fitCredits() {
    document.querySelectorAll("[data-jj-credits] .dot, [data-jj-credits] .jj-dot").forEach(function (d) {
      var a = d.previousElementSibling, b = d.nextElementSibling;
      d.style.visibility = "";
      if (!a || !b || !d.offsetParent) return;
      var ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect();
      if (Math.abs(ra.top - rb.top) > 2) d.style.visibility = "hidden";
    });
  }

  /* ---------- clicks: Dark mode and Back to top ---------- */
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("[data-jj-mode]");
    if (b) {
      e.preventDefault();
      setMode(getMode() === "dark" ? "light" : "dark");
      var again = document.querySelector("[data-jj-mode]");   // a site may redraw on change: keep focus on the button
      if (again && document.activeElement !== again && (document.activeElement === document.body || !document.contains(b))) again.focus();
      return;
    }
    var t = e.target.closest && e.target.closest("[data-jj-top]");
    if (t) {
      e.preventDefault();
      var sel = t.getAttribute("data-jj-top") || t.getAttribute("href") || "#top";
      var target = (sel && sel.charAt(0) === "#" && sel.length > 1 && document.querySelector(sel)) || document.getElementById("top");
      window.scrollTo(0, 0);
      if (target) {
        if (!target.hasAttribute("tabindex") && !/^(A|BUTTON|INPUT|SELECT|TEXTAREA)$/.test(target.tagName)) target.setAttribute("tabindex", "-1");
        target.focus({ preventScroll: true });
      }
    }
  });

  /* ---------- the Menu drawer on narrow screens (section 3) ---------- */
  function menu(o) {
    var button = o.button, drawer = o.drawer, scrim = o.scrim;
    if (!button || !drawer) return null;
    if (drawer._jjMenu) return drawer._jjMenu;   // set up once: a second call returns the first (round 4: two would open and close at once)
    var narrow = window.matchMedia("(max-width: " + (o.breakpoint || 900) + "px)");
    var isOpen = false;
    var outside = function () { return (typeof o.outside === "function" ? o.outside() : o.outside || []).filter(Boolean); };
    if (!drawer.id) drawer.id = "jj-drawer";
    button.setAttribute("aria-controls", drawer.id);
    button.setAttribute("aria-expanded", "false");
    if (!button.innerHTML.trim()) button.innerHTML = ICON.menu + "<span>Menu</span>";

    function setInert() {
      var small = narrow.matches;
      drawer.inert = small && !isOpen;
      outside().forEach(function (el) { el.inert = small && isOpen; });
    }
    function focusInDrawer() {
      var cur = (o.current && o.current()) || drawer.querySelector('[aria-current="page"]') || drawer.querySelector('a[href="#home"], a[href="#/"], a[href="./"], a[href="#"]') || drawer.querySelector("a[href]:not([data-jj-home])") || drawer.querySelector("a[href]");
      if (cur) cur.focus({ preventScroll: false });
    }
    function open() {
      if (isOpen || !narrow.matches) return;
      isOpen = true;
      root.classList.add("jj-menu-open");
      drawer.classList.add("jj-open");
      if (scrim) scrim.hidden = false;
      button.setAttribute("aria-expanded", "true");
      setInert();
      focusInDrawer();
      if (o.onChange) o.onChange(true);
    }
    function close(how) {
      if (!isOpen) return;
      isOpen = false;
      root.classList.remove("jj-menu-open");
      drawer.classList.remove("jj-open");
      if (scrim) scrim.hidden = true;
      button.setAttribute("aria-expanded", "false");
      setInert();
      if (how === "link") {
        setTimeout(function () { var m = typeof o.main === "function" ? o.main() : o.main; if (m) { if (!m.hasAttribute("tabindex")) m.setAttribute("tabindex", "-1"); m.focus({ preventScroll: true }); } }, 0);
      } else if (how !== "silent") button.focus();
      if (o.onChange) o.onChange(false);
    }
    button.addEventListener("click", function () { isOpen ? close() : open(); });
    if (scrim) { scrim.hidden = true; scrim.addEventListener("click", function () { close(); }); }
    drawer.addEventListener("click", function (e) { var a = e.target.closest("a[href]"); if (a && isOpen) close("link"); });
    document.addEventListener("keydown", function (e) {
      if (!isOpen) return;
      if (e.key === "Escape") { e.preventDefault(); close(); return; }
      if (e.key !== "Tab") return;
      // Tab and Shift+Tab go round the drawer's own links and never reach the page or the browser bar (round 4: one lap reached the body)
      var items = Array.prototype.filter.call(drawer.querySelectorAll('a[href], button:not([disabled]), input:not([disabled]), select, textarea, [tabindex]:not([tabindex="-1"])'),
        function (el) { return el.offsetParent !== null || el.getClientRects().length; });
      if (!items.length) return;
      var first = items[0], last = items[items.length - 1], at = document.activeElement;
      if (e.shiftKey && (at === first || !drawer.contains(at))) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && (at === last || !drawer.contains(at))) { e.preventDefault(); first.focus(); }
    });
    function onWidth() {
      var hadFocus = drawer.contains(document.activeElement);
      if (!narrow.matches && isOpen) close("silent");
      setInert();
      if (narrow.matches && hadFocus && !isOpen) button.focus();
    }
    if (narrow.addEventListener) narrow.addEventListener("change", onWidth); else narrow.addListener(onWidth);
    setInert();
    drawer._jjMenu = { open: open, close: close, isOpen: function () { return isOpen; }, refresh: setInert };
    return drawer._jjMenu;
  }

  /* ---------- start ---------- */
  window.JJFamily = {
    LINE1: LINE1, ICON: ICON,
    mode: { get: getMode, set: setMode, toggle: function () { setMode(getMode() === "dark" ? "light" : "dark"); }, onChange: function (f) { changeListeners.push(f); } },
    paint: paint, fitCredits: fitCredits, menu: menu
  };
  if (!root.hasAttribute("data-mode")) root.setAttribute("data-mode", "light");   // if a page forgot mode.js
  function start() {
    paint(true);
    var queued = false;
    new MutationObserver(function () { if (queued) return; queued = true; requestAnimationFrame(function () { queued = false; paint(false); }); })
      .observe(document.body, { childList: true, subtree: true });
    var rt; window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(fitCredits, 100); });
    // another tab or window of the same browser changed the mode: follow it straight away (round 3 review)
    window.addEventListener("storage", function (e) {
      if (e.key !== "jj-mode" || (e.newValue !== "dark" && e.newValue !== "light") || e.newValue === getMode()) return;
      root.setAttribute("data-mode", e.newValue);
      if (root.hasAttribute("data-jj-server-mode")) root.setAttribute("data-jj-server-mode", e.newValue);
      paint(true);
      changeListeners.forEach(function (f) { try { f(e.newValue); } catch (x) {} });
    });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitCredits);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
