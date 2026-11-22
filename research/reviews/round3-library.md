# Review, round 3: Jemma’s Library (22 Nov 2026, after the move)

Read-only review of `Documents\JemmasJournals\library` at **506463a** (submodule of Jemma’s Journals, on `main`, clean). Nothing in the Library or the parent was changed by this review. (At the end the parent showed `tools/serve_all.py` modified: that edit came from another session during this review, not from this one. See Should fix 2.)

**How it was checked.**
- **Pages:** `library/site` served from disk through Playwright `page.route` (Edge). Every non-GET request was aborted and none were made. 39 page types at 1600, 1280, 1000, 901, 899 and 390, light and dark: Home, All shelves, all 11 shelves (including the empty “Not on a shelf yet”), Old books Children’s/Fiction/Non-Fiction/To Find, 10 book pages (long blurb, blurb opening with a quote mark, blurb opening with a number, special edition, no cover, old book, signed, long title, Display, review with a spoiler), a not-owned book, Reading, History, To Buy, Authors, Enid Blyton (largest author), Stats, Add, New covers and an unknown address. That is 468 page checks for console/page errors, failed requests, broken images, alt text, h1, sideways overflow, clipped text, section-heading overlaps, small-text contrast (measured on plain backgrounds), the footer, data-mode, and topbar vs sidebar.
- **Behaviour:** the drawer by keyboard and mouse at 899 and 390, dark mode, the old key, blocked storage, Back to top, the skip link and focus rings.
- **Fonts actually drawn:** CDP `getPlatformFontsForNode`, plus a fontTools comparison of every character in data.js/app.js/index.html against each WOFF2.
- **Other modes:** opened as a file. The family address http://localhost:8050/library/ in LIVE mode, with POSTs blocked and scan-setup never asked for.
- **Read-only checks on her PC:** Windows tasks and shortcuts via PowerShell.

**Screenshots:** `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review3\library\` (235 files: `<page>_<width>_<light|dark>.jpg`, plus `drawer-open_*`, `focus-*`, `live-*`, `cut-title_390_light.jpg`, `nocover-card_899_light.jpg`, `ornament-*`, `arrow-homelink_*`, `stats_1000_light_full.jpg`, `oldbooks-gone-row_1000_light.jpg`). Raw results: `..\..\r3lib\sweep-all.json`, `behave.txt`, `behave2.txt`, `live.txt`, `crops.txt`.

## What held from rounds 1 and 2 (all checked, all fixed)

- **Drawer:**
  - After a link or search Enter, focus goes to `#view`.
  - Tab no longer reaches the top bar while the drawer is open, because the top bar is inert.
  - The drawer opens on the page’s own link: Reading on Reading, Fantasy on a Fantasy book, the name when the page has no link.
- **901–1100 wide:**
  - Stats no longer runs off the side.
  - No heading collides with its button or note.
  - The figures sit two by two.
- **Smaller fixes:**
  - Drop capital: skipped for a blurb that starts with a number, kept after a quote mark (her pick).
  - Children’s card: the cloth is darkened by `paleCloth()`.
  - Old books shelves: a dark board in dark mode.
- **Page weight:** EB Garamond is now 4 × 60–67 KB WOFF2 (was 2.6 MB), and no Google fonts are loaded.
- **Try switch:** removed cleanly (no `try-` CSS, JS or attributes left). The Display shelf is #5E3D22 in `data/shelves.json`, so its dot and card match.
- **Clean everywhere:**
  - No page errors.
  - No broken images, and every image has alt text.
  - No external requests and no POSTs.
  - One h1 per page except New covers.
  - Footer present, line 1 word for word, buttons 44 px and level, no dot left at a line end.
  - `data-mode` always matches the mode.
  - Topbar at ≤900, sidebar at ≥901.

---

## Broken

### 1. “← Jemma’s Journals” goes to `file:///C:/` when the site is opened as a file
- **Where:** `site/index.html:34`, `<a class="home-link" href="/">`.
- **What:** commit 506463a says “link home as a file is ../../site/index.html”. That commit changed only CLAUDE.md, and no code does it. Opened from the folder (“Opening `site/index.html` straight from the folder still works”, CLAUDE.md), the link opens the root of drive C:.
- **Evidence:** `behave2.txt`, “as a file: homeLink file:///C:/”. Over http, `/` works: at 8050 it opens Jemma’s Journals (`live.txt`). At 8020 it opens the Library’s own start, as intended.
- **Fix:** a few lines in app.js. When `location.protocol === "file:"`, set the link’s href to `../../site/index.html` (as Sim World does).

