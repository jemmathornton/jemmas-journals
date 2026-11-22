# Review, round 5: Jemma’s Travels (22 Nov 2026)

Read-only. Reviewed Travels at **3249f2e** (`main`, clean before and after, HEAD unchanged), with the parent’s `site/family/` as served by the family server at the time. Nothing in any repo was changed; the only files written are this report and screenshots. Every request that wasn’t GET/HEAD was answered inside Playwright (the two Dark mode presses sent `POST /family/mode`, both caught); `logs/family-mode.txt` read “dark” before and after.

**Seen during the review, not caused by it:** the parent’s working tree changed while it ran (another session: `site/family/family.js` +39/−8, `site/home.js`, `site/index.html`, `site/404.html`, `templates/new-site/…`, `sim-world` and `library` pointers). Results below are against whatever `family.js` was served at the time (no family problem was seen).

**How it was checked**
- **Every page type, 63 addresses** through http://localhost:8050/travels/: home, Trips, Trips by country, the 5 years, all 11 trips, all 13 posts, Map and `#/countries`, all 13 visited countries plus GB (home) and FJ (not on the list), the 4 continents, Stats, Timeline, Search (empty, “japan”, “zzzz”, “são”), Write, Not found (`#/nothing-here`, `#/trip/nope`), Surprise me.
- Each at **1600, 1280, 1000, 950, 901, 899 and 390, light and dark** (device set to the opposite scheme; the server’s mode rewritten in the browser for each run): page errors, console errors and warnings, failed requests, HTTP ≥ 400, **CSP violations** (a `securitypolicyviolation` listener on every page), sideways scroll, broken images, one h1, cut text (ellipsis/hidden overflow), text sticking out of its box, overlapping boxes (stat tiles, facts, cards, tiles, chips, filters, bars, footer buttons, post nav, trip head, months), straight apostrophes, “you/your” in the site’s own text, American spellings, “undefined/NaN/null”, footer line 1 word for word, footer buttons 44px and level, drawer inert and top bar at ≤900, sidebar at >900. 882 page checks.
- **axe-core** on all 62 pages at 1280 and 390, light and dark (CSP bypassed only for injecting axe).
- **Crawl** of every internal link from home (53 distinct addresses reached).
- **Behaviour:** hover titles on cut names at 1600/1280/1000/901/899/390 (every year and continent opened); drawer at 899 and 390 in both modes (Enter opens, focus, scrim colour, inert, page locked, 40 Tab/Shift+Tab, Escape, scrim tap, link, across 900 and back); Dark mode by keyboard (label, `aria-pressed`, theme colour, `jj-mode`, focus kept), a second tab following; Back to top; skip link on a fresh load; keyboard through the Map page; sidebar search with accents and spaces; empty search; Write page state; Surprise me and Back.
- **Online-style:** 8060 (`_site/`), a fresh copy of today’s files served the same way on 8061 (from my scratchpad), and the same copy under a made-up real host name (`--host-resolver-rules`), so `LOCAL` is false as it will be online.
- **Opened as a file** (light, and with `jj-mode` dark saved).
- **Performance:** page weight, per-page render time, the same at 4× CPU slowdown at 390.
- **Data** recomputed independently in Python (distances, counts, months, furthest, most visited).
- **Code read:** `site/js/app.js`, `map.js`, `index.html`, `site.css` (parts), `tools/serve.py`, `build.py`, `check_data.py`, the parent’s `tools/weekly.py` (`travels_backup`) and `tools/build_site.py`, `site/family/mode.js` and `family.js`.
- **Her suite:** `python -B -X utf8 tests/run_tests.py`.

