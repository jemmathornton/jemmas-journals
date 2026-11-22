# Review, round 5: the family (22 Nov 2026, about 13:30)

This was a read-only review, and I changed nothing in any repo. I compared `git status` in the parent and all four submodules before and after. The only differences came from other helpers who were working at the same time: Travels committed `3249f2e`, and the parent got `1c51270` (templates/new-site, tools/new_site.py) and `e4750ed` (Record app versions: travels). I did not review the new template or `new_site.py`, because they appeared during this review.
- That commit also changed one line in `site/home.js`: a place with no picture gets the striped stand-in. My home runs used the version just before it.
- Another helper also had an uncommitted edit to `CLAUDE.md` in progress (see Docs).

`logs/family-mode.txt` is unchanged (md5 `a82fd95…`, content `dark`). Every dark-mode press in the browser had its `POST /family/mode` answered inside the browser, so none reached the server. The raw POSTs I sent were refusal probes and cannot write: no `X-Family`, a bad value, a bad `Content-Length`, or a negative length with no body. I did not touch any task, shortcut or server.

**How I tested**
- Edge through the parent's Playwright, with service workers blocked.
- Sites tested:
  - `http://localhost:8050`: `serve_all.py`, pid 838312. It was started at 01:50, after the file's last edit at 01:27, so it runs the current code.
  - `http://localhost:8060`: `build_site.py --serve`, built at 12:58.
  - `file://` (home only).
- Raw-socket probes (`probe.py`).
- `tests/check_page.js`: **104 passed, 0 failed.**
- I did not run the apps' own suites (their helpers are editing them).

**Screenshots and data:** `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review5\family\`
- `shots\home-<8050|8060|file>-<1600|1280|1000|390>-<light|dark>.png`
- `shots\404-*.png`, `shots\more3-*.png`, `shots\toast-*.png`, `shots\app-<8050|8060>-<app>-1600.png`
- Results: `results-*.json`
- Scripts: `r5.js`, `probe.py`, `harness.js`, `toast.js`, `ent.js`

---

## Round 4 items: where they stand

| Round 4 | Now |
|---|---|
| SF1: connections refused under load | **Fixed.** 60, 150 and 300 connections at once were all answered (`request_queue_size = 128`) |
| SF2: home's theme colour stuck on dark gold | **Fixed.** Light → dark → light gives `#8E6520` → `#6A4A17` → `#8E6520` on 8050, 8060 and file. The four apps also restore both colours |
| SF3: stale preview servers on 8045, 8046 and 8040 | **Fixed:** none are running. But `.claude/launch.json` still defines them (see Should fix 9) |
| SF4: `menu()` could be set up twice | **Fixed** (`drawer._jjMenu`) |
| Minor: keepalive on the mode save; writing the mode file whole; the forwarded body limit | **Fixed** |
| Minor: `Content-Length` on `POST /family/mode` | **Not fixed.** `abc` drops the connection with a traceback. `-1` makes `rfile.read(-1)` wait until the client hangs up, and the thread stays held (measured: still waiting at the 3 s timeout). `serve_all.py:140` |
| Minor: HEAD isn't handled like GET | **Not fixed.** HEAD `/pokedex/api/collection` → 404, and HTML pages get no mode attribute |
| Minor: `setInert()` clears a site's own `inert` on the "outside" elements | Not changed (nothing relies on it yet) |
| Home's footer is not `.jj-foot` | Not changed: still `footer.foot`/`.foot-links`, so family.css changes won't reach home |
| Round 3 SF8: no home or Travels shortcut | **Still missing**, and `setup_pc.ps1` only makes the three app shortcuts |
| Round 3 SF9: old-folder leftovers | `research/app-styles/*/*.js` (10 scripts) still require `Documents/SimTracker/node_modules`, and `research/submodules-plan.md:23` still says Node lives in SimTracker |
| Round 3 SF11: home's Try-switch leftovers | **Partly fixed:** the `--sw-*` colours are gone. Still there: "navy cloth" (`index.html:33`, `:68`), the "As now … switch, bottom right" notes (`:21–27`), the `.v2` layer, and in `home.js:79` the "title on scroll" comment, `firstRender` (render runs once) and the unused `plus`/`image` icons |

