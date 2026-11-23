# The family’s shared code

The one copy of what every site shares (her decision, 21 Nov 2026: Jemma’s Journals is the parent and holds the shared code; the apps are submodules that use it). The rules it carries out are in `research/family-rules.md`.

Every site loads it **from Jemma’s Journals directly**, at `/family/…` (her choice, 21 Nov): online all sites share one address, and on her PC `tools/serve_all.py` (http://localhost:8050) serves the family the same way. Each app’s own server (Library 8020, Pokédex 8030, Travels 8041) also serves `/family/` from here, and each app’s test server does too.

| File | Loaded | Does |
|---|---|---|
| `mode.js` | `<script src="/family/mode.js" data-old-key="…">` in `<head>`, before the stylesheet | sets `data-mode` before the page draws, from the shared `jj-mode`; on her PC the family server’s choice (`data-jj-server-mode` on `<html>`, from `logs/family-mode.txt`) wins. Until family.js has drawn them, it gives the empty Back to top and Dark mode controls a stand-in `aria-label`, so they are never nameless on a slow load (23 Nov) |
| `family.css` | `<link rel="stylesheet" href="/family/family.css">` before the site’s own stylesheet | footer layout, drawer scrim, Menu button and bar-name sizes; colours and fonts from the site’s `--jj-*` variables |
| `family.js` | `<script src="/family/family.js" defer>` | Dark mode button, theme colour and tab icon, Back to top, footer line 1, credit dots, the Menu drawer (`JJFamily.menu`) |

## The footer markup (every site)

```html
<footer class="jj-foot">
  <b class="jj-name">Jemma’s Library</b>
  <p data-jj-line1></p>
  <p data-jj-credits><span class="cr">Book covers from their publishers</span><span class="dot" aria-hidden="true">&nbsp;·</span> <span class="cr">…</span></p>
  <div class="jj-foot-links"><a href="#top" data-jj-top></a><button data-jj-mode></button></div>
</footer>
```

The no-break space goes **inside** the dot: a “·” never starts a line, and on phones (dots hidden, credits one per line) no empty line is left behind. `family.js` hides any “·” that would end a line.

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

It closes on Escape, a tap on the scrim, choosing a link, or (round 5) **a swipe to the left** on the drawer or scrim: touch only, passive (scrolling the drawer’s list is never held up: the first 10 px decide, and only a mostly sideways move to the left counts), closing when the finger lifts after 50 px (`swipe: 60` in the options to change it). Nothing to add in a site.

**Drawer width:** `min(300px, 86vw)`, the family’s width (round 5: Pokédex, Travels and Sim World use it; Library was 280px).

**The way home in the drawer** (round 5): give the drawer’s “← Jemma’s Journals” link the class `jj-home-link` (and `data-jj-home`, so focus never starts on it):

```html
<a class="home-link jj-home-link" href="/" data-jj-home>← Jemma’s Journals</a>
```

Under 900px it is then at least 44px tall with 12.5px text (a floor that beats the site’s own `.home-link` size); the site keeps its colour, capitals, letter-spacing and margins, and the laptop sidebar is unchanged. The link grows by about 18px, so trim the margin above it or the padding of what follows if the drawer should look the same.

## Safe areas (notch and rounded corners)

Every page has `viewport-fit=cover`, so in phone landscape the page reaches under the notch (about 47px). Add to the element that holds the page’s sides:

| Class | Pads | With |
|---|---|---|
| `jj-safe` | left and right | `max(var(--jj-safe-pad, 0px), env(safe-area-inset-left/right))` |
| `jj-safe-top` | top | `max(var(--jj-safe-pad-top, 0px), env(safe-area-inset-top))` |

Set `--jj-safe-pad` to the gutter the element already has and remove its own `padding-left/right` (these are `:where()`, so a site rule would win). On a laptop `env()` is 0, so only the gutter shows. Sticky bars: `top: env(safe-area-inset-top, 0px)` as well. Home uses `.gut` (the same sum) and pads the cover’s top.

## Changing it

Change it here once; every site follows. Then run every site’s tests (each app’s own suite, and here `tests/check_page.js` and `tests/family/family.test.js`, which checks these rules on all five sites; `python tools/check_all.py --quick` runs the parent’s checks in one go), commit here, and push.
