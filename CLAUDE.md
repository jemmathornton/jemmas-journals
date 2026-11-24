# Jemma’s Journals

The home page that links Jemma’s other sites: her Sims 4 save (`Documents\JemmasJournals\sim-world`, “My Sim World”), her home library (`Documents\JemmasJournals\library`, “My Library”) and her Pokémon GO collection (`Documents\JemmasJournals\pokedex`, “My Pokédex”) and her travel blog (`Documents\JemmasJournals\travels`, “My Travels”, added 21 Nov with her yes). Not her Budget app. Started 19 Nov 2026. Public, but not advertised: it’s mostly for her, to reach everything from her phone or laptop. More places will be added, so the page must grow by adding one entry.

**How the parts connect** (parent and submodules, shared code, servers, backup, build, tests): [ARCHITECTURE.md](ARCHITECTURE.md). Before changing anything across the family, follow “Making a change across the family” below. Slash commands for common jobs: `/status`, `/check-all`, `/record`, `/family-change`, `/new-site` (in `.claude/commands/`).

## Working rules (as for her other apps)

- **Home is a landing space only:** a name, a picture and a way in for each place, plus an Introduction. No figures, no “latest”, no dates. It must read like a website (header, sections, footer), not a screen of app icons.
- **Never edit Jemma’s own files without asking** (Downloads, Documents, Pictures, her other projects). Copy into this project and work on the copy.
- **British English**; **curly apostrophes** in shown text.
- **No made-up text on the site:** her words, or an app’s own text word for word. Missing means a marked placeholder. Labels like “Contents” or “Open …” are fine.
- **No AI-generated art.** Pictures come from her apps (Sims maps by filipesims, and 20th Century Plumbob for the worlds filipesims hasn't made (her pick, 23 Nov; see Sim World's notes), the games’ region maps, publishers’ covers, her own screenshots). Icons: Lucide, or the sets her apps use; never a real logo.
- **Show, don’t ask, for looks:** build each option into the running page or app (a trial switch, bottom right, added only while she is choosing and removed after) and **open it in the browser pane for her to click through** (her ask, 21 Nov: screenshots in chat are blurry and comparison pages are harder to check). Screenshots at 1600 and phone size only as a record. Words are fine for facts.
- **When asking her to choose, list every option** in the message (the two-button box hides choices).
- **Label suggestions** as “my suggestion (not decided)”.
- **Light mode by default** (her preference, 20 Nov): dark only when the button is pressed.
- Short, plain answers. When she’s away for hours, keep working through checks, research and small fixes in one turn.

## Her decisions so far