---

## Broken

1. **On the online-style copy (8060), and online at her own domain, home's Open links don't open anything.** They show a toast saying "My Library opens here once the sites are online" instead.
   - Measured on 8060: clicking "Open My Library" stays on `http://localhost:8060/` and shows the toast. On 8050 the same click goes to `/library/`.
   - Cause: `home.js:6` treats a page as online only if it is on `*.github.io`, on `HOME_DOMAIN` (currently empty), or on localhost **port 8050**. So 8060 is "offline". If she moves to her own domain and nobody fills in `HOME_DOMAIN`, all four links are dead there too.
   - This defeats the point of 8060, which is "what works here works online". `check_page.js` didn't catch it (see Should fix 7).
   - Fix: turn the test round. Show the toast only where links truly can't work: `location.protocol === 'file:'`, or the Claude artifact host. Everywhere else, follow the link.

## Should fix

1. **The daily backup can commit and push someone's half-finished work.**
   - Library `backup.py` runs `git add -u`, so it commits every change to a tracked file. Pokédex `backup.py:98` runs `git add -A`.
   - Both then commit as "Weekly backup …" and push to the public GitHub, and `record_apps` records that version in the parent.
   - Right now both repos have helpers' uncommitted edits (`site/js/app.js`, `site/site.css`, `site/index.html` and tests). If the task ran now, those would go out half-done.
   - The task runs at 09:30 and catches up at login after the PC was off, which is exactly when she or a session starts work.
   - Fix: back up only data paths, as Travels does (Library `data/`, its covers; Pokédex `data/collection/`, the What's on files). Or skip the run and log it when code files are dirty.
2. **The Travels part of the daily backup commits the whole index, not just its own paths.**
   - `weekly.py:129–133`: `git add -- data site/photos site/js/data.js`, then `git diff --cached` (the whole index), then `git commit -m …` with no paths.
   - Anything a session had already staged in Travels goes in under "Posts saved up to …". Also, a staged unrelated change alone triggers a commit.
   - Fix: `git diff --cached --name-only -- <paths>` and `git commit -m … -- <paths>`.
3. **When the PC is off on a Sunday, the Sim World Gallery refresh is skipped for a whole week.**
   - `weekly.py:143` only checks `weekday() == 6`. The task's catch-up run happens on Monday, which isn't Sunday, so the refresh waits until the next Sunday (up to 13 days between runs).
   - Fix: run the refresh when the last successful one was 7 or more days ago (keep a date in `logs/`, or read `weekly.log`).
4. **The task's 1-hour limit is shorter than the jobs' own limits.**
   - `setup_pc.ps1:306` sets `ExecutionTimeLimit` to 1 h (and so does the live task: `PT1H`).
   - On Sundays the job limits add up to 1800 + 900 + 1200 s, plus Travels git (up to 600 s per call), plus record_apps 600 s: about 85 minutes or more.
   - If the Gallery is slow, Task Scheduler kills `weekly.py` in the middle, possibly during a git commit or push, and nothing gets logged.
   - Fix: set the limit to 3 h.
5. **Already-open app windows don't follow a dark-mode change made in another app window.**
   - The server attribute only arrives when a page loads, and the `storage` event only reaches tabs in the same Chrome profile. Her app windows each have their own profile.
   - Example: press Dark mode in the Library window. The open Pokédex window (a hash-routed app that never reloads) stays light until it is closed and reopened.
   - `GET /family/mode` already exists, but nothing uses it.
   - Fix: in family.js, when the page has `data-jj-server-mode`, fetch `/family/mode` on `visibilitychange` and `focus`, and apply the mode if it differs.
6. **Quick presses can leave the server's saved mode out of step with the page** (rare).
   - Each press sends its own keepalive POST. The threaded server can handle them out of order, so dark → light → dark quickly can leave `family-mode.txt` at `light`. The next window then opens light.
   - Fix (either):
     - Debounce the save by about 300 ms (send only the last).
     - Send a counter and have the server ignore an older one.
7. **`check_page.js` tests home without family.css, and misses the 8060 bug.**
   - `TYPES` (`check_page.js:10`) has no `.css`, `.js` or `.ico`. `family.css` is sent as `application/octet-stream`, and Edge refuses it in standards mode. The stylesheet object exists but has 0 rules (checked with the same route in `harness.js`). There was no console error, so the "no errors" check passed.
   - Also:
     - Two checks are empty: `creditsShown` looks for `.foot .credits`, which doesn't exist, and "trial switch gone" looks for `.sw`.
     - `wrap()` still handles the fragment page, which no longer exists.
     - The header still says it uses "the Playwright that her Sim World project already has".
     - There is no 1000 px width, and no check of the Open links on 8050 or 8060.
   - Fix:
     - Add `'.css': 'text/css', '.js': 'text/javascript', '.ico': 'image/x-icon'`.
     - Drop the dead checks.
     - Add one run against 8060 that clicks an Open link and expects `/library/`.
8. **`check_all.py` will always fail "git pokedex" after a backup.**
   - Every Pokédex backup leaves `logs/backup.log` modified: the log line is written after the commit, and it is modified now.
   - `check_all.py:216` only excuses `data/collection/go.json`. `record_apps` excuses `logs/`.
   - Also, "NOT recorded in parent" doesn't count as a failure, though the docstring lists it as a check.
   - Fix: use the same `logs/` rule as record_apps, and decide whether "not recorded" should fail.
9. **Five launch configs open apps that can no longer load the shared code.**
   - `sims-view` (8047), `pokedex-view` (8048), `simworld-live` (8045) and `travels-view` (8046) are plain `http.server` on an app's `site/`. Every app loads `/family/mode.js`, `/family/family.css` and `/family/family.js` from the root, so on those ports dark mode, footer line 1, the mode button and the Menu drawer are all missing.
   - `simworld-trial` (8044, `tools/trial_server.py`) has the same problem: it serves only `sim-world/site`. Its Try switch has also been removed for good (her pick was built).
   - `home` (8040) still works, because home uses relative `family/`.
   - Fix: delete these configs and `trial_server.py`, or point them at 8050.
10. **A new PC starts with every submodule detached, so the backups and recording silently do nothing.**
    - `git clone --recurse-submodules` (new-pc.md step 3) checks each app out at the recorded commit on a detached HEAD.
    - Then `record_apps.py` says "not on main, not recorded" for every app, `weekly.py`'s Travels part says "not on main, nothing saved", and Sim World's backup_push skips.
    - The Library recovers on its own if HEAD equals its local `main` (`backup.py:51`). The Pokédex backup commits on the detached HEAD and pushes `HEAD`.
    - Fix (either):
      - Add a step to new-pc.md: `git submodule foreach git checkout main`.
      - Have `setup_pc.ps1` run it.
11. **`setup_pc.ps1` can't find Python if "Add to PATH" wasn't ticked.**
    - `Get-Command python.exe` then finds the Windows Store alias `%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe`. Checked on this PC: it is second on PATH, and `WindowsApps\pythonw.exe` doesn't exist.
    - So `$pyw` becomes `…WindowsApps\pythonw.exe` and the script throws "Python not found". The fallback `…\Python313\python.exe` is never tried.
    - Fix: try the Python313 path first, or ignore any path under `WindowsApps`.
12. **The online-style build copies the working folder, not what's in git.**
    - `build_site.py` uses `copytree` on each `site/`, so `_site` includes:
      - git-ignored files (`library/site/covers/_straightened/` with 24 files, and `library/site/backup-status.json`)
      - every uncommitted edit, for example the 12:52 build has the Pokédex's in-progress **Try switch** (`shots\app-8060-pokedex-1600.png`)
    - So 8060 can work where the published site (built from git) would not, and the reverse.
    - Fix: build from `git ls-files` (or `git archive HEAD`) in each repo. Then 8060 matches a publish exactly.

## Looks (for her to judge; list only)

- `http://localhost:8060/` and `file:///…/site/index.html` at 360 px wide: the toast runs past both edges (−1 to 361 px). At 320 px it runs −21 to 341 px. At 390 px it fits with only 14 px each side (`white-space:nowrap`, `.toast` in `index.html:195`). See `shots\toast-8060-360.png` and `-320.png`.
- `http://localhost:8050/nope` (any 404) in dark mode: the tab icon stays the light one. `404.html` has no `data-dark` on its icon links, though home has them.
- `http://localhost:8050/`: home's footer is about 240 px tall at 1600 and 346 px at 390, set by its own `.foot` rules. Other sites follow family.css (see round 4's footer-height note).

