# Review: the five sites as one family (21 Nov 2026)

Read-only cross-site check of Jemma’s Journals (home), Library, Sim World, Pokédex and Travels. Nothing was changed in any project.

How: Edge via Sim World’s Playwright. All five served from disk under one pretend address, as they would be online: home at `/`, apps at `/library/`, `/sim-tracker/`, `/pokedex/`, `/travels/` (home wrapped in a doctype skeleton as `tests/check_page.js` does; Pokédex `/api/collection` from `data/collection/go.json`, other `/api` 503). Each home page at 1600 × 930 and 390 × 844, device light and dark; phone menus opened, closed with Escape and with a tap outside, then tabbed through; menu breakpoint found by resizing; each back link clicked. Sim World also opened as a local file (how her shortcut opens it). Only each site’s **home page** was checked for wording, so the spelling and apostrophe result covers those pages only.

Pictures: `family-laptop.jpg` and `family-phone.jpg` (this folder). Raw shots and numbers: `C:\Users\Jemma\AppData\Local\Temp\claude\9cff366c1b60a8f8\2df2d807-e7a9-4322-8b41-c4059cb2ba00\scratchpad\family\` (`shots\`, `measure.json`, scripts `fam.js`, `local.js`).

No page errors, and no sideways scrolling on any of the five at either size or in either mode.

## At a glance

| | Home | Library | Sim World | Pokédex | Travels |
|---|---|---|---|---|---|
| Tab title | Jemma’s Journals | Jemma’s Library (+ page name) | Jemma’s Sim World (+ page name) | Jemma’s Pokédex (never changes) | Jemma’s Travels (+ page name) |
| Tab icon | her drawn J’s, flips in dark | Lucide library, yellow on brown | plumbob PNGs | drawn from shapes, SVG + PNGs | **none** |
| theme-color | #8E6520, #6A4A17 after the Dark mode button | #3B2616 | #EEEAF2 light, #1B1524 dark | #7A1E2A | #ECF1EA |
| Name lockup | Jemma’s *Journals* (gold italic) | Jemma’s *Library* (gold italic) | Jemma’s *Sim World* (gold italic); **phone bar: plain, not italic, not a link** | Jemma’s *Pokédex* (yellow italic) | Jemma’s *Travels* (sea-green italic) |
| Back link | none (it is home) | “← JEMMA’S JOURNALS”, top of sidebar, Manrope 10px caps | same | same | same, 11px |
| Back link on a phone | n/a | inside the drawer only | inside the drawer only | inside the drawer only | **always visible**, above the name |
| Back link goes to (online) | n/a | `/` → home ✓ | `/` → home ✓ | `/` → home ✓ | `/` → home ✓ |
| Back link goes to (her PC) | n/a | `/` = Library’s own start (port 8020) | home’s local file ✓ | `/` = Pokédex’s own start (port 8030) | `/` = Travels’ own start |
| Home’s “Open” links | “This would open your …” message, no address | | | | |
| Phone menu from | no menu (single page) | ≤ 900px | ≤ 900px | ≤ 900px | **≤ 820px** |
| Menu button | | “Shelves”, left | “Worlds”, left | “Menu”, left | **icon only**, after the name |
| Escape closes | | yes | **no** | yes | yes |
| Tap outside closes | | yes | yes | yes | yes |
| aria-expanded | | yes | **no** | yes | yes |
| Focus on opening | | first shelf link | stays on button | back link, kept inside the drawer | stays on button |
| Dark mode | opens light always; footer button, remembered | follows the device, no button | follows the device, no button | follows the device, no button | **none** |
| Fonts | Instrument Serif + Manrope, local | Instrument Serif + Manrope **from Google**, EB Garamond local | local | local | local |
| Footer / credits | About this site + all credits | **none** | credits + “as of” dates | **none** | “No cookies…” + credits |
| Skip link | yes | yes | **no** | **no** | yes |
| Focus ring | 2px solid, gold | 2px solid, gold | 2px solid, gold | 2px solid, red | 2px solid, sea green |
| Placeholders | italic + dashed PLACEHOLDER tag | (missing = blank) | empty boxes for missing portraits | n/a | italic + dashed Placeholder tag (same as home) |
| noindex / noai | yes | **no** | **no** | **no** | yes |
| Repo → GitHub Pages path | `jemmas-journals` → `/jemmas-journals/` | `library` → `/library/` | `sim-tracker` → `/sim-tracker/` | `pokedex` → `/pokedex/` | `jemmas-travels` → `/jemmas-travels/` |
| British English, curly ’ | ✓ | ✓ | ✓ | ✓ | ✓ |

---

## Broken

### 1. On her PC there is no way round the family
- **Sites:** all.
- **What:** Home’s “Open My …” links go nowhere yet (they show “This would open your Sim World”). Library, Pokédex and Travels are served from the root of their own local servers, so their “← Jemma’s Journals” (`href="/"`) just reloads the app itself. Only Sim World (opened as a file) reaches home, through its `HOME_LOCAL` rule.
- **Evidence:** home `concepts/index.html` lines 288–312 (`href="#"`, `say('This would open your …')`); clicking Open on the local file leaves the page where it is. Back links measured `href="/"` in all four; Sim World as `file:` rewrites to `../../JemmasJournals/concepts/index.html`.
- **Online:** fine. Served under one address, all four back links landed on Jemma’s Journals.
- **Fix:** put each app’s address in home’s `PLACES` now (`"/library/"` etc.), so it works the moment they’re online, and drop the “would open” message. For her PC there is no neat fix while each app has its own port (a web page can’t open a `file:` link). Options for her: (a) accept that the round trip only works online; (b) let one of the local servers (e.g. Library’s `serve.py`) also serve the home page and point the back links there when on `localhost`. My suggestion (not decided): (a), plus the `PLACES` addresses.

## Should fix

### 2. Sim World’s phone menu doesn’t close with Escape and doesn’t say if it’s open
- **Site:** Sim World (the menu the others were copied from).
- **What:** the Worlds button only toggles a class. Escape does nothing, there is no `aria-expanded`/`aria-controls`, and focus stays on the button while the whole page behind stays reachable by Tab (25 of 25 Tab presses landed outside the drawer).
- **Evidence:** `site/js/app.js` 1542–1543; after Escape the drawer was still at x = 0.
- **Fix:** do what Library and Pokédex do (their `setMenu`): Escape closes and returns focus to the button, `aria-expanded` follows, focus moves into the drawer on opening.

### 3. Travels has no dark mode
- **Site:** Travels.
- **What:** with the device in dark, Library, Sim World and Pokédex turn dark; Travels stays light (no `prefers-color-scheme` rules at all). Home also stays light, but by her choice and it has a button.
- **Evidence:** `family-laptop.jpg` / `family-phone.jpg`, bottom row.
- **Fix:** give Travels a dark set of its tokens like the others (or make it a decision: see question 13).

### 4. Travels has no tab icon
- **Site:** Travels.
- **What:** no `<link rel="icon">`, so the browser’s blank page icon shows; the other four each have their own.
- **Fix:** an icon in its own colours, made from Lucide like the others (shown to her first).

### 5. Library loads two fonts from Google
- **Site:** Library.
- **What:** Instrument Serif and Manrope come from `fonts.googleapis.com`; the other four (and Library’s own EB Garamond) are local. It means a request to Google on every visit, a slower first paint, and the family can’t say “no tracking” everywhere.
- **Evidence:** `HomeLibrary/site/index.html` lines 18–20.
- **Fix:** copy the same `.woff2` files and `@font-face` lines the others use (`Pokedex/site/fonts/` has them, with the licences).

### 6. The back link assumes home is at the address’s root
- **Sites:** all four apps; home.
- **What:** `href="/"` only works if the home page is the root of the address. With GitHub Pages and today’s repo names, home would be at `/jemmas-journals/` (unless the repo is the account’s own `jemmathornton.github.io`, or a custom domain is set on it), so every back link would 404. Repo names also set the app paths: Travels would be `/jemmas-travels/`, Sim World `/sim-tracker/`.
- **Evidence:** `git remote` of each project; `research/going-online.md`.
- **Fix:** when hosting is picked, put home in the root repo (or her domain) and choose the app paths; then set them once in home’s `PLACES` (see 1). No change to the back links needed if home is at the root.

### 7. Pokédex’s phone banner line runs over the maps
- **Site:** Pokédex (found in passing).
- **What:** at 390 wide the small caps line “POKÉMON GO · 1,014 POKÉMON OUT, PLUS THEIR FORMS” wraps onto the region maps and is cut off at the right; grey on busy pictures, hard to read.
- **Evidence:** `shots\pokedex-phone-light.png` (top).
- **Fix:** on phones put the map strip behind the totals only, or give the line a solid band.

## Polish

### 8. The way home on a phone is in two different places
- Library, Sim World, Pokédex: inside the drawer (you open the menu to go home). Travels: always visible above the name, on its own line. Either is fine; pick one for all. My suggestion (not decided): inside the drawer, as three apps already do; it keeps the phone bar to one line.

### 9. Phone menu buttons differ more than they need to
- Labels: “Shelves”, “Worlds”, “Menu”, and an unlabelled icon in Travels. Position: left edge in three; in Travels after the name (x = 168 of 390), though its notes say she asked for it on the left. A themed word is nice personality; an icon with no word is the odd one out. See question 12.
- Breakpoint: 900px in three, 820px in Travels (between 821 and 900 Travels still shows its sidebar while the others show the bar).
- Focus on opening: Library first shelf, Pokédex the back link (and keeps focus inside the drawer), Sim World and Travels leave it on the button and let Tab wander behind. Pokédex’s is the best to copy.

### 10. Sim World’s phone bar name isn’t the lockup
- Every other bar shows “Jemma’s *X*” with the italic coloured word and links to the app’s home; Sim World’s is plain `<b>Jemma’s Sim World</b>`, not italic, not a link (`site/index.html` line 22). `bars.jpg` in the scratchpad shows the four bars stacked.

### 11. Smaller gaps between the apps
- **noindex/noai:** only home and Travels have the robots tag. Add `<meta name="robots" content="noindex, noai, noimageai">` to Library, Sim World and Pokédex before going online (home’s `robots.txt` covers AI crawlers for all of them only if home is at the root, see 6).
- **Credits:** Library and Pokédex have no footer at all; Sim World and Travels credit their maps, fonts and icons; home credits everything. Before going online: a short credits line in each (covers from their publishers; game pictures, Lucide, fonts).
- **Skip link:** Sim World and Pokédex have none; the other three do.
- **Pokédex tab title** never changes (“Jemma’s Pokédex” on every page); the other apps add the page name.
- **Back link size:** 10px text and 14–18px tall in the sidebars (Library 32px on phones). Hard to tap; it was asked to be subtle, but a little more height (padding, not bigger text) would help.
- **Pokédex** calls `/api/collection` and `/api/tick` from the address root; Library uses relative `api/…`. Online under `/pokedex/` it would ask the wrong place (it should not ask at all off her PC: `research/going-online.md`).
- **Sim World’s local back link** opens home’s `concepts/index.html`, which is a body fragment: it renders in quirks mode with no viewport tag. Fine on the laptop (checked), wrong on a phone. Only matters until it’s online.

## Questions for her

### 12. Same menu word everywhere, or each app’s own?
Options: (a) keep each app’s word (Shelves, Worlds, Menu) and give Travels one (e.g. “Trips”); (b) “Menu” in all four; (c) icon only in all four. My suggestion (not decided): (a).

### 13. Dark mode across the family
Now: home opens light whatever the device says and has a Dark mode button; the apps follow the device and have no button; Travels has none. On a phone set to dark she goes light (home) → dark (app) → light (Travels). Options: (a) leave it: home is her chosen exception; (b) all five open light, each with the same button; (c) all five follow the device, home included. Note: once they share one address, one saved setting (home already saves `jj-…`) could carry her choice to every app, and the apps’ CSS already listens for `data-theme`.

### 14. Do Sim World and Travels look too alike?
On the laptop (`family-laptop.jpg`) they are the closest pair: pale sidebar with a faint grid, pale paper, a wide plan/map banner, a white row of figures. Colours keep them apart (lilac and gold vs pale green and sea green). Home and Library share cream and gold, but Library’s dark brown binding and home’s gold cover keep them clearly different. Also four of five put the italic word in gold (Journals, Library, Sim World, Pokédex in yellow); Travels in green. That can stay as the family thread, or Sim World could take its purple for the word.

### 15. “My …” on home, “Jemma’s …” in the apps
Home calls them My Sim World, My Library, My Pokédex, My Travels (her pick, 20 Nov); each app is titled Jemma’s *X*. It reads as her voice on home and the site name in the app, so nothing to fix; just check she’s happy. Home’s description lines for Sim World and Library are word for word from those apps’ own pages; Pokédex and Travels are marked placeholders.
