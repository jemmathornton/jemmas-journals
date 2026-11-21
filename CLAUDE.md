# Jemma’s Journals

The home page that links Jemma’s other sites: her Sims 4 save (`Documents\SimTracker`, “My Sim World”), her home library (`Documents\HomeLibrary`, “My Library”) and her Pokémon GO collection (`Documents\Pokedex`, “My Pokédex”) and her travel blog (`Documents\Travels`, “My Travels”, added 21 Nov with her yes). Not her Budget app. Started 19 Nov 2026. Public, but not advertised: it’s mostly for her, to reach everything from her phone or laptop. More places will be added, so the page must grow by adding one entry.

## Working rules (as for her other apps)

- **Home is a landing space only:** a name, a picture and a way in for each place, plus an Introduction. No figures, no “latest”, no dates. It must read like a website (header, sections, footer), not a screen of app icons.
- **Never edit Jemma’s own files without asking** (Downloads, Documents, Pictures, her other projects). Copy into this project and work on the copy.
- **British English**; **curly apostrophes** in shown text.
- **No made-up text on the site:** her words, or an app’s own text word for word. Missing means a marked placeholder. Labels like “Contents” or “Open …” are fine.
- **No AI-generated art.** Pictures come from her apps (maps by 20th Century Plumbob, the games’ region maps, publishers’ covers, her own screenshots). Icons: Lucide, or the sets her apps use; never a real logo.
- **Show, don’t ask, for looks:** build each option into the running page or app (a trial switch, bottom right, added only while she is choosing and removed after) and **open it in the browser pane for her to click through** (her ask, 21 Nov: screenshots in chat are blurry and comparison pages are harder to check). Screenshots at 1600 and phone size only as a record. Words are fine for facts.
- **When asking her to choose, list every option** in the message (the two-button box hides choices).
- **Label suggestions** as “my suggestion (not decided)”.
- **Light mode by default** (her preference, 20 Nov): dark only when the button is pressed.
- Short, plain answers. When she’s away for hours, keep working through checks, research and small fixes in one turn.

## Her decisions so far

