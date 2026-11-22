# The family’s tests: audit and refactor, phase 1 (22 Nov 2026)

What tests exist across Jemma’s five sites and their tools, what each covers, how long each takes, where they repeat each other, what nothing tested before tonight, and what phase 1 added in the parent. Phase 2 (later, in each app, by its own session) removes the app tests listed in section 5.

## 1. The suites before tonight

| Suite | Where / how to run | What it covers | Time |
|---|---|---|---|
| Home page | `tests/check_page.js` (Node + Playwright, Edge) | Home at 1600, 1280, 390 (1000 added tonight): opens light, title, four places 2 × 2 and how it grows (`#more1–3`), only the photo and “Open …” are links, pictures load, footer and credits, dark mode button and icon flip, reload keeps dark, Back to top focus, robots, tab icons, the 404 page’s footer and mode button | ~35 s |
| Accessibility | `tests/axe_all.js` | axe-core serious/critical problems on 11 pages of all five sites, 1600/390, light/dark; a report, not a failure. Needed her 8050 server | ~1–2 min |
| Everything | `tools/check_all.py` | Ran the five suites above, axe, and git tidiness per app | ~20 min |
| Library | `library/tests/run_tests.py` (unittest; `unit` / `e2e`) | unit/ (server, build, importers, covers, backups, safety, ISBNs, reading watch, add book, scan…: 15 files) and e2e/ (an in-page harness, `harness.js`, run by `test_site.py`: `fixture.test.js` on a made-up library, `site.test.js` on her real books, `phone.test.js` at 390). 331 tests | ~2 min |
| Sim World | `sim-world/tools/run_tests.py` (unittest + `@playwright/test`) | 20 Python files (tools, build, data plan, gallery refresh, backups, imports, reviews) then 22 Playwright specs in `tests/site/` (pages, navigation, layout, look, keyboard, family words, calendar, CSP, family rules, footer/mode, reviews). 396 Python tests + the specs | ~3 min |
| Pokédex | `pokedex/tests/run_tests.py` (unittest; `unit` / `e2e` / `slow`) | unit/ (data, build, importers, calcy, server and its edges, family files and recording) and e2e/ (`site.test.js`, `keys.test.js` in the page, run by Python). 97 tests | ~3 min |
| Travels | `travels/tests/run_tests.py` (unittest; `unit`) | unit/ (server, data and build, world map) and e2e/`run.js` (every page at five widths, links, figures, banner, family rules, Write page, CSP, contrast) on a fixture and her real trips. 100 tests | ~11 min |
| Sheets and shots | `travels/tests/*.js` (banner_widths, family_shots, shoot, variants…), `*/tools/check_pages.js` | Screenshot and comparison helpers for choosing looks, not tests (no pass/fail) | — |

Timings are from logs/check-all (22 Nov, 01:50–02:08) and tonight’s runs.

## 2. Repeated in every app: the family rules

When the family rules (`research/family-rules.md`) were agreed on 21 Nov, each app’s session wrote its own tests for them, and again when the shared code moved to `site/family/` on 22 Nov. The same checks now exist four or five times, written four different ways (Playwright specs, two in-page harnesses, a Node script):

| Family rule | Home | Library | Sim World | Pokédex | Travels |
|---|---|---|---|---|---|
| Opens light with the device dark | ✓ | ✓ | ✓ ✓ | ✓ ✓ | ✓ ✓ |
| Dark mode button, `jj-mode`, reload keeps it, bar colour | ✓ | ✓ ✓ | ✓ ✓ | ✓ | ✓ ✓ |
| Old per-site key moved once | | ✓ | ✓ | | ✓ |
| Footer order, name, line 1, credits capitals | ✓ | ✓ | ✓ | ✓ | ✓ |
| Credit dots never at a line end; one per line on phones | | ✓ ✓ | ✓ | | |
| Back to top and Dark mode 44px, level; Back to top focus | ✓ | ✓ ✓ ✓ | ✓ ✓ | ✓ ✓ | ✓ |
| Drawer at 899/901; open/close by button, Escape, scrim, link; focus; inert; reset | — | ✓ ✓ ✓ ✓ | ✓ ✓ ✓ ✓ ✓ ✓ | ✓ ✓ | ✓ ✓ ✓ ✓ |
| Sizes: Menu 44px, bar name 26px, scrim 45%, back link 24px | — | ✓ | ✓ | | ✓ |
| Robots meta | ✓ | ✓ | ✓ | ✓ | |
| CSP present, no violations | | ✓ (harness) | ✓ (8 tests) | ✓ | ✓ |
| `/family/` files load, `JJFamily` there | | ✓ | ✓ | ✓ | ✓ |
| Fonts only local | | ✓ | | | |
| Each app’s own server serves `/family/` and nothing else | — | unit | unit | unit | unit |

