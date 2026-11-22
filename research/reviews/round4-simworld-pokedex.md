# Review, round 4: Sim World and the Pokédex after the shared-code switch (22 Nov 2026, early hours)

Read-only. Nothing in `sim-world`, `pokedex` or the parent was edited, staged or committed (all three `git status` clean apart from the parent’s existing untracked `for-jemma/concepts/app-styles/built/round3/`; every repo level with `origin/main`). Her ticks file `pokedex/data/collection/go.json` has the same SHA-256 before and after (c294d8f3…6b564). The family server’s stored dark-mode choice (`logs/family-mode.txt`, “light”) was never changed: every POST was answered inside the browser by the test harness and never reached a server (the Dark mode button’s `POST /family/mode` was faked there, and the fake fed back into the page’s `data-jj-server-mode` so the server path could still be followed).

Versions checked: Sim World 998c1f9 (with 50e08e6), Pokédex 7a9e342, parent e781fa4 (`site/family/` as in 6b964db).

**How it was checked:** Edge through Playwright. Sim World: 33 page types through `http://localhost:8050/sim-world/` at 1600, 1280, 1000, 901, 899 and 390, light (device set to dark) and dark, 396 loads. Pokédex: 27 page types through `http://localhost:8050/pokedex/` at 1600, 1584, 1280, 1000, 901, 899 and 390, light and dark, plus her own server `http://localhost:8030/` at 1280 and 390. Per page: console errors, failed requests (including `/family/`), outside requests, broken pictures, sideways scroll, H1, `data-mode`, theme colour, footer line 1 word for word, credits, a “·” at a line’s start or end, credits one per line on phones with no empty line, 12.5px, name 24px plain, both buttons ≥44px and level, Menu bar on/off, closed drawer inert, Menu 44px, bar name 26px, `aria-current`; Pokédex banner tabs (rows, width, size) per region. Then scripted runs of the drawer, focus, dark mode across pages, tabs and apps, Back to top, view-only, the `/family/` route on 8030, and both apps opened as files.

Scripts and raw results: `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review4\swpd\`. Screenshots: `…\scratchpad\review4\simworld\` and `…\scratchpad\review4\pokedex\`.

---

# Sim World

## Not fixed (from round 3)

All round-3 Should-fix items in Sim World itself are fixed and hold, except:

- **Should fix 9 (other small low contrast)**: unchanged (late relative’s monogram 2.37:1, family-tree initials in dark, Admin Progress “not owned” and “/ 5”). No CSS for them was touched.
- **Should fix 8 (weekly task’s last run failed)**: cannot be confirmed yet. Task Scheduler still shows last run 15 Nov 12:18, result 1, for *both* the Sim World refresh and the Pokédex backup (same second). Next runs are today 07:54 (Sim World) and 09:40 (Pokédex), after this review. Look at `logs/gallery-refresh.log` after 07:54; it should now end with a “Jemma’s Journals: …” line from `record_apps.py`.
- **Should fix 6 (parent: `tools/serve_all.py` refuses connections under load)**: **confirmed, not fixed.** With this review and another session’s sweep running together, Sim World pictures and scripts failed with `ERR_CONNECTION_REFUSED` (San Myshuno at 899, Rio Verde at 901/899: four pictures broken). The Pokédex’s own `serve.py` and Sim World’s test server now queue 64/128; `serve_all.py`’s `Server` still has Python’s default queue of 5. Fix: `request_queue_size = 64` on `Server` in `tools/serve_all.py`. Unlikely with her one window, but the family server is now the way she opens every app.

Checked fixed: 1 (notes copied from the memory folder worked out from the project path); 2 (the project’s `.lnk` opens `tools/open_site.pyw sim-world`; Desktop and Start menu ones do too); 3 (keyboard Enter on Home, Willow Creek, Calendar, Clubs and Admin keeps focus on that link at 1280; in the drawer focus goes to `#view`); 4 (`aria-current="page"` on exactly one link on every page except the missing page); 5 (Not owned label 4.97:1, names 5.38, counts 5.06 light; 6.83 / 7.67 / 7.31 dark); 7 (live-hook test now runs: 1 skipped, the game one); 10 (dead CSS gone, purple name is `var(--water)`, CLAUDE.md explains 8001 vs 8050).

