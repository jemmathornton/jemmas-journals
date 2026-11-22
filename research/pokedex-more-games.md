# The Pokédex beyond Pokémon GO: other games and Pokémon HOME

Research and suggestions, 22 Nov 2026. Nothing in the Pokédex was changed; no code was touched. Everything below that proposes something is **my suggestion (not decided)**. Her summary, in plain words: `for-jemma/pokedex-more-games.md`.

Her ask: one site for all her Pokémon things (perhaps a game switch), other games and Pokémon HOME as well as GO, and the main page **not** covered in Pokémon.

---

## 1. Where the Pokédex stands (read from its code, 22 Nov)

- **Built for one game, with a door left open.** `DATA.game` is `"go"`; `pokedex/CLAUDE.md` “Later: other games” already says each game gets its own `data/<game>/` import, `collection/<game>.json` and its own sidebar section.
- **What is GO-only today (nearly everything):**
  - Data: `data/go/dex.json` (1,292 entries, 1,024 species; ids like `37`, `37-alolan`, `678-female`), `costumes.json`, `pictures.json`, `upcoming*.json`, `release-fixes.json`, `flag-fixes.json`; `data/events.json`, `special-backgrounds.json`, `costume-events.json`.
  - Her ticks: `data/collection/go.json` (93 KB): `have` {`d:<entry>`, `c:<costume>`, `b:<event>:<entry>`: [ticks]}, `went`, `costumes`. Ticks are the GO set: `c cm cf s l h sd pu dx gx mg mx my xl xs ss`.
  - Server: `tools/serve.py` has one fixed file (`FILE = …/collection/go.json`) and one fixed tick list (`TICKS`).
  - Page: `site/js/app.js` (1,531 lines): `GENS` (10 regions incl. Hisui), `REGION_GEN`, `BOXF`/`POSSIBLE`/`EXTRAS` (box rules: Lucky, XXL/XXS, Shadow, Dynamax, G-Max, Mega), `FORM_SPECIES`, `GMAX_SPECIES`, `UNTRADEABLE`, the routes in `drawRoute` (`#home`, `#dex`, `#gen-<g>`, `#p-<key>`, `#sets`, `#set-…`, `#fast`, `#want`, `#coming`), `navHtml`, `home()`, `statsHtml`/`fitTabs` (banner tabs), `card()`, `pokemonPage()`.
  - Build: `tools/build.py` writes one `site/js/data.js` (885 KB) with entries, costumes, events, collection.
  - Pictures: `site/sprites/` (41 MB, the game’s own GO pictures from PokeMiners), `site/regions/` (22 MB, official painted region maps), `site/backgrounds/` (3.8 MB).
- **Already game-neutral enough to reuse:** the binder look (cards, region colours, index tabs), `groupByNumber`/`groupKey` (regional forms as Pokémon of their own), the National Dex number on every entry, the region maps, the family footer/drawer/dark mode, the view-only mode, the tests’ throwaway copy.
- **Her ids are close to a game-neutral form list already:** `25`, `37-alolan`, `58-hisuian`, `678-female`, `201-…` (Unown letters), so a National Dex list can reuse the same ids and her GO ticks line up without being touched.

## 2. What “collecting” means in each game (research)

