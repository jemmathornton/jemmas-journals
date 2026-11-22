# Review, round 4: Library and Travels after the round-3 fixes and the switch to the family’s shared code (22 Nov 2026)

Read-only. Reviewed Library at **a964acb** and Travels at **a51f219** (both on `main`, clean before and after), with the parent’s `site/family/` (mode.js, family.js, family.css) and `tools/serve_all.py` as committed at e781fa4. Nothing in any repo was changed; the only file written is this report. No request with a method other than GET/HEAD left the browser: every POST (including `/family/mode` when Dark mode was pressed) was answered inside Playwright by a stand-in, and the family server’s stored choice (`logs/family-mode.txt`) was rewritten into pages only inside the browser.

**How it was checked**
- **Pages** (Edge, Playwright, service workers blocked so every request is seen):
  - Library through http://localhost:8050/library/: 22 page types (Home, All shelves, Fantasy, Children’s, the Old Book Collection, Old books Children’s/Fiction/Non-Fiction/To find, Reading, History, To buy, Authors, Enid Blyton, Stats, Add, New covers, Not found, 4 book pages: no cover *Witness*, an old book, the longest title, the longest blurb).
  - Travels: 18 page types (home, trips, trips by country, 2024, three trips, two posts, map, Japan, Spain, Europe, stats, timeline, search, Write, Not found). First through 8050; because 8050 kept refusing connections (New problems, Should fix 1) the clean run was through Travels’ own server, 8041, with the family server’s `data-jj-server-mode` added to the page in the browser so it behaves the same.
  - Each at **1600, 1280, 1000, 901, 899 and 390, light and dark** (device set to the opposite scheme): page errors, console errors, failed requests (incl. `/family/`), outside requests, sideways scroll, broken images, `data-mode`, theme colour, top bar vs sidebar, closed drawer inert, Menu button attributes and size, bar name 26px, and the footer (line 1 word for word, name not italic, 12.5px, credits with capitals, no visible “·” at a line start or end, credits one per line on phones with no empty line, Back to top and Dark mode 44px and level, their words, icons and `aria-pressed`).
- **Behaviour:** drawer at 899 and 390 (Tab can’t reach it closed; opening by click and by Enter; focus to the page’s link, Home/brand on a page with none; everything else inert; scrim; page locked; Tab and Shift+Tab ×70 never leave it; Escape, scrim tap, link; across 900 and back); Back to top by click and Enter; dark mode on Library → Travels tab and home tab follow by the storage event without reloading, new loads of Travels and home open dark, Light on Travels brings both back; keyboard Enter/Space keep focus on the button; a second browser profile opens in the server’s choice; each app’s own server (8020, 8041) with the old key; opened as a file (light and with `jj-mode` dark already saved); `/family/` and path traversal on 8050, 8020 and 8041; 60 parallel requests at 8050 and 8020.
- **Both full test suites.**

**Screenshots:** `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review4\`
- `library\` and `travels\`: `<page>_<width>_<mode>.jpg` (every page at 1600, 899 and 390; the first pages at every width) and `footer_home_<width>_<mode>.jpg` (footer crop at all six widths, both modes).
- `behave\`: drawer open at 899 and 390 for both apps; `travels-followed-dark.jpg` (the Travels tab after Dark was pressed in the Library tab).
- `extra\`: both apps opened as a file (1280, 899, 390), `library-supernaturalis-390.jpg`, `library-witness-899.jpg`.
- Raw results: `library-sweep.txt/.json`, `travels-sweep.txt/.json` (8041 run), `travels-sweep-run1.txt` and `-run2-8050.txt` (the refused 8050 runs), `behave.txt`, `extra.txt`, `probe.py` (traversal), `burst.py`.

Compared with the before/after pictures in `for-jemma/concepts/app-styles/built/round3/`: the footers, drawers and pages match the “after” shots; nothing moved apart from the review fixes.

**Not caused by this review, seen during it:** `logs/family-mode.txt` changed several times while it ran (01:12 and after; another session pressing Dark/Light mode through 8050). For a while the real server injected `dark` into pages, which showed up as “dark in a light run” in an early sweep with service workers allowed (the Library’s `sw.js` passes requests straight to the network, so Playwright’s rewrite never saw them). That run was thrown away and repeated with service workers blocked. Also new in the parent during the review: `research/reviews/round4-family.md` and `round4-simworld-pokedex.md` (other sessions).

---

# Library

## Not fixed (from round 3)

All round-3 Broken and Should-fix items were checked. Fixed: Broken 1 (home link as a file → `file:///C:/Users/Jemma/Documents/JemmasJournals/site/index.html`, opens “Jemma’s Journals”), Broken 2 (no title cut sideways at 390 on Fantasy; *Witness* at 899 is whole, 187/187 px), Should fix 2 (serve_all forwards to 127.0.0.1, `/library/api/reading-status` 0.02 s, Host check in serve_all, bad Host → 403), 3 (as a file the New covers switch is hidden and `#trial-covers` shows Home), 4 (backup status is `api/backup-status`, `{}` before the first backup), 5 (missing books now 5.15:1 light, 7.44:1 dark), 6 (backup only on `main`, pushes `main` by name, unit tests), 7 (Stats frame test: full suite passed), 8 (capitalise only on added nodes; manifest `#F3EAD5`).