## New problems

### Broken

1. **Opened as a file, at 900px and below the whole page is under the dark scrim and nothing can be tapped.** `site/index.html` has `<div class="scrim" id="scrim"></div>` with no `hidden`, and `site.css` shows it whenever it isn’t hidden (`@media (max-width:900px){ .scrim:not([hidden]){display:block; … rgba(0,0,0,.45); z-index:15} }`). Only `family.js` sets `hidden`, and as a file `/family/` doesn’t load (`file:///C:/family/…` not found). Result at 899 and 390: page and top bar dimmed, every click lands on the scrim (Playwright could not click Menu), Menu does nothing anyway, and the off-screen sidebar is not inert, so Tab walks into an invisible drawer. At 1280 the page works but has no Back to top or Dark mode (hidden, as intended). Screenshot `simworld\file_390.jpg`. Her shortcuts all open through the family server, so she only meets this by double-clicking `index.html`, but the code says file mode is handled (“the two buttons are hidden there rather than left empty”). *Fix:* add `hidden` to the scrim in the markup (as the Pokédex does), and in `familyReady()`’s no-family branch also make the sidebar usable (or show a one-line “Open it through Jemma’s Journals” note).

### Should fix

2. **`aria-current="page"` lands on a world on group pages.** On a club, dynasty or organisation page the only link marked is a world: Paragons → “Magnolia Promenade”, Goth dynasty → “Willow Creek”, Art Society → “Britechester”; Britechester’s calendar → “Calendar”. `navCurrent()` falls back to any `.on` link, which there is the page’s *context*, not the page. Screen readers then say “Willow Creek, current page” on the dynasty page. *Fix:* only the address match (or `.cur`) gets `"page"`; a context link gets `aria-current="true"` or nothing.
3. **Two copies of “Tab stays in the drawer”.** Sim World keeps its own Tab-wrap keydown handler (`js/app.js`, “kept from 21 Nov”) on top of the family’s inert-outside approach; the Pokédex dropped its wrap and only pulls focus back if it was lost. Both pass the 70-Tab test, but they behave differently at the end of the drawer (Sim World wraps; the Pokédex lets one Tab reach the browser’s own bar). If the family rule is “wraps”, it belongs in `family.js` `menu()` once.
4. **`drawerStart()` and `navCurrent()` both work out “this page’s link”** with slightly different rules (one needs the link visible, the other falls back to `.cur`/`.on`). One function would stop them drifting (see 2).
5. **Family CSS hides any `.dot` in the footer on phones** (`family.css`: `:where(.jj-foot) :where(.dot, .jj-dot){display:none}` under 600px). Sim World’s map pin in the footer rule is also `.dot`, rescued only by `.foot-rule .dot{display:block;margin:0}` in site.css. Fragile: scope the family rule to `[data-jj-credits] .dot`.

## Looks (list only)

- Phone footer: line 1 and the five credits run on as one block of seven same-coloured lines (`simworld\footer_390_dark.png`); a little space between line 1 and the credits would help.
- Round 3’s Looks list still applies (gold “Sim World” on the home banner, rounded group cards, gold one-word titles on bright maps, faint footer dots, chip cut on the organisation page, calendar on a phone).

## Family rules (all pass over http)

