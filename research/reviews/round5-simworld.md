# Review, round 5: Jemma’s Sim World (22 Nov 2026, afternoon)

Read-only. Nothing in `sim-world` was edited, built or committed: `git status` clean before and after, still at e9cfa3c. No POST reached a server (every POST was aborted or answered inside the browser), so the family server’s stored mode (`logs/family-mode.txt`) was never touched by this review. The parent moved on during the review (368eb32 → cd4b121, plus uncommitted edits to `CLAUDE.md`, `README.md`, `research/family-rules.md`): that was another session, not this one.

**How it was checked** (Edge through Playwright, `http://localhost:8050/sim-world/`):
- **Crawl:** every internal `#link` (and `data-lot-link`) on every page, starting from Home. 1,120 pages reached: 25 worlds, 81 neighbourhoods, 359 lots, 25 household lists, 159 households, 422 Sims, 11 clubs, 8 dynasties, 6 organisations, Calendar and 14 world calendars, the 5 Across-the-worlds pages and 3 Admin pages. All 1,355 picture addresses found were fetched with GET.
- **Sweep:** 48 pages (every page type, plus the five deep-colour worlds and the heaviest pages) at 1600, 1280, 1000, 901, 899 and 390, light and dark. That is 576 loads, each scrolled to the bottom so lazy pictures load.
- **axe-core:** 29 pages at 1280 and 390, light and dark.
- **Scripted checks:** keyboard, focus, the drawer, dark mode carrying across sites, Back to top, Back/Forward, the lightbox, today’s four changes, data consistency, page weight, and a text scan of all 1,120 pages.
- **Test suite:** run once.

**Watch out when testing on 8050:** the family server writes `data-jj-server-mode` into the page, and that beats `jj-mode` in localStorage. The stored mode is currently **dark**, so any check that sets dark or light through localStorage alone actually runs in dark. My first sweep did exactly that, so it was rerun with the attribute removed from the page.

