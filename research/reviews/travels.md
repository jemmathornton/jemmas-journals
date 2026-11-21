# Review: Jemma’s Travels (work in progress)

Reviewed 21 Nov 2026, read-only, against `Documents\Travels\CLAUDE.md` and `TODO.md`. Nothing in Travels was changed.

**State reviewed:** the working copy of `site/` as it stood (with the other session’s uncommitted changes to `app.js`, `index.html`, `tools/`). The brief mentioned a trial switch with looks B, C, E, F, G, but that has moved on: CLAUDE.md says the look is **decided** (Old Atlas, pale gridded sidebar, banner, plain paper) and the switch is gone. So this review covers the chosen look.

**How:** `site/` served from disk through Playwright `page.route` in Edge, at 1600×930 and 390×844 in light mode, as `localhost` (her PC) and as a made-up online host (to check that Write is hidden). Spot checks at 320, 768, 1024 and 1280 wide, and opened as a `file://` page. There is no dark mode yet (it’s listed under Later in TODO), so the site stays light even when the device asks for dark.

**Screenshots:** `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review\travels\` (named `local|online`-`laptop|phone`-`page`.png, plus `zoom-*` crops and `sheet-*` contact sheets). Raw results: `..\report-travels.json` and `..\report-travels2.json`.

**What passed:** no console errors or page errors on any page. No failed requests, no broken images (there are no real photos yet), no outside requests. No straight apostrophes or American spellings in any text shown. Every `[placeholder]` field shows its dashed Placeholder badge (outside the Japan slip below). The Write link and page are absent on the online host and give “Not found”. `lang="en-GB"` and the robots meta (`noindex, noai, noimageai`) are present. The skip link works, keyboard order is sensible and focus is visible. The sidebar stays on screen when you scroll. There is no sideways scroll at 1600, 1280, 1024 or 768 wide, and none on phone except the Write page. On phone there is a menu button (top left, slides in from the left, × / tap outside / Esc all close it), like Sim World. The “← Jemma’s Journals” link is at the top of the sidebar and top bar on every page.

**Figures checked against `data/`:** all correct.
- 11 trips, 5 different years, 13 countries (GB not counted), 4 continents.
- Europe 7 of 44, Asia 2 of 48, North America 2 of 23, South America 2 of 12, Africa and Oceania 0. Total 195, 6.7%.
- Busiest year: 2024, 2025, 2026 (3 trips each).
- Most visited: France, Spain, United States (2 trips each). Tenerife counts as Spain and Strasbourg as France, which is right.
- September: 5 of 11 trips. Months: Mar 1, Apr 1, Jun 2, Sep 5, Oct 1, Nov 1, Dec 2.
- Longest gap: 2012 to 2023.
- Furthest from Birmingham: Argentina, 11,338 km to the country’s map point (shown as “about 11,300 km”).

---

## Broken

1. **Write page runs off the side on phones** (local only).
   - Where: `#/write` at 390 and 320 wide.
   - What: the Trip dropdown and the fields stick out past the white card and the screen.
   - Evidence: page width 429 at 390 (+39 px) and +108 px at 320. See `local-phone-write.png` and `local-320-write.png`. Likely cause: long option text such as “Brazil and Argentina · November – December 2025” sets the `<select>` width, and grid items default to `min-width:auto`.
   - Fix: `.write label{min-width:0}` and `.write select, .write input, .write textarea{width:100%;min-width:0}`. Add `#/write` to the sideways-scroll check in `tests/shoot.js`. It isn’t caught there now.

2. **“← Jemma’s Journals” doesn’t reach Journals on her PC.**
   - Where: the sidebar and top-bar link, `href="/"`.
   - What: on the preview server (port 8041) it reloads Travels’ own home page. Opened as a file, it goes to `file:///C:/` (a folder listing of her C drive).
   - Evidence: `report-travels2.json` → `file.home: "file:///C:/"`.
   - Fix: do what Sim World does. Keep `/` online, but when `location.protocol` is `file:` (or the host is local), point to `../../JemmasJournals/concepts/index.html` or the Journals preview address. Online, `/` only works once all the sites share one address, which is the decision already recorded in Journals.

## Should fix

3. **Unmarked made-up sentence in a post** (breaks her “no made-up text” rule).
   - Where: `data/posts/japan-2024/01.md`, second paragraph.
   - What: “A second paragraph shows how longer posts look.” has no `[placeholder]`, so it shows as if it were her words, with no badge.
   - Evidence: it is the only paragraph in any post without `[placeholder]` or a photo marker (scan of all 13 posts).
   - Fix: start it with `[placeholder]`. Make `tools/check_data.py` fail when a post with `placeholder: yes` has a paragraph without the prefix.

