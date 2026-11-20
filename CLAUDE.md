# Jemma’s Journals

The home page that links Jemma’s other sites: her Sims 4 save (`Documents\SimTracker`, “My Sim World”), her home library (`Documents\HomeLibrary`, “My Library”) and her Pokémon GO collection (`Documents\Pokedex`, “My Pokédex”). Not her Budget app. Started 19 Nov 2026. Public, but not advertised: it’s mostly for her, to reach everything from her phone or laptop. More places will be added, so the page must grow by adding one entry.

## Working rules (as for her other apps)

- **Home is a landing space only:** a name, a picture and a way in for each place, plus About me. No figures, no “latest”, no dates. It must read like a website (header, sections, footer), not a screen of app icons.
- **Never edit Jemma’s own files without asking** (Downloads, Documents, Pictures, her other projects). Copy into this project and work on the copy.
- **British English**; **curly apostrophes** in shown text.
- **No made-up text on the site:** her words, or an app’s own text word for word. Missing means a marked placeholder. Labels like “Contents” or “Open …” are fine.
- **No AI-generated art.** Pictures come from her apps (maps by 20th Century Plumbob, the games’ region maps, publishers’ covers, her own screenshots). Icons: Lucide, or the sets her apps use; never a real logo.
- **Show, don’t ask, for looks:** build each option into the page behind the bottom-right switch, screenshot at 1600 wide (her window) and at phone size, send them labelled. Words are fine for facts.
- **When asking her to choose, list every option** in the message (the two-button box hides choices).
- **Label suggestions** as “my suggestion (not decided)”.
- **Light mode by default** (her preference, 20 Nov): dark only when the button is pressed.
- Short, plain answers. When she’s away for hours, keep working through checks, research and small fixes in one turn.

## Her decisions so far

- Navy cloth-cover banner with the title on a cream label; no elastic-band stripe.
- Places as photos in album corners, named “My Sim World”, “My Library”, “My Pokédex”, nothing above the names.
- Only the photo and “Open …” are links (not the whole card).
- Library’s picture: the tilted wall of her covers. Sim World and Pokédex: a full map, nothing added on top. Which ones is open: she’ll supply a Sims picture; for Pokédex she’d like the combined Johto and Kanto painting (official HeartGold/SoulSilver art, PidgiWiki `File:Johto_and_Kanto_-_Pokemon_HeartGold_and_SoulSilver.jpg`; not on her PC yet).
- No “Elsewhere” links (the Sims Gallery belongs in Sim World).
- 20 Nov: the Improved version (gold corner brackets on the cover, serif section headings with a diamond rule, About photo in album corners, centred footer, Back to top), with About this site laid out across the footer. Not wanted: quick links, an empty slot, an edition mark.

## Where things are

- `concepts/index.html`: the page as it stands, with the trial switch (bottom right) and “+ More places”. The places are one list, `PLACES`, in its script. Published for her phone as a private Claude artifact: https://claude.ai/artifact/Ad37As365K3HDcR8iHw7HE (republish after changes).
- `concepts/img/`: pictures copied from her apps (`maps/` every Sims world and Pokémon region map, `wall/` 40 of her covers, `icons/` each app’s own icon). `concepts/fonts/`: Instrument Serif and Manrope (SIL OFL).
- `for-jemma/concepts/`: screenshots of each round and the labelled choice sheets (older rounds in `round-1/` …).
- `research/going-online.md`: hosting research (GitHub Pages and what each app needs, checked in each app’s code).
- `research/site-ideas.md`: ideas to make the site better, what was tried on the page, a checklist for going online. `research/drafts/`: draft head tags, robots.txt, manifest and a publishing workflow (none in use until she decides).
- `concepts/404.html` (not-found page) and `concepts/img/share-preview.png` (link preview picture), for when it’s online. Pictures on the page are WebP at the size shown (`img/wall/*.webp`, `img/maps/*.webp`); the JPGs are the larger originals.
- `tests/check_page.js`: checks the page in Edge at 1600, 1280 and 390 wide (run with `C:/Users/Jemma/Documents/SimTracker/.tools/node/node.exe tests/check_page.js`; uses Sim World’s Playwright). Run after every change.

## Git

Repo on `main`, pushed to https://github.com/jemmathornton/jemmas-journals (**public**). Commit after each piece of work and push with `git -c "credential.helper=!'C:/Program Files/GitHub CLI/gh.exe' auth git-credential" push`. Name and email are set in this repo’s own git config (copied from her Library project).
