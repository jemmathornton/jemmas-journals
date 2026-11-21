# Review, round 2: Jemma’s Pokédex (21 Nov 2026, evening)

Read-only review of `C:\Users\Jemma\Documents\Pokedex\site` at 71cd8bf (the binder look, review fixes, Gigantamax full rows, tabs as the filter, the family rules). Nothing in Pokedex was edited, built, staged or committed. `git status` was clean before and after, and her ticks file `data/collection/go.json` has the same SHA-256 before and after (dd7a49f4…).

**How it was checked.** `site/` was served from disk through Playwright `page.route` in Edge. `/api/collection` was answered from `go.json`, read only. Every other `/api/` call got a 503, and none was made. Light runs had the **device set to dark**, to prove the site still opens light. Dark runs had `jj-mode=dark` in storage. Sizes: 1600×930, 1280×800, 901, 899 and 390×844, each in light and dark, which made 470 page loads. Pages: Home, Every Pokémon, all ten regions, Event Pokémon, four set pages, Looking for (every tab), What’s on, Fast tick (Pokédex, Costumes, Backgrounds, Forms check), 16 Pokémon pages (including Charizard, Pikachu, Unown, Rotom, Vivillon, Mewtwo, Paldean Tauros, Toxtricity, Urshifu and #1012), an unknown address, and searches for “pika”, “25”, “farfetch’d” and “zzzz”. Then separate runs for the drawer, tabs as the filter, carrying the mode across, keyboard focus, the footer, and widths scanned from 360 to 1600. Scripts and data (`report-*.json`, `inter.json`, `probe.json`) are in the screenshot folder’s parent.

Screenshots: `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review2\pokedex\`. Empty art windows far down full-page captures are a capture artefact: the pictures load lazily and the capture never scrolls to them.

**Tests:** `tests/run_tests.py` was run with `-B` and `PYTHONDONTWRITEBYTECODE`: **88 tests OK (2 skipped as slow), 60 of 60 page tests, 310 s.** Nothing was written to the repo.

## What is now right

- **Family dark mode: all correct.** It opens light with the device set to dark. The footer button reads “Dark mode” with a moon, then “Light mode” with a sun, and `aria-pressed` follows. `jj-mode` is saved and survives a reload, and `jj-mode=dark` opens dark with no flash (it is set in `<head>`). `theme-color` swaps between #7A1E2A and #4E1018. The old `jemmas-pokedex-mode` is moved over once. With storage blocked, the page opens light, the button still works and there are no errors.
- **Family drawer: everything on the list works** at 899 and 390, light and dark. Below 900 there is a Menu bar; at 901 the sidebar shows. Menu has `aria-controls="side"` and `aria-expanded` that changes. Opening puts focus on “← Jemma’s Journals”, which sits at the top. Tab stays inside the drawer (30 presses). Escape closes it and puts focus back on Menu. Tapping the scrim closes it, as does choosing a link. The page behind is locked (`overflow:hidden`; wheeling on the scrim doesn’t move it). While closed the drawer is `inert`, so Tab goes from the top name straight to the tabs. Widening the window while it is open resets it. (One small gap: Polish 6.)
- **Family footer:** the order is right. Back to top and Dark mode are both 44px tall and level. The text is 12.5px in #6E5A58 (light) or #B8A29F (dark), both above 4.5:1. On phones the credits stack and the “·” is hidden. Back to top scrolls up and moves focus to the page. (But see Broken 1 and Should fix 2.)
- **Tabs as the filter work:** each of the 13 tabs filters the cards (Kanto: Lucky 10, Gigantamax 4, Dynamax 29 …), sets `aria-pressed`, keeps focus on the tab you clicked or pressed Enter on, and turns “Hide ones I have” on. Clicking the same tab again goes back to all. Clear resets. The chosen tab carries to other regions. The shiny picture shows only with the Shiny tab.
- **Clean:** no console errors, no failed requests, no “undefined” or “NaN”, no straight apostrophes, no US spellings, and every control has a name. **No card box label is cut** at any size, and each word is the same size on every card (Gigantamax full rows work).
- **Fixed since round 1:** facts table at 901–965 (item 1); banner text kept off the map (3: at 1280 Fast tick’s text clears the map, and on phones the map sits above the words); What’s on on a phone is now a list by week (4); card labels on phones (5); dark red text in dark mode (6: `--deep-2` is #E48A96 in dark); light muted text (7: #6E5A58); sidebar focus ring (8: gold); the Shiny Shadow box is framed (11); phone box buttons are now 24px (12).

---

## Broken

### 1. Every page scrolls sideways at 601–879 and 901–1113 wide (new, from the family footer)
- **Where:** the footer’s credits line, on every page.
- **What:** each credit is `white-space:nowrap` (`site.css` 1103), and in `index.html` the credit and dot spans touch with no space between them: `</span><span class="dot">·</span><span class="cr">`. So the line has nowhere to break. It is 857px wide and can’t wrap. Above 600px, until the stacked phone style takes over, the page becomes wider than the window. Measured page width: 857 at 601–850; **1113 at 901–1112** (857 plus the 256px sidebar). At 1000 the line is cut at “Icons by L…” and the whole page can be dragged sideways. That covers a small laptop window, a tablet, or her window snapped to half the screen. The tests didn’t catch it: they check 390, 899 and 1600, where it fits.
- **Evidence:** `footer-overflow_1000.jpg`, `probe-901-scrolled-right.jpg`. Every page at 901 in `report-901…json` has `sw 1113 > 901`. `probe.json` → `wide901…1100` names the overflowing `.cr` spans.
- **Fix:** put spaces around each dot in `index.html` (`</span> <span class="dot">·</span> <span class="cr">`), or make the `<p>` `display:flex;flex-wrap:wrap;justify-content:center`. Each credit then stays whole and the line wraps between credits. Add 1000 and 700 to the test widths.

## Should fix

### 2. The footer’s icon credit is not true
- **Where:** footer line 2: “Icons by Lucide and Phosphor”.
- **What:** the box icons also come from **Tabler** (Dynamax and G-Max), **MingCute** (Shadow) and **Solar** (Purified, CC BY 4.0, which requires credit). `site/js/LICENSE-lucide.txt` lists all five. The family rule is “only that site’s real credits … check each against what the site actually uses”.
- **Fix:** “Icons by Lucide, Phosphor, Tabler, MingCute and Solar” (or “Icons by Lucide and other open icon sets”, if she prefers it short; that wording would be my suggestion, not decided). On phones the stacked line is still one line per credit.

### 3. At 1280 (her checking width) the last tab is cut off, and the tab row hides most tabs below that
- **Where:** the 13 index tabs on Every Pokémon, the regions and search.
- **What:** each tab is at least 72px wide and the row scrolls sideways (`overflow-x:auto`). The row needs 996px. At 1280 it has 962px, so **“4★” is cut in half at the banner’s edge**, and Gigantamax is shrunk to **7.5px**. Below 1280 more is hidden: at 1100 three and a half tabs; at 901 only 7½ of 13 are visible (594 of 996px); on a phone 4½ of 13. Nothing but a half-cut tab says the row scrolls. Home and Event Pokémon wrap into rows instead, so the two kinds of tab rows behave differently. Sinnoh (12 tabs) just fits at 1280.
- **Evidence:** `crop-tabs-gen1_1280_light.png`, `gen-1_1280_light.jpg`, `tabrow-gen1_1100.jpg`, `tabrow-gen1_390.jpg`. Width scan in the review notes (`tabrow.js`).
- **Fix:** at 1280 a minimum of about 68px (or 4px less gap) is enough to fit all 13. Below about 1200, wrap into two rows (7 + 6), as Home already does, rather than scrolling. If she wants the single scrolling row (her “one small row” note), at least fade the right edge so it is clear the row scrolls. A layout change like this should be shown to her as a picture first.

### 4. Tab labels cut by a fraction of a pixel in three places
- **Where:** Home and an unknown address at 901 (“Gigantamax”, 57.2px of text in a 56.6px box); Event Pokémon at 901 (“Backgrounds”, 57.1 in 56.6); search at 1280 (“Gigantamax”, 48.4 in 47.5).
- **What:** the tab part of `fitLabels` still compares `scrollWidth > clientWidth`, which rounds, so the last letter loses a sliver. The card labels already use the exact `textOver()` measure (fixed in round 1).
- **Fix:** use `textOver(l)` in the `.hero .stat .slt` loop too.

## Polish

### 5. The family of evolutions still scrolls sideways (round 1, item 10)
On a phone, Charizard’s page shows Charmander, “25 Candy” and half of Charmeleon. Charizard, the page you are on, is out of sight (`.evo` is 696px wide in 356). The same happens at 901–960 with the sidebar (696 in 589). Evidence: `probe-p6_390_light.jpg`. Fix: on narrow widths, wrap the family or stack it with a down arrow.

### 6. Drawer: tapping the scrim leaves focus on the page, not on Menu
After Escape, focus returns to Menu. After a scrim tap it goes to `<body>`, because the tap has already moved focus out of the drawer before `setMenu` checks `wasIn`. The family rule says “closing returns focus to the button”. This matters little for touch, but it is a one-line fix: let the scrim handler always refocus (`setMenu(false)` with `wasIn` forced true, or focus `menuBtn` directly).

### 7. Cards in a row are still different heights (round 1, item 9)
`.grid{align-items:start}`. Every Pokémon at 1600 has 15 different heights among the first 60 cards, so bottom frames and numbers don’t line up. Fix: `align-items:stretch`, with the number pinned to the bottom (`margin-top:auto`).

### 8. Smaller things
- **Phone tap targets:** “× Clear”, the “Hide ones I have” switch and the name links on cards are under 24px tall at 390 (`report-…390` smallTaps). The box buttons are now 24px, which is fine.
- **Form picker:** names are still cut with “…” at every width (“Paldean Combat” 84px in 53; Toxtricity, Urshifu, Vivillon). This predates the restyle.
- **Fast tick → Backgrounds:** long square names are clipped at three lines (“Pokémon GO x LEGO (GO Fest Copenhagen and LEGO stores)”, “Goggles · Pokémon Horizons 2026”). That is reasonable in a grid, but the full name could go in a `title`.
- **What’s on (laptop):** bar names are shortened with “…” (accepted in round 1 for a calendar).
- **Stale notes, not on the site:** the comment above `fitLabels` (app.js 378) says “never below 10px … then without its icon, then on two lines”, but the code shrinks to 7px and never drops the icon. Pokedex `CLAUDE.md`, in the paragraph “The foot of every page”, still says the choice is kept in `jemmas-pokedex-mode`; the family-rules section below it is right.

## Questions for her

1. **Tabs on narrow windows:** one scrolling row (as now: on a phone you see about 4 of 13 and swipe for the rest) or two wrapping rows like Home? Show both as pictures. (This is Should fix 3.)
2. **“Hide ones I have” starts on, but switches off after you use a tab.** On a first visit Kanto opens with the switch on and shows 1 card (“Red and Blue · 1 shown”). After you click any tab and click it again, or press Clear, the switch is off and all 151 show. Which should the resting state be? (`prefs.workShow` defaults to "need", but `data-work`/Clear set it to "all".)
3. **Search with “Hide ones I have” on** (round 1, question 3, still open): “pika” shows “Search · 0 shown”, because she has every Pikachu (`search-pika_390_light.jpg`).
4. **White on the Lucky gold box is faint:** 2.5:1 (#D09B00), and on the Shiny grey 3.65:1, at 9–12px. White text on every box is her rule, so the only change possible is a slightly deeper gold or grey. Show it as a picture of the boxes, if she wants to look.