4. **Trip and country maps cut off the places she went.**
   - Where: `focusOn` and `mainBox` in `app.js`, which zoom to each country’s single biggest piece of land.
   - Evidence:
     - **Spain** (`local-laptop-country-ES.png`): the map is mainland Spain only, so the Canary Islands and the Tenerife pin are missing from the page of the country she went to Tenerife in.
     - **Tenerife trip** (`zoom-tenerife-map.png`, `zoom-tenerife-phone.png`): centred on mainland Spain, with Tenerife squeezed into the bottom-left corner.
     - **Japan** (`local-laptop-trip-japan.png`): framed on Honshu, so Hokkaido is cut off at the top and the southern islands are missing.
   - Fix: when a trip has named places, frame on those places (plus a margin) rather than the mainland. On country pages, include the pins of trips to that country in the frame (`focusOn([code], pins)`). For countries spread over several big islands (Japan), frame on all pieces above a size threshold, not just the largest.
   - Code smell, same function: `pageCountry` filters with `placePins(ts).filter(p => ts.some(t => t.countries.length === 1))`. The test doesn’t look at `p`, so a place on a different country of a multi-country trip could appear on the wrong country page.

5. **Location data in photos: there’s a rule but no tool yet, and the repo is public.**
   - Where: CLAUDE.md says to strip EXIF GPS from the copies. `site/photos/` is empty today.
   - Evidence: nothing in `tools/` reads or strips EXIF (grep for exif/gps/PIL found only the sheet makers). The GitHub repo is public, so the first real photo committed with GPS in it is public for good, even if it is removed later (it stays in git history).
   - Fix, before any real photo goes in:
     - (a) one import step, Python with Pillow (already used here), that resizes and re-saves each copy with no EXIF at all;
     - (b) a check in `build.py` or the tests that fails if any file under `site/photos/` has EXIF or GPS;
     - (c) keep originals out of the repo (e.g. `.gitignore` an `imports/photos/` folder).

     The plan in `for-jemma/writing-options.md` to use the photos’ own dates and places for matching should read them from the originals, never the copies.

6. **Stats count the template posts as her writing.**
   - Where: Stats, “Written so far: 13 posts · 17 days · 39 photos”.
   - What: all 13 posts are placeholders (10 of them are the Italy layout templates), so this figure isn’t true.
   - Fix: leave out posts marked `placeholder: yes` (it would read 0 for now), or show the tile as a marked placeholder. The same goes for “10 posts” on the Italy card and in the trip meta.

7. **The busiest month on Stats is hard to read** (and the dark cell’s label is too).
   - Where: Stats → Which months.
   - What: in the dark September cell, the “Sep” label is dark teal on dark teal and almost invisible.
   - Evidence: `local-laptop-stats.png` and `sheet-phone-1.png` (third column).
   - Fix: the round-by-round overrides in `site.css` (lines ~240–244, ~442–444 and later look-specific rules) fight each other. Make `.mcell.dark span` white in the final Old Atlas rules, or tidy this as part of the planned CSS clean-up.

8. **Low-contrast small text across the site** (WCAG AA needs 4.5:1 for text this size).
   - Where: sidebar counts and “Years”, and the “← Jemma’s Journals” link, all 3.4:1. Dates, “No posts yet”, notes, stat labels and the “of 44” figures are 3.4:1. Day pills, “Read post” and country codes are 4.1:1. Map country stamps are 4.3:1. The home kicker and tagline placeholder over the banner are 2.75:1.
   - Evidence: `report-travels2.json` → `contrast`.
   - Fix: darken the muted ink colour (roughly `--muted`/`--side-muted`) a step, until it reaches 4.5:1 on paper and on the pale sidebar. The look stays pale, only the small grey text gets darker. Show her before and after, since it changes the look slightly.

9. **Maps say “image” but contain links.**
   - Where: `map.js`, `<svg role="img">` with `<a>` country and pin links inside.
   - What: `role="img"` tells screen readers to treat the whole map as one picture, so the links inside aren’t announced, yet the keyboard still stops on each one. On phone, Tab goes straight from the menu button into a run of unnamed-sounding country links on the home map.
   - Fix: use `role="group"` with the same `aria-label` when the map has links. The country list under the map already gives the same links in text.

10. **Text written to Jemma shows on the public site.**
    - Comments note: “Comments switch on when the site goes online (your choice, 21 Nov).” That is a working note, and visitors will read it once the site is online. Fix: keep the box hidden until comments are chosen, or show the note only when `LOCAL`.
    - Map note: “Countries you’ve been to are coloured in.” A visitor isn’t the “you”. This is a question for her, see Q2.