| Game | Platform / year | Its own Pokédex | What collectors track there | Goes into HOME? |
|---|---|---|---|---|
| **Pokémon GO** (now) | phone | National numbers, ~1,024 species in the game | what she has now: caught ♀/♂, shiny, lucky, 4★, XXL/XXS, Shadow/Purified, Dynamax/G-Max, Mega, costumes, backgrounds | yes, one way (GO Transporter; some costumes/forms can’t) |
| **Pokémon Legends: Z-A** | Switch / Switch 2, Oct 2025; DLC *Mega Dimension* 10 Dec 2025 | Lumiose Pokédex (232) + Hyperspace Pokédex (132, DLC) | caught, shiny, **Alpha**, **Mega** (Mega Stones/forms) | yes since HOME 4.0.0 (1–2 Apr 2026), but Z-A Pokémon can only go on to Champions, and only Lumiose-dex Pokémon can go into Z-A |
| **Pokémon Scarlet / Violet** (+ Teal Mask, Indigo Disk) | Switch, 2022–23 | Paldea (400), Kitakami (200), Blueberry (243) | caught, shiny, gender, **marks** (e.g. the raid marks), Tera raids | both ways |
| **Pokémon Legends: Arceus** | Switch, 2022 | Hisui (242) | caught, shiny, **Alpha**, **research level** (Complete / Perfect) | both ways (in from HOME limited to its dex) |
| **Brilliant Diamond / Shining Pearl** | Switch, 2021 | Sinnoh (151) + National | caught, shiny | both ways |
| **Sword / Shield** (+ Isle of Armor, Crown Tundra) | Switch, 2019–20 | Galar (400), Isle (211), Crown (210) | caught, shiny, **Gigantamax**, marks and ribbons | both ways |
| **Let’s Go Pikachu / Eevee** | Switch, 2018 | Kanto (153: 151 + Meltan, Melmetal), Alolan forms | caught, shiny; GO Park link from GO | one way into HOME |
| **FireRed / LeafGreen** (Switch release) | Switch, 2026 | Kanto | caught (completing the Kanto dex gives Celebi in HOME) | one way, since HOME 4.1.0 (6–7 Oct 2026) |
| **Pokémon Champions** | Switch Apr 2026, phone later | battles only | — (Pokémon come in from HOME; can’t go back) | takes from HOME |
| **Pokémon Winds / Waves** (Gen 10) | Switch 2, 2027 (no date) | — | not out | — |
| **Pokémon HOME** | Switch + phone | **National Pokédex** (1,025 species and their forms) + one Pokédex per connected game (since 2.0.0) | registered or not, **shiny registered separately**, forms (regional, many cosmetic, also Mega and Gigantamax when moved in), gender differences registered as a pair except shiny; completing game dexes gives shiny mythicals (Paldea + Kitakami + Blueberry → shiny Meloetta; Celebi for FRLG Kanto) | it is the place |

Notes:
- **“Registered” is not “have”.** HOME’s Pokédex fills when a Pokémon is deposited, and stays filled after it leaves; a **living dex** (one of every Pokémon kept in boxes, 30 a box) is the collectors’ other goal. Popular trackers offer both, and a shiny version of each.
- **Forms are where trackers differ.** The best-known HOME spreadsheet (Austin John’s, via PokeJungle) offers Living Dex (regional forms only), Living Form Lite (all forms, no gender differences) and Living Form (with gender differences). Pokédex Tracker (pokedextracker.com) treats HOME as “a new game type” with a normal and a shiny dex. This matches her GO choices: regional forms as Pokémon of their own, some species form by form (`FORM_SPECIES`), the rest one card.
- **Origin marks** show which game a Pokémon came from (Gen VI on, and Gen I–II; GO has its own mark). In a HOME view this could be a fact on a Pokémon, not a box.
- **Pokémon from GO** carry the GO mark in HOME; GO → HOME is one way. Her Melmetal question (Meltan/Melmetal sit under no region; HOME calls it “Unknown Origin”; her call was Alola) carries over.

## 3. Data sources usable offline