- Cloth-cover banner with the title on a cream label; no elastic-band stripe. **Cover colour: old gold** (#8E6520, cream trim; dark #6A4A17), her pick 20 Nov evening, replacing navy (too cool). Share picture retaken from the gold banner (img/share-preview.jpg, 1200×630, 86 KB).
- Places as photos in album corners, named “My Sim World”, “My Library”, “My Pokédex”, nothing above the names.
- **Only “Open …” is a link** (her decision, 22 Nov, replacing 20 Nov’s “the photo and Open …”): the picture is a plain element, not a link, not focusable, no pointer and no change on hover.
- Library’s picture: the tilted wall of her covers. Sim World and Pokédex: a full map, nothing added on top. Which ones is open: she’ll supply a Sims picture; Pokédex now uses the combined Johto and Kanto painting (official HeartGold/SoulSilver art, from PidgiWiki `File:Johto_and_Kanto_-_Pokemon_HeartGold_and_SoulSilver.jpg`, downloaded 20 Nov with her OK).
- No “Elsewhere” links (the Sims Gallery belongs in Sim World).
- 20 Nov: the Improved version (gold corner brackets on the cover, serif section headings with a diamond rule, centred footer, Back to top), with About this site in the footer. (Its About photo was later dropped: see “Introduction” below.) Not wanted: quick links, an empty slot, an edition mark.
- 20 Nov (later): links say “Open My Sim World” etc. (she found “Open Sim World” odd beside “My Sim World”). About this site must be small and subtle (she hated the table-like band). A way back home in each app: **A**, a small “← Jemma’s Journals” link at the top of each app’s sidebar (subtle). **Added 20 Nov evening** (her go-ahead) to all three apps (Sim World 1201ff9, Library f852f84, Pokédex f7d00a3): href "/" (home once all sites share one address; she leans to her own domain, hosting undecided; at the time separate repos, no submodules: since 21 Nov late they are submodules, see “The family layout”). Sim World opened as a local file points at ../../site/index.html instead (was ../../JemmasJournals/site/index.html before the move; updated 22 Nov). Screens: for-jemma/concepts/back-home/back-home-added.jpg.

- 20 Nov (evening): **About this site = option 2**, two lines (No cookies… / the credits), each credit with a capital; on phones the credits stack one per line. The other footer options are gone from the switch.
- 20 Nov (evening): Pokédex picture = the combined Johto and Kanto painting (downloaded from PidgiWiki with her OK; page copies img/maps/region-johto-kanto.*). Shown whole for now; whole vs fill the photo is her choice.
- 20 Nov (evening): **keep out of search engines and AI crawlers**: robots meta (noindex, noai, noimageai) on the pages and site/robots.txt. Going online: later.
- 20 Nov (evening): page ideas: **stitching on the cover, yes** (always on now); **paper and tilted photos, no** (removed). Bookmark ribbon (as a link): no, removed. Title on scroll: no, removed. Red ribbon: removed (her pick). **Gentle entrance: yes** (plays once as the page opens; skipped for reduced motion). The Ideas row is gone from the switch.
- 20 Nov (evening): pictures parked again: she will change them later (Pokédex whole-vs-fill not decided).
- 20 Nov (late): the top section is an **Introduction** to the site (her pick; was “About me”), words only, no photo, lined up with Contents.
- 20 Nov (late): **dark mode button moved to the footer**, level with Back to top (both kept; header clean).
- 20 Nov (evening): dark mode: opens light; the footer’s Dark mode button switches and is remembered. Dark **swaps colours consistently** (her ask): page and title label the same warm black (#29221B), photo mats deeper warm black (#0D0A07) so photos stand out, photo corners cream.
- 20 Nov (evening): **tab icon is her own design**, drawn in `site/tools/draw-icon.html` (redrawn simpler 20 Nov late): cream square, old gold book outline, warm black upright J in front with a cream gap, old gold slanted J just lower right; no corners. **Light icon is the default**; in dark mode the page swaps to a flipped version (img/icon/icon-dark-*: warm black square, cream J, bright gold book and slanted J), her rule 20 Nov. Files in `site/img/icon/` and `site/favicon.ico`, linked from the page. For looks she can’t describe, offer her that canvas rather than more guesses.

- 21 Nov: **My Travels added** (her yes). Picture: Travels’ own world map in its chosen Old Atlas look (`img/maps/travels-map.*`, from its Map page, redone 21 Nov). Its line is a placeholder. Four places sit 2 × 2; the checks now expect four. Screen: for-jemma/concepts/travels-added.jpg.

- 21 Nov: **the family rules** (her decision): dark mode the same on every site and carried across (all open light; footer Dark mode button; shared localStorage key `jj-mode`), the same footer, the same Menu drawer under 900px. Written in `research/family-rules.md`; home now uses `jj-mode`. Sim World and Travels: she is fixing those herself. (22 Nov: done; every site now loads the one shared copy in `site/family/`.)

## The apps’ own styles (21 Nov)

She felt the three apps were too same-y (same sidebar, name style, hero, cards; only colour differs). Mock-ups (pictures only, apps unchanged) in `for-jemma/concepts/app-styles/`, compared with `compare.html` (launch config `app-styles`, port 8043); the CSS is in `research/app-styles/`.
- **Library: L1 · Bound book**, as mocked, no notes (cloth-bound sidebar with gilt rules, paper pages with a gutter, title-page banner with a plate of covers, ornaments, book-face reading text; needs EB Garamond). Also gives the Library a phone layout (sidebar as a top band).
- **Sim World: S1 · Map** is the direction, not final: grid/contour lines only on the sidebar and banner, plain paper behind the cards. Variants S1a–S1d mocked; she liked S1c’s home but not the repeated colour on neighbourhood pages, and Sim World must not look like her new Travels site (world maps, pale blue/green, atlas frames, airmail, postcards, parchment). Then S1e and S1f (town plan). **She picked S1f · Town plan, purple**, but its neighbourhood lot cards must match the home cards: **she picked S1f-a (lot cards in the world colour)**, with the town plan paler over map banners (overlay 18%). (The live try-out server used then, `tools/trial_server.py`, was removed 22 Nov: options are now built into the apps themselves.) CSS: research/app-styles/simworld/s1fa.css.
- **Pokédex: a mix**: P1’s collector’s cards (Pokémon, regions, other cards) + P2’s binder gap between sidebar and page (no metal rings/silver) + P2’s index tabs hanging from the banner. She picked **P3 · Cards in a binder**; P3b removes the stitching that crossed the sidebar items (her note). **Confirmed P3b**, with the shiny art window softer (same pastel rainbow, fainter, no stripes; shiny = Shiny box ticked). Card colour = the region colour of the page (REGION_COLOURS in the Pokédex’s app.js).
- **Built into the real apps 21 Nov** (her go-ahead): Library c88a065 (laptop; its own session builds the phone mode), Sim World 978bcd6 + review fixes 926993a, Pokédex 77e18f2 (with a Menu drawer under 900px) + review fixes 1d12ed6.
- 21 Nov: full critical review of all five sites (incl. Travels) and the family: `research/reviews/`; summary and her open questions: `for-jemma/review-21-nov.md`.

## Home: journals and landscape pictures (22 Nov, her picks)

She felt home was “a bit bland, needs more” and the four pictures didn’t sit together. From a Try switch of pictures (As now / Same frame / Site previews / Tinted) and layouts (As now / Journals / Feature / Side by side / Index) **she picked Journals, with no numbers on the journals, and every picture the same landscape shape** (22 Nov). Built and the other options removed.
- **Journals:** each place is a cloth-bound journal in its colour (spine, stitching, a page edge), its picture a plate with album corners, its name on a cream label overlapping the plate like the banner’s, its line and “Open …” in cream. Four to a row on a laptop, two below 1200px, one on phones; more places wrap centred (seven = 4 + 3).
- **Pictures:** one shared shape, 2:1 (close to the Travels and Pokédex maps, ~2.3:1). `site/img/home/frame-*.webp`: Willow Creek cropped to its lots (filipesims’ map since 23 Nov, her yes; same crop as before: full width, 15.7% to 86.8% down, made from `sim-world/site/maps/willow-creek.jpg` at 1000 × 500; the footer credit says “World maps by filipesims and 20th Century Plumbob”, the same as Sim World’s, her go-ahead 24 Nov), the whole Johto–Kanto painting, the Travels map trimmed at the edges; the Library’s wall of covers fills the same plate.
- **Extras dropped** (22 Nov, she wasn’t sold): no drop capital, no colour bars, plain “Open …”.
- **Journals chosen** (22 Nov): after trying Notebooks, Album and Field notes she kept the cloth journals; the other styles were removed.
- **Rejected 22 Nov, don’t offer again:** the journal styles Notebooks, Album and Field notes; the page looks Gallery (pale cool page, sans headings, flat gold band), Desk (blue-grey backdrop, slim strip) and Bold (big title on white, no banner) (“way worse”). The page stays as it was (cream page, cloth banner with the cream label, serif headings with diamond rules) with the journals; no Try switch on the page now.
- **Photo corners and mat (22 Nov):** the original black album corners, a little softer (warm near-black #4A423A to #342D27; in dark the cream corners softened the same way), on the original plain flat mat. Rejected 22 Nov, don’t offer again: Gold, Cream, Clear, Brackets, None, Frosted and Smoky corners; the Soft and Deep mats. No Try switch on the page.
- **Open:** the overall look (she feels the page is too like the Library). No option is being shown; ask her before building anything.
- Screens: `for-jemma/concepts/home-options/` (the first round), `home-options/chosen/` (journals as built) `home-options/styles/` (the four styles) and `home-options/page-looks/` (the four page looks at 1600, dark, 1000, 390 and with seven places).

## Where things are

- `site/index.html`: the page as it stands; the trial switch was removed 20 Nov late (her ask). Stand-in places for checking growth: add `#more1`…`#more3` to the address. The places are one list, `PLACES`, in `site/home.js` (moved out of the page 22 Nov for the Content Security Policy). Published for her phone as a private Claude artifact: https://claude.ai/artifact/Ad37As365K3HDcR8iHw7HE (republish after changes).
- `site/img/`: pictures copied from her apps (`maps/` every Sims world and Pokémon region map, `wall/` 40 of her covers, `icons/` each app’s own icon). `site/fonts/`: Instrument Serif and Manrope (SIL OFL).
- `for-jemma/concepts/`: screenshots of each round and the labelled choice sheets (older rounds in `round-1/` …).
- `research/going-online.md`: hosting research (GitHub Pages and what each app needs, checked in each app’s code).
- `research/site-ideas.md`: ideas to make the site better, what was tried on the page, a checklist for going online. `research/drafts/`: draft head tags, robots.txt, manifest and a publishing workflow, for going online (the robots and noindex choices are made and already on the page; `site/robots.txt` is the live copy).
- `site/404.html` (not-found page) and `site/img/share-preview.jpg` (link preview picture), for when it’s online. Pictures on the page are WebP at the size shown (`img/wall/*.webp`, `img/maps/*.webp`); the JPGs are the larger originals.
- `tests/check_page.js`: checks the page in Edge at 1600, 1280, 1000 and 390 wide (run with `C:/Users/Jemma/Documents/JemmasJournals/.tools/node/node.exe tests/check_page.js`; uses the shared Playwright in node_modules/). Run after every change.

## Git

Repo on `main`, pushed to https://github.com/jemmathornton/jemmas-journals (**public**). Commit after each piece of work and push with `git -c "credential.helper=!'C:/Program Files/GitHub CLI/gh.exe' auth git-credential" push`. Name and email are set in this repo’s own git config (copied from her Library project).

## Making a change across the family (checklist for Claude sessions, 22 Nov)

1. **Is it quiet?** Other sessions work in the parent and in each app. Run `git status` and `git log --oneline -5` in the parent and in the app you’ll touch (or `/status`). If there are uncommitted changes you didn’t make, or a commit in the last few minutes, leave those files alone and commit only your own (`git add <your files>`, never `git add -A`).
2. **Where the code goes:** shared behaviour (dark mode, footer, Back to top, Menu drawer) in `site/family/` here, once, for every site (`/family-change`); an app’s own look and features in that app’s folder, following its own `CLAUDE.md`. Home is `site/`. Family rules: `research/family-rules.md`.
3. **Never change her data:** Pokédex ticks (`pokedex/data/collection/go.json`; its test server on 8031 writes to the same file), the Library’s `library/data/`, Travels’ posts and photos, Sim World’s plan data, or her own files outside these projects. Tests run on throwaway copies; generated files (`site/js/data.js`) are rebuilt, never edited.
4. **Her rules:** British English; curly apostrophes in shown text; no made-up text (her words, an app’s own text, or a marked placeholder); no AI art, no real logos; light mode by default. For looks, **show, don’t ask**: build the options into the running page with a Try switch (bottom right, removed once she picks) and open it in the browser pane. When asking her to choose, list every option, and label your own as “my suggestion (not decided)”.
5. **Check:** the app’s own tests and, for home, `tests/check_page.js`; after a `site/family/` change, every site (`python tools/check_all.py --quick`, or `/check-all`).
6. **Commit in the app first, then record it here:** commit and push in the app, then `python tools/record_apps.py` (or `/record`) commits “Record app versions: …” in the parent and pushes. Push everywhere with the gh credential helper above; commit messages end with the Co-Authored-By line.
7. **Home changed?** Republish the private artifact (link in “Where things are”).
8. **Update the notes:** her decisions in the right `CLAUDE.md` (dated), how-things-connect changes in `ARCHITECTURE.md`, shared-code use in `site/family/README.md`.

## Her picks after the second review (21 Nov, late)

Answers in `for-jemma/review-2-21-nov.md`. All built and the Try switches removed:
- **Home:** the four places span the full width, lined up with the headings.
- **All sites:** footer line 1 “Made with HTML, CSS and JavaScript, kept on GitHub.” (family rule updated). 22 Nov, her ask: now “… HTML, CSS, JavaScript and Python, kept on GitHub.” (in `site/family/family.js`).
- **Sim World:** town-plan look on lot, Sim and household pages; “Sim World” in the sidebar purple.
- **Library:** Display shelf walnut brown (was green); big first letter kept after a quote mark; EB Garamond shrunk to WOFF2; read-only without its server. The Library’s “no green” line was removed at her ask (not a rule to keep).
- **Pokédex:** card art tinted by the first type; Lucky box stays white; tabs one row at 1280 (8.5px floor); Hide off on opening; search ignores Hide; 32px under the chips on Pokémon pages.
- **Travels:** Favourite month removed; neutral wording; distance on trip pages; writing from a phone: option 5, draft on the phone and publish from the PC (her pick; options in its `research/write-from-phone.md`).

## The family layout (21 Nov, late: her decision)

Jemma’s Journals is the **parent**; the apps are **submodules** in it: `library/`, `sim-world/`, `pokedex/`, `travels/` (their own repos on GitHub unchanged; plan and checks in `research/submodules-plan.md`). Home’s own folder is `site/` (was `concepts/`). Shared code goes in Jemma’s Journals (next job: dark mode, footer, Menu drawer, sidebar into `site/family/`, one app at a time); the apps keep their own looks.
- **Shared code (22 Nov, overnight):** `site/family/` (`mode.js`, `family.js`, `family.css`, README): dark mode, footer, Back to top, credit dots, the Menu drawer. Every site loads it from Jemma’s Journals directly (`/family/…`; home uses `family/…`), her choice. The family server keeps her dark-mode choice in `logs/family-mode.txt` and writes it into each page (`data-jj-server-mode`), so it carries between app windows with their own Chrome profiles.
- **Opening the sites:** her shortcuts run `tools/open_site.pyw <app>` (starts the family server if needed, opens the app window at 8050); the Startup folder has “Jemma's Journals server” (serve_all.py, which also starts the app servers). `tools/record_apps.py` records the apps’ new versions in the parent (the daily backup runs it: see below).
- **One address for all:** `tools/serve_all.py` (launch config `family`, http://localhost:8050): `/` home, `/library/`, `/sim-world/`, `/pokedex/`, `/travels/`; saves are passed on to each app’s own server (Library 8020, Pokédex 8030, Travels 8041), which still does the saving. Home’s Open links work there; dark mode carries.
- **Shared test tools:** Node in `.tools/node`, Playwright in `node_modules/` (both git-ignored), moved here from Sim World.
- **Re-pointed 21 Nov:** the three weekly tasks (22 Nov: replaced by one daily task, “Jemma's Journals - backup”, 09:30, running `tools/weekly.py`; the three old tasks are disabled), the desktop and Start-menu shortcuts and the Library server’s Startup shortcut now use the new folders. The old folders (`Documents\HomeLibrary`, `SimTracker`, `Pokedex`, `Travels`) are kept untouched for now (her choice); delete only with her OK.
- **After committing in an app:** commit the new version in the parent too (`git add <app>`), and push both.
- **Claude memory** for each app was copied to its new folder (21 Nov); she starts each app’s chats from its new folder. Repos renamed on GitHub to `sim-world` and `travels` (her ask); old addresses forward.

## Adding a new site (22 Nov)

- **One command:** `python -X utf8 tools/new_site.py <folder> "<Name>" ["#accent"]` (e.g. `recipes "Recipes" "#8A3B2E"`; `--dry-run` shows everything first). It copies `templates/new-site/` to `JemmasJournals/<folder>/` (filled in: “Jemma’s <Name>”, the accent checked to 4.5:1 or more in light and dark and adjusted if not), runs `git init` there with a first commit, and wires it into `tools/serve_all.py` (APPS), `tools/open_site.pyw` (SITES), `tools/build_site.py` (APPS), `tools/check_all.py` (its tests), `tests/axe_all.js`, `tools/backup_new_sites.py` (the daily backup, once it has a GitHub repo) and the parent’s `.gitignore`. Each edit is marked “added by tools/new_site.py” and safe to run twice. Restart the family server afterwards.
- **Home is not changed** unless `--add-to-home` (a new place on home is her yes; it adds a placeholder entry to PLACES in `site/home.js` with the striped stand-in picture, and `tests/check_page.js`’s “four places” checks then need updating). Without it, the line to add is printed.
- **No GitHub repo:** creating one is her decision; the script prints the `gh repo create` and `git submodule add` commands. After it is a submodule, add it to `tools/record_apps.py` APPS and the git list in `tools/check_all.py`.
- **Undo:** `python -X utf8 tools/new_site.py <folder> --remove` takes the wiring back out (exactly, also the home entry); it never deletes the folder, only prints how.
- **The template** follows the family rules out of the box (robots and CSP meta, `/family/` code, local fonts, skip link, sidebar with “← Jemma’s Journals”, Menu drawer under 900px, family footer, light by default) with a neutral look to restyle from the tokens at the top of `site/site.css`, a tiny hash router (Home, a list, item pages, Not found) and data in `site/js/data.js`, all marked Placeholder. Its `tests/check_site.js` (177 checks: errors, CSP, footer, drawer at 899/901, dark mode, 390 sideways, apostrophes, axe) passed on a throwaway site; screenshots in `for-jemma/concepts/new-site-template/`. Plain steps for her: `for-jemma/new-site.md`.
