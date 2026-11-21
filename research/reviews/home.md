# Review: Jemma’s Journals home page (21 Nov 2026)

Read-only review of `concepts/index.html`, `concepts/404.html`, `concepts/robots.txt`, the tab icons and the share picture, judged against CLAUDE.md. Nothing was changed.

How: Edge via Sim World’s Playwright, page served wrapped in a doctype skeleton (as `tests/check_page.js` does), at 1600×930, 1280×800 and 390×844, light and dark (dark via the footer button), plus `#more1`…`#more3`, reduced motion and keyboard. Screenshots and raw measurements are in
`C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review\home\` (called `shots\` below; `measure.json` holds the numbers). The review script is `rev.js` in the folder above it.

`tests/check_page.js`: **90 checks passed, 0 failed.**

Overall: the page is in good shape. No sideways scroll at any size, no console errors at the real page’s state, every picture loads, it opens light although the device asks for dark, dark is remembered, the icon flips, reduced motion is respected, all text passes contrast in both modes. The findings below are mostly small.

---

## Broken

### 1. `#more3` throws an error and leaves the page dead
- **Where:** `concepts/index.html`, end of `render()`: `if(more===3) mb.textContent='Showing 6 places · back to 3';`
- **What:** `mb` was the trial-switch button, which was removed. With `#more3` the script stops at this line, so the click handler is never attached: the Dark mode button, Back to top and the Open links do nothing. (The line also wrongly says “6 places”: with Travels it is 7.)
- **Evidence:** console `ReferenceError: mb is not defined` at 1600, 1280 and 390; after clicking Dark mode the page stays `light` (`measure.json` → `more3-*`, follow-up run). `check_page.js` only tries `#more1` and `#more2`, so it misses this. CLAUDE.md documents `#more1…#more3`.
- **Real visitors:** not affected (only the checking stand-ins).
- **Fix:** delete that line; add `#more3` (7 places → 3 + 3 + 1) to `check_page.js`.

---

## Should fix

### 2. With four places the cards don’t line up with the headings (desktop)
- **Where:** `.cards:has(>.card:nth-child(4):last-child){max-width:…}`.
- **What:** Introduction and Contents (and their gold rules) start at the left of the 1160px column, but the 2 × 2 block is narrowed to 760px and centred, so the first card starts 200px to the right of the “Contents” heading and the rule runs 200px past the last card. With 3, 5 or 6 places the cards fill the column and do line up, so 4 (the real state now) is the odd one out.
- **Evidence:** 1600: headings x = 220, cards x = 420–1180, rule to 1380. 1280: headings x = 60, cards x = 260–1020. `shots\page-1600-light.png` vs `shots\more1-1600-main.png`.
- **Fix (options for her, my suggestion not decided):** (a) 2 × 2 at the full column width (two 560px photos), or (b) keep 360px photos but left-align the 2 × 2 under the heading, or (c) narrow the headings’ column to match the cards when there are four. Show her as a trial switch per her rules.

### 3. Back to top leaves keyboard focus at the bottom
- **Where:** click handler `[data-top]` → `window.scrollTo(0,0)`; link is `href="#top"` but nothing has `id="top"`.
- **What:** the view scrolls up but focus stays on “Back to top”, so the next Tab jumps on from the footer (out of the page). Without the script, `#top` goes nowhere.
- **Evidence:** after Enter on Back to top: `scrollY 0`, active element still “Back to top” (`measure.json` → `totop-1600`, `totop-390`).
- **Fix:** give the header `id="top"` and `tabindex="-1"`, and focus it after scrolling (or just let the link jump to `#top`, which smooth-scrolls already).

### 4. Footer says “plain HTML and CSS”, but the page is built by JavaScript
- **Where:** About this site, line 1; `<div id="page"></div>` is filled by the script.
- **What:** with JavaScript off (or if the script fails, as in item 1) the page is completely blank: no title, no links. The footer line is therefore not quite true, and a landing page with four links doesn’t need to depend on a script.
- **Fix:** either write the four places straight into the HTML (keeping the script only for dark mode), or change the wording to something she approves (her words only, so ask; e.g. drop “and CSS” → mention JavaScript). Question for her on the wording.

---

## Polish

### 5. 150px of empty space under the footer
- **Where:** `.foot .wrap{padding-block:26px 150px}`. The 150px was room for the trial switch (bottom right), which is gone.
- **Evidence:** blank band under Back to top / Dark mode in `shots\page-1600-light.png` and `shots\page-390-light.png`.
- **Fix:** about 48px, plus `env(safe-area-inset-bottom)` on phones.

### 6. Small tap targets in the footer on a phone
- **Where:** Back to top and Dark mode.
- **What:** 94 × 22 and 91 × 22 px at 390 wide. They pass WCAG’s 24px minimum only through the spacing exception (26px gap, nothing above or below) and are well under the 44px Apple/Google advise. Open links are 30px tall, photos are large: fine.
- **Fix:** `padding:11px 4px` (or `min-height:44px`) on both, keeping the look.

### 7. Placeholder lines for Pokédex and Travels aren’t marked the same way as the Introduction
- **What:** the Introduction placeholder has the dashed “PLACEHOLDER” tag; the two card placeholders (“A line or two about Pokédex, in your own words.”) are only grey italic. Her rule: missing text is a *marked* placeholder.
- **Fix:** add the same tag in `aboutPlace()` for null lines. (Pokédex and Travels have no home-page line of their own to quote; I checked their sites for a description and found none that fits.)

### 8. Travels map not credited
- **Where:** About this site credits.
- **What:** the Travels map is drawn from Natural Earth shapes (public domain, per Travels’ CLAUDE.md). Public domain needs no credit, but the other map sources are credited, so it reads as missing.
- **Fix:** ask her whether to add “Country shapes from Natural Earth” (wording hers).

