# Review, round 5: Jemma’s Library after the 22 Nov changes

Read-only review of `Documents\JemmasJournals\library` at **d446ef0** (on `main`; `git status` clean before and after). This review changed nothing in any repo. The only files it wrote are this report and the screenshots.

- Every non-GET request was answered inside Playwright and never reached a server. This includes the one POST to `/family/mode` when Dark mode was pressed.
- The family server’s `data-jj-server-mode` was rewritten only inside the browser. `logs/family-mode.txt` is the same as before (checked byte for byte).
- `api/lookup`, `api/covers`, `api/straighten` and `api/scan-setup` were never asked for.

**Changes by other sessions while this review ran.**
- The parent got new commits (a655695, 38dc7af) and changes to its working tree.
- `tools/serve_all.py` was restarted at 13:45. For about a minute 8050 refused or reset every connection, which broke part of the first sweep (901 dark onwards). Those widths were swept again.
- Another session ran the Library’s unit tests.

## How it was checked

- **Pages:** 43 addresses through http://localhost:8050/library/ (her save server 8020 behind it, so LIVE):
  - Home, All shelves, all 11 shelves (including the empty “Not on a shelf yet”), Old books Children’s/Fiction/Non-Fiction/To find, Reading, History, To buy, Authors, Stats, Add, New covers, an unknown address.
  - 13 book pages: no cover (*Witness*), a second no-cover, the longest title, the longest no-cover title, the longest blurb, a blurb opening with a quote mark, two series books, a special edition, a signed-to-you copy, a rated book, an old book, an old book with her note, a review with a spoiler.
  - 2 not-owned books and 3 authors (Enid Blyton, a one-book author, the longest name).
  - Each at **1600, 1280, 1000, 901, 899 and 390, light and dark**.
  - Result: **clean on every page at every width and mode** (516 page checks), apart from the problems below and the known missing h1 on New covers.
  - Each page was scrolled to the bottom so lazy pictures load. Checks on each: console and page errors, CSP violations (a `securitypolicyviolation` listener), inline `on…` handlers, failed and 4xx requests, outside requests, broken images, sideways scroll, text cut sideways, section-head overlaps, title alignment in cover rows, stars over covers, `data-mode`, top bar vs sidebar, closed drawer inert, footer buttons and dots.
- **Every internal link:** 1,001 distinct addresses followed from Home. Each must draw its own page (no silent fall back to Home), with one h1 and no “undefined” or “NaN”. A text scan of all 1,001 pages looked for straight quotes, doubled words, space before punctuation and US spellings.
- **Behaviour:**
  - Sidebar fades at 1280×800, 1280×720, 1600×1000 and 1000×700, including Tab to the last link.
  - Drawer at 390 and 899; search (9 terms, including an ISBN with and without hyphens, markup and accents).
  - Dark mode pressed, carrying to Jemma’s Journals and to another Library tab, then back.
  - Stars (cursor, selection, list view); keyboard Tab order and focus rings on Home.
  - Tesseract and ZXing loaded under the CSP, and a real OCR run.
  - The Add page’s lookup with the API down (stubbed).
- **Other modes:** opened as a file (with `jj-mode` dark already saved); the online-style copy at http://localhost:8060/library/ (`tools/build_site.py --serve`, current at the time of the check).
- **axe-core** on 19 pages × 1600/390 × light/dark, with `bypassCSP` (see Tests 2).
- **Data:** the figures on Home, All shelves, every shelf, Stats, Reading, History, To buy and the old-books pages compared with each other and with the sidebar.
- **Files:** every cover and thumbnail decoded with Pillow; covers referenced vs on disk; thumbnails vs covers.
- **Performance:** page weight first and after scrolling, at 1600 and 390, for 16 page types.
- **The full test suite.**