## Shared code (`site/family/`)

I read every line. **No defects found beyond Should fix 5 and 6.**

| Check | Result |
|---|---|
| mode.js precedence | ✓ Server attribute > `jj-mode` > old key. Copied into localStorage on 8050. Old key removed. Blocked storage → light |
| `setMode` | ✓ Saves to localStorage. POST only when the server attribute is present (8060 and file sent **no** POST). Repaints. Listeners are wrapped in try/catch |
| `chrome()` | ✓ theme-color and icons swap both ways on home and the four apps (8050 and 8060) |
| `paint()` / MutationObserver | ✓ Watches `childList` on `body` only, once per frame. Button redrawn only when its mode differs, and line 1 only when its text differs, so there is no loop |
| `fitCredits` | ✓ No visible "·" ends a line at any width, base or mode. On phones the dots are hidden by CSS, `offsetParent` is null, so they are skipped. Note: a footer revealed by a class or `hidden` change (not childList) isn't refitted until a resize. No site does that today |
| Click handling | ✓ Mode button by mouse, Enter and Space keeps focus. Back to top moves focus to `#top` and `scrollY` = 0 |
| Storage event | ✓ (round 4) same-profile tabs follow. Cross-profile windows don't (Should fix 5) |
| Drawer at 899 px, all four apps | ✓ Opens to Home (Library: its name link). 30 Tab/Shift+Tab presses never left the drawer. Escape → focus back on Menu, `aria-expanded=false`, only the drawer is inert, the page lock comes off |
| CSP | ✓ No `securitypolicyviolation` on home, 404 or the four apps (8050 and 8060). family.js only uses CSSOM `style` and `innerHTML` with static SVG, which the policies allow |
| How the sites use it | ✓ All five load mode.js → family.css → family.js (defer) in head. Each has `data-old-key` (404 has none, as it should). All four apps use `.jj-foot`, `.jj-name`, `data-jj-line1`, `data-jj-credits`, `.jj-foot-links` and `data-jj-top="#view"`. Home doesn't (see the table above). Library leaves line 1 empty for family.js to fill; the others carry the text. All match the README |
| Online carry (8060) | ✓ Dark on home → Library, Sim World, Pokédex, Travels and the 404 all open dark from localStorage alone |

