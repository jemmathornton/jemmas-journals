# Review, round 2: the five sites as one family (21 Nov 2026, evening)

Read-only check that the family rules (`research/family-rules.md`) now hold the same way on home, Library, Sim World, Pokédex and Travels. I changed nothing in any project. Round 1 is `consistency.md` in this folder.

**How:** Edge through Sim World’s Playwright. All five were served from disk under one pretend address, as they would be online: home at `/`, apps at `/library/`, `/sim-tracker/`, `/pokedex/`, `/travels/`. Home was wrapped in a doctype skeleton, as `tests/check_page.js` does. Pokédex `/api/collection` came from `data/collection/go.json` and every other `/api` call got a 503. Google Fonts were let through so Library looks as it would online; nothing else external was requested.
- **Sizes and pages:** each start page at 1600 × 930 and 390 × 844, plus 899 and 901 wide for the menu. Footers were checked on every page linked from each sidebar: Library 25, Sim World 25, Pokédex 17, Travels 25, home 1. On phones, the first 6 pages of each app.
- **Dark mode carrying across:** I pressed Dark mode on each site in turn and then opened the other four, giving 5 × 4 visits.
- **Old keys:** each site was opened with only its old per-site key saved, to check it is moved over.

**Pictures:**
- `round2-family-laptop.jpg`: the five sites at 1600. Light is a first visit with the device set to dark. Dark is after pressing Dark mode on home only.
- `round2-family-phone.jpg`: 390 wide, light, dark and with the drawer open.
- `round2-footers.jpg`: the five footers.