**Screenshots:** `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review5\library\`
- `<address>_<width>_<mode>.jpg`: 1600 and 1280 from the first sweep; `_b` = 901 dark again; `_c` = 899 and 390 again.
- Close-ups:
  - `zoom-home-figures-rule_1600.jpg`, `zoom-fantasy-figures-rule_1600_dark.jpg` (Broken 1)
  - `shelf-row-misaligned_fantasy_1280.jpg` (Should fix 1)
  - `sidebar-addabook-focused_1280x720.jpg` (Should fix 3)
  - `sidebar-fade_*.jpg`, `drawer-open_390.jpg` / `_899.jpg`, `footer-credits-dots_1600_x3.png`, `footer_<w>_light.jpg`, `home-just-finished-head_390.jpg` / `_1000.jpg`, `search-harry-potter_1280.jpg`, `add_1280_light.jpg`, `add-lookup-failed_1280.jpg`, `stats_1280_dark-after-press.jpg`, `book-rated_1280_dark.jpg`, `file-mode_stats_1280_dark.jpg`
- Scripts and raw results: `…\scratchpad\r5lib\` (`sweep*.out`, `interact.txt`, `perf.txt`, `axe.txt`, `crawl.json`, `text.json`, `data.json`, `tests.txt`).

## Today’s changes: did they land?

| Change (22 Nov) | Result |
|---|---|
| Stats in the Bound book look | **Yes.** Mounted paper figure panel (square, two by two at ≤1100), chart names in EB Garamond, italic figures, thin square bars in shelf colours / `--chart`, square decade bars. No overlaps at any width; no sideways scroll at 390. |
| Stars under covers, no strip | **Yes**, on book pages (`figure.plate`) and cover cards. Arrow cursor, not selectable, `role="img"` with an aria-label, none in list view or shelf fans, never over the cover. **But the cover rows lose their line: see Should fix 1.** |
| Permanent thumbnails | **Yes.** Home cards use `covers/thumbs/*.webp` (79 small pictures on Home); banners use `*-s.webp`. All 1,632 thumbnails exist, decode, and are smaller than their covers. The fallback works (test). **New covers never get one: see Should fix 2.** |
| Sidebar fade | **Yes** at the top and foot while more links are hidden; none when the list fits. In the drawer too. **A focused last link sits in the fade: see Should fix 3.** |
| ISBN capitals | **Yes.** `dt.caps` = `font-variant: lining-nums`; other labels stay small capitals. |
| Blurbs ragged right | **Yes.** No `justify` left in site.css; drop capital kept. |
| Ornament under the heading on phones (≤1100) | **Yes.** At 1000 and 390 the ❦ is drawn by the `h2` and the button sits 10px below it; at 1280+ the ❦ is on the section head as before. |
| Footer dot spacing | **Yes: 5.5px each side** (measured on the glyphs at 1600). Dots hidden at 390. Never at a line start or end (all pages, all widths). |
| Ornaments in EB Garamond | **Yes.** Font lists start with “Library Ornaments”. (★ is outside its range: Looks 4.) |
| CSP | **Holds everywhere:** no violation on any page in any sweep, no inline handler. Tesseract (worker plus WASM) and ZXing load and read a number under it. It is judged in Should fix 6. |

## Round 4 fixes: did they hold?

- **Held:** `request_queue_size = 128` in `serve.py`; the skip link has no inline `onclick`; old-book spine lettering picks the better of gilt and dark; ornaments are in EB Garamond.
- **Still open from round 4:**
  - **Opened as a file:** still 3 × `ERR_FILE_NOT_FOUND` (`file:///C:/family/mode.js`, `family.css`, `family.js`) on every load. With dark saved, the first paint is still light (`data-mode` “light” at `interactive`, dark only after `app.js`). See Should fix 7.
  - `/family/README.md` is still served by 8020 (harmless).
  - Old-book spines are still under 4.5:1 on mid-tone cloths. axe flags 10 spines on Old books · Children’s, worst 3.91:1 (see Old books).

---

## Broken

### 1. The figures’ rules run across the cover plate at 1600 wide
- **Where:** every page with a cover plate and figures, at about 1500–1600 wide. Seen at http://localhost:8050/library/#home, `#shelves`, `#shelf-fantasy`, `#shelf-childrens`, `#history`, `#authors`, `#a-enid-blyton` and `#shelf-old-book-collection`. Light and dark.
- **What she’d see:** the double rule above the figures and the thin rule under them run about 25px into the mounted plate. They are drawn over its cream mount and onto the first column of covers: across “Michelle Obama” on Home, across the Trudi Canavan covers on Fantasy.
- **Why:** `.figures{max-width:64%}` and `.hero.shelved h1{max-width:64%}`. At 1600 that is 684px, so they end at x=1090, but the plate starts at x=1065. The text sits above the plate (`z-index:2`), so the borders are painted over the covers. At 1440 and below it clears. The h1 box also reaches 9–14px into the plate at 1000 and 901, but the letters stay short of it.
- **Fix:** limit the text column by the plate, not a percentage. For example, `max-width: calc(100% - <plate width> - 32px)`, or a grid with the plate in its own column.

## Should fix

### 1. Stars under covers push titles out of line (her decision’s side effect)
- **Where:** every cover grid with a mix of rated and unrated books. On http://localhost:8050/library/#shelf-fantasy, 20 of the rows are uneven; on `#shelves`, 68 rows; on `#shelf-adult-fiction`, 25. Also on Home’s “Just finished” (only *Hope Street* is rated), History, Reading and author pages. Every width, both modes.
- **What she’d see:** in one row, a rated book’s title and author start **25px lower** than its neighbours’. Example: *The Restaurant at the End of the Universe* and *Foundation* sit higher than *The Bear and the Nightingale* beside them (`shelf-row-misaligned_fantasy_1280.jpg`). The covers stay level; only the text steps.
- **Options (her call; my suggestion, not decided):**
  - (a) every card in a grid keeps an empty star line of the same height, so all titles line up and unrated books show a small gap;
  - (b) the stars go under the author line instead, so titles line up and only the card’s foot varies;
  - (c) leave as is.
- On book pages (one cover) it is fine.

### 2. A cover added or changed later never gets a small copy, and a changed cover keeps its old small copy
- `make_thumbs.py` is run by hand only. Nothing calls it: not `serve.py`’s Add-a-book or rebuild, not `build.py`, not the weekly backup.
- **New book added on the site:** Home’s “New on the shelves” shows exactly the newest books. For each one Home asks for `covers/thumbs/<isbn>.webp`, gets a 404 (a red console error), then loads the full cover. The fallback hides it, but the saving is lost exactly where it matters.
- **Cover replaced:** for example a straightened or chosen-again cover at the same name. `thumbSrc()` keeps the cover’s `?v=` hash, so the address changes, but the file in `thumbs/` is still the old picture until `make_thumbs.py` runs. **Home and every banner would show the old cover** while book pages show the new one.
- Today all 1,632 small copies are up to date (none older than its cover). So this is a gap waiting to happen, not a visible fault yet.
- **Fix:** run `make_thumbs.make()` for the one cover inside `serve.py` after a cover is saved, and at the end of `build.py`. Add a check to `test_build`’s “site up to date” test: every cover has both small copies, none older than the cover.

### 3. With the keyboard, the sidebar’s last link sits inside the fade
- **Where:** http://localhost:8050/library/ at laptop heights (1280×720, 1000×700; at 1600×1000 the list overflows by only 24px and it still happens). Tab down the sidebar to “Add a Book”.
- **What she’d see:** “Add a Book” and its focus ring are faded to almost nothing at the foot (`sidebar-addabook-focused_1280x720.jpg`).
- **Why:** Tab scrolls the link only just into view. The nav’s 16px bottom padding stays below, so `scrollTop` is 288 of 304 and `more-below` stays on. The 48px mask then covers the focused link.
- **Fix:** `scroll-padding-block: 48px 56px` on `.nav` (or `:focus-visible{scroll-margin-block:56px}` on its links), or drop the fade while focus is inside the nav. A mouse wheel to the bottom is fine (the fade goes).

### 4. Shelves load the full-size covers: 105 MB for All shelves
- Measured after scrolling, at 1600 (390 is about the same):

| Page | Pictures loaded | Small copies would be about |
|---|---|---|
| http://localhost:8050/library/#shelves | **105 MB** (709 covers) | 12 MB |
| `#shelf-fantasy` | 41 MB | 4 MB |
| `#shelf-adult-fiction` | 30 MB | |
| `#shelf-childrens` | 14 MB | |
| `#a-enid-blyton` | 10 MB | |
| A book page | 3–4 MB (its own cover plus “More by”) | |

- Home is now 2.95 MB (1.5 MB of pictures).
- **Why:**
  - Only Home uses `thumbs/` (`thumbSrc()` returns nothing unless the address is `#home`). Shelf cards are 222px tall at most, the same size as Home’s cards.
  - The covers themselves are bigger than the notes say. `copy_covers.py` makes covers 600px tall, but **376 of the 816 files are taller** (up to 2,560px; 49 files over 500 KB; the largest `9781035901364.jpg` is 1.4 MB). They came in through the sharper scans, straightening and her own photos, not `copy_covers.py`.
- **On her PC this is just slower;** online (her phone) it would be a lot of data.
- **Fix:**
  - (a) use the 460px small copies on every cover grid (shelves, authors, history, More by) and keep full covers for book pages. That is one change in `thumbSrc()`, and it was her pick for Home already.
  - (b) also cap the covers themselves at about 1,000px tall for the book page, with `make_thumbs`-style resizing.
  - Changes nothing she sees.
- Related: unknown addresses (e.g. `#nope`) draw Home but use full covers, because `thumbSrc()` reads `location.hash` rather than the page being drawn.

### 5. Search heading: “Results For ‘9780552134637’”
- **Where:** type an ISBN (or anything without letters) in the search.
- **What she’d see:** “Results **For** ‘9780552134637’”; for words it is “Results for ‘pratchett’”.
- **Why:** `capitaliseEls()` counts only words with a letter, so “for” is taken as the last word and capitalised.
- **Fix:** count the search term (`.keep`) as a word even when it has no letters.

### 6. Content Security Policy: good, with two notes
- **Strong points:** `script-src 'self'` with no inline code, no eval, `object-src 'none'`, `base-uri` and `form-action` limited, `frame-src 'none'`; set before any script. No violations anywhere, including the OCR worker (its own script, so its WASM is not blocked).
- **`img-src … https:`** lets the page show a picture from any HTTPS site. Only the Add page needs it, and the Add page exists only with her server (LIVE). Online (read-only) it is never used, but still open.
  - Every page builds its HTML with `esc()`, so injected markup is unlikely. The risk is a tracking pixel through some future slip, which sits against “no tracking” in the footer.
  - **Tighter (my suggestion, not decided):** either list the hosts the lookup really uses (`covers.openlibrary.org`, `books.google.com`, `images-na.ssl-images-amazon.com`, `pictures.abebooks.com`, `image-server.worldofbooks.com`, Oxfam’s image host, Goodreads’ image host), or have `serve.py` pass looked-up pictures through `/api/…` so `img-src 'self' data: blob:` is enough.
- A `<meta>` CSP can’t set `frame-ancestors`. Online, a header (or GitHub Pages’ defaults) would be needed to stop framing. A note for going online.
- Side effect: **the family’s axe check `tests/axe_all.js` can no longer inject axe into the Library**. `page.addScriptTag({content})` is blocked by `script-src 'self'` and the script stops with an error (seen in this review). Fix there: `browser.newContext({ bypassCSP: true })`.

### 7. Opened as a file: three errors and a flash of light (round 4, still open)
- **Where:** `site/index.html` opened from the folder.
- **What she’d see:** three “Failed to load resource” errors in the console. With dark chosen, the page draws light first and turns dark a moment later.
- **Fix (family-wide):** a small loader in `<head>` that picks `/family/` or `../../site/family/` before the first paint.

### 8. Smaller points
- **Online (8060), every page load logs a red 404** for `api/reading-status` (the LIVE check). Harmless, but every visitor’s console shows an error. Only ask when the host is `localhost`/`127.0.0.1`, or answer the check with a static `api/reading-status` file that is not JSON.
- **The Add page’s lookup messages assume the reply is a lookup.**
  - `api()` never checks `r.ok`. A JSON error reply with no `error` field is shown as “Open Library, Waterstones and Goodreads don’t know that number yet”.
  - A non-JSON reply (8050 up but 8020 down) says “Couldn’t reach Open Library” when it is her own server that is missing.
  - A real outage on her PC would mislead her.
  - Fix: on a non-OK status, say the library server didn’t answer.

## Looks (list only, for her)

1. Cover rows uneven where some books have stars: http://localhost:8050/library/#shelf-fantasy (Should fix 1).
2. Stars twice on a rated book page: under the cover and in the Your reading panel. Example: http://localhost:8050/library/#b-j7z4907qlq.
3. Empty stars are very faint: about 1.4:1 on cream in light mode, near-invisible dark grey in dark mode. A 2-star book reads as “two stars” only. Example: http://localhost:8050/library/#b-6uc5yww8dt (dark).
4. ★ is still drawn by the system symbol font: “Library Ornaments” covers only ← ❦ ❧, and EB Garamond has no ★.
5. The sidebar fade also shows when only 24px is hidden (1600×1000): the last link is half-faded for a tiny overflow.
6. Banner plates load 32 small covers but show 18 (6 on phones). Not visible: 14 extra requests per page (tiny files now).
7. Still open from earlier rounds: “Got It” vs “Got it”; New covers page at 390 off the side and with no h1 (LIVE only); the old-book spines (below).

## Old books (brief: she’ll sort these herself)

- **Spine contrast:** 10 spines on http://localhost:8050/library/#old-childrens under 4.5:1. Examples: “The Island of Adventure” 3.91:1 (`#3a2614` on `#77898c`); series numbers 4.12:1 (`#f6de9c` on `#7a6650`). Same in dark mode.
- The New covers switch (bottom right, LIVE only) is still there for the 82 trial covers. The online copy still ships `covers-trial/` (3.1 MB, never shown read-only).
- Nothing else broke on the old-books pages: no errors, no sideways scroll at any width, footer fine.

## Data

- **Counts agree** across Home, Stats, All shelves, each shelf, the sidebar, Reading and History:
  - 599 books.
  - 70 read in 2026 (= the month bars 13+8+3+6+6+5+18+8+2+1).
  - 425 not read yet.
  - 172 read on the shelves (29%) and 229 read in all.
  - 200 rated (= the “How you rate” bars).
  - 66 old books (= 53+4+9).
- **Two counts that look different for the same thing:**
  - **Authors:** Home and All shelves say “251 authors” (people who wrote one: her rule, 21 Nov), but the sidebar says “Authors 267” and the Authors page “267 people”. A sidebar figure of 251 (or a Home label of “writers”) would make them agree.
  - **To buy:** the sidebar says “To Buy 59”, but the To buy page says “29 to buy · 30 old books to find”. The 30 are also counted under Old books → To Find 30.
- **Titles:** *A/S/L* (Jeanne Thornton) shows as “A/s/l” on its page and cards (Libib’s spelling; StoryGraph has “A/S/L”). Needs a `displayTitle`. *The Story of a New Name*: Libib’s title “The Story of a New Name : My Brilliant Friend Book 2 (Neapolitan Novels)” keeps its space before the colon in the Full title row, on http://localhost:8050/library/#b-0b5q53udcu. Data, not a code fault.
- **Links:** all 1,001 internal addresses draw their own page. The only non-# link is “← Jemma’s Journals” (`/`).
- **Files:**
  - 787 covers referenced, all present and decodable.
  - 29 files in `site/covers/` are referenced by nothing (3 MB, e.g. `9780007559220.jpg`, `9780246114235.jpg`). Left from cover changes; they are published with the site.
  - Every referenced cover has both small copies.

## Text

- **Clean:** no straight apostrophes or quotes in any shown text (all 1,001 pages; book data with `'` is curled by `esc()`), no doubled words, no US spellings in the site’s own words. Footer line 1 is word for word the family’s (“…HTML, CSS, JavaScript and Python, kept on GitHub.”). Credits have capitals.
- “Results For ‘<number>’” (Should fix 5).
- Stats heading “Most Books By” (with the note “Written, Not Illustrated or Translated”): the title-casing turns the final “by” into “By”. “Most books by” would read better.
- **Notes out of date:**
  - library/CLAUDE.md says “331 tests” (now 339).
  - `tools/make_thumbs.py`’s docstring says it is “for the Try switch ‘Pictures on Home: Smaller’” (the switch is gone).
  - CLAUDE.md says covers are “at most 600px tall” (376 aren’t: Should fix 4).

## Performance

- **Weight:** see Should fix 4. Every page also loads:
  - `data.js`: 866 KB, sent uncompressed by `serve.py` and `serve_all`. GitHub Pages would gzip it to about 150 KB.
  - Fonts: 329 KB.
  - `app.js`: 144 KB.
  - `zxing.min.js` (336 KB) and Tesseract (about 11 MB) load only when the camera is used. Good.
- **Speed (local):** DOMContentLoaded 150–360 ms on every page measured. All shelves has 7,943 elements and 709 pictures, and is 43,000px tall at 1600 (68,500px at 390). Rendering is fine on the laptop; on a phone it will be heavy mainly because of the pictures.
- **Slowest to settle:** Home (1.4 s first load: 97 requests), then All shelves (1.2 s before scrolling).
- The service worker (`sw.js`) passes every request to the network, so it adds a step to every request. Online it gives visitors nothing (she prefers the shortcut to the installed app). Consider registering it only on localhost.

## Code

- **Try switch leftovers:**
  - None in the code: no `trySmall`, `TRY SWITCH`, `try-` classes or attributes. The banner’s inline `onerror` was replaced by the listener.
  - One comment is left: `/* her stars on a cover */` above the new block (site.css:324). Duplicated, conflicting comments sit at site.css:458–461 (“every cover the same height…”, twice).
  - The `make_thumbs.py` docstring (Text).
- **`thumbSrc()` decides by `location.hash`,** not by the page being drawn. It works for Home, but `#nope` draws Home with full covers, and a test calling `route("home")` from another address would differ. Pass “small” from the caller (`pageHome`, `shelfBanner`) instead.
- **Two error listeners** (window for thumbs, document for covers) depend on capture order and `stopImmediatePropagation`. It works and is commented, but is fragile. A single listener that tries the full cover first and then the title card would be simpler.
- **Duplication:**
  - `fact()` is defined twice (pageBook, pageSgBook) with the new `caps` rule copied into both.
  - `ratedLine()` and `starsShown()` build the same two-row star markup.
  - In site.css the L1 layer and later review blocks override earlier rules again and again. For example, `.bar-row .track i` is set at lines 276 and 717, `.decades i` at 282 and 719, `.search input` at 77 and 601, and `--chart` is defined mid-file (line 720) rather than with the tokens at the top. It works, but each change now needs a search for the last override.
