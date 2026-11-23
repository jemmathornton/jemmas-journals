/* Jemma’s Journals family: dark mode, set before the page draws (research/family-rules.md, section 1).
   One copy for every site; each site loads it in <head>, before its stylesheet:

     <script src="/family/mode.js" data-old-key="jsw-mode"></script>

   - Every site opens light; dark only once she has pressed Dark mode on any of them (localStorage "jj-mode", shared by all).
   - data-old-key (optional): the site's own key from before the family rules, read once if "jj-mode" is missing, then removed.
   - Sets data-mode="light" or "dark" on <html>; every site's dark styles hang off :root[data-mode="dark"].
   - If storage is blocked, light.
   - On her PC the family server (tools/serve_all.py) writes her choice into the page as <html data-jj-server-mode="…">,
     so it carries between app windows that have their own Chrome profiles; that wins when it is there. */
(function () {
  var root = document.documentElement, me = document.currentScript, mode = "light";
  try {
    var server = root.getAttribute("data-jj-server-mode");
    if (server === "dark" || server === "light") { try { localStorage.setItem("jj-mode", server); } catch (e) {} }
    var saved = localStorage.getItem("jj-mode"), old = me && me.getAttribute("data-old-key");
    if (server === "dark" || server === "light") saved = server;
    if (saved !== "dark" && saved !== "light" && old) {
      var o = localStorage.getItem(old);
      if (o === "dark" || o === "light") { saved = o; localStorage.setItem("jj-mode", o); }
    }
    if (old) localStorage.removeItem(old);
    if (saved === "dark") mode = "dark";
  } catch (e) {}
  root.setAttribute("data-mode", mode);

  // Until family.js (deferred) has drawn them, the footer's Back to top and Dark mode controls are empty in the page's HTML;
  // on a slow load a screen reader (or axe) met them with no name (23 Nov, Sim World review). Give each a name as soon as it is
  // parsed; family.js takes it off again when it writes the words in.
  if (document.readyState !== "loading" || !window.MutationObserver) return;
  function name() {
    var els = document.querySelectorAll("[data-jj-mode]:not([data-jj-painted]):not([aria-label]), [data-jj-top]:not([data-jj-painted]):not([aria-label])");
    for (var i = 0; i < els.length; i++) {
      if (els[i].textContent.trim()) continue;
      var isMode = els[i].hasAttribute("data-jj-mode");
      els[i].setAttribute("aria-label", isMode ? (mode === "dark" ? "Light mode" : "Dark mode") : "Back to top");
      if (isMode) els[i].setAttribute("aria-pressed", mode === "dark" ? "true" : "false");
      els[i].setAttribute("data-jj-prelabel", "");
    }
  }
  var watch = new MutationObserver(name);
  watch.observe(root, { childList: true, subtree: true });
  document.addEventListener("DOMContentLoaded", function () { name(); watch.disconnect(); });
})();
