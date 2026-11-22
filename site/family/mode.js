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
})();