| Source | What | Terms | Use |
|---|---|---|---|
| **PokeAPI CSVs** (`github.com/PokeAPI/pokeapi`, `data/v2/csv/`) | species (1,025), forms (1,579 rows incl. Mega, G-Max), `pokemon_dex_numbers.csv` (every game’s regional dex: Lumiose 232, Hyperspace 132, Paldea 400, Kitakami 200, Blueberry 243, Hisui 242, Galar 400, Let’s Go Kanto 153, Champions 231…), `versions`/`version_groups` (up to legends-za, mega-dimension, champions), `pokemon_species_flavor_text.csv` / `pokemon_form_flavor_text.csv` (each game’s Pokédex text, word for word) | BSD-3-Clause (keep the copyright notice if the data is passed on); “Pokémon and Pokémon character names are trademarks of Nintendo”; fair use asks to cache locally (download once, as import_go.py already does for the species CSV) | **main source**: one download into `imports/`, read by a new tool. Checked 22 Nov: the CSVs already include the Z-A dexes |
| **PokeAPI sprites** (`github.com/PokeAPI/sprites`) | `other/home` (HOME’s own renders, normal/shiny/female), `other/official-artwork`, per-game sprites | the repo is CC0 but says “All image contents within are Copyright The Pokémon Company” | HOME renders are the game’s own pictures, like the GO ones she uses. **Avoid** its *shiny* official artwork (the README calls them “custom”) and the Gen 5 sprites over #650 (“not official”, Smogon-made): they break “pictures come from the games” |
| **PokeMiners pogo_assets** (now) | GO’s own pictures | game files | keep for GO; GO has pictures for almost every species, so it could also serve other games at first |
| **Serebii, Bulbapedia** | per-game availability, exclusives, HOME rules | reference only (Bulbapedia refused automated reading on 22 Nov, as Leek Duck does) | read by hand to check, cite in notes |
| **Game files / save readers** | exact per-save data | out of scope (needs dumping her console) | no |

Gap: **“obtainable in game X” is not in PokeAPI for the newer games** (its `encounters.csv` is mostly the old games). The reliable, simple measure is “**in that game’s own Pokédex**” (`pokemon_dex_numbers.csv`), which is how the games and HOME count completion anyway. For HOME, “can be deposited” ≈ every species and most forms.

## 4. Suggestions for her site

### 4.1 Navigation

Every option below is **my suggestion (not decided)**; the first in each list is the one I’d try first.

**A. How to switch game**
1. **Switch in the sidebar header** (my pick to try first): the brand stays “Jemma’s *Pokédex*”, and the small “Pokémon GO” under it becomes a quiet switch (a short list on click: Pokémon GO, Pokémon HOME, Legends: Z-A …). Choosing one redraws the sidebar for that game. Nothing else on screen grows.
2. **One binder per game in the sidebar**: each game a section with its own pages (GO: regions, Event Pokémon, Looking for, What’s on, Fast tick; Z-A: Lumiose, Hyperspace). Clear, but the sidebar gets long with three or more games.
3. **Games on Home only**: no switch; the Pokédex’s Home lists her games and each opens its own sidebar; a “← All games” link at the top of each game’s sidebar.
4. **Tabs along the top of the page** (like the banner tabs, one per game). Clutters every page; not recommended.

**B. Addresses**
1. **Old GO addresses keep working unchanged** (`#gen-1`, `#p-25`, `#fast`), and other games get a prefix: `#home/…`, `#za/…`, `#sv/…`. No bookmark breaks; GO is “the default game”.
2. **Every game prefixed** (`#go/gen-1`, `#za/lumiose`), with the old ones redirected to `#go/…` (as `#costumes` already redirects to `#sets`). Tidier, a little more work.

**C. The Pokédex’s Home page (a calm overview, not a wall of Pokémon)**
Today Home shows the ten region maps in the banner and ten region cards with three Pokémon each (30 sprites). Options:
1. **A shelf of her games**: one card per game she plays, each with its **cover** (publishers’ box art, allowed under her picture rule, as the Library’s covers) or its region map, the game’s name, and “Open Pokémon GO”. One short line of progress per card at most, or none. No Pokémon pictures on Home at all.
2. **Maps with game chips**: the ten region maps as the page’s pictures; each game a small chip under the map of its region (Z-A under Kalos, SV under Paldea, GO everywhere). Calm, but harder to read.
3. **Keep today’s Home as GO’s own front page**, and put a small “Games” page above it. Least change; GO stays busiest.
4. **Words only**, like Jemma’s Journals’ Introduction: a short list of her games, each a link. Plainest.