**Raw numbers and scripts:** `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\family2\` (`fam2.js`, `results.json`, `shots\`).

No page errors. No sideways scrolling on any page checked, at 1600 or 390.

**Note:** Pokédex’s own session changed its footer while I was checking (uncommitted change to `site/index.html`). Its credits now read “Icons by Lucide, Phosphor, MingCute and Solar (480 Design)”, and the “·” separators are `aria-hidden` with spaces. The second run and the footer sheet show that version. Nothing else in the four apps changed during the review (their `git status` is clean).

## Rule × site

✓ = holds, ✗ = fails, ~ = holds, with a difference noted.

| Rule | Home | Library | Sim World | Pokédex | Travels |
|---|---|---|---|---|---|
| Opens light with the device set to dark | ✓ | ✓ | ✓ (but `data-mode` is left unset, not `"light"`) | ✓ | ✓ |
| No `prefers-color-scheme` rules (live stylesheets scanned) | ✓ none | ✓ none | ✓ none | ✓ none | ✓ none |
| Button reads “Dark mode” with a moon, then “Light mode” with a sun; `aria-pressed` | ✓ | ✓ | ✓ | ✓ | ✓ |
| Reload keeps dark | ✓ | ✓ | ✓ | ✓ | ✓ |
| Dark pressed here opens the other four dark (`jj-mode`) | ✓ 4/4 | ✓ 4/4 | ✓ 4/4 | ✓ 4/4 | ✓ 4/4 |
| Light pressed on another site carries back | ✓ | ✓ | ✓ | ✓ | ✓ |
| Old key moved over (only the old key set to dark → opens dark, `jj-mode` saved) | ✓ `jj-mode2` removed | ✓ removed | ✓ removed | ~ **old `jemmas-pokedex-mode` left behind** | ✓ removed |
| theme-color light → dark | #8E6520 → #6A4A17 | #3B2616 → #1C1610 | #EEEAF2 → #1B1524 | #7A1E2A → #4E1018 | #ECF1EA → #15212C |
| Tab icon, files load | ✓ flips to dark icon | ✓ (no dark icon) | ✓ (no dark icon) | ✓ (no dark icon) | ✓ new this round (no dark icon) |
| robots meta `noindex, noai, noimageai` | ✓ | **✗ none** | **✗ none** | **✗ none** | ✓ |
| One footer on every page checked, same words on every page | ✓ 1/1 | ✓ 25/25 | ✓ 25/25 | ✓ 17/17 | ✓ 25/25 |
| Order: name, line 1, credits, buttons | ✓ | ✓ | ✓ | ✓ | ✓ |
| Name in the display font, plain | ✓ Instrument Serif 24px | ✓ 24px | ✓ 24px | ~ 22px | ✓ 24px |
| Line 1 word for word | ✓ | ✓ | ✓ | ✓ | ✓ |
| Credits each start with a capital, “·” between | ✓ | ✓ | ✓ | ✓ (fixed during this review: see note) | ✓ |
| Credits one per line on phones, no visible “·” | ✓ | ✓ | ✓ | ✓ (first credit wraps over 2 lines) | ✓ |
| Back to top and Dark mode 44px tall and level | ✓ 44/44, level | ✓ | ✓ | ✓ | ✓ |
| Back to top → scrolls to 0 and focus to top | ✓ (focus to banner) | ✓ (`#view`) | ✓ | ✓ | ✓ |
| Footer text 12.5px, ≥ 4.5:1 light / dark | ✓ 5.0 / 6.0 | ✓ 5.2 / 7.4 | ~ 12px on phones; 5.9 / 7.2 | ~ 4.5–4.9 on the shaded band / 7.4 | ✓ 4.9 / 7.5 |
| Menu bar at 899, sidebar at 901 | n/a | ✓ | ✓ | ✓ | ✓ |
| Button: Lucide `menu` icon + word “Menu”, on the left | n/a | ✓ | ✓ | ✓ (extra `aria-label` “Open the menu”) | ✓ |
| Bar name: “Jemma’s *X*”, italic, links to the app’s home | n/a | ✓ `#home` | ✓ `#home` (fixed since round 1) | ✓ `#home` | ✓ `#/` |
| `aria-expanded` and `aria-controls` | n/a | ✓ | ✓ (fixed since round 1) | ✓ | ✓ |
| Closes on Escape → focus back to Menu | n/a | ✓ | ✓ (fixed since round 1) | ✓ | ✓ |
| Closes on scrim → focus back to Menu | n/a | ✓ | ✓ | **✗ focus lost to the page** | ✓ |
| Closes on choosing a link | n/a | ✓ | ✓ | ✓ | ✓ |
| Opening moves focus into the drawer | n/a | ~ the page’s link (“All Shelves”) | ~ Home | ~ “← Jemma’s Journals” | ~ “← Jemma’s Journals” |
| Closed drawer is inert (Tab never reaches it in 30 presses) | n/a | ✓ 0 | ✓ 0 | ✓ 0 | ✓ 0 |
| Page behind locked while open (wheel over the scrim doesn’t scroll) | n/a | ✓ | ✓ | ✓ | ✓ |
| Crossing 900 resets (open → 1000 wide → 390: closed, not expanded) | n/a | ✓ focus to Menu | ✓ focus to Menu | ✓ focus to Menu | ~ closed, but focus lost to the page |
| “← Jemma’s Journals” at the very top of the drawer and the wide sidebar | n/a | ✓ | ✓ | ✓ | ✓ |
| Back link reaches home (wide and from the drawer) | n/a | ✓ both | ✓ both | ✓ both | ✓ both |
| Home reaches each app | **✗ “Open …” still shows “This would open your …”** | | | | |

Since round 1, these are fixed: Sim World’s menu (Escape, `aria-expanded`, focus), Sim World’s bar name, the menu word and breakpoint everywhere, dark mode in every app, Travels’ tab icon and footers in Library and Pokédex.

---

## Broken

### 1. Home still can’t open the apps
- **Site:** home.
- **What:** under one address, all four back links land on Jemma’s Journals, but home’s “Open My …” links and photos are still `href="#"` and only show a message (“This would open your Sim World”). So the family only joins up in one direction.
- **Evidence:** `concepts/index.html` lines 288, 290 and 310–311. Clicking Open at `/` stays on `/`.
- **Fix:** give each entry in `PLACES` its address (`/sim-tracker/`, `/library/`, `/pokedex/`, `/travels/`, or whatever paths hosting gives them), use it as the `href`, and drop the `say(...)` message. This is still round 1’s item 1; it now stands out because everything else matches.

## Should fix