Only partly fixed:

1. **Old-book spine lettering is still under 4.5:1 on some cloths** (Should fix 5).
   - Choosing the gilt or the dark lettering by contrast ratio helped a lot (the worst was 2.27:1), but on mid-tone cloths neither lettering reaches 4.5:1.
   - Lowest on Old books · Children’s at 1600 (title / number, 13.5px and 10px text): “Brer Rabbit Book” 3.36 / 3.36, “The New School at Scawdale” 3.76, “Heidi” 3.78, “The Island of Adventure” 3.91 / 3.91, “Brer Rabbit Again” 4.12, “Five on a Treasure Island” 4.12.
   - The text shadow helps a little; the series numbers are 10px, so they need 4.5:1 most.
   - Fix (general): when neither lettering reaches 4.5:1, put the lettering on a small label (a darker or lighter band behind the title) or darken/lighten the cloth on the spine as `paleCloth()` does for shelf cards. Changes the look, so also under Looks.
2. **Ornaments ❦ ❧ and the ← arrow** are still drawn in Windows’ symbol font (Should fix 1). This was knowingly left for her as a Looks question (CLAUDE.md, round 3 notes), so it is not counted as missed.

## New problems

### Broken

None found.

### Should fix

1. **The family server refuses connections under load, and pages lose covers, fonts, icons or the family code** (parent `tools/serve_all.py`; also the Library’s own `serve.py`).
   - 60 parallel GETs of covers: 8050 refused 10 of 60 in the first round; 8020 refused 4 of 60 in one of three rounds (`burst.py`).
   - In the sweep this hit real pages: Authors at 901 lost 9 covers and the icon, New covers 12 pictures, Stats and All shelves one cover each (`library-sweep.txt`). Travels through 8050 was worse (Should fix 1 there): whole pages blank when `icons.js` or `site.css` was refused, and empty footers when `/family/family.js` was refused.
   - Why: `socketserver`’s listen backlog is 5 (`request_queue_size`). A page with many covers opens dozens of connections at once, and Windows refuses the rest instead of queueing them. Other sessions using 8050 at the same time made it worse during this review, but one Authors page is enough to cause it.
   - Fix: `request_queue_size = 128` on `Server` in `serve_all.py`, `library/tools/serve.py` (and Travels’ and Pokédex’s servers). A one-line change in each.
2. **Opened as a file: three console errors on every load, and a flash of light when dark is chosen.**
   - `index.html` asks for `/family/mode.js`, `/family/family.css` and `/family/family.js`, which as a file are `file:///C:/family/…`: three “Failed to load resource: net::ERR_FILE_NOT_FOUND” on every load (`extra.txt`).
   - `app.js` then loads the folder copies, so everything works (footer, Dark mode, drawer at 899 and 390, home link) — but only after the deferred `app.js` runs. With `jj-mode` already dark, the first paint is light (`data-mode` “light” at the first frame and at DOMContentLoaded, dark only afterwards), so the page flashes. Over http there is no flash.
   - (A side effect: a file at `C:\family\mode.js` would run in the page. Unlikely, but the path is outside her folders.)
   - Fix (both apps, ideally once in the family): a tiny inline loader in `<head>` that picks `/family/` or `../../site/family/` by `location.protocol` and writes the three tags synchronously, so mode.js runs before the first paint in both cases and nothing 404s. Then the two separate fallbacks in `app.js` (see Code quality) can go.
3. **Code quality of the switch** (small):
   - **Two different file fallbacks.** Library’s `familyFromFolder()` (Promise chain, inserts the CSS before site.css, starts the drawer after) and Travels’ (async=false scripts, `onload = startFamily`) do the same job in two ways. One shared loader (Should fix 2) removes both.
   - **The skip link still has an inline `onclick`** (`site/index.html:31`). Travels removed its inline handlers for a strict Content-Security-Policy online; the Library still has this one. Same fix as Travels: a listener in app.js.
   - **Leftovers checked:** none of the old toggle, footer or drawer code is left (`showMode`, `footDots`, `setMenu`’s body, `.about-site`, `.sep`, `body.nav-open`, `.totop`, `.mode-text` are all gone from app.js and site.css). `setMenu`/`menuOpen` remain as two-line wrappers over `JJFamily.menu` for `route()` and the tests: fine.
   - `tools/serve.py` serves `/family/README.md` (as text/plain). Harmless, but only the three code files are needed.
   - The weekly backup now runs the parent’s `record_apps.py`, which ends with `git push -q` in the parent: any other unpushed parent commits (her own work in progress) go to the public repo with it on a Sunday morning. Pushing only when the parent has nothing else unpushed (or pushing just the new commit) would be safer.

