# Sim World: overnight review, 23 Nov

## What I fixed

- **Leftover code removed** (commit `c0e885b`, pushed): the old apartment-building card that nothing draws any more (and its styles), plus two small unused helpers. The page looks and works exactly the same. A new test now fails if page code is defined but never used.

Nothing else needed fixing: I found no broken behaviour.

## What needs your decision

1. **Household names cut short in family trees.** In the small cards on family trees, a relative’s “where they live” label is cut off with “…” when the name is long, e.g. “Livin’ In The City · San Myshuno”, “Sylvia & Kenny Cadberry · Newcrest”. About 70 trees have one. The full name shows when you hover. Options:
   - A. Leave as it is.
   - B. Let the label wrap onto a second line, so the cards get a bit taller.
   - C. Show only the world in the label (the household name is on hover).
   - My suggestion (not decided): B.
2. **Fountainview Penthouse (San Myshuno) has no lot size.** Its lot type is now Residential (your call, 6 Nov), so the site counts it as a lot that needs a size, and Admin lists it under “No lot size”. Options:
   - A. Tell me its size and I’ll add it.
   - B. Leave it on the Admin list for now.
3. **One-way partner links** (only reported, nothing changed). In each pair, only one Sim has the link. The site reads both ways round, so the pages show it correctly anyway:
   - Gunther Goth → Cornelia Goth (Spouse)
   - Jacques Villareal → his late wife (“Villareal mother”, Late Spouse)
   - Adekoya Darong → Imani Darong (Late Spouse)
   - Colin Sullivan → Xochitl Luna (Late Spouse)

   Options: A. leave as they are (already decided 15 Nov for three of them); B. I add the link back on the other side of each pair.
   My suggestion (not decided): A.

## What I checked and found fine

- **Every page** (1,132 of them: home, worlds, neighbourhoods, lots, households, Sims, pets, dynasties, clubs, organisations, calendars, Across the worlds, Admin, Page not found) at 1600, 1280, 1000, 901, 899 and 390 wide, in light and dark:
  - no errors
  - no page wider than the screen
  - nothing sticking out of the page or overlapping (cards, family trees, figures, crumbs)
  - no “undefined” or similar
  - no straight apostrophes
  - every page drew in under a quarter of a second
- **Contrast, labels and names** (accessibility check on 18 sample pages at every width, light and dark): no contrast below 4.5:1. The only hit was the footer buttons on one cold first load, before the shared family code had filled them in. They are filled once the page settles.
- **Keyboard:** I pressed Tab 40 times on each sample page at laptop and phone width. Every stop was on screen with a visible focus ring.
- **Pictures and links:** no broken pictures and no missing files. All links inside the site go to real pages.
- **Speed:** the site opens in 0.4 to 0.5 seconds (up to 2.7 seconds on a cold first load). Page changes take 0.25 to 0.65 seconds; Admin, Progress and Notes are the slowest.
- **Data checks** (Admin): all clear except Fountainview Penthouse (above). 1 Gallery upload to sort, 89 items on your list, 20 households with no Sims yet.
- **Tests:** all pass. 401 Python tests (1 skipped, as usual) and 118 site tests, before and after the fix.
- **Your decisions in CLAUDE.md:**
  - opens light; dark only from the button
  - town-plan look
  - purple “Sim World”
  - family footer and Menu drawer
  - percentages only on Progress
  - curly apostrophes

  Nothing contradicts them.
- **Not changed:** your plan data and your own files. Dark mode was set inside my test pages only (your button and `logs/family-mode.txt` untouched). Every save was blocked.