Screenshots: `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review5\simworld\`
- `<page>_<width>_<light|dark>.jpg`: every swept page at 1600, 1280 and 390.
- `full\`: full-page shots of 10 key pages at 1280 and 390.
- `today_*.jpg`, `tree_390_bella.jpg`, `drawer_open_390_willow.jpg`, `calendar_390_light_view.jpg`.

Scripts and raw results are one folder up (`crawl.json`, `sweep-light.json`, `sweep-darkserver.json`, `axe.txt`, `interact.txt`, `perf.txt`, `text.json`).

**Clean everywhere** (1,120 pages crawled, 576 swept loads):
- No dead links: no internal link opens “Page not found”.
- No console errors, no CSP violations, no failed requests, no broken pictures, no requests to other sites.
- No sideways scroll at any width, no undefined/NaN/null, no straight apostrophes, exactly one H1 per page, no duplicate ids.
- Never more than one `aria-current`.
- Footer on every page: line 1 word for word (“…JavaScript and Python…”), 12.5px, both buttons 44px and level, no “·” at a line’s start or end, five credit lines at 390.
- Menu bar at 899 and 390 only; closed drawer inert; theme colour #EEEAF2 / #1B1524.

---

## Today’s changes: all hold

- **Purple “Sim World” on the home banner:** rgb(91,75,176) in light and #B7A8F7 in dark, the same as the sidebar name.
- **Squared plates on Sim and household pages:** family-tree person cards, “Their groups” cards and dynasty/club/organisation badges are all 2px. Club, dynasty and Families pages keep their rounded cards (14px / 99px), as intended.
- **Deep-colour initials:**

  | Household (world) | Disc | Contrast |
  |---|---|---|
  | Cahyaputri (Tomarang) | #0F332C, white | 13.7:1 |
  | Perry (Gibbi Point) | #0F2A40 | 14.7:1 |
  | Cahill (StrangerVille) | #4A1D1E | 14.1:1 |
  | the Watsons (Henford-on-Bagley) | #232E1F | 14.2:1 |
  | Goth (Willow Creek, for comparison) | keeps its own #2E6F80 | 5.7:1 |

  Late relatives are dark letters on grey, 7.0:1. The same in both modes.
- **CSP meta:** no violation on any of the 1,120 pages, in light or dark. Inline scripts are really blocked: axe could not be injected without `bypassCSP`. **This breaks the parent’s `tests/axe_all.js`** (see Tests).

## Past fixes: did they hold?

All of round 4’s Sim World items hold:
- **Opened as a file:** the scrim is hidden in the markup, and `html.no-family` is tested.
- **`aria-current`:** none on club, dynasty, organisation or world-calendar pages; old Stats links mark Progress.
- **Tab in the drawer:** stays inside for 40 Tabs and 10 Shift+Tabs, on 8 pages at 899 and 390. One copy now, in family.js.
- **Footer dot rule:** now scoped, so the map pin shows on phones.
- **Low-contrast leftovers:** fixed and tested.
- **serve_all.py queue:** now 128. No refused connections, even with two sweeps running together.

Round 3’s Looks: the gold home title and the rounded Sim-page cards were done today. Still open: the clipped organisation chip and gold one-word titles on bright maps (see Looks).

---

## Broken

Nothing broken on the pages.

## Should fix

1. **A Sunday the PC is off means no Gallery refresh that week, and Admin says otherwise.**
   - Since today the refresh is run by the parent’s daily job, `tools/weekly.py` (task “Jemma’s Journals - backup”, 09:30, catches up after). It runs Sim World only if *today* is Sunday (`weekly and not sunday: continue`).
   - If the PC is off all Sunday, Monday’s catch-up skips Sim World, and so does every day until the next Sunday.
   - Meanwhile Admin, At a glance (`site/js/sections.js:146–156`) still says “Runs every Sunday at 07:54 (08:54 in summer time) while you’re signed in” and “Sunday’s run hasn’t happened yet; it catches up next time you’re signed in”. Both are now wrong. Its `lastSunday()` also still counts from 07:54 UTC, not 09:30 local.
   - The old task “Jemma’s Sim World - weekly Gallery refresh” is Disabled. The new task has never run yet (first Sunday run 29 Nov).
   - *Fix:* in weekly.py, run the refresh when the last good run in `logs/gallery-refresh.log` is 7 or more days old (or it’s Sunday). Then update the Admin card’s words and time, and `tests/site/versions.spec.js`.

2. **Lot pages: “✓ Built” and “✓ Shared” fail contrast in light mode.**
   - Green #2E8B57 on the lilac facts plate #ECE8F0 is 3.51:1 (13px). Seen on `#l-oasis-springs--rio-verde` and `#l-sulani--admiral-s-wreckage`, at 1280 and 390; any lot with those ticks will show it.
   - It most likely came with the town-plan look on inner pages, which gave the facts plate its lilac background.
   - *Fix:* a darker green for `.progress .yes` on `html[data-inner]` (about #23704A).

3. **Two other small contrast misses (axe, serious):**
   - On `#s-cordelia-thebe-v`, light: the trait chips and the bonus trait are #886F3E on #F4F0E6, 4.2:1 (4.27 for the bonus).
   - On `#h-forgotten-hollow--straud`, dark: the “Vampire” life-state chip `.state.occult` is #7C62D6 on #1E1827, 3.76:1.

4. **Lot pages load every full-size screenshot up front.**
   - The carousel puts all slides’ 1920px JPGs in one horizontal track. `loading="lazy"` does nothing there, because the off-screen slides are inside the browser’s lazy-load margin.
   - `#l-oasis-springs--rio-verde` downloads 3.8 MB in 45 requests before anything is clicked (304–468 KB per photo). Every picture also has a 720px `.thumb.jpg` beside it.
   - On her PC this is instant; online on a phone it isn’t.
   - *Fix:* only the first slide gets `src`, the others get `data-src`, filled when that slide is shown.

5. **Stale notes after today’s changes:**
   - `sim-world/CLAUDE.md` still gives footer line 1 as “Made with HTML, CSS and JavaScript”, and says the refresh “runs by itself every Sunday at 07:54 … as the Windows task ‘Jemma’s Sim World - weekly Gallery refresh’” (that task is now disabled; the parent’s daily `tools/weekly.py` runs it).
   - The parent’s `CLAUDE.md` (“Her picks after the second review”) also still has the old line-1 wording.

## Looks (list only: for her to decide)

- **The end of a world’s description can never be read.** The banner text is cut at three lines with “…” (`site.css:926`), and the rest isn’t shown anywhere else on the page.
  - `#w-britechester` hides half of it (173px of 86px). `#w-willow-creek`, `#w-sulani`, `#w-henford-on-bagley` (“…Villagers…”) and `#n-henford-on-bagley-finchwick` are the same.
  - She sees the text stop mid-sentence. `#w-tomarang` shows “legends of lore.…”: the game’s own “...” plus the cut.
- **On a phone, the family tree is cut at the right edge.** On `#s-bella-goth` at 390, “Member” reads “Memb” and “Young Adult” reads “You” (`tree_390_bella.jpg`). The tree box scrolls sideways (412px of tree in 356px), but nothing says so.
  - The Goth household (872px) and Cordelia Thebe V (1,488px) need a lot of sideways swiping too.
- **Gunther Goth’s initial disc is plain grey** on Bella’s and Cornelia’s pages (the “no home” grey). Next to Cornelia’s late-relative grey, it reads as if he were deceased too.
- **Organisation page:** the chip “Best of Friends · Britechester” on `#g-org-art-society` is still clipped by a few pixels at 1280 and 1000 (round 3).
- **Gold one-word world titles on bright maps:** Britechester, Sulani, StrangerVille, Tomarang. Still her open Question A.
- **The calendar on a phone:** still her open Decide.

## Data

- **Totals and neighbourhood cards disagree.** The world banner and the home tile count the game’s own lots, but the neighbourhood cards don’t.
  - `#w-willow-creek`: 22 lots, but its cards add up to 21 (Sylvan Glade is in the total, not in Foundry Cove’s “5 lots”).
  - The same happens in Oasis Springs (22 vs 21), Selvadorada (8/7), Del Sol Valley (12/11), StrangerVille (12/11) and Mt. Komorebi (17/14).
  - Everything else agrees: home tile = world banner = Households page, for all 25 worlds.
- **One-sided partners in the data:**
  - Gunther Goth → Cornelia (Spouse) with nothing back.
  - Jacques Villareal → “Villareal mother” (Late Spouse).
  - Adekoya → Imani Darong (Late Spouse).
  - Colin Sullivan → Xochitl Luna (Late Spouse).

  The pages read correctly because the relationships are worked out both ways, but `data/people.json` is the only place that knows. A data check would keep it tidy.
- **Family trees:** no Sim is their own parent, no one has more than two parents, every parent id exists. The three “Unknown” Sims are separate ids, as intended. “John Wilson Beard Beard” looks like a typo but is the game’s own name.
- **No dead links:** every `#link` on all 1,120 pages opens a real page. Gallery links all go to `www.ea.com`.
- **`aria-current` is missing on 48 Sim pages and one household.** These are relatives with no household of their own (e.g. `#s-agnes-crumplebottom`, the Thebe ancestors) and the NPC Scotts. They have no link of their own in the sidebar, so the drawer opens on Home. That is consistent with the rule, but she might expect the family’s household.

## Text

- **British English:** the only American spellings found are the game’s own names: Information Center, Stay-at-Home Mom, Neighborhood Confidante, Color Theory Critic, Teen Neighborhood, Mold, Cozy in Gallery titles. These are allowed.
- **No straight quotes, no “1 lots”/“0 lot” plurals, no undefined/NaN** anywhere on the site.
- **Gallery descriptions**, her own and the game’s: 46 use “ - ” where a dash is meant, and 28 use “...”, e.g. `#w-sulani` “from afar...”, `#h-ondarion--aloisio-romualdo` “the end...always”. These are her words and the game’s, word for word, so only `text-fixes.json` could change them if she wants.

## Performance

- **Fast everywhere:** first page ready in 220–520 ms. `route()` takes 2–6 ms (44 ms on Admin, Progress, which has 10,400 elements). No page took more than 1.3 s to draw.
- **Weight:**
  - `js/data.js` is 830 KB on every first load. The family server sends no gzip, with `Cache-Control: no-cache`. Online, GitHub Pages would gzip it to about a fifth.
  - World and neighbourhood pages load the full 3,074px map (Britechester 1.24 MB, Mt. Komorebi 1.29 MB), shared by the banner and every card on that page.
  - Lot pages: see Should fix 4.
  - Home: 1.9 MB first view, 3.0 MB after scrolling.

## Code

- **Dead CSS:** about 18 rules for markup no code draws any more, in `site/site.css`:
  - `.a-filters`, `.day-h`, `.seg`, `.mini .dh`, `.key i.k2/.k3` (the old calendar filters, 948–1014)
  - `.fam-groups`, `.fam-group`, `.rel-none` (829–843)
  - `details.adm-more`, `.adm-two` (1108–1110, 1147)
  - `.sub-h` (928), `span.bornchip` (812), `.sim-about .hint` (828), `.roster .lvl` (758–759), `.subnav .fam-link` (431), `.medal.m1` (943)
  - `.otag` and `.sublabel-link` are only used inside `:not()`.

  Worth checking before deleting.
- **After a keyboard search, focus lands on the world link.** At 1280, choosing a search result for a group page (e.g. Goth dynasty) with Enter puts focus on “Willow Creek” in the sidebar. `route()` falls back to `a.cur, a.path, a.on` when `navCurrent()` has nothing. When there is no own link, `#view` would be the better place.
- **`gallery_refresh.py`:** the two `build.py` runs have no time limit (new_save_check has 900 s). A hung build is only stopped by weekly.py’s 30 minutes, after which nothing is logged as “Finished”.
- **`record_apps.py` runs twice:** once from the refresh (`record_in_parent`) and again at the end of weekly.py. Harmless, but one call would do.
- **The 22 Nov 11:28 refresh log ends “sim-world: not on main, not recorded”,** although its push to main had just worked. The submodule was briefly detached by something else at that moment; it was recorded by hand later (7453798). Worth keeping an eye on next Sunday.
- **The CSP is a meta tag,** so it can’t set `frame-ancestors`. Online, add that as a real header if the host allows it. `style-src 'unsafe-inline'` is needed for the many inline `style="--c:…"` attributes; that’s fine as noted.
- **Escaping:** other people’s Gallery comments, names and URLs are all escaped (`esc()`). Nothing else on the site is filled from the address bar.
- **Still no skip link:** 42 Tab presses from the top to reach the page at 1280. Not a family rule.

## Tests

- **`python -B -X utf8 tools/run_tests.py`: all passed.** Python: 396 tests OK (1 skipped, needs the game). Site: 124 passed (2.2 min). No files changed.
- **The parent’s `tests/axe_all.js` now crashes on its first Sim World page.** `page.addScriptTag({content: AXE})` is an inline script, which Sim World’s CSP blocks. The call isn’t caught, so the whole family check stops at `/sim-world/#home` and never reaches the Pokédex or Travels. *Fix:* `bypassCSP: true` in its `newContext`, or `addScriptTag({path: require.resolve('axe-core/axe.min.js')})` (an inline tag either way, so `bypassCSP` is the real fix).
- **Gaps worth a test:**
  - Sim World’s own suite has no axe check. The contrast misses in Should fix 2–3 would have been caught.
  - Nothing checks that weekly.py actually runs the refresh after a missed Sunday.
  - `versions.spec.js` encodes the old 07:54 Sunday schedule.