### 9. Dark mode: theme colour stays light gold
- **Where:** `<meta name="theme-color" content="#8E6520">` is never changed; the dark cover is #6A4A17.
- **What:** on Android Chrome the browser bar stays the light gold above the darker cover.
- **Fix:** set it in `applyMode()` like the icon swap.

### 10. Leftovers in the code (no visible effect)
- `--sw-*` colour variables, the `.toast` styled with them, `ICON.plus` and `ICON.image` (unused), `localStorage.removeItem('jj-foot')`, the comment “title on scroll: show the slim bar…” above `render()`, `.intro` 180px photo column (overridden), `.v2` class and comments that still say “navy cloth”, “beside As now (switch, bottom right)”, “Ideas to try (switch)”, “round 9”. Harmless, but they mislead the next person reading the file.
- **Fix:** tidy in one commit and confirm pixel-identical with screenshots, as was done on 20 Nov.

### 11. Unused pictures in `concepts/img/` (about 13 MB folder)
- Top-level `cover-*.jpg`, `lot-*.jpg`, `map-*.jpg`, `region-*.jpg`, `shot-*.jpg`, `bg-go-fest-*.jpg`, `mon/`, `icons/` and every `maps/*.jpg` original are not used by `index.html` or `404.html`. They are candidates for her picture choices, so keep them, but leave them out when the site goes online (they would be published with it; it is a public repo).

### 12. 404 page is an older version of the cover
- **Where:** `concepts/404.html`.
- **What:** works and looks tidy (`shots\404-1600.png`, `shots\404-390.png`), no sideways scroll, noindex set. But the cover has no gold corner brackets or stitching, its gradient differs a little from the home cover, and it has no footer. Paths start with `/`, so it only works where the site sits at the root of its address (fine for her own domain; breaks if published under `github.io/jemmas-journals/`).
- **Fix:** copy the home cover styles (brackets, stitching) across.

### 13. Small tab-icon note
- `favicon.ico` is a valid 16/32/48 icon (decodes fine). In dark mode its `<link>` swaps to a single 32px PNG while keeping `sizes="16x16 32x32 48x48"`; harmless, could be `sizes="32x32"` for the dark one.
- `apple-touch-icon.png` (and 192/512) have transparent rounded corners. iOS fills transparent corners with black before applying its own rounding, so the home-screen icon may get dark corner slivers. A full-bleed square cream apple-touch-icon avoids this. (`shots\share-and-icons.png`.)

---

## Question for her

### 14. The Pokédex and Travels pictures are small inside their photos
Both maps are much wider than the 4:3 photo, so they sit as a strip with large empty mat above and below (map shown 336 × 147 in a 336 × 246 window). In dark mode that empty mat is near-black, which reads as letterboxing. This is the open “whole vs fill” choice in CLAUDE.md; worth showing her both again now Travels has the same issue. (`shots\page-1600-light.png`, `shots\page-1600-dark.png`.)

### 15. 404 wording
“Page not found” is a label, but “There’s nothing at this address.” is a sentence not taken from her or an app. Keep, or her own words?

### 16. Toast when an Open link is clicked
Until the links are real, clicking shows “This would open your Sim World” (says “your”, the page says “My”). Fine as a placeholder; just note it must go when the real addresses are in. Links are `href="#"`, so ctrl/middle-click opens this page again.

---

## Checked and fine
- **Layout:** no sideways scroll (0px) at 1600/1280/390, light and dark; Open links level across each row; 5 = 3 + 2 centred, 6 = 3 + 3, 7 = 3 + 3 + 1 centred; phone is one column, credits stack one per line.
- **Dark mode:** opens light with the device in dark; button switches, label changes to “Light mode”, focus returns to it, choice remembered after reload; label and page share #29221B, mats #0D0A07, corners cream, as decided.
- **Contrast:** all body text ≥ 4.5:1 in both modes (lowest: gold links 4.55 on cream; grey text 5.01). “Journals” in gold on the label is 4.18, fine for text that large (3:1 needed).
- **Keyboard:** skip link appears on first Tab (`shots\focus-skip-390.png`) and goes to Contents; tab order Skip → photo → Open, per card → Back to top → Dark mode; gold focus ring clear on photos and links (`shots\focus-photo-1600.png`).
- **Headings:** h1 Jemma’s Journals → h2 Introduction, Contents → h3 per place. Photos have names (“Open My Sim World” etc.); the cover wall has role img with a description.
- **Reduced motion:** no animations, cards fully visible, smooth scrolling off.
- **Text rules:** British English throughout (“neighbourhoods”); all apostrophes curly in shown text; Sim World and Library lines match their apps word for word (`SimTracker/site/js/app.js`, `HomeLibrary/site/js/app.js`).
- **Robots:** `noindex, noai, noimageai` on both pages; `robots.txt` asks the main AI crawlers to stay out and correctly leaves search engines unblocked so they can see noindex.
- **Share picture:** 1200 × 630, 86 KB, the gold banner. Not yet linked by any `og:image` tag (that’s in `research/drafts/`, for going online).

## CLAUDE.md vs the page
Mostly current (Travels, 2 × 2 and the icon are all recorded). Small gaps:
- “Places … named My Sim World, My Library, My Pokédex” and “Sim World and Pokédex: a full map” don’t mention My Travels.
- “A way back home in each app … all three apps”: Travels has the link too (recorded in Travels’ own CLAUDE.md only).
- “add `#more1`…`#more3`”: `#more3` is broken (item 1).
- Not checked: whether the private artifact (https://claude.ai/artifact/Ad37As365K3HDcR8iHw7HE) has been republished since My Travels was added.
