# Review, round 2: Jemma’s Sim World (21 Nov evening)

Read-only: nothing in SimTracker was edited, built or committed (`git status` clean before and after, still at 20cedf8).

**How it was checked:** 41 pages served from `site/` on disk through Playwright in Edge: home; 7 world pages (Willow Creek, Britechester, StrangerVille, Sulani, San Myshuno, Mt. Komorebi, Oasis Springs) plus the unowned Forgotten Hollow address; 4 neighbourhoods (incl. StrangerVille Secret Lots); 6 lots (with photos, Community Space Admiral’s Wreckage, rental Rio Verde, Oakenstead, Key Point, 8 Bells); Willow Creek Households; 4 households (Goth, Straud and Laurent in unowned worlds, Fletcher); Bella, Vladislaus Straud, Mortimer; a dynasty, club and organisation; Calendar and Britechester’s calendar; Clubs, Dynasties, Organisations, Families, Businesses; Admin, Progress, Notes; a missing page. Each at 1600×930, 1280×800, 901, 899 and 390×844, light (with the device set to **dark**, to prove it still opens light) and dark (`jj-mode=dark` stored before load). Per page: sideways scroll, text contrast against its real background, broken images, missing alt, straight apostrophes, American spellings, “1 downloads”-type plurals, undefined/NaN, H1 count, console errors, failed requests, footer, phone tap targets. Plus scripted checks of dark-mode carry, Back to top, the Menu drawer (every family behaviour), focus rings and search.

Screenshots: `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review2\simworld\` (`<page>_<width>_<light|dark>.jpg`; full pages for 1280 and 390 in `full\`; `drawer-open_*`, `focus-*`, `cs-tabs_901_light.jpg`, `grid-*`). Raw results: `..\sw-sweep-*.json`.

**Tests:** `tools/run_tests.py`: all passed (387 Python tests, 1 skipped; 100 site tests). It changed no files.

**Clean everywhere:** no console errors, no failed requests, no broken images, no missing alt, no straight apostrophes, no undefined/NaN, one H1 per page, footer on every page (one `<footer>`, both buttons 44 px and level). No sideways scroll except item 1. Only American spellings are the game’s own names (“Neighborhood Brawl”), which her rules allow.

## Family rules: all pass

- **Dark mode:** opens light with the device set to dark; `jj-mode=dark` → dark before first paint (already set at DOMContentLoaded), theme-color `#1B1524`, button reads “Light mode”, `aria-pressed=true`. Click → dark, saved as `jj-mode`, survives reload. Old `jsw-mode` is moved to `jj-mode` once and removed. A junk value falls back to light. No `prefers-color-scheme` anywhere. Other windows follow via the `storage` event.
- **Footer:** pin on dashed rule, “Jemma’s Sim World” plain display font, line 1 word for word, credits one per line under 700 px, Back to top (scrolls to 0, focus to `#view`; next Tab goes to page content) and Dark mode, 44 px, level, 12.5 px muted text at about 6:1.
- **Menu (≤900):** at 901 the sidebar, at 899 the bar with Lucide menu icon, “Menu” and “Jemma’s *Sim World*” linking `#home`. `aria-controls="side"`, `aria-expanded` toggles; closed drawer is `inert` (Tab goes straight to the page); opening focuses Home (her call); page behind is inert and doesn’t scroll; Escape, scrim and a link all close it with focus back on Menu; with words in the search, the first Escape only clears them; crossing 900 both ways resets it closed. Same at 390.

## Previous review: what happened to each item

| # | Item | Now |
|---|---|---|
| 1 | World descriptions cut off at 1280 | **Fixed** (banner grows; all checked worlds show 3 lines) |
| 2 | Dark Member/Heir badges unreadable | **Fixed** (`color:var(--ink)`) |
| 3 | Calendar “All worlds” chip in dark | **Fixed** |
| 4 | Gold one-word titles on bright maps | Fade + shadow added (her “in between” pick); still weak on Britechester, Sulani, StrangerVille: see Question A |
| 5 | Empty column at 1600 | **Fixed** (3 × 328 px) |
| 6 | Faint “Not owned” sidebar text | **Fixed** (no sidebar text under 4.5:1 now) |
| 7 | Lot-size brackets on household cards | **Fixed** |
| 8 | Search focus | **Fixed** (2 px gold ring) |
| 9 | Drawer keyboard | **Fixed** (see family rules), one gap left: item 2 below |
| 10 | Half restyled pages | Unchanged; still her Question B |
| 11 | Small card text | Unchanged |
| 12 | Uneven card titles (no description) | Unchanged (StrangerVille Secret Lots) |
| 13 | Faint world colours as text/pins | Unchanged (Sulani “Explore” label, Britechester and Mt. Komorebi pins almost vanish on the lilac sidebar) |
| 14 | Not-owned “Not owned” text | Decided by her (“as they were”) |
| 15 | “1 downloads” | **Fixed** (none found) |
| 16 | Phone tap targets | Unchanged: “← Jemma’s Journals” 18 px tall, Sim names 22 px, calendar ticks 16 px, events 19–21 px |
| 17 | Admin contrast | Unchanged (Progress: not-owned rows 3.16, “not owned” 2.22) |
| 18 | Calendar on phone | Unchanged: day names run together, event names overlap, Saturday/Sunday cut off (`full/calendar_390_light.jpg`); on her list as a Decide |

