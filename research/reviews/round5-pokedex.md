# Review, round 5: Jemma’s Pokédex (22 Nov 2026, afternoon)

Read-only. Pokédex at 447b320 (Try switch, Home maps, CSP, one-row tabs, Kanto sky, no date). Nothing in `pokedex` or the parent was edited, staged or committed by this review. `pokedex` git status was the same before and after (only `logs/backup.log`, already modified at the start). Her ticks file `data/collection/go.json` has the same SHA-256 before and after (c294d8f3…6b564). Every non-GET request was answered inside the browser and never reached a server (`POST /family/mode` from the Dark mode button included). The Try switch was set through localStorage before each load; no switch button, box or Tick all was pressed on a page that could save.

**Note:** another session committed and edited the parent’s shared code while this review ran (`a655695` at 13:41, then more uncommitted edits to `site/family/*`, `site/home.js`, `site/index.html`). The sweeps after 13:45 ran against that new `family.js`.

**How it was checked:** Edge through Playwright at `http://localhost:8050/pokedex/`. 39 page types × 9 widths (1600, 1584, 1450, 1280, 1100, 1000, 901, 899, 390) × light and dark = 702 page draws. Light was shown by rewriting `data-jj-server-mode` in the served page, because her stored mode is dark. Then: an in-page crawl of every page the app can draw (1,220 pages: every Pokémon page, every set, every Fast tick region × box, every Looking for and filter tab), with every internal link drawn and every picture fetched (5,444). Also axe at 1600 and 390 in both modes and with both box colours (CSP bypassed only to inject axe), page weight and render cost, keyboard and drawer checks, view-only at 8060, address-value injection probes, and the test suite.

Scripts and raw results: `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review5\pdscripts\`. Screenshots: `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review5\pokedex\` (Try switch pictures and 2 × 2 comparison sheets are in `try\`).

## Today’s changes: verified

- **One-row tabs over 900:** this holds on Every Pokémon and all ten regions, in both modes, with no label cut, no sideways slide, and nothing past the window edge.

  | Width | Layout | Label size |
  |---|---|---|
  | 1600 / 1584 | beside the icon | 10.5px |
  | 1450 | beside the icon | 10px |
  | 1280 | beside the icon | 8.5px |
  | 1100 | stacked | 9.25px |
  | 1000 | stacked | 8.5px |
  | 901 | stacked | 7.25px |
  | 899 | 7 + 6 rows | 10px |
  | 390 | 4 + 4 + 4 + 1 rows | 10px |

  The stacked tabs are readable but small (see Looks).
- **Kanto haze:** gone from the Kanto region banner at 1000 dark (top-right brightness went from white to map). **But it is still there on the other Kanto banners** (Should fix 2).
- **No date on Home:** confirmed.
- **Home maps:** Home is now 2.6 MB with 58 requests. The ten WebP copies are 76–197 KB each.
- **CSP:** no violation in 702 sweep draws, 1,220 crawl pages, view-only or the probes. There are no inline scripts or `on…=` handlers in the code.
- **Round 4 fixes still hold:**
  - `?pic` / `?fit` / `?ratio` / `?boxes` are strictly checked and escaped (probes below).
  - At 1280, a sidebar link chosen by keyboard keeps focus on the new link. The next Tab goes to the next link.
  - Tab stays inside the open drawer: 30 presses at 899 never left it, and the Try box is not reachable.
  - View-only boxes are `aria-disabled` (1,486 of 1,486 on Kanto).
  - Opened as a file: `no-family` class.

---

## Broken

None found. No console errors, failed requests, outside requests, broken pictures, sideways scroll, “undefined”/“NaN”, wrong mode or missing footer in any sweep or crawl. Her real server did not receive anything from this review.

## Should fix

1. **Every Pokémon freezes for about 5–6 seconds after every tick, and on every window resize.**
   - **Where:** `http://localhost:8050/pokedex/#dex`.
   - **Measured:** `rerender()` (what every tick runs) took 5.8 / 5.4 / 5.9 s at 1600 and about 5.1 s at 390. The same call on Kanto takes about 190 ms, and about 20 ms on Charizard’s page. The page has 1,014 cards and 73,300 elements. Almost all the time is in `fitLabels()`. It loops over 8,982 card-box labels and calls `getComputedStyle` and `getBoundingClientRect` on each, while it also writes font sizes. That forces a layout per label. On a second pass, the call alone took 19 s.
   - **Also:** `fitLabels` runs on every resize frame (`addEventListener("resize", () => requestAnimationFrame(fitLabels))`), so dragging the window on Every Pokémon locks the page.
   - **Fix:** measure all labels first, then write (two passes), and only measure words not yet sized. The same word is the same size everywhere, so measure one “Gigantamax”, one “Dynamax 3/4” and so on, and apply that size to all of them. Debounce the resize call. Card boxes could also wait until they scroll into view (`content-visibility:auto` on `.card`).
