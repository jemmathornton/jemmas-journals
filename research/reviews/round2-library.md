# Review, round 2: Jemma’s Library (21 Nov 2026, evening)

Read-only review of `C:\Users\Jemma\Documents\HomeLibrary\site` at **bec49fb** (Bound book everywhere, phone mode with the drawer, family rules). Nothing in HomeLibrary was changed (`git status` is the same before and after).

**How it was checked.** `site/` served from disk through Playwright `page.route` (Edge), at 1600×930, 1280×800, 901×900, 899×900 and 390×844, light and dark (dark by setting `jj-mode=dark` before load). 29 page types each way: Home, All shelves, Adult Fiction, Fantasy, Children’s, Display, Not on a shelf yet, Old Book Collection, Old books Children’s / Fiction / To Find, eight book pages (blurb starting with a number, special edition, no cover, longest title, Pratchett, old book, several authors, no blurb), a not-owned book, Reading, History, To Buy, Authors, Terry Pratchett, Stats, Add a book, New covers, an unknown address; search from the drawer. Each: console errors, failed requests, broken images, alt text, sideways overflow, h1, straight apostrophes, footer buttons. Also: the drawer by button, Escape, scrim, link (mouse and keyboard), search Enter, Tab while closed and open, crossing 900px; dark mode carry, old key, blocked storage; Back to top; focus rings; contrast from the tokens; widths 901–1600 for headings colliding.

**Screenshots:** `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review2\library\` (`<page>_<width>_<light|dark>.jpg`, `_full` for whole pages; also `drawer-*`, `foot_*`, `focus-*`, `search-results_*`, `stats-ledger_901_light.jpg`, `stats-published_901_light.jpg`, `add-lookup_1280_light.jpg`). Raw results: `..\library-sweep-phone.json`, `..\library-sweep-data.json`.

**Tests:** `python -B -X utf8 tests/run_tests.py`: **309 tests, all OK** (229 s). They work on a throwaway copy.

## What’s good

- **Family rules, dark mode: all pass.** Opens light with the device set to dark; the footer button switches, reads “Light mode” with `aria-pressed="true"`, saves `jj-mode`, sets theme-color #1C1610; reload keeps it; back to light works. `jj-mode=dark` before load opens dark, already set when the page becomes interactive (no flash). The old `jemmas-library-mode` is moved over once and removed; `jj-mode` wins if both exist. Blocked storage: opens light, no errors, the button still switches for the visit.
- **Footer: passes on every page at every width.** ❦ between rules, “Jemma’s Library” in Instrument Serif (not italic), line 1 word for word, credits each with a capital, one per line at 390 with no dots. Back to top and Dark mode both 44px tall and level. Back to top scrolls to the top and focuses the page. Text 12.5px: muted 5.15:1 light, 7.44:1 dark; buttons 5.64:1 / 10.6:1.
- **Drawer: nearly all pass** at 899 and 390: Menu bar at 899, sidebar at 901; `aria-controls="side"`, `aria-expanded` follows; closed drawer is inert (25 Tabs never reach it); open: page inert, body doesn’t scroll (wheel on the scrim moves nothing, and the place on the page is kept after closing); Escape and scrim close it and return focus to Menu; Escape in a filled search clears it first; typing keeps it open; crossing 900px closes it and lifts inert. “← Jemma’s Journals” is first in the drawer. The nav scrolls inside the drawer, so Reading … Add a Book are reachable on a phone.
- **Clean:** no console errors except the server calls (below), no failed requests, no broken images, every image has alt text, no straight apostrophes, exactly one h1 on every page but New covers, no sideways scrolling except the two pages below. Keyboard focus clear in both modes (walnut on paper, brass in dark).
- **Fixed since round 1:** figures no longer wrap at 1280 (they do below about 1100, see 4); muted text now 5.15:1; Stats panels are cloth with a gilt border, not walnut slabs; series link uses gilt-ink; the search clear × is gilt; filters, buttons, To Buy cards, Add form, Authors list in the Bound book look.

---

## Broken

None. Nothing fails to load or stops working.

## Should fix

### 1. Choosing a page from the drawer leaves keyboard focus on nothing
- **Where:** drawer at 899 and 390: a link chosen by Enter or tap, the same page chosen again, and Enter in the search.
- **What:** after the drawer closes, `document.activeElement` is `<body>`. A keyboard or screen-reader user starts again from the top of the document instead of on the new page. CLAUDE.md says “a link chosen: the new page takes focus instead”, but it doesn’t.
- **Evidence:** behaviour run: “link (keyboard) → #reading … focus BODY”, same for click, same-page link and search Enter.
- **Why:** `route()` sees the focus came from the nav and focuses `#nav a[href=active]`, which is inside the now-inert drawer, so `focus()` does nothing (the `|| view` fallback is never reached because the link exists). Search Enter calls `q.blur()`.
- **Fix:** in `route()`, use the nav link only when `!phoneNav.matches`; otherwise focus `#view`. After search Enter, focus `#view` (the results).