## Looks (list only, for her)

1. Old-book spines: a label or adjusted cloth where neither lettering reaches 4.5:1 (Not fixed 1).
2. Ornaments ❦ ❧ and ← in EB Garamond rather than the system symbol font (round 3, left for her).
3. Stars ★ in the system symbol font (round 3).
4. The credits’ dots sit closer to the credit before than after (“publishers ·  Some”): the dot’s margin is right only. As before the switch.
5. New covers page at 390 still runs 43px off the side and has no h1. Now only shown to her with the server, so it matters less.
6. Still open from earlier rounds: sidebar links below the fold at 1280×800, “ISBN-13” in small capitals, justified blurbs, “Got It” vs “Got it”, Stats panel rounded on phones, the section ornament under the button on phones, the New covers switch above the scrim at 601–900.

## Family rules (Library)

| Rule | Result |
|---|---|
| Opens light with the device dark; button switches; key `jj-mode`; reload keeps it | **Pass** (8020: localStorage; 8050: the server’s choice, carried) |
| “Dark mode”/moon ↔ “Light mode”/sun, `aria-pressed`; focus stays on the button (click, Enter, Space) | **Pass** |
| theme-color #3B2616 / #1C1610 follows | **Pass** |
| Old key `jemmas-library-mode` moved once and removed | **Pass** (8020) |
| Carries to home and Travels; a second tab follows without reload (storage event) | **Pass** (both tabs, label and theme colour too) |
| Footer line 1 word for word, name plain, 12.5px, credits with capitals | **Pass** on 264 page checks (the only other findings were refused connections, Should fix 1, and New covers at 390) |
| No “·” at a line start or end; credits one per line on phones, no empty line | **Pass** (1–2 lines wide; 4 lines in 4 lines’ height at 390) |
| Back to top and Dark mode 44px and level | **Pass**, every page, width and mode |
| Back to top scrolls and focuses the page | **Pass** (click and Enter; next Tab goes into the page) |
| Menu at 899, sidebar at 901; 44px button; bar name 26px; `aria-expanded`/`aria-controls` | **Pass** |
| Drawer: closed inert; opens on the page’s link (brand on Not found); others inert; Tab/Shift+Tab trapped; Escape/scrim → Menu; link → `#view`; locked page; reset across 900 | **Pass** |
| Scrim black 45% | **Pass** |
| `/family/` files load (no failures apart from server refusals) | **Pass** over http; 3 errors as a file (Should fix 2) |

## Tests result

`python -B -X utf8 tests/run_tests.py`: **331 tests, all OK** (145 s), run while the Travels suite was running. `git status` in `library/` clean before and after.

---

# Travels

## Not fixed (from round 3)

All round-3 Broken and Should-fix items were checked. Fixed:
- Broken 1: Save is off until `api/ping` answers. With a simulated slow 503 it stayed off at 0.8 s and then said “The Travels save server isn’t running…” with Save still off; with the real server through 8050 the ping takes 0.003 s and Save turns on. Save with a non-JSON answer reads plainly (code checked; covered by her test).
- Broken 2: `#/search/%E0%A4%A`, `#/trip/%`, `#/%` show Not found with no page error.
- Should fix 3: no “you/your” in the posts or on the Italy template page; titles read “Template: …”.
- Should fix 4: `#/stats/x`, `#/year/2024/x`, `#/timeline/x`, `#/trip/japan-2024/01/x`, `#/country/JP/x`, `#/continent/Europe/x`, `#/write/x`, `#/surprise/x` are Not found.
- Should fix 5: notes updated (repo name, file link, no ×, writing-options folder).
- Should fix 6: `serve.py` refuses a foreign Host (403 for pages and `/family/`).
- Should fix 7: no inline handlers (skip link, search forms and continent chips work by listeners: checked), Timeline “about 3,040 km” (nearest 10), rebuilt-site check at most every 10 s.

Not done (small, from Should fix 7):
1. **The page sweeps’ `WIDTHS` still have no 899 or 901** (`tests/e2e/run.js:14`). The family tests cover 899/901 for the drawer, but no page is swept at those widths.

## New problems

### Broken

None found.

### Should fix

