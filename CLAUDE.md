# Jemma’s Journals

The home page that links Jemma’s other sites: her Sims 4 save (`Documents\SimTracker`, “My Sim World”), her home library (`Documents\HomeLibrary`, “My Library”) and her Pokémon GO collection (`Documents\Pokedex`, “My Pokédex”). Not her Budget app. Started 19 Nov 2026. Public, but not advertised: it’s mostly for her, to reach everything from her phone or laptop. More places will be added, so the page must grow by adding one entry.

## Working rules (as for her other apps)

- **Home is a landing space only:** a name, a picture and a way in for each place, plus About me. No figures, no “latest”, no dates. It must read like a website (header, sections, footer), not a screen of app icons.
- **Never edit Jemma’s own files without asking** (Downloads, Documents, Pictures, her other projects). Copy into this project and work on the copy.
- **British English**; **curly apostrophes** in shown text.
- **No made-up text on the site:** her words, or an app’s own text word for word. Missing means a marked placeholder. Labels like “Contents” or “Open …” are fine.
- **No AI-generated art.** Pictures come from her apps (maps by 20th Century Plumbob, the games’ region maps, publishers’ covers, her own screenshots). Icons: Lucide, or the sets her apps use; never a real logo.
- **Show, don’t ask, for looks:** build each option into the page (a trial switch, bottom right, added only while she is choosing and removed after), screenshot at 1600 wide (her window) and at phone size, send them labelled. Words are fine for facts.
- **When asking her to choose, list every option** in the message (the two-button box hides choices).
- **Label suggestions** as “my suggestion (not decided)”.
- **Light mode by default** (her preference, 20 Nov): dark only when the button is pressed.
- Short, plain answers. When she’s away for hours, keep working through checks, research and small fixes in one turn.

## Her decisions so far

- Cloth-cover banner with the title on a cream label; no elastic-band stripe. **Cover colour: old gold** (#8E6520, cream trim; dark #6A4A17), her pick 20 Nov evening, replacing navy (too cool). Share picture retaken from the gold banner (img/share-preview.jpg, 1200×630, 86 KB).
- Places as photos in album corners, named “My Sim World”, “My Library”, “My Pokédex”, nothing above the names.
- Only the photo and “Open …” are links (not the whole card).
- Library’s picture: the tilted wall of her covers. Sim World and Pokédex: a full map, nothing added on top. Which ones is open: she’ll supply a Sims picture; for Pokédex she’d like the combined Johto and Kanto painting (official HeartGold/SoulSilver art, PidgiWiki `File:Johto_and_Kanto_-_Pokemon_HeartGold_and_SoulSilver.jpg`; not on her PC yet).
- No “Elsewhere” links (the Sims Gallery belongs in Sim World).
- 20 Nov: the Improved version (gold corner brackets on the cover, serif section headings with a diamond rule, About photo in album corners, centred footer, Back to top), with About this site laid out across the footer. Not wanted: quick links, an empty slot, an edition mark.
- 20 Nov (later): links say “Open My Sim World” etc. (she found “Open Sim World” odd beside “My Sim World”). About this site must be small and subtle (she hated the table-like band). A way back home in each app: **A**, a small “← Jemma’s Journals” link at the top of each app’s sidebar (subtle). **Added 20 Nov evening** (her go-ahead) to all three apps (Sim World 1201ff9, Library f852f84, Pokédex f7d00a3): href "/" (home once all sites share one address; she leans to her own domain, hosting undecided, separate repos, no submodules). Sim World opened as a local file points at ../../JemmasJournals/concepts/index.html instead. Screens: for-jemma/concepts/back-home/back-home-added.jpg.

- 20 Nov (evening): **About this site = option 2**, two lines (No cookies… / the credits), each credit with a capital; on phones the credits stack one per line. The other footer options are gone from the switch.
- 20 Nov (evening): Pokédex picture = the combined Johto and Kanto painting (downloaded from PidgiWiki with her OK; page copies img/maps/region-johto-kanto.*). Shown whole for now; whole vs fill the photo is her choice.
- 20 Nov (evening): **keep out of search engines and AI crawlers**: robots meta (noindex, noai, noimageai) on the pages and concepts/robots.txt. Going online: later.
- 20 Nov (evening): page ideas: **stitching on the cover, yes** (always on now); **paper and tilted photos, no** (removed). Bookmark ribbon (as a link): no, removed. Title on scroll: no, removed. Red ribbon: removed (her pick). **Gentle entrance: yes** (plays once as the page opens; skipped for reduced motion). The Ideas row is gone from the switch.
- 20 Nov (evening): pictures parked again: she will change them later (Pokédex whole-vs-fill not decided).
- 20 Nov (evening): dark mode: opens light; moon button switches and is remembered. Dark **swaps colours consistently** (her ask): page and title label the same warm black (#29221B), photo mats deeper warm black (#0D0A07) so photos stand out, photo corners cream.
- 20 Nov (evening): **tab icon is her own design**, drawn in `concepts/tools/draw-icon.html` (redrawn simpler 20 Nov late): cream square, old gold book outline, warm black upright J in front with a cream gap, old gold slanted J just lower right; no corners. **Light icon is the default**; in dark mode the page swaps to a flipped version (img/icon/icon-dark-*: warm black square, cream J, bright gold book and slanted J), her rule 20 Nov. Files in `concepts/img/icon/` and `concepts/favicon.ico`, linked from the page. For looks she can’t describe, offer her that canvas rather than more guesses.

## Where things are

- `concepts/index.html`: the page as it stands; the trial switch was removed 20 Nov late (her ask). Stand-in places for checking growth: add `#more1`…`#more3` to the address. The places are one list, `PLACES`, in its script. Published for her phone as a private Claude artifact: https://claude.ai/artifact/Ad37As365K3HDcR8iHw7HE (republish after changes).
- `concepts/img/`: pictures copied from her apps (`maps/` every Sims world and Pokémon region map, `wall/` 40 of her covers, `icons/` each app’s own icon). `concepts/fonts/`: Instrument Serif and Manrope (SIL OFL).
- `for-jemma/concepts/`: screenshots of each round and the labelled choice sheets (older rounds in `round-1/` …).
- `research/going-online.md`: hosting research (GitHub Pages and what each app needs, checked in each app’s code).
- `research/site-ideas.md`: ideas to make the site better, what was tried on the page, a checklist for going online. `research/drafts/`: draft head tags, robots.txt, manifest and a publishing workflow (none in use until she decides).
- `concepts/404.html` (not-found page) and `concepts/img/share-preview.jpg` (link preview picture), for when it’s online. Pictures on the page are WebP at the size shown (`img/wall/*.webp`, `img/maps/*.webp`); the JPGs are the larger originals.
- `tests/check_page.js`: checks the page in Edge at 1600, 1280 and 390 wide (run with `C:/Users/Jemma/Documents/SimTracker/.tools/node/node.exe tests/check_page.js`; uses Sim World’s Playwright). Run after every change.

## Git

Repo on `main`, pushed to https://github.com/jemmathornton/jemmas-journals (**public**). Commit after each piece of work and push with `git -c "credential.helper=!'C:/Program Files/GitHub CLI/gh.exe' auth git-credential" push`. Name and email are set in this repo’s own git config (copied from her Library project).