**D. Banner tabs and cards per game**
- The tabs are already built from a list of boxes; each game simply has its own list. GO keeps its 13; HOME might have 3 (Registered, Shiny, ♀/♂); Z-A 3–4 (Caught, Shiny, Alpha, Mega). Fewer tabs → bigger tiles; `fitTabs` copes.
- **Sections follow the game’s own Pokédexes**, not the ten regions: Z-A → Lumiose, Hyperspace; SV → Paldea, Kitakami, Blueberry; HOME → the ten regions (as GO, and as HOME’s own “region first found” sort).
- **Cards stay the collector’s cards.** Frame colour: the section’s colour (Kalos blue for Lumiose, as `REGION_COLOURS` today). The art window keeps the first-type tint. A small game mark is not needed inside a game; only on the HOME “where it lives” view.
- **GO-only pages stay in GO’s sidebar only**: Event Pokémon (costumes, backgrounds), What’s on, Looking for (its Lucky-trade tab is GO), the Shiny Shadow bonus box. **Fast tick** could work for any game (the game’s Pokédex screen side by side) — her call.

### 4.2 Data model

**Rule zero: her GO ticks are never rewritten.** `data/collection/go.json` keeps its file name, keys and ticks. New games get new files beside it. No migration, so nothing can be lost; the tests already check the ticks file is unchanged.

Suggested layout (**my suggestion, not decided**):

```
data/
  national/                     generated by a new tools/import_national.py from PokeAPI CSVs
    species.json                1,025 species: dex, names, gen, gender ratio, class
    forms.json                  every form, with ids in the Pokédex’s own style (25, 37-alolan, 678-female, 201-a …),
                                types, kind (regional / cosmetic / gender / mega / gmax / battle-only), picture keys
  go/       (unchanged)         dex.json, costumes.json … her GO data as now
  home/     game.json           which forms count, which boxes, its Pokédexes (generated + small hand-fixes file)
  za/       game.json           Lumiose / Hyperspace lists from pokemon_dex_numbers.csv; boxes Caught, Shiny, Alpha, Mega
  collection/
    go.json   (unchanged)
    home.json                   {"have": {"d:25": ["c","s"], …}}   same shape as go.json
    za.json
```

- **One id scheme for forms across games** (the GO ids extended), so “Hisuian Growlithe” is `58-hisuian` everywhere; a game file only lists ids and what is possible there.
- **Per-game box definitions** in the game file, e.g. `{"boxes": ["c","cf","cm","s","al","mg"]}`, with the same short codes where the meaning is the same (`c` caught, `s` shiny, `cf`/`cm`) and new ones only where needed (`al` Alpha, `rg` registered…). The page’s `BOXF` list becomes one list per game; GO’s stays exactly as it is.
- **GO-only features stay GO-only by living in GO’s files**: events, backgrounds, costumes, Lucky, XXL/XXS, Shadow/Purified, Dynamax are only in `data/go/` and `collection/go.json`; other games simply never load them.
- **Server** (`tools/serve.py`): one file per game from an allow-list (`go`, `home`, `za` …), the tick list checked against that game’s boxes; GO’s path and behaviour unchanged. Same lock and `.bak` per file.
- **Build**: one data file per game (`data-go.js`, `data-home.js` …) plus a small shared one, so the page loads only the game shown. Today’s `data.js` is 885 KB for GO alone; a National list with names, types and forms is about 300–400 KB more. Content Security Policy is fine (own files).
- **Pokédex text**: each game’s own entry word for word from PokeAPI’s flavour-text CSVs (her “no made-up text” rule holds). GO keeps GO’s text.

### 4.3 Pokémon HOME: three ways to have it

1. **HOME as a game of its own** (my pick to try first): its National Pokédex in the ten regions, boxes **Registered** (or “In HOME”, her word), **Shiny**, and ♀/♂ where they look different; forms as she already decided for GO (regional forms their own Pokémon, her form-by-form list, the rest one card). Simple, matches what HOME shows on her phone.
2. **HOME as the “where they live” view**: no ticks of its own; every Pokémon’s card shows small marks for the games she has it in (GO, Z-A, SV…), worked out from her ticks in each game. Good for a living-dex overview; nothing to tick twice. Can’t show what’s only in HOME.
3. **Both**: HOME with its own ticks, plus a “Where it is” line on each Pokémon’s page (GO ✓ shiny, HOME ✓, Z-A Alpha) and a filter “in GO, not in HOME yet” (useful before a GO Transporter session).