---

## Broken

Nothing broken.

## Should fix

1. **Sideways scroll on Community Space lot pages at 901–about 955 px.** *Where:* any lot with version tabs (Admiral’s Wreckage), sidebar showing, window just over 900. *What:* the 2-column version tabs in the right-hand column can’t shrink below 2 × 160 px, so the page scrolls 28 px sideways at 901 (19 at 920, 5 at 950); names and counts are cut (“Marke…”, “Comm… space”). *Evidence:* `cs-tabs_901_light.jpg`, `l-sulani--admiral-s-wreckage_901_light.jpg`. *Fix:* `.ver-tabs{grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}` (or one column when the aside is narrow), plus `min-width:0` on the buttons; add 901 to the no-sideways-scroll test.

2. **Open drawer covers the Menu button and the bar’s name link, but Tab still lands on them.** *Where:* ≤900, drawer open. *What:* the drawer (z-index 20) sits over the top bar (z-index 10). The Tab loop includes the Menu button (hidden under the drawer), and Shift+Tab from “← Jemma’s Journals” goes to the bar’s “Jemma’s Sim World” link, which isn’t in the loop and is also hidden. So focus disappears for one or two presses. *Evidence:* `drawer-open_390_light.jpg`; Shift+Tab order from Home: search → brand → Journals → bar name link. *Fix:* either start the drawer below the bar (`top:` bar height) so Menu stays visible as the close control, or make `.brand-bar` inert while open and leave the Menu button out of the loop (Escape and the scrim still close it). Family rule check: fine on paper, but a hidden focus stop is the sort of thing a family test should catch.

3. **Gold focus ring hard to see on map banners.** *Where:* neighbourhood tags and other links on map banners, light mode. *What:* the ring is the light-mode brass `#A47A24`, which nearly disappears on Britechester’s olive-brown fade. *Evidence:* `focus-maptag_1280_light.jpg`. *Fix:* on `.hero.mapped` use the brighter `--brass-light` (already defined there) or white for `:focus-visible`.

## Polish

4. **Footer credits leave a “·” at the end of a line on laptops.** At 1600 (her window) the last “·” ends line 1; at 1280, 1024 and 901 one or two do. The phone version stacks them correctly. *Fix:* hide a separator that ends a line (e.g. put each “· credit” together in one `nowrap` span, so the dot travels with the next credit). Under 700 the credit text is 12 px, not the family’s 12.5.
5. **Top bar name “Sim World” in light-mode gold is 3.28:1** at 22 px (just under the large-text size). Sidebar version is larger and passes. *Fix:* `--brass-light`-style darker gold in the bar, or 24 px.
6. **Solid gold “Head” badge 4.29:1**, organisation “Member” 4.03:1, the lot page’s gold “View on the Gallery” button 4.43:1, family-tree initials 3.1–4.3:1. All slightly under 4.5; darken the gold a touch behind dark text.
7. **Secret Lots card says “0 of 0 lots built”** while the neighbourhood holds 1 lot (The ██████ Lab) and its banner says “1 lot”. Probably on purpose (it can’t be built), but reads odd; “Community lots only” plus no count would be clearer. *Evidence:* `full/w-strangerville_1280_light.jpg`, `full/n-strangerville-secret-lots_1280_light.jpg`.
8. **Phone world banner figures:** the 4th figure (“41 Sims”) drops to a row of its own at 390. *Evidence:* `w-willow-creek_390_dark.jpg`.
9. **Household “The Sims” table on phone** is a fixed 720 px table in a sideways scroller, so “Young Adul…” is cut at the edge; fine for keyboard/touch, but a stacked list would read better. *Evidence:* `full/h-willow-creek--goth_390_light.jpg`.
10. **World descriptions stop mid-phrase** at 3 lines (“…the more lavish upscale Lani St.…”, “…spend time in the…”). The clamp is deliberate; a 4th line on laptops would finish most of them.
11. **Calendar banner on phone:** the text starts on the banner’s inner frame line (both at 16 px). *Evidence:* `calendar_390_light.jpg`.

## Question for her

A. **Gold one-word world titles on bright maps** (Britechester, Sulani, StrangerVille most): keep as now (gold with shadow), white, or white with the gold only on a second word? (Still open from round 1; show side by side.) *Evidence:* `w-britechester_1280_light.jpg`, `w-sulani_899_light.jpg`, `full/w-strangerville_1280_light.jpg`.
B. **Lot, Sim and household pages in the town-plan style** (square cards, square crumbs) or keep rounded? (Still open.)
C. **Calendar on a phone:** her open Decide; it’s still the one page that doesn’t work at 390.