None of them could test what only shows between sites: dark mode carrying from one site to another, the storage event between open tabs, home’s Open links and every app’s “← Jemma’s Journals”, or the family server itself.

## 3. Gaps after tonight’s moves (before phase 1)

Nothing tested:
- **`tools/serve_all.py`** (the family server, 8050): the Host check, path traversal (raw, encoded, backslash, NUL), size limits, the 404 page, no folder listings, `/family/mode` get/save with and without `X-Family`, writing the mode into every page, passing saves on to each app’s server, the 503 when one is down and starting it again, one copy only.
- **`tools/record_apps.py`**: its skip rules (uncommitted, not on main, not pushed), `logs/` ignored, only the apps in the commit, push failure.
- **`tools/weekly.py`**: the Sunday-or-overdue rule, one job failing not stopping the others, `travels_backup` (commit only the Write page’s files, no-op when nothing new, not on main, not pushing someone’s unpushed commits).
- **`tools/build_site.py`**: that every file a page asks for is in the build.
- **`tools/new_site.py`**: dry run, real run, running twice, `--add-to-home`, `--remove`, bad names.
- **`tools/open_site.pyw`**: the right address and Chrome profile per site, starting the server when needed.
- **The online-style copy (8060)**: everything loads, the apps view-only, no errors except the expected save-request 404s.
- **The shared code itself** (`family.js`, `mode.js`): which setting wins in `mode.js` (server choice, `jj-mode`, old key, junk, blocked storage) was only tested indirectly, per site.
- **Between sites**: dark mode carried across sites and across app windows with their own Chrome profiles (the server’s choice); the storage event; home’s Open links; every app’s “← Jemma’s Journals”.
- `tests/check_page.js` served `family.css` without a CSS content type, so Edge refused it and home was tested **without the family stylesheet**; two of its checks tested nothing (`.foot .credits`, `.sw`) (round 5 review).
- `tests/axe_all.js` crashed on Sim World’s first page once its CSP blocked the injected axe script, so it never reached the Pokédex or Travels.

## 4. What phase 1 added (in the parent only)