1. **Through the family server, Travels pages came up blank or without footer** — the same refused connections as the Library (Library, Should fix 1). In two runs through 8050: `trips/by-country` and `trip/brazil-argentina-2025` blank (“VIEW EMPTY”) when `js/icons.js` or `site.css` was refused; `timeline` and `search/japan` at 899 with an empty footer, no Dark mode button and a drawer not inert when `/family/family.js` was refused; fonts and icons missing on others (`travels-sweep-run1.txt`, `-run2-8050.txt`). The same pages were all clean through 8041. Fix: `request_queue_size` on `serve_all.py` (and `ThreadingHTTPServer` in `tools/serve.py`, line 260).
   - Related robustness point: everything shared now depends on one file. If `/family/family.js` fails to load, the footer is empty (no line 1, no buttons) and the drawer is never set up — at ≤900 the Menu button does nothing and the closed sidebar isn’t inert. A quiet fallback isn’t needed for her PC once the backlog is fixed, but online it’s worth keeping the static line 1 (Travels already has it in the markup; the Library doesn’t).
2. **Opened as a file: three console errors and a flash of light when dark is chosen** — same cause and fix as Library Should fix 2. Travels has no `data-mode` at all until the folder copy of mode.js runs (null at the first frame and at DOMContentLoaded).
3. **Code quality** (small):
   - Two different file fallbacks for the same job (see Library, Should fix 3).
   - On an address with extra parts, `body[data-page]` is the first part (“stats”, “trip”, “map”) while the page shows Not found; only broken % addresses get “notfound”. Nothing in site.css uses it today, so it’s cosmetic, but it would mislead any style or test that does.
   - `serve.py` serves `/family/` subfolders and Windows name forms (`mode.js.`, `mode.js%20`, `mode.js::$DATA` all return mode.js). Everything stays inside `site/family` (traversal with `..`, `%2f`, `%5c`, drive and UNC paths all 404), so it is safe; the Library’s plain-name rule is stricter.
   - The drawer is closed twice after a link (family.js on the click, `render()` with `close("silent")` on hashchange). Harmless: the second is a no-op.
   - Once, in the first skip-link check at 1280, Enter on the skip link changed the address to `#view` (Not found). It did not happen again in 18 tries (click and Enter, 899/1280/1600), so it may have been the page’s rebuilt-site reload racing the key press; noted only.

## Looks (list only, for her)

1. Long sidebar trip names cut with “…”, no tooltip (round 3).
2. Small trip map at 901–1000 (round 3).
3. Footer “·” 3.76:1 in light mode (decorative).
4. Natural Earth short names in map tooltips (“Côte d'Ivoire” with a straight apostrophe).
5. Dark-mode scrim deep blue 60% (kept on purpose; the family’s is black 45%).
6. Home long on phones (her choice to keep).

## Family rules (Travels)

| Rule | Result |
|---|---|
| Opens light; button switches; `jj-mode`; reload keeps it | **Pass** (8041 localStorage; 8050 server choice) |
| Labels, icons, `aria-pressed`, focus kept | **Pass** |
| theme-color #ECF1EA / #15212C follows | **Pass** |
| Old key `jt-mode` moved once and removed | **Pass** (8041) |
| Follows a change in another tab without reload; carries to home and Library | **Pass** |
| Footer per the rules (line 1, credits, dots, phones one per line, 44px level buttons) | **Pass** on all 216 page checks of the 8041 sweep (no errors, failed requests, outside requests or sideways scroll either; one h1 on every page; 1–2 credit lines wide, 4 lines in 4 lines’ height at 390) |
| Back to top scrolls and focuses `#view` | **Pass** |
| Menu/drawer at 899 and 390: everything as the rules say | **Pass** (focus to Stats link, Home on Not found; Tab trapped; Escape/scrim → Menu; link → `#view`; reset across 900) |
| Scrim | black 45% light, deep blue 60% dark (Looks 5) |
| `/family/` served by 8041 and 8050, traversal safe | **Pass** |

## Tests result

`python -B -X utf8 tests/run_tests.py`: **100 tests, all OK** (663 s), run alongside the Library suite. `git status` in `travels/` clean before and after.

---

# Shared code and servers (both apps)

- **`/family/` traversal:** 23 crafted paths × GET/HEAD on 8050, 8020 and 8041 (`probe.py`): nothing outside `site/family` is served by the apps’ servers. On 8050, `/family/../index.html` returns home’s own page (inside `site/`, fine). One small fault in the parent: `/family/mode.js%00` makes `serve_all.py` drop the connection with an exception (embedded NUL in `os.path`), on GET and HEAD; the server keeps running. Worth a `try` around `translate_path`/`isdir`.
- **Dark mode POST:** only sent when the page carries `data-jj-server-mode` (8050); 8020 and 8041 sent none. The server needs `X-Family: 1` and a local Host, so another site can’t set it.
- **Load:** the backlog refusal (Library Should fix 1) is the one problem affecting both apps day to day through 8050.