**Screenshots:** `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review5\travels\`
- `sweep8050_<page>_<width>_<mode>.jpg`: every page, full length, at 1600 and 390 in both modes and 899 light.
- `behave_*`: drawer open at 899/390 light and dark, sidebar with a year open at 1280/899, Write page at 1280.
- `online_*`: the Write page on 8060, 8061 and under a real host name. `file_map_899_*`: opened as a file.
- Raw results and scripts in `…\scratchpad\review5\travels-work\` (`sweep8050.txt/.json`, `axe-out.txt`, `crawl-8050.json`, `interact-8050.txt`, and the scripts).

---

## Today’s changes: verified

| Change | Result |
|---|---|
| **Hover titles on cut trip names** | **Works.** At 1600, 1280, 1000 and 901 the one cut name, “Norway, Denmark and Sweden”, gets `title` equal to its text on hover; none of the other 23 sidebar names gets one; below 900 the drawer is wider and nothing is cut. A test covers it. Limits under Should fix 4. |
| **Dark scrim black 45%** | **Works.** `rgba(0, 0, 0, 0.45)` in light and dark at 899 and 390; the site’s override is gone (only `z-index` left in site.css). |
| **CSP meta** | **Works.** No violation on any of the 882 page checks (both modes, all widths), on the Write page (blob: previews allowed), online-style or opened as a file. Note: because of it, any tool that injects inline script (axe, some screenshot helpers) needs `bypassCSP`. The parent’s `tests/axe_all.js` uses `addScriptTag({content})` without it, so it now stops with an error at Travels (Tests 2). |
| **Daily backup step for posts** (`tools/weekly.py`, `travels_backup`) | Runs as described, but has two real faults: Should fix 2. |

## Not fixed (from round 4)

1. **Opened as a file: still three console errors and a flash of light when dark is chosen** (round 4, Should fix 2). `file:///C:/family/mode.js`, `family.css`, `family.js` → `ERR_FILE_NOT_FOUND` on every load; `data-mode` is still unset at DOMContentLoaded with `jj-mode` dark, so the first paint is light. Everything works once `app.js` loads the folder copies (footer, Dark mode, drawer, home link to `…/JemmasJournals/site/index.html`).
2. **The page sweeps still have no 899 or 901** (`tests/e2e/run.js:14`, `WIDTHS`), round 3/4. The family tests cover those widths for the drawer only.
3. **`body[data-page]`** is still the first part of the address when an address with extra parts shows Not found (`#/stats/x` → `data-page="stats"`; `app.js:587`). Nothing uses it yet.
4. **`/family/` name forms** on `serve.py`: `mode.js.`, `mode.js%20`, `mode.js::$DATA` all return `mode.js`, and `README.md` is served. Safe (nothing outside `site/family`), just looser than the Library.
5. (The server backlog from round 4 Should fix 1 **is fixed**: `request_queue_size = 128`; the 8050 sweep had no refused or failed request on 882 checks.)

---

## Broken

None found. No page errors, console errors, failed requests, CSP violations, broken images, sideways scroll or missing h1 on any page, width or mode; no internal link leads to Not found.

## Should fix

1. **Canada is left out of the “Canada and Boston” route and distance** (`tripStops`, `app.js:117`).
   - What she’d see: http://localhost:8050/travels/#/trip/canada-boston-2023 colours Canada in, but the line goes Birmingham → Boston → Birmingham and the Distance says **10,230 km**, which is exactly the Boston round trip. Timeline (“about 10,230 km there and back”) and Stats’ Distance travelled use the same figure.
   - Why: when a trip has any named places, only the places are used; countries with no named place are dropped. Today only this trip has places for some but not all of its countries, but it will happen whenever she names one city on a multi-country trip.
   - Fix: build the stops from the places, then add each country that has no place inside it (`inCountry` is already there), in the trip’s country order; or require a place for every country once one is given (a `check_data` rule). Add a fixture trip like it (the fixture has none).
2. **The daily backup (`tools/weekly.py`, `travels_backup`) commits more and less than it should.**
   - **Less:** every save rebuilds `site/js/data.js` *and* restamps `site/index.html` (`build.py` writes `data.js?v=<new>`), but only `data`, `site/photos` and `site/js/data.js` are added. So the committed `index.html` keeps the old fingerprint for the new `data.js` (online, a browser or the host’s cache can serve the old data under the old address, which the fingerprint exists to prevent), and `site/index.html` stays modified in her working tree after every save, to be swept into the next hand-made commit. Fix: add `site/index.html` to `TRAVELS_PATHS` (only `?v=` lines change).
   - **More:** `git commit` with no paths commits *everything staged*, not just these paths: anything another session has staged in `travels/` goes out at 09:30 under “Posts saved up to … (daily backup)”. Likewise `git add data` takes any half-finished hand edit of `trips.json`/`countries.json`. Fix: `git commit -- <paths>` (or stop if the index had anything staged before the add), and run `tools/check_data.py` first, skipping the commit if it reports problems.
   - Also: when nothing is new it still pushes (`push -q origin main`), so any local commits she hasn’t meant to publish yet go to the public repo every morning. Same point as the Library’s in round 4.
   - Not covered by any test.
