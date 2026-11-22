# Review, round 3: Jemma’s Pokédex (22 Nov 2026)

Read-only review of `Documents\JemmasJournals\pokedex` at eba32a1 (the move into Jemma’s Journals, her 21 Nov picks: tabs in one row at 1280, Hide off on opening, search ignores Hide, card art tinted by first type, Lucky box white, Try switch removed). Nothing in any repo was edited, built, staged or committed: `git status` was clean in the parent and in `pokedex` before and after. Her ticks file `data/collection/go.json` has the same SHA-256 before and after (c294d8f3…), and the old `Documents\Pokedex` copy has the same hash too.

**How it was checked.** Her real server at http://localhost:8030 and the family server at http://localhost:8050/pokedex/, in Edge through Playwright. Every non-GET request and every `/api/` call except reading the collection was answered by the test harness with a 503 and never reached a server. Two POSTs were tried on purpose to test the error path, and both were blocked. Light runs had the **device set to dark**, to prove the site still opens light; dark runs had `jj-mode=dark` in storage. Sizes: 1600×930, 1584, 1280, 1000, 901, 899 and 390, each in light and dark, which made 656 page loads. Pages: Home, Every Pokémon, all ten regions, Event Pokémon and four set pages, Looking for (every tab), What’s on, Fast tick (Pokédex, Costumes, Backgrounds, Forms check), 17 Pokémon pages (including Charizard, Pikachu, Unown, Rotom, Vivillon, Eevee, Pumpkaboo, Mewtwo, Mew, Hisuian Growlithe, Paldean Tauros, Toxtricity, Urshifu and #1012), `#nope` and `#p-9999`, and searches for “pika”, “25”, “farfetch’d” and “zzzz”. Then separate runs for the drawer, the tabs as the filter, the mode, keyboard focus, the footer, tab sizes across every region, a width scan from 1600 down to 340 in 20px steps, and the 8030 and 8050 addresses side by side.