- 396 loads: no console errors or failed requests except the refused connections above; no outside requests; no sideways scroll at any width; one H1; `data-mode` as wanted; theme colour #EEEAF2 / #1B1524; one footer; line 1 word for word; credits unchanged and each with a capital; no dot starting or ending a line at any width; under 700px credits one per line, dots hidden, no empty line; 12.5px; name 24px plain; Back to top and Dark mode 44px and level; Menu bar at 899 and 390 only; closed drawer inert; Menu 44px, `aria-controls="side"`; bar name 26px.
- Drawer at 899 on Home, Willow Creek, Goth, Bella Goth, Calendar, Clubs and the missing page: opens on that page’s link (Home on the missing page); top bar and page inert; scrim black 45%; page behind doesn’t scroll; 70 Tabs + 8 Shift+Tabs never leave it; Escape and the scrim close it with focus on Menu; a link by keyboard or mouse closes it and focuses `#view` (next Tab goes into the page); search Escape first clears the words and leaves it open; Enter on a search result closes it and focuses the page; crossing to 1000 resets it, back to 899 the sidebar is inert again; focus in the sidebar when narrowing goes to Menu.
- **Folding the current world keeps the drawer open** (click and Enter, fold and unfold), and closing a world with a household open below it keeps it open too. Clicking Home while on Home closes it and focuses the page.
- Dark mode: opens light with the device dark; button → dark, theme colour, “Light mode”, `aria-pressed=true`, focus stays on the button, `jj-mode=dark`, and family.js sends `POST /family/mode` “dark” (blocked here). A second tab follows at once (storage event). Reload, Jemma’s Journals home and the Pokédex all open dark; switching back in the second tab brings the first back to light. As online (no server attribute): the same by `jj-mode` alone, no POST. Old `jsw-mode` moved once and removed; a junk value gives light; storage blocked: opens light, the button still switches, no errors.
- Back to top (Enter and click): scrolls to 0, focus on `#view`, address unchanged, next Tab is the first link in the page.

## Code quality and the weekly task

- The switch is clean: no leftovers of `setNav`, `nav-open`, `nav-lock`, `tidyCredits`, `.sep`, `showMode`, `.foot-links`, `.about-site .sep` in js, css or tests.
- `gallery_refresh.py` runs the parent’s `tools/record_apps.py` only after a good push, with a timeout, no window, output in the log, never failing the run: safe. The risks are in `record_apps.py` itself (parent, shared with the Pokédex): see the Pokédex section, Should fix 4.

## Tests result

`python -B -X utf8 tools/run_tests.py`: **all passed.** Python 396 tests OK (1 skipped, needs the game); site 109 passed (55 s). No files changed.

---

# Pokédex

## Not fixed (from round 3)

Round 3’s Broken and Should-fix items are all dealt with:
- Broken 1 (folder shortcut started the old copy): **fixed**. `Jemma’s Pokédex.lnk` in the folder, on the Desktop and in the Start menu all run `tools/open_site.pyw pokedex` in `Documents\JemmasJournals`.
- Should fix 2 (search with a tab on) and 4 (footer line 1 and the server): **put on her list** (`for-jemma/your-list.md`, Decide), as asked; behaviour unchanged.
- Should fix 3 (Tabler missing from the credits): **fixed** on the page and in the test.

Polish from round 3 still open (not required): the sidebar search box still has `outline:none` (`site.css:174`); no not-found page (`#nope` shows Home); a search typed on a region page keeps that region’s address; the server still answers HTTP/1.0 (the queue of 64 was added: no refusals on 8030 in this review); round 3’s list 7 unchanged. Dead-code leftovers: `.hero > :not(.heroart)` (`site.css:478`) still names the removed parade; `SHOT_FIT` still lists unused pictures (`kanto-15.jpg`, `sinnoh-map-1.jpg`, `kalos-map-3.jpg`, `kalos-map-4.png`); most of the 170 files in `site/regions/` are the old scenery (on her list to decide).

## New problems

### Broken

None on the pages over http.

### Should fix

