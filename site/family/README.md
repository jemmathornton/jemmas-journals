# The family’s shared code

The one copy of what every site shares (her decision, 21 Nov 2026: Jemma’s Journals is the parent and holds the shared code; the apps are submodules that use it). The rules it carries out are in `research/family-rules.md`.

Every site loads it **from Jemma’s Journals directly**, at `/family/…` (her choice, 21 Nov): online all sites share one address, and on her PC `tools/serve_all.py` (http://localhost:8050) serves the family the same way. Each app’s own server (Library 8020, Pokédex 8030, Travels 8041) also serves `/family/` from here, and each app’s test server does too.

| File | Loaded | Does |
|---|---|---|
| `mode.js` | `<script src="/family/mode.js" data-old-key="…">` in `<head>`, before the stylesheet | sets `data-mode` before the page draws, from the shared `jj-mode` |
| `family.css` | `<link rel="stylesheet" href="/family/family.css">` before the site’s own stylesheet | footer layout, drawer scrim, Menu button and bar-name sizes; colours and fonts from the site’s `--jj-*` variables |
| `family.js` | `<script src="/family/family.js" defer>` | Dark mode button, theme colour and tab icon, Back to top, footer line 1, credit dots, the Menu drawer (`JJFamily.menu`) |

## The footer markup (every site)

```html
<footer class="jj-foot">
  <b class="jj-name">Jemma’s Library</b>
  <p data-jj-line1></p>
  <p data-jj-credits><span class="cr">Book covers from their publishers</span>&nbsp;<span class="dot" aria-hidden="true">·</span> <span class="cr">…</span></p>
  <div class="jj-foot-links"><a href="#top" data-jj-top></a><button data-jj-mode></button></div>
</footer>
```

## The Menu drawer (sites with a sidebar)

```js
JJFamily.menu({
  button: document.querySelector(".menu-btn"),     // gets aria-controls/aria-expanded; the Lucide menu icon + “Menu” if empty
  drawer: document.querySelector("#nav"),          // the sidebar; inert while closed on narrow screens
  scrim:  document.querySelector(".jj-scrim"),     // black at 45%; tap closes
  outside: () => [topBar, skipLink, main],         // inert while open, so Tab stays in the drawer
  current: () => drawer.querySelector(".cur"),     // focused on opening (Home if none)
  main: () => document.querySelector("main"),      // focused after choosing a link
});
```

The site styles its own bar and drawer (position, slide, colours); `html.jj-menu-open` and `.jj-open` on the drawer say when it is open.

## Changing it

Change it here once; every site follows. Then run every site’s tests (each app’s own suite, and `tests/check_page.js` here), commit here, and push.