## Tools

**`serve_all.py` (security and behaviour)**
- ✓ Host check: 403 for `localhost.:8050`, `[::1]:8050`, a doubled Host header, `evil.example`, and NUL (`%00`).
- ✓ Absolute-form request lines get the 404 page.
- ✓ `/.git/HEAD`, `/logs/family-mode.txt`, `/library/../library/tools/serve.py` and `/library/.gitignore` all get the 404 page.
- `..%5c` → 301 to the app's index (harmless, as in round 4).
- ✓ PUT and OPTIONS → 501, and the apps only use GET and POST (checked every `fetch` in the four apps).
- ✓ A forwarded `Content-Length` of 99999999999 → 413.
- Open: the `/family/mode` length checks and HEAD (round 4 table).
- No socket timeout: a client that connects and sends nothing holds a thread for ever. Only this computer can connect, so this is low risk; setting `timeout = 30` on the Handler would close it.
- If an app server dies, every failed forward calls `start_app_servers()` again. Spares exit on the bind clash (Library, Pokédex and Travels all refuse to share a port), so this is harmless.

**`open_site.pyw`**
- ✓ Waits up to 8 s for the server.
- Home and Travels profiles are defined, but there are no shortcuts for them (round 3 SF8).

**`record_apps.py`**
- ✓ Commits only the app paths (`git commit -- paths`).
- ✓ Skips dirty, non-main or unpushed apps.
- Edge cases:
  - an app with **no upstream** gives an empty `rev-list` answer, which is treated as pushed, so a commit GitHub doesn't have could be recorded
  - untracked files in an app block recording (porcelain `??`)
  - it pushes any unpushed parent commits along with its own