| File | What it does | Time |
|---|---|---|
| `tests/family/family.test.js` | The family rules for all five sites in one place, through **its own** test copy of the family server (spare port, temp dark-mode file, no app save servers) and the online-style build served like a plain host. 26 tests: opens light, no errors, no outside requests, no sideways scroll and no CSP violations at 1600/1280/901/899/390; robots and CSP (before any script, no inline scripts or handlers) on every site and the 404 page; `/family/` types, load order, `JJFamily`, old keys named; footer (name, line 1 from `family.js`, credits, order, 12.5px, buttons 44px and level); line 1 written in each page’s HTML; credit dots at 9 widths and one per line at 390; Back to top focus; dark mode (`jj-mode`, the server’s choice, bar colour, tab icon, reload); carry across sites and across separate browser profiles; the storage event; the drawer on the four apps (899/901, Menu word and icon, 44px, bar name 26px and italic, “← Jemma’s Journals” first, focus in on the page’s link, Tab stays in, Escape, scrim, link, scroll lock, page inert, reset over 900, no CSP violations); local fonts and no `prefers-color-scheme` styles; links between sites; the 404 page; online: everything loads, view-only apps, dark mode carry by `jj-mode` alone, links, 404; `mode.js` precedence (11 cases plus blocked storage) | ~7 min |
| `tests/family/serve_family.py` | The test copy of the family server (the real `serve_all.py` Handler; never her `logs/family-mode.txt`, never her app servers) | — |
| `tests/family/serve_build.py` | Builds with `build_site.py`’s own `build()` into a temp folder and serves it with its own handler | — |
| `tests/tools/test_serve_all.py` | 22 tests: Host check (other names, empty, wrong port, for GET/HEAD/POST), 14 traversal forms (raw `..`, encoded, double-encoded, backslash, drive letters), NUL, no listings, 404 page with the mode written in, every site and the shared code, the slash redirect, other methods refused, mode get/save with/without `X-Family`, bad values, from another name, mode written into every page with the right length, forwarding to a fake app server (path and query, only the listed headers both ways, errors passed through), Sim World has no save server, size limits (64 MB, negative, not a number), 503 and starting the server when one is down, starting only the missing app servers, a second copy exits, the port is not shared | ~10 s |
| `tests/tools/test_record_apps.py` | 13 tests on a throwaway family (bare “GitHub” remotes, parent with two submodules): recorded and pushed, two apps in one commit, nothing new, uncommitted and untracked work skipped, a backup’s `logs/` ignored, not on main, not pushed, other parent changes left alone, parent not on main, push failure, a missing app, every network call uses the GitHub CLI or nothing | ~80 s |
| `tests/tools/test_weekly.py` | 22 tests: `weekly_due` (Sunday, not when it ran lately, catching up, no good run, `--all`, `--daily-only`), reading the Gallery log, the jobs with stand-in scripts (Monday vs Sunday, one failure doesn’t stop the rest, missing script, Travels failure counted, nothing waits for a window), `travels_backup` on a throwaway repo (new posts committed and pushed, nothing new, only the Write page’s files, other staged work isn’t a backup, not on main, someone’s unpushed commits not pushed, push failure). Every git and job command is fenced to the temp folder | ~3 min |
| `tests/tools/test_build_site.py` | Every site is in the build; every file each page and stylesheet asks for is there; files named in the scripts (`img/…`, `data/…`) are there; no caches; under 1 GB; every page asks to stay out of search; and (expected failure, round 5) no notes or tools published | ~40 s |
| `tests/tools/test_new_site.py` | On a temp copy of the parent: dry run changes nothing; a real run makes the site with its own git, fills every placeholder and wires it in (each edited tool still compiles; the wiring means what it should); running twice changes nothing more; `--add-to-home` then `--remove` puts every file back byte for byte; bad folder names, display names and colours refused before anything is written; pale accents made readable | ~30 s |
| `tests/tools/test_open_site.py` | Each site at the family address, the Chrome profiles, unknown name → home, starts the server only when it isn’t running (detached, no window), falls back to the default browser | <1 s |
| `tests/tools/support.py` | Loads a tool as a fresh module; spare ports; `GitSandbox` (temp folder, git with a test config: no global settings, no sign-in helper) | — |
| `tests/check_page.js` (changed) | Real content types (family.css now actually applies); the two empty checks replaced (credits once in the footer; no Try switch left); every stylesheet has its rules; a 1000px width; home’s Open links and photos go to `/<app>/` on a plain host (round 5) | ~35 s |
| `tests/axe_all.js` (changed) | `bypassCSP` in its own context so axe can run; `--base` to use a test copy of the family server | ~2 min |
| `tools/check_all.py` (changed) | `--quick` = home page + family suite + tool tests + accessibility (on its own test server) + git checks; full = that plus each app’s own suite. The online-style build is made once and shared (`JJ_BUILD_DIR`). One line per part, logs in `logs/check-all/`, exit 1 on failure; a FAIL line, not a traceback, when Node is missing; the git check ignores `logs/` as `record_apps` does (round 5: every Pokédex backup failed it); “not recorded” is a note, not a failure | quick ~12 min |

## 5. Phase 2: app tests now duplicated by the shared suite

These check exactly what `tests/family/family.test.js` now checks for every site. Each app’s session can remove them (or the family part of them) in phase 2. “Partly” means keep the site-specific part named.

**Sim World** (`sim-world/tests/site/`)
- `family-rules.spec.js`
  - “opens light with the device set to dark; the button switches, saves jj-mode, changes the bar colour, and a reload keeps it”: remove
  - “her old choice ("jsw-mode") is kept once, moved to jj-mode; no dark styles hang off the device setting”: remove
  - “the footer, in the family layout, on several kinds of page (laptop)” and “(phone)”: partly (keep only its own credit wording, “World maps by 20th Century Plumbob”)
  - “the Menu bar shows at 899px and the sidebar at 901px; the bar has the Menu button and the name as a link home”: remove
  - “the drawer: button, Escape, scrim and a link close it; focus goes in and back; closed it is inert; crossing 900px resets it”: remove
  - “family sizes and small things: Menu button 44px, bar name 26px, scrim 45% black, back link 24px, robots meta, data-mode always set”: remove
  - “footer credits: a “·” never starts or ends a line, at any laptop width; 12.5px on phones too”: remove
  - “the family’s shared code loads from /family/ and does the shared parts (no own copies left)”: partly (keep the requests to its own test server: `/family/..%2findex.html` refused, `/family/` 404)