2. **Kanto’s white sky is still there on the other Kanto banners.**
   - **Where:** `#fast` with Kanto (Fast tick’s default) and every Kanto Pokémon page (for example `#p-6`), at about 1000 wide, worst in dark.
   - **What:** `SHOT_LIFT` only reaches the region page’s `::after` picture. Fast tick, Pokémon pages, Every Pokémon, Looking for and What’s on draw the map through `heroPics()` (`<i style="background-image">`), which ignores it.
   - **Measured:** the top-right 250 × 25 px of the banner at 1000 dark is 93 % near-white on Fast tick and 49 % on Charizard’s page, against 3 % on the Kanto region page. Screenshots: `fast_1000_dark.jpg`, `p-6_1000_dark.jpg`, `gen-1_1000_dark.jpg`.
   - **Fix:** give `heroPics` the same lift (or crop the sky out of `kanto-map-2.jpg` and its Home copy).
3. **The Pokémon page’s picture strip is cramped below about 1300 wide.**
   - **Where:** `#p-6` (14 boxes) at 1280, 1180, 1100, 1000 and 901. Also `#p-150`, `#p-25`, `#p-1` and `#p-133` from about 1000 down.
   - **Labels:**
     - They run into the box border. At 1280 the labels of Caught, Female, Dynamax, Mega X/Y, Shadow and Purified are 49–53 px wide in a 48 px label box.
     - From 1100 down they shrink to 6.5px.
     - Sizes are mixed within one strip, for example XXL 11.5px beside Dynamax 6.5px. That goes against “the same word the same size”.
   - **Why the check misses it:** `fitLabels` tests `box.scrollWidth > box.clientWidth`, but the overflow is inside `.pclab`, so it never fires.
   - **Pictures:** at 1000–1100 the boxes are 41–48 px wide, so the tick circle covers the Pokémon picture almost completely. Each box was meant to show the look.
   - **Screenshots:** `strip_p-6_1280.png`, `strip_p-6_1100.png`, `zoom_strip_1000.jpg`.
   - **Fix (my suggestion, not decided):** let the strip wrap to two rows under about 1300, as phones already do with 7 rows. Test `.pclab` itself, and give every label in a strip one size.
4. **Every Pokémon, Looking for and What’s on each download about 13 MB.**
   - **Measured:** 13.3 MB (`#dex`), 13.7 MB (`#want`) and 13.3 MB (`#coming`), against 2.6 MB for Home. Each loads all ten full-size maps (307 KB–2.1 MB each) for the same ten-map strip Home now shows from `regions/home/*.webp`.
   - **Fix:** make `ALL_MAPS()` use `homeMaps()`. The strip is the same height there.
   - **Other pages:** region pages are 3.1–3.5 MB (one full map up to 2.1 MB for Galar). A 1,600-px-wide banner copy would save about 1–1.5 MB per region page.
