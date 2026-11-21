# Review: Jemma’s Library after “L1 · Bound book” (21 Nov 2026)

Read-only review of `C:\Users\Jemma\Documents\HomeLibrary\site` at commit c88a065 (L1). The phone-mode session’s uncommitted drawer changes were also in the tree; they only apply under 900px wide, so the laptop views below are L1 as committed. Nothing in HomeLibrary was edited.

**How it was checked.** `site/` served from disk through Playwright (`page.route`, Edge), at 1600×930 and 1280×800, light and dark (`colorScheme`). 40 page types each way: home, All shelves, every shelf (incl. the empty “Not on a shelf yet”), Old books Children’s / Fiction / To Find, book pages (blurb, no blurb, long blurb, numeric first word, series + review, signed, signed to you, special edition, no cover, old book, several authors, long title, Discworld), not-owned pages (with and without a shelf), Reading, History, To Buy, Authors, an author with 109 books and one with 1, Stats, Add a book, New covers (trial), an unknown address, plus search (“pratchett”, “harry”, no results), the pick pop-up and list view. Each page: console errors, failed requests, broken images, sideways overflow, alt text, heading order, straight quotes, US spellings. Contrast measured from the CSS tokens and from pixels.

Screenshots: `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review\library\` (named `<page>_<width>_<light|dark>.jpg`, `_full` for whole pages; also `focus-*`, `search-*`, `pick-popup_*`, `stats-authors_*`, `dropcap-*`, `facts-crop_*`, `ornament-crop_*`, `before-L1_shelf-adult_1280.jpg`). Note: in the `_full` pictures the sidebar stops partway down; that is how full-page screenshots draw a fixed sidebar, not a fault.

**Tests:** `python -X utf8 tests/run_tests.py` (run with `-B` so nothing is written): **253 tests, all OK, 70 s.** They use a throwaway copy of the library.

**Clean:** no console errors on any page (only Add a book, which asks her PC server), no failed requests, no broken pictures, no sideways scrolling, every image has alt text, no straight apostrophes in shown text, no US spellings in the site’s own text (“color”, “neighborhood” appear only inside a publisher’s blurb, which her rule keeps word for word). L1 changed only CSS (and fonts). It added no words; the only new text is the ornaments ❧ and ❦. Keyboard focus shows clearly in both modes (walnut ring on paper, brass in dark and on the sidebar).

**Phone layout:** not reviewed (being built separately).

---

## Broken

None found. Nothing fails to load or stops working.

## Should fix

### 1. Title-page figures wrap onto a second line at 1280 (her main width)
- **Where:** Home, Reading, and the Adult Fiction, Fantasy, Science Fiction, Young Adult, Children’s, Non-Fiction shelves and Old books · Children’s, at 1280×800 (fine at 1600).
- **What:** `.figures` is capped at `max-width:58%`. Four or five figures don’t fit, so the last one (“267 authors”, “34,163 pages”, “24 on your list to find”) drops to its own line, indented, with a stray left rule. The ruled line of the title page looks broken.
- **Evidence:** `home_1280_light.jpg`, `shelf-adult_1280_light.jpg`, `old-childrens_1280_light.jpg`. Measured: 9 page types with figures on 2 rows at 1280, none at 1600.
- **Fix:** let the figures use the width beside the plate (for example `max-width:calc(100% - 31% - 40px)`, or no cap with `flex-wrap:nowrap` and smaller padding below about 1400px). Also drop the left rule on the first item of each wrapped row. Fix the rule, not each page.

### 2. Muted text is now below the readable minimum in light mode
- **Where:** every page in light mode: book bylines under covers, the kicker (“Shelf”, “Home library”), figure labels, “See them all at once”, Details labels, To Buy authors.
- **What:** L1 changed `--muted` to #7A6A52 on paper #F3EAD5, which is **4.37:1**, below 4.5:1 for small text. Before L1 it was #75664F on #F7F1E4, about 4.95:1. Most of this text is now also small italic EB Garamond (15px), which reads lighter still.
- **Evidence:** token contrast measured in the page (light). Dark mode is fine (muted 7.4:1).
- **Fix:** darken `--muted` a little (about #6E5F48 gives roughly 5:1 on the new paper). Also check `--accent` #9A7022, which is 3.7:1: fine for the big italic headings, too weak for the 14px “Book 2 of …” series link (`.in-series`). Use `--gilt-ink` (5.6:1) for small accent text.

### 3. Drop capital breaks a blurb that starts with a number
- **Where:** book page, blurb (`.desc:first-child::first-letter`). For example *A Little Luck* (`#b-2ousnrntqt`).
- **What:** “20 years after…” shows a huge “2”, then “0 years after” on the next line.
- **Evidence:** `book-desc_1280_light_full.jpg`, `dropcap-20_1280_light.png`. One book now; 16 more blurbs start with a quotation mark, which becomes a large “ followed by a drop letter (`dropcap-quote_1280_light.png`). That is a common printing style, so it’s a matter of taste.
- **Fix (general rule):** add the drop capital only when the blurb starts with a letter, for example with a `drop` class set in `blurb()` when `/^\p{L}/u` matches.

