# Review, round 2: Jemma’s Travels (21 Nov evening)

Read-only: nothing in `Documents\Travels` was changed (git status clean before and after). Reviewed at commit **cececc4** (family rules), the latest; no uncommitted work.

**How:** `site/` served from disk through Playwright `page.route` in Edge, as `localhost` (her PC) and as a made-up online host. Every page (home, trips, trips by country, a year, three trips, three posts, map, countries, three countries, a continent, stats, timeline, search, Write, Not found, odd addresses) at 1600×930, 1280×800, 901, 899 and 390×844, light and dark, with the device set to the opposite scheme. Extra checks at 320, 905–1100, and as a `file://` page. Her test suite was run too (it works on throwaway copies): result at the end.

**Screenshots:** `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review2\travels\` (`mode-width-page.png`, `drawer-*`, `zoom-*`). Raw results: `..\report-travels-r2.json`, `..\report-travels-r2b.json`.

## What passed

- **Family rule 1, dark mode:** opens light with the device set to dark; footer button reads “Dark mode” (moon) / “Light mode” (sun), `aria-pressed` follows; saves `jj-mode`; theme-color #ECF1EA ↔ #15212C; reload and other pages keep it; old `jt-mode` moved over once and removed; with storage blocked the page still works and opens light. No `prefers-color-scheme` rules.
- **Family rule 2, footer:** on every page, centred: name in Instrument Serif (not italic), the shared “No cookies…” line, four credits, each starting with a capital (they match what the site uses: photos, Natural Earth, the two fonts, Lucide). Back to top and Dark mode both 44px tall and level (0px apart). 12.5px text. On phones the credits stack one per line. Back to top scrolls to 0 and focuses `#view`.
- **Family rule 3, menu:** at 899 the Menu bar appears (menu icon + “Menu” on the left, “Jemma’s *Travels*” after it, a link home); at 901 the sidebar. `aria-expanded` and `aria-controls="side"`. Opening focuses “← Jemma’s Journals”, the first link in the drawer. It closes on Escape (focus back to Menu), the scrim (focus back to Menu), a link, an opener item (Trips) and a search. The page behind is locked (`overflow:hidden`; wheel scroll stays at 0). The closed drawer is `inert` and `visibility:hidden`, so Tab never reaches it. Crossing 900px with it open resets it.
- **Dark maps:** the night Old Atlas works on every map (dark sea #0E2130, slate land, visited countries green, pale blue pins, a cream home pin, a pale route). Labels keep their sea-coloured halo. See `zoom-map-*-dark.png`.
- **Errors:** no console or page errors and no failed requests on any real page, in either mode, at any width. The only 404 is `api/ping` on the Write page with no server, which is expected and handled with the “start the travels preview” message.
- **Images:** no broken images. There are no real photos yet, and the placeholder frames say “Photo to come”.
- **Placeholders:** every `[placeholder]` field shows its dashed badge. There is no raw marker text outside the Write page’s help.
- **Text rules:** no straight apostrophes and no American spellings in any text shown. `lang="en-GB"`, and the robots meta (`noindex, noai, noimageai`) is there.
- **Privacy:** Write is “Not found” on an online host, with no link to it. The server listens on 127.0.0.1 only and needs `X-Travels: 1`. **Photo location data:** I re-ran `save_photo`’s steps (Pillow 12.3) on a JPEG with GPS in both its EXIF and its XMP. The saved copy has neither. `site/photos/` is empty.
- **Figures, checked against `data/` with my own sum:** 11 trips, 5 years, 13 countries (GB not counted), 4 of 7 continents. Europe 7/44, Asia 2/48, North America 2/23, South America 2/12, 6.7%. Furthest is Argentina, about 11,300 km. Distance travelled is 100,390 km, which is right as “100,000 km, about 2.5 times round the world”. Tenerife trip about 5,900 km, Japan about 18,800 km. Busiest year 2024, 2025 and 2026 (3 each). September 5 of 11. Longest gap 2012 to 2023. Sidebar counts match.
- **No sideways scroll** at 1600, 1280, 899, 390 or 320 (Write included). There is one exception at 901–919, see item 1.

### Items from the first review
- **Fixed:** 1 (Write too wide on phones), 3 (unmarked Japan sentence), 4 for Spain and Tenerife (pins now framed) plus the wrong-country pin filter, 5 (the server strips GPS), 7 (September cell), most of 8, 9 (maps with links are `role="group"`), 10 (comments and map notes), 15, 18, 19, 20, 23 (tab icon), 24 (CSS rewritten), 25 (Natural Earth credited in the footer).
- **Still open:** 2 (Journals link), 4 for Japan, 6 (template posts counted), 11 (phone map labels), 12, 13 (home length, now longer), 21, 22. Details below.

---

## Broken

1. **Map page: the continent bars vanish, and the page scrolls sideways, from 901 to about 1000px wide.**
   - Where: `#/map` (and `#/countries`), the “Countries visited” tracker, laptop layout with the sidebar.
   - What: the tracker stays two columns (`300px 1fr`) until the 820px phone rule, but with the sidebar beside it there is no room.
     - Each bar’s track measures **0px wide at 901 and 960** and 4px at 1000. Only the names and figures show, with no bars.
     - The “7 of 44” figures stick out past the card and the screen: page width 908 at 901, so 7px of sideways scroll (3px at 905, none from 920).
   - Evidence: `light-901-map-viewport.png` (“7 of 4…” cut off at the right). Measured: track 0/0/4/104px at 901/960/1000/1100.
   - Why the tests miss it: `tests/e2e/run.js` WIDTHS are 1600, 1280, 1024 and 390, and nothing between 900 and 1024.
   - Fix: stack the tracker when the content column is narrow, not at 820. For example, `@media (max-width: 1100px) { .tracker { grid-template-columns: 1fr; justify-items: center } .cont-bars { width: 100% } }`, or a container query on `.tracker`. The other phone rules still at 820px are worth checking the same way, because the family breakpoint is now 900. Add 901 (and 960) to the tests’ widths.

2. **`#/trip/constructor` crashes and `#/country/constructor` draws a broken map.**
   - Where: `tripById` and `D.countries` are plain objects, so names like `constructor`, `toString` and `__proto__` are “found”.
   - What:
     - `#/trip/constructor` throws “Cannot read properties of undefined (reading 'slice')”. The old page stays on screen with the new address.
     - `#/country/constructor` shows a page titled “Object” with an SVG full of NaN errors.
   - Evidence: page errors at every width in `report-travels-r2.json`.
   - Risk: low. It is only reached by typing an address, and it is not a security hole (no injection).
   - Fix: look up with `Object.hasOwn(tripById, id)` / `Object.hasOwn(D.countries, code)`, or build them with `Object.create(null)` / `Map`. Add `constructor` to the “unknown addresses say Not found” test.

## Should fix

3. **With the drawer open, Tab and Shift+Tab land on things hidden under it.**
   - Where: drawer at 899 and 390.
   - What: only `#main` is made inert. Shift+Tab from the first drawer link goes to “Jemma’s Travels” in the top bar, which the drawer covers (checked with `elementFromPoint`: not visible). Tab past “Write” goes to the page, then “Skip to the page” (which does nothing, since `#view` is inert), then the hidden Menu button and name. So keyboard users lose sight of focus for three stops.
   - Fix: while open, also make `#topbar` and the skip link inert, or wrap Tab within `#side`. The scrim, Escape and links still close it. A small × at the top of the drawer would also give a visible close control. The Menu button is under the drawer, so today the only visible way out is the 90px strip of scrim on a phone.

4. **Japan’s country page still cuts Japan off.**
   - Where: `#/country/JP` (`focusOn` frames on the biggest piece only, Honshu).
   - Evidence: `zoom-map-country_JP-dark.png`. Hokkaido is cut at the top edge, Kyushu at the bottom, and Okinawa is missing. Spain/Tenerife is fixed because pins are now included, but Japan has no named places.
   - Fix: in `mainBox`, take the union of all pieces above a share of the largest (say 5%), not only the largest. This is the same fix suggested in round 1.

5. **Some small text is still under 4.5:1** (her own test checks only one post page, and it skips see-through backgrounds).
   - Month cells on Stats:
     - light: “Jun”/“Dec” labels 2.8:1 and “Mar/Apr/Oct/Nov” 3.5:1;
     - dark: 2.7:1 and 3.8:1. (September is now fine: 5.5 light, 9.4 dark.)
     - Evidence: `zoom-months-light.png`, `zoom-months-dark.png`.
     - Fix: switch label colour by the cell’s strength (white or near-black text from about `--a > .45`), or keep the cells paler and the text `--ink`.
   - Postcard stamps on trip cards: blue #4A7FA8 on white, 11px, 4.29:1. Darken `--accent2` a touch, to about #3F739B.
   - Home banner kicker (“11 trips · 2012 to 2026”), tagline placeholder and its badge: `--muted` on the sea colour #D9E9EE, 4.31:1 (dark mode is 7:1). Use `--ink2` there.
   - Sidebar counts on the highlighted row (e.g. “11” beside Trips when open): 4.06:1 on the green tint. They are 4.7:1 on the plain sidebar.

6. **Stats still count the template posts as her writing** (round 1, item 6).
   - What: “Written so far: 13 posts · 17 days · 39 photos”. All 13 posts are placeholders (10 are the Italy layout templates). Search and Surprise me already leave placeholders out, so Stats is the odd one out.
   - Fix: count `!p.placeholder` posts (this would show 0 posts now), or mark the tile as a placeholder.

7. **Nothing stops a photo with location data getting into `site/photos/` by another route.**
   - What: the Write page’s server strips GPS (verified, EXIF and XMP). But if a photo is copied in by hand or by an agent, the build and data check don’t look, and the repo is public. Once a photo is pushed, its history keeps it for good.
   - Fix: in `tools/check_data.py`, refuse any file under `site/photos/` that has EXIF GPS, XMP or other EXIF (Pillow `getexif()` and `info.get("xmp")`). Add a unit test.

8. **“← Jemma’s Journals” still doesn’t reach Journals on her PC** (round 1, item 2; in TODO as accepted).
   - What: on the preview it reloads Travels. Opened as a file, it goes to `file:///C:/`, a listing of her C drive.
   - Fix: Sim World handles this already. When `location.protocol === "file:"`, point the link at `../../JemmasJournals/concepts/index.html`. That costs one line and avoids the C-drive listing.

## Polish

9. **Map labels on phones are 8px tall** (round 1, item 11). “Birmingham”, “New York”, “Nashville” on trip maps at 390 (`zoom-map-nyc-390.png`); 13px at 1600. Scale `.worldmap text` by viewBox width ÷ shown width, or hide labels under 500px.
10. **Footer credits leave a dangling “·” at medium widths.** At 901 the second line wraps as “…Fonts: Instrument Serif and Manrope ·” / “Icons by Lucide” (`light-901-stats.png`). The phone rule (one per line) starts at 600px. Either put each separator inside the following `.cr` (`white-space:nowrap`) so it wraps with it, or start the stacked layout higher.
11. **Sidebar search box has no focus ring of its own.** The input is `outline:none`, and the form shows only a soft 2px tint (#E1EFE8 on the pale sidebar, hard to see; `zoom-search-focus-light.png`). Use `.nav-search:focus-within { outline: 2px solid var(--accent) }` like everything else.
12. **Home is getting longer on phones:** 7,310px at 390, up from 6,823 in round 1. The “This time of year” section is new, and every trip is still listed in full again under “Trips by year”. TODO already has this as a question for her.
13. **Headings on home:** under “Trips by year” (h2) the years are h3 and the trip titles inside them are also h3. They should be h4 under a year. Elsewhere the order is fine.
14. **Sidebar openers are links with `aria-expanded`.** “Trips”, a year and a continent navigate *and* expand. Screen readers will hear “link, expanded”, which is unusual but works. Leave it unless a screen-reader user is expected.
15. **Banner map at the top edge:** Greenland and the Arctic islands still touch the top of the banner on laptop and phone (round 1, item 12).
16. **The local server doesn’t check the Host header.** In theory a DNS-rebinding page could post to it while it runs; `X-Travels` doesn’t stop a same-origin attacker. Refuse requests whose `Host` isn’t `localhost:8041` or `127.0.0.1:8041`.
17. **iPhone HEIC photos** chosen on the Write page will fail with “Not saved” (Pillow needs pillow-heif, already noted in research). The file picker accepts `image/*`, so it offers them. Either say “JPEG or PNG” beside the drop box or ask her about installing pillow-heif.
18. **No `/favicon.ico`.** The SVG and PNG icons are linked, but browsers still ask for `/favicon.ico` online. This is only for going online.
19. **The footer says “Made with plain HTML and CSS”.** The site is drawn entirely by JavaScript (blank without it), and the Write page needs a Python server. The family rule says to raise this with her rather than change the words, so it is in the questions below.

## Questions for her

- **Q1. Footer line.** Travels is built with JavaScript as well as HTML and CSS. Keep the shared wording “Made with plain HTML and CSS” on every site, or change it on all of them? (Journals and the apps may be in the same position.)
- **Q2. “Favourite month” and “Longest gap”** (from round 1, not yet answered): the data says September is the month she travelled most, not her favourite. Keep the wording, or use “Busiest month”?
- **Q3. Written so far:** leave out the template posts (shows 0 now), or keep counting them until her real posts arrive?
- **Q4. Home length:** keep every trip on the home page, or show the latest year with a link to Trips? Already in TODO.

## Her test suite

`python -X utf8 tests/run_tests.py`: **81 tests, all OK** (684 s). It ran on throwaway copies, and `git status` in Travels was clean afterwards. Gaps that let the items above through:
- the widths are 1600, 1280, 1024 and 390, with nothing between 900 and 1024 (item 1);
- the contrast test checks one post page and skips tinted backgrounds (item 5);
- the drawer test doesn’t check where Tab goes while the drawer is open (item 3);
- the Not found test doesn’t try names like `constructor` (item 2).
