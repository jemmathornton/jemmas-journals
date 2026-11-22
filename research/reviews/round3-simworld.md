# Review, round 3: Jemma’s Sim World after the move (22 Nov, early hours)

Read-only. Nothing in `sim-world` was edited, built or committed (`git status` clean before and after, still at 1df0098). The parent was clean at the start; by the end it had uncommitted edits to `site/index.html`, `tests/check_page.js` and `tools/serve_all.py` from another session (not this review), plus the round-3 review files.

**How it was checked:** 33 pages through `http://localhost:8050/sim-world/` (tools/serve_all.py) in Edge via Playwright: home; 5 world pages (Willow Creek, Britechester, Sulani, StrangerVille, San Myshuno); 2 neighbourhoods (Sage Estates, StrangerVille Secret Lots); 5 lots (Streamlet Single, Oakenstead, Rio Verde rental, Admiral’s Wreckage Community Space, 8 Bells); Willow Creek Households; 3 households (Goth, Straud in unowned Forgotten Hollow, Fletcher); Bella Goth, Vladislaus Straud; a dynasty, club and organisation; Calendar and Britechester’s calendar; Clubs, Dynasties, Organisations, Families, Businesses; Admin, Progress, Notes; a missing page. Each at 1600, 1280, 1000, 901, 899 and 390, light (device set to **dark**, to prove it opens light) and dark (`jj-mode=dark` stored first). Per page: console errors, failed or outside requests, broken images, missing alt, sideways scroll, clipped text, contrast against the real background, straight apostrophes, undefined/NaN, H1 count, footer words and buttons, Menu bar on/off. Then scripted checks of dark mode, Back to top, keyboard focus, the Menu drawer, the “← Jemma’s Journals” link as a file and over http, the Admin pages without `admin-data.js` (as online), and every place that could still point at `Documents\SimTracker`.

Screenshots: `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review3\simworld\` (`<page>_<width>_<light|dark>.jpg`; full pages at 1280 and 390 in `full\`; `drawer-open_*`, `drawer-search_*`, `focus-*`, `footer_*.png`). Raw results: `..\..\sw3-*.json`, `sw3-interact.txt`.

**Clean everywhere:** no console errors, no failed requests, nothing fetched from another site, no broken images, no missing alt, no sideways scroll at any of the six widths, no straight apostrophes, no undefined/NaN, one H1 per page, one `<footer>` with line 1 word for word, both footer buttons 44 px and level, the Menu bar shows at 899 and not at 901, `data-mode` always set, `data-inner` set on lot, Sim and household pages only. (A first run of two sweeps side by side got “connection refused” from serve_all.py for some pictures; run one at a time there were none. See Should fix 6.)

---

## Broken

Nothing broken on the pages.

## Should fix

1. **The Claude-notes backup still reads the old SimTracker memory folder.** `tools/sync_notes.py:14` has `MEMORY = …'.claude', 'projects', 'C--Users-Jemma-Documents-SimTracker', 'memory'`. Claude now works from `C--Users-Jemma-Documents-JemmasJournals-sim-world` (26 notes copied there on 21 Nov). The weekly refresh (next run today, 22 Nov 07:54, already pointed at the new folder) runs `sync_notes.py` before its save, so from now on any note written in the new folder never reaches `claude-notes/` or GitHub, and once the old folder is deleted it silently copies nothing. `claude-notes/README.md:5` names the old folder too. *Fix:* point MEMORY at the new folder (or work it out from ROOT, as Claude Code does: path with `\`, `:` and `/` turned into `-`).

2. **The shortcut inside the project still opens the old copy.** `sim-world/Jemma's Sim World.lnk` (kept in git) opens `file:///C:/Users/Jemma/Documents/SimTracker/site/index.html`, start-in `Documents\SimTracker\site`. Her Desktop and Start Menu shortcuts are already right (they open `JemmasJournals/sim-world/site/index.html`). If she ever double-clicks the one in the folder she gets the old, frozen site. *Fix:* rerun `tools/make_shortcuts.ps1` (it works from `$PSScriptRoot`) and commit the new .lnk.