Also her choice: living dex (**has one now**) or Pokédex (**ever registered**) as the meaning of HOME’s main box — or both boxes.

### 4.4 Phased plan

| Phase | What | Effort | Needs from her |
|---|---|---|---|
| **0. Choose** | Which games she plays or wants (GO + HOME? Z-A? SV? Legends: Arceus?), and the HOME meaning | — | her list; her picks below |
| **1. A home for several games, with only GO in it** | game switch (A), addresses (B), new Home (C) shown as a Try switch; GO pages unchanged; tests prove go.json untouched | **S–M** | click through the Try options, pick |
| **2. The National list** | `tools/import_national.py` (PokeAPI CSVs into `imports/`, `data/national/`); pictures: GO’s own where they exist, HOME renders only for forms GO lacks | **M** | none (report of differences to check) |
| **3. First new game** | the one she plays most (or HOME): game file, `collection/<game>.json`, serve.py allow-list, box list, sections, banner tabs | **M** | which boxes she wants for it (listed per game in §2) |
| **4. HOME “where it lives”** | per-Pokémon line across games; “in GO not in HOME” filter | **M** | yes/no to §4.3 option 2/3 |
| **5. More games** | each further game mostly a data file | **S** each | name the game |
| **Later** | Winds/Waves (2027), Champions (nothing to collect) | — | — |

**Risks**
- **Her ticks**: kept safe by never migrating `go.json`; each game its own file; the tests’ unchanged-ticks check extended to every collection file.
- **Data size**: one data file per game keeps the page light; National list ~0.3–0.4 MB.
- **Pictures and size**: HOME renders for ~1,300 forms × normal/shiny/female at 256 px WebP ≈ 40–70 MB more in a public git repo already holding 67 MB of pictures. Start with GO’s pictures (already there) and add only what’s missing.
- **Look mismatch**: GO renders vs HOME renders differ in style; mixing them on one page may look odd — show both on a Try switch.
- **Licensing**: all Pokémon pictures are © The Pokémon Company (as now); the site is noindex/noai and mostly private. PokeAPI’s data needs its BSD notice kept (a credit line, e.g. “Pokémon data: PokeAPI”). Box art counts as publishers’ covers.
- **Her rules**: no made-up text (game names, dex names and Pokédex entries word for word from the games via PokeAPI); no AI art; icons from her sets (Alpha and Registered need icons: show options as pictures first); British English; light by default.
- **Accuracy**: “available” for new games = in that game’s Pokédex; exclusives (Scarlet vs Violet) and event-only Pokémon need hand notes from Serebii/Bulbapedia.
- **Clutter**: the sidebar is the danger; option A1 keeps it to one game at a time.

### 4.5 Choices for her (every option listed; first = my suggestion, not decided)

1. **Which games**: GO + HOME first · GO + the console game she plays now · GO + several at once · not yet.
2. **Game switch**: switch in the sidebar header · one binder per game in the sidebar · games on Home only · tabs along the top.
3. **Pokédex Home page**: shelf of game covers · maps with game chips · today’s Home as GO’s front page plus a Games page · words only.
4. **Pictures on Home**: game box art · region maps · none.
5. **HOME**: a game of its own · the “where they live” view · both.
6. **HOME’s main box means**: have it now (living dex) · ever registered · both boxes.
7. **Forms outside GO**: as in GO (regional apart, her form-by-form list, rest one card) · every form its own · regional forms only.
8. **Pictures for other games**: GO’s pictures, HOME renders only where missing · HOME renders for every non-GO game · each game’s own sprites.
9. **Fast tick**: GO only · in every game.
10. **Addresses**: GO addresses unchanged, others prefixed · every game prefixed with redirects.

### 4.6 Mock-ups she could see on a Try switch later (described, not built)