Scripts and data: `scratchpad\review3\` (`sweep.js`, `inter3.js`, `inter3.json`, `refused.js`, `pokedex\report-*.json`). Screenshots: `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review3\pokedex\`.

## What is now right (checked)

- **Both addresses read her ticks.** On 8030 the page asks for `api/collection` and on 8050 for `/pokedex/api/collection`. Both get 1,491 keys, `readOnly` is false and Kanto shows 151 of 151. A save that fails rolls back and shows “Not saved: the Pokédex server isn’t answering…”, with no error left on the page. `/pokedex` without the slash redirects (301) to `/pokedex/`. “← Jemma’s Journals” goes to `localhost:8030/` (the Pokédex itself) on 8030 and to `localhost:8050/` (home) on 8050, as intended.
- **Banner tabs.** There is one row at 1600, 1584 and 1280. At 1280 the writing is exactly 8.5px and the tabs are 71px wide, the same on Every Pokémon and all ten regions. At 1600 and 1584 the writing is 10.5px. Below that there are even rows: 7 + 6 at 1000, 901 and 899, and four rows on a phone, at 10px. No label is cut at any size or on any region, and no tab row scrolls sideways. Size and width are identical across regions at every width; regions with 12 or 11 tabs just leave the end of the row empty.
- **32px under the chips** on every Pokémon page, at every size and in both modes (360 of 360 measurements).
- **Card art** is tinted by the first type through `data-t1` on cards and on the Pokémon page’s picture. The frame keeps the region colour. Background cards don’t carry `data-t1`, which is right, since their art is the location card.
- **Lucky box:** white text on #D09B00 everywhere.
- **The Try switch** is gone from the page, CSS and JS (no `.trybox`, `data-try` or `jemmas-pokedex-try` in the code), and a test checks it.
- **Hide ones I have** is off on opening even when the stored preference was “need”. A tab turns it on, as designed. **A search hides the switch and ignores it.** With Kanto, the Lucky tab and Hide on, “pika” shows Pikachu. (See Should fix 2 for what the tab still does to a search.)
- **No sideways scrolling** at any width from 1600 to 340 on Home, Kanto, Charizard, Unown, Event Pokémon, What’s on, Looking for and Fast tick. The footer overflow from round 2 is fixed.
- **Clean:** no console errors (except the refused connections in Polish 6), no “undefined” or “NaN”, no straight apostrophes in the text shown, no US spellings, and no card label or tab label cut. Each word is the same size on every card. No external requests at all, and the fonts are local.
- **Fixes from round 2 held:** footer overflow (Broken 1); tabs at 1280 (Should fix 3); fractional tab cuts (4); the evolution family stacks on narrow pages (Polish 5: no overflow at 390 or 901); a scrim tap returns focus to Menu (Polish 6); `fitLabels` notes; and Hide/search (questions 2 and 3, now her answers).

---

## Broken

### 1. The shortcut in the Pokédex folder still starts the OLD copy, which would save her ticks to the wrong place
- **Where:** `pokedex\Jemma’s Pokédex.lnk`. It is tracked in git, so it moved with the repo.
- **What:** its target is `pythonw "C:\Users\Jemma\Documents\Pokedex\tools\open_app.pyw"`, with working folder `Documents\Pokedex` and icon `Documents\Pokedex\site\app-v1.ico`. The Desktop and Start menu shortcuts are correct, and point at `JemmasJournals\pokedex`. The weekly backup task points at the new folder too. While her server is already running, the old shortcut only opens the window, so it looks fine. But after a restart, if she opens the app from this folder shortcut first, the old `open_app.pyw` starts the **old** `Documents\Pokedex\tools\serve.py` on 8030. Her ticks then go to `Documents\Pokedex\data\collection\go.json`, which the weekly backup never commits. The new copy wouldn’t see them, and once the old server holds port 8030 the new one can’t start (`allow_reuse_address = False`).
- **Evidence:** a read-only shortcut listing in PowerShell (WScript.Shell `CreateShortcut(...).TargetPath`). The two go.json files are identical today.
- **Fix:** run `tools\make_shortcuts.ps1` from the new folder (it remakes the Desktop, Start menu and project-folder shortcuts), then commit the new `.lnk`. Better still, stop tracking the `.lnk`: it holds an absolute path, so it breaks whenever the folder moves. Until the old folder is deleted, it could also get a note or have its `tools\open_app.pyw` disabled, but only with her yes, since that is her folder.

## Should fix

### 2. With a tab on, a search still filters by that tab, so a search can “lose” the Pokémon it names
- **What:** `dexPage` (app.js 534) still applies `boxFilter(e, "all")`, so a search only lists Pokémon the chosen tab applies to. With the Lucky tab on, “mew” shows only Mewtwo, because Mew can’t be Lucky. The same logic means “zacian” with the Dynamax tab gives “Nothing here”. Her answer on 21 Nov was that a search shows everything that matches. The switch is now ignored, but the tab isn’t, and the page doesn’t say why something is missing.
- **Evidence:** `inter3.json` → `hide.searchMew` (Lucky tab: 1 card, Mewtwo).
- **Fix:** for a search, skip the tab’s `applies` test (keep the tab only for which boxes the cards show), or show a line such as “Only Pokémon that can be Lucky: Clear to see all” (wording would be my suggestion, not decided). This is her call, so put it on her list.

### 3. The footer’s icon credit still leaves out Tabler
- **What:** the Dynamax and Gigantamax icons are Tabler’s `arrow-big-up-line` and `arrow-big-up-lines` (icons.js 51–52; LICENSE-lucide.txt 39–40; her pick 12 Nov). Line 2 says “Icons by Lucide, Phosphor, MingCute and Solar (480 Design)”. The round-2 fix added MingCute and Solar but not Tabler, and the test pins the wrong text (`tests/e2e/site.test.js` 955), so it will fail when this is fixed. The family rule is “only that site’s real credits”.
- **Fix:** “Icons by Lucide, Phosphor, Tabler, MingCute and Solar (480 Design)” in `index.html` 37 and the test.

### 4. Family footer line 1 and the server (tell her, don’t change the words)
“Made with HTML, CSS and JavaScript, kept on GitHub” is true of the page. But the Pokédex also needs its Python server to save ticks. The family rule says that if a site isn’t true to line 1, tell her rather than changing the words. This is just to note, for her to decide.

## Polish

### 5. Small dead code and leftovers (code quality)
- **Quick add CSS** remains (site.css 601–606: `.qlist`, `.qprob`), though the page was removed on 19 Nov. Nothing uses it.
- **The scenery trial:** `REGION_SHOTS`, `PIXEL_SHOTS` (all scenery names), `shotPick` and the “Try a picture” switch markup (app.js 324–357), plus the `data-shotg` click handler (1406). This code can’t run, because every region has a `REGION_CHOSEN` map. The scenery files in `site/regions/` that only it used could go too, if she agrees.
- **`heroArt()`** (app.js 359–367) builds up to 14 parade `<img>`s on every region and Every Pokémon page, which CSS then hides (`.hero.withshot .heroart{display:none}`, site.css 612). They never load, because they are lazy and hidden, but they are dead markup.
- **`ph-butterfly`** is still in icons.js 38 and unused. LICENSE-lucide.txt 19 still says it is the Dynamax icon.
- **Stale comments:** app.js 389–390 says a card label “then drops its icon” (it never does, her rule); 549–550 still describes a “Not caught” toggle; 135 says “Still need / Have / All”.
- **Her browser:** the removed Try switch’s `localStorage` key `jemmas-pokedex-try` is never removed (harmless).

### 6. The server refuses connections under heavy load
During the sweep, about 20 of 656 page loads had some pictures fail with `ERR_CONNECTION_REFUSED` from 8030. That happened while other checks were also running (`report-*.json` → `failed`). One window on its own loaded Hoenn, Galar, Paldea and Event Pokémon (619 requests) with no refusals on either address (`refused.js`). The cause: `serve.py` uses `ThreadingHTTPServer` with Python’s default listen queue of 5, and HTTP/1.0, so each picture is a new connection (1,842 sockets were left in TIME_WAIT after the run). It is unlikely with her one window. A possible fix: `request_queue_size = 64` on `Server` and `protocol_version = "HTTP/1.1"` on `Handler`.

### 7. Unchanged from round 2 (still true)
- Cards in a row are still different heights (`.grid{align-items:start}`, site.css 222: 8 heights among Kanto’s first 60).
- Phone tap targets under 24px: the “Hide ones I have” switch, “× Clear” and the card name links.
- Form picker names are cut with “…” at every width (“Paldean Combat”, “Archipelago”, “Single Strike”).
- Fast tick → Backgrounds clips long names at three lines.
- Bar names on What’s on are shortened with “…”.
- White on the Lucky gold box is 2.5:1 and on the Shiny grey 3.65:1 (her white-text rule; a deeper shade is the only lever).

### 8. Smaller things
- **No not-found page:** `#nope` and `#p-9999` quietly show Home, with nothing lit in the sidebar and the odd address kept.
- **A search typed on a region page** keeps that region’s address and lights it in the sidebar while the page shows the search (“Search · 1 shown”).
- **The sidebar search box** has `outline:none`. Its focus shows only as a 1px gold border (site.css 171–173), the one control without the 2px ring.
- **The mode doesn’t follow another tab:** there is no `storage` listener, so a second tab only follows after a reload. Worth adding in the shared code (below).