3. **Choosing Home, a world, Calendar or any Across-the-worlds/Admin page by keyboard drops focus to the page’s body.** *Where:* sidebar at any width, and the phone drawer. *What:* `route()` (`js/app.js:1399`) puts focus back only on `#nav a.cur, #nav a.path`, but those links are marked `.on` (`renderNav`, `js/app.js:649`, `653`; sections.js the same). So after Enter on “Willow Creek”, “Calendar” or “Home” focus is on `<body>`; in the drawer the next Tab lands somewhere in the middle of the page (seen: “San Myshuno” on the Calendar). Neighbourhood, lot, household and Sim links are fine. The family rule says after a link the focus goes to the page’s main content. *Fix:* include `a.on` in that selector on wide screens, and in the drawer case move focus to `#view` (as Back to top does). A test in `family-rules.spec.js` would catch it: Enter on a drawer link, expect `#view` focused.

4. **No `aria-current` anywhere.** The current page in the sidebar is shown only by colour and a box (`.on`, `.cur`, `.path`). Screen readers can’t tell where you are. *Fix:* add `aria-current="page"` beside `.on`/`.cur` in `renderNav` (one attribute per template).

5. **Sidebar “Not owned” text is still faint (round 1 item 6 is not actually fixed).** Measured now on the lilac sidebar (light): the “Not owned” label **2.18:1** (`.nav-group.dim .label{opacity:.55}`, `site.css:916`), the not-owned world names **2.67:1** (`.nav a.soon` 45 % ink, `site.css:214`), their household counts **2.07:1** (35 %, `site.css:216`). Dark: 2.94, 3.87, 2.84. Round 2 recorded this as fixed, but the values haven’t changed since the town-plan commit (978bcd6); round 2’s contrast check most likely misread the browser’s `color(srgb …)` values (this round’s first pass did the same until corrected). Several of these names are links (they unfold to households). Her list has an open Decide on greyed sidebar text. *Fix:* about 70 % / 65 % and drop the label’s opacity, or answer her Decide first.

6. **(Parent, not Sim World; unconfirmed) `tools/serve_all.py` refused connections once.** Two browsers loading picture-heavy pages at once got `ERR_CONNECTION_REFUSED` for maps, Gallery pictures and icons; one at a time there were none. Either the listen backlog (`request_queue_size`, default 5, on a `ThreadingMixIn` server) or the server being restarted: `tools/serve_all.py` was being changed by another session during this review (uncommitted edits in the parent, not mine). *Fix if it recurs:* `request_queue_size = 64` on the `Server` class.

7. **The live-hook test now always skips.** `tests/test_backup.py:151` looks for `ROOT/.git/hooks/post-commit`, but in a submodule `.git` is a file (`gitdir: ../.git/modules/sim-world`), so `test_live_hook_is_this_one` skips (Python tests: 2 skipped, was 1). The hook itself is in place and identical (`JemmasJournals/.git/modules/sim-world/hooks/post-commit`, checked by diff). *Fix:* ask git for the folder (`git rev-parse --git-path hooks`). `tools/git-hooks/post-commit`’s comment and CLAUDE.md’s “copy it to .git/hooks” need the same note.

8. **The weekly task’s last scheduled run failed.** Windows Task Scheduler: last run 15 Nov 12:18, result **1**; the log’s last entry is a good run at 20:04 the same day (probably run by hand). The task now points at `JemmasJournals\sim-world` (correct). Worth a look after today’s 07:54 run: `logs/gallery-refresh.log`, and the parent will then show `sim-world` as changed (new commit in the submodule) until the parent records it, which the refresh doesn’t do.

