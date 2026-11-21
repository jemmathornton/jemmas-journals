# Review: Jemma’s Pokédex after “Cards in a binder” and the Menu drawer (21 Nov 2026)

Read-only review of `C:\Users\Jemma\Documents\Pokedex\site` at commit 77e18f2. Nothing in Pokedex was edited, built, staged or committed; `git status` was clean before and after, and her ticks file (`data/collection/go.json`) has the same SHA-256 before and after (dd7a49f4…).

**How it was checked.** `site/` served from disk through Playwright `page.route` in Edge. `/api/collection` was answered from `go.json`, read only. Every other `/api/` call got a 503. None was made: no ticks were posted. Sizes: 1600×930 and 1280×800 (light and dark), 901, 900 (light and dark), 899 and 390×844 (light and dark). Dark mode was set with `colorScheme`. 34 page types at each size: Home, Every Pokémon, all ten regions, Event Pokémon, four set pages, Looking for (every tab), What’s on, Fast tick (Pokédex, Costumes, Backgrounds, Forms check) and an unknown address. Pokémon pages: Charizard (G-Max, Mega X/Y, costumes, backgrounds), Pikachu (100+ costumes), Unown, Rotom, Vivillon (forms not caught), Paldean Tauros (three forms), Hisuian Growlithe, Frillish (gender forms), Mewtwo (Armored not caught), Mew, #512 (not caught), #489 (not out), #1012, Spinda. Search: “pika”, “25”, “farfetch’d”, “zzzz”. Then the drawer (open, Tab, Escape, outside tap, link, same-page link, brand, top name, resizing while open), keyboard focus, index-tab labels at 18 widths from 1600 to 360, and banner text against the map.

