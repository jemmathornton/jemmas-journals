/* Jemma’s __NAME__: draws every page from js/data.js. Started from the family template (templates/new-site in Jemma’s Journals).
   A tiny hash router:  #/ Home   #/list the list   #/item/<id> one item   anything else: Not found.
   No inline handlers anywhere (the Content-Security-Policy in index.html runs only this site’s own files).
   The footer, Back to top, Dark mode and the Menu drawer are the family’s shared code (/family/family.js). */
(function () {
  "use strict";
  var SITE = "Jemma’s __NAME__";
  var DATA = window.SITE_DATA || { items: [] };
  var $ = function (s) { return document.querySelector(s); };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };

  // icons: Lucide (ISC licence, js/LICENSE-lucide.txt); add more from lucide.dev as the site needs them
  var ICONS = {
    home: '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    list: '<path d="M3 12h.01"/><path d="M3 18h.01"/><path d="M3 6h.01"/><path d="M8 12h13"/><path d="M8 18h13"/><path d="M8 6h13"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
  };
  function icon(n) { return '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' + ICONS[n] + "</svg>"; }
  // a marked placeholder (her rule: nothing made-up passes for her words)
  var TAG = '<span class="ph-tag">Placeholder</span>';
  // the badge is joined to the last word (a no-break space), so on a phone it never sits alone on its own line
  function words(text, missing) { return text ? "<p>" + esc(text) + "</p>" : '<p class="ph">' + esc(missing) + "&nbsp;" + TAG + "</p>"; }
  var MISSING = "Words about this go here.";   // one neutral voice for every placeholder line
  function head(title, kicker) { return '<header class="page-head">' + (kicker ? '<div class="kicker">' + kicker + "</div>" : "") + "<h1>" + title + "</h1></header>"; }
  function find(id) { return DATA.items.filter(function (i) { return i.id === id; })[0]; }

  /* ---------- the pages ---------- */
  function pageHome() {
    return head("Jemma’s <em>__NAME__</em>")
      + '<section class="sec" aria-labelledby="h-intro"><h2 id="h-intro">Introduction</h2>'
      + words(DATA.intro, "An introduction to the site goes here.") + "</section>"
      + '<section class="sec" aria-labelledby="h-contents"><h2 id="h-contents">Contents</h2>'
      + '<a class="go" href="#/list">Open ' + esc(DATA.listTitle || "the list") + " " + icon("arrow-right") + "</a></section>";
  }
  function card(item) {
    return '<li class="card"><h3><a href="#/item/' + encodeURIComponent(item.id) + '">' + esc(item.title) + "</a>" + (item.placeholder && item.about ? "&nbsp;" + TAG : "") + "</h3>"   // one badge per card
      + words(item.about, MISSING) + "</li>";
  }
  function pageList() {
    return head(esc(DATA.listTitle || "List"))
      + (DATA.items.length ? '<ul class="cards">' + DATA.items.map(card).join("") + "</ul>" : '<p class="ph">Nothing here yet.&nbsp;' + TAG + "</p>");
  }
  function pageItem(item) {
    return '<nav class="crumbs" aria-label="Breadcrumb"><a href="#/list">' + esc(DATA.listTitle || "List") + "</a> / " + esc(item.title) + "</nav>"
      + head(esc(item.title) + (item.placeholder && item.about ? "&nbsp;" + TAG : ""))
      + '<div class="panel">' + words(item.about, MISSING) + "</div>";
  }
  function notFound() {
    return head("Not found") + '<p>There’s no page at this address. <a href="#/">Go to the home page</a>.</p>';
  }

  /* ---------- the sidebar ---------- */
  function nav(r) {
    var item = function (href, ic, label, on) { return '<a href="' + href + '"' + (on ? ' class="cur" aria-current="page"' : "") + ">" + icon(ic) + "<span>" + esc(label) + "</span></a>"; };
    return item("#/", "home", "Home", r === "") + item("#/list", "list", DATA.listTitle || "List", r === "list" || r === "item");
  }

  /* ---------- the router ---------- */
  // the address split into its parts; null if it can’t be read (a broken % code), which shows Not found
  function routeOf(hash) {
    try { return hash.replace(/^#\/?/, "").split("/").filter(Boolean).map(decodeURIComponent); } catch (e) { return null; }
  }
  function render() {
    var read = routeOf(location.hash), route = read || [], r = route[0] || "", html, found = true, item;
    if (!read) found = false;
    else if (!r && route.length === 0) html = pageHome();
    else if (r === "list" && route.length === 1) html = pageList();
    else if (r === "item" && route.length === 2 && (item = find(route[1]))) html = pageItem(item);
    else found = false;
    if (!found) html = notFound();
    $("#view").innerHTML = html;
    $("#nav").innerHTML = nav(found ? r : null);
    document.body.setAttribute("data-page", found ? r || "home" : "notfound");
    if (drawer) drawer.close("silent");   // a link in the drawer: it closes, and focus goes to the page just below
    if (render.done) $("#view").focus({ preventScroll: true });   // after a click, keyboard and screen readers start at the new page
    render.done = true;
    var h1 = $("#view h1");
    document.title = (r || !found) && h1 ? h1.textContent.replace("Placeholder", "").trim() + " · " + SITE : SITE;
    window.scrollTo(0, 0);
  }

  /* ---------- the family’s shared code ---------- */
  var drawer = null;
  function startFamily() {   // the Menu drawer at 900px and below (family.js is deferred, so this waits for it)
    if (drawer || !window.JJFamily) return;
    drawer = JJFamily.menu({
      button: $("#menuBtn"), drawer: $("#side"), scrim: $("#scrim"),
      outside: function () { return [$("#main"), $("#topbar"), $(".skip")]; },
      current: function () { return $("#nav a.cur") || $('#nav a[href="#/"]'); },
      main: function () { return $("#view"); },
    });
  }
  document.addEventListener("DOMContentLoaded", startFamily);
  // opened as a file on her PC, /family/ isn’t there: load it from Jemma’s Journals beside this folder instead
  if (location.protocol === "file:" && !window.JJFamily) {
    var css = document.createElement("link"); css.rel = "stylesheet"; css.href = "../../site/family/family.css";
    document.querySelector('link[href^="site.css"]').before(css);
    var mode = document.createElement("script"); mode.src = "../../site/family/mode.js"; mode.async = false;
    var js = document.createElement("script"); js.src = "../../site/family/family.js"; js.async = false; js.onload = startFamily;
    document.head.append(mode, js);
    $(".home-link").setAttribute("href", "../../site/index.html");
  }
  $(".skip").addEventListener("click", function (e) { e.preventDefault(); $("#view").focus(); });
  window.addEventListener("hashchange", render);
  render();
})();
