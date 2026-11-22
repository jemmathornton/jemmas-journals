# Round 5: phones and tablets by touch (22 Nov 2026)

Read-only review through the family server (http://localhost:8050). Playwright with Edge and real mobile emulation (touch, mobile viewport): iPhone 13 (390×664 visible), iPhone 13 landscape (844×342), Pixel 7 (412), a small phone at 360×740, a tiny one at 320×568, iPad Mini portrait (768×1024) and landscape (1024×768), plus 195 px wide to stand in for 200% page zoom. Light was forced by removing `data-jj-server-mode` and answering `GET /family/mode` with "light" inside the test browser only. Dark was the server's own mode. Every POST was blocked. The only one a page tried was the Pokédex tick (`POST /pokedex/api/tick`, blocked). Nothing in the sites was changed.

**Note on `logs/family-mode.txt`:** it read `dark` at 13:05. At 14:01:36, while this review was running, it changed to `light`. My scripts never pressed a Dark/Light mode button, and every POST went through a route that aborted it, so I don't think this review caused it. But I can't prove that, and other sessions were working in the folder at the same time (they wrote files in this scratchpad from 13:10). I left it as it is. Please check which mode she wants.

Screenshots: `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\review5\mobile\` (`iphone-light-NN-*.png` is the tapped journey, `sweep-<device>-<mode>-<page>.png` is each device, `scrolled-*` shows the sticky bars, `drawer-*` the drawers, `pokedex-*` the ticking checks).

Journeys tested by tap: home → each Open link → Menu → a section → a detail page (Fantasy → a book; Willow Creek → Foundry Cove → Bargain Bend lot; Laurent household → Hector; Kanto → Pikachu; Trips → Italy → Day 1) → Back → search → Library's Add a Book and Travels' Write (fields focused, nothing saved) → footer → ← Jemma's Journals.

---

## Broken

1. **Pokédex: the Try box hides the bottom of the Menu drawer on phones.** The box is fixed, `z-index:60`. The drawer is `z-index:20` and the scrim 90 (it sits above the scrim too). On iPhone 13 it covers 124 px of the 664 px screen. With the drawer open, **Event Pokémon, Looking for, What's on and Fast tick can't be tapped**: a tap lands on the Try box's "Deeper" button (`pokedex-drawer-trybox-covers.png`). On every Pokédex page it also covers the bottom fifth of the content. It's temporary, but until it goes, give it a higher z-index than the drawer or hide it while `html.jj-menu-open`. Better still on phones: a small collapsed "Try" tab.
2. **Back loses your place in Library and Pokédex.** On iPhone: scroll Kanto to Pokémon 31 (y = 6253), open it, press Back, and you're at the top of Kanto again (y = 0, still 0 after 3.5 s). Library's Fantasy shelf does the same (2484 → 0). Sim World keeps the place (it sets `history.scrollRestoration = "manual"` and restores it). Travels gets there too, but only after more than 1.2 s, so you see the top first. On a phone this is the most tiring thing in the family: with 151 cards you scroll all the way down again each time.

## Should fix

### Family (all four apps)
- **Search is only inside the drawer on phones.** It takes two taps (Menu, then the box), in all four apps. A search icon button in the top bar that opens the drawer with the box focused would make it one.
- **Input text under 16 px makes iPhone Safari zoom in when you tap a field** and stay zoomed: Sim World search 14 px, Pokédex search 15.5 px, Travels search 14 px, and every Travels Write field 15 px. Library is 16 px everywhere, which is right. Set inputs to 16 px on phones.
- **Tapping the magnifier in the search box doesn't focus it** (Library, Pokédex, Travels; Sim World does). In Travels the typing area is only 21 px tall inside a 38 px box.
- **Safe area:** every page has `viewport-fit=cover`, but no site pads `env(safe-area-inset-left/right)`. Home and Travels pad none at all. In iPhone landscape the notch will cover the left edge of the text (about 47 px, against 16–24 px gutters). Library, Pokédex and Sim World pad the top only. Checked in the code: emulation can't show a notch.
- **No swipe to close the drawer.** Scrim tap, Escape and tapping a link all close it, which is the essential part. A left swipe is what phone users try first.
- **"← Jemma's Journals" in the drawers** is 10–11 px text, 24–32 px tall (Pokédex 131×24). It's the way home, so make it at least 44 px tall (the text can stay small).
- **Sticky bars in phone landscape:** the top bar takes 52–65 px of a 342 px screen (Pokédex 100 px with its sticky toolbar, 29%). Hiding the bar while scrolling down and showing it on scroll up would help in landscape.
- **Drawer widths differ:** Library and Sim World 280 px, Pokédex and Travels 300 px.

### Home
- The four "Open My …" links are 30 px tall (the photos above them are big links, so this is minor). 44 px would match the footer buttons.

### Library
- **Hover-only information:** shelf cards put the format in a `title` ("Read · Audiobook", "Read · Hardback"). The "Signed to you" mark is an icon with only a title, and so is "Illustrated Edition". A phone can't show titles. Put the format in visible text or in the book page only, and give the signed icon a visible word or put it in the book page.
- **Full-size covers in the shelf grid:** some covers are 1488 px wide and shown at 95 px (5.2× more pixels than a 3× phone needs). They're lazy, but each is a big download. Use the `thumbs/*.webp` copies, as Home does.
- Breadcrumb "Fantasy" on a book page is 17–23 px tall. The "Set up phone scanning" summary on Add a Book is 22 px.
- On a phone the first book on a shelf is three screens down: stats, then the plate of covers, then nine filter chips. Consider collapsing the filter chips into one row that scrolls sideways.

### Sim World
- **Hover-only:** the lot card icons for "Built: yes", "Shared: yes" and "Sims made: not yet" are only in `title` (22 on a neighbourhood page). On a phone they're coloured dots with no meaning. "Bonus trait" on a Sim page is title-only too.
- Household links on neighbourhood lot cards ("Open the Davidson household") are 18 px tall. Sim names on household and Sim pages are 21–22 px tall (10 per page, under the 24 px minimum).
- Lot photo arrows are 42×42 (close to 44; fine).
- Small text: 10–11 px labels ("Base Game", "22 lots · 12 households", "Residential", "Neighbourhood") all over the phone home and world pages.

### Pokédex
- **Fast tick on a phone: the squares show only the number (0001…).** The Pokémon's name is only in `title`, so you have to recognise the sprite. Fine for a fan, but there's no name at all by touch. A long-press, or the name under the number, would help.
- **Ticking on region and Every Pokémon cards:** the boxes are 74×24 (Caught 152×24) with a 4 px gap. That's exactly the 24 px minimum on phones and **23 px on iPad** (portrait and landscape), with "Show the shiny" at 22×22. That's under the minimum, and a slip ticks the neighbour. On the Pokémon's own page the boxes are large 175×199 tiles, which is very comfortable. If she ticks from region pages on her phone, 32–36 px tall boxes would make it much safer.
- "Hide ones I have" switch: 132×21.
- Feedback is good: when saving fails, the box goes back and a toast says "Not saved: the Pokédex server isn't answering…". But the toast sits over the filter chips for a few seconds.
- 8.3–8.5 px text on the banner tabs at iPad landscape (1024): "of 151", "Female". This is below her 8.5 px floor (set for 1280), and the card number "#0001" is 10 px.
- A Pokémon page on a phone opens with the map banner, two buttons and the Prev/Next row, so the boxes start more than two screens down.

### Travels
- Breadcrumbs "Trips › 2026 › Italy" are 18 px tall. "Read post" links on trip pages are 22 px.
- **Map:** countries are tiny targets (Denmark 4×3, Portugal 3×6, pins 6×6), crowded together. The Countries visited list below it covers the same places, so nothing is lost. Maybe don't make the tiny shapes links on phones, so a pinch-zoom doesn't open a country by accident.
- The Write page's "Only on this PC" checkbox row is 21 px tall.
- `world.js` (1.23 MB) loads on every page, including trip lists and posts. See Performance.

## Looks (list only)
- http://localhost:8050/pokedex/#p-25, iPhone 13: the first screen is all banner and heading, and the boxes start below the fold.
- http://localhost:8050/library/#b-yw7av9br71, iPhone 13: the cover fills the first screen and the title starts at the bottom edge.
- http://localhost:8050/library/#shelf-fantasy, iPhone 13: the books start three screens down.
- http://localhost:8050/pokedex/#gen-1, iPad Mini landscape: 13 banner tabs squeezed to 8.3 px text.
- http://localhost:8050/pokedex/ (every page), all phones: the Try box covers the bottom 124 px.
- http://localhost:8050/pokedex/#fast, iPhone 13: the "Not saved" toast covers the Region chips.
- The drawers, iPhone 13: Library and Sim World 280 px wide, Pokédex and Travels 300 px. The search box sits in a different place in each (Travels puts it straight under the name, the others under a rule).
- The footers on iPhone 13 match (name, line 1, credits one per line, Back to top and Dark mode both 44 px), which is good.

## Performance on mobile
Measured on iPhone 13 with the network throttled to "Slow 4G" (1.6 Mbit/s, 150 ms latency, cache off), served by the family server. **The family server doesn't gzip.** GitHub Pages will, which shrinks the data files to the sizes in brackets. The images won't shrink.

| Page | First load | After scrolling | Largest content shown | Biggest files |
|---|---|---|---|---|
| Home `/` | 502 KB | 526 KB | 2.9 s | region-johto-kanto.webp 134 KB |
| Library `/library/` | 1.37 MB | (covers come from the service worker) | 8.6 s | data.js 866 KB (287 KB gzipped), app.js 141 KB |
| Library book | 1.37 MB | n/a | 8.3 s | the same |
| Sim World `/sim-world/` | 1.42 MB | 2.13 MB | 8.3 s | data.js 830 KB (166 KB gzipped) |
| Sim World Willow Creek | 2.91 MB | n/a | 9.0 s | **willow-creek.jpg 832 KB banner** |
| Pokédex `/pokedex/` | 2.59 MB | 2.65 MB | 1.2 s (load 14.6 s) | data.js 864 KB (189 KB gzipped), five home map WebPs of 140–190 KB |
| Pokédex Kanto | 3.06 MB | 3.59 MB | **19.9 s** | **kanto-map-2.jpg 1.76 MB banner** |
| Pokédex Pikachu | 3.37 MB | 3.67 MB | 18.6 s | the same banner |
| Travels (any page) | 1.44 MB | 1.44 MB | 8.8 s | **world.js 1.23 MB** (389 KB gzipped) on every page |

- **Biggest wins:** phone-sized WebP copies of the region and world banners (the Kanto banner is 1.76 MB for a 390 px strip; Home already uses small WebP copies). Gzip once online. Load Travels' `world.js` only on pages with a map.
- Lazy loading is used well (Pokédex lazy-loads all 151 sprites on Kanto; Home all 75 images).
- Sim World lot photo thumbnails are 720 px shown at 84 px. Library shelf covers are the full 1488 px files.
- `Cache-Control: no-cache` on everything from the family server: every visit checks every file again. That's fine on the PC. Online, versioned files (`?v=`) could be cached for a long time.

## Good already
- **No sideways scrolling anywhere:** 19 pages × 8 sizes, including 320 px and 195 px (200% zoom). Wide things (the family tree, photo strips, maps) scroll or clip inside their own boxes.
- **The 900 px breakpoint is sensible:** iPad portrait and phone landscape get the Menu drawer, and iPad landscape (1024) gets the laptop sidebar, which fits.
- **The four drawers behave the same:** Menu button 44 px, scrim tap closes, tapping a link closes and goes there, focus moves into the drawer, the page behind doesn't scroll, and long lists scroll inside the drawer (Sim World's 52 links reach Notes on a 320×568 phone).
- The family footer is identical and touch-friendly on every site, and the credits stack one per line on phones.
- Pokédex's own-page tick tiles are big and clear, and a failed save is undone with a plain message.
- Library's Add a Book uses 16 px fields and a numeric keypad for ISBN and Pages (`inputmode=numeric`).
- Every site has a viewport tag, an apple-touch-icon and a theme-colour. Library also has a manifest and a service worker.
- Dark mode on phones looks consistent (`sweep-iphone-dark-*.png`). No body text under 12 px except labels and counts.

*Not tested:* a real iPhone (notch, Safari's zoom on focus and keyboard covering are from the code and known Safari behaviour). Android-style text scaling couldn't be emulated reliably, so 200% page zoom (195 px) stands in for it.