### 2. Book titles and the no-cover title card are cut mid-word
- **Cover grid at 390:** a single word longer than the card is clipped without a mark. For example “The **Supernaturalis**” on Fantasy and All shelves. `.bk h3` has `overflow:hidden` with a 3-line clamp, `overflow-wrap:normal` and `hyphens:manual`.
- **Book page with no cover, at 899:** the title card shows **“Witne”** for *Witness*. `.cover .t` is 30 px in a 58 px-wide box.
- **Evidence:** `cut-title_390_light.jpg`, `nocover-card_899_light.jpg`; sweep “CUT h3” and “CUT span.t”.
- **Fix (general rule, every card):** `overflow-wrap:anywhere` (or `hyphens:auto` with `lang`) on `.bk h3` and `.cover .t`. Also size the title card’s text from the card width (`font-size:clamp(…, 14cqi, 30px)` with `container-type:inline-size` on `.cover`).

## Should fix

### 1. The ornaments are drawn in Windows’ symbol font, not the site’s fonts
- **What:** the fallback font is visible. CDP shows the ❦ in the footer (`.foot-orn span`), the ❦ under every section heading (`.section-head::after`, site.css:621), the ❦ in `.panel h2::after` (662) and the ❧ before each kicker (`.kicker::before`, 118) all drawn by **Segoe UI Symbol**. The “←” in “← Jemma’s Journals” is drawn by **Segoe UI Semibold**.
- **Why:** these inherit Manrope or Instrument Serif, which have no ❦ ❧ ←. EB Garamond has all three: `make_web_fonts.py` keeps U+2766/2767/2190 on purpose. On a phone they will look different again (Android and iOS symbol fonts).
- **Evidence:** `behave2.txt` (“fonts .foot-orn span {Segoe UI Symbol (SYSTEM)}”, kicker, section-head, panel h2, home-link); crops `ornament-foot_1280_light.jpg`, `ornament-kicker_1280_light.jpg`, `arrow-homelink_1280_light.jpg`.
- **Fix:** `font-family:var(--read)` on those four pseudo-elements and `.foot-orn`. For the arrow, either a Lucide `arrow-left` icon or `<span style="font-family:var(--read)">←</span>`.
- **Stars:** ★ (sg-stars, and “4.75 ★” on Stats, 34 glyphs) also falls back to Segoe UI Symbol. None of the three fonts has ★, so this needs a decision rather than a fix (see Looks).

### 2. Through the family address every API call waits about 2 s, and the first page with it
- **What:** `tools/serve_all.py` (parent) forwarded to `http://localhost:8020`. On Windows, “localhost” tries ::1 first, and `serve.py` listens only on 127.0.0.1.
  - Measured: `GET /library/api/reading-status` takes **2.06 s** at 8050 and 0.002 s at 8020.
  - `checkLive()` waits for that call before drawing anything, so the first page at 8050 was blank for **2.3 s**.
  - Each Add-page poll of `/api/scanned`, and each save, is 2 s slower.
- **Status:** while this review ran, another session changed the parent’s working copy to forward to `127.0.0.1` (uncommitted). `host_ok()` in serve.py accepts `127.0.0.1:8020`, so the change is safe. The running 8050 server needs a restart to pick it up.
- **Related (security, small):** serve_all doesn’t check the `Host` header. A page on another domain that has rebound its name to 127.0.0.1 could reach 8050 and send same-origin requests with `X-Library: 1`. serve_all would forward them with a good Host, which gets round serve.py’s `host_ok()` guard (serve.py:751). Suggest the same Host check in serve_all.

### 3. Read-only mode still shows the New covers switch and its working page
- **What:** with no server (a file or plain hosting), Add, Got it, the pickers and the notes are hidden, but the **“New covers: off”** switch still shows on every Old books page, and `#trial-covers` still opens.
- **Why it matters:** that page shows working notes (“needs taking off no-cover.json”), runs 43 px off the side at 390, and has no h1. For anyone but her online, it’s a stray tool.
- **Evidence:** `old-childrens_1280_dark.jpg` (bottom right); app.js:1386–1393 (`trialShown` doesn’t check `LIVE`); sweep “OVERFLOW trial 390: 43”, “H1=0 trial”.
- **Fix:** `trialSwitch.hidden = !LIVE || …` after `checkLive()` resolves, and route `trial-covers` only when `LIVE`, as `add` is.