Screenshots: `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review\pokedex\`, named `<page>_<width>_<light|dark>.jpg`. Extra shots are named `drawer-*`, `gen-1-all_*` / `gen-1-cards_*` (“Hide ones I have” off), `gen-1-shinytab_*`, `p-*-full_*`, `focus-*` and `crop-*`. Data: `report.json`, `drawer.json`, `extra.json`. Two things in the full-page pictures are how they are captured, not faults: the page background and sidebar stop at the window height, and pictures far down the page show empty art windows, because they load lazily and a full-page capture never scrolls to them.

**Tests:** `python -X utf8 tests/run_tests.py` was run with `-B` and `PYTHONDONTWRITEBYTECODE`, so nothing was written: **88 tests, OK (2 skipped as “slow”), 150 s; 53 of 53 page tests passed.** They work on a throwaway copy and her ticks file was unchanged.

**Clean:** across 420 page loads there were no console errors, no failed requests, no broken pictures, no “undefined” or “NaN”, no straight apostrophes in shown text and no US spellings. Every control has a name and every image has alt text. Sideways scrolling happens only at 901–960 wide (Should fix 1). Pictures show the normal colours. The shiny picture appears only on the Shiny tab (checked: `sprites/pm1.webp` normally, `pm83.s.webp` on the Shiny tab) or with the ✨ button, as her rule says. Box order follows the game. Search works, including the curly “farfetch’d”, and pressing Enter closes the drawer. No line crosses the sidebar items: the hinge shade is in the last 6px, and the links stop 12px short of it at both 256px and the drawer’s 300px.

**The drawer (≤900px) works:** Menu opens it with focus on the first item, and `aria-expanded` changes. Tab stays inside it (25 presses, never left the drawer). Escape closes it and puts focus back on Menu. Tapping outside closes it, as does choosing a link (including the page you’re already on) or the brand. While closed it is `inert`. Widening the window while it is open closes it and brings the sidebar back. Its list scrolls inside itself on a short screen. At 901 the normal sidebar is back and there is no top bar. Both are as intended.

**Known, confirmed:** on phones the index tab labels are cut short (“Pokémo”, “Dynama”, “Giganta”, “Shado”, “Purifie”); details and the wider range are in Should fix 2. The small line over the map on phone banners is also there, visible in `gen-1-all_390_dark.jpg` between the two rows of tabs.

---

## Broken

None. Nothing fails to load, no errors, and saving is untouched.

## Should fix

### 1. Pokémon pages scroll sideways between 901 and about 965 wide
- **Where:** every Pokémon page (14 of 14 checked) at window widths 901–960, the band just above the drawer breakpoint, where the sidebar is still showing.
- **What:** the facts table (Category / Type …) is wider than the page. Its right-hand column (“Fire · Flying”, “Available”) is cut off at the window edge and the page scrolls sideways. The picture card and the facts sit side by side in about 640px.
- **Evidence:** `p-6_901_light.jpg`. Page width measured on Unown: 964px at 901, 965 at 920–940, 966 at 960, fine from 980. `report.json`: HSCROLL on all 14 Pokémon pages at 901.
- **Fix:** start the one-column Pokémon page (`.mondetail{grid-template-columns:minmax(0,1fr)}`, and `.monpic` centred) at about 1000px instead of 900, or set the facts (`.dfacts`) to one column below about 1000px. A `minmax(0,1fr)` on the text column would also stop it pushing out.

### 2. Index tab labels shrink to 7px and are still cut short at most widths below 1280
- **Where:** the totals tabs hanging from every banner (Home, Every Pokémon, regions, search, Event Pokémon).
- **What:** the label is fitted by shrinking its font. Measured smallest label font: 10px at 1600, 9px at 1400, **7.75px at 1280** (her checking width), 7px below that. Even at 7px, words are cut:
  - 1100–1200: “Gigantamax”
  - 1000: Pokémon, Dynamax, Gigantamax, Shadow, Purified
  - **901: nine of thirteen** (“Poké”, “Fema”, “Shin”, “Luck”, “Dyna”, “Giga”, “Mega”, “Shad”, “Purif”)
  - 900: “Gigantama”
  - 701–800: Pokémon, Female, Dynamax, Gigantamax, Shadow, Purified
  - 390 and 360: the known phone cut
  The phone layout (two rows of seven) is fine at 500–700. Her rule is “always Gigantamax in full” and “never cut short”. On Event Pokémon, “Backgrounds” shrinks to 7px at 1280 though there are only three tabs and plenty of room (`crop-sets-tabs_1280.png`).
- **Evidence:** `home_901_light.jpg`, `home_900_light.jpg`, `scrolled-gen1_899_light.jpg`, `crop-tabs_1280.png`. Width scan in the review notes above.
- **Fix:** one rule, not per tab. Let the label wrap to two lines or drop the icon before shrinking, with a floor of about 10px. Use two rows (7 + 6) whenever a tab would be under about 70px wide, not only at ≤700px; in practice that means from about 1200px down, and between 901 and 1100 the sidebar leaves even less room. A tab row that doesn’t fill the width (Event Pokémon, a set) shouldn’t shrink at all: size those tabs to their content.

### 3. Banner text runs under the maps at 1280, 900 and on phones
- **Where:** the banner introductions on Fast tick, Looking for and What’s on (all widths below 1600), and the title and kicker on Home, regions and Pokémon pages on phones.
- **What:** the text column is 380px but the map starts before it ends. At 1280 the map covers the right part of the Fast tick and Looking for introductions (“that you haven’t got yet”, “the usual one”). On a phone the Fast tick, Looking for and What’s on introductions sit almost entirely over the map and can’t be read. Home’s “1,014 Pokémon out, plus their forms” and the gold “Pokédex” do the same, as do “#0006 · Flame Pokémon” and “Red and Blue · 151 shown”. At 1600 the text just clears the map.
- **Evidence:** `fast-dex_1280_light.jpg`, `want-s_1280_light.jpg`, `fast_900_light.jpg`, `fast-dex_390_light.jpg`, `want-l_390_light.jpg`, `coming_390_light.jpg`, `crop-home-top_390.png`, `crop-p6-top_390.png`, `crop-p201-top_390_dark.png`.
- **Fix:** keep the map to the right of the text. Start it at `max(text right edge, 70%)`, or below about 1400px narrow the text to the free space. On phones, either put the map behind a solid colour band under the text (map above, words below) or drop the map from the banner and leave the region colour. The map choice and crop are hers, so show the phone option as a picture first.

### 4. What’s on is not usable on a phone
- **Where:** What’s on at 390.
- **What:** the weekday names run into each other (“MONDAYTUESDAYWEDNESDAYTHURSDAY…”). “Leek Duck lists about six weeks ahead” is squeezed into a one-word-wide column beside the month. One-day events show only their time (“11:00”, “14:00”), with no name. Multi-day bars are cut to “Ba…”, “D”, “Twi…”, “Dy…”. Laptop sizes are fine: names are shortened with “…” at 1280 and 1600, which is reasonable for a calendar.
- **Evidence:** `coming_390_light.jpg`, `crop-coming-cal_390.png`.
- **Fix:** on phones use short weekday letters (M T W T F S S) and put the “six weeks ahead” note under the month line. Better still, show a list by week instead of the grid on phones (one row per event: kind colour, name, days), using the same data. If a layout choice is needed, show it to her as a picture first.

### 5. Card box labels cut short on phones (“Dynam…”, “Mega…”, “Purifi…”)
- **Where:** Pokémon cards at 390 (regions, Every Pokémon, search).
- **What:** her rule says a label too long for its box gets less padding and a smaller font, never cut short (`fitLabels`). At 390 “Dynamax”, “Mega Y” and “Purified” still end in “…”. Gigantamax is fitted correctly. At 1280 one “Gigantamax” on Every Pokémon is also flagged as overflowing.
- **Evidence:** `gen-1-cards_390_light.jpg` (Ivysaur, Charmander: “Dynam…”), `scrolled-gen1_390_light.jpg` (Mewtwo: “Mega…”, “Purifi…”).
- **Fix:** run `fitLabels` for the phone card width too: drop the icon first, then shrink. Or give phone cards one box per row for Dynamax/Gigantamax and Mega X/Y.

### 6. Dark mode: dark red text on the dark page
- **Where:** dark mode, anything coloured `--deep-2` (#7E2530): What’s on’s “until Tue 1 Dec”, “Show the 114 to get”, the italic “need” in “You need in November”, today’s date; “× Clear” on the filter line; links styled as `.linkbtn` (“Copy the list”).
- **What:** #7E2530 on the dark surface (#21171A) is **1.8:1** (2.0 on the paper). It is hard to read. `--deep-2` has no dark value. This was there before the restyle, but the binder look now treats dark mode as a finished mode.
- **Evidence:** `crop-coming-need_1600_dark.png`, `gen-1_1600_dark.jpg` (× Clear).
- **Fix:** give `--deep-2` a dark-mode value in both dark blocks, for example a light rose such as #E48A96 (about 6:1 on #21171A). Check the progress bars that use it still read as red.

### 7. Light mode: grey text slightly below the readable minimum after the paper got darker
- **Where:** light mode, small muted text on the page paper and on cards.
- **What:** the restyle deepened `--paper` from #FAF5EE to #ECE7E0. `--muted` #7A6563 on it is now **4.4:1** (needs 4.5 for small text): banner-tab sub-labels on the page, “A bonus, not counted.”, “Leek Duck lists…”, fact labels. On cards, `--card-mute` #8a7671 on the card stock is **4.1:1**, used at 10–11px for the set number (“#0006”), form names (“Hisuian”) and not-caught names. Dark mode is fine (6.9:1).
- **Evidence:** token contrast computed from site.css. `report.json` flags `span.no` and `small.fm` at 4.14.
- **Fix:** darken `--muted` to about #6E5A58 and `--card-mute` to about #776460 (both about 5:1). The faded “not caught” look comes from the grey picture and frame, so the text can afford to be darker.

### 8. Keyboard focus is invisible in the sidebar (light mode)
- **Where:** sidebar and drawer links, and the search box’s neighbours, in light mode.
- **What:** `:focus-visible` uses `--focus` = `--deep-2` (#7E2530), and the sidebar is now the red cover (#7A1E2A), so the ring is about 1.1:1, invisible. Dark mode uses the gold accent and is fine. The Menu button and the “← Jemma’s Journals” link already use the gold. Before the restyle the sidebar was near-black, so this is new.
- **Evidence:** `focus-nav_1600_light.jpg` (Kanto focused: only the “current page” bar shows).
- **Fix:** `.side :focus-visible{outline-color:var(--accent)}`.

## Polish

### 9. Cards in a row are different heights
- **Where:** every card grid (regions, Every Pokémon, set pages), at all widths.
- **What:** each card is as tall as its boxes, so a row is ragged. Measured in Kanto: 13 different heights, 327–422px. Venusaur and Blastoise stick out below their neighbours, so the bottom frames and set numbers don’t line up. In a binder of cards this shows more than it did with the old flat cards.
- **Evidence:** `gen-1-cards_1600_dark.jpg`, `focus-card_1600_light.jpg`.
- **Fix:** stretch the cards to the row (`align-items:stretch` on `.grid`), with the boxes at the top and the number pinned to the bottom (`margin-top:auto` on the last row).

### 10. Evolution family scrolls sideways on phones, hiding the last stage
- **Where:** Pokémon pages at 390 (`.evo{overflow-x:auto}`).
- **What:** Charizard’s family shows Charmander, “→ 25 Candy” and half of “Charme…”. Charizard itself, the page you’re on, is off to the right, with nothing to say you can scroll.
- **Evidence:** `crop-p6-evo_390.png`.
- **Fix:** on phones, stack the family vertically (arrow pointing down), or wrap it.

### 11. Some parts didn’t get the binder look
- The Shiny Shadow box (Pokémon page) and the What’s on “You need” cards are still the old flat white boxes beside the framed cards (`p-6_1600_light.jpg`). The set-page banner is the red cover fading hard into flat cream (dark: flat black) behind the Pokémon (`set-cos-halloween-2026-part-i_1600_light.jpg` / `_dark`), unlike the map banners.
- **Fix:** frame the Shiny Shadow box like a card in the region colour. Show her the set banner (cover colour across the width, or the background card behind) as a picture before changing it.

### 12. Smaller things
- **Phone tap targets:** the box buttons on cards are about 22px tall at 390 (under the 24px minimum; `report.json` TAPS on every region page). The ✨ flip button is 22px.
- **Drawer:** the page behind isn’t locked while the drawer is open (touch-scrolling the shade scrolls the page). After choosing a link, focus goes to the page body. That is fine, but moving it to the page heading would help screen readers.
- **Hover:** cards no longer change on hover (`.card:hover{border-color:var(--frame)}` is the same as the resting state). Only the cursor changes.
- **Form picker:** names are shortened with “…” (“Archipe…”, “Paldean Co…”) at all widths. That predates the restyle and is mentioned only for completeness.

## Questions for her

1. **Shiny foil on a card that isn’t marked as got.** Mewtwo (Forms 1/2, one form shiny) shows the shiny foil window on a grey “not caught” card. Is the foil meant to be “any form shiny” or “every form shiny”, like the grey/got rule? (`scrolled-gen1_899_light.jpg`)
2. **Background cards when not caught:** the Pokémon is greyed but the location art stays in full colour (Charizard’s backgrounds, `p-6_1600_light.jpg`). Is that wanted, so she can see which background it is?
3. **Search with “Hide ones I have” on:** searching “pika” shows “Nothing here” because she has every Pikachu and the switch is on by default, which can look like search is broken (`search-pika_390_light.jpg`). Should search ignore the switch, or say “All got: switch off Hide ones I have to see them”? (That wording would be my suggestion, not decided.)
