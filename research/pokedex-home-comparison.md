# A game’s Home page in the Pokédex: how others lay it out (22 Nov 2026)

> **Update, 23 Nov:** Pokémon HOME has since been fully built (Pokédex commits 1f24481 and a29b361), so HOME’s figures are real now. Where this note says HOME’s figures are Placeholders, that describes the options as they stood on 22 Nov.

Short comparison for Jemma’s Pokédex, after her picks on 22 Nov: the game switch in the sidebar (HOME | GO), Pokémon HOME the default game, and the Home page still open. Her later note: “maybe there needs to be something overview between games but every mon is game specific so seems weird for them to be together.” Everything that proposes something here is **my suggestion (not decided)**. Background: `research/pokedex-more-games.md`.

## What the sites and apps do

| Where | How a game’s overview is laid out | Across games? |
|---|---|---|
| **Serebii, Pokémon GO section** (`serebii.net/pokemongo/pokemon.shtml`) | A short intro, then a grid of image tiles, one per region (Kanto … Paldea, plus Unknown, Hisui, Mega), each tile named with its National Pokédex range (“Kanto #001-151”) and linking to that region’s page. No Pokémon on the hub itself. | No: each game is its own section of the site; the Pokédex Hub is a separate page of links. |
| **Serebii, Pokémon HOME section** (`serebii.net/pokemonhome/`) | A title and a few paragraphs, then labelled blocks: Game Sections (a bulleted list of the section’s pages), Details, release date. | Supported games are named in the text, each linked to its own section. |
| **PokémonDB** (`pokemondb.net/pokedex/game/scarlet-violet`, `/pokedex/national`) | One page per game’s Pokédex: a title, an intro, links to the DLC dexes, then every Pokémon in order (picture, number, name, types). The National list is grouped by generation with a “Jump to” row and a heading per generation. | Separate pages per game; no combined view. |
| **Pokémon HOME (the app)** | One National Pokédex that fills as games are connected; it can be sorted, shows shiny forms and **the games each Pokémon was found in**. Since version 2.0.0 there is also a Pokédex for each connected game, and completion is confirmed in HOME’s **Games tab** (rewards such as shiny Meloetta for the Scarlet/Violet dexes). Pokémon are kept in **boxes of 30**. | Yes, in two ways: the National Pokédex says which games a Pokémon was found in, and the Games tab lists each game’s dex completion. |
| **PokéTools living dex** (`poketools.com/living-dex`) | “Marked 0 of 1,025” with a percentage at the top, Show All / Missing / Marked, then a “By generation” panel: a row per generation with its own count (0/151 …). Separate tabs for Shiny hunts. | No: one living dex; shiny is a separate list. |
| **Pokédex Tracker** (`pokedextracker.com`) | Each dex a “game type” of its own (HOME counts as one); a normal and a shiny dex; search by name or number; boxes of 30 like the games. | A user’s page lists their dexes one under another, each with its own progress; Pokémon are never mixed between dexes. |

Sources (read 22 Nov): the pages named above; Serebii’s HOME features page (`serebii.net/pokemonhome/features.shtml`); the pokemon.com news item on HOME 3.0.0 and shiny Meloetta; Pokédex Tracker’s blog post on HOME support. Bulbapedia refused automated reading again.

## What this means for her Pokédex

- **Every site keeps Pokémon inside one game.** None mixes two games’ Pokémon in one list; this matches her point that every Pokémon is game-specific. The switch (HOME | GO) does exactly that.
- **Across games, the trackers show only totals:** HOME’s Games tab (each game’s dex completion) and Pokédex Tracker’s list of a person’s dexes. Neither shows Pokémon there. So an overview above the games should be a short page of each game’s progress side by side, with “Open …”, and no Pokémon lists.
- **A game’s own Home is usually one of three shapes:** a hub of region tiles (Serebii), a progress panel (living-dex trackers), or boxes of 30 (HOME and the trackers). All three avoid covering the page in Pokémon.

## The ideas, as Try switch options (built 22 Nov)

Row **Home page** (for GO’s Home, `#go`, and HOME’s, `#home`; HOME shows the same layout with every figure a marked Placeholder):
1. **As now**: GO keeps today’s Home; HOME the plain Placeholder.
2. **Region hub** (Serebii): a tile per region with its map, name, National Pokédex numbers (“#0001–#0151”) and her count; a tile opens the region.
3. **Progress panel** (PokéTools): Every Pokémon’s total and bar at the top, then a row per region (name, its games, a bar, the count).
4. **Box view** (HOME’s boxes of 30, as Pokédex Tracker shows a living dex): the National Pokédex in 35 boxes, each number a dot (filled = got; dashed = not in that game), with the box’s numbers and count. Fits HOME’s main box (“you have it in HOME now”) best, as HOME stores Pokémon in boxes.

Row **All games page** (her note about an overview between games; HOME’s Games tab and Pokédex Tracker’s list of dexes):
1. **None**.
2. **Link above the switch**: a small “All games” link in the sidebar above HOME | GO, opening a page with each game’s totals side by side (GO: Pokémon, Shiny, Lucky, 4★; HOME: Placeholder) and “Open …”.
3. **A third choice in the switch**: All | HOME | GO, the same page.

The page never lists Pokémon, so the games stay apart.

## What Pokémon HOME has and tracks (read 22 Nov 2026)

Her note: “For home do research online for what's available. Thing like lucky aren't a thing there. Most mon are available for it though.”

**Which Pokémon can be kept in HOME**
- **Nearly the whole National Pokédex.** Serebii’s list of depositable Pokémon runs in boxes of 30 from #0001 Bulbasaur to **#1025 Pecharunt** (47 standard boxes, with regional forms, female forms, Unown letters, Vivillon patterns, Furfrou trims, Flabébé colours, Pumpkaboo sizes and the other kept forms). Serebii notes “not all forms and Pokémon can be displayed”.
- **Shiny exceptions** (Serebii’s Shiny boxes): marked “(Not Available)”: the cap Pikachu (Original, Hoenn, Sinnoh, Unova, Kalos, Alola, World), Victini and Battle Bond Greninja; Serebii: if a Pokémon isn’t shown there, “it currently cannot be obtained as Shiny”.
- **From GO** (Serebii, GO → HOME): one way only. **Cannot be sent:** Mega Evolved and Shadow Pokémon, Gigantamax-capable ones, Pokémon caught in GO Safari Balls, Hyper Trained ones, some costumes and forms (Serebii doesn’t list which), and these species/forms: Armored Mewtwo, Spinda, Origin Dialga and Palkia, Black and White Kyurem, every Zygarde form, Dusk Mane and Dawn Wings Necrozma, Crowned Zacian and Zamazenta, Eternatus. **Forms that change on arrival:** Castform’s weather forms → Normal, Sunshine Cherrim → Overcast, Origin Giratina → Altered, Zen Mode Darmanitan → Standard, Resolute Keldeo → Ordinary, Pirouette Meloetta → Aria, Genesect’s Drives → Normal.
- **Room** (Nintendo support): Basic plan 30 Pokémon in one box; Premium plan 6,000 in 200 boxes of 30. A living dex needs Premium.

**What HOME’s Pokédex records**
- One **National Pokédex**, filled when Pokémon are deposited in HOME’s boxes (official features page); it stays filled after a Pokémon leaves, so the Pokédex is “ever registered”, while her chosen meaning, “have it in HOME now”, is about the boxes (a living dex).
- **Forms:** each form has its entry; Mega Evolution and Gigantamax forms are registered too (official page; Serebii: Gigantamax only if you have that one, battle-only forms once seen). Since 2.0.0 there is also a **Pokédex per connected game**, with completion rewards (shiny Manaphy for Sinnoh, shiny Meltan for Kanto, shiny Meloetta for Paldea, Kitakami and Blueberry; pokemon.com).
- **Shiny and gender** (Bulbapedia, via search: the page refuses automated reading): depositing a Pokémon with a gender difference registers both genders, except a shiny, which registers only its own gender; a shiny registers both the shiny and the normal entry.
- **Each entry** shows its forms, its data and the games it is found in; it can be sorted and shown shiny (Serebii’s features page).

**GO’s boxes that are not in HOME at all:** Lucky, 4★ (appraisal), XXL / XXS, Shadow and Purified (Shadow can’t be sent; HOME has no Purified box), Dynamax and Gigantamax as GO uses them (Gigantamax-capable GO Pokémon can’t be sent), Mega (can’t be sent Mega Evolved), costumes and location backgrounds. These stay GO-only.

**HOME’s ticks — my suggestion (not decided):** **Caught** (her “have it in HOME now”) and **Shiny**, on every Pokémon and form HOME keeps (regional forms as Pokémon of their own, her form-by-form list, as in GO); **Female / Male** only where the two look different, as HOME registers them; no Lucky, 4★, XXL/XXS, Shadow, Purified, Dynamax or Mega. Possibly later: Gigantamax and Mega as forms seen in HOME’s Pokédex, and the per-game Pokédexes; her call.

Sources (read 22 Nov 2026): Serebii, [Depositable Pokémon](https://serebii.net/pokemonhome/depositablepokemon.shtml), [National Pokédex](https://serebii.net/pokemonhome/nationalpokedex.shtml), [Features](https://serebii.net/pokemonhome/features.shtml), [Pokémon GO to HOME](https://serebii.net/pokemongo/pokemonhometransfer.shtml); [Pokémon HOME features (official)](https://home.pokemon.com/en-us/features); Nintendo support, [Basic and Premium plans](https://en-americas-support.nintendo.com/app/answers/detail/a_id/48800); pokemon.com news on [shiny Meloetta](https://www.pokemon.com/us/pokemon-news/a-new-pokemon-home-update-and-an-opportunity-to-earn-a-shiny-meloetta) and [shiny Keldeo and Meltan](https://pokemon.com/us/pokemon-news/complete-pokedexes-to-earn-shiny-keldeo-and-shiny-meltan-in-pokemon-home); [Bulbapedia, Pokédex (HOME)](https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9dex_(HOME)) (search snippet only).

**Changed on the HOME side (22 Nov):** the All games page’s HOME card shows only Pokémon and Shiny (each a Placeholder); HOME’s Home-page ideas never mention Lucky, 4★ or the other GO-only boxes (checked in the tests). No HOME data was made.