### 2. Stats runs off the side between 901 and about 1024 wide
- **Where:** Stats at 901–1024 (laptop window half-width, tablets in landscape).
- **What:** “When they were published” has 18 bars with a fixed 10px gap and labels like “1850s”; they can’t shrink, so the newest decades (1990s–2020s, the biggest bars) are cut off and the page scrolls sideways by up to 162px. The top cloth panel also runs the figures together: “162,287307” (pages, then pages per book). The “Two or More Books Rated” and “Written, Not Illustrated or Translated” notes sit on top of their headings.
- **Evidence:** `stats-published_901_light.jpg`, `stats-ledger_901_light.jpg`, `stats_901_light_full.jpg`; sweep: overflow 162 at 901, 105 at 960, 44 at 1024, none at 1100.
- **Fix (general rules):** `.decades div{min-width:0}` everywhere, and use the stand-on-end `.decades.many` labels up to about 1100px, not only ≤600. Let `.ledger-grid` drop to two columns below about 1100. Put a section heading’s note under the heading (as ≤900 does) whenever it would touch the heading (see 3).

### 3. The button or note beside a section heading lands on the heading (901–1100)
- **Where:** Home “Just Finished” + “What Should I Read Next?” (901–960), Reading “Recently Finished” + its button (901–1024), Stats notes (901–1024).
- **What:** the centred heading and the right-hand button/note overlap; “Finished” is half hidden under the button.
- **Evidence:** `home_901_light.jpg`; width scan (901, 960, 1024, 1100, 1180, 1280 …): Home overlaps at 901 and 960, Reading at 901–1024, Stats at 901–1024, none from 1100.
- **Fix:** move the ≤900 rule (`.section-head` in a column, button under the heading) up to about 1100px, or give the heading `padding-inline` equal to the button’s width so they can’t meet.

### 4. Title-page figures still wrap below about 1100 wide
- **Where:** Home, the genre shelves, Old books · Children’s, Reading at 901–1100.
- **What:** round 1’s item 1 is fixed at 1280, but `.figures{max-width:64%}` still sends the third and fourth figures onto a second, indented row at 901–1100 (“425 not read yet …”, “251 authors”).
- **Evidence:** `home_901_light.jpg`; width scan: figures in 2 rows at 901, 960, 1024, 1100 on those pages.
- **Fix:** below about 1150px, use the ≤600 two-by-two grid, or drop the 64% cap once the plate is smaller.

### 5. Drop capital still splits a blurb that starts with a number (round 1, item 3, not done)
- **Where:** book pages, e.g. *A Little Luck* (`#b-2ousnrntqt`).
- **What:** a big “2”, then “0 years after…”.
- **Evidence:** `book-luck_1280_light_full.jpg`, `book-luck_390_light_full.jpg`.
- **Fix:** add the drop capital only when the blurb starts with a letter (a `drop` class set when `/^\p{L}/u` matches). General rule, not this one book.