### 4. Read-only mode isn’t quite silent: a 404 in the console on every load
- **What:** `checkLive()` (app.js:1599) asks `api/reading-status`. On a file host the browser logs “Failed to load resource: 404” on every load (all 12 width/mode starts in the sweep). In LIVE mode before the first Sunday backup, `backup-status.json` 404s on every Home load (`live.txt`).
- **Fix:** harmless for her, but noisy online. Have serve.py answer a HEAD/GET for a static marker, or accept it. For the backup, have `backup.py` (or serve.py at start) write a status file once so it exists, or let serve.py answer `backup-status.json` with `{}` when there is none.

### 5. Old books: spine titles and the faded “missing” rows are hard to read
- **Spine titles:** the pale gold `#EFD38A` text is used unless the cloth is very light (`pale()` threshold luminance >165, app.js:268). Mid-tone cloths fail: “Sunday Times Travel…” 2.27:1, “Brer Rabbit’s a Rascal” 2.29:1, “Fifth Formers at St Clare’s” 2.46:1, “The Island of Adventure” 2.76:1. Most of the series numbers fail too: 10 px text at 2.5–3.5:1. The text shadow helps a little. The same in light and dark.
- **Missing rows:** in list view, the rows for books she doesn’t have (`tr.gone td{opacity:.45}`, site.css:567) come out at **1.88:1** (author, “On your list to find”) and 2.66:1 (title) in light mode. That is real information, not decoration.
- **Evidence:** sweep “LC old-*” and “LC shelf-old-book-collection”; `oldbooks-gone-row_1000_light.jpg`.
- **Fix (general rules):** choose light or dark spine lettering by contrast ratio (the `paleCloth()` way) instead of a fixed threshold. For the gone rows, use `var(--muted)` + italic in place of opacity. Both change the look a little, so they are also listed under Looks.

### 6. The weekly backup in its new home: two loose ends
- **Detached HEAD:** `backup.py` runs `git push origin HEAD` (backup.py:42). The Library is now a submodule, and `git submodule update` leaves submodules on a **detached HEAD**. If that happens, the weekly commit lands on no branch and the push fails (“not currently on a branch”). Today it is on `main`, so it works. Suggest `git push origin HEAD:main`, or check out `main` first and log if it isn’t.
- **Parent left out of date:** each weekly commit in the Library leaves the parent showing `library (new commits)`, and nothing records the new version there. CLAUDE.md says to do that by hand after committing, but the Sunday task does it unattended. Either let the parent’s own routine record it, or note it for her.
- **Task history:** the task’s last run is 15 Nov with result 1 (failure). The 19 Nov success in the log was a manual run. Next run is today at 09:30, from the new folder (task action and working directory are correct).

### 7. A test is flaky since the read-only change
- **What:** the full suite gave **318 tests, 1 failure**: “the Stats page at 390, 360 and 320 wide…” timed out waiting for its 360 px iframe. It passed 3 out of 3 times on its own.
- **Why:** the iframe page now waits for `checkLive()` (a server round trip, up to 3 s) before drawing, and `until()` gives it 5 s. Under load that isn’t enough.
- **Fix:** give the iframe waits 10 s in `phone.test.js:209` (and any other iframe test), or let the harness stub `api/reading-status`.

### 8. Small code points
- **capitalise() on every insertion:** app.js:1639 runs `capitalise(document)` (a query and text walk over all headings, nav and buttons) on every DOM insertion anywhere, including each hover spine card. It works, but it repeats the whole document each time. Limit it to the added nodes.
- **Project-folder shortcut still points at the old folder:** `library\Jemma's Library.lnk` (git-ignored) has its working folder and icon at `Documents\HomeLibrary\site`. The URL is right, but the icon disappears once HomeLibrary is deleted. The Desktop, Start menu and Startup shortcuts are all correct. Re-run `tools\make_shortcuts.ps1`.
- **manifest.json:** `background_color` is still #F7F1E4; the paper is #F3EAD5 (round 2 polish 9).
- **Nothing else points at `Documents\HomeLibrary`:** only comments, the User-Agent name “HomeLibrary/1.0” (fine) and a temp folder name in a test. The Startup server, the backup task and both servers on 8020/8021 run from `JemmasJournals\library`.

## Looks (would change how it looks: for her to decide)