- **`serve.py`:**
  - The LIVE check (`checkLive()` → `api/reading-status` with `X-Library: 1`, JSON only) works through 8050, 8020 and 8060 (8060 → read-only, no Add a book).
  - Host check, header check and `/family/` name rule are unchanged and sound.
  - `/family/README.md` is still served.
  - `GET /api/scan-setup` returns the scan key to anything that can send the `X-Library` header from this computer. Cross-site pages can’t (a custom header needs a pre-flight, which isn’t answered). Fine.
- **The online-style copy** (`tools/build_site.py`, parent) also publishes `site/covers-trial/` and the 29 unreferenced covers. It no longer publishes `backup-status.json` (git-tracked files only): good.

## Tests

1. **The suite:** `python -B -X utf8 tests/run_tests.py`: **339 tests, all OK** (238 s, run while other sessions were busy). `git status` in `library/` clean before and after.
2. **Gaps that let today’s problems through** (one test each):
   - Titles in one cover row start at the same height (or whatever rule she picks for Should fix 1).
   - No hero text box overlaps the plate at 1440–1600 (Broken 1).
   - Every cover has both small copies, newer than the cover (Should fix 2).
   - Tab to the last sidebar link at 1280×720: the link is fully visible, not under the fade (Should fix 3).
   - Search for an ISBN: the heading keeps “for” in lower case (Should fix 5).
3. **The family’s `tests/axe_all.js` breaks on CSP pages.** It needs `bypassCSP: true` in its context (Should fix 6). This review’s axe run used it: the only serious problem is the old-book spine contrast. There are also two moderate ones: heading order (book-title h3 under the page h1 with no h2 on shelf pages), and the top bar’s name outside a landmark at 390.