### 4. Stats still has the old dark walnut panels
- **Where:** Stats, the two figure panels (“648 books on the shelves…”, “229 books read…”), `.ledger`.
- **What:** rounded 22px walnut blocks with Manrope labels, left over from the dark-banner look. Every other page now uses the ruled title-page figures. In dark mode they are brown slabs on the dark page.
- **Evidence:** `stats_1600_light.jpg`, `stats_1280_dark_full.jpg`.
- **Fix:** style `.ledger` like `.figures` (paper, double rule above, single rule below, Instrument Serif numbers, italic EB Garamond labels) or like the `.panel` mount.

### 5. Children’s shelf card: gilt name hard to read on mustard cloth
- **Where:** Home, “The shelves”, the Children’s card (and, less so, Young Adult).
- **What:** L1 tints each card’s cloth with the shelf colour and stamps the name in pale gilt. Children’s is #CF9A2B, so the gilt name is about 3.5:1 and the book count about 2.9:1 (pixel measurement). The other cards are 5–6.8:1.
- **Evidence:** `home_1600_light_full.jpg`; crops in `libreview/crops/light-card5-*.png`.
- **Fix:** darken the cloth mix for light shelf colours (for example `color-mix(var(--c) 55%, #2A170C)`), or add a slightly stronger text shadow under the gilt. Same rule for every card.