- Cloth-cover banner with the title on a cream label; no elastic-band stripe. **Cover colour: old gold** (#8E6520, cream trim; dark #6A4A17), her pick 20 Nov evening, replacing navy (too cool). Share picture retaken from the gold banner (img/share-preview.jpg, 1200×630, 86 KB).
- Places as photos in album corners, named “My Sim World”, “My Library”, “My Pokédex”, nothing above the names.
- Only the photo and “Open …” are links (not the whole card).
- Library’s picture: the tilted wall of her covers. Sim World and Pokédex: a full map, nothing added on top. Which ones is open: she’ll supply a Sims picture; Pokédex now uses the combined Johto and Kanto painting (official HeartGold/SoulSilver art, from PidgiWiki `File:Johto_and_Kanto_-_Pokemon_HeartGold_and_SoulSilver.jpg`, downloaded 20 Nov with her OK).
- No “Elsewhere” links (the Sims Gallery belongs in Sim World).
- 20 Nov: the Improved version (gold corner brackets on the cover, serif section headings with a diamond rule, centred footer, Back to top), with About this site in the footer. (Its About photo was later dropped: see “Introduction” below.) Not wanted: quick links, an empty slot, an edition mark.
- 20 Nov (later): links say “Open My Sim World” etc. (she found “Open Sim World” odd beside “My Sim World”). About this site must be small and subtle (she hated the table-like band). A way back home in each app: **A**, a small “← Jemma’s Journals” link at the top of each app’s sidebar (subtle). **Added 20 Nov evening** (her go-ahead) to all three apps (Sim World 1201ff9, Library f852f84, Pokédex f7d00a3): href "/" (home once all sites share one address; she leans to her own domain, hosting undecided, separate repos, no submodules). Sim World opened as a local file points at ../../JemmasJournals/concepts/index.html instead. Screens: for-jemma/concepts/back-home/back-home-added.jpg.

- 20 Nov (evening): **About this site = option 2**, two lines (No cookies… / the credits), each credit with a capital; on phones the credits stack one per line. The other footer options are gone from the switch.
- 20 Nov (evening): Pokédex picture = the combined Johto and Kanto painting (downloaded from PidgiWiki with her OK; page copies img/maps/region-johto-kanto.*). Shown whole for now; whole vs fill the photo is her choice.
- 20 Nov (evening): **keep out of search engines and AI crawlers**: robots meta (noindex, noai, noimageai) on the pages and concepts/robots.txt. Going online: later.
- 20 Nov (evening): page ideas: **stitching on the cover, yes** (always on now); **paper and tilted photos, no** (removed). Bookmark ribbon (as a link): no, removed. Title on scroll: no, removed. Red ribbon: removed (her pick). **Gentle entrance: yes** (plays once as the page opens; skipped for reduced motion). The Ideas row is gone from the switch.
- 20 Nov (evening): pictures parked again: she will change them later (Pokédex whole-vs-fill not decided).
- 20 Nov (late): the top section is an **Introduction** to the site (her pick; was “About me”), words only, no photo, lined up with Contents.
- 20 Nov (late): **dark mode button moved to the footer**, level with Back to top (both kept; header clean).
- 20 Nov (evening): dark mode: opens light; the footer’s Dark mode button switches and is remembered. Dark **swaps colours consistently** (her ask): page and title label the same warm black (#29221B), photo mats deeper warm black (#0D0A07) so photos stand out, photo corners cream.
- 20 Nov (evening): **tab icon is her own design**, drawn in `concepts/tools/draw-icon.html` (redrawn simpler 20 Nov late): cream square, old gold book outline, warm black upright J in front with a cream gap, old gold slanted J just lower right; no corners. **Light icon is the default**; in dark mode the page swaps to a flipped version (img/icon/icon-dark-*: warm black square, cream J, bright gold book and slanted J), her rule 20 Nov. Files in `concepts/img/icon/` and `concepts/favicon.ico`, linked from the page. For looks she can’t describe, offer her that canvas rather than more guesses.

- 21 Nov: **My Travels added** (her yes). Picture: Travels’ own world map in its chosen Old Atlas look (`img/maps/travels-map.*`, from its Map page, redone 21 Nov). Its line is a placeholder. Four places sit 2 × 2; the checks now expect four. Screen: for-jemma/concepts/travels-added.jpg.

- 21 Nov: **the family rules** (her decision): dark mode the same on every site and carried across (all open light; footer Dark mode button; shared localStorage key `jj-mode`), the same footer, the same Menu drawer under 900px. Written in `research/family-rules.md`; home now uses `jj-mode`. Sim World and Travels: she is fixing those herself.

## The apps’ own styles (21 Nov)

She felt the three apps were too same-y (same sidebar, name style, hero, cards; only colour differs). Mock-ups (pictures only, apps unchanged) in `for-jemma/concepts/app-styles/`, compared with `compare.html` (launch config `app-styles`, port 8043); the CSS is in `research/app-styles/`.
- **Library: L1 · Bound book**, as mocked, no notes (cloth-bound sidebar with gilt rules, paper pages with a gutter, title-page banner with a plate of covers, ornaments, book-face reading text; needs EB Garamond). Also gives the Library a phone layout (sidebar as a top band).
- **Sim World: S1 · Map** is the direction, not final: grid/contour lines only on the sidebar and banner, plain paper behind the cards. Variants S1a–S1d mocked; she liked S1c’s home but not the repeated colour on neighbourhood pages, and Sim World must not look like her new Travels site (world maps, pale blue/green, atlas frames, airmail, postcards, parchment). Then S1e and S1f (town plan). **She picked S1f · Town plan, purple**, but its neighbourhood lot cards must match the home cards: **she picked S1f-a (lot cards in the world colour)**, with the town plan paler over map banners (overlay 18%). Try it live: launch config `simworld-trial` (`tools/trial_server.py`, port 8044) runs her real Sim World with a Try switch; her files are only read. CSS: research/app-styles/simworld/s1fa.css.
- **Pokédex: a mix**: P1’s collector’s cards (Pokémon, regions, other cards) + P2’s binder gap between sidebar and page (no metal rings/silver) + P2’s index tabs hanging from the banner. She picked **P3 · Cards in a binder**; P3b removes the stitching that crossed the sidebar items (her note). **Confirmed P3b**, with the shiny art window softer (same pastel rainbow, fainter, no stripes; shiny = Shiny box ticked). Card colour = the region colour of the page (REGION_COLOURS in the Pokédex’s app.js).
- **Built into the real apps 21 Nov** (her go-ahead): Library c88a065 (laptop; its own session builds the phone mode), Sim World 978bcd6 + review fixes 926993a, Pokédex 77e18f2 (with a Menu drawer under 900px) + review fixes 1d12ed6.
- 21 Nov: full critical review of all five sites (incl. Travels) and the family: `research/reviews/`; summary and her open questions: `for-jemma/review-21-nov.md`.

## Where things are

- `concepts/index.html`: the page as it stands; the trial switch was removed 20 Nov late (her ask). Stand-in places for checking growth: add `#more1`…`#more3` to the address. The places are one list, `PLACES`, in its script. Published for her phone as a private Claude artifact: https://claude.ai/artifact/Ad37As365K3HDcR8iHw7HE (republish after changes).
- `concepts/img/`: pictures copied from her apps (`maps/` every Sims world and Pokémon region map, `wall/` 40 of her covers, `icons/` each app’s own icon). `concepts/fonts/`: Instrument Serif and Manrope (SIL OFL).
- `for-jemma/concepts/`: screenshots of each round and the labelled choice sheets (older rounds in `round-1/` …).
- `research/going-online.md`: hosting research (GitHub Pages and what each app needs, checked in each app’s code).
- `research/site-ideas.md`: ideas to make the site better, what was tried on the page, a checklist for going online. `research/drafts/`: draft head tags, robots.txt, manifest and a publishing workflow, for going online (the robots and noindex choices are made and already on the page; `concepts/robots.txt` is the live copy).
- `concepts/404.html` (not-found page) and `concepts/img/share-preview.jpg` (link preview picture), for when it’s online. Pictures on the page are WebP at the size shown (`img/wall/*.webp`, `img/maps/*.webp`); the JPGs are the larger originals.
- `tests/check_page.js`: checks the page in Edge at 1600, 1280 and 390 wide (run with `C:/Users/Jemma/Documents/SimTracker/.tools/node/node.exe tests/check_page.js`; uses Sim World’s Playwright). Run after every change.

## Git

Repo on `main`, pushed to https://github.com/jemmathornton/jemmas-journals (**public**). Commit after each piece of work and push with `git -c "credential.helper=!'C:/Program Files/GitHub CLI/gh.exe' auth git-credential" push`. Name and email are set in this repo’s own git config (copied from her Library project).

## Her picks after the second review (21 Nov, late)

Answers in `for-jemma/review-2-21-nov.md`. All built and the Try switches removed:
- **Home:** the four places span the full width, lined up with the headings.
- **All sites:** footer line 1 “Made with HTML, CSS and JavaScript, kept on GitHub.” (family rule updated).
- **Sim World:** town-plan look on lot, Sim and household pages; “Sim World” in the sidebar purple.
- **Library:** Display shelf walnut brown (was green); big first letter kept after a quote mark; EB Garamond shrunk to WOFF2; read-only without its server. The Library’s “no green” line was removed at her ask (not a rule to keep).
- **Pokédex:** card art tinted by the first type; Lucky box stays white; tabs one row at 1280 (8.5px floor); Hide off on opening; search ignores Hide; 32px under the chips on Pokémon pages.
- **Travels:** Favourite month removed; neutral wording; distance on trip pages; phone-writing options in its `research/write-from-phone.md`.