11. **Labels on zoomed maps are tiny on phones.**
    - Where: trip maps at 390 wide.
    - What: pin names are about 8 px tall (“New York”, “Nashville”, “Tenerife”), and the map text scales down with the SVG.
    - Evidence: `report-travels2.json` → `phoneLabel`, and `zoom-tenerife-phone.png`.
    - Fix: give the labels a minimum on-screen size (scale the font by viewBox width ÷ rendered width), or hide labels under ~500 px and rely on the pin titles.

## Polish

12. **Home banner map**: Greenland and the Arctic islands touch and are clipped by the top edge at 1600 wide (`zoom-laptop-banner.png`). The Map page shows them whole with sea above. A few px of top margin would match her “drawn whole” ask.
13. **Home on phone is very long** (6,823 px): latest posts plus every trip as a full-width card. It will grow with every trip. Two columns of smaller trip cards on phones, or only the latest year on home with a “All trips” link, would keep it short. She may want to choose this, see Q3.
14. **Stats and Countries on phone**: one tile per row makes 10 tall stat tiles and 13 country tiles (`sheet-phone-1.png`). Two columns would halve the scrolling.
15. **Map page continent order** (Europe, South America, Asia, North America) follows trip order. The Countries tracker uses Europe, Asia, Africa, North America, South America, Oceania. Use one order everywhere.
16. **Country page map sits right on the trip cards** (about 4 px gap, `local-laptop-country-ES.png`). The post navigation sits 5 px above the Comments box on post pages. Add the usual section spacing.
17. **Six-photo mosaic on phone** ends with a lone half-width tile (`sheet-phone-1.png`, first column). Let the last tile span both columns when the count is odd.
18. **“Latest posts”** shows the first three posts (Day 1–3) of the newest trip, not the most recent ones. Name it differently, or take the last posts written.
19. **`#/country/GB`** (home) opens by URL as “0 trips”, with the UK coloured as visited. Not linked anywhere, so it’s low risk. Send it to Not found, or give it a note saying it’s home.
20. **Disabled comments textarea and “Post” button**: no label (placeholder only), and “Post” is 2.5:1. Fine while it’s off. Fix when comments are switched on.
21. **Real photos will have `alt=""`.** Captions (or a short description in the post header) could become the alt text when photos arrive.
22. **Every page loads `world.js` (1.2 MB)**, including phones. Already in TODO for going online.
23. **No tab icon or `favicon.ico`**: online, browsers will ask for `/favicon.ico` and get a 404. In TODO (her own design, like Journals).
24. **`site.css` is 68 KB** with about 300 `data-look` rules for looks she has dropped. Already in TODO. Doing this soon would also clear item 7.
25. **The Map credit (Natural Earth) appears only on the Map page.** The footer credits fonts and Lucide. Add “Map: Natural Earth” to the footer, as Journals credits its sources.
26. **Title shown twice on phone home**: “Jemma’s Travels” in the top bar and again, large, in the banner (`zoom-phone-home-top.png`). Acceptable, but the banner title could drop on phones.

## Questions for her

- **Q1. “Favourite month”**: the Stats tile says September is her *favourite* month. The data only says it’s the month she has travelled in most (5 of 11 trips). Keep “Favourite month”, or call it “Most travelled month” / “Busiest month”? (“Longest gap: 11 years, 2012 to 2023” is the same kind of question: there were 10 years without a trip in between.)
- **Q2. Who is “you”?** Some labels speak to her (“Countries you’ve been to…”, “Your photo” in empty frames). Once online, visitors read them. Keep them, or switch to neutral wording (“Countries visited are coloured in”)?
- **Q3. Home length**: all trips on the home page, or only the latest year (or latest few) with a link to the rest? Show both, as screenshots, before asking.
- **Q4. Distances**: “Furthest from home” is measured to the middle of the country (Argentina: 11,338 km). If she names cities (Buenos Aires would be about 11,100 km), should distances use the places she went?
- **Q5. Dark mode**: Journals has one (button in the footer). Travels lists it under Later. Is that still the plan before going online, so the family matches?
- **Q6. Write page later**: today it is a mock-up and is safe (it shows only on localhost or as a file, and saves nothing). When saving is built, it must be a small server bound to 127.0.0.1 on her PC, never anything inside the online site. That is a note for whoever builds it rather than a choice for her, unless she wants to post from her phone while away (option 3 in `writing-options.md`).