### 2. Library still loads two fonts from Google, under a footer that says “no tracking”
- **Site:** Library.
- **What:** Instrument Serif and Manrope come from `fonts.googleapis.com`. It was the only request off the site in the whole run. The new family footer promises “No cookies, no tracking, no ads” on the same page. The rules say that if a site isn’t true to line 1, she should be told rather than the words changed.
- **Evidence:** `HomeLibrary/site/index.html` lines 22–24. With Google blocked, Library falls back to other fonts; the other four sites don’t change.
- **Fix:** host the two `.woff2` files locally, as the other four already do (`Pokedex/site/fonts/` has them with the licence), and remove the three Google lines.

### 3. Three apps still have no robots tag
- **Sites:** Library, Sim World, Pokédex.
- **What:** home and Travels carry `<meta name="robots" content="noindex, noai, noimageai">`; the other three have none. This was her decision on 20 Nov (keep out of search engines and AI crawlers). Home’s `robots.txt` only covers the others if home ends up at the root of the address.
- **Fix:** add the same line to each `index.html` `<head>`.

### 4. Opening the menu puts focus in a different place on each site
- **Sites:** all four apps.
- **What:**
  - Library: the current page’s link (“All Shelves” on its home page).
  - Sim World: Home (her call 21 Nov: “one Enter shouldn’t leave the site”).
  - Pokédex and Travels: “← Jemma’s Journals”. A keyboard user who opens the menu and presses Enter leaves the site.
- **The rule:** it says “the first link in the drawer”, which Pokédex and Travels follow word for word. Her later call for Sim World is not in the rules page.
- **Fix:** take her Sim World call as the family rule and add it to `family-rules.md` (“focus to the current page’s link, or Home, never the back link”). Then change Pokédex (`js/app.js` 1405, `side.querySelector("a,input,button")`) and Travels (`js/app.js` 586, `$("#side a")`).

### 5. Pokédex: tapping the scrim loses focus
- **Site:** Pokédex.
- **What:** Escape returns focus to Menu, but a tap on the scrim leaves focus on the page body. The other three return it to Menu.
- **Why:** `setMenu` only refocuses when focus was inside the drawer (`wasIn`), and a click on the scrim has already moved focus out.
- **Evidence:** `Pokedex/site/js/app.js` 1401–1406 and 1409; measured focus after the scrim tap: `BODY`.
- **Fix:** let the scrim handler always return focus, as Library and Sim World do (`setMenu(false, true)`, focusing Menu whenever it closes on a narrow screen).

## Polish

### 6. Small differences in the dark-mode code
- **Sim World** only sets `data-mode` when dark. In light, `<html>` has no `data-mode`, even after Light mode is pressed. It works because its CSS only keys off `"dark"`, but the rule says set `"dark"` or `"light"`. Fix: set the attribute in both cases in the head script (`SimTracker/site/index.html` line 23) and in the toggle.
- **Pokédex** moves the old `jemmas-pokedex-mode` over but never deletes it; the other four remove theirs. Fix: add `localStorage.removeItem("jemmas-pokedex-mode")` to the head script (line 16).

### 7. Phone bars: same parts, different sizes
These are measured at 899 wide. The bar strip is `bars.png` in the scratchpad folder.

| | Menu button height | Name size | Name font |
|---|---|---|---|
| Library | 44px | 26px | Instrument Serif |
| Sim World | **41px** | 22px | Instrument Serif |
| Pokédex | **40px** | 22px | Instrument Serif |
| Travels | 44px | 30px | Instrument Serif |

Each button keeps its own skin, which is fine: Library italic serif on cloth, Sim World a boxed white button, Pokédex a pill, Travels a soft tint. But the tap height should be at least 44px everywhere, and a name size range of 22–30px is wider than it needs to be.

Pokédex alone adds `aria-label` “Open the menu” / “Close the menu” on top of the visible word “Menu” and `aria-expanded`. It is harmless, but screen readers then announce it differently from the other three.

### 8. What Tab reaches while the drawer is open
- **Pokédex:** keeps Tab inside the drawer. The Menu button itself can’t be reached, so Escape is the only keyboard way out.
- **Sim World:** cycles the drawer and Menu.
- **Library:** the drawer, Menu and the bar name. The page behind is inert.
- **Travels:** the drawer, Menu, the bar name and also the **skip link** (“Skip to the page”, which points into the inert page).