1. **A crafted link can run script on her Pokédex (attribute injection through `?pic=`, `?fit=` and `?ratio=`).** `regionShot()` and `shotStyle()` (`js/app.js` 336–348) put these address values straight into a `style="…"` attribute through `innerHTML`, unescaped. Checked with GET only: `http://localhost:8030/?pic=x%22%20data-pwn=%22yes#gen-1` gives `<header class="hero withshot" … data-pwn="yes')">`; the same for `fit` and `ratio`. With `"><img src=x onerror=…>` it would run script, and on her PC that script is on the Pokédex’s own address, so it could send `POST /api/tick` with the `X-Pokedex` header and change her ticks (the Host check doesn’t stop a same-address page). It needs her to open a link someone made, and it was there before tonight (tonight’s rewrite of `regionShot` kept it), but the code is public on GitHub and the site is meant to go online. *Fix:* drop `?pic=`, `?fit=` and `?ratio=` (they were for pictures of options only), or accept only known file names and escape with `attr()`.
2. **Tab can leave the open drawer once per lap (regression from the switch).** At 899 with the drawer open, 70 Tabs reached `<body>` 3–5 times on every page tried (Home, Johto, Pikachu, Hisuian Growlithe, Fast tick, Event Pokémon, `#nope`): after the last link the next Tab goes to the browser (in a real window, its address bar), then comes back in. The Pokédex’s own wrap was removed in favour of the family’s inert-outside approach plus a “pull focus back if it was lost” handler; Sim World kept its own wrap, so it never leaves. The family rule is “Tab stays inside the drawer”. *Fix:* put the wrap in `family.js` `menu()` once and drop Sim World’s copy (Sim World Should fix 3).
3. **On a laptop, choosing a sidebar link by keyboard drops focus to the page’s body** (as Sim World’s round-3 Should fix 3, which Sim World has now fixed). At 1280, Enter on Kanto, Fast tick, Home or Event Pokémon: the sidebar is redrawn, the focused link is replaced, and focus ends on `<body>`, so the next Tab starts again from “← Jemma’s Journals”. Like this before tonight too. *Fix:* after a keyboard choice on wide screens, focus the new current link (`nav a.on`) or `#view`.
4. **`tools/record_apps.py` (the parent’s, now run by the Pokédex’s and Sim World’s weekly tasks) can record a version that isn’t on GitHub.** It records every app that is on `main` and clean, but doesn’t check the app’s commit is pushed. The Pokédex backup runs it for *all four* apps, so a Sim World or Library commit made by hand and not yet pushed would be recorded and pushed in the parent, and a clone of Jemma’s Journals would point at a submodule commit GitHub doesn’t have. Also: it doesn’t check the parent itself is on `main` (it pushes whatever branch the parent is on, with any other unpushed parent commits); when it skips an app it still ends with “every app already recorded”; and the Library (09:30) and Pokédex (09:40) backups both run it ten minutes apart, so a slow push could meet an `index.lock`. The callers themselves are safe (only after a good push, timeout, output logged, never failing the backup). *Fix:* skip an app whose `HEAD` isn’t in `origin/main` (`git rev-list origin/main..HEAD` empty), check the parent’s branch, and print “not recorded: …” when something was skipped.
5. **View only: the boxes still act like buttons for the keyboard.** With no save server (served as plain files) the page is quiet, as intended, but every tick box is still a focusable `<button aria-pressed>` that does nothing when pressed, with no word anywhere; only the mouse cursor changes (`cursor:default`). A keyboard or screen-reader user presses “Caught” and nothing happens. *Fix:* `aria-disabled="true"` on the boxes in view-only (or draw them as plain status).
6. **Opened as a file it can’t be used under 900px, and the footer shows two empty buttons.** `/family/` doesn’t load from a file, so Menu does nothing (the sidebar stays off-screen), Back to top and Dark mode are empty, unlabelled buttons (Sim World hides them in that case, the Pokédex doesn’t), and “← Jemma’s Journals” goes to `file:///C:/`. Her shortcuts all open through the family server, so this only matters if she double-clicks `index.html`. *Fix:* hide `.jj-foot-links` when `window.JJFamily` is missing, as Sim World does.

## Looks (list only)

- Banner tabs: the selected tab hangs 8px lower than the rest (by design). One row at 1600 (89px, 10.5px), 1584 (88px, 10.5px) and 1280 (71px, labels 8.5px), the same width and size on Every Pokémon and all ten regions, both modes, both addresses.
- In the drawer, Escape with words in the search closes the drawer and keeps the search; in Sim World the first Escape clears the words. Both meet the family rule; they just differ.
- Round 3’s Looks list still applies.

## View only and the server (checked)