## Looks (list only, for her)

- At 1000, 901 and 899 the tabs sit in two rows (7 + 6), so the second row covers more of the region map. At 1000 in dark, the top of Kanto’s map shows a white haze (`gen-1_1000_dark.jpg`).
- In dark mode the type tint in the art window is quite muted on dark card stock (brownish on Charizard): `p-6_1600_dark.jpg`.
- Uncaught background cards in dark have pale grey serif names that read as faded, which is intended: `footer_390_dark.jpg`.
- Home still says “Pokémon data from the game, checked 18 November 2026” (a date on the app’s Home; fine for an app, just noting it).

## Family rules

| Rule | Pokédex |
|---|---|
| Opens light whatever the device says | Yes (device dark → `data-mode="light"`) |
| Footer button Dark mode ⇄ Light mode, moon/sun, `aria-pressed` | Yes |
| `jj-mode` saved, kept on reload; old `jemmas-pokedex-mode` moved once and removed | Yes |
| No flash: `<head>` script sets `data-mode` before CSS | Yes (index.html 17) |
| `theme-color` swaps (#7A1E2A / #4E1018) | Yes (it has no dark tab icon, so there is nothing to swap) |
| Storage blocked → light, button still works, no errors | Yes |
| Footer: name 24px Instrument Serif plain; line 1 exact; credits; buttons | Yes; line 1 is word for word. Credits: Tabler missing (Should fix 3) |
| Credits `credit&nbsp;· credit`, `text-wrap:balance`, no dot at a line’s end; stacked on phones | Yes |
| 12.5px text, ≥4.5:1, both buttons 44px and level | Yes (both modes, 1600 and 390) |
| Back to top scrolls up and focuses the page | Yes (`#view`) |
| Menu bar ≤900px, sidebar at 901 | Yes (900 has the bar, 901 doesn’t) |
| Menu 44px, bar name 26px, scrim 45% | Yes |
| Opening focuses this page’s link (Home if none), never “← Jemma’s Journals” | Yes: Johto on Johto, Kanto on Pikachu, Hisui on Hisuian Growlithe, Fast tick, Event Pokémon, Home on `#nope` |
| While open: top bar and main inert; Tab trapped (30 presses) | Yes |
| Esc, scrim and link close; focus back to Menu (link → page) | Yes, all three |
| Closed drawer inert; resetting when crossing 900px | Yes |
| Page behind doesn’t scroll | Yes |
| robots `noindex, noai, noimageai` | Yes |
| Local fonts, no external requests | Yes (no requests left localhost) |
| “← Jemma’s Journals” ≥24px | Yes (24px min-height) |

## Shared-code notes (for moving into Jemma’s Journals)

**Markup (`site/index.html`)**
- 13 `<meta name="theme-color" content="#7A1E2A">`; 14 robots meta.
- 15–17 the no-flash script. It reads `jj-mode`, else the old `jemmas-pokedex-mode` (copies it over), removes the old key, sets `data-mode` on `<html>`, and sets the dark `theme-color` #4E1018. Everything is inside try/catch, with light as the fallback.
- 22 top bar: `div.topbar#topbar > button#menuBtn[type=button][aria-controls=side][aria-expanded=false][aria-label="Open the menu"] > span#menuIco + "Menu"`, then `a.topname[href="#home"]` “Jemma’s <em>Pokédex</em>”.
- 23 `div.scrim#scrim` (empty; the click handler is in JS).
- 24 `aside.side#side[aria-label]`; 27 `a.home-link#homeLink[href="/"]` first inside it; 30 `nav.nav#nav` (filled by JS).
- 32 `main#main > div.wrap#view[tabindex=-1]`; the footer is inside `<main>`, so it goes inert with the page.
- 35–38 footer: `footer.foot > div.foot-rule[aria-hidden] + b.foot-name + div.about-site > p (line 1) + p (span.cr, span.dot[aria-hidden] "&nbsp;·", space, span.cr …) + div.foot-links > button.totop#toTop + button.mode-text#modeBtn[aria-pressed=false]`. Both buttons are empty in the HTML, so JS fills icon and text. (In a no-JS state they have no name: that is the one `noName` hit in the sweep.)

**Script (`site/js/app.js`)**
- 4 `ic(name)`: inline SVG from `ICONS` (icons.js) with `class="i" aria-hidden`. The shared code needs `menu`, `sun`, `moon` and `arrow-up`.
- Drawer, 1430–1464:
  - 1435 `side`, `menuBtn` and `narrow = matchMedia("(max-width:900px)")`; 1436 `behind = [#topbar, #main]`; 1437 menu icon.
  - 1438–1448 `setMenu(open, refocus = true)`. It only opens when narrow. It toggles `body.nav-open`, `aria-expanded` and `aria-label` (“Open/Close the menu”), sets `side.inert = narrow && !open`, and sets `behind[].inert = open`. On open it focuses `nav a.on`, else `a[href="#home"]`. On close it refocuses Menu if focus was inside.
  - 1449 Menu click toggles; 1450 a scrim click closes and focuses Menu; 1451 a link click in the side closes and focuses `#view`; 1452 Enter in search closes and focuses `#view` (Pokédex-specific).
  - 1453–1462 global keydown: Escape closes; Tab wraps inside the side (and pulls focus back in if a redraw lost it).
  - 1463 crossing 900px closes, and focuses Menu if focus was inside; 1464 initial `setMenu(false, false)`; 1502 `hashchange` also closes the drawer.
  - The current-page link comes from `navHtml()` 1270–1276 (`class="on"` + `aria-current="page"`).
- Footer dots, 1466–1477: `footDots()` hides (visibility) a `.dot` whose next credit has wrapped to a new line. It runs on resize and on `document.fonts.ready`.
- Mode, 1479–1496: `MODE_KEY = "jj-mode"`; `mode` is read from the `data-mode` the head script set; `applyMode()` sets `data-mode`, the button’s icon and text, `aria-pressed`, and `theme-color` (#4E1018 / #7A1E2A). The click flips `mode`, saves it in try/catch and calls `applyMode()`. There is no `storage` listener.
- Back to top, 1497–1501: `#toTop` gets icon and text. The click does `scrollTo({top:0, behavior: reduced-motion ? "auto" : "smooth"})`, then `#view.focus({preventScroll:true})`.

**Styles (`site/site.css`)**
- 129–141 `:root` tokens (`--focus`, `--deep-text` used by the footer); 143–144 `:root[data-mode="dark"]` base swap (`--paper`, `--surface`, `--ink`, `--muted`, `--line`, `--soft`, `--focus:var(--accent)`, `--deep-text:#E48A96`, `color-scheme`); 877–882 and later blocks: the binder look’s dark tokens. There are no `prefers-color-scheme` rules.
- 160 `.side` (fixed, `z-index:20`); 162–166 `.home-link` (10px uppercase, `min-height:24px`).
- 1000–1018 drawer: `.topbar,.scrim{display:none}` outside the media query. Inside `@media (max-width:900px)`: `--side:0`; `.side` gets `width:min(300px,86vw)`, `translateX(-104%)`, `visibility:hidden` and a delayed visibility transition; `body.nav-open .side` is visible; `body.nav-open .scrim` is `position:fixed; inset:0; rgba(0,0,0,.45); z-index:15`; `.topbar` is sticky, 52px tall, with safe-area padding; the button has `min-height:44px`; `.topname` is 26px in the display font with an accent `em`; reduced motion turns the transition off. 1088 `body.nav-open{overflow:hidden}`.
- 1099–1113 footer: `.foot` padding; `.foot-rule` is a 120px dashed rule; `.foot-name` 24px display; `.about-site` 12.5px in a muted/ink mix (a little deeper for the shaded band); `p + p{text-wrap:balance}`; `.cr{white-space:nowrap}`; at ≤600px `.dot{display:none}` and `.cr{display:block}`; `.foot-links` is a flex row with a 26px gap; buttons are link-style, `min-height:44px`, 700 13px, `--deep-text`, with a 2px `--focus` ring.

**Pokédex-specific bits to keep local:** the theme colours, Enter-in-search closing the drawer (1452), the ← → page keys ignoring an open drawer (1504), and `.toolbar{top:52px…}` under the bar (1016).

## Tests result

`python -B -X utf8 tests/run_tests.py` (with `PYTHONDONTWRITEBYTECODE=1`) in `pokedex/`, on the throwaway copy: **88 tests OK (2 skipped as slow), 67 of 67 page tests passed, 271 s.** `go.json` has the same SHA-256 before and after (c294d8f3…). Nothing was written to the repo.