1. Ornaments ❦ ❧ and the ← arrow in EB Garamond instead of the Windows symbol font (Should fix 1). The shapes change slightly.
2. Stars (★★★★★ on book pages, ★ on Stats) are in the system symbol font. Options: keep, or use a Lucide `star` icon. The empty stars are 1.4–1.5:1 against the panel, so the outline of a 4-out-of-5 is hard to see. The number is shown beside it.
3. Old books spines: dark lettering on more of the mid-tone cloths (Should fix 5).
4. Old books list: books she doesn’t have shown in grey italic rather than faded (Should fix 5).
5. Title words breaking across lines in cover grids at 390, and the no-cover title card text shrinking to fit (Broken 2).
6. Section-heading ornament on phones: with a button under the heading (Home “Just Finished”, Reading), the ❦ sits under the button, not under the heading (`home_390_dark.jpg`).
7. The New covers switch sits above the drawer’s scrim from 601 to 900 px (z-index 50 vs 25); it isn’t dimmed with the page.
8. Still open from earlier rounds:
   - Sidebar links below the fold at 1280×800 (Reading … Stats), with no hint that it scrolls.
   - “ISBN-13” in old-style small capitals.
   - Justified blurbs leave wide gaps.
   - “Got It” on the buttons vs “press Got it” in the sentence above.
   - Stats panel rounded on phones (site.css:838 `border-radius:14px` overrides the bound-book 2px).

## Family rules

| Rule | Result |
|---|---|
| Opens light with the device dark; button switches; reload keeps it; key `jj-mode` | **Pass** |
| Button text/icon “Dark mode” (moon) / “Light mode” (sun), `aria-pressed` | **Pass** |
| theme-color #3B2616 / #1C1610 follows | **Pass** (no dark tab icon: the Library has none, fine) |
| Head script sets `data-mode` before paint, always | **Pass** |
| Old key `jemmas-library-mode` moved once and removed | **Pass** |
| Storage blocked: light, no errors, button still works | **Pass** |
| Footer: ❦ rule, name (display font, not italic), line 1 word for word, credits with capitals | **Pass** (the ❦ is drawn in the system font: Should fix 1) |
| Credits one per line on phones, no edge dots on wide | **Pass** (4 rows at 390; 0 edge dots at any width) |
| Back to top and Dark mode 44 px and level; Back to top focuses the page | **Pass** at all 6 widths, both modes |
| Footer 12.5 px, muted ≥4.5:1 both modes | **Pass** (5.15:1 / 7.4:1; the dots and ❦ are decorative, 2.0:1) |
| Menu at ≤900 (899 yes, 901 no); 44 px button; name 26 px | **Pass** |
| `aria-expanded`/`aria-controls`; closed drawer inert (20 Tabs never reach it) | **Pass** |
| Opens on the page’s link (Home when none), not “← Jemma’s Journals” | **Pass** |
| Escape/scrim return focus to Menu; link/search → `#view` | **Pass** |
| While open everything else inert; body doesn’t scroll | **Pass** (Tab past the last link goes to the browser, never to hidden page parts) |
| Crossing 900 px resets it | **Pass** |
| Scrim 45 % black; “← Jemma’s Journals” first, 32 px tall | **Pass** |
| robots meta noindex, noai, noimageai | **Pass** |
| No fonts/files from other sites | **Pass** (0 external requests on 468 page checks) |
| Line 1 true? (“Made with HTML, CSS and JavaScript, kept on GitHub”) | True. Read-only without the server now makes “no tracking, no ads” hold for plain hosting too. |

## Shared-code notes (for moving into Jemma’s Journals)

All paths in `library/site/`.

**Dark mode**
- **Head script:** `index.html:23`, one IIFE before the stylesheet. Reads `jj-mode`. If null, reads `jemmas-library-mode` and copies it to `jj-mode`, then always removes the old key (all in try/catch). Sets `data-mode` on `<html>` to `dark`/`light`. If dark, sets `meta[name=theme-color]` to `#1C1610`.
  - Markup defaults: `index.html:2` `<html lang="en-GB" data-mode="light">`, `index.html:17` `<meta name="theme-color" content="#3B2616">`.
- **Toggle:** `js/app.js:1427–1442`.
  - `MODE_KEY = "jj-mode"`.
  - `showMode()` (1429) writes the button’s innerHTML as `ic("sun"|"moon") + "Light mode"|"Dark mode"`, sets `aria-pressed`, and updates theme-color.
  - The click handler (1435) flips `data-mode`, saves with try/catch, and calls `showMode()`. `showMode()` also runs once at load (1442).
  - Icons come from `ic()` (app.js:3), which wraps `ICONS[name]` from `js/icons.js` with `class="i" aria-hidden="true"`.
- **CSS:** tokens at `site.css:7–24` (`:root`) and dark overrides at `site.css:26–29` (`:root[data-mode="dark"]`, including `color-scheme:dark`). Extra dark rules at `site.css:931–932`. No `prefers-color-scheme` anywhere.