### 6. Dark mode: the Old books shelves stay cream, and the “to find” spines can’t be read
- **Where:** Old books · Children’s / Fiction / Non-Fiction in dark mode.
- **What:** `.bookshelf` has hard-coded cream boards (#EFE5D1). The gap spines take `var(--muted)`, which is pale in dark mode, so their titles go pale-on-cream and nearly vanish. Bright cream bands also fill a dark page. This was there before L1, but it stands out more on the darker L1 page.
- **Evidence:** `old-childrens_1600_dark_full.jpg`.
- **Fix:** give the board a dark-mode version (dark paper with the walnut board kept), or keep the cream board and set the gap-spine text to a fixed dark brown.

### 7. 2.6 MB of fonts, all four loaded on the first page
- **Where:** `site/fonts/EBGaramond-*.ttf` (602–688 KB each).
- **What:** Regular, Italic, Medium (500) and SemiBold (600–700) are all fetched on Home. A first visit to Home weighs about **16.7 MB**: 2.6 MB fonts and 13 MB of covers (71 pictures; some cover files are 500–860 KB but show at about 100px wide, including the 18 tiny plate covers). This hardly matters on her PC, but it will matter online or on a phone.
- **Fix:** convert to WOFF2 and subset to Latin (roughly 60–100 KB each). Consider dropping Medium (use 400 for the sidebar links) and SemiBold if they’re barely seen. Before going online, small thumbnail copies of covers for grids and the plate would cut most of the rest. The fonts came from her PC (SIL OFL), so converting a copy is allowed; keep the licence file.

## Polish

1. **Ornament sits on a flat patch.** The ❦ under every section heading has a plain `var(--paper)` background, but the page has paper grain, so a small smooth rectangle shows round it (clearer in dark). Evidence: `ornament-crop_1280_dark.png`, `stats_1600_light.jpg`. Fix: a small radial fade instead of a solid box, or draw the rule as two halves with a gap.
2. **Left-aligned headings on book pages keep a centred ornament.** “Your review”, “More by …”, “Other copies you own” are left-aligned (`.book-body .section-head`), but the ❦ still sits mid-column, under nothing. Evidence: `book-series-review_1600_dark_full.jpg`, `book-old_1280_light_full.jpg`. Fix: `left:0; transform:none` for `.book-body .section-head::after`, or centre those headings too.
3. **Older controls not yet in the L1 look:** filter chips (dark filled pill), sort and view buttons, To Buy / To Find cards (rounded 14px, Manrope), Add a book form fields, the Authors list and letter buttons, the “What should I read next?” pop-up, list view, the New covers switch. They work and are readable, but they look like the old app beside the bound-book pages. Evidence: `to-buy_1280_light.jpg`, `add_1280_light.jpg`, `authors_1280_dark.jpg`, `pick-popup_1280_dark.jpg`.
4. **Sidebar: more links off the bottom.** At 1280×800, Reading, History, To Buy, Authors, Stats and Add a book (6 links) need the sidebar scrolled, with no hint that it scrolls. Before L1 it was 5 (`before-L1_shelf-adult_1280.jpg`); at 1600×930, 3 are hidden. The larger EB Garamond links added about 40px. Fix: a little less vertical padding on `.nav a` / group gaps, or a soft fade at the foot of the nav.
5. **Justified blurbs leave wide gaps.** `text-align:justify; hyphens:auto`, but Edge here did not hyphenate, so narrow lines spread (“both anticipated encounters and”). Evidence: `book-desc_1280_light_full.jpg`. Fix: `text-align:left` below about 60 characters a line, or accept it.
6. **Details labels in small capitals make “ISBN-13” look odd.** Old-style digits in small capitals read like “ISBN-ɪ3”. Evidence: `facts-crop_1280_light.png`. Fix: `font-variant-numeric:lining-nums` on `.facts dt`.
7. **Search box clear “×” is the browser’s default blue** on the brown cloth. Evidence: `search-pratchett_1280_light.jpg`. Fix: style `::-webkit-search-cancel-button` in gilt (this predates L1).
8. **Stats “Your highest-rated authors”:** “4.75 ★ · 4 books” wraps to two lines in its 80px column at 1280. Evidence: `stats-authors_1280_light.jpg`. Fix: widen the third column to about 120px for that chart (predates L1).
9. **Stats title page has an empty band.** `.hero.shelved` gets its height from the plate, so Stats (no figures) has about 150px of blank paper under “How the library adds up.”. Evidence: `stats_1600_light.jpg`.
10. **Old Book Collection shows “0 pages”** as a figure (no page counts for old books). Evidence: `shelf-old_1600_light.jpg`. Fix: leave out a figure that is 0 (general rule).
11. **Ornaments inside headings may be read aloud.** The ❦ in `.panel h2::after` is part of the heading for screen readers (“Your reading floral heart”). Fix: `content:"❦" / ""` (alt text for generated content), or move it to the panel.
12. **Heading order (predates L1):** shelf, author and To Find pages jump from the h1 to book titles in h3; search results and New covers have no h1.
13. **“Got It” on the buttons, “Got it” in the sentence above.** Every-word capitals turn the button into “Got It”, while the intro on To Buy / To Find says “press Got it”. Small mismatch.

## Questions for her

1. **Green Display card.** Her rule is no green. The Display shelf colour (#3F6B4A) was only a dot before. L1 now colours the whole Display cloth card on Home dark green. It’s already an open question in her TODO (item on “Green colours?”). L1 makes it much bigger, so it may be worth asking now (with a picture).
2. **Drop capital with an opening quote mark:** keep the large “ + letter (16 blurbs), or start those blurbs plain? (my suggestion, not decided: start them plain, like the number case).
3. **Add a book without her PC server:** the form still shows. Look it up says “Couldn’t reach Open Library. Fill in the details yourself.”, which is misleading when the real problem is that her own server is off. The page also polls `/api/scanned` every 4 seconds (a 404 each time). This is fine on her PC (server always on). If the site goes online it needs a decision: hide Add a book and the Signed / Condition / Inscription pickers on book pages (they show whenever the page is served over http and can’t save online).