- **Plain hosting** (`pokedex/site` served statically with the parent’s `site/family/`, no API, so `api/collection` is a 404): `html.view-only` set, **no notice**, her ticks as at the last build (Kanto 151 of 151), pressing a box changes nothing, no toast, **no request sent**. The only trace is the browser’s own console line for the 404. Screenshot `pokedex\viewonly_p-25_1280.jpg`.
- **Real failures still say so:** a 500, a 403, a 503 (what the family server sends when 8030 is down) and broken JSON each show “The Pokédex server couldn’t read your ticks, so nothing can be saved for now…”, and a tick then gives the “couldn’t read your ticks” toast. A 200 with an HTML page (a web host’s own page) counts as no server, quietly, as designed.
- **Her server, normal:** ticks load; a tick’s POST (answered 503 by the harness) rolls back with “Not saved: the Pokédex server isn’t answering…”.
- **`/family/` on 8030 is safe:** `family.js` 200; `%2e%2e/%2e%2e/CLAUDE.md`, `..%2f..%2fpokedex%2fdata%2fcollection%2fgo.json`, `..%5c..%5cCLAUDE.md`, raw `../../CLAUDE.md`, `C:%2fWindows%2fwin.ini`, `//etc/passwd` and the bare folder all 404; another Host name gets 403. (It also serves `README.md` from that folder: harmless.)

## Family rules (all pass over http, apart from Should fix 2)

- 378 loads on 8050 plus 108 on 8030: no console errors and no failed requests except `ERR_CONNECTION_REFUSED` for sprites on 8050 only, with three sweeps and another session running at once (the parent’s `serve_all.py` queue, see Sim World “Not fixed”; none on 8030); no outside requests; no sideways scroll; one H1; `data-mode` as wanted; theme colour #7A1E2A / #4E1018; footer line 1 word for word; credits now with Tabler; no dot starting or ending a line; under 600px one per line, no dots, no empty line; 12.5px; name 24px plain; both buttons 44px and level; Menu bar at 899 and 390 only, closed drawer inert, Menu 44px, bar name 26px.
- Drawer at 899: opens on this page’s link (Johto on Johto, Kanto on Pikachu, Hisui on Hisuian Growlithe, Fast tick, Event Pokémon, Home on `#nope`); top bar and page inert; scrim 45%; page doesn’t scroll; Escape and scrim return focus to Menu; a link by keyboard or mouse closes it and focuses `#view`, next Tab into the page; Enter in the search closes it and focuses the results; crossing 900 resets it and moves focus to Menu if it was inside.
- `aria-current="page"` on exactly one link everywhere (Kanto on a Kanto Pokémon’s page; none on `#nope`).
- Dark mode, as in Sim World: light with the device dark; button → dark, theme colour, “Light mode”, `aria-pressed`, focus kept, `POST /family/mode` (blocked); **a second tab now follows at once** (round 3 Polish, now in the shared code); reload, home and Sim World open dark; online-style by `jj-mode` alone; old `jemmas-pokedex-mode` moved once and removed; junk → light; storage blocked → light, button works, no errors.
- Back to top: scrolls to 0, focus `#view`, address unchanged, next Tab is the first banner tab.

## Code quality of the switch

- Clean: no leftovers of `setMenu`, `nav-open`, `footDots`, `applyMode`, `.foot`, `.about-site`, `.mode-text`, `.totop`. The scrim has `hidden` in the markup, so it can’t cover the page when `family.js` is missing (unlike Sim World, Broken 1 there).
- `family.js` repaints on every DOM change (a MutationObserver on the whole body, once per frame), and each repaint measures every credit dot, forcing a layout. The Pokédex redraws hundreds of cards on each tick and filter, so this adds a forced layout per redraw. Not noticeable tonight; worth narrowing to the footer.
- Three separate copies of “serve `/family/` safely” (Pokédex `serve.py`, Sim World `tests/site/serve.py`, the parent’s `serve_all.py`), each a little different. All safe; one shared helper would keep them so.
- `backup.py` runs `record_apps.py` only after a good push, with a timeout, no window, output in the log: safe (the risks are in `record_apps.py`, Should fix 4).

## Tests result

`python -B -X utf8 tests/run_tests.py` (with `PYTHONDONTWRITEBYTECODE=1`): **all passed.** 96 tests OK (2 skipped as slow); 70 of 70 page tests passed. `go.json` SHA-256 c294d8f3…6b564 before and after. No files changed.
