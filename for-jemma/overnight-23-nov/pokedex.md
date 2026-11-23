# Pokédex: overnight review (23 Nov)

## Could I make changes?

- 22 Nov night: **no**. Your other Pokédex chat had committed 37 minutes before, so I only looked. Then the PC restarted and I was cut off.
- 23 Nov evening: **yes**. Only `logs/backup.log` was changed and the last commit (the daily backup, a4f4139) was 4 hours old. Your “My Pokédex HOME” chat is active again now, so I made the one fix below and stopped. Everything else is a note for that chat.
- Your ticks were not touched: `data/collection/go.json` md5 **315936237abf07e17aa95e8a276777dc** before and after. Every POST was blocked in my checks. `home.json` doesn’t exist yet (no HOME ticks).

## What I fixed

- **92adc84** (pushed): **every cap Pikachu is male in Pokémon HOME.** All eight cap Pikachu (Original … World, Partner) had “both” genders, so they showed a Female box and counted towards HOME’s Female total. Cap Pikachu are only ever male. The cause was that PokeAPI gives one gender rate for the whole species. `tools/import_home.py` now sets the caps to male. `data/home/dex.json` and `data.js` are rebuilt from the saved copies (nothing else changed). A new test checks the genders of HOME’s own forms (caps male, Eternal Floette female, Original Color Magearna, Dada Zarude and Chest Gimmighoul genderless). I also corrected an out-of-date code comment saying “Hide ones I have” turns on when a tab is picked.
- Tests: **114 run, all pass** (85 of 85 page tests), skipped=2 (the slow ones).
- Not recorded in the parent (as briefed).

## What needs your decision

1. **Box colours under 4.5:1 with white text.** Lucky is under 4.5:1 by your choice (3.31:1). Five more boxes are also just under:
   - Male #078E5A: 4.18:1
   - Purified #0082C5: 4.20:1
   - XXL #0E8A84: 4.21:1
   - 4★ #D14186: 4.36:1
   - Mega #C2571A: 4.49:1

   This affects the cards, the tabs and the What’s on bars (Spotlight Hour green, GO Pass blue, Raid rotation orange). Options:
   - (a) leave them as they are
   - (b) darken each a little until white reaches 4.5:1, the same way Shiny was done (my suggestion (not decided)), shown as a picture of the boxes first
   - (c) darken only the ones under 4.3 (Male, Purified, XXL)
2. **HOME’s teal (#2E6A72)** is still marked as my suggestion (not decided). Options:
   - (a) keep the teal
   - (b) choose another colour from options built into the app
3. **Alcremie’s form picker** on its HOME page shows 63 small buttons whose labels are cut to “Vanilla C…”, “Ruby Cr…”, “Matcha …”. The full name shows on hover, and the pictures differ. The cap Pikachu are cut the same way (“Original…”). Options:
   - (a) leave it
   - (b) let the labels wrap onto two lines
   - (c) show only the cream colour as the label (e.g. “Ruby Cream”), with the sweet in the hover. My suggestion (not decided): (b).

## Notes for the HOME chat (not changed)

- What’s on: long event names are cut with “…” on the calendar bars (e.g. “Deoxys (Normal, Defense, Attack, and Spe…”, “Dynamax Espurr Max Monday”), more at 1000 and 901 wide. This is probably by design for a calendar. The full name shows when the bar is opened.
- There’s no “skip to the page” link: the keyboard goes through the whole sidebar first. The new-site template has one.
- `tests/e2e/keys.test.js` still has a comment saying HOME “has only Home and Every Pokémon so far”.
- `research/pokedex-home-comparison.md` (parent) still says HOME’s figures are Placeholders. They are real now.
- Slowest first loads at 1280: Event Pokémon about 7.9 s, What’s on 7.2 s, Looking for 5.5 s. Every Pokémon is about 4 s. Moving between pages is quick: Every Pokémon 1.1 s in GO and 0.5 s in HOME, everything else under 0.15 s. I measured while other checks were running, so this may be partly the PC.

## What was fine

- 23 pages (HOME: Home, Every Pokémon, Kanto, Galar, Hisui, Charizard, Pikachu, Unown, Alcremie, Fast tick; All games; GO: Home, Every Pokémon, Kanto, Hisui, Charizard, Pikachu, Hisuian Growlithe, Fast tick, Looking for, What’s on, Event Pokémon; an unknown address) at 1600, 1280, 1000, 901, 899 and 390, light and dark:
  - no console errors
  - no missing files
  - no sideways scrolling
  - no “undefined”
  - no straight apostrophes
- **HOME shows only HOME things.** There’s no Lucky, 4★, XXL/XXS, Shadow, Purified, Dynamax, Mega, costume, background, event, Looking for or What’s on on any HOME page or in its sidebar, and no HOME page links to a GO page.
- The HOME | GO switch and All games work. All 399 links on the pages checked work, and an unknown address opens HOME’s Home.
- Search works in both games (“farfetch’d” with the curly apostrophe, “#25”, a name with no match: “Nothing here.”). The Hide switch is hidden during a search.
- “Hide ones I have” is off on opening and stays as it is when a tab is picked, in both games.
- Phone drawer at 899 and 390: Menu opens it, focus goes to this page’s link, and the HOME | GO switch and All games are inside. Switching game closes it. At 901 there’s no drawer.
- Every keyboard stop has a visible focus ring, light and dark.
- No Try-switch code is left, only the one-off clearing of its old saved choices.