One shared pattern would be cleaner. My suggestion (not decided): Sim World’s, a loop of Menu plus the drawer.

### 9. Travels loses focus when the window crosses 900 with the drawer open
Other three: focus goes back to Menu. Travels: the drawer closes correctly, but focus drops to the page (`NARROW` change handler, `js/app.js` 591, calls `setMenu(false)` without refocusing).

### 10. The back link is still tiny
On wide sidebars “← Jemma’s Journals” is 10px text in a 14–18px tall link (Travels 11px, and sitting 10px lower than the others); in Library’s drawer it is 32px. It is meant to be subtle, so more padding is better than bigger text. Make it the same height everywhere (say 32px tall), and the same size and position in all four.

### 11. Footers: nearly the same, a few loose ends
- **A stray “·” where the credits wrap on the laptop (1600):**
  - **Home:** the credits wrap onto two lines and the second line *starts* with a “·” (`homefoot.png` in the scratchpad).
  - **Sim World:** the first line *ends* with a “·” before “Icons by …” wraps (`swfoot.png`).
  - The phone layout already hides the dots. The same guard is needed wherever the line can wrap: keep each “· credit” pair together (`white-space:nowrap` on the pair), or widen the column. Library and Travels fit on one line at 1600. Pokédex’s longer new icons credit now runs past 960px, so check it after its change.
- **Pokédex:**
  - The name is 22px; the other four are 24px.
  - Line 1 on its shaded footer band is about 4.5–4.9:1, right on the limit, against 5–6 elsewhere.
- **Sim World:** line 1 drops to 12px on phones (rule: 12.5px).
- **Visual weight:** it is close now (see `round2-footers.jpg`).
  - Each site has its own small divider, as the rule allows: Library a ❦ between rules, Sim World a pin on a dashed rule, Pokédex a red dashed rule, home its diamond end mark above the footer.
  - Travels has no divider but a 1px rule across the top, so it reads as a separate band.
  - Pokédex’s footer sits on a darker shaded strip, so it looks heavier.
  - Fine as personality; just so she knows.
- Home’s Back to top is a link (`<a href="#top">`); the apps use a `<button>`. It behaves the same.

### 12. Scrim strength differs
- **Library and Pokédex:** they dim the page clearly.
- **Sim World and Travels:** their scrims are very faint on the light pages. Travels’ pale drawer has no edge or shadow, so it barely separates from the page behind (`drawers.png` in the scratchpad).

A shared strength, about 40–50% of the site’s dark ink, would match them.

### 13. Focus rings
All five use a 2px solid ring in the site’s colour. Home’s sits 3px off; the apps’ sit 2px off. The colours:
- Library: brown on the page, brass in the sidebar.
- Sim World: gold, not its purple.
- Pokédex: red.
- Travels: sea green.

That is consistent enough. Sim World’s gold ring on lilac is the one that doesn’t look like its own site.

## Questions for her

### 14. Does Sim World’s name belong in gold?
Home, Library and Sim World all write the italic word in gold (and Pokédex in yellow). Sim World’s look is now purple, but the gold “*Sim World*” makes its header the nearest to home and Library at a glance.
- (a) Keep gold as the family thread.
- (b) Give Sim World its own purple for the word (and focus ring).

My suggestion (not decided): (b).

### 15. Do any two now look too alike?
Less than in round 1. Sim World’s lilac town plan and Travels’ pale green atlas are now clearly apart (`round2-family-laptop.jpg`, rows 3 and 5). Home and Library still share cream and gold, but home’s gold cloth cover and Library’s brown binding keep them distinct. In dark mode, home, Library and Pokédex all go to warm near-black. Their headers (gold cover, brown spine, red banner) still tell them apart. Nothing I’d change, but she may see it differently.

### 16. “Made with plain HTML and CSS” on Library and Pokédex
On her PC both use a small local server for editing (`/api/…`). Online they would be plain files, so line 1 stays true there. Per the rules, she should know; no change suggested.