5. **Prev / Next numbers on a Pokémon page are low contrast.**
   - **Where:** `#p-201` and every Johto page, at any width. `#0200` / `#0202` in `.pn small` is #C0A7AA on the Johto gold, 2.97:1. On Kanto’s red it is 3.96:1, which axe flags too, but only at 390.
   - Both modes, independent of the Try switch.
6. **The sidebar search box still has no focus ring** (round 3 and 4 polish, unchanged).
   - `site.css:174` has `outline:none`. Focus only changes the 1px border to `--accent` and lightens the fill slightly.
   - It is the one control without the 2px ring that every other stop has. All 40 Tab stops on Kanto at 1280 have a 2px ring.
7. **Test fragility.** The first full suite run had 1 failure, “shut and out of the Tab order at 899” (`tests/e2e/site.test.js:980`). It ran while the machine was busy (604 s instead of about 270 s). The rerun passed 77 of 77.
   - The step resizes the frame, waits for the media query, then `await wait(50)` before checking `side.inert`. Under load, the family’s reset hadn’t run yet.
   - **Fix:** use `await until(() => side.inert && !isOpen())` instead of the fixed 50 ms.

## Looks (list only)

- **Tabs, 901–1000** (`#gen-1` at 901 and 1000): stacked tabs with labels at 7.25px (901) and 8.5px (1000). “Gigantamax” touches its tile edge at 901. The 4★ tab sits 7px from the window edge, because the row reaches into the banner padding by design. Legible on a sharp screen, but the smallest writing on the site (`zoom_gen-1_901_light.jpg`).
- **Tabs at 1280** (her second width) are 8.5px beside the icon, smaller than the stacked 9.25px at 1100. The stacked layout at 1280 would give larger writing.
- **Phone tabs** (`#gen-1` at 390): four rows of 4 + 4 + 4 + 1, with “4★” alone on the last row. Even rows were the aim (5 + 5 + 3 doesn’t fit at 8.5px).
- **Form-count numbers** on form-by-form cards are 8.5px at 85 % opacity (“1/2”, “28/28”), for example Unown on `#gen-2`.
- **Form picker names are cut with “…”** at every width (unchanged): “Paldean Combat”, “Archipelago”, “Single Strike” on `#p-128-paldean`, `#p-666` and `#p-892`.
- **What’s on bars are cut with “…”** (unchanged): “Dynamax Espurr Max Monday”, “Twitch Drops for 2027 Pok…”. The Twitch Drops event is listed as an Event, though it is irrelevant to her.
- **Kanto’s white sky at the start of the ten-map strip** on Home, Every Pokémon, Looking for and What’s on (top left of the strip). It is less visible there.
- **Dark Pokémon in dark mode** on the Pokémon page’s plain boxes (Caught, Female, Male): Umbreon on `#p-197` is nearly invisible. The Try switch doesn’t touch these boxes (`try\sheet_art_p-197.jpg`, bottom strip).
- **Not-found addresses** `#nope`, `#p-9999` and `#p-25">` still quietly show Home, with nothing lit in the sidebar (unchanged).
- **Looking for:** its section headings are `h3` with no `h2` above them (axe heading-order; minor).

## Try switch options (fair notes)

Light mode is unchanged by every Card art option: the art-window pixels hash the same for all four on Kanto, Sinnoh, Charizard, Umbreon, Gengar and a costume set. Sheets: `try\sheet_art_*.jpg` (dark, 2 × 2: now / bright / glow / light).

**Card art in dark mode**

- **As now:** muddy olive-grey on most types (Bulbasaur and Charmander look alike). Dark Pokémon nearly vanish (Umbreon, Gengar).
- **Brighter:** each type reads at once (green, orange, blue, yellow-green, purple). It matches the light-mode idea best and is calm.
  - Normal and Dark types stay greyish-brown, close to As now (Starly, Umbreon), but Umbreon is clearly visible.
  - Costume cards and Home’s region sets use the region colour, so every costume card on a set page is the same pink-red whatever the Pokémon.