- **Row “Game switch”**: Header switch · Binders · Home only. A dummy second game (“Pokémon HOME”, marked placeholder, no ticks) so the switch has something to switch to.
- **Row “Home”**: Shelf (2–4 game cards, covers, “Open Pokémon GO”) · Maps with chips · As now + Games page · Words only. Each with no Pokémon pictures except option 3.
- **Row “HOME view”** (once the National list exists): Its own ticks · Where they live (small game marks along the card’s bottom edge, like the number) · Both.
- **Row “Pictures”** on a HOME Kanto page: GO pictures · HOME renders · mixed.
- Shown in the browser pane at 1600 (her window) and 1280; screenshots only as a record.

---

## Sources

- PokeAPI documentation, fair use: https://pokeapi.co/docs/v2
- PokeAPI code and data (BSD-3-Clause, CSVs in `data/v2/csv`): https://github.com/PokeAPI/pokeapi and https://raw.githubusercontent.com/PokeAPI/pokeapi/master/LICENSE.md (CSV counts checked 22 Nov: `pokemon_dex_numbers.csv`, `pokedexes.csv`, `version_groups.csv`, `pokemon_forms.csv`)
- PokeAPI sprites (CC0, images © The Pokémon Company; custom shiny artwork; Gen 5 >650 unofficial): https://github.com/PokeAPI/sprites and its LICENCE.txt
- Pokémon HOME official: https://home.pokemon.com/en-us/ and https://home.pokemon.com/en-us/features
- Nintendo, HOME version history (4.0.0 Legends: Z-A and Champions, 4.1.0 FireRed/LeafGreen for Switch, 3.0.0 Scarlet/Violet): https://en-americas-support.nintendo.com/app/answers/detail/a_id/49104
- VGC on HOME 4.0.0 and Z-A transfer limits: https://www.videogameschronicle.com/news/a-pokemon-home-update-is-coming-this-week-finally-adding-legends-z-a-support and https://www.videogameschronicle.com/guide/pokemon-legends-z-a-pokemon-home-compatibility-explained/
- Nintendo Life, Z-A alpha starters in HOME: https://www.nintendolife.com/news/2026/04/pokemon-home-gets-an-alpha-sized-distribution-to-celebrate-legends-z-a-compatibility
- Gematsu, Mega Dimension DLC date: https://www.gematsu.com/2025/11/pokemon-legends-z-a-dlc-mega-dimension-launches-december-10
- Serebii, Hyperspace Pokédex: https://serebii.net/legendsz-a/hyperspacepokedex.shtml
- Serebii, HOME National Pokédex: https://www.serebii.net/pokemonhome/nationalpokedex.shtml ; depositable Pokémon: https://serebii.net/pokemonhome/depositablepokemon.shtml ; GO to HOME: https://serebii.net/pokemongo/pokemonhometransfer.shtml
- Bulbapedia, Pokédex (HOME) (gender pairs, shiny separate, game dexes since 2.0.0): https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9dex_(HOME) ; origin mark: https://bulbapedia.bulbagarden.net/wiki/Origin_mark ; living Pokédex: https://bulbapedia.bulbagarden.net/wiki/Living_Pok%C3%A9dex
- Pokémon.com, HOME dex rewards: https://www.pokemon.com/uk/pokemon-news/complete-pokedexes-to-earn-shiny-enamorus-and-shiny-manaphy-in-pokemon-home ; GO to HOME and Melmetal: https://www.pokemon.com/uk/pokemon-news/connect-pokemon-go-to-pokemon-home-for-a-melmetal-that-can-gigantamax
- FireRed/LeafGreen HOME support: https://games.gg/news/pokemon-home-firered-leafgreen-release-date/ and https://serebii.net/news/2026/07-October-2026.shtml
- Pokémon Champions: https://www.videogameschronicle.com/news/pokemons-big-switch-and-mobile-battle-game-champions-finally-has-a-release-date
- Winds and Waves (Gen 10, 2027): https://wccftech.com/pokemon-presents-pokemon-winds-pokemon-waves-nintendo-switch-2-exclusive-2027/
- Trackers (ideas only): https://pokedextracker.com/blog/pokemon-home-national-dex-support ; https://pokejungle.net/2023/03/27/how-to-organize-pokemon-home-for-a-living-dex/ ; https://www.poketools.com/living-dex