3. **`serve.py`: a failed save can leave half a post behind.** `save_post` rolls back only on `ValueError`. A build that runs past 300 s (`subprocess.TimeoutExpired`), a disk error (`OSError`) while writing the post or `trips.json`, or any other exception skips the rollback: the photos, the `.md` and a changed `trips.json` stay, the handler dies, and the Write page says “Not saved: TypeError: Failed to fetch” or similar. Fix: `except Exception` around the same rollback (keep the message). Smaller, same function: a reused post number (her last post’s `.md` deleted by hand, its photos left) overwrites `NN-k.jpg`, and a rollback then deletes them; a non-numeric `Content-Length` raises instead of answering 400.
4. **Hover titles cover trip names only.** The listener matches `a.kid2[href^="#/trip/"]`; country names under Map › continent use the same `kid2` style **with a count beside them**, so they have less room than trip names and will be cut first once she adds e.g. “Bosnia and Herzegovina” or “Democratic Republic of the Congo”. None is cut today. Fix: match any `#nav a.kid2` (and the year/continent openers for safety). A title is also mouse-only (no keyboard or touch); fine as she decided, noted for completeness.
5. **Dates aren’t checked as real dates** (`tools/check_data.py`, `DATE = \d{4}-\d{2}-\d{2}`). A post with `dates: 2026-09-31` shows “31 September”; `2026-13-01` shows “1 undefined”; `2026-09-07 to 2026-09-05` shows “7–5 September” and counts 1 day; `days: 4-2` shows “Days 4–2”. All pass the check, and the Write page’s “Or dates” box accepts them. Fix: parse with `datetime.date.fromisoformat` and require end ≥ start (and `b ≥ a` for days).
6. **The online-style copy at 8060 is out of date.** `_site/travels/index.html` was built at 12:48, before the CSP commit (13:05), so 8060 doesn’t show today’s change. A fresh copy of today’s files served the same way (8061) behaved correctly: no CSP violations; on localhost the Write page says “To save, open the site from its own server…” with Save off; under a real host name the Write page is **Not found** and the sidebar has no Write link, no `api/` or `index.html` requests are made, and Dark mode is remembered without any POST. Rebuild `_site` (`tools/build_site.py`) before using 8060 to judge. (On localhost the page shows a harmless console 404 for `api/ping`.)

## Looks (list only, for her)