- **Glow:** the most striking. Small sprites pop.
  - Normal types get almost no glow (Starly, Bidoof), and Dark types only a faint brown halo.
  - On Home’s wide region windows the glow sits only behind the middle Pokémon. The left and right ones are on black, so the middle one looks “chosen” (`try\sheet_art_home.jpg`).
  - On costume sets every card has the same red glow, and uncaught grey Pokémon float on red, which weakens the “not caught = faded” signal.
- **Light window:** the best for seeing every Pokémon, including the darkest ones.
  - It is a bright block on a dark page, the most glare of the four.
  - The type colour is faint.
  - Uncaught grey Pokémon on costume sets become very faint on white (Polteageist).
- **None of the four** changes the plain boxes in the page strip (see Looks).

**Box colours** (sheets: `try\sheet_boxes_*.jpg`, close-up `try\zoom_boxes_now_vs_deeper.jpg`)

- **As now:**
  - axe finds about 590 low-contrast labels on Kanto alone in both modes (white on Male 4.17, Shiny 3.64, Lucky 2.51, Purified 4.2, XXL 4.21, 4★ 4.36, Mega 4.49).
  - It also flags the Looking for Shiny count (3.64) and the What’s on GO Pass bars (4.2).
- **Deeper:**
  - It clears all of those. Every value in the notes was confirmed: 4.50–4.56:1 on white.
  - **Visibly, only Lucky really changes:** bright gold becomes a dark mustard-bronze, next to the other bright boxes. It is less “bright, not dull” (her rule) and less balanced with the rest. Shiny is a shade darker. Male, Purified, XXL, 4★ and Mega look the same.
  - The Lucky colour also changes Home’s Lucky bars and the Community Day bars.
  - Leftovers Deeper doesn’t fix (they are tinted or semi-transparent white, not the box colour):
    - form-count numbers at 85 % opacity: 3.71–3.91:1;
    - the tier label on raid bars (#F3DDD1 on Mega): 3.46:1;
    - day names on GO Pass bars on phones: 3.99:1.

    Making those labels plain white would finish the job.
  - Used as icon colours on dark card stock, the deeper shades drop (Lucky 6.96 to 3.85:1). That still passes the 3:1 rule for icons.

## Data

- **Counts agree everywhere checked.**
  - The sidebar regions add up to the Every Pokémon total: Kanto 151, Johto 100, Hoenn 135, Sinnoh 107, Unova 156, Kalos 72, Alola 106, Galar 108, Hisui 23, Paldea 122, total 1,080.
  - Each matches the species count plus that region’s regional forms: Alola 88 + 18, Galar 89 + 19, Hisui 7 + 16, Paldea 120 + Wooper + one Tauros.
  - Home’s totals equal the tabs: 950 of 1,080 Pokémon, Shiny 847, Lucky 623 of 1,058, Gigantamax 12 of 32, Mega 57 of 89.
  - 124 sets (45 events, 299 costumes).
- **Every internal link works.** 1,216 distinct links each draw a real page (no Pokémon or set link falls back to Home). All 5,444 pictures and backgrounds answer 200.
- **Her ticks match the data:** 1,491 keys, no orphan keys, no impossible box, and nothing ticked on a Pokémon that isn’t out.
- **Flags are consistent:**
  - no Gigantamax outside `GMAX_SPECIES`, and none on a regional form;
  - no Dynamax for Zacian, Zamazenta or Eternatus;
  - no shiny or Mega on an unreleased entry;
  - Shadow carried through every evolution (0 breaks);
  - 64 Megas.
- **Facts spot-checked** (Charizard, Mewtwo, Eternatus, Meltan, Melmetal, Clefable, Unown F, Rotom, Pikachu): types, categories, heights, weights and buddy distances look right. Charizard: Fire · Flying, Flame Pokémon, 1.7 m, 90.5 kg, 3 km, Mega X/Y, Gigantamax. Eternatus: Lucky “Not possible”. Clefable has one Mega, and Mega Clefable is due 28 Nov per her list.
- **Unreleased entries:** all 61 entries with no picture are ones not out (for example Type: Null, Magearna, Pecharunt). They show “?”, as designed. Pecharunt’s page (`#p-1025`) has no picture and no category.
- **No Pokédex entry yet** for 4 released entries: Dipplin, Poltchageist, Sinistcha and Hydrapple show “No Pokédex entry for it in the game’s text yet.”
- **What’s on:** refreshed today with 22 events. Every event link is on leekduck.com.

## Text

- No straight apostrophes in shown text on any of the 1,220 pages. No “undefined” or “NaN”.
- The only US spellings are in GO’s own Pokédex text (“color”, “favorite”, “center”, “behavior”, “defense” on 30 Pokémon pages) and the game’s form name “Defense Forme” (Deoxys). Those are word for word, as the rules allow.
- Footer line 1 is word for word on every page: “No cookies, no tracking, no ads. Made with HTML, CSS, JavaScript and Python, kept on GitHub.” The credits are unchanged and include Tabler.
- A small wording risk: before the server’s answer arrives, `readOnly` is true. A box clicked in that first moment on http gets the toast “Opened from the folder: open it with the shortcut to save ticks.” (`app.js` 1366), which is wrong there.

## Performance

| Page (1600, fresh) | Weight | Requests | Render / rerender |
|---|---|---|---|
| Home | 2.6 MB | 58 | 21–26 ms |
| Every Pokémon | **13.3 MB** | 49 | **5.3–5.9 s** (73k elements) |
| Kanto | 3.1 MB | 46 | 170–190 ms |
| Galar | 3.5 MB | 46 | 86–98 ms |
| Charizard | 3.3 MB | 40 | 14–18 ms |
| Event Pokémon | 3.2 MB | 321 | 38–43 ms |
| Looking for | **13.7 MB** | 149 | 26–30 ms |
| What’s on | **13.3 MB** | 37 | 24–31 ms |
| Fast tick | 3.6 MB | 167 | 25 ms |

- `data.js` is 864 KB on every first load. It is revalidated afterwards (`Cache-Control: no-cache`, so 304s).
- Slowest first draws in the crawl: Every Pokémon, then Hoenn and Unova, then Pokémon pages with large families: Pokémon pages in the crawl drew in 0.3–0.7 s (Mamoswine, Cosmoem, Cresselia, Leafeon) while the machine was busy.
- When 8050 was under heavy parallel load (this review plus the test suite), pictures queued for several seconds, and once a page load got `ERR_CONNECTION_REFUSED` from 8050 for a moment. Her one window won’t see that.
- About 8.8 MB of unused maps are still in `site/regions/`: kalos-map-1, kalos-map-3, kalos-map-4.png, kanto-15, and sinnoh-map-1, 2, 4 and 5. Only `?pic=` and `SHOT_FIT` name some of them. They would be uploaded if the site goes online (“the only folder to upload”).

## Code

- **Duplicated code:**
  - `boxes()` and `formBoxes()` build the same nine-row grid twice, including the `replace('class="tk ', 'class="tk wide ')` string hack.
  - `fitTabs` has its one-row and rows paths with two near-copies of the “shrink to fit Gigantamax” loop (`oneRow` vs lines 482–487).
  - `row()` is defined twice (in `home()` and `setTiles()`).
- **Dead or stale code:**
  - `SHOT_RATIO = {}` (always empty, so `shotCls` / `--shotratio` never apply).
  - `SHOT_FIT` still lists `kanto-15.jpg`, `sinnoh-map-1.jpg`, `kalos-map-3.jpg` and `kalos-map-4.png`.
  - `.hero > :not(.heroart)` (`site.css:478`) names the removed parade.
  - `boxLook()` is a wrapper around a constant.
  - The comment at `app.js` 321–323 still describes “Colours + parade” and a dark sidebar.
  - `DEMO` re-parses `location.search` instead of using `TRY`.
- **Fragile code:**
  - `focusKey()` builds a CSS selector from every `data-*` attribute, including `data-t1` and `style`-free attributes. It works, but any new data attribute changes the key.
  - `fastFormsPage` counts got cells with `c.includes('aria-pressed="true"')` on HTML strings.
  - `kindOf()` guesses event kinds from free text (`/raid|max/i`).
- **Stale docs:**
  - `tools/serve.py`’s docstring says it is started at login from the Startup folder and that the backup “saves it to git and zips it”. Neither is true since 19 Nov.
  - `tools/backup.py` says “Run every Sunday by the Windows task "Jemma's Pokedex - weekly backup"”, and CLAUDE.md says Sundays 09:40. The parent’s `tools/weekly.py` now runs it daily at 09:30 under “Jemma’s Journals - backup”, and the old weekly tasks are disabled.
  - `tools/make_home_maps.py` still says “TEMPORARY trial” though Smaller was picked.
- **Try switch code:** it is cleanly marked (one TRIAL block in `app.js` and one in `site.css`), and the tests already exercise it. When she picks:
  - with Brighter, Glow or Light window, fold the chosen rule into the binder look’s dark block;
  - with Deeper, move the seven values into `:root`;
  - remove both blocks and the two localStorage keys (as was done for `jemmas-pokedex-try` at line 33).

## Security

- **Address values: all 14 probes stayed inert** (GET only, nothing saved).
  - `?pic=x" data-pwn="yes`, `?pic=a.jpg');--x:url('b`, `?fit=center"><img src=x>`, `?ratio=1" data-pwn=1` and `?pic=../../data/collection/go.json` fall back to the chosen map.
  - `?boxes="><b>`, `?only=25,<img>`, `?want=<img src=x>`, `?fastkind=">` and `?demo="><img>` have no effect.
  - `#set-"><img src=x onerror=…>`, `#p-25">` and `#gen-<img>` fall back to sets or Home.
  - No injected element, no CSP report.
- **Escaping:** every data string reaching `innerHTML` goes through `esc()` / `attr()` / `tip()`: names, forms, event names, set titles, notes, the search term, ids and keys.
- **One defence-in-depth gap:** the What’s on link uses `attr(ev.link)`, which doesn’t stop a `javascript:` URL from the ScrapedDuck feed. `import_events.py` stores `ev.get('link')` unchecked. The CSP (`script-src 'self'`) would block it, and today all 22 links are `https://leekduck.com/…`. Even so, (my suggestion) accept only `https://leekduck.com/` links in `import_events.py`.
- **Save server unchanged and sound:**
  - `/api/*` checks the Host;
  - POST needs `X-Pokedex: 1`, so a cross-site page can’t send it without a preflight;
  - body read capped at 10 KB;
  - keys and ticks allow-listed;
  - `/family/` confined to the folder (round 4 probes).

  The family server checks its own Host and passes only the allowed headers.
- **View only (8060):**
  - `view-only` set on all 7 page types, no notice, and every box `aria-disabled`;
  - no Tick all;
  - clicking Shiny on Pikachu changed nothing and sent no request;
  - no CSP report.

  The only trace is the browser’s own 404 line for `api/collection`. The footer has Back to top and Dark mode, and “← Jemma’s Journals” goes to `/`.
- **Dark mode button:** it switches to dark, `jj-mode=dark`, theme colour #4E1018, “Light mode” with `aria-pressed=true`. With the new debounced save it sends one `POST /family/mode` “dark” (blocked here), so the server’s stored mode stayed dark.

## Tests

- `python -B -X utf8 tests/run_tests.py`: **97 tests, 1 failure, 2 skipped (slow)** on the first run (604 s, machine busy). The failure was the 899 resize timing step (Should fix 7).
- `tests/run_tests.py e2e` rerun: **77 of 77 page tests passed** (220 s).
- `go.json` SHA-256 is the same before and after both runs. No files changed in `pokedex`.