**Footer**
- **Markup:** `index.html:42–45`, inside `<main>` after `#view`. `footer.foot` contains:
  - `div.foot-orn[aria-hidden] > span` (❦),
  - `b.foot-name`,
  - `div.about-site > p` (line 1) + `p` (credits as `span.cr` + `span.sep[aria-hidden]` with `&nbsp;·`),
  - `div.foot-links > button#toTop.totop + button#modeBtn.mode-text[aria-pressed]`, both filled by JS.
- **CSS:** `site.css:96–110` (`.foot`, `.foot-orn` with `::before/::after` gradient rules, `.foot-name`, `.about-site` 12.5 px muted with `text-wrap:balance`, `.about-site .sep`, `.about-site .cr{white-space:nowrap}`, `.foot-links`, `.foot .totop/.mode-text` 44 px, hover underline). Phones: `site.css:901–904` (`@media (max-width:600px)`: `.sep{display:none}`, `.cr{display:block}`).
- **JS:**
  - `footDots()` at `app.js:1444–1450` hides a `.sep` whose next credit starts a new line; it runs on resize, `document.fonts.ready` and load.
  - **Back to top:** `app.js:1428` sets its innerHTML (`ic("arrow-up")` + text). The handler at `app.js:1451–1454` does `scrollTo({top:0, behavior: smooth unless prefers-reduced-motion})` and then `#view.focus({preventScroll:true})`. `#view` has `tabindex="-1"` (`index.html:39`).

**Menu drawer**
- **Markup:** `index.html:29–38`.
  - `div.topbar > button#menuBtn[aria-controls=side][aria-expanded] > span#menuIco + "Menu"`, then `a.topbar-name` (“Jemma’s <em>Library</em>”, `#home`).
  - `div.scrim#scrim`.
  - `aside.side#side[aria-label]` containing `a.home-link` (first), `a.brand`, the search and `nav#nav` (filled by `renderNav()`, app.js:368–388; the current link gets `class="on"` + `aria-current="page"`).
  - Skip link at `index.html:27`.
- **JS:** `app.js:1398–1422`.
  - `phoneNav = matchMedia("(max-width:900px)")`.
  - `setMenu(open, focusBack)` (1400–1412):
    - toggles `body.nav-open` and `aria-expanded`;
    - `side.inert = phone && !open`;
    - sets every `body > *:not(#side):not(#scrim):not(script)` inert while open;
    - on open, focuses `#side .nav a.on || #side .brand` after 30 ms;
    - on close with `focusBack`, focuses `#menuBtn`.
  - `menuOpen()` (1413).
  - Listeners: Menu click toggles; scrim click closes with focus back; document Escape closes with focus back; a link clicked inside `#side` closes and calls `toPage()` (focus `#view`); Enter in `#q` does the same; a `phoneNav` change closes it, with focus back if focus was inside.
  - `setMenu(false)` runs at load.
  - `route()` (1508–1532) also closes it after any page change (1531) and avoids focusing a nav link on phones (1526).
- **CSS:** `site.css:740–763`.
  - `.topbar,.scrim{display:none}`.
  - `@media (max-width:900px)`: sticky `.topbar` 58 px with `env(safe-area-inset-top)`; button 44 px; `.topbar-name` 26 px; `.side` off-canvas `translateX(-102%)` + `visibility:hidden` with a delayed visibility transition, z 30; `body.nav-open .side` shown; `body.nav-open .scrim` fixed, 45 % black, z 25; `body.nav-open{overflow:hidden}`; nav links 44 px; `main{margin-left:0}`; `.skip:focus{left:12px}`.
  - Reduced motion: `site.css:763`.
  - Focus: `site.css:52–53` (`:focus-visible` uses `--focus`; brass inside `.side`) and `site.css:749` (topbar).
- **Home link:** `site.css:63–64` (10 px uppercase Manrope), `site.css:598` (bound-book colour), `site.css:759` (padding in the drawer), `index.html:34`.
- **Library-specific parts to keep local:** the Bound book colours (cloth/gilt tokens, `--weave`), `.brand`, the search box, and `renderNav()`’s content. What can be shared: the head script, `showMode`/toggle, `footDots`/Back to top, and `setMenu` plus its listeners, given ids `#menuBtn #side #scrim #view #toTop #modeBtn` and per-site theme-color values.

## Tests result

- `python -B -X utf8 tests/run_tests.py`: **318 tests, 317 OK, 1 failure** (161 s). The failure was “the Stats page at 390, 360 and 320 wide…”, which timed out waiting for its 360 px iframe. It **passes on its own 3 out of 3 times** (`-k stats`, 5 tests OK each time), so it is flaky (Should fix 7), not a broken Stats page.
- `git status` in the Library is the same before and after (clean). The parent’s `tools/serve_all.py` change and `research/reviews/round3-travels.md` came from other sessions.