**`weekly.py`**: Should fix 1–4.
- The `--daily-only` option is undocumented.
- The Library and Pokédex backups each also call record_apps, so it runs three times. That's harmless.

**`check_all.py`**: exit code is 1 if any suite or app git check fails ✓.
- Should fix 8.
- If Node is missing, it crashes with a traceback rather than a FAIL line.

**`build_site.py`**: Should fix 12. `_site` is 387 MB in 10,882 files (under Pages' 1 GB).
- It also publishes `site/tools/draw-icon.html` (a drawing tool, with no robots meta).
- It also publishes `site/family/README.md`.

**`setup_pc.ps1`**
- ✓ UTF-8 with BOM, so PowerShell 5.1 reads "Pokédex" correctly.
- ✓ Re-running it replaces its own task and shortcuts.
- The shortcut names mix apostrophes: "Jemma's Library" is straight and "Jemma’s Pokédex" is curly. That matches the existing Desktop and Start-menu files, so nothing is duplicated, but keep it that way.
- It doesn't remove the three old disabled tasks. That's fine, but it means a new PC has none of them while this PC still has them, disabled.
- The "Jemma's Library server" Startup item isn't recreated. It isn't needed, because serve_all starts it. On this PC it is still there and races serve_all at login, which is harmless (the second copy exits).
- Should fix 10 and 11.

**`trial_server.py`**: obsolete and broken (Should fix 9).

**`axe_all.js`**
- Home and 404, at 1600 and 390, light and dark: **0 violations** (I ran axe myself).
- Its "never saves anything" depends on routing POSTs, but the Library's service worker hides its requests from Playwright routing (round 4 note). Add `serviceWorkers: 'block'` to make that true.
- It sets `data-mode` directly, so sites that repaint through `JJFamily.mode.onChange` are checked in a half-dark state.

## Docs

- **CLAUDE.md is being edited by another helper as I write**, and the edit isn't committed yet (it adds ARCHITECTURE.md and a "Making a change" checklist).
  - The working copy already fixes these items from the committed version:
    - "separate repos, no submodules" and the `../../JemmasJournals/site/index.html` path
    - `PLACES` now said to be in `site/home.js`
    - record_apps now run by "the daily backup"
    - the three weekly tasks now marked disabled
  - Still out of date in the working copy:
    - **:42** "Sim World and Travels: she is fixing those herself", and **:90** "next job: dark mode, footer, Menu drawer, sidebar into `site/family/`". These are done, apart from the sidebar.
    - **:46–48** point at the `app-styles` and `simworld-trial` launch configs, which are gone or broken (Should fix 9).
    - Nothing yet on `build_site.py`/8060, `setup_pc.ps1`, `axe_all.js` or the CSP, unless ARCHITECTURE.md covers them. I did not review ARCHITECTURE.md; it appeared during this review.
- **research/family-rules.md** §1: "On her PC each local server is a separate address, so it can only carry once online…" is out of date. It now carries through 8050 and `data-jj-server-mode`, but only on load (Should fix 5).
- **site/family/README.md**: accurate. Its footer markup isn't what home uses (noted above).
- **for-jemma/new-pc.md**: missing the submodule `checkout main` step (Should fix 10). Also, step 4 says it "starts everything", but it makes no home or Travels shortcut.
- **research/going-online.md:41** "Separate repos, no submodules" and **research/drafts/publish-site-folder.yml** (`sim-tracker`, one app per repo) contradict the current plan: one build in the parent (`improvements-22-nov.md` §2). Mark them as superseded.
- I did not check the artifact link in CLAUDE.md:52 against the new `home.js` + CSP page.

## Online readiness: what still blocks it

1. **The address must be a domain root.**
   - Every app loads `/family/…`, links home as `/`, and home links `/sim-world/` and the others. robots.txt only works at the root.
   - As a project page (`jemmathornton.github.io/jemmas-journals/`) everything breaks.
   - So it needs the repo renamed to `jemmathornton.github.io`, or her domain. This is her decision (already in improvements-22-nov §2).
2. **Home's online test** (Broken 1): own domain plus empty `HOME_DOMAIN` means dead links.
3. **Publish workflow:** not written yet. It must:
   - build from git, not the working folder (Should fix 12)
   - upload with `actions/upload-pages-artifact`, so Jekyll doesn't run. If she ever publishes from a branch instead, a `.nojekyll` file is needed, or `_straightened` and any `_…` files are dropped
   - add `?v=` to `/family/` links (Pages caches for 10 min)
4. **View-only probes:** online, the Library still asks `api/reading-status` and the Pokédex asks `api/collection`. Each gives a 404 and a console error on every load (seen on 8060). The Pokédex fix in improvements-22-nov (only ask on localhost) is still open.
5. **robots and noindex:** present on all five pages. `site/tools/draw-icon.html` has neither and would be published. Leave it out of the build.
6. **404:** ✓ works on 8060 and 8050 for `/nope`, `/library/nope` and `/sim-world/x/y/z`, with root-absolute paths, dark mode and fonts.
7. **CSP:** ✓ on all five, with no violations. The Library's `img-src` allows `https:` for the Add-a-book lookups, which are PC-only. Online it could be tightened, to keep the footer's "no tracking" strictly true.
8. **Size:** 387 MB, fine (improvements-22-nov expects about 330 MB after the picture work).

## Home, measured (8050, 8060 and file; 1600/1280/1000/390; light and dark: 24 runs)

- ✓ Standards mode, layout width equals the window, no sideways scroll.
- ✓ 4 cards: 2 rows at 1600, 1280 and 1000; 4 rows at 390.
- ✓ No broken images, no CSP violations, no errors or failed requests. All three fonts load.
- ✓ The right icon, theme colour and button text for the mode.
- ✓ No credit dot at a line end.
- ✓ Keyboard order: Skip → (photo, Open) × 4 → Back to top → Dark mode. Every focus has a 2 px outline. Skip then Tab lands on the first photo.
- ✓ The entrance plays once (8 animations) and not with reduced motion. A mode press only runs colour transitions; it doesn't replay the entrance.
- ✓ `#more1–3`: 3+2, 3+3 and 3+3+1 at 1600 and 1000; one column at 390; no sideways scroll. A stand-in shows "A new place would go here".
- ✓ 404: status 404, the family footer, and the mode button works, on 8050 and 8060.
- ✓ axe: 0 violations on home and 404 (1600 and 390, light and dark).