9. **Other low contrast left (small, all from before):** a late relative’s monogram (white on grey #A3AAA5, Cornelia Goth on Bella’s page) 2.37:1 in both modes; family-tree initials in dark 3.1–4.3:1 (round 2 item 6); Admin Progress “not owned” and “/ 5” 2.22 light, 2.66 dark (round 1 item 17). Everything else measured at 4.5:1 or more once text over map pictures is set aside (checked by eye there: shadows and the fade carry it).

10. **Small code tidy-ups.** `site.css:632` `.topbar .brand-bar em{color:var(--brass)}` is dead (overridden by `site.css:1192`); the purple name colours are hard-coded at `site.css:1192–1193` rather than using `--water` (which already holds exactly #5B4BB0 / #B7A8F7). `CLAUDE.md` still says the Library-to-be-checked “app” preview runs on port 8001 from `.claude/launch.json` (still true, but serve_all on 8050 is now the family address); fine either way.

## Looks (would change how it looks: for her to decide, not done)

- **Home banner still says “Sim World” in gold** while the sidebar and Menu bar name are now purple (her 21 Nov pick). Purple there too, or keep the big title gold? (`home_1600_light.jpg`)
- Group cards (“Their groups”), the family-tree box’s inner cards and the dynasty/club badges on Sim pages are still rounded; the rest of the page is squared town-plan plates. (`full/s-bella-goth_1280_dark.jpg`)
- One-word world titles in gold on bright maps (Britechester, Sulani, StrangerVille): still her open Question A from rounds 1 and 2. (`w-britechester_1280_light.jpg`)
- Footer “·” separators are very faint (purple at 60 %); they read as gaps rather than dots. (`footer_1280_light.png`)
- Organisation page: the household chip “Best of Friends · Britechester” is cut by a few pixels at 1280 and 1000. (`g-org-art-society_1280_light.jpg`)
- Calendar on a phone: still her open Decide (day names and events run together at 390).

## Previous rounds: did the fixes hold?

| Item | Now |
|---|---|
| R1 world descriptions cut at 1280 | Held (3 lines on every world checked) |
| R1 dark badges, calendar chip | Held |
| R1 empty column at 1600 | Held |
| R1 sidebar “Not owned” faint | **Not fixed** (Should fix 5) |
| R1 lot-size brackets on household cards | Held |
| R1 search focus ring | Held (2 px gold) |
| R2 sideways scroll on Community Space lots at 901 | **Fixed** (none at 901 or 899) |
| R2 hidden focus stop under the open drawer | **Fixed** (60 Tabs and 6 Shift+Tabs stay inside the drawer; top bar and page inert) |
| R2 gold focus ring on map banners | **Fixed** (white ring on `.hero.mapped`, `site.css:1048`) |
| R2 “·” ending a footer line | **Fixed** (`tidyCredits`, js/app.js:1630; credits 12.5 px on phones) |
| R2 household Sims table on phone | **Fixed** (stacked list under 700 px) |
| R2 4th figure alone on phone | **Fixed** (2 × 2) |
| R2 top-bar name 3.28:1 | **Fixed** (now purple #5B4BB0, about 5.9:1) |
| R1/R2 calendar on phone, small card text, half-restyled pages | Partly: lot/Sim/household pages now town-plan (her pick); calendar still her Decide |

## The 21 Nov changes

- **Town-plan look on lot, Sim and household pages:** `html[data-inner]` set by `route()` (`js/app.js:1394`) on exactly those pages (checked: on for 10 lot/household/Sim pages, off for the other 23); the CSS block is `site.css:1163–1190`. Facts plates, carousel, Sims list, family tree box and “Also in” cards are squared with striped top edges, both modes.
- **Purple name:** sidebar and Menu bar “Sim World” computed `rgb(91,75,176)` light, `#B7A8F7` dark (`site.css:1192–1193`).
- **Try switch removed:** no `trial.js` file, no reference in index.html, js, css, tools or tests; the only mention is a test that checks no switch exists (`tests/site/rules.spec.js:144`). No `jsw-try`-style keys in storage code (keys used: `jj-mode`, `jsw-seen-v1`, `jsw-calendar-4`).
- **“← Jemma’s Journals”:** over http the link is `/` and opens `http://localhost:8050/` (Jemma’s Journals). Opened as a file, `HOME_LOCAL` (`js/app.js:1647–1648`) makes it `../../site/index.html` → `file:///C:/Users/Jemma/Documents/JemmasJournals/site/index.html`, which exists and opens “Jemma’s Journals”. 26 px tall. Home’s Open link back is `/sim-world/` and works. No site test covers the file case (all site tests serve `site/` at the root on port 8011).
- **Nothing still points at Documents\SimTracker** in site/, tools/ (except sync_notes.py, Should fix 1), tests or the scheduled task. Leftovers: the project’s own .lnk (Should fix 2), `claude-notes/README.md`, and history mentions in HANDOVER.md (fine).

## Family rules: all pass

- **Dark mode:** opens light with the device set to dark (theme-color #EEEAF2, button “Dark mode”, `aria-pressed=false`); click → dark, `jj-mode=dark`, theme-color #1B1524, “Light mode”, `aria-pressed=true`; survives reload; carries to Jemma’s Journals on the same address (home opened dark). Old `jsw-mode` is moved to `jj-mode` and removed; a junk value gives light; with storage blocked the page still draws, opens light and the button still switches for the visit. No `prefers-color-scheme` anywhere. Other windows follow by the `storage` event.
- **Footer:** pin on a dashed rule, “Jemma’s Sim World” plain display font, line 1 word for word on every page, Sim World’s credits (each with a capital, glued `&nbsp;·`, `text-wrap:balance`, one per line under 700 px), Back to top (scrolls to 0, focus to `#view`, next Tab goes to the page) and Dark mode, both 44 px and level, 12.5 px.
- **Menu (≤900):** at 901 the sidebar, at 899 and 390 the bar: Lucide menu icon + “Menu” (44 px), “Jemma’s *Sim World*” 26 px italic purple, linking `#home`. `aria-controls="side"`, `aria-expanded` toggles; closed drawer `inert` (Tab: Menu → bar name → page); opening focuses the current page’s link (Goth on the Goth page; Home on home); top bar and page inert while open, page doesn’t scroll; Escape, scrim and a link close it with focus back on Menu (but see Should fix 3 after a link); with words in search the first Escape only clears them; widening past 900 while open resets it. Scrim black 45 %.
- **Small things:** robots meta `noindex, noai, noimageai`; fonts are local (`site/fonts/`, 14 `@font-face` all `url(fonts/…)`); no request left localhost on any page.
- Not required but missing: a skip link. On wide screens it takes 59 Tab stops through the sidebar to reach the page.

## Shared-code notes (for moving dark mode, footer, Back to top and the Menu into Jemma’s Journals)

**Dark mode**
- Head script, `site/index.html:25` (one line, after `<meta name="theme-color" content="#EEEAF2">` at line 19 and before the stylesheet at line 26): reads `jj-mode`; if null reads `jsw-mode` and copies it over; always removes `jsw-mode`; sets `data-mode` light/dark on `<html>`; if dark sets theme-color `#1B1524`; catch → light. `<html … data-mode="light">` is also in the markup (line 2).
- Toggle, `js/app.js:1612–1628`: `MODE_KEY = "jj-mode"`, `modeBtn = #modeBtn`; `showMode()` (1613) fills `.ico` with `ic("sun"|"moon")`, `.txt` with “Light mode”/“Dark mode”, `aria-pressed`, theme-color `#1B1524`/`#EEEAF2`; click handler (1620) flips `data-mode` and saves (try/catch); `showMode()` on load (1626); `storage` listener (1628). No dark tab icon.
- CSS: tokens `:root{…}` `site.css:140–158`, dark `:root[data-mode="dark"]{…}` `160–169` (also sets `color-scheme:dark`), per-component dark fixes `172–181` and `1193`. Light `:root{color-scheme:light}` at line 130.
- Site-specific bits a shared module needs as settings: the two theme colours, the old key name (`jsw-mode`), the icon function (`ic()` from `js/icons.js`).

**Footer**
- Markup `site/index.html:41–44`: `<footer class="site-foot">` › `.foot-rule[aria-hidden]` with `<span class="dot">` (the map pin), `<b class="foot-name">`, `.about-site` (two `<p>`; credits as `<span class="cr">` separated by `<span class="sep" aria-hidden="true">&nbsp;·</span> `), `.foot-links` with `button#toTop.totop` and `button#modeBtn.mode-text[aria-pressed]` each holding `<span class="ico">` (+ `<span class="txt">` on the mode button). It sits inside `<main>` after `#view`, so on wide screens it is centred in the page column, not the window.
- CSS `site.css:651–666` (`#view{outline:none}`, `#view.wrap{padding-bottom:56px}`, `.site-foot`, `.foot-rule` + `::before/::after` dashed lines, `.foot-name` 24 px display, `.about-site`, `.sep`, `.cr{white-space:nowrap}`, `.foot-links` and its buttons 44 px, 13 px bold in `--water`); phone stacking `site.css:1160` inside the `@media (max-width:700px)` block (`.sep{display:none}`, `.cr{display:block}`). The pin is `.dot` styled elsewhere (`--c:var(--neat)`, `site.css:657`).
- JS `js/app.js:1629–1639`: `tidyCredits()` hides a `.sep` whose next credit starts on a lower line; run by a `ResizeObserver` on the credits `<p>` and after `document.fonts.ready`. (Extra to the family rule; the shared version can keep it.)

**Back to top**
- `js/app.js:1640–1644`: icon `ic("arrow-up")` into `#toTop .ico`; click → `scrollTo({top:0, behavior:SMOOTH()})` (`SMOOTH` at `js/app.js:32` honours reduced motion) and `#view.focus({preventScroll:true})` (`#view` has `tabindex="-1"`, `index.html:38`).

**Menu drawer**
- Markup `site/index.html:29–31`: `.topbar` › `button#menuBtn` (`<span id="menuIco">` + “Menu”) and `a.brand-bar[href="#home"]` “Jemma’s <em>Sim World</em>”; `div#scrim.scrim`; `aside#side.side[aria-label="Worlds"]` whose first child is `a.home-link[href="/"]`. `aria-controls` is added by JS, not in markup.
- JS `js/app.js:1508` (menu icon), `1572–1608`: `sideEl`, `menuBtn`, `phoneNav = matchMedia("(max-width:900px)")`; `drawerStart()` (1577) = current page’s visible `#nav a[href]`, else Home, else first link/input; `setNav(open, focus)` (1582) toggles `body.nav-open`, `aria-expanded`, `sideEl.inert` (phone and closed), `inert` on every `body > *` except `#side`, `#scrim` and scripts while open, `html.nav-lock`, focus in/out; listeners: Menu click, scrim click, Escape (1598), Tab wrap inside the drawer (1600–1606), `phoneNav` change → close (1607), `setNav(false)` on load (1608); `route()` closes it after navigation (`js/app.js:1401`). Search’s own Escape (`js/app.js:725`) stops propagation when it has text.
- CSS: `.topbar,.scrim{display:none}` `site.css:221`; `@media (max-width:900px)` `site.css:622–641` (`.side` translateX(-102%) + transition, `body.nav-open .side`, scrim rgba(0,0,0,.45) z 15, `html.nav-lock{overflow:hidden}`, `.side{overscroll-behavior:contain}`, `main{margin-left:0}`, `.topbar` sticky z 10, button 44 px, `.brand-bar` 26 px); purple name `site.css:1192–1193`; `.side` itself `site.css:195–196` (fixed, z 20), `.home-link` `198–200`; reduced motion `site.css:643`.
- Things a shared module must leave to the site: the drawer’s contents and `renderNav` (site-specific), the `inert` sweep’s exclusions (it assumes the drawer, scrim and top bar are direct children of `<body>`), and the focus-after-link step (Should fix 3).

## Tests result

`python -B -X utf8 tools/run_tests.py` in sim-world: **all passed**. Python: 387 tests, OK (2 skipped: the live-hook test, see Should fix 7, and one that needs the game). Site: 105 passed (1.0 min). It changed no files.