- `footer-mode.spec.js`
  - “Back to top goes to the top and moves keyboard focus to the start of the page”: remove
  - “the site opens light even when the device prefers dark”: remove
  - “Dark mode switches the page, says Light mode, and is remembered after a reload”: remove
  - “Back to top and Dark mode sit at the bottom of every kind of page (laptop)” and “(phone)”: partly (keep only “below the page on every kind of page”, which is Sim World’s routing)
- `csp.spec.js` “the page carries the agreed policy, before any script”: remove (the exact policy string is the only extra)
- `look.spec.js` “phone drawer: closed it is out of the Tab order; the button says open or closed; Escape closes it and focus returns”: remove
- `layout.spec.js` “on a phone the sidebar slides in from the menu button and the scrim closes it”: remove; “at 1280px the sidebar sits beside the page and the menu button is hidden”: partly
- `round4.spec.js` “the drawer: Tab and Shift+Tab stay inside for 30 presses each on several pages (the family’s one rule; no copy of Sim World’s own)”: remove
- `fixes-21nov.spec.js` “browser storage: … dark mode follows another window”: partly (keep the calendar key and “seen” list parts)

**Library** (`library/tests/e2e/`)
- `fixture.test.js`
  - “Back to top goes to the top of the page and moves keyboard focus there”: remove
  - “the site opens light, even when the device is set to dark”: remove
  - “Dark mode switches the page to dark and back, and the button says what it will do”: remove
  - “dark mode is remembered when the site opens again, and so is going back to light”: remove
  - “family rules: the foot of every page is the family’s, in order: the name, the two About lines, then Back to top and Dark mode”: remove
  - “family rules: dark mode uses the shared key jj-mode, moves the old key over once, and sets the bar colour”: remove
  - “family rules: the Menu bar shows at 899px wide and the sidebar at 901px”: remove
  - “family rules: the drawer at 899px: aria, focus in and back, inert, Escape, scrim, a link, scroll lock, and reset across 900px”: remove
  - “family rules: sizes: Menu 44px or more, the bar’s name 26px, the scrim black at 45%, “← Jemma’s Journals” 24px or more tall”: remove
  - “family rules: robots meta, data-mode always set, fonts only from the site itself”: remove
  - “family rules: the credits’ dots never start or end a line (a no-break space before each, lines balanced)”: remove
  - “family code: the page loads /family/mode.js, family.css and family.js, and window.JJFamily is there”: remove
  - “Back to top and Dark mode are at the bottom of every page, below the page’s own words”: partly (keep “every page”)
  - “family rules: the drawer opens on the page’s own link (Home when none), and everything outside it is inert while open”: partly (keep the other pages)
- `phone.test.js`
  - “the top bar shows the menu button and the library’s name; the sidebar is away”: remove
  - “the menu button opens the drawer over the page, with the way back to Jemma’s Journals at the top”: remove
  - “the drawer closes on Escape, and focus goes back to the button”: remove
  - “the drawer closes on a tap outside it”: remove
  - “Back to top and Dark mode sit side by side at the bottom of a phone page, big enough to tap”: remove
  - “family rules: on a phone the foot’s credits stand one per line, with no dots”: remove

**Pokédex** (`pokedex/tests/e2e/site.test.js`)
- “in a wide window the sidebar is there and there's no top bar”: remove
- “on a phone (390 wide): Menu opens the drawer; Escape, tapping outside and choosing a link close it”: remove
- “the family's shared code loads from /family/ (mode.js, family.css, family.js) and runs”: remove
- “Back to top scrolls to the top and moves focus to the top of the page”: remove
- “Dark mode: opens light, the button switches it, and it’s remembered after reloading”: remove
- “kept out of search engines and AI (family rules): robots noindex, noai, noimageai”: remove
- “the device's dark setting never switches dark mode on by itself (her rule: light unless pressed)”: remove
- “Back to top and Dark mode are at the foot of every page”: partly (keep “every page”)

