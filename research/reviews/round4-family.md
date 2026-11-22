# Review, round 4: the family after the shared code (22 Nov 2026, about 01:15)

This was a read-only review, and I changed no repo. The parent's `git status` is the same as at the start: only the untracked `for-jemma/concepts/app-styles/built/round3/`, which was already there. I did not touch any shortcut or scheduled task.

The two-browser test had to do real dark-mode saves through `POST /family/mode`. After each test I wrote `logs/family-mode.txt` back to exactly what it held before (`light`). Its content is still `light`. Every other POST I sent was a refusal test: no `X-Family`, a wrong value, a wrong Host, or a non-number `Content-Length`. None of those can write.

**How:** Edge (the parent's Playwright) against the real `http://localhost:8050` (`serve_all.py`, pid 707072). That process was started at 00:31:36, after the file's last edit at 00:31:16, so it runs the current code. The app servers behind it were all up: 8020, 8030 and 8041. I also used raw-socket probes in Python (`probe.py`).

**Pictures and data:** `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review4\family\`
- `footers-1600-light.jpg`, `footers-1600-dark.jpg`: the five footers stacked. Footers next to a sidebar are narrower and were scaled up to 1600, so their size in these pictures isn't a real difference.
- `footers-390-light.jpg`, `footers-390-dark.jpg`: the five footers side by side
- `shots\home-<8050|disk>-<width>-<mode>.png`, `shots\foot-*.png`, `shots\drawer-<app>-899.png`
- `results.json`, `probe.json`; scripts `r4.js`, `r4b.js`, `probe.py`

---

## Not fixed (from round 3)

| Round 3 | Now |
|---|---|
| Broken 1: home has no doctype or viewport | **Fixed.** `CSS1Compat`, 390 lays out at 390, `lang="en-GB"` |
| Broken 2: the Host check was bypassed | **Fixed.** 403 for any other Host on GET, HEAD and POST (`evil.example:8050`, `localhost` with no port, `localhost:8050.evil`, an empty Host, HTTP/1.0 with no Host). It accepts `localhost:8050` and `127.0.0.1:8050`, in any letter case |
| SF1: 2 s delay | **Fixed.** Forwarded calls take 0.003–0.017 s |
| SF2: a malformed request crashes the handler | **Fixed.** The answers are 505, 414 and 400 |
| SF3: Python's bare error page | **Fixed.** `site/404.html` with status 404, for GET and HEAD, also under `/library/…` (its paths are root-absolute, so it draws correctly there) |
| SF4: folder listings | **Fixed.** `/family/`, `/img/` and `/library/covers/` now give 404 |
| SF5: headers | **Not changed.** Only Content-Type and Cache-Control come back from the apps, and the query is still dropped on `/library?x=1` → `/library/`. No app needs these today |
| SF6: the Travels server isn't started | **Fixed.** `start_app_servers()` runs at start and after a failed forward |
| SF7: port clashes | **Fixed.** `sims-view` is on 8047 and `pokedex-view` on 8048 |
| SF8: shortcuts not through 8050 | **Fixed for the three apps** (see Results 7). There is **still no Desktop or Start-menu shortcut for home or Travels**, even though `open_site.pyw` supports both |
| SF9: old-folder leftovers | **Partly fixed.** Fixed: `sim-world/tools/sync_notes.py` now works out the new memory folder, `travels/CLAUDE.md` is fixed, and line 3 of `submodules-plan.md` is fixed. **Still there:** `research/app-styles/*/*.js` (11 scripts still require `Documents/SimTracker/node_modules/playwright`), `research/submodules-plan.md:23` (Node in SimTracker), and `sim-world/claude-notes/app-shows-main-checkout.md:11` (still `Documents\SimTracker\site`) |
| SF10: a credit dot at a line end | **Fixed.** No visible dot ends a line, at any of the four widths, from 8050 or from disk |
| SF11: home's Try-switch leftovers | **Not fixed.** `site/index.html` still has the `--sw-*` colours (lines 32 and 37 area), "navy cloth" (line 31), the "As now" and switch notes (lines 21 and 25), and the `.v2` layer |

## New problems

### Broken
None.

### Should fix

1. **The family server refuses connections when many arrive at once.** This is the "refused connections" another reviewer saw.
   - `Server` (`tools/serve_all.py:182`) keeps Python's default `request_queue_size = 5`. Windows refuses a connection outright once that queue is full.
   - The server also answers HTTP/1.0 (no keep-alive), so every picture is a new connection.
   - Probe results: 20 at once were all fine. **60 at once: 1 refused. 150 at once: 41 refused.**
   - In a normal Edge page load of home, **6 pictures failed with `ERR_CONNECTION_REFUSED`** (`img/wall/38.webp`, `05`, `19`, `26`, `33`, `img/maps/region-johto-kanto.webp`).
   - At login, the Startup server plus several app windows opening together makes this likely.
   - Fix: add `request_queue_size = 128` to `Server`.
   - Optional: `protocol_version = 'HTTP/1.1'`. Every reply already sends Content-Length, but check the redirect and error paths.
2. **On home, the top-bar colour (theme-color) gets stuck on dark gold after switching back to light.** In her app windows that is the window's title-bar colour.
   - To reproduce: open home in dark, press Light mode. The page goes light, but `theme-color` stays `#6A4A17`, and `data-light` is also `#6A4A17`.
   - Cause: home's own leftover mode code, `applyMode()` at `site/index.html:279`, changes `content` to the dark colour before `family.js` runs. `family.js:47` then saves that dark value as the light one.
   - The four apps are fine (checked: light and dark colours both restore).
   - Fix: delete home's own mode code (`site/index.html:268–282`: `userMode`, the `jj-mode`/`jj-mode2` reading and `applyMode`). `mode.js` and `family.js` already do all of it. Or put `data-light="#8E6520"` on the meta tag.
   - Removing that code also drops a second, competing place that reads `jj-mode`. Keep the `#dark`/`#light` address words only if the checks need them.
3. **Leftover preview servers still use the old folders.** Three `http.server` processes have been running since yesterday evening:
   - 8045 serves `Documents\SimTracker\site`
   - 8046 serves `Documents\Travels\site`
   - 8040 serves `--directory concepts` (that folder no longer exists in the parent)

   So the old folders aren't quite unused, and anyone opening those ports sees old copies. Stop them (pids 474936, 587588 and 587408) before the old folders are ever deleted.
4. **`JJFamily.menu()` has no guard against being set up twice** (`site/family/family.js:115`). A second call on the same button adds a second click listener and a second Escape listener. Each click then opens and immediately closes the drawer.
   - Pokédex and Travels guard against it themselves (`if (menu …) return`). Library's `startFamily()` (`library/site/js/app.js:1414`) and Sim World's `familyReady()` don't, but each is only called once today.
   - Fix it once in family.js: keep the controller on the drawer (`if (drawer._jjMenu) return drawer._jjMenu`).

### Minor (shared code and server; fine to leave)
- `setInert()` (`family.js:129`) sets `inert = false` on every "outside" element at start-up and on each close. That would undo a site's own `inert` on anything in that list. Library's list is every child of `<body>`, so a future Library dialog made inert for its own reasons would lose it. Nothing does that today.
- The save in `setMode` (`family.js:38`) is a plain `fetch`. `keepalive: true` would make it survive leaving the page at once. I tested "press, then leave straight away" 12 times and it was never lost, so this is only a safeguard.
- `logs/family-mode.txt` is written in place (`serve_all.py:141`). A page read in the moment between emptying and writing the file would see "light". Writing to a temporary file and renaming it (`os.replace`) closes that gap.
- `Content-Length` isn't checked before it's used.
  - A non-number drops the connection with a traceback (`serve_all.py:137`, `:151`).
  - A negative number makes `rfile.read(-1)` wait until the client hangs up.
  - Forwarded bodies have no size limit at 8050 (the apps limit them themselves).
  - Only this computer can reach the server, so this is low risk.
- HEAD isn't handled like GET.
  - HTML pages don't get the mode attribute, so HEAD's Content-Length is 28 bytes shorter than GET's (25958 against 25986 on `/`).
  - `/…/api/…` gets a 404 instead of being forwarded.
- `/sim-world/api/x` → 404 without Cache-Control (harmless).
- Home's footer is not the README markup: its own `footer.foot` with `.foot-links`, not `.jj-foot` and `.jj-foot-links`. It looks the same and passes every footer check, but family.css footer changes won't reach home.

## Looks (for her to judge; list only)
- Sim World's pin divider is still half cut off by the footer's top edge (1600 and 390).
- The Pokédex footer still has the binder's shaded strip on its left.
- Library at 1600: the credit dots still sit tight against the word before them ("publishers·", "Library·"). The other sites have a space on both sides.
- Footer heights still vary (206–251px at 1600; 291–346px at 390). Only Library has the ❦ ornament.
- A dot hidden at a line end (`visibility:hidden`) still takes up its width, so that line sits a few pixels off centre (home and Sim World at 1600).

## Shared code (`site/family/`)

| Check | Result |
|---|---|
| Painting loop (MutationObserver) | ✓ no loop: 0 DOM changes in 2 s idle on all five. A mode press causes 7–13 changes, then nothing. The button is only redrawn when its painted mode differs, line 1 only when its text differs, and the observer watches `childList` on `body` only (attributes and head are not watched) |
| Flicker | ✓ none seen. `fitCredits` clears and re-hides inside one frame, and visibility doesn't change layout |
| `fitCredits` cost | ✓ 0.03–0.09 ms a call. It runs at most once a frame after DOM changes, and 100 ms after a resize |
| `fitCredits` correctness | ✓ the hidden dots are exactly those where the next credit starts a new line. None are visible at a line end; phones hide all dots |
| mode.js precedence | ✓ server attribute > `jj-mode` > old key. On 8050 the server value is copied into localStorage. An old key is moved over once and then removed, with or without the server (Library `jemmas-library-mode=dark` → dark online; on 8050 the server's `light` wins and the old key is removed). Blocked storage: opens light, no errors |
| Storage event (same browser, two tabs) | ✓ Library pressed dark → the open Pokédex tab turned dark at once, button "Light mode", `aria-pressed=true`; back again ✓ |
| Globals | ✓ only `window.JJFamily`. mode.js leaves nothing behind. No app defines `JJFamily` |
| Load order | ✓ on all four apps: `mode.js` (blocking, in head) → `family.css` → `family.js` (defer) → the app scripts. Each app starts its drawer once family.js has run (Library's app.js is deferred after it; the others wait for DOMContentLoaded) |
| JJFamily.menu: open on a wide screen | ✓ ignored (`open()` returns when not narrow) |
| Resize while open | ✓ at 899 → 1100: closed, scrim hidden, no inert left anywhere, focus stays on the visible sidebar link. Back at 899: focus moved to Menu, closed drawer inert |
| Focus | ✓ opening goes to this page's link (Library: the name, its Home; others: Home). Escape and the scrim → Menu. A link → the page (`#view`) |
| inert restored | ✓ opened: the top bar, page and skip link are inert (Library also its trial switch). Closed: only the drawer. Tab never reached a closed drawer in 25 presses (all four) |
| Page lock | ✓ `overflow:hidden` on html and body while open, removed after |
| Multiple inits | ✗ not guarded in family.js (Should fix 4) |

## Server (`tools/serve_all.py`)

| Check | Result |
|---|---|
| Host check | ✓ GET, HEAD and POST all 403 for a wrong or missing Host |
| Traversal | ✓ nothing escapes. Raw `..`, `%2e%2e`, `..%2f`, `%252e`, `..%c0%af`, `/library/../sim-world/../../`, `/.git/config`, `/tools/serve_all.py`, `/logs/family-mode.txt`, `/site/index.html`, `C:/Windows/win.ini`, `//evil.com/` all give the 404 page. Backslash forms (`..\..\`, `..%5c`, `C:%5c…`) are dropped as one path piece: they redirect to the same address plus `/`, which opens the app's own index. Odd, but harmless |
| `POST /family/mode` | ✓ no `X-Family` → 405; `X-Family: 0` → 405; another `Origin` without the header → 405; value `purple` or empty → 400; `OPTIONS` (preflight) → 501, so another site's page can't send the header. Real saves work (dark and light, written to the file) |
| Body limits | ~ `/family/mode` reads at most 16 bytes ✓. Forwarded bodies have no limit, and Content-Length isn't checked (Minor) |
| App server down | ✓ by reading the code: a 503 naming the app, then `start_app_servers()`. I didn't stop a real server to test it. All three were running, and Travels 8041 had been started by it (pythonw `travels/tools/serve.py` at 00:50) |
| Mode attribute in pages | ✓ `/`, `/404.html`, the 404 page for `/no-such-page` and `/library/no-such`, all four app pages, and `/tools/draw-icon.html`. It goes into the first `<html` after the doctype. No served page lacks `<html>` |
| Caching | ✓ `no-cache` on pages, files, redirects and the 404 page. `/api/` keeps the app's own Cache-Control (`no-cache`). Types: `text/javascript`, `text/css`, `text/plain` for robots.txt |
| Concurrency | ✗ backlog of 5 (Should fix 1) |
| Forward speed | ✓ 0.003–0.017 s |

## Results

1. **Round 3 items:** see Not fixed. Both Broken items and SF1–4, 6, 7 and 10 are fixed. SF8 and SF9 are partly fixed. SF5 and SF11 are not.
2. **Shared code:** solid. One real bug is in home's leftover code, not in family.js (Should fix 2). One robustness gap in `menu()` (Should fix 4).
3. **Server:** secure as tested. Refused connections under load (Should fix 1).
4. **Dark mode across her windows:** ✓ two separate browser contexts (like her separate Chrome profiles) through 8050. For each pair home→Library, Library→Pokédex, Pokédex→Travels, Travels→Sim World and Sim World→home, I pressed dark and then light in context A. Context B then opened the other site, and **10/10 matched**, through `data-jj-server-mode`, and the file followed. Online style (server attribute removed, service workers blocked): home → all four apps dark from localStorage alone, light carried back, and **no** `/family/mode` POST was sent.
   - Note: the Library's service worker hides page requests from Playwright's routing. Any test that rewrites pages needs `serviceWorkers: 'block'`.
5. **Home at 1600, 1280, 1000 and 390, light and dark, through 8050 and from disk (16 runs):**
   - ✓ standards mode, layout width equal to the window, no sideways scroll, robots meta present
   - ✓ dark icon and theme colour when opened dark, no credit dot at a line end, no page errors
   - ✓ the 6 refused pictures (Should fix 1) were in a separate run
   - `tests/check_page.js`: **104 passed, 0 failed**
6. **Family through 8050:** ✓ footer order, name 24px Instrument Serif, line 1 exact on all five, buttons 44px tall and level, 13px. The drawer behaves the same on all four apps (table above). robots `noindex, noai, noimageai` on all five. **No outside requests** in any run.
7. **Shortcuts, Startup and tasks (read only):**
   - ✓ Desktop and Start menu: "Jemma's Library", "Jemma's Sim World" and "Jemma's Pokédex" run `pythonw tools\open_site.pyw library|sim-world|pokedex` in `Documents\JemmasJournals`, with icons from the new folders
   - ✓ Startup: "Jemma's Journals server" (`serve_all.py`) and "Jemma's Library server"
   - ✓ The three scheduled tasks (Library backup, Pokédex backup, Sim World Gallery refresh) are Ready and run from `Documents\JemmasJournals\<app>\tools`
   - ✗ No home or Travels shortcut
   - Old folders: still on disk (her choice). Nothing in the parent's tools, site or the shortcuts uses them, but three stale preview servers do (Should fix 3)
   - Also noted: the Library server listens on the Wi-Fi address at port 8021 for the phone scanner (her yes, 21 Nov), as its notes say
8. **`tools/check_all.py --quick`: skipped.** Three suites were already running (`tests/run_tests.py` ×2 and `tools/run_tests.py`, started 01:08), plus a Library `build.py`.