1. **Home and year pages at 1600:** a year with three trips fills three of the four card columns, leaving an empty slot on the right of each row (http://localhost:8050/travels/#/ at 1600, every “Trips by year” group).
2. **Credits’ dots** sit closer to the credit before than after (“Photos are my own ·  Country shapes…”), as on the Library (family footer, all pages).
3. Still open from earlier rounds: small trip map at 901–1000; footer “·” 3.76:1 in light; Natural Earth short names in map tooltips (“Côte d'Ivoire” with a straight apostrophe, only for countries not in countries.json); long home on phones (her choice).

## Data

All the figures were recomputed independently and match the pages, apart from the Canada route (Should fix 1):
- Trips 11, years 5, countries 13 (GB not counted), continents 4 of 7 (Asia, Europe, North America, South America), 13 of 195 = 6.7%.
- Distances (nearest 10 km): Italy 3,040; Norway, Denmark and Sweden 3,910; Portugal 3,010; Brazil and Argentina 22,690; Strasbourg 1,610; Tenerife 5,900; Japan 18,850; France and Spain 2,960; NYC and Nashville 13,230; Canada and Boston 10,230 (should include Canada); India 14,960. Total 100,390 → “100,000 km, about 2.5 times round the world”.
- Furthest from home Argentina, about 11,300 km; Most visited France, Spain, United States (2 each); Busiest year 2024, 2025, 2026 (3 each); First on record India; months Sep 5, Jun 2, Dec 2, Mar/Apr/Oct/Nov 1.
- Map regions: every visited country coloured and linked; country pages frame the right pieces; continent pages list the right countries.

Small points:
1. **“29 photos” on the Italy trip page** (and “4 photos”, “8 photos” on the Latest posts tiles) count the placeholder frames, though there are no photos yet. Stats already counts only real posts; the trip page and tiles could say “No photos yet” or count only real files.
2. **“Longest gap: 11 years, 2012 to 2023”** on Stats while Timeline says **“2013 – 2022: no trips”** (10 years). Both true (between trips vs years without), but side by side they look inconsistent; “11 years between trips” would remove the doubt.
3. Distances use each country’s middle point where no place is named (Brazil −10, −52; Canada 56, −106), which is far from where people land. Already said “as the crow flies”; fine while trips are placeholders.

## Text

No problems found in the site’s own text: no straight apostrophes in shown text, no “you/your”, no American spellings, no “undefined/NaN”, placeholders all carry the Placeholder badge, footer line 1 word for word on every page (“…JavaScript and Python, kept on GitHub.”). Posts and templates checked too.

- `CLAUDE.md` is stale in a few places: it still names `site/icon-options/` (gone), calls `map.js` the “dotted map”, gives the test count as 100 (now 102), describes `tests/variants.js`, `banner_widths.js` and `make_sheets*.py` as if their options still existed (Code 2), and its “her answers to the second review” line still quotes footer line 1 without “and Python”.

## Performance

- **Page weight 1.47 MB** (uncompressed) on the first load, **1.26 MB of it `js/world.js`** (TODO already: load the 1:50m shapes only on zoomed maps). Everything else is small (app.js 51 KB, site.css 39 KB, three fonts 68 KB, data.js 14 KB). Online, GitHub Pages’ gzip would bring world.js to roughly a third.
- **Rendering:** each page change rebuilds its maps from scratch. Largest map markup: Italy trip 340 KB of SVG, Norway 267 KB, Brazil 205 KB. At 1280 every page draws in under 100 ms; at 390 with the CPU slowed 4× the Map page takes ~290 ms and the Italy trip ~230 ms, home load ~0.9 s. Acceptable; the cheap win is the same split of world.js (the zoomed maps use the 1:50m shapes). The rough-edge filter (`feTurbulence` + `feDisplacementMap` on the whole land group) did not cause slow frames while scrolling here.
- The rebuilt-site check fetches `index.html` at most every 10 s, only on her PC: fine.

## Code

1. **Dead attributes on `<html>`:** `data-look="f" data-layout="side-pale-grid" data-header="banner" data-bg="plain"` are used by nothing (site.css only styles `[data-mode]`; app.js never reads them), while the comment at the end of app.js says her picks are “set on <html> in index.html”. Remove them or the comment.
2. **Dead tooling:** `tests/variants.js`, `tests/banner_widths.js`, `tests/shoot.js` (looks loop) and `tools/make_sheets.py`, `make_sheets3.py`, `make_sheets4.py` pass `?layout=…&header=…&bg=…` options that no longer exist, so they would now make identical pictures labelled as different options. Delete them (they’re in git history) or mark them as history.
3. **Duplication:** the post header parser is written twice (`build.py read_post` and `check_data.py read_post`) and the photo-marker pattern three times (`app.js PHOTO_MARK`, `check_data.py MARK`, and the parent’s understanding in the guide). One Python module for the header and a test that the JS and Python patterns agree would stop them drifting.
4. **Small fragile spots:** “Furthest from home” recomputes `home` instead of using `HOME_AT()`; the Distance travelled fact is an inline IIFE inside the template; `surprisePost` falls back to a random trip, which can be the same as the page she’s on.
5. Still from round 4: two different file-fallback loaders across apps (Not fixed 1).
6. axe (moderate only, no serious or critical): the footer `role="contentinfo"` sits inside `<main>` (landmark nested, every page); on post pages two `<nav>`s (`.crumbs`, `.post-nav`) have no labels to tell them apart; at ≤900 the top bar’s name is outside any landmark. Cheap fixes: move the footer out of `<main>` (or drop the role), `aria-label="Breadcrumb"` / `"Posts"` on the two navs.

## Tests

1. `python -B -X utf8 tests/run_tests.py`: **102 tests, all OK** (710 s). `git status` in `travels/` clean before and after, HEAD 3249f2e unchanged.
2. Gaps:
   - No fixture trip with places for only some of its countries (would have caught Should fix 1).
   - Nothing tests `travels_backup` (Should fix 2); a test on a throwaway clone could check that only the Write page’s files (and `site/index.html`) are committed and that a pre-staged file is left alone.
   - No test for a save that fails with something other than `ValueError` (Should fix 3), or for impossible dates (Should fix 5).
   - The page sweeps lack 899/901 (Not fixed 2).
   - The parent’s `tests/axe_all.js` now **breaks on Travels**: with the CSP, `page.addScriptTag({content: AXE})` throws (“Executing inline script violates … 'script-src 'self''”, checked), and the script has no catch, so the run stops at `/travels/` before writing `logs/check-all/axe.txt` (Travels Stats and every later width/mode go unchecked). Needs `bypassCSP: true` on the context (this review did that: 248 page checks, moderate findings only, Code 6).