**Travels** (`travels/tests/e2e/run.js`)
- “phone menu slides over the page and closes outside, by Esc and a link”: remove
- “family: opens light with the device set to dark; the button switches, saves jj-mode, changes the bar colour; a reload keeps it”: remove
- “family: her old choice (jt-mode) is kept once, moved to jj-mode; the mode is set before the page is drawn”: remove
- “family: the footer in the family layout on several kinds of page (laptop)” and “(phone)”: partly (keep its own credit wording)
- “family: the Menu bar shows at 899px and the sidebar at 901px; Menu on the left, then the name as a link home”: remove
- “family: the drawer: focus in and back, closed it is inert, page locked while open, crossing 900px resets it”: remove
- “family: the shared code loads from /family/ (mode.js, family.css, family.js) and runs (window.JJFamily)”: remove
- “Back to top sits beside Dark mode at the bottom and goes to the top”: remove
- “family: the drawer opens to the page’s own link (Home if none); while open Tab stays inside; focus back on Menu when crossing 900px”: partly (keep the other pages and the crossing-900 focus check)
- “family: the ← Jemma’s Journals link is at least 24px tall; opened as a file it goes to the Journals page, not the C drive”: partly (keep the file: part)
- “dark mode: light at first, the footer button switches and is remembered, text still readable”: partly (keep the contrast part)

**Home** (`tests/check_page.js`): its “family:” block (dark set elsewhere carries here and to the 404 page) is now in the family suite too; it is small and fast, so it can stay.

**Keep everywhere** (not duplicates): each app’s unit test that its *own* server serves `/family/` and nothing else (Library `test_server.py` “the family’s shared code is served” / “nothing else through family”, Sim World `test_family_serve.py`, Pokédex `test_family.py`, Travels `test_server.py` “test_family_shared_code”); every “no CSP violations on every page / with the buttons used” test (the family suite only opens each site’s first page); every contrast test; every “every page / every kind of page” sweep.

## 6. Gaps that remain

- **`tools/setup_pc.ps1`** (new-PC setup: task, Startup server, shortcuts) and **`tools/restart_family.py`**, **`tools/backup_new_sites.py`** (new tonight, being written by another helper): no tests.
- **Each app’s `backup.py`** is tested in its own suite (Library, Pokédex, Sim World); the round 5 review’s point that they commit with `git add -u` / `-A` (someone’s half-done work) is not tested anywhere.
- **The family suite opens each site’s first page only**: page-by-page sweeps (footer under every kind of page, CSP with every feature used, drawer start link on deeper pages) stay in the apps.
- **The family server’s mode carry between two different app windows at once** is tested by reload, not live: a window that is already open follows only through the storage event (same profile) or its own reload (another profile). The app-window follow added in round 5 (`a655695`) has no parent test yet.
- **A site opened as a file** (`file://`): only Sim World’s and Travels’ own suites cover it.
- **Axe** is still a report, not a failure (her OK was for a report).
- **`build_site.py` only copies files git tracks**: the build test reads the build, so a new file a page needs but nobody has committed shows as missing (see results), which is the right warning, but it depends on each app’s git state at the moment of the run.

## 7. Results of the first runs (22 Nov, afternoon)

`python tools/check_all.py --quick`: about 11 minutes.
- **Home page**: 149 checks passed (was 104; family.css now really loads; Open links and photos reach `/<app>/` on a plain host).
- **Family rules**: 18 of 25 passed at first. The failures were real, not test faults:
  - **Pokédex: the temporary Try switch (bottom right) covers the footer’s Dark mode button at 901px and below**, so on a phone she can’t press Dark mode while the switch is there. It goes when the switch is removed after she chooses.
  - **Online-style copy: Travels doesn’t draw its family parts** (no Dark mode button, footer line 1, drawer). Travels’ `index.html` (changed, not committed, by its own session) now loads `js/family-load.js`, which is a new file git doesn’t track yet; `build_site.py` copies only tracked files, so the build has the new page without the file it needs. It clears when Travels’ session commits `family-load.js`; it is also a reminder that the build mixes the working copy of tracked files with “tracked only” (a half-made change can go out broken).
- **Tools**: 79 tests, 1 failure (the same Travels `family-load.js`, from the build test), 1 expected failure (`site/family/README.md` is published).
- **Accessibility** (now reaching all five sites): one kind of serious problem, Pokédex box labels’ contrast on the generation pages.
- **git**: every app has uncommitted work from tonight’s helpers (expected while they work).

**A mistake in the first version of the record_apps test (fixed, no harm done, but recorded here):** `record_apps.git()` takes `cwd=ROOT` as a default argument, fixed when the module loads, so pointing `ROOT` at the temp family left its parent commands running in the real Jemma’s Journals. One test run made the commit `9123b26` “Record app versions: pokedex” in the real parent and pushed it. It recorded Pokédex at `447b320`, which was already on GitHub, on main, with nothing uncommitted except `logs/backup.log`: exactly the commit `record_apps` itself would have made, so it was left in place. The tests now send every git call to the temp family and refuse any other folder (and `test_weekly.py` fences `weekly.py` the same way).