### 6. Children’s shelf card: gilt name too faint on the mustard cloth (round 1, item 5, not done)
- **Where:** Home, The Shelves, the Children’s card (light and dark; the cloth is the same).
- **What:** gilt #E2C47A on the cloth mix of #CF9A2B works out at about **2.3:1 at the top, 3.2:1 mid-card** for the 21px name, worse for the 15px “97 books”. The others are 4.7:1 or more.
- **Evidence:** `home_1600_light_full.jpg`, `home_390_light_full.jpg`; computed from the `.shelf-card` gradient.
- **Fix:** darken the cloth for light shelf colours (for example mix with 55% #2A170C instead of 28%), the same rule for every card.

### 7. Dark mode: the Old books shelves stay cream (round 1, item 6, not done)
- **Where:** Old books · Children’s / Fiction / Non-Fiction, dark.
- **What:** `.bookshelf` boards are hard-coded cream, so big bright bands cross the dark page; the dashed “to find” spines are pale grey on cream and hard to read.
- **Evidence:** `old-childrens_1280_dark_full.jpg`.
- **Fix:** a dark board for dark mode (dark paper, walnut ledge kept), or keep cream and give gap-spine text a fixed dark brown.

### 8. Page weight: fine on her PC, heavy on a phone or online (round 1, item 7, grown)
- **Where:** everywhere; worst on All shelves.
- **What:** EB Garamond still four TTFs (2.5 MB), all fetched on the first page; Instrument Serif and Manrope come from Google Fonts. First visit to Home: **16.2 MB**. Scrolling All shelves on a phone pulls **93 MB** of covers. `site/covers/` is 817 files, 120 MB; median 65 KB, but 52 are over 500 KB (largest 1.4 MB) and are shown about 100–150px wide.
- **Evidence:** bytes served per page in `library-sweep-phone.json` (`kb`), file sizes on disk.
- **Fix (when she wants phone use away from home, or going online):** WOFF2 subsets of the fonts (about 60–100 KB each; keep the OFL file), self-host Instrument Serif and Manrope as the home site does, and small thumbnail copies of covers for grids and plates (the full scan only on the book page).

### 9. Tab reaches hidden things while the drawer is open
- **Where:** drawer open at 899 and 390.
- **What:** Tab past the last drawer link goes to the top bar’s Menu button and “Jemma’s Library”, which sit under the drawer (the point under Menu is the drawer’s “← Jemma’s Journals”), so focus disappears from view for two presses.
- **Evidence:** behaviour run: “tabbing in open drawer, outside side: #menuBtn / A.topbar-name”; elementFromPoint at Menu = home-link.
- **Fix:** make `.topbar-name` inert while open and either let Menu sit above the drawer (as a close button) or make it inert too and close with Escape/scrim only. The family rules don’t ask for a focus trap, so this is small, but it is the one place focus goes invisible.

## Polish

1. **New covers page on a phone runs off the side** by 43px; the text column is cut off, and it shows working notes (“needs taking off no-cover.json”). No h1 on it either. It’s a temporary page for her cover choices, so either let `.trial-row` stack at ≤600 or leave it until the covers are decided. Evidence: `trial_390_light.jpg`.
2. **The New covers switch covers a Got It button at 601–900.** It stays fixed at the bottom right until 600px, over the To Find cards (`old-to-find_899_dark.jpg`), and its z-index (50) puts it above the drawer’s scrim (25). Make it static from 900px down, as at 600.
3. **Sidebar links still go off the bottom on her laptop** (round 1, polish 4): at 1280×800 Reading … Add a Book are below the fold; at 1600×930 Authors is cut in half and Stats and Add a Book hidden, with no hint that it scrolls. Evidence: `home_1280_light.jpg`, `authors_1600_light.jpg`.
4. **Focus on opening the drawer goes to “All Shelves”, not the page’s own link** (CLAUDE.md says the page’s link). `querySelector("#side .nav a.on, #side .nav a")` returns whichever comes first in the page, which is always All Shelves. The family rules say “first link”, so this passes the family check; to match her note, query `a.on` first and fall back to the first link.
5. **Stats panel on a phone is rounded** (`.ledger{border-radius:14px}` in the 600px block overrides the Bound book’s square 2px). `stats_390_light_full.jpg`.
6. **“Set up phone scanning” box** keeps the old rounded Manrope look, and shows on a phone too. `add_390_light_full.jpg`.
7. **Still from round 1:** “ISBN-13” in old-style small capitals reads “ISBN-ı3” (`book-luck_1280_light_full.jpg`); justified blurbs leave wide gaps at 1280; the ornament under left-aligned book-page headings; “Got It” on buttons vs “press Got it” in the sentence above (`to-buy_1280_dark.jpg`, `old-to-find_899_dark.jpg`); shelf pages jump from h1 to h3.
8. **Fantasy shows “12 read but not owned” in the figures and “14 not owned” above the books** (the extra two are reading/paused). Both true, but side by side they look like a mismatch. A label like “not owned” for both, or leave it.
9. **manifest.json** still has the pre-L1 paper colour (`background_color` #F7F1E4; the page is #F3EAD5). Only shows as the splash when installed.

## Questions for her

1. **Footer line 1 isn’t quite true here.** “Made with plain HTML and CSS” — the Library is mostly JavaScript, and Add a book, Got it, the marks and phone scanning need her own server. And “no tracking” holds, but two of the fonts are fetched from Google, which sees each visit’s address. The family rule says to tell her rather than change the words. My suggestion (not decided): self-host the two Google fonts (fixes the second point) and keep the line as it is.
2. **Green Display card** (round 1, question 1, still open): the whole Display cloth on Home is dark green (#3F6B4A); her rule is no green. Show her a picture with a brown alternative?
3. **Drop capital after an opening quote mark** (round 1, question 2): keep the large “ + letter on 16 blurbs, or start those blurbs plain like the number case (my suggestion, not decided)?
4. **Add a book without her server** (round 1, question 3, unchanged): the page polls `/api/scanned` every 4 s (a console 404 each time) and Look It Up says “Couldn’t reach Open Library. Fill in the details yourself.” when the real cause is that her server isn’t there. Home also asks `/api/reading-status` and `backup-status.json`. Fine on her PC; needs a decision before it goes online (hide Add a book, Got it and the marks when there’s no server?). Evidence: `add-lookup_1280_light.jpg`.
